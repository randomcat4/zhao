#!/usr/bin/env python3
"""Finite certificate for tail anchoring in the two large-prime unique-tail rows.

This script imports no author module.  It verifies the frozen dependency bytes,
checks the canonical certificates of the two input reports, and independently
rebuilds every finite arithmetic and trace table used in the accompanying proof.
"""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
SHORT_REPORT_PATH = HERE / "unique_tail_all_packing_short_blocks_report.json"
INTERNAL_REPORT_PATH = (
    HERE / "unique_tail_remaining_long_complement_internal_sums_report.json"
)
REPORT_PATH = HERE / "unique_tail_tail_anchoring_report.json"

EXPECTED_DEPENDENCY_SHA256 = {
    "proofs/unique_tail_labelled_position_next.md": (
        "60384c64dee88487220f3fd7101a5d3abff1cb576fe3a8b43ec398fdd284ddce"
    ),
    "verifications/unique_tail_labelled_position_next_independent_review.md": (
        "7cc525664dbbf7eeb23d04b3e061f0c4feac07100c7b6c294ee018ad658f20dd"
    ),
    "proofs/unique_tail_common_R_next.md": (
        "1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942"
    ),
    "verifications/unique_tail_common_R_next_independent_review.md": (
        "35f355d2fe1b3dc7a98e3011e44f0e3cdea17cfdd104c026042081b00c4539d3"
    ),
    "proofs/unique_tail_all_packing_short_blocks.md": (
        "7abe228fa70dabd8858a40507b11505bd9cee388aa89fd79cd7a22fb8ec68238"
    ),
    "verifications/unique_tail_all_packing_short_blocks_independent_review.md": (
        "d22d9380a0dc98c21a691384901a9f826f88b72bab85042beafc053eed8124e3"
    ),
    "unique_tail_all_packing_short_blocks_report.json": (
        "4dadb5a6fca18da42ccd95821cc176cd9fae1ce2653ddb2e14406e5e66694ceb"
    ),
    "proofs/unique_tail_remaining_long_complement_internal_sums.md": (
        "311730df217f79659cf0d934b8c0df2e02489196208b9e699dc31d8b929d10d1"
    ),
    "verifications/unique_tail_remaining_long_complement_internal_sums_independent_review.md": (
        "44f191264d4505dbeb4803978d86b3101c8207951e41f7d1edd34d4ba40b204a"
    ),
    "unique_tail_remaining_long_complement_internal_sums_report.json": (
        "b6b3de4097627d26a492f4d1034a1f753bc0d58b83edd92bd100815dd8fc3cae"
    ),
    "proofs/unique_tail_position_conflict_frontier.md": (
        "a30707af2f6ef04da720a8eb3c1e97b1c7c297eecc67cf6879ff1191ff9afa8b"
    ),
    "verifications/unique_tail_position_conflict_frontier_independent_review.md": (
        "93381c12a56f32469d6dcb0d21c65b22509837484323e2ad1763a81218d771b5"
    ),
    "proofs/unique_tail_four_edge_joint_csp.md": (
        "87954d09a00aa74d3d43ce7d784deeff325965e61fca80e900d610371260201f"
    ),
    "verifications/unique_tail_four_edge_joint_csp_independent_review.md": (
        "3ddd10c87c6f0de70a67e0cd630f3e2b3075200a8356c491eb4ad0f4b5359f3c"
    ),
}

TAIL = frozenset((1, 2, 3))


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verified_dependencies() -> dict[str, str]:
    actual = {
        relative: file_sha256(HERE / relative)
        for relative in EXPECTED_DEPENDENCY_SHA256
    }
    assert actual == EXPECTED_DEPENDENCY_SHA256
    return actual


def load_verified_report(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    claimed = data.pop("certificate_sha256")
    assert canonical_hash(data) == claimed
    data["certificate_sha256"] = claimed
    return data


def remaining_rows(short_report: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case in short_report["cases"]:
        for packing in case["packing_rows"]:
            if packing["packing_type"] not in ("empty", "(2)", "(3)"):
                continue
            for vector in packing["vectors"]:
                if not vector["survives_q_fibre_gate"]:
                    continue
                atom_sizes = vector["atom_sizes"]
                rows.append(
                    {
                        "p": case["p"],
                        "b": case["b"],
                        "packing_type": packing["packing_type"],
                        "P_size": sum(atom_sizes),
                        "atom_sizes": atom_sizes,
                    }
                )
    assert [
        (row["p"], row["packing_type"], row["P_size"])
        for row in rows
    ] == [
        (233, "empty", 0),
        (233, "(2)", 1),
        (233, "(2)", 2),
        (233, "(3)", 1),
        (233, "(3)", 2),
        (233, "(3)", 3),
        (1399, "empty", 0),
        (1399, "(2)", 1),
        (1399, "(3)", 1),
        (1399, "(3)", 2),
    ]
    return rows


def anchoring_rows() -> list[dict[str, object]]:
    rows = []
    for p, b in ((233, 4), (1399, 5)):
        for coefficient in (1, 2, 3):
            maximum = 4 - b + coefficient
            coefficient_one_excluded = coefficient == 1
            rows.append(
                {
                    "p": p,
                    "b": b,
                    "axis_coefficient_e": coefficient,
                    "X_core_size_b_minus_e": b - coefficient,
                    "U_free_atom_length_upper_bound_4_minus_b_plus_e": maximum,
                    "coefficient_one_excluded": coefficient_one_excluded,
                    "exclusion_reason": (
                        "nonempty length is impossible"
                        if coefficient_one_excluded and maximum == 0
                        else (
                            "the only possible length is one, which adds a q-labelled position to the p-4 q anchors"
                            if coefficient_one_excluded
                            else None
                        )
                    ),
                }
            )
    assert [(row["p"], row["axis_coefficient_e"], row[
        "U_free_atom_length_upper_bound_4_minus_b_plus_e"
    ]) for row in rows] == [
        (233, 1, 1), (233, 2, 2), (233, 3, 3),
        (1399, 1, 0), (1399, 2, 1), (1399, 3, 2),
    ]
    return rows


def common_kernel_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    result = []
    for row in rows:
        n = row["P_size"]
        lower = 2 * row["p"] - 44 - n
        result.append(
            {
                **row,
                "K_length_lower_bound_from_L_at_most_52": lower,
                "K_nonempty": lower > 0,
                "L_plus_P_size_lower_bound_from_Davenport": 10,
            }
        )
    assert min(row["K_length_lower_bound_from_L_at_most_52"] for row in result) == 419
    assert all(row["K_nonempty"] for row in result)
    return result


def type_two_endpoint_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    result = []
    for row in rows:
        if row["packing_type"] != "(2)":
            continue
        n = row["P_size"]
        for h in (6, 7, 8):
            for trace_size in (1, 2):
                if trace_size == 1:
                    survives = h + n >= 8
                    q_status = (
                        "split_(1,1)_forced"
                        if survives and h + n == 8
                        else (
                            "atom_(2)_or_split_(1,1)"
                            if survives
                            else "eliminated_by_V_H_zero_sum_free_length"
                        )
                    )
                else:
                    survives = h + n >= 9
                    q_status = (
                        "atom_(2)_forced"
                        if survives
                        else "eliminated_by_forced_Q_H_atom_length"
                    )
                result.append(
                    {
                        "p": row["p"],
                        "b": row["b"],
                        "P_size": n,
                        "H_size": h,
                        "trace_size": trace_size,
                        "missing_tail_size": 3 - trace_size,
                        "H_plus_P_size": h + n,
                        "survives": survives,
                        "Q_H_status": q_status,
                    }
                )
    surviving = [
        (r["p"], r["P_size"], r["H_size"], r["trace_size"], r["Q_H_status"])
        for r in result if r["survives"]
    ]
    assert surviving == [
        (233, 1, 7, 1, "split_(1,1)_forced"),
        (233, 1, 8, 1, "atom_(2)_or_split_(1,1)"),
        (233, 1, 8, 2, "atom_(2)_forced"),
        (233, 2, 6, 1, "split_(1,1)_forced"),
        (233, 2, 7, 1, "atom_(2)_or_split_(1,1)"),
        (233, 2, 7, 2, "atom_(2)_forced"),
        (233, 2, 8, 1, "atom_(2)_or_split_(1,1)"),
        (233, 2, 8, 2, "atom_(2)_forced"),
        (1399, 1, 7, 1, "split_(1,1)_forced"),
        (1399, 1, 8, 1, "atom_(2)_or_split_(1,1)"),
        (1399, 1, 8, 2, "atom_(2)_forced"),
    ]
    return result


def integer_partitions(total: int, lower: int = 1) -> list[list[int]]:
    if total == 0:
        return [[]]
    result = []
    for first in range(lower, min(3, total) + 1):
        for suffix in integer_partitions(total - first, first):
            result.append([first, *suffix])
    return result


def empty_factorization_rows() -> list[dict[str, object]]:
    patterns = [parts for parts in integer_partitions(4) if len(parts) >= 2]
    assert patterns == [[1, 1, 1, 1], [1, 1, 2], [1, 3], [2, 2]]
    rows = []
    for trace_size in (1, 2):
        missing = 3 - trace_size
        for parts in patterns:
            coefficient_one_count = parts.count(1)
            survives = coefficient_one_count <= missing
            forced_u_free = []
            if survives and parts == [1, 1, 2]:
                forced_u_free = [2]
            if survives and trace_size == 2 and parts == [1, 3]:
                forced_u_free = [3]
            if survives and trace_size == 2 and parts == [2, 2]:
                forced_u_free = [2]
            rows.append(
                {
                    "trace_size": trace_size,
                    "missing_tail_size": missing,
                    "atomic_factor_coefficients": parts,
                    "coefficient_one_factor_count": coefficient_one_count,
                    "survives_tail_anchoring": survives,
                    "forced_U_free_factor_coefficients": forced_u_free,
                }
            )
    assert {
        trace: [
            row["atomic_factor_coefficients"]
            for row in rows
            if row["trace_size"] == trace and row["survives_tail_anchoring"]
        ]
        for trace in (1, 2)
    } == {
        1: [[1, 1, 2], [1, 3], [2, 2]],
        2: [[1, 3], [2, 2]],
    }
    return rows


def empty_endpoint_rows() -> list[dict[str, object]]:
    rows = []
    for p, b in ((233, 4), (1399, 5)):
        maximum = 7 - b
        for h in (6, 7, 8):
            for trace_size in (1, 2):
                missing = 3 - trace_size
                v_excess = max(0, 10 - h - missing)
                survives = v_excess <= maximum
                forced_atom = survives and v_excess > 0
                possible_coefficients = []
                if forced_atom:
                    possible_coefficients = [
                        e for e in (2, 3) if 4 - b + e >= v_excess
                    ]
                exact_f2_coefficient_three = (
                    forced_atom
                    and v_excess == maximum
                    and possible_coefficients == [3]
                )
                rows.append(
                    {
                        "p": p,
                        "b": b,
                        "H_size": h,
                        "trace_size": trace_size,
                        "missing_tail_size": missing,
                        "V_H_length_offset_from_2p": 8 - h - missing,
                        "forced_U_free_atom_length_lower_bound": v_excess,
                        "forced_U_free_atom_length_upper_bound": maximum,
                        "survives": survives,
                        "U_free_atom_forced": forced_atom,
                        "possible_forced_atom_axis_coefficients": possible_coefficients,
                        "exact_coefficient_three_F2_block": exact_f2_coefficient_three,
                        "exact_F2_atom_actual_sum": (
                            "3x-a" if exact_f2_coefficient_three else None
                        ),
                    }
                )
    assert [
        (r["p"], r["H_size"], r["trace_size"])
        for r in rows if not r["survives"]
    ] == [(1399, 6, 2)]
    assert [
        (r["p"], r["H_size"], r["trace_size"])
        for r in rows if r["exact_coefficient_three_F2_block"]
    ] == [(233, 6, 2), (1399, 6, 1), (1399, 7, 2)]
    return rows


def trace_name(trace: frozenset[int]) -> str:
    return "{" + ",".join(str(value) for value in sorted(trace)) + "}"


def trace_relation(left: frozenset[int], right: frozenset[int]) -> str:
    if left == right:
        return "same_singleton" if len(left) == 1 else "same_doubleton"
    if not left & right:
        return (
            "distinct_singletons"
            if len(left) == len(right) == 1
            else "complementary_singleton_doubleton"
        )
    if left < right or right < left:
        return "nested_singleton_doubleton"
    return "distinct_doubletons"


def empty_axial_intersection_rows() -> list[dict[str, object]]:
    traces = [
        frozenset(combo)
        for size in (1, 2)
        for combo in combinations(sorted(TAIL), size)
    ]
    rows = []
    for left_index, right_index in combinations_with_replacement(
        range(len(traces)), 2
    ):
        left = traces[left_index]
        right = traces[right_index]
        comparable = bool(left & right) and left | right != TAIL
        allowed_t = [2, 3] if comparable else []
        rows.append(
            {
                "left_trace": trace_name(left),
                "right_trace": trace_name(right),
                "trace_relation": trace_relation(left, right),
                "tail_intersection_nonempty": bool(left & right),
                "tail_union_is_proper": left | right != TAIL,
                "allowed_axial_intersection_t": allowed_t,
            }
        )
    assert len(rows) == 21
    by_relation: dict[str, set[tuple[int, ...]]] = {}
    for row in rows:
        by_relation.setdefault(row["trace_relation"], set()).add(
            tuple(row["allowed_axial_intersection_t"])
        )
    assert by_relation == {
        "same_singleton": {(2, 3)},
        "same_doubleton": {(2, 3)},
        "nested_singleton_doubleton": {(2, 3)},
        "distinct_singletons": {()},
        "complementary_singleton_doubleton": {()},
        "distinct_doubletons": {()},
    }
    assert all(1 not in row["allowed_axial_intersection_t"] for row in rows)
    return rows


def mixed_target_rows(internal_report: dict[str, object]) -> list[dict[str, object]]:
    rows = []
    for source in internal_report["remaining_nonempty_size_rows"]:
        rows.append(
            {
                "p": source["p"],
                "b": source["b"],
                "packing_type": source["packing_type"],
                "P_axis_coefficient": source["P_axis_coefficient"],
                "P_size": source["P_size"],
                "independent_proper_P_subset_orbit_count": source[
                    "independent_mixed_target_fibre_count"
                ],
                "shared_endpoint_gate": (
                    "if rho(sum(S))=rho(sum(H intersection J)), then "
                    "sum(S)-sum(H intersection J) is in {q,2q,3q}"
                ),
            }
        )
    assert len(rows) == 8
    assert sorted(
        set(
            (row["P_size"], row["independent_proper_P_subset_orbit_count"])
            for row in rows
        )
    ) == [(1, 0), (2, 1), (3, 3)]
    return rows


def build_report() -> dict[str, object]:
    dependencies = verified_dependencies()
    short_report = load_verified_report(SHORT_REPORT_PATH)
    internal_report = load_verified_report(INTERNAL_REPORT_PATH)
    rows = remaining_rows(short_report)
    type_two_rows = type_two_endpoint_rows(rows)
    empty_rows = empty_endpoint_rows()
    axial_rows = empty_axial_intersection_rows()

    report: dict[str, object] = {
        "schema": "unique_tail_tail_anchoring_v1",
        "scope": {
            "assumptions": [
                "p,b are (233,4) or (1399,5)",
                "the common literal partition is Y=L disjoint_union P disjoint_union K with |Y|=2p+8, |L|<=52, and rho(K) zero-sum-free",
                "only packing types empty, (2), and (3), with the frozen surviving P sizes, are considered",
                "every endpoint H is an actual zero-core F3 block of length 6..8 with a nonempty proper trace in the three-position tail U",
                "the complete literal long-complement axial criterion, the quotient-zero gap, the short spectrum, the unique positive-core F3 tail, and the p-4 nonzero-fibre bound are used",
            ],
            "conclusion": (
                "every U-free rho-zero block of axis coefficient e=1,2,3 has length at most 4-b+e; coefficient-one atom factors must consume distinct positions of U\\H; the finite type-(2), empty-packing, endpoint-intersection, and mixed-target consequences listed below follow"
            ),
            "not_concluded": [
                "the empty packing is impossible",
                "packing type (2) is impossible",
                "packing type (3) is impossible",
                "a mixed target collision exists",
                "a complete quotient-label SAT or UNSAT result",
                "any height or Hasse constraint",
                "A_p",
            ],
        },
        "dependencies_sha256": dependencies,
        "remaining_packing_rows": rows,
        "common_kernel_bounds": common_kernel_rows(rows),
        "tail_anchoring_bounds": anchoring_rows(),
        "type_2": {
            "endpoint_state_rows": type_two_rows,
            "V_H_zero_sum_free_for_every_trace": True,
            "all_distinct_endpoint_intersections_are_nonaxial": True,
        },
        "empty": {
            "atomic_factorization_rows": empty_factorization_rows(),
            "endpoint_U_free_atom_rows": empty_rows,
            "V_H_maximum_disjoint_rho_atom_count": 1,
            "conditional_coefficient_two_singleton": {
                "p": 1399,
                "short_block": "X_3 disjoint_union U disjoint_union {y}",
                "short_block_length": 7,
                "short_block_family": "F2",
                "quotient_label": "2q",
                "actual_label": "2x-a",
            },
            "axial_endpoint_intersection_trace_rows": axial_rows,
            "axial_intersection_t_one_excluded": True,
            "axial_intersection_requires_comparable_traces": True,
        },
        "mixed_target_shared_endpoint_rows": mixed_target_rows(internal_report),
        "summary": {
            "remaining_packing_row_count": len(rows),
            "tail_anchoring_arithmetic_row_count": 6,
            "type_2_endpoint_state_row_count": len(type_two_rows),
            "type_2_surviving_endpoint_state_count": sum(
                row["survives"] for row in type_two_rows
            ),
            "empty_factorization_state_count": 8,
            "empty_endpoint_state_row_count": len(empty_rows),
            "empty_eliminated_endpoint_states": [
                {"p": 1399, "H_size": 6, "trace_size": 2}
            ],
            "empty_exact_coefficient_three_F2_states": [
                {"p": 233, "H_size": 6, "trace_size": 2},
                {"p": 1399, "H_size": 6, "trace_size": 1},
                {"p": 1399, "H_size": 7, "trace_size": 2},
            ],
            "empty_trace_pair_row_count": len(axial_rows),
            "mixed_target_row_count": 8,
        },
        "status": "TAIL_ANCHORING_PROVED_REDUCTION__PENDING_INDEPENDENT_REVIEW__GLOBAL_INCOMPLETE",
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    report = build_report()
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
