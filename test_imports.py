"""Smoke test for the ASR-evaluation environment.

Verifies that every package the pipeline depends on imports cleanly and reports
its version. Also prints whether a CUDA GPU is visible to torch (the pipeline
runs on CPU otherwise, just slower). This does NOT download or run any model.

Run with:
    .\.venv\Scripts\python.exe test_imports.py
"""

import importlib
import sys

# (import name, friendly label)
CHECKS = [
    ("torch", "torch"),
    ("transformers", "transformers"),
    ("qwen_asr", "qwen-asr"),
    ("whisper", "openai-whisper"),
    ("jiwer", "jiwer"),
    ("soundfile", "soundfile"),
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("tabulate", "tabulate"),
]


def main() -> int:
    print(f"Python: {sys.version.split()[0]} ({sys.executable})\n")

    failures = []
    for module_name, label in CHECKS:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "unknown")
            print(f"  OK   {label:<16} {version}")
        except Exception as exc:  # noqa: BLE001 - we want to report any failure
            failures.append((label, exc))
            print(f"  FAIL {label:<16} {exc}")

    # The two classes the pipeline actually uses up front.
    print()
    try:
        from whisper.normalizers import BasicTextNormalizer

        sample = BasicTextNormalizer()("HELLO [noise] WORLD")
        print(f"  OK   BasicTextNormalizer -> {sample!r}")
    except Exception as exc:  # noqa: BLE001
        failures.append(("BasicTextNormalizer", exc))
        print(f"  FAIL BasicTextNormalizer  {exc}")

    try:
        from qwen_asr import Qwen3ASRModel  # noqa: F401

        print("  OK   qwen_asr.Qwen3ASRModel import")
    except Exception as exc:  # noqa: BLE001
        failures.append(("Qwen3ASRModel", exc))
        print(f"  FAIL Qwen3ASRModel        {exc}")

    # GPU visibility (informational, not a failure either way).
    print()
    try:
        import torch

        if torch.cuda.is_available():
            print(f"  CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("  CUDA not available -> pipeline will run on CPU (slower).")
    except Exception as exc:  # noqa: BLE001
        print(f"  Could not query CUDA: {exc}")

    print()
    if failures:
        print(f"{len(failures)} import(s) FAILED:")
        for label, exc in failures:
            print(f"  - {label}: {exc}")
        return 1

    print("All imports OK. Environment is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
