"""Independent full-tree verifier for root_continue_all_H12.md.

The tree uses explicit sets of tuplewise sums and a global sorted pool/index,
rather than the producers' translated 125-bit masks and child-list DFS.
Distances are then recomputed in vectorized integer arrays.
"""

from collections import Counter
from hashlib import sha256
from itertools import permutations
from json import dump, loads
from pathlib import Path
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "proofs"
S = ROOT / "scripts"
E = ROOT / "evidence"
VEC = np.array([(i % 5, (i // 5) % 5, i // 25) for i in range(125)], dtype=np.int16)
ADD = np.empty((125, 125), dtype=np.uint8)
SUB = np.empty((125, 125), dtype=np.uint8)
for a in range(125):
    for b in range(125):
        z = (VEC[a] + VEC[b]) % 5
        ADD[a, b] = int(z[0] + 5*z[1] + 25*z[2])
        z = (VEC[a] - VEC[b]) % 5
        SUB[a, b] = int(z[0] + 5*z[1] + 25*z[2])
NEG = [int(SUB[0, g]) for g in range(125)]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def initial_reach(base):
    reach = {0}
    for g in base:
        reach |= {int(ADD[x, g]) for x in tuple(reach)}
    return frozenset(reach)


def orbit_min(g, perms):
    v = VEC[g]
    return min(int(v[p[0]] + 5*v[p[1]] + 25*v[p[2]]) for p in perms)


def config(kind, parameter):
    basis = (1, 5, 25)
    if kind == "double":
        r = parameter
        base = tuple(g for j, g in enumerate(basis) for _ in range(2 if j < r else 1))
        # Total capacities in the final sequence.
        total_cap = [2 if not np.any(VEC[g, r:]) else 1 for g in range(125)]
        excluded = set(basis)
        perms = [p for p in permutations(range(3)) if set(p[:r]) == set(range(r))]
        profile = E / f"root_continue_h12_double_rank{r}_profiles.jsonl"
        summary = E / f"root_continue_h12_double_rank{r}.json"
        name = f"double_rank{r}"
    else:
        a = parameter
        base = tuple(g for j, g in enumerate(basis) for _ in range(3 if j < a else 1))
        total_cap = [2] * 125
        for j in range(a):
            total_cap[basis[j]] = 3
        excluded = set()
        perms = [p for p in permutations(range(3)) if set(p[:a]) == set(range(a))]
        profile = E / f"root_continue_h12_triples{a}_profiles.jsonl"
        summary = E / f"root_continue_h12_triples{a}.json"
        name = f"triples{a}"
    reach = initial_reach(base)
    counts = [0] * 125
    for g in base:
        counts[g] += 1
    pool = [g for g in range(1, 125)
            if g not in excluded and counts[g] < total_cap[g] and NEG[g] not in reach]
    roots = [g for g in pool if orbit_min(g, perms) == g]
    return name, base, total_cap, pool, roots, reach, counts, profile, summary


def rebuild(kind, parameter):
    name, base, caps, pool, roots, reach0, counts, profile_path, summary_path = config(kind, parameter)
    index = {g: i for i, g in enumerate(pool)}
    nodes = 0
    depth = Counter()
    root_nodes = []
    leaves = []
    start_time = time.monotonic()

    def dfs(seq, reach, start):
        nonlocal nodes
        nodes += 1
        depth[len(seq)] += 1
        if len(seq) == 12:
            leaves.append(seq)
            return
        for ix in range(start, len(pool)):
            g = pool[ix]
            if counts[g] >= caps[g] or NEG[g] in reach:
                continue
            counts[g] += 1
            newer = frozenset(set(reach) | {int(ADD[x, g]) for x in reach})
            dfs(seq + (g,), newer, ix)
            counts[g] -= 1

    for g in roots:
        if counts[g] >= caps[g] or NEG[g] in reach0:
            raise AssertionError((name, "invalid root", g))
        counts[g] += 1
        newer = frozenset(set(reach0) | {int(ADD[x, g]) for x in reach0})
        before = nodes
        dfs(base + (g,), newer, index[g])
        root_nodes.append((g, nodes-before))
        counts[g] -= 1

    producer_rows = [loads(line) for line in profile_path.read_text(encoding="utf-8").splitlines() if line]
    producer = {tuple(row["sequence"]): row for row in producer_rows}
    if len(producer) != len(producer_rows):
        raise AssertionError((name, "duplicate producer rows"))
    if set(leaves) != set(producer):
        missing = set(producer) - set(leaves)
        extra = set(leaves) - set(producer)
        raise AssertionError((name, "leaf set mismatch", len(missing), len(extra)))

    return {
        "name": name,
        "base": list(base),
        "pool": len(pool),
        "roots": roots,
        "nodes": nodes,
        "depth_counts": dict(sorted(depth.items())),
        "root_node_counts": root_nodes,
        "leaves": len(leaves),
        "seconds_tree": time.monotonic()-start_time,
        "leaf_sequences": leaves,
        "producer": producer,
        "profile_path": profile_path,
        "summary_path": summary_path,
    }


def recompute_profiles(tree, batch_size=2048):
    leaves = tree.pop("leaf_sequences")
    producer = tree.pop("producer")
    hist = Counter()
    e9hist = Counter()
    e10hist = Counter()
    exact = 0
    remaining_patterns = Counter()
    geometry = Counter()
    remaining_sequences = []
    started = time.monotonic()
    for lo in range(0, len(leaves), batch_size):
        seqs = leaves[lo:lo+batch_size]
        arr = np.asarray(seqs, dtype=np.uint8)
        n = len(seqs)
        d = np.full((n, 125), 99, dtype=np.int16)
        d[:, 0] = 0
        rows = np.arange(n)[:, None]
        for col in range(12):
            targets = SUB[:, arr[:, col]].T
            d = np.minimum(d, 1 + d[rows, targets])
        sigvec = np.mod(VEC[arr].sum(axis=1), 5)
        sigma = (sigvec[:, 0] + 5*sigvec[:, 1] + 25*sigvec[:, 2]).astype(int)
        for k, seq in enumerate(seqs):
            dist = d[k].tolist()
            sig = int(sigma[k])
            if dist[0] != 0 or dist[sig] != 12 or dist.count(12) != 1 or max(dist) != 12:
                raise AssertionError((tree["name"], "distance boundary", seq))
            mx = max(x for i, x in enumerate(dist) if i != sig)
            e9 = sum(x >= 9 for x in dist)
            e10 = sum(x >= 10 for x in dist)
            row = producer[seq]
            if (row["sigma"] != sig or row["distances"] != dist
                    or row["max_except_total"] != mx
                    or row["E9"] != e9 or row["E10"] != e10):
                raise AssertionError((tree["name"], "profile mismatch", seq))
            hist[mx] += 1
            e9hist[e9] += 1
            e10hist[e10] += 1
            exact += 1
            if tree["name"].startswith("triples"):
                ex = [VEC[i].astype(int).tolist() for i, x in enumerate(dist) if x >= 9]
                lin = rank5(ex)
                aff = rank5([[(x-y) % 5 for x, y in zip(v, ex[0])] for v in ex[1:]])
                if lin <= 1:
                    kind = "linear_line"
                elif lin > aff:
                    kind = "affine_separated_from_zero"
                else:
                    kind = "remaining"
                    mult = Counter(seq)
                    pattern = tuple(sorted(mult.values(), reverse=True))
                    remaining_patterns[pattern] += 1
                    remaining_sequences.append(list(seq))
                geometry[kind] += 1
    tree.update({
        "profiles_exactly_matched": exact,
        "max_except_total_histogram": dict(sorted(hist.items())),
        "E9_histogram": dict(sorted(e9hist.items())),
        "E10_histogram": dict(sorted(e10hist.items())),
        "geometry_histogram": dict(geometry),
        "remaining_multiplicity_patterns": {str(k): v for k, v in remaining_patterns.items()},
        "remaining_sequences": remaining_sequences,
        "seconds_profiles": time.monotonic()-started,
    })
    # Keep the public machine result compact.
    tree.pop("profile_path")
    tree.pop("summary_path")
    return tree


def rank5(rows):
    a = [[x % 5 for x in row] for row in rows]
    if not a:
        return 0
    rr = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(rr, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[rr], a[pivot] = a[pivot], a[rr]
        inv = pow(a[rr][c], -1, 5)
        a[rr] = [(inv*x) % 5 for x in a[rr]]
        for i in range(len(a)):
            if i != rr and a[i][c]:
                m = a[i][c]
                a[i] = [(x-m*y) % 5 for x, y in zip(a[i], a[rr])]
        rr += 1
    return rr


def main():
    named = [
        ("double", 1), ("double", 2), ("triple", 1), ("triple", 2),
    ]
    results = []
    for kind, p in named:
        print("TREE", kind, p, flush=True)
        tree = rebuild(kind, p)
        print(tree["name"], tree["nodes"], tree["leaves"], tree["seconds_tree"], flush=True)
        results.append(recompute_profiles(tree))
        print("PROFILE", results[-1]["name"], results[-1]["profiles_exactly_matched"], flush=True)
    files = [
        P / "root_continue_all_H12.md",
        S / "root_continue_h12_low_double_rank.py",
        S / "root_continue_h12_one_two_triples.py",
        S / "root_continue_exception_geometry.py",
        E / "root_continue_h12_double_rank1.json",
        E / "root_continue_h12_double_rank1_profiles.jsonl",
        E / "root_continue_h12_double_rank2.json",
        E / "root_continue_h12_double_rank2_profiles.jsonl",
        E / "root_continue_h12_triples1.json",
        E / "root_continue_h12_triples1_profiles.jsonl",
        E / "root_continue_h12_triples2.json",
        E / "root_continue_h12_triples2_profiles.jsonl",
        E / "root_continue_exception_geometry.json",
    ]
    out = {
        "status": "PASS",
        "method": "independent explicit-sum global-index DFS plus vectorized distance recomputation",
        "hashes": {str(p): digest(p) for p in files},
        "trees": results,
        "total_nodes": sum(r["nodes"] for r in results) + 174501,
        "total_leaves": sum(r["leaves"] for r in results) + 1881,
        "rank3_height2_reused_from_separate_fresh_report": "verify_root_continue_core.md",
    }
    path = E / "verify_root_continue_all_H12.json"
    with path.open("w", encoding="utf-8") as f:
        dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("PASS", path, out["total_nodes"], out["total_leaves"], flush=True)


if __name__ == "__main__":
    main()
