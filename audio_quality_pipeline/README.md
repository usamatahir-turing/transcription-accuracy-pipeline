# Audio quality pipeline

Client review methodology from `sample_review_report_delivery0701_0707_2026.md`:

| Module | Report section | Metric |
|--------|----------------|--------|
| `dnsmos_calculation` | §3.2 | DNSMOS P.835 SIG / BAK / OVRL |
| `bandwidth_calculation` | §3.3 | Effective bandwidth (LTAS cutoff) |

Neither module is wired into `run_pipeline.py` yet — run them separately.

## Install

```powershell
.\.venv\Scripts\pip.exe install -r audio_quality_pipeline\requirements.txt
```

### DNSMOS GPU notes

Uses Microsoft DNSMOS P.835 (`sig_bak_ovr.onnx`) via `onnxruntime-gpu`.
Install with the `[cuda,cudnn]` extras (CUDA 12 wheels). On first score you should
see `CUDAExecutionProvider`. If CUDA fails to load, scoring falls back to CPU.
Weights download into `audio_quality_pipeline/models/` on first run.

---

## DNSMOS P.835

| Item | Behaviour |
|------|-----------|
| Inputs | Individual speaker `*.wav` next to `*.seglst.json` |
| Speech mask (default) | **Speech timeline**: keep full file length, zero non-speech seglst gaps (NSV-only dropped) |
| Polyfit (default) | **Personalized** (Microsoft `dnsmos_local.py -p`) |
| Pass rule | `SIG > 3.0` |
| Mixed tracks | Not scored in v1 |

Defaults were calibrated against client-report Worst-100 SIG (Batch 4 fails).
Overrides: `--window speech_concat|speech_timeline|full`, `--non-personalized`.

```powershell
python -m audio_quality_pipeline.dnsmos_calculation --conversation NV-KO-SS15-CONVO34
python -m audio_quality_pipeline.dnsmos_calculation --batch delivery_batch_07142026 --overwrite
# previous behaviour:
python -m audio_quality_pipeline.dnsmos_calculation --window speech_concat --non-personalized --overwrite
```

| Output | Role |
|--------|------|
| `{speaker}_dnsmos.json` | Per-channel SIG/BAK/OVRL + diagnostics |
| `dnsmos.json` | Conversation rollup |

### Export CSV

```powershell
python -m audio_quality_pipeline.export_dnsmos_csv
python -m audio_quality_pipeline.export_dnsmos_csv --batch delivery_batch_07142026
```

Writes `audio_quality_pipeline/reports/dnsmos_channels.csv` with columns:
`batch, session_id, file_name, sig, bak, ovrl, pass, speech_min, peak_dbfs`
(sorted by batch, session_id, file_name). `file_name` is the channel WAV
(e.g. `SPK01.wav`). Use `-o` to change the path.

---

## Effective bandwidth (§3.3)

Estimates the highest frequency with **sustained** speech energy (median LTAS
over speech frames, contiguous ~300 Hz band ≥12 dB above the HF noise floor).
This is **not** the max FFT bin with any energy.

| Item | Behaviour |
|------|-----------|
| Inputs | Same speech-masked channels as DNSMOS |
| Pass rule | `effective_hz > 8000` (severe ≤8 kHz group fails) |
| Buckets | `le_8khz` / `le_12khz` / `le_16khz` / `gt_16khz` |
| Spectrograms | `{speaker}_bandwidth_spectrogram.png` (skip with `--no-spectrogram`) |

```powershell
python -m audio_quality_pipeline.bandwidth_calculation --conversation NV-GR-SS08-CONVO15
python -m audio_quality_pipeline.bandwidth_calculation --batch delivery_batch_07142026 --overwrite
python -m audio_quality_pipeline.bandwidth_calculation --conversation NV-GR-SS08-CONVO15 --no-spectrogram
```

| Output | Role |
|--------|------|
| `{speaker}_bandwidth.json` | `effective_hz`, bucket, flags, method |
| `{speaker}_bandwidth_spectrogram.png` | Log-power STFT for listening review |
| `bandwidth.json` | Rollup: `n_le_8khz` / `n_le_12khz` / `n_le_16khz` (nested counts like the report) |

### How to analyze

1. Count `bucket == le_8khz` (and nested ≤12 / ≤16) across a batch — same style as the report table.
2. Join with DNSMOS on `speaker` / `session_id` (bandwidth defects often sit near SIG≈3.0).
3. Open spectrogram PNGs for `le_8khz` channels; confirm a dark band above ~8 kHz.
4. Flag sessions where any speaker fails (`conversation.pass == false`).

Scope flags match the rest of the repo (`--conversations`, `--batch`,
`--conversation` repeatable, `--overwrite`, `--limit`).

Email-style channel IDs (`ha.c1@turing.com`) use the same output naming as DetER
(`ha.c1_bandwidth.json`); the WAV is still read as `ha.c1@turing.com.wav`.
