"""Rank the worst-scoring segments per speaker for manual review.

Reads normalized reference + hypothesis JSONL (same inputs as compute_metrics.py):
    SPK*_transcript_norm.jsonl
    SPK*_qwen_norm.jsonl

For each scored segment, computes per-segment error counts with jiwer and
writes the top-N segments to ``SPK*_top_errors.json`` in the conversation folder.

Ranking key (absolute errors = substitutions + deletions + insertions):
  - Japanese (JA): character errors on whitespace-stripped text (CER).
  - All other languages: word errors on whitespace .split() tokens (WER).

This matches the micro-averaging definitions in compute_metrics.py — segments
with the highest absolute error counts are the largest contributors to the
conversation-level WER / CER numerator.

Usage
-----
    .\\.venv\\Scripts\\python.exe rank_error_segments.py
    .\\.venv\\Scripts\\python.exe rank_error_segments.py --conversation NV-JA-SS04-CONVO11
    .\\.venv\\Scripts\\python.exe rank_error_segments.py --conversation NV-KO-SS03-CONVO07 --file SPK01
    .\\.venv\\Scripts\\python.exe rank_error_segments.py --top 20 --min-ref-units 5
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import jiwer

from workflow_common import add_scope_args, resolve_speaker_files

# Same language choice as compute_metrics.py — CER is the meaningful rank for JA.
CER_PRIMARY = {"JA"}


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _pct(errors: int, ref_units: int) -> float | None:
    return round(100.0 * errors / ref_units, 2) if ref_units else None


def segment_errors(ref_norm: str, hyp_norm: str, *, use_cer: bool) -> dict:
    """Return per-segment S/D/I counts and ref/hyp unit totals."""
    if use_cer:
        ref = "".join(ref_norm.split())
        hyp = "".join(hyp_norm.split())
        out = jiwer.process_characters([ref], [hyp])
    else:
        ref = ref_norm
        hyp = hyp_norm
        out = jiwer.process_words([ref], [hyp])

    ref_units = out.hits + out.substitutions + out.deletions
    hyp_units = out.hits + out.substitutions + out.insertions
    errors = out.substitutions + out.deletions + out.insertions
    return {
        "ref_units": ref_units,
        "hyp_units": hyp_units,
        "substitutions": out.substitutions,
        "deletions": out.deletions,
        "insertions": out.insertions,
        "errors": errors,
        "error_rate_pct": _pct(errors, ref_units),
    }


def rank_speaker(
    ref_path: Path,
    hyp_path: Path,
    *,
    top_n: int,
    min_ref_units: int,
) -> dict | None:
    ref_rows = read_jsonl(ref_path)
    hyp_rows = read_jsonl(hyp_path)
    if len(ref_rows) != len(hyp_rows):
        raise ValueError(
            f"row mismatch: {ref_path.name}={len(ref_rows)} vs {hyp_path.name}={len(hyp_rows)}"
        )
    if not ref_rows:
        return None

    language = ref_rows[0].get("language", "")
    speaker = ref_rows[0].get("speaker", ref_path.name[: -len("_transcript_norm.jsonl")])
    session_id = ref_rows[0].get("session_id", ref_path.parent.name)
    use_cer = language in CER_PRIMARY
    rank_metric = "cer" if use_cer else "wer"

    candidates: list[dict] = []
    for r, h in zip(ref_rows, hyp_rows):
        if not r.get("scored"):
            continue
        ref_norm = (r.get("text_norm") or "").strip()
        hyp_norm = (h.get("text_norm") or "").strip()
        if not ref_norm:
            continue

        stats = segment_errors(ref_norm, hyp_norm, use_cer=use_cer)
        if stats["ref_units"] < min_ref_units:
            continue
        if stats["errors"] == 0:
            continue

        candidates.append({
            "idx": r["idx"],
            "start": r.get("start"),
            "end": r.get("end"),
            **stats,
            "ref_norm": ref_norm,
            "hyp_norm": hyp_norm,
            "ref_raw": r.get("text") or "",
            "hyp_raw": h.get("text") or "",
        })

    candidates.sort(
        key=lambda s: (
            -s["errors"],
            -s["ref_units"],
            -(s["error_rate_pct"] or 0),
            s["idx"],
        )
    )
    top = candidates[:top_n]
    for rank, seg in enumerate(top, start=1):
        seg["rank"] = rank

    return {
        "session_id": session_id,
        "speaker": speaker,
        "language": language,
        "rank_metric": rank_metric,
        "top_n": top_n,
        "min_ref_units": min_ref_units,
        "n_scored_candidates": len(candidates),
        "segments": top,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=True)
    parser.add_argument("--top", type=int, default=10,
                        help="Number of worst segments to keep per speaker (default: 10).")
    parser.add_argument("--min-ref-units", type=int, default=3,
                        help="Skip segments whose reference word/char count is below this "
                             "(default: 3).")
    args = parser.parse_args(argv)

    root = Path(args.conversations)
    try:
        ref_files = resolve_speaker_files(
            root, args.batch, args.conversation, args.file, "_transcript_norm.jsonl")
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit > 0:
        ref_files = ref_files[: args.limit]

    n_done = n_skipped = n_empty = n_fail = 0
    for ref_path in ref_files:
        speaker = ref_path.name[: -len("_transcript_norm.jsonl")]
        out_path = ref_path.with_name(f"{speaker}_top_errors.json")
        if out_path.exists() and not args.overwrite:
            n_skipped += 1
            continue

        hyp_path = ref_path.with_name(f"{speaker}_qwen_norm.jsonl")
        if not hyp_path.is_file():
            print(f"  SKIP {ref_path.parent.name}/{speaker}: no {hyp_path.name}")
            n_fail += 1
            continue

        try:
            result = rank_speaker(
                ref_path, hyp_path,
                top_n=args.top,
                min_ref_units=args.min_ref_units,
            )
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"  FAIL {ref_path.parent.name}/{speaker}: {exc}")
            n_fail += 1
            continue

        if result is None or not result["segments"]:
            print(f"  EMPTY {ref_path.parent.name}/{speaker}  "
                  f"(no segments above min_ref_units with errors)")
            n_empty += 1
            continue

        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        metric = result["rank_metric"].upper()
        worst = result["segments"][0]
        print(
            f"  OK   {result['session_id']}/{speaker} [{result['language']}]  "
            f"{metric}  top={len(result['segments'])}  "
            f"worst: idx={worst['idx']} errors={worst['errors']}"
        )
        n_done += 1

    print(
        f"\nDone. {n_done} speaker file(s) written, {n_skipped} skipped "
        f"(output exists), {n_empty} empty, {n_fail} failed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
