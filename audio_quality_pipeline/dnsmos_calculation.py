"""DNSMOS P.835 pipeline: score each speaker channel (speech-timeline masked).

Default (calibrated to client report Worst-100 SIG):
  - Window: speech seglst on the full timeline (non-speech zeroed; NSV-only dropped)
  - Polyfit: Microsoft personalized (``dnsmos_local.py -p``)

Per speaker writes ``{speaker}_dnsmos.json``; per conversation writes ``dnsmos.json``.

Usage
-----
    python -m audio_quality_pipeline.dnsmos_calculation --conversation NV-KO-SS15-CONVO34
    python -m audio_quality_pipeline.dnsmos_calculation --batch delivery_batch_07142026 --overwrite

    # Score WAVs under riverside_raw; load seglst from Conversations (skip if missing)
    python -m audio_quality_pipeline.dnsmos_calculation \\
        --conversations riverside_raw --batch delivery_batch_07012026 \\
        --seglst-root Conversations --overwrite
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from audio_quality_pipeline.channel_pairs import iter_wav_seglst_pairs
from audio_quality_pipeline.dnsmos_p835 import (
    SIG_WARN_MIN,
    score_audio,
    session_device,
)
from audio_quality_pipeline.speech_windows import (
    extract_speech_audio,
    extract_speech_timeline_audio,
)
from diarization_pipeline.common import channel_id_from_path, speaker_output_name
from workflow_common import add_scope_args, resolve_conversation_dirs

DNSMOS_JSON_SUFFIX = "_dnsmos.json"
DNSMOS_ROLLUP = "dnsmos.json"

WINDOW_SPEECH_TIMELINE = "speech_timeline"
WINDOW_SPEECH_CONCAT = "speech_concat"
WINDOW_FULL = "full"

SPEECH_MASK_LABELS = {
    WINDOW_SPEECH_TIMELINE: (
        "speech seglst on full timeline (non-speech zeroed; NSV-only excluded)"
    ),
    WINDOW_SPEECH_CONCAT: "speech-only seglst concat (NSV-only excluded)",
    WINDOW_FULL: "full channel WAV (no seglst mask)",
}


def dnsmos_json_path_for_speaker(session_dir: Path, speaker: str) -> Path:
    return session_dir / f"{speaker}{DNSMOS_JSON_SUFFIX}"


def _load_window(wav_path: Path, seglst_path: Path, window: str) -> dict:
    if window == WINDOW_SPEECH_TIMELINE:
        return extract_speech_timeline_audio(wav_path, seglst_path)
    if window == WINDOW_SPEECH_CONCAT:
        return extract_speech_audio(wav_path, seglst_path)
    if window == WINDOW_FULL:
        from audio_quality_pipeline.speech_windows import load_mono_wav, peak_dbfs

        audio, sr = load_mono_wav(wav_path)
        speech = extract_speech_audio(wav_path, seglst_path)
        return {
            "audio": audio,
            "sample_rate": sr,
            "speech_s": speech["speech_s"],
            "speech_min": speech["speech_min"],
            "peak_dbfs": peak_dbfs(audio) if audio.size else None,
            "n_speech_segments": speech["n_speech_segments"],
            "n_samples": speech["n_samples"],
            "file_s": round(len(audio) / sr, 3) if sr else 0.0,
            "mode": WINDOW_FULL,
        }
    raise ValueError(f"unknown window mode: {window}")


def score_speaker(
    wav_path: Path,
    seglst_path: Path,
    *,
    window: str = WINDOW_SPEECH_TIMELINE,
    personalized: bool = True,
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
    if win["n_samples"] < 1600:  # < 0.1 s of speech
        print(f"    WARN {speaker}: too little speech ({win['speech_s']}s)")
        return None

    scores = score_audio(
        win["audio"], win["sample_rate"], personalized=personalized)
    flags: list[str] = []
    if not scores["pass"]:
        flags.append("sig_below_3.0")

    diagnostics = {
        "speech_s": win["speech_s"],
        "speech_min": win["speech_min"],
        "peak_dbfs": win["peak_dbfs"],
        "n_speech_segments": win["n_speech_segments"],
        "sample_rate": win["sample_rate"],
    }
    if "file_s" in win:
        diagnostics["file_s"] = win["file_s"]

    return {
        "session_id": session_id or wav_path.parent.name,
        "speaker": speaker,
        "channel_id": channel_id,
        "wav": wav_path.name,
        "dnsmos": {
            "sig": scores["sig"],
            "bak": scores["bak"],
            "ovrl": scores["ovrl"],
            "sig_raw": scores["sig_raw"],
            "bak_raw": scores["bak_raw"],
            "ovrl_raw": scores["ovrl_raw"],
            "n_hops": scores["n_hops"],
            "pass": scores["pass"],
            "threshold_sig": scores["threshold_sig"],
            "personalized": scores["personalized"],
        },
        "diagnostics": diagnostics,
        "flags": flags,
        "method": {
            "metric": "DNSMOS_P835",
            "speech_mask": SPEECH_MASK_LABELS[window],
            "window": window,
            "personalized": personalized,
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
            "DNSMOS P.835 SIG/BAK/OVRL with speech-timeline mask and "
            f"{'personalized' if personalized else 'non-personalized'} polyfit "
            f"(SIG > {SIG_WARN_MIN} warning threshold)."
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
        choices=(WINDOW_SPEECH_TIMELINE, WINDOW_SPEECH_CONCAT, WINDOW_FULL),
        default=WINDOW_SPEECH_TIMELINE,
        help=(
            "Audio window for DNSMOS (default: speech_timeline). "
            "speech_concat = old tight concat; full = entire WAV."
        ),
    )
    parser.add_argument(
        "--non-personalized",
        action="store_true",
        help="Use non-personalized polyfit (Microsoft default without -p).",
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
    personalized = not args.non_personalized
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
