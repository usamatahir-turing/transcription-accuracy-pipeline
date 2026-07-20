"""Build speech-only waveforms from seglst + WAV for DNSMOS windows."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

from diarization_pipeline.seglst_to_rttm import load_speech_seglst_rows


def peak_dbfs(samples: np.ndarray) -> float:
    """Peak level in dBFS (0 = full scale)."""
    peak = float(np.max(np.abs(samples))) if samples.size else 0.0
    if peak < 1e-12:
        return float("-inf")
    return round(20.0 * np.log10(peak), 3)


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

    Silence outside annotated speech is excluded (report §3 / DNSMOS windows).
    Uses the same ``is_speech_segment`` filter as DetER (NSV-only dropped).
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
    }
