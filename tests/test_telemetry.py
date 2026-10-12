from receipts.controller import Controller
from receipts.telemetry import Telemetry
from contextlib import contextmanager


class RecordingTelemetry(Telemetry):
    @contextmanager
    def span(self, name, kind, **attrs):
        if kind == "WORKFLOW":
            self.trace_ids.append("trace-" + str(len(self.trace_ids)))
        self.expected_spans.append({"name": name, "kind": kind})
        yield None


def test_each_run_exports_only_its_own_trace_and_span_expectations():
    telemetry = RecordingTelemetry()
    a = Controller(telemetry).run()
    b = Controller(telemetry).run()
    assert len(a["trace_ids"]) == len(b["trace_ids"]) == 1
    assert a["trace_ids"] != b["trace_ids"]
    assert len(a["expected_spans"]) == len(b["expected_spans"])
