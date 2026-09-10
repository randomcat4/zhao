#!/usr/bin/env python3
"""Complete profile shards for the support-eight p=7,m=3 atom frontier.

The distinguished quotient value q=(1,0,0) occurs three times.  Every other
value occurs between one and four times.  This program enumerates normalized
support-eight zero-sum candidates, retaining only candidates that can still
have a six-position zero-sum tail whose entries lie in the complete singleton
escape set.

Each requested profile interval is exhaustive for exactly that interval.  A
survivor is only a necessary quotient-layer checkpoint, never a counterexample.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import product

import p7_length19_canonical_augmentation as old


P = 7
ZERO = old.ZERO
Q = old.Q
E2 = old.E2
E3 = old.E3
ALL_NONZERO = old.ALL_NONZERO
FIXED = (Q, E2, E3)
FIXED_LINES = frozenset()
EXPECTED_PROFILES = 462
EXPECTED_FULL_AGGREGATE = {
    "complete_tail_pruned": 1_846,
    "complete_zero_sum_candidates": 1_846,
    "depth1_atomic_pruned": 29_239,
    "depth1_entered": 54_648,
    "depth1_survived": 25_409,
    "depth2_atomic_pruned": 3_314_714,
    "depth2_entered": 3_802_701,
    "depth2_survived": 487_987,
    "depth3_atomic_pruned": 55_372_517,
    "depth3_entered": 55_938_687,
    "depth3_survived": 566_170,
    "depth4_atomic_pruned": 55_129_186,
    "depth4_entered": 55_156_682,
    "depth4_survived": 27_496,
    "forced_invalid_pruned": 12_835,
    "forced_order_pruned": 5_140,
    "forced_projective_pruned": 7_675,
}
EXPECTED_FULL_REPORT_SHA256 = "25cdd6726db7605d5981e6c024d8ea6b7885ee2d4c87953700f852550559c0f5"
EXPECTED_EMPTY_ORBIT_SHA256 = "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
VECTOR_ID = {value: old.vector_id(value) for value in old.ALL}
VECTORS = old.ALL
ZERO_ID = VECTOR_ID[ZERO]
TRANSLATE = tuple(
    tuple(VECTOR_ID[old.add(VECTORS[current], offset)] for current in range(P**3))
    for offset in VECTORS
)
SCALE_ID = tuple(
    tuple(VECTOR_ID[old.scale(coefficient, value)] for coefficient in range(5))
    for value in VECTORS
)


def line_key(value):
    """Canonical projective point containing a nonzero vector."""
    first = next(entry for entry in value if entry)
    return old.scale(pow(first, -1, P), value)


FIXED_LINES = frozenset(line_key(value) for value in FIXED)


def support_eight_profiles():
    """All normalized ordered multiplicity profiles.

    After choosing a largest non-q fibre as e2, its multiplicity is the first
    coordinate and is maximal among all seven non-q multiplicities.
    """
    return tuple(
        profile
        for profile in product(range(1, 5), repeat=7)
        if sum(profile) == 16 and profile[0] == max(profile)
    )


def strict_extend_reachable(reachable, value, multiplicity, forbidden):
    """Extend a proper support prefix or reject a forced proper zero-sum.

    ``reachable`` contains the sums of all coefficient choices on the already
    selected nonbasis support values.  Every nonempty new coefficient choice
    must avoid both zero and the negatives of all nonzero admissible basis
    coefficient sums.  The empty choice remains represented by ZERO.
    """
    extended = set(reachable)
    value_id = VECTOR_ID[value]
    for coefficient in range(1, multiplicity + 1):
        translation = TRANSLATE[SCALE_ID[value_id][coefficient]]
        translated = {translation[current] for current in reachable}
        if ZERO_ID in translated or translated & forbidden:
            return None
        extended.update(translated)
    return frozenset(extended)


def projectively_allowed(value, chosen_lines, multiplicity, m3):
    if value in FIXED or line_key(value) in chosen_lines:
        return False
    if value[2] != 0 and multiplicity > m3:
        return False
    return True


def position_layers_for_blocks(blocks, maximum=11):
    """Exact fixed-cardinality subset supports for value/multiplicity blocks."""
    layers = [set() for _ in range(maximum + 1)]
    layers[0].add(ZERO)
    length = 0
    for value, multiplicity in blocks:
        prior = tuple(frozenset(layer) for layer in layers)
        new_layers = [set(layer) for layer in prior]
        multiples = tuple(old.scale(count, value) for count in range(multiplicity + 1))
        for size in range(maximum + 1):
            for count in range(1, min(multiplicity, size) + 1):
                for subtotal in prior[size - count]:
                    new_layers[size].add(old.add(subtotal, multiples[count]))
        layers = new_layers
        length += multiplicity
    return tuple(frozenset(layer) for layer in layers)


def escape_from_blocks(blocks):
    layers = position_layers_for_blocks(blocks)
    covered = frozenset().union(*(layers[size] for size in range(4, 12)))
    return tuple(value for value in ALL_NONZERO if value not in covered)


def six_tail_possible(escape):
    """Whether six entries, with repetition allowed, can sum to zero."""
    if not escape:
        return False
    reachable = {ZERO}
    for _ in range(6):
        reachable = {
            old.add(subtotal, value)
            for subtotal in reachable
            for value in escape
        }
    return ZERO in reachable


def candidate_payload(profile_index, support, multiplicities):
    return bytes((profile_index & 255, profile_index >> 8)) + bytes(
        [entry for value in support for entry in value] + list(multiplicities)
    )


def enumerate_profile(profile_index, profile, prefix_tail_prune=True):
    m2, m3, m1, m2p, m3p, m4p, m5p = profile
    extra_multiplicities = (m1, m2p, m3p, m4p, m5p)
    basis_bounds = (3, m2, m3)
    forbidden = {
        VECTOR_ID[((-c1) % P, (-c2) % P, (-c3) % P)]
        for c1 in range(basis_bounds[0] + 1)
        for c2 in range(basis_bounds[1] + 1)
        for c3 in range(basis_bounds[2] + 1)
    } - {ZERO_ID}
    fixed_sum = old.add(old.scale(3, Q), old.add(old.scale(m2, E2), old.scale(m3, E3)))
    allowed_by_multiplicity = {
        multiplicity: tuple(
            value
            for value in old.EXTRA_VALUES
            if projectively_allowed(value, FIXED_LINES, multiplicity, m3)
        )
        for multiplicity in set(extra_multiplicities)
    }

    counts = Counter()
    complete_hasher = hashlib.sha256()
    viable_hasher = hashlib.sha256()
    atom_hasher = hashlib.sha256()
    viable_atoms = []

    # Solve the total-sum equation for a smallest-multiplicity extra variable.
    # Enumerate the other four in decreasing multiplicity order so that proper
    # zero-sums are exposed as early as possible.  The x1<...<x5 conditions are
    # attached to variable indices, not to this heuristic traversal order.
    minimum = min(extra_multiplicities)
    forced_index = max(
        index for index, multiplicity in enumerate(extra_multiplicities)
        if multiplicity == minimum
    )
    traversal = tuple(
        sorted(
            (index for index in range(5) if index != forced_index),
            key=lambda index: (-extra_multiplicities[index], index),
        )
    )
    counts["forced_variable_index"] = forced_index
    counts["traversal_code"] = sum((index + 1) * 10**position for position, index in enumerate(traversal))
    assigned = [None] * 5

    def respects_known_order(index, value):
        value_id = old.vector_id(value)
        for other_index, other in enumerate(assigned):
            if other is None:
                continue
            other_id = old.vector_id(other)
            if other_index < index and other_id >= value_id:
                return False
            if other_index > index and value_id >= other_id:
                return False
        return True

    def finish(state, lines, subtotal):
        forced_multiplicity = extra_multiplicities[forced_index]
        forced = old.scale(-pow(forced_multiplicity, -1, P), subtotal)
        if forced in (ZERO, Q, E2, E3):
            counts["forced_invalid_pruned"] += 1
            return
        if forced[2] != 0 and forced_multiplicity > m3:
            counts["forced_plane_pruned"] += 1
            return
        if line_key(forced) in lines:
            counts["forced_projective_pruned"] += 1
            return
        if not respects_known_order(forced_index, forced):
            counts["forced_order_pruned"] += 1
            return

        assigned[forced_index] = forced
        extras = tuple(assigned)
        support = (Q, E2, E3) + extras
        multiplicities = (3,) + profile
        counts["complete_zero_sum_candidates"] += 1
        payload = candidate_payload(profile_index, support, multiplicities)
        complete_hasher.update(payload)

        blocks = tuple(zip(support, multiplicities))
        escape = escape_from_blocks(blocks)
        if not six_tail_possible(escape):
            counts["complete_tail_pruned"] += 1
        else:
            counts["tail_viable_candidates"] += 1
            viable_hasher.update(payload)
            if not old.bounded_atom(support, multiplicities):
                counts["tail_viable_nonatoms"] += 1
            else:
                counts["tail_viable_atoms"] += 1
                atom_hasher.update(payload)
                labels = old.expanded(support, multiplicities)
                viable_atoms.append((labels, escape))
        assigned[forced_index] = None

    def visit(depth, state, lines, subtotal):
        if depth == len(traversal):
            finish(state, lines, subtotal)
            return
        index = traversal[depth]
        multiplicity = extra_multiplicities[index]
        entered_key = f"depth{depth + 1}_entered"
        atomic_key = f"depth{depth + 1}_atomic_pruned"
        survived_key = f"depth{depth + 1}_survived"
        for value in allowed_by_multiplicity[multiplicity]:
            if line_key(value) in lines or not respects_known_order(index, value):
                continue
            counts[entered_key] += 1
            next_state = strict_extend_reachable(state, value, multiplicity, forbidden)
            if next_state is None:
                counts[atomic_key] += 1
                continue
            assigned[index] = value
            if prefix_tail_prune and depth == 2:
                blocks = [(Q, 3), (E2, m2), (E3, m3)]
                blocks.extend(
                    (assigned[position], extra_multiplicities[position])
                    for position in range(5) if assigned[position] is not None
                )
                if not six_tail_possible(escape_from_blocks(tuple(blocks))):
                    counts["depth3_tail_pruned"] += 1
                    assigned[index] = None
                    continue
            counts[survived_key] += 1
            visit(
                depth + 1,
                next_state,
                lines | {line_key(value)},
                old.add(subtotal, old.scale(multiplicity, value)),
            )
            assigned[index] = None

    visit(0, frozenset((ZERO_ID,)), FIXED_LINES, fixed_sum)

    return {
        "profile_index": profile_index,
        "profile": profile,
        "counts": dict(sorted(counts.items())),
        "complete_sha256": complete_hasher.hexdigest(),
        "tail_viable_sha256": viable_hasher.hexdigest(),
        "tail_viable_atom_sha256": atom_hasher.hexdigest(),
        "tail_viable_atoms": tuple(viable_atoms),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-profile", type=int, default=1)
    parser.add_argument("--stop-profile", type=int)
    parser.add_argument(
        "--signature",
        help="comma-separated sorted seven-part non-q signature",
    )
    parser.add_argument("--no-prefix-tail-prune", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    profiles = support_eight_profiles()
    assert len(profiles) == EXPECTED_PROFILES
    selected_signature = None
    if args.signature:
        selected_signature = tuple(sorted(map(int, args.signature.split(",")), reverse=True))
        if len(selected_signature) != 7:
            raise ValueError("signature must have seven entries")

    stop = len(profiles) if args.stop_profile is None else min(args.stop_profile, len(profiles))
    if not (1 <= args.start_profile <= stop):
        raise ValueError("invalid profile interval")

    reports = []
    orbit_groups = defaultdict(list)
    combined = hashlib.sha256()
    aggregate_counts = Counter()
    for profile_index in range(args.start_profile, stop + 1):
        profile = profiles[profile_index - 1]
        if selected_signature is not None and tuple(sorted(profile, reverse=True)) != selected_signature:
            continue
        report = enumerate_profile(
            profile_index,
            profile,
            prefix_tail_prune=not args.no_prefix_tail_prune,
        )
        for labels, escape in report.pop("tail_viable_atoms"):
            orbit_groups[old.canonical_q_key(labels)].append((labels, escape))
        serial = json.dumps(report, sort_keys=True, separators=(",", ":"), default=list)
        combined.update(serial.encode("ascii"))
        reports.append(report)
        aggregate_counts.update(
            {key: value for key, value in report["counts"].items() if not key.endswith("_index") and key != "traversal_code"}
        )
        if not args.quiet:
            print("SUPPORT8 PROFILE", serial, flush=True)

    orbit_reports = []
    for representative in sorted(orbit_groups):
        escapes = {tuple(escape) for _labels, escape in orbit_groups[representative]}
        assert len(escapes) == 1
        orbit_reports.append(
            {
                "representative": representative,
                "normalized_preimages": len(orbit_groups[representative]),
                "escape": next(iter(escapes)),
            }
        )

    orbit_payload = json.dumps(orbit_reports, sort_keys=True, separators=(",", ":"), default=list).encode("ascii")
    report_digest = combined.hexdigest()
    orbit_digest = hashlib.sha256(orbit_payload).hexdigest()
    full_official_run = (
        args.start_profile == 1
        and stop == len(profiles)
        and selected_signature is None
        and args.no_prefix_tail_prune
    )
    if full_official_run:
        assert len(reports) == EXPECTED_PROFILES
        assert dict(sorted(aggregate_counts.items())) == EXPECTED_FULL_AGGREGATE
        assert report_digest == EXPECTED_FULL_REPORT_SHA256
        assert not orbit_reports
        assert orbit_digest == EXPECTED_EMPTY_ORBIT_SHA256
    print("SUPPORT8 total normalized profiles:", len(profiles))
    print("SUPPORT8 executed profiles:", len(reports))
    print("SUPPORT8 aggregate counts:", json.dumps(dict(sorted(aggregate_counts.items())), separators=(",", ":")))
    print("SUPPORT8 report stream SHA256:", report_digest)
    print("SUPPORT8 tail-viable GL_q orbits:", len(orbit_reports))
    print("SUPPORT8 orbit report SHA256:", orbit_digest)
    for index, report in enumerate(orbit_reports, 1):
        print("SUPPORT8 ORBIT", index, json.dumps(report, separators=(",", ":"), default=list))
    if full_official_run:
        print("CERTIFIED: all 462 support-eight profiles have no six-tail-compatible target atom")
    print("STATUS: exhaustive only for the printed profile interval/filter; global branch INCOMPLETE")


if __name__ == "__main__":
    main()
