#!/usr/bin/env python3
"""Structural, monotone pruning for the p=7 support-nine-and-up frontier.

This is not a support-nine atom enumeration.  It verifies exact pointed
multiplicity denominators, the projective-plane load gate, a support-nine
geometry compatibility probe, and low-side tail-spectrum gates which are safe
on every actual-position prefix.  Every solver-facing rejection is a necessary
condition only until a complete length-19 quotient atom has been supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations, combinations_with_replacement


P = 7
ORDER = P**3
ZERO = (0, 0, 0)
Q = (1, 0, 0)
VECTORS = tuple(
    (x, y, z)
    for x in range(P)
    for y in range(P)
    for z in range(P)
)
VECTOR_ID = {value: index for index, value in enumerate(VECTORS)}
ZERO_ID = VECTOR_ID[ZERO]
NONZERO_IDS = tuple(range(1, ORDER))
EXPECTED_PROFILE_STREAM_SHA256 = "b908d1d052668eb5929ff7dee261b0dd3494581ca0390f2d7f4372429c2ce513"
EXPECTED_ARC_SHA256 = "344333c7161106038dcb70e4ec4701d47196b5a956a300c0273197213f262333"
EXPECTED_PLANE_ORBIT_SHA256 = "e82f6d8f4a52cde840c9e7061b0ffcb9b4d209c03643c6d6c7abb24e03962404"
EXPECTED_PLANE_BASIS_WITNESS_SHA256 = "7f8a0434f07b0405a92e2698754e10b6dd32f7a71352268d067f60ac6580ca81"
EXPECTED_SUPPORT9_PROBE_SHA256 = "6639594239b593708d4deff0a5976b138168ae73f241b9c92399a1a137fb3677"
EXPECTED_REPORT_SHA256 = "3d9431053ad7379303b238773077d7503be034e66c320c143f66a19d527d327f"


def add(left, right):
    return tuple((left[i] + right[i]) % P for i in range(3))


def neg(value):
    return tuple((-entry) % P for entry in value)


def scale(coefficient, value):
    return tuple((coefficient * entry) % P for entry in value)


def dot(left, right):
    return sum(left[i] * right[i] for i in range(3)) % P


def cross(left, right):
    return (
        (left[1] * right[2] - left[2] * right[1]) % P,
        (left[2] * right[0] - left[0] * right[2]) % P,
        (left[0] * right[1] - left[1] * right[0]) % P,
    )


def total(values):
    answer = ZERO
    for value in values:
        answer = add(answer, value)
    return answer


def projective_key(value):
    assert value != ZERO
    first = next(entry for entry in value if entry)
    return scale(pow(first, -1, P), value)


PROJECTIVE_POINTS = tuple(
    value for value in VECTORS[1:] if projective_key(value) == value
)
assert len(PROJECTIVE_POINTS) == 57


def position_layers(labels, maximum=15):
    """Exact fixed-cardinality sum supports on labelled positions."""
    layers = [set() for _ in range(maximum + 1)]
    layers[0].add(ZERO_ID)
    for index, label in enumerate(labels):
        label_id = VECTOR_ID[label]
        upper = min(maximum, index + 1)
        for size in range(upper, 0, -1):
            layers[size].update(
                VECTOR_ID[add(VECTORS[subtotal], VECTORS[label_id])]
                for subtotal in layers[size - 1]
            )
    return tuple(frozenset(layer) for layer in layers)


def is_atom(labels):
    """Exact for a zero-sum length-19 sequence, using complement symmetry."""
    assert len(labels) == 19 and total(labels) == ZERO
    layers = position_layers(labels, 9)
    return all(ZERO_ID not in layers[size] for size in range(1, 10))


def is_projectively_simple(labels):
    support = set(labels)
    if ZERO in support:
        return False
    return len({projective_key(value) for value in support}) == len(support)


def plane_loads(blocks):
    """Actual-position loads of all 57 two-dimensional subspaces."""
    return {
        normal: sum(
            multiplicity
            for value, multiplicity in blocks
            if dot(normal, value) == 0
        )
        for normal in PROJECTIVE_POINTS
    }


def plane_support_counts(blocks):
    return {
        normal: sum(1 for value, _multiplicity in blocks if dot(normal, value) == 0)
        for normal in PROJECTIVE_POINTS
    }


def q_plane_bins(blocks, q_value=Q):
    """Bin non-q support values by their direction in G/<q>."""
    answer = {}
    for value, multiplicity in blocks:
        if value == q_value:
            continue
        normal = projective_key(cross(q_value, value))
        answer.setdefault(normal, []).append((value, multiplicity))
    return answer


FRAME = (Q, (0, 1, 0), (0, 0, 1), (1, 1, 1))


def is_arc_extension(chosen, candidate):
    """Whether candidate creates no collinear triple with chosen points."""
    for left, right in combinations(chosen, 2):
        if dot(cross(left, right), candidate) == 0:
            return False
    return True


def fixed_frame_arc_certificate():
    """Exhaust all arcs containing the standard ordered projective frame."""
    assert all(is_arc_extension(FRAME[:index], FRAME[index]) for index in range(3, 4))
    candidates = tuple(
        point
        for point in PROJECTIVE_POINTS
        if point not in FRAME and is_arc_extension(FRAME, point)
    )
    counts = Counter()
    maximal_arcs = []

    def visit(start, chosen):
        counts[len(chosen)] += 1
        extensions = []
        for index in range(start, len(candidates)):
            point = candidates[index]
            if is_arc_extension(chosen, point):
                extensions.append((index, point))
        if not extensions:
            maximal_arcs.append(tuple(sorted(chosen)))
            return
        for index, point in extensions:
            visit(index + 1, chosen + (point,))

    visit(0, FRAME)
    maximum = max(map(len, maximal_arcs))
    maximum_arcs = tuple(sorted(set(arc for arc in maximal_arcs if len(arc) == maximum)))
    payload = json.dumps(maximum_arcs, separators=(",", ":"), default=list).encode("ascii")
    return {
        "frame_candidates": len(candidates),
        "visited_by_size": dict(sorted(counts.items())),
        "maximum": maximum,
        "maximum_fixed_frame_arcs": len(maximum_arcs),
        "maximum_arcs_sha256": hashlib.sha256(payload).hexdigest(),
    }


P2_VECTORS = tuple((x, y) for x in range(P) for y in range(P))
P2_ID = {value: index for index, value in enumerate(P2_VECTORS)}
P2_ZERO_ID = P2_ID[(0, 0)]
P2_E1 = (1, 0)
P2_E2 = (0, 1)
P2_REMAINING_DIRECTIONS = tuple((1, slope) for slope in range(1, P))


def p2_add(left, right):
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def p2_scale(coefficient, value):
    return (coefficient * value[0] % P, coefficient * value[1] % P)


def p2_extend(reachable, value, multiplicity):
    """Add one projectively new block, or reject a zero-sum."""
    new_reachable = set(reachable)
    for copies in range(1, multiplicity + 1):
        offset = p2_scale(copies, value)
        translated = {
            P2_ID[p2_add(P2_VECTORS[subtotal], offset)]
            for subtotal in reachable
        }
        if P2_ZERO_ID in translated:
            return None
        new_reachable.update(translated)
    return frozenset(new_reachable)


def p2_transform_to_basis(first, second, value):
    determinant = (first[0] * second[1] - first[1] * second[0]) % P
    assert determinant
    inverse = pow(determinant, -1, P)
    return (
        (second[1] * value[0] - second[0] * value[1]) * inverse % P,
        (-first[1] * value[0] + first[0] * value[1]) * inverse % P,
    )


def p2_canonical_key(blocks):
    best = None
    for first, _first_multiplicity in blocks:
        for second, _second_multiplicity in blocks:
            if first == second:
                continue
            if (first[0] * second[1] - first[1] * second[0]) % P == 0:
                continue
            image = tuple(sorted(
                (P2_ID[p2_transform_to_basis(first, second, value)], multiplicity)
                for value, multiplicity in blocks
            ))
            if best is None or image < best:
                best = image
    assert best is not None
    return best


def projectively_simple_plane_classification():
    """Exact C_7^2 search with one label per projective direction, m<=4.

    Every rank-two orbit has an ordered support basis.  Sending that pair to
    e1,e2 puts at least one preimage in this search, so canonicalizing all
    maximum leaves gives the complete GL(2,7)-orbit list.
    """
    global_best = 4  # rank-one sections have at most four positions
    global_orbits = set()
    nodes = atomic_pruned = bound_pruned = 0
    base_rows = []

    for first_multiplicity in range(1, 5):
        first_state = p2_extend(frozenset((P2_ZERO_ID,)), P2_E1, first_multiplicity)
        assert first_state is not None
        for second_multiplicity in range(1, 5):
            second_state = p2_extend(first_state, P2_E2, second_multiplicity)
            if second_state is None:
                continue
            local_best = first_multiplicity + second_multiplicity
            local_orbits = set()
            local_witnesses = []

            def record(blocks, length):
                nonlocal local_best, local_orbits, local_witnesses
                if length < local_best:
                    return
                key = p2_canonical_key(blocks)
                raw = tuple(sorted((P2_ID[value], multiplicity) for value, multiplicity in blocks))
                if length > local_best:
                    local_best = length
                    local_orbits = {key}
                    local_witnesses = [raw]
                else:
                    local_orbits.add(key)
                    local_witnesses.append(raw)

            def visit(direction_index, reachable, blocks, length):
                nonlocal nodes, atomic_pruned, bound_pruned
                nodes += 1
                record(blocks, length)
                remaining = len(P2_REMAINING_DIRECTIONS) - direction_index
                if length + 4 * remaining < local_best:
                    bound_pruned += 1
                    return
                if direction_index == len(P2_REMAINING_DIRECTIONS):
                    return
                visit(direction_index + 1, reachable, blocks, length)
                direction = P2_REMAINING_DIRECTIONS[direction_index]
                for scalar in range(1, P):
                    value = p2_scale(scalar, direction)
                    for multiplicity in range(1, 5):
                        extended = p2_extend(reachable, value, multiplicity)
                        if extended is None:
                            atomic_pruned += 1
                            continue
                        visit(
                            direction_index + 1,
                            extended,
                            blocks + ((value, multiplicity),),
                            length + multiplicity,
                        )

            visit(
                0,
                second_state,
                ((P2_E1, first_multiplicity), (P2_E2, second_multiplicity)),
                first_multiplicity + second_multiplicity,
            )
            witness = min(local_witnesses)
            base_rows.append({
                "basis_multiplicities": (first_multiplicity, second_multiplicity),
                "maximum_weight": local_best,
                "witness": witness,
            })
            if local_best > global_best:
                global_best = local_best
                global_orbits = set(local_orbits)
            elif local_best == global_best:
                global_orbits.update(local_orbits)

    ordered_orbits = tuple(sorted(global_orbits))
    for orbit in ordered_orbits:
        reachable = frozenset((P2_ZERO_ID,))
        for value_id, multiplicity in orbit:
            reachable = p2_extend(reachable, P2_VECTORS[value_id], multiplicity)
            assert reachable is not None
    signature_counts = Counter(
        tuple(sorted((multiplicity for _value_id, multiplicity in orbit), reverse=True))
        for orbit in ordered_orbits
    )
    payload = json.dumps(ordered_orbits, separators=(",", ":"), default=list).encode("ascii")
    base_payload = json.dumps(base_rows, separators=(",", ":"), default=list).encode("ascii")
    return {
        "maximum_weight": global_best,
        "basis_cases": tuple(base_rows),
        "basis_witness_sha256": hashlib.sha256(base_payload).hexdigest(),
        "gl2_orbits": len(ordered_orbits),
        "signature_counts": tuple(
            {"signature": signature, "orbits": signature_counts[signature]}
            for signature in sorted(signature_counts, reverse=True)
        ),
        "orbit_sha256": hashlib.sha256(payload).hexdigest(),
        "nodes": nodes,
        "atomic_pruned": atomic_pruned,
        "bound_pruned": bound_pruned,
    }


def bounded_compositions(length, total_sum, maximum):
    if length == 0:
        if total_sum == 0:
            yield ()
        return
    lower_rest = length - 1
    upper_rest = maximum * (length - 1)
    for first in range(1, maximum + 1):
        remainder = total_sum - first
        if lower_rest <= remainder <= upper_rest:
            for suffix in bounded_compositions(length - 1, remainder, maximum):
                yield (first,) + suffix


def pointed_profiles(distinguished_multiplicity, support_size):
    """Profiles after selecting a largest non-distinguished fibre as e2."""
    profiles = []
    for first in range(1, 5):
        for suffix in bounded_compositions(
            support_size - 2,
            19 - distinguished_multiplicity - first,
            first,
        ):
            profiles.append((first,) + suffix)
    return tuple(profiles)


def signature_rows(distinguished_multiplicity, support_size):
    profiles = pointed_profiles(distinguished_multiplicity, support_size)
    counts = Counter(
        tuple(sorted((distinguished_multiplicity,) + profile, reverse=True))
        for profile in profiles
    )
    return profiles, tuple(
        {"signature": signature, "profiles": counts[signature]}
        for signature in sorted(counts, reverse=True)
    )


def profile_tables():
    tables = []
    stream = []
    for distinguished_multiplicity in (3, 4):
        maximum_support = 20 - distinguished_multiplicity
        for support_size in range(9, maximum_support + 1):
            profiles, signatures = signature_rows(
                distinguished_multiplicity, support_size
            )
            stream.append(
                (distinguished_multiplicity, support_size, profiles)
            )
            tables.append({
                "distinguished_multiplicity": distinguished_multiplicity,
                "support": support_size,
                "profile_count": len(profiles),
                "signature_count": len(signatures),
                "non_q_singleton_lower_bound": (
                    2 * support_size + distinguished_multiplicity - 21
                ),
                "signatures": signatures,
            })
    payload = json.dumps(stream, separators=(",", ":"), default=list).encode("ascii")
    return tuple(tables), hashlib.sha256(payload).hexdigest()


def support9_probe_blocks(distinguished_multiplicity, profile):
    """Conic-plus-point zero-sum skeleton for any pointed support-9 profile.

    It is deliberately not claimed to be an atom.  The construction shows
    that total sum, projective simplicity, all-eight quotient directions, and
    the Davenport plane-load gate alone cannot remove a support-9 signature.
    """
    assert len(profile) == 8 and sum(profile) == 19 - distinguished_multiplicity
    conic = tuple((1, t, t * t % P) for t in range(1, P))
    infinity = (0, 0, 1)
    extra = (0, 1, 0)
    representatives = (extra, infinity) + conic

    m = distinguished_multiplicity
    weights = (m - 1, m - 1, (9 - m) % P) + (1,) * 5
    assert len(weights) == len(representatives) == 8
    labels = tuple(
        scale(weight * pow(multiplicity, -1, P) % P, representative)
        for weight, multiplicity, representative in zip(
            weights, profile, representatives
        )
    )
    blocks = ((Q, m),) + tuple(zip(labels, profile))
    return blocks


def expanded(blocks):
    return tuple(
        value
        for value, multiplicity in blocks
        for _ in range(multiplicity)
    )


def forbidden_low(layers, tail_size):
    """Low-side form Sigma_{r+3..r+10} for a tail r-subset."""
    return frozenset().union(*(
        layers[size]
        for size in range(tail_size + 3, tail_size + 11)
        if size < len(layers)
    ))


def escape_from_layers(layers):
    return tuple(
        value_id
        for value_id in NONZERO_IDS
        if value_id not in forbidden_low(layers, 1)
    )


def threefold_sum_witness(values):
    witnesses = {ZERO_ID: ()}
    for _ in range(3):
        next_witnesses = {}
        for subtotal, prefix in witnesses.items():
            for value_id in values:
                new_sum = VECTOR_ID[add(VECTORS[subtotal], VECTORS[value_id])]
                next_witnesses.setdefault(new_sum, prefix + (value_id,))
        witnesses = next_witnesses
    for subtotal, first in witnesses.items():
        opposite = VECTOR_ID[neg(VECTORS[subtotal])]
        if opposite in witnesses:
            return first + witnesses[opposite]
    return None


def validate_tail(tail_ids, forbidden, maximum_tail_subset=3):
    if len(tail_ids) != 6 or total(VECTORS[index] for index in tail_ids) != ZERO:
        return False
    for size in range(1, maximum_tail_subset + 1):
        for positions in combinations(range(6), size):
            subtotal = total(VECTORS[tail_ids[position]] for position in positions)
            if VECTOR_ID[subtotal] in forbidden[size]:
                return False
    return True


def conditioned_tail_gate(
    labels,
    maximum_tail_subset=3,
    exact_domain_limit=32,
):
    """Safe tail gate for a partial actual-position prefix.

    Level one is always exact via 0 in 3E+3E.  Levels two and three use exact
    multiset enumeration when the singleton domain is small.  A large domain
    returns KEEP_UNRESOLVED and never causes a rejection.
    """
    assert 1 <= maximum_tail_subset <= 3
    layers = position_layers(labels, 13)
    forbidden = {
        size: forbidden_low(layers, size)
        for size in range(1, maximum_tail_subset + 1)
    }
    domain = tuple(value_id for value_id in NONZERO_IDS if value_id not in forbidden[1])
    level_one_witness = threefold_sum_witness(domain)
    if level_one_witness is None:
        return {
            "status": "PRUNE_EXACT",
            "domain_size": len(domain),
            "level": 1,
            "witness": None,
        }
    if maximum_tail_subset == 1:
        return {
            "status": "KEEP_WITNESS",
            "domain_size": len(domain),
            "level": 1,
            "witness": level_one_witness,
        }
    if len(domain) > exact_domain_limit:
        return {
            "status": "KEEP_UNRESOLVED",
            "domain_size": len(domain),
            "level": maximum_tail_subset,
            "witness": None,
        }

    domain_set = frozenset(domain)
    for first_five in combinations_with_replacement(domain, 5):
        subtotal = total(VECTORS[index] for index in first_five)
        forced = VECTOR_ID[neg(subtotal)]
        if forced not in domain_set or forced < first_five[-1]:
            continue
        tail = first_five + (forced,)
        if validate_tail(tail, forbidden, maximum_tail_subset):
            return {
                "status": "KEEP_WITNESS",
                "domain_size": len(domain),
                "level": maximum_tail_subset,
                "witness": tail,
            }
    return {
        "status": "PRUNE_EXACT",
        "domain_size": len(domain),
        "level": maximum_tail_subset,
        "witness": None,
    }


def direct_high_forbidden(layers, tail_size):
    high = frozenset().union(*(
        layers[size]
        for size in range(9 - tail_size, 17 - tail_size)
    ))
    return frozenset(VECTOR_ID[neg(VECTORS[value_id])] for value_id in high)


def deleted_escape_audit(labels, target):
    """Actual-position R/C alternating identities for one complete atom."""
    target_id = VECTOR_ID[target]
    negative_id = VECTOR_ID[neg(target)]
    families = {"R": [], "C": []}
    for size in range(1, 8):
        for positions in combinations(range(19), size):
            subtotal = total(labels[position] for position in positions)
            subtotal_id = VECTOR_ID[subtotal]
            if size <= 3 and subtotal_id == target_id:
                families["R"].append(positions)
            if subtotal_id == negative_id:
                families["C"].append(positions)

    def signed(family):
        return sum(-1 if len(positions) % 2 else 1 for positions in family) % P

    rho = signed(families["R"])
    kappa = signed(families["C"])
    assert rho == kappa
    for position in range(19):
        rho_i = signed([entry for entry in families["R"] if position in entry])
        kappa_i = signed([entry for entry in families["C"] if position in entry])
        assert (rho - rho_i - kappa_i) % P == 1
        assert (kappa - kappa_i - rho_i) % P == 1
    for left in families["R"]:
        left_set = frozenset(left)
        assert all(left_set.intersection(right) for right in families["C"])
    return {
        "target": target,
        "R": len(families["R"]),
        "C": len(families["C"]),
        "rho": rho,
    }


def gap_ladder(labels, target, fibre):
    multiplicity = labels.count(fibre)
    outside = tuple(value for value in labels if value != fibre)
    layers = position_layers(outside, 11)
    rows = []
    for copies in range(multiplicity + 1):
        shifted = add(target, neg(scale(copies, fibre)))
        lower = max(0, 4 - copies)
        upper = min(len(outside), 11 - copies)
        rows.append(all(
            VECTOR_ID[shifted] not in layers[size]
            for size in range(lower, upper + 1)
        ))
    return all(rows)


SUPPORT9_EMPTY = expanded((
    (Q, 3), ((0, 0, 1), 1), ((0, 1, 0), 1),
    ((0, 1, 6), 3), ((1, 0, 1), 4), ((1, 5, 1), 1),
    ((1, 6, 1), 4), ((4, 5, 3), 1), ((5, 4, 4), 1),
))

SUPPORT7_SINGLETON = expanded((
    ((0, 0, 1), 4), ((0, 1, 0), 4), ((0, 1, 6), 2), (Q, 3),
    ((1, 0, 6), 1), ((1, 2, 1), 4), ((6, 0, 2), 1),
))


def run_regressions():
    arc_report = fixed_frame_arc_certificate()
    assert arc_report["maximum"] == 8
    assert arc_report["visited_by_size"] == {4: 1, 5: 20, 6: 70, 7: 20, 8: 5}
    assert arc_report["maximum_arcs_sha256"] == EXPECTED_ARC_SHA256
    plane_section_report = projectively_simple_plane_classification()
    assert plane_section_report["maximum_weight"] == 11
    assert len(plane_section_report["basis_cases"]) == 16
    assert all(row["maximum_weight"] == 11 for row in plane_section_report["basis_cases"])
    assert plane_section_report["gl2_orbits"] == 77
    assert plane_section_report["orbit_sha256"] == EXPECTED_PLANE_ORBIT_SHA256
    assert plane_section_report["basis_witness_sha256"] == EXPECTED_PLANE_BASIS_WITNESS_SHA256
    profile_data, profile_sha256 = profile_tables()
    assert profile_sha256 == EXPECTED_PROFILE_STREAM_SHA256
    support9_rows = {
        row["distinguished_multiplicity"]: row
        for row in profile_data if row["support"] == 9
    }
    assert support9_rows[3]["profile_count"] == 771
    assert support9_rows[3]["signature_count"] == 10
    assert support9_rows[4]["profile_count"] == 476
    assert support9_rows[4]["signature_count"] == 8

    probe_reports = []
    for row in (support9_rows[3], support9_rows[4]):
        m = row["distinguished_multiplicity"]
        profiles = pointed_profiles(m, 9)
        representative_by_signature = {}
        for profile in profiles:
            signature = tuple(sorted((m,) + profile, reverse=True))
            representative_by_signature.setdefault(signature, profile)
        for signature, profile in sorted(representative_by_signature.items(), reverse=True):
            blocks = support9_probe_blocks(m, profile)
            labels = expanded(blocks)
            loads = plane_loads(blocks)
            support_counts = plane_support_counts(blocks)
            bins = q_plane_bins(blocks)
            assert len(labels) == 19 and total(labels) == ZERO
            assert is_projectively_simple(labels)
            assert len(bins) == 8 and all(len(entries) == 1 for entries in bins.values())
            assert max(loads.values()) <= 11
            assert max(support_counts.values()) <= 3
            layers = position_layers(labels, 13)
            escape = escape_from_layers(layers)
            tail1 = conditioned_tail_gate(labels, 1)
            probe_reports.append({
                "distinguished_multiplicity": m,
                "signature": signature,
                "profile": profile,
                "atom": is_atom(labels),
                "max_plane_load": max(loads.values()),
                "escape_size": len(escape),
                "tail1_status": tail1["status"],
            })
    assert len(probe_reports) == 18
    assert all(not row["atom"] for row in probe_reports)
    assert all(row["max_plane_load"] <= 11 for row in probe_reports)
    assert all(row["escape_size"] == 0 for row in probe_reports)
    assert all(row["tail1_status"] == "PRUNE_EXACT" for row in probe_reports)
    probe_payload = json.dumps(
        probe_reports, sort_keys=True, separators=(",", ":"), default=list
    ).encode("ascii")
    assert hashlib.sha256(probe_payload).hexdigest() == EXPECTED_SUPPORT9_PROBE_SHA256

    known_reports = []
    for name, labels, expected_escape_size in (
        ("support9_empty", SUPPORT9_EMPTY, 0),
        ("support7_singleton", SUPPORT7_SINGLETON, 1),
    ):
        assert len(labels) == 19 and total(labels) == ZERO and is_atom(labels)
        assert is_projectively_simple(labels)
        blocks = tuple(Counter(labels).items())
        assert max(plane_loads(blocks).values()) <= 11
        layers = position_layers(labels, 15)
        escape = escape_from_layers(layers)
        assert len(escape) == expected_escape_size
        for tail_size in (1, 2, 3):
            assert forbidden_low(layers, tail_size) == direct_high_forbidden(
                layers, tail_size
            )
        for prefix_size in range(20):
            prefix_layers = position_layers(labels[:prefix_size], 13)
            for tail_size in (1, 2, 3):
                assert forbidden_low(prefix_layers, tail_size).issubset(
                    forbidden_low(layers, tail_size)
                )
        gate = conditioned_tail_gate(labels, 3)
        if expected_escape_size <= 1:
            assert gate["status"] == "PRUNE_EXACT"
        known_reports.append({
            "name": name,
            "support": len(set(labels)),
            "max_plane_load": max(plane_loads(blocks).values()),
            "escape_size": len(escape),
            "tail3_status": gate["status"],
        })

    empty_prefix_gate = conditioned_tail_gate((), 1)
    assert empty_prefix_gate["status"] == "KEEP_WITNESS"
    singleton_target = VECTORS[escape_from_layers(position_layers(SUPPORT7_SINGLETON, 13))[0]]
    deleted_report = deleted_escape_audit(SUPPORT7_SINGLETON, singleton_target)

    ladder_checks = 0
    for labels in (SUPPORT9_EMPTY, SUPPORT7_SINGLETON):
        full_escape = frozenset(escape_from_layers(position_layers(labels, 13)))
        for fibre, multiplicity in Counter(labels).items():
            if multiplicity not in (3, 4):
                continue
            for target_id in NONZERO_IDS:
                assert gap_ladder(labels, VECTORS[target_id], fibre) == (
                    target_id in full_escape
                )
                ladder_checks += 1

    return {
        "fixed_frame_arc_certificate": arc_report,
        "projectively_simple_plane_classification": plane_section_report,
        "profile_table": profile_data,
        "profile_stream_sha256": profile_sha256,
        "support9_signature_probe": tuple(probe_reports),
        "support9_signature_probe_sha256": hashlib.sha256(probe_payload).hexdigest(),
        "known_atom_regressions": tuple(known_reports),
        "empty_prefix_level1_witness": empty_prefix_gate["witness"],
        "deleted_escape_audit": deleted_report,
        "gap_ladder_target_checks": ladder_checks,
        "scope": (
            "exact structural and monotone necessary pruning; "
            "no support-nine atom enumeration and no full-68 UNSAT claim"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full-json",
        action="store_true",
        help="print the complete deterministic report payload",
    )
    args = parser.parse_args()
    report = run_regressions()
    payload = json.dumps(report, sort_keys=True, separators=(",", ":"), default=list)
    digest = hashlib.sha256(payload.encode("ascii")).hexdigest()
    assert digest == EXPECTED_REPORT_SHA256
    print("PASS pointed support>=9 profile denominators and signatures")
    print("PASS fixed-frame PG(2,7) arc maximum:", report["fixed_frame_arc_certificate"]["maximum"])
    print("PASS projectively simple C7^2 section maximum:", report["projectively_simple_plane_classification"]["maximum_weight"])
    print("PASS support9 conic-plus-point compatibility probes:", len(report["support9_signature_probe"]))
    print("PASS projective plane load <=11 on all frozen complete atoms")
    print("PASS low/high tail-spectrum complement and prefix monotonicity")
    print("PASS exact six-tail 3E intersection gate and small-domain r<=3 gate")
    print("PASS deleted-position alternating audit:", json.dumps(report["deleted_escape_audit"], separators=(",", ":")))
    print("PASS exact three/four-fibre gap ladder checks:", report["gap_ladder_target_checks"])
    print("PROFILE STREAM SHA256:", report["profile_stream_sha256"])
    print("REPORT SHA256:", digest)
    if args.full_json:
        print("REPORT JSON:", payload)
    print("STATUS: PROVED necessary pruning / support>=9 and full 68-scalar branch INCOMPLETE")


if __name__ == "__main__":
    main()
