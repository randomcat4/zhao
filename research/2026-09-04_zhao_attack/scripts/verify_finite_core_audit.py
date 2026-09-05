"""Audit input provenance, original DP, positional witnesses, and limit flags.

The separate verify_finite_cores_fresh.py provides the independent exhaustive
replay. This file intentionally imports the originals only to audit them.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import atom_five_triples as five
import atom_four_independent as four


BASE = Path(__file__).resolve().parents[1]


def read_evidence(name):
    return json.loads((BASE / "evidence" / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coords(k):
    return (k % 5, (k // 5) % 5, (k // 25) % 5, k // 125)


def enc(v):
    return v[0] + 5 * v[1] + 25 * v[2] + 125 * v[3]


def positional_gray_audit(sequence, plus):
    """Visit every nonempty position subset; no subsequence DP is used here."""
    vectors = [coords(g) for g in sequence]
    current = [0, 0, 0, 0]
    length, previous_gray = 0, 0
    counts = Counter()
    minimum_lengths = [99] * 625
    minimum_lengths[0] = 0
    for step in range(1, 1 << len(sequence)):
        gray = step ^ (step >> 1)
        changed = gray ^ previous_gray
        position = changed.bit_length() - 1
        sign = 1 if gray & changed else -1
        length += sign
        v = vectors[position]
        for i in range(4):
            current[i] = (current[i] + sign * v[i]) % 5
        total = enc(current)
        if length < minimum_lengths[total]:
            minimum_lengths[total] = length
        if total == 0:
            counts[length] += 1
        previous_gray = gray
    dp = [five.INF] * 625
    dp[0] = 0
    for g in sequence:
        dp = five.extend_distances(dp, g, plus)
    assert dp == minimum_lengths
    return {"positions": len(sequence), "subsets_checked": (1 << len(sequence)) - 1,
            "minimum_nonempty_zero_sum": min(counts) if counts else None,
            "zero_sum_counts_by_length": {str(k): v for k, v in sorted(counts.items())},
            "all_625_minimum_lengths_match_original_dp": True}


def same_tree_record(a, b):
    for key in ("nodes_by_length", "leaves_by_length", "nodes", "max_reached_length",
                "terminal_extensions", "completed_exhaustively"):
        assert a[key] == b[key], key


def audit_record(r, prefix, extension_key):
    assert r["completed_exhaustively"] is True
    assert r["nodes"] == sum(r["nodes_by_length"].values())
    assert r["max_reached_length"] == max(map(int, r["nodes_by_length"]))
    assert r["max_reached_length"] == prefix + len(r[extension_key])
    assert not r["terminal_extensions"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    old5 = read_evidence("atom_five_triples.json")
    old4 = read_evidence("atom_four_independent_A.json")
    replay5 = read_evidence("verify_finite_original_five_rerun.json")
    replay4 = read_evidence("verify_finite_original_four_rerun.json")
    independent = read_evidence("verify_finite_cores_independent.json")
    paths = [BASE / "frozen_theorem_v1.md", BASE / "proofs/atom_structure.md",
             BASE / "scripts/atom_five_triples.py", BASE / "scripts/atom_four_independent.py",
             BASE / "scripts/verify_finite_cores_fresh.py",
             BASE / "scripts/verify_finite_core_audit.py",
             BASE / "evidence/atom_five_triples.json",
             BASE / "evidence/atom_four_independent_A.json",
             BASE / "evidence/atom_four_longest18_graycheck.json",
             BASE / "evidence/verify_finite_original_five_rerun.json",
             BASE / "evidence/verify_finite_original_four_rerun.json",
             BASE / "evidence/verify_finite_cores_independent.json"]
    hashes = {str(p.relative_to(BASE)).replace("\\", "/"): sha(p) for p in paths}
    assert old5["script_sha256"] == replay5["script_sha256"] == hashes["scripts/atom_five_triples.py"]
    assert old4["script_sha256"] == replay4["script_sha256"] == hashes["scripts/atom_four_independent.py"]
    assert independent["script_sha256"] == hashes["scripts/verify_finite_cores_fresh.py"]
    assert independent["status"] == "PASS" and independent["all_completed"]

    expected5 = {(n, m, x) for n, m in ((21, 13), (20, 14)) for x in five.CORE_TYPES}
    for log in (old5, replay5):
        keys = [(r["n"], r["m"], tuple(r["core_type"])) for r in log["runs"]]
        assert len(keys) == len(set(keys)) == 10 and set(keys) == expected5
        assert log["all_runs_completed"] and log["counterexample_count"] == 0
        for r in log["runs"]:
            audit_record(r, 15, "one_longest_extension_encoded")
            assert r["nodes"] <= 1000000
    for r, replay in zip(old5["runs"], replay5["runs"]):
        assert (r["core_type"], r["n"], r["m"]) == (replay["core_type"], replay["n"], replay["m"])
        assert r["initial_safe_candidates"] == replay["initial_safe_candidates"]
        assert r["core_sequence_encoded"] == replay["core_sequence_encoded"]
        same_tree_record(r, replay)

    for log in (old4, replay4):
        assert (log["case"], log["n"], log["m"]) == ("A", 21, 13)
        assert log["all_roots_selected"] and log["all_selected_roots_completed"]
        roots = log["canonical_roots"]
        assert len(roots) == len(set(roots)) == 34
        assert roots == log["selected_roots"] == [r["root"] for r in log["runs"]]
        assert roots == independent["four_roots"]
        assert log["initial_safe_candidates"] == independent["four_initial_safe_candidates"]
        for r in log["runs"]:
            audit_record(r, 12, "one_longest_extension")
            assert r["nodes"] <= 100000
    for a, b in zip(old4["runs"], replay4["runs"]):
        same_tree_record(a, b)

    plus, neg = five.make_tables()
    for g in range(625):
        a = coords(g)
        assert five.decode(g) == a and five.encode(a) == g
        assert neg[g] == enc(tuple((-x) % 5 for x in a))
        for h in range(625):
            b = coords(h)
            assert plus[g][h] == enc(tuple((a[i] + b[i]) % 5 for i in range(4)))

    witnesses = []
    edge_cases = ((), (0,), (1, 1, 1, 1, 1), (1, 4), (1, 2, 2))
    for i, seq in enumerate(edge_cases):
        record = positional_gray_audit(seq, plus)
        record["source"] = "edge_case_" + str(i)
        witnesses.append(record)
    for r in old5["runs"]:
        seq = r["core_sequence_encoded"] + r["one_longest_extension_encoded"]
        assert max(Counter(seq).values()) <= 3
        record = positional_gray_audit(seq, plus)
        assert record["minimum_nonempty_zero_sum"] is None or record["minimum_nonempty_zero_sum"] > r["m"]
        record["source"] = "five_n=" + str(r["n"]) + "_core=" + str(r["core_type"])
        witnesses.append(record)
    for r in old4["runs"]:
        core = [g for g in (1, 5, 25, 125) for _ in range(3)]
        extension = r["one_longest_extension"]
        assert max(Counter(extension).values()) <= 2
        assert not set(extension).intersection(core)
        record = positional_gray_audit(core + extension, plus)
        assert record["minimum_nonempty_zero_sum"] is None or record["minimum_nonempty_zero_sum"] > 13
        record["source"] = "four_root=" + str(r["root"])
        witnesses.append(record)
    gray_evidence = read_evidence("atom_four_longest18_graycheck.json")
    record = positional_gray_audit([enc(v) for v in gray_evidence["sequence_coordinates"]], plus)
    assert record["zero_sum_counts_by_length"] == gray_evidence["zero_sum_counts_by_length"]
    assert record["minimum_nonempty_zero_sum"] == gray_evidence["minimum_zero_sum_length"]
    assert record["subsets_checked"] == gray_evidence["subsets_checked"]
    record["source"] = "atom_four_longest18_graycheck"
    witnesses.append(record)

    # Force local node/time limits and global pre-root deadline expiry.
    limited5 = five.search(five.CORE_TYPES[0], 21, 13, plus, neg, node_limit=1)
    assert not limited5["completed_exhaustively"]
    dist = [five.INF] * 625
    dist[0] = 0
    for g in (1, 5, 25, 125):
        for _ in range(3):
            dist = five.extend_distances(dist, g, plus)
    root = old4["canonical_roots"][0]
    initial = old4["initial_safe_candidates"]
    limited4 = four.run_root(root, dist, 21, 13, initial, plus, neg, 0, float("inf"))
    expired4 = four.run_root(root, dist, 21, 13, initial, plus, neg, 100000, time.monotonic() - 1)
    assert not limited4["completed_exhaustively"] and not expired4["completed_exhaustively"]
    stop_files = []
    for label, options in (("global_expired", ["--seconds", "0"]),
                           ("single_root", ["--seconds", "180", "--root-index", "33"])):
        path = BASE / "evidence" / ("verify_finite_" + label + ".json")
        command = [sys.executable, "-B", str(BASE / "scripts/atom_four_independent.py"),
                   "--case", "A", "--output", str(path)] + options
        run = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=True)
        log = json.loads(path.read_text(encoding="utf-8"))
        if label == "global_expired":
            assert not log["all_selected_roots_completed"] and not log["runs"]
        else:
            assert log["all_selected_roots_completed"] and not log["all_roots_selected"]
            assert len(log["runs"]) == 1
        stop_files.append({"kind": label, "file": str(path), "sha256": sha(path),
                           "all_selected_roots_completed": log["all_selected_roots_completed"],
                           "all_roots_selected": log["all_roots_selected"],
                           "roots_run": len(log["runs"])})

    level_totals = Counter()
    for r in old4["runs"]:
        level_totals.update(r["nodes_by_length"])
    output = {"status": "PASS", "scope": "two finite exclusions, with h(S)<=3 explicit",
              "input_sha256": hashes, "original_tables_all_390625_pairs_match": True,
              "original_and_replay_logs_have_all_required_roots": True,
              "original_replay_tree_counts_match": True,
              "four_aggregate_levels": dict(sorted(level_totals.items())),
              "four_max_root_nodes": max(r["nodes"] for r in old4["runs"]),
              "four_original_recorded_root_seconds_sum": sum(r["seconds"] for r in old4["runs"]),
              "four_rerun_recorded_root_seconds_sum": sum(r["seconds"] for r in replay4["runs"]),
              "positional_gray_checks": witnesses,
              "total_nonempty_position_subsets_checked": sum(r["subsets_checked"] for r in witnesses),
              "five_forced_node_limit_completed": limited5["completed_exhaustively"],
              "four_forced_node_limit_completed": limited4["completed_exhaustively"],
              "four_forced_deadline_completed": expired4["completed_exhaustively"],
              "cli_limit_and_selection_checks": stop_files,
              "seconds": round(time.monotonic() - started, 6)}
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: output[k] for k in ("status", "four_aggregate_levels", "four_max_root_nodes",
                                            "total_nonempty_position_subsets_checked", "seconds")}), flush=True)


if __name__ == "__main__":
    main()
