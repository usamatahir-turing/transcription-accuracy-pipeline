"""Build speech-only DetER reference RTTMs from seglst.json annotations."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

from diarization_pipeline.common import channel_id_from_path, speaker_output_name
from workflow_common import add_scope_args, resolve_speaker_files

DEFAULT_SPEECH_TAGS = frozenset(
    {"unintelligible", "muffled", "foreign", "singing", "redacted"}
)

_TAG_RE = re.compile(r"\[[^\]]*\]")
DER_RTTM_SUFFIX = "_der.rttm"


def _norm_tag(tag: str) -> str:
    return re.sub(r"[\u200b\s]", "", tag.strip("[]")).lower()


def has_real_words(words: str) -> bool:
    no_tags = _TAG_RE.sub(" ", words)
    return any(unicodedata.category(ch)[0] in ("L", "N") for ch in no_tags)


def is_speech_segment(words: str, speech_tags: frozenset[str] = DEFAULT_SPEECH_TAGS) -> bool:
    if has_real_words(words):
        return True
    tags = {_norm_tag(t) for t in _TAG_RE.findall(words)}
    return bool(tags & speech_tags)


def der_rttm_path(seglst_path: Path) -> Path:
    speaker = speaker_output_name(channel_id_from_path(seglst_path))
    return seglst_path.with_name(f"{speaker}{DER_RTTM_SUFFIX}")


def convert_seglst(
    seglst_path: Path,
    rttm_path: Path,
    *,
    file_id: str | None = None,
    speech_tags: frozenset[str] = DEFAULT_SPEECH_TAGS,
) -> tuple[int, int]:
    """Write speech-only RTTM. Returns (n_kept, n_dropped)."""
    segs = json.loads(seglst_path.read_text(encoding="utf-8-sig"))
    if file_id is None:
        file_id = speaker_output_name(channel_id_from_path(seglst_path))
    kept = dropped = 0
    rttm_path.parent.mkdir(parents=True, exist_ok=True)
    with rttm_path.open("w", encoding="utf-8") as fh:
        for seg in segs:
            words = seg.get("words", "")
            if not is_speech_segment(words, speech_tags):
                dropped += 1
                continue
            try:
                start = float(seg["start_time"])
                dur = float(seg["end_time"]) - start
            except (KeyError, TypeError, ValueError):
                dropped += 1
                continue
            if dur <= 0:
                dropped += 1
                continue
            spk = seg.get("speaker", file_id)
            fh.write(
                f"SPEAKER {file_id} 1 {start:.3f} {dur:.3f} <NA> <NA> {spk} <NA> <NA>\n"
            )
            kept += 1
    return kept, dropped


def nonspeech_spans(
    seglst_path: Path,
    speech_tags: frozenset[str] = DEFAULT_SPEECH_TAGS,
) -> list[tuple[float, float]]:
    """``(start, end)`` of turns dropped by :func:`convert_seglst` (NSV-only).

    Used to build a DetER UEM so VAD on audible laughter/breath in those
    intervals is neither a false alarm nor a miss.
    """
    segs = json.loads(seglst_path.read_text(encoding="utf-8-sig"))
    spans: list[tuple[float, float]] = []
    for seg in segs:
        if is_speech_segment(seg.get("words", ""), speech_tags):
            continue
        try:
            start = float(seg["start_time"])
            end = float(seg["end_time"])
        except (KeyError, TypeError, ValueError):
            continue
        if end > start:
            spans.append((start, end))
    return spans


def load_speech_seglst_rows(
    seglst_path: Path,
    speech_tags: frozenset[str] = DEFAULT_SPEECH_TAGS,
) -> list[dict]:
    """Return seglst rows kept as speech, with idx and timing."""
    segs = json.loads(seglst_path.read_text(encoding="utf-8-sig"))
    out: list[dict] = []
    for idx, seg in enumerate(segs):
        words = seg.get("words", "")
        if not is_speech_segment(words, speech_tags):
            continue
        try:
            start = float(seg["start_time"])
            end = float(seg["end_time"])
        except (KeyError, TypeError, ValueError):
            continue
        if end <= start:
            continue
        out.append({
            "idx": idx,
            "start": start,
            "end": end,
            "words": words,
            "duration_s": round(end - start, 3),
        })
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=True)
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

    n_done = n_skipped = 0
    for seglst_path in seglst_files:
        out_path = der_rttm_path(seglst_path)
        if out_path.exists() and not args.overwrite:
            n_skipped += 1
            continue
        kept, dropped = convert_seglst(seglst_path, out_path)
        rel = out_path.relative_to(root)
        print(f"  OK   {rel}  kept={kept}  dropped={dropped}")
        n_done += 1

    print(f"\nDone. {n_done} written, {n_skipped} skipped (exists).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
