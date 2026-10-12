# Real-world expansion and evaluation

Updated 12 October 2026. This is the next execution specification, not a claim that the external evaluations have run.

## Product decision

Build an acceptance gate for agent-produced artifacts. A coding agent proposes a patch; reviewers cite evidence; a separate verifier checks the exact patch against a fixed contract. The gate records what was checked, blocks unsupported acceptance, and allows bounded repair. The customer is a team using coding agents to resolve repository issues and reviewing their output in CI.

The useful distinction is **approval versus independently supported completion**. Avoid promising a general collusion detector: shared evidence can be valid, and correlated mistakes need not be intentional. A failed test, protected-file edit, or unverifiable assertion is an observable event; intent is a separate research question.

## Real tasks and their oracles

| Workflow | Concrete task | Independent acceptance evidence | Boundary |
| --- | --- | --- | --- |
| Repository issue resolution, first priority | Agent changes a retry handler or repairs a parser | Patch replay at the recorded base commit; trusted regression and task tests; untouched verifier; logs and artifact hashes | Tests cover a contract, not all possible behavior |
| Data reconciliation, later | Agent explains a discrepancy between invoice and ledger exports | Deterministic recomputation from immutable input snapshots; sums, joins, missing IDs and duplicate checks | Accounting policy needs explicit human-approved rules |
| Operational runbook changes, later | Agent changes a deployment configuration | Schema checks, disposable staging checks, rollback rehearsal and explicit environment identity | Staging success does not authorize production deployment |
| Research evidence, later | Agent produces a cited technical report | Resolve each claim to a source and version; verify quotations and numerical provenance | Source support is not proof the underlying research is correct |

Do the repository workflow first. The data, operations and research rows are designs, not implemented features. Simulated payment and discount fixtures remain the fastest demonstration of why acceptance needs independent checks.

## Flagship capability benchmark: SWE-Bench Pro V2

Use the current [official V2 task release and locked protocol](https://github.com/scaleapi/SWE-bench_Pro-os/blob/main/v2/README.md), rather than silently treating the original Pro release or Verified as interchangeable. V2 contains 642 tasks across 11 repositories, packaged with Harbor tasks and verifier tooling. Those sizes are release facts, not Receipts results.

1. Pin the benchmark repository commit, Harbor version, container image digests, agent/model configuration, prompt templates and Receipts commit. Verify the release checksums and record the checks performed.
2. Predeclare a feasibility subset spanning repositories and languages. Use up to 30 tasks initially, selected before observing model outcomes; publish the selection algorithm, seed and IDs. A pilot score is a subset result. HARD-51 is a separate stress track, not a representative substitute.
3. Run the release's reference-solution and no-op controls for the selected tasks. Quarantine failed controls with reasons before the comparison; publish the original and evaluable denominators.
4. Use the official locked agent protocol: restrict agent network access to the model endpoint, keep hidden verifier material outside worker context, and capture the final patch. Run the supplied network/history probes.
5. Replay every final patch into a fresh benchmark image using the official regrader and unchanged verifier. Publish original agent-environment outcomes and fresh-environment outcomes. Only the latter supports the resolution claim.
6. Compare standard review, always-audit, and Receipts using the same model, task instructions, initial patches where appropriate, timeout and declared total token budget. Charge verifier and repair resources to their respective arm. Report a paired fixed-patch gate comparison separately from end-to-end agent solving; they answer different questions.
7. Keep errors, timeouts, empty patches and missing results in the attempted denominator. Permit infrastructure retries only under a predeclared policy and retain every attempt. Report rates with uncertainty and paired outcome counts, plus median/p95 time, tokens and complete measured cost when available.

The upstream README provides Harbor/Modal commands for oracle, no-op, locked agents and `patch_replay:PatchReplayAgent`. Run them from a pinned upstream checkout. Receipts does **not** currently wrap Harbor or authenticate its execution receipts. Do not present the legacy adapter's policy checks as V2 verifier equivalence. Cloud benchmark execution requires an authenticated environment and incurs resource costs; no cloud run was started here.

## Implemented compatibility bridge: SWE-bench Verified

`receipts benchmark prepare` accepts official prediction JSON/JSONL and a task snapshot. It creates worker-safe task instructions, normalized predictions, patch/base/task bindings, a unique run ID and an official harness command. Workers do not receive gold/test patches or grading scripts. The implementation-only patch profile flags protected evaluation/configuration paths; legitimate authorized test changes need a different policy.

```bash
uv run receipts benchmark prepare --predictions predictions.jsonl \
  --tasks tasks.json --dataset-revision DATASET_COMMIT --output artifacts/batch
uv run receipts benchmark audit --predictions artifacts/batch/predictions.jsonl \
  --manifest artifacts/batch/manifest.json --report results.json \
  --output artifacts/batch/audit.json
```

The audit rejects stale prediction files and inconsistent report IDs/counts. Missing outcomes remain in the denominator. An operator-imported report remains explicitly unauthenticated, even if it reports a pass. The generated harness command does not enforce the recorded dataset revision: the execution operator must pin and record the actual dataset and harness versions before trusting results.

The committed [preflight evidence](../evidence/swebench-preflight.json) checks five real upstream reference patches from the first five Astropy rows for task identity and patch-policy compatibility. These are reference solutions, not model solutions, and were not executed. Docker is unavailable on this host. [OpenAI's Verified audit](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) documents test and contamination concerns; use this bridge for compatibility and regression tooling, not a frontier capability headline.

## Reward-hacking and verifier-hardening tracks

[EvilGenie](https://arxiv.org/abs/2511.21654) distinguishes benchmark-visible success from held-out task performance and includes environments with opportunities to exploit rewards. Use its official tasks/harness in a separate experiment, preserving its labels and conditions. Report visible success, held-out success, observable exploit attempts, successful exploits and legitimate errors separately. A held-out failure alone does not establish reward hacking.

[Hardening Agent Benchmarks with Adversarial Hacker-Fixer Loops](https://arxiv.org/abs/2606.08960) motivates a three-role development loop: an attacker proposes verifier exploits, a maintainer fixes the verifier, and a legitimate solver checks that the fix still permits correct solutions. For Receipts, start with stale receipts, forged origins, test edits, report fabrication, output-parser tricks and skipped-task accounting. Reserve unseen attack templates and a different attacker configuration for the final evaluation. Approve verifier revisions offline; freeze them before the measured run. A gate that rejects everything is not a successful defense.

## Multi-agent coordination track

[Emergent Collusion in Long-Horizon LLM Agent Interaction](https://arxiv.org/abs/2609.24967) studies repeated interactions, memory and reward/protocol conflicts. Its conditions are not an observed production coding-agent incident. Add repeated episodes with and without retained memory and vary communication visibility, then label protocol violations against a predefined rule. Preserve full logs privately for audit and share redacted evidence where appropriate.

Keep the previously documented Orbit and Colosseum experiments as distinct research contexts. Do not pool paper rates, scripted attacks, seeded live repairs and ordinary live tasks into one “collusion prevented” statistic. Test shared valid evidence as a clean control. Record origin sharing and failed requirements separately from inferred coordination intent.

## Minimal build order

1. Finish trusted external execution capture: controller-owned environment, pinned identities, untouched verifier, captured exit status/output, fresh-patch replay and durable receipt binding. The current report importer is deliberately not this component.
2. Attach that executor to the acceptance ledger; invalidate receipts when patch, base, contract, environment or verifier changes. Authenticate the executor independently of the proposing agent.
3. Run release controls and the predeclared pilot. Preserve all outcomes before writing comparative claims.
4. Add verifier attacks and legitimate controls. Measure false acceptance and false rejection alongside successful repair and resource cost.
5. Extend to retained-memory teams only after the artifact gate and ordinary-task evaluation work reliably.

neatlogs provides trace and usage evidence; Entire links reasoning/provenance to changes; cfo.ai models measured review/verifier/repair economics. None substitutes for a trusted correctness check. Keep native cfo.ai authoring and missing cost observations explicitly pending.
