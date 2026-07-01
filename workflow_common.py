"""Shared scope-resolution helpers for the batched Conversations layout.

Folder layout:

    Conversations/<batch>/<conversation>/<channel>/...

All workflow scripts (``word_error_pipeline/``, ``run_pipeline.py``, and the
``diarization_pipeline/`` DetER scripts) use these helpers so they share the same
``--batch`` / ``--conversation`` / ``--file`` / ``--overwrite`` / ``--limit``
arguments and discovery behavior.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def add_scope_args(parser: argparse.ArgumentParser, with_file: bool = False) -> None:
    """Add the common scope-selection arguments to a parser."""
    parser.add_argument("--conversations", default="Conversations",
                        help="Root folder (default: ./Conversations).")
    parser.add_argument("--batch", default=None,
                        help="Only this batch folder, e.g. delivery_batch_06092026.")
    parser.add_argument(
        "--conversation",
        action="append",
        default=None,
        metavar="NAME",
        help="Only this conversation, e.g. NV-AR-SS03-CONVO09; repeat for "
             "multiple (searched across all batches unless --batch is given).",
    )
    if with_file:
        parser.add_argument("--file", default=None,
                            help="Only this channel stem, e.g. SPK01. Requires --conversation.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Reprocess items whose output already exists.")
    parser.add_argument("--limit", type=int, default=0,
                        help="Process only the first N items (0 = all).")


def _conversation_filter(
    conversation: str | list[str] | None,
) -> set[str] | None:
    if conversation is None:
        return None
    if isinstance(conversation, str):
        return {conversation}
    return set(conversation)


def resolve_conversation_dirs(root: Path, batch: str | None = None,
                              conversation: str | list[str] | None = None) -> list[Path]:
    """Return conversation directories (root/<batch>/<conversation>) in scope.

    ``conversation`` may be a single name or a list; when omitted, all
    conversations in scope are returned. Raises FileNotFoundError for a bad
    batch or any requested conversation name with no matching folder.
    """
    if not root.is_dir():
        raise FileNotFoundError(f"conversations folder not found: {root.resolve()}")

    if batch:
        bdir = root / batch
        if not bdir.is_dir():
            raise FileNotFoundError(f"batch folder not found: {bdir.resolve()}")
        batch_dirs = [bdir]
    else:
        batch_dirs = sorted(p for p in root.iterdir() if p.is_dir())

    wanted = _conversation_filter(conversation)

    conv_dirs: list[Path] = []
    for b in batch_dirs:
        for c in sorted(p for p in b.iterdir() if p.is_dir()):
            if wanted and c.name not in wanted:
                continue
            conv_dirs.append(c)

    if wanted:
        found = {c.name for c in conv_dirs}
        missing = sorted(wanted - found)
        if missing:
            where = f" in batch {batch!r}" if batch else ""
            names = ", ".join(missing)
            raise FileNotFoundError(
                f"conversation(s) not found{where}: {names}.")
    return conv_dirs


def resolve_speaker_files(root: Path, batch: str | None, conversation: str | None,
                          file: str | None, suffix: str) -> list[Path]:
    """Return channel files matching ``*{suffix}`` across the resolved scope.

    If ``file`` (e.g. 'SPK01') is given it requires ``conversation`` and matches
    that single channel's ``{file}{suffix}`` in each resolved conversation.
    """
    if file and not conversation:
        raise ValueError("--file requires --conversation to also be set.")

    conv_dirs = resolve_conversation_dirs(root, batch, conversation)
    files: list[Path] = []
    for cdir in conv_dirs:
        if file:
            p = cdir / f"{file}{suffix}"
            if p.is_file():
                files.append(p)
        else:
            files.extend(sorted(cdir.glob(f"*{suffix}")))

    if file and not files:
        raise FileNotFoundError(
            f"speaker file {file}{suffix} not found for the given scope.")
    return files
