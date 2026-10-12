"""Optional neatlogs spans. Credentials never enter evidence or span attributes."""

from contextlib import contextmanager
import json
import os
from pathlib import Path


def load_env(path: Path = Path(".env")):
    """Load simple KEY=VALUE settings without overriding the process environment."""
    if path.exists():
        for line in path.read_text().splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            key, sep, value = line.partition("=")
            if sep and key.strip():
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


class Telemetry:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.trace_ids: list[str] = []
        self.expected_spans: list[dict] = []
        if enabled:
            import neatlogs
            if not os.environ.get("NEATLOGS_API_KEY"):
                raise ValueError("Set NEATLOGS_API_KEY in the environment or ignored .env")
            options = {"api_key": os.environ["NEATLOGS_API_KEY"], "sample_rate": 1.0}
            if os.environ.get("NEATLOGS_ENDPOINT"):
                options["endpoint"] = os.environ["NEATLOGS_ENDPOINT"]
            # The installed stable SDK does not take the docs' workflow_name kwarg.
            # Assign the workflow attribute on the actual root instead.
            neatlogs.init(**options)

    @contextmanager
    def span(self, name: str, kind: str, **attributes):
        if not self.enabled:
            yield None
            return
        import neatlogs
        with neatlogs.trace(name, kind=kind) as span:
            context = span.get_span_context()
            trace_id = f"{context.trace_id:032x}"
            span_id = f"{context.span_id:016x}"
            if kind == "WORKFLOW":
                self.trace_ids.append(trace_id)
                span.set_attribute("neatlogs.workflow.name", "receipts-swarmguard")
            for key, value in attributes.items():
                if value is not None:
                    span.set_attribute(f"receipts.{key}", value)
            self.expected_spans.append({"trace_id": trace_id, "span_id": span_id,
                                        "name": name, "kind": kind})
            yield span

    def guardrail(self, name: str, result: dict, **attributes):
        with self.span(name, "GUARDRAIL", **attributes) as span:
            if span is not None:
                span.set_attribute("neatlogs.guardrail.input", json.dumps(attributes, sort_keys=True))
                span.set_attribute("neatlogs.guardrail.passed", bool(result["passed"]))
                summary = {k: result[k] for k in ("passed", "reasons", "missing_requirements", "error") if k in result}
                span.set_attribute("neatlogs.guardrail.output", json.dumps(summary)[:1500])

    def close(self):
        if self.enabled:
            import neatlogs
            neatlogs.flush(timeout_millis=10000)
            neatlogs.shutdown(timeout_millis=10000)
