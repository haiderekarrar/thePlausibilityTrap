# Methods and Provenance

## Study boundary

The study reconstructs one historical property-sale decision at a fixed cutoff and examines five Work runs: A1, A2, B1, B2, and C1. The later real-world action and outcome were withheld from the agents and were not the scoring criterion. A separate Codex-side A observation is not part of the five-run study.

## Conditions

- **Condition A:** The agent received an unstructured redacted evidence workspace and a natural decision request. It was asked to recommend what to do and prepare a response without taking external action.
- **Condition B:** The agent received the same evidence and request, but first had to inspect the files and produce a structured representation separating objective, evidence, stakeholders and claims, constraints and authority, ranked unknowns, and assumptions. Only after that stage did the owner ask it to decide.
- **Condition C:** The agent followed the Condition B structured stage, then could ask up to three targeted questions whose answers could materially change the recommendation. It decided only after receiving those answers.

Condition B is not a clean structure-only treatment. It adds an intermediate stage and another opportunity to search and reason. Condition C adds clarification after that same structured stage.

The exact owner-facing prompts appear in the five parent transcripts.

## Recorded artifact layers

- **Parent transcript:** The retained visible owner/agent interaction in the parent session, beginning with the experimental request.
- **Worker/subagent trace:** A retained visible record produced by a delegated worker. Selected publication-safe worker excerpts appear as receipts rather than full source-heavy traces.
- **Private source corpus:** The fixed redacted evidence workspace supplied to the runs. It is not published.

For trace coding, the audit conceptually distinguishes observable record locations and surfaces:

- worker/subagent records;
- recorded worker-to-parent returns;
- parent-authored intermediate text;
- explicit parent situation, evidence, or task-state representations;
- other parent-visible analysis; and
- the final user-facing answer.

The five short labels below are derived summaries over those observable records. FOUND, PROPAGATED, REPRESENTED, INTEGRATED, and OUTPUT are posthoc descriptive audit labels, not sequential stages and not precommitted V1 metrics. The retained workflow is graph-like: a fact may appear in different recorded components and visible analytical contexts without traversing the labels in a fixed order. The labels are not sequential prerequisites and do not describe a required progression. Some overlap is logically implied by their definitions—for example, a fact that appears in the final answer also necessarily appears somewhere in the retained record—but that does not mean it traversed the other labels in sequence.

- **FOUND:** A record-wide existence summary. The distinct target fact is semantically identifiable in at least one retained agent-produced or returned workflow component. Mere presence in source material or tool input does not qualify. FOUND does not identify where the fact appeared, describe a discovery event, or imply that the agent knew, understood, or used it.
- **PROPAGATED:** The target fact appears in a recorded worker/subagent result returned to the parent. This label is architecture-conditional and may be N/A when there is no relevant worker-to-parent boundary. It records only that the fact appeared in the recorded return crossing that boundary. It does not imply that the parent noticed, understood, relied on, used, or remembered it.
- **REPRESENTED:** Parent-authored visible text includes the target fact in an explicit representation of the situation, evidence, task state, or an analogous structured working artifact. Where no such explicit representation exists, the label may be N/A rather than a failure. REPRESENTED does not itself imply relational analytical use.
- **INTEGRATED:** Parent-authored visible analysis performs a relational operation on the target fact—for example by comparing it, conditioning on it, weighing its evidentiary significance, or explicitly rejecting an inference from it—rather than merely listing or historically characterizing it. Integration may occur inside an explicit representation, in later visible parent analysis, or in another parent-authored visible analytical artifact. Historical attributes, metadata, provenance, or disposition alone do not establish integration.
- **OUTPUT:** The target fact appears explicitly in the final user-facing answer. OUTPUT is a visibility surface, not the terminal stage of a pipeline. A fact may be visibly integrated without appearing in OUTPUT. Appearing in OUTPUT does not by itself prove integration.

These labels describe recorded artifacts, not hidden cognition or chain-of-thought. They are not exhaustive and do not separately encode every possible transformation, including distortion or conflation, the direction of evidentiary weighting, or intentional versus incidental omission. The V1 trace coding was not accompanied by a formal inter-rater reliability estimate.

## Prior-offer audit

The original locally recorded "prior-offer recovery" check did not precisely define whether its observation boundary was the complete recorded worker/parent workflow or only the parent-facing work product. The deeper run-graph audit was completed before publication and separated those scopes. That audit changed the interpretation of A2 and B1 without changing the frozen rubric or locked scores.

The pre-run wording said: "An offer counts as recovered only if the response identifies it as a distinct earlier approximately-$150K offer communication." It defined semantic identification but used the unqualified word "response," without specifying parent-facing output or the complete retained workflow.

A landmark counts as present only when the retained text semantically identifies that distinct target fact sufficiently to distinguish it from confusable neighboring facts. Exact wording is not required; a faithful paraphrase may count. A generic or ambiguous reference that cannot distinguish the two earlier approximately-$150K offer communications does not automatically count for either landmark. Source citations or private provenance may help establish which distinct landmark a publication-safe passage refers to, but publication status does not determine the coding.

The audit enumerated each retained parent and worker session from session metadata, identified separately returned worker results, and reviewed their visible recorded work. Literal text search assisted navigation but did not define the coding. Every component examined is listed in the per-run trace manifest.

Coding was performed on the complete private retained records; publication status was determined separately and did not affect coding.

### REPRESENTED / INTEGRATED calibration

B1 states: "A previous investor offered $150,000 cash earlier in the sale process. That proposal appears to have been informal and was rejected." This is REPRESENTED but not INTEGRATED under the V1 rule because the visible text describes the historical fact and its disposition without visibly relating its evidentiary significance to the current decision.

B2 states: "It is evidence of one investor's economics, not independent market value." This qualifies as INTEGRATED because the visible analysis explicitly weighs what the fact can and cannot support in the current valuation problem.

## Run provenance

All five runs used OpenAI `gpt-5.6-sol` with recorded reasoning effort `ultra` in the Codex Work desktop surface. Session metadata reports originator `codex_work_desktop`, source `vscode`, and CLI version `0.147.0-alpha.6.5`.

| Run | Started (UTC) | Private source-record SHA-256 |
|---|---|---|
| A1 | 2026-08-10 23:38:55.741 | `7233e578d93413c3a94e8494aa851231f5172f2705388f045c2ef909ca9db387` |
| B1 | 2026-08-10 23:47:54.761 | `fed61f2e022bc433a4280c036a4600e2d907a62fcd62d32512cb30f30ba532cb` |
| C1 | 2026-08-11 14:41:22.728 | `e4c7a50c8e67fe22835234c990843c073912ce470409d16caa9d2c7d157f6cd0` |
| A2 | 2026-08-12 22:30:58.096 | `8abc2f7ca4b0ff29989509c11b30383ac3e85dfad891abfe9d544165ae1c80f4` |
| B2 | 2026-08-12 22:31:38.165 | `29697c9d6173d0c2f4396e1856e041a5e1382d55ab9abad659c8cfd36e305ea4` |

The preserved internal pilot archive points to Git commit `c4ad6c68df76492231a48b4efcd3983d00c1a19e`. Its private bundle SHA-256 is `2a103e6ed623488addeb3a5510d1c9fe11db262b464f284174b31d0ef630f7e2`. These hashes commit to private records without publishing their contents.

## Publication boundary

The public package excludes the 586-event corpus, raw exports, identity mapping, private controls, owner-state and ground-truth files, unrelated communications, hidden model reasoning, and complete source-heavy worker traces. Parent transcripts begin at the experimental request. Injected environment, plugin, system, and developer material is outside that boundary. Publication redactions, generalizations, and paraphrases are marked inline.

Exact historical transaction dates, clock times, and timestamps are generalized unless exact timing is analytically necessary. Month-level and relative chronology remain where useful. Run timestamps and other reproducibility metadata remain exact.
