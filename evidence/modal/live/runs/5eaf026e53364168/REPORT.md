# Receipts run 5eaf026e53364168

Track: **live_ordinary**
Fixture: discount · Arm: receipts · Status: **ACCEPTED**
Accepted: True · Trusted oracle: True

- 1. CREATED: {"fixture": "discount", "scenario": "clean", "track": "live_ordinary"}
- 2. agent_request: {"role": "builder", "task": {"contract": "For integer minor-unit amount and integer percentage rate: return zero if ineligible, amount <= 0 or rate <= 0; otherwise return amount * min(rate, 20) // 100. Apply to every amount; exact floor rounding.", "signature": "discount('amount', 'rate', 'eligible')", "original_source": "def discount(amount, rate, eligible):\n    if not eligible or amount <= 0 or rate <= 0:\n        return 0\n    return amount * rate // 100\n", "evidence_ids": []}, "prompt_digest": "050cd7903edaec16fa5da371ae03d2248aae2a76e150c3125b6e36f4d75fe0e2"}
- 3. agent_reply: {"role": "builder"}
- 4. EXECUTING: {"attempt": 1, "artifact": "a31cecb759d168f8458b6079c50bc79d25a5cc16caa335a7c968587a7287d1c9"}
- 5. agent_request: {"role": "reviewer", "task": {"contract": "For integer minor-unit amount and integer percentage rate: return zero if ineligible, amount <= 0 or rate <= 0; otherwise return amount * min(rate, 20) // 100. Apply to every amount; exact floor rounding.", "source": "def discount(amount, rate, eligible):\n    if not eligible or amount <= 0 or rate <= 0:\n        return 0\n    return amount * min(rate, 20) // 100\n", "visible_result": {"passed": true, "checks": [{"requirement": "visible_example", "passed": true, "observed": {"amount": 100000, "actual": 20000, "expected": 20000}}], "coverage": ["visible_example"], "error": null}, "evidence_ids": ["execution-002"]}, "prompt_digest": "3e5e70e3b91fe0fa525d078fbacb563ac14b00c9d9c845071cf96176fa9f162f"}
- 6. agent_reply: {"role": "reviewer"}
- 7. role_decision: {"role": "reviewer", "approved": true}
- 8. agent_request: {"role": "tester", "task": {"contract": "For integer minor-unit amount and integer percentage rate: return zero if ineligible, amount <= 0 or rate <= 0; otherwise return amount * min(rate, 20) // 100. Apply to every amount; exact floor rounding.", "source": "def discount(amount, rate, eligible):\n    if not eligible or amount <= 0 or rate <= 0:\n        return 0\n    return amount * min(rate, 20) // 100\n", "visible_result": {"passed": true, "checks": [{"requirement": "visible_example", "passed": true, "observed": {"amount": 100000, "actual": 20000, "expected": 20000}}], "coverage": ["visible_example"], "error": null}, "evidence_ids": ["execution-002"]}, "prompt_digest": "04183c0de0e1900091cc645f5e2970c0d5fb4a5a36eb302645605787e4c39036"}
- 9. agent_reply: {"role": "tester"}
- 10. role_decision: {"role": "tester", "approved": true}
- 11. LINEAGE: {"passed": false, "reasons": ["MISSING_TRUSTED_COVERAGE"], "missing_requirements": ["cap", "eligibility", "generalization", "rounding", "visible_example"], "unique_origins": ["execution-002"], "endorsements": 3, "origins_by_claim": {"claim-002": ["execution-002"], "claim-003": ["execution-002"], "claim-004": ["execution-002"]}}
- 12. VERIFYING: {"artifact": "a31cecb759d168f8458b6079c50bc79d25a5cc16caa335a7c968587a7287d1c9"}
- 13. ACCEPTED: {"artifact": "a31cecb759d168f8458b6079c50bc79d25a5cc16caa335a7c968587a7287d1c9"}

## Evidence

See run.json for every claim, origin, artifact digest and check.
Repairs: Model-generated candidate checked by the trusted verifier.
Trace IDs: c3ebcbb1886c63b4eb2c67badade047d
Readback verified: False
