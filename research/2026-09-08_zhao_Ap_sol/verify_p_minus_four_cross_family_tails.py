#!/usr/bin/env python3
"""Finite audits for p_minus_four_cross_family_tails.md.

The proof of existence and the exchange identities are symbolic.  This
script checks all core-count boundaries for primes 11 <= p <= 500 and checks
the formal three-tail interface assignment.  It does not construct the Hasse design,
a complement atom, or a ROUTE-A4 sequence.
"""

from __future__ import annotations

from fractions import Fraction


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


PRIMES = tuple(prime for prime in range(11, 501) if is_prime(prime))
ALLOWED_LENGTHS = {
    1: tuple(range(2, 7)),
    2: tuple(range(4, 8)),
    3: tuple(range(6, 9)),
}
POINT_DEGREES = {
    1: Fraction(-3, 4),
    2: Fraction(3, 10),
    3: Fraction(-1, 20),
}


def add(left, right, prime):
    return tuple((first + second) % prime for first, second in zip(left, right))


def sub(left, right, prime):
    return tuple((first - second) % prime for first, second in zip(left, right))


def scale(scalar, vector, prime):
    return tuple(scalar * value % prime for value in vector)


def residue(value: Fraction, prime: int) -> int:
    return value.numerator * pow(value.denominator, -1, prime) % prime


def feasible_core_intersections(m: int, b: int, bp: int):
    return tuple(range(max(0, b + bp - m), min(b, bp) + 1))


def verify_nonzero_point_degrees(prime: int) -> None:
    # Since prime >= 11, none of the displayed numerators or denominators
    # vanishes modulo prime.
    assert all(residue(value, prime) != 0 for value in POINT_DEGREES.values())


def verify_exchange_combinatorics(prime: int) -> None:
    m = prime - 4
    for family in (1, 2):
        for length in ALLOWED_LENGTHS[family]:
            for b in range(1, length):
                for length3 in ALLOWED_LENGTHS[3]:
                    for b3 in range(1, length3):
                        for k in feasible_core_intersections(m, b, b3):
                            union_core_size = b + b3 - k
                            assert union_core_size <= m
                            for alpha in range(b - k + 1):
                                for beta in range(b3 - k + 1):
                                    d = beta - alpha
                                    bstar = b3 - d
                                    direct_bstar = (
                                        k + (b3 - k - beta) + alpha
                                    )
                                    assert bstar == direct_bstar
                                    assert 0 <= bstar <= m

                                    usize = length - b
                                    u3size = length3 - b3
                                    for wsize in range(min(usize, u3size) + 1):
                                        rsize = usize - wsize
                                        ssize = u3size - wsize
                                        for esize in range(rsize + 1):
                                            for fsize in range(ssize + 1):
                                                direct_length = (
                                                    bstar
                                                    + wsize
                                                    + esize
                                                    + ssize
                                                    - fsize
                                                )
                                                formula_length = (
                                                    length3 - d + esize - fsize
                                                )
                                                assert direct_length == formula_length


def verify_automatic_cross_intersection_threshold(prime: int) -> None:
    m = prime - 4
    max_core = {family: max(ALLOWED_LENGTHS[family]) - 1 for family in (1, 2, 3)}
    if prime >= 17:
        assert max_core[1] + max_core[3] <= m
        assert max_core[2] + max_core[3] <= m
    else:
        assert prime in (11, 13)
        # At both exceptional boundary primes, the largest allowed cores can
        # no longer be chosen disjoint, so tail intersection is not automatic.
        assert max_core[1] + max_core[3] > m
        assert max_core[2] + max_core[3] > m


def verify_three_tail_local_state(prime: int) -> None:
    """Check the formal pair interface with one tail from each family."""
    m = prime - 4
    q = (1, 0, 0)
    x = (1, 0, 0, 0)
    zero = (0, 0, 0, 0)
    w = (0, 1, 0, 0)
    remainders = {
        family: ((-4) % prime, (-1) % prime, 0, family)
        for family in (1, 2, 3)
    }
    tails = {family: (w, remainders[family]) for family in (1, 2, 3)}

    b = 4
    length = 6
    assert b <= m and length in ALLOWED_LENGTHS[1]
    assert length in ALLOWED_LENGTHS[2] and length in ALLOWED_LENGTHS[3]

    for family, tail in tails.items():
        total = add(tail[0], tail[1], prime)
        assert total == ((-4) % prime, 0, 0, family)
        assert tail[0][:3] != (0, 0, 0)  # the common T-part
    assert len(set(remainders.values())) == 3

    # Distinct F3 blocks generated by the same F3 tail have nonzero quotient
    # intersection.  Core intersection four is the identical block boundary.
    f3_tail_quotient = add(w[:3], remainders[3][:3], prime)
    assert f3_tail_quotient == scale(-4, q, prime)
    for k in feasible_core_intersections(m, b, b):
        if k < b:
            assert add(f3_tail_quotient, scale(k, q, prime), prime) != (0, 0, 0)

    # Each mandatory lower-family/F3 pair has only its two endpoint exchanges.
    for family in (1, 2):
        r = remainders[family]
        s = remainders[3]
        hits = []
        for ebit in (0, 1):
            for fbit in (0, 1):
                e = r if ebit else zero
                f = s if fbit else zero
                quotient_difference = sub(e[:3], f[:3], prime)
                for d in range(-b, b + 1):
                    if quotient_difference != scale(d, q, prime):
                        continue
                    defect = sub(sub(e, f, prime), scale(d, x, prime), prime)
                    assert defect[:3] == (0, 0, 0)
                    delta = defect[3]
                    bstar = b - d
                    new_length = length - d + ebit - fbit
                    if (ebit, fbit) == (0, 0):
                        assert d == 0 and delta == 0
                        assert bstar == 4 and new_length == 6
                        new_family = 3
                    elif (ebit, fbit) == (1, 1):
                        assert d == 0 and delta == (family - 3) % prime
                        assert bstar == 4 and new_length == 6
                        new_family = family
                    else:
                        raise AssertionError("a proper exchange unexpectedly survived")
                    assert new_length in ALLOWED_LENGTHS[new_family]
                    hits.append((ebit, fbit, d, delta, new_family))
        assert hits == [
            (0, 0, 0, 0, 3),
            (1, 1, 0, (family - 3) % prime, family),
        ]

    # The repeated fibre value occurs exactly at its permitted cap; all three
    # exterior values are distinct actual values with quotient != q.
    assert m == prime - 4
    assert all(value[:3] != q for value in remainders.values())


def main() -> None:
    # The rational check is the all-prime proof behind the finite audit.
    assert {value.numerator for value in POINT_DEGREES.values()} == {-3, 3, -1}
    assert {value.denominator for value in POINT_DEGREES.values()} == {4, 10, 20}

    for prime in PRIMES:
        verify_nonzero_point_degrees(prime)
        verify_exchange_combinatorics(prime)
        verify_automatic_cross_intersection_threshold(prime)
        verify_three_tail_local_state(prime)

    print(f"PASS all {len(PRIMES)} primes 11 <= p <= 500")
    print("PASS nonzero three-family point-degree residues")
    print("PASS cross-family exchange core and length formulas")
    print("PASS p >= 17 automatic mandatory-tail intersections")
    print("PASS formal three-family pair-interface assignment")
    print("SCOPE no induced short-spectrum audit, Hasse realization, complement atom, or ROUTE-A4 model")


if __name__ == "__main__":
    main()
