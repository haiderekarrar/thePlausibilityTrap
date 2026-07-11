# Deal Autopsy — Build Specification

**One-line pitch:** Feed the complete digital exhaust of a real $226K distressed-property sale into a pipeline that reconstructs the deal, decomposes it into agent-executable primitives, and replays its hardest decisions against frontier models to show exactly where today's AI succeeds and fails at real knowledge work.

**What it proves:** You push agents to their limits (replay harness), you ship clean code (the repo), and you understand knowledge work outside SF (the corpus is your own life). One artifact, all three traits.

---

## 1. What the finished thing looks like

A public GitHub repo plus one self-contained HTML report. The report has four sections:

1. **The Deal** — header stats (final price vs. investor ceiling, duration, message count, dollar volume) and a timeline of the real transaction segmented into episodes (agent search, tenant negotiation, heating crisis, meter crisis, closing sprint).
2. **Primitive Decomposition** — every action in the corpus classified into a small taxonomy, with two charts: share of *actions* per primitive and share of *dollar outcome* attributable to each primitive. The punchline stat lives here (e.g., "chase and draft were 80% of actions; verify and negotiate produced ~$76K of the upside").
3. **Capability Matrix** — for each primitive: automatable today / automatable with human approval / fails today, each verdict backed by evidence from section 4, not vibes.
4. **The Replays** — 4 decision points from the real deal, each shown as: the context the human had → what the models did (verbatim transcripts, 2–3 models) → what actually happened → the delta in dollars or outcome.

The video screen-records this report. The repo lets anyone run the pipeline on an included synthetic sample corpus.

---

## 2. Architecture

```
raw/                  # your real exports (NEVER committed)
  gmail_export.txt
  imessage_*.txt
  whatsapp_chat.txt
  statements/*.pdf
  invoices/*.pdf
sample/               # tiny synthetic corpus, committed, so others can run it
src/
  ingest.py           # every source -> events.jsonl (one schema)
  redact.py           # deterministic pseudonymization, runs BEFORE any API call
  episodes.py         # LLM pass: segment timeline into named episodes
  classify.py         # LLM pass: tag each action with a primitive (cheap model, batched)
  replay.py           # the harness: context pack -> model decision -> vs ground truth
  report.py           # renders everything into report.html (templated, no server)
replays/
  01_the_150k_offer/  # each replay = context.md + ground_truth.md + transcripts/
  ...
report.html           # the artifact
README.md             # doubles as your product memo (see §7)
NOTES.md              # log of how you drove the agents while building (see §8)
```

**Event schema** (keep it this boring):

```python
class Event(BaseModel):
    id: str
    timestamp: datetime
    channel: Literal["email", "imessage", "whatsapp", "bank", "invoice", "payment_app"]
    actor: str            # pseudonymized: "me", "agent_m", "tenant", "electrician_1"
    counterparty: str
    text: str
    amount: float | None  # for financial events
    source_file: str
```

**Stack:** Python + pydantic for the pipeline, Anthropic and OpenAI SDKs called directly (no LangChain, no agent framework — hand-rolled calls read as taste in Gabriel's world), Chart.js via CDN inside a single templated HTML file. No database, no deployment, no auth. If it needs a server, you over-scoped it.

---

## 3. The pipeline, step by step

**Step 1 — Ingest.** You already have most exports (Google Apps Script for Gmail, imessage-exporter output, the WhatsApp _chat.txt). Write one parser per source producing `Event` rows into `events.jsonl`. Bank PDFs: `pdftotext` then regex the transaction rows; you only need the ~15 deal-relevant transactions, so hand-listing them in a CSV is acceptable and faster. Do not perfect this step. Target: one clean chronological JSONL, roughly 300–1,500 events.

**Step 2 — Redact.** A YAML mapping file of real string → pseudonym (names, address, phone numbers, emails, account numbers), applied deterministically to every event before anything touches an API. Keep dollar amounts and dates — they are the substance. Finish with a verification grep that fails loudly if any mapped string survives. This step matters twice: it protects your family and the counterparties, and it shows professional judgment on screen in the video.

**Step 3 — Episodes.** One strong-model pass over the timeline: "segment into episodes, each with a goal, actors, duration, and outcome." Hand-correct the output. Expect 8–12 episodes. This gives the report its narrative spine.

**Step 4 — Classify.** Tag every outbound action with one primitive from the taxonomy below. Use the cheapest capable model, batched, with 5–10 few-shot examples you label by hand first. Spot-check ~50 rows; fix the prompt, not the outputs.

**The taxonomy** (this is a product artifact — Gabriel's company will build one of these, and yours comes from lived data):

| Primitive | Definition | Deal examples |
|---|---|---|
| draft | compose a document or message | offer emails, POA, notarized agreement |
| chase | follow up until response | tenant silence, agent check-ins, vendor callbacks |
| gather | source options and information | dozens of agent interviews, CMA collection, vendor quotes |
| verify | test a claim against ground truth | site visits, conditioning payment on Xcel inspection, cheque authentication |
| negotiate | adversarial exchange with stakes | tenant move-out, $220K→$226K counter, commission design |
| decide | commit under uncertainty | rejecting $150K, repair-vs-sell-as-is |
| coordinate | multi-party scheduling and logistics | closing sprint, key handoff, contractor sequencing |
| reconcile | match money to paper | payments vs. invoices vs. statements |

**Step 5 — Replay harness.** The core feature. For each of 4 chosen moments, build a context pack: the redacted events up to that timestamp plus a neutral system prompt ("You are handling this transaction on the owner's behalf. Decide the next action and justify it."). Run against 2–3 models. Save verbatim transcripts. Render side-by-side with ground truth (what you did, what it produced).

The four replays, chosen because each has a measurable delta:

1. **The $150K offer.** Context: trashed-property photos described, months of offers capping at $150K, the CMA range. Does the model accept? Ground truth: rejected, targeted repairs, closed $226K. Delta: $76K.
2. **The padded quotes.** Context: first debris-removal quotes ($2,000+) and repair estimates. Does the model accept the first quote, or keep sourcing and cross-checking prices? Ground truth: ~10x cheaper via exhaustive sourcing. Tests price memory and skepticism.
3. **The silent tenant.** Context: repeated refused cash offers, then silence. What does the model propose? Ground truth: the structured, notarized written offer that ended the standoff. Tests adversarial negotiation.
4. **The meter payment.** Context: electrician invoice ready, work done. Does the model think to condition final payment on the utility's inspection? Ground truth: you did. Tests verification instinct.

**Integrity rule, non-negotiable:** run the replays honestly and report whatever happens. If a model does reject the $150K offer, say so — then show where it actually breaks (persistence over weeks of chasing, cross-vendor price memory, initiative to verify). Gabriel has watched a thousand rigged demos; an honest "here's where they surprised me and here's where they collapsed" is what "rational product discussion" means. The insight is whatever the truth turns out to be.

**Step 6 — Report.** `report.py` templates everything into one `report.html`. Dark, clean, fast, zero dependencies beyond CDN Chart.js. Static file = nothing can break during the screen recording or when he opens it himself.

---

## 4. Scope tiers (protect the ship date)

- **Tier 1, must ship:** ingest + redact + classify + episode timeline + static report. This alone is DM-worthy.
- **Tier 2, the magic:** the 4 replays. Cut to 2 replays (the $150K offer and the padded quotes) if time compresses — those two carry the story.
- **Tier 3, only if ahead of schedule:** Dubai corpus as a second deal, interactivity, model-vs-model comparison charts.

Anything not listed above is out of scope. No exceptions mid-build.

---

## 5. Four-day plan

- **Day 1:** Assemble raw corpus, write ingest parsers, write and verify redaction. Hand-pick the 4 replay moments and write their ground_truth.md files (do this Day 1 — they anchor everything else). End state: clean `events.jsonl`.
- **Day 2:** Episode segmentation, primitive classification, rollup stats. End state: the numbers exist; you know what the punchline stat actually is.
- **Day 3:** Replay harness, run all models, collect transcripts. Start `report.py`. End state: all content final.
- **Day 4:** Finish report, write README and NOTES.md, publish repo (synthetic sample included, real corpus excluded via .gitignore, double-checked). Record the 90-second video against the finished report. Buffer for retakes.
- **Day 5 (buffer):** X post, DM send with video, first three cold sends to the backup list.

---

## 6. Video shot list (90 seconds, Loom-raw)

1. 0:00–0:10 — file manager showing the raw pile. "In 2022, at 19, I sold this trashed house from 1,200 miles away. Every email, invoice, text, and bank statement from that deal is on my drive. I gave all of it to an agent."
2. 0:10–0:25 — pipeline run + timeline renders. One sentence on episodes.
3. 0:25–0:55 — primitive chart, then ONE replay shown properly: context → model transcript → what actually happened → the dollar delta.
4. 0:55–1:20 — capability matrix. The single product claim, stated plainly, whatever the honest version turned out to be.
5. 1:20–1:30 — face on camera: "I've done hundreds of hours of this work across three countries and still know the people who do it. I'll map five more real workflows for you, free."

---

## 7. README = product memo

Don't write a separate memo. The README's first section is "Why this exists": your compressed take on the knowledge-work-interface thesis, where it holds, where the data from your own deal complicates it, and what primitive you'd build first. Then architecture, then how to run on the sample corpus. A reader should get the product argument and the code quality signal in one scroll.

## 8. NOTES.md = the agent-driving log

Keep a running log while you build: which model did what, where they failed, how you decomposed tasks for them, what you rewrote by hand. Three honest paragraphs of this outperform any claim that you "push agents to their limits," because it is the receipts.

---

## 9. Privacy checklist (run before every push and before recording)

- Mapping file and `raw/` in .gitignore from commit one; verify with `git log --stat`.
- Verification grep passes on `events.jsonl`, `report.html`, and all replay transcripts.
- No account numbers, no real names of family or counterparties, no exact street address anywhere in repo, report, or video frame.
- Screen recording done with a clean desktop and the real corpus folder closed.

## 10. Definition of done

Someone who has never met you clones the repo, runs `make demo`, and gets a working report on the synthetic sample in under two minutes. Gabriel watches 90 seconds and understands what you're good at without you telling him. Both true = ship.
