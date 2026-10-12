import subprocess
from types import SimpleNamespace

import pytest

from receipts.agents import ModelAgent


def test_codex_adapter_preserves_usage_but_does_not_forward_application_secrets(monkeypatch):
    monkeypatch.setenv("NEATLOGS_API_KEY", "test-secret")
    monkeypatch.setenv("CFO_AI_ACCESS_TOKEN", "other-secret")
    monkeypatch.delenv("RECEIPTS_MODEL", raising=False)
    def execute(command, **kwargs):
        import json
        from pathlib import Path
        assert "NEATLOGS_API_KEY" not in kwargs["env"]
        assert "CFO_AI_ACCESS_TOKEN" not in kwargs["env"]
        output = Path(command[command.index("--output-last-message") + 1])
        output.write_text(json.dumps({"source": "", "statement": "No independent evidence",
                                      "evidence_ids": [], "approved": False}))
        return SimpleNamespace(returncode=0, stdout='{"type":"thread.started","thread_id":"test-session"}\n'
                               '{"type":"turn.completed","usage":{"input_tokens":12,"output_tokens":7,"cached_input_tokens":2}}\n')
    monkeypatch.setattr(subprocess, "run", execute)
    agent = ModelAgent("codex")
    reply = agent.ask("reviewer", {"evidence_ids": []})
    assert not reply.approved
    assert agent.usage.input_tokens == 12
    assert agent.usage.output_tokens == 7
    assert agent.usage.cached_tokens == 2
    assert agent.sessions == ["test-session"]
    assert agent.usage.model_cost_usd is None


def test_codex_timeout_is_a_sanitized_recoverable_failure(monkeypatch):
    def execute(command, **kwargs):
        raise subprocess.TimeoutExpired(command, 180)
    monkeypatch.setattr(subprocess, "run", execute)
    with pytest.raises(ValueError, match="timed out"):
        ModelAgent("codex").ask("builder", {})
