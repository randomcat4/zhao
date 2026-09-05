"""Bounded 3332 audit: independent roots, provenance, and small-root replay.

Never launches the 20-million-node full replay. Reports its measured estimated
cost so the task owner can make an explicit continuation decision.
"""

from collections import Counter
import hashlib
from itertools import permutations
import json
from pathlib import Path
import time

from verify_finite_cores_fresh import ExactLengths, E, VECTORS, elements, number


BASE = Path(__file__).resolve().parents[1]
CORE = tuple(g for i, g in enumerate(E) for _ in range(3 if i < 3 else 2))
PROBES = (144, 218, 549)


def read(name):
    return json.loads((BASE / "evidence" / name).read_text(encoding="utf-8"))


def jsonl(name):
    return [json.loads(s) for s in (BASE / "evidence" / name).read_text(encoding="utf-8").splitlines() if s]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(g):
    a = VECTORS[g]
    return min(number(tuple(a[i] for i in p) + (a[3],))
               for p in permutations(range(3)))


def replay_root(root, engine):
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
    terminals = []
    longest = []

    def dfs(state, saturated, lower):
        nonlocal longest
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

    dfs(engine.append(state, root), saturated, root)
    return {"root": root, "completed_exhaustively": True,
            "nodes": sum(levels.values()),
            "nodes_by_length": {str(k): v for k, v in sorted(levels.items())},
            "leaves_by_length": {str(k): v for k, v in sorted(leaves.items())},
            "max_reached_length": max(levels), "terminal_count": len(terminals),
            "one_longest_extension": longest, "seconds": time.perf_counter() - start}


def zero_terminals(record):
    return len(record["terminal_extensions"]) if "terminal_extensions" in record else record["terminal_count"]


def compare(a, b):
    for field in ("nodes", "nodes_by_length", "leaves_by_length", "max_reached_length", "completed_exhaustively"):
        assert a[field] == b[field], (a["root"], field)
    assert zero_terminals(a) == zero_terminals(b) == 0


def main():
    log = read("atom_three_double_final.json")
    engine = ExactLengths(13)
    saturated = sum(1 << g for g in E)
    initial = elements(engine.candidates(engine.build(CORE), saturated))
    roots = sorted({canonical(g) for g in initial})
    assert len(initial) == 429 and initial == log["initial_safe_candidates"]
    assert len(roots) == 113 and roots == log["canonical_roots"]
    assert roots == [g for g in initial if tuple(sorted(VECTORS[g][:3], reverse=True)) == VECTORS[g][:3]]
    assert roots == [r["root"] for r in log["runs"]]
    assert all(r["completed_exhaustively"] and zero_terminals(r) == 0 for r in log["runs"])
    assert all(r["nodes"] == sum(r["nodes_by_length"].values()) for r in log["runs"])
    assert all(r["max_reached_length"] == max(map(int, r["nodes_by_length"])) for r in log["runs"])
    assert log["completed_roots"] == 113 and log["all_roots_completed"]
    assert sum(r["nodes"] for r in log["runs"]) == log["complete_record_node_total"] == 20707001
    assert max(r["max_reached_length"] for r in log["runs"]) == 18
    assert (log["case"], log["n"], log["m"], log["core_multiplicities"]) == ("A", 21, 13, [3, 3, 3, 2])

    fast_hash = digest(BASE / "scripts/atom_core_fast.ps1")
    assert log["script_sha256"] == digest(BASE / "scripts/atom_three_with_double.py")
    assert log["helper_sha256"] == digest(BASE / "scripts/atom_five_triples.py")
    sources = [read("atom_three_with_double_A.json")["runs"]]
    for filename in ("atom_three_double_fast_remaining.jsonl", "atom_three_double_fast_last4.jsonl"):
        lines = jsonl(filename)
        meta = lines[0]
        assert meta["type"] == "metadata" and meta["mode"] == "three_double"
        assert meta["script_sha256"] == fast_hash
        assert meta["canonical_roots"] == roots and meta["initial_safe_count"] == len(initial)
        assert (meta["m"], meta["target"], meta["core_length"]) == (13, 21, 11)
        sources.append([r for r in lines if r["type"] == "root"])
    provenance_counts = Counter()
    for final in log["runs"]:
        matching = [(j, r) for j, source in enumerate(sources) for r in source
                    if r["root"] == final["root"] and r["completed_exhaustively"]]
        assert matching, ("no completed original source", final["root"])
        for j, r in matching:
            compare(final, r)
        provenance_counts[str(matching[0][0])] += 1

    # Bind the C# generic DP to the already independently replayed four-core
    # trees, using the same fast script hash as the 3332 production runs.
    fast_four = jsonl("atom_four_fast_crosscheck.jsonl")
    assert fast_four[0]["script_sha256"] == fast_hash
    original_four = read("atom_four_independent_A.json")
    fast_roots = [r for r in fast_four if r["type"] == "root"]
    assert sorted(r["root"] for r in fast_roots) == original_four["canonical_roots"]
    for r in fast_roots:
        other = next(x for x in original_four["runs"] if x["root"] == r["root"])
        compare(r, other)

    probes = []
    for root in PROBES:
        record = replay_root(root, engine)
        compare(record, next(r for r in log["runs"] if r["root"] == root))
        record["complete_log_counts_match"] = True
        probes.append(record)
    rate = sum(r["nodes"] for r in probes) / sum(r["seconds"] for r in probes)
    estimate = log["complete_record_node_total"] / rate
    filenames = ["scripts/atom_three_with_double.py", "scripts/atom_core_fast.ps1",
                 "scripts/verify_finite_cores_fresh.py", "scripts/verify_finite_332_probe.py",
                 "evidence/atom_three_double_final.json", "evidence/atom_three_with_double_A.json",
                 "evidence/atom_three_double_fast_remaining.jsonl",
                 "evidence/atom_three_double_fast_last4.jsonl", "evidence/atom_four_fast_crosscheck.jsonl"]
    output = {"status": "PARTIAL_INDEPENDENT_REPLAY_PASS",
              "scope": "3332 core, exactly three independent tripled elements, capacity two elsewhere",
              "initial_candidates": initial, "canonical_roots": roots,
              "full_log_completed_roots": 113, "full_log_total_nodes": 20707001,
              "full_log_maximum_length": 18, "all_root_source_provenance_checked": True,
              "provenance_counts_python_remaining_last4": dict(provenance_counts),
              "same_hash_csharp_four_core_all_34_roots_match_independent_replay": True,
              "independent_probes": probes, "measured_nodes_per_second": rate,
              "estimated_full_independent_replay_seconds": estimate,
              "full_independent_replay_started": False,
              "limit_decision": "No full replay in this bounded probe; report estimate to task owner",
              "input_sha256": {name: digest(BASE / name) for name in filenames}}
    target = BASE / "evidence/verify_finite_332_probe.json"
    target.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: output[k] for k in ("status", "full_log_completed_roots", "full_log_total_nodes",
                                            "provenance_counts_python_remaining_last4",
                                            "measured_nodes_per_second", "estimated_full_independent_replay_seconds")}))


if __name__ == "__main__":
    main()
