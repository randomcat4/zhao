#!/usr/bin/env python3
"""Exact arithmetic for proofs/p_minus_four_single_height_probe.md.

This checks the pure-X Hasse moment model and all singleton-anchor bounds.  It
does not check mixed Hasse equations or construct quotient labels,
intersecting remainder families, or an atom.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb


def is_prime(value: int) -> bool:
    return value >= 2 and all(
        value % divisor for divisor in range(2, int(value**0.5) + 1)
    )


def negative_binomial(c: int, degree: int) -> int:
    """Return binom(-c, degree)."""
    return (-1) ** degree * comb(c + degree - 1, degree)


MODEL = {
    # (family, length, X-intersection): rational count
    (1, 5, 1): Fraction(-9, 2),
    (1, 5, 2): Fraction(-3, 2),
    (1, 5, 3): Fraction(-1, 4),
    (2, 6, 1): Fraction(6, 5),
    (2, 6, 2): Fraction(3, 10),
    (3, 7, 1): Fraction(9, 20),
    (3, 7, 2): Fraction(1, 10),
}


def moment(family: int, fixed: int, pair_sign: bool = False) -> Fraction:
    total = Fraction(0)
    for (lam, length, b), count in MODEL.items():
        if lam != family or b < fixed:
            continue
        sign_exponent = length if pair_sign else length - 1
        coefficient = (
            (-1) ** sign_exponent
            * negative_binomial(4 + fixed, b - fixed)
        )
        total += coefficient * count
    return total


def audit_moment_model() -> None:
    point = tuple(moment(family, 1) for family in (1, 2, 3))
    assert point == (
        Fraction(-3, 4),
        Fraction(3, 10),
        Fraction(-1, 20),
    )

    pair = tuple(
        moment(family, 2, pair_sign=True) for family in (1, 2, 3)
    )
    assert pair == (Fraction(0), Fraction(3, 10), Fraction(-1, 10))
    assert 8 * pair[0] + 10 * pair[1] == 3
    assert 2 * pair[0] - 10 * pair[2] == 1

    triple = tuple(moment(family, 3) for family in (1, 2, 3))
    assert triple == (Fraction(-1, 4), Fraction(0), Fraction(0))
    assert 4 * triple[0] + 10 * triple[1] + 20 * triple[2] == -1

    assert all(length - b >= 2 for (_, length, b) in MODEL)


def anchor_resources(prime: int, b: int, family: int, copies: int):
    x_positions = (-copies * b) % prime
    anchors = (copies * family - 3) % prime
    feasible = x_positions <= prime - 4 and anchors <= prime - 4
    return feasible, x_positions, anchors


def first_closing_copy_count(prime: int, b: int, family: int):
    for copies in range(1, 9):
        feasible, x_positions, anchors = anchor_resources(
            prime, b, family, copies
        )
        if feasible and x_positions + anchors > 0:
            return copies, x_positions, anchors
    return None


def audit_singleton_bounds() -> int:
    checked = 0
    primes = [p for p in range(11, 1000) if is_prime(p)]
    for prime in primes:
        expected_f1 = {
            1: 4,
            2: 3,
            3: 3,
            4: 4 if prime == 11 else 3,
            5: 4 if prime == 13 else 3,
        }
        expected_f2 = {
            3: 2,
            4: 2,
            5: 2,
            6: 3 if prime == 11 else 2,
        }
        expected_f3 = {5: 1, 6: 1, 7: 1}
        for family, expected in (
            (1, expected_f1),
            (2, expected_f2),
            (3, expected_f3),
        ):
            for b, copies in expected.items():
                result = first_closing_copy_count(prime, b, family)
                assert result is not None
                assert result[0] == copies, (prime, family, b, result)
                assert result[1] <= prime - 4
                assert result[2] <= prime - 4
                checked += 1
    return checked


def audit_pure_t_f3() -> int:
    checked = 0
    for prime in [p for p in range(11, 1000) if is_prime(p)]:
        for b in (4, 5, 6, 7):
            feasible, x_positions, anchors = anchor_resources(prime, b, 3, 1)
            assert feasible
            assert x_positions == prime - b
            assert anchors == 0
            checked += 1
        feasible, x_positions, anchors = anchor_resources(prime, 3, 3, 2)
        assert feasible
        assert x_positions == prime - 6
        assert anchors == 3
        checked += 1
    return checked


def audit_integer_representatives() -> int:
    checked = 0
    for prime in [p for p in range(11, 1000) if is_prime(p)]:
        for value in MODEL.values():
            representative = (
                value.numerator * pow(value.denominator, -1, prime)
            ) % prime
            assert 0 <= representative <= prime - 1
            if value:
                assert representative != 0
            checked += 1
    return checked


def main() -> None:
    audit_moment_model()
    singleton_cases = audit_singleton_bounds()
    pure_t_cases = audit_pure_t_f3()
    representative_cases = audit_integer_representatives()
    print(
        "PASS p-4 single-height probe: "
        f"singleton bounds={singleton_cases}, "
        f"pure-T F3 cases={pure_t_cases}, "
        f"moment representatives={representative_cases}"
    )
    print(
        "SCOPE: the rational model certifies Hasse-level compatibility only; "
        "it is not a labelled atom or remainder hypergraph"
    )


if __name__ == "__main__":
    main()
