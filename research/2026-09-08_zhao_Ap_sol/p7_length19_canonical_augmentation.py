#!/usr/bin/env python3
"""Canonical augmentation for short-support length-19 atoms in C_7^3.

The distinguished value q=(1,0,0) occurs exactly three times.  Every other
fibre has multiplicity at most four.  The default run classifies, up to the
stabilizer of q in GL(3,7), every zero-sum atom with support size at most six.

The optional ``--support7`` run uses a provably complete canonical-basis
reduction and classifies support size seven.  It can be split into deterministic
profile shards with ``--start-profile`` and ``--stop-profile``.  A shard is a
complete interval of the printed normalized multiplicity-profile list; shard
results must be unioned and canonicalized before an orbit count is claimed.

This is a structural finite layer, not a neighbourhood of a previously known
atom and not a classification of supports of size eight or larger.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from typing import Iterable, Sequence


P = 7
ZERO = (0, 0, 0)
Q = (1, 0, 0)
E2 = (0, 1, 0)
E3 = (0, 0, 1)
ALL = tuple(product(range(P), repeat=3))
ALL_NONZERO = tuple(value for value in ALL if value != ZERO)
EXTRA_VALUES = tuple(value for value in ALL_NONZERO if value not in (Q, E2, E3))

EXPECTED_SUPPORT5_CANDIDATES = 167
EXPECTED_SUPPORT6_PROFILES = 42
EXPECTED_SUPPORT6_CANDIDATES = 788_022
EXPECTED_SUPPORT6_RAW_ATOMS = 24
EXPECTED_SUPPORT6_RAW_SHA256 = "95ca4b0dc8ca677d6417cbe964af7cc55ee3880c51648c551d12c3b0de3660a8"
EXPECTED_SUPPORT6_ORBIT_SHA256 = "1f54ed3f1d2ae08ca90b0de3570577a632a27d94ea1c78336c29d2269b7e3b3a"
EXPECTED_SUPPORT6_REPRESENTATIVES = (
    tuple(sorted(
        ((0, 0, 1),) * 4
        + ((0, 1, 0),) * 4
        + ((0, 1, 6),)
        + (Q,) * 3
        + ((1, 1, 0),) * 3
        + ((2, 5, 1),) * 4
    )),
    tuple(sorted(
        ((0, 0, 1),) * 4
        + ((0, 1, 0),) * 4
        + ((0, 1, 6),)
        + (Q,) * 3
        + ((1, 6, 0),) * 3
        + ((2, 3, 1),) * 4
    )),
)


def add(left: tuple[int, int, int], right: tuple[int, int, int]):
    return tuple((left[index] + right[index]) % P for index in range(3))


def neg(value: tuple[int, int, int]):
    return tuple((-entry) % P for entry in value)


def scale(scalar: int, value: tuple[int, int, int]):
    return tuple((scalar * entry) % P for entry in value)


def total(values: Iterable[tuple[int, int, int]]):
    answer = ZERO
    for value in values:
        answer = add(answer, value)
    return answer


def vector_id(value: tuple[int, int, int]):
    return P * P * value[0] + P * value[1] + value[2]


def determinant(columns: Sequence[tuple[int, int, int]]):
    a, b, c = columns
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    ) % P


def matrix_from_columns(columns):
    return tuple(tuple(columns[column][row] for column in range(3)) for row in range(3))


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


def matrix_vector(matrix, vector):
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(3)) % P
        for row in range(3)
    )


def expanded(support, multiplicities):
    return tuple(
        sorted(
            value
            for value, multiplicity in zip(support, multiplicities)
            for _ in range(multiplicity)
        )
    )


def bounded_atom(support, multiplicities):
    """Exact atom test after support[0:3] has been normalized to a basis.

    A submultiset is encoded by coefficients 0 <= c_i <= multiplicities[i].
    Once the coefficients on the nonbasis support are chosen, the three basis
    coefficients are forced modulo seven.  As every multiplicity is below
    seven, this tests every submultiset exactly once.
    """
    assert support[:3] == (Q, E2, E3)
    basis_bounds = multiplicities[:3]
    extra_support = support[3:]
    extra_bounds = multiplicities[3:]
    zero_relation = (0,) * len(support)
    full_relation = tuple(multiplicities)
    for extra_coefficients in product(*(range(bound + 1) for bound in extra_bounds)):
        basis_coefficients = tuple(
            -sum(
                coefficient * value[coordinate]
                for coefficient, value in zip(extra_coefficients, extra_support)
            ) % P
            for coordinate in range(3)
        )
        relation = basis_coefficients + tuple(extra_coefficients)
        if not all(
            coefficient <= bound
            for coefficient, bound in zip(basis_coefficients, basis_bounds)
        ):
            continue
        if relation not in (zero_relation, full_relation):
            return False
    return True


def canonical_q_key(labels):
    """Complete canonical key for the stabilizer GL(3,7)_q.

    For every ordered support pair u,v with (q,u,v) a basis, apply the unique
    map sending that basis to (e1,e2,e3), sort the resulting multiset, and take
    the lexicographic minimum.  Every q-stabilizer equivalence appears in this
    list of basis transports, so equality of keys is equivalent to orbit
    equality.
    """
    support = tuple(sorted(set(labels)))
    others = tuple(value for value in support if value != Q)
    best = None
    for first in others:
        for second in others:
            if first == second or determinant((Q, first, second)) == 0:
                continue
            transform = inverse_matrix(matrix_from_columns((Q, first, second)))
            image = tuple(sorted(matrix_vector(transform, value) for value in labels))
            if best is None or image < best:
                best = image
    assert best is not None
    return best


def position_supports(labels, maximum):
    supports = [set() for _ in range(maximum + 1)]
    supports[0].add(ZERO)
    for index, label in enumerate(labels):
        for size in range(min(maximum, index + 1), 0, -1):
            supports[size].update(add(old_sum, label) for old_sum in supports[size - 1])
    return tuple(frozenset(layer) for layer in supports)


def full_singleton_escape(labels):
    supports = position_supports(labels, 15)
    forbidden = frozenset().union(*(supports[size] for size in range(8, 16)))
    escape = tuple(value for value in ALL_NONZERO if neg(value) not in forbidden)
    layers = tuple(len(supports[size]) for size in range(8, 16))
    return layers, len(forbidden - {ZERO}), escape


def payload_digest(sequences):
    serial = [[list(value) for value in sequence] for sequence in sorted(sequences)]
    return hashlib.sha256(json.dumps(serial, separators=(",", ":")).encode("ascii")).hexdigest()


def support_five_candidates():
    """Enumerate every normalized support-five candidate.

    The four non-q multiplicities must all be four.  The final extra support
    value is forced by the zero-sum equation; ordering the two extra values
    removes their permutation symmetry.
    """
    candidates = []
    inverse_four = pow(4, -1, P)
    fixed_sum = add(scale(3, Q), add(scale(4, E2), scale(4, E3)))
    for first in EXTRA_VALUES:
        second = scale(-inverse_four, add(fixed_sum, scale(4, first)))
        if second in (ZERO, Q, E2, E3) or vector_id(first) >= vector_id(second):
            continue
        support = (Q, E2, E3, first, second)
        multiplicities = (3, 4, 4, 4, 4)
        candidates.append((support, multiplicities))
    return tuple(candidates)


def support_six_profiles():
    """All normalized multiplicity assignments after ordering e2,e3."""
    return tuple(
        profile
        for profile in product(range(1, 5), repeat=5)
        if sum(profile) == 16 and profile[0] >= profile[1]
    )


def support_six_candidates():
    """Yield all normalized support-six candidates and their profile index."""
    for profile_index, profile in enumerate(support_six_profiles(), 1):
        m2, m3, m_first, m_second, m_last = profile
        inverse_last = pow(m_last, -1, P)
        fixed_sum = add(scale(3, Q), add(scale(m2, E2), scale(m3, E3)))
        for first, second in combinations(EXTRA_VALUES, 2):
            subtotal = add(
                fixed_sum,
                add(scale(m_first, first), scale(m_second, second)),
            )
            last = scale(-inverse_last, subtotal)
            if last in (ZERO, Q, E2, E3) or vector_id(last) <= vector_id(second):
                continue
            support = (Q, E2, E3, first, second, last)
            multiplicities = (3,) + profile
            yield profile_index, support, multiplicities


def extend_reachable(reachable, value, multiplicity, forbidden_basis_sums):
    multiples = tuple(scale(coefficient, value) for coefficient in range(multiplicity + 1))
    extended = {add(old_sum, multiple) for old_sum in reachable for multiple in multiples}
    if extended & forbidden_basis_sums:
        return None
    return extended


def support_seven_profiles():
    """Profiles surviving the canonical maximal-first-basis rule.

    In an atom containing q^3, every other point on <q> has multiplicity at
    most one.  Since six other positive multiplicities sum to 16, a maximum
    multiplicity support value is off <q>.  Choose it as e2.  This justifies
    requiring m2 to be the maximum of the six non-q multiplicities.
    """
    return tuple(
        profile
        for profile in product(range(1, 5), repeat=6)
        if sum(profile) == 16 and profile[0] == max(profile)
    )


def support_seven_shard(start_profile: int, stop_profile: int | None):
    """Complete normalized profile shard for support size seven.

    After e2 is chosen with maximum multiplicity, choose e3 with maximum
    multiplicity outside span(q,e2).  In normalized coordinates that plane is
    z=0, hence every extra point with z != 0 has multiplicity at most m3.
    """
    profiles = support_seven_profiles()
    stop = len(profiles) if stop_profile is None else min(stop_profile, len(profiles))
    if not (1 <= start_profile <= stop + 1):
        raise ValueError("invalid support-seven profile interval")
    raw_atoms = []
    profile_reports = []
    for profile_index in range(start_profile, stop + 1):
        profile = profiles[profile_index - 1]
        m2, m3, m_first, m_second, m_third, m_last = profile
        forbidden_basis_sums = {
            ((-c1) % P, (-c2) % P, (-c3) % P)
            for c1 in range(4)
            for c2 in range(m2 + 1)
            for c3 in range(m3 + 1)
        } - {ZERO}

        def allowed_values(multiplicity):
            return tuple(
                value
                for value in EXTRA_VALUES
                if not (value[2] != 0 and multiplicity > m3)
            )

        first_values = allowed_values(m_first)
        second_values = allowed_values(m_second)
        third_values = allowed_values(m_third)
        first_states = []
        for first in first_values:
            state = extend_reachable({ZERO}, first, m_first, forbidden_basis_sums)
            if state is not None:
                first_states.append((first, state))
        pair_states = []
        for first, state in first_states:
            for second in second_values:
                if vector_id(second) <= vector_id(first):
                    continue
                next_state = extend_reachable(state, second, m_second, forbidden_basis_sums)
                if next_state is not None:
                    pair_states.append((first, second, next_state))

        inverse_last = pow(m_last, -1, P)
        fixed_sum = add(scale(3, Q), add(scale(m2, E2), scale(m3, E3)))
        final_candidates = 0
        profile_atoms = 0
        for first, second, state in pair_states:
            for third in third_values:
                if vector_id(third) <= vector_id(second):
                    continue
                next_state = extend_reachable(
                    state, third, m_third, forbidden_basis_sums
                )
                if next_state is None:
                    continue
                subtotal = add(
                    fixed_sum,
                    add(
                        add(scale(m_first, first), scale(m_second, second)),
                        scale(m_third, third),
                    ),
                )
                last = scale(-inverse_last, subtotal)
                if last in (ZERO, Q, E2, E3) or vector_id(last) <= vector_id(third):
                    continue
                if last[2] != 0 and m_last > m3:
                    continue
                final_candidates += 1
                support = (Q, E2, E3, first, second, third, last)
                multiplicities = (3,) + profile
                if bounded_atom(support, multiplicities):
                    raw_atoms.append(expanded(support, multiplicities))
                    profile_atoms += 1
        profile_reports.append(
            {
                "profile_index": profile_index,
                "profile": profile,
                "first_states": len(first_states),
                "pair_states": len(pair_states),
                "final_candidates": final_candidates,
                "raw_atoms": profile_atoms,
            }
        )
        print("SUPPORT7 PROFILE", json.dumps(profile_reports[-1], separators=(",", ":")), flush=True)
    return profiles, tuple(raw_atoms), tuple(profile_reports)


def orbit_report(raw_atoms):
    groups = defaultdict(list)
    for atom in raw_atoms:
        groups[canonical_q_key(atom)].append(atom)
    reports = []
    for key in sorted(groups):
        layers, union_size, escape = full_singleton_escape(key)
        reports.append(
            {
                "representative": key,
                "multiplicity_signature": tuple(
                    sorted(Counter(key).values(), reverse=True)
                ),
                "normalized_preimages": len(groups[key]),
                "middle_layers_8_15": layers,
                "middle_nonzero_union": union_size,
                "escape": escape,
            }
        )
    return tuple(reports)


def run_support_at_most_six():
    five_candidates = support_five_candidates()
    five_atoms = tuple(
        expanded(support, multiplicities)
        for support, multiplicities in five_candidates
        if bounded_atom(support, multiplicities)
    )
    assert len(five_candidates) == EXPECTED_SUPPORT5_CANDIDATES
    assert five_atoms == ()

    profile_counts = Counter()
    six_atoms = []
    candidate_count = 0
    for profile_index, support, multiplicities in support_six_candidates():
        candidate_count += 1
        profile_counts[profile_index] += 1
        if bounded_atom(support, multiplicities):
            six_atoms.append(expanded(support, multiplicities))
    reports = orbit_report(six_atoms)
    raw_digest = payload_digest(six_atoms)
    representatives = tuple(report["representative"] for report in reports)
    orbit_digest = payload_digest(representatives)
    assert len(support_six_profiles()) == EXPECTED_SUPPORT6_PROFILES
    assert candidate_count == EXPECTED_SUPPORT6_CANDIDATES
    assert len(six_atoms) == EXPECTED_SUPPORT6_RAW_ATOMS
    assert raw_digest == EXPECTED_SUPPORT6_RAW_SHA256
    assert representatives == EXPECTED_SUPPORT6_REPRESENTATIVES
    assert orbit_digest == EXPECTED_SUPPORT6_ORBIT_SHA256
    assert tuple(report["normalized_preimages"] for report in reports) == (12, 12)
    assert all(
        report["multiplicity_signature"] == (4, 4, 4, 3, 3, 1)
        and report["middle_layers_8_15"] == (218, 225, 225, 218, 202, 173, 134, 88)
        and report["middle_nonzero_union"] == 342
        and not report["escape"]
        for report in reports
    )
    print("SUPPORT5 normalized zero-sum candidates:", len(five_candidates))
    print("SUPPORT5 raw atoms:", len(five_atoms))
    print("SUPPORT6 profiles:", len(support_six_profiles()))
    print("SUPPORT6 normalized zero-sum candidates:", candidate_count)
    print("SUPPORT6 raw normalized atom hits:", len(six_atoms))
    print("SUPPORT6 raw atom SHA256:", raw_digest)
    print("SUPPORT6 GL_q orbits:", len(reports))
    print("SUPPORT6 orbit representative SHA256:", orbit_digest)
    for index, report in enumerate(reports, 1):
        serial = dict(report)
        serial["representative"] = [list(value) for value in serial["representative"]]
        serial["escape"] = [list(value) for value in serial["escape"]]
        print("SUPPORT6 ORBIT", index, json.dumps(serial, separators=(",", ":")))
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--support7", action="store_true")
    parser.add_argument("--start-profile", type=int, default=1)
    parser.add_argument("--stop-profile", type=int)
    args = parser.parse_args()

    if not args.support7:
        run_support_at_most_six()
        print("CERTIFIED: every target atom of support at most six is classified")
        print("STATUS: structural finite layer; supports seven and above not covered")
        return

    profiles, atoms, profile_reports = support_seven_shard(
        args.start_profile, args.stop_profile
    )
    reports = orbit_report(atoms)
    print("SUPPORT7 total canonical profiles:", len(profiles))
    print("SUPPORT7 completed profile interval:", (args.start_profile, profile_reports[-1]["profile_index"] if profile_reports else args.start_profile - 1))
    print("SUPPORT7 shard raw atom hits:", len(atoms))
    print("SUPPORT7 shard raw atom SHA256:", payload_digest(atoms))
    print("SUPPORT7 shard GL_q keys:", len(reports))
    nonempty = tuple(report for report in reports if report["escape"])
    print("SUPPORT7 shard nonempty full-singleton escape keys:", len(nonempty))
    for index, report in enumerate(nonempty, 1):
        serial = dict(report)
        serial["representative"] = [list(value) for value in serial["representative"]]
        serial["escape"] = [list(value) for value in serial["escape"]]
        print("SUPPORT7 ESCAPE ORBIT", index, json.dumps(serial, separators=(",", ":")))
    if args.start_profile == 1 and (args.stop_profile is None or args.stop_profile >= len(profiles)):
        print("CERTIFIED: the full support-seven normalized profile list was exhausted")
    else:
        print("STATUS: complete deterministic support-seven profile shard only")


if __name__ == "__main__":
    main()
