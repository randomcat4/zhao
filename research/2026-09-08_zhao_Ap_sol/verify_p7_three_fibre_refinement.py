#!/usr/bin/env python3
"""Exact F_7 refinement of the 12 three-fibre height orbits.

The script projects the point/pair/triple Hasse system to its full-core and
lower-trace F3-bearing coordinates.  It also checks a singleton-zero formal
slice and reproduces the obstruction to a previously proposed local labelled
tail witness.  Singleton-zero is not used as a necessary condition, and no
labelled complement atom or complete ROUTE-A4 sequence is constructed.
"""

from __future__ import annotations

from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from math import comb
from pathlib import Path


P = 7
HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_module("p7_base", HERE / "verify_p7_six_fibre_exclusion.py")
FOUR = load_module("p7_four", HERE / "verify_p7_four_fibre_refinement.py")

EXCEPTIONAL_PROFILE = (0, 0, 0)
PAIR_LOW_PROFILES = {(0, 0, 1), (0, 0, 6)}
ZERO_LOW_PROFILES = {(0, 0, 2), (0, 0, 5), (0, 1, 2)}
NO_LOW_PROFILES = {
    (0, 0, 3),
    (0, 0, 4),
    (0, 1, 3),
    (0, 1, 4),
    (0, 1, 5),
    (0, 2, 4),
}


def is_singleton(star) -> bool:
    length, trace_size, _, _, _ = star
    return length - trace_size == 1


def is_full_f3(star) -> bool:
    _, trace_size, _, _, families = star
    return trace_size == 3 and families == (3,)


def bears_f3(star) -> bool:
    return 3 in star[4]


def solve_with_fixed_values(stars, matrix, rhs, fixed_values):
    """Check exact extension after assigning selected star coordinates."""
    fixed = set(fixed_values)
    adjusted_rhs = [
        (
            target
            - sum(row[column] * value for column, value in fixed_values.items())
        )
        % P
        for row, target in zip(matrix, rhs)
    ]
    keep = [column for column in range(len(stars)) if column not in fixed]
    restricted = [[row[column] for column in keep] for row in matrix]
    consistent, _, solution, certificate = BASE.rref_solve(
        restricted, adjusted_rhs
    )
    assert consistent and solution is not None and certificate is None
    BASE.verify_solution(restricted, adjusted_rhs, solution)


def vec_add(*vectors):
    return tuple(
        sum(vector[index] for vector in vectors) % P for index in range(3)
    )


def vec_scale(scalar, vector):
    return tuple(scalar * value % P for value in vector)


def subset_sum(labels, subset):
    return vec_add(*(labels[index] for index in subset))


def audit_profiles():
    profiles = BASE.height_profiles(3)
    assert profiles == [
        (0, 0, 0),
        (0, 0, 1),
        (0, 0, 2),
        (0, 0, 3),
        (0, 0, 4),
        (0, 0, 5),
        (0, 0, 6),
        (0, 1, 2),
        (0, 1, 3),
        (0, 1, 4),
        (0, 1, 5),
        (0, 2, 4),
    ]

    classes = Counter()
    low_counts = Counter()
    singleton_counts = Counter()

    for profile in profiles:
        stars, matrix, rhs, _ = BASE.build_hasse_system(profile)
        consistent, rank, solution, certificate = BASE.rref_solve(matrix, rhs)
        assert consistent and solution is not None and certificate is None
        BASE.verify_solution(matrix, rhs, solution)
        classes[(len(stars), rank)] += 1

        singleton_columns = [
            column for column, star in enumerate(stars) if is_singleton(star)
        ]
        full_columns = [
            column for column, star in enumerate(stars) if is_full_f3(star)
        ]
        low_columns = [
            column
            for column, star in enumerate(stars)
            if bears_f3(star) and star[1] < 3
        ]
        all_f3_columns = [
            column for column, star in enumerate(stars) if bears_f3(star)
        ]

        singleton_counts[len(singleton_columns)] += 1
        low_counts[len(low_columns)] += 1
        assert [stars[column][0] for column in full_columns] == [6, 7, 8]

        # This is only a deliberately restricted formal slice.  It is not
        # treated as a necessary condition on real singleton tails.
        assert FOUR.solve_after_zeroing(
            stars, matrix, rhs, singleton_columns
        )[0]

        full_projection = FOUR.affine_projection(
            stars, matrix, rhs, full_columns
        )
        low_projection = (
            FOUR.affine_projection(stars, matrix, rhs, low_columns)
            if low_columns
            else []
        )

        if profile == EXCEPTIONAL_PROFILE:
            assert full_projection == []
            assert low_projection == []
            assert [
                (stars[column][0], stars[column][1], stars[column][2])
                for column in low_columns
            ] == [
                (6, 1, 3),
                (6, 2, 3),
                (7, 1, 3),
                (7, 2, 3),
                (8, 1, 3),
                (8, 2, 3),
            ]
            all_f3_projection = FOUR.affine_projection(
                stars, matrix, rhs, all_f3_columns
            )
            assert all_f3_projection == [
                ([1, 2, 1, 6, 5, 6, 1, 2, 1], 6)
            ]
            conditional_low = FOUR.affine_projection(
                stars, matrix, rhs, low_columns, full_columns
            )
            assert conditional_low == [([1, 2, 6, 5, 1, 2], 6)]

            # Full core and singletons zero; only (ell,b,c)=(6,2,3)
            # survives among the F3-bearing columns, with residue three.
            selected = next(
                column
                for column in low_columns
                if stars[column][:3] == (6, 2, 3)
            )
            fixed = {
                column: 0
                for column in singleton_columns + all_f3_columns
            }
            fixed[selected] = 3
            solve_with_fixed_values(stars, matrix, rhs, fixed)
            continue

        assert full_projection == [([1, 6, 1], 6)]
        if profile in PAIR_LOW_PROFILES:
            assert len(low_columns) == 4
            assert low_projection == [
                ([1, 0, 6, 0], 0),
                ([0, 1, 0, 6], 0),
            ]
        elif profile in ZERO_LOW_PROFILES:
            assert len(low_columns) == 2
            assert low_projection == [([1, 0], 0), ([0, 1], 0)]
        else:
            assert profile in NO_LOW_PROFILES
            assert low_columns == []

        # No full-tail length is forced in the formal Hasse system.  All
        # singletons and all other F3-bearing columns can be zero while the
        # length-seven full-core column is one.
        selected = next(
            column for column in full_columns if stars[column][0] == 7
        )
        fixed = {
            column: 0
            for column in singleton_columns + all_f3_columns
        }
        fixed[selected] = 1
        solve_with_fixed_values(stars, matrix, rhs, fixed)

    assert classes == {(10, 3): 6, (12, 5): 3, (20, 7): 2, (33, 6): 1}
    assert low_counts == {0: 6, 2: 3, 4: 2, 6: 1}
    assert singleton_counts == {2: 11, 4: 1}

    capacities = {
        tail_size: min(
            comb(22, tail_size) - comb(22 - t_size, tail_size)
            for t_size in (6, 7, 8)
        )
        for tail_size in range(1, 8)
    }
    assert capacities == {
        1: 6,
        2: 111,
        3: 980,
        4: 5495,
        5: 21966,
        6: 66605,
        7: 159104,
    }
    return profiles, classes, low_counts, capacities


def verify_nonexceptional_single_tail_arithmetic(profile):
    """Check one designated F3 tail, without claiming global compatibility."""
    q = (1, 0, 0)
    labels = {
        "t": (0, 1, 0),
        "u1": (0, 0, 1),
        "u2": (0, 0, 2),
        "u3": (4, 6, 4),
    }
    heights = {
        "t": 0,
        "u1": 0,
        "u2": 0,
        "u3": (3 - sum(profile)) % P,
    }
    tail = frozenset(labels)
    assert subset_sum(labels, tail) == vec_scale(-3, q)
    assert labels["t"] != (0, 0, 0)
    assert sum(heights[index] for index in tail) % P == (
        3 - sum(profile)
    ) % P
    assert vec_add(vec_scale(3, q), subset_sum(labels, tail)) == (0, 0, 0)
    assert (sum(profile) + sum(heights.values())) % P == 3

    actual_values = [(q, height) for height in profile]
    actual_values.extend((labels[index], heights[index]) for index in tail)
    assert max(Counter(actual_values).values()) <= 3


def verify_exceptional_candidate_failure():
    """Reproduce the fatal extra-block collision in the three-tail candidate."""
    q = (1, 0, 0)
    labels = {
        "t": (0, 1, 0),
        "a1": (0, 0, 1),
        "a2": (0, 0, 2),
        "a3": (5, 6, 4),
        "b1": (0, 0, 3),
        "b2": (0, 0, 4),
        "b3": (5, 6, 0),
        "c1": (0, 0, 5),
        "c2": (0, 0, 6),
        "c3": (5, 6, 3),
    }
    tails = [
        frozenset({"t", "a1", "a2", "a3"}),
        frozenset({"t", "b1", "b2", "b3"}),
        frozenset({"t", "c1", "c2", "c3"}),
    ]
    heights = {index: 0 for index in labels}
    heights["a1"] = heights["b1"] = heights["c1"] = 3

    for tail in tails:
        assert subset_sum(labels, tail) == vec_scale(-2, q)
        assert tail & {"t"} == {"t"}
        assert subset_sum(labels, tail & {"t"}) == labels["t"]
        assert sum(heights[index] for index in tail) % P == 3

    actual_values = [(q, 0)] * 3
    actual_values.extend(
        (labels[index], heights[index]) for index in labels
    )
    assert max(Counter(actual_values).values()) <= 3

    # The three designated tails are not a compatible labelled witness.
    # Their assigned positions force two additional length-six F3 blocks.
    all_labels = {
        "x1": q,
        "x2": q,
        "x3": q,
        **labels,
    }
    all_heights = {
        "x1": 0,
        "x2": 0,
        "x3": 0,
        **heights,
    }
    first_block = frozenset({"x1", "x2", "t", "a1", "b3", "c2"})
    second_block = frozenset({"x1", "x2", "t", "a2", "b3", "c1"})
    assert first_block != second_block
    for block in (first_block, second_block):
        assert len(block) == 6
        assert subset_sum(all_labels, block) == (0, 0, 0)
        assert sum(all_heights[index] for index in block) % P == 3
    block_intersection = first_block & second_block
    assert block_intersection == frozenset({"x1", "x2", "t", "b3"})
    assert subset_sum(all_labels, block_intersection) == (0, 0, 0)


def main() -> None:
    profiles, classes, low_counts, capacities = audit_profiles()
    for profile in profiles:
        if profile != EXCEPTIONAL_PROFILE:
            verify_nonexceptional_single_tail_arithmetic(profile)
    verify_exceptional_candidate_failure()

    print("PASS exact p=7, m=3 affine star projections")
    print("11/12 profiles force a full-core F3 tail")
    print("full-core residues: N_6 - N_7 + N_8 = 6 (mod 7)")
    print("000 all-F3 coefficients: 1,2,1,-1,-2,-1,1,2,1; rhs 6")
    print(f"system classes: {dict(sorted(classes.items()))}")
    print(f"lower-trace F3 column counts: {dict(sorted(low_counts.items()))}")
    print(f"raw meet-T capacities for tail sizes 1--7: {capacities}")
    print("PASS singleton-zero formal slices and raw capacity arithmetic")
    print("EXPECTED REJECTION: old three-tail labels induce two extra F3 blocks")
    print("EXPECTED REJECTION: their intersection has quotient sum zero")
    print("LABEL STATUS: unresolved; the former three-tail witness is invalid")
    print(
        "SCOPE: singleton-zero is a formal slice; no complement atom or "
        "complete ROUTE-A4 model is constructed"
    )


if __name__ == "__main__":
    main()
