"""Authorized <=240-second independent full 3332 replay with checkpoints.

Uses exact-length packed bitsets and regenerates every node's candidate set
from the full group. Imports only the fresh independent verifier helpers.
"""

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time

from verify_finite_cores_fresh import ExactLengths, E, elements
from verify_finite_332_probe import CORE, canonical, compare


BASE = Path(__file__).resolve().parents[1]


def search(root, engine, deadline):
    start = time.perf_counter()
    capacities = [2] * 625
    for g in E[:3]:
        capacities[g] = 3
    counts = Counter(CORE)
    saturated = sum(1 << g for g in E)
    state = engine.build(CORE)
    assert engine.candidates(state, saturated) & (1 << root)
    counts[root] = 1
    path = [root]
    levels, leaves = Counter(), Counter()
    terminals, longest = [], []
    complete = True
    nodes = 0

    def dfs(state, saturated, lower):
        nonlocal longest, complete, nodes
        nodes += 1
        if nodes % 1024 == 0 and time.perf_counter() >= deadline:
            complete = False
            return
        length = 11 + len(path)
        levels[length] += 1
        assert not state & engine.nonempty_zero
        if len(path) > len(longest):
            longest = path[:]
        if length == 21:
            terminals.append(path[:])
            return
        possible = engine.candidates(state, saturated, lower)
        if not possible:
            leaves[length] += 1
        while possible:
            bit = possible & -possible
            possible ^= bit
            g = bit.bit_length() - 1
            counts[g] += 1
            assert counts[g] <= capacities[g]
            filled = saturated | bit if counts[g] == capacities[g] else saturated
            path.append(g)
            dfs(engine.append(state, g), filled, g)
            path.pop()
            counts[g] -= 1
            if not complete:
                return

    dfs(engine.append(state, root), saturated, root)
    return {"root": root, "completed_exhaustively": complete,
            "nodes": nodes,
            "nodes_by_length": {str(k): v for k, v in sorted(levels.items())},
            "leaves_by_length": {str(k): v for k, v in sorted(leaves.items())},
            "max_reached_length": max(levels), "terminal_count": len(terminals),
            "terminal_extensions": terminals, "one_longest_extension": longest,
            "seconds": time.perf_counter() - start}


def main():
    start = time.perf_counter()
    deadline = start + 240.0
    input_path = BASE / "evidence/atom_three_double_final.json"
    reference = json.loads(input_path.read_text(encoding="utf-8"))
    engine = ExactLengths(13)
    initial = elements(engine.candidates(engine.build(CORE), sum(1 << g for g in E)))
    roots = sorted({canonical(g) for g in initial})
    assert initial == reference["initial_safe_candidates"] and len(initial) == 429
    assert roots == reference["canonical_roots"] and len(roots) == 113
    assert (reference["case"], reference["n"], reference["m"], reference["core_multiplicities"]) == ("A", 21, 13, [3, 3, 3, 2])
    by_root = {r["root"]: r for r in reference["runs"]}
    result = {"status": "RUNNING", "all_roots_completed": False,
              "algorithm": "independent exact-length bitsets; fresh all-group candidates",
              "n": 21, "m": 13, "core_multiplicities": [3, 3, 3, 2],
              "outside_core_capacity": 2, "seconds_limit": 240,
              "python": sys.version, "canonical_roots": roots,
              "initial_safe_candidates": initial, "runs": [],
              "input_sha256": {str(p.relative_to(BASE)).replace("\\", "/"):
                               hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (Path(__file__), input_path,
                                         BASE / "scripts/verify_finite_cores_fresh.py",
                                         BASE / "scripts/verify_finite_332_probe.py")}}
    output = BASE / "evidence/verify_finite_332_full.json"

    def save():
        result["seconds"] = time.perf_counter() - start
        result["completed_roots"] = sum(r["completed_exhaustively"] for r in result["runs"])
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    save()
    for root in roots:
        if time.perf_counter() >= deadline:
            result["status"] = "INCOMPLETE_DEADLINE"
            break
        record = search(root, engine, deadline)
        result["runs"].append(record)
        if not record["completed_exhaustively"]:
            result["status"] = "INCOMPLETE_DEADLINE"
            save()
            break
        try:
            compare(record, by_root[root])
        except AssertionError as error:
            result["status"] = "FAIL_COUNT_MISMATCH"
            result["error"] = str(error)
            save()
            raise
        record["all_tree_counts_match"] = True
        save()
        print(json.dumps({"root": root, "nodes": record["nodes"],
                          "completed_roots": result["completed_roots"],
                          "seconds": result["seconds"]}), flush=True)
    if len(result["runs"]) == len(roots) and all(r["completed_exhaustively"] and r.get("all_tree_counts_match") for r in result["runs"]):
        result["all_roots_completed"] = True
        result["status"] = "FULL_INDEPENDENT_REPLAY_PASS"
        result["total_nodes"] = sum(r["nodes"] for r in result["runs"])
        result["maximum_reached_length"] = max(r["max_reached_length"] for r in result["runs"])
        levels, leaves = Counter(), Counter()
        for r in result["runs"]:
            levels.update(r["nodes_by_length"])
            leaves.update(r["leaves_by_length"])
        result["aggregate_nodes_by_length"] = dict(sorted(levels.items()))
        result["aggregate_leaves_by_length"] = dict(sorted(leaves.items()))
        assert result["total_nodes"] == 20707001 and result["maximum_reached_length"] == 18
    save()
    print(json.dumps({key: result.get(key) for key in ("status", "completed_roots", "total_nodes", "maximum_reached_length", "seconds")}), flush=True)


if __name__ == "__main__":
    main()
