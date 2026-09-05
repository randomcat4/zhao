"""Bind the audited versions, inspect the complete 3332 certificate, and log Lean."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess

BASE = Path(__file__).resolve().parents[1]
EVIDENCE = BASE / "evidence"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def run_command(argv):
    run = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", check=False)
    return {"command": argv, "exit_code": run.returncode,
            "stdout": run.stdout, "stderr": run.stderr}


def main():
    original_path = EVIDENCE / "atom_three_double_final.json"
    checked_path = EVIDENCE / "verify_finite_332_resumed.json"
    original = json.loads(original_path.read_text(encoding="utf-8"))
    checked = json.loads(checked_path.read_text(encoding="utf-8"))
    assert checked["status"] == "FULL_INDEPENDENT_REPLAY_PASS"
    assert checked["all_roots_completed"] and original["all_roots_completed"]
    a = {row["root"]: row for row in original["runs"]}
    b = {row["root"]: row for row in checked["runs"]}
    assert len(a) == len(original["runs"]) == len(b) == len(checked["runs"]) == 113
    assert sorted(a) == sorted(b) == sorted(checked["canonical_roots"]) == sorted(original["canonical_roots"])
    nodes, levels = 0, Counter()
    for root, row in b.items():
        assert row["completed_exhaustively"] and row["all_tree_counts_match"]
        assert a[root]["completed_exhaustively"]
        for key in ("nodes", "nodes_by_length", "leaves_by_length", "max_reached_length"):
            assert row[key] == a[root][key]
        assert row["nodes"] == sum(row["nodes_by_length"].values())
        assert row["max_reached_length"] == max(map(int, row["nodes_by_length"]))
        assert row["terminal_count"] == 0
        nodes += row["nodes"]
        levels.update(row["nodes_by_length"])
    assert nodes == checked["total_nodes"] == original["complete_record_node_total"] == 20707001
    assert max(map(int, levels)) == checked["maximum_reached_length"] == original["max_reached_length"] == 18
    assert checked["input_sha256"]["evidence/atom_three_double_final.json"] == digest(original_path)
    script_sha = digest(BASE / "scripts" / "atom_double_blocks.ps1")
    for mode in ("3322", "2222"):
        path = EVIDENCE / f"atom_{mode}_m13_blocks.jsonl"
        meta = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
        assert meta["script_sha256"] == script_sha

    snapshots = {}
    for source, target in (
        ("proofs/certified_reduction.md", "verify_combined_certified_reduction_snapshot.md"),
        ("proofs/lower_bound_18.md", "verify_combined_lower_bound_18_snapshot.md"),
        ("formal/LowerBound18.lean", "verify_combined_LowerBound18_snapshot.lean"),
        ("proofs/stronger_algebra.md", "verify_combined_stronger_algebra_snapshot.md"),
    ):
        source_path, target_path = BASE/source, EVIDENCE/target
        target_path.write_bytes(source_path.read_bytes())
        assert digest(source_path) == digest(target_path)
        snapshots[source] = {"snapshot": str(target_path.relative_to(BASE)), "sha256": digest(target_path)}

    lean_file = EVIDENCE / "verify_combined_LowerBound18_snapshot.lean"
    lean_text = lean_file.read_text(encoding="utf-8")
    forbidden = re.findall(r"\bsorry\b|\badmit\b|^\s*axiom\b|\bunsafe\b", lean_text, re.M)
    assert not forbidden
    lean = "C:/Users/UIO/.elan/bin/lean.exe"
    lake = "C:/Users/UIO/.elan/bin/lake.exe"
    toolchain = "+leanprover/lean4:v4.30.0"
    commands = [run_command([lean, toolchain, "--version"]),
                run_command([lake, toolchain, "--version"]),
                run_command([lean, toolchain, str(lean_file)])]
    assert all(run["exit_code"] == 0 for run in commands), commands
    assert "'noShortZero18' does not depend on any axioms" in commands[-1]["stdout"]
    log = []
    for run in commands:
        log.extend(["COMMAND: " + json.dumps(run["command"]), f"EXIT_CODE: {run['exit_code']}",
                    "STDOUT:", run["stdout"].rstrip(), "STDERR:", run["stderr"].rstrip(), ""])
    (EVIDENCE/"verify_combined_lean_log.txt").write_text("\n".join(log), encoding="utf-8")
    result = {"status": "PASS", "script_sha256": digest(Path(__file__)), "snapshots": snapshots,
              "3332_scope": "certificate binding and all-root comparison only; no new 20M replay",
              "3332_source_sha256": digest(original_path), "3332_verified_sha256": digest(checked_path),
              "3332_roots": len(b), "3332_nodes": nodes, "3332_levels": dict(levels),
              "double_script_source_hashes_match": True,
              "lean": {"file": str(lean_file), "file_sha256": digest(lean_file),
                       "commands": commands, "forbidden_tokens": forbidden,
                       "axioms": [], "coverage": "finite noShortZero18 only; not endpoints A/B"}}
    (EVIDENCE/"verify_combined_bindings_fresh.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status": "PASS", "3332_roots": len(b), "3332_nodes": nodes,
                      "lean_exit": commands[-1]["exit_code"], "lean_axioms": []}))


if __name__ == "__main__":
    main()
