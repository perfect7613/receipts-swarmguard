"""Small role adapters. Models propose source and claims, never trusted verdicts."""

from dataclasses import dataclass, asdict
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Literal
from .telemetry import Telemetry

from pydantic import BaseModel, ConfigDict, Field


class Reply(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: str = Field(max_length=16384)
    statement: str = Field(max_length=4000)
    evidence_ids: list[str] = Field(max_length=32)
    approved: bool


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    calls: int = 0
    model_cost_usd: float | None = None
    cost_complete: bool = False

    def export(self):
        return asdict(self)


LANGUAGE = (
    "Use exactly one plain Python function with the supplied name/arguments. "
    "Supported: assignments, if/else, bounded for loops, return, dict/list literals, "
    "subscript, comparisons, boolean expressions, integer + - * // %, and calls "
    "len/list/dict/str/min/max, dict.get, list.append. No imports, type annotations, "
    "comprehensions, generators, exceptions, helper functions, file/network access, "
    "slicing, f-strings or keyword arguments. Candidate code is interpreted, not executed."
)


class ModelAgent:
    def __init__(self, backend: Literal["openai", "codex"], telemetry=None):
        self.backend = backend
        self.telemetry = telemetry or Telemetry()
        self.usage = Usage()
        self.sessions: list[str] = []
        self.model = os.environ.get("RECEIPTS_MODEL")
        if backend == "openai":
            from openai import OpenAI
            if not os.environ.get("OPENAI_API_KEY") or not self.model:
                raise ValueError("Live OpenAI mode requires OPENAI_API_KEY and RECEIPTS_MODEL")
            self.client = OpenAI(timeout=90, max_retries=0)
            if telemetry and telemetry.enabled:
                import neatlogs
                self.client = neatlogs.wrap(self.client)

    def ask(self, role: str, task: dict) -> Reply:
        system = (
            f"You are the {role} in a coding-agent workflow. Follow the task contract. "
            "Return the structured reply. For a builder/repair role provide complete source. "
            "For a reviewer/tester/auditor keep source empty and assess the supplied artifact. "
            "Cite only evidence IDs supplied to you. Never claim hidden tests ran. " + LANGUAGE
        )
        user = json.dumps(task, sort_keys=True)
        self.usage.calls += 1
        if self.backend == "openai":
            try:
                response = self.client.chat.completions.parse(
                    model=self.model, messages=[{"role": "system", "content": system},
                                                {"role": "user", "content": user}],
                    response_format=Reply)
            except Exception as exc:
                raise ValueError(f"Model request failed ({type(exc).__name__})") from None
            if response.usage:
                u = response.usage
                self.usage.input_tokens += u.prompt_tokens
                self.usage.output_tokens += u.completion_tokens
                self.usage.cached_tokens += getattr(u.prompt_tokens_details, "cached_tokens", 0) or 0
            message = response.choices[0].message
            if message.parsed is None:
                raise ValueError("Model refused or returned no valid structured reply")
            reply = message.parsed
        else:
            before_input, before_output = self.usage.input_tokens, self.usage.output_tokens
            with self.telemetry.span("codex.inference", "LLM", role=role) as span:
                reply = self._codex(system + "\nTASK JSON:\n" + user)
                if span is not None:
                    prompt_tokens = self.usage.input_tokens - before_input
                    output_tokens = self.usage.output_tokens - before_output
                    span.set_attribute("neatlogs.llm.token_count.prompt", prompt_tokens)
                    span.set_attribute("neatlogs.llm.token_count.completion", output_tokens)
                    span.set_attribute("neatlogs.llm.token_count.total", prompt_tokens + output_tokens)
                    span.set_attribute("neatlogs.llm.model_name", self.model or "codex-cli-default")
                    span.set_attribute("input.value", json.dumps({"role": role, "task": task})[:4000])
                    span.set_attribute("output.value", json.dumps({"statement": reply.statement, "approved": reply.approved})[:1500])
        self._price()
        return reply

    def _codex(self, prompt: str) -> Reply:
        # The CLI reads its own existing auth. Do not pass application API keys.
        allowed_env = ("PATH", "HOME", "USER", "TMPDIR", "CODEX_HOME", "SYSTEMROOT", "LANG")
        env = {key: os.environ[key] for key in allowed_env if key in os.environ}
        with tempfile.TemporaryDirectory(prefix="receipts-role-") as directory:
            root = Path(directory)
            schema = root / "schema.json"
            output = root / "reply.json"
            schema.write_text(json.dumps(Reply.model_json_schema()))
            command = ["codex", "exec", "--ignore-user-config", "--skip-git-repo-check",
                       "--sandbox", "read-only", "--json", "--cd", directory,
                       "--output-schema", str(schema), "--output-last-message", str(output), "-"]
            if self.model:
                command[2:2] = ["--model", self.model]
            try:
                result = subprocess.run(command, input=prompt, capture_output=True, text=True,
                                        env=env, timeout=180)
            except subprocess.TimeoutExpired:
                raise ValueError("Codex role timed out") from None
            for line in result.stdout.splitlines():
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if event.get("type") == "thread.started":
                    self.sessions.append(event["thread_id"])
                if event.get("type") == "turn.completed":
                    usage = event.get("usage", {})
                    self.usage.input_tokens += usage.get("input_tokens", 0)
                    self.usage.output_tokens += usage.get("output_tokens", 0)
                    self.usage.cached_tokens += usage.get("cached_input_tokens", 0)
            if result.returncode or not output.exists():
                raise ValueError("Codex role failed; verify local Codex auth/model availability")
            return Reply.model_validate_json(output.read_text())

    def _price(self):
        # Cached-token pricing is provider-specific; report unknown rather than overclaim.
        rates = (os.environ.get("RECEIPTS_INPUT_USD_PER_MILLION"),
                 os.environ.get("RECEIPTS_OUTPUT_USD_PER_MILLION"))
        if all(rates) and self.usage.cached_tokens == 0:
            self.usage.model_cost_usd = (
                self.usage.input_tokens * float(rates[0]) + self.usage.output_tokens * float(rates[1])) / 1e6
        self.usage.cost_complete = False  # tool/verifier infrastructure is not yet priced
