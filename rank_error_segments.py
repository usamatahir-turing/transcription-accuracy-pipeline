"""Backward-compatible entry point. See ``word_error_pipeline.rank_error_segments``."""

from word_error_pipeline.rank_error_segments import main

if __name__ == "__main__":
    raise SystemExit(main())
