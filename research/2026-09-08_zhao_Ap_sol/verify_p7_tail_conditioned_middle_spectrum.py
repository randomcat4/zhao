#!/usr/bin/env python3
"""Verify the exact p=7 tail-conditioned middle-spectrum interface.

The finite regression reuses the frozen atoms from
``p7_length19_pair_mutation_frontier`` but recomputes every position-subset
support through size 15.  It does not classify arbitrary length-19 atoms.
"""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement

import p7_length19_pair_mutation_frontier as frontier


P = 7
ZERO = (0, 0, 0)


def add(left, right):
    return tuple((left[i] + right[i]) % P for i in range(3))


def neg(value):
    return tuple((-entry) % P for entry in value)


def position_supports(labels, maximum):
    supports = [set() for _ in range(maximum + 1)]
    supports[0].add(ZERO)
    for index, label in enumerate(labels):
        for size in range(min(maximum, index + 1), 0, -1):
            supports[size].update(add(old, label) for old in supports[size - 1])
    return tuple(frozenset(layer) for layer in supports)


def conditioned_forbidden_support(b_supports, tail_size):
    lower = max(0, 9 - tail_size)
    upper = min(19, 16 - tail_size)
    return frozenset().union(*(b_supports[k] for k in range(lower, upper + 1)))


def conditioned_ranges(tail_length):
    b_length = 25 - tail_length
    return tuple(
        (j, max(0, 9 - j), min(b_length, 16 - j))
        for j in range(tail_length + 1)
    )


def full_singleton_escape(atom):
    supports = position_supports(atom, 15)
    forbidden = conditioned_forbidden_support(supports, 1)
    return tuple(
        value for value in frontier.ALL_NONZERO if neg(value) not in forbidden
    )


def exact_middle_compatible(atom, tail):
    """Direct definition: no quotient-zero subset of total size 9 through 16."""
    labels = tuple(atom) + tuple(tail)
    supports = position_supports(labels, 16)
    return all(ZERO not in supports[size] for size in range(9, 17))


def conditioned_middle_compatible(atom, tail):
    """The j=0..6 convolution formulation from equation (4)."""
    b_supports = position_supports(atom, 16)
    t_supports = position_supports(tail, 6)
    for j in range(7):
        forbidden = conditioned_forbidden_support(b_supports, j)
        if any(neg(value) in forbidden for value in t_supports[j]):
            return False
    return True


def three_row_middle_compatible(atom, tail):
    """For zero-sum B,T with B atomic, j=1,2,3 are sufficient."""
    b_supports = position_supports(atom, 15)
    t_supports = position_supports(tail, 3)
    for j in (1, 2, 3):
        forbidden = conditioned_forbidden_support(b_supports, j)
        if any(neg(value) in forbidden for value in t_supports[j]):
            return False
    return True


def audit_symbolic_index_ranges():
    rows = conditioned_ranges(6)
    assert rows == (
        (0, 9, 16),
        (1, 8, 15),
        (2, 7, 14),
        (3, 6, 13),
        (4, 5, 12),
        (5, 4, 11),
        (6, 3, 10),
    )
    for tail_length in (6, 7, 8):
        generic_rows = conditioned_ranges(tail_length)
        b_length = 25 - tail_length
        for j, lower, upper in generic_rows:
            other = generic_rows[tail_length - j]
            assert b_length - upper == other[1]
            assert b_length - lower == other[2]
    return rows


def audit_small_differential():
    """Compare direct and convolution formulations on deterministic tails."""
    atoms = frontier.PRIOR_ATOMS + frontier.FROZEN_ATOMS
    probes = []
    values = frontier.ALL_NONZERO[:12]
    for atom_index, atom in enumerate(atoms):
        for indices in combinations(range(len(values)), 5):
            prefix = tuple(values[index] for index in indices)
            closing = neg(frontier.total(prefix))
            tail = prefix + (closing,)
            if closing == ZERO:
                continue
            probes.append((atom, tail))
            if len(probes) >= 72 + atom_index:
                break
    assert probes
    for atom, tail in probes:
        direct = exact_middle_compatible(atom, tail)
        convolution = conditioned_middle_compatible(atom, tail)
        reduced = three_row_middle_compatible(atom, tail)
        assert direct == convolution == reduced
    return len(probes)


def compatible_zero_sum_tail_multisets(atom):
    """Enumerate six-position tails after the exact j=1,2,3 filter.

    This is used only for the frozen atoms, whose full singleton escape sets
    have size at most seven.
    """
    escape = full_singleton_escape(atom)
    survivors = []
    for tail in combinations_with_replacement(escape, 6):
        if frontier.total(tail) != ZERO:
            continue
        if three_row_middle_compatible(atom, tail):
            survivors.append(tail)
    return tuple(survivors)


def main():
    rows = audit_symbolic_index_ranges()
    prior_escape = tuple(full_singleton_escape(atom) for atom in frontier.PRIOR_ATOMS)
    mutation_escape = tuple(
        full_singleton_escape(atom) for atom in frontier.FROZEN_ATOMS
    )
    assert tuple(map(len, prior_escape)) == (0, 0, 0, 0)
    assert tuple(map(len, mutation_escape)) == (0, 1, 0, 0, 7, 0, 0, 1)
    low_fibre = tuple(
        index + 1
        for index, atom in enumerate(frontier.FROZEN_ATOMS)
        if max(frontier.Counter(atom).values()) <= 4
    )
    assert low_fibre == (1, 3, 4, 6, 7)
    assert all(not mutation_escape[index - 1] for index in low_fibre)
    tail_survivors = tuple(
        compatible_zero_sum_tail_multisets(atom)
        for atom in frontier.FROZEN_ATOMS
    )
    assert tuple(map(len, tail_survivors)) == (0, 0, 0, 0, 1, 0, 0, 0)
    assert tail_survivors[4] == ((
        (1, 6, 1),
        (1, 6, 1),
        (1, 6, 1),
        (1, 6, 1),
        (1, 6, 1),
        (2, 5, 2),
    ),)
    probes = audit_small_differential()

    print(f"PASS conditioned middle ranges: {rows}")
    print("PASS prior-B full singleton escape sizes: (0, 0, 0, 0)")
    print("PASS mutation full singleton escape sizes: (0, 1, 0, 0, 7, 0, 0, 1)")
    print("PASS exact middle-compatible zero-sum tail counts: (0, 0, 0, 0, 1, 0, 0, 0)")
    print(f"PASS direct/convolution/three-row differential probes: {probes}")
    print("CERTIFIED: all known max-fibre<=4 atoms have empty full singleton escape")
    print("STATUS: exact B|T interface; global length-19 classification INCOMPLETE")


if __name__ == "__main__":
    main()
