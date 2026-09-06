#!/usr/bin/env python3
"""Run the archived round-1 verifier source, stored in ordered parts."""
from pathlib import Path

base = Path(__file__).resolve().parent
parts = sorted((base / "verify_src").glob("part*.py"))
source = "".join(path.read_text(encoding="utf-8") for path in parts)
exec(compile(source, str(base / "verify_original.py"), "exec"), {"__name__": "__main__", "__file__": str(base / "verify_original.py")})
