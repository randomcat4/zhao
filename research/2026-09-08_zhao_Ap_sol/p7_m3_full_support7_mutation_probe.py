#!/usr/bin/env python3
"""Exact one-pair mutation probe around the four support-seven escape atoms.

This is deliberately a finite neighbourhood test.  It asks whether an
equal-sum replacement of two positions can produce a support-at-least-eight
length-19 atom with q exactly threefold, every other fibre at most fourfold,
and nonempty complete singleton escape.  Such an atom would refute the useful
but unproved global ``all E1 empty above support seven`` heuristic.  Failure to
find one has no global force.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations

import p7_length19_canonical_augmentation as canonical
import p7_length19_pair_mutation_frontier as mutation
import verify_p7_maximal_atom_escape_algebra as algebra


Q = canonical.Q
ZERO = canonical.ZERO
SOURCES = tuple(entry[1] for entry in algebra.ATOMS if entry[0].startswith("support7_escape_"))
EXPECTED_RAW_REPLACEMENTS = 234_612
EXPECTED_CANDIDATES = 17_936
EXPECTED_CANDIDATE_SHA256 = "f1e224d4a25328c6624e2a3f95a1e4af4ea9b5dc6fcc3d372e1c23d34630ffe5"
EXPECTED_LITERAL_TARGET_MULTIPLICITY = 12_945
EXPECTED_LITERAL_SUPPORT_EIGHT_PLUS = 12_684
EXPECTED_ZERO_LABEL_CANDIDATES = 69
EXPECTED_TARGET_MULTIPLICITY = 12_876
EXPECTED_SUPPORT_EIGHT_PLUS = 12_615
EXPECTED_ATOMS = 0
EXPECTED_EMPTY_SHA256 = "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"


def payload(collection):
    serial = [[list(value) for value in sequence] for sequence in sorted(collection)]
    return json.dumps(serial, separators=(",", ":")).encode("ascii")


def discover():
    candidates = set()
    witnesses = {}
    raw_replacements = 0
    for source_index, source in enumerate(SOURCES):
        for left_index, right_index in combinations(range(19), 2):
            target = mutation.add(source[left_index], source[right_index])
            remainder = tuple(
                source[index]
                for index in range(19)
                if index not in (left_index, right_index)
            )
            for first in mutation.ALL:
                raw_replacements += 1
                second = mutation.add(target, mutation.neg(first))
                candidate = tuple(sorted(remainder + (first, second)))
                if candidate == source:
                    continue
                candidates.add(candidate)
                witnesses.setdefault(
                    candidate,
                    (source_index, (source[left_index], source[right_index]), tuple(sorted((first, second)))),
                )
    return raw_replacements, frozenset(candidates), witnesses


def literal_target_multiplicity(candidate):
    counts = Counter(candidate)
    return (
        counts[Q] == 3
        and all(multiplicity <= 4 for value, multiplicity in counts.items() if value != Q)
    )


def main():
    assert len(SOURCES) == 4
    raw_replacements, candidates, witnesses = discover()
    literal_multiplicity_filtered = tuple(
        sorted(candidate for candidate in candidates if literal_target_multiplicity(candidate))
    )
    literal_support_eight_plus = tuple(
        candidate for candidate in literal_multiplicity_filtered if len(set(candidate)) >= 8
    )
    zero_label_candidates = tuple(
        candidate for candidate in literal_multiplicity_filtered if ZERO in candidate
    )
    multiplicity_filtered = tuple(
        candidate for candidate in literal_multiplicity_filtered if ZERO not in candidate
    )
    support_eight_plus = tuple(
        candidate for candidate in multiplicity_filtered if len(set(candidate)) >= 8
    )
    atoms = tuple(
        candidate for candidate in support_eight_plus if mutation.is_length_19_atom(candidate)
    )
    escape_atoms = tuple(
        (candidate, canonical.full_singleton_escape(candidate)[2])
        for candidate in atoms
        if canonical.full_singleton_escape(candidate)[2]
    )

    groups = defaultdict(list)
    for candidate, escape in escape_atoms:
        groups[canonical.canonical_q_key(candidate)].append((candidate, escape))

    candidate_digest = hashlib.sha256(payload(candidates)).hexdigest()
    atom_digest = hashlib.sha256(payload(atoms)).hexdigest()
    assert raw_replacements == EXPECTED_RAW_REPLACEMENTS
    assert len(candidates) == EXPECTED_CANDIDATES
    assert candidate_digest == EXPECTED_CANDIDATE_SHA256
    assert len(literal_multiplicity_filtered) == EXPECTED_LITERAL_TARGET_MULTIPLICITY
    assert len(literal_support_eight_plus) == EXPECTED_LITERAL_SUPPORT_EIGHT_PLUS
    assert len(zero_label_candidates) == EXPECTED_ZERO_LABEL_CANDIDATES
    assert len(multiplicity_filtered) == EXPECTED_TARGET_MULTIPLICITY
    assert len(support_eight_plus) == EXPECTED_SUPPORT_EIGHT_PLUS
    assert len(atoms) == EXPECTED_ATOMS
    assert atom_digest == EXPECTED_EMPTY_SHA256
    assert not escape_atoms and not groups

    print("RAW POSITION-PAIR REPLACEMENTS:", raw_replacements)
    print("DISTINCT NONTRIVIAL EXACT MULTISETS:", len(candidates))
    print("CANDIDATE SHA256:", candidate_digest)
    print("LITERAL TARGET-MULTIPLICITY MULTISETS:", len(literal_multiplicity_filtered))
    print("LITERAL SUPPORT>=8 MULTISETS:", len(literal_support_eight_plus))
    print("AUTOMATIC NONATOMS WITH ZERO LABEL:", len(zero_label_candidates))
    print("ZERO-FREE TARGET-MULTIPLICITY MULTISETS:", len(multiplicity_filtered))
    print("ZERO-FREE SUPPORT>=8 TARGET MULTISETS:", len(support_eight_plus))
    print("SUPPORT>=8 LENGTH-19 ATOMS:", len(atoms))
    print("ATOM SHA256:", atom_digest)
    print("NONEMPTY-E1 ATOMS:", len(escape_atoms))
    print("NONEMPTY-E1 GL_q ORBITS:", len(groups))
    for index, representative in enumerate(sorted(groups), 1):
        escape_sets = {entry[1] for entry in groups[representative]}
        assert len(escape_sets) == 1
        report = {
            "representative": representative,
            "support": len(set(representative)),
            "multiplicity_signature": tuple(sorted(Counter(representative).values(), reverse=True)),
            "escape": next(iter(escape_sets)),
            "exact_preimages": len(groups[representative]),
            "witness": witnesses[groups[representative][0][0]],
        }
        print("ESCAPE ORBIT", index, json.dumps(report, separators=(",", ":"), default=list))
    print(
        "STATUS: union of four per-source nontrivial one-step neighbourhoods only; "
        "not the strict graph-distance-one layer from the four-source set; "
        "no global classification claim"
    )


if __name__ == "__main__":
    main()
