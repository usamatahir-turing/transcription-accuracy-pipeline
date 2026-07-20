"""Export a lean per-channel DNSMOS CSV from ``*_dnsmos.json`` files.

Columns: batch, session_id, file_name, sig, bak, ovrl, pass, speech_min, peak_dbfs

Usage
-----
    python -m audio_quality_pipeline.export_dnsmos_csv
    python -m audio_quality_pipeline.export_dnsmos_csv --batch delivery_batch_07142026
    python -m audio_quality_pipeline.export_dnsmos_csv --conversation NV-KO-SS15-CONVO34
    python -m audio_quality_pipeline.export_dnsmos_csv -o audio_quality_pipeline/reports/dnsmos_channels.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from workflow_common import add_scope_args, resolve_conversation_dirs

DNSMOS_JSON_SUFFIX = "_dnsmos.json"
DEFAULT_OUT = Path(__file__).resolve().parent / "reports" / "dnsmos_channels.csv"

COLUMNS = (
    "batch",
    "session_id",
    "file_name",
    "sig",
    "bak",
    "ovrl",
    "pass",
    "speech_min",
    "peak_dbfs",
)


def row_from_dnsmos_json(path: Path, batch: str) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  WARN skip {path}: {exc}")
        return None

    dnsmos = data.get("dnsmos") or {}
    diag = data.get("diagnostics") or {}
    file_name = data.get("wav")
    if not file_name:
        channel_id = data.get("channel_id") or path.name.removesuffix(DNSMOS_JSON_SUFFIX)
        file_name = f"{channel_id}.wav"
    return {
        "batch": batch,
        "session_id": data.get("session_id") or path.parent.name,
        "file_name": file_name,
        "sig": dnsmos.get("sig"),
        "bak": dnsmos.get("bak"),
        "ovrl": dnsmos.get("ovrl"),
        "pass": dnsmos.get("pass"),
        "speech_min": diag.get("speech_min"),
        "peak_dbfs": diag.get("peak_dbfs"),
    }


def collect_rows(session_dirs: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for session_dir in session_dirs:
        batch = session_dir.parent.name
        for path in sorted(session_dir.glob(f"*{DNSMOS_JSON_SUFFIX}")):
            row = row_from_dnsmos_json(path, batch)
            if row is not None:
                rows.append(row)
    return rows


def write_csv(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


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
    # Sort by batch, session, file_name for stable browsing.
    rows.sort(
        key=lambda r: (
            r["batch"] or "",
            r["session_id"] or "",
            r["file_name"] or "",
        )
    )

    out_path = Path(args.output)
    write_csv(rows, out_path)
    n_fail = sum(1 for r in rows if r.get("pass") is False)
    print(
        f"Wrote {len(rows)} channel row(s) to {out_path} "
        f"({n_fail} with pass=False)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
