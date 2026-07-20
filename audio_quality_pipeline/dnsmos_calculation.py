"""DNSMOS P.835 pipeline: score each speaker channel (speech-masked).

Per speaker writes ``{speaker}_dnsmos.json``; per conversation writes ``dnsmos.json``.

Usage
-----
    python -m audio_quality_pipeline.dnsmos_calculation --conversation NV-KO-SS15-CONVO34
    python -m audio_quality_pipeline.dnsmos_calculation --batch delivery_batch_07142026
    python -m audio_quality_pipeline.dnsmos_calculation --batch delivery_batch_07142026 --overwrite
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from audio_quality_pipeline.dnsmos_p835 import (
    SIG_WARN_MIN,
    score_audio,
    session_device,
)
from audio_quality_pipeline.speech_windows import extract_speech_audio
from diarization_pipeline.common import channel_id_from_path, speaker_output_name
from workflow_common import add_scope_args, resolve_conversation_dirs

DNSMOS_JSON_SUFFIX = "_dnsmos.json"
DNSMOS_ROLLUP = "dnsmos.json"


def dnsmos_json_path(seglst_path: Path) -> Path:
    speaker = speaker_output_name(channel_id_from_path(seglst_path))
    return seglst_path.with_name(f"{speaker}{DNSMOS_JSON_SUFFIX}")


def score_speaker(seglst_path: Path) -> dict | None:
    channel_id = channel_id_from_path(seglst_path)
    speaker = speaker_output_name(channel_id)
    wav_path = seglst_path.with_name(f"{channel_id}.wav")
    if not wav_path.is_file():
        print(f"    SKIP {speaker}: no {wav_path.name}")
        return None

    window = extract_speech_audio(wav_path, seglst_path)
    if window["n_samples"] < 1600:  # < 0.1 s at 16 kHz after resample floor
        print(f"    WARN {speaker}: too little speech ({window['speech_s']}s)")
        return None

    scores = score_audio(window["audio"], window["sample_rate"])
    flags: list[str] = []
    if not scores["pass"]:
        flags.append("sig_below_3.0")

    return {
        "session_id": seglst_path.parent.name,
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
        },
        "diagnostics": {
            "speech_s": window["speech_s"],
            "speech_min": window["speech_min"],
            "peak_dbfs": window["peak_dbfs"],
            "n_speech_segments": window["n_speech_segments"],
            "sample_rate": window["sample_rate"],
        },
        "flags": flags,
        "method": {
            "metric": "DNSMOS_P835",
            "speech_mask": "speech-only seglst (NSV-only excluded)",
            "model": "sig_bak_ovr.onnx",
            "device": scores["device"],
        },
    }


def process_conversation(session_dir: Path, *, overwrite: bool) -> dict | None:
    seglst_files = sorted(session_dir.glob("*.seglst.json"))
    if not seglst_files:
        return None

    speakers_out: dict[str, dict] = {}
    for seglst_path in seglst_files:
        speaker = speaker_output_name(channel_id_from_path(seglst_path))
        out_path = dnsmos_json_path(seglst_path)
        if out_path.exists() and not overwrite:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
            speakers_out[speaker] = existing
            print(f"    SKIP {speaker}: {out_path.name} exists")
            continue
        try:
            result = score_speaker(seglst_path)
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

    return {
        "session_id": session_dir.name,
        "method": {
            "metric": "DNSMOS_P835",
            "description": (
                "DNSMOS P.835 SIG/BAK/OVRL on speech-only seglst windows "
                f"(SIG > {SIG_WARN_MIN} warning threshold)."
            ),
            "speech_mask": "speech-only seglst (NSV-only excluded)",
            "threshold_sig": SIG_WARN_MIN,
            "device": session_device(),
        },
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
    args = parser.parse_args(argv)

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
            result = process_conversation(session_dir, overwrite=args.overwrite)
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
