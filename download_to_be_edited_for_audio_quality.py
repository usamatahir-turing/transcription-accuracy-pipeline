"""Copy conversation channel files into the audio-quality edit workspace.

Reads ``to_be_edited_for_audio_quality.csv`` for session IDs, locates each
conversation under ``Conversations/<batch>/<session_id>/``, and copies every
speaker's canonical ``.wav``, ``.rttm``, and ``.seglst.json`` (excluding
``*_approved`` / ``*_fixed`` seglst variants) into
``to_be_edited_for_audio_quality/<session_id>/``.

Existing destination files are left unchanged; only missing files are copied.

Usage
-----
    python download_to_be_edited_for_audio_quality.py --dry-run
    python download_to_be_edited_for_audio_quality.py
    python download_to_be_edited_for_audio_quality.py --csv to_be_edited_for_audio_quality.csv
"""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path

from conversation_structure_pipeline.mute_failing_regions import (
    canonical_seglst_files,
    load_csv,
)

DEFAULT_CSV = Path("to_be_edited_for_audio_quality.csv")
DEFAULT_CONVERSATIONS = Path("Conversations")
DEFAULT_WORKSPACE = Path("to_be_edited_for_audio_quality")
_SEGLST_SUFFIX = ".seglst.json"


@dataclass
class CopyStats:
    copied: int = 0
    skipped_existing: int = 0
    missing_source: int = 0


def unique_session_ids(csv_rows: list[dict[str, str]]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for row in csv_rows:
        session_id = row["session_id"]
        if session_id in seen:
            continue
        seen.add(session_id)
        out.append(session_id)
    return out


def find_session_dir(conversations_root: Path, session_id: str) -> Path:
    """Return ``Conversations/<batch>/<session_id>`` searching all batch folders."""
    if not conversations_root.is_dir():
        raise FileNotFoundError(f"Conversations root not found: {conversations_root}")

    matches: list[Path] = []
    for batch_dir in sorted(p for p in conversations_root.iterdir() if p.is_dir()):
        candidate = batch_dir / session_id
        if candidate.is_dir():
            matches.append(candidate)

    if not matches:
        raise FileNotFoundError(
            f"{session_id}: not found under any batch in {conversations_root}",
        )
    if len(matches) > 1:
        paths = ", ".join(str(p) for p in matches)
        raise FileNotFoundError(
            f"{session_id}: found in multiple batches: {paths}",
        )
    return matches[0]


def channel_triplet_paths(session_dir: Path, seglst_path: Path) -> tuple[Path, Path, Path]:
    """Return (seglst, wav, rttm) for one canonical speaker stem."""
    stem = seglst_path.name[: -len(_SEGLST_SUFFIX)]
    wav = session_dir / f"{stem}.wav"
    rttm = session_dir / f"{stem}.rttm"
    return seglst_path, wav, rttm


def copy_session(
    *,
    source_dir: Path,
    dest_dir: Path,
    dry_run: bool,
) -> CopyStats:
    stats = CopyStats()
    seglst_files = canonical_seglst_files(source_dir)
    if not seglst_files:
        raise FileNotFoundError(f"{source_dir.name}: no canonical .seglst.json files")

    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)

    for seglst in seglst_files:
        seglst_src, wav_src, rttm_src = channel_triplet_paths(source_dir, seglst)
        for src in (seglst_src, wav_src, rttm_src):
            if not src.is_file():
                stats.missing_source += 1
                print(f"    MISSING source: {src.name}")
                continue

            dest = dest_dir / src.name
            if dest.is_file():
                stats.skipped_existing += 1
                continue

            if dry_run:
                print(f"    PLAN {src} -> {dest}")
            else:
                shutil.copy2(src, dest)
                print(f"    COPY {src.name}")
            stats.copied += 1

    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help=f"work queue CSV (default: {DEFAULT_CSV})",
    )
    parser.add_argument(
        "--conversations",
        type=Path,
        default=DEFAULT_CONVERSATIONS,
        help=f"source Conversations root (default: {DEFAULT_CONVERSATIONS})",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=DEFAULT_WORKSPACE,
        help=f"destination workspace root (default: {DEFAULT_WORKSPACE})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print planned copies without writing files",
    )
    args = parser.parse_args(argv)

    if not args.csv.is_file():
        print(f"ERROR: CSV not found: {args.csv.resolve()}")
        return 1

    csv_rows = load_csv(args.csv)
    session_ids = unique_session_ids(csv_rows)
    if not session_ids:
        print(f"ERROR: no session_id rows in {args.csv}")
        return 1

    totals = CopyStats()
    errors = 0

    print(
        f"{'DRY-RUN ' if args.dry_run else ''}"
        f"Copying {len(session_ids)} session(s) from {args.conversations} "
        f"to {args.workspace}",
    )

    for session_id in session_ids:
        print(f"{session_id}")
        try:
            source_dir = find_session_dir(args.conversations, session_id)
            dest_dir = args.workspace / session_id
            print(f"  from {source_dir}")
            stats = copy_session(
                source_dir=source_dir,
                dest_dir=dest_dir,
                dry_run=args.dry_run,
            )
            totals.copied += stats.copied
            totals.skipped_existing += stats.skipped_existing
            totals.missing_source += stats.missing_source
            if stats.missing_source:
                errors += 1
        except (FileNotFoundError, OSError) as exc:
            errors += 1
            print(f"  ERROR: {exc}")

    print(
        f"\nDone: copied={totals.copied}, "
        f"skipped_existing={totals.skipped_existing}, "
        f"missing_source={totals.missing_source}"
        + (f", {errors} session error(s)" if errors else ""),
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
