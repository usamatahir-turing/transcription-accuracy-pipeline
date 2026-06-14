"""Normalize reference + Qwen transcripts for WER/CER/WCMR scoring.

For every ``Conversations/<SESSION>/SPK*_transcript.jsonl`` and its sibling
``SPK*_qwen.jsonl`` this writes two row-aligned outputs:

    SPK*_transcript_norm.jsonl   (normalized reference)
    SPK*_qwen_norm.jsonl         (normalized hypothesis)

Normalization track (same as Sample_review_report_06042026.md):
  1. OpenAI Whisper BasicTextNormalizer (lower-case, NFKC, brackets/punctuation
     stripped, diacritics preserved). This also removes well-formed NSV like
     [laugh] / [breath].
  2. Language-specific filler / backchannel stripping from fillers_by_lang.json:
       - *_safe  tokens (hesitation + backchannel) are ALWAYS stripped.
       - *_ambiguous tokens are kept inline when the segment has real content;
         a segment is treated as a pure backchannel/filler turn (and dropped
         from scoring) only when the REFERENCE has no real content left.
       - lexical_fillers are kept (treated as content).

Empty / pure-backchannel handling: rows are never deleted. Every row is kept and
flagged with ``scored`` (bool) and ``drop_reason``. The decision is anchored on
the REFERENCE and copied to the hypothesis row, so the two files stay aligned and
the scorer just keeps rows where ``scored`` is true. A scored row may still have
an empty hypothesis (Qwen missed real speech) -> that correctly counts later.

Usage
-----
    .\.venv\Scripts\python.exe normalize_transcripts.py
    .\.venv\Scripts\python.exe normalize_transcripts.py --ambiguous-mode keep
    .\.venv\Scripts\python.exe normalize_transcripts.py --collapse-elongation
    .\.venv\Scripts\python.exe normalize_transcripts.py --conversation NV-AR-SS03-CONVO09 --file SPK01
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from whisper.normalizers import BasicTextNormalizer

from workflow_common import add_scope_args, resolve_speaker_files

# Diacritics preserved -> remove_diacritics=False (matches the report).
_NORM = BasicTextNormalizer(remove_diacritics=False)

# Tokenization is whitespace-based for ALL languages, faithful to the report's
# `len(ref.split())` definition. The Japanese annotations are already space-
# segmented into words (e.g. "日本 人 が 海外 で"), so whitespace tokenization
# preserves that segmentation; we must NOT re-tokenize JA (e.g. with nagisa) or
# collapse those spaces, or `.split()`-based WER/WCMR would break.


def basic_normalize(text: str, collapse_elongation: bool) -> str:
    s = _NORM(text or "")
    if collapse_elongation:
        # collapse runs of 3+ identical chars to one (esteee -> este)
        s = re.sub(r"(.)\1{2,}", r"\1", s)
        s = re.sub(r"\s+", " ", s).strip()
    return s


def tokenize(text: str, lang: str) -> list[str]:
    # Whitespace tokenization for every language (see note above).
    return text.split() if text else []


def load_fillers(path: Path, collapse_elongation: bool) -> dict:
    """Return per-language sets of NORMALIZED filler phrases + match metadata."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for lang, groups in raw.items():
        safe, ambiguous, lexical = set(), set(), set()
        targets = {
            "hesitation_safe": safe,
            "backchannel_safe": safe,
            "hesitation_ambiguous": ambiguous,
            "backchannel_ambiguous": ambiguous,
            "lexical_fillers": lexical,
        }
        for group, bucket in targets.items():
            for canonical, variants in groups.get(group, {}).items():
                for form in [canonical, *variants]:
                    norm = basic_normalize(form, collapse_elongation)
                    if norm:
                        bucket.add(norm)
        # match_joiner: how to glue candidate tokens before comparing to a filler
        # entry. JA filler entries are space-less (e.g. "そうですね") while the data
        # is space-segmented ("そう です ね"), so JA matches on "". Output always
        # rejoins with a space to preserve word segmentation.
        match_joiner = "" if lang == "JA" else " "
        # max n-gram length to test when matching (in tokens)
        if lang == "JA":
            max_n = 6
        else:
            max_n = max((len(p.split()) for p in safe | ambiguous | lexical), default=1)
        out[lang] = {
            "safe": safe,
            "ambiguous": ambiguous,
            "lexical": lexical,
            "match_joiner": match_joiner,
            "out_joiner": " ",
            "max_n": max(1, max_n),
        }
    return out


def tag_tokens(tokens: list[str], fill: dict) -> list[tuple[list[str], str]]:
    """Greedy longest-match tagging into safe / ambiguous / lexical / content."""
    joiner = fill["match_joiner"]
    max_n = fill["max_n"]
    safe, ambiguous, lexical = fill["safe"], fill["ambiguous"], fill["lexical"]
    result: list[tuple[list[str], str]] = []
    i, n = 0, len(tokens)
    while i < n:
        matched = False
        for size in range(min(max_n, n - i), 0, -1):
            gram = joiner.join(tokens[i : i + size])
            if gram in safe:
                cat = "safe"
            elif gram in ambiguous:
                cat = "ambiguous"
            elif gram in lexical:
                cat = "lexical"
            else:
                continue
            result.append((tokens[i : i + size], cat))
            i += size
            matched = True
            break
        if not matched:
            result.append(([tokens[i]], "content"))
            i += 1
    return result


def normalize_segment(text: str, lang: str, fill: dict, ambiguous_mode: str,
                      collapse_elongation: bool) -> dict:
    """Return {norm, n_content, n_nonsafe, has_ambiguous, drop_reason_self}."""
    base = basic_normalize(text, collapse_elongation)
    tokens = tokenize(base, lang)
    tagged = tag_tokens(tokens, fill)

    n_content = sum(1 for _, c in tagged if c in ("content", "lexical"))
    n_nonsafe = sum(len(t) for t, c in tagged if c != "safe")
    has_ambiguous = any(c == "ambiguous" for _, c in tagged)

    kept: list[str] = []
    for toks, cat in tagged:
        if cat == "safe":
            continue
        if cat == "ambiguous" and ambiguous_mode == "strip-always":
            continue
        kept.extend(toks)
    norm = fill["out_joiner"].join(kept)

    # reason this segment would be empty/non-content (used for the ref)
    if not tokens:
        reason = "empty"
    elif n_content == 0:
        reason = "backchannel_only" if has_ambiguous else "filler_only"
    else:
        reason = None
    return {
        "norm": norm,
        "n_content": n_content,
        "n_nonsafe": n_nonsafe,
        "drop_reason_self": reason,
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


def process_pair(ref_path: Path, hyp_path: Path, fill_by_lang: dict,
                 ambiguous_mode: str, collapse_elongation: bool, root: Path) -> tuple[int, int]:
    ref_rows = read_jsonl(ref_path)
    hyp_rows = read_jsonl(hyp_path)
    if len(ref_rows) != len(hyp_rows):
        raise ValueError(
            f"row mismatch: {ref_path.name}={len(ref_rows)} vs {hyp_path.name}={len(hyp_rows)}"
        )

    lang = ref_rows[0]["language"] if ref_rows else ""
    fill = fill_by_lang.get(lang)
    if fill is None:
        raise ValueError(f"no filler config for language {lang!r} ({ref_path})")

    ref_norms, hyp_norms = [], []
    scored_flags, reasons = [], []
    for ref, hyp in zip(ref_rows, hyp_rows):
        rn = normalize_segment(ref["text"], lang, fill, ambiguous_mode, collapse_elongation)
        hn = normalize_segment(hyp["text"], lang, fill, ambiguous_mode, collapse_elongation)
        # disposition anchored on the REFERENCE
        if ambiguous_mode == "keep":
            scored = rn["n_nonsafe"] > 0
        else:  # drop-if-alone (default) / strip-always
            scored = rn["n_content"] > 0
        ref_norms.append(rn)
        hyp_norms.append(hn)
        scored_flags.append(scored)
        reasons.append(None if scored else rn["drop_reason_self"])

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
    parser.add_argument("--fillers", default="fillers_by_lang.json")
    parser.add_argument("--ambiguous-mode", choices=["keep", "drop-if-alone", "strip-always"],
                        default="drop-if-alone")
    parser.add_argument("--collapse-elongation", action="store_true",
                        help="Collapse runs of 3+ identical chars (esteee -> este).")
    args = parser.parse_args(argv)

    root = Path(args.conversations)

    fill_path = Path(args.fillers)
    if not fill_path.is_file():
        print(f"ERROR: fillers file not found: {fill_path.resolve()}")
        return 1
    fill_by_lang = load_fillers(fill_path, args.collapse_elongation)

    try:
        ref_files = resolve_speaker_files(
            root, args.batch, args.conversation, args.file, "_transcript.jsonl")
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if not ref_files:
        print("No SPK*_transcript.jsonl files found for the given scope.")
        return 1

    work: list[tuple[Path, Path]] = []
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
        work.append((ref_path, hyp_path))

    if args.limit > 0:
        work = work[: args.limit]

    print(f"{len(ref_files)} reference file(s); {len(work)} to normalize "
          f"({skipped} already done, {missing_hyp} missing qwen). "
          f"ambiguous-mode={args.ambiguous_mode}\n")
    if not work:
        print("Nothing to do.")
        return 0

    total_seg = total_scored = 0
    for ref_path, hyp_path in work:
        try:
            n, scored = process_pair(ref_path, hyp_path, fill_by_lang,
                                     args.ambiguous_mode, args.collapse_elongation, root)
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
