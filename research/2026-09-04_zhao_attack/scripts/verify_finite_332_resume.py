"""Authorized staged continuation: only unverified 3332 roots, <=180 seconds.

Completed roots from the first full attempt and the independent probes are
hash-bound and rechecked against the frozen reference. No completed tree is
searched again. The incomplete first-stage root is restarted and stays in the
unmodified previous evidence file.
"""

from collections import Counter
import hashlib
import json
from pathlib import Path
import time

from verify_finite_cores_fresh import ExactLengths
from verify_finite_332_probe import compare
from verify_finite_332_full import search


BASE = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((BASE / "evidence" / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    start = time.perf_counter()
    deadline = start + 180.0
    prior = load("verify_finite_332_full.json")
    probes = load("verify_finite_332_probe.json")
    reference = load("atom_three_double_final.json")
    assert prior["status"] == "INCOMPLETE_DEADLINE"
    assert probes["status"] == "PARTIAL_INDEPENDENT_REPLAY_PASS"
    for evidence in (prior, probes):
        for relative, recorded_hash in evidence["input_sha256"].items():
            assert sha(BASE / relative) == recorded_hash, relative
    roots = prior["canonical_roots"]
    assert roots == reference["canonical_roots"] == probes["canonical_roots"]
    assert prior["initial_safe_candidates"] == reference["initial_safe_candidates"] == probes["initial_candidates"]
    expected = {r["root"]: r for r in reference["runs"]}
    verified = {}
    for r in prior["runs"]:
        if r["completed_exhaustively"]:
            assert r["all_tree_counts_match"]
            compare(r, expected[r["root"]])
            verified[r["root"]] = dict(r, source_stage="first_240_seconds")
    for r in probes["independent_probes"]:
        assert r["completed_exhaustively"] and r["complete_log_counts_match"]
        compare(r, expected[r["root"]])
        if r["root"] in verified:
            compare(r, verified[r["root"]])
        else:
            verified[r["root"]] = dict(r, all_tree_counts_match=True, source_stage="earlier_probe")
    completed_prior = [r for r in prior["runs"] if r["completed_exhaustively"]]
    recent = completed_prior[-4:]
    recent_rate = sum(r["nodes"] for r in recent) / sum(r["seconds"] for r in recent)
    remaining_roots = [r for r in roots if r not in verified]
    remaining_nodes = sum(expected[r]["nodes"] for r in remaining_roots)
    estimate = remaining_nodes / recent_rate
    assert estimate <= 180.0, estimate
    assert len(verified) == 18 and sum(r["nodes"] for r in verified.values()) == 16156191
    assert len(remaining_roots) == 95 and remaining_nodes == 4550810
    result = {"status": "RUNNING", "all_roots_completed": False,
              "scope": "3332 core; exact-length independent replay; staged completion",
              "n": 21, "m": 13, "core_multiplicities": [3, 3, 3, 2],
              "outside_core_capacity": 2, "seconds_limit_this_stage": 180,
              "canonical_roots": roots, "initial_safe_candidates": prior["initial_safe_candidates"],
              "carried_completed_roots": sorted(verified),
              "carried_completed_nodes": sum(r["nodes"] for r in verified.values()),
              "remaining_roots_at_start": remaining_roots,
              "remaining_nodes_at_start": remaining_nodes,
              "recent_measured_nodes_per_second": recent_rate,
              "estimated_seconds_at_start": estimate,
              "resumed_roots": [], "runs": [],
              "input_sha256": {name: sha(BASE / name) for name in (
                  "scripts/verify_finite_332_resume.py", "scripts/verify_finite_332_full.py",
                  "scripts/verify_finite_332_probe.py", "scripts/verify_finite_cores_fresh.py",
                  "evidence/verify_finite_332_full.json", "evidence/verify_finite_332_probe.json",
                  "evidence/atom_three_double_final.json")}}
    target = BASE / "evidence/verify_finite_332_resumed.json"

    def save():
        result["runs"] = [verified[r] for r in roots if r in verified]
        result["completed_roots"] = sum(r["completed_exhaustively"] for r in result["runs"])
        result["seconds_this_stage"] = time.perf_counter() - start
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    save()
    print(json.dumps({"carried_roots": 18, "carried_nodes": result["carried_completed_nodes"],
                      "remaining_roots": 95, "remaining_nodes": remaining_nodes,
                      "estimated_seconds": estimate}), flush=True)
    engine = ExactLengths(13)
    for root in remaining_roots:
        if time.perf_counter() >= deadline:
            result["status"] = "INCOMPLETE_DEADLINE"
            break
        record = search(root, engine, deadline)
        record["source_stage"] = "resumed_180_seconds"
        verified[root] = record
        result["resumed_roots"].append(root)
        if not record["completed_exhaustively"]:
            result["status"] = "INCOMPLETE_DEADLINE"
            save()
            break
        try:
            compare(record, expected[root])
        except AssertionError as error:
            result["status"] = "FAIL_COUNT_MISMATCH"
            result["error"] = str(error)
            save()
            raise
        record["all_tree_counts_match"] = True
        save()
        print(json.dumps({"root": root, "nodes": record["nodes"],
                          "completed_roots": result["completed_roots"],
                          "seconds_this_stage": result["seconds_this_stage"]}), flush=True)
    if len(verified) == len(roots) and all(r["completed_exhaustively"] and r.get("all_tree_counts_match") for r in verified.values()):
        result["status"] = "FULL_INDEPENDENT_REPLAY_PASS"
        result["all_roots_completed"] = True
        result["total_nodes"] = sum(r["nodes"] for r in verified.values())
        result["maximum_reached_length"] = max(r["max_reached_length"] for r in verified.values())
        levels, leaves = Counter(), Counter()
        for r in verified.values():
            levels.update(r["nodes_by_length"])
            leaves.update(r["leaves_by_length"])
        result["aggregate_nodes_by_length"] = dict(sorted(levels.items()))
        result["aggregate_leaves_by_length"] = dict(sorted(leaves.items()))
        assert result["total_nodes"] == 20707001 and result["maximum_reached_length"] == 18
    save()
    print(json.dumps({key: result.get(key) for key in ("status", "completed_roots", "total_nodes", "maximum_reached_length", "seconds_this_stage")}), flush=True)


if __name__ == "__main__":
    main()
