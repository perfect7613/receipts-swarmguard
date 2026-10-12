# Claims and evidence boundaries

Updated 12 October 2026. Use this document when explaining the project, writing a submission or preparing a benchmark headline.

## Wording supported now

> Receipts SwarmGuard is a working prototype that binds coding-agent approvals to independent execution evidence, rejects stale or insufficient evidence, and verifies bounded repairs. It demonstrates this on two simulated contracts, includes one live model repair, and provides a preparation/audit bridge for SWE-bench prediction artifacts.

- The controlled 12-run matrix includes two seeded faulty candidates accepted by standard review. Both protected policies reject them and accept known fixture repairs. Six clean controls pass without repair. State that this is a controlled smoke matrix, with simulated always-audit handoffs.
- One seeded faulty candidate was repaired by real Codex calls and passed the supported independent payment contract. This establishes a working recovery path, not a reliable population-level recovery rate.
- The observed neatlogs trace has 15 finalized spans and 57,925 tokens, with readback metadata matched. Guardrail content rendering was not separately screenshot-verified.
- A real repair transcript is manually associated with an Entire logs-only checkpoint. Automatic hook capture is not established.
- 54 automated tests pass, including benchmark preparation and report-consistency tests. A build succeeds. These are software checks, not 54 real benchmark tasks.
- Five official SWE-bench Verified reference patches pass format/identity/policy preflight. No candidate execution, external task resolution rate or comparative gain follows from that preflight.

## What would justify expanded claims

| Proposed statement | Minimum supporting evidence |
| --- | --- |
| “Works on repository issues” | Pinned real tasks, isolated execution, fresh replay, passing release controls and published patch/log receipts |
| “Reduces unsafe acceptance” | Same initial artifacts under paired policies; independent oracle; all attempted cases; clean-control false-rejection rate and uncertainty |
| “Improves end-to-end resolution” | Paired ordinary tasks with declared equal budget; final fresh-regraded outcomes; errors and timeouts retained; uncertainty and raw counts |
| “Resists verifier exploitation” | Successful attacks against baseline, blocked attacks against frozen defense, unseen attack holdout and legitimate-solver controls |
| “Saves review cost” | Measured model, verifier, infrastructure and human-review cost; matched success criteria; missing observations disclosed |
| “Detects collusion” | A defined coordination violation, evidence beyond correlated mistakes, repeated-memory protocol and validated labels. The current product does not establish this |

## Do not claim

No production deployment, payment processing, broad code correctness, natural collusion frequency, guaranteed reward-hacking prevention, benchmark superiority, native cfo.ai Model completion, or economic savings has been demonstrated. Do not transfer a paper's reported percentage to Receipts.

Say “resolved on these tasks under this verifier and configuration,” not “correct in general.” Treat a benchmark pass as bounded evidence. Imported reports and user-provided manifests cannot authenticate themselves; the audit output keeps their trust flags false.

## Submission explanation

Start with the checkout-retry failure: multiple reviewers endorse one incomplete test, yet replay charges twice. Show the original failure, its dependent approvals, the independent rejection, the repair, and the fresh accepted check. Then show the trace and provenance. Explain that the next step is fresh-environment evaluation on real repository tasks, with capability, exploit resistance and coordination evaluated separately.

Read [the expansion specification](REAL-WORLD-EXPANSION.md) for the current research sources, benchmark choices and execution order.
