#!/usr/bin/env python3
"""Exact finite checks for the p=13 unique-tail labelled reduction.

This script audits only the coefficient tables and symmetry-cover counts in
proofs/p13_unique_tail_labelled_attack.md.  It is not a labelled Y-instance
solver and does not claim to exclude either surviving p=13 type.
"""

from __future__ import annotations

import itertools


P = 13


def singleton_axis_survivors(remainder_size: int) -> tuple[int, ...]:
    """Axial coefficients alpha left by the two automatic-block tests."""
    survivors = []
    for alpha in range(P):
        core = (-alpha) % P
        if core == 0:
            # A quotient-zero singleton would lie on H.
            continue
        if 1 <= core <= 6:
            # X_core + {u} is a length 2..7 transversal, contradicting an
            # F3 block that avoids u.
            continue
        if core == 7:
            # A new positive-core length-eight F3 tail.
            continue
        if 8 <= core <= 9:
            # Forbidden lengths nine and ten.
            continue

        assert core in (10, 11, 12)
        complement_core = 3 + alpha
        complement_length = remainder_size - 1 + complement_core
        if complement_length == 8:
            # A new positive-core length-eight F3 tail.
            continue
        if 9 <= complement_length <= 2 * P + 2:
            continue
        assert complement_length in (6, 7)
        survivors.append(alpha)
    return tuple(survivors)


def canonical_rank_one_triple(values: tuple[int, int, int]) -> tuple[int, ...]:
    orbit = []
    for scalar in range(1, P):
        orbit.append(tuple(sorted((scalar * value) % P for value in values)))
    return min(orbit)


def rank_one_projection_orbits() -> tuple[tuple[int, ...], ...]:
    representatives = set()
    for values in itertools.combinations_with_replacement(range(1, P), 3):
        if sum(values) % P == 0:
            representatives.add(canonical_rank_one_triple(values))
    return tuple(sorted(representatives))


def determinant(left: tuple[int, int], right: tuple[int, int]) -> int:
    return (left[0] * right[1] - left[1] * right[0]) % P


def audit_rank_two_projection() -> int:
    """Check every independent pair gives the single standard atom orbit."""
    vectors = [
        (x, y)
        for x in range(P)
        for y in range(P)
        if (x, y) != (0, 0)
    ]
    checked = 0
    for left in vectors:
        for right in vectors:
            det = determinant(left, right)
            if det == 0:
                continue
            inverse_det = pow(det, -1, P)

            # The inverse of the matrix with columns left,right sends them to
            # e1,e2 and therefore sends -left-right to -e1-e2.
            def normalize(value: tuple[int, int]) -> tuple[int, int]:
                return (
                    (right[1] * value[0] - right[0] * value[1])
                    * inverse_det
                    % P,
                    (-left[1] * value[0] + left[0] * value[1])
                    * inverse_det
                    % P,
                )

            third = ((-left[0] - right[0]) % P,
                     (-left[1] - right[1]) % P)
            assert normalize(left) == (1, 0)
            assert normalize(right) == (0, 1)
            assert normalize(third) == (P - 1, P - 1)
            checked += 1
    return checked


def component_status(size: int, core: int) -> str:
    if core > P - 4:
        return "unavailable"
    length = size + core
    if length <= 7:
        return "short"
    if length == 8:
        return "new_positive_f3"
    if length <= 2 * P + 2:
        return "forbidden_length"
    raise AssertionError((size, core, length))


def decomposable_five_tail_table():
    rows = []
    allowed = []
    for coefficient in range(P):
        other = (3 - coefficient) % P
        pair_status = component_status(2, coefficient)
        triple_status = component_status(3, other)
        rejected = (
            pair_status in ("new_positive_f3", "forbidden_length")
            or triple_status in ("new_positive_f3", "forbidden_length")
        )
        if not rejected:
            allowed.append(coefficient)
        forced_sides = tuple(
            side
            for side, status in (("P", pair_status), ("Q", triple_status))
            if status == "short"
        )
        rows.append(
            (coefficient, other, pair_status, triple_status, forced_sides)
        )
    return tuple(allowed), tuple(rows)


def main() -> None:
    assert singleton_axis_survivors(3) == (1, 2)
    assert singleton_axis_survivors(5) == ()

    rank_one = rank_one_projection_orbits()
    expected_rank_one = ((1, 1, 11), (1, 2, 10), (1, 3, 9))
    assert rank_one == expected_rank_one
    rank_two_checks = audit_rank_two_projection()
    assert rank_two_checks == 168 * 156

    quotient_template_bound = 1 + len(rank_one) * P + 2
    actual_template_bound = 1 + len(rank_one) * P * P + 2 * P
    assert quotient_template_bound == 42
    assert actual_template_bound == 534

    allowed, rows = decomposable_five_tail_table()
    assert allowed == (0, 1, 2, 3, 4, 5, 12)
    forced = {row[0]: row[4] for row in rows if row[0] in allowed}
    assert all(forced[c] == ("P", "Q") for c in range(4))
    assert forced[4] == forced[5] == ("P",)
    assert forced[12] == ("Q",)

    print("PASS singleton-axis coefficients: r=3 -> {1,2}, r=5 -> empty")
    print(f"PASS projected atom normal forms: rank-1={rank_one}, rank-2=1")
    print(
        "PASS symmetry-cover bounds: "
        f"quotient={quotient_template_bound}, actual-tail={actual_template_bound}"
    )
    print(f"PASS decomposable r=5 coefficients: {allowed}")
    print("SCOPE: PROVED_REDUCTION only; neither p=13 tail type is excluded")


if __name__ == "__main__":
    main()
