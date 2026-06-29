"""Backward-compatible entry point. See ``word_error_pipeline.filler_removal``."""

import sys

from word_error_pipeline.filler_removal import _cli

if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
