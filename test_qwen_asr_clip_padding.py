"""Unit tests for Qwen ASR clip padding (no model load)."""

import numpy as np

from word_error_pipeline.qwen_asr_transcription import (
    min_asr_clip_samples,
    prepare_clip_for_asr,
    slice_clip,
)


def test_min_asr_clip_samples_at_16k():
    assert min_asr_clip_samples(16000) == 400


def test_prepare_clip_for_asr_pads_short_clips():
    clip = np.ones(160, dtype=np.float32)
    out = prepare_clip_for_asr(clip, 16000)
    assert out.shape == (400,)
    assert np.allclose(out[:160], 1.0)
    assert np.allclose(out[160:], 0.0)


def test_prepare_clip_for_asr_leaves_long_clips():
    clip = np.arange(500, dtype=np.float32)
    out = prepare_clip_for_asr(clip, 16000)
    assert out is clip


def test_slice_clip_zero_length():
    audio = np.zeros(16000, dtype=np.float32)
    assert slice_clip(audio, 16000, 1.0, 1.0).shape == (0,)
