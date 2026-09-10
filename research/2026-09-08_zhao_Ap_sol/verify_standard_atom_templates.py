#!/usr/bin/env python3
"""Audit fixed C-templates over the standard extreme C_p^3 atom.

The main computation is an exact orbit calculation over F_7.  A second,
finite regression checks the sparse pair obstruction for the natural strong
template over primes p>=11.  The proof of that infinite statement is symbolic
in route_a_standard_atom_templates.md.  Nothing here classifies arbitrary
six-point complements or arbitrary extreme atoms.
"""

from __future__ import annotations

from itertools import combinations
import math
import time

import numpy as np


P = 7
CLASS_SIZES = (6, 6, 6, 1, 1, 1, 1, 1, 1, 1)
E1 = (1, 0, 0)
E2 = (0, 1, 0)
E3 = (0, 0, 1)
G = (1, 1, 1)
B_LABELS = (E1, E2, E3, G)
FAMILIES = ("F1", "F2", "F3")
LENGTHS = {
    "F1": range(2, 7),
    "F2": range(4, 8),
    "F3": range(6, 9),
}
TRIPLE_WEIGHTS = {"F1": 4, "F2": 10, "F3": 20}
ZERO_VECTOR = (0,) * len(CLASS_SIZES)

BALANCED_C = (
    E1,
    (-1, 0, 0),
    E2,
    (0, -1, 0),
    E3,
    (0, 0, -1),
)
STRONG_C = (E1, E2, E3, G, G, (4, 4, 4))


def residue_vector(vector):
    return tuple(coordinate % P for coordinate in vector)


BALANCED_C = tuple(residue_vector(vector) for vector in BALANCED_C)


def count_vectors(total: int):
    output = []

    def visit(index: int, remaining: int, prefix: tuple[int, ...]):
        if index == len(CLASS_SIZES):
            if remaining == 0:
                output.append(prefix)
            return
        for value in range(min(CLASS_SIZES[index], remaining) + 1):
            visit(index + 1, remaining - value, prefix + (value,))

    visit(0, total, ())
    return output


COUNT_VECTORS = {total: count_vectors(total) for total in range(9)}


def orbit_coefficient(edge_type, required_type):
    coefficient = 1
    for class_size, selected, required in zip(
        CLASS_SIZES, edge_type, required_type
    ):
        if required > selected:
            return 0
        coefficient *= math.comb(class_size - required, selected - required)
    return coefficient


def quotient_sum(edge_type, labels):
    return tuple(
        sum(edge_type[index] * labels[index][coordinate]
            for index in range(len(CLASS_SIZES))) % P
        for coordinate in range(3)
    )


def row_scheme():
    rows = []
    rhs = []
    for family in FAMILIES:
        for point_type in COUNT_VECTORS[1]:
            rows.append(("point", family, point_type))
            rhs.append(1)
    for pair_type in COUNT_VECTORS[2]:
        rows.append(("pair1", pair_type))
        rhs.append(3)
    for pair_type in COUNT_VECTORS[2]:
        rows.append(("pair2", pair_type))
        rhs.append(1)
    for triple_type in COUNT_VECTORS[3]:
        rows.append(("triple", triple_type))
        rhs.append(6)
    rows.append(("n6",))
    rhs.append(3)
    assert len(COUNT_VECTORS[1]) == 10
    assert len(COUNT_VECTORS[2]) == 48
    assert len(COUNT_VECTORS[3]) == 150
    assert len(rows) == 277
    return rows, np.asarray(rhs, dtype=np.int64)


ROWS, RHS = row_scheme()
ROW_INDEX = {row: index for index, row in enumerate(ROWS)}


def build_template(c_labels):
    labels = tuple(residue_vector(vector) for vector in B_LABELS + c_labels)
    assert all(label != (0, 0, 0) for label in labels)
    assert tuple(sum(label[j] for label in c_labels) % P for j in range(3)) == (
        0,
        0,
        0,
    )

    zero_sum_types = {
        length: [
            edge_type
            for edge_type in COUNT_VECTORS[length]
            if quotient_sum(edge_type, labels) == (0, 0, 0)
        ]
        for length in range(2, 9)
    }
    # The standard B is an atom, so every proper short zero sum meets C.
    assert all(
        sum(edge_type[4:]) > 0
        for types in zero_sum_types.values()
        for edge_type in types
    )

    variables = []
    columns = []
    for family in FAMILIES:
        for length in LENGTHS[family]:
            for edge_type in zero_sum_types[length]:
                point_sign = 1 if length % 2 else -1
                pair_sign = -point_sign
                column = np.zeros(len(ROWS), dtype=np.int64)
                for point_type in COUNT_VECTORS[1]:
                    column[ROW_INDEX[("point", family, point_type)]] = (
                        point_sign * orbit_coefficient(edge_type, point_type)
                    )
                for pair_type in COUNT_VECTORS[2]:
                    count = orbit_coefficient(edge_type, pair_type)
                    if family == "F1":
                        column[ROW_INDEX[("pair1", pair_type)]] = 8 * pair_sign * count
                        column[ROW_INDEX[("pair2", pair_type)]] = 2 * pair_sign * count
                    elif family == "F2":
                        column[ROW_INDEX[("pair1", pair_type)]] = 10 * pair_sign * count
                    else:
                        column[ROW_INDEX[("pair2", pair_type)]] = -10 * pair_sign * count
                for triple_type in COUNT_VECTORS[3]:
                    column[ROW_INDEX[("triple", triple_type)]] = (
                        TRIPLE_WEIGHTS[family]
                        * point_sign
                        * orbit_coefficient(edge_type, triple_type)
                    )
                if family == "F2" and length == 6:
                    column[ROW_INDEX[("n6",)]] = orbit_coefficient(
                        edge_type, ZERO_VECTOR
                    )
                variables.append((family, edge_type))
                columns.append(column % P)

    coefficients = np.column_stack(columns) % P
    return labels, zero_sum_types, variables, coefficients


def rank_mod(matrix):
    work = matrix.copy() % P
    pivot_row = 0
    for column in range(work.shape[1]):
        candidates = np.flatnonzero(work[pivot_row:, column])
        if candidates.size == 0:
            continue
        selected = pivot_row + int(candidates[0])
        work[[pivot_row, selected]] = work[[selected, pivot_row]]
        inverse = pow(int(work[pivot_row, column]), -1, P)
        work[pivot_row] = work[pivot_row] * inverse % P
        affected = np.flatnonzero(work[:, column])
        affected = affected[affected != pivot_row]
        if affected.size:
            work[affected] = (
                work[affected]
                - work[affected, column, None] * work[pivot_row]
            ) % P
        pivot_row += 1
        if pivot_row == work.shape[0]:
            break
    return pivot_row


def unit(class_index):
    vector = [0] * len(CLASS_SIZES)
    vector[class_index] = 1
    return tuple(vector)


def pair(first, second):
    vector = [0] * len(CLASS_SIZES)
    vector[first] += 1
    vector[second] += 1
    return tuple(vector)


def verify_thirteen_term_certificate(coefficients):
    """Check the sparse left-null certificate for STRONG_C orbit columns."""
    terms = (
        (3, ("point", "F1", unit(9))),
        (6, ("point", "F1", unit(8))),
        (6, ("point", "F1", unit(7))),
        (6, ("point", "F1", unit(6))),
        (1, ("point", "F1", unit(2))),
        (3, ("point", "F2", unit(3))),
        (2, ("pair1", pair(8, 9))),
        (2, ("pair1", pair(7, 9))),
        (4, ("pair1", pair(7, 8))),
        (6, ("pair1", pair(6, 9))),
        (6, ("pair1", pair(5, 9))),
        (1, ("pair1", pair(5, 6))),
        (6, ("pair1", pair(1, 2))),
    )
    certificate = np.zeros(len(ROWS), dtype=np.int64)
    for coefficient, row in terms:
        certificate[ROW_INDEX[row]] += coefficient
    column_values = certificate @ coefficients % P
    right_value = int(certificate @ RHS % P)
    assert np.all(column_values == 0)
    assert right_value == 1
    assert np.count_nonzero(certificate % P) == 13
    return right_value


def triple_orbits_covered(zero_sum_types):
    all_types = [edge_type for types in zero_sum_types.values() for edge_type in types]
    return sum(
        any(all(required <= selected for required, selected in zip(triple, edge_type))
            for edge_type in all_types)
        for triple in COUNT_VECTORS[3]
    )


def is_prime(value):
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def audit_infinite_strong_pair_bound():
    """Regress the p>=11 claim for all primes through 500.

    Here x_i counts every position with quotient label e_i, z counts every
    g-position, tau selects the unique -3g position, and x_1>=2 fixes a pair
    in the B_{e_1} class.  Candidate lengths are at most eight.
    """
    primes = [value for value in range(11, 501) if is_prime(value)]
    for prime in primes:
        candidates = []
        for tau in range(2):
            for x1 in range(2, 9):
                for x2 in range(9):
                    for x3 in range(9):
                        for z in range(4):
                            length = tau + x1 + x2 + x3 + z
                            if length > 8:
                                continue
                            coordinates = (
                                x1 + z - 3 * tau,
                                x2 + z - 3 * tau,
                                x3 + z - 3 * tau,
                            )
                            if all(coordinate % prime == 0 for coordinate in coordinates):
                                candidates.append(length)
        assert candidates
        assert min(candidates) == 8
    return len(primes)


def audit_template(name, c_labels, expected_counts, expected_variables, expected_ranks):
    _, zero_sum_types, variables, coefficients = build_template(c_labels)
    counts = {length: len(types) for length, types in zero_sum_types.items()}
    assert counts == expected_counts
    assert len(variables) == expected_variables
    coefficient_rank = rank_mod(coefficients)
    augmented_rank = rank_mod(np.column_stack((coefficients, RHS)))
    assert (coefficient_rank, augmented_rank) == expected_ranks
    covered = triple_orbits_covered(zero_sum_types)
    print(
        f"{name}: zero-sum orbit counts {counts}; variables {len(variables)}; "
        f"ranks {coefficient_rank} < {augmented_rank}; triple orbits covered {covered}/150"
    )
    return coefficients, covered


def main():
    started = time.perf_counter()
    averaging_factor = pow(math.factorial(6), 3, P)
    assert averaging_factor == 6
    assert math.gcd(averaging_factor, P) == 1

    audit_template(
        "balanced C",
        BALANCED_C,
        {2: 6, 3: 0, 4: 13, 5: 0, 6: 8, 7: 3, 8: 0},
        62,
        (54, 55),
    )
    strong_coefficients, covered = audit_template(
        "strong C",
        STRONG_C,
        {2: 0, 3: 0, 4: 1, 5: 0, 6: 24, 7: 3, 8: 24},
        104,
        (66, 67),
    )
    assert covered == 150
    assert verify_thirteen_term_certificate(strong_coefficients) == 1
    checked_primes = audit_infinite_strong_pair_bound()

    elapsed = time.perf_counter() - started
    print(
        "PASS: both fixed templates are inconsistent over F_7; "
        "the 13-term strong-template certificate has left side 0 and right side 1"
    )
    print(
        f"orbit averaging is legal: (6!)^3 = {averaging_factor} mod 7 is invertible"
    )
    print(
        f"p>=11 strong-template pair bound checked for {checked_primes} primes through 500"
    )
    print("SCOPE: no conclusion for arbitrary C or arbitrary extreme atoms")
    print(f"elapsed: {elapsed:.3f} s")


if __name__ == "__main__":
    main()
