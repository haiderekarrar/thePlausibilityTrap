# Project Instructions

## Source of Truth

- `deal_autopsy_build_spec_v2.md` replaces the original build specification and is the source of truth for this project.

## Privacy and Safety

- Never read, print, summarize, or send anywhere the contents of `raw/` or `mapping.yaml`. They contain unredacted personal data.
- Scripts may process `raw/` locally when explicitly requested, but agents must not inspect those files directly.
- Before anything is committed, `.gitignore` must contain `raw/`, `mapping.yaml`, and `.env`.
- Do not introduce frameworks, agent libraries, databases, or web servers. Use plain Python, pydantic schemas, direct API calls, and one static HTML report.

## Identity Handling

- Parsers extract source text verbatim.
- All identity transformation happens only in `redact.py` via `mapping.yaml`.
- This includes mapping the user's own name and `Me` to `ME`; do not special-case this in parsers.
- Keep parser output literal so the later leak-check grep remains simple and reliable.

## Working Style

- Keep tasks small so diffs stay readable.
- The user reviews every change before it is applied.
- Briefly explain non-obvious choices while working.
- Do not produce code that could not be explained clearly in an interview.
- If a clever approach seems necessary, flag it and explain why before using it.

## Build Log Habit

- Prompt the user to add a `NOTES.md` entry when something surprising happens, including failures, corrections, implementation decisions, or scope changes.

## Replay Integrity

- Every `ground_truth.md` file is written by the user by hand. Never generate, edit, rewrite, or improve its substantive content.
- Write out the replay harness plan and obtain the user's approval before writing any `replay.py` code.
- Run replays honestly and publish the results whatever they show, including results that flatter the models or complicate the project's thesis.
