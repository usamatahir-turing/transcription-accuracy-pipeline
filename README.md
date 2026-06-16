# Transcription accuracy pipeline

Measure how closely **human-annotated transcripts** agree with **Qwen3-ASR-1.7B** output on the same audio segments. The pipeline extracts segment-level reference text, runs ASR per segment, normalizes both sides identically, computes WER / CER / WCMR, and produces an Excel report with baseline comparison.

---

## Summary: how metrics are calculated

The evaluation is **segment-level**. Each speech segment defined in `SPK*.seglst.json` is treated as one row throughout the pipeline.

1. **Reference** — text from human annotation (`seglst.json`).
2. **Hypothesis** — Qwen3-ASR transcription of the same audio slice (`SPK*.wav`, cut to the segment's start/end time).
3. **Normalization (both sides, same rules)** — two stages applied to both reference and hypothesis:
   - **Whisper `BasicTextNormalizer`** — lowercase, NFKC, strip punctuation/brackets. This **removes NSV tags** (e.g. `[laugh]`, `[breath]`, `[inhale]`) from the text used for scoring; diacritics are preserved.
   - **Filler/backchannel stripping** — ``filler_removal.py`` removes pure hesitation vocalizations and backchannels (discourse markers like *genau*, *tipo*, *そうですね* are kept).
   
   Segments where the **reference** has no real speech left after normalization (NSV-only, empty, filler-only, or backchannel-only) are marked `scored: false` and excluded from metrics.
4. **Scoring** — on all `scored` segments, micro-averaged via `jiwer`:
   - **WER** — word error rate on whitespace-delimited tokens.
   - **CER** — character error rate on whitespace-stripped text (preferred for Japanese).
   - **WCMR** — share of segments where reference and hypothesis **word counts** differ (`len(ref.split()) != len(hyp.split())`), plus breakdown by gap size |m−n|.

Results are written per conversation as `metrics.json`. The Excel report aggregates by batch and language, and compares against an independent **baseline reference** corpus (same scoring pipeline, different vendor annotations).

**Reading the numbers:** lower WER, CER, and WCMR are better. For **Japanese**, trust **CER** over WER/WCMR (annotation uses morpheme spacing; Qwen outputs unsegmented text, which inflates word-count metrics). For **Arabic**, Qwen3-ASR is poor and inconsistent — treat WER/WCMR with caution.

Methodology aligns with `Sample_review_report_06042026.md`.

---

## Folder layout

```
Conversations/
  <batch>/                          e.g. delivery_batch_06092026
    <conversation>/                 e.g. NV-KO-SS03-CONVO07
      SPK01.seglst.json               human annotation (input)
      SPK01.wav                       per-speaker audio
      SPK01_transcript.jsonl          step 1 output
      SPK01_qwen.jsonl                step 2 output
      SPK01_transcript_norm.jsonl     step 3 output
      SPK01_qwen_norm.jsonl           step 3 output
      SPK01_top_errors.json           step 4 output (optional review)
      metrics.json                    step 5 output
      SPK01_der.rttm                  DetER speech-only reference (from seglst)
      SPK01_sad.rttm                  DetER SAD hypothesis (Sortformer ∪ Silero)
      SPK01_deter.json                DetER per-speaker result
      deter.json                      DetER conversation rollup
```

Legacy ``SPK*.rttm`` files (if present) copy every seglst turn including NSV-only
segments; **do not** use them for DetER. The pipeline writes ``SPK*_der.rttm`` instead.

---

## DetER pipeline (optional)

See [`diarization_pipeline/README.md`](diarization_pipeline/README.md) for the
full DetER (detection error rate) pipeline: speech-only reference RTTMs,
configurable SAD hypothesis (`--sad-mode sortformer|silero|union`), and NeMo scoring.

Quick start:

```powershell
.\.venv\Scripts\pip.exe install -r diarization_pipeline\requirements.txt

python -m diarization_pipeline.deter_calculation --conversation NV-KO-SS03-CONVO08
python -m diarization_pipeline.deter_calculation --sad-mode sortformer --conversation NV-KO-SS03-CONVO08
```

---

## Setup

### 1. Create a virtual environment and install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
```

For **GPU** transcription (recommended), install a CUDA build of PyTorch **before or after** the requirements file:

```powershell
.\.venv\Scripts\pip.exe install torch --index-url https://download.pytorch.org/whl/cu128
```

Pick the `cuXXX` index that matches your driver: [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/)

### 2. Verify the environment

```powershell
.\.venv\Scripts\python.exe test_imports.py
```

Confirms imports, `BasicTextNormalizer`, and `Qwen3ASRModel` load. Reports whether CUDA is available.

---

## Pipeline (run in order)

All workflow scripts share the same scope arguments (from `workflow_common.py`):

| Argument | Description |
|----------|-------------|
| `--conversations` | Root folder (default: `Conversations`) |
| `--batch` | Single batch folder, e.g. `delivery_batch_06092026` |
| `--conversation` | Single session, e.g. `NV-KO-SS03-CONVO07` |
| `--file` | Single speaker, e.g. `SPK01` (requires `--conversation`) |
| `--overwrite` | Reprocess even if output already exists |
| `--limit N` | Process only the first N items (0 = all) |

---

### Step 1 — `transcript_extraction.py`

**What it does:** Reads `SPK*.seglst.json` and writes one row per segment to `SPK*_transcript.jsonl`. Text is kept **raw** (NSV tags like `[laugh]` preserved). Each line includes `idx`, `session_id`, `language`, `speaker`, `start`, `end`, and `text`.

**Run:**

```powershell
# all conversations in all batches
.\.venv\Scripts\python.exe transcript_extraction.py

# one batch
.\.venv\Scripts\python.exe transcript_extraction.py --batch delivery_batch_06092026

# one conversation
.\.venv\Scripts\python.exe transcript_extraction.py --conversation NV-KO-SS03-CONVO07

# one speaker
.\.venv\Scripts\python.exe transcript_extraction.py --conversation NV-KO-SS03-CONVO07 --file SPK01
```

---

### Step 2 — `qwen_asr_transcription.py`

**What it does:** For each `SPK*_transcript.jsonl`, loads the matching `SPK*.wav`, slices audio per segment timestamp, transcribes each slice with **Qwen3-ASR-1.7B**, and writes row-aligned `SPK*_qwen.jsonl` (same row count and `idx` as the reference).

**Run:**

```powershell
# all (slow — downloads/runs the model on first use)
.\.venv\Scripts\python.exe qwen_asr_transcription.py

# smoke test: first item only
.\.venv\Scripts\python.exe qwen_asr_transcription.py --limit 1

# one conversation
.\.venv\Scripts\python.exe qwen_asr_transcription.py --conversation NV-KO-SS03-CONVO07

# one speaker
.\.venv\Scripts\python.exe qwen_asr_transcription.py --conversation NV-KO-SS03-CONVO07 --file SPK03

# re-run after code/model changes
.\.venv\Scripts\python.exe qwen_asr_transcription.py --overwrite
```

Uses `float16` on Turing GPUs (e.g. RTX 2070). Requires network on first run to download model weights from Hugging Face.

---

### Step 3 — `normalize_transcripts.py`

**What it does:** Pairs each `SPK*_transcript.jsonl` with `SPK*_qwen.jsonl` and writes:

- `SPK*_transcript_norm.jsonl` (normalized human annotation)
- `SPK*_qwen_norm.jsonl` (normalized Qwen output)

Both sides go through the **same normalization track**:

1. **Whisper `BasicTextNormalizer`** on the raw text — lowercases, NFKC, strips punctuation and bracketed tokens. Well-formed **NSV tags** (`[laugh]`, `[breath]`, `[inhale]`, etc.) are removed here (they are not counted as words in WER/CER/WCMR). The original raw text is kept in the `text` field; the cleaned string is in `text_norm`.
2. **Filler/backchannel stripping** via ``filler_removal.py`` — removes pure hesitation/backchannel vocalizations; segments whose reference is empty after this step are marked `scored: false` (`drop_reason: filler_only`).

Each row gets `text_norm`, `scored` (bool), and `drop_reason`. If the reference is NSV-only, normalization leaves nothing to score → `drop_reason: "empty"`, `scored: false`. Scoring eligibility is decided from the **reference** only, so the two files stay row-aligned.

**Run:**

```powershell
.\.venv\Scripts\python.exe normalize_transcripts.py

.\.venv\Scripts\python.exe normalize_transcripts.py --batch delivery_batch_06092026

.\.venv\Scripts\python.exe normalize_transcripts.py --conversation NV-AR-SS03-CONVO09 --file SPK01
```

---

### Step 4 — `rank_error_segments.py` (optional review)

**What it does:** Joins `SPK*_transcript_norm.jsonl` with `SPK*_qwen_norm.jsonl` on scored rows and ranks segments by absolute error count. Writes `SPK*_top_errors.json` per speaker with the worst segments for manual review.

- **Japanese:** ranked by **CER** (character errors, whitespace stripped).
- **Other languages:** ranked by **WER** (word errors, whitespace `.split()`).

**Run:**

```powershell
.\.venv\Scripts\python.exe rank_error_segments.py

.\.venv\Scripts\python.exe rank_error_segments.py --conversation NV-JA-SS04-CONVO11

.\.venv\Scripts\python.exe rank_error_segments.py --conversation NV-KO-SS03-CONVO07 --file SPK01

.\.venv\Scripts\python.exe rank_error_segments.py --top 20 --min-ref-units 5 --overwrite
```

---

### Step 5 — `compute_metrics.py`

**What it does:** Joins normalized reference and hypothesis by `idx`, keeps `scored == true` rows, and computes WER, CER, and WCMR per speaker and per conversation. Writes `metrics.json` into each conversation folder (includes raw error counts for micro-aggregation).

**Run:**

```powershell
.\.venv\Scripts\python.exe compute_metrics.py

.\.venv\Scripts\python.exe compute_metrics.py --batch delivery_batch_06092026

.\.venv\Scripts\python.exe compute_metrics.py --conversation NV-AR-SS03-CONVO09

.\.venv\Scripts\python.exe compute_metrics.py --overwrite
```

---

### Step 6 — `generate_report.py`

**What it does:** Reads all `metrics.json` files and builds `reports/transcription_accuracy_metrics.xlsx` with:

- **Definitions** — column glossary
- **One tab per batch** — language summary (cols A–K) and per-conversation table (cols M→) side by side
- **All Batches** — combined view
- **top_erroneous_segments** — worst segments per speaker (from `SPK*_top_errors.json`; run `rank_error_segments.py` first)
- **Reference** — baseline reference numbers per language

Δ columns show human-annotated transcript minus baseline (percentage points), color-coded.

**Run:**

```powershell
.\.venv\Scripts\python.exe generate_report.py

.\.venv\Scripts\python.exe generate_report.py --output reports/transcription_accuracy_metrics.xlsx

.\.venv\Scripts\python.exe generate_report.py --batch delivery_batch_06092026
```

---

## Supporting files

| File | Role |
|------|------|
| `workflow_common.py` | Shared `--batch` / `--conversation` / `--file` argument parsing and file discovery |
| `filler_removal.py` | Language-specific filler/backchannel removal for normalization |
| `diarization_pipeline/` | DetER pipeline (seglst ref RTTM, SAD hypothesis, NeMo scoring) |
| `guidelines_for_languages/` | Source transcription guidelines (reference for annotation rules) |
| `requirements.txt` | Python dependencies |
| `test_imports.py` | Environment smoke test |
| `Sample_review_report_06042026.md` | Reference methodology and baseline context |

---

## Full run (example)

```powershell
.\.venv\Scripts\python.exe transcript_extraction.py
.\.venv\Scripts\python.exe qwen_asr_transcription.py
.\.venv\Scripts\python.exe normalize_transcripts.py
.\.venv\Scripts\python.exe rank_error_segments.py
.\.venv\Scripts\python.exe compute_metrics.py
.\.venv\Scripts\python.exe generate_report.py
```

Output: `reports/transcription_accuracy_metrics.xlsx`
