"""Parse supported communication exports into the project's shared Event schema."""

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ValidationError


TIMESTAMP_PATTERN = re.compile(
    r"^(?P<timestamp>[A-Z][a-z]{2} \d{1,2}, \d{4}\s+\d{1,2}:\d{2}:\d{2} [AP]M)"
    r"(?: \([^)]*\))?$"
)
EMAIL_SEPARATOR_PATTERN = re.compile(r"^={60}$")
GMAIL_QUOTE_PATTERN = re.compile(r"^On .+ wrote:\s*$")
IMESSAGE_TIMEZONE = ZoneInfo("America/Los_Angeles")


class Event(BaseModel):
    id: str
    timestamp: datetime
    channel: Literal["email", "imessage", "whatsapp", "bank", "invoice", "payment_app"]
    actor: str
    counterparty: str
    text: str
    amount: float | None
    source_file: str


def read_events(input_path: Path) -> list[Event]:
    """Read and validate Event objects from a JSONL file."""
    events: list[Event] = []

    for line_number, line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event_data = json.loads(line)
            events.append(Event.model_validate(event_data))
        except (json.JSONDecodeError, ValidationError):
            # Validation details can contain source text, so suppress the original error.
            raise ValueError(f"Invalid Event JSONL on line {line_number}.") from None

    return events


def parse_imessage_export(input_path: Path) -> list[Event]:
    """Parse a two-person iMessage export without transforming identities."""
    lines = input_path.read_text(encoding="utf-8").splitlines()
    messages: list[tuple[datetime, str, str]] = []
    line_index = 0

    while line_index < len(lines):
        if not lines[line_index].strip():
            line_index += 1
            continue

        timestamp_match = TIMESTAMP_PATTERN.match(lines[line_index])
        if timestamp_match is None:
            raise ValueError(f"Expected a timestamp on line {line_index + 1}.")

        timestamp = datetime.strptime(
            timestamp_match.group("timestamp"), "%b %d, %Y %I:%M:%S %p"
        ).replace(tzinfo=IMESSAGE_TIMEZONE)
        line_index += 1

        if line_index >= len(lines) or not lines[line_index].strip():
            raise ValueError(f"Expected an actor after timestamp on line {line_index + 1}.")
        actor = lines[line_index]
        line_index += 1

        message_lines: list[str] = []
        while line_index < len(lines) and not TIMESTAMP_PATTERN.match(lines[line_index]):
            message_lines.append(lines[line_index])
            line_index += 1

        # The export uses blank separator lines between messages, not in message text.
        while message_lines and not message_lines[-1].strip():
            message_lines.pop()

        messages.append((timestamp, actor, "\n".join(message_lines)))

    actors: list[str] = []
    for _, actor, _ in messages:
        if actor not in actors:
            actors.append(actor)
    if len(actors) != 2:
        raise ValueError(
            "This parser currently supports exactly two distinct actors; "
            f"found {len(actors)}."
        )

    source_file = input_path.name
    events: list[Event] = []
    for event_number, (timestamp, actor, text) in enumerate(messages, start=1):
        counterparty = actors[1] if actor == actors[0] else actors[0]
        events.append(
            Event(
                id=f"{source_file}:{event_number:06d}",
                timestamp=timestamp,
                channel="imessage",
                actor=actor,
                counterparty=counterparty,
                text=text,
                amount=None,
                source_file=source_file,
            )
        )

    return events


def _trim_trailing_blank_lines(lines: list[str]) -> list[str]:
    """Remove export-only blank lines from the end of a text section."""
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def _find_email_reply_boundary(lines: list[str]) -> int:
    """Find where Gmail or Outlook quoted reply history begins."""
    for line_index, line in enumerate(lines):
        if GMAIL_QUOTE_PATTERN.match(line):
            return line_index
        if (
            line.startswith("From: ")
            and line_index + 1 < len(lines)
            and lines[line_index + 1].startswith("Sent: ")
        ):
            return line_index
    return len(lines)


def parse_gmail_export(input_path: Path) -> list[Event]:
    """Parse a Gmail Apps Script export without transforming identities."""
    records = input_path.read_text(encoding="utf-8").splitlines()
    email_sections: list[list[str]] = [[]]

    for line in records:
        if EMAIL_SEPARATOR_PATTERN.match(line):
            email_sections.append([])
        else:
            email_sections[-1].append(line)

    source_file = input_path.name
    events: list[Event] = []
    for section_number, section in enumerate(email_sections, start=1):
        while section and not section[0].strip():
            section.pop(0)
        if not any(line.strip() for line in section):
            continue

        expected_headers = ("Subject", "Date", "From", "To")
        if len(section) < 5:
            raise ValueError(f"Email section {section_number} is missing required headers.")

        header_values: dict[str, str] = {}
        for line_index, header_name in enumerate(expected_headers):
            prefix = f"{header_name}: "
            if not section[line_index].startswith(prefix):
                raise ValueError(
                    f"Expected '{header_name}:' at the start of email section {section_number}."
                )
            header_values[header_name] = section[line_index][len(prefix) :]

        if section[4].strip():
            raise ValueError(f"Expected a blank line after headers in email section {section_number}.")

        date_without_timezone_name = header_values["Date"].split(" (", maxsplit=1)[0]
        try:
            timestamp = datetime.strptime(
                date_without_timezone_name, "%a %b %d %Y %H:%M:%S GMT%z"
            )
        except ValueError:
            raise ValueError(f"Invalid date in email section {section_number}.") from None

        body_lines = section[5 : _find_email_reply_boundary(section[5:]) + 5]
        text = "\n".join(_trim_trailing_blank_lines(body_lines))
        events.append(
            Event(
                id=f"{source_file}:{len(events) + 1:06d}",
                timestamp=timestamp,
                channel="email",
                actor=header_values["From"],
                counterparty=header_values["To"],
                text=text,
                amount=None,
                source_file=source_file,
            )
        )

    return events


def write_events(events: list[Event], output_path: Path) -> None:
    """Write one JSON Event per line for the next pipeline stage."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        for event in events:
            output_file.write(event.model_dump_json() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse an iMessage or Gmail export into Event JSONL."
    )
    parser.add_argument("input_path", type=Path, help="Path to an export text file.")
    parser.add_argument(
        "--channel",
        choices=("imessage", "email"),
        default="imessage",
        help="Export format to parse (default: imessage).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Path for the JSONL output file.",
    )
    parser.add_argument(
        "--preview",
        type=int,
        default=5,
        help="Number of events to print before the total count (default: 5).",
    )
    args = parser.parse_args()

    if args.preview < 0:
        parser.error("--preview must be zero or greater.")

    if args.channel == "imessage":
        events = parse_imessage_export(args.input_path)
    else:
        events = parse_gmail_export(args.input_path)
    write_events(events, args.out)

    for event in events[: args.preview]:
        print(event.model_dump_json(indent=2))
    print(f"Total events: {len(events)}")
    print(f"Wrote JSONL to: {args.out}")


if __name__ == "__main__":
    main()
