"""Collect likely redaction mapping candidates from local Event JSONL."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re

from ingest import Event, read_events
from verify_redaction import PII_PATTERNS


CAPITALIZED_PHRASE_PATTERN = re.compile(
    r"\b[A-Z][A-Za-z0-9&'-]*(?:[ \t]+[A-Z][A-Za-z0-9&'-]*){1,5}\b"
)
CAPITALIZED_WORD_PATTERN = re.compile(r"\b[A-Z][A-Za-z0-9&'-]*\b")
COMMON_CAPITALIZED_WORDS = {
    "A",
    "An",
    "And",
    "Are",
    "As",
    "At",
    "Be",
    "But",
    "By",
    "Can",
    "Could",
    "Date",
    "Dear",
    "Do",
    "For",
    "Friday",
    "From",
    "Hello",
    "Hi",
    "I",
    "If",
    "In",
    "Is",
    "It",
    "Monday",
    "My",
    "No",
    "Not",
    "Of",
    "On",
    "Or",
    "Our",
    "Please",
    "Re",
    "Saturday",
    "Sent",
    "Subject",
    "Sunday",
    "Thank",
    "Thanks",
    "The",
    "This",
    "Thursday",
    "To",
    "Tuesday",
    "Wednesday",
    "We",
    "What",
    "When",
    "Where",
    "Will",
    "With",
    "Yes",
    "You",
    "Your",
}


def _add_matches(counter: Counter[str], pattern: re.Pattern, text: str) -> None:
    """Add every non-empty regex match to a frequency counter."""
    for match in pattern.finditer(text):
        candidate = match.group(0).strip()
        if candidate:
            counter[candidate] += 1


def collect_candidates(events: list[Event]) -> dict[str, Counter[str]]:
    """Collect exact participants and heuristic identity-shaped text."""
    candidates: dict[str, Counter[str]] = {
        "participants": Counter(),
        "source_files": Counter(),
        "email_addresses": Counter(),
        "email_domains": Counter(),
        "phone_numbers": Counter(),
        "long_digit_sequences": Counter(),
        "possible_street_addresses": Counter(),
        "capitalized_phrases": Counter(),
        "capitalized_words_review": Counter(),
    }

    for event in events:
        for participant in (event.actor, event.counterparty):
            participant = participant.strip()
            if participant:
                candidates["participants"][participant] += 1

        candidates["source_files"][event.source_file] += 1

        for text in (event.actor, event.counterparty, event.text, event.source_file):
            email_matches = list(PII_PATTERNS["email_address"].finditer(text))
            for match in email_matches:
                email = match.group(0)
                candidates["email_addresses"][email] += 1
                candidates["email_domains"][email.split("@", maxsplit=1)[1]] += 1

            _add_matches(candidates["phone_numbers"], PII_PATTERNS["phone_number"], text)
            _add_matches(
                candidates["long_digit_sequences"],
                PII_PATTERNS["long_digit_sequence"],
                text,
            )
            _add_matches(
                candidates["possible_street_addresses"],
                PII_PATTERNS["possible_street_address"],
                text,
            )
            _add_matches(candidates["capitalized_phrases"], CAPITALIZED_PHRASE_PATTERN, text)

            for match in CAPITALIZED_WORD_PATTERN.finditer(text):
                word = match.group(0)
                if word not in COMMON_CAPITALIZED_WORDS:
                    candidates["capitalized_words_review"][word] += 1

    return {category: values for category, values in candidates.items() if values}


def write_candidates(
    candidates: dict[str, Counter[str]], output_path: Path
) -> int:
    """Write candidates with counts without printing private values to Terminal."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# PRIVATE LOCAL FILE: do not commit or share.",
        "# Counts are followed by JSON-quoted exact candidate strings.",
        "# Review every section; capitalized_words_review is intentionally noisy.",
    ]

    candidate_count = 0
    for category, values in candidates.items():
        lines.extend(("", f"## {category}"))
        for candidate, count in sorted(
            values.items(), key=lambda item: (-item[1], item[0].casefold())
        ):
            lines.append(f"{count}\t{json.dumps(candidate, ensure_ascii=False)}")
            candidate_count += 1

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return candidate_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write likely redaction mapping candidates to a private local file."
    )
    parser.add_argument("input_path", type=Path, help="Path to unredacted Event JSONL.")
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Path for the private candidate list, normally under work/.",
    )
    args = parser.parse_args()

    events = read_events(args.input_path)
    candidates = collect_candidates(events)
    candidate_count = write_candidates(candidates, args.out)

    print(
        f"Wrote {candidate_count} unique candidates across "
        f"{len(candidates)} categories to: {args.out}"
    )


if __name__ == "__main__":
    main()
