"""Upload riverside_raw channel WAVs to Google Drive (batch/conversation layout).

Uploads only ``*.wav`` from ``riverside_raw/<batch>/<conversation>/`` into Drive
folder ``1a4_IU71HnHsmVS-mFl59J70oSrMcIiNA`` as:

    <batch>/<conversation>/<file>.wav

No ``riverside_raw`` wrapper folder on Drive. Existing files are skipped unless
``--overwrite``. Auth matches ``download_and_upload_data.py`` (SA impersonation).

Usage
-----
    python -m audio_quality_pipeline.upload_riverside_wavs
    python -m audio_quality_pipeline.upload_riverside_wavs --batch delivery_batch_07012026
    python -m audio_quality_pipeline.upload_riverside_wavs --conversation NV-EN-SS12-CONVO30
    python -m audio_quality_pipeline.upload_riverside_wavs --overwrite
"""

from __future__ import annotations

import argparse
import mimetypes
from pathlib import Path

from workflow_common import add_scope_args, resolve_conversation_dirs

DEFAULT_LOCAL_ROOT = Path("riverside_raw")
DEFAULT_DRIVE_FOLDER_ID = "1a4_IU71HnHsmVS-mFl59J70oSrMcIiNA"
FOLDER_MIME = "application/vnd.google-apps.folder"


def list_children_by_name(drive_service, folder_id: str) -> dict[str, tuple[str, str]]:
    """Return ``{name: (id, mimeType)}`` for non-trashed children of ``folder_id``."""
    out: dict[str, tuple[str, str]] = {}
    page_token = None
    while True:
        res = (
            drive_service.files()
            .list(
                q=f"'{folder_id}' in parents and trashed = false",
                spaces="drive",
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token,
                pageSize=1000,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )
        for f in res.get("files", []):
            out[f["name"]] = (f["id"], f["mimeType"])
        page_token = res.get("nextPageToken")
        if not page_token:
            break
    return out


def ensure_child_folder(
    drive_service,
    parent_id: str,
    name: str,
    *,
    cache: dict[str, dict[str, tuple[str, str]]],
) -> str:
    """Return folder id for ``name`` under ``parent_id``, creating if needed."""
    if parent_id not in cache:
        cache[parent_id] = list_children_by_name(drive_service, parent_id)
    children = cache[parent_id]
    existing = children.get(name)
    if existing and existing[1] == FOLDER_MIME:
        return existing[0]
    if existing and existing[1] != FOLDER_MIME:
        raise RuntimeError(
            f"Drive item '{name}' under {parent_id} exists but is not a folder "
            f"(mime={existing[1]})"
        )

    created = (
        drive_service.files()
        .create(
            body={"name": name, "mimeType": FOLDER_MIME, "parents": [parent_id]},
            supportsAllDrives=True,
            fields="id",
        )
        .execute()
    )
    folder_id = created["id"]
    children[name] = (folder_id, FOLDER_MIME)
    cache[folder_id] = {}  # new empty folder
    print(f"  MKDIR  {name}")
    return folder_id


def upload_or_skip_wav(
    drive_service,
    *,
    parent_id: str,
    local_path: Path,
    overwrite: bool,
    cache: dict[str, dict[str, tuple[str, str]]],
) -> str:
    """Upload ``local_path`` into ``parent_id``. Returns action uploaded|updated|skipped."""
    from googleapiclient.http import MediaFileUpload

    if parent_id not in cache:
        cache[parent_id] = list_children_by_name(drive_service, parent_id)
    children = cache[parent_id]
    name = local_path.name
    existing = children.get(name)

    if existing and existing[1] == FOLDER_MIME:
        raise RuntimeError(f"Drive item '{name}' is a folder; cannot upload WAV over it")

    if existing and not overwrite:
        return "skipped"

    media = MediaFileUpload(
        str(local_path),
        mimetype=mimetypes.guess_type(name)[0] or "audio/wav",
        resumable=True,
    )

    if existing and overwrite:
        (
            drive_service.files()
            .update(
                fileId=existing[0],
                media_body=media,
                supportsAllDrives=True,
                fields="id",
            )
            .execute()
        )
        return "updated"

    created = (
        drive_service.files()
        .create(
            body={"name": name, "parents": [parent_id]},
            media_body=media,
            supportsAllDrives=True,
            fields="id",
        )
        .execute()
    )
    children[name] = (created["id"], "audio/wav")
    return "uploaded"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # Reuse scope flags but default WAV root to riverside_raw.
    add_scope_args(parser, with_file=False)
    parser.set_defaults(conversations=str(DEFAULT_LOCAL_ROOT))
    parser.add_argument(
        "--drive-folder-id",
        default=DEFAULT_DRIVE_FOLDER_ID,
        help=f"Destination Drive folder id (default: {DEFAULT_DRIVE_FOLDER_ID})",
    )
    # add_scope_args already has --overwrite; use it for Drive replace.
    args = parser.parse_args(argv)

    local_root = Path(args.conversations)
    if not local_root.is_dir():
        print(f"ERROR: local root not found: {local_root.resolve()}")
        return 1

    try:
        session_dirs = resolve_conversation_dirs(
            local_root, args.batch, args.conversation)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit > 0:
        session_dirs = session_dirs[: args.limit]

    from download_and_upload_data import get_authenticated_drive_service

    drive = get_authenticated_drive_service()
    folder_cache: dict[str, dict[str, tuple[str, str]]] = {}
    stats = {"uploaded": 0, "updated": 0, "skipped": 0, "errors": 0, "wavs": 0}

    print(f"Local root: {local_root.resolve()}")
    print(f"Drive folder: {args.drive_folder_id}")
    print(f"Sessions: {len(session_dirs)} (overwrite={args.overwrite})")

    for session_dir in session_dirs:
        batch = session_dir.parent.name
        session = session_dir.name
        wavs = sorted(session_dir.glob("*.wav"))
        if not wavs:
            continue

        try:
            batch_id = ensure_child_folder(
                drive, args.drive_folder_id, batch, cache=folder_cache)
            session_id = ensure_child_folder(
                drive, batch_id, session, cache=folder_cache)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL folders {batch}/{session}: {exc}")
            stats["errors"] += 1
            continue

        for wav_path in wavs:
            stats["wavs"] += 1
            rel = f"{batch}/{session}/{wav_path.name}"
            try:
                action = upload_or_skip_wav(
                    drive,
                    parent_id=session_id,
                    local_path=wav_path,
                    overwrite=args.overwrite,
                    cache=folder_cache,
                )
                stats[action] = stats.get(action, 0) + 1
                print(f"  {action.upper():8s} {rel}")
            except Exception as exc:  # noqa: BLE001
                stats["errors"] += 1
                print(f"  FAIL {rel}: {exc}")

    print(
        f"\nDone. wavs={stats['wavs']} uploaded={stats['uploaded']} "
        f"updated={stats['updated']} skipped={stats['skipped']} "
        f"errors={stats['errors']}"
    )
    return 0 if stats["errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
