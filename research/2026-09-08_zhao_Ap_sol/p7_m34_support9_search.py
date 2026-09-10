#!/usr/bin/env python3
"""Canonical support-nine frontier for the p=7 exact-three/four union.

The search is deliberately organized as an unpointed cache.  Every target
atom either has maximum multiplicity four, in which case a fourfold fibre is
normalized to Q, or has maximum multiplicity three, in which case a threefold
fibre is normalized to Q.  Pointed q^3 and q^4 consequences are recovered
from the multiplicities of the unpointed atom after the quotient obstruction
has been tested.

Each profile shard is exhaustive for its printed interval.  A survivor is a
necessary quotient-layer object, not a counterexample to the full theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Iterable, Sequence

import p7_length19_support7_escape_search as FAST


P = 7
ORDER = P**3
ZERO_ID = FAST.ZERO_ID
Q_ID = FAST.Q_ID
E2_ID = FAST.E2_ID
E3_ID = FAST.E3_ID
VECTORS = FAST.VECTORS
FIXED_IDS = (Q_ID, E2_ID, E3_ID)
EXPECTED_PROFILE_COUNTS = {3: 358, 4: 476}
LIGHT_PROFILE_INTERVALS = {3: (1, 1), 4: (1, 7)}
PLANE_WEIGHT_CAP = 11
EXPECTED_UNPOINTED_SIGNATURES = 13
EXPECTED_COLLINEAR_PROFILES = 5_741
EXPECTED_EMPTY_SHA256 = "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
EXPECTED_LIGHT_SHARDS = {
    (3, 1, 1): {
        "aggregate": {
            "complete_empty_escape_pruned": 2,
            "complete_zero_sum_candidates": 2,
            "depth1_atomic_pruned": 52,
            "depth1_entered": 324,
            "depth1_survived": 272,
            "depth2_atomic_pruned": 21_853,
            "depth2_entered": 44_876,
            "depth2_survived": 23_023,
            "depth3_atomic_pruned": 2_303_455,
            "depth3_entered": 2_615_422,
            "depth3_survived": 303_819,
            "depth3_tail_pruned": 8_148,
            "depth4_atomic_pruned": 27_344_257,
            "depth4_entered": 27_604_871,
            "depth4_survived": 219_759,
            "depth4_tail_pruned": 40_855,
            "depth5_atomic_pruned": 17_415_161,
            "depth5_entered": 17_415_441,
            "depth5_survived": 68,
            "depth5_tail_pruned": 212,
            "forced_order_pruned": 66,
        },
        "profile_report_sha256": "8f646487a4d7f9d85a004358d948e7b87601de2930352473dfaff204332d7ae7",
    },
    (4, 1, 7): {
        "aggregate": {
            "depth1_atomic_pruned": 385,
            "depth1_entered": 1_980,
            "depth1_survived": 1_595,
            "depth2_atomic_pruned": 148_234,
            "depth2_entered": 262_868,
            "depth2_survived": 114_634,
            "depth3_atomic_pruned": 12_224_598,
            "depth3_entered": 13_228_550,
            "depth3_plane_pruned": 2_522,
            "depth3_survived": 900_276,
            "depth3_tail_pruned": 101_154,
            "depth4_atomic_pruned": 81_134_934,
            "depth4_entered": 81_890_334,
            "depth4_plane_pruned": 274_332,
            "depth4_survived": 350_478,
            "depth4_tail_pruned": 130_590,
            "depth5_atomic_pruned": 21_622_308,
            "depth5_entered": 23_281_014,
            "depth5_plane_pruned": 1_658_706,
        },
        "profile_report_sha256": "b6d269bb7569c5759b6549738333ce8c05fa14cf3463ade6b59357cf598b3691",
    },
}


def line_key(value: tuple[int, int, int]) -> tuple[int, int, int]:
    first = next(entry for entry in value if entry)
    return FAST.scale_value(pow(first, -1, P), value)


LINE_KEYS = tuple(line_key(value) if value != FAST.ZERO else None for value in VECTORS)
FIXED_LINES = frozenset(LINE_KEYS[value_id] for value_id in FIXED_IDS)
PROJECTIVE_POINTS = tuple(sorted(set(LINE_KEYS[1:])))
assert len(PROJECTIVE_POINTS) == 57
PLANES_CONTAINING = tuple(
    tuple(
        plane_index
        for plane_index, normal in enumerate(PROJECTIVE_POINTS)
        if sum(normal[coordinate] * value[coordinate] for coordinate in range(3)) % P == 0
    )
    for value in VECTORS
)
assert all(len(PLANES_CONTAINING[value_id]) == 8 for value_id in range(1, ORDER))


def normalized_profiles(anchor_multiplicity: int):
    """Profiles after choosing a largest non-anchor fibre as E2.

    For anchor 4 this covers every target with a fourfold fibre.  For anchor
    3 the range is capped at three, so it covers exactly the remaining targets
    whose maximum multiplicity is three.
    """
    if anchor_multiplicity not in (3, 4):
        raise ValueError("anchor multiplicity must be 3 or 4")
    profiles = tuple(
        profile
        for profile in product(range(1, anchor_multiplicity + 1), repeat=8)
        if sum(profile) == 19 - anchor_multiplicity
        and profile[0] == max(profile)
    )
    assert len(profiles) == EXPECTED_PROFILE_COUNTS[anchor_multiplicity]
    return profiles


def support_signature(anchor_multiplicity: int, profile: Sequence[int]):
    return tuple(sorted((anchor_multiplicity,) + tuple(profile), reverse=True))


def unpointed_signatures():
    """All support-nine multiplicity signatures in the target union."""
    signatures = tuple(
        sorted(
            {
                tuple(sorted(profile, reverse=True))
                for profile in product(range(1, 5), repeat=9)
                if sum(profile) == 19
            }
        )
    )
    assert len(signatures) == EXPECTED_UNPOINTED_SIGNATURES
    return signatures


def collinear_multiplicity_profiles():
    """Complete profile denominator for the collinear-triple normalization.

    The first three entries are the multiplicities on a collinear triple,
    sorted decreasingly.  The fourth is a largest multiplicity outside that
    line, and the final five are attached to the remaining support values in
    increasing vector-id order.  This function records the strictly smaller
    future DFS interface; the current anchor search does not rely on it.
    """
    profiles = []
    for signature in unpointed_signatures():
        triple_multisets = {
            tuple(sorted((signature[index] for index in indices), reverse=True))
            for indices in combinations(range(9), 3)
        }
        for triple in sorted(triple_multisets, reverse=True):
            remainder = list(signature)
            for multiplicity in triple:
                remainder.remove(multiplicity)
            # The chosen three-point line may contain further support points,
            # so the largest multiplicity among all six remaining points need
            # not occur outside the line.  Enumerate every possible E3
            # multiplicity; a search using this interface must then require
            # every remaining z!=0 point to have multiplicity at most m(E3).
            for outside_maximum in sorted(set(remainder), reverse=True):
                tail_values = remainder.copy()
                tail_values.remove(outside_maximum)
                for tail in sorted(set(permutations(tail_values))):
                    profiles.append((signature, triple + (outside_maximum,) + tail))
    answer = tuple(profiles)
    assert len(answer) == EXPECTED_COLLINEAR_PROFILES
    return answer


def basis_forbidden_mask(anchor_multiplicity: int, m2: int, m3: int):
    answer = 0
    for c1 in range(anchor_multiplicity + 1):
        for c2 in range(m2 + 1):
            for c3 in range(m3 + 1):
                if c1 == c2 == c3 == 0:
                    continue
                basis_sum = FAST.vector_id((c1 % P, c2 % P, c3 % P))
                answer |= 1 << FAST.NEG_ID[basis_sum]
    return answer


def add_plane_weight(packed: int, value_id: int, multiplicity: int):
    """Add one fibre or reject a >11 intersection with a two-space."""
    answer = packed
    for plane_index in PLANES_CONTAINING[value_id]:
        shift = 4 * plane_index
        weight = ((answer >> shift) & 15) + multiplicity
        if weight > PLANE_WEIGHT_CAP:
            return None
        answer += multiplicity << shift
    return answer


def initial_plane_weights(anchor_multiplicity: int, m2: int, m3: int):
    answer = 0
    for value_id, multiplicity in (
        (Q_ID, anchor_multiplicity),
        (E2_ID, m2),
        (E3_ID, m3),
    ):
        answer = add_plane_weight(answer, value_id, multiplicity)
        assert answer is not None
    return answer


def negate_mask(mask: int):
    answer = 0
    while mask:
        least = mask & -mask
        value_id = least.bit_length() - 1
        answer |= 1 << FAST.NEG_ID[value_id]
        mask ^= least
    return answer


def sumset(mask: int, allowed_ids: Sequence[int]):
    answer = 0
    for value_id in allowed_ids:
        answer |= FAST.translate_mask(mask, value_id)
        if answer == FAST.ALL_MASK:
            break
    return answer


def six_tail_possible_mask(escape: int):
    """Exact test for 0 in the repeated six-fold sumset of E1."""
    if not escape:
        return False
    allowed_ids = FAST.mask_ids(escape)
    twice = sumset(escape, allowed_ids)
    thrice = sumset(twice, allowed_ids)
    if thrice.bit_count() >= 172:
        return True
    return bool(thrice & negate_mask(thrice))


def payload_digest(items: Iterable[object]):
    serial = json.dumps(tuple(items), sort_keys=True, separators=(",", ":"), default=list)
    return hashlib.sha256(serial.encode("ascii")).hexdigest()


def candidate_payload(
    anchor_multiplicity: int,
    profile_index: int,
    support_ids: Sequence[int],
    multiplicities: Sequence[int],
):
    return (
        bytes((anchor_multiplicity,))
        + profile_index.to_bytes(2, "little")
        + b"".join(value_id.to_bytes(2, "little") for value_id in support_ids)
        + bytes(multiplicities)
    )


def canonical_gl_key(labels: Sequence[int]):
    """Canonicalize an unpointed position multiset under GL(3,7)."""
    support = tuple(sorted(set(labels)))
    best = None
    for first in support:
        for second in support:
            if second == first:
                continue
            for third in support:
                columns = (VECTORS[first], VECTORS[second], VECTORS[third])
                if third in (first, second) or FAST.determinant(columns) == 0:
                    continue
                transform = FAST.inverse_matrix(FAST.matrix_from_columns(columns))
                image = tuple(
                    sorted(
                        FAST.vector_id(FAST.matrix_vector(transform, VECTORS[value_id]))
                        for value_id in labels
                    )
                )
                if best is None or image < best:
                    best = image
    assert best is not None
    return best


def allowed_extra_ids(multiplicity: int, m3: int):
    return tuple(
        value_id
        for value_id in range(1, ORDER)
        if LINE_KEYS[value_id] not in FIXED_LINES
        and not (VECTORS[value_id][2] != 0 and multiplicity > m3)
    )


def search_profile(
    anchor_multiplicity: int,
    profile_index: int,
    profile: Sequence[int],
    prefix_tail_depth: int = 3,
):
    m2, m3, *extra_multiplicities = profile
    extra_multiplicities = tuple(extra_multiplicities)
    assert len(extra_multiplicities) == 6
    multiplicities = (anchor_multiplicity,) + tuple(profile)
    forbidden = basis_forbidden_mask(anchor_multiplicity, m2, m3)
    fixed_sum = FAST.vector_id(
        (anchor_multiplicity % P, m2 % P, m3 % P)
    )

    base_layers = FAST.EMPTY_LAYERS
    for value_id, multiplicity in zip(FIXED_IDS, multiplicities[:3]):
        base_layers = FAST.add_repeated_positions(base_layers, value_id, multiplicity)
    base_plane_weights = initial_plane_weights(anchor_multiplicity, m2, m3)
    allowed_by_multiplicity = {
        multiplicity: allowed_extra_ids(multiplicity, m3)
        for multiplicity in set(extra_multiplicities)
    }

    forced_index = max(
        index
        for index, multiplicity in enumerate(extra_multiplicities)
        if multiplicity == min(extra_multiplicities)
    )
    traversal = tuple(
        sorted(
            (index for index in range(6) if index != forced_index),
            key=lambda index: (-extra_multiplicities[index], index),
        )
    )
    assigned: list[int | None] = [None] * 6
    counts = Counter()
    complete_hasher = hashlib.sha256()
    e1_atom_hasher = hashlib.sha256()
    viable_atom_hasher = hashlib.sha256()
    viable_atoms = []

    def respects_known_order(index: int, value_id: int):
        for other_index, other_id in enumerate(assigned):
            if other_id is None:
                continue
            if other_index < index and other_id >= value_id:
                return False
            if other_index > index and value_id >= other_id:
                return False
        return True

    def finish(reachable: int, lines, subtotal: int, layers, plane_weights: int):
        forced_multiplicity = extra_multiplicities[forced_index]
        inverse = pow(forced_multiplicity, -1, P)
        forced = FAST.SCALE_ID[FAST.NEG_ID[subtotal]][inverse]
        if forced == ZERO_ID or LINE_KEYS[forced] in FIXED_LINES:
            counts["forced_invalid_pruned"] += 1
            return
        if LINE_KEYS[forced] in lines:
            counts["forced_projective_pruned"] += 1
            return
        if VECTORS[forced][2] != 0 and forced_multiplicity > m3:
            counts["forced_outside_max_pruned"] += 1
            return
        if not respects_known_order(forced_index, forced):
            counts["forced_order_pruned"] += 1
            return
        final_plane_weights = add_plane_weight(
            plane_weights, forced, forced_multiplicity
        )
        if final_plane_weights is None:
            counts["forced_plane_pruned"] += 1
            return

        assigned[forced_index] = forced
        extras = tuple(value_id for value_id in assigned if value_id is not None)
        assert len(extras) == 6
        support_ids = FIXED_IDS + tuple(assigned)  # type: ignore[arg-type]
        counts["complete_zero_sum_candidates"] += 1
        payload = candidate_payload(
            anchor_multiplicity, profile_index, support_ids, multiplicities
        )
        complete_hasher.update(payload)
        full_layers = FAST.add_repeated_positions(
            layers, forced, forced_multiplicity
        )
        escape = FAST.escape_mask(full_layers)
        if not escape:
            counts["complete_empty_escape_pruned"] += 1
            assigned[forced_index] = None
            return
        counts["complete_nonempty_escape"] += 1
        if not FAST.bounded_atom(support_ids, multiplicities):
            counts["complete_nonempty_escape_nonatoms"] += 1
            assigned[forced_index] = None
            return
        counts["complete_nonempty_escape_atoms"] += 1
        labels = FAST.expanded(support_ids, multiplicities)
        e1_atom_hasher.update(payload)
        if not six_tail_possible_mask(escape):
            counts["complete_atom_six_tail_pruned"] += 1
            assigned[forced_index] = None
            return
        counts["tail_viable_atoms"] += 1
        viable_atom_hasher.update(payload)
        viable_atoms.append(
            {
                "labels": labels,
                "escape": FAST.mask_ids(escape),
                "unpointed_key": canonical_gl_key(labels),
            }
        )
        assigned[forced_index] = None

    def visit(
        depth: int,
        reachable: int,
        lines,
        subtotal: int,
        layers,
        plane_weights: int,
    ):
        if depth == len(traversal):
            finish(reachable, lines, subtotal, layers, plane_weights)
            return
        index = traversal[depth]
        multiplicity = extra_multiplicities[index]
        for value_id in allowed_by_multiplicity[multiplicity]:
            if LINE_KEYS[value_id] in lines or not respects_known_order(index, value_id):
                continue
            counts[f"depth{depth + 1}_entered"] += 1
            next_plane_weights = add_plane_weight(
                plane_weights, value_id, multiplicity
            )
            if next_plane_weights is None:
                counts[f"depth{depth + 1}_plane_pruned"] += 1
                continue
            next_reachable = FAST.extend_atomic_prefix(
                reachable, value_id, multiplicity, forbidden
            )
            if next_reachable is None:
                counts[f"depth{depth + 1}_atomic_pruned"] += 1
                continue
            assigned[index] = value_id
            next_layers = FAST.add_repeated_positions(
                layers, value_id, multiplicity
            )
            if depth + 1 >= prefix_tail_depth:
                partial_escape = FAST.escape_mask(next_layers)
                if not six_tail_possible_mask(partial_escape):
                    counts[f"depth{depth + 1}_tail_pruned"] += 1
                    assigned[index] = None
                    continue
            counts[f"depth{depth + 1}_survived"] += 1
            visit(
                depth + 1,
                next_reachable,
                lines | {LINE_KEYS[value_id]},
                FAST.add_id(
                    subtotal, FAST.SCALE_ID[value_id][multiplicity]
                ),
                next_layers,
                next_plane_weights,
            )
            assigned[index] = None

    visit(
        0,
        1,
        FIXED_LINES,
        fixed_sum,
        base_layers,
        base_plane_weights,
    )
    return {
        "anchor_multiplicity": anchor_multiplicity,
        "profile_index": profile_index,
        "profile": tuple(profile),
        "signature": support_signature(anchor_multiplicity, profile),
        "forced_variable_index": forced_index,
        "traversal": traversal,
        "prefix_tail_depth": prefix_tail_depth,
        "counts": dict(sorted(counts.items())),
        "complete_sha256": complete_hasher.hexdigest(),
        "nonempty_escape_atom_sha256": e1_atom_hasher.hexdigest(),
        "tail_viable_atom_sha256": viable_atom_hasher.hexdigest(),
        "tail_viable_atoms": tuple(viable_atoms),
    }


def self_test():
    assert tuple(len(normalized_profiles(anchor)) for anchor in (3, 4)) == (358, 476)
    assert len(unpointed_signatures()) == EXPECTED_UNPOINTED_SIGNATURES
    assert len(collinear_multiplicity_profiles()) == EXPECTED_COLLINEAR_PROFILES
    assert support_signature(3, normalized_profiles(3)[0]) == (3,) + (2,) * 8
    assert all(
        support_signature(4, normalized_profiles(4)[index])
        == (4,) + (2,) * 7 + (1,)
        for index in range(7)
    )
    for mask in (1, 2, 7, (1 << 97) | (1 << 246), FAST.NONZERO_MASK):
        allowed = FAST.mask_ids(mask & FAST.NONZERO_MASK)
        direct = FAST.zero_sum_tail_multiset_count(allowed) > 0
        assert six_tail_possible_mask(mask & FAST.NONZERO_MASK) == direct
    prior = next(labels for name, labels, _escape in __import__(
        "verify_p7_maximal_atom_escape_algebra"
    ).ATOMS if name == "prior_B0")
    packed = 0
    for value, multiplicity in Counter(prior).items():
        packed = add_plane_weight(packed, FAST.vector_id(value), multiplicity)
        assert packed is not None


def write_report(path: Path, report):
    serial = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=list)
    path.write_text(serial + "\n", encoding="utf-8", newline="\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--anchor", type=int, choices=(3, 4))
    parser.add_argument("--start-profile", type=int, default=1)
    parser.add_argument("--stop-profile", type=int)
    parser.add_argument("--light-slice", action="store_true")
    parser.add_argument("--prefix-tail-depth", type=int, default=3)
    parser.add_argument("--skip-self-test", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.prefix_tail_depth not in range(1, 6):
        raise ValueError("prefix-tail-depth must be between 1 and 5")
    if not args.skip_self_test:
        self_test()

    if args.light_slice:
        if args.anchor is not None or args.start_profile != 1 or args.stop_profile is not None:
            raise ValueError("--light-slice cannot be combined with an explicit shard")
        jobs = tuple(
            (anchor, profile_index, normalized_profiles(anchor)[profile_index - 1])
            for anchor in (3, 4)
            for profile_index in range(
                LIGHT_PROFILE_INTERVALS[anchor][0],
                LIGHT_PROFILE_INTERVALS[anchor][1] + 1,
            )
        )
    else:
        if args.anchor is None:
            raise ValueError("choose --anchor 3 or 4, or use --light-slice")
        profiles = normalized_profiles(args.anchor)
        stop = len(profiles) if args.stop_profile is None else min(args.stop_profile, len(profiles))
        if not 1 <= args.start_profile <= stop:
            raise ValueError("invalid profile interval")
        jobs = tuple(
            (args.anchor, profile_index, profiles[profile_index - 1])
            for profile_index in range(args.start_profile, stop + 1)
        )

    reports = []
    viable_atoms = []
    aggregate = Counter()
    report_hasher = hashlib.sha256()
    for anchor, profile_index, profile in jobs:
        report = search_profile(
            anchor,
            profile_index,
            profile,
            prefix_tail_depth=args.prefix_tail_depth,
        )
        viable_atoms.extend(report.pop("tail_viable_atoms"))
        serial = json.dumps(report, sort_keys=True, separators=(",", ":"), default=list)
        report_hasher.update(serial.encode("ascii"))
        reports.append(report)
        aggregate.update(report["counts"])
        if not args.quiet:
            print("SUPPORT9 PROFILE", serial, flush=True)

    orbit_groups = defaultdict(list)
    for atom in viable_atoms:
        orbit_groups[tuple(atom["unpointed_key"])].append(atom)
    orbit_reports = []
    for key in sorted(orbit_groups):
        multiplicities = Counter(key)
        orbit_reports.append(
            {
                "unpointed_key": key,
                "normalized_preimages": len(orbit_groups[key]),
                "exact_three_fibres": sum(value == 3 for value in multiplicities.values()),
                "exact_four_fibres": sum(value == 4 for value in multiplicities.values()),
            }
        )
    result = {
        "schema": "p7-m34-support9-frontier-v1",
        "scope": "unpointed maximum-four plus maximum-three support-nine quotient frontier",
        "jobs": tuple((anchor, index, tuple(profile)) for anchor, index, profile in jobs),
        "profile_count": len(reports),
        "prefix_tail_depth": args.prefix_tail_depth,
        "aggregate": dict(sorted(aggregate.items())),
        "profile_report_sha256": report_hasher.hexdigest(),
        "tail_viable_unpointed_orbits": len(orbit_reports),
        "tail_viable_orbit_sha256": payload_digest(orbit_reports),
        "profiles": reports,
        "tail_viable_orbits": orbit_reports,
    }
    shard_key = None
    if not args.light_slice and jobs:
        shard_key = (jobs[0][0], jobs[0][1], jobs[-1][1])
    if args.prefix_tail_depth == 3 and shard_key in EXPECTED_LIGHT_SHARDS:
        expected = EXPECTED_LIGHT_SHARDS[shard_key]
        assert result["aggregate"] == expected["aggregate"]
        assert result["profile_report_sha256"] == expected["profile_report_sha256"]
        assert result["tail_viable_unpointed_orbits"] == 0
        assert result["tail_viable_orbit_sha256"] == EXPECTED_EMPTY_SHA256
    print(
        "SUPPORT9 TOTAL",
        json.dumps(
            {key: value for key, value in result.items() if key not in {"profiles", "tail_viable_orbits"}},
            separators=(",", ":"),
            default=list,
        ),
        flush=True,
    )
    if args.light_slice:
        assert len(reports) == 8
        print("COVERAGE: exact light slice, anchor-3 profile 1 and anchor-4 profiles 1..7")
    else:
        print("COVERAGE: exact deterministic profile shard only")
    if args.report is not None:
        digest = write_report(args.report, result)
        print("REPORT:", args.report)
        print("REPORT SHA256:", digest)
    print("STATUS: finite quotient frontier only; survivors are necessary conditions")


if __name__ == "__main__":
    main()
