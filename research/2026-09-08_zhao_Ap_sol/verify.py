#!/usr/bin/env python3
"""Finite arithmetic checks for the 2026-09-08 A_p research notes.

This is not an A_p verifier.  It checks the explicit four-layer inverse,
the six-coefficient boundary and route-deduplication anchor sumsets for the
double-line corollary, and the formulas in the U_p pointwise-short-
representation counterexample.
"""

from fractions import Fraction
from math import comb


def primes_upto(n: int) -> list[int]:
    out: list[int] = []
    for k in range(2, n + 1):
        if all(k % q for q in out if q * q <= k):
            out.append(k)
    return out


def p_matrix(d: int) -> list[list[Fraction]]:
    return [
        [
            -Fraction((d - 2) * (d - 3) * (d - 4), 6),
            Fraction((d - 2) * (d - 3), 2),
            Fraction(2 - d),
            Fraction(1),
        ],
        [
            -Fraction((d - 1) * (d - 3) * (d - 4), 2),
            Fraction(3 * d * d - 13 * d + 12, 2),
            Fraction(5 - 3 * d),
            Fraction(3),
        ],
        [
            -Fraction((d - 1) * (d - 2) * (d - 4), 2),
            Fraction(3 * d * d - 11 * d + 8, 2),
            Fraction(4 - 3 * d),
            Fraction(3),
        ],
        [
            -Fraction((d - 1) * (d - 2) * (d - 3), 6),
            Fraction((d - 1) * (d - 2), 2),
            Fraction(1 - d),
            Fraction(1),
        ],
    ]


def mod_fraction(x: Fraction, p: int) -> int:
    return x.numerator * pow(x.denominator, -1, p) % p


def check_inverse(p: int, d: int) -> None:
    # H_q = sum_j B[q,j] n_j, after removing the empty representation.
    b = []
    for q in range(4):
        row = []
        for j in range(1, 5):
            k = 3 * p + j - d
            row.append(((-1) ** (k + q) * comb(k, q)) % p)
        b.append(row)
    pm = p_matrix(d)
    a = [
        [((-1) ** d * mod_fraction(pm[j][q], p)) % p for q in range(4)]
        for j in range(4)
    ]
    for i in range(4):
        for j in range(4):
            z = sum(a[i][q] * b[q][j] for q in range(4)) % p
            assert z == int(i == j), (p, d, i, j, z)


def check_double_line(p: int) -> None:
    for kappa in range(p):
        covered = {1 % p, 2 % p, 3 % p}
        covered |= {(kappa - j) % p for j in (1, 2, 3)}
        assert len(covered) <= 6 < p


def check_anchor_sumsets(p: int) -> None:
    available = set(range(p - 3))
    assert {(x + y) % p for x in available for y in available} == set(range(p))
    positive = set(range(1, p - 3))
    positive_sumset = {(x + y) % p for x in positive for y in positive}
    if p >= 11:
        assert positive_sumset == set(range(p))
    else:
        assert p == 7 and positive_sumset != set(range(p))


def check_up(p: int) -> None:
    assert p >= 29
    assert pow(8, 4, p) != 0
    candidates = []
    for ell in range(4):
        for k in range(p - 3):
            if (k + 2 * ell - (p - 4)) % p == 0:
                candidates.append((k + ell, k, ell))
    assert min(candidates) == (p - 7, p - 10, 3)
    assert 4 * (p - 7) > 3 * p - 2
    # The same family has a short zero-sum and therefore is not an A_p model.
    assert (p - 6) + 2 * 3 == p
    assert (p - 6) + 3 == p - 3


def check_type_witness(
    p: int, witness: tuple[Fraction, Fraction], special: list[tuple[Fraction, Fraction]]
) -> None:
    r0 = Fraction(1, 4)
    m, d = witness
    mm, dd = mod_fraction(m, p), mod_fraction(d, p)
    assert mm != mod_fraction(r0, p)  # cannot pair with an ordinary class
    assert dd != (mm - 1) % p  # cannot be a half-value class
    inverse = (dd, mm)
    types_mod = {(mod_fraction(x, p), mod_fraction(y, p)) for x, y in special}
    assert inverse not in types_mod


def check_route_b_types(p: int) -> None:
    # K_{2,n}: the Z type alone already has no possible reflection partner.
    k2n = [
        (Fraction(2), Fraction(9, 8)),
        (Fraction(-1, 4), Fraction(-3, 4)),
        (Fraction(-3, 2), Fraction(-1, 4)),
    ]
    check_type_witness(p, k2n[2], k2n)

    # Two-star cases: listed types are the complete special tables needed by
    # the selected obstructing Z or large-leaf class.
    z_regular = (Fraction(-3, 2), Fraction(-1, 4))
    check_type_witness(
        p,
        z_regular,
        [z_regular, (Fraction(1), Fraction(1, 2)), (Fraction(2), Fraction(-3, 4))],
    )
    z_exceptional = (Fraction(-5, 2), Fraction(-1, 4))
    check_type_witness(
        p,
        z_exceptional,
        [
            z_exceptional,
            (Fraction(1), Fraction(1, 2)),
            (Fraction(2), Fraction(-3, 4)),
            (Fraction(1), Fraction(9, 4)),
        ],
    )
    z_merged = (Fraction(-5, 2), Fraction(-3, 4))
    check_type_witness(
        p,
        z_merged,
        [z_merged, (Fraction(1), Fraction(1, 2)), (Fraction(2), Fraction(-3, 4))],
    )
    leaf_merged = (Fraction(-3, 2), Fraction(-3, 4))
    check_type_witness(
        p,
        leaf_merged,
        [
            leaf_merged,
            (Fraction(1), Fraction(1, 2)),
            (Fraction(1), Fraction(-1, 4)),
            (Fraction(1), Fraction(7, 4)),
        ],
    )


def main() -> None:
    ps = [p for p in primes_upto(500) if p >= 7]
    for p in ps:
        for d in range(5):
            check_inverse(p, d)
        check_double_line(p)
        check_anchor_sumsets(p)
    for p in (29, 31, 37, 101, 499):
        check_up(p)
    for p in [q for q in primes_upto(2000) if q >= 149]:
        check_route_b_types(p)
    print(
        "PASS: four-layer inverse for p<=500 and d=0..4; "
        "double-line six-coefficient bound and anchor-sumset deduplication; "
        "U_p formulas; route-B type tables"
    )


if __name__ == "__main__":
    main()
