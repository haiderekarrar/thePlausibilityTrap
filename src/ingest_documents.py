"""Parse owner-authored document rows into the project's shared Event schema."""

import argparse
import csv
from datetime import datetime
import math
from pathlib import Path
import re

from ingest import Event, write_events


CSV_FIELDS = (
    "timestamp",
    "channel",
    "actor",
    "counterparty",
    "text",
    "amount",
    "source_file",
)
DOCUMENT_CHANNELS = {"bank", "document", "invoice", "payment_app"}
NEUTRAL_SOURCE_PATTERN = re.compile(r"^document_\d{3,}(?:\.pdf)?$")


def _required_value(row: dict[str, str | None], field: str, row_number: int) -> str:
    """Return one required CSV value without changing its source text."""
    value = row.get(field)
    if value is None or not value.strip():
        raise ValueError(f"Missing {field} on CSV row {row_number}.")
    return value


def _parse_timestamp(value: str, row_number: int) -> datetime:
    """Parse an exact email-received timestamp that includes a UTC offset."""
    try:
        timestamp = datetime.fromisoformat(value)
    except ValueError:
        raise ValueError(
            f"Invalid timestamp on CSV row {row_number}; "
            "expected ISO 8601 with a UTC offset."
        ) from None

    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError(
            f"Timestamp on CSV row {row_number} must include a UTC offset."
        )
    return timestamp


def _parse_amount(value: str | None, row_number: int) -> float | None:
    """Parse an optional plain numeric amount."""
    if value is None or not value.strip():
        return None
    try:
        amount = float(value)
    except ValueError:
        raise ValueError(
            f"Invalid amount on CSV row {row_number}; omit currency symbols and commas."
        ) from None
    if not math.isfinite(amount):
        raise ValueError(f"Amount on CSV row {row_number} must be finite.")
    return amount


def parse_document_csv(input_path: Path) -> list[Event]:
    """Parse manually selected document facts without transforming identities."""
    events: list[Event] = []

    with input_path.open("r", encoding="utf-8", newline="") as input_file:
        reader = csv.DictReader(input_file)
        if tuple(reader.fieldnames or ()) != CSV_FIELDS:
            raise ValueError(
                "Document CSV must use exactly these columns in order: "
                + ", ".join(CSV_FIELDS)
                + "."
            )

        try:
            for event_number, row in enumerate(reader, start=1):
                row_number = reader.line_num
                if None in row:
                    raise ValueError(f"Unexpected extra column on CSV row {row_number}.")

                timestamp = _parse_timestamp(
                    _required_value(row, "timestamp", row_number), row_number
                )
                channel = _required_value(row, "channel", row_number)
                if channel not in DOCUMENT_CHANNELS:
                    raise ValueError(f"Invalid channel on CSV row {row_number}.")

                source_file = _required_value(row, "source_file", row_number)
                if NEUTRAL_SOURCE_PATTERN.fullmatch(source_file) is None:
                    raise ValueError(
                        f"source_file on CSV row {row_number} must use the neutral "
                        "format document_001 or document_001.pdf."
                    )

                events.append(
                    Event(
                        id=f"document_event:{event_number:06d}",
                        timestamp=timestamp,
                        channel=channel,
                        actor=_required_value(row, "actor", row_number),
                        counterparty=_required_value(row, "counterparty", row_number),
                        text=_required_value(row, "text", row_number),
                        amount=_parse_amount(row.get("amount"), row_number),
                        source_file=source_file,
                    )
                )
        except csv.Error:
            raise ValueError(
                f"Invalid CSV structure near line {reader.line_num}."
            ) from None

    return events


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse an owner-authored document CSV into Event JSONL."
    )
    parser.add_argument("input_path", type=Path, help="Path to the document CSV.")
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Path for the unredacted JSONL output file.",
    )
    parser.add_argument(
        "--preview",
        type=int,
        default=0,
        help="Number of events to print (default: 0; use only with safe input).",
    )
    args = parser.parse_args()

    if args.preview < 0:
        parser.error("--preview must be zero or greater.")

    events = parse_document_csv(args.input_path)
    write_events(events, args.out)

    for event in events[: args.preview]:
        print(event.model_dump_json(indent=2))
    print(f"Total events: {len(events)}")
    print(f"Wrote JSONL to: {args.out}")


if __name__ == "__main__":
    main()
