#!/usr/bin/env python3
"""Exact F_7 refinement of the 29 four-fibre height orbits.

This script imports the exhaustive star construction from
verify_p7_six_fibre_exclusion.py.  It computes exact affine projections of
the point/pair/triple Hasse system, checks that singleton tails may all be
zero, and verifies small local tail witnesses.  The witnesses do not realize
a quotient atom or a complete ROUTE-A4 sequence.
"""

from __future__ import annotations

from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from math import comb
from pathlib import Path


P = 7
HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_p7_six_fibre_exclusion.py"
SPEC = spec_from_file_location("p7_base", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

EXCEPTIONAL_PROFILE = (0, 0, 0, 1)


def rref(matrix, rhs):
    """Reduced row echelon form over F_7, with zero rows deleted."""
    if not matrix:
        return []
    rows = len(matrix)
    columns = len(matrix[0])
    augmented = [
        [value % P for value in row] + [target % P]
        for row, target in zip(matrix, rhs)
    ]
    pivot_row = 0
    for column in range(columns):
        selected = next(
            (
                row
                for row in range(pivot_row, rows)
                if augmented[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        augmented[pivot_row], augmented[selected] = (
            augmented[selected],
            augmented[pivot_row],
        )
        inverse = pow(augmented[pivot_row][column], -1, P)
        augmented[pivot_row] = [
            value * inverse % P for value in augmented[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row or not augmented[row][column]:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                (value - factor * pivot) % P
                for value, pivot in zip(augmented[row], augmented[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return [
        (row[:-1], row[-1])
        for row in augmented
        if any(row[:-1]) or row[-1]
    ]


def affine_projection(stars, matrix, rhs, targets, fixed_zero=()):
    """Project Mz=rhs to target coordinates, with selected columns zero.

    Nuisance columns are eliminated first.  The remaining rows are then put
    in RREF, so the returned equations describe the exact affine projection,
    not merely necessary relations.
    """
    target_set = set(targets)
    fixed_set = set(fixed_zero)
    assert not target_set & fixed_set
    nuisance = [
        column
        for column in range(len(stars))
        if column not in target_set and column not in fixed_set
    ]
    order = nuisance + list(targets)
    projected_matrix = [[row[column] for column in order] for row in matrix]
    rows = len(projected_matrix)
    nuisance_count = len(nuisance)
    augmented = [
        [value % P for value in row] + [target % P]
        for row, target in zip(projected_matrix, rhs)
    ]

    pivot_row = 0
    for column in range(nuisance_count):
        selected = next(
            (
                row
                for row in range(pivot_row, rows)
                if augmented[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        augmented[pivot_row], augmented[selected] = (
            augmented[selected],
            augmented[pivot_row],
        )
        inverse = pow(augmented[pivot_row][column], -1, P)
        augmented[pivot_row] = [
            value * inverse % P for value in augmented[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row or not augmented[row][column]:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                (value - factor * pivot) % P
                for value, pivot in zip(augmented[row], augmented[pivot_row])
            ]
        pivot_row += 1

    target_matrix = []
    target_rhs = []
    for row in augmented:
        if any(row[:nuisance_count]):
            continue
        target_part = row[nuisance_count:-1]
        if any(target_part) or row[-1]:
            target_matrix.append(target_part)
            target_rhs.append(row[-1])
    return rref(target_matrix, target_rhs)


def solve_after_zeroing(stars, matrix, rhs, zero_columns):
    keep = [
        column
        for column in range(len(stars))
        if column not in set(zero_columns)
    ]
    restricted = [[row[column] for column in keep] for row in matrix]
    consistent, rank, solution, certificate = BASE.rref_solve(restricted, rhs)
    if consistent:
        assert solution is not None and certificate is None
        BASE.verify_solution(restricted, rhs, solution)
    return consistent, rank, keep, solution


def is_singleton(star):
    length, trace_size, _, _, _ = star
    return length - trace_size == 1


def is_full_f3(star):
    _, trace_size, _, _, families = star
    return trace_size == 4 and families == (3,)


def bears_f3(star):
    return 3 in star[4]


def vec_add(*vectors):
    return tuple(sum(vector[index] for vector in vectors) % P for index in range(3))


def vec_scale(scalar, vector):
    return tuple(scalar * value % P for value in vector)


def subset_sum(labels, subset):
    return vec_add(*(labels[index] for index in subset))


def audit_local_tail_candidates():
    """Check named tails, then reject the old exceptional labelled candidate."""
    q = (1, 0, 0)
    t_label = (0, 1, 0)

    # A full-core length-seven F3 block has a three-point tail of sum 3q.
    full_labels = {
        0: t_label,
        1: (0, 0, 1),
        2: (3, 6, 6),
    }
    full_tail = frozenset(full_labels)
    assert subset_sum(full_labels, full_tail) == vec_scale(3, q)
    assert subset_sum(full_labels, {0}) == t_label != (0, 0, 0)

    # For 0001 with full-core F3 columns suppressed, the residues can be
    # represented by one tail in each of (7,1), (6,2), and (7,3).
    labels = {
        0: t_label,
        1: (0, 0, 1),
        2: (0, 0, 2),
        3: (0, 0, 3),
        4: (0, 0, 4),
        5: (6, 6, 4),
        6: (0, 0, 1),
        7: (0, 0, 2),
        8: (5, 6, 4),
        9: (0, 0, 3),
        10: (0, 0, 4),
        11: (4, 6, 0),
    }
    tails = {
        1: frozenset({0, 1, 2, 3, 4, 5}),
        2: frozenset({0, 6, 7, 8}),
        3: frozenset({0, 9, 10, 11}),
    }
    for trace_size, tail in tails.items():
        assert subset_sum(labels, tail) == vec_scale(-trace_size, q)
        assert tail & {0} == {0}
        assert subset_sum(labels, tail & {0}) == t_label

    # The F3 traces for profile 0001 are exactly those containing point 3.
    profile = EXCEPTIONAL_PROFILE
    f3_traces = {}
    for trace_size in (1, 2, 3):
        f3_traces[trace_size] = [
            frozenset(trace)
            for trace in __import__("itertools").combinations(range(4), trace_size)
            if (2 + sum(profile[index] for index in trace)) % P == 3
        ]
        assert all(3 in trace for trace in f3_traces[trace_size])

    # Distinct forced tails meet only at the T point.  For every possible F3
    # trace pair, the block intersection has quotient t_label + kq != 0.
    for first_b in (1, 2, 3):
        for second_b in range(first_b + 1, 4):
            tail_intersection = tails[first_b] & tails[second_b]
            assert tail_intersection == {0}
            for first_trace in f3_traces[first_b]:
                for second_trace in f3_traces[second_b]:
                    core_sum = vec_scale(len(first_trace & second_trace), q)
                    intersection_sum = vec_add(
                        subset_sum(labels, tail_intersection), core_sum
                    )
                    assert intersection_sum != (0, 0, 0)

    heights = {index: 0 for index in labels}
    heights[1] = heights[6] = heights[9] = 2
    for tail in tails.values():
        assert sum(heights[index] for index in tail) % P == 2
    actual_counts = Counter((labels[index], heights[index]) for index in labels)
    assert max(actual_counts.values()) <= 3

    # The named tails are not closed under all subsets of the labelled
    # positions.  After adjoining the four core positions of profile 0001,
    # the following two additional blocks are both F3, while their
    # intersection already has quotient sum zero.  Thus the old labels are
    # an expected rejection, not a local compatibility witness.
    expanded_labels = {f"x{i}": q for i in range(4)}
    expanded_heights = {f"x{i}": (0, 0, 0, 1)[i] for i in range(4)}
    expanded_labels.update({f"y{i}": value for i, value in labels.items()})
    expanded_heights.update({f"y{i}": value for i, value in heights.items()})
    first = frozenset({"x3", "y0", "y5", "y9"})
    second = frozenset({"x3", "y0", "y3", "y4", "y5", "y9"})
    for block in (first, second):
        assert 2 <= len(block) <= 8
        assert subset_sum(expanded_labels, block) == (0, 0, 0)
        assert sum(expanded_heights[index] for index in block) % P == 3
    assert first != second
    assert subset_sum(expanded_labels, first & second) == (0, 0, 0)


def audit_profiles():
    profiles = BASE.height_profiles(4)
    assert len(profiles) == 29
    forced_full = []
    exceptional_relations = None

    for profile in profiles:
        stars, matrix, rhs, _ = BASE.build_hasse_system(profile)
        singleton_columns = [
            column for column, star in enumerate(stars) if is_singleton(star)
        ]
        consistent, _, _, _ = solve_after_zeroing(
            stars, matrix, rhs, singleton_columns
        )
        assert consistent

        full_columns = [
            column for column, star in enumerate(stars) if is_full_f3(star)
        ]
        assert [stars[column][0] for column in full_columns] == [6, 7, 8]
        full_projection = affine_projection(
            stars, matrix, rhs, full_columns
        )

        if profile == EXCEPTIONAL_PROFILE:
            assert full_projection == []
            fixed_zero = full_columns
            lower_f3 = [
                column
                for column, star in enumerate(stars)
                if bears_f3(star)
                and column not in full_columns
                and column not in singleton_columns
            ]
            assert [
                (stars[column][0], stars[column][1], stars[column][2])
                for column in lower_f3
            ] == [
                (6, 1, 2),
                (6, 2, 2),
                (6, 3, 2),
                (7, 1, 2),
                (7, 2, 2),
                (7, 3, 2),
            ]
            exceptional_relations = affine_projection(
                stars, matrix, rhs, lower_f3, fixed_zero
            )
            assert exceptional_relations == [
                ([1, 0, 0, 6, 0, 0], 6),
                ([0, 1, 0, 0, 6, 0], 1),
                ([0, 0, 1, 0, 0, 6], 6),
            ]

            # Imposing the stronger formal choice that all singleton tails
            # vanish leaves exactly the same projection.
            bounded_relations = affine_projection(
                stars,
                matrix,
                rhs,
                lower_f3,
                full_columns + singleton_columns,
            )
            assert bounded_relations == exceptional_relations

            # The minimal residue choice (0,1,0,1,0,1) extends exactly.
            choice = [0, 1, 0, 1, 0, 1]
            assert all(
                sum(coefficient * value for coefficient, value in zip(row, choice))
                % P
                == target
                for row, target in exceptional_relations
            )
            fixed_choice = list(full_columns + singleton_columns)
            adjusted_rhs = list(rhs)
            for column, value in zip(lower_f3, choice):
                adjusted_rhs = [
                    (target - row[column] * value) % P
                    for row, target in zip(matrix, adjusted_rhs)
                ]
                fixed_choice.append(column)
            keep = [
                column
                for column in range(len(stars))
                if column not in set(fixed_choice)
            ]
            restricted = [[row[column] for column in keep] for row in matrix]
            assert BASE.rref_solve(restricted, adjusted_rhs)[0]
            continue

        assert full_projection == [([1, 6, 1], 6)]
        forced_full.append(profile)

        # There is no forced full-tail length: after zeroing every singleton
        # and every other F3-bearing column, the sole length-seven full-core
        # column has residue one and the system remains consistent.
        selected = next(
            column
            for column in full_columns
            if stars[column][0] == 7
        )
        zero_columns = [
            column
            for column, star in enumerate(stars)
            if is_singleton(star) or (bears_f3(star) and column != selected)
        ]
        consistent, _, keep, solution = solve_after_zeroing(
            stars, matrix, rhs, zero_columns
        )
        assert consistent and solution is not None
        assert solution[keep.index(selected)] == 1

    assert len(forced_full) == 28
    assert exceptional_relations is not None

    # Raw position capacities for a d-point tail meeting T.  The minimum is
    # attained at |T|=6 and is already much larger than all F_7 residues.
    capacities = {
        tail_size: min(
            comb(21, tail_size) - comb(21 - t_size, tail_size)
            for t_size in (6, 7, 8)
        )
        for tail_size in range(2, 7)
    }
    assert capacities == {2: 105, 3: 875, 4: 4620, 5: 17346, 6: 49259}
    assert all(capacity >= 6 for capacity in capacities.values())
    return forced_full, capacities


def main():
    forced_full, capacities = audit_profiles()
    audit_local_tail_candidates()
    print("PASS exact p=7, m=4 affine star projections")
    print("28/29 profiles force a full-core F3 tail")
    print("full-core residues: N_6 - N_7 + N_8 = 6 (mod 7)")
    print("exception 0001 without full core forces b=1,2,3 F3-bearing layers")
    print(f"raw meet-T capacities for tail sizes 2--6: {capacities}")
    print("PASS named-tail arithmetic and raw capacity checks")
    print("EXPECTED REJECTION: old 0001 labels induce two extra F3 blocks")
    print("EXPECTED REJECTION: their intersection has quotient sum zero")
    print("LABEL STATUS: unresolved; the former exceptional witness is invalid")
    print(
        "SCOPE: no labelled complement atom or complete ROUTE-A4 model is constructed"
    )


if __name__ == "__main__":
    main()
