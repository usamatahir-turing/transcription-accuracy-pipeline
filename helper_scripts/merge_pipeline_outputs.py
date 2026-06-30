"""Merge pipeline outputs from ``Conversations_output_files/`` into ``Conversations/``.

For each file under the output folder, copy it to the same relative path under
``Conversations/`` when:

  - the destination directory already exists, and
  - no file with that name is already there.

Skips files when the destination folder is missing (folders are never created)
or when the destination file already exists.

Run once from the repo root:
    python helper_scripts/merge_pipeline_outputs.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

SOURCE = Path("Conversations_output_files")
DEST = Path("Conversations")


def main() -> int:
    if not SOURCE.is_dir():
        print(f"ERROR: source folder not found: {SOURCE.resolve()}")
        return 1
    if not DEST.is_dir():
        print(f"ERROR: destination folder not found: {DEST.resolve()}")
        return 1

    n_copied = n_skip_exists = n_skip_no_dir = 0

    for src in sorted(SOURCE.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(SOURCE)
        out = DEST / rel
        if not out.parent.is_dir():
            n_skip_no_dir += 1
            continue
        if out.is_file():
            n_skip_exists += 1
            continue
        shutil.copy2(src, out)
        n_copied += 1

    print(
        f"Done. {SOURCE.resolve()} -> {DEST.resolve()}\n"
        f"  {n_copied} file(s) copied\n"
        f"  {n_skip_exists} skipped (destination file already exists)\n"
        f"  {n_skip_no_dir} skipped (destination folder missing)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
