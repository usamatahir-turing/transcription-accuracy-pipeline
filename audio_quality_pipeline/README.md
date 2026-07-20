# Audio quality pipeline — DNSMOS P.835

Perceptual speech quality screening (**SIG** / **BAK** / **OVRL**) matching the
client review methodology in `sample_review_report_delivery0701_0707_2026.md`
§3.2.

## Install

```powershell
.\.venv\Scripts\pip.exe install -r audio_quality_pipeline\requirements.txt
```

Uses **Microsoft DNSMOS P.835** (`sig_bak_ovr.onnx`) via `onnxruntime-gpu`
when CUDA is available (falls back to CPU otherwise). The ONNX weights download
automatically into `audio_quality_pipeline/models/` on first run.

Install with `pip install -r audio_quality_pipeline/requirements.txt` so the
`[cuda,cudnn]` extras (CUDA 12 wheels) are present. On first score you should
see `CUDAExecutionProvider` in the provider list. If CUDA still fails to load,
scoring falls back to CPU.

## What is scored

| Item | Behaviour |
|------|-----------|
| Inputs | Individual speaker `*.wav` next to `*.seglst.json` |
| Speech mask | Speech-only seglst (same `is_speech_segment` as DetER; NSV-only dropped) |
| Pass rule | `SIG > 3.0` (warning threshold from the review report) |
| Mixed tracks | Not scored in v1 |

## Usage

```powershell
# One conversation
python -m audio_quality_pipeline.dnsmos_calculation --conversation NV-KO-SS15-CONVO34

# Whole batch
python -m audio_quality_pipeline.dnsmos_calculation --batch delivery_batch_07142026

# Force re-score
python -m audio_quality_pipeline.dnsmos_calculation --batch delivery_batch_07142026 --overwrite
```

Scope flags match the rest of the repo (`--conversations`, `--batch`,
`--conversation` repeatable, `--overwrite`, `--limit`).

**Not** wired into `run_pipeline.py` yet — run this module separately.

## Outputs (per conversation folder)

| File | Role |
|------|------|
| `{speaker}_dnsmos.json` | Per-channel SIG/BAK/OVRL + speech diagnostics |
| `dnsmos.json` | Conversation rollup (means, fail counts) |

Example per-channel fields: `dnsmos.sig` / `bak` / `ovrl`, `diagnostics.speech_min`,
`diagnostics.peak_dbfs`, `flags` (e.g. `sig_below_3.0`).

## Notes

- DNSMOS does **not** produce bandwidth spectrograms or localize clipping; those
  are separate analyses in the client report.
- Email-style channel IDs (`ha.c1@turing.com`) use the same output naming as
  DetER (`ha.c1_dnsmos.json`); the WAV is still read as `ha.c1@turing.com.wav`.
