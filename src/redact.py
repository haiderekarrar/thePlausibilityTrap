"""Redact mapped identity strings from Event JSONL before external use."""

import argparse
from pathlib import Path

import yaml

from ingest import Event, read_events, write_events


STRING_FIELDS = ("id", "actor", "counterparty", "text", "source_file")


def load_mapping(mapping_path: Path) -> dict[str, str]:
    """Load a non-empty real-string-to-pseudonym mapping without exposing it."""
    try:
        mapping = yaml.safe_load(mapping_path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        raise ValueError("Could not read the mapping file.") from None

    if not isinstance(mapping, dict) or not mapping:
        raise ValueError("The mapping file must contain at least one text replacement.")

    for original, pseudonym in mapping.items():
        if not isinstance(original, str) or not original or not isinstance(pseudonym, str):
            raise ValueError("Every mapping entry must be a non-empty text key and text value.")

    original_strings = set(mapping)
    if any(pseudonym in original_strings for pseudonym in mapping.values()):
        raise ValueError("Mapping pseudonyms must not also be source strings.")

    return mapping


def replace_text(value: str, replacements: list[tuple[str, str]]) -> str:
    """Apply prepared replacements to one text value."""
    for original, pseudonym in replacements:
        value = value.replace(original, pseudonym)
    return value


def redact_events(events: list[Event], mapping: dict[str, str]) -> list[Event]:
    """Replace mapped identity strings in every Event string field."""
    replacements = sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True)
    redacted_events: list[Event] = []

    for event in events:
        event_data = event.model_dump()
        for field_name in STRING_FIELDS:
            event_data[field_name] = replace_text(event_data[field_name], replacements)
        redacted_events.append(Event.model_validate(event_data))

    return redacted_events


def verify_no_leaks(events: list[Event], mapping: dict[str, str]) -> None:
    """Fail without revealing values if a mapped source string remains."""
    for event in events:
        for field_name in STRING_FIELDS:
            value = getattr(event, field_name)
            if any(original in value for original in mapping):
                raise ValueError("Redaction leak check failed.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Redact mapped identity strings from Event JSONL."
    )
    parser.add_argument("input_path", type=Path, help="Path to unredacted Event JSONL.")
    parser.add_argument(
        "--mapping",
        type=Path,
        required=True,
        help="Path to a YAML real-string-to-pseudonym mapping.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Path for redacted Event JSONL.",
    )
    args = parser.parse_args()

    events = read_events(args.input_path)
    mapping = load_mapping(args.mapping)
    redacted_events = redact_events(events, mapping)
    verify_no_leaks(redacted_events, mapping)
    write_events(redacted_events, args.out)

    print(f"Redacted {len(redacted_events)} events.")


if __name__ == "__main__":
    main()
