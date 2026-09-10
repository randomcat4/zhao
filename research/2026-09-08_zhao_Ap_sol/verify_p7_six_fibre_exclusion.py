#!/usr/bin/env python3
"""Exact F_7 audit for proofs/p7_six_fibre_exclusion.md.

The script enumerates height multisets in quotient fibres of sizes three
through six, modulo height translation and permutation.  For every profile
it constructs all relaxed remainder stars allowed by (SQ) and the short
positive-length windows, then builds the point, pair, and triple Hasse system.
Every one of the 104 size-six profiles is inconsistent.  Every size-five
profile becomes inconsistent after imposing the actual multiplicity bound on
singleton remainders.

For comparison, the bounded-singleton system is consistent for every height
profile of size three or four, even with all singleton-star counts set to
zero.  Those consistent systems are formal finite-field star-count models
only: they do not construct quotient labels, actual remainder subsets, a
complement atom, or a ROUTE-A4 sequence.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, combinations_with_replacement, product


P = 7
LENGTH_WINDOWS = {
    2: frozenset({1}),
    3: frozenset({1}),
    4: frozenset({1, 2}),
    5: frozenset({1, 2}),
    6: frozenset({1, 2, 3}),
    7: frozenset({2, 3}),
    8: frozenset({3}),
}

EXPECTED_PROFILE_COUNTS = {3: 12, 4: 29, 5: 59, 6: 104}
EXPECTED_MINIMUM_TRACE_COUNTS = {
    3: {3: 12},
    4: {3: 9, 4: 20},
    5: {3: 3, 4: 7, 5: 49},
    6: {4: 1, 5: 8, 6: 95},
}
EXPECTED_SYSTEM_CLASSES = {
    3: {(10, 3): 6, (12, 5): 3, (20, 7): 2, (33, 6): 1},
    4: {(8, 3): 20, (10, 5): 3, (11, 6): 3, (19, 8): 1, (23, 8): 2},
    5: {(6, 3): 49, (8, 5): 7, (10, 7): 1, (17, 9): 2},
    6: {(3, 2): 95, (5, 4): 8, (13, 8): 1},
}

# The nine profiles admitting a trace smaller than six.  Each listed row
# combination annihilates every admissible-star column and has right side 1.
SPARSE_CERTIFICATES = {
    (0, 0, 0, 1, 1, 2): (("P1(5)", 1),),
    (0, 0, 0, 1, 1, 6): (("P1(1)", 6), ("P1(4)", 2)),
    (0, 0, 0, 1, 2, 2): (("P1(3)", 6), ("P1(4)", 2)),
    (0, 0, 0, 1, 6, 6): (
        ("P1(1)", 2),
        ("P1(4)", 6),
        ("P2(0)", 1),
        ("P2(3)", 6),
    ),
    (0, 0, 0, 2, 2, 2): (("P1(3)", 3), ("P2(0)", 6), ("Q1(01)", 2)),
    (0, 0, 0, 5, 5, 6): (("P1(1)", 3), ("P1(5)", 5)),
    (0, 0, 0, 5, 6, 6): (("P1(1)", 3), ("P1(4)", 5)),
    (0, 0, 1, 1, 2, 2): (("P1(2)", 6), ("P1(4)", 2)),
    (0, 0, 0, 1, 1, 1): (
        ("P1(0)", 1),
        ("P1(3)", 3),
        ("P2(3)", 6),
        ("P3(0)", 2),
        ("Q1(01)", 6),
        ("Q1(34)", 5),
        ("T(012)", 2),
    ),
}


def canonical_profile(profile: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize a height multiset under common translation."""
    return min(
        tuple(sorted((height + shift) % P for height in profile))
        for shift in range(P)
    )


def height_profiles(size: int) -> list[tuple[int, ...]]:
    """Profiles with actual-height multiplicity at most three."""
    raw = [
        profile
        for profile in combinations_with_replacement(range(P), size)
        if max(Counter(profile).values()) <= 3
    ]
    profiles = sorted({canonical_profile(profile) for profile in raw})
    # No multiset of size < 7 is invariant under a nonzero translation.
    assert len(raw) == P * len(profiles)
    return profiles


def admissible_stars(profile: tuple[int, ...]):
    """Return every relaxed (length, trace size, remainder height) star.

    A star contains one block for every trace of the fixed size.  The final
    two entries record those traces and their resulting families.
    """
    size = len(profile)
    points = tuple(range(size))
    stars = []
    for length in range(2, 9):
        for trace_size in range(1, min(size, length - 1) + 1):
            traces = tuple(combinations(points, trace_size))
            trace_sums = tuple(
                sum(profile[index] for index in trace) % P for trace in traces
            )
            for remainder_height in range(P):
                families = tuple(
                    (value + remainder_height) % P for value in trace_sums
                )
                if all(family in LENGTH_WINDOWS[length] for family in families):
                    stars.append(
                        (
                            length,
                            trace_size,
                            remainder_height,
                            traces,
                            families,
                        )
                    )
    return stars


def minimum_triple_trace(profile: tuple[int, ...]) -> int:
    traces = [
        trace_size
        for _, trace_size, _, _, _ in admissible_stars(profile)
        if trace_size >= 3
    ]
    assert traces
    return min(traces)


def build_hasse_system(profile: tuple[int, ...]):
    """Build the relaxed star-count Hasse system over F_7."""
    size = len(profile)
    points = tuple(range(size))
    pairs = tuple(combinations(points, 2))
    triples = tuple(combinations(points, 3))
    stars = admissible_stars(profile)
    matrix: list[list[int]] = []
    rhs: list[int] = []
    labels: list[str] = []

    # Each family's signed point degree is 1 modulo 7.
    for family in (1, 2, 3):
        for point in points:
            row = []
            for length, _, _, traces, families in stars:
                value = sum(
                    (-1) ** (length - 1)
                    for trace, current_family in zip(traces, families)
                    if point in trace and current_family == family
                )
                row.append(value % P)
            matrix.append(row)
            rhs.append(1)
            labels.append(f"P{family}({point})")

    # d_1 + 3 d_2 = 3 and 2 d_1 - 3 d_3 = 1 modulo 7.
    first_pair_weights = {1: 1, 2: 3, 3: 0}
    second_pair_weights = {1: 2, 2: 0, 3: -3}
    for first, second in pairs:
        for name, weights, target in (
            ("Q1", first_pair_weights, 3),
            ("Q2", second_pair_weights, 1),
        ):
            row = []
            for length, _, _, traces, families in stars:
                value = sum(
                    (-1) ** length * weights[family]
                    for trace, family in zip(traces, families)
                    if first in trace and second in trace
                )
                row.append(value % P)
            matrix.append(row)
            rhs.append(target)
            labels.append(f"{name}({first}{second})")

    # 4 delta_1 + 3 delta_2 + 6 delta_3 = 6 modulo 7.
    triple_weights = {1: 4, 2: 3, 3: 6}
    for triple in triples:
        fixed = frozenset(triple)
        row = []
        for length, _, _, traces, families in stars:
            value = sum(
                (-1) ** (length - 1) * triple_weights[family]
                for trace, family in zip(traces, families)
                if fixed.issubset(trace)
            )
            row.append(value % P)
        matrix.append(row)
        rhs.append(6)
        labels.append(f"T({''.join(map(str, triple))})")

    expected_rows = 3 * size + 2 * len(pairs) + len(triples)
    assert len(matrix) == len(rhs) == len(labels) == expected_rows
    return stars, matrix, rhs, labels


def rref_solve(matrix: list[list[int]], rhs: list[int]):
    """Return consistency, rank, one solution, and a contradiction witness."""
    row_count = len(matrix)
    column_count = len(matrix[0]) if matrix else 0
    augmented = [
        [value % P for value in row] + [target % P]
        for row, target in zip(matrix, rhs)
    ]
    transform = [
        [int(row == column) for column in range(row_count)]
        for row in range(row_count)
    ]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
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
        transform[pivot_row], transform[selected] = (
            transform[selected],
            transform[pivot_row],
        )
        inverse = pow(augmented[pivot_row][column], -1, P)
        augmented[pivot_row] = [
            value * inverse % P for value in augmented[pivot_row]
        ]
        transform[pivot_row] = [
            value * inverse % P for value in transform[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not augmented[row][column]:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                (value - factor * pivot) % P
                for value, pivot in zip(augmented[row], augmented[pivot_row])
            ]
            transform[row] = [
                (value - factor * pivot) % P
                for value, pivot in zip(transform[row], transform[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    bad_row = next(
        (
            row
            for row in range(row_count)
            if all(value == 0 for value in augmented[row][:-1])
            and augmented[row][-1]
        ),
        None,
    )
    if bad_row is not None:
        inverse = pow(augmented[bad_row][-1], -1, P)
        certificate = [
            value * inverse % P for value in transform[bad_row]
        ]
        return False, len(pivots), None, certificate

    solution = [0] * column_count
    for row, column in enumerate(pivots):
        solution[column] = augmented[row][-1]
    return True, len(pivots), solution, None


def dot(left: list[int], right: list[int]) -> int:
    return sum(first * second for first, second in zip(left, right)) % P


def verify_solution(
    matrix: list[list[int]], rhs: list[int], solution: list[int]
) -> None:
    assert all(dot(row, solution) == target % P for row, target in zip(matrix, rhs))


def verify_certificate(
    matrix: list[list[int]], rhs: list[int], certificate: list[int]
) -> None:
    column_count = len(matrix[0]) if matrix else 0
    for column in range(column_count):
        assert sum(
            certificate[row] * matrix[row][column] for row in range(len(matrix))
        ) % P == 0
    assert dot(certificate, rhs) == 1


def verify_sparse_certificate(
    matrix: list[list[int]],
    rhs: list[int],
    labels: list[str],
    sparse: tuple[tuple[str, int], ...],
) -> None:
    row_index = {label: index for index, label in enumerate(labels)}
    certificate = [0] * len(labels)
    for label, value in sparse:
        certificate[row_index[label]] = value
    verify_certificate(matrix, rhs, certificate)


def solve_with_singleton_bounds(stars, matrix, rhs):
    """Solve after restricting singleton-remainder counts to 0,1,2,3.

    A singleton remainder belongs to T and all remainders in one star column
    are the same actual group value.  Thus the global actual multiplicity cap
    gives the stated integer, hence residue, bound.
    """
    singleton_columns = [
        column
        for column, (length, trace_size, _, _, _) in enumerate(stars)
        if length - trace_size == 1
    ]
    other_columns = [
        column for column in range(len(stars)) if column not in singleton_columns
    ]
    restricted_matrix = [
        [row[column] for column in other_columns] for row in matrix
    ]
    for values in product(range(4), repeat=len(singleton_columns)):
        restricted_rhs = [
            (
                target
                - sum(
                    row[column] * value
                    for column, value in zip(singleton_columns, values)
                )
            )
            % P
            for row, target in zip(matrix, rhs)
        ]
        consistent, _, solution, certificate = rref_solve(
            restricted_matrix, restricted_rhs
        )
        if consistent:
            assert solution is not None and certificate is None
            full_solution = [0] * len(stars)
            for column, value in zip(singleton_columns, values):
                full_solution[column] = value
            for column, value in zip(other_columns, solution):
                full_solution[column] = value
            verify_solution(matrix, rhs, full_solution)
            return full_solution, len(singleton_columns)
        assert solution is None and certificate is not None
        verify_certificate(restricted_matrix, restricted_rhs, certificate)
    return None, len(singleton_columns)


def audit_profiles():
    profile_counts = {}
    minimum_trace_counts = {}
    system_classes = {}
    consistent_counts = {}
    bounded_singleton_counts = {}
    singleton_column_classes = {}

    for size in range(3, 7):
        profiles = height_profiles(size)
        profile_counts[size] = len(profiles)
        trace_counter = Counter(minimum_triple_trace(profile) for profile in profiles)
        minimum_trace_counts[size] = dict(sorted(trace_counter.items()))
        class_counter: Counter[tuple[int, int]] = Counter()
        singleton_counter: Counter[int] = Counter()
        consistent = 0
        bounded_singleton_consistent = 0

        for profile in profiles:
            stars, matrix, rhs, labels = build_hasse_system(profile)
            is_consistent, rank, solution, certificate = rref_solve(matrix, rhs)
            class_counter[(len(stars), rank)] += 1
            if is_consistent:
                assert solution is not None and certificate is None
                verify_solution(matrix, rhs, solution)
                consistent += 1
            else:
                assert solution is None and certificate is not None
                verify_certificate(matrix, rhs, certificate)

            if size == 6:
                assert not is_consistent
                if minimum_triple_trace(profile) == 6:
                    # These 95 profiles have only the three full-trace stars;
                    # none contains an F1 block, so every P1 row is 0 = 1.
                    assert len(stars) == 3
                    assert all(
                        family != 1
                        for _, _, _, _, families in stars
                        for family in families
                    )
                else:
                    verify_sparse_certificate(
                        matrix, rhs, labels, SPARSE_CERTIFICATES[profile]
                    )

            if size <= 5:
                bounded_solution, singleton_count = solve_with_singleton_bounds(
                    stars, matrix, rhs
                )
                singleton_counter[singleton_count] += 1
                if bounded_solution is not None:
                    bounded_singleton_consistent += 1
                    if size <= 4:
                        # The stopping line is stronger than mere bounded
                        # consistency: no singleton remainder is needed.
                        assert all(
                            bounded_solution[column] == 0
                            for column, (length, trace_size, _, _, _) in enumerate(stars)
                            if length - trace_size == 1
                        )

        system_classes[size] = dict(sorted(class_counter.items()))
        consistent_counts[size] = consistent
        if size <= 5:
            bounded_singleton_counts[size] = bounded_singleton_consistent
            singleton_column_classes[size] = dict(sorted(singleton_counter.items()))

    assert profile_counts == EXPECTED_PROFILE_COUNTS
    assert minimum_trace_counts == EXPECTED_MINIMUM_TRACE_COUNTS
    assert system_classes == EXPECTED_SYSTEM_CLASSES
    assert consistent_counts == {3: 12, 4: 29, 5: 59, 6: 0}
    assert bounded_singleton_counts == {3: 12, 4: 29, 5: 0}
    assert singleton_column_classes == {
        3: {2: 11, 4: 1},
        4: {2: 26, 3: 3},
        5: {3: 57, 4: 2},
    }
    assert set(SPARSE_CERTIFICATES) == {
        profile
        for profile in height_profiles(6)
        if minimum_triple_trace(profile) < 6
    }
    return (
        profile_counts,
        minimum_trace_counts,
        system_classes,
        consistent_counts,
        bounded_singleton_counts,
        singleton_column_classes,
    )


def main() -> None:
    profiles, traces, classes, consistent, bounded, singleton_classes = audit_profiles()
    print("PASS p=7 high-fibre exclusion: multiplicities five and six are impossible")
    print(f"profile orbit counts: {profiles}")
    print(f"minimum trace-size classes: {traces}")
    print(f"(admissible stars, rank) classes: {classes}")
    print(f"consistent relaxed Hasse systems: {consistent}")
    print(f"consistent after singleton actual-cap bounds: {bounded}")
    print(f"singleton-column classes: {singleton_classes}")
    print(
        "SCOPE: sizes 3--4 are formal F_7 star-count solutions only; "
        "they are not labelled atoms or ROUTE-A4 models"
    )


if __name__ == "__main__":
    main()
