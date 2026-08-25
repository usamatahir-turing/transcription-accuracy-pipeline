"""Load per-channel RTTM annotation intervals."""

from __future__ import annotations

from pathlib import Path


def load_rttm_spans(rttm_path: Path) -> list[tuple[float, float]]:
    """Return ``(start_s, end_s)`` intervals from a NIST RTTM file."""
    spans: list[tuple[float, float]] = []
    if not rttm_path.is_file():
        return spans
    for line in rttm_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("SPEAKER"):
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        start = float(parts[3])
        dur = float(parts[4])
        if dur <= 0:
            continue
        spans.append((start, start + dur))
    spans.sort(key=lambda x: x[0])
    return spans


def rttm_speech_seconds(spans: list[tuple[float, float]]) -> float:
    return float(sum(e - s for s, e in spans))


def rttm_path_for_channel(session_dir: Path, channel_id: str) -> Path:
    return session_dir / f"{channel_id}.rttm"
