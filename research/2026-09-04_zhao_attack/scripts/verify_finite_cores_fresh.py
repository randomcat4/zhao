"""Independent exact-length-bitset replay of the two finite core exclusions.

No imports from atom_five_triples or atom_four_independent. Every DFS node
rebuilds its candidate set from all 625 vectors; there is no inherited safe
candidate list. No time limit, node limit, random choices, or external package.
The output is RUNNING until every requested finite tree returns normally.
"""

import argparse
from collections import Counter
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import platform
import sys
import time


Q = 625
FULL = (1 << Q) - 1
VECTORS = tuple((i % 5, (i // 5) % 5, (i // 25) % 5, i // 125)
                for i in range(Q))
E = (1, 5, 25, 125)
PERMS = tuple(permutations(range(4)))


def number(v):
    a, b, c, d = v
    return a + 5 * b + 25 * c + 125 * d


def digits_masks():
    return tuple(tuple(sum(1 << k for k, v in enumerate(VECTORS) if v[i] == a)
                       for a in range(5)) for i in range(4))


DIGITS = digits_masks()


def negative_bits(bits):
    """Coordinate-wise additive inversion of a 625-bit subset of F_5^4."""
    for i, masks in enumerate(DIGITS):
        u = 5 ** i
        bits = ((bits & masks[0]) | ((bits & masks[1]) << (3 * u))
                | ((bits & masks[2]) << u) | ((bits & masks[3]) >> u)
                | ((bits & masks[4]) >> (3 * u)))
    return bits


def translation_ops(layers):
    repeated = tuple(tuple(sum(mask << (Q * k) for k in range(layers))
                           for mask in masks) for masks in DIGITS)
    result = []
    for v in VECTORS:
        ops = []
        for i, a in enumerate(v):
            if a:
                no_wrap = sum(repeated[i][:5 - a])
                wrap = sum(repeated[i][5 - a:])
                ops.append((no_wrap, wrap, a * 5 ** i, (5 - a) * 5 ** i))
        result.append(tuple(ops))
    return tuple(result)


def translate(bits, ops):
    for no_wrap, wrap, left, right in ops:
        bits = ((bits & no_wrap) << left) | ((bits & wrap) >> right)
    return bits


class ExactLengths:
    """Bit (625*l+h) is present iff an l-position subsequence sums to h."""

    def __init__(self, cutoff):
        self.m = cutoff
        self.ops = translation_ops(cutoff + 1)
        self.all_layers = (1 << (Q * (cutoff + 1))) - 1
        self.nonempty_zero = sum(1 << (Q * k) for k in range(1, cutoff + 1))

    def append(self, state, g):
        shifted = (translate(state, self.ops[g]) << Q) & self.all_layers
        return state | shifted

    def candidates(self, state, saturated=0, lower=1):
        # A new zero sum of length <=m uses a sum -g of length 0,...,m-1.
        reachable = 0
        for _ in range(self.m):
            reachable |= state & FULL
            state >>= Q
        allowed = FULL & ~negative_bits(reachable) & ~saturated
        return (allowed >> lower) << lower

    def build(self, sequence):
        state = 1  # empty subsequence, length 0, sum 0
        for g in sequence:
            state = self.append(state, g)
        return state


def elements(bits):
    result = []
    while bits:
        bit = bits & -bits
        bits ^= bit
        result.append(bit.bit_length() - 1)
    return result


def orbit_minimum(g):
    v = VECTORS[g]
    return min(number(tuple(v[i] for i in p)) for p in PERMS)


def primitive_checks():
    group_ops = translation_ops(1)
    pairs = 0
    for g, a in enumerate(VECTORS):
        expected_neg = number(tuple((-x) % 5 for x in a))
        assert negative_bits(1 << g) == 1 << expected_neg
        assert number(a) == g
        for h, b in enumerate(VECTORS):
            expected = number(tuple((a[i] + b[i]) % 5 for i in range(4)))
            assert translate(1 << h, group_ops[g]) == 1 << expected
            pairs += 1

    # Independent coefficient enumeration: every zero sum in V*x^3 has t>0.
    accepted = []
    nonempty_zero_free = []
    for x, v in enumerate(VECTORS):
        lengths = []
        for t in (1, 2, 3):
            coefficients = tuple((-t * a) % 5 for a in v)
            if max(coefficients) <= 3:
                lengths.append(t + sum(coefficients))
        if not lengths:
            nonempty_zero_free.append(x)
        if not lengths or min(lengths) > 13:
            accepted.append(x)
        assert (not lengths or min(lengths) > 13) == ({1, 2, 3} <= set(v))
    assert accepted == nonempty_zero_free
    classes = sorted({tuple(sorted(VECTORS[x])) for x in accepted})
    assert classes == [(0, 1, 2, 3), (1, 1, 2, 3), (1, 2, 2, 3),
                       (1, 2, 3, 3), (1, 2, 3, 4)]

    # Compare every reachable (length,sum) with direct position subsets on
    # deterministic edge cases. Repeated positions remain separate choices.
    samples = [(), (0,), (1,), (1, 1, 1, 1, 1),
               (1, 4), (1, 5, 25, 125, 6, 130),
               (624, 124, 24, 4, 311, 311, 42, 0)]
    states = 0
    for m in (3, 13, 14):
        engine = ExactLengths(m)
        for seq in samples:
            direct = 0
            for inclusion in product((0, 1), repeat=len(seq)):
                length = sum(inclusion)
                if length > m:
                    continue
                v = tuple(sum(VECTORS[g][i] * use for g, use in zip(seq, inclusion)) % 5
                          for i in range(4))
                direct |= 1 << (Q * length + number(v))
            assert engine.build(seq) == direct
            states += 1
        assert not (engine.candidates(1) & 1)
        assert not (engine.candidates(engine.build((1,) * 4)) & (1 << 1)) if m >= 5 else True
    return {"coordinate_addition_pairs": pairs, "coordinate_negations": Q,
            "exact_length_edge_case_states": states,
            "all_x_classified": Q, "admissible_x": len(accepted),
            "normalized_classes": [list(v) for v in classes]}, classes


def search_tree(core, n, engine, capacity, root=None):
    begun = time.monotonic()
    counts = Counter(core)
    caps = [capacity] * Q
    for g in counts:
        caps[g] = 3
    saturated = sum(1 << g for g in counts if counts[g] == caps[g])
    state = engine.build(core)
    assert not (state & engine.nonempty_zero)
    added = []
    if root is not None:
        assert engine.candidates(state, saturated) & (1 << root)
        counts[root] += 1
        added.append(root)
        state = engine.append(state, root)
        if counts[root] == caps[root]:
            saturated |= 1 << root
    levels, leaves = Counter(), Counter()
    longest, terminals = [], []

    def visit(current, saturated_bits, lower):
        nonlocal longest
        length = len(core) + len(added)
        levels[length] += 1
        assert not (current & engine.nonempty_zero)
        if len(added) > len(longest):
            longest = added[:]
        if length == n:
            terminals.append(added[:])
            return
        # Recompute from the full group. No use of the parent's candidate set.
        candidates = engine.candidates(current, saturated_bits, lower)
        if not candidates:
            leaves[length] += 1
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            g = bit.bit_length() - 1
            counts[g] += 1
            assert counts[g] <= caps[g]
            new_saturated = saturated_bits | bit if counts[g] == caps[g] else saturated_bits
            added.append(g)
            visit(engine.append(current, g), new_saturated, g)
            added.pop()
            counts[g] -= 1

    visit(state, saturated, 1 if root is None else root)
    return {"n": n, "m": engine.m, "root": root,
            "completed_exhaustively": True,
            "nodes_by_length": {str(k): v for k, v in sorted(levels.items())},
            "leaves_by_length": {str(k): v for k, v in sorted(leaves.items())},
            "nodes": sum(levels.values()), "max_reached_length": max(levels),
            "one_longest_extension_encoded": longest,
            "terminal_extensions": terminals,
            "seconds": round(time.monotonic() - begun, 6)}


def compare_counts(actual, reference):
    for field in ("nodes_by_length", "leaves_by_length", "nodes", "max_reached_length",
                  "terminal_extensions", "completed_exhaustively"):
        assert actual[field] == reference[field], (field, actual, reference)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    base = Path(__file__).resolve().parents[1]
    started = time.monotonic()
    result = {"status": "RUNNING", "all_completed": False,
              "algorithm": "all exact lengths; packed bitsets; fresh all-vector candidates",
              "limits": "none", "height_assumption": 3,
              "python": sys.version, "platform": platform.platform(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "five_runs": [], "four_roots": [], "four_runs": []}

    def save():
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    save()
    checks, cores = primitive_checks()
    result["primitive_checks"] = checks
    old_five = json.loads((base / "evidence/atom_five_triples.json").read_text(encoding="utf-8"))
    old_four = json.loads((base / "evidence/atom_four_independent_A.json").read_text(encoding="utf-8"))
    for n, m in ((21, 13), (20, 14)):
        engine = ExactLengths(m)
        for v in cores:
            core = tuple(g for g in (*E, number(v)) for _ in range(3))
            record = search_tree(core, n, engine, capacity=3)
            record["core_type"] = list(v)
            previous = next(r for r in old_five["runs"]
                            if r["core_type"] == list(v) and r["n"] == n and r["m"] == m)
            compare_counts(record, previous)
            record["original_counts_match"] = True
            result["five_runs"].append(record)
            save()
            print(json.dumps({"kind": "five", "core_type": v,
                              "n": n, "nodes": record["nodes"]}), flush=True)

    # Root representatives are independently generated by all 24 permutations.
    engine = ExactLengths(13)
    core = tuple(g for g in E for _ in range(3))
    initial = elements(engine.candidates(engine.build(core), sum(1 << g for g in E)))
    assert initial == [g for g in range(Q) if 1 in VECTORS[g] and g not in E]
    roots = sorted({orbit_minimum(g) for g in initial})
    assert all(g in initial for g in roots)
    assert roots == [g for g in initial if tuple(sorted(VECTORS[g], reverse=True)) == VECTORS[g]]
    assert initial == old_four["initial_safe_candidates"]
    assert roots == old_four["canonical_roots"] == old_four["selected_roots"]
    result["four_initial_safe_candidates"] = initial
    result["four_roots"] = roots
    save()
    for root in roots:
        record = search_tree(core, 21, engine, capacity=2, root=root)
        previous = next(r for r in old_four["runs"] if r["root"] == root)
        compare_counts(record, previous)
        record["original_counts_match"] = True
        result["four_runs"].append(record)
        save()
        print(json.dumps({"kind": "four", "root": root, "nodes": record["nodes"],
                          "max_length": record["max_reached_length"],
                          "seconds": record["seconds"]}), flush=True)
    result["four_total_nodes"] = sum(r["nodes"] for r in result["four_runs"])
    result["four_max_reached_length"] = max(r["max_reached_length"] for r in result["four_runs"])
    result["all_completed"] = True
    result["status"] = "PASS"
    result["seconds"] = round(time.monotonic() - started, 6)
    save()
    print(json.dumps({k: result[k] for k in ("status", "all_completed", "four_total_nodes",
                                            "four_max_reached_length", "seconds")}), flush=True)


if __name__ == "__main__":
    main()
