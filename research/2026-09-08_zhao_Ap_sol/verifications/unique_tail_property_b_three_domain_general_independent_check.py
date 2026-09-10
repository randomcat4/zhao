#!/usr/bin/env python3
"""No-import audit of the three Property-B support domains.

This file deliberately does not import either production checker.  It rebuilds
the three support-domain unions from the three cases for the repeated label,
derives their line equations, enumerates the rational D1-D2 intersections, and
checks the exceptional characteristics and the separate p=233 capacity proof.
Reiher's external theorem is source-audited in the paired Markdown review.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import isqrt


Line = tuple[int, int, int]
Point = tuple[int, int]


# A*x+B*y+C=0.  These constants are independently derived in the review.
D1: tuple[Line, ...] = ((1, 0, 1), (-1, 1, -1), (-2, 1, 0), (-2, 1, -1))
D2: tuple[Line, ...] = ((0, 1, 1), (-1, 1, 1), (1, -2, 0), (1, -2, -1))
D3: tuple[Line, ...] = ((0, 1, -1), (1, 0, -1), (1, 1, 0), (1, 1, -1))


def prime_divisors(n: int) -> set[int]:
    n = abs(n)
    out: set[int] = set()
    q = 2
    while q <= isqrt(n):
        while n % q == 0:
            out.add(q)
            n //= q
        q += 1
    if n > 1:
        out.add(n)
    return out


def rational_intersection(left: Line, right: Line) -> tuple[Fraction, Fraction] | None:
    a, b, c = left
    d, e, f = right
    determinant = a * e - b * d
    if determinant == 0:
        return None
    return (Fraction(b * f - c * e, determinant), Fraction(c * d - a * f, determinant))


def value(line: Line, point: tuple[Fraction, Fraction]) -> Fraction:
    a, b, c = line
    x, y = point
    return a * x + b * y + c


def line_union(p: int, family: tuple[Line, ...]) -> set[Point]:
    return {
        (x, y)
        for x in range(p)
        for y in range(p)
        if (x, y) != (0, 0)
        and any((a * x + b * y + c) % p == 0 for a, b, c in family)
    }


def add(p: int, x: Point, y: Point) -> Point:
    return ((x[0] + y[0]) % p, (x[1] + y[1]) % p)


def scale(p: int, c: int, x: Point) -> Point:
    return ((c * x[0]) % p, (c * x[1]) % p)


def span(p: int, x: Point) -> set[Point]:
    return {scale(p, c, x) for c in range(p)}


def support_union_from_three_cases(p: int, a: Point, b: Point) -> set[Point]:
    """Union of {g} union L over the exhaustive three repeated-label cases."""
    out = {a} | {add(p, b, x) for x in span(p, a)}
    out |= {b} | {add(p, a, x) for x in span(p, b)}
    delta = ((b[0] - a[0]) % p, (b[1] - a[1]) % p)
    affine = {add(p, a, x) for x in span(p, delta)}
    for c in range(1, p):
        out |= {scale(p, c, delta)} | affine
    out.discard((0, 0))
    return out


def finite_geometry(p: int) -> dict[str, object]:
    e, f, w = (1, 0), (0, 1), ((-1) % p, (-1) % p)
    pairs = ((f, w), (e, w), (e, f))
    from_cases = [support_union_from_three_cases(p, *pair) for pair in pairs]
    from_lines = [line_union(p, family) for family in (D1, D2, D3)]
    assert from_cases == from_lines
    triple = set.intersection(*from_cases)
    return {
        "support_union_sizes": [len(x) for x in from_cases],
        "pair_intersection_sizes": [
            len(from_cases[0] & from_cases[1]),
            len(from_cases[0] & from_cases[2]),
            len(from_cases[1] & from_cases[2]),
        ],
        "triple_hits": [list(x) for x in sorted(triple)],
    }


def main() -> None:
    raw_points: list[tuple[Fraction, Fraction]] = []
    exceptional = set()
    parallel_pairs = 0
    for left in D1:
        for right in D2:
            determinant = left[0] * right[1] - left[1] * right[0]
            if determinant:
                exceptional |= prime_divisors(determinant)
            point = rational_intersection(left, right)
            if point is None:
                parallel_pairs += 1
            else:
                raw_points.append(point)

    candidates = sorted(set(raw_points))
    expected = {
        (Fraction(-1), Fraction(-1)),
        (Fraction(-1), Fraction(-2)),
        (Fraction(-1), Fraction(-1, 2)),
        (Fraction(-2), Fraction(-1)),
        (Fraction(-3), Fraction(-2)),
        (Fraction(-1, 2), Fraction(-1)),
        (Fraction(0), Fraction(0)),
        (Fraction(-1, 3), Fraction(-2, 3)),
        (Fraction(-2), Fraction(-3)),
        (Fraction(-2, 3), Fraction(-1, 3)),
    }
    assert set(candidates) == expected
    assert len(raw_points) == 15 and parallel_pairs == 1 and len(candidates) == 10

    for point in candidates:
        if point == (0, 0):
            continue
        for coordinate in point:
            exceptional |= prime_divisors(coordinate.denominator)
        for line in D3:
            residue = value(line, point)
            if residue:
                exceptional |= prime_divisors(residue.numerator)
                exceptional |= prime_divisors(residue.denominator)
    assert exceptional == {2, 3, 5}

    finite = {str(p): finite_geometry(p) for p in (2, 3, 5, 7, 11, 233)}
    assert [len(finite[str(p)]["triple_hits"]) for p in (2, 3, 5)] == [3, 5, 6]
    assert all(not finite[str(p)]["triple_hits"] for p in (7, 11, 233))
    assert finite["233"]["support_union_sizes"] == [926, 926, 926]
    assert finite["233"]["pair_intersection_sizes"] == [9, 9, 9]

    # Independent arithmetic for the weaker p=233 capacity/coset proof.
    p = 233
    atom_length = 2 * p - 1
    repeated_in_common_kernel = (p - 1) - 30
    assert atom_length == 465 and repeated_in_common_kernel == 202
    assert 3 * repeated_in_common_kernel == 606 > atom_length
    w1, w2, w3 = (1, 0), (0, 1), (p - 1, p - 1)
    determinant_rows = {
        "g1=g2=w3": ((w1[0] - w2[0]) * w3[1] - (w1[1] - w2[1]) * w3[0]) % p,
        "g1=g3=w2": ((w1[0] - w3[0]) * w2[1] - (w1[1] - w3[1]) * w2[0]) % p,
        "g2=g3=w1": ((w2[0] - w3[0]) * w1[1] - (w2[1] - w3[1]) * w1[0]) % p,
    }
    assert determinant_rows == {"g1=g2=w3": 231, "g1=g3=w2": 2, "g2=g3=w1": 231}

    core = {
        "schema": "unique_tail_property_b_three_domain_general/independent-audit-v1",
        "method": "fresh no-import reconstruction",
        "rational_D1_D2": {
            "raw_finite_intersections": len(raw_points),
            "parallel_pairs": parallel_pairs,
            "unique_candidates": [
                [str(point[0]), str(point[1])] for point in candidates
            ],
            "exceptional_characteristics": sorted(exceptional),
        },
        "finite_fields": finite,
        "p233_capacity_cross_check": {
            "atom_length": atom_length,
            "minimum_repeated_positions_in_K": repeated_in_common_kernel,
            "three_distinct_required": 3 * repeated_in_common_kernel,
            "parallel_coset_determinants": determinant_rows,
        },
        "conclusion": (
            "The three Property-B support domains have no common nonzero point "
            "for every prime p>=7; the separate p=233 capacity proof also checks."
        ),
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report = dict(core)
    report["certificate_sha256"] = sha256(canonical).hexdigest()
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
