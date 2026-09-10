#!/usr/bin/env python3
"""Finite audit for the short coordinate-pair template proof.

The proof itself is symbolic.  This script checks the allowed length table and
exhausts the support-two / support-three composition cases used in the finite
subset-sum lemma for all relevant primes through 101.
"""

from __future__ import annotations

from itertools import combinations


LENGTHS = {
    1: set(range(2, 7)),
    2: set(range(4, 8)),
    3: set(range(6, 9)),
}
EXPECTED = {
    1: {1},
    2: {1},
    3: {1, 2},
    4: {1, 2},
    5: {1, 2, 3},
    6: {2, 3},
    7: {3},
}


def is_prime(value: int) -> bool:
    return value >= 2 and all(
        value % divisor for divisor in range(2, int(value**0.5) + 1)
    )


def subset_sum_values(values, multiplicities, choose, prime):
    output = set()

    def visit(index, remaining, total):
        if index == len(values):
            if remaining == 0:
                output.add(total % prime)
            return
        for count in range(min(multiplicities[index], remaining) + 1):
            visit(index + 1, remaining - count, total + count * values[index])

    visit(0, choose, 0)
    return output


def audit_support_two(prime, choose, target_size):
    n = prime - 1
    checked = 0
    for first_count in range(1, n):
        multiplicities = (first_count, n - first_count)
        if max(multiplicities) > prime - 4:
            continue
        checked += 1
        sums = subset_sum_values((0, 1), multiplicities, choose, prime)
        assert len(sums) > target_size
    return checked


def audit_support_three_for_five(prime):
    n = prime - 1
    checked = 0
    for middle in range(2, prime):
        if middle == 1:
            continue
        for first_count in range(1, n - 1):
            for second_count in range(1, n - first_count):
                multiplicities = (
                    first_count,
                    second_count,
                    n - first_count - second_count,
                )
                if max(multiplicities) > prime - 4:
                    continue
                checked += 1
                sums = subset_sum_values(
                    (0, 1, middle), multiplicities, 5, prime
                )
                assert len(sums) > 3
    return checked


def main():
    observed = {
        k: {lam for lam, lengths in LENGTHS.items() if k + 1 in lengths}
        for k in range(1, 8)
    }
    assert observed == EXPECTED

    # For normalized k >= 8, enumerate every possible contribution to the
    # selected coordinate of a block containing three fixed B_{e_i} positions.
    for prime in [value for value in range(17, 102) if is_prime(value)]:
        for k in range(8, (prime - 1) // 2 + 1):
            for b_i in range(3, 9):
                for epsilon in range(2):
                    for gamma_plus in range(2):
                        for gamma_minus in range(2):
                            if b_i + epsilon + gamma_plus + gamma_minus > 8:
                                continue
                            coordinate = (
                                b_i + epsilon + k * gamma_plus - k * gamma_minus
                            )
                            assert coordinate % prime != 0

    totals = {"support_two": 0, "support_three_k5": 0}
    primes = [value for value in range(7, 102) if is_prime(value)]
    for prime in primes:
        for choose in (3, 4):
            totals["support_two"] += audit_support_two(prime, choose, 2)
        if prime >= 11:
            totals["support_two"] += audit_support_two(prime, 6, 2)
            totals["support_two"] += audit_support_two(prime, 5, 3)
            totals["support_three_k5"] += audit_support_three_for_five(prime)

    print("PASS: canonical block length table k=1,...,7 and k>=8 triple obstruction")
    print(
        "PASS: all normalized support-two and support-three composition cases "
        f"through p=101 ({totals})"
    )
    print("SCOPE: all nonzero coordinatewise amplitudes; no arbitrary-C claim")


if __name__ == "__main__":
    main()
