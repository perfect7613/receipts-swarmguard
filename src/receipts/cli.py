"""Small command-line surface; no credentials in command output."""

import argparse
import json
from pathlib import Path
import sys

from .agents import ModelAgent
from .controller import Controller, save_run
from .sponsors import CFOClient, capture_entire, cfo_bridge
from .telemetry import Telemetry, load_env


def main(argv=None):
    parser = argparse.ArgumentParser(description="Receipts SwarmGuard: independent evidence for agent teams")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Run a controlled or live task and bounded repair")
    run.add_argument("--fixture", choices=("payment", "discount"), default="payment")
    run.add_argument("--scenario", choices=("shortcut", "clean", "misleading", "collusion"), default="shortcut")
    run.add_argument("--arm", choices=("standard", "always-audit", "receipts"), default="receipts")
    run.add_argument("--backend", choices=("scripted", "openai", "codex"), default="scripted")
    run.add_argument("--max-repairs", type=int, default=2)
    run.add_argument("--seed-shortcut", action="store_true", help="Use a controlled faulty candidate with live review/repair")
    run.add_argument("--neatlogs", action="store_true")
    run.add_argument("--output", type=Path, default=Path("artifacts/runs"))
    demo = sub.add_parser("demo", help="Run the paired controlled failure and clean-control matrix")
    demo.add_argument("--neatlogs", action="store_true")
    demo.add_argument("--output", type=Path, default=Path("artifacts/demo"))
    entire = sub.add_parser("entire", help="Save actual Entire/Graph evidence")
    entire.add_argument("--output", type=Path, default=Path("artifacts/entire"))
    cfo = sub.add_parser("cfo", help="Discover or call authenticated cfo.ai MCP tools")
    cfo.add_argument("action", choices=("tools", "call"))
    cfo.add_argument("--tool")
    cfo.add_argument("--args", type=Path)
    cfo.add_argument("--execute", action="store_true", help="Actually invoke the supplied tool; otherwise preview")
    args = parser.parse_args(argv)
    load_env()
    try:
        if args.command == "entire":
            print(json.dumps(capture_entire(Path.cwd(), args.output), indent=2))
            return 0
        if args.command == "cfo":
            if args.action == "call":
                if not args.tool or not args.args:
                    parser.error("cfo call requires --tool and --args")
                arguments = json.loads(args.args.read_text())
                if not args.execute:
                    print(json.dumps({"preview": True, "tool": args.tool, "arguments": arguments}, indent=2))
                    return 0
            client = CFOClient()
            try:
                result = client.tools() if args.action == "tools" else client.call(args.tool, arguments)
                print(json.dumps(result, indent=2))
            finally:
                client.close()
            return 0
        telemetry = Telemetry(args.neatlogs)
        try:
            if args.command == "run":
                agent = None if args.backend == "scripted" else ModelAgent(args.backend, telemetry)
                result = Controller(telemetry, agent).run(args.fixture, args.scenario, args.arm, args.max_repairs,
                                                           args.seed_shortcut)
                directory = save_run(result, args.output)
                print(json.dumps({"run_id": result["run_id"], "track": result["track"],
                                  "status": result["status"], "accepted": result["accepted"],
                                  "oracle_passed": result["oracle_passed"], "repair_attempts": result["repair_attempts"],
                                  "trace_ids": result["trace_ids"], "evidence_path": str(directory)}, indent=2))
                return 0 if result["correct_completion"] else 2
            runs = []
            for fixture in ("payment", "discount"):
                for scenario in ("shortcut", "clean"):
                    for arm in ("standard", "always-audit", "receipts"):
                        # Each controller starts with fresh per-task state.
                        result = Controller(telemetry).run(fixture, scenario, arm)
                        save_run(result, args.output / "runs")
                        runs.append(result)
                        print(f"{fixture}/{scenario}/{arm}: {result['status']}; oracle={result['oracle_passed']}")
            bridge = cfo_bridge(runs)
            args.output.mkdir(parents=True, exist_ok=True)
            (args.output / "summary.json").write_text(json.dumps(bridge, indent=2) + "\n")
            print(f"Controlled smoke matrix: {len(runs)} runs. Evidence: {args.output}")
            return 0
        finally:
            telemetry.close()
    except (ValueError, OSError, KeyError) as exc:
        print(f"Receipts: {type(exc).__name__}: {str(exc)[:200]}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
