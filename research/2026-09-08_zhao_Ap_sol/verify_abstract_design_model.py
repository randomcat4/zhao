#!/usr/bin/env python3
"""Rebuild and audit the p=7 weak abstract short-block model.

This is a finite-field certificate for a deliberately weakened, weighted
hypergraph problem.  It is not a group-valued model of the Zhao problem.
In particular, the script also verifies two expected obstructions:

* the model violates the later three-point-cover lemma; and
* its support incidence matrix has full column rank, so all global quotient
  labels whose sum vanishes on every support edge are zero.

The construction is deterministic under Python 3.12's ``random.Random`` and
uses NumPy only for finite-field row reduction.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import random
import time

import numpy as np


P = 7
N = 25
VERTICES = tuple(range(N))
CORE = frozenset(range(7))
OUTSIDE = frozenset(set(VERTICES) - CORE)
FAMILIES = ("F1", "F2", "F3")
FAMILY_INDEX = {family: index for index, family in enumerate(FAMILIES)}
SPECS = {
    "F1": (range(2, 7), 3),
    "F2": (range(4, 8), 4),
    "F3": (range(6, 9), 5),
}
EXPECTED_CANDIDATES = {"F1": 41006, "F2": 38326, "F3": 21950}
EXPECTED_SUPPORT = {"F1": 282, "F2": 277, "F3": 23}
EXPECTED_COPIES = {"F1": 1001, "F2": 995, "F3": 90}
EXPECTED_LENGTH_SUPPORT = {
    ("F1", 4): 5,
    ("F1", 5): 36,
    ("F1", 6): 241,
    ("F2", 4): 1,
    ("F2", 5): 4,
    ("F2", 6): 43,
    ("F2", 7): 229,
    ("F3", 7): 4,
    ("F3", 8): 19,
}
EXPECTED_LENGTH_COPIES = {
    ("F1", 4): 18,
    ("F1", 5): 132,
    ("F1", 6): 851,
    ("F2", 4): 5,
    ("F2", 5): 21,
    ("F2", 6): 136,
    ("F2", 7): 833,
    ("F3", 7): 17,
    ("F3", 8): 73,
}


def sampled_candidates() -> tuple[list[tuple[str, tuple[int, ...]]], dict[str, int]]:
    """Enumerate lexicographically and take three sequential Random(99) samples."""
    rng = random.Random(99)
    variables: list[tuple[str, tuple[int, ...]]] = []
    counts: dict[str, int] = {}
    for family in FAMILIES:
        lengths, core_threshold = SPECS[family]
        eligible = [
            edge
            for length in lengths
            for edge in combinations(VERTICES, length)
            if len(CORE.intersection(edge)) >= core_threshold
        ]
        counts[family] = len(eligible)
        variables.extend((family, edge) for edge in rng.sample(eligible, 700))
    return variables, counts


def build_system(
    variables: list[tuple[str, tuple[int, ...]]],
) -> tuple[np.ndarray, list[tuple[int, int]]]:
    """Build the 676-by-(2100+1) augmented matrix over F_7."""
    pairs = list(combinations(VERTICES, 2))
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    point_rows = len(FAMILIES) * N
    first_pair_row = point_rows
    second_pair_row = first_pair_row + len(pairs)
    n6_row = second_pair_row + len(pairs)
    row_count = n6_row + 1
    matrix = np.zeros((row_count, len(variables) + 1), dtype=np.int16)

    for column, (family, edge) in enumerate(variables):
        point_sign = 1 if len(edge) % 2 else -1
        pair_sign = -point_sign
        family_offset = FAMILY_INDEX[family] * N
        for vertex in edge:
            matrix[family_offset + vertex, column] = point_sign
        for pair in combinations(edge, 2):
            index = pair_index[pair]
            if family == "F1":
                matrix[first_pair_row + index, column] += 8 * pair_sign
                matrix[second_pair_row + index, column] += 2 * pair_sign
            elif family == "F2":
                matrix[first_pair_row + index, column] += 10 * pair_sign
            else:
                matrix[second_pair_row + index, column] -= 10 * pair_sign
        if family == "F2" and len(edge) == 6:
            matrix[n6_row, column] = 1

    # At p=7, -3/4 = 3/10 = -1/20 = 1 and 1/5 = 3.
    matrix[:point_rows, -1] = 1
    matrix[first_pair_row:second_pair_row, -1] = 3
    matrix[second_pair_row:n6_row, -1] = 1
    matrix[n6_row, -1] = 3
    matrix %= P
    return matrix, pairs


def deterministic_rref_solve(augmented: np.ndarray) -> tuple[np.ndarray, int, bool]:
    """Left-to-right RREF, always choosing the first available pivot row."""
    matrix = augmented.copy()
    row_count, augmented_width = matrix.shape
    variable_count = augmented_width - 1
    pivot_row = 0
    pivots: list[int] = []
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
        np.any(
            np.all(matrix[:, :-1] == 0, axis=1)
            & (matrix[:, -1] != 0)
        )
    )
    solution = np.zeros(variable_count, dtype=np.int16)
    for row, column in enumerate(pivots):
        solution[column] = matrix[row, -1]
    return solution, len(pivots), inconsistent


def rank_mod(matrix: np.ndarray) -> int:
    """Column rank over F_7 using the same deterministic pivot convention."""
    work = matrix.copy() % P
    row_count, column_count = work.shape
    pivot_row = 0
    for column in range(column_count):
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
        if pivot_row == row_count:
            break
    return pivot_row


def signed_degree(
    support: list[tuple[str, tuple[int, ...], int]], family: str, vertex: int
) -> int:
    return sum(
        multiplicity * (-1) ** (len(edge) - 1)
        for current, edge, multiplicity in support
        if current == family and vertex in edge
    ) % P


def signed_codegree(
    support: list[tuple[str, tuple[int, ...], int]],
    family: str,
    first: int,
    second: int,
) -> int:
    return sum(
        multiplicity * (-1) ** len(edge)
        for current, edge, multiplicity in support
        if current == family and first in edge and second in edge
    ) % P


def minimum_intersection(
    left: list[frozenset[int]], right: list[frozenset[int]], same: bool
) -> tuple[int, int]:
    sizes = [
        len(first.intersection(second))
        for i, first in enumerate(left)
        for j, second in enumerate(right)
        if not same or i < j
    ]
    return min(sizes), len(sizes)


def main() -> None:
    started = time.perf_counter()
    variables, candidate_counts = sampled_candidates()
    assert candidate_counts == EXPECTED_CANDIDATES
    assert len(variables) == 2100

    augmented, pairs = build_system(variables)
    solution, equation_rank, inconsistent = deterministic_rref_solve(augmented)
    assert equation_rank == 676
    assert not inconsistent
    coefficients = augmented[:, :-1].astype(np.int64)
    rhs = augmented[:, -1].astype(np.int64)
    assert np.all(coefficients @ solution.astype(np.int64) % P == rhs)

    support = [
        (family, edge, int(multiplicity))
        for (family, edge), multiplicity in zip(variables, solution)
        if multiplicity
    ]
    support_counts = Counter(family for family, _, _ in support)
    copy_counts = {
        family: sum(mult for current, _, mult in support if current == family)
        for family in FAMILIES
    }
    length_support = Counter((family, len(edge)) for family, edge, _ in support)
    length_copies = Counter()
    for family, edge, multiplicity in support:
        length_copies[(family, len(edge))] += multiplicity
    assert dict(support_counts) == EXPECTED_SUPPORT
    assert copy_counts == EXPECTED_COPIES
    assert dict(length_support) == EXPECTED_LENGTH_SUPPORT
    assert dict(length_copies) == EXPECTED_LENGTH_COPIES

    for family in FAMILIES:
        assert {signed_degree(support, family, vertex) for vertex in VERTICES} == {1}
    first_pair_values = {
        (
            8 * signed_codegree(support, "F1", first, second)
            + 10 * signed_codegree(support, "F2", first, second)
        ) % P
        for first, second in pairs
    }
    second_pair_values = {
        (
            2 * signed_codegree(support, "F1", first, second)
            - 10 * signed_codegree(support, "F3", first, second)
        ) % P
        for first, second in pairs
    }
    assert first_pair_values == {3}
    assert second_pair_values == {1}
    n6 = sum(
        multiplicity
        for family, edge, multiplicity in support
        if family == "F2" and len(edge) == 6
    )
    assert n6 == 136 and n6 % P == 3

    family_edges = {
        family: [frozenset(edge) for current, edge, _ in support if current == family]
        for family in FAMILIES
    }
    for family, edges in family_edges.items():
        assert frozenset().union(*edges) == frozenset(VERTICES), family
        assert frozenset.intersection(*edges) == frozenset(), family
    intersection_results = {
        "F2-F2": minimum_intersection(family_edges["F2"], family_edges["F2"], True),
        "F3-F3": minimum_intersection(family_edges["F3"], family_edges["F3"], True),
        "F1-F3": minimum_intersection(family_edges["F1"], family_edges["F3"], False),
        "F2-F3": minimum_intersection(family_edges["F2"], family_edges["F3"], False),
    }
    assert intersection_results == {
        "F2-F2": (1, 38226),
        "F3-F3": (3, 253),
        "F1-F3": (1, 6486),
        "F2-F3": (2, 6371),
    }
    six_edges = [
        frozenset(edge)
        for family, edge, _ in support
        if family == "F2" and len(edge) == 6
    ]
    thick_pairs = [
        (edge, other)
        for edge in six_edges
        for other in family_edges["F3"]
    ]
    assert len(thick_pairs) == 43 * 23 == 989
    assert min(len(edge.intersection(other)) for edge, other in thick_pairs) >= 2

    # The strengthened triple-cover lemma is intentionally not imposed in the
    # linear system.  Audit its failure, especially on triples outside CORE.
    covered_triples: set[tuple[int, int, int]] = set()
    for _, edge, _ in support:
        covered_triples.update(combinations(edge, 3))
    all_triples = set(combinations(VERTICES, 3))
    outside_triples = set(combinations(sorted(OUTSIDE), 3))
    uncovered = sorted(all_triples - covered_triples)
    uncovered_outside = sorted(outside_triples - covered_triples)
    assert uncovered
    assert uncovered_outside

    triple_relation_failures = []
    for triple in combinations(VERTICES, 3):
        deltas = {}
        for family in FAMILIES:
            deltas[family] = sum(
                multiplicity * (-1) ** (len(edge) - 1)
                for current, edge, multiplicity in support
                if current == family and set(triple).issubset(edge)
            ) % P
        value = (4 * deltas["F1"] + 10 * deltas["F2"] + 20 * deltas["F3"]) % P
        if value != (-1) % P:
            triple_relation_failures.append((triple, value))
    assert triple_relation_failures
    assert (uncovered_outside[0], 0) in triple_relation_failures

    incidence = np.asarray(
        [[int(vertex in edge) for vertex in VERTICES] for _, edge, _ in support],
        dtype=np.int16,
    )
    incidence_rank = rank_mod(incidence)
    assert incidence.shape == (582, 25)
    assert incidence_rank == 25

    elapsed = time.perf_counter() - started
    print("PASS: deterministically reconstructed the weak p=7 weighted model")
    print(f"candidate counts: {candidate_counts}; equation rank: {equation_rank}")
    print(f"support counts: {dict(support_counts)}; copy counts: {copy_counts}")
    print(f"intersection minima/counts: {intersection_results}")
    print(f"N6(F2) = {n6} = {n6 % P} (mod 7)")
    print(
        "EXPECTED REJECTION by triple-cover lemma: "
        f"{len(uncovered)}/{len(all_triples)} triples uncovered; "
        f"{len(uncovered_outside)}/{len(outside_triples)} outside-core triples uncovered; "
        f"first outside-core witness {uncovered_outside[0]}"
    )
    print(
        "triple signed-congruence failures: "
        f"{len(triple_relation_failures)}/{len(all_triples)}; "
        f"first {triple_relation_failures[0]}"
    )
    print(
        "EXPECTED REJECTION as a group-valued model: "
        f"support incidence rank {incidence_rank}/25, hence kernel dimension 0"
    )
    print(f"elapsed: {elapsed:.3f} s")


if __name__ == "__main__":
    main()
