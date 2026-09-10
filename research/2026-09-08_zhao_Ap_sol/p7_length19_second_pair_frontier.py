#!/usr/bin/env python3
"""Exact second pair-mutation frontier around the seven known low-fibre atoms.

The source set consists of the four prior p=7,m=3 atoms and the three new
low-fibre orbit representatives from the first pair-mutation frontier, after
exact-multiset deduplication.  For every source, replace two positions by two
positions with the same sum, retain maximum multiplicity at most four, and
deduplicate the union.  This is a finite neighbourhood, not a classification
of all length-19 atoms in C_7^3.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from itertools import combinations

import p7_length19_pair_mutation_frontier as first
import verify_p7_tail_conditioned_middle_spectrum as middle


EXPECTED_SOURCES = 7
EXPECTED_CANDIDATES = 39276
EXPECTED_ATOMS = 10
EXPECTED_NEW_ATOMS = 3
EXPECTED_CANDIDATE_SHA256 = "26c1feefcfade3dae76c8221f0e38f2c8e6075e374b112f13f3fb978693e3657"
EXPECTED_ATOM_SHA256 = "312184b9e170b8e9ad9f6ba69762f1ee717c6d4df61622c58d0eaf1f1df9cd3f"
EXPECTED_NEW_SHA256 = "a269531cccef3dacee1c3f2a7e119c0deb6eb87c10e885214dd29158163a283d"
EXPECTED_GL_TRIALS = 8016


def source_atoms():
    candidates = first.PRIOR_ATOMS + first.FROZEN_ATOMS
    sources = tuple(sorted(set(
        atom for atom in candidates if max(Counter(atom).values()) <= 4
    )))
    assert len(sources) == EXPECTED_SOURCES
    return sources


def pair_neighbourhood_union(sources):
    candidates = set()
    for atom in sources:
        for left_index, right_index in combinations(range(19), 2):
            target = first.add(atom[left_index], atom[right_index])
            remainder = tuple(
                atom[index] for index in range(19)
                if index not in (left_index, right_index)
            )
            for left in first.ALL:
                right = first.add(target, first.neg(left))
                candidate = tuple(sorted(remainder + (left, right)))
                if max(Counter(candidate).values()) <= 4:
                    candidates.add(candidate)
    assert len(candidates) == EXPECTED_CANDIDATES
    return frozenset(candidates)


def digest(collection):
    return hashlib.sha256(first.canonical_payload(collection)).hexdigest()


def exact_orbit_trials(new_atoms, sources):
    trials = 0
    for atom in new_atoms:
        for source in sources:
            equivalent, count, _matrix = first.gl_equivalent(atom, source)
            assert not equivalent
            trials += count
    for left, right in combinations(new_atoms, 2):
        equivalent, count, _matrix = first.gl_equivalent(left, right)
        assert not equivalent
        trials += count
    assert trials == EXPECTED_GL_TRIALS
    return trials


def main():
    sources = source_atoms()
    candidates = pair_neighbourhood_union(sources)
    atoms = tuple(sorted(
        candidate for candidate in candidates if first.is_length_19_atom(candidate)
    ))
    new_atoms = tuple(atom for atom in atoms if atom not in sources)

    assert len(atoms) == EXPECTED_ATOMS
    assert len(new_atoms) == EXPECTED_NEW_ATOMS
    assert all(source in candidates for source in sources)
    assert digest(candidates) == EXPECTED_CANDIDATE_SHA256
    assert digest(atoms) == EXPECTED_ATOM_SHA256
    assert digest(new_atoms) == EXPECTED_NEW_SHA256

    trials = exact_orbit_trials(new_atoms, sources)
    signatures = tuple(
        tuple(sorted(Counter(atom).values(), reverse=True)) for atom in new_atoms
    )
    assert signatures == (
        (4, 4, 3, 2, 2, 1, 1, 1, 1),
        (4, 4, 4, 2, 2, 1, 1, 1),
        (4, 4, 3, 2, 2, 1, 1, 1, 1),
    )
    escape_sizes = tuple(
        len(middle.full_singleton_escape(atom)) for atom in new_atoms
    )
    assert escape_sizes == (0, 0, 0)

    print(f"PASS source low-fibre orbit representatives: {len(sources)}")
    print(f"PASS second-neighbourhood exact multisets: {len(candidates)}")
    print(f"CANDIDATE SHA256: {digest(candidates)}")
    print(f"PASS length-19 atoms in union: {len(atoms)}; new exact atoms: {len(new_atoms)}")
    print(f"ATOM SHA256: {digest(atoms)}")
    print(f"NEW ATOM SHA256: {digest(new_atoms)}")
    print(f"PASS new-vs-known and pairwise GL inequivalence; target-basis trials: {trials}")
    print(f"PASS new atom signatures: {signatures}")
    print("PASS all three new atoms have empty full singleton escape")
    print("STATUS: exact second finite neighbourhood / global classification INCOMPLETE")


if __name__ == "__main__":
    main()
