import pytest

from receipts.fixtures import FIXTURES, verify
from receipts.sandbox import Program, CandidateRejected


@pytest.mark.parametrize("name", ["payment", "discount"])
def test_visible_shortcut_passes_but_trusted_contract_fails(name):
    fixture = FIXTURES[name]
    assert verify(fixture, fixture.shortcut, visible=True)["passed"]
    assert not verify(fixture, fixture.shortcut)["passed"]
    correct = verify(fixture, fixture.correct)
    assert correct["passed"]
    assert fixture.required <= set(correct["coverage"])


def test_duplicate_charge_counterexample_is_observed():
    fixture = FIXTURES["payment"]
    result = verify(fixture, fixture.shortcut)
    replay = next(c for c in result["checks"] if c["requirement"] == "replay")
    assert not replay["passed"]
    assert replay["observed"]["charges_after_replay"] == 2


@pytest.mark.parametrize("source", [
    "import os\ndef discount(amount, rate, eligible):\n return 0",
    "def discount(amount, rate, eligible):\n return open('secret').read()",
    "def discount(amount, rate, eligible):\n return amount.__class__",
    "def discount(amount, rate, eligible):\n return eval('1')",
    "def discount(amount, rate, eligible):\n while True:\n  pass",
    "def discount(amount, rate, eligible):\n return 2 ** 10000000",
    "def discount(amount, rate, eligible):\n return 'x' * 10000000",
    "def discount(amount, rate, eligible):\n x = []\n x.append(x)\n return x",
])
def test_candidate_cannot_access_host_or_exceed_data_capabilities(source):
    with pytest.raises(CandidateRejected):
        Program(source, "discount", ("amount", "rate", "eligible"))(100, 20, True)


def test_nested_loops_are_fuel_bounded():
    source = """def discount(amount, rate, eligible):
    for a in "abcdefghijklmnopqrstuv":
        for b in "abcdefghijklmnopqrstuv":
            for c in "abcdefghijklmnopqrstuv":
                amount = amount + 1
    return amount
"""
    with pytest.raises(CandidateRejected):
        Program(source, "discount", ("amount", "rate", "eligible"))(100, 20, True)


def test_malformed_candidate_result_is_rejected_not_crashed():
    assert not verify(FIXTURES["payment"], "def checkout(request, ledger):\n return 5\n")["passed"]


def test_candidate_cannot_mutate_callers_input_ledger():
    ledger = []
    Program(FIXTURES["payment"].correct, "checkout", ("request", "ledger"))({"key": "x", "amount": 1}, ledger)
    assert ledger == []


@pytest.mark.parametrize("mutant", [
    FIXTURES["payment"].shortcut,
    FIXTURES["payment"].correct.replace('if charge["amount"] != amount:', 'if False:'),
    FIXTURES["payment"].correct.replace('if charge["key"] == key:', 'if True:'),
    FIXTURES["payment"].correct.replace('if not key or amount <= 0:', 'if False:'),
])
def test_trusted_payment_suite_kills_defined_behavior_mutants(mutant):
    assert not verify(FIXTURES["payment"], mutant)["passed"]
