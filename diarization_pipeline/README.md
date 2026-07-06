# DetER (detection error rate) pipeline

Measures how well automated speech-activity detection covers the human
**speech-only** seglst timeline. Not full diarization DER — reference and
hypothesis are flattened to one `speech` track (no speaker confusion).

## Install

```powershell
.\.venv\Scripts\pip.exe install -r diarization_pipeline\requirements.txt
```

## SAD modes (`--sad-mode`)

| Mode | Hypothesis |
|------|------------|
| `union` | Sortformer + Silero VAD union (**default**, matches client QA spec) |
| `sortformer` | Sortformer diarizer only |
| `silero` | Silero VAD only |

## Scripts

Run from the repo root:

```powershell
# Reference RTTMs only (no GPU)
python -m diarization_pipeline.seglst_to_rttm --conversation NV-KO-SS03-CONVO08

# SAD hypothesis RTTMs
python -m diarization_pipeline.sad_hypothesis --conversation NV-KO-SS03-CONVO08
python -m diarization_pipeline.sad_hypothesis --sad-mode sortformer --conversation NV-KO-SS03-CONVO08

# Full pipeline (ref + SAD + score)
python -m diarization_pipeline.deter_calculation --conversation NV-KO-SS03-CONVO08
python -m diarization_pipeline.deter_calculation --sad-mode sortformer --conversation NV-KO-SS03-CONVO08

# Re-score existing RTTMs
python -m diarization_pipeline.deter_calculation --score-only --reuse-sad --conversation NV-KO-SS03-CONVO08

# Rank worst DetER intervals for Excel review tab
python -m diarization_pipeline.rank_deter_error_segments --conversation NV-KO-SS03-CONVO08
```

## Outputs (per conversation folder)

| File | Role |
|------|------|
| `SPK*_der.rttm` | Speech-only reference from seglst |
| `SPK*_sad.rttm` | SAD hypothesis (mode selected via `--sad-mode`) |
| `SPK*_deter.json` | Per-speaker DetER + diagnostics |
| `SPK*_top_deter_errors.json` | Top 10 missed + top 10 false-alarm intervals per speaker |
| `deter.json` | Conversation rollup |

Pass threshold: **10% per channel** (`--deter-ch-max 0.10`). Collar: **0.25 s**.

NSV-only seglst turns (`[laugh]`, `[inhale]`, …) are excluded from DetER scoring
via a UEM (un-partitioned evaluation map), matching `chsep_audio_qa` with
`--deter_uem_exclude_nsv`. VAD firing on those intervals is neither a false alarm
nor a miss.
