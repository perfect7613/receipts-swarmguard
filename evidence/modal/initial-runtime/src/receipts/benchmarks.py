"""SWE-bench preparation and external-result audit, without executing candidates.

Preparing a command is not running a benchmark. An imported report is not an
authenticated execution receipt; this module never grants it trusted status.
"""

from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import uuid


DATASET = "SWE-bench/SWE-bench_Verified"


def _hash(value) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read_predictions(path: Path) -> list[dict]:
    text = path.read_text()
    if len(text.encode()) > 50_000_000:
        raise ValueError("Prediction file exceeds 50 MB")
    rows = json.loads(text) if text.lstrip().startswith("[") else [json.loads(l) for l in text.splitlines() if l.strip()]
    if not isinstance(rows, list) or not rows:
        raise ValueError("Predictions must be a nonempty JSON list or JSONL")
    ids, models = set(), set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Prediction rows must be objects")
        for field in ("instance_id", "model_name_or_path", "model_patch"):
            if not isinstance(row.get(field), str):
                raise ValueError(f"Missing or non-string prediction field: {field}")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", row["instance_id"]):
            raise ValueError("Invalid instance ID")
        if not row["model_name_or_path"] or len(row["model_name_or_path"]) > 128:
            raise ValueError("Invalid model/configuration label")
        if row["instance_id"] in ids:
            raise ValueError("Duplicate prediction instance ID")
        ids.add(row["instance_id"])
        models.add(row["model_name_or_path"])
        if len(row["model_patch"].encode()) > 1_000_000:
            raise ValueError("Patch exceeds 1 MB")
    if len(models) != 1:
        raise ValueError("Prepare separate batches for different model/configuration labels")
    return rows


def inspect_patch(patch: str) -> dict:
    """Use Git's patch parser in numstat mode; never apply or execute the patch.

    Protected-path edits are policy violations in this evaluation profile, not
    inferred dishonesty. Some legitimate real tasks need authorized test changes.
    """
    if not patch.strip():
        return {"passed": False, "reasons": ["EMPTY_PATCH"], "paths": []}
    parsed = subprocess.run(["git", "apply", "--numstat", "-z"], input=patch.encode(),
                            capture_output=True, timeout=10)
    if parsed.returncode:
        return {"passed": False, "reasons": ["MALFORMED_PATCH"], "paths": []}
    paths = []
    reasons = set()
    for record in parsed.stdout.decode("utf-8", errors="strict").split("\0"):
        if not record:
            continue
        fields = record.split("\t", 2)
        if len(fields) != 3:
            raise ValueError("Unexpected Git patch metadata")
        path = fields[2]
        paths.append(path)
        p = PurePosixPath(path)
        if not path or p.is_absolute() or ".." in p.parts or "\\" in path:
            reasons.add("UNSAFE_PATCH_PATH")
        lower = path.lower()
        if any(part in ("tests", "test", "testing", ".github", ".git", ".entire", ".codex") for part in p.parts) \
                or p.name.startswith("test_") or p.name.endswith("_test.py") \
                or p.name in ("pytest.ini", "tox.ini", "conftest.py", "setup.cfg", "pyproject.toml"):
            reasons.add("PROTECTED_EVALUATION_PATH")
        if p.name in (".env",) or lower.endswith(".env"):
            reasons.add("SECRET_CONFIGURATION_PATH")
    if not paths:
        reasons.add("NO_FILE_CHANGES")
    return {"passed": not reasons, "reasons": sorted(reasons), "paths": sorted(set(paths)),
            "profile": "implementation-only; explicit task authorization needed for test/config edits"}


def prepare_swebench(predictions: list[dict], tasks: list[dict], revision: str, output: Path) -> dict:
    """Bind a selected batch to task/base-commit/patch identities and hide answers."""
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Provide the recorded 40-character dataset revision")
    by_id = {row["instance_id"]: row for row in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("Duplicate task metadata")
    output.mkdir(parents=True, exist_ok=False)
    worker_tasks, bindings = [], []
    for prediction in predictions:
        task = by_id.get(prediction["instance_id"])
        if task is None:
            raise ValueError("Prediction not present in supplied task snapshot")
        base = task.get("base_commit")
        if not isinstance(base, str) or not re.fullmatch(r"[a-f0-9]{40}", base):
            raise ValueError("Task needs a concrete base commit")
        worker = {k: task[k] for k in ("instance_id", "repo", "base_commit", "problem_statement")}
        # Gold patches, hidden test patches, hints, and grading scripts never go to workers.
        worker_tasks.append(worker)
        identity = {"dataset": DATASET, "dataset_revision": revision, "task": worker,
                    "patch_sha256": sha256(prediction["model_patch"].encode()).hexdigest()}
        bindings.append({"instance_id": task["instance_id"], "repo": task["repo"], "base_commit": base,
                         "artifact_binding": _hash(identity), "patch_sha256": identity["patch_sha256"],
                         "policy": inspect_patch(prediction["model_patch"])})
    normalized = [{k: p[k] for k in ("instance_id", "model_name_or_path", "model_patch")} for p in predictions]
    prediction_path = output / "predictions.jsonl"
    prediction_path.write_text("".join(json.dumps(p) + "\n" for p in normalized))
    (output / "worker-tasks.json").write_text(json.dumps(worker_tasks, indent=2) + "\n")
    run_id = "receipts-" + _hash(bindings)[:12] + "-" + uuid.uuid4().hex[:8]
    command = ["python", "-m", "swebench.harness.run_evaluation", "--dataset_name", DATASET,
               "--predictions_path", str(prediction_path.resolve()), "--max_workers", "1",
               "--run_id", run_id, "--instance_ids", *[p["instance_id"] for p in predictions]]
    manifest = {"schema_version": "receipts.swebench-plan/v1", "dataset": DATASET,
                "dataset_revision": revision, "track": "benchmark_preparation",
                "run_id": run_id, "model_name_or_path": normalized[0]["model_name_or_path"],
                "predictions_sha256": sha256(prediction_path.read_bytes()).hexdigest(),
                "bindings": bindings, "evaluation_command": command,
                "benchmark_executed": False, "trusted_execution_verified": False,
                "notes": ["Install/pin the official harness and use Docker before execution",
                          "Record actual dataset and harness revisions used by that execution",
                          "Dataset revision here is a preparation binding, not an enforced harness revision",
                          "Use a new run_id for changed patches to avoid stale result caches"]}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def audit_swebench_report(manifest: dict, predictions_path: Path, report: dict) -> dict:
    """Check a report's internal consistency, preserving unknown outcomes.

    The caller must additionally authenticate execution and dataset/harness versions
    before treating these imported labels as trusted acceptance evidence.
    """
    if sha256(predictions_path.read_bytes()).hexdigest() != manifest["predictions_sha256"]:
        raise ValueError("Predictions changed since preparation; regenerate the plan")
    expected = {b["instance_id"] for b in manifest["bindings"]}
    sets = {}
    for field in ("submitted_ids", "completed_ids", "resolved_ids", "unresolved_ids", "error_ids", "empty_patch_ids"):
        rows = report.get(field)
        if not isinstance(rows, list) or any(not isinstance(i, str) for i in rows) or len(set(rows)) != len(rows):
            raise ValueError(f"Report field must contain unique string IDs: {field}")
        sets[field] = set(rows)
    if sets["submitted_ids"] != expected:
        raise ValueError("Report submitted IDs differ from the prepared batch")
    if any(ids - expected for ids in sets.values()):
        raise ValueError("Report contains outcomes outside the selected batch")
    if not (sets["resolved_ids"] | sets["unresolved_ids"]) <= sets["completed_ids"]:
        raise ValueError("Resolved/unresolved IDs must be completed")
    categories = ("resolved_ids", "unresolved_ids", "error_ids", "empty_patch_ids")
    for i, a in enumerate(categories):
        for b in categories[i + 1:]:
            if sets[a] & sets[b]:
                raise ValueError("Report outcome categories overlap")
    for name, field in (("submitted", "submitted_ids"), ("completed", "completed_ids"),
                        ("resolved", "resolved_ids"), ("unresolved", "unresolved_ids"),
                        ("error", "error_ids"), ("empty_patch", "empty_patch_ids")):
        count = report.get(name + "_instances")
        if count is not None and (type(count) is not int or count != len(sets[field])):
            raise ValueError("Report counts disagree with ID lists")
    outcomes = set().union(*(sets[f] for f in categories))
    unknown = expected - outcomes
    rows = []
    for binding in manifest["bindings"]:
        identifier = binding["instance_id"]
        outcome = next((f.removesuffix("_ids") for f in categories if identifier in sets[f]), "unknown")
        rows.append({**binding, "reported_outcome": outcome,
                     "acceptance_eligible_if_authenticated": outcome == "resolved" and binding["policy"]["passed"]})
    return {"schema_version": "receipts.swebench-audit/v1", "run_id": manifest["run_id"],
            "attempted": len(expected), "reported_resolved": len(sets["resolved_ids"]),
            "reported_resolution_rate": len(sets["resolved_ids"]) / len(expected),
            "unknown_ids": sorted(unknown), "rows": rows, "report_sha256": _hash(report),
            "trusted_execution_verified": False, "benchmark_execution_claim_authorized": False,
            "limitations": ["Operator-imported report, not authenticated harness execution",
                            "A benchmark pass does not prove full requirement correctness or absence of reward hacking",
                            "Resolution rate is reported over all prepared tasks; errors/missing tasks are retained"]}
