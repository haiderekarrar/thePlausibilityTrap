# Deal Autopsy — Build Specification v2

**One-line pitch:** Turn the redacted digital exhaust of a real $226K distressed-property sale into a reproducible test of the missing knowledge-work interface: can structured reasoning and targeted clarification help models discover what the operator actually wants and produce a better next action?

**What the finished artifact should demonstrate:** You can test agents against consequential real-world decisions, ship clean code and a tested interface, understand knowledge work outside SF because the corpus comes from your own life, and recognize a valuable data class before anyone asks: a long trajectory linking messy context to decisions and delayed outcomes.

**Framing rule for the README and video:** This is explicitly not a "% correct" benchmark or a general-purpose product. It is a real-trajectory evaluation case study. Real knowledge work arrives as messy context with an under-specified goal; the operator in this deal did not fully know how to express what he wanted either, and "the most money, safely, fast" contained conflicting parts. The experiment compares performance across model capability, a two-stage structured workflow, and clarification from the operator. Added calls and cost are measured tradeoffs, not independent sources of improvement.

---

## 1. What the finished thing looks like

A public GitHub repository, one hosted URL, and one self-contained HTML report that also works from `file://` with networking disabled. The first screen is the actual replay interface rather than a marketing page or analytics dashboard.

1. **Replay interface** — lead with the most surprising generated number, then let the viewer select a replay, model tier, and Condition A/B/C. Show only the historical context available at that decision, the model workflow, its options and executable action packet, the actual outcome, and the measured scores.
2. **The trajectory** — hero facts ($226,000 close vs. $150K prior ceiling, duration, generated event count, and dollar volume), a timeline segmented into episodes, and a public `trajectory.jsonl` connecting each replay's prior state, decision, action, and delayed outcome.
3. **Findings** — compare interface lift, model-tier lift, and cost. Show decision quality, intent discovery, option generation versus selection, calls, tokens, latency, and dollars. State the result that actually occurred.
4. **Primitive decomposition and capability routing** — include only if classification is complete. Compare action frequency with outcome leverage, then route each supported primitive to AI acts / AI prepares and a human approves / human-led with AI support. Label unsupported routing conclusions as product hypotheses.
5. **Methods and limitations** — prompts, frozen materials, all run records, privacy method, one-owner scoring, hindsight risk, unequal call counts, exploratory sample size, and other constraints needed to interpret the findings honestly.

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
  01_the_150k_offer/        # each = ground_truth.md + operator_state.md + context + transcripts/
  02_first_quotes/
  03_silent_tenant/
  04_cash_offer_decision/
  05_meter_payment/          # optional, build if ahead of schedule
trajectory.jsonl            # public redacted decision/outcome rows
report.html
README.md             # doubles as the product memo
NOTES.md              # agent-driving log: failures, corrections, decisions, surprises
AGENTS.md             # standing instructions for the coding agent
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

**Stack:** Plain Python + pydantic, direct model API calls (no LangChain, no agent frameworks, no databases, and no application server), and one static HTML file. Static hosting is allowed. Required report assets are rendered directly or embedded so the report works offline; do not depend on a CDN. The agent-building and verification process is recorded through concrete failures, corrections, tests, and commits in `NOTES.md`.

---

## 3. Pipeline

**Step 1 — Ingest.** One parser per source (iMessage, Gmail, WhatsApp, payments) producing Event rows into `events.jsonl`. Parsers extract VERBATIM — no identity mapping in parsers, ever; identity appears inside message bodies, not just sender fields, so partial mapping anywhere creates unauditable leaks. Bank statements: hand-list the ~15 deal-relevant transactions in a CSV rather than parsing PDFs. Target: one clean chronological JSONL.

**Step 2 — Redact.** `mapping.yaml` holds every real string → pseudonym. The uniformity rule: ALL identity strings get mapped, including the owner's own name and aliases (full name, first-name case variants, "Me" → ME, surname references, and usernames inside attachment paths). No exceptions inside the replay corpus: a uniform rule is machine-checkable, while exceptions force human judgment on every hit. Raw source files remain local and never enter agent or replay-model context. A separately authorized, isolated mapping task may inspect extracted identity candidates and `mapping.yaml`; record that exception honestly. No unredacted corpus reaches replay or analysis models. Finish with verification over every model-visible or publishable output, including owner-authored replay files and staged Condition C answers before API use. Verification fails loudly on any surviving mapped string, unapproved case variant, or structural PII warning.

**Step 3 — Episodes.** Strong-model pass to segment the timeline into 8–12 episodes (goal, actors, duration, outcome). Hand-correct. This remains early because it creates the visual timeline and helps define replay context windows.

**Step 4 — Replays and report vertical slice.** Before broad classification, complete one headline replay end to end: frozen owner-authored materials → redacted context pack → all three conditions for one model → recorded run metadata → scored transcript → visible report state. Start the report skeleton as soon as this vertical slice exists.

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

Each `replays/NN_name/ground_truth.md` is written by the person who lived the deal. Template headers:

- **Situation** — what was happening at that moment
- **Context available** — what information existed then (and only then; no hindsight)
- **What I did**
- **Why** — the full reasoning, including counterparty dynamics and what a naive optimizer would have done wrong
- **Outcome** — with dollar figures where they exist

The Why section is the evaluation's rarest content. Example, replay 04: the seller maximally valued speed (tenant escalating threats and carrying them out), yet the speed-optimal move was still to counter $220K at $232K — because fast acceptance signals desperation, invites repair-demand renegotiation, and capitulation reads as fast but plays out slow. Strength was the fast path. That reasoning belongs only in ground truth; it must never be supplied as an elicitation answer.

Each headline replay also has an `operator_state.md`, written by the owner before any scored runs. It freezes what the owner could truthfully answer at that historical moment:

- stable fact ID plus contemporaneous observation or event
- stated preferences, constraints, and tradeoffs
- beliefs and uncertainties held at the time
- facts that may not be explicit in the digital context

It must exclude the eventual outcome, hindsight, the ground-truth action, and strategic conclusions the model is supposed to discover. During Condition C, answer only what was asked, at the same level of specificity as the question, using this frozen state. Do not volunteer additional reasoning. If the answer is absent, respond: "That information was not available in this replay."

The owner writes every substantive sentence in `ground_truth.md` and `operator_state.md`. Agents may scaffold required headers and validate structure but never generate, edit, rewrite, or improve the contents.

Both files use pseudonyms and pass redaction verification before they are frozen, committed, or used.

### `trajectory.jsonl`

Publish a redacted trajectory row for each completed replay. It is a specimen of the long-trajectory data class missing from conventional evaluations: state before a decision → options → action → delayed outcome. At minimum:

```json
{
  "decision_id": "04_cash_offer_decision",
  "decision_timestamp": "ISO-8601 timestamp",
  "context_event_ids": ["event IDs available before the decision"],
  "state_summary": "owner-authored contemporaneous state",
  "objective_at_the_time": "owner-authored objective",
  "constraints": ["owner-authored constraints"],
  "options_considered": ["historical options, if known"],
  "action_taken": "historical action",
  "outcome": "observed outcome",
  "outcome_lag_days": 0,
  "dollar_delta": 6000
}
```

Generate and validate this public file from redacted events plus frozen owner-authored replay materials. The owner supplies every substantive trajectory field explicitly. Code may assemble identifiers and timestamps, copy owner-supplied fields, and validate the schema, but it must not infer or summarize state, objectives, options, actions, or outcomes. Counts displayed in the README and report come from generated artifacts rather than hardcoded copy.

## 5. The replay harness (the intellectual center — plan reviewed before building)

Before any `replay.py` code, write a concrete implementation plan covering prompts, answer handling, run IDs, persistence, retries, scoring inputs, API failures, and cost limits; obtain owner approval.

For each replay, create a context pack containing redacted events available up to the decision timestamp and nothing afterward. Every condition starts from the same context pack and must return the same output schema.

Generation prompts never contain ground truth, outcomes, scores, post-decision events, or replay filenames and slugs. Conditions A and B never receive `operator_state.md`. Condition C receives only the verified, redacted answers to the questions it actually asked, never the complete file.

The B/C scaffold operationalizes the owner's notebook method. If contemporaneous notebook pages exist, describe the method as contemporaneously documented and use only safely redacted images; otherwise describe it as retrospectively reconstructed. The runtime scaffold is a tested interface hypothesis, not a claim that this is the universally best way to organize decisions.

**Condition A — raw one-shot**

One deciding call receives the full context pack. It must infer the objective, generate options, choose, and produce an action packet without a separate reasoning scaffold or clarification.

**Condition B — structured reasoning**

Call 1 receives the same full context pack and produces a five-part evidence brief. It organizes the situation without recommending, drafting, or scheduling an action:

- **Decision frame** — the decision that must be made now; objectives, constraints, and material conflicts among them
- **Evidence ledger** — observations or documented facts, stakeholder claims, inferences, and assumptions kept separate, with source event IDs where available
- **Stakeholder map** — known incentives, leverage, and likely reactions, with inferred elements explicitly marked
- **Causal map** — how material evidence, stakeholder behavior, and potential consequences appear to connect, including gaps in the chain
- **Ranked unknowns** — missing information that could change the decision, each with a stable unknown ID and ranked by value of information: likely decision impact together with practical answerability; name the best source where one is apparent

Identifying who could resolve an unknown is part of organizing the situation; choosing, drafting, or scheduling outreach belongs in Call 2. Call 2 sees only the evidence brief and produces the common options and action packet. No new human information enters this condition. A → B estimates the bundled effect of a two-stage structured workflow, including an extra model call and a compressed representation, while holding the initial context pack and model tier constant.

**Condition C — structured reasoning plus clarification**

Call 1 first produces the same five-part evidence brief as B. It then selects no more than three high-value unknowns that the owner could realistically answer and asks one question for each. Every question references the unknown ID from the completed brief and states why the answer could materially change the action. The owner answers under the frozen `operator_state.md` policy, and each answer is redacted and verified before API use. Call 2 receives Call 1's evidence brief verbatim plus the verified, verbatim question-and-answer transcript, integrates the answers, and produces the common options and action packet. There is no intermediate model invocation. B → C estimates the incremental effect of the interactive clarification workflow while holding the number of model calls and the reasoning scaffold constant. A → C estimates total guided-interface lift.

Condition C tests whether dialogue helps; it does not by itself prove whether the owner already knew but failed to express something, held conflicting preferences, or discovered a new implication through the question.

Condition C tests one batched clarification round. Adaptive multi-turn questioning may behave differently; it remains untested and is a named future experiment.

The scaffold comes from the operator's own decision method, and the headline replays come from the same deal in which that method was used. Any lift establishes usefulness on this operator and corpus; it does not by itself establish cross-operator or cross-domain generality.

**Common output: options and action packet**

Every condition returns:

- two to four viable options with one-line tradeoffs
- chosen action
- exact message, document, or instruction to execute, when applicable
- immediate computer or operational actions
- verification condition
- follow-up trigger
- strongest case against the chosen action, including its major downside
- new evidence that would change the recommendation
- likely counterparty response

This makes advice inspectable and executable and enables a direct brainstorm-versus-decide comparison: did the model generate the ground-truth move, and did it select it?

**Three model tiers per condition** (small / mid / frontier): use three tiers from one provider family for the headline grid so provider differences do not contaminate the tier curve. Use explicit tier IDs and the same maximum reasoning effort supported by all three anchor tiers. For a GPT-5.6 anchor grid, set `reasoning.effort` to `max`, omit temperature and seed, and do not enable pro mode. This is a quality-first comparison; actual reasoning tokens, latency, and cost remain measured outcomes. The tier gap per replay or decision type is itself a finding — where on the capability curve does this work become reliable enough to delegate, and at what cost per task. Do not generalize this to primitive-level automation without broader classification evidence.

For headline replays 1 and 4, run every condition × tier cell three times. First complete one unscored vertical-slice run to debug the harness; then freeze scored-run materials and execute all scheduled repeats. Publish every scheduled transcript rather than selecting the strongest one. Three repeats remain exploratory evidence, not a statistically generalizable benchmark.

**Scoring, two headline axes per transcript:**

1. **Decision quality** against a frozen replay-specific rubric that permits defensible alternatives rather than requiring imitation of the historical action.
2. **Intent discovery**, three levels:
   - `0` — assumes the objective without surfacing its important structure
   - `1` — identifies or elicits a stated surface preference
   - `2` — identifies the conflict beneath that preference and its material consequences

A model that asks whether speed or price matters, hears "speed," and accepts $220K receives intent grade 1; its poor strategic choice is reflected in decision quality and the diagnostic labels rather than being smuggled into the intent score.

Define and approve the exact decision-quality scale and replay-specific criteria in the replay implementation plan before scored runs. A response may receive full decision-quality credit without matching the historical action if it satisfies the frozen criteria using only contemporaneously available evidence. Historical-action matching is reported separately and never determines the quality score by itself. Observed dollar outcomes may be shown as historical context, but they must never be attributed to a model as counterfactual value created or saved.

**Additional measured fields, not headline scoring axes:**

- whether the ground-truth move appeared in the option set
- whether the model selected it
- Condition C fact IDs recovered through questions
- number of questions asked
- targeted versus generic questions, using a frozen rubric
- call count, input/output tokens, latency, and dollar cost

**Diagnostic labels, not a third scoring axis:** when a response is weak, the human scorer may attach any of four fixed labels: `missed_relevant_evidence`, `treated_claim_as_fact`, `misunderstood_objective`, or `ignored_counterparty_response`. These labels explain failures in the replay detail; they do not create another headline score or chart. Record the exact model identifier, prompts, token usage, latency, and cost for each run so the extra calls in Conditions B and C remain visible.

**Run provenance:** every attempt records a stable run ID, UTC timestamp, replay, condition, model tier and exact identifier, repeat number, supported parameters, prompts, token usage, latency, cost, status, and verbatim response. Use dated model snapshots where the provider offers them. Failed and aborted scored runs remain recorded with a non-private explanation. Retry only attempts that fail before a model response because of a timeout, rate limit, transport error, or provider 5xx error. A completed refusal, malformed response, or poor answer remains the recorded result for that scheduled run and is never rerolled. Once scored or included in the report, a run is immutable; corrections receive new IDs.

**Integrity rule, non-negotiable:** freeze prompts, rubrics, ground truths, operator states, exact model identifiers, supported parameters, retry rules, and cost limits before the first scored run. Run everything honestly and publish whatever happens, including results that flatter the models or complicate the thesis. The insight is whatever the truth turns out to be.

**The five replays:**
1. **The $150K offer** — months of offers capping at $150K, trashed property, CMA range. Accept, or repair and relist? Ground truth: rejected, ~$3K targeted repairs, relisted. Tests: decide, verify.
2. **The padded quotes** — first debris quotes ($2,000+) and repair estimates. Accept or keep sourcing and cross-check prices? Ground truth: ~10x cheaper via exhaustive sourcing. Tests: gather, price skepticism.
3. **The silent tenant** — refused cash offers, then silence. Next move? Ground truth: structured, notarized written offer that ended the standoff. Tests: negotiate, draft.
4. **The $220K counter** — cash no-inspection bid in hand, tenant escalating, every incentive screaming "take it." Ground truth: countered $232K against agent advice, closed $226K. Tests: intent discovery and second-order counterparty reasoning (the speed trap).
5. **The meter payment** (optional) — invoice ready, work done. Does the model think to condition payment on the utility's inspection? Tests: verify.

---

## 6. Scope tiers

- **Tier 1, must ship:** verified ingest and redaction; owner-authored ground truth and operator state for replays 1 and 4; episode timeline; public `trajectory.jsonl`; replays 1 and 4 under Conditions A/B/C × three model tiers × three repeats; complete run provenance and cost; hosted self-contained replay interface; README; limitations; 90-second video.
- **Tier 2, should ship after the central experiment works:** first run a cross-provider robustness check on replay 4 under Conditions A/B/C × three repeats using the other provider's frontier model (nine transcripts and fifteen model calls), reported separately from the within-family tier curve. Then add replays 2 and 3, full classification, primitive-frequency and outcome-leverage charts, and an evidence-backed capability matrix. A slim replay-scoped matrix may ship earlier, but must not imply full-corpus evidence.
- **Tier 3, only if ahead:** replay 5, Dubai corpus as a second trajectory, or additional interface features.

Anything not listed is out of scope. No mid-build exceptions.

## 7. Build order from the current position

1. Finish mapping, produce redacted events, and make verification green. Commit the privacy tooling checkpoint.
2. The owner writes and freezes `ground_truth.md` and `operator_state.md` for replays 1 and 4. Create and validate their first public trajectory rows.
3. Segment the episode timeline and begin the report skeleton immediately, using generated fixture data until scored runs exist.
4. Write the replay implementation plan and obtain approval before writing `replay.py`.
5. Complete one unscored replay vertical slice through persistence, scoring input, and the visible report. Fix the harness before spending on the experiment.
6. Freeze prompts and rubrics; run and publish all 54 scheduled headline transcripts, including failures. Populate interface/model/cost findings.
7. Finish the hosted report, README, limitations, offline/mobile release checks, and 90-second video. Prepare the exact DM before optional breadth.
8. Only then run the defined cross-provider replay-4 robustness check; after that, add replays 2 and 3, classification, and the full capability matrix.

## 8. Video shot list (90 seconds, Loom-raw)

1. **0:00–0:10 — concrete hook.** "At 19, I rejected a $150K ceiling on this distressed sale and closed at $226K. I later realized I had something models rarely see: the context before each decision and the outcome afterward."
2. **0:10–0:25 — provenance.** Show the local pipeline and generated count without exposing private values. "I reconstructed [generated event count] messages and emails, redacted the corpus, and linked its hardest decisions to their delayed outcomes."
3. **0:25–0:55 — replay interface.** Use replay 04. Switch A → B → C for one model so the viewer sees raw reasoning, structured reasoning, clarification, the options, and the executable action packet.
4. **0:55–1:20 — findings.** Show interface lift versus model-tier lift, brainstorm versus selection, and quality versus cost. State one exact result, whichever way it came out.
5. **1:20–1:30 — direct offer.** "I've operated hundreds of hours of messy work across three countries. Give me one user workflow and a weekend; I'll return a concrete instrumented prototype, not a plan."

## 9. README = product memo

Lead with the most surprising generated number, then the thesis:

> Most evaluations contain isolated questions with immediate answers. This repository contains a redacted real-world trajectory: timestamped interactions linked to what was known at each decision, what action was taken, and what happened afterward. The operator who made the decisions wrote the ground truth before any model runs.

Within one scroll: hosted replay link; concrete deal facts; why long-trajectory decision/outcome data matters; A/B/C experimental question; exact findings; quality-versus-cost result; and three product implications, each tied to a numbered transcript, chart, or measured result. Then methods, limitations, architecture, and how to run the synthetic sample. Do not publish unsupported automation claims or generic ideas without evidence.

Prepare the delivery message as part of the artifact:

> You wrote that models lack long-trajectory data connecting business decisions to outcomes. I realized I had one on my laptop: hundreds of messages and emails from a distressed sale I operated at 19, linked to the decisions and outcomes. I turned it into a reproducible interface experiment.

## 10. NOTES.md = the receipts

Ongoing log: agent failures and corrections, measured classification agreement, verify-then-downgrade decisions, the isolated mapping exception, replay preregistration changes, report test failures, and anything surprising. Draft concise entries for owner review rather than relying on reminders. Concrete failures, fixes, and verification results outperform claims about "pushing agents to their limits."

## 11. Privacy checklist (before every push and before recording)

- `raw/`, `mapping.yaml`, `.env` in .gitignore from commit zero; verify with `git log --stat`.
- Raw source files remain local and are never inspected by coding agents or sent to replay models.
- Record the separately authorized mapping-task exception; do not describe the whole workflow as "no unredacted text ever reached a model."
- Verification green over redacted events, owner-authored replay files, staged Condition C answers before API use, `trajectory.jsonl`, all transcripts, and `report.html`.
- No account numbers, no real names of family or counterparties, no street address, anywhere in repo, report, or video frame.
- Recording done with a clean desktop, raw/ closed.

## 12. Definition of done

- A stranger opens one hosted URL and lands directly in a working replay interface.
- The report works from `file://` with networking disabled. Every condition, tier, and replay control works with zero console errors on desktop and mobile.
- A stranger clones the repository, runs `make demo` on the synthetic sample, and gets a working report in under two minutes.
- Replays 1 and 4 include A/B/C × three tiers × three published repeats with complete provenance, costs, scores, and no selected-away failures.
- `trajectory.jsonl` links each completed replay's prior state, decision, action, and outcome without invented substantive content.
- Displayed counts are generated from artifacts, privacy verification is green, and every public product claim points to evidence or is labeled as a hypothesis.
- Gabriel watches 90 seconds and understands the concrete work, the unique insight, and the exact result without being told that you are capable. All true = ship.
