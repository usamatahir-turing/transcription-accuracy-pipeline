"""Compute per-conversation overlap ratio from speech-only seglst segments.

Writes ``overlap_ratio.json`` into each conversation folder.

Overlap ratio (canonical, literature):

    overlap_ratio = T_overlap / T_speech

NSV-only / token-only seglst rows are excluded (same speech filter as DetER).

Total audio: duration of ``*_mixed.wav`` when present, else max speaker ``.wav``
duration.

Usage
-----
    python -m conversation_structure_pipeline.overlap_calculation
    python -m conversation_structure_pipeline.overlap_calculation --batch delivery_batch_05192026
    python -m conversation_structure_pipeline.overlap_calculation --conversation NV-KO-SS03-CONVO08
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from conversation_structure_pipeline.common import (
    compute_overlap_ratio,
    resolve_total_audio_s,
)
from diarization_pipeline.seglst_to_rttm import is_speech_segment
from workflow_common import add_scope_args, resolve_conversation_dirs

OVERLAP_JSON = "overlap_ratio.json"


def _speaker_from_seglst(path: Path) -> str:
    return path.name[: -len(".seglst.json")]


def _count_seglst_segments(seglst_path: Path) -> tuple[int, int]:
    """Return (n_speech, n_dropped) for one seglst file."""
    segs = json.loads(seglst_path.read_text(encoding="utf-8-sig"))
    if not isinstance(segs, list):
        raise ValueError(f"{seglst_path} did not contain a JSON array")
    kept = dropped = 0
    for seg in segs:
        words = seg.get("words", "")
        if not is_speech_segment(words):
            dropped += 1
            continue
        try:
            start = float(seg["start_time"])
            end = float(seg["end_time"])
        except (KeyError, TypeError, ValueError):
            dropped += 1
            continue
        if end <= start:
            dropped += 1
            continue
        kept += 1
    return kept, dropped


def _speech_segments_from_seglst(
    seglst_path: Path, speaker: str,
) -> list[tuple[float, float, str]]:
    """Return (start, duration, speaker) tuples for speech-only rows."""
    segs = json.loads(seglst_path.read_text(encoding="utf-8-sig"))
    out: list[tuple[float, float, str]] = []
    for seg in segs:
        words = seg.get("words", "")
        if not is_speech_segment(words):
            continue
        try:
            start = float(seg["start_time"])
            end = float(seg["end_time"])
        except (KeyError, TypeError, ValueError):
            continue
        if end <= start:
            continue
        out.append((start, end - start, speaker))
    return out


def process_conversation(session_dir: Path) -> dict | None:
    seglst_files = sorted(session_dir.glob("*.seglst.json"))
    if not seglst_files:
        return None

    all_segments: list[tuple[float, float, str]] = []
    speakers_out: dict[str, dict] = {}
    total_kept = total_dropped = 0

    for seglst_path in seglst_files:
        speaker = _speaker_from_seglst(seglst_path)
        kept, dropped = _count_seglst_segments(seglst_path)
        total_kept += kept
        total_dropped += dropped

        segs = _speech_segments_from_seglst(seglst_path, speaker)
        all_segments.extend(segs)
        talk_time = round(sum(d for _s, d, _sp in segs), 3)
        speakers_out[speaker] = {
            "speech_s": talk_time,
            "n_speech_segments": kept,
            "n_dropped_segments": dropped,
            "n_seglst_segments": kept + dropped,
        }

    speech_s, overlap_s, file_span_s, ratio = compute_overlap_ratio(all_segments)
    speaker_stems = [_speaker_from_seglst(p) for p in seglst_files]
    total_audio_s, total_audio_source = resolve_total_audio_s(session_dir, speaker_stems)

    return {
        "session_id": session_dir.name,
        "method": {
            "metric": "overlap_ratio",
            "definition": "overlap_s / speech_s  (T_overlap / T_speech)",
            "numerator": "overlap_s — wall-clock seconds where >= 2 speakers are active",
            "denominator": "speech_s — wall-clock seconds where >= 1 speaker is active",
            "speech_source": "speech-only seglst segments (NSV-only rows excluded)",
            "total_audio": (
                "duration of *_mixed.wav when present, else max speaker .wav duration"
            ),
            "reference": "chsep_audio_qa/ami_rttm_stats.py compute_overlap_ratio",
        },
        "conversation": {
            "n_speakers": len(seglst_files),
            "total_audio_s": total_audio_s,
            "total_audio_source": total_audio_source,
            "speech_s": round(speech_s, 3),
            "overlap_s": round(overlap_s, 3),
            "overlap_ratio": round(ratio, 6),
            "overlap_ratio_pct": round(ratio * 100, 2),
            "file_span_s": round(file_span_s, 3),
            "n_speech_segments": total_kept,
            "n_dropped_segments": total_dropped,
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
        out_path = session_dir / OVERLAP_JSON
        if out_path.exists() and not args.overwrite:
            n_skipped += 1
            continue
        try:
            result = process_conversation(session_dir)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {session_dir.name}: {exc}")
            n_fail += 1
            continue
        if result is None:
            n_empty += 1
            continue
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        c = result["conversation"]
        print(
            f"  OK   {session_dir.name}  "
            f"overlap={c['overlap_ratio_pct']:.2f}%  "
            f"speakers={c['n_speakers']}  "
            f"speech={c['speech_s']:.1f}s  overlap={c['overlap_s']:.1f}s"
        )
        n_done += 1

    print(
        f"\nDone. {n_done} conversation(s) scored, {n_skipped} skipped "
        f"(overlap_ratio.json exists), {n_empty} with no seglst files, {n_fail} failed."
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
