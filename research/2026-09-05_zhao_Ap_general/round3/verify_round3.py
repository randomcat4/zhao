#!/usr/bin/env python3
"""Run the archived round-3 verifier source, stored in ordered parts."""
from pathlib import Path

base = Path(__file__).resolve().parent
parts = sorted((base / "verify_src").glob("part*.py"))
source = "".join(path.read_text(encoding="utf-8") for path in parts)
original = base / "verify_round3_original.py"
original.write_text(source, encoding="utf-8")
try:
    exec(compile(source, str(original), "exec"), {"__name__": "__main__", "__file__": str(original)})
finally:
    original.unlink(missing_ok=True)
