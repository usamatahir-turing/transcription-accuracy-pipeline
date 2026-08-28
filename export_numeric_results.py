"""Export Batch-style numeric results from existing pipeline JSON artifacts.

Reads ``Conversations/<batch>/`` outputs (DNSMOS, DetER, overlap, optional WER)
without re-running scoring. Writes::

    numerical_results/audio_numerical_results_<batch>/
        numeric_results_inventory.csv
        dnsmos/individual/shard*.sessions.jsonl
        dnsmos_p835_individual.json
        individual_channel_numeric_results.csv
        session_numeric_results.csv

Usage
-----
    python export_numeric_results.py --batch delivery_batch_08082026
    python export_numeric_results.py --batch delivery_batch_08082026 --output-root numerical_results
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from workflow_common import add_scope_args, resolve_conversation_dirs

# Batch 8/9 reference ONNX fingerprint (sig_bak_ovr.onnx).
MODEL_SHA256 = (
    "269fbebdb513aa23cddfbb593542ecc540284a91849ac50516870e1ac78f6edd"
)

SCORING_CONFIG = {
    "algorithm": "annotated_natural_window_dnsmos_p835",
    "algorithm_version": 1,
    "model_sha256": MODEL_SHA256,
    "calibration": "official_non_personalized",
    "sample_rate": 16000,
    "window_sec": 9.01,
    "context_before_sec": 0.5,
    "clip_threshold": 0.9999,
}

CONFIG_ID = hashlib.sha256(
    json.dumps(SCORING_CONFIG, sort_keys=True).encode("utf-8"),
).hexdigest()[:16]

DEFAULT_OUTPUT_ROOT = Path("numerical_results")
DNSMOS_SUFFIX = "_dnsmos.json"
DETER_SUFFIX = "_deter.json"
SHARD_SIZE = 5

LANGUAGE_NAMES = {
    "AR": "Arabic",
    "DE": "German",
    "EN": "English",
    "ES": "Spanish",
    "FR": "French",
    "GR": "Greek",
    "IT": "Italian",
    "JA": "Japanese",
    "KO": "Korean",
    "PT": "Portuguese",
    "RU": "Russian",
}


def derive_language(session_id: str) -> str:
    parts = session_id.split("-")
    return parts[1] if len(parts) >= 2 else ""


def language_label(code: str) -> str:
    return LANGUAGE_NAMES.get(code.upper(), code.upper())


def batch_delivery_date(batch_name: str) -> str:
    m = re.search(r"(\d{8})$", batch_name)
    if not m:
        return ""
    raw = m.group(1)
    try:
        dt = datetime.strptime(raw, "%m%d%Y")
        return dt.strftime("%m/%d/%Y")
    except ValueError:
        return ""


def output_dir_name(batch_name: str) -> str:
    return f"audio_numerical_results_{batch_name}"


def _read_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _wav_duration_seconds(wav_path: Path) -> float | None:
    if not wav_path.is_file():
        return None
    try:
        import soundfile as sf

        info = sf.info(str(wav_path))
        if info.samplerate <= 0:
            return None
        return float(info.frames / info.samplerate)
    except Exception:  # noqa: BLE001
        return None


def _session_fingerprint(conv_dir: Path, session_id: str) -> str:
    parts = [session_id]
    for wav in sorted(conv_dir.glob("SPK*.wav")):
        stat = wav.stat()
        parts.append(f"{wav.name}:{stat.st_size}:{int(stat.st_mtime)}")
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return digest[:20]


def _export_window(window: dict) -> dict:
    return {
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
        "speech_peak": window.get("speech_peak"),
        "full_scale_samples": window.get("full_scale_samples"),
        "speech_samples": window.get("speech_samples"),
        "speech_sum_squares": window.get("speech_sum_squares"),
    }


def _export_channel(
    speaker_data: dict,
    *,
    conv_dir: Path,
) -> dict:
    dns = speaker_data.get("dnsmos") or {}
    diag = speaker_data.get("diagnostics") or {}
    speaker = speaker_data.get("speaker") or speaker_data.get("channel_id")
    wav_name = speaker_data.get("wav") or f"{speaker}.wav"
    wav_path = conv_dir / wav_name
    duration = _wav_duration_seconds(wav_path)
    windows = [_export_window(w) for w in (speaker_data.get("windows") or [])]
    return {
        "speaker": speaker,
        "status": "ok",
        "n_annotated_spans": diag.get("n_speech_segments"),
        "annotated_speech_seconds": dns.get("annotated_speech_seconds"),
        "audio_duration_seconds": duration,
        "n_windows": dns.get("n_windows", dns.get("n_hops")),
        "scored_speech_seconds": dns.get("scored_speech_seconds"),
        "sig": dns.get("sig"),
        "sig_std": dns.get("sig_std"),
        "bak": dns.get("bak"),
        "bak_std": dns.get("bak_std"),
        "ovrl": dns.get("ovrl"),
        "ovrl_std": dns.get("ovrl_std"),
        "speech_peak_dbfs": dns.get("speech_peak_dbfs"),
        "speech_rms_dbfs": dns.get("speech_rms_dbfs"),
        "full_scale_samples": dns.get("full_scale_samples"),
        "speech_samples": dns.get("speech_samples"),
        "full_scale_clipped_sample_ratio": dns.get(
            "full_scale_clipped_sample_ratio",
        ),
        "windows": windows,
    }


def build_session_record(conv_dir: Path, dnsmos_rollup: dict) -> dict | None:
    session_id = dnsmos_rollup.get("session_id", conv_dir.name)
    speakers = dnsmos_rollup.get("speakers") or {}
    if not speakers:
        return None

    channels = []
    annotated_total = 0.0
    n_windows_total = 0
    for speaker in sorted(speakers):
        ch = _export_channel(speakers[speaker], conv_dir=conv_dir)
        channels.append(ch)
        ann = ch.get("annotated_speech_seconds")
        if ann is not None:
            annotated_total += float(ann)
        nw = ch.get("n_windows")
        if nw is not None:
            n_windows_total += int(nw)

    lang = derive_language(session_id)
    return {
        "schema_version": 1,
        "tool": "DNSMOS P.835",
        "config_id": CONFIG_ID,
        "scoring_config": dict(SCORING_CONFIG),
        "input_fingerprint": _session_fingerprint(conv_dir, session_id),
        "session_id": session_id,
        "lang": lang,
        "n_channels": len(channels),
        "n_windows": n_windows_total,
        "annotated_speech_seconds": annotated_total,
        "channels": channels,
    }


def load_speaker_artifacts(conv_dir: Path, speaker: str) -> dict:
    dns = _read_json(conv_dir / f"{speaker}{DNSMOS_SUFFIX}") or {}
    deter = _read_json(conv_dir / f"{speaker}{DETER_SUFFIX}") or {}
    return {"speaker": speaker, "dnsmos": dns, "deter": deter}


def build_channel_row(
    *,
    batch_name: str,
    conv_dir: Path,
    session_id: str,
    speaker: str,
) -> dict:
    lang = derive_language(session_id)
    iso = lang.lower()
    artifacts = load_speaker_artifacts(conv_dir, speaker)
    dns_block = (artifacts["dnsmos"].get("dnsmos") or {})
    diag = artifacts["dnsmos"].get("diagnostics") or {}
    deter_block = (artifacts["deter"].get("deter") or {})
    wav_name = artifacts["dnsmos"].get("wav") or f"{speaker}.wav"
    seglst_name = f"{speaker}.seglst.json"
    wav_path = conv_dir / wav_name
    return {
        "batch": batch_name,
        "delivery_date": batch_delivery_date(batch_name),
        "session_id": session_id,
        "language": language_label(lang),
        "iso": iso,
        "channel": speaker,
        "wav_path": wav_path.as_posix(),
        "seglst_path": (conv_dir / seglst_name).as_posix(),
        "dnsmos_n_annotated_spans": diag.get("n_speech_segments"),
        "dnsmos_annotated_speech_seconds": dns_block.get(
            "annotated_speech_seconds",
        ),
        "dnsmos_audio_duration_seconds": _wav_duration_seconds(wav_path),
        "dnsmos_n_windows": dns_block.get("n_windows", dns_block.get("n_hops")),
        "dnsmos_scored_speech_seconds": dns_block.get("scored_speech_seconds"),
        "dnsmos_sig": dns_block.get("sig"),
        "dnsmos_sig_std": dns_block.get("sig_std"),
        "dnsmos_bak": dns_block.get("bak"),
        "dnsmos_bak_std": dns_block.get("bak_std"),
        "dnsmos_ovrl": dns_block.get("ovrl"),
        "dnsmos_ovrl_std": dns_block.get("ovrl_std"),
        "dnsmos_speech_peak_dbfs": dns_block.get("speech_peak_dbfs"),
        "dnsmos_speech_rms_dbfs": dns_block.get("speech_rms_dbfs"),
        "dnsmos_full_scale_samples": dns_block.get("full_scale_samples"),
        "dnsmos_speech_samples": dns_block.get("speech_samples"),
        "dnsmos_full_scale_clipped_sample_ratio": dns_block.get(
            "full_scale_clipped_sample_ratio",
        ),
        "dnsmos_pass": dns_block.get("pass"),
        "deter": deter_block.get("error_rate"),
        "deter_scored_speaker_time_seconds": deter_block.get("scored_speech_s"),
        "deter_missed_speaker_time_seconds": deter_block.get("missed_s"),
        "deter_false_alarm_speaker_time_seconds": deter_block.get("false_alarm_s"),
        "deter_speaker_error_time_seconds": deter_block.get("confusion_s"),
        "deter_pass": deter_block.get("pass"),
    }


def build_session_row(
    *,
    batch_name: str,
    conv_dir: Path,
    session_id: str,
    dnsmos_rollup: dict,
) -> dict:
    lang = derive_language(session_id)
    overlap = _read_json(conv_dir / "overlap_ratio.json") or {}
    deter = _read_json(conv_dir / "deter.json") or {}
    conv_dns = dnsmos_rollup.get("conversation") or {}
    conv_overlap = overlap.get("conversation") or {}
    conv_deter = deter.get("conversation") or {}
    speakers = dnsmos_rollup.get("speakers") or {}

    sigs = [
        (s.get("dnsmos") or {}).get("sig")
        for s in speakers.values()
        if (s.get("dnsmos") or {}).get("sig") is not None
    ]
    n_fail_sig = sum(
        1
        for s in speakers.values()
        if not (s.get("dnsmos") or {}).get("pass", True)
    )

    return {
        "batch": batch_name,
        "delivery_date": batch_delivery_date(batch_name),
        "session_id": session_id,
        "language": language_label(lang),
        "iso": lang.lower(),
        "n_speakers": conv_dns.get("n_speakers", len(speakers)),
        "audio_duration_seconds": conv_overlap.get("total_audio_s"),
        "speaking_time_union_seconds": conv_overlap.get("speech_s"),
        "overlap_seconds": conv_overlap.get("overlap_s"),
        "overlap_ratio": conv_overlap.get("overlap_ratio"),
        "n_speech_segments": conv_overlap.get("n_speech_segments"),
        "mean_deter": conv_deter.get("mean_deter"),
        "mean_deter_pct": conv_deter.get("mean_deter_pct"),
        "deter_pass": conv_deter.get("pass"),
        "channels_dnsmos_sig_below_3": n_fail_sig,
        "minimum_dnsmos_sig": min(sigs) if sigs else None,
        "mean_dnsmos_sig": conv_dns.get("mean_sig"),
        "mean_dnsmos_bak": conv_dns.get("mean_bak"),
        "mean_dnsmos_ovrl": conv_dns.get("mean_ovrl"),
        "dnsmos_conversation_pass": conv_dns.get("pass"),
    }


CHANNEL_CSV_COLUMNS = [
    "batch",
    "delivery_date",
    "session_id",
    "language",
    "iso",
    "channel",
    "wav_path",
    "seglst_path",
    "dnsmos_n_annotated_spans",
    "dnsmos_annotated_speech_seconds",
    "dnsmos_audio_duration_seconds",
    "dnsmos_n_windows",
    "dnsmos_scored_speech_seconds",
    "dnsmos_sig",
    "dnsmos_sig_std",
    "dnsmos_bak",
    "dnsmos_bak_std",
    "dnsmos_ovrl",
    "dnsmos_ovrl_std",
    "dnsmos_speech_peak_dbfs",
    "dnsmos_speech_rms_dbfs",
    "dnsmos_full_scale_samples",
    "dnsmos_speech_samples",
    "dnsmos_full_scale_clipped_sample_ratio",
    "dnsmos_pass",
    "deter",
    "deter_scored_speaker_time_seconds",
    "deter_missed_speaker_time_seconds",
    "deter_false_alarm_speaker_time_seconds",
    "deter_speaker_error_time_seconds",
    "deter_pass",
]

SESSION_CSV_COLUMNS = [
    "batch",
    "delivery_date",
    "session_id",
    "language",
    "iso",
    "n_speakers",
    "audio_duration_seconds",
    "speaking_time_union_seconds",
    "overlap_seconds",
    "overlap_ratio",
    "n_speech_segments",
    "mean_deter",
    "mean_deter_pct",
    "deter_pass",
    "channels_dnsmos_sig_below_3",
    "minimum_dnsmos_sig",
    "mean_dnsmos_sig",
    "mean_dnsmos_bak",
    "mean_dnsmos_ovrl",
    "dnsmos_conversation_pass",
]

INVENTORY_ROWS = [
    ("numeric_results_inventory.csv", "csv", "1", "Manifest of exported artifacts"),
    (
        "dnsmos/individual/shard*.sessions.jsonl",
        "jsonl",
        "varies",
        "Per-session DNSMOS P.835 results with channel and window detail",
    ),
    (
        "dnsmos_p835_individual.json",
        "json",
        "nested",
        "Consolidated per-session DNSMOS export for the batch",
    ),
    (
        "individual_channel_numeric_results.csv",
        "csv",
        "varies",
        "Joined per-channel DNSMOS and DetER metrics",
    ),
    (
        "session_numeric_results.csv",
        "csv",
        "varies",
        "Session-level overlap, DetER, and DNSMOS aggregates",
    ),
]


def _write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _write_shards(
    out_dnsmos_dir: Path,
    sessions: list[dict],
    *,
    shard_size: int,
) -> int:
    out_dnsmos_dir.mkdir(parents=True, exist_ok=True)
    n_shards = 0
    for i in range(0, len(sessions), shard_size):
        shard_sessions = sessions[i : i + shard_size]
        shard_path = out_dnsmos_dir / f"shard{n_shards}.sessions.jsonl"
        with shard_path.open("w", encoding="utf-8") as fh:
            for session in shard_sessions:
                fh.write(json.dumps(session, ensure_ascii=False))
                fh.write("\n")
        n_shards += 1
    return n_shards


def export_batch(
    *,
    conversations_root: Path,
    batch_name: str,
    output_root: Path,
    shard_size: int = SHARD_SIZE,
) -> Path:
    conv_dirs = resolve_conversation_dirs(conversations_root, batch_name, None)
    out_dir = output_root / output_dir_name(batch_name)

    sessions: list[dict] = []
    channel_rows: list[dict] = []
    session_rows: list[dict] = []

    for conv_dir in conv_dirs:
        session_id = conv_dir.name
        dnsmos_rollup = _read_json(conv_dir / "dnsmos.json")
        if not dnsmos_rollup or not dnsmos_rollup.get("speakers"):
            print(f"  SKIP {session_id}: missing dnsmos.json rollup")
            continue

        session_record = build_session_record(conv_dir, dnsmos_rollup)
        if session_record is None:
            print(f"  SKIP {session_id}: no DNSMOS speakers")
            continue
        sessions.append(session_record)

        session_rows.append(
            build_session_row(
                batch_name=batch_name,
                conv_dir=conv_dir,
                session_id=session_id,
                dnsmos_rollup=dnsmos_rollup,
            ),
        )

        for speaker in sorted(dnsmos_rollup["speakers"]):
            channel_rows.append(
                build_channel_row(
                    batch_name=batch_name,
                    conv_dir=conv_dir,
                    session_id=session_id,
                    speaker=speaker,
                ),
            )

        print(
            f"  OK   {session_id}  channels={session_record['n_channels']}  "
            f"windows={session_record['n_windows']}",
        )

    if not sessions:
        raise RuntimeError(f"No DNSMOS rollups found under batch {batch_name}")

    dnsmos_dir = out_dir / "dnsmos" / "individual"
    n_shards = _write_shards(dnsmos_dir, sessions, shard_size=shard_size)
    _write_json(out_dir / "dnsmos_p835_individual.json", sessions)
    _write_csv(
        out_dir / "individual_channel_numeric_results.csv",
        CHANNEL_CSV_COLUMNS,
        channel_rows,
    )
    _write_csv(
        out_dir / "session_numeric_results.csv",
        SESSION_CSV_COLUMNS,
        session_rows,
    )

    inventory = [
        {
            "filename": name,
            "format": fmt,
            "records": str(
                len(sessions) if "dnsmos_p835" in name
                else len(channel_rows) if "individual_channel" in name
                else len(session_rows) if "session_numeric" in name
                else n_shards if "shard" in name
                else records,
            ),
            "description": desc,
        }
        for name, fmt, records, desc in INVENTORY_ROWS
    ]
    _write_csv(
        out_dir / "numeric_results_inventory.csv",
        ["filename", "format", "records", "description"],
        inventory,
    )

    print(
        f"\nWrote {out_dir}\n"
        f"  sessions={len(sessions)}  channels={len(channel_rows)}  "
        f"shards={n_shards}",
    )
    return out_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=False)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=f"Parent folder for exports (default: {DEFAULT_OUTPUT_ROOT}).",
    )
    parser.add_argument(
        "--shard-size",
        type=int,
        default=SHARD_SIZE,
        help="Sessions per dnsmos shard JSONL file (default: 5).",
    )
    args = parser.parse_args(argv)

    if not args.batch:
        print("ERROR: --batch is required (exports one batch folder at a time).")
        return 1

    root = Path(args.conversations)
    output_root = args.output_root.resolve()
    try:
        export_batch(
            conversations_root=root,
            batch_name=args.batch,
            output_root=output_root,
            shard_size=max(1, args.shard_size),
        )
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
