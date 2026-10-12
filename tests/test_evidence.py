import pytest
from receipts.evidence import Ledger


def observation(ledger, artifact="v1", trusted=True, passed=True):
    return ledger.observe(artifact, {"coverage": ["replay"], "passed": passed},
                          "trusted_verifier" if trusted else "visible_runner")


def test_three_endorsements_resolve_to_one_origin_without_false_block():
    ledger = Ledger()
    evidence = observation(ledger)
    builder = ledger.claim("builder", "v1", "pass", [evidence])
    reviewer = ledger.claim("reviewer", "v1", "agree", dependencies=[builder])
    tester = ledger.claim("tester", "v1", "agree", dependencies=[reviewer])
    result = ledger.assess([builder, reviewer, tester], "v1", frozenset({"replay"}))
    assert result["passed"]
    assert result["endorsements"] == 3
    assert result["unique_origins"] == [evidence]


def test_visible_tests_cannot_authenticate_trusted_coverage():
    ledger = Ledger()
    identifier = observation(ledger, trusted=False)
    claim = ledger.claim("builder", "v1", "pass", [identifier])
    result = ledger.assess([claim], "v1", frozenset({"replay"}))
    assert not result["passed"]
    assert result["missing_requirements"] == ["replay"]


@pytest.mark.parametrize("kind", ["stale_observation", "stale_claim", "unknown_origin", "cycle", "failure", "empty"])
def test_untrustworthy_approval_cannot_pass(kind):
    ledger = Ledger()
    oid = observation(ledger, artifact="old" if kind == "stale_observation" else "v1", passed=kind != "failure")
    cid = ledger.claim("builder", "old" if kind == "stale_claim" else "v1", "pass",
                       [] if kind == "empty" else ["forged-id" if kind == "unknown_origin" else oid])
    if kind == "cycle":
        ledger.claims[cid].dependencies = (cid,)
    assert not ledger.assess([cid], "v1", frozenset({"replay"}))["passed"]


def test_invalidate_downstream_only_and_preserve_unrelated_work():
    ledger = Ledger()
    failed = ledger.claim("builder", "bad", "changed")
    dependent = ledger.claim("reviewer", "other", "depends", dependencies=[failed])
    independent = ledger.claim("documentation", "unrelated", "independent")
    assert ledger.invalidate("bad") == sorted([failed, dependent])
    assert not ledger.claims[independent].invalidated


def test_new_observation_is_required_after_source_changes():
    ledger = Ledger()
    old = observation(ledger, "old")
    claim = ledger.claim("builder", "new", "pass", [old])
    assert not ledger.assess([claim], "new", frozenset({"replay"}))["passed"]
    fresh = observation(ledger, "new")
    fresh_claim = ledger.claim("verifier", "new", "fresh", [fresh])
    assert ledger.assess([fresh_claim], "new", frozenset({"replay"}))["passed"]
