# NOTES.md — agent-driving log

A running record of decisions, failures, corrections, and surprises while building Deal Autopsy. Newest entries at the bottom. Entries marked [FILL] need details from my own sessions — do not ship the file with [FILL] markers in it.

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

**[FILL] — Redaction verification results.** What the leak-check grep caught on its first run, if anything, and what was added to mapping.yaml as a result.

**[FILL] — Anything that surprised me.** Standing rule: one line, same day, every time an agent does something unexpectedly good or unexpectedly bad.
