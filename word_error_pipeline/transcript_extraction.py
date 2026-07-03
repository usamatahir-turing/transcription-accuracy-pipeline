"""Extract per-segment reference transcripts from the seglst.json annotations.

For every ``Conversations/<SESSION>/*.seglst.json`` this writes a row-aligned
``{stem}_transcript.jsonl`` next to it. Each line is one segment, in original order,
carrying everything the downstream pipeline needs:

    {"idx", "session_id", "language", "speaker", "start", "end", "text"}

Notes
-----
- ``text`` is kept RAW (NSV tokens like [laugh]/[inhale] are preserved). The
  normalization / NSV-stripping happens in a later stage so both the reference
  and the Qwen3-ASR hypothesis go through the *same* normalizer.
- One row is emitted per segment, including empty / NSV-only ones, so this file
  stays index-aligned with the Qwen hypothesis file produced later (which slices
  each SPK*.wav by these same start/end times).

Usage
-----
    python -m word_error_pipeline.transcript_extraction
    python -m word_error_pipeline.transcript_extraction --batch delivery_batch_06092026
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from workflow_common import add_scope_args, resolve_speaker_files


def derive_language(session_id: str) -> str:
    """Language code is the 2nd token of the session name, e.g. NV-AR-SS03-CONVO09 -> AR."""
    parts = session_id.split("-")
    return parts[1] if len(parts) >= 2 else "UNK"


def to_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def extract_file(seglst_path: Path) -> tuple[Path, int, str]:
    """Convert a single .seglst.json into a row-aligned _transcript.jsonl.

    Returns (output_path, n_segments, language).
    """
    raw = seglst_path.read_text(encoding="utf-8")
    segments = json.loads(raw)
    if not isinstance(segments, list):
        raise ValueError(f"{seglst_path} did not contain a JSON array of segments")

    session_id = seglst_path.parent.name
    language = derive_language(session_id)
    speaker = seglst_path.name[: -len(".seglst.json")]

    out_path = seglst_path.with_name(f"{speaker}_transcript.jsonl")
    with out_path.open("w", encoding="utf-8") as out:
        for idx, seg in enumerate(segments):
            row = {
                "idx": idx,
                "session_id": seg.get("session_id", session_id),
                "language": language,
                "speaker": seg.get("speaker", speaker),
                "start": to_float(seg.get("start_time")),
                "end": to_float(seg.get("end_time")),
                "text": seg.get("words", ""),
            }
            out.write(json.dumps(row, ensure_ascii=False))
            out.write("\n")

    return out_path, len(segments), language


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
    if not seglst_files:
        print(f"No *.seglst.json files found for the given scope under {root.resolve()}")
        return 1
    if args.limit > 0:
        seglst_files = seglst_files[: args.limit]

    total_segments = 0
    per_language: Counter[str] = Counter()
    skipped = 0
    print(f"Found {len(seglst_files)} seglst file(s).\n")

    for seglst_path in seglst_files:
        out_check = seglst_path.with_name(
            seglst_path.name[: -len(".seglst.json")] + "_transcript.jsonl")
        if out_check.exists() and not args.overwrite:
            skipped += 1
            continue
        try:
            out_path, n_segments, language = extract_file(seglst_path)
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"  FAIL {seglst_path}: {exc}")
            continue
        total_segments += n_segments
        per_language[language] += n_segments
        rel = out_path.relative_to(root)
        print(f"  OK   {rel}  ({n_segments} segments)")

    print(
        f"\nDone. {len(seglst_files) - skipped} file(s) written, {skipped} skipped, "
        f"{total_segments} segments total."
    )
    print("Segments per language:")
    for lang in sorted(per_language):
        print(f"  {lang}: {per_language[lang]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
