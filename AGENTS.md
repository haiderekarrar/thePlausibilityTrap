# Project Instructions

## Source of Truth

- `deal_autopsy_build_spec_v3.md` replaces the earlier build specifications and is the source of truth for Tier 1 architecture and Tier 1a execution.
- The `replay.py` implementation plan required by v3 is the remaining approval gate before any `replay.py` code is written.

## Tier 1a Execution Scope

- Execute Replay 04 only under Conditions A, B, and C across three model tiers and three repeats per cell: 27 scored attempts.
- Replay 01 is the first post-ship expansion.
- Keep document ingestion in the Tier 1a pre-run path. It may proceed in parallel with `replay.py` planning and development, synthetic tests, schemas, persistence, and the report skeleton.
- Complete document ingestion, merge, redaction, blocking/advisory verification, and owner review before generating or freezing the final Replay 04 context pack, running the real Replay 04 vertical slice, or beginning the 27 scored attempts.
- Use a strong-model pass to segment the full transaction timeline into coherent named episodes based on meaningful changes in goal, actors, situation, or outcome. Aim for roughly 8–12 episodes for report readability, but use fewer or more when the evidence supports it. Hand-correct the result.
- All other approved v3 requirements remain in force.

## Product Goal

- This is a hiring demo showing how an interface can help a person discover and communicate an underspecified intention, then turn messy context into an executable next action.
- When the spec does not choose between implementation paths, choose the one that gets a complete, user-visible workflow working sooner. Do not sacrifice correctness, privacy, or required verification.
- Prioritize the replay interface and a working end-to-end vertical slice over reusable infrastructure, broad analytics, or extra documentation.
- Every public claim must point to a transcript, test, measured result, or concrete artifact. Label unsupported conclusions as hypotheses.

## Privacy and Model Boundaries

- Never inspect, print, summarize, or send the contents of `raw/`. Scripts may process `raw/` locally when explicitly requested.
- `mapping.yaml` and private derived candidate files may be inspected only in a separately authorized mapping task. Treat that as a scoped exception, not standing access.
- Do not quote private source values in chat responses, logs, exceptions, commit messages, `NOTES.md`, or public artifacts.
- Replay and analysis model calls receive redacted artifacts only. `ingest.py` and `redact.py` remain offline by construction and must not import network clients.
- All committed fixtures and `sample/` data are invented. Never derive sample text from `raw/`, even in edited form.
- Before anything is committed, `.gitignore` must contain `raw/`, `mapping.yaml`, and `.env`.

## Constraints

- Do not introduce frameworks, agent libraries, databases, or web servers.
- Use plain Python, pydantic schemas, direct model API calls, and one static HTML report.
- Static hosting of the generated report is allowed; do not build or run an application server.
- The finished report must work without a network connection; inline or locally render every required asset.

## Identity Handling

- Parsers extract source text verbatim.
- All identity transformation happens only in `redact.py` via `mapping.yaml`.
- This includes mapping the user's own name and `Me` to `ME`; do not special-case this in parsers.
- Keep parser output literal so the later leak-check grep remains simple and reliable.

## Working Style

- Keep tasks small so diffs stay readable.
- Explain and obtain approval before substantive, irreversible, schema, scoring, or scope changes.
- Small reversible corrections within an approved task may be applied after they are explained; show the diff before committing.
- Briefly explain non-obvious choices while working.
- Do not produce code that could not be explained clearly in an interview.
- If a clever approach seems necessary, flag it and explain why before using it.
- Do not let beginner explanations stall delivery. Explain briefly, implement approved work, and revisit concepts when asked.

## Build Log Habit

- After a surprising failure, correction, implementation decision, or scope change, draft a concise `NOTES.md` entry for the user's review. Do not apply substantive wording without approval.

## Verification

- After code changes, run the checks relevant to the changed behavior and report exactly what passed or could not be run.
- Before any artifact reaches a replay model or becomes public, run `verify_redaction.py` over it. This includes hand-written `ground_truth.md` and `operator_state.md` files before freeze or commit.
- Save each Condition C answer as redacted local text and verify it before sending it to a model API.
- After report changes, open the report with networking disabled, exercise every control, check for console errors, and inspect desktop and mobile screenshots.
- Once `make demo` and `make report` exist, keep them working as new stages are added.

## Replay Integrity

- Every `ground_truth.md` file is written by the user by hand. Never generate, edit, rewrite, or improve its substantive content.
- Every `operator_state.md` file is also written by the user by hand. Agents may scaffold headers but must not supply its facts, preferences, reasoning, or answers.
- Both owner-authored files must use pseudonyms and pass redaction verification before they are frozen, committed, or used.
- Write out the `replay.py` implementation plan and obtain the user's approval before writing any `replay.py` code.
- Generation prompts must never contain ground truth, outcomes, scores, post-decision events, or replay filenames and slugs. Use outcome-neutral internal replay IDs.
- Conditions A and B never receive `operator_state.md`. Condition C receives only the verified, redacted answers to the questions it actually asked, never the complete file.
- Freeze each replay's rubric, prompts, ground truth, operator state, exact model identifiers, supported parameters, retry rules, and cost limits before its first scored run. Use dated model snapshots when the provider offers them. Record later changes in `NOTES.md` and create new run IDs.
- Decision-quality scoring must permit defensible alternatives supported by contemporaneous evidence. Report historical-action matching separately; never use it by itself as the quality score.
- Retry only attempts that fail before a model response because of a timeout, rate limit, transport error, or provider 5xx error. A completed refusal, malformed response, or poor answer remains the recorded result for that scheduled run and is never rerolled.
- Run replays honestly and publish the results whatever they show, including results that flatter the models or complicate the project's thesis.
- Publish all scheduled repeats rather than selecting the strongest transcript.

## Run Provenance

- Every model run records a stable run ID, UTC timestamp, replay, condition, repeat, model identifier, supported parameters, prompts, token usage, latency, cost, status, and verbatim model response.
- Retain failed and aborted scored runs with their status and a short non-private explanation.
- Once a run has been scored or included in the report, treat its record as immutable; corrections create a new run.
