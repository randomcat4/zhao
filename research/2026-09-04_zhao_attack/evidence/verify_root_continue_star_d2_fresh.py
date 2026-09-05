"""Independent finite checks for proofs/root_continue_star_d2.md.

No code is imported from scripts/root_continue_star_d2.py.  The fixed core is
evaluated by multiplicity-count tuples with binomial weights, rather than by the
author's bit-mask loop.  Scalar interfaces are generated recursively before the
supplied JSON is read.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "verify_root_continue_star_d2_fresh.json"
POINTS = list(itertools.product(range(5), repeat=3))
ZERO = (0, 0, 0)
BASIS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
CORE_TYPES = (
    ((1, 0, 0), 1),
    ((1, 1, 0), 3),
    ((0, 1, 0), 3),
    ((1, 0, 1), 2),
    ((0, 0, 1), 2),
)


def add(a, b):
    return tuple((a[i] + b[i]) % 5 for i in range(3))


def neg(a):
    return tuple((-z) % 5 for z in a)


def scale(c, a):
    return tuple((c * z) % 5 for z in a)


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3)) % 5


def core_audit():
    distance = {t: 99 for t in POINTS}
    signed = Counter()
    nonempty_zeros = []
    represented_position_subsets = 0
    coefficient_patterns = 0

    for counts in itertools.product(*(range(mult + 1) for _, mult in CORE_TYPES)):
        coefficient_patterns += 1
        length = sum(counts)
        total = ZERO
        multiplicity = 1
        for count, (value, available) in zip(counts, CORE_TYPES):
            total = add(total, scale(count, value))
            multiplicity *= math.comb(available, count)
        represented_position_subsets += multiplicity
        distance[total] = min(distance[total], length)
        signed[total] += (-1 if length % 2 else 1) * multiplicity
        if length and total == ZERO:
            nonempty_zeros.append(counts)

    assert coefficient_patterns == 2 * 4 * 4 * 3 * 3 == 288
    assert represented_position_subsets == 2**11 == 2048
    assert not nonempty_zeros

    p = {t: signed[t] % 5 for t in POINTS}
    assert p[ZERO] == 1
    ell = tuple((p[e] - 1) % 5 for e in BASIS)
    assert ell == (3, 1, 1)
    assert all(p[t] == (1 + dot(ell, t)) % 5 for t in POINTS)

    sigma = ZERO
    for value, mult in CORE_TYPES:
        sigma = add(sigma, scale(mult, value))
    assert sigma == (1, 1, 4) and dot(ell, sigma) == 3

    missing = {t for t in POINTS if distance[t] == 99}
    e10 = {t for t in POINTS if distance[t] >= 10}
    e11 = {t for t in POINTS if distance[t] >= 11}
    fiber0 = {t for t in e10 if dot(ell, t) == 0}
    fiber3 = {t for t in e10 if dot(ell, t) == 3}
    expected_missing = {(0, 4, 0), (1, 2, 4), (2, 4, 4), (4, 2, 0)}
    expected_e10 = expected_missing | {(0, 1, 4), (1, 0, 4), (1, 1, 4)}
    assert missing == expected_missing
    assert e10 == expected_e10
    assert e11 == missing | {sigma}
    assert all(dot(ell, t) == 4 for t in missing)
    assert fiber0 == {(0, 1, 4)}
    assert fiber3 == {sigma}

    # The actual four-point M cannot have a four-point intersection with a
    # distinct translate.  The general proof uses the stronger orbit argument.
    intersection_sizes = {}
    for delta in POINTS:
        if delta == ZERO:
            continue
        shifted = {add(t, delta) for t in missing}
        intersection_sizes[delta] = len(missing & shifted)
        assert shifted != missing

    return {
        "coefficient_patterns": coefficient_patterns,
        "represented_position_subsets": represented_position_subsets,
        "sigma": sigma,
        "ell": ell,
        "missing": sorted(missing),
        "E10": sorted(e10),
        "E11_equals_M_union_sigma": True,
        "E10_fiber0": sorted(fiber0),
        "E10_fiber3": sorted(fiber3),
        "maximum_M_translate_intersection": max(intersection_sizes.values()),
        "distance_and_signed": [
            {"t": t, "d": distance[t], "P": p[t]} for t in POINTS
        ],
    }


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def bounded_choices(n, total=5):
    def rec(index, remaining, prefix):
        if index == len(n) - 1:
            if remaining <= n[index]:
                yield tuple(prefix + [remaining])
            return
        for value in range(min(n[index], remaining) + 1):
            yield from rec(index + 1, remaining - value, prefix + [value])

    yield from rec(0, total, [])


def varying_classes(n, repeat_class, k):
    return [
        c
        for c in range(5)
        if 0 < k[c] < n[c] and not (c == repeat_class and n[c] == 2)
    ]


def scalar_audit():
    count_vectors = list(compositions(9, 5))
    assert len(count_vectors) == 715 and len(set(count_vectors)) == 715
    interfaces = []
    for n in count_vectors:
        interfaces.append((n, -1))
        interfaces.extend((n, r) for r in range(5) if n[r] >= 2)
    assert len(interfaces) == 2365 and len(set(interfaces)) == 2365
    assert sum(r == -1 for _, r in interfaces) == 715
    assert sum(r != -1 for _, r in interfaces) == 1650

    independent_witnesses = {}
    availability = Counter()
    for n, repeat_class in interfaces:
        by_residue = {0: [], 2: []}
        for k in bounded_choices(n):
            residue = sum(c * k[c] for c in range(5)) % 5
            if residue in by_residue and varying_classes(n, repeat_class, k):
                by_residue[residue].append(k)
        available = tuple(r for r in (0, 2) if by_residue[r])
        assert available
        availability[str(available)] += 1
        chosen_residue = available[0]
        independent_witnesses[(n, repeat_class)] = (
            by_residue[chosen_residue][0],
            chosen_residue,
        )

    supplied = json.loads((ROOT / "evidence" / "root_continue_star_d2.json").read_text(encoding="utf-8"))
    rows = supplied["scalar_certificates"]
    lookup = {(tuple(row["n"]), row["repeat_class"]): row for row in rows}
    assert len(rows) == len(lookup) == 2365
    assert set(lookup) == set(interfaces)
    supplied_residues = Counter()
    for key, row in lookup.items():
        n, repeat_class = key
        k = tuple(row["k"])
        assert len(k) == 5 and sum(k) == 5
        assert all(0 <= k[c] <= n[c] for c in range(5))
        residue = sum(c * k[c] for c in range(5)) % 5
        assert residue == row["residue"] and residue in (0, 2)
        eligible = varying_classes(n, repeat_class, k)
        assert row["vary_class"] in eligible
        supplied_residues[residue] += 1

    return {
        "count_vectors": len(count_vectors),
        "distinct_interfaces": 715,
        "one_double_interfaces": 1650,
        "total_interfaces": len(interfaces),
        "independent_residue_availability": dict(availability),
        "supplied_residue_counts": dict(supplied_residues),
    }


def restricted_pair_sum_audit():
    # Translate the repeated value to zero and exhaust all unordered triples of
    # distinct nonzero b,c,d in F_5^3.
    nonzero = [t for t in POINTS if t != ZERO]
    minimum = 999
    attaining = 0
    triples = 0
    for b, c, d in itertools.combinations(nonzero, 3):
        triples += 1
        values = [ZERO, ZERO, b, c, d]
        sums = {
            add(values[i], values[j])
            for i in range(5)
            for j in range(i + 1, 5)
        }
        size = len(sums)
        if size < minimum:
            minimum = size
            attaining = 1
        elif size == minimum:
            attaining += 1
    assert triples == math.comb(124, 3)
    assert minimum >= 5
    return {
        "translated_distinct_triples_checked": triples,
        "minimum_restricted_pair_sum_size": minimum,
        "triples_attaining_minimum": attaining,
    }


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    core = core_audit()
    scalar = scalar_audit()
    pair_sums = restricted_pair_sum_audit()

    # Compare the independently computed core only after its assertions pass.
    supplied = json.loads((ROOT / "evidence" / "root_continue_star_d2.json").read_text(encoding="utf-8"))
    supplied_profile = {
        tuple(row["t"]): {"d": row["d"], "P": row["P"]}
        for row in supplied["distance_and_signed"]
    }
    own_profile = {tuple(row["t"]): {"d": row["d"], "P": row["P"]} for row in core["distance_and_signed"]}
    assert supplied_profile == own_profile
    assert tuple(supplied["sigma"]) == tuple(core["sigma"])
    assert tuple(supplied["ell"]) == tuple(core["ell"])
    assert {tuple(t) for t in supplied["missing"]} == set(map(tuple, core["missing"]))
    assert {tuple(t) for t in supplied["E10"]} == set(map(tuple, core["E10"]))
    assert {tuple(t) for t in supplied["E10_fiber_0"]} == set(map(tuple, core["E10_fiber0"]))
    assert {tuple(t) for t in supplied["E10_fiber_3"]} == set(map(tuple, core["E10_fiber3"]))

    result = {
        "status": "INDEPENDENT_FINITE_CHECKS_PASSED",
        "method": "binomially weighted core coefficient tuples plus independently generated bounded scalar compositions",
        "core_summary": {k: v for k, v in core.items() if k != "distance_and_signed"},
        "scalar_summary": scalar,
        "restricted_pair_sum_summary": pair_sums,
        "frozen_sha256": {
            "proofs/root_continue_star_d2.md": sha256(ROOT / "proofs" / "root_continue_star_d2.md"),
            "scripts/root_continue_star_d2.py": sha256(ROOT / "scripts" / "root_continue_star_d2.py"),
            "evidence/root_continue_star_d2.json": sha256(ROOT / "evidence" / "root_continue_star_d2.json"),
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
