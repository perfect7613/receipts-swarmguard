"""Controller-owned, dependency-free verifier entry point for a fresh sandbox.

Candidate source stays data for the restricted interpreter; it is never exec'd.
"""
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
from .fixtures import FIXTURES, verify


def verifier_identity(root: Path) -> str:
    files = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
             for name in ("fixtures.py", "sandbox.py", "modal_worker.py")}
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def main():
    request = json.loads(sys.argv[1])
    fixture = FIXTURES[request["fixture"]]
    source = request["source"]
    if not isinstance(source, str) or len(source.encode()) > 65536:
        raise ValueError("Invalid candidate input")
    probe = None
    if request.get("probe"):
        try:
            with socket.create_connection(("1.1.1.1", 443), timeout=2):
                probe = {"outbound_connection_succeeded": True}
        except OSError as exc:
            probe = {"outbound_connection_succeeded": False, "exception_type": type(exc).__name__}
        probe["credential_variables_present"] = [k for k in (
            "OPENAI_API_KEY", "NEATLOGS_API_KEY", "CFO_AI_ACCESS_TOKEN", "MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET")
            if k in os.environ]
    print(json.dumps({"fixture": fixture.name,
                      "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
                      "contract_sha256": hashlib.sha256(fixture.contract.encode()).hexdigest(),
                      "verifier_sha256": verifier_identity(Path(__file__).parent),
                      "result": verify(fixture, source), "probe": probe}))


if __name__ == "__main__":
    main()
