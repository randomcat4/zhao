"""Bounded producer search, not an independent certification of its conclusion.

For all supplied length-15 3222 cores with <=20 outside-safe values, decide
whether five new distinct values can be adjoined while avoiding zero sums of
length <=13. Uses pair compatibility, proper-coloring clique bounds, and
incremental exact-length subset-sum states. Excludes the nine 127-value cores.
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


BASE = Path(__file__).resolve().parents[1]
FIXED = (1, 1, 1, 5, 5, 25, 25, 125, 125)
NEG = [number(tuple((-x) % 5 for x in v)) for v in VECTORS]
ONE_MASK = [sum(1 << (Q * l + NEG[g]) for l in range(13)) for g in range(Q)]
PAIR_MASK = [sum(1 << (Q * l + NEG[g]) for l in range(12)) for g in range(Q)]
FORBIDDEN_ZERO = sum(1 << (Q * l) for l in range(1, 14))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    source = BASE / "evidence/atom_3222_len15_scan.jsonl"
    check_path = BASE / "evidence/atom_3222_len15_scan_check.json"
    check = json.loads(check_path.read_text(encoding="utf-8"))
    assert check["source_sha256"] == sha(source)
    records, excluded = [], []
    seen = set()
    by_root = Counter()
    root_records = {}
    histogram = Counter()
    metadata = summary = None
    with source.open(encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            if row["type"] == "metadata":
                assert metadata is None
                metadata = row
            elif row["type"] == "root":
                assert row["root"] not in root_records
                root_records[row["root"]] = row
            elif row["type"] == "summary":
                assert summary is None
                summary = row
            else:
                assert row["type"] == "leaf_profile" and row["length"] == 15
                blocks = tuple(row["blocks"])
                candidates = tuple(row["outside_safe_additions"])
                assert len(blocks) == 3 and blocks == tuple(sorted(set(blocks)))
                assert blocks not in seen and not set(blocks).intersection(E)
                assert row["root"] == blocks[0]
                assert candidates == tuple(sorted(set(candidates)))
                assert not set(candidates).intersection(set(E) | set(blocks))
                assert row["five_subset_count"] == math.comb(len(candidates), 5)
                seen.add(blocks)
                histogram[len(candidates)] += 1
                by_root[row["root"]] += 1
                entry = (len(seen) - 1, row["root"], blocks, candidates)
                if len(candidates) <= 20:
                    records.append(entry)
                else:
                    assert len(candidates) == 127
                    excluded.append(entry)
    assert metadata and summary and summary["all_roots_completed"]
    assert (metadata["mode"], metadata["m"], metadata["target"]) == ("3222", 13, 15)
    assert sorted(root_records) == metadata["canonical_roots"]
    assert len(root_records) == 106
    for root, row in root_records.items():
        assert row["completed_exhaustively"]
        assert by_root[root] == row["nodes_by_length"].get("15", 0)
    assert len(seen) == check["length15_node_count"] == summary["leaf_profile_count"] == 107656
    assert dict(sorted(histogram.items())) == {int(k): v for k, v in check["outside_safe_count_distribution"].items()}
    assert len(records) == 107647 and len(excluded) == 9
    assert {x[2] for x in excluded} == {tuple(x["blocks"]) for x in check["extreme_nodes_with_more_than20_candidates"]}
    return records, excluded, by_root, metadata, source, check_path


def coloring(mask, adjacency):
    """Produce a proper coloring; each returned bitset is an independent set."""
    remaining = mask
    classes = []
    while remaining:
        available, color_class = remaining, 0
        while available:
            bit = available & -available
            v = bit.bit_length() - 1
            color_class |= bit
            remaining ^= bit
            available ^= bit
            available &= ~adjacency[v]
        classes.append(color_class)
    return classes


def search_core(state, candidates, plus, engine, deadline):
    n = len(candidates)
    adjacency = [0] * n
    pair_checks = 0
    for i in range(n):
        for j in range(i + 1, n):
            pair_checks += 1
            if not state & PAIR_MASK[plus[candidates[i]][candidates[j]]]:
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
    full = (1 << n) - 1
    root_colors = coloring(full, adjacency)
    # Check that the explicit certificate really is a proper partition.
    union = 0
    for color_class in root_colors:
        assert not union & color_class
        union |= color_class
        for i in elements(color_class):
            assert not adjacency[i] & color_class
    assert union == full

    path = []
    levels = Counter()
    prune = Counter()
    trace = hashlib.sha256()
    stopped_for_time = False
    witness = None
    nodes = 0

    def dfs(current, available):
        nonlocal nodes, stopped_for_time, witness
        nodes += 1
        if nodes % 128 == 0 and time.perf_counter() >= deadline:
            stopped_for_time = True
            return
        depth = len(path)
        levels[depth] += 1
        trace.update(bytes((depth,)) + available.to_bytes(3, "little") + bytes(path))
        need = 5 - depth
        if need == 0:
            witness = [candidates[i] for i in path]
            return
        if available.bit_count() < need:
            prune["candidate_count"] += 1
            trace.update(b"N")
            return
        classes = root_colors if depth == 0 else coloring(available, adjacency)
        if len(classes) < need:
            prune["proper_coloring"] += 1
            trace.update(b"C")
            return
        choices = available
        while choices:
            if choices.bit_count() < need:
                prune["remaining_candidate_count"] += 1
                trace.update(b"R")
                return
            bit = choices & -choices
            choices ^= bit
            i = bit.bit_length() - 1
            g = candidates[i]
            assert not current & ONE_MASK[g]
            updated = engine.append(current, g)
            assert not updated & FORBIDDEN_ZERO
            following = choices & adjacency[i]
            safe_following = 0
            while following:
                hbit = following & -following
                following ^= hbit
                j = hbit.bit_length() - 1
                if not updated & ONE_MASK[candidates[j]]:
                    safe_following |= hbit
                else:
                    prune["dynamic_short_zero"] += 1
            path.append(i)
            dfs(updated, safe_following)
            path.pop()
            if stopped_for_time or witness is not None:
                return

    dfs(state, full)
    return {"completed_exhaustively": not stopped_for_time and witness is None,
            "decision_complete": not stopped_for_time,
            "stopped_for_time": stopped_for_time, "witness_added_values": witness,
            "candidate_count": n, "adjacency_bitmasks": adjacency,
            "root_proper_color_classes": root_colors, "pair_checks": pair_checks,
            "dfs_nodes": nodes, "nodes_by_added": {str(k): v for k, v in sorted(levels.items())},
            "prune_counts": dict(sorted(prune.items())), "tree_trace_sha256": trace.hexdigest()}


def gray_witness(sequence):
    """Different oracle: all 2^20-1 nonempty position subsets in Gray order."""
    current = [0, 0, 0, 0]
    previous, length = 0, 0
    counts = Counter()
    for index in range(1, 1 << len(sequence)):
        gray = index ^ (index >> 1)
        bit = gray ^ previous
        position = bit.bit_length() - 1
        sign = 1 if gray & bit else -1
        length += sign
        v = VECTORS[sequence[position]]
        for i in range(4):
            current[i] = (current[i] + sign * v[i]) % 5
        if not any(current):
            counts[length] += 1
        previous = gray
    minimum = min(counts) if counts else None
    assert minimum is None or minimum > 13
    return {"sequence_encoded": list(sequence), "sequence_coordinates": [list(VECTORS[g]) for g in sequence],
            "subsets_checked": (1 << len(sequence)) - 1,
            "nonempty_zero_sum_counts_by_length": {str(k): v for k, v in sorted(counts.items())},
            "minimum_nonempty_zero_sum_length": minimum,
            "is_B_counterexample_by_direct_subsets": minimum is None or minimum > 14,
            "independent_external_certification": "required"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--prefix", default="finite_single_extension_trial")
    args = parser.parse_args()
    assert args.seconds > 0
    assert args.prefix.startswith("finite_single_extension_") and Path(args.prefix).name == args.prefix
    start = time.perf_counter()
    deadline = start + args.seconds
    records, excluded, input_by_root, metadata, source, check_path = prepare()
    engine = ExactLengths(13)
    base_state = engine.build(FIXED)
    plus = [[number(tuple((a[i] + b[i]) % 5 for i in range(4))) for b in VECTORS] for a in VECTORS]
    root_states, prefix_states = {}, {}
    eligible_by_root = Counter(r[1] for r in records)
    processed_by_root = Counter()
    denominator = sum(math.comb(len(r[3]), 5) for r in records)
    assert denominator == 47953716
    result = {"status": "RUNNING", "role": "bounded execution producer; prior verifier role does not certify this result",
              "independent_certification": "required", "scope": "a=1,b=6 length15 core plus five new distinct singleton values",
              "avoidance_cutoff": 13, "target_length": 20, "seconds_limit": args.seconds,
              "input_length15_cores": 107656, "eligible_cores": len(records),
              "excluded_cores": [{"source_index": i, "root": r, "blocks": list(b), "candidate_count": len(c)} for i, r, b, c in excluded],
              "input_root_count": len(metadata["canonical_roots"]), "eligible_cores_by_root": dict(sorted(eligible_by_root.items())),
              "five_subset_denominator": denominator, "processed_cores": 0, "completed_cores": 0,
              "processed_five_subset_denominator": 0, "total_pair_checks": 0, "total_dfs_nodes": 0,
              "trivial_fewer_than5_cores": 0, "root_coloring_excluded_cores": 0,
              "candidate_count_distribution": {}, "aggregate_prune_counts": {}, "witness": None,
              "input_sha256": {"scripts/finite_single_extension_search.py": sha(Path(__file__)),
                               "scripts/verify_finite_cores_fresh.py": sha(BASE / "scripts/verify_finite_cores_fresh.py"),
                               "evidence/atom_3222_len15_scan.jsonl": sha(source),
                               "evidence/atom_3222_len15_scan_check.json": sha(check_path)},
              "python": sys.version}
    summary_path = BASE / "evidence" / (args.prefix + ".json")
    cores_path = BASE / "evidence" / (args.prefix + "_cores.jsonl")
    histogram, pruning = Counter(), Counter()

    def save():
        result["seconds"] = time.perf_counter() - start
        result["completed_cores_by_root"] = dict(sorted(processed_by_root.items()))
        result["candidate_count_distribution"] = dict(sorted(histogram.items()))
        result["aggregate_prune_counts"] = dict(sorted(pruning.items()))
        summary_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    save()
    print(json.dumps({"eligible_cores": len(records), "denominator": denominator,
                      "excluded_cores": len(excluded), "setup_seconds": time.perf_counter() - start}), flush=True)
    with cores_path.open("w", encoding="utf-8") as out:
        out.write(json.dumps({"type": "metadata", "input_sha256": result["input_sha256"],
                              "eligible_cores": len(records), "max_outside_candidates": 20, "cutoff": 13,
                              "trace_order": "ascending candidate index; complete proper-coloring partition"}) + "\n")
        for source_index, root, blocks, candidates in records:
            if time.perf_counter() >= deadline:
                result["status"] = "INCOMPLETE_TIME_LIMIT"
                break
            if blocks[0] not in root_states:
                state = engine.append(engine.append(base_state, blocks[0]), blocks[0])
                root_states[blocks[0]] = state
            prefix = blocks[:2]
            if prefix not in prefix_states:
                state = root_states[blocks[0]]
                prefix_states[prefix] = engine.append(engine.append(state, blocks[1]), blocks[1])
            state = prefix_states[prefix]
            state = engine.append(engine.append(state, blocks[2]), blocks[2])
            assert not state & FORBIDDEN_ZERO
            used = sum(1 << g for g in (*E, *blocks))
            computed = elements(engine.candidates(state, used, 1))
            assert computed == list(candidates), blocks
            if len(candidates) < 5:
                record = {"completed_exhaustively": True, "decision_complete": True,
                          "candidate_count": len(candidates), "reason": "fewer_than_five_outside_safe_values",
                          "pair_checks": 0, "dfs_nodes": 0, "nodes_by_added": {},
                          "prune_counts": {"initial_candidate_count": 1}, "witness_added_values": None}
                result["trivial_fewer_than5_cores"] += 1
            else:
                record = search_core(state, candidates, plus, engine, deadline)
                if len(record["root_proper_color_classes"]) < 5:
                    result["root_coloring_excluded_cores"] += 1
            record.update({"type": "core_result", "source_index": source_index, "root": root,
                           "blocks": list(blocks), "outside_safe_values": list(candidates),
                           "five_subset_denominator": math.comb(len(candidates), 5)})
            out.write(json.dumps(record, separators=(",", ":")) + "\n")
            result["processed_cores"] += 1
            result["total_pair_checks"] += record["pair_checks"]
            result["total_dfs_nodes"] += record["dfs_nodes"]
            pruning.update(record["prune_counts"])
            if record["completed_exhaustively"]:
                result["completed_cores"] += 1
                processed_by_root[root] += 1
                histogram[len(candidates)] += 1
                result["processed_five_subset_denominator"] += record["five_subset_denominator"]
            if record["witness_added_values"] is not None:
                sequence = FIXED + tuple(g for g in blocks for _ in range(2)) + tuple(record["witness_added_values"])
                result["witness"] = gray_witness(sequence)
                result["witness"]["core_blocks"] = list(blocks)
                result["witness"]["added_values"] = record["witness_added_values"]
                result["status"] = "EXISTENCE_WITNESS_FOUND_REQUIRES_INDEPENDENT_VERIFICATION"
                save()
                break
            if not record["completed_exhaustively"]:
                result["status"] = "INCOMPLETE_TIME_LIMIT"
                save()
                break
            if result["processed_cores"] % 5000 == 0:
                out.flush()
                save()
                print(json.dumps({"completed_cores": result["completed_cores"],
                                  "pair_checks": result["total_pair_checks"], "dfs_nodes": result["total_dfs_nodes"],
                                  "seconds": result["seconds"]}), flush=True)
        if result["completed_cores"] == len(records):
            assert dict(processed_by_root) == dict(eligible_by_root)
            assert result["processed_five_subset_denominator"] == denominator
            result["status"] = "COMPUTATION_COMPLETE_NO_SAFE_FIVE_EXTENSION_REQUIRES_INDEPENDENT_VERIFICATION"
        out.write(json.dumps({"type": "summary", "status": result["status"],
                              "completed_cores": result["completed_cores"],
                              "eligible_cores": len(records), "total_dfs_nodes": result["total_dfs_nodes"]}) + "\n")
    result["core_records_sha256"] = sha(cores_path)
    save()
    print(json.dumps({k: result[k] for k in ("status", "completed_cores", "total_pair_checks", "total_dfs_nodes", "seconds")}), flush=True)


if __name__ == "__main__":
    main()
