# Sponsor integration runbook

Source-checked 12 October 2026. Commands below are preparation instructions; they were not executed during this planning request. Check installed help and current release capabilities before use.

## 1. neatlogs: application trace and real readback

Use a custom Python orchestration loop. Install the relevant provider extra, e.g. `python -m pip install -U 'neatlogs[openai]'`, in the project's own environment and pin the validated release. [Python SDK](https://docs.neatlogs.com/sdk/python).

Start with `python -m neatlogs doctor --local --json`. After the project SDK key is available through the environment, run `python -m neatlogs doctor --probe --json`. Require the documented Doctor v2 result, Python runtime, schema 2, and pass status. Local pass, hosted probe pass, and real-workflow readback are three separate checks. [SDK Doctor](https://docs.neatlogs.com/sdk/doctor).

The application owns one meaningful workflow root per run. Use `AGENT` spans for roles, wrapped provider clients for LLM calls, `TOOL` spans for broker operations, and `GUARDRAIL` spans for contract/integrity checks. Avoid double wrapping the same provider or tool operation.

Illustrative integration using documented fields:

```python
import json
import os
import neatlogs
from openai import OpenAI

neatlogs.init(
    api_key=os.environ["NEATLOGS_API_KEY"],
    workflow_name="receipts-swarmguard",
)
client = neatlogs.wrap(OpenAI())

@neatlogs.span(kind="WORKFLOW", name="receipts.run",
               capture_input=False, capture_output=False)
def run(run_id):
    with neatlogs.trace("contract.payment_replay", kind="GUARDRAIL") as span:
        span.set_attribute("receipts.run_id", run_id)
        span.set_attribute("neatlogs.guardrail.input", json.dumps({
            "artifact_digest": "<actual digest>",
            "requirement_id": "PAYMENT-REPLAY"
        }))
        passed, reason = trusted_check()  # proposed application function
        span.set_attribute("neatlogs.guardrail.passed", bool(passed))
        span.set_attribute("neatlogs.guardrail.output", reason[:500])
        return {"passed": passed}

try:
    run("<actual run id>")
finally:
    neatlogs.flush(timeout_millis=10_000)
    neatlogs.shutdown(timeout_millis=10_000)
```

This is a sketch, not a complete executable integration: `trusted_check`, real digests, agent spans, model calls, and root trace ID capture still need implementation. The documented guardrail fields are `input`, boolean `passed`, and `output`; additional `receipts.*` fields are application attributes. The dashboard documents Passed/Blocked. Confirm actual appearance before promising a particular red color. [Custom attributes](https://docs.neatlogs.com/sdk/custom-attributes), [span kinds](https://docs.neatlogs.com/sdk/span-kinds).

### Content and context

- Disable automatic capture for functions with large artifacts; export short result summaries and evidence references.
- Keep guardrail payloads compact. The earlier 7.7–9.7 KB loss claim was anecdotal; it is not a verified universal service limit.
- Keep the full claim/message graph in local evidence files. Record its digest and run ID in spans.
- Use a separate run ID for each benchmark trial. Do not reuse one session ID across unrelated trials; retries belong to the same logical task.
- For separate processes, use `neatlogs.inject_trace_context` / `extract_trace_context` rather than the global OTel propagator. Rebind identity separately. Correlate CLI hook traces with controller runs in the manifest when joining a trace is not supported. [Distributed tracing](https://docs.neatlogs.com/sdk/distributed-tracing), [sessions](https://docs.neatlogs.com/sdk/sessions).

### Detections

Create conditions or regex matches on controller-emitted outcomes. Proposed application reason codes: `UNSUPPORTED_APPROVAL`, `STALE_EVIDENCE`, `PROTECTED_ASSET_CHANGED`, `CONTRACT_VIOLATION`, `RECOVERY_STARTED`, `VERIFIED_PASS`. These are not built-in neatlogs detector IDs.

The current feature guide describes regex, condition, PII, and classifier detections. Start with simple structured outcomes; do not assume a custom-function detector from the old conversation is available in the chosen deployment. Detections annotate captured spans; the controller must actually reject/stop the workflow. [Detections](https://docs.neatlogs.com/docs/features/detections).

### Readback credentials and release check

An SDK project key does not authenticate Public API CLI reads. Use human OAuth or an appropriately scoped service-account token bound to the correct project. The current CLI docs target `neatlogs-cli@0.2.1` and explicitly mark it pending publication. Do not assume installation or flags exist; check `npm view neatlogs-cli dist-tags --json` and installed help first. [CLI](https://docs.neatlogs.com/cli), [automation credentials](https://docs.neatlogs.com/cli/automation).

For an available 0.2.1 release, the documented flow is:

```bash
neatlogs --host https://app.neatlogs.com --profile receipts-us --credential-source profile auth login
env -u NEATLOGS_PROJECT_ID neatlogs --host https://app.neatlogs.com --profile receipts-us --credential-source profile projects list
neatlogs --host https://app.neatlogs.com --profile receipts-us --credential-source profile --project '<actual-project-uuid>' traces get '<actual-trace-id>' --json
neatlogs --host https://app.neatlogs.com --profile receipts-us --credential-source profile --project '<actual-project-uuid>' traces spans list '<actual-trace-id>' --limit 25 --json
```

Use an unused or correctly bound profile. On 0.2.0, omit `--credential-source profile` and isolate conflicting environment credentials as its docs prescribe. For EU projects use the corresponding EU ingest and dashboard hosts throughout. Paginate full span readback; 25 spans may not be the whole tree.

**Acceptance:** exact run trace exists in the intended project, is finalized, has expected parent-child relationships and guardrails, and includes numeric usage without duplicate or missing meaningful spans. Flush or HTTP 2xx alone is insufficient. Dashboard/manual readback is valid evidence when CLI auth is unavailable; label missing programmatic checks explicitly.

### Coding-session instrumentation

Optional separately from application tracing: the documented Codex package is `@neatlogs/codex`; install it and use `neatlogs-codex setup --project` with the documented credential setup, then `status`/`doctor`, restart Codex, and trust reviewed hooks. Avoid literal keys in shared commands/logs. Both neatlogs and Entire write `.codex/hooks.json`; verify both hook sets survive setup instead of overwriting the file. [Codex hooks](https://docs.neatlogs.com/integrations/codex).

## 2. Entire: provenance and code impact

Current installation docs show CLI 0.10.5; Graph needs CLI 0.10.0+ and Git 2.36+. Record actual installed versions instead of treating documentation examples as observed environment state. [Installation](https://docs.entire.io/installation), [Graph setup](https://docs.entire.io/guides/graph/set-up-graph).

For this macOS host:

```bash
brew install --cask entireio/tap/entire
entire version
git --version
```

From an actual Git repository, before the implementation session:

```bash
entire enable --agent codex
entire status
entire plugin install graph
entire graph version
entire graph capabilities --json
entire graph init-agents --repo .
```

Commit generated `.entire/graph-agent.md`, `AGENTS.md`, and `CLAUDE.md` as the Graph guide instructs. Keep repository-specific instructions outside managed markers. Restart the coding session so hooks/instructions load. [Enable reference](https://docs.entire.io/cli-reference/enable), [Codex integration](https://docs.entire.io/agents/codex).

Use actual commands to select context:

```bash
entire graph search --repo . --profile full --query 'checkout retry creates duplicate charge' --format json
entire graph impact --repo . --symbol '<actual-payment-symbol>'
```

Save stdout, exit status, queried symbol, and candidate digest. Graph reads the working tree by default; use `--head` for the committed version. Do not add invented `--json` flags to commands whose documented output contract differs. [Graph reference](https://docs.entire.io/cli-reference/graph).

After a genuine captured session changes code and a normal commit is made:

```bash
entire checkpoint list --json
entire checkpoint explain '<actual-checkpoint-id>' --json
entire checkpoint explain '<actual-checkpoint-id>' --transcript
entire why '<actual-source-file>:<actual-line>' --json
```

Metadata JSON does not embed transcript bytes; export transcripts separately if required. A JSON recovery snapshot made by Receipts is not an Entire checkpoint. Codex read-only subagents can be absent from checkpoints, and ephemeral runs may lack full transcripts; use Receipts events for the complete swarm record and disclose provenance gaps. [Checkpoint reference](https://docs.entire.io/cli-reference/checkpoint), [Codex limitations](https://docs.entire.io/agents/codex).

Optional review: configure `entire review` first, then run a configured profile against the actual base ref. Record unresolved findings and reviewer timeouts. It is supporting context, not the trusted acceptance authority. [Review reference](https://docs.entire.io/cli-reference/review).

**Acceptance:** real graph/provenance output is associated with the demonstrated artifact. If sharing checkpoints, verify their sync independently: a successful source push can coexist with failed checkpoint upload. Local Graph output is explicitly accepted evidence by the hackathon page; do not claim remote checkpoints without verifying them.

## 3. cfo.ai: native model and verified scenario values

```bash
codex mcp add cfoai --url https://api.cfo.ai/mcp
codex mcp login cfoai
```

Complete browser authentication, then verify tools are available in the selected harness. If several workspaces exist, call `list_orgs`, choose the correct ID/slug, and pass `org_id` on later calls. [MCP guide](https://docs.cfo.ai/integrations/mcp-server).

Read live tool schemas before building requests. The documented tools include `inspect_table_blocks`, `edit_table_blocks`, `inspect_pages`, `edit_pages`, `inspect_scenarios`, and `edit_scenarios`. A multi-action tool takes exactly one action block; scenario selection is explicit.

1. Create a visible assumptions/observations table and the unit-economics/forecast tables.
2. Declare dependencies before formulas that reference them; related dependent tables can be created in one ordered request.
3. Use `dry_run: true` to validate the intended create/update, then apply once.
4. Read saved tables, copied row references, calculated values, and write warnings.
5. Set monthly forecast rules through `default_formulas.forecast`; undated assumptions use timeless `formula`.
6. Set ratios as percentage values and verify annual ratios calculate from annual totals rather than summing monthly percentages.
7. Preserve exact scenario identity, date window, and grain across read/write/verification.
8. For a committed write with missing readback, inspect the saved revision rather than resending the mutation.

[Create/update formulas](https://docs.cfo.ai/formulas/agent-docs/create-and-update), [validate/verify](https://docs.cfo.ai/formulas/agent-docs/validate-and-verify).

Build Main for the Receipts business and child scenarios for standard swarm, always-audit, and downside economics. Child scenarios inherit unmodified Main assumptions; store differences deliberately and preserve a submission snapshot/version reference. Snapshots stop inheritance but remain editable, so they are not immutable evidence. [Scenarios](https://docs.cfo.ai/scenarios/understand-scenarios).

Share the actual Page with its intended Scenario. Individual formulas/scenarios are not independently shareable. Verify the link externally, save screenshots and key assumptions, and include pricing/cost/revenue/runway. [Sharing](https://docs.cfo.ai/dashboards/share-pages-and-scenarios).

**Acceptance:** native Model tables exist, sampled results reconcile to benchmark cost totals and independent arithmetic, scenario comparisons use the intended overrides, and judge evidence is accessible. A local CSV/JSON fallback is a preparation artifact, not actual cfo.ai use.
