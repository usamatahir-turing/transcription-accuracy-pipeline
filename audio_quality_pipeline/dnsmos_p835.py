"""DNSMOS P.835 (SIG / BAK / OVRL) via Microsoft's ``sig_bak_ovr.onnx``.

Inference follows ``microsoft/DNS-Challenge`` ``DNSMOS/dnsmos_local.py``.
Default polyfit is **personalized** (``-p`` in the Microsoft script), which
matched client-report SIG best with speech-timeline masking.
Uses ``onnxruntime`` with CUDA when available.
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

import numpy as np

SAMPLING_RATE = 16_000
INPUT_LENGTH = 9.01
SIG_WARN_MIN = 3.0

# Official model from Microsoft DNS-Challenge (P.835 primary). Nested path
# DNSMOS/DNSMOS/ — GitHub may serve LFS pointers via raw URLs, so we try
# Microsoft first then a public mirror.
_MODEL_URLS = (
    "https://github.com/microsoft/DNS-Challenge/raw/master/DNSMOS/DNSMOS/sig_bak_ovr.onnx",
    "https://huggingface.co/Vyvo-Research/dnsmos/resolve/main/sig_bak_ovr.onnx",
)
_MODEL_DIR = Path(__file__).resolve().parent / "models"
_MODEL_NAME = "sig_bak_ovr.onnx"

# Personalized polyfit (dnsmos_local.py ``is_personalized_MOS=True``).
_P_SIG_PERS = np.poly1d([-0.01019296, 0.02751166, 1.19576786, -0.24348726])
_P_BAK_PERS = np.poly1d([-0.04976499, 0.44276479, -0.1644611, 0.96883132])
_P_OVR_PERS = np.poly1d([-0.00533021, 0.005101, 1.18058466, -0.11236046])

# Non-personalized polyfit (dnsmos_local.py default).
_P_SIG = np.poly1d([-0.08397278, 1.22083953, 0.0052439])
_P_BAK = np.poly1d([-0.13166888, 1.60915514, -0.39604546])
_P_OVR = np.poly1d([-0.06766283, 1.11546468, 0.04602535])

_session = None
_session_device = ""


def default_model_path() -> Path:
    return _MODEL_DIR / _MODEL_NAME


def _looks_like_onnx(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size < 10_000:
        return False
    # Reject Git LFS pointer text files.
    head = path.read_bytes()[:100]
    return not head.startswith(b"version https://git-lfs.github.com")


def ensure_model(model_path: Path | None = None) -> Path:
    """Download ``sig_bak_ovr.onnx`` into ``models/`` if missing."""
    path = Path(model_path) if model_path else default_model_path()
    if _looks_like_onnx(path):
        return path
    if path.exists():
        path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    last_err: Exception | None = None
    for url in _MODEL_URLS:
        try:
            print(f"Downloading DNSMOS P.835 model from {url} ...")
            urllib.request.urlretrieve(url, path)
            if _looks_like_onnx(path):
                return path
            path.unlink(missing_ok=True)
            last_err = RuntimeError(f"downloaded file is not a valid ONNX: {url}")
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            path.unlink(missing_ok=True)
    raise RuntimeError(
        f"Failed to download DNSMOS model to {path}. Last error: {last_err}"
    )


def _preload_cuda_dlls() -> None:
    """Load pip-installed NVIDIA CUDA/cuDNN DLLs into the process (Windows)."""
    import onnxruntime as ort

    if not hasattr(ort, "preload_dlls"):
        return
    try:
        ort.preload_dlls(cuda=True, cudnn=True, msvc=True)
    except Exception as exc:  # noqa: BLE001
        print(f"DNSMOS CUDA DLL preload skipped ({exc})")


def get_session(model_path: Path | None = None):
    """Lazy-load ONNX session (GPU preferred, CPU fallback)."""
    global _session, _session_device
    if _session is not None:
        return _session

    import onnxruntime as ort

    path = ensure_model(model_path)
    _preload_cuda_dlls()
    available = ort.get_available_providers()
    # Prefer CUDA when listed, but load CPU-only if CUDA DLLs fail (common on
    # machines without matching CUDA/cuDNN). Avoids noisy ORT stderr spam.
    if "CUDAExecutionProvider" in available:
        try:
            _session = ort.InferenceSession(
                str(path), providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
            )
            if "CUDAExecutionProvider" in _session.get_providers():
                active = _session.get_providers()
                _session_device = active[0]
                print(f"DNSMOS ONNX providers: {active}")
                return _session
        except Exception as exc:  # noqa: BLE001
            print(f"DNSMOS CUDA unavailable ({exc}); using CPU.")
            _session = None

    _session = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])
    active = _session.get_providers()
    _session_device = active[0] if active else "unknown"
    print(f"DNSMOS ONNX providers: {active}")
    return _session


def session_device() -> str:
    get_session()
    return _session_device


def _polyfit(
    sig_raw: float,
    bak_raw: float,
    ovr_raw: float,
    *,
    personalized: bool,
) -> tuple[float, float, float]:
    if personalized:
        return (
            float(_P_SIG_PERS(sig_raw)),
            float(_P_BAK_PERS(bak_raw)),
            float(_P_OVR_PERS(ovr_raw)),
        )
    return float(_P_SIG(sig_raw)), float(_P_BAK(bak_raw)), float(_P_OVR(ovr_raw))


def score_audio(
    audio: np.ndarray,
    sample_rate: int,
    *,
    model_path: Path | None = None,
    personalized: bool = True,
) -> dict:
    """Score a mono float waveform with DNSMOS P.835.

    Returns mean SIG/BAK/OVRL over 9.01 s hops (1 s hop), plus raw means and
    hop count. Audio shorter than 9.01 s is repeated (Microsoft script behaviour).

    ``personalized=True`` uses the cubic polyfit from Microsoft ``dnsmos_local.py
    -p`` (default here after client-report calibration).
    """
    if audio.ndim > 1:
        audio = np.mean(audio, axis=-1)
    audio = np.asarray(audio, dtype=np.float64).reshape(-1)
    if audio.size == 0:
        raise ValueError("empty audio for DNSMOS")

    import librosa

    fs = SAMPLING_RATE
    if sample_rate != fs:
        audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=fs)
    audio = np.asarray(audio, dtype=np.float64)

    len_samples = int(INPUT_LENGTH * fs)
    while len(audio) < len_samples:
        audio = np.append(audio, audio)

    num_hops = int(np.floor(len(audio) / fs) - INPUT_LENGTH) + 1
    if num_hops < 1:
        num_hops = 1

    sess = get_session(model_path)
    hop_len = fs
    sig_raw_l: list[float] = []
    bak_raw_l: list[float] = []
    ovr_raw_l: list[float] = []
    sig_l: list[float] = []
    bak_l: list[float] = []
    ovr_l: list[float] = []

    for idx in range(num_hops):
        start = int(idx * hop_len)
        end = start + len_samples
        if end > len(audio):
            break
        seg = audio[start:end]
        if len(seg) < len_samples:
            continue
        feats = np.asarray(seg, dtype=np.float32)[np.newaxis, :]
        mos_sig_raw, mos_bak_raw, mos_ovr_raw = sess.run(
            None, {"input_1": feats})[0][0]
        mos_sig, mos_bak, mos_ovr = _polyfit(
            float(mos_sig_raw),
            float(mos_bak_raw),
            float(mos_ovr_raw),
            personalized=personalized,
        )
        sig_raw_l.append(float(mos_sig_raw))
        bak_raw_l.append(float(mos_bak_raw))
        ovr_raw_l.append(float(mos_ovr_raw))
        sig_l.append(mos_sig)
        bak_l.append(mos_bak)
        ovr_l.append(mos_ovr)

    if not sig_l:
        # Single truncated segment fallback (should be rare after padding).
        seg = audio[:len_samples]
        feats = np.asarray(seg, dtype=np.float32)[np.newaxis, :]
        mos_sig_raw, mos_bak_raw, mos_ovr_raw = sess.run(
            None, {"input_1": feats})[0][0]
        mos_sig, mos_bak, mos_ovr = _polyfit(
            float(mos_sig_raw),
            float(mos_bak_raw),
            float(mos_ovr_raw),
            personalized=personalized,
        )
        sig_l = [mos_sig]
        bak_l = [mos_bak]
        ovr_l = [mos_ovr]
        sig_raw_l = [float(mos_sig_raw)]
        bak_raw_l = [float(mos_bak_raw)]
        ovr_raw_l = [float(mos_ovr_raw)]

    sig = float(np.mean(sig_l))
    bak = float(np.mean(bak_l))
    ovrl = float(np.mean(ovr_l))
    return {
        "sig": round(sig, 6),
        "bak": round(bak, 6),
        "ovrl": round(ovrl, 6),
        "sig_raw": round(float(np.mean(sig_raw_l)), 6),
        "bak_raw": round(float(np.mean(bak_raw_l)), 6),
        "ovrl_raw": round(float(np.mean(ovr_raw_l)), 6),
        "n_hops": len(sig_l),
        "pass": sig > SIG_WARN_MIN,
        "threshold_sig": SIG_WARN_MIN,
        "personalized": personalized,
        "device": session_device(),
    }
