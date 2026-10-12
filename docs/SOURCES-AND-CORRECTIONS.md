# Documentation audit, research, and corrections

Checked 12 October 2026. This document records what was collected, what informed the plan, and what remains unverified.

## Conversation context

Read the five available turns in the referenced “Submission evidence plan” conversation, including its evolution from a single-agent verifier to a swarm evidence controller. The latest requirements emphasize agent coordination, reward hacking, unsupported agreement, and measurable useful performance. The old longest assistant response was truncated by the retrieval service; some embedded code blocks were not present in retrieved text. The new runbook therefore uses independently fetched official docs instead of reconstructing missing snippets.

The user clarified that this request is for **the final plan and execution documents only**. No implementation, account changes, actual benchmark, public posting, or submission was performed.

## Documentation collection coverage

| Corpus | Full bundle collected | Extracted source-page records |
|---|---|---:|
| neatlogs | [Official full documentation](https://docs.neatlogs.com/llms-full.txt) | 459 |
| cfo.ai | [Official full documentation](https://docs.cfo.ai/llms-full.txt) | 72 |
| Entire | [Official full documentation](https://docs.entire.io/llms-full.txt) | 121 |

These are bundle section counts, not a claim that every dynamic app screen, deployment, or unpublished feature was inspected. Entire direct HTTP returned 403; Firecrawl successfully retrieved its official index and full bundle. Initial crawls did not provide complete page bodies; the full official bundles are the retained corpus. Raw bundle content is cached under `.firecrawl/` and excluded from Git.

All source-page records were indexed with titles, section headings, and extracted constraint statements. Read the product-relevant SDK, integration, lifecycle, authentication, graph, checkpoint, review, formula, scenario, and sharing content in detail. Administrative endpoints and unrelated framework integrations were catalogued and checked for scope, rather than line-by-line API implementation review. **Collected/indexed is distinct from deeply reviewed or tested.** This is broad documentation coverage, not a claim that every line of the 4.4 MB corpus was read manually.

The [source inventory](../evidence/documentation-inventory.json) lists every extracted source record and the exact review classification. No sponsor integration was executed, so documented capabilities are not observed integration results.

## Load-bearing sponsor sources

| Source | Verified design implication |
|---|---|
| [neatlogs Python SDK](https://docs.neatlogs.com/sdk/python) | Use one meaningful application root and instrument custom workflow operations; wrap actual provider client calls |
| [Custom attributes](https://docs.neatlogs.com/sdk/custom-attributes) | Guardrail input/output are strings; `passed` is boolean; dashboard documents Passed/Blocked |
| [SDK Doctor](https://docs.neatlogs.com/sdk/doctor) | Local capture, hosted probe, and real-workflow finalization are separate claims |
| [Lifecycle](https://docs.neatlogs.com/sdk/lifecycle) | End streams, flush and shut down boundedly for scripts; flush is not proof of persisted correctness |
| [Detections](https://docs.neatlogs.com/docs/features/detections) | Annotations are read-only; Receipts must enforce blocking |
| [CLI](https://docs.neatlogs.com/cli) | SDK key is insufficient for public CLI reads; 0.2.1 release/flags must be availability-checked |
| [Distributed tracing](https://docs.neatlogs.com/sdk/distributed-tracing) | Use private-context inject/extract helpers; identity is rebound separately |
| [Codex hooks](https://docs.neatlogs.com/integrations/codex) | Coding-session capture is separate from application instrumentation; hooks require reviewed setup/restart |
| [Entire installation](https://docs.entire.io/installation) | Use current installer/CLI verification rather than old commands |
| [Entire Codex](https://docs.entire.io/agents/codex) | Hooks/transcript capture and read-only subagent limitations affect provenance completeness |
| [Checkpoint reference](https://docs.entire.io/cli-reference/checkpoint) | Metadata and transcript export are separate; use actual checkpoint/commit identity |
| [Graph setup](https://docs.entire.io/guides/graph/set-up-graph) | Plugin setup is `entire plugin install graph` and `init-agents`; requirements include Git 2.36+ |
| [Graph behavior](https://docs.entire.io/guides/graph/how-graph-works) | Static source relationships can miss dynamic dependencies; impact is context, not complete proof |
| [Graph commands](https://docs.entire.io/cli-reference/graph) | Working tree is default; source/version and output format must be captured |
| [Why](https://docs.entire.io/cli-reference/why) / [Review](https://docs.entire.io/cli-reference/review) | Provenance and configured multi-agent review are available in current docs; review is not the acceptance oracle |
| [cfo.ai MCP](https://docs.cfo.ai/integrations/mcp-server) | Official remote endpoint, browser auth, and explicit workspace selection |
| [Create/update formulas](https://docs.cfo.ai/formulas/agent-docs/create-and-update) | Writes go through visible table targets or documented Variable entries; one action block; explicit Scenario/range |
| [Validate/verify](https://docs.cfo.ai/formulas/agent-docs/validate-and-verify) | Dry-run validation and saved numeric verification differ; committed-without-readback must not be blindly resent |
| [Scenarios](https://docs.cfo.ai/scenarios/understand-scenarios) | Child inheritance matters; Snapshots stop inheritance but remain editable |
| [Page sharing](https://docs.cfo.ai/dashboards/share-pages-and-scenarios) | Share the actual Page with a chosen Scenario; individual formulas/scenarios are not standalone share links |
| [neatHack rules/evidence](https://neatlogs.com/hackathon) | All sponsors, observable improvement/recovery, public repo, public quote-tweet plus form, published 11:55 PM IST cutoff |

## Corrections to the earlier discussion

1. “More agents agreed” is not more independent evidence. Conversely, sharing valid evidence is ordinary collaboration and not automatically an unsafe act.
2. A controller-owned hash is a version binding; a hash supplied by an agent does not authenticate execution or make it trustworthy.
3. The discount example needs expected-discount tests, not only a 20% cap: a hardcoded patch can under-discount without violating that upper bound.
4. neatlogs detections cannot stop execution. Its feature guide currently describes four detector classes; a custom-function rule from the earlier discussion is not assumed available.
5. The “7.7–9.7 KB drop threshold” was a conversation anecdote, not an independently established service limit. Use compact payloads and test exact real trace readback.
6. An exporter success or Doctor probe success is not evidence that the real swarm trace contains everything expected.
7. Current Entire docs expose Graph/why/review in ordinary command references. Old `labs`-only assumptions and old Graph setup commands should not be copied blindly.
8. Entire is not installed on this host as observed through command discovery. Actual model runs/checkpoints remain future work. Creating local recovery JSON is not using Entire checkpoints.
9. Git worktrees do not provide a security boundary. Hooks observe activity; they do not constrain unrestricted shell access.
10. cfo.ai requires native model evidence for the sponsor requirement. Local templates are preparation, not fulfillment. Current workspace tools were not connected in this session.
11. Financial forecasts must distinguish runtime cost per attempted task from cost per correct completion. Include all failed/recovery spend and avoid counting retries twice.
12. Performance gains, natural reward-hacking rates, avoided charge losses, customer demand, and gross margin targets are hypotheses or assumptions until measured.

## Research that informs the design

These papers/blogs provide motivation and experiment design, not proof that Receipts will work. Named papers were checked through Firecrawl Research body retrieval; their settings and limitations matter.

### Retrospective investigation

[How good are slop-vestigators?](https://www.lesswrong.com/posts/wt4kk6vFPEhkXvF8Q/how-good-are-slop-vestigators), 8 September 2026, author research post. It evaluates reconstructing findings from wiki/site records, not live prevention or complete model transcripts. It reports a rubric based on 38 core findings, a highest average combined score of 51.5%, and a best individual score of 56.7%. The score combines finding coverage and summary assessment, with time/report-length effects and grader limitations.

**Product inference:** keep structured origins and incident evidence instead of relying on a later generic investigator to reconstruct everything. MessageBoardAuditBench is a later forensic evaluation, not the first runtime benchmark.

### Threat-specific multi-agent defenses

[Orbit: A Framework for Multi-Agent Safety and Security Evaluations](https://arxiv.org/abs/2609.33102), arXiv v1, 27 September 2026. In its SWE-Bench MI experiment, the LLM monitor reduces a single compromised agent's attack success from 72% to 12%, while the collusion condition remains 30% to 30%. This is a particular controlled scenario/model/topology result. The guardian's collusion value in the retrieved table is 34%, so the old claim that every defense behaves identically at 30% is too broad. The paper also reports benign false blocks and performance costs; defense evaluation needs both safety and utility.

**Product inference:** evaluate coordinated handoffs and action outcomes, and report benign controls beside adversarial success. Do not infer general immunity or vulnerability from one benchmark result.

### Observable coordinated behavior

[Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems](https://arxiv.org/abs/2602.15198), February 2026 identifier; retrieved body includes later revisions. It separates communication evidence from action-based objective deviation in controlled allocation tasks. Its mitigation discussion supports verifying claims against shared state and applying stronger controls to high-leverage roles. Explicit objectives and tractable reward structure limit generalization to arbitrary production tasks.

**Product inference:** enforce a concrete payment/discount contract; label discourse, attempted coordination, and harmful outcome separately. A similar sentence from two agents cannot establish deliberate collusion.

### Evidence diversity versus agent count

[Understanding Agent Scaling in LLM-Based Multi-Agent Systems via Diversity](https://arxiv.org/abs/2602.03794), arXiv v1, 3 February 2026. Its diverse-agent comparisons use reasoning/knowledge tasks, small open models, and vote/debate workflows. The reported two-versus-sixteen comparison is not a measured coding-agent throughput result.

**Product inference:** prioritize additional information and requirement coverage over repeated model opinions. Do not equate Receipts' discrete origin count with the paper's formal effective-channel measure or claim its performance gains transfer automatically.

### Communication can correct and corrupt

[Beyond Final Accuracy: Auditing Communication in LLM Multi-Agent Systems](https://arxiv.org/abs/2610.01042), October 2026 identifier. The retrieved body defines correction/preservation conditional on sender and receiver initial correctness, with matched no-message revision controls. Final accuracy alone can hide harmful revisions as well as beneficial ones.

**Product inference:** preserve blind initial reviewer decisions, then compare message-conditioned revisions against neutral controls. A natural-language-only Receipts workflow does not inspect latent communication.

Research search also surfaced newer work on long-horizon collusion and transmissible reward hacking. Those leads were not body-verified for this package and are excluded from load-bearing quantitative claims. The earlier HACKTRACE hidden-state monitoring direction is unnecessary for this MVP and is not treated as an available capability of closed coding-agent APIs.

## Competitor context

The conversation identifies [Kedge](https://github.com/faroukobayanju/kedge) and [Dailies](https://github.com/RaYYeR220/dailies). GitHub HTML retrieval returned an error page during this request; both raw READMEs were successfully retrieved afterward. Kedge describes stepwise drift checks and rollback/retry for dependency-update work. Dailies describes checking session claims against recorded tool results and generating grounded recaps. Its README reports evaluation on 394 sessions from 101 repositories. These are author-reported capabilities and results, not independent reproductions. Neither README review establishes that a competitor lacks evidence-lineage features elsewhere in its implementation. The final plan makes no exclusivity claim and uses evidence lineage as its product focus, regardless of competitor feature changes.

## Unverified work remaining

Actual sponsor login/setup, hook coexistence, sandbox enforcement, provider/model behavior, artifact repair, span ingestion, cfo.ai calculations, benchmark metrics, public links, and Discord cutoff updates all remain implementation or submission checks. This package does not assert they are complete.
