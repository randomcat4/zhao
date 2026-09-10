#!/usr/bin/env python3
"""Exact checks for p_minus_four_unique_f3_tail_arithmetic.md.

The all-prime argument is the divisibility reduction in the proof.  This
script factors all fifteen fixed integers, checks the exact exceptional
type table, and probes the binomial congruence on primes through 5000.
It does not construct any actual tail, complement atom, or ROUTE-A4 model.
"""

from math import ceil, comb


ALLOWED_TYPES = tuple(
    (length, b)
    for length in (6, 7, 8)
    for b in range(1, length - 1)
)

EXPECTED = {
    11: ((7, 2),),
    13: ((6, 3), (8, 3)),
    19: ((6, 1), (8, 1)),
    23: ((6, 3), (8, 3)),
    43: ((7, 3),),
    101: ((6, 2), (8, 2)),
    233: ((7, 4),),
    467: ((7, 5),),
    701: ((6, 4), (8, 4)),
    1399: ((8, 5),),
    2521: ((8, 6),),
}


def is_prime(number):
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def factor_integer(number):
    number = abs(number)
    factors = []
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            factors.append(divisor)
            number //= divisor
        divisor += 1
    if number > 1:
        factors.append(number)
    assert all(is_prime(factor) for factor in factors)
    return tuple(factors)


def obstruction_integer(length, b):
    return 20 * ((-1) ** (length + b)) * comb(b + 3, 4) + 1


def exact_exception_table():
    table = {}
    factor_table = {}
    for length, b in ALLOWED_TYPES:
        value = obstruction_integer(length, b)
        factors = factor_integer(value)
        factor_table[(length, b)] = (value, factors)
        for prime in sorted(set(factors)):
            if prime >= 11:
                table.setdefault(prime, []).append((length, b))
    return (
        {prime: tuple(types) for prime, types in sorted(table.items())},
        factor_table,
    )


def verify_binomial_identity(prime, length, b):
    direct = comb(prime - 5, b - 1) % prime
    negative = ((-1) ** (b - 1) * comb(b + 3, 4)) % prime
    assert direct == negative

    left = ((-1) ** (length - 1) * direct) % prime
    target = (-pow(20, -1, prime)) % prime
    congruence_holds = left == target
    divides_fixed_integer = obstruction_integer(length, b) % prime == 0
    assert congruence_holds == divides_fixed_integer
    return congruence_holds


def verify_structural_subtables():
    two_point_types = sorted(
        (prime, length, b)
        for prime, types in EXPECTED.items()
        for length, b in types
        if length - b == 2
    )
    assert two_point_types == [
        (467, 7, 5),
        (701, 6, 4),
        (2521, 8, 6),
    ]

    # Every exceptional F1 core can be chosen disjoint from the unique F3
    # core.  The only possible F2 boundary failure is (p,b,b2)=(11,2,6).
    for prime, types in EXPECTED.items():
        m = prime - 4
        for _, b in types:
            assert b + 5 <= m
            bad_f2 = tuple(b2 for b2 in range(1, 7) if b + b2 > m)
            expected_bad = (6,) if (prime, b) == (11, 2) else ()
            assert bad_f2 == expected_bad


def verify_integer_tail_count_lift():
    contributions = tuple(
        (-1) ** (length + b) * comb(b + 3, 4)
        for length, b in ALLOWED_TYPES
    )
    assert max(abs(value) for value in contributions) == 126

    # If K tails occur, M=20*sum(c_U)+1 is a nonzero multiple of p and
    # |M|<=2520*K+1.  The dynamic check below independently confirms that
    # no smaller K can hit the required residue for the finite probe range.
    for prime in range(11, 5001):
        if not is_prime(prime):
            continue
        lower = ceil((prime - 1) / 2520)
        target = (-pow(20, -1, prime)) % prime
        reachable = {0}
        for count in range(lower):
            if count > 0:
                reachable = {
                    (old + contribution) % prime
                    for old in reachable
                    for contribution in contributions
                }
            assert target not in reachable


def main():
    table, factor_table = exact_exception_table()
    assert len(ALLOWED_TYPES) == 15
    assert table == EXPECTED

    for prime in range(11, 5001):
        if not is_prime(prime):
            continue
        surviving = tuple(
            tail_type
            for tail_type in ALLOWED_TYPES
            if verify_binomial_identity(prime, *tail_type)
        )
        assert surviving == EXPECTED.get(prime, ())

    verify_structural_subtables()
    verify_integer_tail_count_lift()

    print("PASS all 15 non-singleton positive-core F3 tail types")
    for tail_type in ALLOWED_TYPES:
        value, factors = factor_table[tail_type]
        print(f"  {tail_type}: {value} -> {factors}")
    print(f"PASS exact exceptional primes: {tuple(EXPECTED)}")
    print("PASS direct congruence probe for every prime 11 <= p <= 5000")
    print("PASS two-point and cross-family boundary subtables")
    print("PASS ordinary tail-count lift K >= ceil((p-1)/2520)")
    print("SCOPE necessary unique-tail arithmetic only; no exceptional type realized")


if __name__ == "__main__":
    main()
