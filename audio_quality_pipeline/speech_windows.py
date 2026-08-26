"""Build speech-masked waveforms from seglst + WAV for DNSMOS / bandwidth."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

from diarization_pipeline.seglst_to_rttm import load_speech_seglst_rows


def peak_dbfs(samples: np.ndarray, *, round_db: bool = True) -> float:
    """Peak level in dBFS (0 = full scale)."""
    peak = float(np.max(np.abs(samples))) if samples.size else 0.0
    if peak < 1e-12:
        return float("-inf")
    db = 20.0 * np.log10(peak)
    return round(db, 3) if round_db else float(db)


def rms_dbfs(samples: np.ndarray) -> float:
    """RMS level in dBFS (0 = full scale)."""
    if samples.size == 0:
        return float("-inf")
    rms = float(np.sqrt(np.mean(np.square(samples))))
    if rms < 1e-12:
        return float("-inf")
    return round(20.0 * np.log10(rms), 3)


def speech_level_stats(
    samples: np.ndarray,
    *,
    clip_threshold: float = 0.9999,
) -> dict:
    """Batch 8/9 clipping stats on a speech sample vector (linear peak + full-scale count)."""
    speech = np.asarray(samples, dtype=np.float64).reshape(-1)
    if speech.size == 0:
        return {
            "speech_peak": None,
            "speech_peak_dbfs": None,
            "full_scale_samples": 0,
            "speech_samples": 0,
            "speech_sum_squares": 0.0,
            "full_scale_clipped_sample_ratio": 0.0,
        }

    peak_lin = float(np.max(np.abs(speech)))
    if peak_lin < 1e-12:
        peak_dbfs_val = float("-inf")
    else:
        peak_dbfs_val = float(20.0 * np.log10(peak_lin))
    n_speech = int(speech.size)
    n_full_scale = int(np.sum(np.abs(speech) >= clip_threshold))
    ratio = float(n_full_scale / n_speech) if n_speech else 0.0
    return {
        "speech_peak": peak_lin,
        "speech_peak_dbfs": peak_dbfs_val,
        "full_scale_samples": n_full_scale,
        "speech_samples": n_speech,
        "speech_sum_squares": float(np.sum(speech * speech)),
        "full_scale_clipped_sample_ratio": ratio,
    }


def is_full_scale_clipped(
    *,
    full_scale_samples: int = 0,
    speech_peak_dbfs: float | None = None,
) -> bool:
    """Client clipping flag: any full-scale sample, or peak exactly at 0 dBFS."""
    if full_scale_samples > 0:
        return True
    return speech_peak_dbfs is not None and speech_peak_dbfs == 0.0


def channel_speech_level_stats(
    audio: np.ndarray,
    sample_rate: int,
    spans: list[tuple[float, float]] | None,
    *,
    clip_threshold: float = 0.9999,
) -> dict:
    """Clipping stats on all annotated speech in a channel."""
    audio = np.asarray(audio, dtype=np.float64).reshape(-1)
    if not spans:
        return speech_level_stats(np.zeros(0), clip_threshold=clip_threshold)

    chunks: list[np.ndarray] = []
    for start, end in spans:
        i0 = max(0, int(round(start * sample_rate)))
        i1 = min(len(audio), int(round(end * sample_rate)))
        if i1 > i0:
            chunks.append(audio[i0:i1])
    if not chunks:
        return speech_level_stats(np.zeros(0), clip_threshold=clip_threshold)
    return speech_level_stats(
        np.concatenate(chunks), clip_threshold=clip_threshold,
    )


def _speech_chunks_in_window(
    audio: np.ndarray,
    sample_rate: int,
    spans: list[tuple[float, float]],
    start_sec: float,
    end_sec: float,
    *,
    max_speech_sec: float | None = None,
) -> list[np.ndarray]:
    """Annotated speech inside ``[start_sec, end_sec]``, optionally capped by duration."""
    audio = np.asarray(audio, dtype=np.float64).reshape(-1)
    chunks: list[np.ndarray] = []
    budget = max_speech_sec

    for span_start, span_end in spans:
        overlap_start = max(span_start, start_sec)
        overlap_end = min(span_end, end_sec)
        if overlap_end <= overlap_start:
            continue

        seg_dur = overlap_end - overlap_start
        if max_speech_sec is not None:
            if budget is None or budget <= 0:
                break
            take_dur = min(seg_dur, budget)
            overlap_end = overlap_start + take_dur
            budget -= take_dur

        i0 = max(0, int(round(overlap_start * sample_rate)))
        i1 = min(len(audio), int(round(overlap_end * sample_rate)))
        if i1 > i0:
            chunks.append(audio[i0:i1])

    return chunks


def window_speech_level_stats(
    audio: np.ndarray,
    sample_rate: int,
    start_sec: float,
    end_sec: float,
    spans: list[tuple[float, float]] | None,
    *,
    clip_threshold: float = 0.9999,
    speech_only_slice: bool = False,
    max_speech_sec: float | None = None,
) -> dict:
    """Clipping stats on annotated speech inside a DNSMOS window.

    When ``max_speech_sec`` is set (Batch 8/9 natural-window weight), clipping is
    measured on the first ``max_speech_sec`` of annotated speech between
    ``start_sec`` and ``end_sec`` (callers pass ``start_sec`` past the 0.5 s
    context pad for natural windows).
    """
    audio = np.asarray(audio, dtype=np.float64).reshape(-1)

    if speech_only_slice:
        i0 = max(0, int(round(start_sec * sample_rate)))
        i1 = min(len(audio), int(round(end_sec * sample_rate)))
        chunks = [audio[i0:i1]] if i1 > i0 else []
    elif spans:
        weight = max_speech_sec if max_speech_sec is not None else None
        chunks = _speech_chunks_in_window(
            audio, sample_rate, spans, start_sec, end_sec,
            max_speech_sec=weight,
        )
    else:
        chunks = []

    if not chunks:
        return speech_level_stats(np.zeros(0), clip_threshold=clip_threshold)
    return speech_level_stats(
        np.concatenate(chunks), clip_threshold=clip_threshold,
    )


def load_mono_wav(wav_path: Path) -> tuple[np.ndarray, int]:
    audio, sr = sf.read(str(wav_path), dtype="float32", always_2d=False)
    if getattr(audio, "ndim", 1) > 1:
        audio = np.mean(audio, axis=1)
    return np.asarray(audio, dtype=np.float32), int(sr)


def extract_speech_audio(
    wav_path: Path,
    seglst_path: Path,
) -> dict:
    """Concatenate speech-only seglst intervals from ``wav_path``.

    Silence outside annotated speech is excluded. Uses the same
    ``is_speech_segment`` filter as DetER (NSV-only dropped).
    """
    audio, sr = load_mono_wav(wav_path)
    rows = load_speech_seglst_rows(seglst_path)
    chunks: list[np.ndarray] = []
    for row in rows:
        i0 = max(0, int(round(row["start"] * sr)))
        i1 = min(len(audio), int(round(row["end"] * sr)))
        if i1 > i0:
            chunks.append(audio[i0:i1])

    if not chunks:
        speech = np.zeros(0, dtype=np.float32)
        speech_s = 0.0
    else:
        speech = np.concatenate(chunks)
        speech_s = float(len(speech) / sr)

    return {
        "audio": speech,
        "sample_rate": sr,
        "speech_s": round(speech_s, 3),
        "speech_min": round(speech_s / 60.0, 3),
        "peak_dbfs": peak_dbfs(speech) if speech.size else None,
        "n_speech_segments": len(rows),
        "n_samples": int(speech.size),
        "mode": "speech_concat",
    }


def extract_speech_timeline_audio(
    wav_path: Path,
    seglst_path: Path,
) -> dict:
    """Zero non-speech regions but keep the full file timeline.

    Speech seglst intervals (NSV-only dropped) stay intact; everything else is
    set to zero so DNSMOS still hears gating / dead-air between turns — closer
    to client report SIG than tight speech concatenation.
    """
    audio, sr = load_mono_wav(wav_path)
    rows = load_speech_seglst_rows(seglst_path)
    mask = np.zeros(len(audio), dtype=np.float32)
    speech_samples = 0
    for row in rows:
        i0 = max(0, int(round(row["start"] * sr)))
        i1 = min(len(audio), int(round(row["end"] * sr)))
        if i1 > i0:
            mask[i0:i1] = 1.0
            speech_samples += i1 - i0

    masked = audio * mask
    speech_s = float(speech_samples / sr) if sr else 0.0
    speech_peak = peak_dbfs(masked) if speech_samples else None

    return {
        "audio": masked,
        "sample_rate": sr,
        "speech_s": round(speech_s, 3),
        "speech_min": round(speech_s / 60.0, 3),
        "peak_dbfs": speech_peak,
        "n_speech_segments": len(rows),
        "n_samples": int(speech_samples),
        "file_s": round(len(audio) / sr, 3) if sr else 0.0,
        "mode": "speech_timeline",
    }
