"""Export region-level DNSMOS windows from ``*_dnsmos.json`` to CSV.

One row per scored window in each speaker JSON. Files without a ``windows``
array are skipped (legacy aggregate-only outputs).

Usage
-----
    python -m audio_quality_pipeline.dnsmos_report_gen
    python -m audio_quality_pipeline.dnsmos_report_gen --batch delivery_batch_08082026
    python -m audio_quality_pipeline.dnsmos_report_gen --conversation NV-GR-SS13-CONVO22
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from workflow_common import add_scope_args, resolve_conversation_dirs

DNSMOS_JSON_SUFFIX = "_dnsmos.json"
DEFAULT_OUT = Path(__file__).resolve().parent / "reports" / "dnsmos_data.csv"

COLUMNS = (
    "batch",
    "session_id",
    "speaker",
    "channel_id",
    "window_idx",
    "start_sec",
    "end_sec",
    "sig",
    "sig_rank",
    "bak",
    "ovrl",
    "sig_raw",
    "bak_raw",
    "ovrl_raw",
    "speech_weight_sec",
    "speech_in_window_sec",
    "channel_sig",
    "channel_bak",
    "channel_ovrl",
    "channel_sig_std",
    "channel_bak_std",
    "channel_ovrl_std",
    "channel_n_windows",
    "annotated_speech_seconds",
    "scored_speech_seconds",
    "speech_peak_dbfs",
    "speech_rms_dbfs",
    "dnsmos_pass",
)


def _channel_fields(dnsmos: dict) -> dict:
    return {
        "channel_sig": dnsmos.get("sig"),
        "channel_bak": dnsmos.get("bak"),
        "channel_ovrl": dnsmos.get("ovrl"),
        "channel_sig_std": dnsmos.get("sig_std"),
        "channel_bak_std": dnsmos.get("bak_std"),
        "channel_ovrl_std": dnsmos.get("ovrl_std"),
        "channel_n_windows": dnsmos.get("n_windows", dnsmos.get("n_hops")),
        "annotated_speech_seconds": dnsmos.get("annotated_speech_seconds"),
        "scored_speech_seconds": dnsmos.get("scored_speech_seconds"),
        "speech_peak_dbfs": dnsmos.get("speech_peak_dbfs"),
        "speech_rms_dbfs": dnsmos.get("speech_rms_dbfs"),
        "dnsmos_pass": dnsmos.get("pass"),
    }


def _assign_sig_ranks(rows: list[dict]) -> None:
    """Set ``sig_rank`` per channel (1 = lowest SIG)."""
    by_channel: dict[tuple[str, str, str], list[dict]] = {}
    for row in rows:
        key = (row["batch"], row["session_id"], row["speaker"])
        by_channel.setdefault(key, []).append(row)

    for channel_rows in by_channel.values():
        ranked = sorted(
            channel_rows,
            key=lambda r: (
                r["sig"] if r["sig"] is not None else float("inf"),
                r["start_sec"] if r["start_sec"] is not None else 0.0,
                r["window_idx"],
            ),
        )
        for rank, row in enumerate(ranked, start=1):
            row["sig_rank"] = rank


def collect_window_rows(session_dirs: list[Path]) -> tuple[list[dict], int, int]:
    rows: list[dict] = []
    n_files = 0
    n_skipped_no_windows = 0

    for session_dir in session_dirs:
        batch = session_dir.parent.name
        session_id = session_dir.name

        for path in sorted(session_dir.glob(f"*{DNSMOS_JSON_SUFFIX}")):
            n_files += 1
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                print(f"  WARN skip {path}: {exc}")
                continue

            windows = data.get("windows")
            if not windows:
                n_skipped_no_windows += 1
                speaker = data.get("speaker") or path.name[: -len(DNSMOS_JSON_SUFFIX)]
                print(f"  SKIP {session_id}/{speaker}: no windows[] in {path.name}")
                continue

            dnsmos = data.get("dnsmos") or {}
            channel = _channel_fields(dnsmos)
            speaker = data.get("speaker") or path.name[: -len(DNSMOS_JSON_SUFFIX)]
            channel_id = data.get("channel_id") or speaker
            sid = data.get("session_id") or session_id

            for window_idx, window in enumerate(windows):
                rows.append({
                    "batch": batch,
                    "session_id": sid,
                    "speaker": speaker,
                    "channel_id": channel_id,
                    "window_idx": window_idx,
                    "start_sec": window.get("start_sec"),
                    "end_sec": window.get("end_sec"),
                    "sig": window.get("sig"),
                    "bak": window.get("bak"),
                    "ovrl": window.get("ovrl"),
                    "sig_raw": window.get("sig_raw"),
                    "bak_raw": window.get("bak_raw"),
                    "ovrl_raw": window.get("ovrl_raw"),
                    "speech_weight_sec": window.get("speech_weight_sec"),
                    "speech_in_window_sec": window.get("speech_in_window_sec"),
                    **channel,
                })

    _assign_sig_ranks(rows)
    rows.sort(key=lambda r: (
        r["batch"],
        r["session_id"],
        r["speaker"],
        r["window_idx"],
        r["start_sec"] if r["start_sec"] is not None else 0.0,
    ))
    return rows, n_files, n_skipped_no_windows


def write_csv(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows({k: r.get(k) for k in COLUMNS} for r in rows)


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

    out_path = args.output.resolve()
    if out_path.exists() and not args.overwrite:
        print(f"SKIP: {out_path} exists (use --overwrite to replace)")
        return 0

    root = Path(args.conversations)
    try:
        session_dirs = resolve_conversation_dirs(root, args.batch, args.conversation)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit > 0:
        session_dirs = session_dirs[: args.limit]

    rows, n_files, n_skipped = collect_window_rows(session_dirs)
    if not rows:
        print(
            f"No window rows found ({n_files} *_dnsmos.json scanned, "
            f"{n_skipped} without windows[])."
        )
        return 1

    write_csv(rows, out_path)
    n_sessions = len({(r["batch"], r["session_id"]) for r in rows})
    n_speakers = len({(r["batch"], r["session_id"], r["speaker"]) for r in rows})
    print(
        f"Wrote {len(rows)} window row(s) from {n_speakers} speaker(s) "
        f"in {n_sessions} conversation(s) to {out_path}"
    )
    if n_skipped:
        print(f"  ({n_skipped} file(s) skipped: no windows[])")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
