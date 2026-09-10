#!/usr/bin/env python3
"""Exact missing short-support search for p=7,m=4,0001,s=6.

This program fills precisely the part of the support-at-most-seven quotient
classification which is not already covered by the frozen multiplicity-three
classification: length-19 quotient atoms with a distinguished four-fold
value q, maximum multiplicity four, and no fibre of multiplicity three.

The only possible multiplicity signatures are

    support 6: (4,4,4,4,2,1),
    support 7: (4,4,4,4,1,1,1), (4,4,4,2,2,2,1).

Canonical augmentation is exhaustive but may generate an orbit more than
once.  It searches only the necessary frontier E1(B) != empty; candidates
with empty E1 are safely discarded by monotonicity of position-subset sums.
Every surviving completion is checked by the exact bounded-kernel atom test
and then against all proper T-subset middle-gap rows and the 0001 quotient
trace windows.  No height assignment or complete 68-scalar candidate is
claimed by this quotient-only layer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import permutations
from pathlib import Path
from typing import Iterable, Sequence

import p7_length19_support7_escape_search as BASE
import p7_m4_68_layered_solver as LAYERED


P = BASE.P
ORDER = BASE.ORDER
ZERO_ID = BASE.ZERO_ID
Q_ID = BASE.Q_ID
E2_ID = BASE.E2_ID
E3_ID = BASE.E3_ID
BASE_IDS = BASE.BASE_IDS
NONZERO_MASK = BASE.NONZERO_MASK
VECTORS = BASE.VECTORS
SCALE_ID = BASE.SCALE_ID
NEG_ID = BASE.NEG_ID

SIGNATURES = (
    (4, 4, 4, 4, 2, 1),
    (4, 4, 4, 4, 1, 1, 1),
    (4, 4, 4, 2, 2, 2, 1),
)

EXPECTED_FULL_COUNTERS = {
    "ordered_prefix_nodes": 13_031_018,
    "atomic_prefix_pruned": 12_330_921,
    "escape_prefix_pruned": 0,
    "forced_last_rejected": 450_027,
    "final_zero_sum_candidates": 84_524,
    "final_escape_pruned": 82_127,
    "final_nonatoms": 2_397,
    "target_atom_hits": 0,
    "target_with_T_survivor": 0,
}
EXPECTED_PROFILES_SHA256 = "accfb24af50eb1ea99d5329f5fe4a3e0915cb90bdcb7f352d466e7ca305d6d2a"
EXPECTED_REPORT_SHA256 = "08fa72437eb097ce9b8960dfc0ed03ddec546eb4ed2d416cee58e06909cac1f2"


def payload_digest(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode(
        "ascii"
    )
    return hashlib.sha256(payload).hexdigest()


def profile_list(signature: Sequence[int]):
    """All ordered multiplicity profiles after removing the pointed q^4.

    The first remaining entry is the chosen maximal fibre e2.  The second is
    the chosen maximal off-plane fibre e3; its maximality is enforced during
    label augmentation by ``allowed_value``.
    """
    remainder = list(signature)
    remainder.remove(4)
    return tuple(
        sorted(
            profile
            for profile in set(permutations(remainder))
            if profile[0] == max(profile)
        )
    )


def projective_key(value_id: int):
    value = VECTORS[value_id]
    pivot = next(index for index, entry in enumerate(value) if entry)
    inverse = pow(value[pivot], -1, P)
    return tuple(inverse * entry % P for entry in value)


PROJECTIVE_KEY = tuple(
    None if value_id == ZERO_ID else projective_key(value_id)
    for value_id in range(ORDER)
)


def forbidden_basis_mask(m2: int, m3: int) -> int:
    answer = 0
    for c1 in range(5):
        for c2 in range(m2 + 1):
            for c3 in range(m3 + 1):
                if c1 == c2 == c3 == 0:
                    continue
                basis_sum = BASE.vector_id((c1 % P, c2 % P, c3 % P))
                answer |= 1 << NEG_ID[basis_sum]
    return answer


def allowed_value(
    value_id: int,
    multiplicity: int,
    m3: int,
    prior_support: Sequence[int],
) -> bool:
    if value_id in BASE_IDS:
        return False
    if VECTORS[value_id][2] != 0 and multiplicity > m3:
        return False
    key = PROJECTIVE_KEY[value_id]
    return all(key != PROJECTIVE_KEY[old] for old in prior_support)


def empty_counters():
    return {
        "ordered_prefix_nodes": 0,
        "atomic_prefix_pruned": 0,
        "escape_prefix_pruned": 0,
        "forced_last_rejected": 0,
        "final_zero_sum_candidates": 0,
        "final_escape_pruned": 0,
        "final_nonatoms": 0,
        "target_atom_hits": 0,
        "target_with_T_survivor": 0,
    }


def add_counters(target: dict[str, int], source: dict[str, int]):
    for key in target:
        target[key] += source[key]


def labels_from_ids(ids: Sequence[int]):
    return tuple(VECTORS[value_id] for value_id in ids)


def search_profile(
    signature: Sequence[int], profile_index: int, profile: Sequence[int]
):
    """Exhaust one normalized profile and return all E1-nonempty atom hits."""
    counters = empty_counters()
    hits = []
    m2, m3, *extra_multiplicities = profile
    assert extra_multiplicities
    chosen_multiplicities = extra_multiplicities[:-1]
    last_multiplicity = extra_multiplicities[-1]
    multiplicities = (4,) + tuple(profile)
    forbidden = forbidden_basis_mask(m2, m3)

    base_layers = BASE.EMPTY_LAYERS
    for value_id, multiplicity in (
        (Q_ID, 4),
        (E2_ID, m2),
        (E3_ID, m3),
    ):
        base_layers = BASE.add_repeated_positions(
            base_layers, value_id, multiplicity
        )
    assert BASE.covered_nonzero(base_layers) != NONZERO_MASK
    fixed_sum = BASE.vector_id((4 % P, m2 % P, m3 % P))
    inverse_last = pow(last_multiplicity, -1, P)

    def finish(chosen, reachable, layers, subtotal):
        last = SCALE_ID[NEG_ID[subtotal]][inverse_last]
        prior = (Q_ID, E2_ID, E3_ID) + chosen
        if chosen and last <= chosen[-1]:
            counters["forced_last_rejected"] += 1
            return
        if not allowed_value(last, last_multiplicity, m3, prior):
            counters["forced_last_rejected"] += 1
            return
        counters["final_zero_sum_candidates"] += 1
        full_layers = BASE.add_repeated_positions(
            layers, last, last_multiplicity
        )
        remaining = BASE.escape_mask(full_layers)
        if not remaining:
            counters["final_escape_pruned"] += 1
            return
        support = (Q_ID, E2_ID, E3_ID) + chosen + (last,)
        if not BASE.bounded_atom(support, multiplicities):
            counters["final_nonatoms"] += 1
            return
        expanded_ids = BASE.expanded(support, multiplicities)
        assert len(expanded_ids) == 19
        assert len(set(expanded_ids)) == len(signature)
        assert tuple(sorted(Counter(expanded_ids).values(), reverse=True)) == tuple(
            signature
        )
        direct = BASE.direct_position_layers(expanded_ids, 15)
        low = set().union(*(direct[size] for size in range(4, 12)))
        escape_ids = tuple(
            value_id for value_id in range(1, ORDER) if value_id not in low
        )
        assert set(escape_ids) == set(BASE.mask_ids(remaining))
        middle = set().union(*(direct[size] for size in range(8, 16)))
        exact_e1 = tuple(
            value_id
            for value_id in range(1, ORDER)
            if NEG_ID[value_id] not in middle
        )
        assert exact_e1 == escape_ids

        atom_vectors = labels_from_ids(expanded_ids)
        forbidden_t, _ = LAYERED.forbidden_T_sum_tables(atom_vectors)
        q_vector = VECTORS[Q_ID]
        unary, levels, closure, tails = LAYERED.enumerate_T_multisets(
            atom_vectors, q_vector, forbidden_t
        )
        assert tuple(BASE.vector_id(value) for value in unary) == escape_ids or set(
            BASE.vector_id(value) for value in unary
        ).issubset(set(escape_ids))
        hit = {
            "atom_ids": expanded_ids,
            "escape_ids": escape_ids,
            "unary_after_0001_ids": tuple(
                BASE.vector_id(value) for value in unary
            ),
            "prefix_levels": levels,
            "closure": closure,
            "T_survivors_ids": tuple(
                tuple(BASE.vector_id(value) for value in tail) for tail in tails
            ),
        }
        hits.append(hit)
        counters["target_atom_hits"] += 1
        counters["target_with_T_survivor"] += bool(tails)

    def walk(chosen, reachable, layers, subtotal, depth):
        if depth == len(chosen_multiplicities):
            finish(chosen, reachable, layers, subtotal)
            return
        multiplicity = chosen_multiplicities[depth]
        start = chosen[-1] + 1 if chosen else 0
        prior = (Q_ID, E2_ID, E3_ID) + chosen
        for value_id in range(start, ORDER):
            if not allowed_value(value_id, multiplicity, m3, prior):
                continue
            counters["ordered_prefix_nodes"] += 1
            next_reachable = BASE.extend_atomic_prefix(
                reachable, value_id, multiplicity, forbidden
            )
            if next_reachable is None:
                counters["atomic_prefix_pruned"] += 1
                continue
            next_layers = BASE.add_repeated_positions(
                layers, value_id, multiplicity
            )
            if BASE.covered_nonzero(next_layers) == NONZERO_MASK:
                counters["escape_prefix_pruned"] += 1
                continue
            next_sum = BASE.add_id(
                subtotal, SCALE_ID[value_id][multiplicity]
            )
            walk(
                chosen + (value_id,),
                next_reachable,
                next_layers,
                next_sum,
                depth + 1,
            )

    walk((), 1, base_layers, fixed_sum, 0)
    return {
        "signature": tuple(signature),
        "profile_index": profile_index,
        "profile": tuple(profile),
        **counters,
        "hit_sha256": payload_digest(hits),
    }, tuple(hits)


def jsonable(value):
    if isinstance(value, tuple):
        return [jsonable(item) for item in value]
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    return value


def write_report(path: Path, report):
    payload = json.dumps(
        jsonable(report), ensure_ascii=False, indent=2, sort_keys=True
    )
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload + "\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def self_test():
    assert tuple(len(profile_list(signature)) for signature in SIGNATURES) == (
        12,
        10,
        20,
    )
    for value_id in range(1, ORDER):
        key = PROJECTIVE_KEY[value_id]
        assert key is not None
        for coefficient in range(1, P):
            assert PROJECTIVE_KEY[SCALE_ID[value_id][coefficient]] == key


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument("--signature", type=int, choices=range(1, 4))
    parser.add_argument("--start-profile", type=int, default=1)
    parser.add_argument("--stop-profile", type=int)
    args = parser.parse_args()
    self_test()

    signature_indices = (
        (args.signature - 1,) if args.signature is not None else range(3)
    )
    all_reports = []
    all_hits = []
    aggregate = empty_counters()
    completed = []
    for signature_index in signature_indices:
        signature = SIGNATURES[signature_index]
        profiles = profile_list(signature)
        stop = len(profiles) if args.stop_profile is None else min(
            args.stop_profile, len(profiles)
        )
        if not 1 <= args.start_profile <= stop + 1:
            raise ValueError("invalid profile interval")
        interval = (args.start_profile, stop)
        completed.append((signature, len(profiles), interval))
        for profile_index in range(args.start_profile, stop + 1):
            report, hits = search_profile(
                signature, profile_index, profiles[profile_index - 1]
            )
            all_reports.append(report)
            all_hits.extend(hits)
            add_counters(aggregate, report)
            print(
                "FULL68 SHORT-SUPPORT PROFILE",
                json.dumps(jsonable(report), separators=(",", ":")),
                flush=True,
            )

    atom_orbits = defaultdict(list)
    for hit in all_hits:
        atom_orbits[BASE.canonical_q_key(hit["atom_ids"])].append(hit)
    orbit_keys = tuple(sorted(atom_orbits))
    result = {
        "schema": "p7-m4-full68-short-support-v1",
        "scope": (
            "all normalized no-multiplicity-three length-19 atoms with a "
            "pointed q^4, max fibre four, and support six or seven; quotient "
            "necessary layer only"
        ),
        "completed": completed,
        "profile_count": len(all_reports),
        **aggregate,
        "hit_sha256": payload_digest(all_hits),
        "orbit_count": len(orbit_keys),
        "orbit_sha256": BASE.payload_digest(orbit_keys),
        "profiles_sha256": payload_digest(all_reports),
        "hits": all_hits,
    }
    print("FULL68 SHORT-SUPPORT TOTAL", json.dumps(jsonable(result), separators=(",", ":")), flush=True)
    full_run = args.signature is None and args.start_profile == 1 and args.stop_profile is None
    if full_run:
        assert result["profile_count"] == 42
        assert aggregate == EXPECTED_FULL_COUNTERS
        assert result["profiles_sha256"] == EXPECTED_PROFILES_SHA256
        assert result["hit_sha256"] == payload_digest([])
        assert result["orbit_sha256"] == BASE.payload_digest(())
        assert result["target_with_T_survivor"] == 0
        print("CERTIFIED: all 42 missing no-three normalized profiles exhausted")
        print("CERTIFIED: no E1-nonempty atom hit has a strict quotient T extension")
        print("SCOPE: support at most seven after adjoining the frozen q^3 classification")
        print("STATUS: PROVED short-support quotient exclusion; full 68-scalar slice incomplete")
    else:
        print("STATUS: deterministic profile shard only")
    if args.report is not None:
        digest = write_report(args.report, result)
        if full_run:
            assert digest == EXPECTED_REPORT_SHA256
        print("REPORT:", args.report)
        print("REPORT SHA256:", digest)


if __name__ == "__main__":
    main()
