"""Exact certificates for the positional-congruence relaxation (not a sequence search)."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def mask(items):
    return sum(1 << i for i in items)


def positions(bits, n):
    return [i for i in range(n) if bits >> i & 1]


def write_result(name, data):
    path = ROOT / "evidence" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(path), **data}, ensure_ascii=False))


def exact_construction():
    n = 20
    # Pairwise intersections are 0, 4, 4, so the removed 5-block families
    # are disjoint. Positions are zero based throughout this certificate.
    removed_ground_sets = [list(range(9)), list(range(9, 18)),
                           list(range(4)) + list(range(9, 13)) + [18]]
    forbidden = [mask(a) for a in removed_ground_sets]
    blocks = [mask(c) for c in combinations(range(n), 5)
              if not any(mask(c) & f == mask(c) for f in forbidden)]
    incidence = [Counter() for _ in range(5)]
    for b in blocks:
        pts = positions(b, n)
        for d in range(5):
            incidence[d].update(mask(c) for c in combinations(pts, d))
    failures = []
    row_counts = []
    for d in range(5):
        rows = list(combinations(range(n), d))
        row_counts.append(len(rows))
        for c in rows:
            value = incidence[d][mask(c)]
            if value % 5 != 1:
                failures.append({"positions": c, "value": value})
    assert not failures
    assert len(blocks) == 15126
    assert len(blocks) % 25 == 1

    # A 4-core with two extensions records two 15-blocks differing by
    # one position; any actual group realization forces those positions
    # to carry the same group element. A spanning tree is enough.
    by_core = {}
    equal_edges = []
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            a = parent[a]
        return a

    for b in blocks:
        for i in positions(b, n):
            core = b ^ (1 << i)
            if core in by_core:
                j, other = by_core[core]
                if find(i) != find(j):
                    parent[find(i)] = find(j)
                    equal_edges.append({"i": i, "j": j,
                                        "complement_1": positions(b, n),
                                        "complement_2": positions(other, n)})
            else:
                by_core[core] = (i, b)
    classes = {}
    for i in range(n):
        classes.setdefault(find(i), []).append(i)
    assert len(classes) == 1
    data = {
        "status": "RELAXATION_FEASIBLE_NOT_A_GROUP_SEQUENCE",
        "n": n,
        "complement_size": 5,
        "zero_block_size": 15,
        "zero_blocks": len(blocks),
        "removed_ground_sets": removed_ground_sets,
        "checked_rows_by_d": row_counts,
        "all_containment_counts_mod_5": 1,
        "zero_blocks_mod_25": len(blocks) % 25,
        "A_extension": "Append position 20 to every complement; leave every zero block unchanged.",
        "swap_forced_equal_classes": list(classes.values()),
        "swap_equal_spanning_tree": equal_edges,
        "scope": "All individual deletion congruences plus binary membership and the new scalar mod-25 identity. Does not satisfy bounded multiplicity or rank-four realizability.",
    }
    write_result("algebra_positional_pseudomodel.json", data)


def cycle(bits, cycle_size):
    lower = bits & ((1 << cycle_size) - 1)
    return ((lower << 1) & ((1 << cycle_size) - 1)) | (lower >> (cycle_size - 1)) | (bits & (1 << cycle_size))


def orbit(bits, cycle_size):
    found = {bits}
    nxt = cycle(bits, cycle_size)
    while nxt not in found:
        found.add(nxt)
        nxt = cycle(nxt, cycle_size)
    return tuple(sorted(found))


def cyclic_milp(time_limit):
    sys.path.insert(0, str(ROOT / "local_deps"))
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    n, cycle_size = 20, 19
    start = time.monotonic()
    orbit_cache = {}

    def canonical(b):
        if b not in orbit_cache:
            orb = orbit(b, cycle_size)
            for bb in orb:
                orbit_cache[bb] = orb[0]
        return orbit_cache[b]

    block_orbits = {}
    for c in combinations(range(n), 5):
        b = mask(c)
        cb = canonical(b)
        if cb not in block_orbits:
            block_orbits[cb] = orbit(cb, cycle_size)
    row_reps = [sorted({canonical(mask(c)) for c in combinations(range(n), d)})
                for d in range(5)]
    # Strengthened relaxation: distinct elements. Thus at most one
    # selected 5-complement contains any fixed 4-core.
    usable_orbits = []
    for orb in block_orbits.values():
        counts = Counter(mask(c) for b in orb for c in combinations(positions(b, n), 4))
        if max(counts.values()) <= 1:
            usable_orbits.append(orb)
    modular_reps = sum(row_reps[:4], [])
    packing_reps = row_reps[4]
    nb, nq = len(usable_orbits), len(modular_reps)
    rows, cols, values = [], [], []
    for ridx, rep in enumerate(modular_reps + packing_reps):
        for cidx, orb in enumerate(usable_orbits):
            count = sum(rep & b == rep for b in orb)
            if count:
                rows.append(ridx)
                cols.append(cidx)
                values.append(count)
        if ridx < nq:
            rows.append(ridx)
            cols.append(nb + ridx)
            values.append(-5)
    nr = nq + len(packing_reps)
    matrix = coo_matrix((values, (rows, cols)), shape=(nr, nb + nq)).tocsc()
    lower = np.concatenate([np.ones(nq), np.full(len(packing_reps), -np.inf)])
    upper = np.ones(nr)
    objective = np.concatenate([np.array([len(o) for o in usable_orbits]), np.zeros(nq)])
    result = milp(objective, integrality=np.ones(nb + nq),
                  bounds=Bounds(np.zeros(nb + nq), np.concatenate([np.ones(nb), np.full(nq, 10000)])),
                  constraints=LinearConstraint(matrix, lower, upper),
                  options={"time_limit": time_limit, "mip_rel_gap": 0.0})
    data = {"status": int(result.status), "message": result.message,
            "elapsed_seconds": time.monotonic() - start,
            "block_orbits": nb, "modular_rows": nq,
            "packing_rows": len(packing_reps),
            "restriction": "Only 15-zero blocks; invariant under a 19-cycle fixing the 20th point; no Johnson-adjacent pair."}
    if result.x is not None:
        chosen = [o for i, o in enumerate(usable_orbits) if result.x[i] > 0.5]
        blocks = sorted(b for o in chosen for b in o)
        data["zero_blocks"] = len(blocks)
        data["orbit_representatives"] = [positions(o[0], n) for o in chosen]
        # Exact integer independent check of the returned floating point incumbent.
        for rep in modular_reps:
            assert sum(rep & b == rep for b in blocks) % 5 == 1
        for rep in packing_reps:
            assert sum(rep & b == rep for b in blocks) <= 1
        data["exact_incumbent_check"] = True
    if getattr(result, "mip_dual_bound", None) is not None:
        data["mip_dual_bound"] = float(result.mip_dual_bound)
    write_result("algebra_cyclic_distinct_probe.json", data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["exact-construction", "cyclic-milp"])
    parser.add_argument("--seconds", type=float, default=45)
    args = parser.parse_args()
    if args.mode == "exact-construction":
        exact_construction()
    else:
        cyclic_milp(args.seconds)
