# Project Instructions

## Source of Truth

- `deal_autopsy_build_spec_v3.md` remains the source of truth for the broader Tier 1 architecture and the historical Tier 1a design.
- `V1_STATUS.md` is the current additive execution addendum. Its later owner-approved V1 decision supersedes the unexecuted v3 run-count and build-order requirements without rewriting what v3 originally planned.
- No `replay.py` code is in V1 scope. Any future replay harness still requires the written implementation plan and owner approval required by v3.

## Current V1 Scope

- V1, publicly titled **The Plausibility Trap**, is an exploratory Replay 04 case study based on five Work runs: A1, B1, C1, A2, and B2. A separate Codex A1 remains a side observation.
- The manual pilot originally informed rather than replaced the larger v3 design. A3/B3/C2/C3 and the 27-attempt Tier 1a grid were not run and are deferred, not completed.
- Do not add model runs, conditions, repeats, a replay harness, or scoring changes to V1 without a new explicit owner approval.
- Preserve the completed-run materials, frozen manual-pilot rubric, and final V1 score lock. Do not rescore V1 without explicit owner approval.
- Treat all pilot findings as exploratory and obey the interpretation and publication boundaries in `V1_STATUS.md`.

## Product Goal

- This is a public technical case study of one historical decision replay and five runs, focused on inspectable evidence, inference, uncertainty, judgment, recommendations, and human authority.
- Treat historical decision replay as the method used in this exploratory case, not as a universally validated framework. **The Plausibility Trap** is V1's public title and framing, not a settled umbrella thesis; no public umbrella name has been chosen.
- Keep the core repository and artifact audience-neutral and evidence-led. Hiring- or employer-specific positioning belongs in outreach/application materials rather than the core research framing, and do not phrase an experimental hypothesis as though its result is already established.
- Lead with the strongest claim the evidence supports. State what happened and what it means clearly, place caveats where they become relevant, and do not confuse intellectual caution with timid or apologetic writing.
- Describe observable recorded artifacts and traces without presenting them as hidden model cognition. Preserve distinctions among evidence found in worker work, propagated to a parent, represented explicitly, integrated later, and exposed in a final answer when the record supports them.
- When the spec does not choose between implementation paths, choose the one that gets a complete, user-visible workflow working sooner. Do not sacrifice correctness, privacy, or required verification.
- Prioritize the replay interface and a working end-to-end vertical slice over reusable infrastructure, broad analytics, or extra documentation.
- Every public claim must point to a transcript, test, measured result, or concrete artifact. Label unsupported conclusions as hypotheses.

## Privacy and Model Boundaries

- Never inspect, print, summarize, or send the contents of `raw/`. Scripts may process `raw/` locally when explicitly requested.
- Reserve `raw/` and "raw" for private unredacted source material. Describe model-visible experimental context as "unstructured redacted context" or "redacted evidence" so future plans do not imply that replay models receive `raw/`.
- `mapping.yaml` and private derived candidate files may be inspected only in a separately authorized mapping task. Treat that as a scoped exception, not standing access.
- Do not quote private source values in chat responses, logs, exceptions, commit messages, `NOTES.md`, or public artifacts.
- Replay and analysis model calls receive redacted artifacts only. `ingest.py` and `redact.py` remain offline by construction and must not import network clients.
- All committed fixtures and `sample/` data are invented. Never derive sample text from `raw/`, even in edited form.
- Before configuring the first public remote or making the first public push, perform a bounded history-level privacy audit of every commit and file reachable from `master`; confirm that no non-public material entered that history. This release check is separate from redaction verification for model-visible artifacts.
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
- Document CSV rows use neutral owner-assigned source identifiers such as `document_001.pdf`, never original PDF filenames.

## Working Style

- Keep tasks small so diffs stay readable.
- Explain and obtain approval before substantive, irreversible, schema, scoring, or scope changes.
- Small reversible corrections within an approved task may be applied after they are explained; show the diff before committing.
- Briefly explain non-obvious choices while working.
- Surface an implementation tradeoff only when it materially affects current correctness, privacy, interpretability, or approved scope.
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
- Publish all five executed V1 Work runs rather than selecting the strongest transcript. A future approved experiment must publish every attempt scheduled by its own frozen plan.

## Run Provenance

- Every model run records a stable run ID, UTC timestamp, replay, condition, repeat, model identifier, supported parameters, prompts, token usage, latency, cost, status, and verbatim model response.
- Retain failed and aborted scored runs with their status and a short non-private explanation.
- Once a run has been scored or included in the report, treat its record as immutable; corrections create a new run.
