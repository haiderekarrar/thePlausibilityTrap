# NOTES.md — agent-driving log

A running record of decisions, failures, corrections, and surprises while building Deal Autopsy. Newest entries at the bottom. Entries marked [FILL] need details from my own sessions — do not ship the file with [FILL] markers in it.

**Contrarian thesis.** I believe the most valuable untapped evidence about knowledge-work automation is not sitting in public benchmark datasets. It is buried in the private digital exhaust of real transactions: messages, emails, documents, decisions, and outcomes. Deal Autopsy turns one such transaction into a privacy-preserving, reproducible test of where AI can act reliably, where better interfaces must structure context, and where human judgment still matters. The project itself is the wager: I started building that evidence before anyone paid me to.

---

**Tooling split.** Daily driver is Codex (builder). Hard architecture, plan reviews, schema decisions, and pre-publication redaction checks get escalated to Claude in a separate session that holds the full project context (architect/verifier). Chose this split partly because my brother uses Codex, so I have a human escalation path too. Will note where each earns its keep as the build progresses.

**Parser design rule.** Parsers extract verbatim; ALL identity transformation lives in redact.py only. Reason discovered from my own sample data: my full name appeared inside a message body, not on a sender line — any parser-level identity handling would only touch sender fields and miss body text, creating leaks in places no one would look. One transformation stage = one auditable place to fail.

**Redaction uniformity rule.** Every identity string gets mapped, including my own name and all its aliases (full name, first-name case variants, "Me" -> ME, surname catch-all, my username inside attachment file paths). No exceptions: a rule with zero exceptions is machine-checkable (any grep hit = leak, script fails loudly); one exception forces human judgment on every hit. Also mapped weakly-identifying counterparty first names to stable pseudonyms because identification is combinatorial: first name + city + role + date is findable, and mapping costs one YAML line.

**Model routing protocol (pipeline).** Verify, then downgrade: hand-label 50 events, run the cheap model on the same 50, measure agreement. At >=95% the cheap model owns classification; below that, fix the prompt and retry, or have the cheap model emit a confidence flag and escalate only uncertain rows. Measured agreement: [FILL after running].

**Model tiers are a finding, not a cost problem.** In the pipeline, models are workers: route to the cheapest verified tier. In the replays, models are the subjects: deliberately run small/mid/frontier on the SAME decisions, because where on the capability curve each primitive becomes automatable (and at what cost per task) is exactly the question an interface company needs answered.

**Codex flagged a real misconfiguration.** During skeleton setup it discovered my project folder was inheriting Git from a stray .git in my home directory, meaning Git treated most of my machine as one repository. Approved a project-level git init for a clean boundary and removed the stray. The agent surfaced a problem I didn't know I had instead of silently working around it — result of instructing it up front to explain non-obvious findings.

**Replay design: the A/B conditions (my addition).** Added a second condition to every replay: (A) raw full context -> decision, vs. (B) model triages what's relevant first, then decides on its own distillation. Insight behind it: deciding what's relevant IS most of the decision — in the real deal, separating fact from claim (scrutinizing everything that wasn't verifiable, regardless of whether it came from a professional) is where most of the $76K upside came from. Splitting triage from deciding makes failures diagnosable: "couldn't find what mattered" vs. "had it and chose badly." If B beats A, that's evidence the bottleneck is context structuring — the interface layer — not model capability.

**Replay design: the elicitation axis got three grades, not two.** Original design scored whether the model asks about priorities before acting (e.g., "speed or price?"). I caught the flaw from my own deal: I DID maximally value speed (tenant escalating threats and acting on them), and the speed-optimal move was still to counter the $220K bid at $232K — fast acceptance signals desperation, invites repair-demand renegotiation, and capitulation reads as fast but plays out slow. So a model that elicits "speed" and recommends accepting has optimized the stated preference into a trap. Final grades: (i) one-shots without interrogating the goal; (ii) elicits surface preferences and optimizes them literally (the speed trap); (iii) reasons about how the counterparty responds to the move — recognizes strength as the fast path.

**Integrity rule.** Replays run honestly; results publish whatever they show, including outcomes that flatter the models or complicate the thesis. The audience builds evals for a living and will detect a rigged demo instantly; honest surprising results are worth more than clean confirming ones.

**Intent transfer beats task transfer.** Noticed my builder agent made better unsupervised micro-decisions after I explained WHY the plan changed, not just what changed — so I now end context updates with "when the spec is silent, decide in the direction these points push." Same lesson as the founder's eval critique, applied to my own tooling: the bottleneck wasn't the agent's capability, it was how much intent I'd transferred to it.

**GPT-5.6 tier routing (builder side).** Terra for well-specified work (parsers, scaffolding, report templating), Sol reserved for genuinely ambiguous problems, Luna for mechanical bulk edits. Same verify-then-downgrade logic as the pipeline, applied to my own tooling spend. Replay model tiers will be selected separately from verified callable API models during the approved replay-plan phase.

**Email export correction.** The first Gmail Apps Script intentionally exported only messages I sent, leaving received messages buried inside quoted reply history. Revised the export to include every message in the manually curated Minnesota-deal label and to record both From and To headers, so ingestion can represent both sides without reconstructing threads from quotes.

**First parser failure and correction.** The first Gmail fixture run failed because each 60-character separator was followed by a blank line, so the parser expected `Subject:` one line too early. The safe fixture exposed the assumption immediately. Updated the parser to skip export-only leading blank lines, recorded the decision, and reran both Gmail and iMessage fixtures successfully.

**Cross-channel timestamp decision.** Gmail exports include a Pacific UTC offset, while the iMessage export has no timezone. Because both exports were downloaded in San Francisco, iMessage timestamps are interpreted as `America/Los_Angeles` before merging, and the merge rejects any Event whose timestamp still lacks timezone information.

**Redaction verification boundary.** The final checker confirms that known original strings from mapping.yaml do not remain in a chosen publishable file. It cannot discover a sensitive value that was never added to the mapping; mapping completeness remains a deliberate human review step. Run the checker after redaction and again before sharing or publishing later artifacts.

**Email-pattern verification correction.** The first negative fixture revealed that the heuristic email pattern missed addresses followed by sentence-ending punctuation. Corrected the boundary rule and reran both passing and deliberately failing fictional fixtures.

**Redaction verification simplification.** Removed case-insensitive mapped-string verification after review. Exact mapping entries remain the source of truth, boundary-aware replacement prevents substring corruption, and the separate structural scan checks for unknown PII-shaped text. Chose the simpler design for v1 explainability.

**Decision framework from the original deal.** When a problem appeared, I tried to define it clearly, expose my assumptions, use what I knew about every person involved, reason upward from the most defensible truths, seek outside perspectives, schedule concrete action, write to organize my thinking, and develop the strongest arguments against my intended plan. I also used mind maps and scenario branches to prepare reactions in advance. The underlying posture was to maximize the odds rather than demand certainty: notice every useful opportunity, accept that outcomes cannot be guaranteed, and stay calm enough to keep acting.

**Operationalizing the framework for models.** General advice such as "think from first principles" is too vague to test. In the v1 replay design, Condition B turns a restrained version of the framework into required outputs: objective and constraints; observations/facts versus claims; assumptions; stakeholders and incentives; uncertainties and valuable missing information; then options, downside, counterparty response, chosen action, and immediate next step. The full framework — broader perspective gathering, richer scenario trees, scheduling, written state, and systematic arguments against the plan — is a candidate for a later workflow experiment after the first demo ships.

**Evidence and authority rule.** Professional or expert status is evidence about a source's likely knowledge, not a substitute for reasoning. Keep observations, external claims, interpretations, predictions, and decisions distinct. Expert conclusions can receive weight from experience and base rates, but they should not silently become facts when their evidence or reasoning is unclear.

**Disciplined audacity.** Do not tune a model by merely telling it to be aggressive. Route it using downside bounds, reversibility, cost of delay, objective clarity, and counterparty dynamics. The desired behavior is bold action when downside is bounded and upside is asymmetric, paired with caution around irreversible or catastrophic outcomes. A later version should test whether this risk posture corrects models that default to excessive caution without producing reckless confidence.

**Future version — microdecision audit.** After the first hiring demo, sample roughly 12–20 ordinary decision points across draft, chase, gather, verify, coordinate, and reconcile. Give the model only the information available at each moment and have the owner judge each proposed next action as safe to automate, useful with human approval, or incorrect/unsafe. This would test day-to-day decision quality; primitive classification by itself only proves that the model can label work, not perform it.

**Future version — continuous delegation loop.** The end-state system would maintain a live representation of the situation, execute bounded routine actions, observe responses, update its state, escalate consequential decisions with organized context, execute the human's choice, and continue. Escalation should depend on reversibility, capped downside, legal/financial/reputational commitment, adversarial effects, objective ambiguity, and evidence quality — not whether an action merely looks "small."

**Future version — cross-domain transfer.** Test which parts of the decision loop transfer beyond this transaction: objective discovery, evidence discipline, stakeholder modeling, option generation, value-of-information questions, scenario triggers, risk routing, execution, and feedback. Candidate applications include other real-estate transactions and a distressed-property renovation workflow that ranks repair bundles by cost, time, expected sale-price increase, uncertainty, holding cost, and ROI. Domain data changes; the decision machinery may transfer.

**Future evaluation safeguards.** A broader study could predefine replay-specific rubrics, blind condition/model identities during human scoring, repeat the most important cells to measure run-to-run variation, and compare raw, triage-only, and fuller decision-protocol workflows. It must also state the counterfactual limitation: the historical record reveals the outcome of the action actually taken, not with certainty what every alternative would have produced.

**V1 scope decision after the broader autonomy discussion.** Do not add the microdecision audit or continuous agent to the first shipping path. Preserve both A/B conditions, run replays 1 and 4 first across all three tiers, and use the report's Capability Matrix to describe the immediate operating model: AI acts on bounded work, AI prepares consequential work for approval, and humans lead strategic or irreversible decisions with AI-organized context.

**Replay experiment redesign.** Split the experiment into raw, structured-reasoning, and clarification conditions so reasoning-process lift can be separated from intent-transfer lift. Made the long-trajectory artifact, two headline replays across three tiers and three repeats, and quality-versus-cost reporting must-ship; deferred breadth.

**Replay integrity cleanup.** Neutralized outcome-bearing replay IDs, made prompt leakage boundaries and the two-call Condition C explicit, separated historical-action matching from decision quality, froze retry and model-configuration rules, and restored a mapped case-variant privacy warning.

**Notebook-method replay scaffold.** Conditions B and C now organize context into the same five-part evidence brief before any decision; C derives up to three owner-answerable questions from its ranked unknowns before Call 2 decides. Decision-quality scoring can fully credit defensible alternatives, while historical-action matching remains separate. The headline grid uses one model family at maximum explicit reasoning effort and reports actual cost; a second-provider replay-4 check is post-v1. Rejected a separate model preflight system as unnecessary: explicit model IDs, UTC timestamps, frozen settings, and the existing unscored vertical slice are enough for this demo.

**[FILL] — Redaction verification results.** What the leak-check grep caught on its first run, if anything, and what was added to mapping.yaml as a result.

**[FILL] — Anything that surprised me.** Standing rule: one line, same day, every time an agent does something unexpectedly good or unexpectedly bad.

**Redaction and verification correction.** Replacement and mapped-source verification now share one capitalization policy: mapped sources are case-insensitive except exact-case `Me -> ME`, preserving ordinary lowercase pronouns. Mapped sources, emails, telephone numbers, and possible street addresses remain blocking findings. Generic long-digit sequences are advisory because they may represent either sensitive numbers or harmless structural identifiers. Standard UUID-contained runs are suppressed. The real corpus passed all blocking verification. The owner reviewed the 15 remaining numeric advisories and classified all of them as public application IDs or generated URL, email, and attachment metadata. No mapping changes were required.

**V3 experiment freeze (superseded for execution by the Tier 1a addendum below).** Build specification v3 freezes Tier 1 at two headline replays, three conditions, three model tiers, and three repeats per cell: 54 scheduled attempts. Every condition receives the same minimal owner-written task brief and authority boundary. Decision quality and intent discovery remain the two headline axes; diagnostic recurrence is reported within comparable three-repeat cells.

**Notebook-derived interface and clarification.** Conditions B and C use five notebook-derived containers with nine nested completeness blocks. The first call organizes without choosing an action. Condition C asks up to three questions derived from ranked unknowns and receives only verified answers. The scaffold is a floor rather than a ceiling, and concrete work products must distinguish the stated request, inferred outcome, permissions, recommendation, and verification.

**Evaluation boundaries and deferred scope.** The owner authors the task briefs, ground truths, operator states, and replay rubrics. Defensible alternatives may earn full decision-quality credit, while historical-action matching remains separate. One-owner judgment, hindsight, unequal calls, scaffold circularity, and limited generality are disclosed. Document ingestion remains an owner decision within the Tier 1a pre-run path; deferred experiments live in POST_SHIP.md.

**Tier 1a execution addendum.** Tier 1a narrows scored execution to Replay 04 under Conditions A, B, and C across three model tiers and three repeats per cell: 27 scored attempts. Replay 01 becomes the first post-ship expansion. Document ingestion may proceed in parallel with replay planning and development, synthetic tests, schemas, persistence, and the report skeleton, but ingestion, merge, redaction, verification, and owner review must finish before the final Replay 04 context pack, real vertical slice, or scored attempts. All other approved v3 architecture, experimental, provenance, scoring, trajectory, reporting, privacy, and publication requirements remain in force.

**Episode segmentation correction.** Segment the full transaction timeline into coherent named episodes around meaningful changes in goal, actors, situation, or outcome. Roughly 8–12 episodes is a report-readability target rather than a quota; use fewer or more when the evidence supports it, then hand-correct the result.

---

## Replay 04 manual pilot — Phase 0

This section records pilot setup and methodology observations only. It is not a result from the scored experiment and must not enter experimental-agent evidence or input.

**Pilot setup failure.** The initial corpus audit incorrectly concluded that no earlier approximately-$150K offer history existed. The evidence was present, but a long-running search returned no immediate output and the agent failed to await completion. This demonstrates that agentic knowledge-work reliability depends not only on reasoning quality but also on correct tool-state handling and retrieval completion.

**Corrected earlier-offer evidence.** The pre-cutoff corpus contains two distinct earlier approximately-$150K offer communications. V1 conclusions use that corpus-supported communication-level distinction and do not rely on additional private owner recollection.

**Pilot interpretation, not a scored-experiment conclusion.** Two similar-price communications are stronger evidence of the relevant market level than one isolated communication. This can matter when interpreting the later decision-triggering offer, but it does not change the experimental cutoff or require a redesign of Replay 04.

**Final Phase 0 conclusion.** Replay 04 passes the viability gate for the stripped-down manual pilot.

Historical cutoff methodology:

- Use the first timestamped outbound response to the decision-triggering offer as the cutoff.
- Include only events timestamped before that response; exclude the response and every later event.
- Preserve eligible inbound material immediately before the response, but suppress untimestamped reaction metadata whose timing cannot be established as pre-response.

The eligible pre-cutoff corpus contains meaningful contemporaneous evidence including:

- the owner's sell-soon objective and decision authority;
- property condition, repair, and sale-preparation history;
- agent valuations and pricing posture;
- earlier investor-offer communications and the owner's responses;
- listing activity and recent market signals;
- the decision-triggering offer and its known headline terms.

Material gaps remain, including the complete formal offer and some contractual terms, proof of funds, and some unavailable or untranscribed phone and audio context. These gaps are allowed to remain unknown. A competent agent should identify material uncertainty rather than have the experiment retroactively fill every missing detail.

## 2026-08-12 — Replay 04 pilot follow-up descriptive checks

The initial exploratory Work pilot consists of A1, B1, and C1. Review of those runs surfaced several useful descriptive observations that were not preregistered before those runs. They therefore remain post-hoc/exploratory for A1/B1/C1.

Before running the bounded A2/B2 follow-up, the following descriptive checks were frozen for A2 and B2 only:

1. **Known prior-offer recovery** — record how many of the two known earlier approximately-$150K offer communications are recovered: 0/2, 1/2, or 2/2. An offer counts as recovered only if the response identifies it as a distinct earlier approximately-$150K offer communication. A generic statement that there had previously been approximately-$150K investor interest does not count as recovering both offers.
2. **Evidence integration** — if either prior offer is recovered, record whether it is meaningfully integrated into the final reasoning. Meaningful integration means the recovered evidence is used to support, modify, constrain, or compare the recommendation, price range, confidence, or fallback policy. Merely listing or mentioning the evidence does not count.
3. **Unsupported factual claims** — record any material factual claim presented as established without visible support in the supplied evidence.
4. **Opening action** — record the initial recommended action and relevant price/terms.
5. **Fallback policy** — record what the model recommends if the opening move is rejected or the buyer holds firm.

These are descriptive checks, not new rubric scores or headline metrics. The existing frozen rubric remains the scoring rubric.

A2 and B2 are sensitivity/follow-up runs using the same respective treatment procedures as A1 and B1. Their prompts or context were not altered in response to the exploratory findings above, and the models were not shown results from earlier pilot runs.

Visible recovery varied across nominally identical structured passes: B1 and B2 each surfaced one of the two earlier communications, but not the same one, while C1 surfaced both during its structured stage before asking clarification questions. These are run-level observations, not retrieval-rate estimates. Clarification must not be credited for C1's pre-clarification retrieval.

Retrieval and integration remain distinct: surfacing an earlier communication does not establish that it materially affected the recommendation. A versus B is also a bundled comparison because B adds both a structured intermediate representation and another opportunity to search and reason; the pilot cannot isolate which part caused any observed difference.

Unless A2/B2 exposed a necessary experimental defect, no additional pilot conditions or repeats were to be added before scoring and analysis.

## 2026-08-12: V1 execution reconciliation

The v3 design planned a 27-attempt Replay 04 grid. The later nine-run manual pilot was created to inform that design and explicitly did not replace it. What actually ran in Work was the exploratory A1/B1/C1 pilot plus the bounded A2/B2 follow-up; a separate Codex A1 remains a side observation. The owner later decided to ship those five Work runs as an exploratory V1 rather than mechanically complete either stale grid. The unexecuted pilot remainder and 27-attempt design are deferred, not completed.

The follow-up descriptive checks and stop rule immediately above were recorded locally before A2 and B2 began. Preserved local metadata places the `NOTES.md` modification before both Codex run start times, although the note was not committed before the runs. Describe them as pre-run descriptive checks recorded in `NOTES.md`, not Git-preregistered metrics. The frozen rubric remains unchanged, and the final owner-adjudicated scores are locked in `V1_STATUS.md`.

## 2026-08-14: Final V1 score lock

The owner finalized A1/A2 Evidence Retrieval at `1` and C1 Actionability at `2`, resolving the remaining scoring disputes without changing the frozen rubric. All five Work runs officially meet the STRONG threshold, but that count is anchor-sensitive: the plausible alternate A-run Retrieval score of `0` would produce `3/5` rather than `5/5`, so the STRONG count is not a headline finding. Earlier provisional/reconstructed scoring remains part of the experiment chronology rather than being presented as though the final values had always been fixed.
