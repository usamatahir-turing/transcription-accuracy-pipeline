"""Effective-bandwidth pipeline: LTAS cutoff per speaker channel (speech-masked).

Per speaker writes ``{speaker}_bandwidth.json`` (+ optional spectrogram PNG);
per conversation writes ``bandwidth.json``.

Usage
-----
    python -m audio_quality_pipeline.bandwidth_calculation --conversation NV-GR-SS08-CONVO15
    python -m audio_quality_pipeline.bandwidth_calculation --batch delivery_batch_07142026
    python -m audio_quality_pipeline.bandwidth_calculation --batch delivery_batch_07142026 --overwrite
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from audio_quality_pipeline.effective_bandwidth import (
    WARN_8KHZ,
    WARN_12KHZ,
    WARN_16KHZ,
    estimate_effective_bandwidth,
    save_bandwidth_spectrogram,
)
from audio_quality_pipeline.speech_windows import extract_speech_audio
from diarization_pipeline.common import channel_id_from_path, speaker_output_name
from workflow_common import add_scope_args, resolve_conversation_dirs

BANDWIDTH_JSON_SUFFIX = "_bandwidth.json"
BANDWIDTH_ROLLUP = "bandwidth.json"
SPECTROGRAM_SUFFIX = "_bandwidth_spectrogram.png"


def bandwidth_json_path(seglst_path: Path) -> Path:
    speaker = speaker_output_name(channel_id_from_path(seglst_path))
    return seglst_path.with_name(f"{speaker}{BANDWIDTH_JSON_SUFFIX}")


def spectrogram_path(seglst_path: Path) -> Path:
    speaker = speaker_output_name(channel_id_from_path(seglst_path))
    return seglst_path.with_name(f"{speaker}{SPECTROGRAM_SUFFIX}")


def _public_estimate(est: dict) -> dict:
    """Drop internal STFT arrays before JSON serialization."""
    return {
        "effective_hz": est["effective_hz"],
        "nyquist_hz": est["nyquist_hz"],
        "bucket": est["bucket"],
        "pass": est["pass"],
        "hf_floor_db": est["hf_floor_db"],
        "margin_db": est["margin_db"],
        "contiguous_hz": est["contiguous_hz"],
        "n_stft_frames": est["n_stft_frames"],
        "n_fft": est["n_fft"],
        "stft_ms": est.get("stft_ms"),
    }


def score_speaker(seglst_path: Path, *, write_spectrogram: bool) -> dict | None:
    channel_id = channel_id_from_path(seglst_path)
    speaker = speaker_output_name(channel_id)
    wav_path = seglst_path.with_name(f"{channel_id}.wav")
    if not wav_path.is_file():
        print(f"    SKIP {speaker}: no {wav_path.name}")
        return None

    window = extract_speech_audio(wav_path, seglst_path)
    if window["n_samples"] < int(0.1 * window["sample_rate"]):
        print(f"    WARN {speaker}: too little speech ({window['speech_s']}s)")
        return None

    est = estimate_effective_bandwidth(window["audio"], window["sample_rate"])
    sr = window["sample_rate"]
    flags: list[str] = []
    if est["effective_hz"] <= WARN_8KHZ:
        flags.append("le_8khz")
    elif est["effective_hz"] <= WARN_12KHZ:
        flags.append("le_12khz")
    elif est["effective_hz"] <= WARN_16KHZ:
        flags.append("le_16khz")
    if sr >= 44_100 and est["effective_hz"] <= WARN_8KHZ:
        flags.append("container_vs_content_mismatch")

    artifacts: dict = {}
    if write_spectrogram:
        png = spectrogram_path(seglst_path)
        save_bandwidth_spectrogram(
            window["audio"],
            sr,
            png,
            effective_hz=est["effective_hz"],
            title=f"{seglst_path.parent.name}/{speaker}  B≈{est['effective_hz']:.0f} Hz",
        )
        artifacts["spectrogram_png"] = png.name

    return {
        "session_id": seglst_path.parent.name,
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
            "speech_s": window["speech_s"],
            "speech_min": window["speech_min"],
            "peak_dbfs": window["peak_dbfs"],
            "n_speech_segments": window["n_speech_segments"],
            "sample_rate": sr,
            "hf_floor_db": est["hf_floor_db"],
            "margin_db": est["margin_db"],
            "n_stft_frames": est["n_stft_frames"],
        },
        "flags": flags,
        "artifacts": artifacts,
        "method": {
            "metric": "effective_bandwidth_ltas",
            "speech_mask": "speech-only seglst (NSV-only excluded)",
            "aggregate": "median",
            "contiguous_hz": est["contiguous_hz"],
            "margin_db": est["margin_db"],
            "stft_ms": est.get("stft_ms"),
            "description": (
                "Highest frequency with sustained LTAS energy "
                f"(median over frames, contiguous {est['contiguous_hz']} Hz) "
                f"at least {est['margin_db']} dB above the HF noise floor."
            ),
        },
    }


def process_conversation(
    session_dir: Path,
    *,
    overwrite: bool,
    write_spectrogram: bool,
) -> dict | None:
    seglst_files = sorted(session_dir.glob("*.seglst.json"))
    if not seglst_files:
        return None

    speakers_out: dict[str, dict] = {}
    for seglst_path in seglst_files:
        speaker = speaker_output_name(channel_id_from_path(seglst_path))
        out_path = bandwidth_json_path(seglst_path)
        if out_path.exists() and not overwrite:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
            speakers_out[speaker] = existing
            print(f"    SKIP {speaker}: {out_path.name} exists")
            continue
        try:
            result = score_speaker(seglst_path, write_spectrogram=write_spectrogram)
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
            "metric": "effective_bandwidth_ltas",
            "description": (
                "Effective bandwidth from speech-only LTAS "
                f"(pass if effective_hz > {WARN_8KHZ:.0f} Hz)."
            ),
            "speech_mask": "speech-only seglst (NSV-only excluded)",
            "thresholds_hz": {
                "warn_8k": WARN_8KHZ,
                "warn_12k": WARN_12KHZ,
                "warn_16k": WARN_16KHZ,
            },
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
    args = parser.parse_args(argv)

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
