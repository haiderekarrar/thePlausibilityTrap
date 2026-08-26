# V1 Status Addendum (2026-08-12)

This additive status document records the later owner-approved V1 decision. It does not rewrite the history of `deal_autopsy_build_spec_v3.md` or the Replay 04 manual-pilot control files.

## Current public framing

**Public title:** The Plausibility Trap

AI is not only used to find objective truths, such as answers to math problems. It is also used in subjective situations where there may be no objective answer key. In those situations, people should be able to see why the AI reached the reasoning or judgment that it did and decide whether they want to disagree with it. That requires distinguishing evidence, inference, uncertainty, assumptions, model or default priors, preference or value judgment, and recommendation.

The motivating question is: "Where does the evidence end and the agent's judgment begin, and can the user see and contest that boundary?"

Widely used agents may inherit defaults, policies, priors, or values from the organizations that build them. Concentrated control over widely used agents makes visibility into the evidence-and-judgment boundary more important.

V1 remains an exploratory case study of one historical decision scenario executed in five Work runs. Replay 04 does not directly test institutional or provider influence. It motivates why making the evidence-and-judgment boundary visible may matter.

## What was planned and what ran

The frozen v3 design planned 27 Replay 04 attempts: Conditions A, B, and C across three model tiers with three repeats per cell.

The later manual-pilot fork planned nine stripped-down runs, A1–A3, B1–B3, and C1–C3, to inform that larger design. Its frozen fork memo and rubric explicitly said that the pilot did not replace or amend v3.

What was actually executed in Work was:

- initial exploratory pilot: A1, B1, and C1;
- bounded follow-up: A2 and B2.

A separate Codex A1 was a side observation, not one of the five Work runs. No C2 or A3/B3/C3 was run, the nine-run thresholds were not evaluated as a completed experiment, and the 27-attempt Tier 1a grid was not executed.

Session provenance is resolved with high confidence from explicit originator metadata and timestamps:

| Record | Session UUID | Started (PDT) | Originator |
|---|---|---|---|
| Discarded Codex-side A | `019fee00-5594-74e1-901d-715b25731182` | 2026-08-10 4:27:07 PM | `Codex Desktop` |
| Work A1 | `019fee0b-257d-7f42-9a16-e0946c792e29` | 2026-08-10 4:38:55 PM | `codex_work_desktop` |
| Work A2 | `019ff819-a530-77a1-b20d-97007e8f70c8` | 2026-08-12 3:30:58 PM | `codex_work_desktop` |

The later V1 decision is to ship the useful evidence from the **Replay 04 manual pilot plus bounded follow-up** as an exploratory five-Work-run case study. The unexecuted remainder of the nine-run pilot and the larger grid are deferred, not completed. Resuming either requires a separately approved post-ship design decision.

## Why the next step changed

The broader architecture was designed before the owner fully appreciated how much corpus search and historical reconstruction a frontier coding agent could already perform from a short request. A historically bounded, cutoff-controlled, redacted corpus remained necessary: live access to current accounts would expose post-decision information and invalidate the replay. In hindsight, the cheap pilot could have happened earlier and might have reduced design churn, although the cutoff, corpus, privacy, redaction, and provenance work was still necessary for a defensible historical replay.

The pilot made evidence search, visible evidence reconstruction, integration, claim discipline, owner-state elicitation, fallback calibration, run-to-run variation, and tool completion more useful V1 questions than mechanically finishing the stale grid.

## Posthoc run-graph audit

The two earlier approximately-$150K offer communications are labeled `PRIOR OFFER A` and `PRIOR OFFER B` here. The locally recorded pre-A2/B2 descriptive check defined how a response had to identify distinct communications and separately defined meaningful integration into final reasoning, but it did not specify whether recovery meant appearance anywhere in the complete recorded worker/parent workflow or appearance in the parent-facing structured or final work product. The original recovery boundary was therefore underspecified.

A later independent primary-record audit separated observable locations in the retained record:

| Work run | Complete retained worker/parent workflow | Explicit parent-facing representation or final answer |
|---|---|---|
| A1 | Neither landmark visibly recovered | Neither appeared |
| A2 | Both landmarks appeared in worker work returned to the parent | Neither appeared in the final answer |
| B1 | Both landmarks appeared across the retained workflow | One appeared in the structured representation; neither was explicitly carried into the final answer |
| B2 | One landmark appeared across the retained workflow | That landmark appeared in the structured representation; it was not explicitly carried into the final answer |
| C1 | Both landmarks appeared before clarification | Both were comparatively represented before clarification |

These are properties of recorded artifacts, not claims about hidden cognition. The omissions in A2's and B1's final answers could reflect multiple unresolved mechanisms, including reasonable relevance filtering: the earlier offers were similar in amount and preceded later renovation and sale-preparation work. Do not label the omissions as failure, compression loss, forgetting, intelligent filtering, or any other mechanism without additional evidence.

A final output alone is a lossy view of recorded agent work in both directions: missing evidence may reflect work that never occurred, or earlier work that occurred but was not exposed in the final answer. This audit establishes that distinction in these records; it does not establish a general law about agents or stable condition-level rates.

## Interpretation boundaries

**A versus B is bundled.** A uses evidence and solves. B adds a structured intermediate stage, another opportunity to search and reason, and a compressed representation before solving. The observed association cannot distinguish structure itself from additional opportunity to work. A matched-effort natural-request condition is deferred in `POST_SHIP.md`.

**Recovery location is not integration.** A2 and B1 each contain prior-offer evidence in retained worker or parent work that does not appear in the final answer. B1 and B2 each represented one landmark in their structured work without explicitly carrying it into the final answer. C1 comparatively represented both before clarification. These observations do not establish that the earlier offers caused any final recommendation or that final-answer omission reveals why the evidence was omitted.

**Clarification did not cause C1's 2/2 result.** C1 surfaced both communications during its initial structured stage, before asking questions or receiving owner answers. Clarification instead elicited relevant contemporaneous owner state, improved owner-specific calibration, and changed fallback reasoning more than the opening action. The operator-state amendment records information surfaced during C1; it was not preregistered owner state and must not be presented as such.

**Earlier offers were not necessarily decisive.** They were similar in amount and preceded targeted renovation and sale-preparation work, while the $220K offer was the first offer after that work. More current evidence included the current offer, the pricing instruction, limited recent market exposure, inquiries/showings, and the current agent's broad as-is estimate. Their omission from a later artifact may therefore reflect reasonable relevance filtering, although the audit does not establish that mechanism. Opening recommendations were relatively stable despite different visible evidence reconstruction. Differences may matter more for grounding, confidence, auditability, and fallback reasoning than for the exact opening number. Shared anchoring on $249,900 remains a hypothesis.

**Epistemic posture varied.** Here, epistemic posture means whether expressed certainty or status matches what the available evidence supports. The supplied evidence established an intended or selected approximately-$249,900 starting price, but did not establish before clarification that it definitely remained the current live listing price. A1 and A2 presented it as the current or list price. B1 treated it as intended and unverified. B2 treated it as likely and unconfirmed. C1 marked it unverified, asked the owner, received confirmation, and only then treated it as established. The structured runs handled this evidentiary uncertainty more carefully than the direct runs.

This does not establish that structure itself caused the improvement. B and C were explicitly instructed to separate evidence from assumptions, and B also had an additional stage and opportunity to work. Had the uncertain fact been genuinely decision-pivotal, the difference in evidence handling could have affected the recommendation. That is a motivation for harder future tests, not something Replay 04 demonstrated.

C1 also handled an ambiguous earlier “Signed” record without assuming that the later offer had already been accepted. Separately, one exploratory run prematurely concluded evidence was absent when a long-running search had not immediately returned output. This is a tool-state and completion observation, not proof of a broader retrieval mechanism.

Do not collapse visible recovery, evidence integration, source coverage, claim discipline, confidence, and decision quality into one measure. Citation breadth demonstrates visible coverage, not completeness, correctness, weighting, integration, or overall reliability.

## Measurement chronology and current boundary

The frozen manual-pilot rubric and STRONG RUN definition remain unchanged. Prior-offer recovery, evidence integration, unsupported factual claims, opening action, and fallback policy were identified post hoc for A1/B1/C1. `NOTES.md` records those descriptive checks and the stop rule before A2/B2; preserved local file and Codex thread metadata support that ordering. Because the note was not committed before the runs, describe the checks as locally recorded pre-run descriptive checks, not Git-preregistered metrics. Its recovery definition did not fix the worker/parent observation boundary. The later run-graph audit is a separate posthoc analysis and does not alter the frozen rubric or locked scores.

## Final V1 score lock (2026-08-14)

A1, B1, and C1 had earlier provisional/reconstructed scoring history. A2 and B2 were scored later under the same frozen rubric. The owner then explicitly adjudicated A1/A2 Evidence Retrieval and C1 Actionability. The following scores are final for V1:

| Run | Objective | Retrieval | Discipline | Uncertainty | Decision | Actionability | Authority | Total | STRONG? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A1 | 2 | 1 | 1 | 2 | 1 | 2 | 2 | 11 | Yes |
| A2 | 2 | 1 | 1 | 2 | 1 | 2 | 2 | 11 | Yes |
| B1 | 2 | 1 | 2 | 2 | 1 | 2 | 2 | 12 | Yes |
| B2 | 2 | 1 | 2 | 2 | 1 | 2 | 2 | 12 | Yes |
| C1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | Yes |

**A-run Retrieval adjudication.** A1 and A2 are locked at `1`. The owner adjudication treated the absence of prior-offer history from the scored parent-facing work as material, but not "major load-bearing evidence" under the rubric's `0` anchor. Both runs found important evidence while missing material pieces under that scoring scope, matching the rubric's `1` anchor. The later posthoc run-graph audit does not rescore this frozen judgment.

**C1 Actionability adjudication.** C1 is locked at `2`. It supplied a clear immediate recommendation, a specific `$235K` counter, fallback guidance, and a usable draft while preserving owner approval. The rubric does not require every due-diligence safeguard to be repeated inside the draft.

All five runs officially meet the rubric's STRONG threshold. This `5/5` count is not a headline scientific finding: under the plausible alternate interpretation that A1/A2 Retrieval should be `0`, the count would be `3/5`. The count is therefore anchor-sensitive even though the official scores remain locked.

The score lock does not alter the interpretation boundaries above. All five runs produced broadly defensible recommendations; visible evidence reconstruction differed materially; retrieval and integration remained distinct; and opening recommendations stayed relatively stable. The five runs do not complete the original manual-pilot or Tier 1a designs and do not establish causal or stable condition-level effects.

No additional model run, pilot condition, repeat, harness, prompt change, rubric change, or transcript change is authorized for V1 by this addendum.

## Publication boundary

Pseudonymization alone does not make private transcripts safe to publish. Chronology, prices, property facts, relationships, legal/title issues, disputes, and agent relationships may be identifying in combination. Public excerpts require a separate privacy and confidentiality review. Private ground truth and sensitive explanations remain private even when they would make the story more interesting.
