#!/usr/bin/env python3
"""Audit the scalar system in p_minus_four_monochromatic_frontier.md."""

from __future__ import annotations

from fractions import Fraction
from math import comb


LENGTHS = {
    1: range(2, 7),
    2: range(4, 8),
    3: range(6, 9),
}

SPARSE_SOLUTION = {
    (1, 6, 1): Fraction(3, 4),
    (2, 6, 1): Fraction(6, 5),
    (2, 7, 2): Fraction(-3, 10),
    (3, 6, 1): Fraction(3, 10),
    (3, 7, 2): Fraction(-1, 5),
    (3, 8, 3): Fraction(1, 20),
}


def negative_binomial(positive_part, choose):
    """Return binom(-positive_part, choose)."""
    return Fraction((-1) ** choose * comb(positive_part + choose - 1, choose))


def indices():
    return [
        (family, length, x_count)
        for family, lengths in LENGTHS.items()
        for length in lengths
        for x_count in range(1, length)
    ]


def moments(solution):
    point = [Fraction(0) for _ in range(4)]
    pair = [Fraction(0) for _ in range(4)]
    triple = [Fraction(0) for _ in range(4)]
    for (family, length, x_count), value in solution.items():
        point[family] += (
            (-1) ** (length - 1)
            * negative_binomial(5, x_count - 1)
            * value
        )
        if x_count >= 2:
            pair[family] += (
                (-1) ** length
                * negative_binomial(6, x_count - 2)
                * value
            )
        if x_count >= 3:
            triple[family] += (
                (-1) ** (length - 1)
                * negative_binomial(7, x_count - 3)
                * value
            )
    return point, pair, triple


def audit_type_table():
    all_indices = indices()
    assert len(all_indices) == 51
    assert sum(x_count >= 3 for _, _, x_count in all_indices) == 28
    expected_high = {
        (family, length, x_count)
        for family, lengths in LENGTHS.items()
        for length in lengths
        for x_count in range(3, length)
    }
    assert len(expected_high) == 28

    singleton_tails = {
        index for index in all_indices if index[1] - index[2] == 1
    }
    assert len(singleton_tails) == 12
    assert all(
        length - x_count == 5
        for family, length, x_count in SPARSE_SOLUTION
    )


def audit_thresholds():
    vanished = {}
    for prime in (11, 13, 17, 19, 23):
        vanished[prime] = {
            index
            for index in indices()
            if index[1] - index[2] == 1
            and index[2] <= prime - 12
        }
    assert len(vanished[11]) == 0
    assert len(vanished[13]) == 1
    assert len(vanished[17]) == 9
    assert len(vanished[19]) == 12
    assert len(vanished[23]) == 12
    return {prime: len(values) for prime, values in vanished.items()}


def audit_sparse_solution():
    point, pair, triple = moments(SPARSE_SOLUTION)
    assert tuple(point[1:]) == (
        Fraction(-3, 4),
        Fraction(3, 10),
        Fraction(-1, 20),
    )
    assert 8 * pair[1] + 10 * pair[2] == 3
    assert 2 * pair[1] - 10 * pair[3] == 1
    assert 4 * triple[1] + 10 * triple[2] + 20 * triple[3] == -1
    assert tuple(pair[1:]) == (
        Fraction(0),
        Fraction(3, 10),
        Fraction(-1, 10),
    )
    assert tuple(triple[1:]) == (
        Fraction(0),
        Fraction(0),
        Fraction(-1, 20),
    )
    return point[1:], pair[1:], triple[1:]


def main():
    audit_type_table()
    thresholds = audit_thresholds()
    moments_value = audit_sparse_solution()
    print("PASS: 51 total variables and 28 triple-cover variables")
    print(f"PASS: singleton-tail vanish counts {thresholds}")
    print(f"PASS: sparse scalar solution moments {moments_value}")
    print(
        "SCOPE: algebraic Hasse compatibility only; no actual quotient-tail "
        "family is constructed"
    )


if __name__ == "__main__":
    main()
