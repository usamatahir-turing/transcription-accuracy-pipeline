"""DNSMOS P.835 pipeline: Batch 8/9 annotated natural-window scoring.

Default (matches ``batch8and9review`` Batch 8/9 QA):
  - Algorithm: annotated natural windows on seglst speech (0.5 s context)
  - Polyfit: official non-personalized
  - Aggregation: speech-in-window weighted mean

Per speaker writes ``{speaker}_dnsmos.json`` with channel aggregates and all
scored ``windows`` (chronological); per conversation writes ``dnsmos.json``.

Usage
-----
    python -m audio_quality_pipeline.dnsmos_calculation --conversation NV-GR-SS13-CONVO22
    python -m audio_quality_pipeline.dnsmos_calculation --batch delivery_batch_08082026 --overwrite

    # Legacy Worst-100 calibration:
    python -m audio_quality_pipeline.dnsmos_calculation --window speech_timeline --personalized --overwrite
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from audio_quality_pipeline.channel_pairs import iter_wav_seglst_pairs
from audio_quality_pipeline.dnsmos_p835 import (
    SIG_WARN_MIN,
    score_annotated_natural_window,
    score_audio,
    session_device,
)
from audio_quality_pipeline.natural_window_dnsmos import (
    CONTEXT_BEFORE_SEC,
    natural_window_starts,
    speech_weight_sec,
    _speech_seconds,
    CLIP_THRESHOLD,
)
from audio_quality_pipeline.speech_windows import (
    channel_speech_level_stats,
    extract_speech_audio,
    extract_speech_timeline_audio,
    rms_dbfs,
    window_speech_level_stats,
)
from diarization_pipeline.seglst_to_rttm import load_speech_seglst_rows
from diarization_pipeline.common import channel_id_from_path, speaker_output_name
from workflow_common import add_scope_args, resolve_conversation_dirs

DNSMOS_JSON_SUFFIX = "_dnsmos.json"
DNSMOS_ROLLUP = "dnsmos.json"

WINDOW_NATURAL = "natural_window"
WINDOW_SPEECH_TIMELINE = "speech_timeline"
WINDOW_SPEECH_CONCAT = "speech_concat"
WINDOW_FULL = "full"

SPEECH_MASK_LABELS = {
    WINDOW_NATURAL: (
        "annotated natural-window seglst (0.5 s context; NSV-only excluded)"
    ),
    WINDOW_SPEECH_TIMELINE: (
        "speech seglst on full timeline (non-speech zeroed; NSV-only excluded)"
    ),
    WINDOW_SPEECH_CONCAT: "speech-only seglst concat (NSV-only excluded)",
    WINDOW_FULL: "full channel WAV (no seglst mask)",
}


def dnsmos_json_path_for_speaker(session_dir: Path, speaker: str) -> Path:
    return session_dir / f"{speaker}{DNSMOS_JSON_SUFFIX}"


def _speech_rms_dbfs(
    audio,
    sample_rate: int,
    spans: list[tuple[float, float]] | None,
) -> float | None:
    chunks = _speech_chunks(audio, sample_rate, spans)
    if chunks is None:
        return rms_dbfs(np.asarray(audio, dtype=np.float32))
    if not chunks:
        return None
    import numpy as np

    return rms_dbfs(np.concatenate(chunks))


def _speech_peak_dbfs(
    audio,
    sample_rate: int,
    spans: list[tuple[float, float]] | None,
) -> float | None:
    stats = channel_speech_level_stats(
        audio, sample_rate, spans, clip_threshold=CLIP_THRESHOLD,
    )
    return stats["speech_peak_dbfs"]


def _speech_chunks(
    audio,
    sample_rate: int,
    spans: list[tuple[float, float]] | None,
):
    if spans is None:
        return None
    import numpy as np

    chunks: list[np.ndarray] = []
    for start, end in spans:
        i0 = max(0, int(round(start * sample_rate)))
        i1 = min(len(audio), int(round(end * sample_rate)))
        if i1 > i0:
            chunks.append(np.asarray(audio[i0:i1], dtype=np.float32))
    return chunks


def _enrich_window_speech_weights(
    windows: list[dict],
    *,
    window: str,
    spans: list[tuple[float, float]] | None,
    speech_s: float,
) -> list[dict]:
    if window == WINDOW_SPEECH_CONCAT:
        for row in windows:
            wt = max(0.0, min(9.01, speech_s - row["start_sec"]))
            wt = round(wt, 6)
            row["speech_weight_sec"] = wt
            row["speech_in_window_sec"] = wt
    elif spans and window in (WINDOW_SPEECH_TIMELINE, WINDOW_FULL):
        for row in windows:
            wt = round(speech_weight_sec(spans, row["start_sec"]), 6)
            row["speech_weight_sec"] = wt
            row["speech_in_window_sec"] = wt
    return windows


def _enrich_window_speech_levels(
    windows: list[dict],
    *,
    audio,
    sample_rate: int,
    window: str,
    spans: list[tuple[float, float]] | None,
) -> list[dict]:
    """Add per-window speech peak / full-scale clipping (Batch 8/9 field names)."""
    speech_only = window == WINDOW_SPEECH_CONCAT
    natural = window == WINDOW_NATURAL
    for row in windows:
        start_sec = float(row["start_sec"])
        end_sec = float(row["end_sec"])
        weight = row.get("speech_weight_sec")
        if spans and not speech_only and weight is not None:
            row["speech_in_window_sec"] = round(
                _speech_seconds(spans, start_sec, end_sec), 6,
            )
        clip_start = start_sec
        if natural and weight is not None:
            clip_start = start_sec + CONTEXT_BEFORE_SEC
        stats = window_speech_level_stats(
            audio,
            sample_rate,
            clip_start,
            end_sec,
            spans if not speech_only else None,
            clip_threshold=CLIP_THRESHOLD,
            speech_only_slice=speech_only,
            max_speech_sec=float(weight) if weight is not None else None,
        )
        row["speech_peak"] = stats["speech_peak"]
        row["full_scale_samples"] = stats["full_scale_samples"]
        row["speech_samples"] = stats["speech_samples"]
        row["speech_sum_squares"] = stats["speech_sum_squares"]
    return windows


def _windows_for_json(windows: list[dict]) -> list[dict]:
    """All scored windows, chronological (reference ``windows[]`` order)."""
    return sorted(windows, key=lambda w: (w["start_sec"], w["end_sec"]))


def _load_window(wav_path: Path, seglst_path: Path, window: str) -> dict:
    rows = load_speech_seglst_rows(seglst_path)
    spans = [(float(r["start"]), float(r["end"])) for r in rows]
    if window == WINDOW_NATURAL:
        starts = natural_window_starts(seglst_path)
        from audio_quality_pipeline.speech_windows import load_mono_wav

        audio, sr = load_mono_wav(wav_path)
        speech_s = sum(e - s for s, e in spans)
        weights = [speech_weight_sec(spans, st) for st in starts]
        return {
            "audio": audio,
            "sample_rate": sr,
            "speech_s": round(speech_s, 3),
            "speech_min": round(speech_s / 60.0, 3),
            "peak_dbfs": _speech_peak_dbfs(audio, sr, spans),
            "speech_rms_dbfs": _speech_rms_dbfs(audio, sr, spans),
            "n_speech_segments": len(rows),
            "n_samples": int(sum(max(0, int(round((e - s) * sr))) for s, e in spans)),
            "window_starts": starts,
            "window_weights": weights,
            "spans": spans,
            "mode": WINDOW_NATURAL,
        }
    if window == WINDOW_SPEECH_TIMELINE:
        win = extract_speech_timeline_audio(wav_path, seglst_path)
        from audio_quality_pipeline.speech_windows import load_mono_wav

        audio, sr = load_mono_wav(wav_path)
        win["spans"] = spans
        win["speech_rms_dbfs"] = _speech_rms_dbfs(audio, sr, spans)
        return win
    if window == WINDOW_SPEECH_CONCAT:
        win = extract_speech_audio(wav_path, seglst_path)
        win["spans"] = spans
        win["speech_rms_dbfs"] = rms_dbfs(win["audio"])
        return win
    if window == WINDOW_FULL:
        from audio_quality_pipeline.speech_windows import load_mono_wav

        audio, sr = load_mono_wav(wav_path)
        speech = extract_speech_audio(wav_path, seglst_path)
        return {
            "audio": audio,
            "sample_rate": sr,
            "speech_s": speech["speech_s"],
            "speech_min": speech["speech_min"],
            "peak_dbfs": _speech_peak_dbfs(audio, sr, spans),
            "speech_rms_dbfs": _speech_rms_dbfs(audio, sr, spans),
            "n_speech_segments": speech["n_speech_segments"],
            "n_samples": speech["n_samples"],
            "file_s": round(len(audio) / sr, 3) if sr else 0.0,
            "spans": spans,
            "mode": WINDOW_FULL,
        }
    raise ValueError(f"unknown window mode: {window}")


def score_speaker(
    wav_path: Path,
    seglst_path: Path,
    *,
    window: str = WINDOW_NATURAL,
    personalized: bool = False,
    session_id: str | None = None,
) -> dict | None:
    channel_id = channel_id_from_path(wav_path)
    speaker = speaker_output_name(channel_id)
    if not wav_path.is_file():
        print(f"    SKIP {speaker}: no {wav_path.name}")
        return None
    if not seglst_path.is_file():
        print(f"    SKIP {speaker}: no {seglst_path.name}")
        return None

    win = _load_window(wav_path, seglst_path, window)
    if win["n_samples"] < 1600:
        print(f"    WARN {speaker}: too little speech ({win['speech_s']}s)")
        return None

    if window == WINDOW_NATURAL:
        scores = score_annotated_natural_window(
            win["audio"],
            win["sample_rate"],
            win["window_starts"],
            win["window_weights"],
            personalized=personalized,
        )
    else:
        scores = score_audio(
            win["audio"], win["sample_rate"], personalized=personalized)

    flags: list[str] = []
    if not scores["pass"]:
        flags.append("sig_below_3.0")

    windows = list(scores.get("windows") or [])
    if window != WINDOW_NATURAL:
        windows = _enrich_window_speech_weights(
            windows,
            window=window,
            spans=win.get("spans"),
            speech_s=float(win["speech_s"]),
        )
    windows = _enrich_window_speech_levels(
        windows,
        audio=win["audio"],
        sample_rate=int(win["sample_rate"]),
        window=window,
        spans=win.get("spans"),
    )

    ch_levels = channel_speech_level_stats(
        win["audio"],
        int(win["sample_rate"]),
        win.get("spans"),
        clip_threshold=CLIP_THRESHOLD,
    )

    diagnostics = {
        "speech_s": win["speech_s"],
        "speech_min": win["speech_min"],
        "peak_dbfs": ch_levels["speech_peak_dbfs"],
        "speech_rms_dbfs": win.get("speech_rms_dbfs"),
        "full_scale_samples": ch_levels["full_scale_samples"],
        "speech_samples": ch_levels["speech_samples"],
        "full_scale_clipped_sample_ratio": ch_levels[
            "full_scale_clipped_sample_ratio"
        ],
        "n_speech_segments": win["n_speech_segments"],
        "sample_rate": win["sample_rate"],
    }
    if "file_s" in win:
        diagnostics["file_s"] = win["file_s"]
    if scores.get("n_windows") is not None:
        diagnostics["n_windows"] = scores["n_windows"]

    dnsmos = {
        "sig": scores["sig"],
        "bak": scores["bak"],
        "ovrl": scores["ovrl"],
        "sig_raw": scores["sig_raw"],
        "bak_raw": scores["bak_raw"],
        "ovrl_raw": scores["ovrl_raw"],
        "sig_std": scores.get("sig_std"),
        "bak_std": scores.get("bak_std"),
        "ovrl_std": scores.get("ovrl_std"),
        "n_windows": scores.get("n_windows", scores["n_hops"]),
        "n_hops": scores["n_hops"],
        "annotated_speech_seconds": win["speech_s"],
        "scored_speech_seconds": scores.get(
            "scored_speech_seconds",
            scores.get("n_windows", scores["n_hops"]) * 9.01,
        ),
        "speech_peak_dbfs": ch_levels["speech_peak_dbfs"],
        "speech_rms_dbfs": win.get("speech_rms_dbfs"),
        "full_scale_samples": ch_levels["full_scale_samples"],
        "speech_samples": ch_levels["speech_samples"],
        "full_scale_clipped_sample_ratio": ch_levels[
            "full_scale_clipped_sample_ratio"
        ],
        "pass": scores["pass"],
        "threshold_sig": scores["threshold_sig"],
        "personalized": scores["personalized"],
    }

    return {
        "session_id": session_id or wav_path.parent.name,
        "speaker": speaker,
        "channel_id": channel_id,
        "wav": wav_path.name,
        "dnsmos": dnsmos,
        "windows": _windows_for_json(windows),
        "diagnostics": diagnostics,
        "flags": flags,
        "method": {
            "metric": "DNSMOS_P835",
            "algorithm": (
                "annotated_natural_window_dnsmos_p835"
                if window == WINDOW_NATURAL
                else "sliding_window_dnsmos_p835"
            ),
            "speech_mask": SPEECH_MASK_LABELS[window],
            "window": window,
            "personalized": personalized,
            "calibration": (
                "official_non_personalized"
                if not personalized
                else "personalized"
            ),
            "model": "sig_bak_ovr.onnx",
            "device": scores["device"],
            "seglst": seglst_path.as_posix(),
        },
    }


def process_conversation(
    session_dir: Path,
    *,
    overwrite: bool,
    window: str,
    personalized: bool,
    seglst_root: Path | None,
) -> dict | None:
    pairs = iter_wav_seglst_pairs(session_dir, seglst_root=seglst_root)
    if not pairs:
        return None

    speakers_out: dict[str, dict] = {}
    for wav_path, seglst_path in pairs:
        channel_id = channel_id_from_path(wav_path)
        speaker = speaker_output_name(channel_id)
        out_path = dnsmos_json_path_for_speaker(session_dir, speaker)
        if out_path.exists() and not overwrite:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
            speakers_out[speaker] = existing
            print(f"    SKIP {speaker}: {out_path.name} exists")
            continue
        try:
            result = score_speaker(
                wav_path,
                seglst_path,
                window=window,
                personalized=personalized,
                session_id=session_dir.name,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"    FAIL {speaker}: {exc}")
            continue
        if result is None:
            continue
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        speakers_out[speaker] = result
        d = result["dnsmos"]
        verdict = "PASS" if d["pass"] else "FAIL"
        print(
            f"    OK   {session_dir.name}/{speaker}  "
            f"SIG={d['sig']:.3f}  BAK={d['bak']:.3f}  OVRL={d['ovrl']:.3f}  {verdict}"
        )

    if not speakers_out:
        return None

    sigs = [s["dnsmos"]["sig"] for s in speakers_out.values()]
    baks = [s["dnsmos"]["bak"] for s in speakers_out.values()]
    ovrls = [s["dnsmos"]["ovrl"] for s in speakers_out.values()]
    n_fail = sum(1 for s in speakers_out.values() if not s["dnsmos"]["pass"])

    method = {
        "metric": "DNSMOS_P835",
        "description": (
            "DNSMOS P.835 SIG/BAK/OVRL on annotated natural windows with "
            f"{'personalized' if personalized else 'official non-personalized'} "
            f"polyfit (SIG > {SIG_WARN_MIN} warning threshold)."
        ),
        "speech_mask": SPEECH_MASK_LABELS[window],
        "window": window,
        "personalized": personalized,
        "threshold_sig": SIG_WARN_MIN,
        "device": session_device(),
    }
    if seglst_root is not None:
        method["seglst_root"] = str(seglst_root)

    return {
        "session_id": session_dir.name,
        "method": method,
        "conversation": {
            "n_speakers": len(speakers_out),
            "n_fail_sig": n_fail,
            "mean_sig": round(sum(sigs) / len(sigs), 6),
            "mean_bak": round(sum(baks) / len(baks), 6),
            "mean_ovrl": round(sum(ovrls) / len(ovrls), 6),
            "min_sig": round(min(sigs), 6),
            "pass": n_fail == 0,
        },
        "speakers": speakers_out,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=False)
    parser.add_argument(
        "--window",
        choices=(
            WINDOW_NATURAL,
            WINDOW_SPEECH_TIMELINE,
            WINDOW_SPEECH_CONCAT,
            WINDOW_FULL,
        ),
        default=WINDOW_NATURAL,
        help="Audio window for DNSMOS (default: natural_window / Batch 8/9 QA).",
    )
    parser.add_argument(
        "--personalized",
        action="store_true",
        help="Use personalized polyfit (legacy Worst-100 calibration).",
    )
    parser.add_argument(
        "--non-personalized",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--seglst-root",
        type=Path,
        default=None,
        help=(
            "Optional root with the same <batch>/<conversation>/ layout that "
            "holds *.seglst.json (e.g. Conversations). WAV root is still "
            "--conversations. Channels without a matching seglst are skipped."
        ),
    )
    args = parser.parse_args(argv)
    personalized = args.personalized and not args.non_personalized
    seglst_root = args.seglst_root.resolve() if args.seglst_root else None
    if seglst_root is not None and not seglst_root.is_dir():
        print(f"ERROR: seglst root not found: {seglst_root}")
        return 1

    root = Path(args.conversations)
    try:
        session_dirs = resolve_conversation_dirs(root, args.batch, args.conversation)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit > 0:
        session_dirs = session_dirs[: args.limit]

    n_done = n_skipped = n_empty = n_fail = 0
    for session_dir in session_dirs:
        out_path = session_dir / DNSMOS_ROLLUP
        if out_path.exists() and not args.overwrite:
            n_skipped += 1
            print(f"  SKIP {session_dir.name}: {DNSMOS_ROLLUP} exists")
            continue
        try:
            result = process_conversation(
                session_dir,
                overwrite=args.overwrite,
                window=args.window,
                personalized=personalized,
                seglst_root=seglst_root,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {session_dir.name}: {exc}")
            n_fail += 1
            continue
        if result is None:
            n_empty += 1
            continue
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        c = result["conversation"]
        verdict = "PASS" if c["pass"] else "FAIL"
        print(
            f"  OK   {session_dir.name}  mean SIG={c['mean_sig']:.3f}  "
            f"fail_sig={c['n_fail_sig']}/{c['n_speakers']}  {verdict}"
        )
        n_done += 1

    print(
        f"\nDone. {n_done} conversation(s) scored, {n_skipped} skipped "
        f"({DNSMOS_ROLLUP} exists), {n_empty} with no scorable speakers, "
        f"{n_fail} failed."
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
