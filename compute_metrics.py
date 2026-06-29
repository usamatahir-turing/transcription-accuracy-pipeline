"""Backward-compatible entry point. See ``word_error_pipeline.compute_metrics``."""

from word_error_pipeline.compute_metrics import main

if __name__ == "__main__":
    raise SystemExit(main())
