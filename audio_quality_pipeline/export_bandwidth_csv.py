"""Export per-channel effective-bandwidth CSV; upload spectrogram PNGs to Drive.

Columns: batch, session_id, file_name, effective_hz, bucket, pass, speech_min,
peak_dbfs, spectrogram_url

Drive uploads use the same service-account impersonation as
``download_and_upload_data.py``. Remote PNG names are
``{batch}__{session_id}__{png_basename}`` to avoid collisions. Existing Drive
files are skipped unless ``--overwrite-drive``.

Usage
-----
    python -m audio_quality_pipeline.export_bandwidth_csv
    python -m audio_quality_pipeline.export_bandwidth_csv --batch delivery_batch_07012026
    python -m audio_quality_pipeline.export_bandwidth_csv --overwrite-drive
    python -m audio_quality_pipeline.export_bandwidth_csv --skip-upload
"""

from __future__ import annotations

import argparse
import csv
import json
import mimetypes
from pathlib import Path

from workflow_common import add_scope_args, resolve_conversation_dirs

BANDWIDTH_JSON_SUFFIX = "_bandwidth.json"
SPECTROGRAM_SUFFIX = "_bandwidth_spectrogram.png"
DEFAULT_OUT = Path(__file__).resolve().parent / "reports" / "bandwidth_channels.csv"
DEFAULT_DRIVE_FOLDER_ID = "1oTljr07Q6Sjj1x6UwCBf7b3r3c3d8jTC"

COLUMNS = (
    "batch",
    "session_id",
    "file_name",
    "effective_hz",
    "bucket",
    "pass",
    "speech_min",
    "peak_dbfs",
    "spectrogram_url",
)


def drive_view_url(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/view"


def remote_png_name(batch: str, session_id: str, png_name: str) -> str:
    return f"{batch}__{session_id}__{png_name}"


def list_drive_files_by_name(drive_service, folder_id: str) -> dict[str, str]:
    """Return ``{file_name: file_id}`` for non-trashed files in ``folder_id``."""
    out: dict[str, str] = {}
    page_token = None
    while True:
        res = (
            drive_service.files()
            .list(
                q=f"'{folder_id}' in parents and trashed = false",
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
                pageSize=1000,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )
        for f in res.get("files", []):
            out[f["name"]] = f["id"]
        page_token = res.get("nextPageToken")
        if not page_token:
            break
    return out


def upload_or_update_png(
    drive_service,
    *,
    folder_id: str,
    local_path: Path,
    remote_name: str,
    existing_id: str | None,
    overwrite: bool,
) -> tuple[str, str]:
    """Upload PNG; return ``(file_id, action)`` where action is uploaded|updated|skipped."""
    from googleapiclient.http import MediaFileUpload

    media = MediaFileUpload(
        str(local_path),
        mimetype=mimetypes.guess_type(local_path.name)[0] or "image/png",
        resumable=True,
    )

    if existing_id and not overwrite:
        return existing_id, "skipped"

    if existing_id and overwrite:
        updated = (
            drive_service.files()
            .update(
                fileId=existing_id,
                media_body=media,
                supportsAllDrives=True,
                fields="id",
            )
            .execute()
        )
        return updated["id"], "updated"

    created = (
        drive_service.files()
        .create(
            body={"name": remote_name, "parents": [folder_id]},
            media_body=media,
            supportsAllDrives=True,
            fields="id",
        )
        .execute()
    )
    return created["id"], "uploaded"


def ensure_spectrogram_urls(
    rows: list[dict],
    *,
    drive_folder_id: str,
    skip_upload: bool,
    overwrite_drive: bool,
) -> dict[str, int]:
    """Fill ``spectrogram_url`` on each row. Returns upload stats."""
    stats = {"uploaded": 0, "updated": 0, "skipped": 0, "missing_local": 0, "errors": 0}

    if skip_upload:
        for row in rows:
            row["spectrogram_url"] = ""
        return stats

    from download_and_upload_data import get_authenticated_drive_service

    drive = get_authenticated_drive_service()
    existing = list_drive_files_by_name(drive, drive_folder_id)
    print(f"Drive folder has {len(existing)} existing file(s).")

    # Cache remote_name -> url within this run.
    url_by_remote: dict[str, str] = {}

    for row in rows:
        local = row.pop("_png_path", None)
        remote = row.pop("_remote_png_name", None)
        if not local or not remote:
            row["spectrogram_url"] = ""
            stats["missing_local"] += 1
            continue
        local_path = Path(local)
        if not local_path.is_file():
            row["spectrogram_url"] = ""
            stats["missing_local"] += 1
            print(f"  MISS PNG {local_path}")
            continue

        if remote in url_by_remote and not overwrite_drive:
            row["spectrogram_url"] = url_by_remote[remote]
            stats["skipped"] += 1
            continue

        try:
            file_id, action = upload_or_update_png(
                drive,
                folder_id=drive_folder_id,
                local_path=local_path,
                remote_name=remote,
                existing_id=existing.get(remote),
                overwrite=overwrite_drive,
            )
            url = drive_view_url(file_id)
            url_by_remote[remote] = url
            existing[remote] = file_id
            row["spectrogram_url"] = url
            stats[action] = stats.get(action, 0) + 1
            print(f"  {action.upper():8s} {remote}")
        except Exception as exc:  # noqa: BLE001
            row["spectrogram_url"] = ""
            stats["errors"] += 1
            print(f"  FAIL {remote}: {exc}")

    return stats


def row_from_bandwidth_json(path: Path, batch: str) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  WARN skip {path}: {exc}")
        return None

    bw = data.get("bandwidth") or {}
    diag = data.get("diagnostics") or {}
    artifacts = data.get("artifacts") or {}
    file_name = data.get("wav")
    if not file_name:
        channel_id = data.get("channel_id") or path.name.removesuffix(BANDWIDTH_JSON_SUFFIX)
        file_name = f"{channel_id}.wav"

    session_id = data.get("session_id") or path.parent.name
    png_name = artifacts.get("spectrogram_png")
    png_path = path.parent / png_name if png_name else None
    if png_path is None or not png_path.is_file():
        # Fallback naming if JSON omitted artifact but PNG exists.
        speaker = data.get("speaker") or path.name.removesuffix(BANDWIDTH_JSON_SUFFIX)
        candidate = path.parent / f"{speaker}{SPECTROGRAM_SUFFIX}"
        if candidate.is_file():
            png_path = candidate
            png_name = candidate.name

    remote = (
        remote_png_name(batch, session_id, png_name)
        if png_name
        else None
    )

    return {
        "batch": batch,
        "session_id": session_id,
        "file_name": file_name,
        "effective_hz": bw.get("effective_hz"),
        "bucket": bw.get("bucket"),
        "pass": bw.get("pass"),
        "speech_min": diag.get("speech_min"),
        "peak_dbfs": diag.get("peak_dbfs"),
        "spectrogram_url": "",
        "_png_path": str(png_path) if png_path and png_path.is_file() else None,
        "_remote_png_name": remote,
    }


def collect_rows(session_dirs: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for session_dir in session_dirs:
        batch = session_dir.parent.name
        for path in sorted(session_dir.glob(f"*{BANDWIDTH_JSON_SUFFIX}")):
            row = row_from_bandwidth_json(path, batch)
            if row is not None:
                rows.append(row)
    return rows


def write_csv(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    clean = [{k: r.get(k) for k in COLUMNS} for r in rows]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(clean)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=False)
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output CSV path (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--drive-folder-id",
        default=DEFAULT_DRIVE_FOLDER_ID,
        help=f"Google Drive folder for spectrogram PNGs (default: {DEFAULT_DRIVE_FOLDER_ID})",
    )
    parser.add_argument(
        "--skip-upload",
        action="store_true",
        help="Write CSV without uploading PNGs (spectrogram_url left empty).",
    )
    parser.add_argument(
        "--overwrite-drive",
        action="store_true",
        help="Re-upload PNGs that already exist in the Drive folder.",
    )
    args = parser.parse_args(argv)

    root = Path(args.conversations)
    try:
        session_dirs = resolve_conversation_dirs(root, args.batch, args.conversation)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit > 0:
        session_dirs = session_dirs[: args.limit]

    rows = collect_rows(session_dirs)
    rows.sort(
        key=lambda r: (
            r["batch"] or "",
            r["session_id"] or "",
            r["file_name"] or "",
        )
    )

    stats = ensure_spectrogram_urls(
        rows,
        drive_folder_id=args.drive_folder_id,
        skip_upload=args.skip_upload,
        overwrite_drive=args.overwrite_drive,
    )

    out_path = Path(args.output)
    write_csv(rows, out_path)
    n_fail = sum(1 for r in rows if r.get("pass") is False)
    print(
        f"\nWrote {len(rows)} channel row(s) to {out_path} "
        f"({n_fail} with pass=False)."
    )
    if not args.skip_upload:
        print(
            "Drive PNGs: "
            f"uploaded={stats['uploaded']} updated={stats['updated']} "
            f"skipped={stats['skipped']} missing_local={stats['missing_local']} "
            f"errors={stats['errors']}"
        )
    return 0 if stats.get("errors", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
