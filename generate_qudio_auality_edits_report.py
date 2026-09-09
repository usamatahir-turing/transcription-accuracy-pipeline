"""Build ``audio_quality_edits.csv`` from ``mute_pipeline_state.json``.

Usage
-----
    python generate_qudio_auality_edits_report.py
    python generate_qudio_auality_edits_report.py --state to_be_edited_for_audio_quality/mute_pipeline_state.json
    python generate_qudio_auality_edits_report.py -o reports/audio_quality_edits.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

DEFAULT_WORKSPACE = Path("to_be_edited_for_audio_quality")
DEFAULT_STATE = DEFAULT_WORKSPACE / "mute_pipeline_state.json"
DEFAULT_OUTPUT = Path("audio_quality_edits.csv")

CSV_COLUMNS = [
    "conversation",
    "channel",
    "overlap_before_pct",
    "overlap_after_pct",
    "old_sig",
    "new_sig",
    "num_muted_segments",
    "time_muted_segments",
    "total_speech_time_after_muting",
    "stopped_reason",
]


def parse_entry_key(key: str) -> tuple[str, str]:
    if "|" not in key:
        raise ValueError(f"invalid state entry key (expected session|channel): {key!r}")
    session_id, channel = key.split("|", 1)
    return session_id.strip(), channel.strip()


def load_state(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    entries = data.get("entries")
    if not isinstance(entries, dict):
        raise ValueError(f"{path}: expected top-level 'entries' object")
    return entries


def entry_to_row(key: str, entry: dict) -> dict[str, object]:
    conversation, channel = parse_entry_key(key)
    return {
        "conversation": conversation,
        "channel": channel,
        "overlap_before_pct": entry.get("overlap_before_pct"),
        "overlap_after_pct": entry.get("overlap_after_pct"),
        "old_sig": entry.get("old_sig"),
        "new_sig": entry.get("new_sig"),
        "num_muted_segments": entry.get("num_muted_segments"),
        "time_muted_segments": entry.get("time_muted_segments"),
        "total_speech_time_after_muting": entry.get("total_speech_time_after_muting"),
        "stopped_reason": entry.get("stopped_reason"),
    }


def build_rows(entries: dict) -> list[dict[str, object]]:
    rows = [entry_to_row(key, entry) for key, entry in entries.items()]
    rows.sort(key=lambda row: (str(row["conversation"]), str(row["channel"])))
    return rows


def write_csv(rows: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--state",
        type=Path,
        default=DEFAULT_STATE,
        help=f"mute pipeline state JSON (default: {DEFAULT_STATE})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"output CSV path (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args(argv)

    if not args.state.is_file():
        print(f"ERROR: state file not found: {args.state.resolve()}")
        return 1

    try:
        entries = load_state(args.state)
        rows = build_rows(entries)
        write_csv(rows, args.output)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"Wrote {len(rows)} row(s) to {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
