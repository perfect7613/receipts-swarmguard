"""Entire evidence capture and an authenticated cfo.ai MCP bridge."""

import json
import os
from pathlib import Path
import subprocess

import httpx


def capture_entire(root: Path, output: Path) -> dict:
    """Collect actual installed-command output. Never invent provenance IDs."""
    output.mkdir(parents=True, exist_ok=True)
    commands = {
        "version": ["entire", "version"],
        "status": ["entire", "status"],
        "graph_search": ["entire", "graph", "search", "--repo", str(root), "--profile", "full",
                         "--query", "trusted verification and dependent claim recovery", "--format", "json"],
        "graph_impact": ["entire", "graph", "impact", "--repo", str(root), "--symbol", "verify"],
        "checkpoints": ["entire", "checkpoint", "list", "--json"],
    }
    records = {}
    for name, command in commands.items():
        try:
            result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=45)
            (output / (name + ".txt")).write_text(result.stdout)
            records[name] = {"exit_code": result.returncode, "path": str(output / (name + ".txt"))}
        except (OSError, subprocess.TimeoutExpired):
            records[name] = {"exit_code": None, "status": "unavailable"}
    (output / "manifest.json").write_text(json.dumps(records, indent=2) + "\n")
    return records


class CFOClient:
    """Minimal Streamable HTTP MCP client; requires a valid authenticated token.

    Prefer `codex mcp add/login` for interactive OAuth. This client is for an
    already-authorized token injected by an operator. It does not implement or
    bypass browser consent, nor reuse the neatlogs project key.
    """

    def __init__(self, token: str | None = None, client: httpx.Client | None = None):
        token = token or os.environ.get("CFO_AI_ACCESS_TOKEN")
        if not token:
            raise ValueError("cfo.ai requires authenticated access; use Codex MCP OAuth or CFO_AI_ACCESS_TOKEN")
        self.client = client or httpx.Client(timeout=60)
        self.headers = {"Authorization": "Bearer " + token,
                        "Accept": "application/json, text/event-stream",
                        "Content-Type": "application/json"}
        self.session = None
        self.counter = 0
        self.initialized = False

    def _request(self, method, params, notification=False):
        self.counter += 1
        body = {"jsonrpc": "2.0", "method": method, "params": params}
        if not notification:
            body["id"] = self.counter
        response = self.client.post("https://api.cfo.ai/mcp", headers=self.headers, json=body)
        if response.status_code >= 400:
            raise ValueError(f"cfo.ai MCP request refused (HTTP {response.status_code})")
        if response.headers.get("mcp-session-id"):
            self.headers["Mcp-Session-Id"] = response.headers["mcp-session-id"]
        if notification:
            return {}
        if "text/event-stream" in response.headers.get("content-type", ""):
            packets = [json.loads(line[5:].strip()) for line in response.text.splitlines() if line.startswith("data:")]
            packet = next((p for p in packets if p.get("id") == self.counter), None)
            if packet is None:
                raise ValueError("MCP stream did not contain the matching response")
        else:
            packet = response.json()
        if "error" in packet:
            raise ValueError(f"cfo.ai MCP error ({packet['error'].get('code', 'unknown')})")
        if packet.get("id") != self.counter:
            raise ValueError("MCP response ID mismatch")
        return packet["result"]

    def initialize(self):
        if not self.initialized:
            result = self._request("initialize", {
                "protocolVersion": "2025-03-26", "capabilities": {},
                "clientInfo": {"name": "receipts-swarmguard", "version": "0.1.0"}})
            self.headers["MCP-Protocol-Version"] = result["protocolVersion"]
            self._request("notifications/initialized", {}, notification=True)
            self.initialized = True

    def tools(self) -> list[dict]:
        self.initialize()
        tools, cursor = [], None
        for _ in range(20):
            result = self._request("tools/list", {"cursor": cursor} if cursor else {})
            tools.extend(result.get("tools", []))
            cursor = result.get("nextCursor")
            if not cursor:
                return tools
        raise ValueError("Tool discovery exceeded pagination limit")

    def call(self, name: str, arguments: dict):
        published = {tool["name"] for tool in self.tools()}
        if name not in published:
            raise ValueError("Tool not published by the authenticated cfo.ai server")
        return self._request("tools/call", {"name": name, "arguments": arguments})

    def close(self):
        self.client.close()


def cfo_bridge(runs: list[dict]) -> dict:
    if len({r["track"] for r in runs}) > 1:
        raise ValueError("Export each experiment track separately; do not pool controlled and live outcomes")
    arms = {}
    for arm in sorted({r["arm"] for r in runs}):
        group = [r for r in runs if r["arm"] == arm]
        correct = sum(r["correct_completion"] for r in group)
        known = [r["usage"].get("model_cost_usd") for r in group]
        costs_complete = all(r["usage"].get("cost_complete", False) for r in group)
        total_model = sum(known) if all(x is not None for x in known) else None
        arms[arm] = {"attempts": len(group), "correct_completions": correct,
                     "unsafe_accepted": sum(r["unsafe_accepted"] for r in group),
                     "model_spend_usd": total_model, "cost_complete": costs_complete,
                     "cost_per_correct_task": None,  # total infrastructure cost is not measured
                     "model_cost_per_correct_task": total_model / correct if correct and total_model is not None else None,
                     "tracks": sorted({r["track"] for r in group}),
                     "sum_task_seconds": sum(r["wall_seconds"] for r in group)}
    return {"schema_version": "receipts.cfo-bridge/v1", "native_cfo_model_created": False,
            "currency": "USD", "forecast_start": "2026-11-01", "forecast_months": 12,
            "observations": arms,
            "assumptions_pending": ["platform_fee", "included_tasks", "overage_price", "customers",
                                    "growth", "churn", "hosting", "support", "payroll", "opening_cash"],
            "notes": ["Controlled replay is not a natural model-behavior benchmark",
                      "Zero fixture inference spend is not zero product cost",
                      "Do not combine tracks into a natural cheat rate",
                      "Use docs/CFO-MODEL.md for the native model and Ari prompt"]}
