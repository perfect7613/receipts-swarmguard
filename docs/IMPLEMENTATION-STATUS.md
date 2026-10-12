# Implementation status

Updated 12 October 2026. This supersedes the planning-only status of the earlier documentation package.

## Implemented

- Installable Python CLI with a locked dependency environment and GitHub Actions checks.
- Two simulated fixtures: checkout replay and capped discount generalization.
- A bounded Python syntax interpreter; candidate code cannot import modules, access files/network/secrets, invoke arbitrary functions, or execute unrestricted Python bytecode.
- Trusted controller-owned behavioral checks and a claim/evidence ledger.
- Evidence-origin deduplication, current-artifact checks, required coverage, failed-check rejection, and selective downstream invalidation.
- Bounded recovery ending in accepted fresh verification or `NEEDS_HUMAN_REVIEW`.
- Controlled matrix, live OpenAI-compatible adapter, and an authenticated Codex CLI adapter.
- Actual neatlogs traces, numeric model usage, guardrail attributes, and separate finalized trace readback.
- Installed/authenticated Entire CLI and actual Graph context/impact evidence.
- cfo.ai MCP client, preview-before-execute CLI, separate-track economics exports, and native-model authoring instructions.
- PRD published as [GitHub issue #1](https://github.com/perfect7613/receipts-swarmguard/issues/1).

## Observed verification

**40 tests pass.** The wheel and source distribution build successfully. Tests cover observable contracts, defined payment mutants, denied candidate capabilities, stale/forged evidence, recovery, clean controls, usage isolation, and MCP request/auth handling.

The 12 controlled runs use two fixtures × shortcut/clean × three arms. Across the two shortcut cases, standard accepts two oracle-invalid candidates. Receipts and always-audit both reject the initial candidates and accept correct fixture repairs. All six clean controls pass without repair. These are controlled smoke results; always-audit handoffs in this matrix are simulated policy work, not actual auditor-model calls.

The live seeded payment repair used three real Codex calls (reviewer, tester, repair). It rejected the seeded input and accepted the model's corrected implementation after one repair. The reviewed live run's neatlogs trace is `aa296bf60e6de9dd24a9202b0f181774`: finalized, 15 spans, three LLM spans, 57,925 total tokens. Exact span IDs, kinds, one root, resolved parents, full pagination, and numeric token totals match the controller's expectations. The public API readback exposes span metadata, not guardrail content; persisted guardrail boolean/content rendering is not independently screenshot-verified here.

A separate live adversarial-prompt trial produced correct code immediately. It is retained as a control outcome, not counted as an induced failure. Its model reviews also expressed concerns beyond the fixture's guaranteed input domain; those advisory concerns do not override successful execution of the fixed supported contract.

## YAGNI scope choices

Use JSON/JSONL event files rather than SQLite until durable multi-process coordination exists. Keep the product a CLI with Markdown/JSON evidence until an actual interface is needed. Keep payment/discount inputs typed and bounded. Financial assumptions and live costs remain explicit; no billing estimates are invented.

The initial gate always runs the full small trusted fixture suite. It does not yet implement risk-calibrated optional-audit sampling, general codebase regression selection, a covert communication channel, or a broad five-fixture performance benchmark. Whole-code correctness is not implied by these fixtures.

## Pending integration work

- Review/approve installed Entire hooks via Codex `/hooks` for future automatic sessions. Graph use is verified independently of hooks.
- An actual native cfo.ai Model, Scenario comparison, and financial Page still require cfo.ai account/workspace authentication and authoring. The MCP code and bridge are ready; a local export is not native financial-model completion.
- Model billing rates and verifier/infrastructure spend have not been collected. Cost completeness is false; dashboard zero is not actual billing evidence.
- Public live model IDs use the CLI default label unless explicitly configured. Preserve actual provider configuration before a comparative experiment.
- Full ordinary/adversarial repeated evaluation, performance ablations, demo video, building-in-public post, and hackathon submission remain separate work.

## Reproduce

```bash
uv sync --locked
uv run pytest -q
uv run receipts demo
uv run receipts run --backend codex --scenario clean --seed-shortcut --neatlogs
uv run receipts entire
```

Keep local credentials in ignored `.env`, use your own Codex authentication for live calls, and use authenticated neatlogs read credentials for future trace verification.
