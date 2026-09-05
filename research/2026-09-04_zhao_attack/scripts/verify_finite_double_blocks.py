"""Fresh exact-length replay of 2222/3322 block trees and every 2222 length-16 leaf.

Uses no production search functions and no NumPy. Every admitted double block
is adjoined as two separate positions, both checked for forbidden zero sums.
The independent leaf JSONL includes all 625 minimum lengths, not only a histogram.
"""

from collections import Counter
import hashlib
from itertools import permutations
import json
from pathlib import Path
import time

from verify_finite_cores_fresh import ExactLengths, E, VECTORS, DIGITS, FULL, Q, elements, number, negative_bits


BASE = Path(__file__).resolve().parents[1]
M = 13
STATE_LENGTH = 16
ZERO_FORBIDDEN = sum(1 << (Q * l) for l in range(1, M + 1))
NEG = [number(tuple((-x) % 5 for x in v)) for v in VECTORS]
DANGER = [sum(1 << (Q * l + NEG[g]) for l in range(M)) for g in range(Q)]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_lines(name):
    return [json.loads(s) for s in (BASE / "evidence" / name).read_text(encoding="utf-8").splitlines() if s]


def twice_bits(bits):
    for i, masks in enumerate(DIGITS):
        u = 5 ** i
        bits = ((bits & masks[0]) | ((bits & masks[1]) << u)
                | ((bits & masks[2]) << (2 * u))
                | ((bits & masks[3]) >> (2 * u)) | ((bits & masks[4]) >> u))
    return bits


def block_candidates(state, used, lower):
    # A zero sum using exactly one new g requires -g at length <=12.
    # One using two requires -2g at length <=11; equivalently g=2h in F_5.
    shorter = 0
    for _ in range(M - 1):
        shorter |= state & FULL
        state >>= Q
    single = shorter | (state & FULL)
    allowed = FULL & ~negative_bits(single) & ~twice_bits(shorter) & ~used
    return (allowed >> lower) << lower


def append_two(engine, state, g):
    assert not state & DANGER[g]
    first = engine.append(state, g)
    assert not first & DANGER[g]
    second = engine.append(first, g)
    assert not second & ZERO_FORBIDDEN
    return second


def allowed_permutations(mode):
    if mode == "2222":
        return tuple(permutations(range(4)))
    return ((0, 1, 2, 3), (1, 0, 2, 3), (0, 1, 3, 2), (1, 0, 3, 2))


def canonical(g, perms):
    v = VECTORS[g]
    return min(number(tuple(v[i] for i in p)) for p in perms)


def all_distances(state):
    distances = [99] * Q
    seen = 0
    for length in range(STATE_LENGTH + 1):
        layer = state & FULL
        fresh = layer & ~seen
        while fresh:
            bit = fresh & -fresh
            fresh ^= bit
            distances[bit.bit_length() - 1] = length
        seen |= layer
        state >>= Q
    return distances


def root_search(mode, root, engine, core, profile_callback):
    started = time.perf_counter()
    used = sum(1 << g for g in E) | (1 << root)
    state = append_two(engine, engine.build(core), root)
    path = [root]
    levels, leaves = Counter(), Counter()
    longest, terminal = [], []
    sequential_adjoins = 2

    def dfs(state, used, lower):
        nonlocal longest, sequential_adjoins
        length = len(core) + 2 * len(path)
        levels[length] += 1
        assert not state & ZERO_FORBIDDEN
        if len(path) > len(longest):
            longest = path[:]
        if mode == "2222" and length == 16:
            profile_callback(path, state)
        if length == 18:
            terminal.append(path[:])
            return
        candidates = block_candidates(state, used, lower)
        if not candidates:
            leaves[length] += 1
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            g = bit.bit_length() - 1
            child = append_two(engine, state, g)
            sequential_adjoins += 2
            path.append(g)
            dfs(child, used | bit, g + 1)
            path.pop()

    dfs(state, used, root + 1)
    return {"root": root, "completed_exhaustively": True,
            "nodes": sum(levels.values()),
            "nodes_by_length": {str(k): v for k, v in sorted(levels.items())},
            "leaves_by_length": {str(k): v for k, v in sorted(leaves.items())},
            "max_reached_length": max(levels), "one_longest_extension_blocks": longest,
            "terminal_count": len(terminal), "terminal_blocks": terminal,
            "separate_position_adjoins": sequential_adjoins,
            "seconds": time.perf_counter() - started}


def same_record(actual, expected):
    for field in ("nodes", "nodes_by_length", "leaves_by_length", "max_reached_length",
                  "terminal_count", "completed_exhaustively"):
        assert actual[field] == expected[field], (actual["root"], field)


def main():
    start = time.perf_counter()
    engine = ExactLengths(STATE_LENGTH)
    for g, v in enumerate(VECTORS):
        assert twice_bits(1 << g) == 1 << number(tuple((2 * x) % 5 for x in v))
    profile_lines = load_lines("atom_2222_leaf_profiles.jsonl")
    profile_meta, profile_summary = profile_lines[0], profile_lines[-1]
    assert profile_meta["script_sha256"] == digest(BASE / "scripts/atom_double_block_leaf_profiles.ps1")
    assert (profile_meta["mode"], profile_meta["m"], profile_meta["target"]) == ("2222", 13, 16)
    original_profiles = {}
    profile_roots = {}
    for row in profile_lines[1:-1]:
        if row["type"] == "leaf_profile":
            key = tuple(row["blocks"])
            assert key not in original_profiles and row["root"] == key[0]
            original_profiles[key] = row
        else:
            assert row["type"] == "root" and row["root"] not in profile_roots
            profile_roots[row["root"]] = row
    assert len(original_profiles) == profile_summary["leaf_profile_count"] == 10196
    assert profile_summary["all_roots_completed"]

    output_path = BASE / "evidence/verify_finite_double_blocks.json"
    leaf_path = BASE / "evidence/verify_finite_double_leaf_profiles.jsonl"
    safe_hist, coverage_hist, maximum_hist = Counter(), Counter(), Counter()
    observed_leaf_keys = set()
    result = {"status": "RUNNING", "all_completed": False,
              "algorithm": "independent exact-length bitsets; two separate position adjoins per block",
              "avoidance_cutoff": 13, "independent_target": 18, "state_maximum_length": 16,
              "limits": "none", "runs": [],
              "input_sha256": {name: digest(BASE / name) for name in (
                  "scripts/verify_finite_double_blocks.py", "scripts/verify_finite_cores_fresh.py",
                  "scripts/atom_double_blocks.ps1", "scripts/atom_double_block_leaf_profiles.ps1",
                  "evidence/atom_2222_m13_blocks.jsonl", "evidence/atom_3322_m13_blocks.jsonl",
                  "evidence/atom_2222_leaf_profiles.jsonl")}}

    def save():
        result["seconds"] = time.perf_counter() - start
        output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    save()
    with leaf_path.open("w", encoding="utf-8") as leaf_file:
        leaf_file.write(json.dumps({"type": "metadata", "mode": "2222", "length": 16,
                                    "cutoff": 13, "distance_encoding": "index h is low-coordinate-first base 5",
                                    "script_sha256": result["input_sha256"]["scripts/verify_finite_double_blocks.py"]}) + "\n")

        def profile(path, state):
            key = tuple(path)
            assert key not in observed_leaf_keys and key in original_profiles
            observed_leaf_keys.add(key)
            old = original_profiles[key]
            distances = all_distances(state)
            histogram = {str(k): v for k, v in sorted(Counter(distances).items())}
            safe = [g for g in range(Q) if distances[NEG[g]] + 1 > 13]
            safe14 = [g for g in range(Q) if distances[NEG[g]] + 1 > 14]
            coverage = sum(x < 99 for x in distances)
            row = {"type": "leaf_profile", "root": path[0], "blocks": list(path), "length": 16,
                   "minimum_lengths": distances, "coverage": coverage, "unreachable_count": 625 - coverage,
                   "maximum_distance": max(distances),
                   "finite_maximum_distance": max(x for x in distances if x < 99),
                   "distance_counts": histogram, "safe_single_additions": safe,
                   "safe_single_additions_cutoff14": safe14}
            for field in ("coverage", "unreachable_count", "maximum_distance", "finite_maximum_distance",
                          "distance_counts", "safe_single_additions", "safe_single_additions_cutoff14"):
                assert row[field] == old[field], (key, field)
            # Verify the safety list directly against adding each of 625 positions.
            # This uses zero bits in the translated state, not the distance lookup.
            direct_safe = [g for g in range(Q) if not engine.append(state, g) & ZERO_FORBIDDEN]
            assert direct_safe == safe
            assert len(safe) <= 1
            safe_hist[len(safe)] += 1
            coverage_hist[coverage] += 1
            maximum_hist[max(distances)] += 1
            leaf_file.write(json.dumps(row, separators=(",", ":")) + "\n")

        for mode, expected_total, expected_root_count in (("2222", 185077, 44), ("3322", 24267, 122)):
            raw = load_lines("atom_" + mode + "_m13_blocks.jsonl")
            meta, summary = raw[0], raw[-1]
            reference_roots = [r for r in raw if r["type"] == "root"]
            assert meta["script_sha256"] == digest(BASE / "scripts/atom_double_blocks.ps1")
            assert (meta["mode"], meta["m"], meta["target"], meta["block_multiplicity"]) == (mode, 13, 20, 2)
            multiplicities = [2] * 4 if mode == "2222" else [3, 3, 2, 2]
            core = tuple(g for g, c in zip(E, multiplicities) for _ in range(c))
            state0 = engine.build(core)
            assert not state0 & ZERO_FORBIDDEN
            used0 = sum(1 << g for g in E)
            initial = elements(block_candidates(state0, used0, 1))
            assert initial == meta["initial_safe_candidates"]
            assert len(initial) == meta["initial_safe_count"]
            # Full-domain test of the block mask against two sequential additions.
            explicit = []
            for g in range(1, Q):
                if g in E:
                    continue
                one = engine.append(state0, g)
                two = engine.append(one, g)
                if not two & ZERO_FORBIDDEN:
                    explicit.append(g)
            assert explicit == initial
            roots = sorted({canonical(g, allowed_permutations(mode)) for g in initial})
            assert len(roots) == expected_root_count and roots == meta["canonical_roots"]
            assert sorted(r["root"] for r in reference_roots) == roots
            assert len(reference_roots) == len(roots)
            assert all(r["completed_exhaustively"] for r in reference_roots)
            assert summary["all_roots_completed"] and summary["completed_roots_this_run"] == len(roots)
            assert summary["nodes_this_run"] == expected_total
            if mode == "2222":
                assert profile_meta["initial_safe_candidates"] == initial
                assert profile_meta["canonical_roots"] == roots == sorted(profile_roots)
            mode_result = {"mode": mode, "core_multiplicities": multiplicities,
                           "initial_safe_count": len(initial), "canonical_roots": roots, "roots": []}
            result["runs"].append(mode_result)
            for root in roots:
                record = root_search(mode, root, engine, core, profile)
                reference = next(r for r in reference_roots if r["root"] == root)
                same_record(record, reference)
                assert record["nodes"] == sum(record["nodes_by_length"].values())
                assert record["terminal_count"] == 0
                record["all_tree_counts_match"] = True
                mode_result["roots"].append(record)
                if mode == "2222":
                    earlier = profile_roots[root]
                    assert earlier["completed_exhaustively"]
                    for field in ("nodes", "nodes_by_length", "max_reached_length"):
                        assert earlier[field] == record[field]
                    assert earlier["terminal_count"] == record["nodes_by_length"].get("16", 0)
                    assert earlier["leaves_by_length"] == {k: v for k, v in record["leaves_by_length"].items() if k != "16"}
                leaf_file.flush()
                save()
            mode_result["all_roots_completed"] = True
            mode_result["nodes"] = sum(r["nodes"] for r in mode_result["roots"])
            mode_result["maximum_reached_length"] = max(r["max_reached_length"] for r in mode_result["roots"])
            assert mode_result["nodes"] == expected_total and mode_result["maximum_reached_length"] == 16
            totals = Counter()
            for r in mode_result["roots"]:
                totals.update(r["nodes_by_length"])
            mode_result["aggregate_nodes_by_length"] = dict(sorted(totals.items()))
            print(json.dumps({"mode": mode, "roots": len(roots), "nodes": mode_result["nodes"],
                              "maximum": 16, "seconds": time.perf_counter() - start}), flush=True)

        assert observed_leaf_keys == set(original_profiles)
        assert dict(safe_hist) == {0: 2153, 1: 8043}
        assert len(observed_leaf_keys) == 10196
        assert len(observed_leaf_keys) == result["runs"][0]["aggregate_nodes_by_length"]["16"]
        leaf_file.write(json.dumps({"type": "summary", "status": "PASS",
                                    "leaf_count": len(observed_leaf_keys),
                                    "safe_additions_count_distribution": dict(safe_hist),
                                    "coverage_distribution": dict(coverage_hist),
                                    "maximum_distance_distribution": dict(maximum_hist)}) + "\n")
    result["status"] = "FULL_INDEPENDENT_REPLAY_PASS"
    result["all_completed"] = True
    result["leaf_count"] = len(observed_leaf_keys)
    result["safe_additions_count_distribution"] = dict(sorted(safe_hist.items()))
    result["leaf_coverage_distribution"] = dict(sorted(coverage_hist.items()))
    result["leaf_maximum_distance_distribution"] = dict(sorted(maximum_hist.items()))
    result["leaf_output_sha256"] = digest(leaf_path)
    result["all_625_single_additions_tested_at_each_leaf"] = True
    save()
    print(json.dumps({k: result[k] for k in ("status", "leaf_count", "safe_additions_count_distribution", "seconds")}), flush=True)


if __name__ == "__main__":
    main()
