# Deal Autopsy — Build Specification v3

**STATUS: FROZEN FOR TIER 1a EXECUTION.**

**Central thesis:** Deal Autopsy turns the redacted digital exhaust of a real $226K distressed-property sale into a reproducible test of whether structured context and targeted clarification help an AI convert a short human request and messy evidence into correct, evidence-grounded, executable work while respecting human authority boundaries.

**What the finished artifact should demonstrate:** You can test models against consequential real-world decisions, ship clean code and a tested interface, understand knowledge work outside SF because the corpus comes from your own life, and recognize a valuable data class before anyone asks: a long trajectory linking messy context to decisions and delayed outcomes.

**Framing rule for the README and video:** This is not a "% correct" benchmark, a general model benchmark, or a general-purpose product. It is a real-trajectory evaluation case study. Real knowledge work arrives as messy context and a short request whose objective, constraints, proxy goals, dependencies, and authority boundaries may be incomplete. The experiment compares model capability, a two-stage structured workflow, and targeted clarification. Added calls, compressed representations, latency, cost, and owner input are measured tradeoffs rather than hidden sources of improvement.

## Changes from v2

- The initial task brief is now a minimal realistic user request rather than a complete human-authored specification.
- Explicit authority boundaries remain part of every condition.
- Replay 01 is the operational outcome-execution test; Replay 04 is the consequential-judgment and escalation-boundary test.
- Every condition must produce concrete, usable work products rather than advice alone.
- The common output distinguishes the stated request from an inferred underlying outcome.
- A means-versus-end check tests whether the requested action is only one possible route to the user's outcome.
- The nine simple conceptual blocks are a completeness check nested inside the existing five-part notebook-derived scaffold.
- Condition C derives questions from ranked missing blocks.
- Human input burden is measured.
- Notebook provenance is confirmed as contemporaneous.
- Redaction replacement and verification now share one matching policy.
- Tier 1a execution is narrowed to Replay 04; Replay 01 and document ingestion move behind the first shipped artifact.

## Tier 1a execution addendum

Tier 1a executes Replay 04 under Conditions A, B, and C across three model tiers and three repeats per cell: 27 scored attempts.

Replay 01 is the first post-ship expansion. Document ingestion is deferred until after the Replay 04 artifact ships because the existing iMessage corpus fully supports the headline replay.

This addendum narrows execution scope only. All other approved v3 architecture, experimental design, provenance, scoring, trajectory, reporting, privacy, and publication requirements remain in force.

## Experimental question

When the AI fails to do what the user actually intended, is the strongest observed bottleneck:

- model capability
- organization of available context
- missing or underspecified intent
- literal optimization of a poor proxy or requested means
- authority and escalation calibration

This matters because:

- It tests an outcome-based computer-work thesis on actual, messy real-world evidence rather than a clean synthetic prompt.
- It tests whether the operator's own contemporaneously documented problem-solving method improves model performance.
- It evaluates whether product design can supply some of the problem framing, evidence discipline, and clarification that otherwise depend on the user.
- It evaluates the gap between a user's short request and reliable work.
- It does not evaluate live GUI execution.

Frontier models provide substantial capability, but users still differ in their ability to specify valuable outcomes, structure ambiguous situations, recognize proxy goals, judge outputs, and correct course. Deal Autopsy tests how much of that gap can be supplied by an interface.

Do not claim cross-user, cross-company, or cross-domain generality. Do not claim that AI is purely a multiplier or that all remaining human performance differences live upstream of execution.

---

## 1. What the finished thing looks like

A public GitHub repository, one hosted URL, and one self-contained HTML report that also works from `file://` with networking disabled. The report loads directly into the real replay interface, not a marketing page, splash screen, or analytics dashboard.

1. **Replay interface** — the default loaded replay makes the decision situation, the model's proposed action, the operator's historical action, and the observed outcome understandable without interaction. Replay, model-tier, condition, and repeat controls remain visible. Show only context available at the decision, the model workflow, concrete work products, scores, and measured costs.
2. **The trajectory** — hero facts ($226,000 close vs. $150K prior ceiling, duration, generated event count, and dollar volume), a timeline segmented into episodes, and a public `trajectory.jsonl` connecting each replay's prior state, decision, action, and delayed outcome.
3. **Findings** — compare bundled structured-workflow lift, clarification lift, model-tier lift, and cost. Show decision quality, intent discovery, diagnostic recurrence, option generation versus selection, owner input burden, calls, tokens, latency, and dollars. State the result that actually occurred.
4. **Primitive decomposition and capability routing** — include only if classification is complete. Compare action frequency with outcome leverage, then route each supported primitive to AI acts / AI prepares and a human approves / human-led with AI support. Label unsupported routing conclusions as product hypotheses.
5. **Methods and limitations** — prompts, frozen materials, all run records, privacy method, one-owner scoring, hindsight risk, unequal call counts, exploratory sample size, notebook-method circularity, batched clarification, lack of live GUI execution, and other constraints needed to interpret the findings honestly.

---

## 2. Architecture

```
raw/                  # real exports (NEVER committed, NEVER read by the coding agent)
sample/               # tiny synthetic corpus, committed, so others can run the pipeline
src/
  ingest.py           # every source -> events.jsonl (verbatim extraction, no identity logic)
  redact.py           # ALL identity transformation, in exactly one place
  episodes.py         # strong-model pass: segment timeline into named episodes
  classify.py         # cheap-model pass: tag each action with a primitive
  replay.py           # the harness (see section 5)
  report.py           # renders everything into report.html (templated, no server)
replays/
  01_the_150k_offer/        # each = owner brief/rubric/truth/state + context + transcripts/
  02_padded_quotes/
  03_silent_tenant/
  04_the_220k_counter/
  05_meter_payment/          # Tier 2
trajectory.jsonl            # public redacted decision/outcome rows
report.html
README.md             # doubles as the product memo
NOTES.md              # agent-driving log: failures, corrections, decisions, surprises
AGENTS.md             # standing instructions for the coding agent
POST_SHIP.md          # concise deferred work; no Tier 1a scope expansion
mapping.yaml          # real string -> pseudonym (NEVER committed)
```

**Event schema:**

```python
class Event(BaseModel):
    id: str
    timestamp: datetime
    channel: Literal["email", "imessage", "whatsapp", "bank", "invoice", "payment_app"]
    actor: str            # verbatim from source; pseudonymized later by redact.py
    counterparty: str
    text: str
    amount: float | None
    source_file: str
```

Each headline replay contains owner-authored `task_brief.md`, `ground_truth.md`, `operator_state.md`, and `rubric.md`, plus a generated redacted context pack and immutable run records. Agents may scaffold and validate owner-authored files but must not supply their substantive contents.

**Stack:** Plain Python + pydantic and PyYAML, direct model API calls (no LangChain, no agent frameworks, no databases, and no application server), and one static HTML file. Static hosting is allowed. Required report assets are rendered directly or embedded so the report works offline; do not depend on a CDN. The agent-building and verification process is recorded through concrete failures, corrections, tests, and commits in `NOTES.md`.

---

## 3. Pipeline

**Step 1 — Ingest.** One parser per source (iMessage, Gmail, WhatsApp, payments) producing Event rows into `events.jsonl`. Parsers extract VERBATIM — no identity mapping in parsers, ever; identity appears inside message bodies, not just sender fields, so partial mapping anywhere creates unauditable leaks. The existing iMessage corpus fully supports Replay 04. Document ingestion remains a pending owner decision and is deferred until after the Tier 1a artifact ships. The current proposed approach is for the owner to hand-list only deal-relevant facts and transactions from local PDFs in a simple CSV rather than parse the PDFs. Do not treat that approach as approved until the owner selects it. Target after any post-ship expansion: one clean chronological JSONL.

**Step 2 — Redact.** `mapping.yaml` holds every real string → pseudonym. Replacement and mapped-source verification share one boundary-aware policy: mapped sources match case-insensitively except exact-case `Me` → `ME`, which preserves ordinary lowercase pronouns. Capitalization-equivalent aliases coalesce only when they produce the same pseudonym; collisions fail safely without printing source values. Raw files remain local and never enter agent or replay-model context. A separately authorized, isolated mapping task may inspect extracted identity candidates and `mapping.yaml`; record that exception honestly. No unredacted corpus reaches replay or analysis models. Verification blocks on surviving mapped sources, emails, telephone numbers, and possible street addresses. Generic long-digit sequences remain visible as owner-review advisories; standard UUID-contained digit runs are suppressed as unambiguous structural metadata. Run verification over every model-visible or publishable output, including owner-authored replay files and staged Condition C answers before API use.

**Step 3 — Episodes.** Strong-model pass to segment the timeline into 8–12 episodes (goal, actors, duration, outcome). Hand-correct. This remains early because it creates the visual timeline and helps define replay context windows.

**Step 4 — Replays and report vertical slice.** Before broad classification, complete one headline replay end to end: frozen owner-written minimal task brief, rubric, ground truth, and operator state → redacted context pack → all three conditions for one model → recorded run metadata → scored transcript → visible work product in the report. Start the report skeleton as soon as this vertical slice exists.

**Step 5 — Classify, if the central experiment is working.** Tag outbound actions with one primitive. Routing protocol (verify, then downgrade): hand-label 50 events, run the cheap model on the same 50, and measure agreement. At ≥95%, the cheap model owns the task; below that, fix the prompt and retry or escalate only uncertain rows. Record measured agreement in `NOTES.md`. Do not delay the headline replay experiment for full-corpus classification.

**The taxonomy:**

| Primitive | Definition | Deal examples |
|---|---|---|
| draft | compose a document or message | offer emails, POA, notarized agreement |
| chase | follow up until response | tenant silence, vendor callbacks |
| gather | source options and information | dozens of agent interviews, CMAs, quotes |
| verify | test a claim against ground truth | site visits, payment conditioned on Xcel inspection |
| negotiate | adversarial exchange with stakes | tenant move-out, $220K→$232K counter, commission design |
| decide | commit under uncertainty | rejecting $150K, repair-vs-sell-as-is |
| coordinate | multi-party scheduling and logistics | closing sprint, key handoff |
| reconcile | match money to paper | payments vs. invoices vs. statements |

---

## 4. Owner-authored replay materials and trajectory data

Every substantive replay-specific success criterion, historical fact, preference, constraint, action, and outcome is written by the person who lived the deal. Agents may scaffold headings and validate structure, schema, completeness, and redaction; they never generate, edit, rewrite, improve, or infer the substantive content.

### Minimal task brief

Every headline replay begins with one frozen owner-written `task_brief.md`. It is the shortest realistic one- or two-sentence request a person might give an outcome-oriented computer at that moment, not a complete specification.

The brief contains:

- the user's stated request or desired outcome
- only constraints the user would naturally state then
- the explicit authority boundary
- actions clearly reserved for owner approval

It does not need to contain complete success criteria, hidden preferences, every material tradeoff, all constraints, subgoals, dependencies, missing information, or the best means. Recovering, organizing, or eliciting those elements is part of the experiment. The identical frozen brief is supplied to Conditions A, B, and C.

The brief must not contain the historical answer, post-decision events, the observed outcome, hindsight, private ground-truth reasoning, or the complete operator state. Codex may scaffold and validate it but must not write, rewrite, improve, or infer its substance.

Replay 01's brief preserves the accept-versus-repair fork; it must not assume that renovation, targeted repairs, relisting, rejection, or acceptance is correct. Replay 04's brief may ask the AI to evaluate the current offer and prepare a response, but accepting, rejecting, or countering requires owner approval.

### Ground truth

Each `ground_truth.md` uses these owner-written headers:

- **Situation** — what was happening at that moment
- **Context available** — what information existed then and only then
- **What I did**
- **Why** — full reasoning, including counterparty dynamics and what a naive optimizer could miss
- **Outcome** — with dollar figures where they exist

The Why section is the evaluation's rarest content. For Replay 04, the historical reasoning includes the speed trap: fast acceptance could signal desperation and invite a renegotiation spiral. That reasoning belongs only in ground truth and must never be supplied as a clarification answer or generation input.

### Operator state

Each headline replay has an owner-written `operator_state.md` frozen before scored runs. It contains:

- stable fact ID plus contemporaneous observation or event
- stated preferences, constraints, and tradeoffs
- beliefs and uncertainties held at the time
- facts that may not be explicit in the digital context

It excludes the eventual outcome, hindsight, the ground-truth action, and strategic conclusions the model must discover. Condition C receives only verified redacted answers to questions it actually asked, at the same specificity as the question. Do not volunteer additional reasoning. If an answer is absent, respond: "That information was not available in this replay."

### Frozen replay rubric

Each headline replay has an owner-written `rubric.md` frozen before any scored run. Because the task brief is intentionally minimal, this rubric is the evaluator's precommitted definition of successful performance. It tests whether the model correctly reconstructs or elicits:

- the underlying outcome
- material constraints and tradeoffs
- success criteria
- authority boundaries
- necessary work products
- factual grounding and verification requirements

The rubric must permit defensible alternatives, separate outcome quality from historical-action matching, exclude the eventual outcome as a required answer, avoid rewarding hindsight, and specify approval discipline. Generation models never receive it.

Codex may scaffold rubric headings and validate completeness or schema. It must not invent substantive criteria, rewrite the owner's wording, infer criteria from the observed outcome, or improve the rubric.

All owner-authored replay files use pseudonyms and pass redaction verification before freeze, commit, or use.

### `trajectory.jsonl`

Publish a redacted trajectory row for each completed replay. It is a specimen of the long-trajectory data class missing from conventional evaluations: state before a decision → options → action → delayed outcome. At minimum:

```json
{
  "decision_id": "replay_04",
  "decision_timestamp": "ISO-8601 timestamp",
  "context_event_ids": ["event IDs available before the decision"],
  "state_summary": "owner-authored contemporaneous state",
  "objective_at_the_time": "owner-authored objective",
  "constraints": ["owner-authored constraints"],
  "options_considered": ["historical options, if known"],
  "action_taken": "historical action",
  "outcome": "observed outcome",
  "outcome_lag_days": 0,
  "dollar_delta": null
}
```

Generate and validate this file from redacted events plus frozen owner-authored materials. The owner supplies every substantive trajectory field. Code may assemble identifiers and timestamps, copy owner-supplied fields, and validate the schema, but it must not infer or summarize state, objectives, options, actions, or outcomes. Counts in the README and report come from generated artifacts rather than hardcoded copy.

## 5. The replay harness (the intellectual center — plan reviewed before building)

Before any `replay.py` code, write a concrete implementation plan covering prompt text, schemas, owner-answer handling, run IDs, persistence, retries, scoring inputs, failures, supported parameters, and cost limits; obtain owner approval. This is the remaining Tier 1a approval gate.

For each replay, create one frozen redacted context pack containing events available up to the decision timestamp and nothing afterward. Hold constant across conditions:

- owner-written minimal task brief
- initial historical context
- model tier and family
- supported settings
- common output schema
- retry rules
- cost accounting
- frozen materials

Generation prompts never contain ground truth, outcomes, scores, rubrics, post-decision events, or replay filenames and slugs. Use outcome-neutral internal replay IDs. Conditions A and B never receive `operator_state.md`. Condition C receives only verified, redacted answers to questions it actually asked, never the complete file.

### Condition A — minimal request plus raw historical context

One deciding call receives the task brief and full context pack. It must reconstruct the outcome, generate options, make a recommendation, and produce the common work product without a separate reasoning scaffold or clarification.

### Conditions B and C — five-part notebook-derived scaffold

The structured-reasoning scaffold was derived from a contemporaneous handwritten problem-solving framework the operator used during the transaction. The runtime scaffold remains a tested interface hypothesis, not a claim that it is universally optimal.

The five parts below are the output containers. Their required contents are the nested simple-block completeness check, not nine additional peer-level sections.

The nine conceptual blocks are:

- outcome, with stated request and inferred underlying outcome distinguished
- success criteria
- constraints and tradeoffs
- documented facts and observations
- claims, assumptions, and inferences
- missing information
- authority and permissions
- subgoals and dependencies
- verification conditions

The means-versus-end and alternative-solution checks operate inside the Decision frame rather than adding new sections. The Stakeholder map remains one of the five notebook-derived containers; it does not replace verification conditions in the completeness check.

1. **Decision frame**

   Required contents:

   - stated request
   - inferred underlying outcome, clearly labeled as an inference and briefly grounded
   - success criteria
   - explicit and materially inferred constraints
   - material tradeoffs and conflicts
   - means-versus-end check
   - alternative solution hypothesis
   - authority boundary and permissions

   The means-versus-end check asks whether the requested action is only one possible means of achieving the user's underlying outcome. The alternative solution hypothesis asks whether another framing or solution class may better satisfy the user's values. Ground the inferred outcome inline. Do not create separate fields for confidence/evidence or clarification need; clarification need belongs only in Ranked unknowns.

2. **Evidence ledger**

   Required contents:

   - documented facts and observations
   - stakeholder claims
   - operator claims
   - assumptions
   - inferences
   - source event IDs where available

3. **Stakeholder map**

   Required contents:

   - incentives
   - leverage
   - likely reactions
   - uncertain or inferred elements clearly marked

4. **Dependency and causal map**

   Required contents:

   - required subgoals
   - ordering and dependencies
   - how evidence and actions connect to the outcome
   - verification conditions
   - gaps in the chain

5. **Ranked unknowns**

   Required contents:

   - missing blocks of information
   - why each matters
   - whether the answer could change the plan or work product
   - best available source
   - whether the owner can answer it
   - stable unknown IDs

The core hypothesis is: break the outcome and situation into simple, evidence-backed blocks, identify the consequential missing blocks, and ask the user only about the highest-value missing information. Do not introduce another ontology or reasoning framework beside this.

### Condition B — structured reasoning

Call 1 receives the task brief and context pack and produces the five-part brief without recommending, drafting, choosing, or scheduling an action. Call 2 receives the brief and produces the common output. No new factual information enters this condition.

A → B estimates the bundled effect of a two-stage structured workflow, including an extra model call and a compressed representation. It does not perfectly isolate organization.

### Condition C — structured reasoning plus clarification

Call 1 creates the same five-part brief as B, then derives no more than three questions from the highest-value ranked missing blocks that the owner can realistically answer. Each question references its stable unknown ID and states why the answer could materially change the plan or work product.

The owner answers under the frozen `operator_state.md` policy. Save each answer as redacted local text and verify it before API use. Call 2 receives Call 1's brief verbatim plus only the verified verbatim answers to questions actually asked, then produces the common output. There is no intermediate model invocation.

B → C estimates clarification lift while holding the scaffold and number of model calls constant. A → C estimates total guided-interface lift. Condition C does not prove whether the owner already knew but failed to express something, held conflicting preferences, or discovered a new implication through the question.

Tier 1a uses one batched clarification round. This is a lower bound on what adaptive dialogue could recover; adaptive multi-round clarification is a named post-ship experiment.

### The scaffold is a floor, not a ceiling

The five-part brief defines the minimum evidence and decision structure the model must make explicit. It must not restrict the model to the user's literal framing, historical options, eventual action, schema examples, or a fixed solution class.

The model may surface additional considerations, challenge a false premise, identify a better means, propose a non-obvious solution, or place an alternative solution class in the option set. It must not silently replace the user's objective. A materially different objective or consequential change to commitments or authority must remain a grounded hypothesis or recommendation requiring owner approval.

### Common output: options, permissions, and concrete work

Every condition returns the same replay-appropriate schema:

- stated request
- inferred underlying outcome, distinguished from the stated request
- two to four viable options and their tradeoffs
- recommended action
- one structured work product appropriate to the replay
- exact draft message, document, checklist, or instruction where applicable
- immediate next steps
- permissions
- verification condition
- follow-up trigger
- strongest case against the recommendation, including its major downside
- new evidence that would change the recommendation
- likely counterparty response

The permissions field states what the AI could perform autonomously, what it may only prepare, and what requires owner approval. Do not add live external execution.

### Headline replay roles

**Replay 01 — first post-ship expansion and operational outcome-execution test.** It tests whether the AI preserves the accept-versus-repair fork, distinguishes non-equivalent offers and scopes, organizes evidence, identifies sale blockers and missing information, produces usable comparisons and follow-ups, respects approvals, and defines completion verification. It must not assume repairs are already the chosen strategy.

**Replay 04 — Tier 1a consequential-judgment and escalation-boundary test.** It tests whether the AI identifies the conflict among speed, price, certainty, and risk; distinguishes a stated preference from the outcome it serves; models likely counterparty response; prepares a defensible recommendation and exact response; and recognizes that the consequential final action belongs to the human.

The remaining replays retain their existing roles:

1. **The $150K offer** — accept, or preserve the repair/relist fork? Tests: decide, verify, and produce executable comparison work.
2. **The padded quotes** — accept early quotes or keep sourcing and cross-checking scopes? Tests: gather and price skepticism.
3. **The silent tenant** — what bounded next move should follow refusal and silence? Tests: negotiate and draft.
4. **The $220K counter** — evaluate the offer under the speed trap and prepare a response. Tests: intent discovery, second-order counterparty reasoning, and escalation.
5. **The meter payment** (Tier 2) — condition payment on utility inspection? Tests: verify.

### Model tiers and repeats

Use three tiers from one provider family for the headline grid so provider differences do not contaminate the tier curve. Pin explicit model IDs and use the same maximum reasoning effort supported by all three anchor tiers. For a GPT-5.6 anchor grid, set `reasoning.effort` to `max`, omit temperature and seed, and do not enable pro mode. Actual reasoning tokens, latency, and cost remain measured outcomes.

For Replay 04 in Tier 1a, run every condition × tier cell three times: 27 scored attempts. Complete one unscored vertical slice first, then freeze scored-run materials and execute every scheduled repeat. Publish all transcripts, including failures. Three repeats are exploratory evidence, not a statistically generalizable benchmark. Replay 01 uses the same experimental architecture when it becomes the first post-ship expansion unless a later approved addendum changes it.

### Scoring: two headline axes

1. **Decision quality** against the frozen replay rubric. Define it broadly enough to include factual and evidentiary accuracy, correct understanding of the stated request, reconstruction of the underlying outcome, recommendation quality, usability of the structured work product and execution artifact, approval discipline, and verification quality.
2. **Intent discovery**, scored `0`–`2`:
   - `0` — optimizes the surface request without reconstructing its material objective, constraints, or conflicts
   - `1` — identifies or elicits important unstated preferences, constraints, or success criteria
   - `2` — identifies the deeper conflict or proxy beneath the request, explains its material consequences, and handles it through a grounded proposal or targeted clarification

Replay-specific frozen criteria define these levels in context. Replay 04's highest level preserves the speed-trap logic. A response may receive full decision-quality credit without matching the historical action when it satisfies the frozen criteria using only contemporaneous evidence. Historical-action matching remains separate.

Report separately:

- whether the historical move appeared in the option set
- whether it was selected
- questions asked
- fact IDs recovered
- calls
- input/output tokens
- latency
- cost

Observed dollar outcomes may be historical context but must never be attributed to a model as counterfactual value created or saved.

### Diagnostic labels

The human scorer may attach four fixed diagnostic labels: `missed_relevant_evidence`, `treated_claim_as_fact`, `misunderstood_objective`, or `ignored_counterparty_response`. They explain failure mechanisms and are not a third scoring axis.

`misunderstood_objective` applies when the model either follows a literal request despite material evidence that it is a poor proxy for the user's outcome or replaces the user's objective with an unsupported model-generated objective.

Before scored runs, preregister: "Condition A may be more likely than B or C to treat strategic, provisional, or negotiation-posture language as verified operating reality." Use `treated_claim_as_fact`; do not create a posture-blindness score or taxonomy. A failure includes asserting a provisional action had definitely begun, excluding valid options because of that assumption, presenting it as fact without qualification, or drafting work from the unverified literal reading.

### DIAGNOSTIC RECURRENCE

For each diagnostic label, summarize recurrence across the three repeats of the same experimental cell:

`replay × condition × model tier`

Report:

- the number of affected repeats
- the affected repeat IDs

Example:

```text
Replay 04 · Condition A · high tier
treated_claim_as_fact: 2 of 3 repeats
affected repeats: 1, 3
```

Mark a failed, timed-out, or malformed repeat as unevaluable when the diagnostic cannot be judged. Diagnostic recurrence is a compact summary of existing labels, not a new score or headline axis.

### Condition C question diagnostics

Record:

1. `recovered_fact_scope`
   - `stable_operating_preference`
   - `situational_fact`
   - `unknown`
2. `missed_necessary_question` — scorer-judged against frozen ranked unknowns and rubric
3. `unnecessary_question` — true when already answerable from supplied evidence or immaterial to the requested work

These fields distinguish stable user-specific information from one-time situational information. Do not implement personalization in Tier 1a.

### Human input burden

Measure without creating another headline score:

- task-brief word or token count
- owner-clarification word or token count
- total owner-supplied information after the initial request
- number of clarification questions
- whether the model challenged a requested means or proxy
- whether the challenge was evidence-grounded
- whether the challenge respected the authority boundary

The target is minimum necessary clarification, not zero clarification. Never reduce questions at the expense of correctness.

### Product interpretation

For every major finding, state which bottleneck the evidence most strongly suggests: model capability, context organization, intent transfer, user framing or proxy-goal failure, or authority calibration. Tie the interpretation to transcripts, produced artifacts, clarification questions, rubric results, and diagnostic labels.

Do not claim a general law from one trajectory or claim that a historical dollar outcome proves what every alternative would have produced. The reusable contribution is a method for turning messy workflow evidence into an auditable test of objective recovery, evidence organization, missing-information discovery, clarification quality, work-product quality, and authority boundaries.

### Run provenance and integrity

Every attempt records a stable run ID, UTC timestamp, replay, condition, model tier and exact identifier, repeat number, supported parameters, prompts, token usage, latency, cost, status, and verbatim response. Failed and aborted scored runs remain recorded with a non-private explanation.

Retry only attempts that fail before a model response because of timeout, rate limit, transport error, or provider 5xx. A completed refusal, malformed response, or poor answer remains the recorded result and is never rerolled. Once scored or reported, a run is immutable; corrections receive new IDs.

Freeze task briefs, prompts, schemas, rubrics, ground truths, operator states, context packs, explicit model IDs, supported settings, retry rules, and cost limits before the first scored run. Run honestly and publish whatever happens, including findings that flatter the models or complicate the thesis.

### Notebook provenance and limitation

Contemporaneous notebook pages have been found. The framework included defining the problem, exposing assumptions, understanding the people involved, reasoning upward from defensible truths, seeking relevant outside perspectives, scheduling concrete action, writing to organize thought, and developing arguments against the intended plan.

Plan exactly one safely cropped and redacted image of the page titled `How to solve a problem` for methods or provenance. Do not publish or transcribe the complete notebook, create a gallery, put notebook reasoning into replay context, or leak the historical answer.

The scaffold encodes the operator's own method, and the graded replays come from episodes where that method was used successfully. This creates mild circularity: lift establishes usefulness for this operator and corpus, not cross-user or cross-domain superiority.

---

## 6. Scope tiers

- **Tier 1a, must ship:** preserve the verified existing ingest/redaction pipeline; owner-written task brief, ground truth, operator state, and rubric for Replay 04; a full-trajectory 8–12 episode timeline locating Replay 04 within the transaction; its public `trajectory.jsonl` row; all 27 scored attempts from A/B/C × three anchor tiers × three repeats; complete run provenance, costs, scores, diagnostic recurrence, and human-input burden; hosted self-contained replay interface; README; methods and limitations; and a 90-second video.
- **First post-ship expansion:** run Replay 01 under the approved experimental architecture.
- **Tier 2, after Replay 01:** run the cross-provider robustness check on Replay 04 under A/B/C × three repeats using the other provider's frontier model, reported separately from the within-family tier curve. Then add Replays 02, 03, and 05, full classification, primitive-frequency and outcome-leverage charts, and an evidence-backed capability matrix.
- **Tier 3, later:** add the Dubai corpus as a second real-world trajectory, a design-partner replication, or additional interface and execution features.

Tier 1a contains exactly three experimental conditions. Do not add a raw-context-plus-clarification condition, adaptive dialogue, personalization, a second provider, a live GUI, or any other experiment before shipping. New ideas go to `POST_SHIP.md`; they do not change the Tier 1a plan.

## 7. Build order from the current position

1. Preserve the committed redaction-policy checkpoint. The current 739-event message-and-email corpus passes blocking verification.
2. The owner writes and freezes `task_brief.md`, `ground_truth.md`, `operator_state.md`, and `rubric.md` for Replay 04. Validate structure and redaction without changing substance.
3. Segment the full transaction timeline into 8–12 episodes and hand-correct the result. Create Replay 04's public trajectory row and begin the report skeleton with fictional generated fixtures.
4. Write the replay implementation plan and obtain owner approval before writing `replay.py`.
5. Complete one unscored Replay 04 vertical slice through persistence, scoring input, and the visible report. Correct the harness before spending on the experiment.
6. Freeze prompts, materials, supported settings, retries, and cost limits. Run and publish all 27 scheduled Tier 1a attempts, including failures.
7. Finish scoring, diagnostic-recurrence summaries, input-burden and cost findings, the static report, README, methods and limitations, offline/mobile checks, and the 90-second video.
8. Ship the Replay 04 Tier 1a artifact and prepare the exact delivery message.
9. Begin Replay 01 as the first post-ship expansion. Resolve the pending document-ingestion decision after Tier 1a ships and before freezing any expanded corpus; merge any resulting rows and rerun redaction and blocking/advisory verification. Agents do not inspect the PDFs or raw rows.

## 8. Video shot list (90 seconds, Loom-raw)

1. **0:00–0:10 — concrete hook.** "At 19, I rejected a $150K ceiling on this distressed sale and closed at $226K, 51% above every prior pre-intervention offer. I later realized I had something models rarely see: the context before each decision and the outcome afterward."
2. **0:10–0:25 — provenance.** Show the local pipeline and generated count without exposing private values. "I reconstructed [generated event count] messages and emails, redacted the corpus, and linked its hardest decisions to their delayed outcomes."
3. **0:25–0:55 — replay interface.** Use Replay 04. Switch A → B → C for one model so the viewer sees the situation, structured brief, targeted questions, model action, historical action, observed outcome, and concrete work product.
4. **0:55–1:20 — findings.** Show structured-workflow lift, clarification lift, model-tier lift, recurrence, human input, and quality versus cost. State one exact result, whichever way it came out.
5. **1:20–1:30 — direct offer.** "I've operated hundreds of hours of messy work across three countries. Give me one user workflow and a weekend; I'll return a concrete instrumented prototype, not a plan."

## 9. README = product memo

Lead with the most surprising generated number, then the thesis:

> Most evaluations contain isolated questions with immediate answers. This repository contains a redacted real-world trajectory: timestamped interactions linked to what was known at each decision, what action was taken, and what happened afterward. The operator who made the decisions wrote the ground truth before any model runs.

Within one scroll: hosted replay link; concrete deal facts; why long-trajectory decision/outcome data matters; A/B/C experimental question; exact findings; quality-versus-cost result; and three product implications, each tied to a numbered transcript, chart, or measured result. Then methods, limitations, architecture, and how to run the synthetic sample. Do not publish unsupported automation claims or generic ideas without evidence.

Include this distinction:

> This case study distinguishes models that optimize the user's stated means from models that recover the outcome those means were supposed to serve. In other words, it tests whether the model merely builds a faster horse or notices that the user may need a car.

Do not call the project "my benchmark," claim that A → B perfectly isolates organization, state a counterfactual dollar gain as fact, or generalize beyond this owner and trajectory.

Prepare the delivery message as part of the artifact:

> You wrote that models lack long-trajectory data connecting business decisions to outcomes. I realized I had one on my laptop: hundreds of messages and emails from a distressed sale I operated at 19, linked to the decisions and outcomes. I turned it into a reproducible interface experiment.

## 10. Canonical Minnesota deal facts

Use these distinctions consistently in the README, report, video, trajectory, and interview materials:

- `$18,473` was a whole-property proposal.
- `$73,625` was a separate maximal-restoration proposal.
- They were not one bid negotiated downward. They represented different scopes and capital strategies, so comparisons between them are imperfect.
- `$78,089` was a separate tenant-damage demand, not a contractor bid.
- The property closed at `$226,000`.
- The owner-approved public framing is: the property closed 51% above every prior pre-intervention offer.
- Do not present the difference between an insurance payment and repair spending as an accomplishment.
- Do not modify the owner's résumé as part of this project.

## 11. Methods and limitations

State these plainly:

- The Tier 1a scored corpus covers one owner, one transaction, and one headline decision; Replay 01 remains defined but unscored until the first post-ship expansion. This does not establish cross-user, cross-company, or cross-domain generality.
- The owner writes the replay materials and performs or approves scoring, creating one-owner judgment and hindsight risks.
- Defensible alternatives can earn full decision-quality credit; matching the historical action is recorded separately.
- A → B is a bundled workflow comparison because B adds a call and a compressed intermediate representation. It does not isolate organization alone.
- B → C estimates clarification lift inside that shared two-call structure.
- Three repeats per cell expose recurrence and run-to-run variation but remain exploratory, not statistically generalizable.
- Batched one-round clarification is a lower bound on what adaptive dialogue could recover.
- The notebook scaffold comes from the same operator and transaction family whose decisions are graded, creating mild circularity.
- Conditions receive different amounts of owner input; measure and report that input rather than hiding it.
- The system produces proposed work and artifacts but does not execute live GUI actions or consequential commitments.
- Historical outcomes do not prove what a model's alternative action would have caused.

## 12. NOTES.md = the receipts

Ongoing log: agent failures and corrections, measured classification agreement, verify-then-downgrade decisions, the isolated mapping exception, replay preregistration changes, report test failures, and anything surprising. Draft concise entries for owner review rather than relying on reminders. Concrete failures, fixes, and verification results outperform claims about "pushing agents to their limits."

## 13. Privacy checklist (before every push and before recording)

- `raw/`, `mapping.yaml`, `.env` in .gitignore from commit zero; verify with `git log --stat`.
- Raw source files remain local and are never inspected by coding agents or sent to replay models.
- Record the separately authorized mapping-task exception; do not describe the whole workflow as "no unredacted text ever reached a model."
- Run the external verifier over redacted events, owner-authored replay files, staged Condition C answers before API use, `trajectory.jsonl`, all transcripts, and `report.html`.
- Block publication on mapped-source, email-address, telephone-number, or possible-street-address findings. Review generic long-digit advisories locally; standard UUID-contained runs remain suppressed as structural metadata.
- No account numbers, no real names of family or counterparties, no street address, anywhere in repo, report, or video frame.
- Recording done with a clean desktop, raw/ closed.

## 14. Definition of done

- A stranger opens one hosted URL and lands directly in a working replay interface.
- The default screen makes the decision situation, model action, historical action, observed outcome, and concrete work product understandable without interaction.
- The report works from `file://` with networking disabled. Every headline condition, tier, repeat, and replay control works with zero console errors on desktop and mobile.
- A stranger clones the repository, runs `make demo` on the synthetic sample, and gets a working report in under two minutes.
- Replay 04 includes A/B/C × three tiers × three published repeats: 27 scheduled Tier 1a attempts with complete provenance, costs, scores, and no selected-away failures.
- Owner-written task briefs, ground truths, operator states, and rubrics are frozen and redaction-verified before scored runs.
- Each replay produces usable work products and separates the stated request, inferred outcome, permissions, recommendation, verification, and follow-up.
- Findings report both headline axes, existing diagnostic labels with recurrence and unevaluable repeats, human-input burden, calls, tokens, latency, and cost.
- `trajectory.jsonl` links each completed replay's prior state, decision, action, and outcome without invented substantive content.
- Displayed counts are generated from artifacts, blocking privacy verification passes, advisories receive owner review, and every public product claim points to evidence or is labeled as a hypothesis.
- Gabriel watches 90 seconds and understands the concrete work, the unique insight, and the exact result without being told that you are capable. All true = ship.
