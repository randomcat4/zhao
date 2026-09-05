"""Bounded producer continuation on exactly the 1022 coloring residual cores.

Classify all 156 linear hyperplanes. H12 cases stay conditional on a separate
pending lemma. For other cases, search six new distinct values with incremental
exact-length subset sums, pair graph intersections, and proper-coloring bounds.
Never equate a graph clique with an actual m13-safe extension.
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
from finite_two_triples_probe import FIXED, assert_coloring, sha


BASE = Path(__file__).resolve().parents[1]
NEG = [number(tuple((-x) % 5 for x in v)) for v in VECTORS]
ONE_MASK = [sum(1 << (Q * length + NEG[g]) for length in range(13)) for g in range(Q)]
ZERO = sum(1 << (Q * length) for length in range(1, 14))


def hyperplanes():
    representatives = [v for v in VECTORS[1:] if next(x for x in v if x) == 1]
    assert len(representatives) == 156
    masks = []
    for functional in representatives:
        masks.append(sum(1 << g for g, v in enumerate(VECTORS)
                         if sum(a * b for a, b in zip(functional, v)) % 5 == 0))
    assert len(set(masks)) == 156 and all(mask.bit_count() == 125 for mask in masks)
    return representatives, masks


def classify(sequence, representatives, masks):
    multiplicities = Counter(sequence)
    assert sorted(multiplicities.values()) == [2, 2, 2, 2, 3, 3]
    counts = [sum(count for g, count in multiplicities.items() if mask & (1 << g)) for mask in masks]
    assert max(counts) <= 12
    h12 = []
    for index, count in enumerate(counts):
        if count == 12:
            mask = masks[index]
            inside = [g for g in sequence if mask & (1 << g)]
            outside = [g for g in sequence if not mask & (1 << g)]
            assert len(outside) == 2 and outside[0] == outside[1]
            assert sorted(Counter(inside).values()) == [2, 2, 2, 3, 3]
            h12.append({"functional_encoded": number(representatives[index]),
                        "functional_coordinates": list(representatives[index]),
                        "inside_sequence": inside, "outside_double_value": outside[0],
                        "inside_multiplicity_profile": [3, 3, 2, 2, 2]})
    return counts, h12


def search(state, candidates, adjacency, engine, deadline):
    n = len(candidates)
    path = []
    levels, leaves, pruning = Counter(), Counter(), Counter()
    nodes = 0
    incomplete = False
    witness = None
    trace = hashlib.sha256()
    width = max(1, (n + 7) // 8)

    def color_available(mask):
        classes = []
        while mask:
            available, color_class = mask, 0
            while available:
                bit = available & -available
                i = bit.bit_length() - 1
                color_class |= bit
                mask ^= bit
                available ^= bit
                available &= ~adjacency[i]
            classes.append(color_class)
        return classes

    def dfs(current, available):
        nonlocal nodes, incomplete, witness
        nodes += 1
        if nodes % 128 == 0 and time.perf_counter() >= deadline:
            incomplete = True
            return
        depth = len(path)
        levels[depth] += 1
        trace.update(bytes((depth,)) + available.to_bytes(width, "little") + bytes(path))
        need = 6 - depth
        if need == 0:
            witness = [candidates[i] for i in path]
            trace.update(b"W")
            return
        if available.bit_count() < need:
            pruning["candidate_count"] += 1
            leaves[depth] += 1
            trace.update(b"N")
            return
        classes = color_available(available)
        if len(classes) < need:
            pruning["proper_coloring"] += 1
            leaves[depth] += 1
            trace.update(b"C")
            return
        choices = available
        has_child = False
        while choices:
            if choices.bit_count() < need:
                pruning["remaining_candidate_count"] += 1
                trace.update(b"R")
                break
            bit = choices & -choices
            choices ^= bit
            i = bit.bit_length() - 1
            g = candidates[i]
            assert not current & ONE_MASK[g]
            updated = engine.append(current, g)
            assert not updated & ZERO
            following = choices & adjacency[i]
            safe_following = 0
            while following:
                next_bit = following & -following
                following ^= next_bit
                j = next_bit.bit_length() - 1
                if not updated & ONE_MASK[candidates[j]]:
                    safe_following |= next_bit
                else:
                    pruning["dynamic_short_zero"] += 1
            path.append(i)
            has_child = True
            dfs(updated, safe_following)
            path.pop()
            if incomplete or witness is not None:
                return
        if not has_child:
            leaves[depth] += 1

    dfs(state, (1 << n) - 1)
    return {"completed_exhaustively": not incomplete and witness is None,
            "decision_complete": not incomplete, "time_limit_reached": incomplete,
            "nodes": nodes, "nodes_by_added": dict(sorted(levels.items())),
            "leaves_by_added": dict(sorted(leaves.items())),
            "prune_counts": dict(sorted(pruning.items())),
            "tree_trace_sha256": trace.hexdigest(), "witness_added_values": witness}


def verify_witness(sequence):
    """Integer counting DP, distinct from the boolean exact-length engine."""
    assert len(sequence) == 20
    plus = {}
    for g in set(sequence):
        a = VECTORS[g]
        plus[g] = [number(tuple((a[i] + b[i]) % 5 for i in range(4))) for b in VECTORS]
    counts = [[0] * Q for _ in range(21)]
    counts[0][0] = 1
    for used, g in enumerate(sequence):
        destinations = plus[g]
        for length in range(used, -1, -1):
            old, following = counts[length], counts[length + 1]
            for h, count in enumerate(old):
                if count:
                    following[destinations[h]] += count
    assert sum(sum(layer) for layer in counts) == 1 << 20
    zero_counts = {length: counts[length][0] for length in range(1, 21) if counts[length][0]}
    minimum = min(zero_counts) if zero_counts else None
    assert minimum is None or minimum > 13
    return {"sequence_encoded": sequence,
            "sequence_coordinates": [list(VECTORS[g]) for g in sequence],
            "nonempty_position_subsets_represented": (1 << 20) - 1,
            "nonempty_zero_counts_by_length": zero_counts,
            "minimum_nonempty_zero_length": minimum,
            "is_B_bad_by_this_counting_DP": minimum is None or minimum > 14,
            "independent_external_certification": "required"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--prefix", default="finite_two_triples_residual")
    args = parser.parse_args()
    assert args.seconds > 0
    assert args.prefix.startswith("finite_two_triples_") and Path(args.prefix).name == args.prefix
    started = time.perf_counter()
    deadline = started + args.seconds
    graph_path = BASE / "evidence/finite_two_triples_probe_cores.jsonl"
    original_summary = json.loads((BASE / "evidence/finite_two_triples_probe.json").read_text(encoding="utf-8"))
    assert original_summary["status"] == "COMPLETE_PROBE_WITH_EXACT_COLORING_RESIDUAL"
    assert sha(graph_path) == original_summary["certificate_sha256"]
    residuals = []
    with graph_path.open(encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            if row["type"] == "core_result" and not row["no_six_new_singletons_certified_by_this_coloring"]:
                assert row["graph_completed"]
                residuals.append(row)
    assert len(residuals) == len({tuple(row["blocks"]) for row in residuals}) == 1022
    assert [row["blocks"] for row in residuals] == original_summary["unresolved_core_keys"]
    representatives, masks = hyperplanes()
    engine = ExactLengths(13)
    profile_path = BASE / "evidence" / (args.prefix + "_hyperplanes.jsonl")
    records_path = BASE / "evidence" / (args.prefix + "_cores.jsonl")
    summary_path = BASE / "evidence" / (args.prefix + ".json")
    h12_keys, direct_cases = [], []
    h12_multiplicity_hist, maximum_hist = Counter(), Counter()
    result = {
        "status": "CLASSIFYING", "role": "bounded execution producer; independent certification required",
        "scope": "only 1022 uncolored residuals of the 8461-core probe",
        "avoidance_cutoff": 13, "extension_size": 6, "seconds_limit": args.seconds,
        "original_already_colored_cores_not_rerun": 7439,
        "expected_residual_cores": 1022, "linear_hyperplanes_per_core": 156,
        "classification_complete": False, "h12_conditional_cores": 0, "direct_search_cores": 0,
        "direct_completed_cores": 0, "direct_attempted_cores": 0, "direct_nodes": 0,
        "direct_root_results": [], "h12_core_keys": [], "unprocessed_core_keys": [],
        "h12_dependency": "pending independent certification of H12 profile and abstract A/B extension lemma; not used to claim closed",
        "input_sha256": {name: sha(BASE / name) for name in (
            "scripts/finite_two_triples_residual.py", "scripts/finite_two_triples_probe.py",
            "scripts/verify_finite_cores_fresh.py", "scripts/verify_finite_double_blocks.py",
            "evidence/finite_two_triples_probe.json", "evidence/finite_two_triples_probe_cores.jsonl")},
        "witness": None, "time_limit_reached": False, "python": sys.version}
    def save():
        result["seconds"] = time.perf_counter() - started
        summary_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    save()
    with profile_path.open("w", encoding="utf-8") as out:
        out.write(json.dumps({"type": "metadata", "hyperplane_functionals": [list(v) for v in representatives],
                              "expected_core_count": 1022, "input_sha256": result["input_sha256"]}) + "\n")
        for index, row in enumerate(residuals):
            if time.perf_counter() >= deadline:
                raise TimeoutError("classification incomplete; no complete claim")
            sequence = list(FIXED) + [g for g in row["blocks"] for _ in range(2)]
            state = engine.build(sequence)
            assert not state & ZERO
            support = sum(1 << g for g in set(sequence))
            assert elements(engine.candidates(state, support, 1)) == row["outside_safe_values"]
            counts, h12 = classify(sequence, representatives, masks)
            maximum_hist[max(counts)] += 1
            h12_multiplicity_hist[len(h12)] += 1
            profile = {"type": "hyperplane_profile", "residual_index": index,
                       "blocks": row["blocks"], "root": row["root"],
                       "all_156_item_counts": counts, "maximum_items_in_hyperplane": max(counts),
                       "h12_hyperplanes": h12, "candidate_count": row["candidate_count"],
                       "classification": "H12_PENDING_EXTERNAL_LEMMA" if h12 else "DIRECT_EXACT_EXTENSION_SEARCH"}
            out.write(json.dumps(profile, separators=(",", ":")) + "\n")
            if h12:
                h12_keys.append(row["blocks"])
            else:
                assert_coloring(row["proper_color_classes"], row["adjacency_bitmasks"])
                direct_cases.append((row, sequence, state))
        out.write(json.dumps({"type": "summary", "classification_complete": True,
                              "core_count": len(residuals), "h12_core_count": len(h12_keys),
                              "direct_core_count": len(direct_cases)}) + "\n")
    result["classification_complete"] = True
    result["h12_conditional_cores"] = len(h12_keys)
    result["h12_core_keys"] = h12_keys
    result["direct_search_cores"] = len(direct_cases)
    result["direct_expected_core_keys"] = [row["blocks"] for row, _, _ in direct_cases]
    result["maximum_hyperplane_item_distribution"] = dict(sorted(maximum_hist.items()))
    result["h12_hyperplanes_per_core_distribution"] = dict(sorted(h12_multiplicity_hist.items()))
    result["direct_six_subset_denominator"] = sum(row["six_subset_count"] for row, _, _ in direct_cases)
    result["direct_seven_subset_denominator"] = sum(row["seven_subset_count"] for row, _, _ in direct_cases)
    result["status"] = "SEARCHING_DIRECT_RESIDUALS"
    save()
    print(json.dumps({"classified": 1022, "h12_conditional": len(h12_keys), "direct_cases": len(direct_cases),
                      "hyperplane_maximum_distribution": dict(sorted(maximum_hist.items())),
                      "direct_six_subset_denominator": result["direct_six_subset_denominator"],
                      "setup_seconds": time.perf_counter() - started}), flush=True)

    completed_by_root = Counter()
    with records_path.open("w", encoding="utf-8") as out:
        out.write(json.dumps({"type": "metadata", "expected_direct_cores": len(direct_cases),
                              "h12_conditional_cores": len(h12_keys), "extension_size": 6,
                              "input_sha256": result["input_sha256"]}) + "\n")
        for index, (row, sequence, state) in enumerate(direct_cases):
            if time.perf_counter() >= deadline:
                result["time_limit_reached"] = True
                break
            record = search(state, row["outside_safe_values"], row["adjacency_bitmasks"], engine, deadline)
            record.update({"type": "direct_core_result", "direct_index": index,
                           "root": row["root"], "blocks": row["blocks"],
                           "candidate_count": row["candidate_count"],
                           "six_subset_count": row["six_subset_count"]})
            out.write(json.dumps(record, separators=(",", ":")) + "\n")
            out.flush()
            result["direct_attempted_cores"] += 1
            result["direct_nodes"] += record["nodes"]
            result["direct_root_results"].append(record)
            if record["completed_exhaustively"]:
                result["direct_completed_cores"] += 1
                completed_by_root[row["root"]] += 1
            if record["witness_added_values"] is not None:
                values = record["witness_added_values"]
                assert len(set(values)) == 6 and not set(values).intersection(sequence)
                result["witness"] = verify_witness(sequence + values)
                result["witness"]["core_blocks"] = row["blocks"]
                result["witness"]["added_values"] = values
                result["status"] = "M13_SAFE_20_ITEM_WITNESS_FOUND_REQUIRES_INDEPENDENT_VERIFICATION"
                save()
                break
            if record["time_limit_reached"]:
                result["time_limit_reached"] = True
                break
            if result["direct_attempted_cores"] % 25 == 0:
                save()
                print(json.dumps({"completed_direct": result["direct_completed_cores"],
                                  "direct_nodes": result["direct_nodes"], "seconds": result["seconds"]}), flush=True)
        result["direct_completed_by_original_root"] = dict(sorted(completed_by_root.items()))
        done_keys = {tuple(row["blocks"]) for row in result["direct_root_results"] if row["completed_exhaustively"]}
        result["uncompleted_direct_core_keys"] = [row["blocks"] for row, _, _ in direct_cases if tuple(row["blocks"]) not in done_keys]
        result["unprocessed_core_keys"] = [row["blocks"] for row, _, _ in direct_cases[result["direct_attempted_cores"]:]]
        if result["direct_completed_cores"] == len(direct_cases):
            assert not result["time_limit_reached"] and result["witness"] is None
            result["status"] = "ALL_DIRECT_CASES_EXHAUSTED_H12_CASES_PENDING_EXTERNAL_LEMMA_AND_INDEPENDENT_VERIFICATION"
        elif result["time_limit_reached"]:
            result["status"] = "PARTIAL_DIRECT_SEARCH_TIME_LIMIT_H12_CASES_PENDING_EXTERNAL_LEMMA"
        out.write(json.dumps({"type": "summary", "status": result["status"],
                              "completed_direct": result["direct_completed_cores"],
                              "expected_direct": len(direct_cases), "h12_conditional_cores": len(h12_keys),
                              "uncompleted_direct": len(result["uncompleted_direct_core_keys"])}) + "\n")
    result["hyperplane_profiles_sha256"] = sha(profile_path)
    result["direct_core_records_sha256"] = sha(records_path)
    save()
    print(json.dumps({k: result[k] for k in (
        "status", "h12_conditional_cores", "direct_search_cores",
        "direct_completed_cores", "direct_nodes", "seconds")}), flush=True)


if __name__ == "__main__":
    main()
