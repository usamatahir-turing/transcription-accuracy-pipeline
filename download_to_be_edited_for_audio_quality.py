"""Copy conversation channel files into the audio-quality edit workspace.

Reads ``to_be_edited_for_audio_quality.csv`` for session IDs. For each session:

  1. If complete under ``Conversations/<batch>/<session_id>/``, copy canonical
     ``.wav``, ``.rttm``, and ``.seglst.json`` into the workspace (missing
     destination files only).
  2. Otherwise download from the Gecko Drive folder (default
     ``1D8isShidIb1hcZuCezV-Qe7EsmsmKBR1``): pair ``{stem}.wav`` with
     ``{stem}_approved.seglst.json``, save as ``{stem}.wav`` /
     ``{stem}.seglst.json``, generate ``{stem}.rttm``, and overwrite any
     existing workspace files for that session.

Usage
-----
    python download_to_be_edited_for_audio_quality.py --dry-run
    python download_to_be_edited_for_audio_quality.py
    python download_to_be_edited_for_audio_quality.py --csv to_be_edited_for_audio_quality.csv
"""

from __future__ import annotations

import argparse
import io
import json
import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from conversation_structure_pipeline.mute_failing_regions import (
    canonical_seglst_files,
    load_csv,
)

DEFAULT_CSV = Path("to_be_edited_for_audio_quality.csv")
DEFAULT_CONVERSATIONS = Path("Conversations")
DEFAULT_WORKSPACE = Path("to_be_edited_for_audio_quality")
DEFAULT_DRIVE_FOLDER_ID = "1D8isShidIb1hcZuCezV-Qe7EsmsmKBR1"
_SEGLST_SUFFIX = ".seglst.json"
_APPROVED_SEGLST_SUFFIX = "_approved.seglst.json"
_RTTM_CHANNEL = "1"


@dataclass
class CopyStats:
    copied: int = 0
    skipped_existing: int = 0
    missing_source: int = 0


@dataclass
class DriveStats:
    downloaded: int = 0
    rttm_generated: int = 0
    skipped_unpaired: int = 0
    warnings: list[str] = field(default_factory=list)


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


def local_session_complete(source_dir: Path) -> tuple[bool, list[str]]:
    """Return whether every canonical speaker triplet exists locally."""
    issues: list[str] = []
    seglst_files = canonical_seglst_files(source_dir)
    if not seglst_files:
        return False, ["no canonical .seglst.json files"]

    for seglst in seglst_files:
        seglst_src, wav_src, rttm_src = channel_triplet_paths(source_dir, seglst)
        for src in (seglst_src, wav_src, rttm_src):
            if not src.is_file():
                issues.append(f"missing {src.name}")
    return not issues, issues


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


def format_rttm_line(speaker: str, start: float, end: float) -> str:
    duration = end - start
    return (
        f"SPEAKER {speaker} {_RTTM_CHANNEL} {start:.3f} {duration:.3f} "
        f"<NA> <NA> {speaker} <NA> <NA>\n"
    )


def seglst_to_rttm_file(seglst_path: Path, rttm_path: Path) -> int:
    """Write RTTM from seglst (all segments, sorted by start). Returns line count."""
    data: list[dict[str, Any]] = json.loads(
        seglst_path.read_text(encoding="utf-8-sig"),
    )
    if not isinstance(data, list):
        raise ValueError(f"{seglst_path}: expected JSON array")

    segments: list[tuple[float, float, str]] = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"{seglst_path}: item #{index} is not an object")
        try:
            speaker = str(item["speaker"])
            start = float(str(item["start_time"]).strip())
            end = float(str(item["end_time"]).strip())
        except KeyError as exc:
            raise ValueError(
                f"{seglst_path}: item #{index} missing {exc.args[0]!r}",
            ) from exc
        if end <= start:
            continue
        segments.append((start, end, speaker))

    segments.sort(key=lambda row: row[0])
    lines = [format_rttm_line(speaker, start, end) for start, end, speaker in segments]
    rttm_path.write_text("".join(lines), encoding="utf-8", newline="\n")
    return len(lines)


def list_drive_child_folders(drive_service, parent_id: str) -> dict[str, list[dict]]:
    """Return child folders keyed by name (may have duplicate names)."""
    grouped: dict[str, list[dict]] = defaultdict(list)
    page_token = None
    while True:
        query = (
            f"'{parent_id}' in parents and trashed = false "
            "and mimeType = 'application/vnd.google-apps.folder'"
        )
        res = drive_service.files().list(
            q=query,
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        for item in res.get("files", []):
            grouped[item["name"]].append(item)
        page_token = res.get("nextPageToken")
        if page_token is None:
            break
    return grouped


def resolve_session_drive_folder(
    folders_by_name: dict[str, list[dict]],
    session_id: str,
) -> tuple[str | None, str | None]:
    """Return (folder_id, error_message)."""
    matches = folders_by_name.get(session_id, [])
    if not matches:
        return None, f"{session_id}: no folder on Drive under parent"
    if len(matches) > 1:
        ids = ", ".join(m["id"] for m in matches)
        return None, f"{session_id}: expected 1 Drive folder, found {len(matches)} ({ids})"
    return matches[0]["id"], None


def drive_wav_stems(drive_files: dict[str, dict]) -> set[str]:
    return {name[: -len(".wav")] for name in drive_files if name.endswith(".wav")}


def drive_approved_stems(drive_files: dict[str, dict]) -> set[str]:
    return {
        name[: -len(_APPROVED_SEGLST_SUFFIX)]
        for name in drive_files
        if name.endswith(_APPROVED_SEGLST_SUFFIX)
    }


def paired_drive_stems(drive_files: dict[str, dict]) -> tuple[list[str], DriveStats]:
    """Return sorted paired stems and record warnings for unpaired files."""
    stats = DriveStats()
    wav_stems = drive_wav_stems(drive_files)
    approved_stems = drive_approved_stems(drive_files)

    for stem in sorted(wav_stems - approved_stems):
        msg = f"    SKIP {stem}: .wav present but {_APPROVED_SEGLST_SUFFIX} missing"
        print(msg)
        stats.warnings.append(msg.strip())
        stats.skipped_unpaired += 1

    for stem in sorted(approved_stems - wav_stems):
        msg = f"    SKIP {stem}: {_APPROVED_SEGLST_SUFFIX} present but .wav missing"
        print(msg)
        stats.warnings.append(msg.strip())
        stats.skipped_unpaired += 1

    paired = sorted(wav_stems & approved_stems)
    return paired, stats


def fetch_drive_file(
    drive_service,
    file_meta: dict,
    dest: Path,
    *,
    dry_run: bool,
) -> None:
    if dry_run:
        print(f"    PLAN download Drive:{file_meta['name']} -> {dest}")
        return
    from googleapiclient.http import MediaIoBaseDownload

    dest.parent.mkdir(parents=True, exist_ok=True)
    request = drive_service.files().get_media(fileId=file_meta["id"])
    with io.FileIO(str(dest), "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()


def download_session_from_drive(
    drive_service,
    *,
    session_folder_id: str,
    dest_dir: Path,
    dry_run: bool,
) -> DriveStats:
    from download_and_upload_data import list_drive_folder_files

    stats = DriveStats()
    drive_files = list_drive_folder_files(drive_service, session_folder_id)
    paired_stems, pair_stats = paired_drive_stems(drive_files)
    stats.skipped_unpaired += pair_stats.skipped_unpaired
    stats.warnings.extend(pair_stats.warnings)

    if not paired_stems:
        raise FileNotFoundError("no paired wav + _approved.seglst.json speakers on Drive")

    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)

    for stem in paired_stems:
        wav_name = f"{stem}.wav"
        approved_name = f"{stem}{_APPROVED_SEGLST_SUFFIX}"
        wav_dest = dest_dir / wav_name
        seglst_dest = dest_dir / f"{stem}{_SEGLST_SUFFIX}"
        rttm_dest = dest_dir / f"{stem}.rttm"

        print(f"  {stem}")
        fetch_drive_file(
            drive_service,
            drive_files[wav_name],
            wav_dest,
            dry_run=dry_run,
        )
        fetch_drive_file(
            drive_service,
            drive_files[approved_name],
            seglst_dest,
            dry_run=dry_run,
        )
        stats.downloaded += 2

        if dry_run:
            print(f"    PLAN generate {rttm_dest.name} from {seglst_dest.name}")
        else:
            lines = seglst_to_rttm_file(seglst_dest, rttm_dest)
            print(f"    RTTM {rttm_dest.name} ({lines} lines)")
        stats.rttm_generated += 1

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
        "--folder-id",
        default=DEFAULT_DRIVE_FOLDER_ID,
        help=f"Gecko Drive parent folder ID (default: {DEFAULT_DRIVE_FOLDER_ID})",
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

    copy_totals = CopyStats()
    drive_totals = DriveStats()
    errors = 0

    print(
        f"{'DRY-RUN ' if args.dry_run else ''}"
        f"Preparing {len(session_ids)} session(s) -> {args.workspace}",
    )

    drive_service = None
    folders_by_name: dict[str, list[dict]] | None = None

    for session_id in session_ids:
        print(session_id)
        dest_dir = args.workspace / session_id
        use_drive = False
        drive_reason = ""

        try:
            source_dir = find_session_dir(args.conversations, session_id)
            complete, issues = local_session_complete(source_dir)
            if complete:
                print(f"  from {source_dir}")
                stats = copy_session(
                    source_dir=source_dir,
                    dest_dir=dest_dir,
                    dry_run=args.dry_run,
                )
                copy_totals.copied += stats.copied
                copy_totals.skipped_existing += stats.skipped_existing
                copy_totals.missing_source += stats.missing_source
                continue
            use_drive = True
            drive_reason = "; ".join(issues)
        except FileNotFoundError as exc:
            use_drive = True
            drive_reason = str(exc)

        if not use_drive:
            continue

        print(f"  from Drive ({drive_reason})")
        if drive_service is None:
            from download_and_upload_data import get_authenticated_drive_service

            drive_service = get_authenticated_drive_service()
            folders_by_name = list_drive_child_folders(drive_service, args.folder_id)

        assert folders_by_name is not None
        folder_id, err = resolve_session_drive_folder(folders_by_name, session_id)
        if err:
            errors += 1
            print(f"  ERROR: {err}")
            continue

        try:
            stats = download_session_from_drive(
                drive_service,
                session_folder_id=folder_id,  # type: ignore[arg-type]
                dest_dir=dest_dir,
                dry_run=args.dry_run,
            )
            drive_totals.downloaded += stats.downloaded
            drive_totals.rttm_generated += stats.rttm_generated
            drive_totals.skipped_unpaired += stats.skipped_unpaired
            drive_totals.warnings.extend(stats.warnings)
        except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
            errors += 1
            print(f"  ERROR: {exc}")

    print(
        f"\nDone: local_copied={copy_totals.copied}, "
        f"local_skipped_existing={copy_totals.skipped_existing}, "
        f"drive_downloaded={drive_totals.downloaded}, "
        f"drive_rttm={drive_totals.rttm_generated}, "
        f"drive_unpaired_skips={drive_totals.skipped_unpaired}"
        + (f", {errors} session error(s)" if errors else ""),
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
