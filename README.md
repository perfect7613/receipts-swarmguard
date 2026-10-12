# Receipts SwarmGuard — planning package

Prepared 12 October 2026 (IST). This workspace contains the final plan and execution documents requested by the user. Implementation and account setup have not been performed.

**Product:** a controller that checks whether a coding-agent team's approvals are supported by fresh, independently executed evidence, blocks unsafe acceptance, and repairs affected work.

**Demo:** three agents approve a checkout retry change that passes visible tests but allows duplicate charges. Receipts identifies their shared evidence, runs trusted replay tests, rejects the change, and verifies the repair.

Read in this order:

1. [Final product and architecture plan](docs/FINAL-PLAN.md)
2. [Sequenced build checklist](docs/BUILD-CHECKLIST.md)
3. [Sponsor integration runbook](docs/SPONSOR-RUNBOOK.md)
4. [Benchmark and measurement protocol](docs/BENCHMARK-PROTOCOL.md)
5. [Business model and Ari prompt](docs/CFO-MODEL.md)
6. [Demo and submission evidence](docs/SUBMISSION-PLAN.md)
7. [Documentation audit and research](docs/SOURCES-AND-CORRECTIONS.md)

[Evidence manifest template](evidence/manifest.template.json) and [metrics template](evidence/metrics.template.csv) are deliberately unpopulated. Missing results must not appear as zero or as measured gains.

The full official documentation bundles and page inventories are cached locally in `.firecrawl/` (ignored). The source audit explains collection coverage and review depth; downloading a page is not evidence that an integration works.
