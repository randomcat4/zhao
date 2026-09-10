#!/usr/bin/env python3
"""Exact one-step pair-mutation frontier for the old p=7 length-19 atom.

Starting with the fixed ``BASE_B`` from the old m=3 calculation, remove two
positions and insert two (possibly zero at the candidate-generation stage)
quotient labels with the same total.  Candidates are deduplicated as exact
position multisets.  The default run then

* classifies all zero-sum atoms in this finite neighbourhood;
* proves pairwise GL(3,7)-inequivalence by explicit basis transport;
* computes every size-8--11 internal subset-sum support and escape set;
* identifies the two orbits already frozen in the other-B note; and
* checks the fixed-skeleton exclusions that apply to the five atoms whose
  largest quotient fibre has size at most four.

This is a neighbourhood classification, not a classification of all
length-19 atoms in C_7^3.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations, product
from typing import Iterable, Sequence


P = 7
ZERO = (0, 0, 0)
Q = (1, 0, 0)
ALL = tuple(product(range(P), repeat=3))
ALL_NONZERO = tuple(value for value in ALL if value != ZERO)
VECTOR_ID = {value: index for index, value in enumerate(ALL)}
ADD_ID = tuple(
    tuple(VECTOR_ID[tuple((left[coordinate] + right[coordinate]) % P
                          for coordinate in range(3))]
          for right in ALL)
    for left in ALL
)


def add(left: tuple[int, int, int], right: tuple[int, int, int]):
    return tuple((left[index] + right[index]) % P for index in range(3))


def neg(value: tuple[int, int, int]):
    return tuple((-entry) % P for entry in value)


def total(values: Iterable[tuple[int, int, int]]):
    answer = ZERO
    for value in values:
        answer = add(answer, value)
    return answer


def expanded(entries):
    return tuple(sorted(value for value, multiplicity in entries for _ in range(multiplicity)))


BASE_B = expanded((
    (Q, 3),
    ((0, 0, 1), 1),
    ((0, 1, 0), 1),
    ((0, 1, 6), 3),
    ((1, 0, 1), 4),
    ((1, 5, 1), 1),
    ((1, 6, 1), 4),
    ((4, 5, 3), 1),
    ((5, 4, 4), 1),
))

# Stable certificate numbering.  The discovery below is set-valued and
# independently asserts that it finds exactly these eight multisets.
FROZEN_ATOMS = (
    expanded((
        ((0, 0, 1), 1), ((0, 1, 0), 1), ((0, 1, 6), 4),
        (Q, 2), ((1, 0, 1), 4), ((1, 5, 1), 1),
        ((1, 6, 1), 4), ((5, 4, 4), 2),
    )),
    expanded((
        ((0, 0, 1), 1), ((0, 1, 6), 3), (Q, 3),
        ((1, 0, 1), 5), ((1, 5, 1), 1), ((1, 6, 1), 4),
        ((4, 5, 3), 2),
    )),
    expanded((
        ((0, 0, 1), 1), ((0, 1, 0), 1), ((0, 1, 6), 2),
        (Q, 4), ((1, 0, 1), 4), ((1, 5, 1), 1),
        ((1, 6, 1), 4), ((4, 5, 3), 2),
    )),
    expanded((
        ((0, 0, 1), 2), ((0, 1, 6), 3), (Q, 3),
        ((1, 0, 1), 4), ((1, 5, 1), 1), ((1, 6, 1), 4),
        ((4, 5, 3), 1), ((5, 5, 3), 1),
    )),
    expanded((
        ((0, 0, 1), 1), ((0, 1, 0), 1), ((0, 1, 6), 3),
        (Q, 3), ((1, 0, 1), 3), ((1, 6, 1), 6),
        ((4, 5, 3), 1), ((5, 4, 4), 1),
    )),
    expanded((
        ((0, 0, 1), 2), ((0, 1, 0), 1), ((0, 1, 6), 3),
        (Q, 3), ((1, 0, 1), 3), ((1, 5, 1), 1),
        ((1, 6, 1), 4), ((5, 4, 4), 1), ((5, 5, 3), 1),
    )),
    expanded((
        ((0, 0, 1), 1), ((0, 1, 0), 2), ((0, 1, 6), 3),
        (Q, 3), ((1, 0, 1), 3), ((1, 5, 1), 1),
        ((1, 6, 1), 4), ((5, 4, 4), 2),
    )),
    expanded((
        ((0, 0, 1), 1), ((0, 1, 0), 1), ((0, 1, 6), 3),
        (Q, 3), ((1, 0, 1), 4), ((1, 6, 1), 5),
        ((4, 5, 3), 1), ((5, 3, 4), 1),
    )),
)

# B_0,B_1,B_2,B_3 in p7_m3_other_B_frontier.md, represented as full B's.
PRIOR_ATOMS = (
    BASE_B,
    expanded((
        (Q, 3), ((0, 0, 1), 1), ((0, 1, 0), 2),
        ((0, 1, 6), 3), ((1, 0, 1), 3), ((1, 5, 1), 1),
        ((1, 6, 1), 4), ((5, 4, 4), 2),
    )),
    expanded((
        (Q, 3), ((0, 0, 1), 2), ((0, 1, 0), 1),
        ((0, 1, 6), 3), ((1, 0, 1), 3), ((1, 5, 1), 1),
        ((1, 6, 1), 4), ((5, 4, 4), 1), ((5, 5, 3), 1),
    )),
    expanded((
        (Q, 3), ((0, 0, 1), 3), ((0, 1, 6), 3),
        ((1, 0, 1), 3), ((1, 5, 1), 1), ((1, 6, 1), 4),
        ((5, 5, 3), 2),
    )),
)

EXPECTED_CANDIDATES = 6840
EXPECTED_ATOMS = 8
EXPECTED_MAX_FIBRES = (4, 5, 4, 4, 6, 4, 4, 5)
EXPECTED_LAYERS = (
    (291, 303, 303, 291),
    (284, 296, 296, 284),
    (293, 301, 301, 293),
    (318, 326, 326, 318),
    (256, 266, 266, 256),
    (313, 322, 322, 313),
    (291, 302, 302, 291),
    (267, 280, 280, 267),
)
EXPECTED_ESCAPE_COUNTS = (0, 2, 2, 0, 26, 0, 2, 4)
EXPECTED_CANDIDATE_SHA256 = "a123ad016325cbef71acb4da4fd69f662fa8056c9e74ea4c02703c22c3866ad9"
EXPECTED_ATOM_SHA256 = "0b29f69959a8d85fc1a6b573b15b98dc13f44ca8577e491875398810dbaa82e2"
EXPECTED_INTERNAL_GL_TRIALS = 8976
EXPECTED_PRIOR_GL_TRIALS = 10304


def canonical_payload(collection) -> bytes:
    serial = [[list(value) for value in sequence] for sequence in sorted(collection)]
    return json.dumps(serial, separators=(",", ":")).encode("ascii")


def discover_pair_mutations():
    """Return all exact multisets and one position-level mutation witness each."""
    candidates = {}
    for left_index, right_index in combinations(range(len(BASE_B)), 2):
        old_pair = (BASE_B[left_index], BASE_B[right_index])
        target = total(old_pair)
        remainder = [
            value for index, value in enumerate(BASE_B)
            if index not in (left_index, right_index)
        ]
        for first in ALL:
            second = add(target, neg(first))
            new_pair = tuple(sorted((first, second)))
            candidate = tuple(sorted(remainder + list(new_pair)))
            if candidate == BASE_B:
                continue
            candidates.setdefault(candidate, (old_pair, new_pair))
    assert len(candidates) == EXPECTED_CANDIDATES
    return candidates


def fixed_size_supports(labels: Sequence[tuple[int, int, int]], maximum: int):
    """Exact position-subset DP, with repeated labels kept as distinct positions."""
    supports = [set() for _ in range(maximum + 1)]
    supports[0].add(ZERO)
    for index, label in enumerate(labels):
        for size in range(min(maximum, index + 1), 0, -1):
            supports[size].update(add(old_sum, label) for old_sum in supports[size - 1])
    return tuple(frozenset(layer) for layer in supports)


def is_length_19_atom(labels: Sequence[tuple[int, int, int]]):
    """Use total zero and complement symmetry to test sizes 1 through 9."""
    if len(labels) != 19 or total(labels) != ZERO:
        return False
    supports = [set() for _ in range(10)]
    supports[0].add(VECTOR_ID[ZERO])
    for index, label in enumerate(labels):
        label_id = VECTOR_ID[label]
        for size in range(min(9, index + 1), 0, -1):
            supports[size].update(ADD_ID[old_sum][label_id]
                                  for old_sum in supports[size - 1])
        # Early rejection is exact: once a zero-sum subset is present it
        # remains present as later positions are processed.
        if any(VECTOR_ID[ZERO] in supports[size]
               for size in range(1, min(9, index + 1) + 1)):
            return False
    return True


def middle_spectrum(labels):
    supports = fixed_size_supports(labels, 11)
    layers = tuple(len(supports[size]) for size in range(8, 12))
    middle = frozenset().union(*(supports[size] for size in range(8, 12)))
    escape = tuple(sorted(value for value in ALL_NONZERO if neg(value) not in middle))
    return layers, middle, escape


def determinant(columns):
    a, b, c = columns
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    ) % P


def inverse_matrix(matrix):
    augmented = [
        [matrix[row][column] % P for column in range(3)]
        + [int(row == column) for column in range(3)]
        for row in range(3)
    ]
    for column in range(3):
        pivot = next(row for row in range(column, 3) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        factor = pow(augmented[column][column], -1, P)
        augmented[column] = [(factor * entry) % P for entry in augmented[column]]
        for row in range(3):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                (augmented[row][index] - factor * augmented[column][index]) % P
                for index in range(6)
            ]
    return tuple(tuple(augmented[row][column] for column in range(3, 6)) for row in range(3))


def matrix_from_columns(columns):
    return tuple(tuple(columns[column][row] for column in range(3)) for row in range(3))


def matrix_product(left, right):
    return tuple(
        tuple(sum(left[row][inner] * right[inner][column] for inner in range(3)) % P
              for column in range(3))
        for row in range(3)
    )


def matrix_vector(matrix, vector):
    return tuple(sum(matrix[row][column] * vector[column] for column in range(3)) % P
                 for row in range(3))


def fixed_source_basis(labels):
    support = tuple(sorted(set(labels)))
    return next(triple for triple in combinations(support, 3) if determinant(triple))


def gl_equivalent(source, target):
    """Enumerate every target ordered basis image of one fixed source basis."""
    source_basis = fixed_source_basis(source)
    source_inverse = inverse_matrix(matrix_from_columns(source_basis))
    target_multiset = tuple(sorted(target))
    trials = 0
    for target_basis in permutations(sorted(set(target)), 3):
        if not determinant(target_basis):
            continue
        trials += 1
        transform = matrix_product(matrix_from_columns(target_basis), source_inverse)
        image = tuple(sorted(matrix_vector(transform, value) for value in source))
        if image == target_multiset:
            return True, trials, transform
    return False, trials, None


def audit_gl_orbits(atoms):
    pair_trials = 0
    for left, right in combinations(range(len(atoms)), 2):
        equivalent, trials, _ = gl_equivalent(atoms[left], atoms[right])
        pair_trials += trials
        assert not equivalent

    prior_matches = []
    prior_trials = 0
    for atom_index, atom in enumerate(atoms, 1):
        matches = []
        for prior_index, prior in enumerate(PRIOR_ATOMS):
            equivalent, trials, _ = gl_equivalent(atom, prior)
            prior_trials += trials
            if equivalent:
                matches.append(prior_index)
        prior_matches.append(tuple(matches))
    assert tuple(prior_matches) == ((), (), (), (), (), (2,), (1,), ())
    return pair_trials, prior_trials, tuple(prior_matches)


def zero_sum_six_multisets(support):
    return tuple(
        choice for choice in combinations_with_replacement(support, 6)
        if total(choice) == ZERO
    )


def audit_binary_height_window(atom, escape):
    """Check the L_2={1} obstruction for the +/-f escape case."""
    f = (1, 6, 1)
    assert escape == (f, neg(f))
    assert Counter(atom)[f] == 4
    tails = zero_sum_six_multisets(escape)
    assert tails == ((f,) * 3 + (neg(f),) * 3,)

    # Pick one -f position of height r.  Pairing it with each of the four f
    # positions gives a quotient-zero length-2 set, whose actual coefficient
    # is forced into L_2={1}.
    window_profiles = 0
    multiplicity_valid_profiles = 0
    for r in range(P):
        for fibre_heights in product(range(P), repeat=4):
            if not all((r + height) % P == 1 for height in fibre_heights):
                continue
            window_profiles += 1
            if max(Counter(fibre_heights).values()) <= 3:
                multiplicity_valid_profiles += 1
    assert window_profiles == P
    assert multiplicity_valid_profiles == 0
    return tails, window_profiles, multiplicity_valid_profiles


def main():
    mutations = discover_pair_mutations()
    candidates = tuple(mutations)
    atoms_found = tuple(candidate for candidate in candidates if is_length_19_atom(candidate))
    assert len(atoms_found) == EXPECTED_ATOMS
    assert set(atoms_found) == set(FROZEN_ATOMS)
    assert all(ZERO not in atom for atom in atoms_found)

    candidate_hash = hashlib.sha256(canonical_payload(candidates)).hexdigest()
    atom_hash = hashlib.sha256(canonical_payload(atoms_found)).hexdigest()
    assert candidate_hash == EXPECTED_CANDIDATE_SHA256
    assert atom_hash == EXPECTED_ATOM_SHA256

    reports = []
    for index, atom in enumerate(FROZEN_ATOMS, 1):
        counts = Counter(atom)
        maximum = max(counts.values())
        layers, middle, escape = middle_spectrum(atom)
        assert maximum == EXPECTED_MAX_FIBRES[index - 1]
        assert layers == EXPECTED_LAYERS[index - 1]
        assert len(escape) == EXPECTED_ESCAPE_COUNTS[index - 1]
        # Complement symmetry in a zero-sum 19-sequence gives Sigma_k=-Sigma_{19-k}.
        supports = fixed_size_supports(atom, 11)
        assert supports[8] == frozenset(neg(value) for value in supports[11])
        assert supports[9] == frozenset(neg(value) for value in supports[10])
        old_pair, new_pair = mutations[atom]
        assert total(old_pair) == total(new_pair)
        reports.append((maximum, tuple(sorted(counts.values(), reverse=True)),
                        layers, len(middle - {ZERO}), escape, old_pair, new_pair))

    pair_trials, prior_trials, prior_matches = audit_gl_orbits(FROZEN_ATOMS)
    assert pair_trials == EXPECTED_INTERNAL_GL_TRIALS
    assert prior_trials == EXPECTED_PRIOR_GL_TRIALS

    # The five atoms not already cut by the proved quotient-fibre cap <=4.
    assert tuple(index for index, report in enumerate(reports, 1) if report[0] <= 4) == (1, 3, 4, 6, 7)
    assert reports[0][4] == () and reports[3][4] == () and reports[5][4] == ()
    tail_3, lifts_3, valid_3 = audit_binary_height_window(FROZEN_ATOMS[2], reports[2][4])
    tail_7, lifts_7, valid_7 = audit_binary_height_window(FROZEN_ATOMS[6], reports[6][4])
    assert (tail_3, lifts_3, valid_3) == (tail_7, lifts_7, valid_7)

    # Six neighbourhood orbits are absent from the four previously frozen B_i.
    new_orbits = tuple(index for index, matches in enumerate(prior_matches, 1) if not matches)
    assert new_orbits == (1, 2, 3, 4, 5, 8)
    new_low_fibre = tuple(index for index in new_orbits if reports[index - 1][0] <= 4)
    assert new_low_fibre == (1, 3, 4)

    print("PASS exact pair-mutation multisets (unchanged base removed):", len(candidates))
    print("PAIR-MUTATION MULTISET SHA256:", candidate_hash)
    print("PASS length-19 zero-sum atoms:", len(atoms_found))
    print("ATOM MULTISET SHA256:", atom_hash)
    for index, report in enumerate(reports, 1):
        maximum, signature, layers, nonzero_middle, escape, old_pair, new_pair = report
        print(f"ATOM {index}: max_fibre={maximum} signature={signature}")
        print("  mutation:", old_pair, "->", new_pair)
        print("  |Sigma_8..Sigma_11|:", layers,
              "nonzero_union:", nonzero_middle, "escape:", escape)
    print("PASS pairwise GL(3,7)-inequivalent atoms; target-basis trials:", pair_trials)
    print("PASS exact GL comparison with prior B0..B3; trials:", prior_trials)
    print("PRIOR ORBIT MATCHES (candidate -> prior indices):", prior_matches)
    print("PASS max-fibre<=4 candidate ids:", (1, 3, 4, 6, 7))
    print("PASS full-middle exclusions:", (1, 4, 6))
    print("PASS +/-f binary-window exclusions:", (3, 7),
          "window/multiplicity-valid profiles:", (lifts_3, valid_3))
    print("NEW ORBITS AFTER PRIOR-B DEDUP:", new_orbits, "count:", len(new_orbits))
    print("NEW LOW-FIBRE FIXED-SKELETON EXCLUSIONS:", new_low_fibre,
          "count:", len(new_low_fibre))
    print("CERTIFIED: the old-B one-step equal-sum pair-mutation neighbourhood is classified")
    print("STATUS: PROVED finite neighbourhood / global length-19 classification INCOMPLETE")


if __name__ == "__main__":
    main()
