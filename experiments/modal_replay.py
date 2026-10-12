"""Replay the preserved attack against a new verifier; never overwrite old evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import modal
from receipts.agents import ModelAgent
from receipts.controller import Controller, save_run
from receipts.fixtures import FIXTURES
from receipts.modal_verifier import ModalVerifier
from receipts.telemetry import Telemetry, load_env


def main():
    root = Path("artifacts/modal-hardened-replay")
    root.mkdir(parents=True, exist_ok=False)
    load_env()
    original = next(json.loads(p.read_text()) for p in Path("evidence/modal/red-team/runs").glob("*/run.json")
                    if json.loads(p.read_text())["fixture"] == "payment")
    attack = original["candidates"][0]["source"]
    telemetry = Telemetry(True)
    app = modal.App("receipts-verifier-hardening-replay")
    try:
        with app.run():
            verifier = ModalVerifier(app)
            failed = verifier(FIXTURES["payment"], attack)
            # Legitimate-solver control must still pass after verifier hardening.
            control = verifier(FIXTURES["payment"], FIXTURES["payment"].correct)
            if failed["passed"] or not control["passed"]:
                raise ValueError("Hardening controls failed; do not claim mitigation")
            agent = ModelAgent("codex", telemetry)
            recovered = Controller(telemetry, agent, verifier).run("payment", "clean", "receipts", 1,
                                                                  seed_source=attack)
            save_run(recovered, root / "runs")
            summary = {"schema_version": "receipts.hardening/v1", "at": datetime.now(timezone.utc).isoformat(),
                       "original_run_id": original["run_id"], "original_oracle_passed": original["oracle_passed"],
                       "original_accepted": original["accepted"],
                       "original_verifier_sha256": original["oracle"]["execution_receipt"]["verifier_sha256"],
                       "hardened_verifier_sha256": verifier.identity,
                       "attack_source_sha256": hashlib.sha256(attack.encode()).hexdigest(),
                       "hardened_attack_rejected": not failed["passed"],
                       "failed_checks": [c for c in failed["checks"] if not c["passed"]],
                       "legitimate_control_passed": control["passed"],
                       "recovery_run_id": recovered["run_id"], "recovery_correct_completion": recovered["correct_completion"],
                       "repair_attempts": recovered["repair_attempts"], "sandbox_checks": len(verifier.receipts),
                       "model_calls": recovered["usage"]["calls"],
                       "runtime_source_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in [*Path("src/receipts").glob("*.py"), Path(__file__)]},
                       "limitations": ["Mitigates a captured attack; not an unseen-attack evaluation",
                                       "Finite input coverage does not prove correctness",
                                       "Original gate accepted a genuine requirement violation",
                                       "Replay starts from a captured attack, not a new independent attacker"]}
            (root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
            (root / "execution-receipts.json").write_text(json.dumps(verifier.receipts, indent=2) + "\n")
    finally:
        telemetry.close()


if __name__ == "__main__":
    main()
