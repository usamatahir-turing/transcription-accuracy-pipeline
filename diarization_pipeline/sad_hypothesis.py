"""Speech-activity detection hypothesis RTTMs for DetER scoring.

Writes ``SPK*_sad.rttm`` next to each ``SPK*.wav``.

Usage
-----
    python -m diarization_pipeline.sad_hypothesis --conversation NV-KO-SS03-CONVO08
    python -m diarization_pipeline.sad_hypothesis --sad-mode union --conversation NV-KO-SS03-CONVO08
    python -m diarization_pipeline.sad_hypothesis --sad-mode sortformer --conversation NV-KO-SS03-CONVO08
    python -m diarization_pipeline.sad_hypothesis --sad-mode silero --conversation NV-KO-SS03-CONVO08
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from diarization_pipeline.common import (
    SAD_MODES,
    SadMode,
    channel_id_from_path,
    merge_segments,
    sad_rttm_path,
    speaker_output_name,
    write_rttm,
)
from workflow_common import add_scope_args, resolve_speaker_files

_sortformer_model = None
_silero_model = None
_silero_unavailable = False


def add_sad_mode_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--sad-mode",
        choices=SAD_MODES,
        default="union",
        help="SAD hypothesis: sortformer, silero, or union of both (default: union).",
    )


def _get_sortformer_model():
    global _sortformer_model
    if _sortformer_model is None:
        from nemo.collections.asr.models import SortformerEncLabelModel

        repo = "nvidia/diar_streaming_sortformer_4spk-v2.1"
        print(f"Loading Sortformer ({repo}) …")
        t0 = time.time()
        _sortformer_model = SortformerEncLabelModel.from_pretrained(repo)
        _sortformer_model.eval()
        _sortformer_model.sortformer_modules.chunk_len = 340
        _sortformer_model.sortformer_modules.chunk_right_context = 40
        _sortformer_model.sortformer_modules.fifo_len = 40
        _sortformer_model.sortformer_modules.spkcache_update_period = 300
        print(f"Sortformer loaded in {time.time() - t0:.1f}s")
    return _sortformer_model


def _get_torch_device():
    import torch
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def silero_available() -> bool:
    return _get_silero_model() is not None


def _get_silero_model():
    global _silero_model, _silero_unavailable
    if _silero_unavailable:
        return None
    if _silero_model is None:
        import torch
        device = _get_torch_device()
        print(f"Loading Silero VAD (device={device}) …")
        try:
            model, utils = torch.hub.load(
                repo_or_dir="snakers4/silero-vad",
                model="silero_vad",
                trust_repo=True,
                onnx=False,
            )
        except (ImportError, OSError) as exc:
            _silero_unavailable = True
            print(f"WARNING: Silero unavailable ({exc}).")
            return None
        model = model.to(device)
        model._utils = utils
        _silero_model = model
    return _silero_model


def wav_sample_rate(wav_path: Path) -> int:
    with sf.SoundFile(str(wav_path)) as f:
        return int(f.samplerate)


def _segs_str_to_tuples(segs: list[str]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for s in segs:
        parts = s.split()
        out.append((float(parts[0]), float(parts[1])))
    return out


def _run_sortformer(audio_path: Path, batch_size: int = 1) -> list[str]:
    model = _get_sortformer_model()
    return model.diarize(audio=[str(audio_path)], batch_size=batch_size)[0]


def _load_wav_for_silero(audio_path: Path, declared_sr: int):
    import torch

    device = _get_torch_device()
    w, file_sr = sf.read(str(audio_path), dtype="float32")
    if w.ndim > 1:
        w = w[:, 0]
    silero_sr = 8000 if declared_sr == 8000 else 16000
    if file_sr != silero_sr:
        try:
            import torchaudio
            t = torch.from_numpy(w.copy()).float().to(device)
            t = torchaudio.functional.resample(
                t.unsqueeze(0), file_sr, silero_sr,
            ).squeeze(0)
            return t, silero_sr
        except ImportError:
            ratio = silero_sr / file_sr
            n = int(round(len(w) * ratio))
            x_old = np.linspace(0, 1, num=len(w), endpoint=False)
            x_new = np.linspace(0, 1, num=n, endpoint=False)
            w = np.interp(x_new, x_old, w).astype(np.float32)
    t = torch.from_numpy(np.ascontiguousarray(w)).float().to(device)
    return t, silero_sr


def _run_silero(audio_path: Path, declared_sr: int) -> list[str]:
    model = _get_silero_model()
    if model is None:
        return []
    get_speech_timestamps = model._utils[0]
    wav, silero_sr = _load_wav_for_silero(audio_path, declared_sr)
    timestamps = get_speech_timestamps(
        wav, model, sampling_rate=silero_sr, return_seconds=True,
    )
    return [f"{ts['start']:.3f} {ts['end']:.3f} speech" for ts in timestamps]


def run_sad(
    audio_path: Path,
    declared_sr: int,
    mode: SadMode = "union",
    batch_size: int = 1,
) -> dict:
    """Build SAD segments for the requested mode."""
    sf_merged: list[tuple[float, float]] = []
    si_merged: list[tuple[float, float]] = []

    if mode in ("sortformer", "union"):
        sf_raw = _run_sortformer(audio_path, batch_size=batch_size)
        sf_merged = merge_segments(sorted(_segs_str_to_tuples(sf_raw)))

    if mode in ("silero", "union"):
        si_raw = _run_silero(audio_path, declared_sr)
        si_merged = merge_segments(sorted(_segs_str_to_tuples(si_raw)))
        if mode == "silero" and not si_merged:
            raise RuntimeError(
                "Silero VAD unavailable or returned no segments; "
                "install torchaudio or use --sad-mode sortformer."
            )

    if mode == "sortformer":
        segments = sf_merged
    elif mode == "silero":
        segments = si_merged
    else:
        segments = merge_segments(sf_merged + si_merged)

    return {
        "sad_mode": mode,
        "sortformer_segments": len(sf_merged),
        "silero_segments": len(si_merged),
        "hyp_segments": len(segments),
        "segments": segments,
    }


def write_sad_rttm(
    audio_path: Path,
    out_path: Path,
    declared_sr: int,
    mode: SadMode = "union",
    batch_size: int = 1,
) -> dict:
    stats = run_sad(audio_path, declared_sr, mode=mode, batch_size=batch_size)
    file_id = speaker_output_name(channel_id_from_path(audio_path))
    write_rttm(stats["segments"], out_path, file_id=file_id, speaker_label="speech")
    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=True)
    add_sad_mode_arg(parser)
    parser.add_argument("--batch-size", type=int, default=40,
                        help="Sortformer batch size (default: 40).")
    args = parser.parse_args(argv)

    root = Path(args.conversations)
    try:
        seglst_files = resolve_speaker_files(
            root, args.batch, args.conversation, args.file, ".seglst.json")
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit > 0:
        seglst_files = seglst_files[: args.limit]

    n_done = n_skipped = n_fail = 0
    for seglst_path in seglst_files:
        channel_id = channel_id_from_path(seglst_path)
        speaker = speaker_output_name(channel_id)
        wav_path = seglst_path.with_name(f"{channel_id}.wav")
        out_path = sad_rttm_path(seglst_path)
        if out_path.exists() and not args.overwrite:
            n_skipped += 1
            continue
        if not wav_path.is_file():
            print(f"  SKIP {seglst_path.parent.name}/{speaker}: no {wav_path.name}")
            n_fail += 1
            continue
        sr = wav_sample_rate(wav_path)
        try:
            stats = write_sad_rttm(
                wav_path, out_path, sr,
                mode=args.sad_mode, batch_size=args.batch_size,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {seglst_path.parent.name}/{speaker}: {exc}")
            n_fail += 1
            continue
        print(
            f"  OK   {out_path.relative_to(root)}  mode={stats['sad_mode']}  "
            f"sf={stats['sortformer_segments']} si={stats['silero_segments']} "
            f"hyp={stats['hyp_segments']}"
        )
        n_done += 1

    print(f"\nDone. {n_done} written, {n_skipped} skipped, {n_fail} failed.")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
