# Deal Autopsy — Build Specification v2

**One-line pitch:** Feed the complete digital exhaust of a real $226K distressed-property sale into a pipeline that reconstructs the deal, decomposes it into agent-executable primitives, and replays its hardest decisions against frontier models — measuring not "% correct" but whether models can operate inside a real, badly specified situation.

**What it proves:** You push agents to their limits (replay harness), you ship clean code (the repo), and you understand knowledge work outside SF (the corpus is your own life). One artifact, all three traits.

**Framing rule for the README and video:** This is explicitly NOT a % correct eval. The benchmark's premise is that real knowledge work arrives as messy context with an under-specified goal — the human in this deal did not fully know what he wanted either; "the most money, safely, fast" had to be discovered, and its parts conflicted. The replays test whether models can (a) find what matters in raw context, (b) discover the objective's actual structure including adversarial dynamics, and (c) decide well — which is the interface problem, not the one-shot problem.

---

## 1. What the finished thing looks like

A public GitHub repo plus one self-contained HTML report. The report has five sections:

1. **The Deal** — hero stats ($226,000 close vs. $150K ceiling, duration, event count, dollar volume) and a timeline of the real transaction segmented into episodes (agent search, tenant negotiation, heating crisis, meter crisis, closing sprint), with a message-frequency sparkline so the crisis weeks are visible as spikes.
2. **Primitive Decomposition** — every action classified into the taxonomy, with two bars per primitive: share of actions vs. share of dollar outcome. The mismatch between those bars is the product argument drawn as a picture.
3. **Capability Matrix** — per primitive: automatable today / automatable with human approval / fails today, each verdict backed by replay evidence.
4. **The Replays** — the core section. For each decision point: the context the human had → what each model did (verbatim), under two conditions and three model tiers → what actually happened → the delta.
5. **Findings** — the A/B condition chart, the tier-gap chart, and the elicitation-grade table. Three charts, three sentences each.

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
  01_the_150k_offer/        # each = ground_truth.md + context spec + transcripts/
  02_padded_quotes/
  03_silent_tenant/
  04_the_220k_counter/
  05_meter_payment/          # optional, build if ahead of schedule
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

**Stack:** Plain Python + pydantic, direct Anthropic/OpenAI SDK calls (no LangChain, no agent frameworks, no databases, no servers), Chart.js via CDN in one static HTML file. Builder: Codex, driven with small reviewed tasks. Architect/verifier: separate review outside the builder session for schema decisions, the replay plan, and pre-publication redaction checks.

---

## 3. Pipeline

**Step 1 — Ingest.** One parser per source (iMessage, Gmail, WhatsApp, payments) producing Event rows into `events.jsonl`. Parsers extract VERBATIM — no identity mapping in parsers, ever; identity appears inside message bodies, not just sender fields, so partial mapping anywhere creates unauditable leaks. Bank statements: hand-list the ~15 deal-relevant transactions in a CSV rather than parsing PDFs. Target: one clean chronological JSONL.

**Step 2 — Redact.** `mapping.yaml` holds every real string → pseudonym. The uniformity rule: ALL identity strings get mapped, including the owner's own name and aliases (full name, "Haider", "haider", "Me" → ME, "Gilani" as catch-all, the username inside attachment file paths). No exceptions — a rule with zero exceptions is machine-checkable; one exception forces human judgment on every hit. Redaction runs before ANY text reaches a model API. Finish with a verification grep over all outputs (events, transcripts, report) that fails loudly on any surviving mapped string. Counterparties get mapped even when weakly identifying (including first-name-only references): identification is combinatorial — name + city + role + date is findable — and mapping costs one YAML line.

**Step 3 — Episodes.** Strong-model pass to segment the timeline into 8–12 episodes (goal, actors, duration, outcome). Hand-correct.

**Step 4 — Classify.** Tag every outbound action with one primitive. Routing protocol (verify, then downgrade): hand-label 50 events, run the cheap model on the same 50, measure agreement. ≥95%: cheap model owns the task. Below: fix the prompt and retry. Optionally have the cheap model emit a confidence flag and escalate only uncertain rows to a stronger model. Record the measured agreement in NOTES.md.

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

## 4. Ground truths (written by hand, by the owner, before replay code exists)

Each `replays/NN_name/ground_truth.md` is written by the person who lived the deal. Template headers:

- **Situation** — what was happening at that moment
- **Context available** — what information existed then (and only then; no hindsight)
- **What I did**
- **Why** — the full reasoning, including counterparty dynamics and what a naive optimizer would have done wrong
- **Outcome** — with dollar figures where they exist

The Why section is the benchmark's real content. Example, replay 04: the seller maximally valued speed (tenant escalating threats and carrying them out), yet the speed-optimal move was still to counter $220K at $232K — because fast acceptance signals desperation, invites repair-demand renegotiation, and capitulation reads as fast but plays out slow. Strength was the fast path. That reasoning goes in the file nearly verbatim; it is what no dataset contains.

## 5. The replay harness (the intellectual center — plan reviewed before building)

For each replay: a context pack (redacted events up to that timestamp, nothing after) + a neutral system prompt ("You are handling this transaction on the owner's behalf. Decide the next action and justify it.").

**Two conditions per replay (the A/B experiment):**
- **Condition A — raw:** full context pack straight to the deciding call.
- **Condition B — triage first:** call 1 asks the model to identify which information is relevant and why; call 2 decides using only the model's own distillation.

Rationale: triage is not preprocessing — deciding what's relevant is most of the decision (it's where the $76K was made in real life). Splitting it makes failures diagnosable: "couldn't find what mattered" vs. "had it and chose badly." If B reliably beats A, the benchmark yields evidence that capability isn't the bottleneck — context structuring is, i.e., the interface layer. Report whichever way it comes out.

**Three model tiers per condition** (small / mid / frontier): the tier gap per primitive is itself a finding — where on the capability curve does each primitive become automatable, and at what cost per task.

**Scoring, two axes per transcript:**
1. **Decision quality** vs. ground truth (with the dollar delta where computable).
2. **Elicitation grade**, three levels: (i) one-shots without interrogating the goal; (ii) elicits surface preferences and optimizes them literally — e.g., hears "speed matters most" and recommends accepting $220K, the speed trap; (iii) reasons about how the counterparty responds to the move — recognizes strength as the fast path.

**Integrity rule, non-negotiable:** run everything honestly and publish whatever happens, including results that flatter the models or complicate the thesis. The insight is whatever the truth turns out to be.

**The five replays:**
1. **The $150K offer** — months of offers capping at $150K, trashed property, CMA range. Accept, or repair and relist? Ground truth: rejected, ~$3K targeted repairs, relisted. Tests: decide, verify.
2. **The padded quotes** — first debris quotes ($2,000+) and repair estimates. Accept or keep sourcing and cross-check prices? Ground truth: ~10x cheaper via exhaustive sourcing. Tests: gather, price skepticism.
3. **The silent tenant** — refused cash offers, then silence. Next move? Ground truth: structured, notarized written offer that ended the standoff. Tests: negotiate, draft.
4. **The $220K counter** — cash no-inspection bid in hand, tenant escalating, every incentive screaming "take it." Ground truth: countered $232K against agent advice, closed $226K. Tests: the elicitation axis at full depth (the speed trap).
5. **The meter payment** (optional) — invoice ready, work done. Does the model think to condition payment on the utility's inspection? Tests: verify.

---

## 6. Scope tiers

- **Tier 1, must ship:** ingest + redact + classify + episode timeline + static report.
- **Tier 2, the magic:** replays 1–4, both conditions, three tiers, both scoring axes. If time compresses: replays 1 and 4 only, both conditions — those two carry the story.
- **Tier 3, only if ahead:** replay 5, Dubai corpus as a second deal, interactivity.

Anything not listed is out of scope. No mid-build exceptions.

## 7. Day plan (from current position: ingestion/redaction in progress)

- **Now / Day 1–2:** finish parsers → verified `events.jsonl`; redaction + verification grep green; write all ground_truth.md files by hand (no code required — do these in parallel with waiting on builds).
- **Day 2:** episodes + classification with the routing protocol; rollup stats; learn what the punchline numbers actually are.
- **Day 3:** replay harness (plan reviewed first), run all conditions × tiers, collect transcripts. Start report.py.
- **Day 4:** finish report, README, NOTES.md; publish repo (synthetic sample committed, raw/ and mapping.yaml verified excluded); record the 90-second video.
- **Day 5 (buffer):** X post, DM with video, first three sends to the backup list.

## 8. Video shot list (90 seconds, Loom-raw)

1. 0:00–0:10 — the raw file pile. "In 2022, at 19, I sold this trashed house from 1,200 miles away. Every email, invoice, text, and bank statement from that deal is on my drive. I gave all of it to the models."
2. 0:10–0:25 — pipeline run in terminal; timeline with episode segments and the crisis-week spikes.
3. 0:25–0:55 — ONE replay done properly: context → model transcript → what actually happened → dollar delta. Use replay 1 or 4.
4. 0:55–1:20 — the findings charts: A/B conditions, tier gap, elicitation grades. One product claim, stated plainly, whatever the honest result was.
5. 1:20–1:30 — face on camera: "I've done hundreds of hours of this work across three countries and still know the people who do it. I'll map five more real workflows for you, free."

## 9. README = product memo

First section, "Why this exists": the knowledge-work-interface thesis in your own words; the eval critique (messy context and intent discovery, not % correct); what your data showed; the primitive you'd build first, ranked, with reasoning. Then architecture, then how to run the sample. One scroll = the product argument and the code-quality signal.

## 10. NOTES.md = the receipts

Ongoing log: agent failures and corrections, the measured classification agreement, the verify-then-downgrade decisions, tooling observations (Codex daily driver, escalation pattern for hard architecture), anything surprising. Three honest paragraphs of this outperform any claim about "pushing agents to their limits."

## 11. Privacy checklist (before every push and before recording)

- `raw/`, `mapping.yaml`, `.env` in .gitignore from commit zero; verify with `git log --stat`.
- Verification grep green over events.jsonl, all transcripts, report.html.
- No account numbers, no real names of family or counterparties, no street address, anywhere in repo, report, or video frame.
- Recording done with a clean desktop, raw/ closed.

## 12. Definition of done

A stranger clones the repo, runs `make demo` on the synthetic sample, gets a working report in under two minutes. Gabriel watches 90 seconds and understands what you're good at without being told. Both true = ship.
