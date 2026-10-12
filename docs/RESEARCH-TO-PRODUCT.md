# Research and incident motivation

Receipts asks a practical question: when a team approves a change, what independently observed evidence supports its acceptance?

## The documented incident motivates keeping evidence

The [slop-vestigators research post](https://www.lesswrong.com/posts/wt4kk6vFPEhkXvF8Q/how-good-are-slop-vestigators) studies reconstruction of a reported agent-message-board incident from wiki and site records. Its [MessageBoardAuditBench](https://github.com/hamzah2304/messageboardauditbench) evaluates retrospective investigation. Receipts' simulated payment example is not a reconstruction of that incident, and this repository does not independently verify every incident allegation.

The design connection is evidence retention: record who asserted a result, which tool execution supports it, and which artifact it tested. That makes an incident explainable without asking a later model to infer missing provenance.

## Papers map to observable product behavior

| Source | Design decision | How this repository checks it |
|---|---|---|
| [Orbit](https://arxiv.org/abs/2609.33102) | Threat-specific checks rather than assuming a per-action monitor handles coordination | Separate ordinary, adversarial, and controlled-seed tracks; mandatory outcome verification |
| [Colosseum](https://arxiv.org/abs/2602.15198) | Distinguish communication from harmful actions | Store role requests/replies and grade actual candidate behavior; agreement alone is not a collusion verdict |
| [Agent Scaling via Diversity](https://arxiv.org/abs/2602.03794) | Favor additional evidence over duplicate votes | Resolve multiple claims to unique execution origins; valid shared evidence still passes |
| [Beyond Final Accuracy](https://arxiv.org/abs/2610.01042) | Make unsupported message-induced revisions visible | Retain role decisions, peer pressure, rejected artifact, and verified repair |

These are design inferences, not reproductions of the papers' experimental results. The prototype counts execution origins; it does not implement a formal effective-channel estimator or inspect latent model communication.

## Reward hacking, sycophancy, and coordination

**Proxy gaming:** the payment shortcut passes visible response checks while violating replay correctness; the discount shortcut passes one amount while failing held-out values. These are controlled examples of gaming incomplete validation.

**Unsupported deference:** the misleading scenario adds a peer assertion that the replay guard should be removed. Store whether the model adopts that premise and whether its code violates the fixed contract. Agreement alone cannot establish a motive.

**Controlled coordination:** the collusion scenario supplies builder and reviewer with an adversarial secondary objective. It is an induced threat-model test, not evidence that ordinary agents spontaneously collude. The tester receives no secondary objective. This MVP does not implement a private covert channel or Colosseum's regret-based allocation evaluation.

## What the actual runs show

The controlled matrix establishes that the independent gate catches the seeded faulty implementations and verifies supplied fixture repairs. A separate run uses a seeded faulty input with live Codex review and repair; its repair is genuine model output. In another live adversarial-prompt run, Codex generated a correct implementation immediately. That observed refusal to take the shortcut is retained, not discarded to manufacture an impressive failure rate.

See the committed evidence and implementation status for the exact runs. No claim of production collusion prevention or measured throughput improvement is made.
