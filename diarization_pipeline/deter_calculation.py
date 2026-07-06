"""DetER pipeline: speech-only reference RTTM vs configurable SAD hypothesis.

Per speaker writes ``SPK*_deter.json``; per conversation writes ``deter.json``.

Usage
-----
    python -m diarization_pipeline.deter_calculation --ref-only --conversation NV-KO-SS03-CONVO08
    python -m diarization_pipeline.deter_calculation --conversation NV-KO-SS03-CONVO08
    python -m diarization_pipeline.deter_calculation --sad-mode sortformer --conversation NV-KO-SS03-CONVO08
    python -m diarization_pipeline.deter_calculation --score-only --reuse-sad --conversation NV-KO-SS03-CONVO08
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from diarization_pipeline.common import (
    DETER_CH_MAX,
    DEFAULT_COLLAR,
    TOP_MISSED_SEGMENTS,
    SadMode,
    build_nsv_uem,
    merge_segments,
    parse_rttm,
    regions_to_json,
    rttm_to_speech_labels,
    sad_mode_description,
    sad_rttm_path,
    score_deter,
    subtract_regions,
    top_missed_seglst_segments,
    uncovered_regions,
)
from diarization_pipeline.sad_hypothesis import add_sad_mode_arg, wav_sample_rate, write_sad_rttm
from diarization_pipeline.seglst_to_rttm import (
    convert_seglst,
    der_rttm_path,
    load_speech_seglst_rows,
    nonspeech_spans,
)
from workflow_common import add_scope_args, resolve_conversation_dirs

DETER_JSON_SUFFIX = "_deter.json"


def deter_json_path(seglst_path: Path) -> Path:
    speaker = seglst_path.name.split(".seglst.json")[0]
    return seglst_path.with_name(f"{speaker}{DETER_JSON_SUFFIX}")


def _speaker_from_seglst(seglst_path: Path) -> str:
    return seglst_path.name.split(".seglst.json")[0]


def ensure_ref_rttm(seglst_path: Path, *, overwrite: bool) -> Path | None:
    out = der_rttm_path(seglst_path)
    if out.exists() and not overwrite:
        return out
    kept, dropped = convert_seglst(seglst_path, out)
    if kept == 0:
        print(f"    WARN {_speaker_from_seglst(seglst_path)}: no speech segments (dropped={dropped})")
        return None
    return out


def ensure_sad_rttm(
    seglst_path: Path,
    *,
    overwrite: bool,
    batch_size: int,
    sad_mode: SadMode,
) -> tuple[Path | None, dict | None]:
    speaker = _speaker_from_seglst(seglst_path)
    wav_path = seglst_path.with_name(f"{speaker}.wav")
    out = sad_rttm_path(seglst_path)
    if out.exists() and not overwrite:
        return out, None
    if not wav_path.is_file():
        print(f"    SKIP {speaker}: no {wav_path.name}")
        return None, None
    sr = wav_sample_rate(wav_path)
    stats = write_sad_rttm(wav_path, out, sr, mode=sad_mode, batch_size=batch_size)
    return out, stats


def score_speaker(
    seglst_path: Path,
    ref_rttm: Path,
    sad_rttm: Path,
    *,
    collar: float,
    deter_ch_max: float,
    sad_mode: SadMode,
    sad_stats: dict | None = None,
) -> dict | None:
    speaker = _speaker_from_seglst(seglst_path)
    ref_labels = rttm_to_speech_labels(ref_rttm)
    if not ref_labels:
        print(f"    WARN {speaker}: empty reference RTTM")
        return None
    hyp_labels = rttm_to_speech_labels(sad_rttm)
    nsv_spans = nonspeech_spans(seglst_path)
    uem = build_nsv_uem(ref_labels, hyp_labels, nsv_spans)
    uniq_id = f"{seglst_path.parent.name}_{speaker}"
    try:
        scores = score_deter(
            ref_labels, hyp_labels, uniq_id, collar=collar, uem=uem,
        )
    except ValueError as exc:
        print(f"    WARN {speaker}: scoring failed ({exc})")
        return None
    if not scores:
        return None

    ref_segs = parse_rttm(ref_rttm)
    hyp_segs = parse_rttm(sad_rttm)
    missed_regions = uncovered_regions(ref_segs, hyp_segs)
    false_alarm_regions = subtract_regions(
        uncovered_regions(hyp_segs, ref_segs), nsv_spans,
    )
    speech_rows = load_speech_seglst_rows(seglst_path)

    error_rate = scores["error_rate"]
    result: dict = {
        "speaker": speaker,
        "deter": {
            "error_rate": round(error_rate, 6),
            "error_rate_pct": round(error_rate * 100, 2),
            "pass": error_rate <= deter_ch_max,
            "threshold": deter_ch_max,
            "collar_s": collar,
            "scored_speech_s": round(scores["scored_speech_s"], 3),
            "missed_s": round(scores["missed_s"], 3),
            "false_alarm_s": round(scores["false_alarm_s"], 3),
            "confusion_s": round(scores["confusion_s"], 3),
        },
        "ref_rttm": ref_rttm.name,
        "hyp_rttm": sad_rttm.name,
        "n_ref_segments": len(ref_segs),
        "n_hyp_segments": len(hyp_segs),
        "top_missed_regions": regions_to_json(missed_regions, TOP_MISSED_SEGMENTS),
        "top_false_alarm_regions": regions_to_json(
            false_alarm_regions, TOP_MISSED_SEGMENTS),
        "top_missed_seglst_segments": top_missed_seglst_segments(
            speech_rows, hyp_segs, limit=TOP_MISSED_SEGMENTS,
        ),
        "uem_exclude_nsv": True,
        "n_nsv_spans": len(nsv_spans),
        "nsv_excluded_s": round(
            sum(e - s for s, e in merge_segments(nsv_spans)), 3,
        ),
    }
    if sad_stats:
        result["sad"] = {
            "mode": sad_stats["sad_mode"],
            "sortformer_segments": sad_stats["sortformer_segments"],
            "silero_segments": sad_stats["silero_segments"],
            "hyp_segments": sad_stats["hyp_segments"],
        }
    else:
        result["sad"] = {"mode": sad_mode}
    return result


def process_conversation(
    session_dir: Path,
    *,
    ref_only: bool,
    score_only: bool,
    reuse_sad: bool,
    overwrite: bool,
    collar: float,
    deter_ch_max: float,
    batch_size: int,
    sad_mode: SadMode,
) -> dict | None:
    seglst_files = sorted(session_dir.glob("*.seglst.json"))
    if not seglst_files:
        return None

    speakers_out: dict[str, dict] = {}
    for seglst_path in seglst_files:
        speaker = _speaker_from_seglst(seglst_path)
        deter_out = deter_json_path(seglst_path)

        if not ref_only and not score_only:
            if deter_out.exists() and not overwrite:
                existing = json.loads(deter_out.read_text(encoding="utf-8"))
                speakers_out[speaker] = existing
                continue

        if not score_only:
            ref_rttm = ensure_ref_rttm(seglst_path, overwrite=overwrite)
        else:
            ref_rttm = der_rttm_path(seglst_path)
            if not ref_rttm.is_file():
                print(f"    SKIP {speaker}: no {ref_rttm.name} (--score-only)")
                continue

        if ref_only:
            if ref_rttm:
                print(f"    REF  {session_dir.name}/{speaker} -> {ref_rttm.name}")
            continue

        sad_stats = None
        if score_only or reuse_sad:
            sad_rttm = sad_rttm_path(seglst_path)
            if not sad_rttm.is_file():
                print(f"    SKIP {speaker}: no {sad_rttm.name}")
                continue
        else:
            sad_rttm, sad_stats = ensure_sad_rttm(
                seglst_path, overwrite=overwrite,
                batch_size=batch_size, sad_mode=sad_mode,
            )
            if sad_rttm is None:
                continue

        if ref_rttm is None:
            continue

        result = score_speaker(
            seglst_path, ref_rttm, sad_rttm,
            collar=collar, deter_ch_max=deter_ch_max,
            sad_mode=sad_mode, sad_stats=sad_stats,
        )
        if result is None:
            continue
        deter_out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        speakers_out[speaker] = result
        d = result["deter"]
        verdict = "PASS" if d["pass"] else "FAIL"
        print(
            f"    OK   {session_dir.name}/{speaker}  "
            f"DetER={d['error_rate_pct']:.2f}%  mode={sad_mode}  {verdict}"
        )

    if ref_only:
        return None
    if not speakers_out:
        return None

    rates = [s["deter"]["error_rate"] for s in speakers_out.values()]
    scored_s = sum(s["deter"]["scored_speech_s"] for s in speakers_out.values())
    missed_s = sum(s["deter"]["missed_s"] for s in speakers_out.values())
    fa_s = sum(s["deter"]["false_alarm_s"] for s in speakers_out.values())
    conv_rate = sum(rates) / len(rates) if rates else 0.0

    return {
        "session_id": session_dir.name,
        "method": {
            "metric": "DetER",
            "description": (
                "Detection error rate: SAD hypothesis vs speech-only seglst reference, "
                "flattened to one speaker (no speaker confusion). NSV-only turns "
                "([laugh], [inhale], …) are excluded from scoring via a UEM."
            ),
            "sad_mode": sad_mode,
            "hypothesis": sad_mode_description(sad_mode),
            "reference": "SPK*_der.rttm (speech-only seglst)",
            "collar_s": collar,
            "threshold_per_channel": deter_ch_max,
            "scorer": "NeMo der.score_labels (pyannote engine)",
        },
        "conversation": {
            "mean_deter": round(conv_rate, 6),
            "mean_deter_pct": round(conv_rate * 100, 2),
            "pass": all(s["deter"]["pass"] for s in speakers_out.values()),
            "n_speakers": len(speakers_out),
            "scored_speech_s": round(scored_s, 3),
            "missed_s": round(missed_s, 3),
            "false_alarm_s": round(fa_s, 3),
        },
        "speakers": speakers_out,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=False)
    add_sad_mode_arg(parser)
    parser.add_argument("--ref-only", action="store_true",
                        help="Only build SPK*_der.rttm reference RTTMs.")
    parser.add_argument("--score-only", action="store_true",
                        help="Skip ref/SAD generation; require existing *_der.rttm and *_sad.rttm.")
    parser.add_argument("--reuse-sad", action="store_true",
                        help="Reuse existing *_sad.rttm; do not re-run SAD models.")
    parser.add_argument("--collar", type=float, default=DEFAULT_COLLAR,
                        help=f"DetER scoring collar in seconds (default: {DEFAULT_COLLAR}).")
    parser.add_argument("--deter-ch-max", type=float, default=DETER_CH_MAX,
                        help=f"Pass threshold per channel (default: {DETER_CH_MAX}).")
    parser.add_argument("--batch-size", type=int, default=40,
                        help="Sortformer batch size when running SAD (default: 40).")
    args = parser.parse_args(argv)

    if args.ref_only and args.score_only:
        print("ERROR: --ref-only and --score-only are mutually exclusive.")
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
        out_path = session_dir / "deter.json"
        if (
            not args.ref_only
            and out_path.exists()
            and not args.overwrite
            and not args.score_only
        ):
            n_skipped += 1
            continue
        try:
            result = process_conversation(
                session_dir,
                ref_only=args.ref_only,
                score_only=args.score_only,
                reuse_sad=args.reuse_sad,
                overwrite=args.overwrite,
                collar=args.collar,
                deter_ch_max=args.deter_ch_max,
                batch_size=args.batch_size,
                sad_mode=args.sad_mode,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {session_dir.name}: {exc}")
            n_fail += 1
            continue
        if args.ref_only:
            n_done += 1
            continue
        if result is None:
            n_empty += 1
            continue
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        c = result["conversation"]
        verdict = "PASS" if c["pass"] else "FAIL"
        print(
            f"  OK   {session_dir.name}  mean DetER={c['mean_deter_pct']:.2f}%  "
            f"mode={args.sad_mode}  {c['n_speakers']} speaker(s)  {verdict}"
        )
        n_done += 1

    if args.ref_only:
        print(f"\nDone. {n_done} conversation(s) processed (ref RTTMs only).")
    else:
        print(
            f"\nDone. {n_done} conversation(s) scored, {n_skipped} skipped "
            f"(deter.json exists), {n_empty} with no scorable speakers, {n_fail} failed."
        )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
