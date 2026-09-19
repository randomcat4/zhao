#!/usr/bin/env python3
"""Run the archived round-2 verifier source, stored in ordered parts."""
from pathlib import Path

base = Path(__file__).resolve().parent
parts = sorted((base / "verify_src").glob("part*.py"))
source = "".join(path.read_text(encoding="utf-8") for path in parts)
source = source.replace("input_path = ROOT/'inputs'/'round1_research_note.md'", "input_path = ROOT.parent/'round1'/'research_note.md'")
exec(compile(source, str(base / "verify_round2_original.py"), "exec"), {"__name__": "__main__", "__file__": str(base / "verify_round2_original.py")})
