"""Flag spoken-form guideline violations in human reference transcripts.

Scans the **original** annotation files ``SPK*.seglst.json`` (not normalized
JSONL). Reports segments that still contain Arabic numerals or compact
currency/symbol characters that should be written as spoken words per
``guidelines_for_languages/``.

Checks implemented:

1. **Digits** — Arabic numerals (0-9), Eastern Arabic digits, fullwidth digits.
2. **Symbols** — currency signs, percent, ampersand, and compact URL/email markers
   (``$ € £ ¥ % & @ #`` etc.) that must not appear in correct transcriptions.

Writes one CSV row per segment that has at least one issue::

    batch_name, conversation, speaker, start, end, segment, issue

The ``segment`` column holds the raw ``words`` text from the seglst file.
``start`` / ``end`` are segment times in seconds (from ``start_time`` /
``end_time`` in the seglst). The ``issue`` column lists every finding for
that segment (e.g. ``digit:2000; digit:2; symbol:%``). Adjacent digits are
grouped into one label (``10`` not ``1`` + ``0``).

Usage
-----
    .\\.venv\\Scripts\\python.exe check_digit_symbol_guidelines.py
    .\\.venv\\Scripts\\python.exe check_digit_symbol_guidelines.py --batch delivery_batch_06092026
    .\\.venv\\Scripts\\python.exe check_digit_symbol_guidelines.py -o reports/digit_symbol_issues.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from workflow_common import add_scope_args, resolve_speaker_files

# Contiguous Arabic / Eastern Arabic / fullwidth digit runs.
DIGIT_SEQ_RE = re.compile(r"[0-9\u0660-\u0669\u06F0-\u06F9\uFF10-\uFF19]+")

NSV_TAG_RE = re.compile(r"\[[^\]]*\]")
PRO_TAG_RE = re.compile(r"\{PRO:[^}]*\}")

# Currency, percent, ampersand, and compact-notation symbols from the guidelines.
SYMBOL_CHARS = frozenset("$€£¥₹₩₽¢¤฿₫₱%@#&")

CSV_FIELDS = (
    "batch_name", "conversation", "speaker", "start", "end", "segment", "issue",
)


def to_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def clean_for_scan(text: str) -> str:
    """Remove NSV and pronunciation tags before digit/symbol detection."""
    text = NSV_TAG_RE.sub("", text or "")
    return PRO_TAG_RE.sub("", text)


def find_issues(text: str) -> str:
    """Return semicolon-separated issue labels for one segment, or empty string."""
    cleaned = clean_for_scan(text)
    issues: list[str] = []
    seen: set[str] = set()

    def add(label: str) -> None:
        if label not in seen:
            seen.add(label)
            issues.append(label)

    for match in DIGIT_SEQ_RE.finditer(cleaned):
        add(f"digit:{match.group()}")

    for ch in cleaned:
        if ch in SYMBOL_CHARS:
            add(f"symbol:{ch}")

    return "; ".join(issues)


def scan_seglst(path: Path, batch_name: str) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    segments = json.loads(raw)
    if not isinstance(segments, list):
        raise ValueError(f"{path} did not contain a JSON array of segments")

    default_speaker = path.name[: -len(".seglst.json")]
    conversation = path.parent.name
    rows: list[dict] = []

    for seg in segments:
        text = seg.get("words", "") or ""
        speaker = seg.get("speaker", default_speaker)
        start = to_float(seg.get("start_time"))
        end = to_float(seg.get("end_time"))
        issues = find_issues(text)
        if not issues:
            continue
        rows.append({
            "batch_name": batch_name,
            "conversation": conversation,
            "speaker": speaker,
            "start": start,
            "end": end,
            "segment": text,
            "issue": issues,
        })
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=CSV_FIELDS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=True)
    parser.add_argument(
        "--output", "-o",
        default="reports/guideline_digit_symbol_issues.csv",
        help="Output CSV path (default: reports/guideline_digit_symbol_issues.csv).",
    )
    args = parser.parse_args(argv)

    root = Path(args.conversations)
    try:
        seglst_files = resolve_speaker_files(
            root, args.batch, args.conversation, args.file, suffix=".seglst.json",
        )
    except (FileNotFoundError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    if args.limit:
        seglst_files = seglst_files[: args.limit]

    all_rows: list[dict] = []
    for path in seglst_files:
        batch_name = path.parent.parent.name
        all_rows.extend(scan_seglst(path, batch_name))

    out_path = Path(args.output)
    write_csv(out_path, all_rows)

    print(
        f"Wrote {len(all_rows)} segment(s) with issue(s) "
        f"across {len(seglst_files)} seglst file(s) to {out_path.resolve()}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
