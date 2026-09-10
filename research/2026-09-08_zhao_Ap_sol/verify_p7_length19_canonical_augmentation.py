#!/usr/bin/env python3
"""Independent replay checks for the short-support canonical augmentation."""

from __future__ import annotations

from collections import Counter

import p7_length19_canonical_augmentation as canonical
import p7_length19_pair_mutation_frontier as old_frontier
import verify_p7_tail_conditioned_middle_spectrum as conditioned


def direct_position_atom(labels):
    """Position-level test independent of the bounded-kernel implementation."""
    assert len(labels) == 19
    assert old_frontier.total(labels) == canonical.ZERO
    supports = old_frontier.fixed_size_supports(labels, 9)
    return all(canonical.ZERO not in supports[size] for size in range(1, 10))


def audit_conditioned_interface():
    rows = tuple(
        (j, max(0, 9 - j), min(19, 16 - j))
        for j in range(7)
    )
    assert rows == (
        (0, 9, 16),
        (1, 8, 15),
        (2, 7, 14),
        (3, 6, 13),
        (4, 5, 12),
        (5, 4, 11),
        (6, 3, 10),
    )
    for j, lower, upper in rows:
        complement = rows[6 - j]
        assert (19 - upper, 19 - lower) == complement[1:]

    known = old_frontier.PRIOR_ATOMS + old_frontier.FROZEN_ATOMS
    escapes = tuple(conditioned.full_singleton_escape(atom) for atom in known)
    assert tuple(map(len, escapes[:4])) == (0, 0, 0, 0)
    assert tuple(map(len, escapes[4:])) == (0, 1, 0, 0, 7, 0, 0, 1)
    low_fibre_mutations = tuple(
        atom
        for atom in old_frontier.FROZEN_ATOMS
        if max(Counter(atom).values()) <= 4
    )
    assert all(not conditioned.full_singleton_escape(atom) for atom in low_fibre_mutations)
    return rows


def audit_support_six_representatives():
    reports = canonical.run_support_at_most_six()
    representatives = tuple(report["representative"] for report in reports)
    assert all(direct_position_atom(atom) for atom in representatives)
    assert len({canonical.canonical_q_key(atom) for atom in representatives}) == 2
    for atom in representatives:
        supports = canonical.position_supports(atom, 15)
        middle = frozenset().union(*(supports[size] for size in range(8, 16)))
        assert middle == frozenset(canonical.ALL_NONZERO)
    return reports


def audit_support_seven_coverage_reduction():
    """Check that the canonical-basis rule retains the known support-seven B3."""
    known_b3 = old_frontier.PRIOR_ATOMS[3]
    counts = Counter(known_b3)
    support = tuple(sorted(counts))
    others = tuple(value for value in support if value != canonical.Q)
    maximum = max(counts[value] for value in others)
    retained_profiles = []
    for first in others:
        if counts[first] != maximum:
            continue
        outside_plane = tuple(
            second
            for second in others
            if canonical.determinant((canonical.Q, first, second)) != 0
        )
        outside_maximum = max(counts[value] for value in outside_plane)
        for second in outside_plane:
            if counts[second] != outside_maximum:
                continue
            transform = canonical.inverse_matrix(
                canonical.matrix_from_columns((canonical.Q, first, second))
            )
            image = tuple(
                sorted(canonical.matrix_vector(transform, value) for value in known_b3)
            )
            image_counts = Counter(image)
            extras = tuple(
                sorted(
                    value
                    for value in image_counts
                    if value not in (canonical.Q, canonical.E2, canonical.E3)
                )
            )
            profile = (
                image_counts[canonical.E2],
                image_counts[canonical.E3],
                *(image_counts[value] for value in extras),
            )
            assert all(
                image_counts[value] <= image_counts[canonical.E3]
                for value in extras
                if value[2] != 0
            )
            assert profile in canonical.support_seven_profiles()
            retained_profiles.append(profile)
    assert retained_profiles
    return tuple(sorted(set(retained_profiles)))


def main():
    rows = audit_conditioned_interface()
    reports = audit_support_six_representatives()
    retained = audit_support_seven_coverage_reduction()
    print("PASS tail-conditioned middle rows:", rows)
    print("PASS support<=6 canonical classification; orbit count:", len(reports))
    print("PASS direct position-level atom replay and full 8--15 coverage")
    print("PASS support-seven canonical-basis rule retains known B3 via profiles:", retained)
    print("STATUS: verified finite layer; no claim for all support-seven profiles")


if __name__ == "__main__":
    main()
