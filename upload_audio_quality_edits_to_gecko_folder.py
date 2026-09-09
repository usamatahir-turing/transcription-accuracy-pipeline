"""Upload edited audio-quality files to the Gecko Google Drive folder.

Scans ``to_be_edited_for_audio_quality/<session_id>/`` for speakers that were
edited (identified by ``{stem}_og.wav``). For each, replaces the matching
files in Drive under folder ``1D8isShidIb1hcZuCezV-Qe7EsmsmKBR1``:

    local {stem}.wav              -> Drive {stem}.wav
    local {stem}.seglst.json      -> Drive {stem}_approved.seglst.json

Drive targets must already exist; missing session folders or files are skipped
with an error message. Uses the same service-account impersonation as
``download_and_upload_data.py``.

Usage
-----
    python upload_audio_quality_edits_to_gecko_folder.py --dry-run
    python upload_audio_quality_edits_to_gecko_folder.py
    python upload_audio_quality_edits_to_gecko_folder.py --folder-id 1D8is...
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from download_and_upload_data import (
    get_authenticated_drive_service,
    list_drive_folder_files,
)

DEFAULT_WORKSPACE = Path("to_be_edited_for_audio_quality")
DEFAULT_DRIVE_FOLDER_ID = "1D8isShidIb1hcZuCezV-Qe7EsmsmKBR1"
_SEGLST_SUFFIX = ".seglst.json"


@dataclass
class UploadStats:
    uploaded: int = 0
    skipped_missing_drive_file: int = 0
    skipped_missing_local: int = 0
    session_errors: int = 0
    messages: list[str] = field(default_factory=list)


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


def edited_stems(session_dir: Path) -> list[str]:
    stems = sorted({path.name[: -len("_og.wav")] for path in session_dir.glob("*_og.wav")})
    return stems


def drive_targets_for_stem(stem: str) -> tuple[str, str]:
    return f"{stem}.wav", f"{stem}_approved{_SEGLST_SUFFIX}"


def local_sources(session_dir: Path, stem: str) -> tuple[Path, Path]:
    return session_dir / f"{stem}.wav", session_dir / f"{stem}{_SEGLST_SUFFIX}"


def upload_replace_file(
    drive_service,
    *,
    file_meta: dict,
    local_path: Path,
    dry_run: bool,
) -> None:
    if dry_run:
        print(f"    PLAN replace Drive:{file_meta['name']} <- {local_path}")
        return
    media = MediaFileUpload(str(local_path), resumable=True)
    drive_service.files().update(
        fileId=file_meta["id"],
        media_body=media,
        supportsAllDrives=True,
    ).execute()
    print(f"    UPLOAD {local_path.name} -> Drive:{file_meta['name']}")


def upload_edited_file(
    drive_service,
    *,
    drive_files: dict[str, dict],
    drive_name: str,
    local_path: Path,
    dry_run: bool,
    stats: UploadStats,
) -> None:
    if not local_path.is_file():
        stats.skipped_missing_local += 1
        msg = f"    SKIP missing local file: {local_path}"
        print(msg)
        stats.messages.append(msg.strip())
        return

    file_meta = drive_files.get(drive_name)
    if file_meta is None:
        stats.skipped_missing_drive_file += 1
        msg = f"    SKIP missing on Drive: {drive_name}"
        print(msg)
        stats.messages.append(msg.strip())
        return

    upload_replace_file(
        drive_service,
        file_meta=file_meta,
        local_path=local_path,
        dry_run=dry_run,
    )
    stats.uploaded += 1


def upload_session(
    drive_service,
    *,
    workspace: Path,
    session_id: str,
    session_folder_id: str,
    dry_run: bool,
) -> UploadStats:
    stats = UploadStats()
    session_dir = workspace / session_id
    drive_files = list_drive_folder_files(drive_service, session_folder_id)

    for stem in edited_stems(session_dir):
        wav_name, seglst_name = drive_targets_for_stem(stem)
        wav_src, seglst_src = local_sources(session_dir, stem)
        print(f"  {stem}")
        upload_edited_file(
            drive_service,
            drive_files=drive_files,
            drive_name=wav_name,
            local_path=wav_src,
            dry_run=dry_run,
            stats=stats,
        )
        upload_edited_file(
            drive_service,
            drive_files=drive_files,
            drive_name=seglst_name,
            local_path=seglst_src,
            dry_run=dry_run,
            stats=stats,
        )
    return stats


def iter_workspace_sessions(workspace: Path) -> list[str]:
    if not workspace.is_dir():
        return []
    return sorted(
        p.name for p in workspace.iterdir()
        if p.is_dir() and list(p.glob("*_og.wav"))
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=DEFAULT_WORKSPACE,
        help=f"local edit workspace (default: {DEFAULT_WORKSPACE})",
    )
    parser.add_argument(
        "--folder-id",
        default=DEFAULT_DRIVE_FOLDER_ID,
        help=f"Gecko Drive parent folder ID (default: {DEFAULT_DRIVE_FOLDER_ID})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print planned uploads without calling Drive",
    )
    args = parser.parse_args(argv)

    sessions = iter_workspace_sessions(args.workspace)
    if not sessions:
        print(f"No edited sessions found under {args.workspace} (*_og.wav)")
        return 0

    if args.dry_run:
        print(f"DRY-RUN uploading from {args.workspace} to Drive folder {args.folder_id}")
    else:
        print(f"Uploading from {args.workspace} to Drive folder {args.folder_id}")

    drive_service = get_authenticated_drive_service()
    folders_by_name = list_drive_child_folders(drive_service, args.folder_id)

    totals = UploadStats()

    for session_id in sessions:
        print(session_id)
        folder_id, err = resolve_session_drive_folder(folders_by_name, session_id)
        if err:
            totals.session_errors += 1
            print(f"  ERROR: {err}")
            totals.messages.append(err)
            continue

        assert folder_id is not None
        stats = upload_session(
            drive_service,
            workspace=args.workspace,
            session_id=session_id,
            session_folder_id=folder_id,
            dry_run=args.dry_run,
        )
        totals.uploaded += stats.uploaded
        totals.skipped_missing_drive_file += stats.skipped_missing_drive_file
        totals.skipped_missing_local += stats.skipped_missing_local
        totals.messages.extend(stats.messages)

    print(
        f"\nDone: uploaded={totals.uploaded}, "
        f"skipped_missing_drive_file={totals.skipped_missing_drive_file}, "
        f"skipped_missing_local={totals.skipped_missing_local}, "
        f"session_errors={totals.session_errors}",
    )
    return 1 if (totals.session_errors or totals.skipped_missing_local) else 0


if __name__ == "__main__":
    raise SystemExit(main())
