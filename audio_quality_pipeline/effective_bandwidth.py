"""Effective bandwidth via annotated STFT (Batch 8/9 QA).

``annotated-stft-v1-nfft2048-hop1024-profile250`` from
``batch8and9review/batch_8_9_numeric_results``:
RTTM-masked STFT frames, adaptive activity threshold, 90 sampled windows,
250 Hz relative profile, cliff cutoff on 0.25 kHz grid.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

# Review-report buckets (≤8 / ≤12 / ≤16 kHz).
WARN_8KHZ = 8_000.0
WARN_12KHZ = 12_000.0
WARN_16KHZ = 16_000.0

ANALYSIS_VERSION = "annotated-stft-v1-nfft2048-hop1024-profile250"
N_FFT = 2048
HOP = 1024
PROFILE_BIN_HZ = 250
PROFILE_LO_HZ = 300.0
N_PROFILE_BINS = 96
SAMPLED_WINDOWS = 90
SPEECH_NORM_BINS = 15  # ~0.3–4 kHz at 250 Hz resolution
ACTIVITY_QUIET_MARGIN_DB = 21.176
ACTIVITY_QUIET_CUTOFF_DB = -77.0
ACTIVITY_LOUD_SILENCE_DB = -64.0
ACTIVITY_LOUD_MARGIN_DB = 8.687
ACTIVITY_DEFAULT_DB = -60.0
CUTOFF_LOOKAHEAD_BINS = 4
CUTOFF_MIN_DROP_DB = 8.0
MIN_CUTOFF_BIN = 31  # ~8.25 kHz — ignore low/mid-band artefacts


def bucket_for_hz(effective_hz: float) -> str:
    if effective_hz <= WARN_8KHZ:
        return "le_8khz"
    if effective_hz <= WARN_12KHZ:
        return "le_12khz"
    if effective_hz <= WARN_16KHZ:
        return "le_16khz"
    return "gt_16khz"


def category_for_khz(effective_khz: float) -> str:
    if effective_khz <= 8.0:
        return "<=8 kHz severe"
    if effective_khz <= 12.0:
        return ">8-12 kHz low"
    if effective_khz <= 16.0:
        return ">12-16 kHz limited"
    return ">16 kHz extended"


def _quantize_khz(khz: float) -> float:
    return round(khz * 4.0) / 4.0


def activity_threshold_db(silence_rms_dbfs: float) -> float:
    """Adaptive threshold from non-RTTM silence RMS (Batch 8/9 style)."""
    if silence_rms_dbfs <= ACTIVITY_QUIET_CUTOFF_DB:
        return silence_rms_dbfs + ACTIVITY_QUIET_MARGIN_DB
    if silence_rms_dbfs <= ACTIVITY_LOUD_SILENCE_DB:
        return ACTIVITY_DEFAULT_DB
    return silence_rms_dbfs + ACTIVITY_LOUD_MARGIN_DB


def _frame_in_spans(frame_idx: int, sample_rate: int, spans: list[tuple[float, float]]) -> bool:
    center = (frame_idx * HOP + N_FFT / 2) / sample_rate
    return any(s <= center <= e for s, e in spans)


def _silence_rms_dbfs(
    audio: np.ndarray,
    sample_rate: int,
    spans: list[tuple[float, float]],
) -> float:
    mask = np.ones(len(audio), dtype=bool)
    for s, e in spans:
        i0 = max(0, int(round(s * sample_rate)))
        i1 = min(len(audio), int(round(e * sample_rate)))
        mask[i0:i1] = False
    silent = audio[mask]
    if silent.size == 0:
        return -80.0
    rms = float(np.sqrt(np.mean(silent.astype(np.float64) ** 2)))
    if rms < 1e-12:
        return -120.0
    return float(20.0 * np.log10(rms))


def _profile_from_stft(power: np.ndarray, sample_rate: int) -> np.ndarray:
    """Mean log-power profile (96 x 250 Hz bins from 300 Hz)."""
    import librosa

    freqs = librosa.fft_frequencies(sr=sample_rate, n_fft=N_FFT)
    eps = 1e-20
    prof = np.zeros(N_PROFILE_BINS, dtype=np.float64)
    for i in range(N_PROFILE_BINS):
        lo = PROFILE_LO_HZ + i * PROFILE_BIN_HZ
        hi = lo + PROFILE_BIN_HZ
        band = (freqs >= lo) & (freqs < hi)
        if not np.any(band):
            continue
        prof[i] = float(np.mean(power[band, :]))
    prof_db = 10.0 * np.log10(prof + eps)
    ref = float(np.mean(prof_db[:SPEECH_NORM_BINS]))
    return prof_db - ref


def _find_cutoff(profile_rel: np.ndarray) -> dict:
    return _find_cutoff_from(
        profile_rel,
        min_bin=MIN_CUTOFF_BIN,
        min_drop=CUTOFF_MIN_DROP_DB,
    )


def _find_cutoff_from(
    profile_rel: np.ndarray,
    *,
    min_bin: int,
    min_drop: float,
) -> dict:
    speech_peak = float(np.max(profile_rel[:SPEECH_NORM_BINS]))
    best_i = min_bin
    best_drop = -1.0
    found = False
    for i in range(N_PROFILE_BINS - CUTOFF_LOOKAHEAD_BINS - 1, min_bin, -1):
        drop = float(profile_rel[i] - profile_rel[i + CUTOFF_LOOKAHEAD_BINS])
        if drop < min_drop:
            continue
        if profile_rel[i] < speech_peak - 45.0:
            continue
        best_i = i
        best_drop = drop
        found = True
        break

    if not found:
        for i in range(N_PROFILE_BINS - CUTOFF_LOOKAHEAD_BINS - 1, min_bin, -1):
            drop = float(profile_rel[i] - profile_rel[i + CUTOFF_LOOKAHEAD_BINS])
            if drop > best_drop:
                best_drop = drop
                best_i = i

    pre = float(profile_rel[best_i])
    post = float(profile_rel[min(best_i + CUTOFF_LOOKAHEAD_BINS, N_PROFILE_BINS - 1)])
    center_hz = PROFILE_LO_HZ + (best_i + 1) * PROFILE_BIN_HZ
    effective_khz = _quantize_khz(center_hz / 1000.0)
    effective_hz = effective_khz * 1000.0

    return {
        "effective_hz": effective_hz,
        "effective_khz": effective_khz,
        "cutoff_drop_db": round(pre - post, 3),
        "pre_cutoff_db_relative": round(pre, 3),
        "post_cutoff_db_relative": round(post, 3),
        "cutoff_bin": best_i,
    }


def estimate_effective_bandwidth(
    audio: np.ndarray,
    sample_rate: int,
    spans: list[tuple[float, float]],
) -> dict:
    """Annotated-STFT effective bandwidth on RTTM-masked frames."""
    audio = np.asarray(audio, dtype=np.float32).reshape(-1)
    nyquist = float(sample_rate) / 2.0

    if audio.size < sample_rate * 0.1 or not spans:
        return {
            "effective_hz": 0.0,
            "effective_khz": 0.0,
            "nyquist_hz": nyquist,
            "bucket": "le_8khz",
            "category": "<=8 kHz severe",
            "pass": False,
            "analysis_version": ANALYSIS_VERSION,
            "n_fft": N_FFT,
            "hop": HOP,
            "profile_bin_hz": PROFILE_BIN_HZ,
            "sampled_windows": 0,
            "activity_threshold_dbfs": None,
            "silence_rms_dbfs": None,
            "cutoff_drop_db": None,
            "n_stft_frames": 0,
        }

    import librosa

    mask = np.zeros(len(audio), dtype=np.float32)
    for s, e in spans:
        i0 = max(0, int(round(s * sample_rate)))
        i1 = min(len(audio), int(round(e * sample_rate)))
        mask[i0:i1] = 1.0
    masked = audio * mask

    stft = librosa.stft(masked, n_fft=N_FFT, hop_length=HOP, window="hann", center=True)
    power = np.abs(stft) ** 2
    n_frames = int(power.shape[1])
    frame_db = 10.0 * np.log10(np.max(power, axis=0) + 1e-20)

    silence_rms = _silence_rms_dbfs(audio, sample_rate, spans)
    act_thr = activity_threshold_db(silence_rms)

    active_idx = [
        i
        for i in range(n_frames)
        if frame_db[i] >= act_thr and _frame_in_spans(i, sample_rate, spans)
    ]
    if not active_idx:
        active_idx = [i for i in range(n_frames) if frame_db[i] >= act_thr]
    if not active_idx:
        return estimate_effective_bandwidth(np.zeros(0, np.float32), sample_rate, [])

    if len(active_idx) > SAMPLED_WINDOWS:
        pick = np.linspace(0, len(active_idx) - 1, SAMPLED_WINDOWS, dtype=int)
        sample_idx = [active_idx[int(i)] for i in pick]
    else:
        sample_idx = active_idx

    sampled_power = power[:, sample_idx]
    profile_rel = _profile_from_stft(sampled_power, sample_rate)
    cutoff = _find_cutoff(profile_rel)
    effective_hz = min(cutoff["effective_hz"], nyquist)
    effective_khz = _quantize_khz(effective_hz / 1000.0)
    effective_hz = effective_khz * 1000.0

    return {
        "effective_hz": effective_hz,
        "effective_khz": effective_khz,
        "nyquist_hz": round(nyquist, 1),
        "bucket": bucket_for_hz(effective_hz),
        "category": category_for_khz(effective_khz),
        "pass": effective_hz > WARN_8KHZ,
        "analysis_version": ANALYSIS_VERSION,
        "n_fft": N_FFT,
        "hop": HOP,
        "profile_bin_hz": PROFILE_BIN_HZ,
        "sampled_windows": len(sample_idx),
        "active_stft_frames": len(active_idx),
        "activity_threshold_dbfs": round(act_thr, 4),
        "silence_rms_dbfs": round(silence_rms, 4),
        "cutoff_drop_db": cutoff["cutoff_drop_db"],
        "pre_cutoff_db_relative": cutoff["pre_cutoff_db_relative"],
        "post_cutoff_db_relative": cutoff["post_cutoff_db_relative"],
        "cutoff_bin": cutoff["cutoff_bin"],
        "n_stft_frames": n_frames,
    }


def save_bandwidth_spectrogram(
    audio: np.ndarray,
    sample_rate: int,
    out_path: Path,
    *,
    effective_hz: float | None = None,
    title: str | None = None,
) -> Path:
    """Write a log-power spectrogram PNG for review."""
    import librosa
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    audio = np.asarray(audio, dtype=np.float32).reshape(-1)
    max_samples = int(sample_rate * 120)
    if audio.size > max_samples:
        audio = audio[:max_samples]

    stft = librosa.stft(audio, n_fft=N_FFT, hop_length=HOP, window="hann", center=True)
    db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 4), dpi=120)
    img = ax.imshow(
        db,
        origin="lower",
        aspect="auto",
        extent=[0, db.shape[1] * HOP / sample_rate, 0, sample_rate / 2],
        cmap="magma",
        vmin=max(-80, float(np.percentile(db, 5))),
        vmax=0,
    )
    ax.set_ylabel("Frequency (Hz)")
    ax.set_xlabel("Time (s)")
    if title:
        ax.set_title(title)
    if effective_hz is not None:
        ax.axhline(
            effective_hz,
            color="cyan",
            linestyle="--",
            linewidth=1.2,
            label=f"B≈{effective_hz:.0f} Hz",
        )
        ax.axhline(WARN_8KHZ, color="white", linestyle=":", linewidth=0.8, alpha=0.7, label="8 kHz")
        ax.legend(loc="upper right", fontsize=8)
    fig.colorbar(img, ax=ax, format="%+2.0f dB", pad=0.02)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return out_path
