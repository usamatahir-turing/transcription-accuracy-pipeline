"""Copy edited audio-quality channels to the Gecko handoff folder.

Reads completed mute-pipeline rows from ``mute_pipeline_state.json`` (or
``audio_quality_edits.csv``) and copies the edited ``.wav``, ``.rttm``, and
``.seglst.json`` for each channel that had at least one mute applied.

Destination layout::

    <dest>/<session_id>/<channel_stem>.wav
    <dest>/<session_id>/<channel_stem>_approved.rttm
    <dest>/<session_id>/<channel_stem>_approved.seglst.json

Usage
-----
    python upload_audio_quality_edits.py --dry-run
    python upload_audio_quality_edits.py
    python upload_audio_quality_edits.py --dest "G:/Shared drives/NVidia [Internal]/edits_done_move_to_gecko"
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from conversation_structure_pipeline.mute_failing_regions import resolve_channel_files

DEFAULT_WORKSPACE = Path("to_be_edited_for_audio_quality")
DEFAULT_STATE = DEFAULT_WORKSPACE / "mute_pipeline_state.json"
DEFAULT_EDITS_CSV = Path("audio_quality_edits.csv")
DEFAULT_DEST = Path(
    r"G:\Shared drives\NVidia [Internal]\edits_done_move_to_gecko",
)


@dataclass(frozen=True)
class EditChannel:
    session_id: str
    channel: str


def parse_state_key(key: str) -> tuple[str, str]:
    if "|" not in key:
        raise ValueError(f"invalid state key (expected session|channel): {key!r}")
    session_id, channel = key.split("|", 1)
    return session_id.strip(), channel.strip()


def edited_channels_from_state(state_path: Path) -> list[EditChannel]:
    data = json.loads(state_path.read_text(encoding="utf-8-sig"))
    entries = data.get("entries") or {}
    out: list[EditChannel] = []
    for key, entry in entries.items():
        if entry.get("status") != "done":
            continue
        if int(entry.get("num_muted_segments") or 0) <= 0:
            continue
        session_id, channel = parse_state_key(key)
        out.append(EditChannel(session_id=session_id, channel=channel))
    out.sort(key=lambda row: (row.session_id, row.channel))
    return out


def edited_channels_from_csv(csv_path: Path) -> list[EditChannel]:
    out: list[EditChannel] = []
    with csv_path.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            if int(row.get("num_muted_segments") or 0) <= 0:
                continue
            out.append(
                EditChannel(
                    session_id=(row.get("conversation") or "").strip(),
                    channel=(row.get("channel") or "").strip(),
                ),
            )
    out.sort(key=lambda row: (row.session_id, row.channel))
    return out


def approved_dest_names(channel_stem: str) -> dict[str, str]:
    return {
        "wav": f"{channel_stem}.wav",
        "rttm": f"{channel_stem}_approved.rttm",
        "seglst": f"{channel_stem}_approved.seglst.json",
    }


def copy_edited_channel(
    *,
    workspace: Path,
    dest_root: Path,
    session_id: str,
    channel: str,
    dry_run: bool,
) -> list[tuple[Path, Path]]:
    session_dir = workspace / session_id
    if not session_dir.is_dir():
        raise FileNotFoundError(f"missing session folder: {session_dir}")

    files = resolve_channel_files(session_dir, channel)
    src = {
        "wav": files.wav,
        "rttm": files.rttm,
        "seglst": files.seglst,
    }
    for kind, path in src.items():
        if not path.is_file():
            raise FileNotFoundError(f"missing edited {kind} file: {path}")

    dest_dir = dest_root / session_id
    names = approved_dest_names(files.channel_stem)
    planned: list[tuple[Path, Path]] = []
    for kind, src_path in src.items():
        dest_path = dest_dir / names[kind]
        planned.append((src_path, dest_path))
        if dry_run:
            print(f"  PLAN {src_path} -> {dest_path}")
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest_path)
            print(f"  COPY {src_path.name} -> {dest_path}")
    return planned


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=DEFAULT_WORKSPACE,
        help=f"edited session folders (default: {DEFAULT_WORKSPACE})",
    )
    parser.add_argument(
        "--state",
        type=Path,
        default=DEFAULT_STATE,
        help=f"mute pipeline state JSON (default: {DEFAULT_STATE})",
    )
    parser.add_argument(
        "--edits-csv",
        type=Path,
        default=DEFAULT_EDITS_CSV,
        help=f"fallback edits CSV if state is missing (default: {DEFAULT_EDITS_CSV})",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help="destination root on Shared drive",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print planned copies without writing files",
    )
    args = parser.parse_args(argv)

    if args.state.is_file():
        channels = edited_channels_from_state(args.state)
        source_label = str(args.state)
    elif args.edits_csv.is_file():
        channels = edited_channels_from_csv(args.edits_csv)
        source_label = str(args.edits_csv)
    else:
        print(f"ERROR: neither state nor edits CSV found:")
        print(f"  {args.state.resolve()}")
        print(f"  {args.edits_csv.resolve()}")
        return 1

    if not channels:
        print(f"No edited channels found in {source_label}")
        return 0

    if not args.dry_run and not args.dest.exists():
        print(f"WARNING: destination does not exist yet (will be created): {args.dest}")

    by_session: dict[str, list[str]] = defaultdict(list)
    file_count = 0
    errors = 0

    print(
        f"{'DRY-RUN ' if args.dry_run else ''}"
        f"Uploading {len(channels)} edited channel(s) to {args.dest}",
    )
    print(f"Source list: {source_label}")

    for row in channels:
        by_session[row.session_id].append(row.channel)
        print(f"{row.session_id}/{row.channel}")
        try:
            copies = copy_edited_channel(
                workspace=args.workspace,
                dest_root=args.dest,
                session_id=row.session_id,
                channel=row.channel,
                dry_run=args.dry_run,
            )
            file_count += len(copies)
        except (FileNotFoundError, OSError, ValueError) as exc:
            errors += 1
            print(f"  ERROR: {exc}")

    print(
        f"\nDone: {len(by_session)} session folder(s), "
        f"{len(channels)} channel(s), {file_count} file(s)"
        + (f", {errors} error(s)" if errors else ""),
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
