"""Effective bandwidth via long-term average spectrum (LTAS).

Estimates the highest frequency with *sustained* speech energy above the
high-frequency noise floor — matching the review-report notion of a cutoff
(not the max FFT bin with any energy).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

# Defaults aligned with the review-report buckets (≤8 / ≤12 / ≤16 kHz).
WARN_8KHZ = 8_000.0
WARN_12KHZ = 12_000.0
WARN_16KHZ = 16_000.0

STFT_MS = 80.0
MARGIN_DB = 12.0
CONTIGUOUS_HZ = 300.0
FLOOR_FRAC = 0.75  # HF floor band starts at this fraction of Nyquist


def bucket_for_hz(effective_hz: float) -> str:
    if effective_hz <= WARN_8KHZ:
        return "le_8khz"
    if effective_hz <= WARN_12KHZ:
        return "le_12khz"
    if effective_hz <= WARN_16KHZ:
        return "le_16khz"
    return "gt_16khz"


def _n_fft_for_sr(sample_rate: int, stft_ms: float = STFT_MS) -> int:
    target = int(round(sample_rate * stft_ms / 1000.0))
    n = 1
    while n < target:
        n <<= 1
    return max(256, n)


def estimate_effective_bandwidth(
    audio: np.ndarray,
    sample_rate: int,
    *,
    margin_db: float = MARGIN_DB,
    contiguous_hz: float = CONTIGUOUS_HZ,
    stft_ms: float = STFT_MS,
    floor_frac: float = FLOOR_FRAC,
) -> dict:
    """Return effective bandwidth and diagnostics for a mono float waveform."""
    audio = np.asarray(audio, dtype=np.float32).reshape(-1)
    nyquist = float(sample_rate) / 2.0

    if audio.size < sample_rate * 0.1:
        return {
            "effective_hz": 0.0,
            "nyquist_hz": nyquist,
            "bucket": "le_8khz",
            "pass": False,
            "hf_floor_db": None,
            "margin_db": margin_db,
            "contiguous_hz": contiguous_hz,
            "n_stft_frames": 0,
            "n_fft": 0,
        }

    import librosa

    n_fft = _n_fft_for_sr(sample_rate, stft_ms)
    hop = max(1, n_fft // 2)
    stft = librosa.stft(audio, n_fft=n_fft, hop_length=hop, window="hann", center=True)
    power = np.abs(stft) ** 2
    n_frames = int(power.shape[1])

    # Sustained spectrum: median across frames (resistant to brief HF spikes).
    ltas = np.median(power, axis=1)
    eps = 1e-20
    ltas_db = 10.0 * np.log10(ltas + eps)

    freqs = librosa.fft_frequencies(sr=sample_rate, n_fft=n_fft)
    # Light smoothing so one bin does not define the cutoff.
    kernel = 5
    if ltas_db.size >= kernel:
        kernel_v = np.ones(kernel, dtype=np.float64) / kernel
        ltas_smooth = np.convolve(ltas_db, kernel_v, mode="same")
    else:
        ltas_smooth = ltas_db

    f_lo = floor_frac * nyquist
    floor_mask = freqs >= f_lo
    if not np.any(floor_mask):
        floor_mask = freqs >= (0.9 * nyquist)
    hf_floor_db = float(np.median(ltas_smooth[floor_mask]))
    threshold = hf_floor_db + margin_db
    above = ltas_smooth >= threshold

    bin_hz = float(freqs[1] - freqs[0]) if len(freqs) > 1 else nyquist
    n_contig = max(1, int(round(contiguous_hz / max(bin_hz, 1e-6))))

    effective_idx = 0
    for i in range(n_contig - 1, len(above)):
        if bool(np.all(above[i - n_contig + 1 : i + 1])):
            effective_idx = i

    effective_hz = float(freqs[effective_idx])
    # Clamp to Nyquist; never report above what the file can hold.
    effective_hz = min(effective_hz, nyquist)
    bucket = bucket_for_hz(effective_hz)

    return {
        "effective_hz": round(effective_hz, 1),
        "nyquist_hz": round(nyquist, 1),
        "bucket": bucket,
        "pass": effective_hz > WARN_8KHZ,
        "hf_floor_db": round(hf_floor_db, 3),
        "margin_db": margin_db,
        "contiguous_hz": contiguous_hz,
        "n_stft_frames": n_frames,
        "n_fft": n_fft,
        "stft_ms": stft_ms,
        "_freqs": freqs,
        "_ltas_db": ltas_smooth,
        "_power": power,
        "_hop": hop,
    }


def save_bandwidth_spectrogram(
    audio: np.ndarray,
    sample_rate: int,
    out_path: Path,
    *,
    effective_hz: float | None = None,
    title: str | None = None,
) -> Path:
    """Write a log-power spectrogram PNG (speech window) for review."""
    import librosa
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    audio = np.asarray(audio, dtype=np.float32).reshape(-1)
    n_fft = _n_fft_for_sr(sample_rate)
    hop = max(1, n_fft // 2)
    # Cap plot length for very long speech (keep ~120 s for readability).
    max_samples = int(sample_rate * 120)
    if audio.size > max_samples:
        audio = audio[:max_samples]

    stft = librosa.stft(audio, n_fft=n_fft, hop_length=hop, window="hann", center=True)
    db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 4), dpi=120)
    img = ax.imshow(
        db,
        origin="lower",
        aspect="auto",
        extent=[0, db.shape[1] * hop / sample_rate, 0, sample_rate / 2],
        cmap="magma",
        vmin=max(-80, float(np.percentile(db, 5))),
        vmax=0,
    )
    ax.set_ylabel("Frequency (Hz)")
    ax.set_xlabel("Time (s)")
    if title:
        ax.set_title(title)
    if effective_hz is not None:
        ax.axhline(effective_hz, color="cyan", linestyle="--", linewidth=1.2, label=f"B≈{effective_hz:.0f} Hz")
        ax.axhline(WARN_8KHZ, color="white", linestyle=":", linewidth=0.8, alpha=0.7, label="8 kHz")
        ax.legend(loc="upper right", fontsize=8)
    fig.colorbar(img, ax=ax, format="%+2.0f dB", pad=0.02)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return out_path
