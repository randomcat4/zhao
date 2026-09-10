#!/usr/bin/env python3
"""Verify a p=7 weighted model with all triple relations and kernel dimension 3.

The certificate deliberately stops short of a group-valued ROUTE-A4 model:
its three-dimensional incidence kernel vanishes on 19 vertices, so it cannot
support the required long quotient atom; every intersection of two distinct
F3 support edges also has quotient sum zero.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import math
import time

import numpy as np


P = 7
N = 25
VERTICES = tuple(range(N))
CORE = tuple(range(7))
OUTSIDE = tuple(range(7, 25))
FAMILIES = ("F1", "F2", "F3")
SPECS = {
    "F1": (range(2, 7), 3),
    "F2": (range(4, 8), 4),
    "F3": (range(6, 9), 5),
}
TRIPLE_WEIGHTS = {"F1": 4, "F2": 10, "F3": 20}
PAIRS = ((0, 1), (2, 3), (4, 5))


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def balanced(core_set: tuple[int, ...]) -> bool:
    selected = set(core_set)
    return all((first in selected) == (second in selected) for first, second in PAIRS)


def row_system():
    pair_types = (
        [("cc", first, second) for first, second in combinations(CORE, 2)]
        + [("co", vertex) for vertex in CORE]
        + [("oo",)]
    )
    triple_types = [
        (core_part, 3 - core_size)
        for core_size in range(4)
        for core_part in combinations(CORE, core_size)
    ]
    rows = []
    rhs = []
    for family in FAMILIES:
        for vertex_type in [("c", vertex) for vertex in CORE] + [("o",)]:
            rows.append(("point", family, vertex_type))
            rhs.append(1)
    for pair_type in pair_types:
        rows.append(("pair1", pair_type))
        rhs.append(3)
    for pair_type in pair_types:
        rows.append(("pair2", pair_type))
        rhs.append(1)
    for triple_type in triple_types:
        rows.append(("triple", triple_type))
        rhs.append(6)
    rows.append(("n6",))
    rhs.append(3)
    assert len(rows) == 147
    return rows, rhs, pair_types, triple_types


def orbit_system():
    """Build the S_18-invariant system on zero-sum core/outside orbits."""
    rows, rhs, pair_types, triple_types = row_system()
    row_index = {row: index for index, row in enumerate(rows)}
    variables = []
    columns = []
    outside_size = len(OUTSIDE)

    for family in FAMILIES:
        lengths, core_threshold = SPECS[family]
        for length in lengths:
            for core_size in range(core_threshold, min(len(CORE), length) + 1):
                outside_count = length - core_size
                for core_set in combinations(CORE, core_size):
                    if not balanced(core_set):
                        continue
                    vector = np.zeros(len(rows), dtype=np.int16)
                    point_sign = 1 if length % 2 else -1
                    pair_sign = -point_sign
                    selected = set(core_set)

                    for vertex in CORE:
                        if vertex in selected:
                            vector[row_index[("point", family, ("c", vertex))]] = (
                                point_sign * choose(outside_size, outside_count)
                            )
                    vector[row_index[("point", family, ("o",))]] = (
                        point_sign * choose(outside_size - 1, outside_count - 1)
                    )

                    for pair_type in pair_types:
                        if pair_type[0] == "cc":
                            count = (
                                choose(outside_size, outside_count)
                                if pair_type[1] in selected and pair_type[2] in selected
                                else 0
                            )
                        elif pair_type[0] == "co":
                            count = (
                                choose(outside_size - 1, outside_count - 1)
                                if pair_type[1] in selected
                                else 0
                            )
                        else:
                            count = choose(outside_size - 2, outside_count - 2)
                        signed_count = pair_sign * count
                        if family == "F1":
                            vector[row_index[("pair1", pair_type)]] = 8 * signed_count
                            vector[row_index[("pair2", pair_type)]] = 2 * signed_count
                        elif family == "F2":
                            vector[row_index[("pair1", pair_type)]] = 10 * signed_count
                        else:
                            vector[row_index[("pair2", pair_type)]] = -10 * signed_count

                    for core_part, fixed_outside in triple_types:
                        if set(core_part).issubset(selected):
                            count = choose(
                                outside_size - fixed_outside,
                                outside_count - fixed_outside,
                            )
                            vector[row_index[("triple", (core_part, fixed_outside))]] = (
                                TRIPLE_WEIGHTS[family] * point_sign * count
                            )
                    if family == "F2" and length == 6:
                        vector[row_index[("n6",)]] = choose(outside_size, outside_count)
                    variables.append((family, core_set, outside_count))
                    columns.append(vector % P)

    assert len(variables) == 66
    augmented = np.column_stack(columns + [np.asarray(rhs, dtype=np.int16)]) % P
    return variables, augmented


def rref_solve(augmented: np.ndarray):
    matrix = augmented.copy()
    row_count, width = matrix.shape
    variable_count = width - 1
    pivot_row = 0
    pivots = []
    for column in range(variable_count):
        candidates = np.flatnonzero(matrix[pivot_row:, column])
        if candidates.size == 0:
            continue
        selected = pivot_row + int(candidates[0])
        matrix[[pivot_row, selected]] = matrix[[selected, pivot_row]]
        inverse = pow(int(matrix[pivot_row, column]), -1, P)
        matrix[pivot_row] = matrix[pivot_row] * inverse % P
        affected = np.flatnonzero(matrix[:, column])
        affected = affected[affected != pivot_row]
        if affected.size:
            matrix[affected] = (
                matrix[affected]
                - matrix[affected, column, None] * matrix[pivot_row]
            ) % P
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    inconsistent = bool(
        np.any(np.all(matrix[:, :-1] == 0, axis=1) & (matrix[:, -1] != 0))
    )
    solution = np.zeros(variable_count, dtype=np.int16)
    for row, column in enumerate(pivots):
        solution[column] = matrix[row, -1]
    return solution, len(pivots), inconsistent


def rank_mod(matrix: np.ndarray) -> int:
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


def expand_support(variables, solution):
    support = []
    for (family, core_set, outside_count), multiplicity in zip(variables, solution):
        if not multiplicity:
            continue
        for outside_set in combinations(OUTSIDE, outside_count):
            support.append(
                (family, frozenset(core_set + outside_set), int(multiplicity))
            )
    return support


def signed_count(support, family, required, point_sign):
    return sum(
        multiplicity * (-1) ** (len(edge) - point_sign)
        for current, edge, multiplicity in support
        if current == family and required.issubset(edge)
    ) % P


def quotient_labels():
    labels = np.zeros((N, 3), dtype=np.int16)
    labels[0] = (1, 0, 0)
    labels[1] = (-1, 0, 0)
    labels[2] = (0, 1, 0)
    labels[3] = (0, -1, 0)
    labels[4] = (0, 0, 1)
    labels[5] = (0, 0, -1)
    return labels % P


def weak_compositions(total: int, parts: int):
    return [
        values
        for values in product(range(4), repeat=parts)
        if sum(values) == total
    ]


def audit_all_nonzero_six_class_probe():
    """Reject one specific all-nonzero S_3^6-invariant label template."""
    class_count = 6
    class_size = 3
    class_labels = (
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    )
    core_labels = class_labels + ((1, 1, 1),)
    representatives = {}
    for total_size in (1, 2, 3):
        representatives[total_size] = [
            (core_part, outside_counts)
            for core_size in range(total_size + 1)
            for core_part in combinations(CORE, core_size)
            for outside_counts in weak_compositions(
                total_size - core_size, class_count
            )
        ]

    rows = []
    rhs = []
    for family in FAMILIES:
        for representative in representatives[1]:
            rows.append(("point", family, representative))
            rhs.append(1)
    for representative in representatives[2]:
        rows.append(("pair1", representative))
        rhs.append(3)
    for representative in representatives[2]:
        rows.append(("pair2", representative))
        rhs.append(1)
    for representative in representatives[3]:
        rows.append(("triple", representative))
        rhs.append(6)
    rows.append(("n6",))
    rhs.append(3)
    assert len(rows) == 572
    row_index = {row: index for index, row in enumerate(rows)}

    def extension_count(core_set, outside_counts, representative):
        required_core, required_outside = representative
        if not set(required_core).issubset(core_set):
            return 0
        result = 1
        for selected, required in zip(outside_counts, required_outside):
            result *= choose(class_size - required, selected - required)
        return result

    def label_sum(core_set, outside_counts):
        return tuple(
            (
                sum(core_labels[vertex][coordinate] for vertex in core_set)
                + sum(
                    count * class_labels[index][coordinate]
                    for index, count in enumerate(outside_counts)
                )
            )
            % P
            for coordinate in range(3)
        )

    columns = []
    for family in FAMILIES:
        lengths, core_threshold = SPECS[family]
        for length in lengths:
            for core_size in range(core_threshold, min(len(CORE), length) + 1):
                outside_size = length - core_size
                for core_set in combinations(CORE, core_size):
                    for outside_counts in weak_compositions(outside_size, class_count):
                        if label_sum(core_set, outside_counts) != (0, 0, 0):
                            continue
                        point_sign = 1 if length % 2 else -1
                        pair_sign = -point_sign
                        vector = np.zeros(len(rows), dtype=np.int16)
                        for representative in representatives[1]:
                            vector[row_index[("point", family, representative)]] = (
                                point_sign
                                * extension_count(core_set, outside_counts, representative)
                            )
                        for representative in representatives[2]:
                            count = extension_count(
                                core_set, outside_counts, representative
                            )
                            if family == "F1":
                                vector[row_index[("pair1", representative)]] = (
                                    8 * pair_sign * count
                                )
                                vector[row_index[("pair2", representative)]] = (
                                    2 * pair_sign * count
                                )
                            elif family == "F2":
                                vector[row_index[("pair1", representative)]] = (
                                    10 * pair_sign * count
                                )
                            else:
                                vector[row_index[("pair2", representative)]] = (
                                    -10 * pair_sign * count
                                )
                        for representative in representatives[3]:
                            vector[row_index[("triple", representative)]] = (
                                TRIPLE_WEIGHTS[family]
                                * point_sign
                                * extension_count(
                                    core_set, outside_counts, representative
                                )
                            )
                        if family == "F2" and length == 6:
                            vector[row_index[("n6",)]] = math.prod(
                                choose(class_size, count) for count in outside_counts
                            )
                        columns.append(vector % P)

    coefficients = np.column_stack(columns) % P
    augmented = np.column_stack((coefficients, np.asarray(rhs, dtype=np.int16))) % P
    assert coefficients.shape == (572, 223)
    coefficient_rank = rank_mod(coefficients)
    augmented_rank = rank_mod(augmented)
    assert coefficient_rank == 222
    assert augmented_rank == 223
    return len(columns), coefficient_rank, augmented_rank


def main():
    started = time.perf_counter()
    variables, augmented = orbit_system()
    solution, equation_rank, inconsistent = rref_solve(augmented)
    assert equation_rank == 48
    assert not inconsistent
    assert np.count_nonzero(solution) == 45
    assert np.all(
        augmented[:, :-1].astype(np.int64) @ solution.astype(np.int64) % P
        == augmented[:, -1]
    )

    support = expand_support(variables, solution)
    support_counts = Counter(family for family, _, _ in support)
    copy_counts = {
        family: sum(mult for current, _, mult in support if current == family)
        for family in FAMILIES
    }
    assert dict(support_counts) == {"F1": 1582, "F2": 1201, "F3": 245}
    assert copy_counts == {"F1": 3425, "F2": 1987, "F3": 1163}

    for family in FAMILIES:
        values = {
            signed_count(support, family, frozenset((vertex,)), 1)
            for vertex in VERTICES
        }
        assert values == {1}

    pair1_values = set()
    pair2_values = set()
    for first, second in combinations(VERTICES, 2):
        required = frozenset((first, second))
        d1 = signed_count(support, "F1", required, 0)
        d2 = signed_count(support, "F2", required, 0)
        d3 = signed_count(support, "F3", required, 0)
        pair1_values.add((8 * d1 + 10 * d2) % P)
        pair2_values.add((2 * d1 - 10 * d3) % P)
    assert pair1_values == {3}
    assert pair2_values == {1}

    triple_values = set()
    covered_triples = 0
    for triple in combinations(VERTICES, 3):
        required = frozenset(triple)
        deltas = {
            family: signed_count(support, family, required, 1)
            for family in FAMILIES
        }
        triple_values.add(
            (4 * deltas["F1"] + 10 * deltas["F2"] + 20 * deltas["F3"]) % P
        )
        covered_triples += int(any(required.issubset(edge) for _, edge, _ in support))
    assert triple_values == {6}
    assert covered_triples == choose(N, 3) == 2300

    n6 = sum(
        multiplicity
        for family, edge, multiplicity in support
        if family == "F2" and len(edge) == 6
    )
    assert n6 == 612 and n6 % P == 3

    family_edges = {
        family: [edge for current, edge, _ in support if current == family]
        for family in FAMILIES
    }
    for family, edges in family_edges.items():
        assert frozenset().union(*edges) == frozenset(VERTICES), family
        assert frozenset.intersection(*edges) == frozenset(), family

    intersections = {}
    for left_name, right_name in (
        ("F2", "F2"),
        ("F3", "F3"),
        ("F1", "F3"),
        ("F2", "F3"),
    ):
        sizes = [
            len(left.intersection(right))
            for i, left in enumerate(family_edges[left_name])
            for j, right in enumerate(family_edges[right_name])
            if left_name != right_name or i < j
        ]
        intersections[f"{left_name}-{right_name}"] = (min(sizes), len(sizes))
    assert intersections == {
        "F2-F2": (2, 720600),
        "F3-F3": (3, 29890),
        "F1-F3": (1, 387590),
        "F2-F3": (2, 294245),
    }

    incidence = np.asarray(
        [[int(vertex in edge) for vertex in VERTICES] for _, edge, _ in support],
        dtype=np.int16,
    )
    incidence_rank = rank_mod(incidence)
    assert incidence.shape == (3028, 25)
    assert incidence_rank == 22

    labels = quotient_labels()
    assert rank_mod(labels.T) == 3
    assert sum(np.any(label != 0) for label in labels) == 6
    assert all(np.all(labels[list(edge)].sum(axis=0) % P == 0) for _, edge, _ in support)
    f3_edges = family_edges["F3"]
    zero_intersections = 0
    for i, left in enumerate(f3_edges):
        for right in f3_edges[i + 1 :]:
            intersection = list(left.intersection(right))
            if np.all(labels[intersection].sum(axis=0) % P == 0):
                zero_intersections += 1
    assert zero_intersections == choose(len(f3_edges), 2) == 29890

    all_nonzero_probe = audit_all_nonzero_six_class_probe()
    assert all_nonzero_probe == (223, 222, 223)

    elapsed = time.perf_counter() - started
    print("PASS: triple-complete weighted model with incidence nullity 3 reconstructed")
    print(
        f"orbit variables 66; equation rank {equation_rank}; "
        f"nonzero orbit weights {np.count_nonzero(solution)}"
    )
    print(f"support counts {dict(support_counts)}; copy counts {copy_counts}")
    print(f"all {covered_triples} triple relations equal -1 mod 7")
    print(f"intersection minima/counts {intersections}; N6(F2)={n6}=3 mod 7")
    print(f"support incidence rank {incidence_rank}/25; kernel dimension 3")
    print(
        "EXPECTED FAILURE of the long-atom/intersection semantics: "
        f"the kernel is supported on only 6/25 positions, and all "
        f"{zero_intersections} distinct F3 intersections have quotient sum zero"
    )
    print(
        "specific stronger all-nonzero S_3^6 probe is inconsistent: "
        f"{all_nonzero_probe[0]} variables, ranks "
        f"{all_nonzero_probe[1]} < {all_nonzero_probe[2]}"
    )
    print(f"elapsed: {elapsed:.3f} s")


if __name__ == "__main__":
    main()
