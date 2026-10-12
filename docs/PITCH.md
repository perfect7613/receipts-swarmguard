# Pitch: agent collusion and reward hacking

## One sentence

Receipts SwarmGuard checks whether an agent team's success is real: it links approvals to independent evidence, blocks reward-hacking shortcuts and coordinated unsupported acceptance, and verifies the repair.

## 30-second pitch

Adding more agents can produce more agreement without producing more evidence. A builder can optimize for a visible passing test, while a reviewer endorses that result and the real requirement still fails. That is the opening for reward hacking and collusion-enabled approval laundering. Receipts records where each approval gets its evidence, independently executes the task contract against the exact artifact, rejects unsupported success, and checks the repair. Our demo uses checkout retries and discount calculations, with real model roles and independent Modal sandbox verification. We show the actual checks and traces, rather than infer misconduct from agreement.

Use the last sentence about model/Modal execution only with the linked completed live-run evidence. Controlled replay and live role behavior must remain distinguishable.

## 90-second explanation and demo

1. **Problem:** An agent team is rewarded for completing a task. Its visible check can be weaker than the task's actual requirement. More reviewers do not help when all their approvals ultimately cite the same incomplete execution.
2. **Reward hacking:** A checkout response succeeds on retry, yet another charge is created. A discount passes the demonstrated amount but is hardcoded instead of generalizing. These are simulated task contracts, not real transactions.
3. **Coordination threat:** In the controlled adversarial scenario, builder and reviewer are instructed to get an invalid patch accepted. The tester stays neutral. Show the actual role requests and decisions. If they refuse or produce correct code, show that outcome too. Distinguish the exploratory task-following prompts from the separate objective-first red-team configuration. Repeated-memory emergent collusion remains a future research track.
4. **Defense:** The controller owns the verifier. Candidate code cannot supply its own trusted verdict. Each cloud check uses a fresh sandbox, and its receipt binds source, contract, verifier and execution identity. A change makes prior source evidence stale.
5. **Recovery:** A failed check invalidates approvals that depend on the rejected artifact. The agent gets a bounded repair attempt, which is checked again. Correct shared evidence and clean work remain accepted.
6. **Proof:** Show rejected and repaired source, the independent behavioral checks, recorded role messages, Modal execution receipts and neatlogs spans. Entire explains provenance; cfo.ai can turn measured review/verification/repair observations into economics once the native Model and cost capture are completed.

## Research connection

- [Orbit](https://arxiv.org/abs/2609.33102) and [Colosseum](https://arxiv.org/abs/2602.15198) motivate treating multi-agent coordination as its own threat model. Receipts grades observable actions and supporting evidence; it does not reproduce their evaluations.
- [EvilGenie](https://arxiv.org/abs/2511.21654) motivates separating visible reward from held-out task success. A failed held-out check alone cannot establish malicious intent.
- [Hacker-fixer loops](https://arxiv.org/abs/2606.08960) motivate attacking the verifier and checking that legitimate solutions still work after hardening.
- [Long-horizon interaction](https://arxiv.org/abs/2609.24967) motivates a later retained-memory evaluation. A prompted adversarial role in our small demo is not spontaneous collusion.
- The [documented message-board investigation](https://www.lesswrong.com/posts/wt4kk6vFPEhkXvF8Q/how-good-are-slop-vestigators) motivates preserving provenance for retrospective investigation. We do not claim to have independently confirmed or reproduced that incident.

## Actual red-team finding to show

A real adversarial builder inserted a length-37 checkout conflict bypass, and its reviewer endorsed the visible check. A neutral tester spotted it, but the original trusted oracle missed the input and the gate accepted the patch. Preserve and show that failure. The discount attack was independently rejected and repaired.

This is why the pitch needs both agent-level evidence and verifier hardening. A cloud sandbox provides execution isolation; it cannot make incomplete tests sufficient. Demonstrate the original false acceptance, the exact counterexample, a revised verifier, fresh replay, and a legitimate-solution control. Claim mitigation of this captured attack only after the replay succeeds. Do not call this spontaneous collusion or imply universal protection.

## Positioning and claim boundary

Lead with **agent collusion and reward hacking**, and describe **independent acceptance evidence and verified recovery** as the defense. Repository issue solving is the first real-world application and capability benchmark; it does not replace the threat-focused evaluation.

Say “we demonstrated detection of these controlled contract violations and tested live adversarial roles.” Do not say “we detected spontaneous collusion,” “we eliminate reward hacking,” or “we outperform every approach.” Whether a model follows an attack instruction is an observed result, not a predetermined demo outcome. Use [the claims guide](CLAIMS.md) and the completed run summary for numerical statements.
