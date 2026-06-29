"""Copy all files from a delivery batch into ``Conversations/``.

The input path must be a batch folder whose immediate subfolders are
conversation directories (e.g. ``NV-KO-SS03-CONVO08/``), each holding
``SPK*.seglst.json``, ``SPK*.wav``, ``SPK*.rttm``, and related assets.

Destination layout::

    Conversations/<batch>/<conversation>/<filename>

By default, existing destination files with the same name are skipped.
Use ``--overwrite`` to replace them.

Usage
-----
    .\\.venv\\Scripts\\python.exe copy_delivery_batch.py G:\\\\path\\\\to\\\\delivery_batch_06162026 \\
        --batch delivery_batch_06162026

    .\\.venv\\Scripts\\python.exe copy_delivery_batch.py G:\\\\path\\\\to\\\\batch \\
        --batch delivery_batch_06162026 \\
        --conversation NV-KO-SS03-CONVO08 --conversation NV-PT-SS03-CONVO07

    .\\.venv\\Scripts\\python.exe copy_delivery_batch.py G:\\\\path\\\\to\\\\batch \\
        --batch delivery_batch_06162026 --dry-run
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

DEFAULT_CONVERSATIONS_ROOT = Path("Conversations")


def discover_conversation_dirs(batch_dir: Path,
                             only: list[str] | None = None) -> list[Path]:
    """Return sorted conversation subdirectories under ``batch_dir``."""
    if not batch_dir.is_dir():
        raise FileNotFoundError(f"input batch folder not found: {batch_dir.resolve()}")

    conv_dirs = sorted(p for p in batch_dir.iterdir() if p.is_dir())
    if not conv_dirs:
        raise FileNotFoundError(f"no conversation subfolders in {batch_dir.resolve()}")

    if only:
        wanted = set(only)
        by_name = {p.name: p for p in conv_dirs}
        missing = sorted(wanted - by_name.keys())
        if missing:
            raise FileNotFoundError(
                f"conversation(s) not found under {batch_dir.name}: "
                + ", ".join(missing),
            )
        conv_dirs = [by_name[name] for name in sorted(wanted)]

    return conv_dirs


def copy_batch(
    input_dir: Path,
    dest_root: Path,
    batch_name: str,
    *,
    conversations: list[str] | None = None,
    overwrite: bool = False,
    dry_run: bool = False,
) -> dict[str, int]:
    """Copy every file in each conversation folder; return action counts."""
    counts = {"copied": 0, "skipped": 0, "overwritten": 0, "empty": 0}
    dest_batch = dest_root / batch_name

    for conv_dir in discover_conversation_dirs(input_dir, conversations):
        src_files = sorted(p for p in conv_dir.iterdir() if p.is_file())
        if not src_files:
            print(f"  WARN {conv_dir.name}: no files", file=sys.stderr)
            counts["empty"] += 1
            continue

        dest_conv = dest_batch / conv_dir.name
        for src in src_files:
            dest = dest_conv / src.name
            if dest.is_file() and not overwrite:
                print(f"  skip  {dest.relative_to(dest_root)}")
                counts["skipped"] += 1
                continue

            action = "overwrite" if dest.is_file() else "copy"
            rel = dest.relative_to(dest_root)
            if dry_run:
                print(f"  {action} {rel}")
            else:
                dest_conv.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
                print(f"  {action} {rel}")

            counts["overwritten" if action == "overwrite" else "copied"] += 1

    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "input",
        type=Path,
        help="Path to the delivery batch folder (contains conversation subfolders).",
    )
    parser.add_argument(
        "--batch",
        required=True,
        help="Destination batch name under Conversations/, "
             "e.g. delivery_batch_06162026.",
    )
    parser.add_argument(
        "--conversation",
        action="append",
        default=[],
        metavar="NAME",
        help="Copy only this conversation subfolder; repeat for multiple.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace destination files that already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without copying files.",
    )
    args = parser.parse_args(argv)

    input_dir = args.input.resolve()
    dest_root = DEFAULT_CONVERSATIONS_ROOT.resolve()
    only = args.conversation or None

    print(f"Source batch : {input_dir}")
    print(f"Destination  : {dest_root / args.batch}")
    if only:
        print(f"Conversations: {', '.join(only)}")
    if args.dry_run:
        print("Mode         : dry-run")

    try:
        counts = copy_batch(
            input_dir,
            dest_root,
            args.batch,
            conversations=only,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
        )
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    verb = "Would copy" if args.dry_run else "Copied"
    print(
        f"\n{verb}: {counts['copied']}  "
        f"Overwritten: {counts['overwritten']}  "
        f"Skipped: {counts['skipped']}  "
        f"Empty conv dirs: {counts['empty']}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
