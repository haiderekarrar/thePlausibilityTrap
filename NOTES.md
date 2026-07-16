# Build Notes

- Project setup: removed an accidental Git repository initialized at the home-directory level, then initialized Git inside this project.
- Scope change: began deterministic redaction after completing the ingestion checkpoint.
- Email export decision: the first Gmail export contained sent messages only. The replacement export includes every message in the manually curated Minnesota-deal label and records both From and To headers.
- Email parser correction: Gmail export separators are followed by blank lines, so the parser skips those export-only lines before reading each record's headers.
