import json
import pytest
from receipts.benchmarks import read_predictions, prepare_swebench, audit_swebench_report, inspect_patch


PATCH = 'diff --git a/service.py b/service.py\n--- a/service.py\n+++ b/service.py\n@@ -1 +1 @@\n-return 0\n+return 1\n'


def prepare(tmp_path):
    prediction = tmp_path / "input.jsonl"
    prediction.write_text(json.dumps({"instance_id": "org__repo-1", "model_name_or_path": "receipts-dev",
                                      "model_patch": PATCH}) + "\n")
    task = {"instance_id": "org__repo-1", "repo": "org/repo", "base_commit": "b" * 40,
            "problem_statement": "Fix replay", "patch": "SECRET_GOLD", "test_patch": "SECRET_TESTS",
            "eval_script": "SECRET_EVAL", "FAIL_TO_PASS": ["hidden"]}
    plan = prepare_swebench(read_predictions(prediction), [task], "a" * 40, tmp_path / "plan")
    return plan, tmp_path / "plan/predictions.jsonl"


def report(**overrides):
    return {"submitted_ids": ["org__repo-1"], "completed_ids": ["org__repo-1"],
            "resolved_ids": ["org__repo-1"], "unresolved_ids": [], "error_ids": [],
            "empty_patch_ids": [], **overrides}


def test_plan_binds_patch_and_base_without_exposing_gold_to_worker(tmp_path):
    plan, prediction = prepare(tmp_path)
    worker = (tmp_path / "plan/worker-tasks.json").read_text()
    assert "SECRET" not in worker
    assert "hidden" not in worker
    assert plan["bindings"][0]["base_commit"] == "b" * 40
    assert plan["bindings"][0]["policy"]["passed"]
    assert not plan["benchmark_executed"]
    assert "--instance_ids" in plan["evaluation_command"]


@pytest.mark.parametrize("path", ["tests/test_service.py", ".github/workflows/test.yml", "pytest.ini", "pyproject.toml"])
def test_protected_edits_are_policy_violations_not_allowed_impl_patches(path):
    result = inspect_patch(PATCH.replace("service.py", path))
    assert not result["passed"]
    assert "PROTECTED_EVALUATION_PATH" in result["reasons"]


def test_empty_and_invalid_patches_cannot_appear_valid():
    assert not inspect_patch("")["passed"]
    assert not inspect_patch("not a diff")["passed"]


def test_changed_prediction_cannot_reuse_previous_report(tmp_path):
    plan, prediction = prepare(tmp_path)
    prediction.write_text(prediction.read_text() + " ")
    with pytest.raises(ValueError, match="changed"):
        audit_swebench_report(plan, prediction, report())


@pytest.mark.parametrize("bad", [
    {"submitted_ids": ["wrong"]}, {"resolved_ids": ["org__repo-1", "org__repo-1"]},
    {"completed_ids": []}, {"unresolved_ids": ["org__repo-1"]}, {"resolved_instances": 2},
])
def test_inconsistent_external_report_cannot_create_valid_summary(tmp_path, bad):
    plan, prediction = prepare(tmp_path)
    with pytest.raises(ValueError):
        audit_swebench_report(plan, prediction, report(**bad))


def test_plausible_imported_report_is_never_authenticated_execution(tmp_path):
    plan, prediction = prepare(tmp_path)
    audit = audit_swebench_report(plan, prediction, report())
    assert audit["reported_resolved"] == 1
    assert not audit["trusted_execution_verified"]
    assert not audit["benchmark_execution_claim_authorized"]


def test_missing_tasks_remain_in_denominator(tmp_path):
    plan, prediction = prepare(tmp_path)
    audit = audit_swebench_report(plan, prediction, report(completed_ids=[], resolved_ids=[]))
    assert audit["attempted"] == 1
    assert audit["reported_resolution_rate"] == 0
    assert audit["unknown_ids"] == ["org__repo-1"]
