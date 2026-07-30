"""Synthetic tests for redaction, mapping safety, and external verification."""

from contextlib import redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import verify_redaction as verify_redaction_module  # noqa: E402
from ingest import Event, read_events  # noqa: E402
from redact import (  # noqa: E402
    _redact_events_with_stats,
    load_mapping,
    prepare_replacements,
    redact_events,
    verify_no_leaks,
)
from verify_redaction import (  # noqa: E402
    find_mapped_source_leaks,
    find_pii_pattern_warnings,
    split_pii_warnings,
)


def make_event(
    *,
    actor: str = "PERSON_SENDER",
    counterparty: str = "PERSON_RECIPIENT",
    text: str = "",
    event_id: str = "fictional-event",
    source_file: str = "fictional.txt",
) -> Event:
    """Build one invented Event without repeating irrelevant test setup."""
    return Event(
        id=event_id,
        timestamp=datetime(2022, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
        channel="imessage",
        actor=actor,
        counterparty=counterparty,
        text=text,
        amount=None,
        source_file=source_file,
    )


def serialize_events(events: list[Event]) -> str:
    """Serialize Events exactly as write_events() would."""
    return "".join(event.model_dump_json() + "\n" for event in events)


class RedactionPolicyTests(unittest.TestCase):
    def test_mixed_case_names_are_replaced_and_counted(self) -> None:
        mapping = {
            "Avery Stone": "PERSON_A",
            "Unused Alias": "PERSON_UNUSED",
        }
        event = make_event(
            text="Avery Stone | AVERY STONE | avery stone | AvErY StOnE"
        )

        redacted, substitutions, zero_match_rules = (
            _redact_events_with_stats([event], mapping)
        )

        self.assertEqual(
            redacted[0].text,
            "PERSON_A | PERSON_A | PERSON_A | PERSON_A",
        )
        self.assertEqual(substitutions, {"PERSON_A": 4})
        self.assertEqual(zero_match_rules, 1)

    def test_me_is_exact_case_only(self) -> None:
        event = make_event(
            actor="Me",
            text="Me said call me tomorrow. Meter message ME mE.",
        )

        redacted = redact_events([event], {"Me": "ME"})

        self.assertEqual(redacted[0].actor, "ME")
        self.assertEqual(
            redacted[0].text,
            "ME said call me tomorrow. Meter message ME mE.",
        )

    def test_boundaries_paths_and_longest_source_first(self) -> None:
        mapping = {
            "Avery Stone": "PERSON_A",
            "Avery": "PERSON_FIRST",
            "Al": "PERSON_SHORT",
            "avery@example.test": "EMAIL_A",
        }
        event = make_event(
            text="Avery Stone, Avery, Al, Always.",
            source_file=(
                "/Users/Avery Stone/avery@example.test/Always-Avery.txt"
            ),
        )

        redacted = redact_events([event], mapping)

        self.assertEqual(
            redacted[0].text,
            "PERSON_A, PERSON_FIRST, PERSON_SHORT, Always.",
        )
        self.assertEqual(
            redacted[0].source_file,
            "/Users/PERSON_A/EMAIL_A/Always-PERSON_FIRST.txt",
        )

    def test_fictional_phone_formats_are_replaced(self) -> None:
        mapping = {
            "202-555-0147": "PHONE_A",
            "(415) 555-0136": "PHONE_B",
            "2125550198": "PHONE_C",
        }
        event = make_event(
            text="Call 202-555-0147, (415) 555-0136, or 2125550198."
        )

        redacted = redact_events([event], mapping)

        self.assertEqual(
            redacted[0].text,
            "Call PHONE_A, PHONE_B, or PHONE_C.",
        )

    def test_internal_and_external_verification_share_policy(self) -> None:
        mapping = {"Avery Stone": "PERSON_A"}
        event = make_event(
            actor="AVERY STONE",
            text="Ask aVeRy StOnE for the fictional checklist.",
        )
        redacted = redact_events([event], mapping)

        verify_no_leaks(redacted, mapping)
        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "redacted.jsonl"
            output_path.write_text(
                serialize_events(redacted), encoding="utf-8"
            )

            self.assertEqual(
                find_mapped_source_leaks([output_path], mapping), []
            )
            self.assertEqual(
                find_pii_pattern_warnings([output_path], mapping), []
            )

    def test_exact_and_case_variant_leaks_report_line_locations(self) -> None:
        mapping = {"Avery Stone": "PERSON_A"}

        with self.assertRaises(ValueError):
            verify_no_leaks(
                [make_event(text="Avery Stone remains.")], mapping
            )
        with self.assertRaises(ValueError):
            verify_no_leaks(
                [make_event(text="aVeRy StOnE remains.")], mapping
            )

        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "planted_leaks.txt"
            output_path.write_text(
                "Avery Stone remains.\naVeRy StOnE remains.\n",
                encoding="utf-8",
            )

            self.assertEqual(
                find_mapped_source_leaks([output_path], mapping),
                [
                    (output_path, 1, "mapped_source"),
                    (output_path, 2, "mapped_source"),
                ],
            )

    def test_all_structural_pii_categories_report_line_locations(self) -> None:
        mapping = {"Avery Stone": "PERSON_A"}

        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "planted_pii.txt"
            output_path.write_text(
                "Email user@example.test\n"
                "Call 202-555-0147\n"
                "Reference 7654321\n"
                "Visit 123 Fictional Avenue\n",
                encoding="utf-8",
            )

            warnings = find_pii_pattern_warnings([output_path], mapping)

        self.assertEqual(
            {(line_number, category) for _, line_number, category in warnings},
            {
                (1, "email_address"),
                (2, "phone_number"),
                (3, "long_digit_sequence"),
                (4, "possible_street_address"),
            },
        )
        blocking_warnings, advisory_warnings = split_pii_warnings(
            warnings
        )
        self.assertEqual(
            {category for _, _, category in blocking_warnings},
            {
                "email_address",
                "phone_number",
                "possible_street_address",
            },
        )
        self.assertEqual(
            {category for _, _, category in advisory_warnings},
            {"long_digit_sequence"},
        )

    def test_uuid_is_suppressed_and_numeric_url_is_advisory(self) -> None:
        mapping = {"Avery Stone": "PERSON_A"}

        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "structural_ids.txt"
            output_path.write_text(
                "/attachments/"
                "12345678-abcd-4abc-8def-123456789012/file.jpeg\n"
                "https://example.test/orders/123456789012\n",
                encoding="utf-8",
            )

            warnings = find_pii_pattern_warnings([output_path], mapping)
            blocking_warnings, advisory_warnings = split_pii_warnings(
                warnings
            )

            self.assertEqual(blocking_warnings, [])
            self.assertEqual(
                advisory_warnings,
                [(output_path, 2, "long_digit_sequence")],
            )

            standard_output = StringIO()
            with patch.object(
                sys,
                "argv",
                [
                    "verify_redaction.py",
                    str(output_path),
                    "--mapping",
                    str(PROJECT_ROOT / "sample" / "mapping_demo.yaml"),
                ],
            ), redirect_stdout(standard_output):
                verify_redaction_module.main()

        verifier_output = standard_output.getvalue()
        self.assertIn("Blocking verification passed", verifier_output)
        self.assertIn(
            "Advisory review remains for 1 long-digit line location",
            verifier_output,
        )
        self.assertIn(
            f"{output_path}:2 (long_digit_sequence)",
            verifier_output,
        )
        self.assertNotIn("UUID-contained", verifier_output)

    def test_clean_cli_result_succeeds(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "clean.txt"
            output_path.write_text(
                "Fictional clean content.\n",
                encoding="utf-8",
            )

            standard_output = StringIO()
            with patch.object(
                sys,
                "argv",
                [
                    "verify_redaction.py",
                    str(output_path),
                    "--mapping",
                    str(PROJECT_ROOT / "sample" / "mapping_demo.yaml"),
                ],
            ), redirect_stdout(standard_output):
                verify_redaction_module.main()

        verifier_output = standard_output.getvalue()
        self.assertIn("Blocking verification passed", verifier_output)
        self.assertIn(
            "No advisory long-digit findings remain.",
            verifier_output,
        )
        self.assertNotIn("UUID-contained", verifier_output)

    def test_blocking_cli_result_raises(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "blocking.txt"
            output_path.write_text(
                "https://example.test/call/202-555-0147\n",
                encoding="utf-8",
            )

            standard_output = StringIO()
            with patch.object(
                sys,
                "argv",
                [
                    "verify_redaction.py",
                    str(output_path),
                    "--mapping",
                    str(PROJECT_ROOT / "sample" / "mapping_demo.yaml"),
                ],
            ), redirect_stdout(standard_output):
                with self.assertRaises(SystemExit) as raised:
                    verify_redaction_module.main()

        self.assertEqual(raised.exception.code, 1)
        verifier_output = standard_output.getvalue()
        self.assertIn("Blocking verification failure", verifier_output)
        self.assertIn(
            "Blocking verification failed with 1 finding",
            verifier_output,
        )
        self.assertIn(
            "No advisory long-digit findings remain.",
            verifier_output,
        )
        self.assertIn(
            f"{output_path}:1 (phone_number)",
            verifier_output,
        )
        self.assertNotIn("Blocking verification passed", verifier_output)

    def test_phone_number_inside_url_remains_blocking(self) -> None:
        mapping = {"Avery Stone": "PERSON_A"}

        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "phone_in_url.txt"
            output_path.write_text(
                "https://example.test/call/202-555-0147\n",
                encoding="utf-8",
            )

            warnings = find_pii_pattern_warnings([output_path], mapping)
            blocking_warnings, advisory_warnings = split_pii_warnings(
                warnings
            )

        self.assertEqual(
            blocking_warnings,
            [(output_path, 1, "phone_number")],
        )
        self.assertEqual(advisory_warnings, [])

    def test_capitalization_duplicates_coalesce_deterministically(self) -> None:
        first_mapping = {
            "Avery Stone": "PERSON_A",
            "AVERY STONE": "PERSON_A",
        }
        second_mapping = {
            "AVERY STONE": "PERSON_A",
            "Avery Stone": "PERSON_A",
        }

        first_rules = [
            (pattern.pattern, pattern.flags, pseudonym)
            for pattern, pseudonym in prepare_replacements(first_mapping)
        ]
        second_rules = [
            (pattern.pattern, pattern.flags, pseudonym)
            for pattern, pseudonym in prepare_replacements(second_mapping)
        ]

        self.assertEqual(first_rules, second_rules)
        self.assertEqual(len(first_rules), 1)
        redacted = redact_events(
            [make_event(text="Avery Stone and AVERY STONE")],
            first_mapping,
        )
        self.assertEqual(redacted[0].text, "PERSON_A and PERSON_A")

    def test_conflicting_capitalization_duplicates_fail_safely(self) -> None:
        mapping = {
            "Avery Stone": "PERSON_A",
            "AVERY STONE": "PERSON_B",
        }

        with self.assertRaises(ValueError) as raised:
            prepare_replacements(mapping)

        message = str(raised.exception)
        self.assertNotIn("Avery Stone", message)
        self.assertNotIn("AVERY STONE", message)

    def test_casefold_identity_is_rejected_except_for_me(self) -> None:
        with self.assertRaises(ValueError) as raised:
            prepare_replacements({"Avery Stone": "AVERY STONE"})

        self.assertNotIn("Avery Stone", str(raised.exception))
        self.assertEqual(len(prepare_replacements({"Me": "ME"})), 1)

    def test_overlapping_exact_and_case_insensitive_sources_fail_safely(
        self,
    ) -> None:
        mapping = {"Me": "ME", "me": "PERSON_PRONOUN"}

        with self.assertRaises(ValueError) as raised:
            prepare_replacements(mapping)

        message = str(raised.exception)
        self.assertNotIn("Me", message)
        self.assertNotIn("me", message)

    def test_pseudonym_source_collision_fails_safely(self) -> None:
        mapping = {
            "Avery Stone": "PERSON_A",
            "person_a": "PERSON_B",
        }

        with self.assertRaises(ValueError) as raised:
            prepare_replacements(mapping)

        message = str(raised.exception)
        self.assertNotIn("Avery Stone", message)
        self.assertNotIn("person_a", message)

    def test_redaction_is_idempotent(self) -> None:
        mapping = {
            "Avery Stone": "PERSON_A",
            "Me": "ME",
        }
        event = make_event(
            actor="Me",
            text="Avery Stone and AVERY STONE",
        )

        first_pass = redact_events([event], mapping)
        second_pass = redact_events(first_pass, mapping)

        self.assertEqual(
            serialize_events(first_pass),
            serialize_events(second_pass),
        )

    def test_committed_golden_fixture(self) -> None:
        mapping_path = PROJECT_ROOT / "sample" / "mapping_demo.yaml"
        input_path = PROJECT_ROOT / "sample" / "redaction_input.jsonl"
        expected_path = (
            PROJECT_ROOT / "sample" / "redaction_expected.jsonl"
        )
        mapping = load_mapping(mapping_path)
        events = read_events(input_path)

        redacted = redact_events(events, mapping)

        self.assertEqual(
            serialize_events(redacted),
            expected_path.read_text(encoding="utf-8"),
        )
        verify_no_leaks(redacted, mapping)
        self.assertEqual(
            find_mapped_source_leaks([expected_path], mapping), []
        )
        self.assertEqual(
            find_pii_pattern_warnings([expected_path], mapping), []
        )


if __name__ == "__main__":
    unittest.main()
