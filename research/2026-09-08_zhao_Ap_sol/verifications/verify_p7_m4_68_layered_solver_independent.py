#!/usr/bin/env python3
"""Independent replay of the radius-two p=7,m=4 quotient certificate.

This checker deliberately does not import the layered solver.  Mutation
neighbours are generated from value-pair multiplicities and unordered
replacement pairs, unlike the solver's position-pair/ordered-first-label
enumeration.  Atomicity and fixed-cardinality spectra are also recomputed by
fresh tuple-valued dynamic programs.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path


P = 7
ZERO = (0, 0, 0)
ALL = tuple(product(range(P), repeat=3))
ALL_NONZERO = tuple(value for value in ALL if value != ZERO)
VECTOR_ID = {value: index for index, value in enumerate(ALL)}


def add(left, right):
    return tuple((left[i] + right[i]) % P for i in range(3))


def neg(value):
    return tuple((-entry) % P for entry in value)


# Integer addition table for the independent atom DP.  It is built here from
# the tuple definition rather than imported from either search implementation.
ADD_ID = tuple(
    tuple(VECTOR_ID[add(left, right)] for right in ALL)
    for left in ALL
)


def expanded(entries):
    return tuple(sorted(value for value, count in entries for _ in range(count)))


BASE_B = expanded(
    (
        ((1, 0, 0), 3),
        ((0, 0, 1), 1),
        ((0, 1, 0), 1),
        ((0, 1, 6), 3),
        ((1, 0, 1), 4),
        ((1, 5, 1), 1),
        ((1, 6, 1), 4),
        ((4, 5, 3), 1),
        ((5, 4, 4), 1),
    )
)

EXPECTED_ATOM_COUNTS = (1, 8, 530)
EXPECTED_ATOM_HASHES = (
    "53d459902b63737338d05bc7cf8db1accd7a515615c7031e0116dd0c4ca7df49",
    "0b29f69959a8d85fc1a6b573b15b98dc13f44ca8577e491875398810dbaa82e2",
    "d5f2f8479040c178176882ec86d8f8dbb498d22a987c60ef58a1ba146e08791d",
)
EXPECTED_CANDIDATE_COUNTS = (6840, 43923)
EXPECTED_CANDIDATE_HASHES = (
    "a123ad016325cbef71acb4da4fd69f662fa8056c9e74ea4c02703c22c3866ad9",
    "6e9f25f3f813001acb3605154e019fa8eef50d65058a9f01520b77b4ad613f92",
)
EXPECTED_POINTED_BY_DEPTH = (2, 10, 8)
EXPECTED_UNPOINTED_ATOMS_BY_DEPTH = (1, 5, 4)
EXPECTED_REPORT_SHA256 = (
    "481cf1f7bdcd9b36b08221b1ad99b0f3da9c1be2eda64e3effd24ec0861e699e"
)


def payload(collection):
    serial = [[list(value) for value in sequence] for sequence in sorted(collection)]
    return json.dumps(serial, separators=(",", ":")).encode("ascii")


def digest(collection):
    return hashlib.sha256(payload(collection)).hexdigest()


def replacement_pairs_by_sum():
    result = {value: [] for value in ALL}
    for first_index, first in enumerate(ALL):
        for second in ALL[first_index:]:
            result[add(first, second)].append((first, second))
    return result


REPLACEMENTS = replacement_pairs_by_sum()


def remove_pair(counter, first, second):
    updated = counter.copy()
    updated[first] -= 1
    updated[second] -= 1
    if updated[first] == 0:
        del updated[first]
    if second in updated and updated[second] == 0:
        del updated[second]
    return updated


def mutation_candidates(atom):
    counter = Counter(atom)
    removed_pairs = set(combinations(atom, 2))
    answer = set()
    for first, second in removed_pairs:
        remainder = remove_pair(counter, first, second)
        target = add(first, second)
        for new_first, new_second in REPLACEMENTS[target]:
            new_counter = remainder.copy()
            new_counter[new_first] += 1
            new_counter[new_second] += 1
            candidate = tuple(
                sorted(
                    value
                    for value, count in new_counter.items()
                    for _ in range(count)
                )
            )
            if candidate != atom:
                answer.add(candidate)
    return answer


def sum_all(values):
    total = ZERO
    for value in values:
        total = add(total, value)
    return total


def is_atom(atom):
    if len(atom) != 19 or sum_all(atom) != ZERO:
        return False
    zero_id = VECTOR_ID[ZERO]
    layers = [set() for _ in range(10)]
    layers[0].add(zero_id)
    for position, value in enumerate(atom):
        value_id = VECTOR_ID[value]
        for size in range(min(9, position + 1), 0, -1):
            layers[size].update(
                ADD_ID[previous][value_id] for previous in layers[size - 1]
            )
        if any(
            zero_id in layers[size]
            for size in range(1, min(9, position + 1) + 1)
        ):
            return False
    return True


def supports(atom, maximum=15):
    layers = [set() for _ in range(maximum + 1)]
    layers[0].add(ZERO)
    for position, value in enumerate(atom):
        for size in range(min(maximum, position + 1), 0, -1):
            layers[size].update(add(previous, value) for previous in layers[size - 1])
    return tuple(frozenset(layer) for layer in layers)


def exact_radius_two():
    seen = {BASE_B}
    frontier = {BASE_B}
    layers = [tuple(sorted(frontier))]
    candidate_counts = []
    candidate_hashes = []
    for _ in range(2):
        candidates = set()
        for atom in sorted(frontier):
            candidates.update(mutation_candidates(atom))
        candidate_counts.append(len(candidates))
        candidate_hashes.append(digest(candidates))
        frontier = {
            candidate
            for candidate in candidates
            if candidate not in seen and is_atom(candidate)
        }
        seen.update(frontier)
        layers.append(tuple(sorted(frontier)))
    return tuple(layers), tuple(candidate_counts), tuple(candidate_hashes)


def check_pointed(layers):
    pointed_by_depth = []
    unpointed_atoms_by_depth = []
    for atoms in layers:
        pointed = 0
        unpointed = 0
        for atom in atoms:
            counts = Counter(atom)
            if max(counts.values()) > 4:
                continue
            four_values = tuple(value for value, count in counts.items() if count == 4)
            if not four_values:
                continue
            unpointed += 1
            spectrum = supports(atom)
            middle = frozenset().union(*(spectrum[size] for size in range(8, 16)))
            escape = tuple(
                value for value in ALL_NONZERO if neg(value) not in middle
            )
            assert escape == ()
            pointed += len(four_values)
        pointed_by_depth.append(pointed)
        unpointed_atoms_by_depth.append(unpointed)
    return tuple(pointed_by_depth), tuple(unpointed_atoms_by_depth)


def main():
    layers, candidate_counts, candidate_hashes = exact_radius_two()
    atom_counts = tuple(len(layer) for layer in layers)
    atom_hashes = tuple(digest(layer) for layer in layers)
    assert atom_counts == EXPECTED_ATOM_COUNTS
    assert atom_hashes == EXPECTED_ATOM_HASHES
    assert candidate_counts == EXPECTED_CANDIDATE_COUNTS
    assert candidate_hashes == EXPECTED_CANDIDATE_HASHES

    pointed, unpointed = check_pointed(layers)
    assert pointed == EXPECTED_POINTED_BY_DEPTH
    assert unpointed == EXPECTED_UNPOINTED_ATOMS_BY_DEPTH

    report = Path(__file__).with_name("p7_m4_68_layered_solver_report.json")
    assert hashlib.sha256(report.read_bytes()).hexdigest() == EXPECTED_REPORT_SHA256
    frozen = json.loads(report.read_text(encoding="utf-8"))
    assert tuple(frozen["atom_counts_by_exact_depth"]) == atom_counts
    assert tuple(frozen["atom_sha256_by_exact_depth"]) == atom_hashes
    assert tuple(frozen["candidate_counts_by_expansion"]) == candidate_counts
    assert tuple(frozen["candidate_sha256_by_expansion"]) == candidate_hashes
    assert frozen["pointed_four_fibre_branches"] == sum(pointed) == 20
    assert frozen["quotient_survivor_count"] == 0

    print("PASS independent value-pair mutation generator")
    print("EXACT ATOMS BY DEPTH:", atom_counts)
    print("ATOM HASHES:", atom_hashes)
    print("EXPANSION CANDIDATES:", candidate_counts)
    print("CANDIDATE HASHES:", candidate_hashes)
    print("UNPOINTED FOUR-FIBRE ATOMS BY DEPTH:", unpointed)
    print("POINTED FOUR-FIBRE BRANCHES BY DEPTH:", pointed)
    print("PASS every pointed branch has empty size-8..15 single-T escape domain")
    print("REPORT SHA256:", EXPECTED_REPORT_SHA256)
    print(
        "STATUS: ALGORITHMICALLY-INDEPENDENT SELF-CHECK PASSED; "
        "fresh-context review pending; global slice incomplete"
    )


if __name__ == "__main__":
    main()
