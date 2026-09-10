#!/usr/bin/env python3
"""Exact geometry certificate for the three Property-B support domains.

This checker is deliberately independent of the p=233 exact-slice solver.  It
works first over Q, records every intersection of a line from D_1 with a line
from D_2, and determines the only characteristics in which a nonzero candidate
can also lie in D_3.  It then performs small finite-field spot checks, including
p=233.  The mathematical proof that Reiher's theorem applies is in the paired
Markdown file; this script certifies only the elementary support geometry.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path
from typing import Iterable


Line = tuple[int, int, int, str]


# A line (A,B,C,name) means A*x+B*y+C=0.
D1: tuple[Line, ...] = (
    (1, 0, 1, "x=-1"),
    (-1, 1, -1, "y=x+1"),
    (-2, 1, 0, "y=2x"),
    (-2, 1, -1, "y=2x+1"),
)
D2: tuple[Line, ...] = (
    (0, 1, 1, "y=-1"),
    (-1, 1, 1, "y=x-1"),
    (1, -2, 0, "x=2y"),
    (1, -2, -1, "x=2y+1"),
)
D3: tuple[Line, ...] = (
    (0, 1, -1, "y=1"),
    (1, 0, -1, "x=1"),
    (1, 1, 0, "x+y=0"),
    (1, 1, -1, "x+y=1"),
)


def prime_divisors(n: int) -> set[int]:
    n = abs(n)
    ans: set[int] = set()
    d = 2
    while d <= isqrt(n):
        while n % d == 0:
            ans.add(d)
            n //= d
        d += 1
    if n > 1:
        ans.add(n)
    return ans


def rational_intersection(l1: Line, l2: Line) -> tuple[Fraction, Fraction] | None:
    a, b, c, _ = l1
    d, e, f, _ = l2
    det = a * e - b * d
    if det == 0:
        return None
    return (Fraction(b * f - c * e, det), Fraction(c * d - a * f, det))


def line_value(line: Line, point: tuple[Fraction, Fraction]) -> Fraction:
    a, b, c, _ = line
    x, y = point
    return a * x + b * y + c


def fmt_fraction(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def fmt_point(point: tuple[Fraction, Fraction]) -> list[str]:
    return [fmt_fraction(point[0]), fmt_fraction(point[1])]


def mod_line_holds(line: Line, point: tuple[int, int], p: int) -> bool:
    a, b, c, _ = line
    x, y = point
    return (a * x + b * y + c) % p == 0


def domain_hits(p: int) -> list[list[int]]:
    hits: list[list[int]] = []
    for x in range(p):
        for y in range(p):
            if x == 0 and y == 0:
                continue
            point = (x, y)
            if (
                any(mod_line_holds(line, point, p) for line in D1)
                and any(mod_line_holds(line, point, p) for line in D2)
                and any(mod_line_holds(line, point, p) for line in D3)
            ):
                hits.append([x, y])
    return hits


def unique_preserving_order(items: Iterable[tuple[Fraction, Fraction]]) -> list[tuple[Fraction, Fraction]]:
    seen: set[tuple[Fraction, Fraction]] = set()
    ans: list[tuple[Fraction, Fraction]] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ans.append(item)
    return ans


def main() -> None:
    intersections = []
    raw_points = []
    determinant_exception_primes: set[int] = set()
    for left in D1:
        for right in D2:
            det = left[0] * right[1] - left[1] * right[0]
            if det != 0:
                determinant_exception_primes |= prime_divisors(det)
            point = rational_intersection(left, right)
            intersections.append(
                {
                    "d1_line": left[3],
                    "d2_line": right[3],
                    "point": None if point is None else fmt_point(point),
                }
            )
            if point is not None:
                raw_points.append(point)

    candidates = unique_preserving_order(raw_points)
    nonzero_exception_primes: set[int] = set(determinant_exception_primes)
    candidate_rows = []
    for point in candidates:
        is_origin = point == (Fraction(0), Fraction(0))
        values = [line_value(line, point) for line in D3]
        row_exception_primes: set[int] = set()
        for value in values:
            if value != 0:
                row_exception_primes |= prime_divisors(value.numerator)
                row_exception_primes |= prime_divisors(value.denominator)
        if not is_origin:
            nonzero_exception_primes |= row_exception_primes
        candidate_rows.append(
            {
                "point": fmt_point(point),
                "is_origin": is_origin,
                "d3_values": [fmt_fraction(value) for value in values],
                "possible_exception_primes": sorted(row_exception_primes),
            }
        )

    checks = {str(p): domain_hits(p) for p in (2, 3, 5, 7, 11, 233)}
    if any(checks[str(p)] for p in (7, 11, 233)):
        raise AssertionError("unexpected nonzero triple-domain hit in characteristic >= 7")
    if not checks["2"] or not checks["3"] or not checks["5"]:
        raise AssertionError("the advertised small-characteristic exception set is incomplete")
    if nonzero_exception_primes != {2, 3, 5}:
        raise AssertionError(nonzero_exception_primes)

    core = {
        "schema": "unique_tail_property_b_three_domain_general/v1",
        "scope": {
            "group": "C_p^2",
            "tail_normal_form": [[1, 0], [0, 1], [-1, -1]],
            "prime_range_proved_by_geometry": "p>=7",
            "property_b_input": "each maximal atom has a (p-1)-fold label",
        },
        "domain_lines": {
            "D(f,-e-f)": [line[3] for line in D1],
            "D(e,-e-f)": [line[3] for line in D2],
            "D(e,f)": [line[3] for line in D3],
        },
        "pairwise_line_intersections": intersections,
        "unique_rational_candidates": candidate_rows,
        "exceptional_characteristics": sorted(nonzero_exception_primes),
        "finite_field_triple_hits_excluding_origin": checks,
        "conclusion": (
            "For every prime p>=7 the three possible Property-B support domains "
            "have empty common nonzero intersection."
        ),
        "boundary": (
            "The script certifies the affine geometry only; invoking Property B "
            "uses Reiher's external theorem."
        ),
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report = dict(core)
    report["certificate_sha256"] = sha256(canonical).hexdigest()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    report_path = Path(__file__).with_name(
        "unique_tail_property_b_three_domain_general_report.json"
    )
    report_path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
