# Evidence index

Receipts SwarmGuard ties agent approvals to independently executed evidence and verifies repairs.

| Claim | Inspectable evidence |
|---|---|
| Reproducible working product | README commands, source, tests, and CI |
| Controlled before/after | [12-case controlled run directory](evidence/observed/controlled), including candidate code and complete event records |
| Real model repair | [Live repair](evidence/observed/live-repair/run.json), its rejected and corrected source, and report |
| Honest control outcome | [Adversarial-prompt run producing correct code](evidence/observed/live-adversarial-control/run.json) |
| neatlogs use | [Doctor probe](evidence/neatlogs-doctor-probe.json), [finalized live trace readback](evidence/observed/neatlogs-live-readback.json), run trace IDs |
| Entire use | [Actual Graph impact](evidence/observed/entire/graph_impact.txt), [Graph search](evidence/observed/entire/graph_search.txt), installed CLI version |
| cfo.ai bridge code | Sponsor MCP client, [controlled economics export](evidence/observed/cfo-bridge.json), [live repair export](evidence/observed/live-repair-cfo-bridge.json), and [native model specification](docs/CFO-MODEL.md) |
| Research relevance | [Research-to-product explanation](docs/RESEARCH-TO-PRODUCT.md) and [source audit](docs/SOURCES-AND-CORRECTIONS.md) |
| Requirements | [PRD issue](https://github.com/perfect7613/receipts-swarmguard/issues/1) |
| Current limits | [Implementation status](docs/IMPLEMENTATION-STATUS.md) |

Controlled fixture repairs are not autonomous actions. Live seeded repair is model-generated but begins with a supplied faulty candidate. The cfo.ai native Model is pending. No natural cheat-rate, verified gross margin, or throughput gain is claimed. The repository is a narrow fixture prototype rather than a production arbitrary-code sandbox.
