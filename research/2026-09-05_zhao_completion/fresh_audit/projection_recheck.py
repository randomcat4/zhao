#!/usr/bin/env python3
"""Independent standard-library checker for the harvested projection certificate.

This file deliberately reconstructs every quantity from the mathematical
definitions in squarefree_projection_proof.md.  It does not import any code or
data produced by the candidate proof.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path


Y = (
    110035772135,
    740330105, 146735985, 13116494, 1035439, 3968753,
    1018012, -940450, -1064478, -955415, -1042313,
    -602281, -81707, -2610548, 5600000, 6400000,
    0, -10197065, -10714482, 8444805, -288669517,
    392432875,
    -1128909059, -234438893, 0, -121779747,
)

CERTIFICATE_TERMS = (
    ((0, 0, 20, 1), 123896386),
    ((0, 0, 1, 20), 493811528),
    ((0, 0, 18, 3), 2327784),
    ((0, 1, 19, 1), 6224972),
    ((0, 0, 6, 15), 3177256),
    ((0, 0, 1, 3), 7935062),
    ((0, 0, 2, 19), 103186263),
    ((0, 1, 18, 1), 2716142),
    ((0, 0, 2, 18), 12296084),
    ((0, 0, 18, 2), 11324885),
    ((0, 1, 2, 18), 12961230),
    ((0, 0, 4, 17), 6525360),
    ((0, 0, 19, 1), 53337946),
    ((0, 0, 1, 19), 22809481),
    ((0, 1, 1, 19), 39120863),
    ((0, 0, 1, 2), 10573163),
    ((0, 1, 3, 0), 886175),
    ((0, 10, 11, 0), 121337),
)


def profiles():
    """Generate the raw set N in the exact lexicographic order used here."""
    for n0 in range(12):
        remaining = 21 - n0
        for n1 in range(remaining + 1):
            for n2 in range(remaining - n1 + 1):
                for n3 in range(remaining - n1 - n2 + 1):
                    n4 = remaining - n1 - n2 - n3
                    n = (n0, n1, n2, n3, n4)
                    if max(n) <= 20:
                        yield n


def scalar_image(n, scalar):
    out = [0] * 5
    for old_residue, multiplicity in enumerate(n):
        out[(scalar * old_residue) % 5] = multiplicity
    return tuple(out)


def canonical(n):
    return min(scalar_image(n, scalar) for scalar in range(1, 5))


def zero_subset_counts(n):
    # dp[k][r] counts k labelled positions with projected sum r.
    dp = [[0] * 5 for _ in range(22)]
    dp[0][0] = 1
    used = 0
    for residue, multiplicity in enumerate(n):
        nxt = [[0] * 5 for _ in range(22)]
        for old_k in range(used + 1):
            for old_r, old_count in enumerate(dp[old_k]):
                if not old_count:
                    continue
                for take in range(multiplicity + 1):
                    nxt[old_k + take][(old_r + residue * take) % 5] += (
                        old_count * math.comb(multiplicity, take)
                    )
        used += multiplicity
        dp = nxt
    return tuple(dp[k][0] for k in range(22))


def ap_count(n):
    # Choose a centre position, remove it, then choose an unordered endpoint
    # pair among the remaining positions with endpoint residues summing to
    # twice the centre residue.
    total = 0
    for centre_residue, centre_count in enumerate(n):
        if not centre_count:
            continue
        remaining = list(n)
        remaining[centre_residue] -= 1
        pairs = 0
        for a in range(5):
            for b in range(a, 5):
                if (a + b - 2 * centre_residue) % 5:
                    continue
                if a == b:
                    pairs += math.comb(remaining[a], 2)
                else:
                    pairs += remaining[a] * remaining[b]
        total += centre_count * pairs
    return total


@lru_cache(maxsize=None)
def local_allocations(group_size, targets):
    """Ways to place exceptional coefficient classes in one residue group."""
    ans = []
    ranges = [range(t + 1) for t in targets]
    group_fact = math.factorial(group_size)
    for ds in itertools.product(*ranges):
        placed = sum(ds)
        if placed > group_size:
            continue
        ways = group_fact // math.factorial(group_size - placed)
        for d in ds:
            ways //= math.factorial(d)
        ans.append((ds, ways))
    return tuple(ans)


def coefficient_assignment_count(n, c1234):
    counts = (21 - sum(c1234),) + tuple(c1234)
    assert min(counts) >= 0 and sum(counts) == 21
    base = max(range(5), key=lambda a: counts[a])
    exceptional_coeffs = tuple(a for a in range(5) if a != base and counts[a])
    targets = tuple(counts[a] for a in exceptional_coeffs)
    total_projection_sum = sum(j * n[j] for j in range(5)) % 5
    start_residue = base * total_projection_sum % 5
    zero_counts = (0,) * len(targets)
    dp = {(zero_counts, start_residue): 1}

    for projected_residue, group_size in enumerate(n):
        nxt = {}
        options = local_allocations(group_size, targets)
        for (used, old_mod), old_ways in dp.items():
            for ds, local_ways in options:
                new_used = tuple(used[i] + ds[i] for i in range(len(targets)))
                if any(new_used[i] > targets[i] for i in range(len(targets))):
                    continue
                delta = projected_residue * sum(
                    (exceptional_coeffs[i] - base) * ds[i]
                    for i in range(len(targets))
                )
                key = (new_used, (old_mod + delta) % 5)
                nxt[key] = nxt.get(key, 0) + old_ways * local_ways
        dp = nxt
    return dp.get((targets, 0), 0)


def features(n):
    z = zero_subset_counts(n)
    e = sum(math.comb(x, 2) for x in n)
    j = math.comb(n[0], 2)
    t = int(sum(residue * n[residue] for residue in range(5)) % 5 == 0)
    ap = ap_count(n)
    return z + (e, j, t, ap)


def multinomial_21(c1234):
    counts = (21 - sum(c1234),) + tuple(c1234)
    ans = math.factorial(21)
    for c in counts:
        ans //= math.factorial(c)
    return ans


def certificate_check():
    raw_profiles = list(profiles())
    orbit_reps = sorted({canonical(n) for n in raw_profiles})
    positive = []
    maximum = None
    maximum_profiles = []
    maximum_row = None
    layer_counts = [0] * 12
    row_hash = hashlib.sha256()
    r_min = [None] * len(CERTIFICATE_TERMS)
    r_max = [None] * len(CERTIFICATE_TERMS)

    # Deliberately recompute all 18 R_c values on every one of the 11,931 raw
    # profiles.  The 2,997 scalar orbits are counted only as a cross-check; no
    # orbit representative is used to skip a certificate row.
    for index, n in enumerate(raw_profiles, 1):
        f = features(n)
        r_values = tuple(
            coefficient_assignment_count(n, composition)
            for composition, _beta in CERTIFICATE_TERMS
        )
        p = sum(y * x for y, x in zip(Y, f)) + sum(
            beta * r for ((_composition, beta), r) in zip(CERTIFICATE_TERMS, r_values)
        )
        layer_counts[n[0]] += 1
        row_hash.update((",".join(map(str, n + f + r_values + (p,))) + "\n").encode("ascii"))
        for j, r in enumerate(r_values):
            r_min[j] = r if r_min[j] is None else min(r_min[j], r)
            r_max[j] = r if r_max[j] is None else max(r_max[j], r)
        if p > 0:
            positive.append((n, p))
        if maximum is None or p > maximum:
            maximum = p
            maximum_profiles = [n]
            maximum_row = {"profile": n, "features": f, "R_values": r_values, "P": p}
        elif p == maximum:
            maximum_profiles.append(n)
        if index % 500 == 0:
            print(f"computed_raw_profiles={index}/{len(raw_profiles)}", flush=True)

    b = tuple(
        31 * math.comb(21, k) + 125 * int(k == 0) for k in range(22)
    ) + (
        31 * math.comb(21, 2),
        6 * math.comb(21, 2),
        31,
        31 * 21 * math.comb(20, 2),
    )
    k_value = sum(y * x for y, x in zip(Y, b)) + 31 * sum(
        beta * multinomial_21(composition)
        for composition, beta in CERTIFICATE_TERMS
    )

    return {
        "raw_profile_count": len(raw_profiles),
        "raw_checked": len(raw_profiles),
        "R_values_recomputed": len(raw_profiles) * len(CERTIFICATE_TERMS),
        "orbit_count": len(orbit_reps),
        "layer_counts_n0_0_to_11": layer_counts,
        "certificate_term_count": len(CERTIFICATE_TERMS),
        "Y_length": len(Y),
        "positive_profile_count": len(positive),
        "first_positive_profiles": positive[:10],
        "maximum_P": maximum,
        "maximum_profiles": maximum_profiles[:20],
        "maximum_profile_count": len(maximum_profiles),
        "first_maximum_row": maximum_row,
        "R_minima_in_certificate_order": r_min,
        "R_maxima_in_certificate_order": r_max,
        "independent_row_encoding_sha256": row_hash.hexdigest(),
        "K": k_value,
        "Y_relations": {
            "125Y14": 125 * Y[14],
            "125Y15": 125 * Y[15],
            "Y16": Y[16],
        },
    }


def projective_functional_check():
    reps = []
    for v in itertools.product(range(5), repeat=4):
        if v == (0, 0, 0, 0):
            continue
        first = next(x for x in v if x)
        inverse = pow(first, -1, 5)
        normalized = tuple(inverse * x % 5 for x in v)
        if normalized == v:
            reps.append(v)
    vectors = [v for v in itertools.product(range(5), repeat=4) if any(v)]

    def dot(a, b):
        return sum(x * y for x, y in zip(a, b)) % 5

    kill_single = {sum(dot(lam, v) == 0 for lam in reps) for v in vectors}
    common_independent = set()
    independent_pairs = 0
    for i, v in enumerate(vectors):
        multiples = {tuple(a * x % 5 for x in v) for a in range(1, 5)}
        for w in vectors[i + 1:]:
            if w in multiples:
                continue
            independent_pairs += 1
            common_independent.add(
                sum(dot(lam, v) == 0 and dot(lam, w) == 0 for lam in reps)
            )
    return {
        "projective_functional_representatives": len(reps),
        "annihilators_of_nonzero_vector_values": sorted(kill_single),
        "independent_unordered_pair_count_checked": independent_pairs,
        "common_annihilator_values_for_independent_pairs": sorted(common_independent),
        "annihilators_of_zero_vector": len(reps),
    }


def deletion_and_exception_check():
    # Residue solution sets for the complete deletion equations (3).
    solutions = {}
    for n in range(17, 22):
        good = []
        for a, b, c in itertools.product(range(5), repeat=3):
            okay = True
            for q in range(17, n + 1):
                lhs = math.comb(n, q)
                lhs += math.comb(n - 14, q - 14) * a
                lhs -= math.comb(n - 15, q - 15) * b
                lhs += math.comb(n - 16, q - 16) * c
                if lhs % 5:
                    okay = False
                    break
            if okay:
                good.append((a, b, c))
        solutions[str(n)] = good

    exceptions = []
    for c in (0, 1):
        for b in range(5 - c):
            for a in range(100):
                if (1 + a - b + c) % 5:
                    continue
                if a + 4 * b + c < 9 or 2 * a + 3 * b - 3 * c < 13:
                    exceptions.append((a, b, c))
    return {
        "deletion_residue_solutions": solutions,
        "local_exception_triples": exceptions,
        "local_exception_count": len(exceptions),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_suffix(".json"))
    args = parser.parse_args()
    result = {
        "certificate": certificate_check(),
        "projective_geometry": projective_functional_check(),
        "finite_structural_checks": deletion_and_exception_check(),
    }
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
