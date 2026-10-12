# Demo and submission evidence plan

Prepared 12 October 2026. Submission itself is outside this planning-only request.

## Official obligations

The [official neatHack page](https://neatlogs.com/hackathon) says:

- Build an agent or team that completes a substantial task end to end.
- Use neatlogs and Entire to build/improve it, and cfo.ai to plan the business.
- Include before/after runs and compared measurements, failure recovery, sponsor evidence, public-building links, and a public repository with hackathon-dated commits.
- Publicly quote-tweet the official launch post with the demo and `@neatlogs`, `@EntireHQ`, and `@arithecfo`, then complete the three-step submission form. Both are required.
- Published submission window: 12 October 2026, 7:00–11:55 PM IST. Latest official Discord cutoff updates take precedence. Discord changes have not been checked in this request.

Judging weights: agent 30%, sponsor use 25%, demo 20%, building in public 15%, usefulness/originality 10%. Prioritize a working task, inspectable sponsor outputs, and a clear demonstration.

## The three-minute demo

This is an editorial target, not a verified platform video-length requirement. Record a completed run; use its actual numbers.

| Time | What to show | Spoken point |
|---|---|---|
| 0:00–0:20 | Checkout task and replay contract | “A retry should return the same receipt and never charge twice.” |
| 0:20–0:45 | Builder/reviewer/tester approvals and passing visible tests | “All three agents approve the patch.” |
| 0:45–1:10 | Three claim nodes resolving to one narrow execution | “They share the same incomplete evidence.” |
| 1:10–1:35 | Trusted replay produces two ledger charges; guardrail blocked | “The independent check finds the real defect and blocks acceptance.” |
| 1:35–2:00 | Invalidated approvals, repair diff, fresh trusted pass | “Receipts repairs the affected work and verifies one charge on replay.” |
| 2:00–2:20 | Real neatlogs trace and Entire checkpoint/Graph output | “Here is the failed check, recovery, code origin, and affected functions.” |
| 2:20–2:45 | A/B/C measurements and native cfo.ai scenario table | “These are measured run economics and the business assumptions they inform.” |
| 2:45–3:00 | Accepted artifact and evidence index | “Every claim links to an execution, artifact, and result.” |

For a seeded attempt, say “controlled failure scenario” on screen. For observed live behavior, say how many trials were run and retain failures. If benchmarks are incomplete, replace the gain chart with raw observed counts and explicitly label sample size.

Avoid screen text claiming “collusion detected” for a shared-source graph alone. Use “shared evidence,” “missing replay coverage,” and “contract violated.” The adversarial coordination case gets its own clearly labeled optional segment.

## Minimum evidence bundle

| Claim | Required evidence | Finish check |
|---|---|---|
| Task completed correctly | Contract version, accepted artifact, trusted oracle result | Same digest in all three |
| Unsafe candidate blocked | Candidate patch, failed replay output, gate decision | No accepted verdict for failed artifact |
| Agents reused evidence | Authenticated claim/message graph and original execution IDs | Three endorsements visibly resolve to original source |
| Recovery worked | Failed attempt, repair event/diff, fresh verification | Model repair versus fixture repair distinguished |
| neatlogs used | Real before/after trace IDs/links or screenshots, finalized span trees | Expected guardrails, calls, usage readable |
| Entire used | Actual Graph output and/or actual checkpoint evidence | Correct source/version; no fabricated checkpoint |
| cfo.ai used | Native business Page/table/Scenario, formulas, screenshots/share link | Pricing, costs, revenue, runway covered |
| Performance changed | Protocol, raw rows, aggregate code/results, sample size | Defined denominators and cost completeness |
| Built during event | Public repo history and dated commits | Dates accurate, no rewritten/backdated evidence |
| Built in public | Public posts with #neatHack | Actual URLs |
| Submission complete | Quote-tweet URL and form confirmation | Both verified |

Suggested implementation outputs: `evidence/runs/<run-id>/events.jsonl`, `claims.json`, `artifact.patch`, `verification.json`, `usage.json`, `entire/`, `neatlogs/`, `benchmark/results.csv`, `benchmark/summary.json`, and `cfo/`. These are intended future outputs; this package currently contains templates only.

## Submission narrative draft

**Title:** Receipts SwarmGuard

**Tagline:** Independent evidence and recovery for coding-agent teams.

**Problem:** A coding-agent team can agree that a change works while all its approvals depend on the same incomplete test. In payment code, that can mean a retry looks successful while charging twice.

**Solution:** Receipts records the origin and artifact version behind each approval, requires trusted checks for important contracts, invalidates downstream claims when a candidate fails, and verifies the repair before acceptance.

**What the demo shows:** [Insert actual fixture, controlled/live label, rejected result, repair result, sample size, and accessible evidence links after execution.]

**Sponsor use:** neatlogs records the workflow, checks, and recovery; Entire records real coding provenance and supplies code-impact context; cfo.ai translates execution economics into editable pricing, cost, revenue, and cash scenarios.

**What is distinctive:** Evidence dependence across agent handoffs, fresh artifact-bound acceptance, and recovery that preserves unaffected work.

**Limits:** The initial evaluation covers [actual fixtures and conditions]. The system enforces the defined contracts and execution boundary; it does not prove intent or eliminate all possible coordinated behavior. Financial forecasts are assumptions informed by [actual measurements].

## Quote-tweet draft

> Three AI agents approved a checkout fix that could charge a customer twice.
>
> Receipts SwarmGuard traces their shared evidence, blocks unsafe acceptance, and verifies the repair.
>
> [Insert measured result or say “controlled demo”] · [demo link] · [public repo]
>
> Built with @neatlogs @EntireHQ @arithecfo #neatHack

Do not post the draft with placeholders or treat it as authorized messaging. This request is planning only.

## Final preflight

- [ ] Repo, demo, traces/screenshots, Entire evidence, and cfo.ai Page are accessible to judges.
- [ ] Results use real values or are labeled unmeasured; no placeholders disguised as zero.
- [ ] Every artifact digest and run ID reconciles across the evidence index.
- [ ] Controlled behavior and actual model behavior are separated.
- [ ] Costs include failed attempts and recovery, with source dates and completeness.
- [ ] Demo discloses limitations and uses observed outcomes.
- [ ] Official launch post and Discord cutoff have been checked.
- [ ] Quote-tweet and submission form both have confirmed completion evidence.
