import json
import pytest
from receipts.controller import Controller, save_run
from receipts.sponsors import cfo_bridge
from receipts.agents import Reply, Usage


@pytest.mark.parametrize("fixture", ["payment", "discount"])
def test_controlled_shortcut_is_unsafe_without_gate_and_repaired_with_gate(fixture):
    baseline = Controller().run(fixture, "shortcut", "standard")
    protected = Controller().run(fixture, "shortcut", "receipts")
    assert baseline["unsafe_accepted"]
    assert protected["correct_completion"]
    assert protected["repair_attempts"] == 1
    assert protected["invalidated_claim_ids"]
    assert protected["candidates"][0]["digest"] != protected["candidates"][1]["digest"]
    assert protected["track"] == "controlled_replay"


def test_clean_control_passes_without_repair_or_defect_intervention():
    result = Controller().run("payment", "clean")
    assert result["correct_completion"]
    assert result["repair_attempts"] == 0
    assert not result["invalidated_claim_ids"]
    assert "REJECTED" not in [e["event"] for e in result["events"]]


def test_exhausted_repair_budget_stops_without_claiming_success():
    result = Controller().run("payment", "shortcut", max_repairs=0)
    assert result["status"] == "NEEDS_HUMAN_REVIEW"
    assert not result["accepted"]


class BrokenAgent:
    def __init__(self):
        self.usage = Usage()
        self.sessions = []

    def ask(self, role, task):
        return Reply(source="def checkout(request, ledger):\n return 5\n" if role in ("builder", "repair") else "",
                     statement="All tests pass", evidence_ids=["invented"], approved=True)


def test_live_forged_claim_and_invalid_result_do_not_crash_or_accept():
    result = Controller(agent=BrokenAgent()).run(max_repairs=1)
    assert result["status"] == "NEEDS_HUMAN_REVIEW"
    assert not result["accepted"]
    assert result["repair_attempts"] == 1


def test_save_and_economics_keep_actual_artifacts_and_unknown_cost(tmp_path):
    run = Controller().run()
    directory = save_run(run, tmp_path)
    exported = json.loads((directory / "run.json").read_text())
    assert exported["run_id"] == run["run_id"]
    assert (directory / "attempt-2.py").exists()
    bridge = cfo_bridge([run])
    assert bridge["observations"]["receipts"]["cost_per_correct_task"] is None
    assert not bridge["native_cfo_model_created"]


def test_cfo_export_refuses_to_pool_live_behavior_with_controlled_replay():
    run = Controller().run()
    live = {**run, "track": "live_ordinary"}
    with pytest.raises(ValueError, match="separately"):
        cfo_bridge([run, live])
