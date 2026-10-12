"""Fresh Modal sandboxes for trusted fixture checks, with no candidate credentials.

Optional cloud extra only. This does not implement arbitrary-repository execution.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from .modal_worker import verifier_identity


def validate_response(response: dict, fixture, source: str, identity: str) -> dict:
    expected = {"fixture": fixture.name,
                "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
                "contract_sha256": hashlib.sha256(fixture.contract.encode()).hexdigest(),
                "verifier_sha256": identity}
    if any(response.get(k) != value for k, value in expected.items()):
        raise ValueError("Cloud verifier identity mismatch")
    result = response.get("result")
    if not isinstance(result, dict) or type(result.get("passed")) is not bool:
        raise ValueError("Malformed cloud verifier result")
    checks, coverage = result.get("checks"), result.get("coverage")
    if not isinstance(checks, list) or not isinstance(coverage, list):
        raise ValueError("Malformed cloud verifier checks")
    if any(not isinstance(c, dict) or type(c.get("passed")) is not bool for c in checks):
        raise ValueError("Malformed cloud verifier check")
    if result["passed"] and (not checks or not fixture.required <= set(coverage)
                              or not all(c["passed"] for c in checks)):
        raise ValueError("Cloud success lacks required checks")
    return result


class ModalVerifier:
    def __init__(self, app):
        import modal
        self.modal, self.app = modal, app
        root = Path(__file__).parent
        self.identity = verifier_identity(root)
        image = modal.Image.debian_slim(python_version="3.12")
        for name in ("__init__.py", "fixtures.py", "sandbox.py", "modal_worker.py"):
            image = image.add_local_file(root / name, "/verifier/receipts/" + name, copy=True)
        self.image = image.env({"PYTHONPATH": "/verifier"})
        self.receipts = []

    def __call__(self, fixture, source):
        started = time.perf_counter()
        sandbox = self.modal.Sandbox.create(
            "python", "-m", "receipts.modal_worker", json.dumps({
                "fixture": fixture.name, "source": source, "probe": not self.receipts}),
            app=self.app, image=self.image, block_network=True, secrets=[],
            cpu=(0.25, 1.0), memory=(128, 256), timeout=60)
        receipt = {"executor": "modal_sandbox", "sandbox_id": sandbox.object_id,
                   "app_id": self.app.app_id, "image_id": self.image.object_id,
                   "at": datetime.now(timezone.utc).isoformat(),
                   "block_network_requested": True, "injected_secrets": False,
                   "verifier_sha256": self.identity, "fresh_sandbox": True}
        try:
            output = sandbox.stdout.read()
            sandbox.wait()
            receipt["exit_code"] = sandbox.returncode
            if sandbox.returncode != 0:
                raise ValueError("Cloud verifier did not complete successfully")
            if len(output.encode()) > 1_000_000:
                raise ValueError("Cloud output exceeds limit")
            response = json.loads(output)
            result = validate_response(response, fixture, source, self.identity)
            receipt.update({k: response[k] for k in ("source_sha256", "contract_sha256", "probe")})
            receipt["output_sha256"] = hashlib.sha256(output.encode()).hexdigest()
            receipt["passed"] = result["passed"]
            receipt["execution_verified_by_controller"] = True
            return {**result, "execution_receipt": receipt}
        finally:
            receipt["wall_seconds"] = time.perf_counter() - started
            self.receipts.append(receipt)
            sandbox.terminate(wait=True)
