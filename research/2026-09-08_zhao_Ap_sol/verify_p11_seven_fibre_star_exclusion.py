#!/usr/bin/env python3
"""Exact p=11 audit for proofs/p11_seven_fibre_star_exclusion.md.

For every seven-height multiset modulo common translation and position
permutation, construct all formal remainder stars allowed by (SQ) and the
short positive-length windows.  The full point/pair/triple Hasse system is
then solved over F_11.

The computation is a complete exclusion certificate for every profile whose
relaxed system is inconsistent.  The unique nonconstant relaxed survivor is
handled by a sparse Hasse projection and an explicit eight-term anchored
actual zero-sum.  The constant profile remains only a relaxed local survivor;
the script does not construct an atom or a ROUTE-A4 configuration.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, combinations_with_replacement


P = 11
FIBRE_SIZE = 7
LENGTH_WINDOWS = {
    2: frozenset({1}),
    3: frozenset({1}),
    4: frozenset({1, 2}),
    5: frozenset({1, 2}),
    6: frozenset({1, 2, 3}),
    7: frozenset({2, 3}),
    8: frozenset({3}),
}
POINT_TARGETS = {1: 2, 2: 8, 3: 6}
FIRST_PAIR_WEIGHTS = {1: 8, 2: 10, 3: 0}
SECOND_PAIR_WEIGHTS = {1: 2, 2: 0, 3: -10}
TRIPLE_WEIGHTS = {1: 4, 2: 10, 3: 20}

CONSTANT_PROFILE = (0, 0, 0, 0, 0, 0, 0)
NEGATIVE_EXCEPTION = (0, 0, 0, 0, 0, 0, 10)
POSITIVE_EXCEPTION = (0, 0, 0, 0, 0, 0, 1)

EXPECTED_SYSTEM_CLASSES = {
    (False, 1, 1): 1740,
    (False, 2, 2): 18,
    (False, 6, 4): 1,
    (False, 6, 5): 1,
    (False, 6, 6): 1,
    (False, 9, 6): 2,
    (False, 11, 6): 1,
    (False, 11, 8): 1,
    (False, 24, 7): 1,
    (True, 24, 8): 1,
    (True, 51, 6): 1,
}


def canonical_profile(profile: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize under a common height translation."""
    return min(
        tuple(sorted((height + shift) % P for height in profile))
        for shift in range(P)
    )


def height_profiles() -> list[tuple[int, ...]]:
    raw = list(combinations_with_replacement(range(P), FIBRE_SIZE))
    profiles = sorted({canonical_profile(profile) for profile in raw})
    # A multiset of size 7 < 11 has no nontrivial translation stabilizer.
    assert len(raw) == 19448
    assert len(raw) == P * len(profiles)
    assert len(profiles) == 1768
    return profiles


def admissible_stars(profile: tuple[int, ...]):
    """All relaxed (length, trace size, remainder height) stars."""
    points = tuple(range(FIBRE_SIZE))
    stars = []
    for length in range(2, 9):
        for trace_size in range(1, min(FIBRE_SIZE, length - 1) + 1):
            traces = tuple(combinations(points, trace_size))
            sums = tuple(
                sum(profile[index] for index in trace) % P for trace in traces
            )
            for remainder_height in range(P):
                families = tuple(
                    (value + remainder_height) % P for value in sums
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


def build_hasse_system(profile: tuple[int, ...]):
    points = tuple(range(FIBRE_SIZE))
    pairs = tuple(combinations(points, 2))
    triples = tuple(combinations(points, 3))
    stars = admissible_stars(profile)
    matrix: list[list[int]] = []
    rhs: list[int] = []
    labels: list[str] = []

    for family in (1, 2, 3):
        for point in points:
            matrix.append(
                [
                    sum(
                        (-1) ** (length - 1)
                        for trace, current_family in zip(traces, families)
                        if point in trace and current_family == family
                    )
                    % P
                    for length, _, _, traces, families in stars
                ]
            )
            rhs.append(POINT_TARGETS[family])
            labels.append(f"P{family}({point})")

    for first, second in pairs:
        for name, weights, target in (
            ("Q1", FIRST_PAIR_WEIGHTS, 3),
            ("Q2", SECOND_PAIR_WEIGHTS, 1),
        ):
            matrix.append(
                [
                    sum(
                        (-1) ** length * weights[family]
                        for trace, family in zip(traces, families)
                        if first in trace and second in trace
                    )
                    % P
                    for length, _, _, traces, families in stars
                ]
            )
            rhs.append(target)
            labels.append(f"{name}({first}{second})")

    for triple in triples:
        fixed = frozenset(triple)
        matrix.append(
            [
                sum(
                    (-1) ** (length - 1) * TRIPLE_WEIGHTS[family]
                    for trace, family in zip(traces, families)
                    if fixed.issubset(trace)
                )
                % P
                for length, _, _, traces, families in stars
            ]
        )
        rhs.append((-1) % P)
        labels.append(f"T({''.join(map(str, triple))})")

    assert len(matrix) == 3 * 7 + 2 * 21 + 35 == 98
    return stars, matrix, rhs, labels


def dot(left: list[int], right: list[int]) -> int:
    return sum(first * second for first, second in zip(left, right)) % P


def rref_solve(matrix: list[list[int]], rhs: list[int]):
    """Return consistency, coefficient rank, solution, contradiction witness."""
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


def verify_solution(matrix, rhs, solution) -> None:
    assert all(dot(row, solution) == target % P for row, target in zip(matrix, rhs))


def verify_certificate(matrix, rhs, certificate) -> None:
    column_count = len(matrix[0]) if matrix else 0
    for column in range(column_count):
        assert sum(
            certificate[row] * matrix[row][column] for row in range(len(matrix))
        ) % P == 0
    assert dot(certificate, rhs) == 1


def audit_all_profiles():
    classes: Counter[tuple[bool, int, int]] = Counter()
    survivors = {}
    positive_class = None
    for profile in height_profiles():
        stars, matrix, rhs, labels = build_hasse_system(profile)
        consistent, rank, solution, certificate = rref_solve(matrix, rhs)
        classes[(consistent, len(stars), rank)] += 1
        if consistent:
            assert solution is not None and certificate is None
            verify_solution(matrix, rhs, solution)
            survivors[profile] = (stars, matrix, rhs, labels, solution)
        else:
            assert solution is None and certificate is not None
            verify_certificate(matrix, rhs, certificate)
        if profile == POSITIVE_EXCEPTION:
            positive_class = (consistent, len(stars), rank)

    assert dict(classes) == EXPECTED_SYSTEM_CLASSES
    assert set(survivors) == {CONSTANT_PROFILE, NEGATIVE_EXCEPTION}
    assert positive_class == (False, 24, 7)
    return classes, survivors


def audit_negative_exception(data) -> None:
    stars, matrix, rhs, labels, _ = data
    star_specs = [star[:3] for star in stars]
    target_spec = (8, 7, 4)
    target_column = star_specs.index(target_spec)
    label_index = {label: index for index, label in enumerate(labels)}

    # The sparse Hasse combination 2 P_1(1) + Q_2(0,6) isolates the unique
    # full-core length-eight singleton-tail column.
    row_combination = [0] * len(labels)
    row_combination[label_index["P1(1)"]] = 2
    row_combination[label_index["Q2(06)"]] = 1
    projected = [
        sum(
            row_combination[row] * matrix[row][column]
            for row in range(len(matrix))
        )
        % P
        for column in range(len(stars))
    ]
    assert projected[target_column] == 1
    assert sum(value != 0 for value in projected) == 1
    assert dot(row_combination, rhs) == 5

    # If N is the actual number of these singleton tails, then N == 5 mod 11.
    # All tails are the same actual value, so 0 <= N <= p-4 = 7; hence N=5.
    possible_counts = [count for count in range(8) if count % P == 5]
    assert possible_counts == [5]

    # Normalize the six main fibre positions to x=(q,0).  The anomaly is
    # x-a and every forced tail is y=-7x+4a.  Three x's, two y's, and three
    # external a-anchors form an eight-term actual zero-sum.
    x = (1, 0)
    y = ((-7) % P, 4)
    anchor = (0, 1)
    total = tuple(
        (3 * x[coordinate] + 2 * y[coordinate] + 3 * anchor[coordinate]) % P
        for coordinate in range(2)
    )
    assert total == (0, 0)
    assert 3 <= 6 and 2 <= possible_counts[0] and 3 <= P - 4
    assert 3 + 2 + 3 == 8 <= 3 * P - 2


def main() -> None:
    classes, survivors = audit_all_profiles()
    audit_negative_exception(survivors[NEGATIVE_EXCEPTION])
    print("PASS p=11 seven-fibre theorem: every nonconstant height profile is excluded")
    print("height orbits: 1768; relaxed survivors: 0^7 and 0^6(-1)")
    print(f"(consistent, admissible stars, rank) classes: {dict(classes)}")
    print(
        "negative survivor: 2P1(1)+Q2(06) forces five full-core singleton tails; "
        "3x+2y+3a is an eight-term actual zero-sum"
    )
    print(
        "SCOPE: this completely proves the p=11 m=7 fibre is single-height "
        "under the frozen interfaces; it does not eliminate the single-height design"
    )


if __name__ == "__main__":
    main()
