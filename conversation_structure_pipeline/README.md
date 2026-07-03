# Conversation structure pipeline

Metrics derived from multi-speaker seglst timelines (speech-only segments).

## Overlap ratio

Canonical definition (same as `chsep_audio_qa/ami_rttm_stats.py`):

    overlap_ratio = T_overlap / T_speech

- **T_speech** — wall-clock seconds where at least one speaker has speech
- **T_overlap** — wall-clock seconds where two or more speakers overlap

NSV-only seglst segments are excluded (same rules as DetER `*_der.rttm`).

## Run

```powershell
python -m conversation_structure_pipeline.overlap_calculation --batch delivery_batch_05192026
python -m conversation_structure_pipeline.overlap_calculation --conversation NV-KO-SS03-CONVO08
```

Output: `Conversations/<batch>/<conversation>/overlap_ratio.json`

Also runs as part of `run_pipeline.py` (after DetER, before WER). Use `--skip-overlap` to omit.
