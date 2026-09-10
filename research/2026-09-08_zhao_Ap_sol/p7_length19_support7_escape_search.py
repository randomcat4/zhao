#!/usr/bin/env python3
"""Search support-seven length-19 atoms with nonempty singleton escape.

The distinguished quotient value q=(1,0,0) has multiplicity exactly three;
all other multiplicities are at most four.  The 170 normalized multiplicity
profiles and the canonical-basis coverage rule are the ones proved in
``p7_length19_canonical_augmentation.py``.

This program searches only the necessary-condition frontier E1(B) != empty.
Its extra pruning is exact for that purpose: for a position prefix P, if the
fixed-cardinality position-subset sums in sizes 4,...,11 already cover every
nonzero value of C_7^3, then every completion B contains the same subsets and
has E1(B)=empty.  No conclusion about atoms with empty E1 is reported.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter, defaultdict
from itertools import product
from typing import Iterable, Sequence


P = 7
ORDER = P**3
ZERO = (0, 0, 0)
Q = (1, 0, 0)
E2 = (0, 1, 0)
E3 = (0, 0, 1)
VECTORS = tuple(product(range(P), repeat=3))


def vector_id(value: tuple[int, int, int]) -> int:
    return P * P * value[0] + P * value[1] + value[2]


ZERO_ID = vector_id(ZERO)
Q_ID = vector_id(Q)
E2_ID = vector_id(E2)
E3_ID = vector_id(E3)
ALL_MASK = (1 << ORDER) - 1
NONZERO_MASK = ALL_MASK ^ 1
BASE_IDS = frozenset((ZERO_ID, Q_ID, E2_ID, E3_ID))
EXTRA_IDS = tuple(index for index in range(ORDER) if index not in BASE_IDS)

EXPECTED_FULL_COUNTERS = {
    "first_ordered": 38_292,
    "first_atomic_pruned": 15_246,
    "first_escape_pruned": 0,
    "pair_ordered": 3_042_639,
    "pair_atomic_pruned": 2_338_466,
    "pair_escape_pruned": 0,
    "third_ordered": 70_041_761,
    "third_atomic_pruned": 68_427_632,
    "third_escape_pruned": 0,
    "final_zero_sum_candidates": 381_309,
    "final_escape_pruned": 377_381,
    "final_nonatoms": 3_912,
    "target_atom_hits": 16,
}
EXPECTED_FULL_ATOM_SHA256 = "d7e282662b04ef8fe0bbe8de790344c06b0ab1fd60f7279dbf13b00b2fc0fb2a"
EXPECTED_FULL_ORBIT_SHA256 = "1f2d355af2c2713413d90a9efd8483919958979314f695a29037dc27f871b32f"


def add_value(left: tuple[int, int, int], right: tuple[int, int, int]):
    return tuple((left[index] + right[index]) % P for index in range(3))


def scale_value(scalar: int, value: tuple[int, int, int]):
    return tuple((scalar * entry) % P for entry in value)


ADD_ID = tuple(
    tuple(vector_id(add_value(left, right)) for right in VECTORS)
    for left in VECTORS
)
NEG_ID = tuple(vector_id(scale_value(-1, value)) for value in VECTORS)
SCALE_ID = tuple(
    tuple(vector_id(scale_value(coefficient, value)) for coefficient in range(P))
    for value in VECTORS
)


def add_id(left: int, right: int) -> int:
    return ADD_ID[left][right]


# The id layout is x*49+y*7+z.  These masks implement cyclic translation in
# each coordinate using only big-integer shifts and Boolean operations.
Z_NONWRAP = tuple(
    ALL_MASK
    if shift == 0
    else sum(((1 << (P - shift)) - 1) << (P * block) for block in range(P * P))
    for shift in range(P)
)
Y_NONWRAP = tuple(
    ALL_MASK
    if shift == 0
    else sum(
        ((1 << (P * (P - shift))) - 1) << (P * P * block)
        for block in range(P)
    )
    for shift in range(P)
)
X_NONWRAP = tuple(
    ALL_MASK if shift == 0 else (1 << (P * P * (P - shift))) - 1
    for shift in range(P)
)


def translate_mask(mask: int, value_id: int) -> int:
    """Translate a subset of C_7^3 by one group value."""
    dx, dy, dz = VECTORS[value_id]
    if dz:
        nonwrap = Z_NONWRAP[dz]
        mask = ((mask & nonwrap) << dz) | ((mask & (ALL_MASK ^ nonwrap)) >> (P - dz))
    if dy:
        shift = P * dy
        wrap = P * (P - dy)
        nonwrap = Y_NONWRAP[dy]
        mask = ((mask & nonwrap) << shift) | ((mask & (ALL_MASK ^ nonwrap)) >> wrap)
    if dx:
        shift = P * P * dx
        wrap = P * P * (P - dx)
        nonwrap = X_NONWRAP[dx]
        mask = ((mask & nonwrap) << shift) | ((mask & (ALL_MASK ^ nonwrap)) >> wrap)
    return mask


def add_repeated_positions(
    layers: tuple[int, ...], value_id: int, multiplicity: int
) -> tuple[int, ...]:
    """Add actual repeated positions to fixed-cardinality subset-sum layers."""
    answer = [0] * 12
    multiples = SCALE_ID[value_id]
    for old_size, old_mask in enumerate(layers):
        if not old_mask:
            continue
        for coefficient in range(min(multiplicity, 11 - old_size) + 1):
            answer[old_size + coefficient] |= translate_mask(
                old_mask, multiples[coefficient]
            )
    return tuple(answer)


EMPTY_LAYERS = (1,) + (0,) * 11


def covered_nonzero(layers: Sequence[int]) -> int:
    answer = 0
    for size in range(4, 12):
        answer |= layers[size]
    return answer & NONZERO_MASK


def escape_mask(layers: Sequence[int]) -> int:
    return NONZERO_MASK ^ covered_nonzero(layers)


def mask_ids(mask: int) -> tuple[int, ...]:
    answer = []
    while mask:
        least = mask & -mask
        answer.append(least.bit_length() - 1)
        mask ^= least
    return tuple(answer)


def forbidden_basis_mask(m2: int, m3: int) -> int:
    answer = 0
    for c1 in range(4):
        for c2 in range(m2 + 1):
            for c3 in range(m3 + 1):
                if c1 == c2 == c3 == 0:
                    continue
                basis_sum = vector_id((c1 % P, c2 % P, c3 % P))
                answer |= 1 << NEG_ID[basis_sum]
    return answer


def extend_atomic_prefix(
    reachable: int,
    value_id: int,
    multiplicity: int,
    forbidden: int,
) -> int | None:
    """Extend extras, rejecting every zero relation inside a proper prefix.

    ``reachable`` contains the sums of coefficient choices on earlier extra
    support values.  The empty choice is its only zero-sum choice because every
    accepted state was checked inductively.  A positive coefficient on the new
    value produces an extras-only zero relation exactly when the inverse sum is
    already reachable.  Any nonzero target in ``forbidden`` completes with a
    nonempty allowed basis coefficient vector.  Since this is called only
    before the forced last support value is inserted, every such relation is a
    proper submultiset of every final completion.
    """
    answer = reachable
    multiples = SCALE_ID[value_id]
    for coefficient in range(1, multiplicity + 1):
        shift = multiples[coefficient]
        if reachable & (1 << NEG_ID[shift]):
            return None
        answer |= translate_mask(reachable, shift)
    if answer & forbidden:
        return None
    return answer


def support_seven_profiles():
    return tuple(
        profile
        for profile in product(range(1, 5), repeat=6)
        if sum(profile) == 16 and profile[0] == max(profile)
    )


def allowed_extra_ids(multiplicity: int, m3: int):
    return tuple(
        value_id
        for value_id in EXTRA_IDS
        if not (VECTORS[value_id][2] != 0 and multiplicity > m3)
    )


def bounded_atom(support_ids: Sequence[int], multiplicities: Sequence[int]) -> bool:
    """Exact atom test by forcing the three basis coefficients modulo seven."""
    assert tuple(support_ids[:3]) == (Q_ID, E2_ID, E3_ID)
    basis_bounds = multiplicities[:3]
    extra_ids = support_ids[3:]
    extra_bounds = multiplicities[3:]
    full = tuple(multiplicities)
    zero = (0,) * len(multiplicities)
    for extra_coefficients in product(*(range(bound + 1) for bound in extra_bounds)):
        sx = sy = sz = 0
        for coefficient, value_id in zip(extra_coefficients, extra_ids):
            x, y, z = VECTORS[value_id]
            sx += coefficient * x
            sy += coefficient * y
            sz += coefficient * z
        relation = ((-sx) % P, (-sy) % P, (-sz) % P) + tuple(extra_coefficients)
        if any(
            coefficient > bound
            for coefficient, bound in zip(relation[:3], basis_bounds)
        ):
            continue
        if relation not in (zero, full):
            return False
    return True


def expanded(support_ids: Sequence[int], multiplicities: Sequence[int]):
    return tuple(
        sorted(
            value_id
            for value_id, multiplicity in zip(support_ids, multiplicities)
            for _ in range(multiplicity)
        )
    )


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


def canonical_q_key(labels: Sequence[int]):
    label_vectors = tuple(VECTORS[value_id] for value_id in labels)
    support = tuple(sorted(set(label_vectors)))
    others = tuple(value for value in support if value != Q)
    best = None
    for first in others:
        for second in others:
            if first == second or determinant((Q, first, second)) == 0:
                continue
            transform = inverse_matrix(matrix_from_columns((Q, first, second)))
            image = tuple(
                sorted(vector_id(matrix_vector(transform, value)) for value in label_vectors)
            )
            if best is None or image < best:
                best = image
    assert best is not None
    return best


def payload_digest(sequences: Iterable[Sequence[int]]) -> str:
    serial = [list(sequence) for sequence in sorted(sequences)]
    return hashlib.sha256(json.dumps(serial, separators=(",", ":")).encode("ascii")).hexdigest()


def direct_position_layers(labels: Sequence[int], maximum: int = 15):
    layers = [set() for _ in range(maximum + 1)]
    layers[0].add(ZERO_ID)
    for index, label in enumerate(labels):
        for size in range(min(maximum, index + 1), 0, -1):
            layers[size].update(ADD_ID[old][label] for old in layers[size - 1])
    return tuple(frozenset(layer) for layer in layers)


def zero_sum_tail_multiset_count(allowed_ids: Sequence[int], length: int = 6) -> int:
    """Count unordered quotient-label multisets of fixed length and sum zero."""
    counts = {(0, ZERO_ID): 1}
    for value_id in allowed_ids:
        updated = dict(counts)
        for (used, old_sum), count in counts.items():
            for copies in range(1, length - used + 1):
                key = (used + copies, add_id(old_sum, SCALE_ID[value_id][copies % P]))
                updated[key] = updated.get(key, 0) + count
        counts = updated
    return counts.get((length, ZERO_ID), 0)


def self_test():
    for value_id in range(ORDER):
        for old_id in range(ORDER):
            assert translate_mask(1 << old_id, value_id) == 1 << ADD_ID[old_id][value_id]
    sample = ((Q_ID, 3), (E2_ID, 4), (E3_ID, 2), (vector_id((2, 3, 4)), 3))
    layers = EMPTY_LAYERS
    labels = []
    for value_id, multiplicity in sample:
        layers = add_repeated_positions(layers, value_id, multiplicity)
        labels.extend((value_id,) * multiplicity)
    direct = direct_position_layers(labels, 11)
    assert all(mask_ids(layers[size]) == tuple(sorted(direct[size])) for size in range(12))
    assert len(support_seven_profiles()) == 170


def empty_counters():
    return {
        "first_ordered": 0,
        "first_atomic_pruned": 0,
        "first_escape_pruned": 0,
        "pair_ordered": 0,
        "pair_atomic_pruned": 0,
        "pair_escape_pruned": 0,
        "third_ordered": 0,
        "third_atomic_pruned": 0,
        "third_escape_pruned": 0,
        "final_zero_sum_candidates": 0,
        "final_escape_pruned": 0,
        "final_nonatoms": 0,
        "target_atom_hits": 0,
    }


def search_profile(profile_index: int, profile: Sequence[int]):
    started = time.perf_counter()
    counters = empty_counters()
    target_atoms = []
    m2, m3, m_first, m_second, m_third, m_last = profile
    multiplicities = (3,) + tuple(profile)
    forbidden = forbidden_basis_mask(m2, m3)

    base_layers = EMPTY_LAYERS
    for value_id, multiplicity in ((Q_ID, 3), (E2_ID, m2), (E3_ID, m3)):
        base_layers = add_repeated_positions(base_layers, value_id, multiplicity)
    if covered_nonzero(base_layers) == NONZERO_MASK:
        raise AssertionError("the fixed basis prefix unexpectedly covers all nonzero values")

    first_values = allowed_extra_ids(m_first, m3)
    second_values = allowed_extra_ids(m_second, m3)
    third_values = allowed_extra_ids(m_third, m3)
    inverse_last = pow(m_last, -1, P)
    fixed_sum = vector_id((3 % P, m2 % P, m3 % P))

    for first in first_values:
        counters["first_ordered"] += 1
        first_reachable = extend_atomic_prefix(1, first, m_first, forbidden)
        if first_reachable is None:
            counters["first_atomic_pruned"] += 1
            continue
        first_layers = add_repeated_positions(base_layers, first, m_first)
        if covered_nonzero(first_layers) == NONZERO_MASK:
            counters["first_escape_pruned"] += 1
            continue

        for second in second_values:
            if second <= first:
                continue
            counters["pair_ordered"] += 1
            second_reachable = extend_atomic_prefix(
                first_reachable, second, m_second, forbidden
            )
            if second_reachable is None:
                counters["pair_atomic_pruned"] += 1
                continue
            second_layers = add_repeated_positions(first_layers, second, m_second)
            if covered_nonzero(second_layers) == NONZERO_MASK:
                counters["pair_escape_pruned"] += 1
                continue

            for third in third_values:
                if third <= second:
                    continue
                counters["third_ordered"] += 1
                third_reachable = extend_atomic_prefix(
                    second_reachable, third, m_third, forbidden
                )
                if third_reachable is None:
                    counters["third_atomic_pruned"] += 1
                    continue
                third_layers = add_repeated_positions(second_layers, third, m_third)
                if covered_nonzero(third_layers) == NONZERO_MASK:
                    counters["third_escape_pruned"] += 1
                    continue

                subtotal = add_id(
                    fixed_sum,
                    add_id(
                        add_id(SCALE_ID[first][m_first], SCALE_ID[second][m_second]),
                        SCALE_ID[third][m_third],
                    ),
                )
                last = SCALE_ID[NEG_ID[subtotal]][inverse_last]
                if last in BASE_IDS or last <= third:
                    continue
                if VECTORS[last][2] != 0 and m_last > m3:
                    continue
                counters["final_zero_sum_candidates"] += 1

                full_layers = add_repeated_positions(third_layers, last, m_last)
                remaining = escape_mask(full_layers)
                if not remaining:
                    counters["final_escape_pruned"] += 1
                    continue
                support = (Q_ID, E2_ID, E3_ID, first, second, third, last)
                if not bounded_atom(support, multiplicities):
                    counters["final_nonatoms"] += 1
                    continue
                labels = expanded(support, multiplicities)
                assert len(labels) == 19
                assert sum(Counter(labels).values()) == 19
                assert remaining == escape_mask(full_layers)
                direct = direct_position_layers(labels, 15)
                direct_low = set().union(*(direct[size] for size in range(4, 12)))
                assert set(mask_ids(remaining)) == set(range(1, ORDER)) - direct_low
                middle = set().union(*(direct[size] for size in range(8, 16)))
                direct_e1 = {
                    value_id for value_id in range(1, ORDER) if NEG_ID[value_id] not in middle
                }
                assert direct_e1 == set(mask_ids(remaining))
                target_atoms.append(labels)
                counters["target_atom_hits"] += 1

    elapsed = time.perf_counter() - started
    report = {
        "profile_index": profile_index,
        "profile": tuple(profile),
        **counters,
        "target_atom_sha256": payload_digest(target_atoms),
        "elapsed_seconds": round(elapsed, 6),
    }
    return report, tuple(target_atoms)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-profile", type=int, default=1)
    parser.add_argument("--stop-profile", type=int)
    parser.add_argument("--skip-self-test", action="store_true")
    args = parser.parse_args()

    if not args.skip_self_test:
        self_test()
    profiles = support_seven_profiles()
    stop = len(profiles) if args.stop_profile is None else min(args.stop_profile, len(profiles))
    if not (1 <= args.start_profile <= stop + 1):
        raise ValueError("invalid profile interval")

    all_atoms = []
    profile_reports = []
    aggregate = empty_counters()
    started = time.perf_counter()
    for profile_index in range(args.start_profile, stop + 1):
        report, atoms = search_profile(profile_index, profiles[profile_index - 1])
        profile_reports.append(report)
        all_atoms.extend(atoms)
        for key in aggregate:
            aggregate[key] += report[key]
        print("SUPPORT7 ESCAPE PROFILE", json.dumps(report, separators=(",", ":")), flush=True)

    orbit_groups = defaultdict(list)
    for atom in all_atoms:
        orbit_groups[canonical_q_key(atom)].append(atom)
    orbit_keys = tuple(sorted(orbit_groups))
    completed = (
        args.start_profile,
        profile_reports[-1]["profile_index"] if profile_reports else args.start_profile - 1,
    )
    final = {
        "total_profiles": len(profiles),
        "completed_interval": completed,
        **aggregate,
        "target_atom_sha256": payload_digest(all_atoms),
        "target_orbits_within_shard": len(orbit_keys),
        "target_orbit_sha256": payload_digest(orbit_keys),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    full_run = completed == (1, len(profiles))
    if full_run:
        assert aggregate == EXPECTED_FULL_COUNTERS
        assert final["target_atom_sha256"] == EXPECTED_FULL_ATOM_SHA256
        assert len(orbit_keys) == 4
        assert final["target_orbit_sha256"] == EXPECTED_FULL_ORBIT_SHA256
        assert tuple(len(orbit_groups[key]) for key in orbit_keys) == (6, 2, 6, 2)
    print("SUPPORT7 ESCAPE TOTAL", json.dumps(final, separators=(",", ":")), flush=True)
    for index, key in enumerate(orbit_keys, 1):
        direct = direct_position_layers(key, 15)
        middle = set().union(*(direct[size] for size in range(8, 16)))
        escapes = tuple(
            value_id for value_id in range(1, ORDER) if NEG_ID[value_id] not in middle
        )
        tail_count = zero_sum_tail_multiset_count(escapes)
        serial = {
            "index": index,
            "representative": [list(VECTORS[value_id]) for value_id in key],
            "normalized_preimages_in_shard": len(orbit_groups[key]),
            "escape": [list(VECTORS[value_id]) for value_id in escapes],
            "zero_sum_six_tail_multisets": tail_count,
        }
        print("SUPPORT7 ESCAPE ORBIT", json.dumps(serial, separators=(",", ":")))
        if full_run:
            assert len(escapes) == 1
            assert tail_count == 0
    if full_run:
        print("CERTIFIED: all 170 normalized support-seven profiles were exhausted")
        print("CERTIFIED: every target orbit has singleton E1 and no zero-sum six-tail")
        print("STATUS: support seven cannot extend; supports >=8 not covered")
    else:
        print("STATUS: complete deterministic profile shard only; union before orbit claims")


if __name__ == "__main__":
    main()
