# Word-error pipeline

Segment-level WER/CER/WCMR evaluation against Qwen3-ASR hypotheses.

## Steps (in order)

| Module | Input | Output |
|--------|-------|--------|
| `transcript_extraction.py` | `*.seglst.json` | `{stem}_transcript.jsonl` |
| `qwen_asr_transcription.py` | transcript + `*.wav` | `{stem}_qwen.jsonl` |
| `normalize_transcripts.py` | transcript + qwen jsonl | `{stem}_transcript_norm.jsonl`, `{stem}_qwen_norm.jsonl` |
| `rank_error_segments.py` | norm jsonl pair | `{stem}_top_errors.json` |
| `compute_metrics.py` | norm jsonl pair | `metrics.json` |

All steps share scope arguments from `workflow_common.py` at the repo root.

## Run individually

```powershell
python -m word_error_pipeline.transcript_extraction --batch delivery_batch_06302026
python -m word_error_pipeline.qwen_asr_transcription --batch delivery_batch_06302026
python -m word_error_pipeline.normalize_transcripts --batch delivery_batch_06302026
python -m word_error_pipeline.rank_error_segments --batch delivery_batch_06302026
python -m word_error_pipeline.compute_metrics --batch delivery_batch_06302026
```

Root-level shims (`python transcript_extraction.py`, etc.) delegate to these modules.

## Full orchestration

Use `run_pipeline.py` at the repo root to run DetER + this pipeline in one command.
`generate_report.py` is run separately after metrics are produced.
