#!/usr/bin/env python3
"""Regression checks for p_minus_two_residual_degree_system.md."""

from __future__ import annotations

from fractions import Fraction
from math import comb


LENGTH_TARGETS = {
    2: {1},
    3: {1},
    4: {1, 2},
    5: {1, 2},
    6: {1, 2, 3},
    7: {2, 3},
    8: {3},
}

CASES = (
    (11, "plus", (6, 2, 5)),
    (11, "minus", (8, 10, 3)),
    (19, "plus", (2, 7, 1)),
)

EXPECTED_K = {
    (11, "plus"): {"core": (7, 2, 5), "exception": (0, 8, 6)},
    (11, "minus"): {"core": (3, 10, 2), "exception": (8, 7, 0)},
    (19, "plus"): {"core": (7, 6, 1), "exception": (0, 10, 4)},
}

EXPECTED_RESIDUAL = {
    (11, "plus"): {"core": (9, 10, 0), "exception": (2, 5, 1)},
    (11, "minus"): {"core": (5, 7, 8), "exception": (10, 4, 6)},
    (19, "plus"): {"core": (11, 12, 0), "exception": (4, 16, 3)},
}


def residue(value, prime):
    if isinstance(value, int):
        return value % prime
    return value.numerator * pow(value.denominator, -1, prime) % prime


def known_point_counts(prime, orientation, m_values):
    multiplicities = dict(zip((3, 4, 5), m_values))
    output = {}
    for point_type in ("core", "exception"):
        counts = [0, 0, 0, 0]
        for block_x_count, number_of_tails in multiplicities.items():
            if point_type == "core":
                remaining_exceptions = 2
                remaining_cores = prime - 5
                already_exceptional = 0
            else:
                remaining_exceptions = 1
                remaining_cores = prime - 4
                already_exceptional = 1
            for added_exceptions in range(remaining_exceptions + 1):
                added_cores = block_x_count - 1 - added_exceptions
                if not 0 <= added_cores <= remaining_cores:
                    continue
                total_exceptions = already_exceptional + added_exceptions
                family = (
                    1 + total_exceptions
                    if orientation == "plus"
                    else 3 - total_exceptions
                )
                counts[family] += (
                    number_of_tails
                    * comb(remaining_exceptions, added_exceptions)
                    * comb(remaining_cores, added_cores)
                )
        output[point_type] = tuple(value % prime for value in counts[1:])
    return output


def allowed_singleton_types(prime, orientation):
    epsilon = 1 if orientation == "plus" else -1
    output = {}
    for length, targets in LENGTH_TARGETS.items():
        alignments = set()
        for core_family in range(prime):
            exception_family = (core_family + epsilon) % prime
            if core_family in targets and exception_family in targets:
                alignments.add((core_family, exception_family))
        if alignments:
            output[length] = alignments
    return output


def allowed_pair_types(prime, orientation):
    epsilon = 1 if orientation == "plus" else -1
    output = {}
    for length, targets in LENGTH_TARGETS.items():
        alignments = set()
        for shift in range(prime):
            triple = tuple((shift + j * epsilon) % prime for j in range(3))
            if set(triple) <= targets:
                alignments.add(triple)
        if alignments:
            output[length] = alignments
    return output


def main():
    delta = (Fraction(-3, 4), Fraction(3, 10), Fraction(-1, 20))
    for prime, orientation, m_values in CASES:
        counts = known_point_counts(prime, orientation, m_values)
        assert counts == EXPECTED_K[(prime, orientation)]
        target = tuple(residue(value, prime) for value in delta)
        residual = {
            point_type: tuple(
                (target[index] + values[index]) % prime
                for index in range(3)
            )
            for point_type, values in counts.items()
        }
        assert residual == EXPECTED_RESIDUAL[(prime, orientation)]

        singleton_types = allowed_singleton_types(prime, orientation)
        pair_types = allowed_pair_types(prime, orientation)
        if orientation == "plus":
            assert singleton_types == {
                4: {(1, 2)},
                5: {(1, 2)},
                6: {(1, 2), (2, 3)},
                7: {(2, 3)},
            }
            assert pair_types == {6: {(1, 2, 3)}}
            assert residual["exception"][0] != 0
        else:
            assert singleton_types == {
                4: {(2, 1)},
                5: {(2, 1)},
                6: {(2, 1), (3, 2)},
                7: {(3, 2)},
            }
            assert pair_types == {6: {(3, 2, 1)}}
            assert residual["exception"][2] != 0

        print(
            f"PASS p={prime} {orientation}: K={counts}, "
            f"residual={residual}"
        )

    # Exceptional-pair family support contradicts the two pair equations.
    for prime in (11, 19):
        assert 3 % prime != 0  # plus: d1=d2=0 contradicts 8d1+10d2=3
        assert 1 % prime != 0  # symmetric: d1=d3=0 contradicts 2d1-10d3=1
        # minus: 8d1=3 and 2d1=1 would imply 3=4.
        assert (3 - 4) % prime != 0

    print("PASS: exceptional-family supports contradict the pair identities")
    print("SCOPE: finite arithmetic checks the displayed residue tables only")


if __name__ == "__main__":
    main()
