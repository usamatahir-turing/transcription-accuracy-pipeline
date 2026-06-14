"""Generate Excel transcription accuracy reports from per-conversation metrics.json files.

Reads ``Conversations/<batch>/<conversation>/metrics.json`` and writes one
``.xlsx`` workbook with:

  - one worksheet per batch (per-conversation + by-language summary)
  - a final **All Batches** worksheet combining every batch
  - a **Definitions** worksheet explaining each metric column
  - a **Reference** worksheet with baseline reference numbers

Human-annotated transcript metrics are compared to the independent vendor
baseline reference. Delta columns show *annotated transcript − baseline* in
percentage points; lower error rates are better, so negative deltas are green
and positive deltas are amber/red.

Usage
-----
    .\\.venv\\Scripts\\python.exe generate_report.py
    .\\.venv\\Scripts\\python.exe generate_report.py --output reports/transcription_accuracy_metrics.xlsx
    .\\.venv\\Scripts\\python.exe generate_report.py --batch delivery_batch_06092026
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import Workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from workflow_common import add_scope_args, resolve_conversation_dirs

# Baseline reference numbers (independent vendor corpus, identical pipeline).
REFERENCE = {
    "AR": {"wer": 47.04, "cer": 20.28, "wcmr": 63.22, "gt3_pct": 28.49},
    "DE": {"wer": 15.62, "cer": 10.24, "wcmr": 38.92, "gt3_pct": 9.57},
    "EN": {"wer": 8.51, "cer": 6.40, "wcmr": 28.22, "gt3_pct": 3.33},
    "ES": {"wer": 14.37, "cer": 10.73, "wcmr": 36.01, "gt3_pct": 6.50},
    "FR": {"wer": 17.20, "cer": 12.97, "wcmr": 51.12, "gt3_pct": 25.78},
    "IT": {"wer": 11.97, "cer": 7.90, "wcmr": 40.61, "gt3_pct": 9.14},
    "JA": {"wer": 71.83, "cer": 11.77, "wcmr": 43.74, "gt3_pct": 16.16},
    "KO": {"wer": 18.21, "cer": 10.13, "wcmr": 28.27, "gt3_pct": 2.51},
    "PT": {"wer": 12.31, "cer": 6.92, "wcmr": 46.02, "gt3_pct": 8.62},
    "RU": {"wer": 16.80, "cer": 11.13, "wcmr": 54.66, "gt3_pct": 6.39},
    "ALL": {"wer": 19.38, "cer": 10.73, "wcmr": 42.42, "gt3_pct": 11.37},
}

# Side-by-side layout: language summary cols A–K, gap col L, conversations col M→
LANG_COL = 1
GAP_COL = 12
CONV_COL = 13

# Slim tables: core metrics + colored delta columns (vs baseline reference).
CONV_HEADERS = [
    ("Conversation", "session_id", None, False),
    ("Language", "language", None, False),
    ("Scored", "n_scored", "#,##0", False),
    ("WER %", "wer_pct", "0.00", False),
    ("Δ WER", "d_wer", "+0.0;-0.0", True),
    ("CER %", "cer_pct", "0.00", False),
    ("Δ CER", "d_cer", "+0.0;-0.0", True),
    ("WCMR %", "wcmr_pct", "0.00", False),
    ("Δ WCMR", "d_wcmr", "+0.0;-0.0", True),
    ("|m-n|>3 %", "gt3_pct", "0.00", False),
    ("Δ >3", "d_gt3", "+0.0;-0.0", True),
]

LANG_HEADERS = [
    ("Language", "language", None, False),
    ("Conv.", "n_conversations", "#,##0", False),
    ("Scored", "n_scored", "#,##0", False),
    ("WER %", "wer_pct", "0.00", False),
    ("Δ WER", "d_wer", "+0.0;-0.0", True),
    ("CER %", "cer_pct", "0.00", False),
    ("Δ CER", "d_cer", "+0.0;-0.0", True),
    ("WCMR %", "wcmr_pct", "0.00", False),
    ("Δ WCMR", "d_wcmr", "+0.0;-0.0", True),
    ("|m-n|>3 %", "gt3_pct", "0.00", False),
    ("Δ >3", "d_gt3", "+0.0;-0.0", True),
]

REF_HEADERS = [
    ("Language", "language", None, False),
    ("Scored (ref)", "n_scored", "#,##0", False),
    ("WER %", "wer", "0.00", False),
    ("CER %", "cer", "0.00", False),
    ("WCMR %", "wcmr", "0.00", False),
    ("|m-n|>3 %", "gt3_pct", "0.00", False),
]

REF_N_SCORED = {
    "AR": 2352, "DE": 2058, "EN": 3157, "ES": 2799, "FR": 3224,
    "IT": 2231, "JA": 5290, "KO": 4336, "PT": 3931, "RU": 3037, "ALL": 32415,
}

METRIC_DEFINITIONS = [
    (
        "Scored",
        "Number of speech segments included in scoring. Segments where the "
        "human-annotated reference has no real content after normalization "
        "(empty, filler-only, or backchannel-only) are excluded.",
    ),
    (
        "WER %",
        "Word Error Rate — (substitutions + deletions + insertions) ÷ reference "
        "word count, micro-averaged across scored segments. Compares human-"
        "annotated transcript vs Qwen3-ASR. Whitespace-delimited tokens after "
        "normalization. Lower is better.",
    ),
    (
        "Δ WER",
        "Human-annotated transcript WER % minus the baseline reference WER % "
        "for that language (percentage points). Negative = better than baseline.",
    ),
    (
        "CER %",
        "Character Error Rate — same as WER but on characters with whitespace "
        "removed before comparison. Human annotation vs Qwen3-ASR, micro-averaged. "
        "Lower is better. Preferred metric for Japanese (and useful when WER/WCMR "
        "are unreliable).",
    ),
    (
        "Δ CER",
        "Human-annotated transcript CER % minus the baseline reference CER % "
        "for that language (percentage points). Negative = better than baseline.",
    ),
    (
        "WCMR %",
        "Word-Count Mismatch Rate — share of scored segments where the human "
        "annotation and Qwen3-ASR hypothesis disagree on word count "
        "(len(ref.split()) ≠ len(hyp.split())). Flags text↔segment alignment "
        "issues. Lower is better.",
    ),
    (
        "Δ WCMR",
        "Human-annotated transcript WCMR % minus the baseline reference WCMR % "
        "for that language (percentage points). Negative = better than baseline.",
    ),
    (
        "|m-n|>3 %",
        "Share of scored segments where the absolute word-count gap between "
        "human annotation (m) and Qwen3-ASR output (n) exceeds 3. Large gaps "
        "often indicate segments whose text does not line up with the audio. "
        "Lower is better.",
    ),
    (
        "Δ >3",
        "Human-annotated transcript |m-n|>3 % minus the baseline reference value "
        "for that language (percentage points). Negative = better than baseline.",
    ),
]


def _pct(num: int, den: int) -> float | None:
    return round(100.0 * num / den, 2) if den else None


def _delta(actual: float | None, baseline: float | None) -> float | None:
    if actual is None or baseline is None:
        return None
    return round(actual - baseline, 2)


def _baseline_for(lang: str) -> dict:
    if lang == "ALL":
        return REFERENCE["ALL"]
    return REFERENCE.get(lang, {})


def enrich_with_deltas(record: dict) -> dict:
    """Add delta fields vs baseline reference for the row's language."""
    ref = _baseline_for(record.get("language", ""))
    out = dict(record)
    out["d_wer"] = _delta(record.get("wer_pct"), ref.get("wer"))
    out["d_cer"] = _delta(record.get("cer_pct"), ref.get("cer"))
    out["d_wcmr"] = _delta(record.get("wcmr_pct"), ref.get("wcmr"))
    out["d_gt3"] = _delta(record.get("gt3_pct"), ref.get("gt3_pct"))
    return out


def load_metrics(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def metrics_to_record(batch: str, data: dict) -> dict:
    """Flatten conversation-level ``total`` block into a row dict (+ raw counts)."""
    t = data["total"]
    wer = t.get("wer") or {}
    cer = t.get("cer") or {}
    wcmr = t.get("wcmr") or {}
    buckets = wcmr.get("buckets") or {}

    def _b(key: str) -> dict:
        return buckets.get(key) or {}

    record = {
        "batch": batch,
        "session_id": data["session_id"],
        "language": data.get("language") or "",
        "n_segments_total": t.get("n_segments_total", 0),
        "n_scored": t.get("n_scored", 0),
        "wer_pct": wer.get("pct"),
        "cer_pct": cer.get("pct"),
        "wcmr_pct": wcmr.get("pct"),
        "n_mismatch": wcmr.get("n_mismatch", 0),
        "gt3_n": _b("gt3").get("n", 0),
        "gt3_pct": _b("gt3").get("pct"),
        "ref_words": wer.get("ref_words", 0),
        "wer_s": wer.get("substitutions", 0),
        "wer_d": wer.get("deletions", 0),
        "wer_i": wer.get("insertions", 0),
        "ref_chars": cer.get("ref_chars", 0),
        "cer_s": cer.get("substitutions", 0),
        "cer_d": cer.get("deletions", 0),
        "cer_i": cer.get("insertions", 0),
    }
    return enrich_with_deltas(record)


def aggregate_records(records: list[dict], label: str) -> dict:
    """Micro-average a list of conversation records into one summary row."""
    n_scored = sum(r["n_scored"] for r in records)
    ref_words = sum(r["ref_words"] for r in records)
    ref_chars = sum(r["ref_chars"] for r in records)
    wer_err = sum(r["wer_s"] + r["wer_d"] + r["wer_i"] for r in records)
    cer_err = sum(r["cer_s"] + r["cer_d"] + r["cer_i"] for r in records)
    n_mismatch = sum(r["n_mismatch"] for r in records)
    gt3_n = sum(r.get("gt3_n", 0) for r in records)

    row = {
        "language": label,
        "n_conversations": len(records),
        "n_scored": n_scored,
        "wer_pct": _pct(wer_err, ref_words),
        "cer_pct": _pct(cer_err, ref_chars),
        "wcmr_pct": _pct(n_mismatch, n_scored),
        "n_mismatch": n_mismatch,
        "gt3_pct": _pct(gt3_n, n_scored),
    }
    return enrich_with_deltas(row)


def language_summary(records: list[dict]) -> list[dict]:
    by_lang: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_lang[r["language"]].append(r)
    rows = [aggregate_records(by_lang[lang], lang) for lang in sorted(by_lang)]
    if rows:
        rows.append(aggregate_records(records, "ALL"))
    return rows


def discover_records(root: Path, batch: str | None) -> dict[str, list[dict]]:
    """Return {batch_name: [conversation records]} for conversations with metrics.json."""
    batches: dict[str, list[dict]] = defaultdict(list)
    for conv_dir in resolve_conversation_dirs(root, batch, None):
        metrics_path = conv_dir / "metrics.json"
        if not metrics_path.is_file():
            continue
        batch_name = conv_dir.parent.name
        data = load_metrics(metrics_path)
        batches[batch_name].append(metrics_to_record(batch_name, data))
    for batch_name in batches:
        batches[batch_name].sort(key=lambda r: r["session_id"])
    return dict(sorted(batches.items()))


# ---------------------------------------------------------------------------
# Excel styling
# ---------------------------------------------------------------------------

CLR_TITLE = "1F3864"
CLR_HEADER = "2F5496"
CLR_SECTION = "D6DCE4"
CLR_ALT = "F2F2F2"
CLR_TOTAL = "E0E0E0"

# Delta color scale (lower error = better → negative Δ is good).
CLR_MUCH_BETTER = "A9D18E"   # ≤ −5 pp
CLR_BETTER = "C6EFCE"        # −5 to −2
CLR_NEAR = "FFFFFF"          # −2 to +2
CLR_WORSE = "FFEB9C"         # +2 to +5
CLR_BAD = "FFC7CE"           # +5 to +10
CLR_MUCH_WORSE = "FF9999"    # > +10

FONT_TITLE = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
FONT_SUBTITLE = Font(name="Calibri", size=10, italic=True, color="595959")
FONT_SECTION = Font(name="Calibri", size=11, bold=True, color=CLR_TITLE)
FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
FONT_BODY = Font(name="Calibri", size=10)
FONT_TOTAL = Font(name="Calibri", size=10, bold=True)
FONT_LEGEND = Font(name="Calibri", size=9, italic=True, color="595959")
FONT_DELTA_GOOD = Font(name="Calibri", size=10, color="375623")
FONT_DELTA_OK = Font(name="Calibri", size=10, color="404040")
FONT_DELTA_WARN = Font(name="Calibri", size=10, color="9C6500")
FONT_DELTA_BAD = Font(name="Calibri", size=10, color="9C0006")

FILL_TITLE = PatternFill("solid", fgColor=CLR_TITLE)
FILL_HEADER = PatternFill("solid", fgColor=CLR_HEADER)
FILL_SECTION = PatternFill("solid", fgColor=CLR_SECTION)
FILL_ALT = PatternFill("solid", fgColor=CLR_ALT)
FILL_TOTAL = PatternFill("solid", fgColor=CLR_TOTAL)
FILL_DELTA = {
    "much_better": PatternFill("solid", fgColor=CLR_MUCH_BETTER),
    "better": PatternFill("solid", fgColor=CLR_BETTER),
    "near": PatternFill("solid", fgColor=CLR_NEAR),
    "worse": PatternFill("solid", fgColor=CLR_WORSE),
    "bad": PatternFill("solid", fgColor=CLR_BAD),
    "much_worse": PatternFill("solid", fgColor=CLR_MUCH_WORSE),
}

THIN = Side(style="thin", color="B4B4B4")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT = Alignment(horizontal="left", vertical="center")
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")


def _delta_band(delta: float | None) -> str | None:
    if delta is None:
        return None
    if delta <= -5:
        return "much_better"
    if delta <= -2:
        return "better"
    if delta <= 2:
        return "near"
    if delta <= 5:
        return "worse"
    if delta <= 10:
        return "bad"
    return "much_worse"


def _delta_font(band: str | None) -> Font:
    if band in ("much_better", "better"):
        return FONT_DELTA_GOOD
    if band in ("bad", "much_worse"):
        return FONT_DELTA_BAD
    if band == "worse":
        return FONT_DELTA_WARN
    return FONT_DELTA_OK


def _safe_sheet_name(name: str) -> str:
    bad = set(r'\/*?:[]')
    cleaned = "".join(c if c not in bad else "_" for c in name)
    return cleaned[:31]


def _write_title_block(ws, title: str, subtitle: str, n_cols: int) -> int:
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=n_cols)
    c = ws.cell(row=1, column=1, value=title)
    c.font = FONT_TITLE
    c.fill = FILL_TITLE
    c.alignment = ALIGN_LEFT

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=n_cols)
    c2 = ws.cell(row=2, column=1, value=subtitle)
    c2.font = FONT_SUBTITLE
    c2.alignment = ALIGN_LEFT
    return 3


def _write_reading_guide(ws, row: int, merge_end: int) -> int:
    """Legend + notes at the top, before any data tables."""
    items = [
        ("≤ −5", "much_better"),
        ("−5 to −2", "better"),
        ("±2", "near"),
        ("+2 to +5", "worse"),
        ("+5 to +10", "bad"),
        ("> +10", "much_worse"),
    ]
    label = ws.cell(row=row, column=LANG_COL, value="Δ color key (pp vs baseline):")
    label.font = FONT_LEGEND
    label.alignment = ALIGN_LEFT
    for i, (text, band) in enumerate(items, start=2):
        cell = ws.cell(row=row, column=LANG_COL + i - 1, value=text)
        cell.font = FONT_BODY
        cell.fill = FILL_DELTA[band]
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER

    row += 1
    callout_font = InlineFont(rFont="Calibri", sz=8, i=True, color="595959")
    note = CellRichText(
        "Δ = human-annotated transcript minus baseline reference (percentage points; "
        "lower error is better). See Definitions and Reference tabs for details.",
        "\n",
        TextBlock(
            callout_font,
            "JA: trust CER over WER/WCMR"
            "output inflates word-count metrics.",
        ),
        "\n",
        TextBlock(
            callout_font,
            "AR: Qwen3-ASR performance is poor and inconsistent for Arabic.",
        ),
    )
    ws.merge_cells(start_row=row, start_column=LANG_COL, end_row=row, end_column=merge_end)
    c = ws.cell(row=row, column=LANG_COL, value=note)
    c.font = FONT_LEGEND
    c.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    ws.row_dimensions[row].height = 36
    return row + 1


def _write_section_header(ws, row: int, text: str, n_cols: int,
                          start_col: int = 1) -> int:
    end_col = start_col + n_cols - 1
    ws.merge_cells(start_row=row, start_column=start_col, end_row=row, end_column=end_col)
    c = ws.cell(row=row, column=start_col, value=text)
    c.font = FONT_SECTION
    c.fill = FILL_SECTION
    c.alignment = ALIGN_LEFT
    c.border = BORDER
    return row + 1


def _style_gap_column(ws, start_row: int, end_row: int) -> None:
    """Narrow grey gutter between the two side-by-side tables."""
    ws.column_dimensions[get_column_letter(GAP_COL)].width = 2
    fill = PatternFill("solid", fgColor="E7E6E6")
    for r in range(start_row, end_row + 1):
        ws.cell(row=r, column=GAP_COL).fill = fill


def _write_table(ws, start_row: int, headers: list[tuple], rows: list[dict],
                 total_labels: set[str] | None = None,
                 start_col: int = 1) -> int:
    total_labels = total_labels or {"ALL"}

    for i, (label, _, _, _) in enumerate(headers):
        col = start_col + i
        cell = ws.cell(row=start_row, column=col, value=label)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER

    text_keys = {"session_id", "language", "batch"}
    for i, record in enumerate(rows):
        r = start_row + 1 + i
        is_total = record.get("language") in total_labels
        is_alt = i % 2 == 1 and not is_total
        for j, (_, key, fmt, is_delta) in enumerate(headers):
            col = start_col + j
            val = record.get(key)
            if val is None and is_delta:
                display = "—"
            else:
                display = val
            cell = ws.cell(row=r, column=col, value=display)
            cell.border = BORDER

            if is_delta and val is not None:
                band = _delta_band(val)
                cell.fill = FILL_DELTA[band]
                cell.font = _delta_font(band)
                cell.number_format = fmt or "+0.0;-0.0"
                cell.alignment = ALIGN_CENTER
            else:
                cell.font = FONT_TOTAL if is_total else FONT_BODY
                if is_total:
                    cell.fill = FILL_TOTAL
                elif is_alt:
                    cell.fill = FILL_ALT
                if fmt and val is not None:
                    cell.number_format = fmt
                cell.alignment = (
                    ALIGN_LEFT if key in text_keys else ALIGN_RIGHT
                )

    return start_row + 1 + len(rows)


def _autosize_columns(ws, col_ranges: list[tuple[int, int]],
                      min_width: int = 9, max_width: int = 22) -> None:
    for start, end in col_ranges:
        for col_idx in range(start, end + 1):
            letter = get_column_letter(col_idx)
            max_len = 0
            for row in range(1, ws.max_row + 1):
                val = ws.cell(row=row, column=col_idx).value
                if val is not None:
                    max_len = max(max_len, len(str(val)))
            ws.column_dimensions[letter].width = min(
                max(max_len + 2, min_width), max_width)


def _write_metrics_sheet(ws, title: str, subtitle: str,
                         conv_headers: list[tuple], conv_records: list[dict],
                         lang_records: list[dict]) -> None:
    """Side-by-side layout: language summary (A:K) | gap (L) | conversations (M→)."""
    sheet_end_col = CONV_COL + len(conv_headers) - 1
    row = _write_title_block(ws, title, subtitle, sheet_end_col)
    row = _write_reading_guide(ws, row, sheet_end_col)

    table_row = row
    row = _write_section_header(
        ws, row,
        "Summary by language (micro-averaged)",
        len(LANG_HEADERS), start_col=LANG_COL,
    )
    row = _write_section_header(
        ws, table_row,
        f"Per conversation ({len(conv_records)} session(s))",
        len(conv_headers), start_col=CONV_COL,
    )
    row = max(row, table_row + 1)

    header_row = row
    lang_end = _write_table(
        ws, row, LANG_HEADERS, lang_records, start_col=LANG_COL)
    conv_end = _write_table(
        ws, row, conv_headers, conv_records, start_col=CONV_COL)
    data_end = max(lang_end, conv_end)

    _style_gap_column(ws, table_row, data_end - 1)

    # Freeze title + legend + column headers only (row 7); columns scroll freely.
    ws.freeze_panes = ws.cell(row=header_row + 1, column=LANG_COL)
    _autosize_columns(ws, [(LANG_COL, LANG_COL + len(LANG_HEADERS) - 1),
                           (CONV_COL, sheet_end_col)])


def write_batch_sheet(ws, batch_name: str, records: list[dict], generated: str) -> None:
    title = f"Batch — {batch_name}"
    subtitle = (
        f"Human-annotated transcript vs Qwen3-ASR  ·  vs baseline reference  ·  "
        f"{len(records)} conversation(s)  ·  Generated {generated} UTC"
    )
    _write_metrics_sheet(
        ws, title, subtitle,
        CONV_HEADERS, records, language_summary(records),
    )


def write_all_batches_sheet(ws, all_records: list[dict], generated: str) -> None:
    conv_headers = [("Batch", "batch", None, False)] + list(CONV_HEADERS)
    title = "All batches — combined"
    subtitle = (
        f"Human-annotated transcript vs Qwen3-ASR  ·  vs baseline reference  ·  "
        f"{len(all_records)} conversation(s)  ·  Generated {generated} UTC"
    )
    _write_metrics_sheet(
        ws, title, subtitle,
        conv_headers, all_records, language_summary(all_records),
    )


def write_reference_sheet(ws) -> None:
    """Baseline reference corpus — separate tab for lookup."""
    n_cols = len(REF_HEADERS)
    row = _write_title_block(
        ws,
        "Baseline reference",
        "Independent vendor corpus · identical scoring pipeline (Qwen3-ASR, normalization, metrics)",
        n_cols,
    )
    row += 1
    row = _write_section_header(ws, row, "Per language", n_cols)
    ref_rows = []
    for lang in sorted(k for k in REFERENCE if k != "ALL"):
        ref = REFERENCE[lang]
        ref_rows.append({
            "language": lang,
            "n_scored": REF_N_SCORED[lang],
            "wer": ref["wer"],
            "cer": ref["cer"],
            "wcmr": ref["wcmr"],
            "gt3_pct": ref["gt3_pct"],
        })
    all_ref = REFERENCE["ALL"]
    ref_rows.append({
        "language": "ALL",
        "n_scored": REF_N_SCORED["ALL"],
        "wer": all_ref["wer"],
        "cer": all_ref["cer"],
        "wcmr": all_ref["wcmr"],
        "gt3_pct": all_ref["gt3_pct"],
    })
    _write_table(ws, row, REF_HEADERS, ref_rows)
    _autosize_columns(ws, [(1, n_cols)])


def write_definitions_sheet(ws) -> None:
    """Glossary of metric columns used in the batch / All Batches tabs."""
    n_cols = 2
    row = _write_title_block(
        ws,
        "Metric definitions",
        "Column glossary · human-annotated transcript vs Qwen3-ASR-1.7B",
        n_cols,
    )
    row += 1
    row = _write_section_header(ws, row, "Columns", n_cols)

    wrap = Alignment(horizontal="left", vertical="top", wrap_text=True)
    for col, label in enumerate(("Metric", "Definition"), start=1):
        cell = ws.cell(row=row, column=col, value=label)
        cell.font = FONT_HEADER
        cell.fill = FILL_HEADER
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER

    for i, (metric, definition) in enumerate(METRIC_DEFINITIONS):
        r = row + 1 + i
        m_cell = ws.cell(row=r, column=1, value=metric)
        m_cell.font = FONT_BODY
        m_cell.border = BORDER
        m_cell.alignment = ALIGN_LEFT
        d_cell = ws.cell(row=r, column=2, value=definition)
        d_cell.font = FONT_BODY
        d_cell.border = BORDER
        d_cell.alignment = wrap
        if i % 2 == 1:
            m_cell.fill = FILL_ALT
            d_cell.fill = FILL_ALT
        ws.row_dimensions[r].height = 36

    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 88
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def build_workbook(batches: dict[str, list[dict]], generated: str) -> Workbook:
    wb = Workbook()
    wb.remove(wb.active)

    ws_def = wb.create_sheet(title=_safe_sheet_name("Definitions"), index=0)
    write_definitions_sheet(ws_def)

    all_records: list[dict] = []
    for batch_name, records in batches.items():
        all_records.extend(records)
        ws = wb.create_sheet(title=_safe_sheet_name(batch_name))
        write_batch_sheet(ws, batch_name, records, generated)

    if all_records:
        all_records.sort(key=lambda r: (r["batch"], r["session_id"]))
        ws_all = wb.create_sheet(title=_safe_sheet_name("All Batches"))
        write_all_batches_sheet(ws_all, all_records, generated)

    ws_ref = wb.create_sheet(title=_safe_sheet_name("Reference"))
    write_reference_sheet(ws_ref)

    return wb


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_scope_args(parser, with_file=False)
    parser.add_argument(
        "--output", "-o", default="reports/transcription_accuracy_metrics.xlsx",
        help="Output .xlsx path (default: reports/transcription_accuracy_metrics.xlsx).",
    )
    args = parser.parse_args(argv)

    root = Path(args.conversations)
    try:
        batches = discover_records(root, args.batch)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        return 1

    if not batches:
        print("No metrics.json files found in scope.")
        return 1

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    wb = build_workbook(batches, generated)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)

    n_conv = sum(len(v) for v in batches.values())
    print(f"Wrote {out_path.resolve()}")
    print(f"  Definitions tab + {len(batches)} batch tab(s) + All Batches + Reference  "
          f"({n_conv} conversation(s)).")
    for batch_name, records in batches.items():
        langs = sorted({r["language"] for r in records})
        print(f"    {batch_name}: {len(records)} conversation(s)  [{', '.join(langs)}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
