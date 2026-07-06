"""Shared RTTM / interval utilities and NeMo DetER scoring."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

DETER_CH_MAX = 0.10
DEFAULT_COLLAR = 0.25
SAD_RTTM_SUFFIX = "_sad.rttm"
TOP_MISSED_SEGMENTS = 20
TOP_DETER_ERRORS = 10

SadMode = Literal["sortformer", "silero", "union"]
SAD_MODES: tuple[SadMode, ...] = ("sortformer", "silero", "union")


def sad_rttm_path(speaker_wav_or_seglst: Path) -> Path:
    """``SPK01.wav`` or ``SPK01.seglst.json`` -> ``SPK01_sad.rttm``."""
    stem = speaker_wav_or_seglst.name.split(".")[0]
    return speaker_wav_or_seglst.with_name(f"{stem}{SAD_RTTM_SUFFIX}")


def parse_rttm(rttm_path: Path) -> list[tuple[float, float]]:
    segments: list[tuple[float, float]] = []
    with rttm_path.open(encoding="utf-8") as fh:
        for line in fh:
            parts = line.strip().split()
            if len(parts) < 5 or parts[0] != "SPEAKER":
                continue
            onset = float(parts[3])
            dur = float(parts[4])
            segments.append((onset, onset + dur))
    return segments


def merge_segments(
    segments: list[tuple[float, float]],
    collar: float = 0.0,
) -> list[tuple[float, float]]:
    if not segments:
        return []
    segs = sorted(segments)
    merged = [segs[0]]
    for s, e in segs[1:]:
        if s <= merged[-1][1] + collar:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return merged


def write_rttm(
    segments: list[tuple[float, float]],
    rttm_path: Path,
    file_id: str,
    speaker_label: str = "speech",
) -> None:
    rttm_path.parent.mkdir(parents=True, exist_ok=True)
    with rttm_path.open("w", encoding="utf-8") as fh:
        for start, end in segments:
            dur = end - start
            if dur <= 0:
                continue
            fh.write(
                f"SPEAKER {file_id} 1 {start:.3f} {dur:.3f} <NA> <NA> "
                f"{speaker_label} <NA> <NA>\n"
            )


def segments_to_label_strings(segments: list[tuple[float, float]]) -> list[str]:
    merged = merge_segments(segments)
    return [f"{s:.3f} {e:.3f} speech" for s, e in merged]


def rttm_to_speech_labels(rttm_path: Path) -> list[str]:
    return segments_to_label_strings(parse_rttm(rttm_path))


def uncovered_regions(
    reference: list[tuple[float, float]],
    hypothesis: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    """Portions of ``reference`` timeline not covered by ``hypothesis``."""
    ref = merge_segments(reference)
    hyp = merge_segments(hypothesis)
    if not ref:
        return []
    if not hyp:
        return list(ref)

    missed: list[tuple[float, float]] = []
    for rs, re in ref:
        cursor = rs
        for hs, he in hyp:
            if he <= cursor or hs >= re:
                continue
            if hs > cursor:
                missed.append((cursor, min(hs, re)))
            cursor = max(cursor, he)
            if cursor >= re:
                break
        if cursor < re:
            missed.append((cursor, re))
    return [(s, e) for s, e in missed if e - s > 1e-6]


def subtract_regions(
    regions: list[tuple[float, float]],
    holes: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    """Remove ``holes`` from ``regions`` (for UEM-aligned false-alarm diagnostics)."""
    if not regions:
        return []
    if not holes:
        return list(regions)
    holes_m = merge_segments(holes)
    out: list[tuple[float, float]] = []
    for rs, re in regions:
        parts = [(rs, re)]
        for hs, he in holes_m:
            next_parts: list[tuple[float, float]] = []
            for ps, pe in parts:
                if pe <= hs or ps >= he:
                    next_parts.append((ps, pe))
                else:
                    if ps < hs:
                        next_parts.append((ps, hs))
                    if pe > he:
                        next_parts.append((he, pe))
            parts = next_parts
        out.extend((s, e) for s, e in parts if e - s > 1e-6)
    return out


def build_nsv_uem(
    ref_labels: list[str],
    hyp_labels: list[str],
    nsv_spans: list[tuple[float, float]],
):
    """Pyannote UEM = [0, T] minus NSV spans (no-score zones)."""
    merged = merge_segments(nsv_spans)
    if not merged:
        return None
    from pyannote.core import Segment, Timeline

    def _max_end(labels: list[str]) -> float:
        return max((float(label.split()[1]) for label in labels), default=0.0)

    end_t = max(_max_end(ref_labels), _max_end(hyp_labels), merged[-1][1])
    scored: list[tuple[float, float]] = []
    cur = 0.0
    for start, end in merged:
        start = max(0.0, start)
        end = min(end_t, end)
        if start > cur:
            scored.append((cur, start))
        cur = max(cur, end)
    if cur < end_t:
        scored.append((cur, end_t))
    return Timeline([Segment(s, e) for s, e in scored if e > s])


def interval_coverage(
    interval: tuple[float, float],
    haystack: list[tuple[float, float]],
) -> float:
    s, e = interval
    hyp = merge_segments(haystack)
    total = 0.0
    for hs, he in hyp:
        total += max(0.0, min(e, he) - max(s, hs))
    return min(total, e - s)


def score_deter(
    ref_labels: list[str],
    hyp_labels: list[str],
    uniq_id: str,
    collar: float = DEFAULT_COLLAR,
    uem=None,
) -> dict:
    """Score DetER via NeMo ``der.score_labels`` (pyannote engine).

    When ``uem`` is set, regions outside the UEM (e.g. NSV-only seglst turns)
    are excluded from missed/false-alarm accounting.
    """
    if not ref_labels:
        raise ValueError("empty reference speech timeline")

    from nemo.collections.asr.metrics.der import score_labels
    from nemo.collections.asr.parts.utils.speaker_utils import labels_to_pyannote_object

    ref_ann = labels_to_pyannote_object(ref_labels, uniq_name=uniq_id)
    hyp_ann = labels_to_pyannote_object(hyp_labels, uniq_name=uniq_id)
    out = score_labels(
        {uniq_id: {}},
        [(uniq_id, ref_ann)],
        [(uniq_id, hyp_ann)],
        all_uem=([uem] if uem is not None else None),
        collar=collar,
        ignore_overlap=False,
        verbose=False,
    )
    if not out:
        return {}
    metric, _mapping, (der, _cer, _fa, _miss) = out
    return {
        "error_rate": float(der),
        "scored_speech_s": float(metric["total"]),
        "missed_s": float(metric["missed detection"]),
        "false_alarm_s": float(metric["false alarm"]),
        "confusion_s": float(metric["confusion"]),
    }


def regions_to_json(regions: list[tuple[float, float]], limit: int) -> list[dict]:
    items = sorted(regions, key=lambda x: x[1] - x[0], reverse=True)[:limit]
    return [
        {"start": round(s, 3), "end": round(e, 3), "duration_s": round(e - s, 3)}
        for s, e in items
    ]


def top_missed_seglst_segments(
    speech_rows: list[dict],
    hyp_segments: list[tuple[float, float]],
    limit: int = TOP_MISSED_SEGMENTS,
) -> list[dict]:
    ranked: list[dict] = []
    for row in speech_rows:
        ref_s = row["duration_s"]
        covered = interval_coverage((row["start"], row["end"]), hyp_segments)
        miss_s = max(0.0, ref_s - covered)
        if miss_s <= 1e-6:
            continue
        ranked.append({
            "idx": row["idx"],
            "start": row["start"],
            "end": row["end"],
            "words": row["words"],
            "ref_speech_s": ref_s,
            "hyp_coverage_s": round(covered, 3),
            "miss_s": round(miss_s, 3),
        })
    ranked.sort(key=lambda x: (-x["miss_s"], -x["ref_speech_s"], x["idx"]))
    return ranked[:limit]


def sad_mode_description(mode: SadMode) -> str:
    if mode == "sortformer":
        return "Sortformer diarizer only"
    if mode == "silero":
        return "Silero VAD only"
    return "Sortformer + Silero VAD union"
