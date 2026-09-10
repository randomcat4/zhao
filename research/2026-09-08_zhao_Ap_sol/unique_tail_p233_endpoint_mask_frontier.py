#!/usr/bin/env python3
"""Exact endpoint-mask frontier for one canonical p=233 outer shard.

The generator treats U=(u_e,u_f,u_t), the common witness y, and the two-place
packing block P as marked positions.  The remaining 468 positions are
quotiented only by their complete membership pattern across the labelled
endpoints.  Pattern multiplicities are therefore exact orbits under
permutations of the unmarked positions, not a relaxed incidence model.

Only the canonical decorated shard selected below is fully enumerated.  No
quotient or actual labels are assigned, so label-dependent edge sums, atom
conditions, mixed targets, short closure, Hasse rows, and Z atomicity remain
pending.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from math import comb, factorial
from pathlib import Path
from typing import Iterable


P = 233
Y_SIZE = 474
TAIL_BY_BIT = {1: "u_e", 2: "u_f", 4: "u_t"}
TAIL_POSITIONS = frozenset(TAIL_BY_BIT.values())
CANONICAL_DECORATED_SHARD = "decorated-1356"

HERE = Path(__file__).resolve().parent
SOURCE_REPORT = HERE / "unique_tail_p233_length_decorated_trace_reduction_report.json"
DUPLICATE_REPORT = HERE / "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_report.json"
EXACT_SLICE_REPORT = HERE / "unique_tail_p233_type3_p2_exact_slice_report.json"
REPORT_PATH = HERE / "unique_tail_p233_endpoint_mask_frontier_report.json"

DEPENDENCY_SHA256 = {
    "unique_tail_p233_length_decorated_trace_reduction_report.json": (
        "3c2f2c0405842b75c47fbf7fcedf09f0ef5275e9fe2a0339e1e9e71d47e4df47"
    ),
    "proofs/unique_tail_p233_type3_p2_exact_slice.md": (
        "30ce9d66a91d0e47c22b5731b66b450e9cc9155c872e60d482154dc6e8c6f274"
    ),
    "unique_tail_p233_type3_p2_exact_slice.py": (
        "22631e977e14b12e4e8d1cbd18e7cde0c7c81d7b3989364f0d66e616ce3371f1"
    ),
    "unique_tail_p233_type3_p2_exact_slice_report.json": (
        "440b9fecb57e66b018bab44b37f87e97e68cb03155f71e7ddb8d9c76f975281a"
    ),
    "proofs/unique_tail_p233_duplicate_remainder_unique_tail_obstruction.md": (
        "10c0277cbbabff192123183292cd7f1dc2c3a6825759d116361f8c851db1714c"
    ),
    "unique_tail_p233_duplicate_remainder_unique_tail_obstruction.py": (
        "b113cb6fc380b46bbefc64fed264b3176c4a4a7f45fe6acd0e4053f2ae86cce6"
    ),
    "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_report.json": (
        "ae5089e75a8f8ed7eb4de43f9fd7cac3e031286d1be9dc16618a99bbe7844a37"
    ),
}

EXPECTED_CERTIFICATES = {
    "unique_tail_p233_length_decorated_trace_reduction_report.json": (
        "37a86e2606fe21329a1cfb663d70528420648b042817600ecf0e62e18a548c02"
    ),
    "unique_tail_p233_type3_p2_exact_slice_report.json": (
        "05f913f2b8d1508cf09aacb42f56c4805550731c3fed3a0ef0b43f4d3e11a2db"
    ),
    "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_report.json": (
        "fa9707c2dd84d484bb7dd23d91f05262d1b687660e92bb70f2aa6b8a5b86c4b9"
    ),
}


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
            "ascii"
        )
    ).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_dependencies() -> dict[str, str]:
    actual = {relative: file_sha256(HERE / relative) for relative in DEPENDENCY_SHA256}
    assert actual == DEPENDENCY_SHA256
    return actual


def load_certified_report(path: Path) -> tuple[dict[str, object], str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    certificate = value.pop("certificate_sha256")
    assert isinstance(certificate, str)
    assert canonical_hash(value) == certificate
    assert certificate == EXPECTED_CERTIFICATES[path.name]
    value["certificate_sha256"] = certificate
    return value, certificate


def tail_set(mask: int) -> frozenset[str]:
    assert 1 <= mask <= 6
    return frozenset(name for bit, name in TAIL_BY_BIT.items() if mask & bit)


def candidate_duplicate_pairs(row: dict[str, object]) -> list[dict[str, object]]:
    traces = [int(value) for value in row["endpoint_trace_masks"]]
    lengths = [int(value) for value in row["endpoint_lengths"]]
    result: list[dict[str, object]] = []
    for first, second in itertools.combinations(range(len(traces)), 2):
        if lengths[first] != lengths[second]:
            continue
        first_tail = tail_set(traces[first])
        second_tail = tail_set(traces[second])
        if first_tail < second_tail and len(second_tail - first_tail) == 1:
            small, large = first, second
        elif second_tail < first_tail and len(first_tail - second_tail) == 1:
            small, large = second, first
        else:
            continue
        result.append(
            {
                "small": small,
                "large": large,
                "swapped_tail": next(
                    iter(tail_set(traces[large]) - tail_set(traces[small]))
                ),
            }
        )
    return result


def pattern_side_count(
    counts: tuple[int, ...], patterns: tuple[int, ...], left: int, right: int
) -> int:
    return sum(
        count
        for count, pattern in zip(counts, patterns)
        if pattern >> left & 1 and not (pattern >> right & 1)
    )


def containment_hits(
    counts: tuple[int, ...], patterns: tuple[int, ...], traces: tuple[int, ...]
) -> list[dict[str, int]]:
    hits: list[dict[str, int]] = []
    for left, right in itertools.permutations(range(len(traces)), 2):
        tail_left_only = (traces[left] & ~traces[right] & 7).bit_count()
        anonymous_left_only = pattern_side_count(counts, patterns, left, right)
        if tail_left_only + anonymous_left_only == 0:
            hits.append({"subset_endpoint": left, "superset_endpoint": right})
    return hits


def duplicate_remainder_hits(
    counts: tuple[int, ...],
    patterns: tuple[int, ...],
    duplicate_pairs: list[dict[str, object]],
) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for pair in duplicate_pairs:
        small = int(pair["small"])
        large = int(pair["large"])
        small_only = pattern_side_count(counts, patterns, small, large)
        large_only = pattern_side_count(counts, patterns, large, small)
        # Trace nesting contributes exactly the one swapped tail on the large side.
        if small_only == 1 and large_only == 0:
            hits.append(
                {
                    **pair,
                    "small_anonymous_only": small_only,
                    "large_anonymous_only": large_only,
                }
            )
    return hits


def edge_intersections_are_exact_y(
    counts: tuple[int, ...], patterns: tuple[int, ...], edges: tuple[tuple[int, int], ...]
) -> bool:
    return all(
        not any(
            count and pattern >> left & 1 and pattern >> right & 1
            for count, pattern in zip(counts, patterns)
        )
        for left, right in edges
    )


def orbit_weight(counts: tuple[int, ...], marked_choice_factor: int) -> int:
    used = sum(counts)
    answer = marked_choice_factor * factorial(468) // factorial(468 - used)
    for count in counts:
        answer //= factorial(count)
    return answer


def representative_masks(
    counts: tuple[int, ...], patterns: tuple[int, ...], row: dict[str, object]
) -> dict[str, object]:
    traces = tuple(int(value) for value in row["endpoint_trace_masks"])
    lengths = tuple(int(value) for value in row["endpoint_lengths"])
    endpoint_count = len(traces)
    endpoint_masks = [set(tail_set(trace)) | {"y"} for trace in traces]
    anonymous_positions_by_pattern: dict[int, list[str]] = {}
    next_position = 1
    for pattern, count in sorted(zip(patterns, counts)):
        positions = [
            f"z_{index:03d}" for index in range(next_position, next_position + count)
        ]
        next_position += count
        anonymous_positions_by_pattern[pattern] = positions
        for vertex in range(endpoint_count):
            if pattern >> vertex & 1:
                endpoint_masks[vertex].update(positions)

    used_anonymous = next_position - 1
    all_anonymous = {f"z_{index:03d}" for index in range(1, 469)}
    used_set = {position for positions in anonymous_positions_by_pattern.values() for position in positions}
    k_set = all_anonymous - used_set
    p_set = {"p_1", "p_2"}
    y_universe = set(TAIL_POSITIONS) | {"y"} | p_set | all_anonymous
    l_set = set(TAIL_POSITIONS) | set().union(*endpoint_masks)
    r_set = y_universe - l_set
    assert r_set == k_set | p_set and k_set.isdisjoint(p_set)
    assert len(y_universe) == Y_SIZE
    assert all(len(endpoint) == length for endpoint, length in zip(endpoint_masks, lengths))
    assert all(endpoint & TAIL_POSITIONS == tail_set(trace) for endpoint, trace in zip(endpoint_masks, traces))

    q_sets = [k_set | (l_set - endpoint) for endpoint in endpoint_masks]
    assert all(q_set == y_universe - endpoint - p_set for q_set, endpoint in zip(q_sets, endpoint_masks))

    pair_rows: list[dict[str, object]] = []
    for left, right in itertools.combinations(range(endpoint_count), 2):
        intersection = endpoint_masks[left] & endpoint_masks[right]
        pair_rows.append(
            {
                "left": left,
                "right": right,
                "intersection": sorted(intersection),
                "left_only_size": len(endpoint_masks[left] - endpoint_masks[right]),
                "right_only_size": len(endpoint_masks[right] - endpoint_masks[left]),
            }
        )

    return {
        "common_marked_position": "y",
        "packing_P": ["p_1", "p_2"],
        "endpoint_masks": [sorted(endpoint) for endpoint in endpoint_masks],
        "endpoint_pair_data": pair_rows,
        "used_anonymous_position_count": used_anonymous,
        "L_size": len(l_set),
        "R_size": len(r_set),
        "K_size": len(k_set),
        "K_description": (
            f"z_{used_anonymous + 1:03d}..z_468"
            if used_anonymous < 468
            else "empty"
        ),
        "Q_H_sizes": [len(q_set) for q_set in q_sets],
        "Q_H_sha256": [canonical_hash(sorted(q_set)) for q_set in q_sets],
    }


def literal_endpoint_core_masks(
    counts: tuple[int, ...], patterns: tuple[int, ...], traces: tuple[int, ...]
) -> list[set[str]]:
    """Build only the used endpoint positions for a literal oracle cross-check."""

    endpoints = [set(tail_set(trace)) | {"y"} for trace in traces]
    for pattern, count in zip(patterns, counts):
        for copy in range(count):
            position = f"pattern_{pattern:02d}_copy_{copy:02d}"
            for vertex in range(len(traces)):
                if pattern >> vertex & 1:
                    endpoints[vertex].add(position)
    return endpoints


def memoized_orbit_count(patterns: tuple[int, ...], residual: tuple[int, ...]) -> int:
    @lru_cache(maxsize=None)
    def count(index: int, remaining: tuple[int, ...]) -> int:
        if index == len(patterns):
            return int(not any(remaining))
        pattern = patterns[index]
        capacity = min(
            remaining[vertex]
            for vertex in range(len(remaining))
            if pattern >> vertex & 1
        )
        total = 0
        for multiplicity in range(capacity + 1):
            next_remaining = tuple(
                remaining[vertex] - multiplicity * ((pattern >> vertex) & 1)
                for vertex in range(len(remaining))
            )
            total += count(index + 1, next_remaining)
        return total

    return count(0, residual)


def enumerate_canonical_shard(row: dict[str, object]) -> dict[str, object]:
    traces = tuple(int(value) for value in row["endpoint_trace_masks"])
    lengths = tuple(int(value) for value in row["endpoint_lengths"])
    edges = tuple(tuple(int(vertex) for vertex in edge) for edge in row["edges"])
    endpoint_count = len(traces)
    assert endpoint_count == 4
    assert traces == (1, 2, 4, 6)
    assert lengths == (8, 7, 8, 8)
    assert edges == ((0, 1), (1, 2), (2, 0), (0, 3))
    assert all(not (traces[left] & traces[right]) for left, right in edges)

    residual = tuple(
        lengths[vertex] - 1 - len(tail_set(traces[vertex]))
        for vertex in range(endpoint_count)
    )
    assert residual == (6, 5, 6, 5)
    patterns = tuple(
        sorted(range(1, 1 << endpoint_count), key=lambda mask: (-mask.bit_count(), mask))
    )
    duplicate_pairs = candidate_duplicate_pairs(row)
    assert duplicate_pairs == [{"small": 2, "large": 3, "swapped_tail": "u_f"}]

    marked_choice_factor = (Y_SIZE - 3) * comb(Y_SIZE - 4, 2)
    assert marked_choice_factor == 471 * comb(470, 2) == 51_911_265
    closed_form_fixed_marks = 1
    for degree in residual:
        closed_form_fixed_marks *= comb(468, degree)
    closed_form_all_marks = marked_choice_factor * closed_form_fixed_marks

    counts = [0] * len(patterns)
    orbit_counts: Counter[str] = Counter()
    literal_counts: Counter[str] = Counter()
    used_position_histogram: Counter[int] = Counter()
    survivor_used_position_histogram: Counter[int] = Counter()
    stream_hash = hashlib.sha256()
    first_nested: tuple[int, ...] | None = None
    first_duplicate: tuple[int, ...] | None = None
    first_survivor: tuple[int, ...] | None = None

    def visit(index: int, remaining: tuple[int, ...]) -> None:
        nonlocal first_nested, first_duplicate, first_survivor
        if index == len(patterns):
            if any(remaining):
                return
            frozen_counts = tuple(counts)
            nested = containment_hits(frozen_counts, patterns, traces)
            duplicate = duplicate_remainder_hits(
                frozen_counts, patterns, duplicate_pairs
            )
            exact_y = edge_intersections_are_exact_y(frozen_counts, patterns, edges)
            literal_endpoints = literal_endpoint_core_masks(
                frozen_counts, patterns, traces
            )
            literal_nested = any(
                literal_endpoints[left] < literal_endpoints[right]
                for left, right in itertools.permutations(range(endpoint_count), 2)
            )
            literal_duplicate = False
            for pair in duplicate_pairs:
                small = int(pair["small"])
                large = int(pair["large"])
                small_only = literal_endpoints[small] - literal_endpoints[large]
                large_only = literal_endpoints[large] - literal_endpoints[small]
                literal_duplicate |= (
                    len(small_only) == 1
                    and not (small_only & TAIL_POSITIONS)
                    and large_only == {pair["swapped_tail"]}
                )
            literal_exact_y = all(
                literal_endpoints[left] & literal_endpoints[right] == {"y"}
                for left, right in edges
            )
            assert bool(nested) is literal_nested
            assert bool(duplicate) is literal_duplicate
            assert exact_y is literal_exact_y
            weight = orbit_weight(frozen_counts, marked_choice_factor)
            used = sum(frozen_counts)
            signature = {
                "counts_by_numeric_pattern": [
                    frozen_counts[patterns.index(mask)] for mask in range(1, 16)
                ],
                "containment_hit": bool(nested),
                "duplicate_remainder_hit": bool(duplicate),
                "edge_intersections_exactly_y": exact_y,
            }
            stream_hash.update(
                json.dumps(signature, sort_keys=True, separators=(",", ":")).encode("ascii")
                + b"\n"
            )

            orbit_counts["raw"] += 1
            literal_counts["raw"] += weight
            used_position_histogram[used] += 1
            if nested:
                orbit_counts["containment_hit_raw"] += 1
                literal_counts["containment_hit_raw"] += weight
                if first_nested is None:
                    first_nested = frozen_counts
            else:
                orbit_counts["after_containment"] += 1
                literal_counts["after_containment"] += weight
            if duplicate:
                orbit_counts["duplicate_hit_raw"] += 1
                literal_counts["duplicate_hit_raw"] += weight
                if first_duplicate is None:
                    first_duplicate = frozen_counts
            if nested and duplicate:
                orbit_counts["containment_and_duplicate_overlap"] += 1
                literal_counts["containment_and_duplicate_overlap"] += weight
            if not nested and duplicate:
                orbit_counts["duplicate_deleted_after_containment"] += 1
                literal_counts["duplicate_deleted_after_containment"] += weight
            if exact_y:
                orbit_counts["edge_intersections_exactly_y_raw"] += 1
                literal_counts["edge_intersections_exactly_y_raw"] += weight
            if not nested and not duplicate:
                orbit_counts["survivors"] += 1
                literal_counts["survivors"] += weight
                survivor_used_position_histogram[used] += 1
                if exact_y:
                    orbit_counts["edge_intersections_exactly_y_survivors"] += 1
                    literal_counts["edge_intersections_exactly_y_survivors"] += weight
                if first_survivor is None:
                    first_survivor = frozen_counts
            return

        pattern = patterns[index]
        capacity = min(
            remaining[vertex]
            for vertex in range(endpoint_count)
            if pattern >> vertex & 1
        )
        for multiplicity in range(capacity + 1):
            counts[index] = multiplicity
            next_remaining = tuple(
                remaining[vertex] - multiplicity * ((pattern >> vertex) & 1)
                for vertex in range(endpoint_count)
            )
            visit(index + 1, next_remaining)
        counts[index] = 0

    visit(0, residual)
    assert orbit_counts["raw"] == memoized_orbit_count(patterns, residual)
    assert literal_counts["raw"] == closed_form_all_marks
    assert orbit_counts == Counter(
        {
            "raw": 27172,
            "after_containment": 26966,
            "containment_hit_raw": 206,
            "duplicate_hit_raw": 567,
            "containment_and_duplicate_overlap": 12,
            "duplicate_deleted_after_containment": 555,
            "survivors": 26411,
            "edge_intersections_exactly_y_raw": 21,
            "edge_intersections_exactly_y_survivors": 19,
        }
    )
    assert (
        literal_counts["survivors"]
        == literal_counts["raw"]
        - literal_counts["containment_hit_raw"]
        - literal_counts["duplicate_hit_raw"]
        + literal_counts["containment_and_duplicate_overlap"]
    )
    assert first_nested is not None and first_duplicate is not None and first_survivor is not None

    def pattern_vector(frozen_counts: tuple[int, ...]) -> dict[str, int]:
        return {
            format(pattern, f"0{endpoint_count}b"): frozen_counts[index]
            for index, pattern in enumerate(patterns)
            if frozen_counts[index]
        }

    first_survivor_masks = representative_masks(first_survivor, patterns, row)
    assert not containment_hits(first_survivor, patterns, traces)
    assert not duplicate_remainder_hits(first_survivor, patterns, duplicate_pairs)
    assert edge_intersections_are_exact_y(first_survivor, patterns, edges)
    assert first_survivor_masks["K_size"] == 446
    assert first_survivor_masks["Q_H_sizes"] == [464, 465, 464, 464]

    return {
        "membership_pattern_convention": (
            "a four-bit word records membership in labelled endpoints H_0,H_1,H_2,H_3; "
            "the rightmost bit is H_0"
        ),
        "anonymous_position_count_after_marking_U_y_P": 468,
        "nonempty_membership_pattern_count": len(patterns),
        "endpoint_anonymous_degrees": list(residual),
        "marked_choice_factor_for_y_and_unordered_P": marked_choice_factor,
        "symmetry_group": (
            "S_471 on non-tail positions; y is a distinguished singleton, P is an unordered "
            "two-position marked block, and the other 468 positions are classified by membership pattern"
        ),
        "no_endpoint_or_tail_colour_quotient": True,
        "raw_literal_marked_mask_count_fixed_y_and_P": str(closed_form_fixed_marks),
        "raw_literal_marked_mask_count_all_y_and_P_choices": str(closed_form_all_marks),
        "orbit_counts": dict(orbit_counts),
        "literal_marked_mask_counts": {key: str(value) for key, value in literal_counts.items()},
        "used_anonymous_position_orbit_histogram": {
            str(key): value for key, value in sorted(used_position_histogram.items())
        },
        "survivor_used_anonymous_position_orbit_histogram": {
            str(key): value for key, value in sorted(survivor_used_position_histogram.items())
        },
        "complete_orbit_stream_sha256": stream_hash.hexdigest(),
        "literal_oracle_crosschecked_orbits": orbit_counts["raw"],
        "duplicate_candidate_pairs": duplicate_pairs,
        "first_containment_hit_pattern": pattern_vector(first_nested),
        "first_duplicate_hit_pattern": pattern_vector(first_duplicate),
        "first_survivor_pattern": pattern_vector(first_survivor),
        "first_survivor_literal_instance": first_survivor_masks,
    }


def build_report() -> dict[str, object]:
    dependencies = verify_dependencies()
    source, source_certificate = load_certified_report(SOURCE_REPORT)
    duplicate, duplicate_certificate = load_certified_report(DUPLICATE_REPORT)
    exact_slice, exact_slice_certificate = load_certified_report(EXACT_SLICE_REPORT)
    assert source["counts"]["surviving_outer_shards"] == 720
    rows = source["surviving_shards"]
    assert isinstance(rows, list) and len(rows) == 720
    matches = [
        row for row in rows if row["decorated_shard_id"] == CANONICAL_DECORATED_SHARD
    ]
    assert len(matches) == 1
    canonical_row = matches[0]
    enumeration = enumerate_canonical_shard(canonical_row)
    assert duplicate["quantifier_boundary"]["deletion_count_now"] == 0
    assert exact_slice["slice"]["P_size"] == 2

    report: dict[str, object] = {
        "schema": "unique_tail_p233_endpoint_mask_frontier_v1",
        "status": (
            "ONE_CANONICAL_LENGTH_DECORATED_SHARD_EXACTLY_ENUMERATED/"
            "26411_MASK_ORBITS_SURVIVE_LITERAL_ORACLES/"
            "INDEPENDENT_REVIEW_CORRECT/"
            "LABELLED_INTERSECTION_AND_ATOM_ORACLES_PENDING/FINITE_GLOBAL_INCOMPLETE"
        ),
        "p": P,
        "dependencies_sha256": dependencies,
        "dependency_certificates": {
            SOURCE_REPORT.name: source_certificate,
            DUPLICATE_REPORT.name: duplicate_certificate,
            EXACT_SLICE_REPORT.name: exact_slice_certificate,
        },
        "source_720_row_denominator": {
            "rows": 720,
            "fully_enumerated_rows_here": 1,
            "not_enumerated_rows_here": 719,
        },
        "canonical_shard": canonical_row,
        "exact_mask_schema": {
            "fixed_tail_positions": sorted(TAIL_POSITIONS),
            "marked_common_position": "y in Y minus U, required in every endpoint",
            "marked_packing_block": "P={p_1,p_2}, disjoint from U, y, and every endpoint",
            "anonymous_positions": "z_001,...,z_468",
            "endpoint_equations": (
                "H_i={y} union tail(trace_i) union all anonymous positions whose membership "
                "pattern contains i; pattern multiplicities solve the exact residual-size equations"
            ),
            "derived_sets": (
                "L=U union all H_i, R=Y minus L, K=R minus P, "
                "Q_H=K union (L minus H)=Y minus (H union P)"
            ),
            "complete_for_fixed_row": True,
            "equivalence_reason": (
                "two marked literal mask instances are in the same unmarked-position orbit iff "
                "all nonempty endpoint-membership pattern multiplicities agree"
            ),
        },
        "canonical_enumeration": enumeration,
        "oracle_ledger": [
            {
                "oracle": "endpoint_size_and_tail_trace",
                "scope": "exactly generated",
                "raw_orbits_deleted": 0,
            },
            {
                "oracle": "common_marked_y_and_stored_edge_incidence",
                "scope": (
                    "y lies in every endpoint and hence every stored edge intersection; edge tail traces are disjoint"
                ),
                "raw_orbits_deleted": 0,
            },
            {
                "oracle": "proper_endpoint_containment",
                "scope": (
                    "a proper containment of equal-sum endpoint blocks would leave a nonempty actual zero-sum difference"
                ),
                "raw_orbits_deleted": enumeration["orbit_counts"]["containment_hit_raw"],
            },
            {
                "oracle": "literal_duplicate_remainder",
                "scope": "the certified one-tail/one-outside-position sufficient obstruction",
                "raw_orbits_hit": enumeration["orbit_counts"]["duplicate_hit_raw"],
                "overlap_with_containment": enumeration["orbit_counts"][
                    "containment_and_duplicate_overlap"
                ],
                "orbits_deleted_after_containment": enumeration["orbit_counts"][
                    "duplicate_deleted_after_containment"
                ],
            },
            {
                "oracle": "literal_K_L_P_and_Q_derivation",
                "scope": "P is literally outside L, K=R minus P is nonempty, and every Q_H is derived from the same positions",
                "raw_orbits_deleted": 0,
                "minimum_K_size": 446,
            },
            {
                "oracle": "edge_intersection_rho_sum_nonzero",
                "scope": (
                    "19 survivors have every stored edge intersection exactly {y}, so this gate follows "
                    "once rho(y) is marked nonzero; the other 26392 survivors require shared rho labels"
                ),
                "not_a_mask_only_deletion": True,
            },
        ],
        "first_irreducible_denominator": {
            "mask_orbits_after_all_sound_mask_only_deletions": enumeration["orbit_counts"][
                "survivors"
            ],
            "exact_y_edge_intersection_orbits": enumeration["orbit_counts"][
                "edge_intersections_exactly_y_survivors"
            ],
            "nontrivial_edge_intersection_orbits_requiring_labels": (
                enumeration["orbit_counts"]["survivors"]
                - enumeration["orbit_counts"]["edge_intersections_exactly_y_survivors"]
            ),
            "next_required_layer": (
                "one shared rho label per literal position, the nonzero rho-sum of every stored edge "
                "intersection, P atomicity, K zero-sum-freeness, every Q_H atom/internal target, "
                "then unified q/height short closure"
            ),
        },
        "strict_boundaries": [
            "only decorated-1356 is completely enumerated; the other 719 length-decorated rows are untouched",
            "the S_471 quotient is only by unmarked-position permutations; endpoint identities and tail colours are not quotiented",
            "the two packing positions are exact literal positions but do not yet carry labels proving that rho(P) is an atom or that its sums are 3q and 3x-a",
            "a common marked y is present, but a larger edge intersection can have zero rho-sum after labels are assigned",
            "no unified rho, q-coordinate, height, short-spectrum, Hasse, long-complement, multiplicity, or actual-Z oracle is claimed clear",
            "this finite mask enumeration proves neither the canonical shard nor the p=233 slice SAT or UNSAT",
        ],
        "external_dependency_note": (
            "The certified 720-row input inherits the upstream Property-B length reduction.  "
            "The endpoint-mask orbit enumeration and its two literal deletion counts use no "
            "additional Property-B assertion."
        ),
        "conclusion": (
            "The first genuine endpoint-mask denominator is now exact for one canonical parent/length shard. "
            "Of 27172 unmarked-position orbits, 206 meet a proper-containment obstruction and a further "
            "555 meet the duplicate-remainder oracle, leaving 26411 literal mask orbits.  These survivors "
            "are inputs to the shared-label layer, not realizations."
        ),
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    report = build_report()
    with REPORT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    counts = report["canonical_enumeration"]["orbit_counts"]
    print("PASS canonical decorated-1356 endpoint-mask orbit enumeration")
    print("RAW ORBITS", counts["raw"])
    print("DELETE containment", counts["containment_hit_raw"])
    print("DELETE duplicate after containment", counts["duplicate_deleted_after_containment"])
    print("SURVIVING MASK ORBITS", counts["survivors"])
    print("CERTIFICATE", report["certificate_sha256"])
    print("SCOPE one of 720 rows; all shared-label oracles pending")


if __name__ == "__main__":
    main()
