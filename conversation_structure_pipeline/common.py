"""Shared overlap-ratio utilities (from chsep_audio_qa/ami_rttm_stats.py)."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import soundfile as sf


def compute_overlap_ratio(
    segments: Iterable[tuple[float, float, str]],
) -> tuple[float, float, float, float]:
    """Compute speech / overlap durations for one session timeline.

    Returns (T_speech, T_overlap, T_filespan, overlap_ratio) where overlap_ratio
    is T_overlap / T_speech (0 if no speech). Sweep-line over segment endpoints.
    """
    events: list[tuple[float, int]] = []
    for start, dur, _spk in segments:
        events.append((start, +1))
        events.append((start + dur, -1))
    if not events:
        return 0.0, 0.0, 0.0, 0.0

    events.sort()
    total_speech = 0.0
    total_overlap = 0.0
    active = 0
    prev_t = events[0][0]
    min_t = events[0][0]
    max_t = events[0][0]
    for t, delta in events:
        if t > prev_t and active > 0:
            span = t - prev_t
            total_speech += span
            if active >= 2:
                total_overlap += span
        active += delta
        prev_t = t
        if t > max_t:
            max_t = t
    file_span = max(0.0, max_t - min_t)
    ratio = (total_overlap / total_speech) if total_speech > 0 else 0.0
    return total_speech, total_overlap, file_span, ratio


def wav_duration_s(path: Path) -> float:
    """Return audio file duration in seconds."""
    with sf.SoundFile(str(path)) as f:
        return f.frames / float(f.samplerate)


def resolve_total_audio_s(
    session_dir: Path, speaker_stems: list[str],
) -> tuple[float, str | None]:
    """Mixed ``*_mixed.wav`` duration, else max duration among speaker ``*.wav``."""
    mixed_files = sorted(session_dir.glob("*_mixed.wav"))
    if mixed_files:
        path = mixed_files[0]
        return round(wav_duration_s(path), 3), path.name

    best = 0.0
    for stem in speaker_stems:
        wav = session_dir / f"{stem}.wav"
        if not wav.is_file():
            continue
        best = max(best, wav_duration_s(wav))
    if best > 0:
        return round(best, 3), "max_speaker_wav"
    return 0.0, None
