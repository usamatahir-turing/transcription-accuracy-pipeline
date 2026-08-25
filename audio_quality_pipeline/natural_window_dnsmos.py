"""Batch 8/9 style annotated natural-window DNSMOS window placement."""

from __future__ import annotations

from diarization_pipeline.seglst_to_rttm import load_speech_seglst_rows

WINDOW_SEC = 9.01
CONTEXT_BEFORE_SEC = 0.5
HOP_SEC = WINDOW_SEC - CONTEXT_BEFORE_SEC
CLIP_THRESHOLD = 0.9999
CLUSTER_GAP_SEC = 1.0
TAIL_MIN_SPEECH_SEC = HOP_SEC - 0.05
MAX_TAIL_PAST_CLUSTER = 2


def _speech_seconds(spans: list[tuple[float, float]], start: float, end: float) -> float:
    total = 0.0
    for s, e in spans:
        total += max(0.0, min(e, end) - max(s, start))
    return total


def _covered_by(starts: list[float], s: float, e: float) -> bool:
    return any(s >= st and e <= st + WINDOW_SEC + 0.01 for st in starts)


def _cluster_end(spans: list[tuple[float, float]], t: float, *, gap: float) -> float:
    idx = 0
    for i, (s, e) in enumerate(spans):
        if s - gap <= t <= e + gap:
            idx = i
            break
    cs, ce = spans[idx]
    j = idx
    while j > 0 and spans[j][0] - spans[j - 1][1] <= gap:
        j -= 1
        cs = spans[j][0]
    j = idx
    while j + 1 < len(spans) and spans[j + 1][0] - spans[j][1] <= gap:
        j += 1
        ce = spans[j][1]
    return ce


def natural_window_starts_from_spans(
    spans: list[tuple[float, float]],
    *,
    cluster_gap: float = CLUSTER_GAP_SEC,
) -> list[float]:
    """Place 9.01 s windows on seglst speech spans (Batch 8/9 QA style).

    Chronological span triggers with optional hop fill before a later span-aligned
    window, plus a short tail hop chain after the last span. Reverse-engineered
    from ``batch8and9review`` reference artifacts (not bit-exact on all channels).
    """
    if not spans:
        return []

    starts: list[float] = []

    def _add(ns: float) -> bool:
        ns = round(ns, 2)
        if ns in starts or _speech_seconds(spans, ns, ns + WINDOW_SEC) <= 0:
            return False
        starts.append(ns)
        return True

    for s, e in spans:
        if _covered_by(starts, s, e):
            continue
        span_ns = round(max(0.0, s - CONTEXT_BEFORE_SEC), 2)
        if not starts:
            _add(span_ns)
            continue

        last = starts[-1]
        t = round(last + HOP_SEC, 2)
        while t + 0.01 < span_ns:
            si = _speech_seconds(spans, t, t + WINDOW_SEC)
            if si <= 0:
                break
            ce = _cluster_end(spans, last, gap=cluster_gap)
            if t + WINDOW_SEC > ce + 0.01:
                prev_si = _speech_seconds(spans, last, last + WINDOW_SEC)
                if prev_si < TAIL_MIN_SPEECH_SEC:
                    break
            if not _add(t):
                break
            last = t
            t = round(last + HOP_SEC, 2)

        hop_ns = round(starts[-1] + HOP_SEC, 2)
        ns = span_ns if span_ns >= hop_ns - 0.01 else hop_ns
        _add(ns)

    last = starts[-1]
    past = 0
    while True:
        t = round(last + HOP_SEC, 2)
        if t in starts or _speech_seconds(spans, t, t + WINDOW_SEC) <= 0:
            break
        ce = _cluster_end(spans, last, gap=cluster_gap)
        if t + WINDOW_SEC > ce + 0.01:
            prev_si = _speech_seconds(spans, last, last + WINDOW_SEC)
            if prev_si < TAIL_MIN_SPEECH_SEC or past >= MAX_TAIL_PAST_CLUSTER:
                break
            past += 1
        if not _add(t):
            break
        last = t

    return sorted(set(starts))


def natural_window_starts(seglst_path) -> list[float]:
    rows = load_speech_seglst_rows(seglst_path)
    spans = [(float(r["start"]), float(r["end"])) for r in rows]
    return natural_window_starts_from_spans(spans)


def speech_weight_sec(spans: list[tuple[float, float]], start: float) -> float:
    return _speech_seconds(spans, start, start + WINDOW_SEC)
