"""Redact mapped identity strings from Event JSONL before external use."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re

import yaml

from ingest import Event, read_events, write_events


STRING_FIELDS = ("id", "actor", "counterparty", "text", "source_file")
CASE_SENSITIVE_SOURCES = frozenset({"Me"})


def load_mapping(mapping_path: Path) -> dict[str, str]:
    """Load a non-empty real-string-to-pseudonym mapping without exposing it."""
    try:
        mapping = yaml.safe_load(mapping_path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        raise ValueError("Could not read the mapping file.") from None

    if not isinstance(mapping, dict) or not mapping:
        raise ValueError("The mapping file must contain at least one text replacement.")

    for original, pseudonym in mapping.items():
        if (
            not isinstance(original, str)
            or not original
            or not isinstance(pseudonym, str)
            or not pseudonym
        ):
            raise ValueError("Every mapping entry must be a non-empty text key and text value.")

    prepare_replacements(mapping)

    return mapping


def compile_source_pattern(source: str) -> re.Pattern[str]:
    """Compile one source using the shared case and boundary policy."""
    escaped_source = re.escape(source)
    if source[0].isalnum() and source[-1].isalnum():
        escaped_source = rf"(?<!\w){escaped_source}(?!\w)"

    flags = 0 if source in CASE_SENSITIVE_SOURCES else re.IGNORECASE
    return re.compile(escaped_source, flags)


def _entry_ids_text(entry_ids: tuple[int, ...]) -> str:
    """Format opaque mapping entry IDs without exposing source values."""
    return ", ".join(str(entry_id) for entry_id in entry_ids)


def _coalesce_mapping(
    mapping: dict[str, str],
) -> list[tuple[str, str, tuple[int, ...]]]:
    """Coalesce equivalent rules and reject unsafe mapping relationships."""
    grouped_entries: dict[
        tuple[str, str], list[tuple[int, str, str]]
    ] = {}
    protected_casefolds = {
        source.casefold() for source in CASE_SENSITIVE_SOURCES
    }

    for entry_id, (source, pseudonym) in enumerate(mapping.items(), start=1):
        is_case_sensitive = source in CASE_SENSITIVE_SOURCES

        if not is_case_sensitive and source.casefold() in protected_casefolds:
            raise ValueError(
                f"Mapping entry {_entry_ids_text((entry_id,))} overlaps "
                "a protected exact-case rule."
            )
        if not is_case_sensitive and source.casefold() == pseudonym.casefold():
            raise ValueError(
                f"Mapping entry {_entry_ids_text((entry_id,))} has a "
                "case-insensitive source/pseudonym identity."
            )

        policy = "exact" if is_case_sensitive else "ignore_case"
        source_key = source if is_case_sensitive else source.casefold()
        grouped_entries.setdefault((policy, source_key), []).append(
            (entry_id, source, pseudonym)
        )

    effective_rules: list[tuple[str, str, tuple[int, ...]]] = []
    for entries in grouped_entries.values():
        pseudonyms = {pseudonym for _, _, pseudonym in entries}
        entry_ids = tuple(sorted(entry_id for entry_id, _, _ in entries))
        if len(pseudonyms) != 1:
            raise ValueError(
                f"Mapping entries {_entry_ids_text(entry_ids)} use "
                "capitalization-equivalent sources with different pseudonyms."
            )

        source = min(source for _, source, _ in entries)
        pseudonym = entries[0][2]
        effective_rules.append((source, pseudonym, entry_ids))

    effective_rules.sort(
        key=lambda rule: (-len(rule[0]), rule[0].casefold(), rule[0])
    )

    compiled_rules = [
        (compile_source_pattern(source), pseudonym, entry_ids)
        for source, pseudonym, entry_ids in effective_rules
    ]
    for _, produced_pseudonym, producer_entry_ids in compiled_rules:
        for source_pattern, _, source_entry_ids in compiled_rules:
            if source_pattern.search(produced_pseudonym):
                involved_entry_ids = tuple(
                    sorted(set(producer_entry_ids + source_entry_ids))
                )
                raise ValueError(
                    f"Mapping entries {_entry_ids_text(involved_entry_ids)} "
                    "create a pseudonym/source collision."
                )

    return effective_rules


def prepare_replacements(
    mapping: dict[str, str],
) -> list[tuple[re.Pattern[str], str]]:
    """Compile one deterministic, longest-first set of effective rules."""
    return [
        (compile_source_pattern(source), pseudonym)
        for source, pseudonym, _ in _coalesce_mapping(mapping)
    ]


def prepare_verification_patterns(
    mapping: dict[str, str],
) -> list[re.Pattern[str]]:
    """Use the replacement rules themselves to prepare leak checks."""
    return [pattern for pattern, _ in prepare_replacements(mapping)]


def _redact_events_with_stats(
    events: list[Event], mapping: dict[str, str]
) -> tuple[list[Event], dict[str, int], int]:
    """Redact Events while collecting internal aggregate statistics."""
    replacements = prepare_replacements(mapping)
    redacted_events: list[Event] = []
    substitutions_by_pseudonym: Counter[str] = Counter()
    substitutions_by_rule = [0] * len(replacements)

    for event in events:
        event_data = event.model_dump()
        for field_name in STRING_FIELDS:
            value = event_data[field_name]
            for rule_index, (pattern, pseudonym) in enumerate(replacements):
                value, substitution_count = pattern.subn(
                    lambda _: pseudonym, value
                )
                substitutions_by_rule[rule_index] += substitution_count
                if substitution_count:
                    substitutions_by_pseudonym[pseudonym] += substitution_count
            event_data[field_name] = value
        redacted_events.append(Event.model_validate(event_data))

    zero_match_rule_count = sum(
        substitution_count == 0
        for substitution_count in substitutions_by_rule
    )
    return (
        redacted_events,
        dict(sorted(substitutions_by_pseudonym.items())),
        zero_match_rule_count,
    )


def redact_events(events: list[Event], mapping: dict[str, str]) -> list[Event]:
    """Replace mapped identity strings in every Event string field."""
    redacted_events, _, _ = _redact_events_with_stats(events, mapping)
    return redacted_events


def verify_no_leaks(events: list[Event], mapping: dict[str, str]) -> None:
    """Fail without revealing values if a mapped source string remains."""
    source_patterns = prepare_verification_patterns(mapping)

    for event in events:
        for field_name in STRING_FIELDS:
            value = getattr(event, field_name)
            if any(pattern.search(value) for pattern in source_patterns):
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
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show per-pseudonym and zero-match-rule diagnostics.",
    )
    args = parser.parse_args()

    events = read_events(args.input_path)
    mapping = load_mapping(args.mapping)
    (
        redacted_events,
        substitutions_by_pseudonym,
        zero_match_rule_count,
    ) = _redact_events_with_stats(events, mapping)
    verify_no_leaks(redacted_events, mapping)
    write_events(redacted_events, args.out)

    print(f"Redacted {len(redacted_events)} events.")
    print(f"Total substitutions: {sum(substitutions_by_pseudonym.values())}")
    if args.stats:
        if substitutions_by_pseudonym:
            print("Substitutions by pseudonym:")
            for pseudonym, substitution_count in (
                substitutions_by_pseudonym.items()
            ):
                print(
                    f"  {json.dumps(pseudonym, ensure_ascii=True)}: "
                    f"{substitution_count}"
                )
        else:
            print("Substitutions by pseudonym: none")
        print(f"Effective rules with zero matches: {zero_match_rule_count}")


if __name__ == "__main__":
    main()
