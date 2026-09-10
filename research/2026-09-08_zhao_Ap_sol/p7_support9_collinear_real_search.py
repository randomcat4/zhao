#!/usr/bin/env python3
"""Exact collinear support-nine quotient search for p=7.

This is the lower-DFS interface promised by ``p7_m34_support9_search``.
It fixes a genuine collinear triple Q,E2,C and an outside point E3, searches
the remaining five projective support values (four free, one forced by the
total sum), and keeps all repeated positions in every subset-sum layer.

For each complete length-19 quotient atom it applies the exact six-position
tail conditions from ``p7_tail_conditioned_middle_spectrum``.  A quotient
tail survivor is expanded to 25 distinct positions; every quotient-zero
block of length 2..8 is reconstructed, the length 9..16 gap is checked
directly, and every short block whose quotient complement is an atom is
recorded.  No height, Hasse, or actual C_7^4 condition is asserted here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Sequence

import p7_length19_support7_escape_search as FAST
import p7_m34_support9_search as OLD


P = 7
ZERO_ID = FAST.ZERO_ID
Q_ID = FAST.Q_ID
E2_ID = FAST.E2_ID
E3_ID = FAST.E3_ID
FIXED_BASIS_IDS = (Q_ID, E2_ID, E3_ID)
PLANE_WEIGHT_CAP = OLD.PLANE_WEIGHT_CAP
TARGET_SIGNATURES = (
    (3, 3, 3, 3, 3, 1, 1, 1, 1),
    (3, 3, 2, 2, 2, 2, 2, 2, 1),
    (4, 4, 4, 2, 1, 1, 1, 1, 1),
    (4, 4, 3, 3, 1, 1, 1, 1, 1),
)
EXPECTED_PROFILE_COUNTS = (56, 118, 197, 282)


def payload_digest(items: Iterable[object]) -> str:
    serial = json.dumps(tuple(items), sort_keys=True, separators=(",", ":"), default=list)
    return hashlib.sha256(serial.encode("ascii")).hexdigest()


def add_layers(
    layers: tuple[int, ...], value_id: int, multiplicity: int, maximum: int = 15
) -> tuple[int, ...]:
    """Add repeated actual positions to fixed-cardinality sum masks."""
    answer = [0] * (maximum + 1)
    multiples = FAST.SCALE_ID[value_id]
    for old_size, old_mask in enumerate(layers):
        if not old_mask:
            continue
        for coefficient in range(min(multiplicity, maximum - old_size) + 1):
            answer[old_size + coefficient] |= FAST.translate_mask(
                old_mask, multiples[coefficient]
            )
    return tuple(answer)


EMPTY_LAYERS = (1,) + (0,) * 15


def negate_mask(mask: int) -> int:
    answer = 0
    while mask:
        least = mask & -mask
        value_id = least.bit_length() - 1
        answer |= 1 << FAST.NEG_ID[value_id]
        mask ^= least
    return answer


def union_layers(layers: Sequence[int], lower: int, upper: int) -> int:
    answer = 0
    for size in range(lower, upper + 1):
        answer |= layers[size]
    return answer


def singleton_escape_mask(layers: Sequence[int]) -> int:
    """Exact monotone E1: -t is absent from B layers 8..15."""
    forbidden_tail_values = negate_mask(union_layers(layers, 8, 15))
    return FAST.NONZERO_MASK & ~forbidden_tail_values


def tail_forbidden_masks(layers: Sequence[int]) -> dict[int, int]:
    """Forbidden sums of j tail positions for the exact middle gap."""
    return {
        j: negate_mask(union_layers(layers, 9 - j, 16 - j))
        for j in (1, 2, 3)
    }


def fixed_forbidden_mask(
    fixed_ids: Sequence[int], fixed_multiplicities: Sequence[int]
) -> tuple[int, bool]:
    """All negatives of nonempty fixed-part coefficient sums.

    The Boolean is true exactly when the fixed part already has a nonempty
    zero-sum submultiset, in which case no completion can be an atom.
    """
    forbidden = 0
    has_zero_relation = False
    for coefficients in product(
        *(range(multiplicity + 1) for multiplicity in fixed_multiplicities)
    ):
        if not any(coefficients):
            continue
        subtotal = ZERO_ID
        for value_id, coefficient in zip(fixed_ids, coefficients):
            subtotal = FAST.add_id(subtotal, FAST.SCALE_ID[value_id][coefficient])
        forbidden |= 1 << FAST.NEG_ID[subtotal]
        has_zero_relation |= subtotal == ZERO_ID
    return forbidden, has_zero_relation


def add_plane_weight(packed: int, value_id: int, multiplicity: int):
    return OLD.add_plane_weight(packed, value_id, multiplicity)


def initial_state(
    fixed_ids: Sequence[int], fixed_multiplicities: Sequence[int]
):
    subtotal = ZERO_ID
    layers = EMPTY_LAYERS
    plane_weights = 0
    for value_id, multiplicity in zip(fixed_ids, fixed_multiplicities):
        subtotal = FAST.add_id(subtotal, FAST.SCALE_ID[value_id][multiplicity])
        layers = add_layers(layers, value_id, multiplicity)
        plane_weights = add_plane_weight(plane_weights, value_id, multiplicity)
        if plane_weights is None:
            break
    return subtotal, layers, plane_weights


def profiles_for_signature(signature: Sequence[int]):
    signature = tuple(signature)
    return tuple(
        profile
        for profile_signature, profile in OLD.collinear_multiplicity_profiles()
        if tuple(profile_signature) == signature
    )


def c_ids():
    return tuple(
        FAST.vector_id((u, v, 0))
        for u in range(1, P)
        for v in range(1, P)
    )


COLLINEAR_C_IDS = c_ids()
assert len(COLLINEAR_C_IDS) == 36


def collinear_pair(value_id: int) -> tuple[int, int]:
    u, v, z = FAST.VECTORS[value_id]
    assert u and v and z == 0
    return u, v


def swap_ab(pair: tuple[int, int]) -> tuple[int, int]:
    u, v = pair
    return v, u


def swap_ac(pair: tuple[int, int]) -> tuple[int, int]:
    u, v = pair
    return pow(u, -1, P), (-v * pow(u, -1, P)) % P


def swap_bc(pair: tuple[int, int]) -> tuple[int, int]:
    u, v = pair
    return (-u * pow(v, -1, P)) % P, pow(v, -1, P)


def c_orbits(m_q: int, m_e2: int, m_c: int):
    """Orbits of the collinear scalar C under equal-weight point swaps."""
    generators = []
    if m_q == m_e2:
        generators.append(swap_ab)
    if m_q == m_c:
        generators.append(swap_ac)
    if m_e2 == m_c:
        generators.append(swap_bc)
    universe = {(u, v) for u in range(1, P) for v in range(1, P)}
    unseen = set(universe)
    orbits = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        frontier = [seed]
        while frontier:
            current = frontier.pop()
            for generator in generators:
                image = generator(current)
                assert image in universe
                if image not in orbit:
                    orbit.add(image)
                    frontier.append(image)
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))
    assert set().union(*(set(orbit) for orbit in orbits)) == universe
    assert sum(map(len, orbits)) == 36
    return tuple(sorted(orbits))


def c_representative_ids(m_q: int, m_e2: int, m_c: int):
    return tuple(
        FAST.vector_id((orbit[0][0], orbit[0][1], 0))
        for orbit in c_orbits(m_q, m_e2, m_c)
    )


def allowed_extra_ids(multiplicity: int, outside_anchor_multiplicity: int):
    return tuple(
        value_id
        for value_id in range(1, P**3)
        if not (
            FAST.VECTORS[value_id][2] != 0
            and multiplicity > outside_anchor_multiplicity
        )
    )


def respects_known_order(
    assigned: Sequence[int | None], index: int, value_id: int
) -> bool:
    for other_index, other_id in enumerate(assigned):
        if other_id is None:
            continue
        if other_index < index and other_id >= value_id:
            return False
        if other_index > index and value_id >= other_id:
            return False
    return True


def tail_extension_ok(
    prefix: tuple[int, ...], label: int, forbidden: dict[int, int]
) -> bool:
    """Check every newly completed tail subset of sizes one through three."""
    for size in range(1, min(3, len(prefix) + 1) + 1):
        for old_indices in combinations(range(len(prefix)), size - 1):
            subtotal = label
            for index in old_indices:
                subtotal = FAST.add_id(subtotal, prefix[index])
            if (forbidden[size] >> subtotal) & 1:
                return False
    return True


def enumerate_exact_tails(layers: Sequence[int]):
    """Enumerate S_6-orbits satisfying sum zero and all L1/L2/L3 rows."""
    forbidden = tail_forbidden_masks(layers)
    unary = tuple(
        value_id
        for value_id in range(1, P**3)
        if not ((forbidden[1] >> value_id) & 1)
    )
    unary_index = {value_id: index for index, value_id in enumerate(unary)}
    counts = Counter()
    survivors = []

    def walk(prefix: tuple[int, ...], start: int, subtotal: int):
        if len(prefix) == 5:
            counts["tail_depth5_prefixes"] += 1
            last = FAST.NEG_ID[subtotal]
            last_index = unary_index.get(last)
            if last_index is None:
                counts["tail_forced_not_unary"] += 1
                return
            if last_index < start:
                counts["tail_forced_order_pruned"] += 1
                return
            if not tail_extension_ok(prefix, last, forbidden):
                counts["tail_forced_L123_pruned"] += 1
                return
            completed = prefix + (last,)
            assert FAST.add_id(subtotal, last) == ZERO_ID
            survivors.append(completed)
            return
        for unary_i in range(start, len(unary)):
            label = unary[unary_i]
            counts[f"tail_depth{len(prefix) + 1}_entered"] += 1
            if not tail_extension_ok(prefix, label, forbidden):
                counts[f"tail_depth{len(prefix) + 1}_L123_pruned"] += 1
                continue
            counts[f"tail_depth{len(prefix) + 1}_survived"] += 1
            walk(prefix + (label,), unary_i, FAST.add_id(subtotal, label))

    walk((), 0, ZERO_ID)
    return unary, dict(sorted(counts.items())), tuple(survivors)


def position_layers(labels: Sequence[int], maximum: int) -> tuple[int, ...]:
    layers = (1,) + (0,) * maximum
    for label in labels:
        answer = list(layers)
        for size in range(maximum, 0, -1):
            answer[size] |= FAST.translate_mask(layers[size - 1], label)
        layers = tuple(answer)
    return layers


def all_short_zero_blocks(labels: Sequence[int]):
    """Reconstruct all actual-position quotient-zero masks of sizes 2..8."""
    blocks: list[tuple[int, int]] = []
    by_length = Counter()
    hasher = hashlib.sha256()
    for length in range(2, 9):
        for indices in combinations(range(len(labels)), length):
            subtotal = ZERO_ID
            mask = 0
            for index in indices:
                subtotal = FAST.add_id(subtotal, labels[index])
                mask |= 1 << index
            if subtotal != ZERO_ID:
                continue
            blocks.append((length, mask))
            by_length[length] += 1
            hasher.update(bytes((length,)) + mask.to_bytes(4, "little"))
    return tuple(blocks), dict(sorted(by_length.items())), hasher.hexdigest()


def exact_position_report(atom_labels: Sequence[int], tail: Sequence[int]):
    z_labels = tuple(atom_labels) + tuple(tail)
    assert len(z_labels) == 25
    layers = position_layers(z_labels, 16)
    middle_zero_lengths = tuple(
        length for length in range(9, 17) if (layers[length] >> ZERO_ID) & 1
    )
    blocks, by_length, block_hash = all_short_zero_blocks(z_labels)
    complement_atom_counts = Counter()
    complement_atom_hasher = hashlib.sha256()
    for length, mask in blocks:
        is_atom = not any(other_mask & mask == 0 for _other_length, other_mask in blocks)
        if is_atom:
            complement_atom_counts[length] += 1
            complement_atom_hasher.update(bytes((length,)) + mask.to_bytes(4, "little"))
    return {
        "middle_zero_lengths": middle_zero_lengths,
        "short_block_count": len(blocks),
        "short_block_counts_by_length": by_length,
        "short_block_stream_sha256": block_hash,
        "short_blocks_with_atomic_complement_by_length": dict(
            sorted(complement_atom_counts.items())
        ),
        "atomic_complement_block_stream_sha256": complement_atom_hasher.hexdigest(),
    }


def search_profile(
    signature_index: int,
    profile_index: int,
    profile: Sequence[int],
    prefix_tail_depth: int,
    use_c_symmetry: bool,
):
    m_q, m_e2, m_c, m_e3, *extra_multiplicities = tuple(profile)
    extra_multiplicities = tuple(extra_multiplicities)
    assert len(extra_multiplicities) == 5
    signature = tuple(sorted(profile, reverse=True))
    counts = Counter()
    complete_hasher = hashlib.sha256()
    atom_hasher = hashlib.sha256()
    tail_hasher = hashlib.sha256()
    position_reports = []

    forced_index = max(
        index
        for index, multiplicity in enumerate(extra_multiplicities)
        if multiplicity == min(extra_multiplicities)
    )
    traversal = tuple(
        sorted(
            (index for index in range(5) if index != forced_index),
            key=lambda index: (-extra_multiplicities[index], index),
        )
    )
    allowed_by_multiplicity = {
        multiplicity: allowed_extra_ids(multiplicity, m_e3)
        for multiplicity in set(extra_multiplicities)
    }

    representative_c_ids = (
        c_representative_ids(m_q, m_e2, m_c)
        if use_c_symmetry
        else COLLINEAR_C_IDS
    )
    counts["raw_collinear_c_frames"] = 36
    counts["collinear_c_orbits"] = len(representative_c_ids)
    for c_id in representative_c_ids:
        counts["collinear_c_entered"] += 1
        fixed_ids = (Q_ID, E2_ID, E3_ID, c_id)
        fixed_multiplicities = (m_q, m_e2, m_e3, m_c)
        fixed_lines = frozenset(OLD.LINE_KEYS[value_id] for value_id in fixed_ids)
        assert len(fixed_lines) == 4
        forbidden, fixed_has_zero = fixed_forbidden_mask(
            fixed_ids, fixed_multiplicities
        )
        if fixed_has_zero:
            counts["collinear_c_fixed_atomic_pruned"] += 1
            continue
        fixed_sum, base_layers, base_plane_weights = initial_state(
            fixed_ids, fixed_multiplicities
        )
        if base_plane_weights is None:
            counts["collinear_c_plane_pruned"] += 1
            continue

        assigned: list[int | None] = [None] * 5

        def finish(reachable: int, lines, subtotal: int, layers, plane_weights: int):
            forced_multiplicity = extra_multiplicities[forced_index]
            forced = FAST.SCALE_ID[FAST.NEG_ID[subtotal]][
                pow(forced_multiplicity, -1, P)
            ]
            if forced == ZERO_ID or OLD.LINE_KEYS[forced] in fixed_lines:
                counts["forced_fixed_invalid_pruned"] += 1
                return
            if OLD.LINE_KEYS[forced] in lines:
                counts["forced_projective_pruned"] += 1
                return
            if FAST.VECTORS[forced][2] != 0 and forced_multiplicity > m_e3:
                counts["forced_outside_max_pruned"] += 1
                return
            if not respects_known_order(assigned, forced_index, forced):
                counts["forced_order_pruned"] += 1
                return
            final_plane_weights = add_plane_weight(
                plane_weights, forced, forced_multiplicity
            )
            if final_plane_weights is None:
                counts["forced_plane_pruned"] += 1
                return

            assigned[forced_index] = forced
            extra_ids = tuple(value_id for value_id in assigned if value_id is not None)
            assert len(extra_ids) == 5
            support_ids = fixed_ids + tuple(assigned)  # type: ignore[arg-type]
            multiplicities = fixed_multiplicities + extra_multiplicities
            counts["complete_zero_sum_candidates"] += 1
            payload = (
                bytes((signature_index,))
                + profile_index.to_bytes(2, "little")
                + c_id.to_bytes(2, "little")
                + b"".join(value_id.to_bytes(2, "little") for value_id in support_ids)
                + bytes(multiplicities)
            )
            complete_hasher.update(payload)
            full_layers = add_layers(layers, forced, forced_multiplicity)
            escape = singleton_escape_mask(full_layers)
            if not escape:
                counts["complete_full_singleton_empty_pruned"] += 1
                assigned[forced_index] = None
                return
            counts["complete_full_singleton_nonempty"] += 1
            if not FAST.bounded_atom(support_ids, multiplicities):
                counts["complete_nonatom_pruned"] += 1
                assigned[forced_index] = None
                return
            counts["complete_atoms"] += 1
            atom_hasher.update(payload)
            if not OLD.six_tail_possible_mask(escape):
                counts["complete_atom_six_sumset_pruned"] += 1
                assigned[forced_index] = None
                return
            counts["complete_atom_six_sumset_possible"] += 1
            unary, tail_counts, tails = enumerate_exact_tails(full_layers)
            counts.update(tail_counts)
            if not tails:
                counts["complete_atom_exact_tail_empty"] += 1
                assigned[forced_index] = None
                return
            counts["complete_atom_exact_tail_nonempty"] += 1
            atom_labels = FAST.expanded(support_ids, multiplicities)
            for tail in tails:
                counts["exact_tail_survivors"] += 1
                tail_payload = payload + b"".join(
                    value_id.to_bytes(2, "little") for value_id in tail
                )
                tail_hasher.update(tail_payload)
                position = exact_position_report(atom_labels, tail)
                assert not position["middle_zero_lengths"]
                fibre_counts = Counter(atom_labels)
                position_reports.append(
                    {
                        "instance_id": hashlib.sha256(tail_payload).hexdigest(),
                        "atom_labels": atom_labels,
                        "tail": tail,
                        "z_position_labels": atom_labels + tail,
                        "distinguished_m3_label_ids": tuple(
                            sorted(label for label, count in fibre_counts.items() if count == 3)
                        ),
                        "distinguished_m4_label_ids": tuple(
                            sorted(label for label, count in fibre_counts.items() if count == 4)
                        ),
                        "height_adapter_status": (
                            "quotient skeleton only; expand each distinguished fibre separately "
                            "before calling the m3/m4 full height validator"
                        ),
                        "unary_domain_size": len(unary),
                        **position,
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
                if OLD.LINE_KEYS[value_id] in fixed_lines or OLD.LINE_KEYS[value_id] in lines:
                    continue
                if not respects_known_order(assigned, index, value_id):
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
                next_layers = add_layers(layers, value_id, multiplicity)
                if depth + 1 >= prefix_tail_depth:
                    partial_escape = singleton_escape_mask(next_layers)
                    if not OLD.six_tail_possible_mask(partial_escape):
                        counts[f"depth{depth + 1}_tail_pruned"] += 1
                        assigned[index] = None
                        continue
                counts[f"depth{depth + 1}_survived"] += 1
                visit(
                    depth + 1,
                    next_reachable,
                    lines | {OLD.LINE_KEYS[value_id]},
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
            frozenset(),
            fixed_sum,
            base_layers,
            base_plane_weights,
        )

    return {
        "signature_index": signature_index,
        "profile_index": profile_index,
        "profile": tuple(profile),
        "signature": signature,
        "forced_variable_index": forced_index,
        "traversal": traversal,
        "prefix_tail_depth": prefix_tail_depth,
        "c_symmetry_mode": "full-signature-S3-closure" if use_c_symmetry else "none",
        "counts": dict(sorted(counts.items())),
        "complete_sha256": complete_hasher.hexdigest(),
        "atom_sha256": atom_hasher.hexdigest(),
        "exact_tail_sha256": tail_hasher.hexdigest(),
        "position_reports": tuple(position_reports),
    }


def write_report(path: Path, report) -> str:
    serial = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=list)
    path.write_text(serial + "\n", encoding="utf-8", newline="\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def self_test():
    assert tuple(len(profiles_for_signature(signature)) for signature in TARGET_SIGNATURES) == EXPECTED_PROFILE_COUNTS
    sample = (Q_ID, E2_ID, E3_ID, FAST.vector_id((1, 1, 0)))
    forbidden, has_zero = fixed_forbidden_mask(sample, (1, 1, 1, 1))
    assert not has_zero and forbidden
    full_orbits = c_orbits(3, 3, 3)
    assert tuple(sorted(map(len, full_orbits))) == (1, 2, 3, 3, 3, 3, 3, 6, 6, 6)
    assert tuple(orbit[0] for orbit in full_orbits) == (
        (1, 1), (1, 2), (1, 3), (2, 2), (2, 3),
        (2, 6), (3, 3), (3, 5), (3, 6), (6, 6),
    )
    assert len(c_orbits(3, 3, 1)) == 21
    assert len(c_orbits(3, 2, 1)) == 36
    for labels in (
        (Q_ID, E2_ID),
        (Q_ID, E2_ID, E3_ID),
        (Q_ID, Q_ID, E2_ID),
    ):
        layers = position_layers(labels, min(16, len(labels)))
        for size in range(len(labels) + 1):
            direct = set()
            for indices in combinations(range(len(labels)), size):
                subtotal = ZERO_ID
                for index in indices:
                    subtotal = FAST.add_id(subtotal, labels[index])
                direct.add(subtotal)
            assert set(FAST.mask_ids(layers[size])) == direct


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--signature", type=int, choices=range(1, len(TARGET_SIGNATURES) + 1), required=True)
    parser.add_argument("--start-profile", type=int, default=1)
    parser.add_argument("--stop-profile", type=int)
    parser.add_argument("--prefix-tail-depth", type=int, default=2)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--skip-self-test", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.prefix_tail_depth not in range(1, 5):
        raise ValueError("prefix-tail-depth must lie in 1..4")
    if not args.skip_self_test:
        self_test()

    signature = TARGET_SIGNATURES[args.signature - 1]
    profiles = profiles_for_signature(signature)
    stop = len(profiles) if args.stop_profile is None else min(args.stop_profile, len(profiles))
    if not 1 <= args.start_profile <= stop:
        raise ValueError("invalid profile interval")
    full_signature = args.start_profile == 1 and stop == len(profiles)
    reports = []
    aggregate = Counter()
    position_reports = []
    profile_hasher = hashlib.sha256()
    for profile_index in range(args.start_profile, stop + 1):
        report = search_profile(
            args.signature,
            profile_index,
            profiles[profile_index - 1],
            args.prefix_tail_depth,
            full_signature,
        )
        position_reports.extend(report.pop("position_reports"))
        aggregate.update(report["counts"])
        serial = json.dumps(report, sort_keys=True, separators=(",", ":"), default=list)
        profile_hasher.update(serial.encode("ascii"))
        reports.append(report)
        if not args.quiet:
            print("COLLINEAR PROFILE", serial, flush=True)

    result = {
        "schema": "p7-support9-collinear-real-v1",
        "scope": (
            "exact quotient-position search for one collinear-normalized support-nine signature; "
            "full B atomicity, exact six-tail L1/L2/L3, all induced length-2..8 quotient-zero blocks, "
            "and direct length-9..16 gap; no heights/Hasse/actual-C7^4 claim"
        ),
        "signature_index": args.signature,
        "signature": signature,
        "signature_profile_denominator": len(profiles),
        "completed_profile_interval": (args.start_profile, stop),
        "full_signature": full_signature,
        "c_symmetry_mode": "full-signature-S3-closure" if full_signature else "none",
        "profile_count": len(reports),
        "prefix_tail_depth": args.prefix_tail_depth,
        "aggregate": dict(sorted(aggregate.items())),
        "profile_report_sha256": profile_hasher.hexdigest(),
        "exact_tail_survivor_count": len(position_reports),
        "exact_tail_survivor_sha256": payload_digest(position_reports),
        "profiles": reports,
        "position_reports": position_reports,
    }
    summary = {key: value for key, value in result.items() if key not in {"profiles", "position_reports"}}
    print("COLLINEAR TOTAL", json.dumps(summary, separators=(",", ":"), default=list), flush=True)
    if full_signature and not position_reports:
        print("CERTIFIED: complete signature has no exact six-tail quotient extension")
    elif full_signature:
        print("CERTIFIED: complete signature quotient survivors are listed with exact position spectra")
    else:
        print("COVERAGE: deterministic collinear profile shard only")
    if args.report is not None:
        digest = write_report(args.report, result)
        print("REPORT:", args.report)
        print("REPORT SHA256:", digest)
    print("STATUS: exact finite quotient-position slice; global A_p remains incomplete")


if __name__ == "__main__":
    main()
