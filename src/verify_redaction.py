"""Check publishable text files for mapped strings, case variants, and PII shapes."""

import argparse
from pathlib import Path
import re

from redact import (
    compile_source_pattern,
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


def find_leaking_files(file_paths: list[Path], mapping: dict[str, str]) -> list[Path]:
    """Return files that still contain a mapped source string."""
    source_patterns = prepare_verification_patterns(mapping)
    leaking_files: list[Path] = []

    for file_path in file_paths:
        contents = file_path.read_text(encoding="utf-8")
        if any(pattern.search(contents) for pattern in source_patterns):
            leaking_files.append(file_path)

    return leaking_files


def prepare_case_variant_patterns(
    mapping: dict[str, str],
) -> list[tuple[str, re.Pattern]]:
    """Compile case-insensitive checks when source and pseudonym remain distinct."""
    patterns: list[tuple[str, re.Pattern]] = []

    for source in sorted(mapping, key=len, reverse=True):
        if source.casefold() == mapping[source].casefold():
            continue
        exact_pattern = compile_source_pattern(source)
        patterns.append((source, re.compile(exact_pattern.pattern, re.IGNORECASE)))

    return patterns


def find_case_variant_warnings(
    file_paths: list[Path], mapping: dict[str, str]
) -> list[tuple[Path, int, str]]:
    """Return locations of mapped sources that survive with changed capitalization."""
    source_patterns = prepare_case_variant_patterns(mapping)
    pseudonyms = set(mapping.values())
    warnings: list[tuple[Path, int, str]] = []

    for file_path in file_paths:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            found_variant = False
            for source, pattern in source_patterns:
                for match in pattern.finditer(line):
                    matched_text = match.group(0)
                    if matched_text != source and matched_text not in pseudonyms:
                        warnings.append((file_path, line_number, "case_variant"))
                        found_variant = True
                        break
                if found_variant:
                    break

    return warnings


def find_pii_pattern_warnings(
    file_paths: list[Path], mapping: dict[str, str]
) -> list[tuple[Path, int, str]]:
    """Return locations and categories for PII-shaped text not known as a pseudonym."""
    pseudonyms = tuple(mapping.values())
    warnings: list[tuple[Path, int, str]] = []

    for file_path in file_paths:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            for category, pattern in PII_PATTERNS.items():
                matches = pattern.finditer(line)
                if any(
                    not any(match.group(0) in pseudonym for pseudonym in pseudonyms)
                    for match in matches
                ):
                    warnings.append((file_path, line_number, category))

    return warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check publishable files for mapped strings, case variants, and PII."
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
    leaking_files = find_leaking_files(args.file_paths, mapping)
    case_variant_warnings = find_case_variant_warnings(args.file_paths, mapping)
    pii_warnings = find_pii_pattern_warnings(args.file_paths, mapping)

    for file_path in leaking_files:
        print(f"Mapped-string leak: {file_path}")
    for file_path, line_number, category in case_variant_warnings:
        print(f"Mapped-string warning: {file_path}:{line_number} ({category})")
    for file_path, line_number, category in pii_warnings:
        print(f"PII-pattern warning: {file_path}:{line_number} ({category})")

    if leaking_files or case_variant_warnings or pii_warnings:
        raise ValueError(
            "Redaction verification failed; review the locations above locally."
        )

    print(
        f"Verified {len(args.file_paths)} file(s): "
        "no mapped source strings, unapproved case variants, "
        "or PII-pattern warnings remain."
    )


if __name__ == "__main__":
    main()
