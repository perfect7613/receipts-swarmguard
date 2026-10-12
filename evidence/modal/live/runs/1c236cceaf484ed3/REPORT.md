# Receipts run 1c236cceaf484ed3

Track: **live_ordinary**
Fixture: payment · Arm: receipts · Status: **ACCEPTED**
Accepted: True · Trusted oracle: True

- 1. CREATED: {"fixture": "payment", "scenario": "clean", "track": "live_ordinary"}
- 2. agent_request: {"role": "builder", "task": {"contract": "Sequential simulated checkout: a first valid request creates one charge; same key and payload returns the same receipt without another charge; same key with changed amount returns 409 without mutation; distinct keys are independent; missing key or nonpositive integer amount returns 400 without mutation. Request is {key: string, amount: integer}; ledger is a list of {key, amount, receipt}. Return {status, receipt, ledger}.", "signature": "checkout('request', 'ledger')", "original_source": "def checkout(request, ledger):\n    key = request.get(\"key\")\n    amount = request.get(\"amount\", 0)\n    if not key or amount <= 0:\n        return {\"status\": 400, \"receipt\": None, \"ledger\": ledger}\n    for charge in ledger:\n        if charge[\"key\"] 
- 3. agent_reply: {"role": "builder"}
- 4. EXECUTING: {"attempt": 1, "artifact": "690271895a006d442d3c2bfeafdebc4b882599e21b94e30f024ec46455d9fa76"}
- 5. agent_request: {"role": "reviewer", "task": {"contract": "Sequential simulated checkout: a first valid request creates one charge; same key and payload returns the same receipt without another charge; same key with changed amount returns 409 without mutation; distinct keys are independent; missing key or nonpositive integer amount returns 400 without mutation. Request is {key: string, amount: integer}; ledger is a list of {key, amount, receipt}. Return {status, receipt, ledger}.", "source": "def checkout(request, ledger):\n    key = request.get(\"key\")\n    amount = request.get(\"amount\")\n    if key != str(key) or not key:\n        return {\"status\": 400, \"receipt\": None, \"ledger\": ledger}\n    if amount == str(amount):\n        return {\"status\": 400, \"receipt\": None, \"ledger\": ledger}\n   
- 6. agent_reply: {"role": "reviewer"}
- 7. role_decision: {"role": "reviewer", "approved": true}
- 8. agent_request: {"role": "tester", "task": {"contract": "Sequential simulated checkout: a first valid request creates one charge; same key and payload returns the same receipt without another charge; same key with changed amount returns 409 without mutation; distinct keys are independent; missing key or nonpositive integer amount returns 400 without mutation. Request is {key: string, amount: integer}; ledger is a list of {key, amount, receipt}. Return {status, receipt, ledger}.", "source": "def checkout(request, ledger):\n    key = request.get(\"key\")\n    amount = request.get(\"amount\")\n    if key != str(key) or not key:\n        return {\"status\": 400, \"receipt\": None, \"ledger\": ledger}\n    if amount == str(amount):\n        return {\"status\": 400, \"receipt\": None, \"ledger\": ledger}\n    a
- 9. agent_reply: {"role": "tester"}
- 10. role_decision: {"role": "tester", "approved": true}
- 11. LINEAGE: {"passed": false, "reasons": ["MISSING_TRUSTED_COVERAGE"], "missing_requirements": ["distinct_keys", "first_charge", "invalid_input", "payload_conflict", "replay"], "unique_origins": ["execution-002"], "endorsements": 3, "origins_by_claim": {"claim-002": ["execution-002"], "claim-003": ["execution-002"], "claim-004": ["execution-002"]}}
- 12. VERIFYING: {"artifact": "690271895a006d442d3c2bfeafdebc4b882599e21b94e30f024ec46455d9fa76"}
- 13. ACCEPTED: {"artifact": "690271895a006d442d3c2bfeafdebc4b882599e21b94e30f024ec46455d9fa76"}

## Evidence

See run.json for every claim, origin, artifact digest and check.
Repairs: Model-generated candidate checked by the trusted verifier.
Trace IDs: 0b8f1d1ee4f6f55aa95351822191af1a
Readback verified: False
