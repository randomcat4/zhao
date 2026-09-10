#!/usr/bin/env python3
"""Finite regression for p_minus_four_height_reduction.md."""

from __future__ import annotations

from itertools import combinations


LENGTH_TARGETS = {
    4: {0, 1},
    5: {0, 1},
    6: {0, 1, 2},
    7: {0, 1},
    8: {0},
}


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


def lies_in_translate(values, target, prime):
    return any(
        values <= {(shift + value) % prime for value in target}
        for shift in range(prime)
    )


def classified_two(values, multiplicities, length, prime):
    if multiplicities[0] > multiplicities[1]:
        major_value, minor_value = values
        minor_count = multiplicities[1]
    else:
        major_value, minor_value = values[::-1]
        minor_count = multiplicities[0]
    difference = (minor_value - major_value) % prime
    signed_size = min(difference, prime - difference)
    if length in (4, 5, 7):
        return minor_count == 1 and signed_size == 1
    if length == 6:
        return (
            (minor_count == 1 and signed_size in (1, 2))
            or (minor_count == 2 and signed_size == 1)
        )
    return False


def classified_three(values, multiplicities, length, prime):
    if length != 6 or sorted(multiplicities) != [1, 1, prime - 6]:
        return False
    center_index = multiplicities.index(prime - 6)
    center = values[center_index]
    outer = {
        values[index]
        for index in range(3)
        if index != center_index
    }
    return outer == {(center - 1) % prime, (center + 1) % prime}


def exhaustive_classification(prime):
    size = prime - 4
    totals = {}
    for length in (4, 5, 6, 7, 8):
        for choose in range(3, length):
            two_hits = 0
            for values in combinations(range(prime), 2):
                for first_count in range(1, size):
                    multiplicities = (first_count, size - first_count)
                    sums = subset_sums(values, multiplicities, choose, prime)
                    if lies_in_translate(sums, LENGTH_TARGETS[length], prime):
                        assert classified_two(
                            values, multiplicities, length, prime
                        )
                        two_hits += 1

            three_hits = 0
            for values in combinations(range(prime), 3):
                for first_count in range(1, size - 1):
                    for second_count in range(1, size - first_count):
                        multiplicities = (
                            first_count,
                            second_count,
                            size - first_count - second_count,
                        )
                        sums = subset_sums(
                            values, multiplicities, choose, prime
                        )
                        if lies_in_translate(
                            sums, LENGTH_TARGETS[length], prime
                        ):
                            assert classified_three(
                                values, multiplicities, length, prime
                            )
                            three_hits += 1

            if length == 8:
                assert two_hits == three_hits == 0
            if length in (4, 5, 7):
                assert two_hits > 0 and three_hits == 0
            if length == 6:
                assert two_hits > 0 and three_hits > 0
            totals[(length, choose)] = (two_hits, three_hits)
    return totals


def possible_families_for_fixed(prime, values, multiplicities, fixed_index):
    actual_targets = {
        2: {1},
        3: {1},
        4: {1, 2},
        5: {1, 2},
        6: {1, 2, 3},
        7: {2, 3},
        8: {3},
    }
    possible_families = set()
    for length, target in actual_targets.items():
        for choose in range(1, min(7, length - 1) + 1):
            all_sums = subset_sums(values, multiplicities, choose, prime)
            for shift in range(prime):
                shifted = {(shift + value) % prime for value in all_sums}
                if not shifted <= target:
                    continue
                remaining = list(multiplicities)
                remaining[fixed_index] -= 1
                fixed_sums = subset_sums(
                    values, tuple(remaining), choose - 1, prime
                )
                possible_families.update(
                    (shift + values[fixed_index] + value) % prime
                    for value in fixed_sums
                )
    return possible_families


def exceptional_family_check(prime):
    profiles = (
        ("single+1", (0, 1), (prime - 5, 1), 1),
        ("single-1", (0, -1), (prime - 5, 1), 3),
        ("single+2", (0, 2), (prime - 5, 1), 1),
        ("single-2", (0, -2), (prime - 5, 1), 3),
        ("double+1", (0, 1), (prime - 6, 2), 1),
        ("double-1", (0, -1), (prime - 6, 2), 3),
    )
    for name, values, multiplicities, forbidden_family in profiles:
        possible = possible_families_for_fixed(
            prime, values, multiplicities, 1
        )
        assert forbidden_family not in possible, (name, possible)

    values = (-1, 0, 1)
    multiplicities = (1, prime - 6, 1)
    negative = possible_families_for_fixed(prime, values, multiplicities, 0)
    positive = possible_families_for_fixed(prime, values, multiplicities, 2)
    assert 3 not in negative
    assert 1 not in positive


def p11_endpoint():
    prime = 11
    values = (0, 1)
    multiplicities = (3, 4)
    sums = subset_sums(values, multiplicities, 7, prime)
    assert sums == {4}
    assert lies_in_translate(sums, LENGTH_TARGETS[8], prime)


def main():
    totals = exhaustive_classification(13)
    exceptional_family_check(13)
    p11_endpoint()
    print(f"PASS p=13: {totals}")
    print("PASS: every nonmonochromatic p-4 profile has a missing-family point")
    print("PASS: p=11 length-eight full-core endpoint remains unclassified")
    print("SCOPE: finite regression; the p>=13 reduction is symbolic")


if __name__ == "__main__":
    main()
