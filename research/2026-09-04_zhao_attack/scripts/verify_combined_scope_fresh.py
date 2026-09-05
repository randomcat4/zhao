"""Fresh, bounded-scope verification; no imports of author search programs.

Checks the 36 lower-bound coefficient types, the old multiplicity table,
and replays the two small m=13 distinct-double-block trees using exact
length bitsets. The 20M-node 3332 tree is not re-executed here.
"""
from collections import Counter
from functools import reduce
from hashlib import sha256
from itertools import permutations, product
from math import comb
from operator import or_
from pathlib import Path
import json
import sys
import time

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "evidence" / "verify_combined_scope_fresh.json"
Q = 625
M = 13
W = (1, 5, 25, 125)
V = tuple(tuple((g // w) % 5 for w in W) for g in range(Q))
NEG = tuple(sum((-x % 5) * w for x, w in zip(v, W)) for v in V)
NEG2 = tuple(sum((-2 * x % 5) * w for x, w in zip(v, W)) for v in V)
BIT = tuple(1 << g for g in range(Q))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def lower_bound():
    support = ((4, 1, 0, 0), (1, 3, 1, 0), (1, 3, 0, 1), (4, 4, 1, 1))
    rows = []
    counts = Counter()
    tested = 0
    for extra in product(range(2), range(3), range(3), range(2)):
        tested += 1
        base = tuple(-sum(n * v[j] for n, v in zip(extra, support)) % 5 for j in range(4))
        if any(n == 4 for n in base):
            continue
        length = sum(extra) + sum(base)
        weight = 1
        for cap, n in zip((3, 3, 3, 3, 1, 2, 2, 1), base + extra):
            weight *= comb(cap, n)
        counts[length] += weight
        if length:
            rows.append({"extra_abcd": extra, "basis": base, "length": length,
                         "position_count": weight})
    assert tested == 36
    assert rows == [
        {"extra_abcd": (0, 1, 2, 1), "basis": (3, 2, 3, 2), "length": 14, "position_count": 18},
        {"extra_abcd": (0, 2, 1, 1), "basis": (3, 2, 2, 3), "length": 14, "position_count": 18},
        {"extra_abcd": (0, 2, 2, 0), "basis": (1, 3, 3, 3), "length": 14, "position_count": 3},
        {"extra_abcd": (1, 2, 2, 0), "basis": (2, 2, 3, 3), "length": 15, "position_count": 9},
        {"extra_abcd": (1, 2, 2, 1), "basis": (3, 3, 2, 2), "length": 16, "position_count": 9},
    ]
    assert dict(counts) == {0: 1, 14: 39, 15: 9, 16: 9}
    return {"types": tested, "nonempty_zero_types": rows, "counts": dict(counts),
            "minimum_nonempty_zero_length": 14}


def old_multiplicity_table():
    result = {}
    for n in (21, 20):
        accepted = []
        for a, b, c in product(range(8), range(12), range(22)):
            if 3*a + 2*b + c != n:
                continue
            if a > 3 or a+b > 8 or (a >= 2 and a+b > 7) or (a == 3 and b > 1):
                continue
            accepted.append((a, b, c))
        rows = [{"a": a, "max_b": max(b for aa, b, c in accepted if aa == a),
                 "min_support": min(aa+b+c for aa, b, c in accepted if aa == a)}
                for a in range(4)]
        assert [r["max_b"] for r in rows] == [8, 7, 5, 1]
        assert [r["min_support"] for r in rows] == ([13, 12, 12, 14] if n == 21 else [12, 11, 11, 13])
        result[str(n)] = {"rows": rows, "allowed_triples_abc": accepted,
                          "not_a_realizability_claim": True}
    return result


# Translate exact sum sets by cyclically shifting each base-five coordinate.
# This does not use a shortest-distance table or the author's update routine.
OPS = []
for g in range(Q):
    ops = []
    for j, w in enumerate(W):
        d = V[g][j]
        if d:
            low = sum(BIT[h] for h in range(Q) if V[h][j] < 5-d)
            high = sum(BIT[h] for h in range(Q) if V[h][j] >= 5-d)
            ops.append((low, high, d*w, (5-d)*w))
    OPS.append(ops)


def translate(bits, g):
    for low, high, left, right in OPS[g]:
        bits = ((bits & low) << left) | ((bits & high) >> right)
    return bits


def one_position(state, g):
    # Immutable old tuple guarantees the new position is used at most once.
    nxt = (1,) + tuple(state[k] | translate(state[k-1], g) for k in range(1, M+1))
    assert all((x & 1) == 0 for x in nxt[1:])
    return nxt


def safe_blocks(state, candidates):
    upto12 = reduce(or_, state[:M], 0)
    upto11 = reduce(or_, state[:M-1], 0)
    return [g for g in candidates if not (upto12 & BIT[NEG[g]] or upto11 & BIT[NEG2[g]])]


def replay(mode):
    source = BASE / "evidence" / f"atom_{mode}_m13_blocks.jsonl"
    original = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
    meta = next(r for r in original if r["type"] == "metadata")
    original_rows = [r for r in original if r["type"] == "root"]
    records = {r["root"]: r for r in original_rows}
    assert len(records) == len(original_rows)
    summary = next(r for r in original if r["type"] == "summary")
    mult = (2, 2, 2, 2) if mode == "2222" else (3, 3, 2, 2)
    length0 = sum(mult)
    state = [0]*(M+1)
    for coeffs in product(*(range(k+1) for k in mult)):
        state[sum(coeffs)] |= BIT[sum(x*w for x, w in zip(coeffs, W))]
    state = tuple(state)
    universe = [g for g in range(1, Q) if g not in W]
    initial = safe_blocks(state, universe)
    group = (list(permutations(range(4))) if mode == "2222" else
             [(a,b,c,d) for a,b in ((0,1),(1,0)) for c,d in ((2,3),(3,2))])
    roots = [g for g in initial
             if g == min(sum(V[g][p[j]]*W[j] for j in range(4)) for p in group)]
    assert initial == meta["initial_safe_candidates"]
    assert roots == meta["canonical_roots"]
    assert set(records) == set(roots)
    assert all(r["completed_exhaustively"] for r in records.values())
    checked = []
    for root in roots:
        levels, leaves = Counter(), Counter()

        def walk(current, candidates, length):
            levels[length] += 1
            if not candidates:
                leaves[length] += 1
            for i, g in enumerate(candidates):
                added = one_position(one_position(current, g), g)
                walk(added, safe_blocks(added, candidates[i+1:]), length+2)

        added = one_position(one_position(state, root), root)
        walk(added, safe_blocks(added, [g for g in initial if g > root]), length0+2)
        row = {"root": root, "nodes": sum(levels.values()),
               "nodes_by_length": {str(k): v for k, v in sorted(levels.items())},
               "leaves_by_length": {str(k): v for k, v in sorted(leaves.items())},
               "max_reached_length": max(levels)}
        for key in ("nodes", "nodes_by_length", "leaves_by_length", "max_reached_length"):
            assert row[key] == records[root][key], (mode, root, key)
        assert records[root]["terminal_count"] == 0
        checked.append(row)
    nodes = sum(row["nodes"] for row in checked)
    maximum = max(row["max_reached_length"] for row in checked)
    assert summary["all_roots_completed"]
    assert summary["attempted_roots"] == summary["completed_roots_this_run"] == len(roots)
    assert summary["nodes_this_run"] == nodes
    assert summary["max_reached_length_this_run"] == maximum == 16
    return {"mode": mode, "m": M, "initial_safe_count": len(initial),
            "root_count": len(roots), "nodes": nodes, "maximum_length": maximum,
            "source_sha256": digest(source), "all_per_root_counts_matched": True,
            "roots": checked}


if __name__ == "__main__":
    start = time.monotonic()
    result = {"status": "RUNNING", "python": sys.version,
              "script_sha256": digest(Path(__file__)), "lower_bound": lower_bound(),
              "old_multiplicity_table": old_multiplicity_table(), "replays": []}
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    # All singleton translations checked independently by coordinate arithmetic.
    for g, h in product(range(Q), repeat=2):
        expected = sum(((x+y) % 5)*w for x,y,w in zip(V[g],V[h],W))
        assert translate(BIT[h], g) == BIT[expected]
    result["singleton_translation_checks"] = Q*Q
    for mode in ("3322", "2222"):
        result["replays"].append(replay(mode))
        print(json.dumps({k:v for k,v in result["replays"][-1].items() if k != "roots"}), flush=True)
    result["status"] = "PASS"
    result["elapsed_seconds"] = time.monotonic()-start
    result["input_sha256"] = {
        str(path.relative_to(BASE)): digest(path) for path in [
            BASE/"proofs"/"certified_reduction.md", BASE/"proofs"/"lower_bound_18.md",
            BASE/"formal"/"LowerBound18.lean", BASE/"proofs"/"stronger_algebra.md",
            BASE/"scripts"/"atom_double_blocks.ps1", BASE/"scripts"/"atom_verify_double_blocks.py",
            BASE/"evidence"/"verify_finite_332_resumed.json"]}
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "elapsed_seconds": result["elapsed_seconds"]}), flush=True)
