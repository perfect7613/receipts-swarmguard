# cfo.ai model specification and Ari handoff

Status: model specification only. No customer, revenue, billing, or benchmark results have been observed.

## Commercial decision

Sell a platform subscription with included protected tasks and paid overage. A task is one submitted change contract through acceptance or a recorded terminal failure; retries are part of that task. Display verified outcomes separately from billable task volume.

This creates predictable revenue while making excessive failure/repair costs visible. Model an alternative per-correct-completion offer as a scenario rather than implying failed attempts are free to operate.

Initial customer: an engineering team running coding-agent workflows for application services. Customer value is safer acceptance and less wasted verification/rework. A simulated duplicate-charge example does not establish real-world financial savings; do not turn invented avoided losses into observed revenue.

## Native Model layout

| Page/table | Content |
|---|---|
| Observations | Arm, completed trials, accepted-correct trials, total spend, cost completeness, elapsed time |
| Pricing assumptions | Platform fee, included tasks, overage price, customer growth/churn assumptions |
| Unit economics | Attempted/correct tasks, cost per correct task, marginal runtime COGS, task mix |
| Operating plan | Monthly customers, volume, revenue, COGS, gross profit, OpEx, cash |
| Scenario comparison | Main Receipts versus standard swarm, always-audit, downside |

Model forecast dates: 1 November 2026 through 31 October 2027, monthly grain. Use the actual benchmark date for observations and a clearly separate forecast range. Do not confuse anticipated customer volume with actual revenue.

Use Variables for numeric line items and Dimensions for categories such as Configuration or Customer Tier. Choose either scenario overrides or a Configuration dimension for the comparative economics; if using both, document their separate meanings so the same data is not counted twice.

## Inputs and business equations

All currency is USD unless the actual business chooses a different Model currency. Measured execution prices and forecast assumptions carry source/observation dates.

| Input | Source/status |
|---|---|
| Model spend across attempts/repairs | Provider usage and effective prices; pending |
| Verifier/tool compute and storage | Measured runtime with documented rate basis; pending |
| Correct completion count | Common trusted oracle; pending |
| Platform fee and overage rate | Commercial assumption to choose |
| Customers, new customers, churn | Forecast assumptions; no market evidence yet |
| Support, infrastructure, payroll, opening cash | Explicit operating assumptions |

Equations below express business logic; Ari must validate the actual cfo.ai formula names, scopes, and references before saving them.

```text
Observed cost per correct task = total observed execution spend / correct accepted tasks
Expected task volume = customers * attempted tasks per customer
Expected correct tasks = expected task volume * measured correct completion rate
Overage tasks = max(0, attempted tasks per customer - included tasks per customer) * customers
Revenue = customers * platform fee + overage tasks * overage price
Runtime COGS = expected task volume * measured spend per attempted task
Cost of Revenue = runtime COGS + production hosting + direct support + transaction costs
Gross Profit = Revenue - Cost of Revenue
Gross Margin = Gross Profit / Revenue
Net Burn = operating expenses - Gross Profit
Closing Cash = Opening Cash - Net Burn
```

Runtime COGS uses measured **spend per attempted task**, which already includes retries, verification, and failed completions. Do not multiply that number by retries again or divide by success twice. Cost per correct task is the quality-adjusted evaluation metric; it is not automatically the COGS of each billable attempt.

For a per-correct-completion scenario, Revenue instead depends on expected correct completions × price, while COGS still covers all attempts.

Roll revenue and expense flows with SUM. Cash is an end-of-period balance, not a sum of monthly balances. Annual gross margin is annual gross profit / annual revenue; annual cost per correct task is total cost / total correct tasks. Do not sum or average monthly ratios without their appropriate weights.

Represent zero-denominator metrics as undefined with a visible status. A display formula returning zero through `iferror` must not falsely imply zero cost per correct task. Runway is the first period cash crosses zero in the monthly forecast; if it remains positive, report “beyond modeled horizon.” A simple cash/net-burn ratio can be a secondary steady-state estimate only.

## Scenarios

- **Main — Receipts:** measured C economics, explicit commercial assumptions.
- **Standard swarm:** measured A spend/correct-completion inputs; other common assumptions inherited unless intentionally changed.
- **Always-audit:** measured B inputs.
- **Downside:** lower customer uptake, higher model/verifier costs, lower completion rate, and higher support need; override values explicitly.
- **Per-correct-completion pricing:** alternate billing basis to expose failure costs.

Child scenarios inherit unchanged values from Main. If a benchmark baseline must remain fixed, preserve a snapshot/version and note that a cfo.ai Snapshot remains editable. Save raw benchmark CSV and its digest separately.

Required sensitivities: price versus gross margin, correct completion rate versus cost per correct task, model cost × verification frequency, and customer growth versus cash runway. Illustrative sliders are previews unless their assumptions are actually saved into the Model.

## Paste-ready Ari request

> Build a native cfo.ai business model for Receipts SwarmGuard, a controller that verifies and repairs coding-agent team outputs. Create visible editable tables for Observations, Pricing Assumptions, Unit Economics, Operating Plan, and Scenario Comparison. Use USD and a monthly forecast from November 2026 through October 2027. Separate measured benchmark inputs from commercial assumptions. I will attach a run-metrics CSV; use only rows marked cost-complete for complete cost claims and report incomplete coverage separately. Do not invent missing usage, savings, customer counts, or measured improvements.
>
> Use Main for Receipts and child Scenarios for Standard Swarm, Always-Audit, Downside, and Per-Correct-Completion Pricing. Read exact workspace/table/Variable references first. Create dependent assumptions before derived formulas. Name the Scenario explicitly, dry-run intended writes, then save and read back the calculated values. Use Forecast defaults at monthly grain and preserve actual observations separately.
>
> Model platform fee plus included tasks and overage, attempted volume, correct completed volume, runtime COGS across all attempts and repairs, hosting/direct support, gross profit/margin, OpEx, opening/closing cash, and runway. Runtime spend per attempted task already includes recovery; do not double-count retries. Set appropriate flow/balance rollups and compute annual ratios from annual totals. If there are zero correct completions, show cost per correct task as undefined, not zero. Expose every assumed pricing/growth/cost input for editing. Ask for truly missing commercial inputs rather than inventing them as facts; provisional values must be labeled assumptions.
>
> Reconcile representative monthly and annual cells to the CSV and independent arithmetic. Show the three configuration economics side by side, plus downside sensitivity. Return saved Page/table/Scenario identifiers and a short explanation of assumptions, missing observations, calculation warnings, and verification. Prepare a view-only Page link in the intended Scenario for the submission when sharing is authorized.

## Verification checklist

- [ ] Reconcile total observed spend and correct completions to raw benchmark rows.
- [ ] Verify inferred cost coverage is not presented as complete billing data.
- [ ] Check one monthly revenue/COGS/margin calculation and annual ratio arithmetic.
- [ ] Check period-end cash, cash-crossing month, and no annual balance summation.
- [ ] Read scenario overrides and verify common assumptions inherit correctly.
- [ ] Save exact Page and Scenario IDs and a shareable view/screenshot.
- [ ] Include pricing, costs, revenue, and runway in the submission business plan.

Sources: [financial Model guide](https://docs.cfo.ai/getting-started/build-your-financial-model), [formula authoring](https://docs.cfo.ai/formulas/agent-docs/create-and-update), [verification](https://docs.cfo.ai/formulas/agent-docs/validate-and-verify), [Scenarios](https://docs.cfo.ai/scenarios/understand-scenarios).
