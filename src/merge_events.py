"""Merge validated Event JSONL files into one chronological Event timeline."""

import argparse
from pathlib import Path

from ingest import Event, read_events, write_events


def merge_event_files(input_paths: list[Path]) -> list[Event]:
    """Read Event files, reject duplicate IDs, and sort all events by time."""
    events: list[Event] = []
    event_ids: set[str] = set()

    for input_path in input_paths:
        for event in read_events(input_path):
            if event.timestamp.tzinfo is None:
                raise ValueError("All Event timestamps must include a timezone before merging.")
            if event.id in event_ids:
                raise ValueError("Duplicate Event ID found while merging.")
            event_ids.add(event.id)
            events.append(event)

    return sorted(events, key=lambda event: (event.timestamp, event.source_file, event.id))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge Event JSONL files into one chronological timeline."
    )
    parser.add_argument(
        "input_paths",
        nargs="+",
        type=Path,
        help="Two or more Event JSONL files to merge.",
    )
    parser.add_argument("--out", type=Path, required=True, help="Path for merged Event JSONL.")
    parser.add_argument(
        "--preview",
        type=int,
        default=5,
        help="Number of events to print before the total count (default: 5).",
    )
    args = parser.parse_args()

    if len(args.input_paths) < 2:
        parser.error("Provide at least two Event JSONL files to merge.")
    if args.preview < 0:
        parser.error("--preview must be zero or greater.")

    events = merge_event_files(args.input_paths)
    write_events(events, args.out)

    for event in events[: args.preview]:
        print(event.model_dump_json(indent=2))
    print(f"Total events: {len(events)}")
    print(f"Wrote JSONL to: {args.out}")


if __name__ == "__main__":
    main()
