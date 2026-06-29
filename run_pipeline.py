"""Run DetER + WER pipelines for Conversations data.

Default (full) run:

  1. ``diarization_pipeline.deter_calculation`` - DetER scoring
  2. ``word_error_pipeline`` - extract -> ASR -> normalize -> rank -> metrics

``generate_report.py`` is intentionally excluded; run it manually after metrics exist.

Usage
-----
    python run_pipeline.py --batch delivery_batch_06302026
    python run_pipeline.py --conversation NV-KO-SS03-CONVO07 --skip-deter
    python run_pipeline.py --batch delivery_batch_06302026 --skip-wer
"""

from __future__ import annotations

import argparse
from collections.abc import Callable

from workflow_common import add_scope_args


def build_scope_argv(args: argparse.Namespace) -> list[str]:
    argv: list[str] = []
    if args.conversations != "Conversations":
        argv.extend(["--conversations", args.conversations])
    if args.batch:
        argv.extend(["--batch", args.batch])
    if args.conversation:
        argv.extend(["--conversation", args.conversation])
    if args.file:
        argv.extend(["--file", args.file])
    if args.overwrite:
        argv.append("--overwrite")
    if args.limit:
        argv.extend(["--limit", str(args.limit)])
    return argv


def build_deter_argv(args: argparse.Namespace) -> list[str]:
    argv = build_scope_argv(args)
    argv.extend(["--sad-mode", args.sad_mode])
    if args.reuse_sad:
        argv.append("--reuse-sad")
    if args.ref_only:
        argv.append("--ref-only")
    if args.score_only:
        argv.append("--score-only")
    if args.deter_collar is not None:
        argv.extend(["--collar", str(args.deter_collar)])
    if args.deter_batch_size is not None:
        argv.extend(["--batch-size", str(args.deter_batch_size)])
    return argv


def build_qwen_argv(args: argparse.Namespace) -> list[str]:
    argv = build_scope_argv(args)
    if args.qwen_batch_size is not None:
        argv.extend(["--batch-size", str(args.qwen_batch_size)])
    return argv


def build_rank_argv(args: argparse.Namespace) -> list[str]:
    argv = build_scope_argv(args)
    if args.top is not None:
        argv.extend(["--top", str(args.top)])
    if args.min_ref_units is not None:
        argv.extend(["--min-ref-units", str(args.min_ref_units)])
    return argv


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_scope_args(parser, with_file=True)
    parser.add_argument(
        "--skip-deter",
        action="store_true",
        help="Skip the DetER pipeline (diarization_pipeline).",
    )
    parser.add_argument(
        "--skip-wer",
        action="store_true",
        help="Skip the WER pipeline (word_error_pipeline).",
    )
    parser.add_argument(
        "--sad-mode",
        choices=("sortformer", "silero", "union"),
        default="union",
        help="DetER SAD hypothesis mode (default: union).",
    )
    parser.add_argument(
        "--reuse-sad",
        action="store_true",
        help="Reuse existing *_sad.rttm files during DetER scoring.",
    )
    parser.add_argument(
        "--ref-only",
        action="store_true",
        help="DetER: only build SPK*_der.rttm reference RTTMs.",
    )
    parser.add_argument(
        "--score-only",
        action="store_true",
        help="DetER: score from existing RTTMs; skip ref/SAD generation.",
    )
    parser.add_argument(
        "--deter-collar",
        type=float,
        default=None,
        help="DetER scoring collar in seconds (default: pipeline default).",
    )
    parser.add_argument(
        "--deter-batch-size",
        type=int,
        default=None,
        help="Sortformer batch size when running DetER SAD (default: pipeline default).",
    )
    parser.add_argument(
        "--qwen-batch-size",
        type=int,
        default=None,
        help="Qwen ASR batch size (default: pipeline default).",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Segments per speaker in rank_error_segments (default: pipeline default).",
    )
    parser.add_argument(
        "--min-ref-units",
        type=int,
        default=None,
        help="Minimum reference units for rank_error_segments (default: pipeline default).",
    )
    args = parser.parse_args(argv)

    if args.skip_deter and args.skip_wer:
        print("ERROR: --skip-deter and --skip-wer cannot both be set.")
        return 1

    steps: list[tuple[str, Callable[[list[str] | None], int], list[str]]] = []
    if not args.skip_deter:
        from diarization_pipeline.deter_calculation import main as deter_main

        steps.append(("DetER", deter_main, build_deter_argv(args)))
    if not args.skip_wer:
        from word_error_pipeline.compute_metrics import main as metrics_main
        from word_error_pipeline.normalize_transcripts import main as normalize_main
        from word_error_pipeline.qwen_asr_transcription import main as qwen_main
        from word_error_pipeline.rank_error_segments import main as rank_main
        from word_error_pipeline.transcript_extraction import main as extract_main

        scope = build_scope_argv(args)
        steps.extend(
            [
                ("transcript extraction", extract_main, scope),
                ("Qwen ASR", qwen_main, build_qwen_argv(args)),
                ("normalize transcripts", normalize_main, scope),
                ("rank error segments", rank_main, build_rank_argv(args)),
                ("compute metrics", metrics_main, scope),
            ]
        )

    for name, step_main, step_argv in steps:
        print(f"\n{'=' * 60}\n>>> {name}\n{'=' * 60}\n")
        rc = step_main(step_argv)
        if rc != 0:
            print(f"\nPipeline stopped: {name} exited with code {rc}.")
            return rc

    print("\nPipeline complete.")
    if not args.skip_wer:
        print("Run generate_report.py manually to build the Excel report.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
