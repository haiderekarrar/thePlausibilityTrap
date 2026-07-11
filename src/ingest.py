"""Parse iMessage exports into the project's shared Event schema."""

import argparse
from datetime import datetime
from pathlib import Path
import re
from typing import Literal

from pydantic import BaseModel


TIMESTAMP_PATTERN = re.compile(
    r"^(?P<timestamp>[A-Z][a-z]{2} \d{1,2}, \d{4}\s+\d{1,2}:\d{2}:\d{2} [AP]M)"
    r"(?: \([^)]*\))?$"
)


class Event(BaseModel):
    id: str
    timestamp: datetime
    channel: Literal["email", "imessage", "whatsapp", "bank", "invoice", "payment_app"]
    actor: str
    counterparty: str
    text: str
    amount: float | None
    source_file: str


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
        )
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


def write_events(events: list[Event], output_path: Path) -> None:
    """Write one JSON Event per line for the next pipeline stage."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        for event in events:
            output_file.write(event.model_dump_json() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse a two-person iMessage export into Event JSONL."
    )
    parser.add_argument("input_path", type=Path, help="Path to an iMessage export text file.")
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

    events = parse_imessage_export(args.input_path)
    write_events(events, args.out)

    for event in events[: args.preview]:
        print(event.model_dump_json(indent=2))
    print(f"Total events: {len(events)}")
    print(f"Wrote JSONL to: {args.out}")


if __name__ == "__main__":
    main()
