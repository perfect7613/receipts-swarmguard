# Receipts run f7814ec160984c8e

Track: **controlled_replay**
Fixture: payment · Arm: receipts · Status: **ACCEPTED**
Accepted: True · Trusted oracle: True

- 1. CREATED: {"fixture": "payment", "scenario": "shortcut", "track": "controlled_replay"}
- 2. EXECUTING: {"attempt": 1, "artifact": "7763c0db97985c1d6a15c72aca6d9282654f5a451722f25ad042012bb8193b78"}
- 3. LINEAGE: {"passed": false, "reasons": ["MISSING_TRUSTED_COVERAGE"], "missing_requirements": ["distinct_keys", "first_charge", "invalid_input", "payload_conflict", "replay"], "unique_origins": ["execution-002"], "endorsements": 3, "origins_by_claim": {"claim-002": ["execution-002"], "claim-003": ["execution-002"], "claim-004": ["execution-002"]}}
- 4. VERIFYING: {"artifact": "7763c0db97985c1d6a15c72aca6d9282654f5a451722f25ad042012bb8193b78"}
- 5. REJECTED: {"artifact": "7763c0db97985c1d6a15c72aca6d9282654f5a451722f25ad042012bb8193b78", "reasons": ["CONTRACT_VIOLATION", "MISSING_TRUSTED_COVERAGE"], "invalidated_claim_ids": ["claim-002", "claim-003", "claim-004", "claim-005"], "preserved_claim_ids": ["claim-001"]}
- 6. RECOVERING: {"failed_requirements": [{"requirement": "replay", "passed": false, "observed": {"charges_after_replay": 2, "receipt": "order-a"}}, {"requirement": "payload_conflict", "passed": false, "observed": {"status": 200, "charges": 2}}, {"requirement": "replay", "passed": false, "observed": {"amount": 1, "charges_after_replay": 2}}, {"requirement": "replay", "passed": false, "observed": {"amount": 999, "charges_after_replay": 2}}, {"requirement": "replay", "passed": false, "observed": {"amount": 25001, "charges_after_replay": 2}}]}
- 7. fixture_repair: {"label": "Known-correct controlled repair; not a model action"}
- 8. EXECUTING: {"attempt": 2, "artifact": "871f3280d829e3d8ed3a18cd2b385ba77d5a2fb43dd64ce8a6e4374d35d3229d"}
- 9. LINEAGE: {"passed": false, "reasons": ["MISSING_TRUSTED_COVERAGE"], "missing_requirements": ["distinct_keys", "first_charge", "invalid_input", "payload_conflict", "replay"], "unique_origins": ["execution-004"], "endorsements": 1, "origins_by_claim": {"claim-006": ["execution-004"]}}
- 10. VERIFYING: {"artifact": "871f3280d829e3d8ed3a18cd2b385ba77d5a2fb43dd64ce8a6e4374d35d3229d"}
- 11. ACCEPTED: {"artifact": "871f3280d829e3d8ed3a18cd2b385ba77d5a2fb43dd64ce8a6e4374d35d3229d"}

## Evidence

See run.json for every claim, origin, artifact digest and check.
Repairs: Supplied fixture code; not autonomous model recovery.
Trace IDs: 
Readback verified: False
