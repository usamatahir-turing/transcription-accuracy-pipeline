"""Mirror ``Conversations/`` into ``Conversations_output_files/`` without raw inputs.

Skips:
  - ``*.wav``
  - ``*.seglst.json`` (human annotation)
  - speaker ``*.rttm`` (e.g. ``SPK01.rttm``, ``a@b.com.rttm``)

Keeps pipeline outputs (json/jsonl, ``*_der.rttm``, ``*_sad.rttm``, etc.).
Empty conversation folders are preserved. Existing destination files are overwritten.

Run once from the repo root:
    python helper_scripts/copy_pipeline_outputs.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

SOURCE = Path("Conversations")
DEST = Path("Conversations_output_files")


def should_skip_file(path: Path) -> bool:
    name = path.name.lower()
    if path.suffix.lower() == ".wav":
        return True
    if name.endswith(".seglst.json"):
        return True
    if path.suffix.lower() == ".rttm":
        if name.endswith("_der.rttm") or name.endswith("_sad.rttm"):
            return False
        return True
    return False


def main() -> int:
    if not SOURCE.is_dir():
        print(f"ERROR: source folder not found: {SOURCE.resolve()}")
        return 1

    n_dirs = n_copied = n_skipped = 0

    for dirpath in sorted(SOURCE.rglob("*")):
        if not dirpath.is_dir():
            continue
        rel = dirpath.relative_to(SOURCE)
        (DEST / rel).mkdir(parents=True, exist_ok=True)
        n_dirs += 1

    for src in sorted(SOURCE.rglob("*")):
        if not src.is_file():
            continue
        if should_skip_file(src):
            n_skipped += 1
            continue
        rel = src.relative_to(SOURCE)
        out = DEST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
        n_copied += 1

    print(
        f"Done. {SOURCE.resolve()} -> {DEST.resolve()}\n"
        f"  {n_dirs} director(y/ies) ensured\n"
        f"  {n_copied} file(s) copied\n"
        f"  {n_skipped} file(s) skipped (wav / seglst / speaker rttm)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
