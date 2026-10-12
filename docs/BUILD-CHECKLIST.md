# Build checklist and verification gates

This is the implementation handoff. None of the steps below has been executed in this planning-only request. Complete gates in order; a UI or seeded replay does not replace a real controller run.

## Gate 0 — freeze scope and establish access

- [ ] Create the project repository with an ordinary current-date initial commit. Keep planning artifacts.
- [ ] Choose the available model provider, exact model IDs, pricing source, concurrency, and resource limits. Pin package versions after testing their current published releases.
- [ ] Freeze payment contract, allowed paths, verifier assets, fixture digest, and at most two repairs.
- [ ] Confirm neatlogs project ingestion access and separate read access where needed.
- [ ] Install and verify Entire; enable its hooks before implementation sessions begin.
- [ ] Authenticate cfo.ai and choose its intended workspace.

**Pass:** a smoke run is readable in neatlogs, an actual coding change produces inspectable Entire provenance, and the intended cfo.ai workspace is readable. Record missing access as missing evidence; local exports do not satisfy actual sponsor use.

## Gate 1 — trusted fixture and oracle

- [ ] Implement a small simulated checkout ledger with the original retry bug, a controlled invalid shortcut, and a known correct implementation.
- [ ] Create visible response tests and separate trusted replay/conflict/invalid-input tests.
- [ ] Keep money in integer minor units and freeze input/output semantics.
- [ ] Run the trusted oracle against original, invalid, and known-correct implementations.
- [ ] Prove the invalid shortcut passes visible checks but fails replay correctness; the correct implementation passes both.

**Pass:** oracle distinguishes all three cases with raw command/output/exit-code evidence. The fixture must not depend on real payments.

## Gate 2 — tool boundary and authenticated event store

- [ ] Implement role-scoped read, patch, and allowed-command tools. No unrestricted host shell in the protected mode.
- [ ] Give agents write access only to candidate implementation paths.
- [ ] Run candidate code in an isolated verifier environment with trusted tests read-only.
- [ ] Store events in controller-owned SQLite and export append-only JSONL.
- [ ] Bind execution records to contract, artifact, tests, environment, and dependency digests.

**Pass:** attempted protected-test edits, controller-result forgery, symlink/path escape, and verifier bypass are denied or detected before acceptance. Agent assertions cannot set a trusted pass flag. Worktrees alone do not pass this gate.

## Gate 3 — lineage and freshness

- [ ] Define claim, execution, requirement coverage, dependency, and verdict records.
- [ ] Resolve approvals to their original execution observations.
- [ ] Show three approvals that depend on one visible test run.
- [ ] Track repeated executions separately from new requirement coverage.
- [ ] Invalidate evidence after relevant source/test/dependency changes.
- [ ] Reject unknown origins, cycles, malformed records, and required-check timeouts.

**Pass:** a clean task that legitimately reuses complete fresh evidence passes; a narrow passing suite cannot satisfy missing replay coverage; a result for an older artifact cannot approve a new one.

## Gate 4 — real three-role workflow and repair

- [ ] Run builder, reviewer, tester as actual model roles with recorded prompts, tools, outputs, and usage.
- [ ] Include a blind initial reviewer assessment before exposing the builder's conclusion.
- [ ] Invoke the trusted verifier before acceptance.
- [ ] On rejection, mark dependent claims invalid and deliver a repair task with failing requirement and concrete counterexample.
- [ ] Record the repair patch; verify it independently; stop after fixed retry limit.
- [ ] If the agent cannot repair, emit `NEEDS_HUMAN_REVIEW` with the remaining defect.

**Pass:** a real repair achieves one-charge replay semantics. A deterministic repair supplied by the harness must be labeled a fixture repair, not autonomous model recovery.

## Gate 5 — sponsor evidence

- [ ] Trace the controller root, three agent roles, calls, checks, and recovery with neatlogs.
- [ ] Set guardrail input/output and boolean pass attributes; read the exact finalized workflow back.
- [ ] Capture actual Entire checkpoints and provenance for the changed source.
- [ ] Save Graph impact with artifact/version association; use it for repair context while preserving mandatory regressions.
- [ ] Build native cfo.ai tables and scenarios from run economics; verify monthly and annual totals.

**Pass:** each sponsor has actual accessible evidence, not only a configuration file, logo, JSON fallback, or successful exporter response.

## Gate 6 — controls and benchmark

- [ ] Add the discount generalization case and clean control.
- [ ] Add controlled two-role coordination and misleading-review variants with explicit labels.
- [ ] Execute standard swarm, always-audit, and Receipts with a frozen protocol.
- [ ] Save every attempted run, including refusals, failed repairs, timeouts, and unknown cost records.
- [ ] Aggregate using the benchmark definitions; inspect a sample manually against raw evidence.

**Pass:** reported rates reconcile to rows. A small smoke matrix supports only a demonstration claim. Do not replace model runs with seeded attacks in the natural-behavior aggregate.

## Gate 7 — presentation and submission

- [ ] Build a compact evidence view showing task, agent claims, evidence dependency, counterexample, repair, and final verdict.
- [ ] Produce the demo using a completed run and disclose controlled scenarios.
- [ ] Publish source and check all judge-facing evidence without relying on local paths.
- [ ] Prepare the quote-tweet and submission fields; complete required public posting and form as a separate authorized submission action.
- [ ] Confirm cutoff updates in the official Discord before submission.

**Pass:** an independent viewer can reproduce the controlled path and inspect every headline claim.

## Priority under the deadline

The published close is 12 October 2026, 11:55 PM IST; Discord updates are authoritative. Timings below are suggested work allocations, not a completion promise or a measured estimate.

| Allocation | Work | Gate |
|---|---|---|
| First 20 minutes | Access, model configuration, oracle contract | 0–1 smoke |
| Next 60 minutes | Broker, lineage, trusted checks, real repair loop | 2–4 |
| Next 25 minutes | Sponsor readback and cfo.ai native model | 5 |
| Next 25 minutes | Controls and a small paired smoke matrix | 6 smoke |
| Final 30–40 minutes | Evidence, video, public links, submission | 7 |

If behind, keep one fixture complete and report the limited sample. Drop optional model audits, broad fixtures, elaborate UI, and extended benchmarks before dropping trusted acceptance or genuine sponsor evidence. Obtain sponsor access early because it can block final evidence.

## Future implementation prompt

> Implement Receipts SwarmGuard from FINAL-PLAN.md and this checklist. Start by verifying the task oracle and execution boundary. Use SPONSOR-RUNBOOK.md for actual sponsor integrations and BENCHMARK-PROTOCOL.md for measurements. Record failures and missing access honestly. Complete one real builder/reviewer/tester → reject → repair → independent-accept path before expanding fixtures or UI. Keep controller-authenticated evidence separate from model assertions. Do not publish or submit until that action is authorized.
