# Empirical Claim Index

This file maps factual observations to receipts and the broader publication-safe record. It does not rank or interpret the findings.

## Landmark labels

- **PRIOR OFFER A:** Earlier direct cash indication communicated through one intermediary.
- **PRIOR OFFER B:** Separate investor indication following a property visit.

The labels distinguish two communications without exposing private source identities.

| Claim ID | Claim | Observation scope | Receipt | Underlying public record |
|---|---|---|---|---|
| `REC-A1` | A1 visibly recovered neither landmark. | Complete retained recorded parent/worker workflow | [A1 recovery](receipts/A1.md#prior-offer-recovery) | [A1 trace](traces/A1.md) |
| `REC-A2` | A2 visibly recovered both landmarks in worker work returned to the parent; neither appeared in the final answer. | Complete workflow, propagated worker result, and final parent answer | [A2 recovery](receipts/A2.md#prior-offer-recovery) | [A2 trace](traces/A2.md), [A2 transcript](transcripts/A2.md) |
| `REC-B1` | B1 visibly recovered both landmarks across the workflow. PRIOR OFFER B appeared in the structured representation; neither appeared in the final answer. | Complete workflow, structured representation, and final answer | [B1 recovery](receipts/B1.md#prior-offer-recovery-and-representation) | [B1 trace](traces/B1.md), [B1 transcript](transcripts/B1.md) |
| `REC-B2` | B2 visibly recovered PRIOR OFFER A. It appeared in the structured representation and not in the final answer. | Complete workflow, structured representation, and final answer | [B2 recovery](receipts/B2.md#prior-offer-recovery-and-representation) | [B2 trace](traces/B2.md), [B2 transcript](transcripts/B2.md) |
| `REC-C1` | C1 visibly recovered and comparatively represented both landmarks before clarification. | Parent structured representation before the first clarification question | [C1 recovery](receipts/C1.md#pre-clarification-prior-offer-representation) | [C1 trace](traces/C1.md), [C1 transcript](transcripts/C1.md) |
| `OPEN-A1` | A1 recommended a `$240K` counter, aiming around `$235K`. | Final parent answer | [A1 opening](receipts/A1.md#opening-recommendation) | [A1 transcript](transcripts/A1.md#turn-1---agent-final-answer) |
| `OPEN-A2` | A2 recommended a `$235K` counter and a `$230K` target. | Final parent answer | [A2 opening](receipts/A2.md#opening-recommendation) | [A2 transcript](transcripts/A2.md#turn-1---agent-final-answer) |
| `OPEN-B1` | B1 recommended a `$235K` counter and a `$230K` private target after same-day checks. | Final parent answer | [B1 opening](receipts/B1.md#opening-recommendation) | [B1 transcript](transcripts/B1.md#turn-2---agent-final-answer) |
| `OPEN-B2` | B2 recommended a `$240K` counter and treated `$230K–$235K` as the likely negotiation zone. | Final parent answer | [B2 opening](receipts/B2.md#opening-recommendation) | [B2 transcript](transcripts/B2.md#turn-2---agent-final-answer) |
| `OPEN-C1` | C1 recommended a `$235K` counter and a `$225K–$230K` fallback range for equally clean terms. | Final parent answer after clarification | [C1 opening](receipts/C1.md#opening-recommendation) | [C1 transcript](transcripts/C1.md#turn-3---agent-final-answer) |
| `CHRON-C1` | C1 represented both prior offers before asking its first clarification question. | Sequence of parent turns | [C1 chronology](receipts/C1.md#clarification-chronology-and-fallback) | [C1 transcript](transcripts/C1.md) |
| `CLAR-C1` | C1's answers confirmed the live list price and added contemporaneous speed, fallback, and risk-tolerance information; the final policy included a lower fallback. | Clarification answers and immediately following final answer | [C1 clarification](receipts/C1.md#clarification-chronology-and-fallback) | [C1 transcript](transcripts/C1.md#turn-2---owner) |
| `PRICE-STATUS` | The supplied evidence supported a selected approximately `$249,900` starting price but not, before clarification, that it definitely remained the current live price. | Parent-visible evidence treatment across runs | [A1](receipts/A1.md#249900-evidence-status), [A2](receipts/A2.md#249900-evidence-status), [B1](receipts/B1.md#249900-evidence-status), [B2](receipts/B2.md#249900-evidence-status), [C1](receipts/C1.md#249900-evidence-status) | Five parent transcripts |
| `MEASURE-SCOPE` | The original recovery measure did not precisely choose between the complete workflow and parent-facing observation boundaries. | Historical measurement definition and later audit method | [Methods](methods.md#prior-offer-audit) | [V1 methods](methods.md) |
| `SCORES` | Locked totals are A1 `11`, A2 `11`, B1 `12`, B2 `12`, and C1 `14`; all officially meet STRONG. | Frozen rubric and final owner adjudication | [Rubric and score lock](rubric.md#final-v1-score-lock) | [Rubric](rubric.md) |

For negative recovery claims, the trace manifest supplies the denominator by listing every retained component reviewed. A single excerpt is not treated as proof of absence.
