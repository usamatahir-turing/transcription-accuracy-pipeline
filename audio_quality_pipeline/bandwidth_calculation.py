"""Effective-bandwidth pipeline: annotated STFT on RTTM-masked frames.

Matches Batch 8/9 QA ``annotated-stft-v1-nfft2048-hop1024-profile250``.

Per speaker writes ``{speaker}_bandwidth.json`` (+ optional spectrogram PNG);
per conversation writes ``bandwidth.json``.

Usage
-----
    python -m audio_quality_pipeline.bandwidth_calculation --conversation NV-GR-SS13-CONVO22
    python -m audio_quality_pipeline.bandwidth_calculation --batch delivery_batch_08082026 --overwrite
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from audio_quality_pipeline.channel_pairs import iter_wav_seglst_pairs
from audio_quality_pipeline.effective_bandwidth import (
    ANALYSIS_VERSION,
    WARN_8KHZ,
    WARN_12KHZ,
    WARN_16KHZ,
    estimate_effective_bandwidth,
    save_bandwidth_spectrogram,
)
from audio_quality_pipeline.rttm_utils import (
    load_rttm_spans,
    rttm_speech_seconds,
)
from audio_quality_pipeline.speech_windows import load_mono_wav
from diarization_pipeline.common import channel_id_from_path, speaker_output_name
from workflow_common import add_scope_args, resolve_conversation_dirs

BANDWIDTH_JSON_SUFFIX = "_bandwidth.json"
BANDWIDTH_ROLLUP = "bandwidth.json"
SPECTROGRAM_SUFFIX = "_bandwidth_spectrogram.png"


def bandwidth_json_path_for_speaker(session_dir: Path, speaker: str) -> Path:
    return session_dir / f"{speaker}{BANDWIDTH_JSON_SUFFIX}"


def spectrogram_path_for_speaker(session_dir: Path, speaker: str) -> Path:
    return session_dir / f"{speaker}{SPECTROGRAM_SUFFIX}"


def _public_estimate(est: dict) -> dict:
    return {
        "effective_hz": est["effective_hz"],
        "effective_khz": est.get("effective_khz"),
        "nyquist_hz": est["nyquist_hz"],
        "bucket": est["bucket"],
        "category": est.get("category"),
        "pass": est["pass"],
        "analysis_version": est.get("analysis_version", ANALYSIS_VERSION),
        "activity_threshold_dbfs": est.get("activity_threshold_dbfs"),
        "silence_rms_dbfs": est.get("silence_rms_dbfs"),
        "cutoff_drop_db": est.get("cutoff_drop_db"),
        "pre_cutoff_db_relative": est.get("pre_cutoff_db_relative"),
        "post_cutoff_db_relative": est.get("post_cutoff_db_relative"),
        "sampled_windows": est.get("sampled_windows"),
        "active_stft_frames": est.get("active_stft_frames"),
        "n_stft_frames": est.get("n_stft_frames"),
        "n_fft": est.get("n_fft"),
        "hop": est.get("hop"),
        "profile_bin_hz": est.get("profile_bin_hz"),
    }


def score_speaker(
    wav_path: Path,
    rttm_path: Path,
    *,
    write_spectrogram: bool,
    session_id: str | None = None,
) -> dict | None:
    channel_id = channel_id_from_path(wav_path)
    speaker = speaker_output_name(channel_id)
    if not wav_path.is_file():
        print(f"    SKIP {speaker}: no {wav_path.name}")
        return None
    if not rttm_path.is_file():
        print(f"    SKIP {speaker}: no {rttm_path.name}")
        return None

    spans = load_rttm_spans(rttm_path)
    if not spans:
        print(f"    SKIP {speaker}: empty {rttm_path.name}")
        return None

    audio, sr = load_mono_wav(wav_path)
    speech_s = rttm_speech_seconds(spans)
    if speech_s < 0.1:
        print(f"    WARN {speaker}: too little annotated speech ({speech_s}s)")
        return None

    est = estimate_effective_bandwidth(audio, sr, spans)
    flags: list[str] = []
    if est["effective_hz"] <= WARN_8KHZ:
        flags.append("le_8khz")
    elif est["effective_hz"] <= WARN_12KHZ:
        flags.append("le_12khz")
    elif est["effective_hz"] <= WARN_16KHZ:
        flags.append("le_16khz")
    if sr >= 44_100 and est["effective_hz"] <= WARN_8KHZ:
        flags.append("container_vs_content_mismatch")

    session = session_id or wav_path.parent.name
    artifacts: dict = {}
    if write_spectrogram:
        png = spectrogram_path_for_speaker(wav_path.parent, speaker)
        save_bandwidth_spectrogram(
            audio,
            sr,
            png,
            effective_hz=est["effective_hz"],
            title=f"{session}/{speaker}  B≈{est['effective_hz']:.0f} Hz",
        )
        artifacts["spectrogram_png"] = png.name

    return {
        "session_id": session,
        "speaker": speaker,
        "channel_id": channel_id,
        "wav": wav_path.name,
        "bandwidth": {
            **_public_estimate(est),
            "container_sr": sr,
            "thresholds_hz": {
                "warn_8k": WARN_8KHZ,
                "warn_12k": WARN_12KHZ,
                "warn_16k": WARN_16KHZ,
            },
        },
        "diagnostics": {
            "annotated_speech_s": round(speech_s, 3),
            "speech_min": round(speech_s / 60.0, 3),
            "sample_rate": sr,
            "rttm": rttm_path.name,
        },
        "flags": flags,
        "artifacts": artifacts,
        "method": {
            "metric": "effective_bandwidth_annotated_stft",
            "analysis_version": ANALYSIS_VERSION,
            "annotation": "per-channel RTTM",
            "description": (
                "Batch 8/9 annotated STFT profile cutoff on RTTM-masked frames "
                f"({est.get('sampled_windows', 0)} sampled windows)."
            ),
        },
    }


def process_conversation(
    session_dir: Path,
    *,
    overwrite: bool,
    write_spectrogram: bool,
    seglst_root: Path | None,
) -> dict | None:
    pairs = iter_wav_seglst_pairs(session_dir, seglst_root=seglst_root)
    if not pairs:
        return None

    speakers_out: dict[str, dict] = {}
    for wav_path, _seglst_path in pairs:
        channel_id = channel_id_from_path(wav_path)
        speaker = speaker_output_name(channel_id)
        if seglst_root is None:
            rttm_path = wav_path.parent / f"{channel_id}.rttm"
        else:
            batch = session_dir.parent.name
            rttm_path = seglst_root / batch / session_dir.name / f"{channel_id}.rttm"

        out_path = bandwidth_json_path_for_speaker(session_dir, speaker)
        if out_path.exists() and not overwrite:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
            speakers_out[speaker] = existing
            print(f"    SKIP {speaker}: {out_path.name} exists")
            continue
        try:
            result = score_speaker(
                wav_path,
                rttm_path,
                write_spectrogram=write_spectrogram,
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
        b = result["bandwidth"]
        verdict = "PASS" if b["pass"] else "FAIL"
        print(
            f"    OK   {session_dir.name}/{speaker}  "
            f"B={b['effective_hz']:.0f} Hz  bucket={b['bucket']}  {verdict}"
        )

    if not speakers_out:
        return None

    effs = [s["bandwidth"]["effective_hz"] for s in speakers_out.values()]
    n_le_8 = sum(1 for e in effs if e <= WARN_8KHZ)
    n_le_12 = sum(1 for e in effs if e <= WARN_12KHZ)
    n_le_16 = sum(1 for e in effs if e <= WARN_16KHZ)

    return {
        "session_id": session_dir.name,
        "method": {
            "metric": "effective_bandwidth_annotated_stft",
            "analysis_version": ANALYSIS_VERSION,
            "description": (
                "Effective bandwidth from RTTM-masked annotated STFT "
                f"(pass if effective_hz > {WARN_8KHZ:.0f} Hz)."
            ),
        },
        "conversation": {
            "n_speakers": len(speakers_out),
            "n_le_8khz": n_le_8,
            "n_le_12khz": n_le_12,
            "n_le_16khz": n_le_16,
            "min_effective_hz": round(min(effs), 1),
            "mean_effective_hz": round(sum(effs) / len(effs), 1),
            "pass": n_le_8 == 0,
        },
        "speakers": speakers_out,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=False)
    parser.add_argument(
        "--no-spectrogram",
        action="store_true",
        help="Skip writing *_bandwidth_spectrogram.png review plots.",
    )
    parser.add_argument(
        "--seglst-root",
        type=Path,
        default=None,
        help=(
            "Optional root for locating RTTM/seglst alongside WAVs when WAVs "
            "live under another tree (same layout as DNSMOS)."
        ),
    )
    args = parser.parse_args(argv)

    seglst_root = args.seglst_root.resolve() if args.seglst_root else None
    if seglst_root is not None and not seglst_root.is_dir():
        print(f"ERROR: annotation root not found: {seglst_root}")
        return 1

    root = Path(args.conversations)
    try:
        session_dirs = resolve_conversation_dirs(root, args.batch, args.conversation)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit > 0:
        session_dirs = session_dirs[: args.limit]

    write_spectrogram = not args.no_spectrogram
    n_done = n_skipped = n_empty = n_fail = 0
    for session_dir in session_dirs:
        out_path = session_dir / BANDWIDTH_ROLLUP
        if out_path.exists() and not args.overwrite:
            n_skipped += 1
            print(f"  SKIP {session_dir.name}: {BANDWIDTH_ROLLUP} exists")
            continue
        try:
            result = process_conversation(
                session_dir,
                overwrite=args.overwrite,
                write_spectrogram=write_spectrogram,
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
            f"  OK   {session_dir.name}  mean B={c['mean_effective_hz']:.0f} Hz  "
            f"le_8khz={c['n_le_8khz']}/{c['n_speakers']}  {verdict}"
        )
        n_done += 1

    print(
        f"\nDone. {n_done} conversation(s) scored, {n_skipped} skipped "
        f"({BANDWIDTH_ROLLUP} exists), {n_empty} with no scorable speakers, "
        f"{n_fail} failed."
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
