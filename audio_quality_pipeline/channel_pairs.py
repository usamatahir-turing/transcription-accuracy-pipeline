"""Pair channel WAVs with seglst files (same folder or a separate seglst root)."""

from __future__ import annotations

from pathlib import Path

from diarization_pipeline.common import channel_id_from_path, speaker_output_name


def iter_wav_seglst_pairs(
    session_dir: Path,
    *,
    seglst_root: Path | None,
) -> list[tuple[Path, Path]]:
    """Return ``(wav_path, seglst_path)`` pairs for this conversation.

    - Default (``seglst_root is None``): discover ``*.seglst.json`` in
      ``session_dir`` and pair with ``{channel_id}.wav`` beside them.
    - With ``seglst_root``: discover ``*.wav`` in ``session_dir`` and look up
      ``seglst_root/<batch>/<session>/{channel_id}.seglst.json``. Missing
      seglst files are skipped (printed).
    """
    pairs: list[tuple[Path, Path]] = []

    if seglst_root is None:
        for seglst_path in sorted(session_dir.glob("*.seglst.json")):
            channel_id = channel_id_from_path(seglst_path)
            wav_path = session_dir / f"{channel_id}.wav"
            pairs.append((wav_path, seglst_path))
        return pairs

    batch = session_dir.parent.name
    session = session_dir.name
    seglst_session = seglst_root / batch / session
    for wav_path in sorted(session_dir.glob("*.wav")):
        channel_id = channel_id_from_path(wav_path)
        seglst_path = seglst_session / f"{channel_id}.seglst.json"
        if not seglst_path.is_file():
            speaker = speaker_output_name(channel_id)
            print(
                f"    SKIP {speaker}: no seglst at "
                f"{seglst_path.as_posix()}"
            )
            continue
        pairs.append((wav_path, seglst_path))
    return pairs
