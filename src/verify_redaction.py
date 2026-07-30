"""Check publishable text files for mapped strings and PII shapes."""

import argparse
from pathlib import Path
import re

from redact import (
    load_mapping,
    prepare_verification_patterns,
)


PII_PATTERNS = {
    "email_address": re.compile(
        r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w-])"
    ),
    "phone_number": re.compile(
        r"(?<!\w)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}(?!\w)"
    ),
    "long_digit_sequence": re.compile(r"(?<!\d)\d{7,}(?!\d)"),
    "possible_street_address": re.compile(
        r"(?<![\d-])\b\d{1,6}[ \t]+(?:[A-Za-z0-9.'-]+[ \t]+){1,5}"
        r"(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd|"
        r"Court|Ct|Circle|Cir|Parkway|Pkwy)\b",
        re.IGNORECASE,
    ),
}
UUID_PATTERN = re.compile(
    r"(?<![0-9A-Fa-f])"
    r"[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-"
    r"[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}"
    r"(?![0-9A-Fa-f])"
)
BLOCKING_PII_CATEGORIES = frozenset(
    {"email_address", "phone_number", "possible_street_address"}
)
ADVISORY_PII_CATEGORIES = frozenset({"long_digit_sequence"})


def find_mapped_source_leaks(
    file_paths: list[Path], mapping: dict[str, str]
) -> list[tuple[Path, int, str]]:
    """Return safe line locations for mapped sources that remain."""
    source_patterns = prepare_verification_patterns(mapping)
    leaks: list[tuple[Path, int, str]] = []

    for file_path in file_paths:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            if any(pattern.search(line) for pattern in source_patterns):
                leaks.append((file_path, line_number, "mapped_source"))

    return leaks


def find_pii_pattern_warnings(
    file_paths: list[Path], mapping: dict[str, str]
) -> list[tuple[Path, int, str]]:
    """Return PII-shaped findings, excluding UUID-contained digit runs."""
    pseudonyms = tuple(mapping.values())
    warnings: list[tuple[Path, int, str]] = []

    for file_path in file_paths:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            uuid_spans = [
                uuid_match.span()
                for uuid_match in UUID_PATTERN.finditer(line)
            ]
            for category, pattern in PII_PATTERNS.items():
                has_unapproved_match = False
                for match in pattern.finditer(line):
                    if category == "long_digit_sequence" and any(
                        uuid_start <= match.start()
                        and match.end() <= uuid_end
                        for uuid_start, uuid_end in uuid_spans
                    ):
                        continue
                    if any(
                        match.group(0) in pseudonym
                        for pseudonym in pseudonyms
                    ):
                        continue
                    has_unapproved_match = True

                if has_unapproved_match:
                    warnings.append((file_path, line_number, category))

    return warnings


def split_pii_warnings(
    warnings: list[tuple[Path, int, str]],
) -> tuple[
    list[tuple[Path, int, str]],
    list[tuple[Path, int, str]],
]:
    """Separate blocking findings from advisory identifier review."""
    known_categories = (
        BLOCKING_PII_CATEGORIES | ADVISORY_PII_CATEGORIES
    )
    advisory_warnings = [
        warning
        for warning in warnings
        if warning[2] in ADVISORY_PII_CATEGORIES
    ]
    blocking_warnings = [
        warning
        for warning in warnings
        if warning[2] in BLOCKING_PII_CATEGORIES
        or warning[2] not in known_categories
    ]
    return blocking_warnings, advisory_warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check publishable files for mapped strings and PII."
    )
    parser.add_argument(
        "file_paths",
        nargs="+",
        type=Path,
        help="One or more redacted text files to check.",
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        required=True,
        help="Path to the private YAML real-string-to-pseudonym mapping.",
    )
    args = parser.parse_args()

    mapping = load_mapping(args.mapping)
    mapped_source_leaks = find_mapped_source_leaks(args.file_paths, mapping)
    pii_warnings = find_pii_pattern_warnings(args.file_paths, mapping)
    blocking_pii_warnings, advisory_pii_warnings = split_pii_warnings(
        pii_warnings
    )

    for file_path, line_number, category in mapped_source_leaks:
        print(
            f"Blocking verification failure: "
            f"{file_path}:{line_number} ({category})"
        )
    for file_path, line_number, category in blocking_pii_warnings:
        print(
            f"Blocking verification failure: "
            f"{file_path}:{line_number} ({category})"
        )
    for file_path, line_number, category in advisory_pii_warnings:
        print(
            f"Advisory identifier review: "
            f"{file_path}:{line_number} ({category})"
        )

    blocking_failure_count = (
        len(mapped_source_leaks) + len(blocking_pii_warnings)
    )
    if blocking_failure_count:
        print(
            f"Blocking verification failed with "
            f"{blocking_failure_count} finding(s)."
        )
    else:
        print(
            f"Blocking verification passed for "
            f"{len(args.file_paths)} file(s): no mapped sources, "
            "email addresses, telephone numbers, "
            "or possible street addresses remain."
        )

    if advisory_pii_warnings:
        print(
            f"Advisory review remains for "
            f"{len(advisory_pii_warnings)} long-digit line location(s) "
            "before public release."
        )
    else:
        print("No advisory long-digit findings remain.")

    if blocking_failure_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
