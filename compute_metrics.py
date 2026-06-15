"""Compute WER / CER / WCMR per conversation from the normalized transcripts.

Consumes the normalized files produced by normalize_transcripts.py:
    SPK*_transcript_norm.jsonl  (reference)
    SPK*_qwen_norm.jsonl        (hypothesis)
joins them by idx, keeps only rows with ``scored == true``, and computes — both
per speaker and for the conversation as a whole — the metrics from
Sample_review_report_06042026.md:

  - WER / CER: micro-averaged via jiwer.
        * WER on whitespace .split() tokens (faithful to the report's
          `len(ref.split())` definition).
        * CER on whitespace-STRIPPED characters (so word-segmentation spaces
          don't dilute/inflate it; essential for Japanese).
  - WCMR: share of scored segments where len(ref.split()) != len(hyp.split()),
    plus the |m-n| gap buckets (=1, =2, =3, >3) as in Appendix A.2.

Raw S/D/I/H counts and reference word/char totals are stored alongside the
rates so a later combiner can re-aggregate exact micro-averages per language.

Output: one ``metrics.json`` written into each conversation folder.

Usage
-----
    .\.venv\Scripts\python.exe compute_metrics.py
    .\.venv\Scripts\python.exe compute_metrics.py --conversation NV-AR-SS03-CONVO09
    .\.venv\Scripts\python.exe compute_metrics.py --overwrite
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import jiwer

from workflow_common import add_scope_args, resolve_conversation_dirs

# Languages where WER/WCMR are whole-segment artifacts (no reliable word spaces);
# CER is the metric to trust. Used only to annotate the output.
CER_PRIMARY = {"JA"}


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def collect_scored_pairs(ref_path: Path, hyp_path: Path) -> tuple[list[tuple[str, str]], int]:
    """Return (list of (ref_norm, hyp_norm) for scored rows, total row count)."""
    ref_rows = read_jsonl(ref_path)
    hyp_rows = read_jsonl(hyp_path)
    if len(ref_rows) != len(hyp_rows):
        raise ValueError(
            f"row mismatch: {ref_path.name}={len(ref_rows)} vs {hyp_path.name}={len(hyp_rows)}"
        )
    pairs: list[tuple[str, str]] = []
    for r, h in zip(ref_rows, hyp_rows):
        if not r.get("scored"):
            continue
        ref_text = (r.get("text_norm") or "").strip()
        hyp_text = (h.get("text_norm") or "").strip()
        if not ref_text:
            # safety: scored rows should always have reference content
            continue
        pairs.append((ref_text, hyp_text))
    return pairs, len(ref_rows)


def _pct(x: int, total: int) -> float:
    return round(100.0 * x / total, 2) if total else 0.0


def compute_block(pairs: list[tuple[str, str]], n_total: int) -> dict:
    n_scored = len(pairs)
    if n_scored == 0:
        return {"n_segments_total": n_total, "n_scored": 0,
                "wer": None, "cer": None, "wcmr": None}

    refs = [r for r, _ in pairs]
    hyps = [h for _, h in pairs]

    # WER (whitespace tokens, micro-averaged)
    wo = jiwer.process_words(refs, hyps)
    ref_words = wo.hits + wo.substitutions + wo.deletions

    # CER (whitespace stripped, micro-averaged)
    refs_c = ["".join(r.split()) for r in refs]
    hyps_c = ["".join(h.split()) for h in hyps]
    co = jiwer.process_characters(refs_c, hyps_c)
    ref_chars = co.hits + co.substitutions + co.deletions

    # WCMR + |m-n| buckets
    n_mm = b1 = b2 = b3 = bg = 0
    for r, h in pairs:
        gap = abs(len(r.split()) - len(h.split()))
        if gap == 0:
            continue
        n_mm += 1
        if gap == 1:
            b1 += 1
        elif gap == 2:
            b2 += 1
        elif gap == 3:
            b3 += 1
        else:
            bg += 1

    return {
        "n_segments_total": n_total,
        "n_scored": n_scored,
        "wer": {
            "pct": round(wo.wer * 100, 2),
            "ref_words": ref_words,
            "substitutions": wo.substitutions,
            "deletions": wo.deletions,
            "insertions": wo.insertions,
        },
        "cer": {
            "pct": round(co.cer * 100, 2),
            "ref_chars": ref_chars,
            "substitutions": co.substitutions,
            "deletions": co.deletions,
            "insertions": co.insertions,
        },
        "wcmr": {
            "pct": _pct(n_mm, n_scored),
            "n_mismatch": n_mm,
            "buckets": {
                "eq1": {"n": b1, "pct": _pct(b1, n_scored)},
                "eq2": {"n": b2, "pct": _pct(b2, n_scored)},
                "eq3": {"n": b3, "pct": _pct(b3, n_scored)},
                "gt3": {"n": bg, "pct": _pct(bg, n_scored)},
            },
        },
    }


def process_conversation(session_dir: Path) -> dict | None:
    ref_files = sorted(session_dir.glob("SPK*_transcript_norm.jsonl"))
    if not ref_files:
        return None

    language = ""
    speakers: dict[str, dict] = {}
    all_pairs: list[tuple[str, str]] = []
    all_total = 0

    for ref_path in ref_files:
        speaker = ref_path.name[: -len("_transcript_norm.jsonl")]
        hyp_path = ref_path.with_name(f"{speaker}_qwen_norm.jsonl")
        if not hyp_path.exists():
            print(f"    SKIP speaker {speaker}: no {hyp_path.name}")
            continue
        rows = read_jsonl(ref_path)
        if rows and not language:
            language = rows[0].get("language", "")
        pairs, n_total = collect_scored_pairs(ref_path, hyp_path)
        speakers[speaker] = compute_block(pairs, n_total)
        all_pairs.extend(pairs)
        all_total += n_total

    if not speakers:
        return None

    return {
        "session_id": session_dir.name,
        "language": language,
        "method": {
            "wer_tokenization": (
                "whitespace .split() on char-spaced text (JA no-space language)"
                if language in CER_PRIMARY
                else "whitespace .split()"
            ),
            "cer_whitespace_stripped": True,
            "averaging": "micro",
            "note": (
                "JA: text_norm is char-spaced after normalization (matches client "
                "wer_scoring_repr); WER and CER are equivalent. CER is the governing metric."
                if language in CER_PRIMARY
                else ""
            ),
        },
        "total": compute_block(all_pairs, all_total),
        "speakers": speakers,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=False)
    args = parser.parse_args(argv)

    root = Path(args.conversations)
    try:
        session_dirs = resolve_conversation_dirs(root, args.batch, args.conversation)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.limit > 0:
        session_dirs = session_dirs[: args.limit]

    n_done = n_skipped = n_empty = 0
    for session_dir in session_dirs:
        out_path = session_dir / "metrics.json"
        if out_path.exists() and not args.overwrite:
            n_skipped += 1
            continue
        try:
            result = process_conversation(session_dir)
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"  FAIL {session_dir.name}: {exc}")
            continue
        if result is None:
            n_empty += 1
            continue
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        t = result["total"]
        wer = t["wer"]["pct"] if t["wer"] else "-"
        cer = t["cer"]["pct"] if t["cer"] else "-"
        wcmr = t["wcmr"]["pct"] if t["wcmr"] else "-"
        print(f"  OK   {session_dir.name} [{result['language']}]  "
              f"n={t['n_scored']}  WER={wer}  CER={cer}  WCMR={wcmr}")
        n_done += 1

    print(f"\nDone. {n_done} conversation(s) scored, {n_skipped} skipped "
          f"(metrics.json exists), {n_empty} with no normalized files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
