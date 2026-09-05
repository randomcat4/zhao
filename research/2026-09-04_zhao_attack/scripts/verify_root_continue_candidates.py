"""Independent verifier for the two root_continue candidates.

Uses tuple-valued addition and explicit enumeration of all 2^12 position
subsets.  It does not import or execute either producer.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations
from json import dump, loads
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOFS = ROOT / "proofs"
SCRIPTS = ROOT / "scripts"
EVIDENCE = ROOT / "evidence"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def decode(n):
    return (n % 5, (n // 5) % 5, n // 25)


def encode(v):
    return v[0] + 5 * v[1] + 25 * v[2]


def decode_big_endian(n):
    return (n // 25, (n // 5) % 5, n % 5)


VEC = [decode(i) for i in range(125)]


def add(a, b):
    va, vb = VEC[a], VEC[b]
    return encode(tuple((va[j] + vb[j]) % 5 for j in range(3)))


def neg(a):
    return encode(tuple((-x) % 5 for x in VEC[a]))


def extend_reachable(reachable, g):
    return reachable | {add(x, g) for x in reachable}


def direct_profile(seq):
    """Enumerate each of the 4096 position masks, with no distance DP."""
    count = 1 << len(seq)
    sums = [0] * count
    sizes = [0] * count
    dist = [99] * 125
    witnesses = [None] * 125
    dist[0] = 0
    witnesses[0] = 0
    zero_masks = []
    for mask in range(1, count):
        bit = mask & -mask
        i = bit.bit_length() - 1
        prev = mask ^ bit
        sums[mask] = add(sums[prev], seq[i])
        sizes[mask] = sizes[prev] + 1
        target = sums[mask]
        if sizes[mask] < dist[target]:
            dist[target] = sizes[mask]
            witnesses[target] = mask
        if target == 0:
            zero_masks.append(mask)
    sigma = sums[-1]
    return dist, witnesses, sigma, zero_masks


def rank_mod5(rows):
    rows = [[x % 5 for x in row] for row in rows]
    if not rows:
        return 0
    m, n = len(rows), len(rows[0])
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, m) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, 5)
        rows[rank] = [(inv * x) % 5 for x in rows[rank]]
        for i in range(m):
            if i != rank and rows[i][col]:
                a = rows[i][col]
                rows[i] = [(x - a * y) % 5 for x, y in zip(rows[i], rows[rank])]
        rank += 1
        if rank == m:
            break
    return rank


def weak_compositions(total, parts, prefix=()):
    if parts == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from weak_compositions(total - first, parts - 1, prefix + (first,))


def verify_label_lemmas():
    seven_cases = 0
    for counts in weak_compositions(7, 4):
        q = tuple(x for x, c in enumerate(counts, 1) for _ in range(c))
        rows = []
        for mask in range(1, 1 << 7):
            if mask.bit_count() <= 5 and sum(q[i] for i in range(7) if mask >> i & 1) % 5 == 0:
                rows.append([int(mask >> i & 1) for i in range(7)])
        if rank_mod5(rows) == rank_mod5([row + [1] for row in rows]):
            raise AssertionError(("seven-label affine system unexpectedly solvable", counts))
        seven_cases += 1

    nine_cases = 0
    rank_hist = Counter()
    for counts in weak_compositions(9, 4):
        q = tuple(x for x, c in enumerate(counts, 1) for _ in range(c))
        rows = []
        for mask in range(1, 1 << 9):
            if mask.bit_count() <= 5 and sum(q[i] for i in range(9) if mask >> i & 1) % 5 == 0:
                rows.append([int(mask >> i & 1) for i in range(9)])
        rank = rank_mod5(rows)
        rank_hist[rank] += 1
        if rank != 8:
            raise AssertionError(("nine-label relation space has wrong rank", counts, rank))
        nine_cases += 1

    q6 = (1, 1, 2, 2, 2, 2)
    b6 = (1, 1, 0, 0, 0, 0)
    qualifying = []
    for mask in range(1, 1 << 6):
        if mask.bit_count() <= 5 and sum(q6[i] for i in range(6) if mask >> i & 1) % 5 == 0:
            bsum = sum(b6[i] for i in range(6) if mask >> i & 1) % 5
            if bsum != 1:
                raise AssertionError(("six-position boundary record fails", mask, bsum))
            qualifying.append(mask)
    return {
        "seven_nonzero_label_multisets_checked": seven_cases,
        "all_seven_affine_systems_inconsistent": True,
        "nine_nonzero_label_multisets_checked": nine_cases,
        "nine_relation_matrix_rank_histogram": dict(rank_hist),
        "all_nine_kernels_equal_span_of_q": True,
        "six_position_boundary_qualifying_subsets": len(qualifying),
        "six_position_boundary_all_have_label_one": True,
    }


def verify_h12():
    base = (1, 1, 5, 5, 25, 25)
    basis = {1, 5, 25}
    reachable = {0}
    for g in base:
        reachable = extend_reachable(reachable, g)
    pool = [
        g for g in range(1, 125)
        if g not in basis and neg(g) not in reachable
    ]
    perms = list(permutations(range(3)))

    def canonical(g):
        v = VEC[g]
        return min(encode(tuple(v[p[j]] for j in range(3))) for p in perms)

    roots = [g for g in pool if canonical(g) == g]
    nodes = 0
    depths = Counter()
    by_root_nodes = []
    sequences = []

    def dfs(seq, sums_now, candidates):
        nonlocal nodes
        nodes += 1
        depths[len(seq)] += 1
        if len(seq) == 12:
            sequences.append(tuple(seq))
            return
        counts = Counter(seq)
        for ix, g in enumerate(candidates):
            if counts[g] >= 2 or neg(g) in sums_now:
                continue
            newer = extend_reachable(sums_now, g)
            child = [
                x for x in candidates[ix:]
                if counts[x] + (x == g) < 2 and neg(x) not in newer
            ]
            dfs(seq + (g,), newer, child)

    for root in roots:
        newer = extend_reachable(reachable, root)
        candidates = [g for g in pool if g >= root and neg(g) not in newer]
        before = nodes
        dfs(base + (root,), newer, candidates)
        by_root_nodes.append((root, nodes - before))

    source_rows = [loads(line) for line in
                   (EVIDENCE / "root_continue_h12_height2_profiles.jsonl")
                   .read_text(encoding="utf-8").splitlines() if line]
    source_by_seq = {tuple(row["sequence"]): row for row in source_rows}
    if len(source_by_seq) != len(source_rows):
        raise AssertionError("producer profile file contains duplicate sequences")
    if set(sequences) != set(source_by_seq):
        raise AssertionError("independent and producer normalized leaves differ")

    histogram = Counter()
    e9_hist = Counter()
    e10_hist = Counter()
    zero_mask_hist = Counter()
    exact_matches = 0
    bad_records = []
    for seq in sequences:
        dist, witness, sigma, zero_masks = direct_profile(seq)
        zero_mask_hist[len(zero_masks)] += 1
        if zero_masks:
            raise AssertionError(("not zero-sumfree", seq, zero_masks))
        if dist[sigma] != 12 or sum(x == 12 for x in dist) != 1:
            raise AssertionError(("non-unique distance 12", seq, sigma, dist))
        mx = max(d for h, d in enumerate(dist) if h != sigma)
        e9 = sum(d >= 9 for d in dist)
        e10 = sum(d >= 10 for d in dist)
        histogram[mx] += 1
        e9_hist[e9] += 1
        e10_hist[e10] += 1
        row = source_by_seq[seq]
        if (row["sigma"] != sigma or row["distances"] != dist
                or row["max_except_total"] != mx
                or row["E9"] != e9 or row["E10"] != e10):
            raise AssertionError(("profile mismatch", seq))
        exact_matches += 1
        if mx > 8:
            bad_records.append((seq, sigma, mx))

    expected_hist = {6: 155, 7: 1443, 8: 217, 9: 46, 10: 20}
    if dict(sorted(histogram.items())) != expected_hist:
        raise AssertionError(("histogram mismatch", histogram))
    if max(e9_hist) > 2 or max(e10_hist) > 2:
        raise AssertionError(("exception sets too large", e9_hist, e10_hist))

    return {
        "initial_pool": len(pool),
        "roots": roots,
        "root_count": len(roots),
        "nodes": nodes,
        "depth_counts": dict(sorted(depths.items())),
        "root_node_counts": by_root_nodes,
        "leaves": len(sequences),
        "producer_rows_exactly_matched": exact_matches,
        "all_4096_position_subsets_checked_per_leaf": True,
        "zero_mask_count_histogram": dict(zero_mask_hist),
        "max_except_total_histogram": dict(sorted(histogram.items())),
        "E9_size_histogram": dict(sorted(e9_hist.items())),
        "E10_size_histogram": dict(sorted(e10_hist.items())),
        "counterexamples_to_L8": len(bad_records),
    }


def verify_dense_counterexample():
    record = loads((EVIDENCE / "root_continue_dense_probe.json")
                   .read_text(encoding="utf-8"))["counterexample"]
    seq = tuple(record["sequence"])
    if len(seq) != 12 or max(Counter(seq).values()) > 2:
        raise AssertionError("dense counterexample has wrong length or height")
    dist, witness, sigma, zero_masks = direct_profile(seq)
    if record["vectors"] != [list(decode_big_endian(g)) for g in seq]:
        raise AssertionError("dense record vectors do not match its encoding")
    if zero_masks:
        raise AssertionError(("dense record is not zero-sumfree", zero_masks))
    target = record["exception"]
    if sigma != record["sigma"] or dist != record["table"]:
        raise AssertionError("dense record table or sigma mismatch")
    if target == sigma or dist[target] != 7 or dist[target] <= 6:
        raise AssertionError("dense record does not disprove L=6")
    mask = witness[target]
    positions = [i for i in range(12) if mask >> i & 1]
    return {
        "sequence": list(seq),
        "vectors_as_printed_in_candidate": [list(decode_big_endian(g)) for g in seq],
        "height": max(Counter(seq).values()),
        "position_subsets_checked": 1 << 12,
        "no_nonempty_zero_sum": True,
        "sigma": sigma,
        "exception": target,
        "exception_vector_as_printed_in_candidate": list(decode_big_endian(target)),
        "distance": dist[target],
        "one_minimal_position_witness_zero_based": positions,
        "one_minimal_witness_values": [seq[i] for i in positions],
    }


def main():
    result = {
        "status": "PASS",
        "method": (
            "Independent tuple arithmetic, independent normalized DFS, and "
            "explicit enumeration of all 4096 position masks for every leaf"
        ),
        "hashes": {
            str(PROOFS / "root_continue_dense19.md"): digest(PROOFS / "root_continue_dense19.md"),
            str(PROOFS / "root_continue_two_exceptions.md"): digest(PROOFS / "root_continue_two_exceptions.md"),
            str(SCRIPTS / "root_continue_h12_height2.py"): digest(SCRIPTS / "root_continue_h12_height2.py"),
            str(SCRIPTS / "root_continue_dense_probe.py"): digest(SCRIPTS / "root_continue_dense_probe.py"),
            str(EVIDENCE / "root_continue_h12_height2_profiles.jsonl"): digest(EVIDENCE / "root_continue_h12_height2_profiles.jsonl"),
            str(EVIDENCE / "root_continue_h12_height2.json"): digest(EVIDENCE / "root_continue_h12_height2.json"),
            str(EVIDENCE / "root_continue_dense_probe.json"): digest(EVIDENCE / "root_continue_dense_probe.json"),
        },
        "label_lemmas": verify_label_lemmas(),
        "h12": verify_h12(),
        "dense_counterexample": verify_dense_counterexample(),
    }
    out = EVIDENCE / "verify_root_continue_candidates.json"
    with out.open("w", encoding="utf-8") as f:
        dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(out)
    print(result["h12"])
    print(result["dense_counterexample"])


if __name__ == "__main__":
    main()
