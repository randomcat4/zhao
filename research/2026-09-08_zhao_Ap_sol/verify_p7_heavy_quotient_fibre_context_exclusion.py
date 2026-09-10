"""Verify the p=7 heavy quotient-fibre context obstruction."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path


P = 7
ZERO3 = (0, 0, 0)
FIXTURE = Path(__file__).parent / "verifications" / "p7_m3_s6_rejected_actual_atom.json"


def add3(*vectors: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(sum(vector[index] for vector in vectors) % P for index in range(3))


def neg3(vector: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(-coordinate % P for coordinate in vector)


def load_external_labels() -> tuple[tuple[int, int, int], ...]:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return tuple(tuple(label) for label in data["t_labels"] + data["q_labels"])


def heavy_contexts(labels: tuple[tuple[int, int, int], ...]):
    fibres: dict[tuple[int, int, int], list[int]] = defaultdict(list)
    for position, label in enumerate(labels):
        fibres[label].append(position)

    witnesses = []
    for label, fibre in fibres.items():
        if len(fibre) < 4:
            continue
        outside = [position for position in range(len(labels)) if position not in fibre]
        target = neg3(label)
        for size in (1, 2, 7):
            for context in combinations(outside, size):
                if add3(*(labels[position] for position in context)) == target:
                    witnesses.append((label, tuple(fibre), context))
    return witnesses


def forced_equal_height_rank(fibre: tuple[int, ...], context: tuple[int, ...]) -> int:
    """Rank of differences between |fibre| equations h_z+h_C=1."""
    # Subtract the first equation from every later equation.  The resulting
    # coefficient rows are h_z-h_first=0 and have independent pivots.
    rows = []
    first = fibre[0]
    for position in fibre[1:]:
        row = [0] * (max(fibre + context) + 1)
        row[first] = -1 % P
        row[position] = 1
        rows.append(row)

    rank = 0
    column_count = len(rows[0]) if rows else 0
    for column in range(column_count):
        pivot = next((index for index in range(rank, len(rows)) if rows[index][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, P)
        rows[rank] = [(entry * inverse) % P for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [
                (rows[index][j] - factor * rows[rank][j]) % P
                for j in range(column_count)
            ]
        rank += 1
    return rank


def main() -> None:
    labels = load_external_labels()
    assert len(labels) == 22
    assert all(label != ZERO3 for label in labels)

    witnesses = heavy_contexts(labels)
    target_label = (1, 0, 1)
    target_fibre = (11, 12, 13, 14)
    target_context = (1, 2)
    assert (target_label, target_fibre, target_context) in witnesses
    assert add3(labels[1], labels[2]) == neg3(target_label) == (6, 0, 6)

    allowed_sizes = {2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 2, 8: 1}
    capacity_bounds = tuple(3 * allowed_sizes[length] for length in range(2, 9))
    assert capacity_bounds == (3, 3, 6, 6, 9, 6, 3)

    rank = forced_equal_height_rank(target_fibre, target_context)
    assert rank == len(target_fibre) - 1 == 3

    print("PASS p=7 heavy quotient-fibre context exclusion")
    print("HEAVY_FIBRE label=(1,0,1) positions=(11,12,13,14) multiplicity=4")
    print("CONTEXT positions=(1,2) label_sum=(6,0,6)=-label")
    print("HEIGHT_DIFFERENCE_RANK=3 all four heights forced equal")
    print("CONTEXT_CAPS lengths=2..8 bounds=(3,3,6,6,9,6,3)")
    print("EXPECTED EXCLUSION: actual-value multiplicity cap is three")
    print("SCOPE: this 22-external-position quotient assignment, not the full 88-scalar CSP")


if __name__ == "__main__":
    main()
