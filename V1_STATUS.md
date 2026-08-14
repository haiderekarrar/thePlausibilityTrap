# V1 Status Addendum (2026-08-12)

This additive status document records the later owner-approved V1 decision. It does not rewrite the history of `deal_autopsy_build_spec_v3.md` or the Replay 04 manual-pilot control files.

## What was planned and what ran

The frozen v3 design planned 27 Replay 04 attempts: Conditions A, B, and C across three model tiers with three repeats per cell.

The later manual-pilot fork planned nine stripped-down runs, A1–A3, B1–B3, and C1–C3, to inform that larger design. Its frozen fork memo and rubric explicitly said that the pilot did not replace or amend v3.

What was actually executed in Work was:

- initial exploratory pilot: A1, B1, and C1;
- bounded follow-up: A2 and B2.

A separate Codex A1 was a side observation, not one of the five Work runs. No C2 or A3/B3/C3 was run, the nine-run thresholds were not evaluated as a completed experiment, and the 27-attempt Tier 1a grid was not executed.

The later V1 decision is to ship the useful evidence from the **Replay 04 manual pilot plus bounded follow-up** as an exploratory five-Work-run case study. The unexecuted remainder of the nine-run pilot and the larger grid are deferred, not completed. Resuming either requires a separately approved post-ship design decision.

## Why the next step changed

The broader architecture was designed before the owner fully appreciated how much corpus search and historical reconstruction a frontier coding agent could already perform from a short request. A historically bounded, cutoff-controlled, redacted corpus remained necessary: live access to current accounts would expose post-decision information and invalidate the replay. In hindsight, the cheap pilot could have happened earlier and might have reduced design churn, although the cutoff, corpus, privacy, redaction, and provenance work was still necessary for a defensible historical replay.

The pilot made evidence search, visible evidence reconstruction, integration, claim discipline, owner-state elicitation, fallback calibration, run-to-run variation, and tool completion more useful V1 questions than mechanically finishing the stale grid.

## Run-level descriptive observations

The two known earlier approximately-$150K offer communications were visibly surfaced as follows:

| Work run | Visible prior-offer result |
|---|---|
| A1 | 0/2 |
| A2 | 0/2 |
| B1 | 1/2: the November 11 AGENT_M communication |
| B2 | 1/2: the different November 6 AGENT_N communication |
| C1 structured stage | 2/2, before clarification questions |

These are run-level observations, not stable condition-level retrieval rates. B1, B2, and C1's pre-clarification stage were nominally the same structured treatment over the same corpus, yet produced 1/2, 1/2 with a different communication, and 2/2 visible recovery. Another nominally identical structured pass could plausibly surface both, one, or neither. Three passes cannot estimate the probability or expected completeness of any outcome.

“Visibly surfaced” does not establish whether omitted evidence was never encountered. Search trajectory, tool choice, work performed, salience, filtering, compression, model variation, and other unobserved mechanisms remain possible explanations. Nominally identical prompts do not establish identical internal search paths or effort. The pilot does not select among these explanations.

## Interpretation boundaries

**A versus B is bundled.** A uses evidence and solves. B adds a structured intermediate stage, another opportunity to search and reason, and a compressed representation before solving. The observed association cannot distinguish structure itself from additional opportunity to work. A matched-effort natural-request condition is deferred in `POST_SHIP.md`.

**Retrieval is not integration.** B1 and B2 each visibly surfaced one earlier offer but made little or no meaningful downstream use of it under the descriptive definition recorded before A2/B2 and applied post hoc to B1. C1 used both in its structured evidence comparison. This does not establish that the offers caused C1's final recommendation.

**Clarification did not cause C1's 2/2 result.** C1 surfaced both communications during its initial structured stage, before asking questions or receiving owner answers. Clarification instead elicited relevant contemporaneous owner state, improved owner-specific calibration, and changed fallback reasoning more than the opening action. The operator-state amendment records information surfaced during C1; it was not preregistered owner state and must not be presented as such.

**Earlier offers were not necessarily decisive.** They preceded targeted renovation and sale-preparation work, while the $220K offer was the first offer after that work. More current evidence included the current offer, the pricing instruction, limited recent market exposure, inquiries/showings, and the current agent's broad as-is estimate. Opening recommendations were relatively stable despite different visible evidence reconstruction. Differences may matter more for grounding, confidence, auditability, and fallback reasoning than for the exact opening number. Shared anchoring on $249,900 remains a hypothesis.

**Evidence discipline varied.** Both natural-request runs treated $249,900 more like a confirmed live listing fact than the supplied corpus alone established. Structured passes were more explicit about that uncertainty; C1 clarification later elicited owner confirmation of the live MLS price. C1 also handled an ambiguous earlier “Signed” record without assuming that the later offer had already been accepted. Separately, one exploratory run prematurely concluded evidence was absent when a long-running search had not immediately returned output; this is a tool-state/completion observation, not proof of a broader retrieval mechanism.

Do not collapse visible recovery, evidence integration, source coverage, claim discipline, confidence, and decision quality into one measure. Citation breadth demonstrates visible coverage, not completeness, correctness, weighting, integration, or overall reliability.

## Measurement chronology and current boundary

The frozen manual-pilot rubric and STRONG RUN definition remain unchanged. Prior-offer recovery, evidence integration, unsupported factual claims, opening action, and fallback policy were identified post hoc for A1/B1/C1. `NOTES.md` records those descriptive checks and the stop rule before A2/B2; preserved local file and Codex thread metadata support that ordering. Because the note was not committed before the runs, describe the checks as locally recorded pre-run descriptive checks, not Git-preregistered metrics.

## Final V1 score lock (2026-08-14)

A1, B1, and C1 had earlier provisional/reconstructed scoring history. A2 and B2 were scored later under the same frozen rubric. The owner then explicitly adjudicated A1/A2 Evidence Retrieval and C1 Actionability. The following scores are final for V1:

| Run | Objective | Retrieval | Discipline | Uncertainty | Decision | Actionability | Authority | Total | STRONG? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A1 | 2 | 1 | 1 | 2 | 1 | 2 | 2 | 11 | Yes |
| A2 | 2 | 1 | 1 | 2 | 1 | 2 | 2 | 11 | Yes |
| B1 | 2 | 1 | 2 | 2 | 1 | 2 | 2 | 12 | Yes |
| B2 | 2 | 1 | 2 | 2 | 1 | 2 | 2 | 12 | Yes |
| C1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 14 | Yes |

**A-run Retrieval adjudication.** A1 and A2 are locked at `1`. The omitted prior-offer history is material, but the owner does not judge it to be "major load-bearing evidence" under the rubric's `0` anchor. Both runs found important evidence while missing material pieces, matching the rubric's `1` anchor.

**C1 Actionability adjudication.** C1 is locked at `2`. It supplied a clear immediate recommendation, a specific `$235K` counter, fallback guidance, and a usable draft while preserving owner approval. The rubric does not require every due-diligence safeguard to be repeated inside the draft.

All five runs officially meet the rubric's STRONG threshold. This `5/5` count is not a headline scientific finding: under the plausible alternate interpretation that A1/A2 Retrieval should be `0`, the count would be `3/5`. The count is therefore anchor-sensitive even though the official scores remain locked.

The score lock does not alter the interpretation boundaries above. All five runs produced broadly defensible recommendations; visible evidence reconstruction differed materially; retrieval and integration remained distinct; and opening recommendations stayed relatively stable. The five runs do not complete the original manual-pilot or Tier 1a designs and do not establish causal or stable condition-level effects.

No additional model run, pilot condition, repeat, harness, prompt change, rubric change, or transcript change is authorized for V1 by this addendum.

## Publication boundary

Pseudonymization alone does not make private transcripts safe to publish. Chronology, prices, property facts, relationships, legal/title issues, disputes, and agent relationships may be identifying in combination. Public excerpts require a separate privacy and confidentiality review. Private ground truth and sensitive explanations remain private even when they would make the story more interesting.
