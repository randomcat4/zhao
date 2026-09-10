#!/usr/bin/env python3
"""Exact checks for p_minus_four_star_design.md.

The computation verifies the binomial reductions and the sparse scalar
solution.  It does not construct actual tail subsets or a group-valued model.
"""

from fractions import Fraction
from math import comb


PRIMES = (11, 13, 17, 19, 23, 29, 31, 37, 41, 43)

ALLOWED_LENGTHS = {
    1: {2, 3, 4, 5, 6},
    2: {4, 5, 6, 7},
    3: {6, 7, 8},
}

Z = {
    (1, 1): Fraction(-7),
    (1, 2): Fraction(2),
    (1, 3): Fraction(-1, 4),
    (2, 1): Fraction(4, 5),
    (2, 2): Fraction(-1, 10),
    (3, 1): Fraction(-1, 20),
}

TYPE_FOR_Z = {
    (1, 1): (3, 1),
    (1, 2): (4, 2),
    (1, 3): (5, 3),
    (2, 1): (5, 1),
    (2, 2): (4, 2),
    (3, 1): (7, 1),
}


def residue(value, prime):
    return value.numerator * pow(value.denominator, -1, prime) % prime


def signed_power(exponent, prime):
    return 1 if exponent % 2 == 0 else prime - 1


def direct_degrees(prime):
    m = prime - 4
    point = [0, 0, 0, 0]
    pair = [0, 0, 0, 0]
    triple = [0, 0, 0, 0]

    for key, value in Z.items():
        family, b = key
        length, check_b = TYPE_FOR_Z[key]
        assert b == check_b
        assert length in ALLOWED_LENGTHS[family]
        assert 1 <= b <= length - 1 <= m
        count = residue(value, prime)
        assert 1 <= count < prime

        point[family] += (
            signed_power(length - 1, prime)
            * comb(m - 1, b - 1)
            * count
        )
        if b >= 2:
            pair[family] += (
                signed_power(length, prime)
                * comb(m - 2, b - 2)
                * count
            )
        if b >= 3:
            triple[family] += (
                signed_power(length - 1, prime)
                * comb(m - 3, b - 3)
                * count
            )

    return (
        tuple(value % prime for value in point[1:]),
        tuple(value % prime for value in pair[1:]),
        tuple(value % prime for value in triple[1:]),
    )


def verify_prime(prime):
    m = prime - 4

    for t in (1, 2, 3):
        for b in range(t, 8):
            left = comb(m - t, b - t) % prime
            right = (
                signed_power(b - t, prime)
                * comb(b + 3, t + 3)
            ) % prime
            assert left == right, (prime, t, b, left, right)

    point, pair, triple = direct_degrees(prime)
    expected_point = tuple(
        residue(value, prime)
        for value in (
            Fraction(-3, 4),
            Fraction(3, 10),
            Fraction(-1, 20),
        )
    )
    assert point == expected_point
    assert (8 * pair[0] + 10 * pair[1]) % prime == 3 % prime
    assert (2 * pair[0] - 10 * pair[2]) % prime == 1 % prime
    assert (
        4 * triple[0] + 10 * triple[1] + 20 * triple[2]
    ) % prime == (prime - 1) % prime

    return point, pair, triple


def feasible_core_overlaps(m, b, other_b):
    return tuple(
        range(max(0, b + other_b - m), min(b, other_b) + 1)
    )


def main():
    for prime in PRIMES:
        point, pair, triple = verify_prime(prime)
        print(
            f"PASS p={prime}: point={point}, pair={pair}, "
            f"triple={triple}"
        )

    counts_11 = tuple(
        residue(Z[key], 11)
        for key in (
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 1),
            (2, 2),
            (3, 1),
        )
    )
    assert counts_11 == (4, 2, 8, 3, 1, 6)

    # Boundary checks for the per-tail intersection rule.
    assert feasible_core_overlaps(15, 5, 7)[0] == 0
    assert feasible_core_overlaps(13, 7, 7)[0] == 1
    for b in (5, 6, 7):
        for other_b in (5, 6, 7):
            assert 0 in feasible_core_overlaps(15, b, other_b)

    print("PASS exact negative-binomial identities and scalar solution")
    print("PASS overlap-interval boundary checks")
    print("SCOPE no actual tail-set or group-valued realization is claimed")


if __name__ == "__main__":
    main()
