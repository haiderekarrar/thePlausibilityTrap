"""Synthetic tests for owner-authored document CSV ingestion."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ingest import write_events  # noqa: E402
from ingest_documents import parse_document_csv  # noqa: E402


class DocumentIngestionTests(unittest.TestCase):
    def test_fictional_sample_matches_expected_jsonl(self) -> None:
        events = parse_document_csv(
            PROJECT_ROOT / "sample" / "document_events_redacted.csv"
        )

        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "events.jsonl"
            write_events(events, output_path)

            self.assertEqual(
                output_path.read_bytes(),
                (
                    PROJECT_ROOT / "sample" / "document_events_expected.jsonl"
                ).read_bytes(),
            )

        self.assertEqual(
            [event.channel for event in events],
            ["document", "invoice", "bank", "payment_app"],
        )
        self.assertEqual(events[0].timestamp.utcoffset().total_seconds(), -21600)
        self.assertEqual(events[0].text, "Fictional repair estimate received.")
        self.assertEqual(events[0].amount, 1250.5)
        self.assertIsNone(events[3].amount)

    def test_timestamp_requires_utc_offset_without_echoing_row(self) -> None:
        private_marker = "PRIVATE_MARKER"
        csv_text = (
            "timestamp,channel,actor,counterparty,text,amount,source_file\n"
            f"2022-01-15T09:30:00,document,{private_marker},ME,"
            f"{private_marker},100.00,document_001.pdf\n"
        )

        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "documents.csv"
            input_path.write_text(csv_text, encoding="utf-8")

            with self.assertRaises(ValueError) as raised:
                parse_document_csv(input_path)

        self.assertIn("CSV row 2", str(raised.exception))
        self.assertNotIn(private_marker, str(raised.exception))

    def test_source_file_requires_neutral_id_without_echoing_value(self) -> None:
        private_marker = "PRIVATE_MARKER.pdf"
        csv_text = (
            "timestamp,channel,actor,counterparty,text,amount,source_file\n"
            "2022-01-15T09:30:00-06:00,document,VENDOR_A,ME,"
            f"Fictional estimate,100.00,{private_marker}\n"
        )

        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "documents.csv"
            input_path.write_text(csv_text, encoding="utf-8")

            with self.assertRaises(ValueError) as raised:
                parse_document_csv(input_path)

        self.assertIn("CSV row 2", str(raised.exception))
        self.assertNotIn(private_marker, str(raised.exception))

    def test_invalid_channel_does_not_echo_source_value(self) -> None:
        private_marker = "PRIVATE_CHANNEL"
        csv_text = (
            "timestamp,channel,actor,counterparty,text,amount,source_file\n"
            f"2022-01-15T09:30:00-06:00,{private_marker},VENDOR_A,ME,"
            "Fictional record,100.00,document_001.pdf\n"
        )

        with TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "documents.csv"
            input_path.write_text(csv_text, encoding="utf-8")

            with self.assertRaises(ValueError) as raised:
                parse_document_csv(input_path)

        self.assertIn("CSV row 2", str(raised.exception))
        self.assertNotIn(private_marker, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
