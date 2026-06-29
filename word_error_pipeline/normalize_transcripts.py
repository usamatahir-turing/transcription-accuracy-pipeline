"""Normalize reference + Qwen transcripts for WER/CER/WCMR scoring.

For every ``Conversations/<SESSION>/SPK*_transcript.jsonl`` and its sibling
``SPK*_qwen.jsonl`` this writes two row-aligned outputs:

    SPK*_transcript_norm.jsonl   (normalized reference)
    SPK*_qwen_norm.jsonl         (normalized hypothesis)

Normalization track (same as Sample_review_report_06042026.md):
  1. OpenAI Whisper BasicTextNormalizer (lower-case, NFKC, brackets/punctuation
     stripped, diacritics preserved). This also removes well-formed NSV like
     [laugh] / [breath].
  2. Language-specific filler / backchannel stripping via ``filler_removal.py``
     (pure vocalizations and backchannels only; discourse markers are kept).
  3. Japanese only: morpheme-spaced text is re-tokenized for scoring — all
     whitespace is removed, then a space is inserted between every character.

Empty / filler-only handling: rows are never deleted. Every row is kept and
flagged with ``scored`` (bool) and ``drop_reason``. The decision is anchored on
the REFERENCE and copied to the hypothesis row. A scored row may still have
an empty hypothesis (Qwen missed real speech) -> that correctly counts later.

Usage
-----
    .\\.venv\\Scripts\\python.exe normalize_transcripts.py
    .\\.venv\\Scripts\\python.exe normalize_transcripts.py --conversation NV-AR-SS03-CONVO09
    .\\.venv\\Scripts\\python.exe normalize_transcripts.py --conversation NV-AR-SS03-CONVO09 --file SPK01
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from word_error_pipeline.filler_removal import (
    canonicalize_lang,
    normalize_text,
    strip_fillers_from_normalized,
)
from workflow_common import add_scope_args, resolve_speaker_files

_NO_SPACE_LANGS = frozenset({"JA"})


def _collapse_all_space(s: str) -> str:
    return re.sub(r"\s+", "", s)


def scoring_repr(text: str, lang: str) -> str:
    """Final text_norm form used by compute_metrics / rank_error_segments."""
    if lang not in _NO_SPACE_LANGS:
        return text
    collapsed = _collapse_all_space(text)
    return " ".join(collapsed) if collapsed else ""


def normalize_segment(text: str, lang: str) -> dict:
    """Return {norm, drop_reason_self} for one segment."""
    whisper = normalize_text(text)
    if not whisper:
        return {"norm": "", "drop_reason_self": "empty"}

    stripped = strip_fillers_from_normalized(whisper, lang)
    if not stripped:
        return {"norm": "", "drop_reason_self": "filler_only"}

    return {
        "norm": scoring_repr(stripped, lang),
        "drop_reason_self": None,
    }


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_norm_jsonl(path: Path, rows: list[dict], norms: list[dict],
                     scored_flags: list[bool], reasons: list) -> None:
    with path.open("w", encoding="utf-8") as out:
        for row, nrm, scored, reason in zip(rows, norms, scored_flags, reasons):
            obj = {
                "idx": row["idx"],
                "session_id": row["session_id"],
                "language": row["language"],
                "speaker": row["speaker"],
                "start": row["start"],
                "end": row["end"],
                "text": row.get("text", ""),
                "text_norm": nrm["norm"],
                "scored": scored,
                "drop_reason": reason,
            }
            out.write(json.dumps(obj, ensure_ascii=False))
            out.write("\n")


def process_pair(ref_path: Path, hyp_path: Path, lang: str, root: Path) -> tuple[int, int]:
    ref_rows = read_jsonl(ref_path)
    hyp_rows = read_jsonl(hyp_path)
    if len(ref_rows) != len(hyp_rows):
        raise ValueError(
            f"row mismatch: {ref_path.name}={len(ref_rows)} vs {hyp_path.name}={len(hyp_rows)}"
        )

    ref_norms, hyp_norms = [], []
    scored_flags, reasons = [], []
    for ref, hyp in zip(ref_rows, hyp_rows):
        rn = normalize_segment(ref["text"], lang)
        hn = normalize_segment(hyp["text"], lang)
        scored = rn["drop_reason_self"] is None
        ref_norms.append(rn)
        hyp_norms.append(hn)
        scored_flags.append(scored)
        reasons.append(rn["drop_reason_self"])

    out_ref = ref_path.with_name(ref_path.name.replace("_transcript.jsonl", "_transcript_norm.jsonl"))
    out_hyp = hyp_path.with_name(hyp_path.name.replace("_qwen.jsonl", "_qwen_norm.jsonl"))
    write_norm_jsonl(out_ref, ref_rows, ref_norms, scored_flags, reasons)
    write_norm_jsonl(out_hyp, hyp_rows, hyp_norms, scored_flags, reasons)

    scored_n = sum(scored_flags)
    print(f"  OK   {out_ref.relative_to(root)}  ({scored_n}/{len(ref_rows)} scored)")
    return len(ref_rows), scored_n


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=True)
    args = parser.parse_args(argv)

    root = Path(args.conversations)

    try:
        ref_files = resolve_speaker_files(
            root, args.batch, args.conversation, args.file, "_transcript.jsonl")
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if not ref_files:
        print("No SPK*_transcript.jsonl files found for the given scope.")
        return 1

    work: list[tuple[Path, Path, str]] = []
    missing_hyp = 0
    skipped = 0
    for ref_path in ref_files:
        hyp_path = ref_path.with_name(ref_path.name.replace("_transcript.jsonl", "_qwen.jsonl"))
        out_ref = ref_path.with_name(ref_path.name.replace("_transcript.jsonl", "_transcript_norm.jsonl"))
        if not hyp_path.exists():
            print(f"  SKIP (no qwen): {ref_path.relative_to(root)}")
            missing_hyp += 1
            continue
        if out_ref.exists() and not args.overwrite:
            skipped += 1
            continue
        ref_rows = read_jsonl(ref_path)
        if not ref_rows:
            continue
        lang = canonicalize_lang(ref_rows[0]["language"])
        work.append((ref_path, hyp_path, lang))

    if args.limit > 0:
        work = work[: args.limit]

    print(f"{len(ref_files)} reference file(s); {len(work)} to normalize "
          f"({skipped} already done, {missing_hyp} missing qwen).\n")
    if not work:
        print("Nothing to do.")
        return 0

    total_seg = total_scored = 0
    for ref_path, hyp_path, lang in work:
        try:
            n, scored = process_pair(ref_path, hyp_path, lang, root)
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"  FAIL {ref_path.relative_to(root)}: {exc}")
            continue
        total_seg += n
        total_scored += scored

    print(f"\nDone. {len(work)} pair(s), {total_seg} segments, {total_scored} scored "
          f"({total_seg - total_scored} dropped).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
