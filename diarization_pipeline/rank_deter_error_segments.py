"""Rank worst DetER error intervals per speaker for manual review.

Reads ``SPK*_deter.json`` (missed seglst segments + false-alarm regions) and
writes ``SPK*_top_deter_errors.json`` with the top-N intervals per error type.

Usage
-----
    python -m diarization_pipeline.rank_deter_error_segments
    python -m diarization_pipeline.rank_deter_error_segments --conversation NV-AR-SS03-CONVO09
    python -m diarization_pipeline.rank_deter_error_segments --top 10 --overwrite
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from diarization_pipeline.common import (
    TOP_DETER_ERRORS,
    TOP_MISSED_SEGMENTS,
    parse_rttm,
    regions_to_json,
    subtract_regions,
    uncovered_regions,
)
from diarization_pipeline.deter_calculation import DETER_JSON_SUFFIX
from diarization_pipeline.seglst_to_rttm import nonspeech_spans
from workflow_common import add_scope_args, resolve_speaker_files


def derive_language(session_id: str) -> str:
    parts = session_id.split("-")
    return parts[1] if len(parts) >= 2 else ""


def rank_speaker(deter_path: Path, *, top_n: int) -> dict | None:
    data = json.loads(deter_path.read_text(encoding="utf-8"))
    deter = data.get("deter") or {}
    sad = data.get("sad") or {}
    session_dir = deter_path.parent
    session_id = session_dir.name
    speaker = data.get("speaker", deter_path.name[: -len(DETER_JSON_SUFFIX)])
    language = derive_language(session_id)

    segments: list[dict] = []

    missed = sorted(
        data.get("top_missed_seglst_segments") or [],
        key=lambda x: (-x.get("miss_s", 0), -x.get("ref_speech_s", 0), x.get("idx", 0)),
    )
    for rank, seg in enumerate(missed[:top_n], start=1):
        ref_s = seg.get("ref_speech_s", 0)
        hyp_cov = seg.get("hyp_coverage_s", 0)
        miss_s = seg.get("miss_s", 0)
        coverage_pct = round(100.0 * hyp_cov / ref_s, 2) if ref_s > 0 else None
        segments.append({
            "error_type": "missed_detection",
            "rank_metric": "miss_s",
            "rank": rank,
            "idx": seg.get("idx"),
            "start": seg.get("start"),
            "end": seg.get("end"),
            "error_s": miss_s,
            "ref_speech_s": ref_s,
            "hyp_coverage_s": hyp_cov,
            "coverage_pct": coverage_pct,
            "words": seg.get("words", ""),
        })

    false_alarms = data.get("top_false_alarm_regions")
    if not false_alarms:
        ref_name = data.get("ref_rttm")
        hyp_name = data.get("hyp_rttm")
        if ref_name and hyp_name:
            ref_path = session_dir / ref_name
            hyp_path = session_dir / hyp_name
            seglst_path = session_dir / f"{speaker}.seglst.json"
            if ref_path.is_file() and hyp_path.is_file():
                nsv_spans = (
                    nonspeech_spans(seglst_path)
                    if seglst_path.is_file() else []
                )
                false_alarms = regions_to_json(
                    subtract_regions(
                        uncovered_regions(
                            parse_rttm(hyp_path), parse_rttm(ref_path)),
                        nsv_spans,
                    ),
                    TOP_MISSED_SEGMENTS,
                )
    false_alarms = sorted(
        false_alarms or [],
        key=lambda x: (-x.get("duration_s", 0), x.get("start", 0)),
    )
    for rank, seg in enumerate(false_alarms[:top_n], start=1):
        segments.append({
            "error_type": "false_alarm",
            "rank_metric": "false_alarm_s",
            "rank": rank,
            "idx": None,
            "start": seg.get("start"),
            "end": seg.get("end"),
            "error_s": seg.get("duration_s"),
            "ref_speech_s": None,
            "hyp_coverage_s": None,
            "coverage_pct": None,
            "words": "",
        })

    if not segments:
        return None

    return {
        "session_id": session_id,
        "speaker": speaker,
        "language": language,
        "channel_deter_pct": deter.get("error_rate_pct"),
        "channel_pass": deter.get("pass"),
        "sad_mode": sad.get("mode", ""),
        "top_n": top_n,
        "segments": segments,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=True)
    parser.add_argument(
        "--top", type=int, default=TOP_DETER_ERRORS,
        help=f"Intervals per error type per speaker (default: {TOP_DETER_ERRORS}).",
    )
    args = parser.parse_args(argv)

    root = Path(args.conversations)
    try:
        deter_files = resolve_speaker_files(
            root, args.batch, args.conversation, args.file, DETER_JSON_SUFFIX)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit > 0:
        deter_files = deter_files[: args.limit]

    n_done = n_skipped = n_empty = n_fail = 0
    for deter_path in deter_files:
        speaker = deter_path.name[: -len(DETER_JSON_SUFFIX)]
        out_path = deter_path.with_name(f"{speaker}_top_deter_errors.json")
        if out_path.exists() and not args.overwrite:
            n_skipped += 1
            continue
        try:
            result = rank_speaker(deter_path, top_n=args.top)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {deter_path.relative_to(root)}: {exc}")
            n_fail += 1
            continue
        if result is None:
            n_empty += 1
            continue
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        n_missed = sum(
            1 for s in result["segments"] if s["error_type"] == "missed_detection")
        n_fa = sum(1 for s in result["segments"] if s["error_type"] == "false_alarm")
        rel = out_path.relative_to(root)
        print(
            f"  OK   {rel}  DetER={result['channel_deter_pct']}%  "
            f"missed={n_missed}  fa={n_fa}"
        )
        n_done += 1

    print(
        f"\nDone. {n_done} speaker file(s) written, {n_skipped} skipped "
        f"(output exists), {n_empty} with no errors, {n_fail} failed."
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
