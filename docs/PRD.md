# Receipts SwarmGuard

## Problem Statement

Engineering teams use builders, reviewers, and testers to produce code. Multiple approvals can appear independent even when all agents repeat one incomplete test result. A team can therefore report success after gaming the visible tests, adopting an unsupported peer assertion, or coordinating an invalid approval. Engineers need to know which requirements were independently checked on the exact code being accepted, and how rejected work was repaired.

## Solution

Receipts is a controller for a narrow coding-agent workflow. It binds claims to controller-owned executions and artifact versions, exposes shared evidence, runs trusted contract checks, blocks invalid acceptance, and verifies a bounded repair. A reproducible checkout replay example shows the consequence: a successful retry response can conceal a second charge. A discount example demonstrates hardcoding beyond visible inputs.

The initial version is a Python command-line product with inspectable JSON/Markdown evidence. It supports deterministic controlled scenarios and a live model adapter. neatlogs traces its workflow, Entire supplies genuine code context/provenance, and a cfo.ai bridge exports observed economics and supports its authenticated MCP tools. It keeps controlled replay and observed model behavior visibly separate.

## User Stories

1. As an engineer, I want to run a complete controlled example with one command, so that I can understand the failure and intervention.
2. As an engineer, I want payment replay rules fixed before execution, so that a passing response cannot conceal a duplicate charge.
3. As an engineer, I want correct discount behavior checked beyond visible examples, so that hardcoded outputs are rejected.
4. As an operator, I want candidate code to have no filesystem, network, import, or secret access, so that it cannot rewrite its own verdict.
5. As an operator, I want unsupported candidate syntax rejected clearly, so that execution never silently becomes unrestricted.
6. As an engineer, I want every test execution bound to the source digest, so that old results cannot approve later edits.
7. As an engineer, I want agent approvals linked to original executions, so that repeated endorsements do not inflate evidence.
8. As an engineer, I want valid shared evidence permitted, so that normal collaboration is not mislabeled as misconduct.
9. As an engineer, I want missing requirement coverage identified, so that visible tests cannot substitute for the full contract.
10. As an operator, I want only trusted verifier results to grant acceptance, so that agent text cannot authenticate itself.
11. As an engineer, I want a failed check to invalidate dependent claims, so that downstream approvals are revisited.
12. As an engineer, I want unaffected claims preserved, so that recovery does not restart unrelated work.
13. As an engineer, I want repairs checked on a new artifact, so that a successful repair has fresh evidence.
14. As an operator, I want retries bounded, so that unresolved work ends in a visible human-review state.
15. As an evaluator, I want clean controls, so that valid patches can pass without false defect interventions.
16. As an evaluator, I want ordinary and adversarial trials labeled separately, so that attack demonstrations are not reported as natural cheat rates.
17. As an evaluator, I want standard, always-audit, and Receipts configurations, so that their safety and costs can be compared.
18. As an evaluator, I want all failures and repair attempts exported, so that favorable results cannot omit expensive failed work.
19. As an operator, I want live builder and reviewer calls available through my authenticated provider, so that the system can perform real model recovery.
20. As an operator, I want usage and cost completeness recorded, so that unknown prices do not become zero-cost claims.
21. As a judge, I want failed and passing neatlogs guardrails, so that the intervention is inspectable.
22. As a judge, I want exact trace readback status, so that successful export is not confused with confirmed ingestion.
23. As an engineer, I want Entire Graph output linked to changed functions, so that I can inspect impact during recovery.
24. As a judge, I want real Entire provenance or clearly identified Graph output, so that sponsor use is verifiable.
25. As a founder, I want measured economics exported to cfo.ai, so that pricing and runway assumptions are editable.
26. As an operator, I want credentials kept outside tracked files and evidence exports, so that publication does not expose access.
27. As a judge, I want the research and actual incident motivation explained with source links, so that product claims are grounded.
28. As a maintainer, I want a small set of tested modules and a reproducible dependency lock, so that the prototype is easy to extend.

## Implementation Decisions

- Keep the initial surface a Python CLI and evidence report. No web framework, distributed service, queue, database, or account system is needed.
- Deep modules: a restricted candidate interpreter/verifier, a controller-owned evidence ledger and acceptance policy, a bounded workflow/recovery controller, and sponsor/provider adapters.
- Candidate source is a small documented subset of Python, interpreted as syntax rather than executed as arbitrary Python bytecode. It supports only fixture data and bounded operations. General repository execution is out of scope.
- Execution observations bind source, verifier revision, coverage, pass/failure, and executor. Agent claims can cite observations but cannot set trusted status.
- Shared origins trigger an explanation or audit; final acceptance depends on fresh trusted coverage and passing checks.
- Deterministic scenarios are explicitly controlled. Live model outputs are validated before use and separately labeled; model failures end in recorded failure states.
- Reuse intact independent work during repair. Always rerun critical payment and discount contract checks.
- Use standard-library JSON event persistence until durable multi-process state is required. This intentionally narrows the earlier SQLite architecture under YAGNI.
- Implement OpenAI-compatible structured model output and a Codex CLI adapter for existing local authentication. Avoid framework orchestration dependencies.
- Trace actual operations with neatlogs guardrail semantics and compact fields. Verify hosted probe and actual workflow separately.
- Use installed Entire CLI/Graph commands and genuine session capture where available; never manufacture checkpoint IDs.
- cfo.ai integration uses its authenticated MCP endpoint and exports an Ari-ready bridge when authentication is absent. A bridge export is not native model completion.
- Record all model usage, failures, and costs with completeness status. Do not claim performance gains from deterministic fixture timings.

## Testing Decisions

- Test externally observable behavior: correct versus invalid artifacts, stale evidence rejection, missing coverage, forgery attempts, selective invalidation, accepted repair, exhausted retries, and clean collaboration.
- Test interpreter capability limits including denied imports/reflection, bounded execution, and malformed output.
- Test payment replay/conflict and discount generalization with trusted oracles and explicit mutants.
- Test provider/MCP request contracts using fake transports and scripts, without credentials or live spend in CI.
- Run actual neatlogs probe and representative trace readback separately from unit tests.
- No existing implementation tests precede this project; use the task contracts as the test oracle. Avoid tests that merely assert internal method calls.

## Out of Scope

Production-wide collusion prevention; formal proofs; hidden model-state access; training a detector; unrestricted candidate shell/code execution; concurrent real payments; deployment; a full MessageBoardAuditBench reproduction; collecting a large benchmark before a complete workflow works; and automatic public submission.

## Further Notes

Research supports checking action outcomes and evidence dependence, not inferring intention from agent agreement. The message-board incident and its retrospective audit motivate retaining evidence; the payment/discount demonstrations are simulated and do not reconstruct that incident.

See the source audit and research note for the papers, limitations, and actual-incident distinction. Financial inputs are observations only when measured; other values remain explicit assumptions. All three sponsor artifacts must be verifiable before claiming complete hackathon integration.
