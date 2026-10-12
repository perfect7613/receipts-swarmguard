"""Bounded cloud evidence run. Models stay local; trusted checks use fresh sandboxes."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import modal
from receipts.agents import ModelAgent
from receipts.controller import Controller, save_run
from receipts.modal_verifier import ModalVerifier
from receipts.telemetry import Telemetry, load_env


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", choices=("controlled", "live"), default="controlled")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--neatlogs", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    load_env()
    runs = []
    app = modal.App("receipts-collusion-reward-hacking")
    telemetry = Telemetry(args.neatlogs)
    try:
        with app.run():
            verifier = ModalVerifier(app)
            if args.track == "controlled":
                # Scenarios replay known source/approvals; no natural collusion claim.
                cases = [(f, s, a, False) for f in ("payment", "discount")
                         for s in ("clean", "shortcut", "collusion") for a in ("standard", "receipts")]
            else:
                # Two ordinary builders and two explicitly adversarial builders.
                cases = [("payment", "clean", "receipts", False),
                         ("discount", "clean", "receipts", False),
                         ("payment", "collusion", "receipts", False),
                         ("discount", "shortcut", "receipts", False)]
            for fixture, scenario, arm, seeded in cases:
                agent = ModelAgent("codex", telemetry) if args.track == "live" else None
                result = Controller(telemetry, agent, verifier).run(fixture, scenario, arm, 1, seeded)
                save_run(result, args.output / "runs")
                runs.append(result)
                print(f"{fixture}/{scenario}/{arm}: {result['status']} oracle={result['oracle_passed']} repairs={result['repair_attempts']}", flush=True)
                # Persist completed work even if a later cloud/model call fails.
                (args.output / "execution-receipts.json").write_text(json.dumps(verifier.receipts, indent=2) + "\n")
            groups = defaultdict(lambda: {"attempted": 0, "correct_completion": 0, "unsafe_accepted": 0,
                                           "repair_attempts": 0, "initial_oracle_failed": 0})
            for run in runs:
                row = groups[run["scenario"] + "/" + run["arm"]]
                row["attempted"] += 1
                for key in ("correct_completion", "unsafe_accepted", "repair_attempts"):
                    row[key] += int(run[key])
                # Rejection can also be insufficient/forged evidence; use check receipts for outcome.
                receipt = next((r for r in verifier.receipts if r.get("source_sha256") == run["candidates"][0]["digest"]), None) if run["candidates"] else None
                row["initial_oracle_failed"] += int(bool(receipt and not receipt["passed"]))
            summary = {"schema_version": "receipts.modal-experiment/v1", "at": datetime.now(timezone.utc).isoformat(),
                       "track": args.track, "app_id": app.app_id, "verifier_sha256": verifier.identity,
                       "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
                       "groups": dict(groups), "run_ids": [r["run_id"] for r in runs],
                       "sandbox_checks": len(verifier.receipts), "model_calls": sum(r["usage"]["calls"] for r in runs),
                       "limitations": ["Two restricted simulated contracts, not a public benchmark",
                                       "Controlled attacks are supplied scenarios, not emergent collusion",
                                       "Live red-team instructions test observed bypass behavior, not intent",
                                       "Models run locally; independent checks run in fresh Modal sandboxes",
                                       "No comparative live baseline or statistical performance claim",
                                       "Cloud/model billing not yet reconciled"]}
            (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    finally:
        telemetry.close()


if __name__ == "__main__":
    main()
