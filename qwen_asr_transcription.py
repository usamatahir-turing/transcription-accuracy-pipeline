"""Backward-compatible entry point. See ``word_error_pipeline.qwen_asr_transcription``."""

from word_error_pipeline.qwen_asr_transcription import main

if __name__ == "__main__":
    raise SystemExit(main())
