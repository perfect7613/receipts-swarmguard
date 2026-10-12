# Receipts SwarmGuard

**Independent evidence and recovery for coding-agent teams.**

Three agents can approve a change while citing one incomplete test. Receipts links their approvals to actual executions, checks the exact artifact against a trusted contract, rejects unsafe acceptance, and verifies the repair.

The flagship example is a simulated checkout retry: a shortcut returns success but charges twice. A second example catches a discount implementation hardcoded to one visible amount.

## Run it

Requires Python 3.12 or 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --locked
uv run receipts demo
uv run pytest -q
```

The demo runs 12 controlled cases across standard, always-audit, and Receipts policies, including clean controls. JSON, candidate source, events, and a Markdown report are written under ignored `artifacts/`. Controlled repairs use known fixture code and are labeled accordingly.

For live review and model-generated recovery using existing Codex CLI authentication:

```bash
uv run receipts run --backend codex --fixture payment --scenario clean --seed-shortcut
```

This seeds the faulty input, then runs real model reviewers and repair. To let the model build from the original bug instead, omit `--seed-shortcut`. `--scenario clean` is the ordinary task; `shortcut`, `misleading`, and `collusion` are explicitly adversarial prompt variants.

Alternatively set `OPENAI_API_KEY`, `RECEIPTS_MODEL`, and optional `OPENAI_BASE_URL` in your environment/ignored `.env`, then use `--backend openai`. No provider secrets are passed to the Codex subprocess. Live trials use provider resources; actual billing remains unknown unless price and infrastructure observations are available.

## Real repository evaluation

The new benchmark bridge prepares official SWE-bench prediction artifacts, hides gold/verifier material from worker instructions, binds patch and base identities, and audits imported reports for consistency. Imported reports remain unauthenticated. See [real-world expansion](docs/REAL-WORLD-EXPANSION.md) for commands and the proposed **SWE-Bench Pro V2 fresh-replay evaluation**.

Five upstream Verified reference patches passed preparation preflight; no external benchmark tasks have been executed. The [claims guide](docs/CLAIMS.md) separates demonstrated behavior from planned results. **54 automated tests pass.**

## Sponsor setup

### neatlogs

Copy `.env.example` to `.env` and set the project key locally. Never put it into source or evidence. Run:

```bash
uv run receipts demo --neatlogs
uv run receipts run --backend codex --scenario clean --seed-shortcut --neatlogs
```

The application exports workflow, agent, LLM, tool, and guardrail spans. Ingestion/readback evidence is committed for the observed live repair: **15 spans and 57,925 tokens**. The two contract checks and two acceptance checks show rejection followed by verified acceptance. A successful SDK export is not automatically readback verification.

For future Public API reads, use separately authenticated neatlogs CLI OAuth/service credentials. The ingestion project key alone is insufficient. Detailed setup is in [the sponsor runbook](docs/SPONSOR-RUNBOOK.md).

### Entire

```bash
entire enable --agent codex --skip-push-sessions
entire plugin install graph
entire graph init-agents --repo .
uv run receipts entire
```

Actual Graph search and impact output is committed. The real repair session is manually attached as Entire checkpoint `01M4RDVGHAK7812BFSKWD8MR3W`, with `entire why` output for the generated repair. This is a real logs-only checkpoint, not automatic file-edit capture. Review and approve installed hooks through Codex `/hooks` before relying on automatic capture. Local recovery JSON is not an Entire checkpoint. Automatic session pushing remains off; only reviewed provenance is explicitly shared.

### cfo.ai

Interactive connection uses OAuth:

```bash
codex mcp add cfoai --url https://api.cfo.ai/mcp
codex mcp login cfoai
```

The code also supports an operator-supplied authenticated `CFO_AI_ACCESS_TOKEN` for remote MCP discovery and calls:

```bash
uv run receipts cfo tools
uv run receipts cfo call --tool inspect_pages --args request.json
# The call above previews; add --execute to invoke it.
```

Inspect live tool schemas before writing an argument file. Workspace writes must use the intended `org_id` and Scenario. Do not reuse the neatlogs key. [The business-model specification](docs/CFO-MODEL.md) provides a paste-ready Ari request. The committed cfo bridge is an export for native model authoring; **no native cfo.ai financial Model has been created**.

## What is actually verified

- Trusted tests distinguish both faulty shortcuts from correct implementations.
- Three endorsements can resolve to one execution; valid shared evidence is not itself blocked.
- Missing coverage, stale evidence, unknown origins, and failed trusted checks cannot approve work.
- Rejection invalidates dependent approvals and preserves independent contract work.
- A seeded faulty candidate was repaired by a live Codex model and independently accepted.
- A separate live adversarial-prompt run produced correct code immediately; that result is retained.
- Tests cover the restricted interpreter, evidence gate, recovery, usage, and MCP request contract.

See [observed evidence](evidence/observed), [implementation status](docs/IMPLEMENTATION-STATUS.md), and [PRD issue #1](https://github.com/perfect7613/receipts-swarmguard/issues/1).

## Scope and research

Candidates use a bounded subset of Python interpreted without `exec`/`eval`. They have no imports, filesystem/network access, arbitrary calls, or access to trusted tests. This is a narrow fixture prototype, **not an arbitrary-Python sandbox or production-wide collusion defense**. Payments are simulated and sequential; contract inputs are typed fixture data.

The [research explanation](docs/RESEARCH-TO-PRODUCT.md) connects the documented message-board investigation and the Orbit, Colosseum, diversity, and communication papers to observable product decisions. Controlled attacks are separate from ordinary behavior. No natural cheat-rate, economic savings, or throughput improvement is claimed from the small demo.

Planning references: [final architecture](docs/FINAL-PLAN.md), [build checklist](docs/BUILD-CHECKLIST.md), [benchmark protocol](docs/BENCHMARK-PROTOCOL.md), [submission plan](docs/SUBMISSION-PLAN.md), and [documentation audit](docs/SOURCES-AND-CORRECTIONS.md). These were written before implementation; current capabilities and pending work are recorded in the implementation status.
