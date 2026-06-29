"""Backward-compatible entry point. See ``word_error_pipeline.transcript_extraction``."""

from word_error_pipeline.transcript_extraction import main

if __name__ == "__main__":
    raise SystemExit(main())
