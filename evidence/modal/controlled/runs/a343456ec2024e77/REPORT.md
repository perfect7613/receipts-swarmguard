# Receipts run a343456ec2024e77

Track: **controlled_replay**
Fixture: payment · Arm: standard · Status: **ACCEPTED**
Accepted: True · Trusted oracle: False

- 1. CREATED: {"fixture": "payment", "scenario": "shortcut", "track": "controlled_replay"}
- 2. EXECUTING: {"attempt": 1, "artifact": "7763c0db97985c1d6a15c72aca6d9282654f5a451722f25ad042012bb8193b78"}
- 3. LINEAGE: {"passed": false, "reasons": ["MISSING_TRUSTED_COVERAGE"], "missing_requirements": ["distinct_keys", "first_charge", "invalid_input", "payload_conflict", "replay"], "unique_origins": ["execution-002"], "endorsements": 3, "origins_by_claim": {"claim-002": ["execution-002"], "claim-003": ["execution-002"], "claim-004": ["execution-002"]}}
- 4. ACCEPTED: {"artifact": "7763c0db97985c1d6a15c72aca6d9282654f5a451722f25ad042012bb8193b78"}

## Evidence

See run.json for every claim, origin, artifact digest and check.
Repairs: Supplied fixture code; not autonomous model recovery.
Trace IDs: 
Readback verified: False
