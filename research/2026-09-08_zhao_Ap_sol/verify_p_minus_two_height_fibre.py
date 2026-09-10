#!/usr/bin/env python3
"""Audit the p-2 height-fibre classification and triple-codegree systems.

The finite searches are regression tests.  The all-prime conclusions are
proved symbolically in proofs/p_minus_two_height_fibre.md.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


WEIGHTS = {1: 4, 2: 10, 3: 20}


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
        for count in range(min(multiplicities[index], remaining) + 1):
            visit(
                index + 1,
                remaining - count,
                total + count * values[index],
            )

    visit(0, choose, 0)
    return output


def lies_in_cyclic_triple(values, prime):
    return any(
        values <= {start, (start + 1) % prime, (start + 2) % prime}
        for start in range(prime)
    )


def classified_support_two(values, multiplicities, prime):
    first, second = values
    first_count, second_count = multiplicities
    if first_count == prime - 4 and second_count == 2:
        return (second - first) % prime in (1, prime - 1)
    if second_count == prime - 4 and first_count == 2:
        return (first - second) % prime in (1, prime - 1)
    return False


def classified_support_three(values, multiplicities, prime):
    if sorted(multiplicities) != [1, 1, prime - 4]:
        return False
    center_index = multiplicities.index(prime - 4)
    center = values[center_index]
    outer = {
        values[index]
        for index in range(3)
        if index != center_index
    }
    return outer == {(center - 1) % prime, (center + 1) % prime}


def exhaustive_classification(prime):
    size = prime - 2
    cap = prime - 4
    totals = {}
    for choose in (3, 4, 5):
        support_two_hits = 0
        for values in combinations(range(prime), 2):
            for first_count in range(2, size - 1):
                multiplicities = (first_count, size - first_count)
                if max(multiplicities) > cap:
                    continue
                sums = subset_sums(values, multiplicities, choose, prime)
                if lies_in_cyclic_triple(sums, prime):
                    assert classified_support_two(
                        values, multiplicities, prime
                    )
                    support_two_hits += 1

        support_three_hits = 0
        for values in combinations(range(prime), 3):
            for first_count in range(1, size - 1):
                for second_count in range(1, size - first_count):
                    multiplicities = (
                        first_count,
                        second_count,
                        size - first_count - second_count,
                    )
                    if max(multiplicities) > cap:
                        continue
                    sums = subset_sums(values, multiplicities, choose, prime)
                    if lies_in_cyclic_triple(sums, prime):
                        assert classified_support_three(
                            values, multiplicities, prime
                        )
                        support_three_hits += 1

        assert support_two_hits == 2 * prime
        assert support_three_hits == prime
        totals[choose] = (support_two_hits, support_three_hits)
    return totals


def determinant(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def solve_three_by_three(matrix):
    augmented = [
        [Fraction(value) for value in row] + [Fraction(1)]
        for row in matrix
    ]
    for column in range(3):
        pivot = next(
            row for row in range(column, 3) if augmented[row][column]
        )
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(3):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                augmented[row][index] - scale * augmented[column][index]
                for index in range(4)
            ]
    return tuple(augmented[index][3] for index in range(3))


def coefficient_matrices():
    plus = (
        (4, -8, -8),
        (10, -40, 90),
        (20, -100, 300),
    )
    minus = (
        (20, -120, 424),
        (10, -56, 186),
        (4, -20, 60),
    )
    symmetric = (
        (10, -46, 122),
        (20, -110, 360),
        (4, -14, 24),
        (10, -50, 150),
    )
    return plus, minus, symmetric


def audit_linear_systems():
    plus, minus, symmetric = coefficient_matrices()
    assert determinant(plus) == -800
    assert determinant(minus) == 96
    assert determinant(symmetric[:3]) == -640
    plus_solution = solve_three_by_three(plus)
    minus_solution = solve_three_by_three(minus)
    symmetric_solution = solve_three_by_three(symmetric[:3])
    assert plus_solution == (
        Fraction(21, 20),
        Fraction(7, 20),
        Fraction(1, 20),
    )
    assert minus_solution == (
        Fraction(21, 4),
        Fraction(7, 4),
        Fraction(1, 4),
    )
    assert symmetric_solution == (
        Fraction(21, 10),
        Fraction(7, 10),
        Fraction(1, 10),
    )
    assert sum(
        symmetric[3][index] * symmetric_solution[index]
        for index in range(3)
    ) == 1
    return plus_solution, minus_solution, symmetric_solution


def residue(fraction, prime):
    return (
        fraction.numerator * pow(fraction.denominator, -1, prime)
    ) % prime


def audit_remaining_primes(solutions):
    survivors = []
    for prime in [value for value in range(11, 500) if is_prime(value)]:
        for profile, solution in zip(("plus", "minus", "symmetric"), solutions):
            m5 = residue(solution[2], prime)
            if m5 == 0 or m5 > min(8, prime - 4):
                continue
            if prime >= 13 and m5 >= 2:
                continue
            survivors.append((prime, profile, m5))
    assert survivors == [
        (11, "plus", 5),
        (11, "minus", 3),
        (19, "plus", 1),
    ]
    return survivors


def main():
    totals = {}
    for prime in (11, 13, 17, 19, 23):
        totals[prime] = exhaustive_classification(prime)
        print(f"PASS p={prime}: exhaustive height profiles {totals[prime]}")

    solutions = audit_linear_systems()
    print(f"PASS exact triple-codegree systems: {solutions}")
    survivors = audit_remaining_primes(solutions)
    print(f"PASS M5 cap/intersection pruning through p<500: {survivors}")
    print(
        "SCOPE: symbolic proof leaves exactly the listed local p=11,19 "
        "profiles; finite ranges are regression tests"
    )


if __name__ == "__main__":
    main()
