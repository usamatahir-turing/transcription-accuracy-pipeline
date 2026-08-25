import csv
import io
import os
import re
import argparse
import requests
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as Oauth2Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Local pipeline artifacts under Conversations/ — never download from Drive and
# never delete during mirror cleanup (even when absent from Drive).
PIPELINE_OUTPUT_EXACT_NAMES = frozenset({
    "deter.json",
    "metrics.json",
    "overlap_ratio.json",
    "dnsmos.json",
    "bandwidth.json",
})
PIPELINE_OUTPUT_SUFFIXES = (
    "_der.rttm",
    "_deter.json",
    "_sad.rttm",
    "_top_deter_errors.json",
    "_qwen_norm.jsonl",
    "_qwen.jsonl",
    "_top_errors.json",
    "_transcript_norm.jsonl",
    "_transcript.jsonl",
    "_dnsmos.json",
    "_bandwidth.json",
    "_bandwidth_spectrogram.png",
)
DEFAULT_CSV = "download_batch.csv"
CONVERSATIONS_ROOT = "Conversations"


def is_pipeline_output(filename: str) -> bool:
    """True for DetER / WER / overlap files produced by run_pipeline.py."""
    name = os.path.basename(filename)
    if name in PIPELINE_OUTPUT_EXACT_NAMES:
        return True
    return any(name.endswith(suffix) for suffix in PIPELINE_OUTPUT_SUFFIXES)


def channel_source_filenames(channel: str) -> tuple[str, ...]:
    """Drive/local basenames synced in CSV batch mode."""
    channel = channel.strip()
    return (f"{channel}.wav", f"{channel}.seglst.json", f"{channel}.rttm")


def parse_drive_folder_id(link: str) -> str:
    """Extract a Google Drive folder ID from a URL or raw ID."""
    link = (link or "").strip()
    if not link:
        raise ValueError("empty Drive folder link")
    if "/folders/" in link:
        return link.split("/folders/", 1)[1].split("?", 1)[0].split("/", 1)[0]
    match = re.search(r"[?&]id=([^&]+)", link)
    if match:
        return match.group(1)
    if "/" not in link:
        return link
    raise ValueError(f"Cannot parse Drive folder ID from: {link}")


def new_sync_stats() -> dict[str, int]:
    return {
        "downloaded": 0,
        "skipped": 0,
        "skipped_pipeline": 0,
        "deleted": 0,
        "preserved_pipeline": 0,
        "missing_on_drive": 0,
    }


def get_authenticated_drive_service():
    """Handles Service Account Impersonation to bypass Vertex VM scopes."""
    print("Authenticating...")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "/home/jupyter/.config/gcloud/application_default_credentials.json"
    )

    base_credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    base_credentials.refresh(Request())

    TARGET_SERVICE_ACCOUNT = 'delivery-nvidia@delivery-nvidia.iam.gserviceaccount.com'

    url = (
        f"https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/"
        f"{TARGET_SERVICE_ACCOUNT}:generateAccessToken"
    )
    headers = {
        "Authorization": f"Bearer {base_credentials.token}",
        "Content-Type": "application/json",
    }
    payload = {
        "scope": ["https://www.googleapis.com/auth/drive"],
        "lifetime": "3600s",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(
            f"Authentication Failed! API Error {response.status_code}: {response.text}"
        )

    sa_token = response.json()['accessToken']
    creds = Oauth2Credentials(sa_token)

    return build('drive', 'v3', credentials=creds)


def list_drive_folder_files(drive_service, folder_id: str) -> dict[str, dict]:
    """Return direct child files in a Drive folder, keyed by basename."""
    out: dict[str, dict] = {}
    page_token = None
    while True:
        query = f"'{folder_id}' in parents and trashed = false"
        res = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType, modifiedTime)',
            pageToken=page_token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()

        for f in res.get('files', []):
            if f['mimeType'] == 'application/vnd.google-apps.folder':
                continue
            if 'application/vnd.google-apps' in f['mimeType']:
                continue
            out[f['name']] = f

        page_token = res.get('nextPageToken')
        if page_token is None:
            break
    return out


def _drive_mtime(file_meta: dict) -> datetime:
    drive_time_str = file_meta['modifiedTime']
    return datetime.fromisoformat(drive_time_str.replace('Z', '+00:00'))


def download_drive_file(
    drive_service,
    file_meta: dict,
    file_path: str,
    stats: dict[str, int],
) -> None:
    """Download one Drive file if local copy is missing or older."""
    drive_mtime = _drive_mtime(file_meta)

    needs_download = True
    if os.path.exists(file_path):
        local_mtime_ts = os.path.getmtime(file_path)
        local_mtime = datetime.fromtimestamp(local_mtime_ts, tz=timezone.utc)
        if local_mtime >= drive_mtime:
            needs_download = False

    if not needs_download:
        stats['skipped'] += 1
        return

    print(f"Downloading: {file_path}...")
    request = drive_service.files().get_media(fileId=file_meta['id'])
    with io.FileIO(file_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    drive_mtime_ts = drive_mtime.timestamp()
    os.utime(file_path, (drive_mtime_ts, drive_mtime_ts))
    stats['downloaded'] += 1


def load_csv_download_rows(csv_path: Path) -> list[dict[str, str]]:
    """Load ``session_id``, ``channel``, ``folder link`` rows from CSV."""
    rows: list[dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {csv_path}")

        normalized = {
            (name or "").strip().lower(): name for name in reader.fieldnames
        }
        for required in ("session_id", "channel", "folder link"):
            if required not in normalized:
                raise ValueError(
                    f"CSV {csv_path} must have columns: session_id, channel, "
                    f"'folder link' (found: {reader.fieldnames})"
                )

        session_key = normalized["session_id"]
        channel_key = normalized["channel"]
        link_key = normalized["folder link"]

        for line_no, raw in enumerate(reader, start=2):
            session_id = (raw.get(session_key) or "").strip()
            channel = (raw.get(channel_key) or "").strip()
            folder_link = (raw.get(link_key) or "").strip()
            if not session_id and not channel and not folder_link:
                continue
            if not session_id or not channel or not folder_link:
                raise ValueError(
                    f"{csv_path}:{line_no}: session_id, channel, and folder link "
                    f"are all required"
                )
            rows.append({
                "session_id": session_id,
                "channel": channel,
                "folder_link": folder_link,
            })
    return rows


def sync_channels_from_csv(
    drive_service,
    csv_rows: list[dict[str, str]],
    *,
    batch: str,
    conversations_root: Path,
) -> dict[str, int]:
    """Download selected channel files listed in a batch CSV."""
    stats = new_sync_stats()
    seen_rows: set[tuple[str, str]] = set()
    folder_cache: dict[str, dict[str, dict]] = {}

    # session_id -> set of scoped local file paths for cleanup
    scoped_by_session: dict[str, set[str]] = defaultdict(set)
    valid_local_paths: set[str] = set()

    batch_dir = conversations_root / batch
    batch_dir.mkdir(parents=True, exist_ok=True)

    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in csv_rows:
        key = (row["session_id"], row["folder_link"])
        grouped[key].append(row["channel"])

    print(
        f"\nCSV sync: {len(csv_rows)} row(s), "
        f"{len(grouped)} conversation folder(s) under {batch_dir}\n"
    )

    for (session_id, folder_link), channels in sorted(grouped.items()):
        folder_id = parse_drive_folder_id(folder_link)
        if folder_id not in folder_cache:
            print(f"Listing Drive folder {folder_id} ({session_id})...")
            folder_cache[folder_id] = list_drive_folder_files(drive_service, folder_id)
        drive_files = folder_cache[folder_id]

        dest_dir = batch_dir / session_id
        dest_dir.mkdir(parents=True, exist_ok=True)

        for channel in channels:
            dedupe_key = (session_id, channel)
            if dedupe_key in seen_rows:
                continue
            seen_rows.add(dedupe_key)

            print(f"  {session_id}/{channel}")
            for file_name in channel_source_filenames(channel):
                file_path = str(dest_dir / file_name)
                scoped_by_session[session_id].add(file_path)

                if is_pipeline_output(file_name):
                    stats['skipped_pipeline'] += 1
                    continue

                drive_meta = drive_files.get(file_name)
                if drive_meta is None:
                    stats['missing_on_drive'] += 1
                    print(f"    MISSING on Drive: {file_name}")
                    continue

                valid_local_paths.add(file_path)
                download_drive_file(drive_service, drive_meta, file_path, stats)

    print("\nStarting scoped local cleanup...")
    for session_id, scoped_paths in sorted(scoped_by_session.items()):
        for file_path in sorted(scoped_paths):
            if file_path in valid_local_paths:
                continue
            if not os.path.exists(file_path):
                continue
            if is_pipeline_output(os.path.basename(file_path)):
                stats['preserved_pipeline'] += 1
                continue
            os.remove(file_path)
            stats['deleted'] += 1
            print(f"Deleted orphaned scoped file: {file_path}")

    print(
        f"\nCSV sync complete! Downloaded: {stats['downloaded']} | "
        f"Skipped: {stats['skipped']} | "
        f"Missing on Drive: {stats['missing_on_drive']} | "
        f"Deleted: {stats['deleted']}"
    )
    return stats


def mirror_folder_sync_recursive(drive_service, root_folder_id, root_destination_dir):
    # State tracking across recursive calls
    stats = new_sync_stats()
    valid_local_paths = set()

    print(f"\nStarting recursive sync for root folder ID: {root_folder_id}")
    print(f"Destination: {root_destination_dir}\n")

    def process_folder(drive_folder_id, current_local_dir):
        # 1. Create the local directory if it doesn't exist
        os.makedirs(current_local_dir, exist_ok=True)
        valid_local_paths.add(current_local_dir)

        page_token = None
        while True:
            query = f"'{drive_folder_id}' in parents and trashed = false"
            res = drive_service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, modifiedTime)',
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            ).execute()

            files = res.get('files', [])

            for f in files:
                file_name = f['name']
                file_path = os.path.join(current_local_dir, file_name)

                # 2. If it's a folder, RECURSE into it
                if f['mimeType'] == 'application/vnd.google-apps.folder':
                    valid_local_paths.add(file_path)
                    process_folder(f['id'], file_path)
                    continue

                # Skip Google Workspace documents (Docs, Sheets)
                if 'application/vnd.google-apps' in f['mimeType']:
                    continue

                # Pipeline outputs are local-only; do not sync from Drive.
                if is_pipeline_output(file_name):
                    stats['skipped_pipeline'] += 1
                    continue

                # Mixed WAVs are large and unused by local pipelines; never download.
                if file_name.endswith("_mixed.wav"):
                    continue

                valid_local_paths.add(file_path)
                download_drive_file(drive_service, f, file_path, stats)

            page_token = res.get('nextPageToken', None)
            if page_token is None:
                break

    # Kick off the recursion from the root
    process_folder(root_folder_id, root_destination_dir)

    # 5. The Recursive Cleanup Phase
    print("\nStarting local cleanup...")
    for root, dirs, files in os.walk(root_destination_dir, topdown=False):

        for name in files:
            if name.startswith('.'):
                continue

            if is_pipeline_output(name):
                stats['preserved_pipeline'] += 1
                continue

            file_path = os.path.join(root, name)
            if file_path not in valid_local_paths:
                os.remove(file_path)
                stats['deleted'] += 1
                print(f"Deleted orphaned file: {file_path}")

        for name in dirs:
            if name.startswith('.'):
                continue

            dir_path = os.path.join(root, name)
            if dir_path not in valid_local_paths:
                shutil.rmtree(dir_path)
                stats['deleted'] += 1
                print(f"Deleted orphaned directory tree: {dir_path}")

    print(
        f"\nMirror Complete! Downloaded: {stats['downloaded']} | "
        f"Skipped: {stats['skipped']} | "
        f"Skipped pipeline (Drive): {stats['skipped_pipeline']} | "
        f"Preserved pipeline (local): {stats['preserved_pipeline']} | "
        f"Deleted: {stats['deleted']}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Mirror Google Drive delivery data locally. "
            "Full-folder mode recursively syncs one Drive root. "
            "CSV mode downloads selected channel files into "
            f"{CONVERSATIONS_ROOT}/<batch>/<session_id>/."
        ),
    )
    parser.add_argument(
        "folder_id",
        nargs='?',
        default="1D8isShidIb1hcZuCezV-Qe7EsmsmKBR1",
        help=(
            "Root Google Drive folder ID to mirror (default full-folder mode only)."
        ),
    )
    parser.add_argument(
        "--destination",
        default="drive_data",
        help="Local directory for full-folder mirror mode (default: drive_data).",
    )
    parser.add_argument(
        "--from-csv",
        nargs='?',
        const=DEFAULT_CSV,
        default=None,
        metavar="CSV",
        help=(
            f"Download channels listed in CSV (default: {DEFAULT_CSV}). "
            f"Requires --batch. Writes under {CONVERSATIONS_ROOT}/<batch>/."
        ),
    )
    parser.add_argument(
        "--batch",
        default=None,
        help="Batch folder name under Conversations/, e.g. delivery_batch_07152026.",
    )
    parser.add_argument(
        "--conversations",
        default=CONVERSATIONS_ROOT,
        help=f"Conversations root for CSV mode (default: {CONVERSATIONS_ROOT}).",
    )

    args = parser.parse_args()

    try:
        drive_svc = get_authenticated_drive_service()

        if args.from_csv is not None:
            if not args.batch:
                parser.error("--from-csv requires --batch")
            csv_path = Path(args.from_csv)
            if not csv_path.is_file():
                raise FileNotFoundError(f"CSV not found: {csv_path.resolve()}")
            rows = load_csv_download_rows(csv_path)
            if not rows:
                raise ValueError(f"No data rows in {csv_path}")
            sync_channels_from_csv(
                drive_svc,
                rows,
                batch=args.batch.strip(),
                conversations_root=Path(args.conversations),
            )
        else:
            if not os.path.exists(args.destination):
                os.makedirs(args.destination)
            mirror_folder_sync_recursive(drive_svc, args.folder_id, args.destination)
    except Exception as e:
        print(f"\nScript failed: {e}")
        raise SystemExit(1) from e
