"""Bounded producer probe: all 8461 normalized 3322, m13, length-14 cores.

Rebuild outside-singleton candidates and pair compatibility graphs. A proper
coloring with at most five colors excludes six (and hence seven) new distinct
singletons. No six-subset enumeration and no certification of a new theorem.
"""

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys
import time

from verify_finite_cores_fresh import ExactLengths, E, VECTORS, Q, elements, number
from verify_finite_double_blocks import append_two, block_candidates, canonical, allowed_permutations


BASE = Path(__file__).resolve().parents[1]
FIXED = (1, 1, 1, 5, 5, 5, 25, 25, 125, 125)
NEG = [number(tuple((-x) % 5 for x in v)) for v in VECTORS]
PAIR_MASK = [sum(1 << (Q * length + NEG[g]) for length in range(12)) for g in range(Q)]
ZERO = sum(1 << (Q * length) for length in range(1, 14))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def greedy_independent_classes(adjacency, order=None):
    """Each produced color class is an independent set."""
    remaining = (1 << len(adjacency)) - 1
    classes = []
    while remaining:
        available = remaining
        color_class = 0
        while available:
            if order is None:
                bit = available & -available
                index = bit.bit_length() - 1
            else:
                index = next(i for i in order if available & (1 << i))
                bit = 1 << index
            color_class |= bit
            remaining ^= bit
            available ^= bit
            available &= ~adjacency[index]
        classes.append(color_class)
    return classes


def dsatur_greedy(adjacency):
    """A bounded greedy heuristic, not an exact coloring or clique solver."""
    n = len(adjacency)
    degree = [row.bit_count() for row in adjacency]
    forbidden = [0] * n
    uncolored = (1 << n) - 1
    classes = []
    while uncolored:
        index = max(elements(uncolored), key=lambda i: (forbidden[i].bit_count(), degree[i], -i))
        color = 0
        while forbidden[index] & (1 << color):
            color += 1
        if color == len(classes):
            classes.append(0)
        classes[color] |= 1 << index
        uncolored ^= 1 << index
        neighbors = adjacency[index] & uncolored
        while neighbors:
            bit = neighbors & -neighbors
            neighbors ^= bit
            forbidden[bit.bit_length() - 1] |= 1 << color
    return classes


def assert_coloring(classes, adjacency):
    union = 0
    for color_class in classes:
        assert color_class and not union & color_class
        union |= color_class
        for i in elements(color_class):
            assert not adjacency[i] & color_class
    assert union == (1 << len(adjacency)) - 1
    for i, row in enumerate(adjacency):
        assert not row & (1 << i)
        for j in elements(row):
            assert adjacency[j] & (1 << i)


def read_reference():
    source = BASE / "evidence/atom_3322_m13_blocks.jsonl"
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line]
    metadata, summary = rows[0], rows[-1]
    assert (metadata["mode"], metadata["m"], metadata["target"]) == ("3322", 13, 20)
    assert metadata["script_sha256"] == sha(BASE / "scripts/atom_double_blocks.ps1")
    roots = {row["root"]: row for row in rows if row["type"] == "root"}
    assert len(roots) == 122 and sorted(roots) == metadata["canonical_roots"]
    assert all(row["completed_exhaustively"] for row in roots.values())
    assert summary["all_roots_completed"] and summary["nodes_this_run"] == 24267
    expected = {root: row["nodes_by_length"].get("14", 0) for root, row in roots.items()}
    assert sum(expected.values()) == 8461
    return source, metadata, expected


def graph(state, candidates, plus, deadline):
    n = len(candidates)
    adjacency = [0] * n
    pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            if pairs % 2048 == 0 and time.perf_counter() >= deadline:
                return None, pairs
            pairs += 1
            if not state & PAIR_MASK[plus[candidates[i]][candidates[j]]]:
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
    assert pairs == math.comb(n, 2)
    return adjacency, pairs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--prefix", default="finite_two_triples_probe")
    args = parser.parse_args()
    assert args.seconds > 0
    assert args.prefix.startswith("finite_two_triples_") and Path(args.prefix).name == args.prefix
    started = time.perf_counter()
    deadline = started + args.seconds
    source, metadata, expected_by_root = read_reference()
    engine = ExactLengths(13)
    base_state = engine.build(FIXED)
    assert not base_state & ZERO
    used_base = sum(1 << g for g in E)
    initial = elements(block_candidates(base_state, used_base, 1))
    assert initial == metadata["initial_safe_candidates"] and len(initial) == 371
    roots = sorted({canonical(g, allowed_permutations("3322")) for g in initial})
    assert roots == metadata["canonical_roots"] and len(roots) == 122

    # Rebuild every length-14 prefix, including nonterminal length-14 nodes.
    records = []
    seen = set()
    generated_by_root = Counter()
    candidate_hist = Counter()
    for root in roots:
        if time.perf_counter() >= deadline:
            raise TimeoutError("length-14 generation incomplete; no complete claim")
        state12 = append_two(engine, base_state, root)
        used12 = used_base | (1 << root)
        for second in elements(block_candidates(state12, used12, root + 1)):
            blocks = (root, second)
            assert blocks not in seen
            seen.add(blocks)
            state14 = append_two(engine, state12, second)
            assert not state14 & ZERO
            outside = elements(engine.candidates(state14, used12 | (1 << second), 1))
            assert not set(outside) & (set(E) | set(blocks))
            generated_by_root[root] += 1
            candidate_hist[len(outside)] += 1
            records.append((blocks, state14, outside))
        assert generated_by_root[root] == expected_by_root[root]
    assert len(records) == len(seen) == 8461
    assert all(generated_by_root[root] == count for root, count in expected_by_root.items())

    plus = [[number(tuple((a[k] + b[k]) % 5 for k in range(4))) for b in VECTORS] for a in VECTORS]
    inputs = {name: sha(BASE / name) for name in (
        "scripts/finite_two_triples_probe.py", "scripts/verify_finite_cores_fresh.py",
        "scripts/verify_finite_double_blocks.py", "scripts/atom_double_blocks.ps1",
        "evidence/atom_3322_m13_blocks.jsonl")}
    result = {
        "status": "RUNNING", "role": "bounded execution producer; independent certification required",
        "scope": "8461 normalized 3322 m13 length14 cores, outside mutually distinct singleton additions",
        "avoidance_cutoff": 13, "core_length": 14,
        "requested_extension_sizes": {"B_relaxed_m13": 6, "A_m13": 7},
        "seconds_limit": args.seconds, "input_sha256": inputs,
        "canonical_root_count": len(roots), "canonical_roots": roots,
        "generated_cores": len(records), "generated_cores_by_root": dict(sorted(generated_by_root.items())),
        "root_length14_count_matches_original": True,
        "outside_candidate_count_distribution": dict(sorted(candidate_hist.items())),
        "six_subset_denominator": sum(math.comb(len(c), 6) for _, _, c in records),
        "seven_subset_denominator": sum(math.comb(len(c), 7) for _, _, c in records),
        "large_candidate_threshold": 20, "large_candidate_cores": [],
        "graph_completed_cores": 0, "at_most_five_colors_cores": 0,
        "unresolved_by_coloring_cores": 0, "unprocessed_cores": len(records),
        "total_pair_checks": 0, "best_color_count_distribution": {},
        "first_unresolved_core": None, "unresolved_core_keys": [],
        "graph_completed_by_root": {}, "complete_certificate": False,
        "time_limit_reached": False, "python": sys.version}
    for blocks, _, candidates in records:
        if len(candidates) > 20:
            result["large_candidate_cores"].append({
                "blocks": list(blocks), "candidate_count": len(candidates),
                "six_subset_count": math.comb(len(candidates), 6),
                "seven_subset_count": math.comb(len(candidates), 7)})
    result["large_candidate_core_count"] = len(result["large_candidate_cores"])
    result["large_candidate_six_subset_denominator"] = sum(row["six_subset_count"] for row in result["large_candidate_cores"])
    result["large_candidate_seven_subset_denominator"] = sum(row["seven_subset_count"] for row in result["large_candidate_cores"])
    summary_path = BASE / "evidence" / (args.prefix + ".json")
    certificate_path = BASE / "evidence" / (args.prefix + "_cores.jsonl")
    colors_hist, completed_by_root = Counter(), Counter()

    def save():
        result["seconds"] = time.perf_counter() - started
        result["best_color_count_distribution"] = dict(sorted(colors_hist.items()))
        result["graph_completed_by_root"] = dict(sorted(completed_by_root.items()))
        result["unprocessed_cores"] = len(records) - result["graph_completed_cores"]
        summary_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    save()
    print(json.dumps({"generated_cores": len(records), "candidate_distribution": dict(sorted(candidate_hist.items())),
                      "large_candidate_cores": result["large_candidate_core_count"],
                      "setup_seconds": time.perf_counter() - started}), flush=True)
    with certificate_path.open("w", encoding="utf-8") as out:
        out.write(json.dumps({"type": "metadata", "input_sha256": inputs, "core_length": 14,
                              "fixed_sequence": list(FIXED), "cutoff": 13,
                              "pair_core_length_limit": 11, "canonical_roots": roots,
                              "expected_cores": 8461, "certificate": "explicit proper color classes of pair graph"}) + "\n")
        for index, (blocks, state, candidates) in enumerate(records):
            if time.perf_counter() >= deadline:
                result["time_limit_reached"] = True
                break
            adjacency, pairs = graph(state, candidates, plus, deadline)
            result["total_pair_checks"] += pairs
            if adjacency is None:
                result["time_limit_reached"] = True
                break
            classes = greedy_independent_classes(adjacency)
            method = "ascending_index_independent_classes"
            attempted = {method: len(classes)}
            if len(classes) > 5:
                order = sorted(range(len(adjacency)), key=lambda i: (-adjacency[i].bit_count(), i))
                alternative = greedy_independent_classes(adjacency, order)
                attempted["descending_degree_independent_classes"] = len(alternative)
                if len(alternative) < len(classes):
                    classes, method = alternative, "descending_degree_independent_classes"
            if len(classes) > 5:
                alternative = dsatur_greedy(adjacency)
                attempted["dsatur_greedy"] = len(alternative)
                if len(alternative) < len(classes):
                    classes, method = alternative, "dsatur_greedy"
            assert_coloring(classes, adjacency)
            ruled_out = len(classes) <= 5
            row = {"type": "core_result", "core_index": index, "root": blocks[0],
                   "blocks": list(blocks), "outside_safe_values": candidates,
                   "candidate_count": len(candidates), "pair_checks": pairs,
                   "six_subset_count": math.comb(len(candidates), 6),
                   "seven_subset_count": math.comb(len(candidates), 7),
                   "adjacency_bitmasks": adjacency, "proper_color_classes": classes,
                   "coloring_method": method, "attempted_color_counts": attempted,
                   "number_of_colors": len(classes),
                   "no_six_new_singletons_certified_by_this_coloring": ruled_out,
                   "graph_completed": True,
                   "status": "PRODUCER_COLOR_CERTIFICATE_REQUIRES_INDEPENDENT_CHECK" if ruled_out else "UNRESOLVED_BY_TESTED_COLORINGS"}
            out.write(json.dumps(row, separators=(",", ":")) + "\n")
            result["graph_completed_cores"] += 1
            completed_by_root[blocks[0]] += 1
            colors_hist[len(classes)] += 1
            if ruled_out:
                result["at_most_five_colors_cores"] += 1
            else:
                result["unresolved_by_coloring_cores"] += 1
                result["unresolved_core_keys"].append(list(blocks))
                if result["first_unresolved_core"] is None:
                    result["first_unresolved_core"] = {
                        "blocks": list(blocks), "root": blocks[0],
                        "sequence_encoded": list(FIXED) + [g for g in blocks for _ in range(2)],
                        "candidate_count": len(candidates), "outside_safe_values": candidates,
                        "attempted_color_counts": attempted, "number_of_colors": len(classes),
                        "six_subset_count": math.comb(len(candidates), 6),
                        "seven_subset_count": math.comb(len(candidates), 7)}
            if result["graph_completed_cores"] % 1000 == 0:
                out.flush()
                save()
                print(json.dumps({"graph_completed": result["graph_completed_cores"],
                                  "unresolved": result["unresolved_by_coloring_cores"],
                                  "pair_checks": result["total_pair_checks"], "seconds": result["seconds"]}), flush=True)
        if result["graph_completed_cores"] == len(records):
            assert dict(completed_by_root) == dict(generated_by_root)
            assert not result["time_limit_reached"]
            result["complete_certificate"] = result["unresolved_by_coloring_cores"] == 0
            result["status"] = ("COMPLETE_ALL_GRAPHS_AT_MOST_FIVE_COLORS_REQUIRES_INDEPENDENT_VERIFICATION"
                                if result["complete_certificate"] else "COMPLETE_PROBE_WITH_EXACT_COLORING_RESIDUAL")
        else:
            result["status"] = "INCOMPLETE_TIME_LIMIT"
        result["unprocessed_core_keys"] = [list(blocks) for blocks, _, _ in records[result["graph_completed_cores"]:]]
        out.write(json.dumps({"type": "summary", "status": result["status"],
                              "generated_cores": len(records), "graph_completed_cores": result["graph_completed_cores"],
                              "at_most_five_colors_cores": result["at_most_five_colors_cores"],
                              "unresolved_by_coloring_cores": result["unresolved_by_coloring_cores"]}) + "\n")
    result["certificate_sha256"] = sha(certificate_path)
    save()
    print(json.dumps({k: result[k] for k in (
        "status", "graph_completed_cores", "at_most_five_colors_cores",
        "unresolved_by_coloring_cores", "total_pair_checks", "seconds")}), flush=True)


if __name__ == "__main__":
    main()
