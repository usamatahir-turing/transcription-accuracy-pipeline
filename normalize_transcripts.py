"""Backward-compatible entry point. See ``word_error_pipeline.normalize_transcripts``."""

from word_error_pipeline.normalize_transcripts import main

if __name__ == "__main__":
    raise SystemExit(main())
