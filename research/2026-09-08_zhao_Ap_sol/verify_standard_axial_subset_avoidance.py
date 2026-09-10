#!/usr/bin/env python3
"""Finite regression for standard_atom_axial_subset_avoidance.md."""

from __future__ import annotations


LENGTH_TARGETS = {
    2: {1},
    3: {1},
    4: {1, 2},
    5: {1, 2},
    6: {1, 2, 3},
    7: {2, 3},
    8: {3},
}
EXCEPTIONS = {(1, 1), (1, 2), (1, 3), (2, 2)}


def is_prime(value):
    return value >= 2 and all(
        value % divisor for divisor in range(2, int(value**0.5) + 1)
    )


def subset_sums(values, multiplicities, choose, prime):
    output = set()

    def visit(index, remaining, total):
        if index == len(values):
            if remaining == 0:
                output.add(total % prime)
            return
        for count in range(min(remaining, multiplicities[index]) + 1):
            visit(index + 1, remaining - count, total + count * values[index])

    visit(0, choose, 0)
    return output


def predicted_exception(t, k):
    length = t + 6 - k
    target_count = len(LENGTH_TARGETS[length])
    if target_count == 1:
        return False
    if target_count == 2:
        return t == 1
    assert target_count == 3
    return t <= 2


def audit_table():
    observed = set()
    for k in range(1, 6):
        for t in range(1, min(7, k + 2) + 1):
            if predicted_exception(t, k):
                observed.add((t, k))
    assert observed == EXCEPTIONS


def audit_small_support(prime):
    n = prime - 1
    checked = 0
    for choose in range(2, 8):
        if n < choose + 2:
            continue
        for first in range(3, n - 2):
            multiplicities = (first, n - first)
            if max(multiplicities) > prime - 4:
                continue
            checked += 1
            assert len(subset_sums((0, 1), multiplicities, choose, prime)) >= 3

    for choose in (3, 4, 5):
        for third_value in range(2, prime):
            for first in range(1, n - 1):
                for second in range(1, n - first):
                    multiplicities = (first, second, n - first - second)
                    if max(multiplicities) > prime - 4:
                        continue
                    checked += 1
                    assert len(
                        subset_sums(
                            (0, 1, third_value), multiplicities, choose, prime
                        )
                    ) >= 4
    return checked


def main():
    audit_table()
    total = 0
    primes = [value for value in range(11, 54) if is_prime(value)]
    for prime in primes:
        total += audit_small_support(prime)
    print(f"PASS: exact (t,k) exception table {sorted(EXCEPTIONS)}")
    print(f"PASS: {total} normalized support cases for primes 11 <= p <= 53")
    print("SCOPE: finite regression; the arbitrary-C avoidance proof is symbolic")


if __name__ == "__main__":
    main()
