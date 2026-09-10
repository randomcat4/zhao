#!/usr/bin/env python3
"""Exact arithmetic checks for the unique-tail position frontier.

This checks only finite arithmetic from the proof.  It does not construct a
labelled tail family or a complement atom.
"""

from __future__ import annotations

from math import ceil


EXCEPTION_TYPES = (
    (11, 7, 2),
    (13, 6, 3),
    (13, 8, 3),
    (19, 6, 1),
    (19, 8, 1),
    (23, 6, 3),
    (23, 8, 3),
    (43, 7, 3),
    (101, 6, 2),
    (101, 8, 2),
    (233, 7, 4),
    (467, 7, 5),
    (701, 6, 4),
    (701, 8, 4),
    (1399, 8, 5),
    (2521, 8, 6),
)

EXPECTED = {
    (11, 7, 2): (5, 5, 18),
    (13, 6, 3): (3, 2, 9),
    (13, 8, 3): (5, 2, 9),
    (19, 6, 1): (5, 1, 6),
    (19, 8, 1): (7, 1, 6),
    (23, 6, 3): (3, 8, 59),
    (23, 8, 3): (5, 8, 56),
    (43, 7, 3): (4, 15, 193),
    (101, 6, 2): (4, 5, 148),
    (101, 8, 2): (6, 5, 146),
    (233, 7, 4): (3, 35, 2355),
    (467, 7, 5): (2, 70, 9400),
    (701, 6, 4): (2, 35, 7040),
    (701, 8, 4): (4, 35, 7030),
    (1399, 8, 5): (3, 70, 28030),
    (2521, 8, 6): (2, 126, 90864),
}

EXPECTED_EXCLUDED = {
    (467, 7, 5),
    (701, 6, 4),
    (2521, 8, 6),
}


def fp(num: int, den: int, p: int) -> int:
    return (num * pow(den, -1, p)) % p


def least_abs(residue: int, p: int) -> int:
    residue %= p
    return min(residue, (-residue) % p)


def check_type(p: int, ell: int, b: int) -> tuple[int, int, int, bool]:
    r = ell - b
    assert 1 <= b <= 6 < p
    assert 2 <= r <= 7

    positive_zero = fp(1, 5 * b, p)
    h0_total = fp(-1, 5 * b, p)
    h0_contains_u = fp(-(b + 4), 20 * b, p)
    h0_avoids_u = fp(1, 20, p)
    h0_contains_y = fp(-1, 20, p)
    h0_avoids_y = fp(b - 4, 20 * b, p)

    assert (positive_zero + h0_total) % p == 0
    assert (h0_contains_u + h0_avoids_u) % p == h0_total
    assert (h0_contains_y + h0_avoids_y) % p == h0_total

    mu = least_abs(pow(20, -1, p), p)
    exterior_bound = ceil((2 * p + 8 - r) * mu / 7)
    omission_bound = ceil(r * mu / (r - 1))
    lower_bound = max(exterior_bound, omission_bound)

    excluded = False
    if r == 2 and b >= 4:
        # The atom argument forces every zero-core block to have U-trace
        # exactly one.  Total trace incidence would then equal total weight.
        trace_incidence = (r * h0_contains_u) % p
        discrepancy = (trace_incidence - h0_total) % p
        assert discrepancy == fp(-(b + 2), 10 * b, p)
        assert discrepancy != 0
        excluded = True

    return r, mu, lower_bound, excluded


def main() -> None:
    excluded = set()
    print("p ell b r mu actual_H0_lower excluded")
    for item in EXCEPTION_TYPES:
        r, mu, lower_bound, is_excluded = check_type(*item)
        assert (r, mu, lower_bound) == EXPECTED[item]
        if is_excluded:
            excluded.add(item)
        print(
            f"{item[0]:4d} {item[1]:3d} {item[2]:1d} {r:1d} "
            f"{mu:3d} {lower_bound:7d} {str(is_excluded):>8s}"
        )

    assert excluded == EXPECTED_EXCLUDED
    survivors = tuple(item for item in EXCEPTION_TYPES if item not in excluded)
    assert len(survivors) == 13
    print(f"EXCLUDED_TYPES={len(excluded)}")
    print(f"SURVIVING_TYPES={len(survivors)}")
    print("STATUS=EXACT_ARITHMETIC_CHECK_PASSED")
    print("SCOPE=actual-position consequences conditional on a frozen configuration")
    print("SCOPE=no labelled family or complement atom constructed")


if __name__ == "__main__":
    main()
