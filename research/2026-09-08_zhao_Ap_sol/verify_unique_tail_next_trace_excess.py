#!/usr/bin/env python3
"""Exact arithmetic checks for the unique-tail trace-excess theorem.

The script regenerates the exceptional types from the one-tail divisibility
condition.  It checks finite-field residues and integer lower bounds only; it
does not construct a labelled short-block family or a quotient atom.
"""

from __future__ import annotations

from math import comb


EXPECTED_SURVIVORS = {
    (11, 7, 2): (5, 5, 1, 18),
    (13, 6, 3): (3, 2, 6, 10),
    (13, 8, 3): (5, 2, 1, 9),
    (19, 6, 1): (5, 1, 2, 7),
    (19, 8, 1): (7, 1, 7, 7),
    (23, 6, 3): (3, 8, 7, 60),
    (23, 8, 3): (5, 8, 6, 57),
    (43, 7, 3): (4, 15, 9, 195),
    (101, 6, 2): (4, 5, 50, 155),
    (101, 8, 2): (6, 5, 21, 149),
    (233, 7, 4): (3, 35, 58, 2364),
    (701, 8, 4): (4, 35, 245, 7065),
    (1399, 8, 5): (3, 70, 322, 28076),
}


def fp(num: int, den: int, p: int) -> int:
    return (num * pow(den, -1, p)) % p


def least_abs(residue: int, p: int) -> int:
    residue %= p
    return min(residue, p - residue)


def ceil_div(num: int, den: int) -> int:
    return (num + den - 1) // den


def prime_factors(value: int) -> tuple[int, ...]:
    value = abs(value)
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        factors.append(value)
    return tuple(factors)


def regenerate_exception_types() -> tuple[tuple[int, int, int], ...]:
    types = set()
    for ell in (6, 7, 8):
        # Single-point tails have already been excluded, so b <= ell - 2.
        for b in range(1, ell - 1):
            obstruction = 20 * (-1) ** (ell + b) * comb(b + 3, 4) + 1
            for p in prime_factors(obstruction):
                if p >= 11:
                    types.add((p, ell, b))
    return tuple(sorted(types))


def check_type(p: int, ell: int, b: int) -> tuple[int, int, int, int, int]:
    r = ell - b
    mu = least_abs(fp(1, 20, p), p)

    total_weight = fp(-1, 5 * b, p)
    contains_u = fp(-(b + 4), 20 * b, p)
    avoids_u = fp(1, 20, p)
    delta = fp(4 - r * (b + 4), 20 * b, p)
    nu = least_abs(delta, p)

    assert (contains_u + avoids_u) % p == total_weight
    assert (r * contains_u - total_weight) % p == delta

    exterior_demand = (2 * p + 8 - r) * mu
    old_bound = max(
        ceil_div(exterior_demand, 7),
        ceil_div(r * mu, r - 1),
    )
    strengthened_bound = max(
        ceil_div(exterior_demand + nu, 7),
        ceil_div(r * mu, r - 1),
    )
    return r, mu, nu, old_bound, strengthened_bound


def main() -> None:
    exception_types = regenerate_exception_types()
    assert len(exception_types) == 16

    excluded = {
        item for item in exception_types if item[1] - item[2] == 2 and item[2] >= 4
    }
    assert excluded == {
        (467, 7, 5),
        (701, 6, 4),
        (2521, 8, 6),
    }

    survivors = tuple(item for item in exception_types if item not in excluded)
    assert set(survivors) == set(EXPECTED_SURVIVORS)

    strict_improvements = 0
    print("p ell b r mu nu old_H0 new_H0 gain")
    for item in survivors:
        r, mu, nu, old_bound, new_bound = check_type(*item)
        assert (r, mu, nu, new_bound) == EXPECTED_SURVIVORS[item]
        gain = new_bound - old_bound
        strict_improvements += gain > 0
        print(
            f"{item[0]:4d} {item[1]:3d} {item[2]:1d} {r:1d} "
            f"{mu:3d} {nu:3d} {old_bound:7d} {new_bound:7d} {gain:4d}"
        )

    assert strict_improvements == 11

    trace_rows = []
    for p, ell, b in survivors:
        r, mu, nu, _, new_bound = check_type(p, ell, b)
        if b < 4:
            continue
        multi_trace = ceil_div(nu, r - 2)
        if r == 3:
            trace_one = least_abs(fp(3 * b + 4, 20 * b, p), p)
            trace_two = least_abs(fp(-(3 * b + 8), 20 * b, p), p)
            assert trace_two == nu
            exterior_pairs = ceil_div(trace_one * mu, 2)
        else:
            trace_one = 0
            trace_two = 0
            exterior_pairs = 0
        trace_rows.append(
            (p, ell, b, new_bound, multi_trace, trace_one, trace_two, exterior_pairs)
        )

    assert trace_rows == [
        (233, 7, 4, 2364, 58, 93, 58, 1628),
        (701, 8, 4, 7065, 123, 0, 0, 0),
        (1399, 8, 5, 28076, 322, 266, 322, 9310),
    ]

    print("STRICTLY_IMPROVED_SURVIVORS=11")
    print("TRACE_ROWS")
    for row in trace_rows:
        print(row)
    print("STATUS=EXACT_TRACE_EXCESS_ARITHMETIC_PASSED")
    print("SCOPE=no labelled family, induced spectrum, or quotient atom constructed")


if __name__ == "__main__":
    main()
