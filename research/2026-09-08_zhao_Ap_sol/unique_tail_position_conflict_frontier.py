#!/usr/bin/env python3
"""Finite certificate for unique_tail_position_conflict_frontier.md.

This checks only the thirteen-type arithmetic and named graph/count interfaces.
It is not a labelled-instance solver and does not claim global infeasibility.
"""

from __future__ import annotations

import hashlib
import json


SURVIVORS = (
    (11, 7, 2, 5),
    (13, 6, 3, 3),
    (13, 8, 3, 5),
    (19, 6, 1, 5),
    (19, 8, 1, 7),
    (23, 6, 3, 3),
    (23, 8, 3, 5),
    (43, 7, 3, 4),
    (101, 6, 2, 4),
    (101, 8, 2, 6),
    (233, 7, 4, 3),
    (701, 8, 4, 4),
    (1399, 8, 5, 3),
)

NAMED = {
    233: {
        "multi_trace_min": 58,
        "singleton_trace_min": 93,
        "tail_disjoint_edges_min": 1628,
        "outside_positions": 471,
        "labelled_edge_congestion_min": 4,
        "local_shard_intersection_size_max": 7,
        "local_shard_union_size_max": 25,
        "local_shard_endpoint_blocks_max": 8,
        "trace_rule": "every_nonempty_proper_trace_projected_nonzero",
    },
    701: {
        "multi_trace_min": 123,
        "singleton_trace_min": 0,
        "tail_disjoint_edges_min": 0,
        "outside_positions": 1406,
        "labelled_edge_congestion_min": 0,
        "trace_rule": "k3_nonaxis;_k2_nonaxis_or_sum_-5q_global_transversal",
    },
    1399: {
        "multi_trace_min": 322,
        "singleton_trace_min": 266,
        "tail_disjoint_edges_min": 9310,
        "outside_positions": 2803,
        "labelled_edge_congestion_min": 4,
        "local_shard_intersection_size_max": 7,
        "local_shard_union_size_max": 25,
        "local_shard_endpoint_blocks_max": 8,
        "trace_rule": "every_nonempty_proper_trace_projected_nonzero",
    },
}

EXPECTED_TYPE_TABLE_SHA256 = (
    "d10bcffce8e708eda4165b329d2dc9ba94852db32535acc035141a1a11da3b37"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "5d4f96f4f03be57ac0cba9c6dd170955a300eba15e833567e72ebcaa9f1da6f3"
)


def least_abs_residue(value: int, p: int) -> int:
    residue = value % p
    return min(residue, p - residue)


def mu(p: int) -> int:
    return least_abs_residue(pow(20, -1, p), p)


def ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def axis_singleton_candidates(p: int, ell: int, b: int) -> list[int]:
    """Run the two-stage arithmetic in Lemma 1.

    alpha means bar(u)=alpha*q.  Stage one uses X_c+u and the complementary
    tail.  Stage two removes alpha=1 by the p-4 complement multiplicity cap.
    """

    assert b + 3 <= p - 4
    candidates: list[int] = []
    for alpha in range(1, p):
        c = (-alpha) % p
        if c == 0 or 1 <= c <= 7 or 8 <= c <= p - 4:
            continue
        assert c in (p - 3, p - 2, p - 1)
        assert alpha in (3, 2, 1)
        complementary_length = ell - 1 + alpha
        if complementary_length >= 8:
            continue
        candidates.append(alpha)
    return [alpha for alpha in candidates if alpha != 1]


def axis_position_upper_bound(p: int, ell: int, b: int, r: int) -> int:
    candidates = axis_singleton_candidates(p, ell, b)
    if not candidates:
        return 0
    assert candidates == [2] and ell == 6
    # If r-1 projected points vanished, the final one would vanish too.
    # All r points cannot equal 2q because 2r != -b (mod p).
    assert (2 * r + b) % p != 0
    return r - 2


def type_record(item: tuple[int, int, int, int]) -> dict[str, object]:
    p, ell, b, r = item
    assert r == ell - b
    candidates = axis_singleton_candidates(p, ell, b)
    return {
        "p": p,
        "ell": ell,
        "b": b,
        "r": r,
        "axis_singleton_coefficients": candidates,
        "axis_position_upper_bound": axis_position_upper_bound(p, ell, b, r),
        "q_label_y_capacity": 3 if b == 4 else 0,
        "q_label_y_common_required": True,
    }


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    records = [type_record(item) for item in SURVIVORS]

    assert len(records) == 13
    assert sum(not row["axis_singleton_coefficients"] for row in records) == 9
    assert sum(row["axis_singleton_coefficients"] == [2] for row in records) == 4
    assert sum(row["q_label_y_capacity"] == 0 for row in records) == 11
    assert sum(row["q_label_y_capacity"] == 3 for row in records) == 2

    for p, row in NAMED.items():
        survivor = next(item for item in SURVIVORS if item[0] == p)
        _, _, _, r = survivor
        assert row["outside_positions"] == 2 * p + 8 - r
        expected_congestion = (
            ceil_div(row["tail_disjoint_edges_min"], row["outside_positions"])
            if row["tail_disjoint_edges_min"]
            else 0
        )
        assert row["labelled_edge_congestion_min"] == expected_congestion
        if expected_congestion:
            assert row["local_shard_intersection_size_max"] == 7
            assert row["local_shard_union_size_max"] == 1 + 4 * (7 - 1)
            assert row["local_shard_endpoint_blocks_max"] == 2 * 4

    assert sum(row["multi_trace_min"] for row in NAMED.values()) == 503
    assert sum(row["tail_disjoint_edges_min"] for row in NAMED.values()) == 10938

    assert mu(233) == 35
    assert mu(1399) == 70
    collision_profiles = {
        233: {
            length: mu(233) > 2 ** (length - 1) - 1
            for length in (6, 7, 8)
        },
        1399: {
            length: mu(1399) > 2 ** (length - 1) - 1
            for length in (6, 7, 8)
        },
    }
    assert collision_profiles == {
        233: {6: True, 7: False, 8: False},
        1399: {6: True, 7: True, 8: False},
    }

    certificate = {
        "status": "PROVED_REDUCTION/NO_TYPE_CLOSED/GLOBAL_INCOMPLETE",
        "types": records,
        "named": NAMED,
        "collision_profiles": collision_profiles,
        "mu": {233: mu(233), 1399: mu(1399)},
    }
    type_table_hash = canonical_hash(records)
    certificate_hash = canonical_hash(certificate)
    assert type_table_hash == EXPECTED_TYPE_TABLE_SHA256
    assert certificate_hash == EXPECTED_CERTIFICATE_SHA256
    report = {
        "type_count": len(records),
        "no_axis_singleton_type_count": 9,
        "only_2q_axis_singleton_type_count": 4,
        "q_label_free_y_type_count": 11,
        "q_label_capacity_three_type_count": 2,
        "multi_trace_total": 503,
        "tail_disjoint_edge_total": 10938,
        "labelled_congestion": {"233": 4, "1399": 4},
        "type_table_sha256": type_table_hash,
        "certificate_sha256": certificate_hash,
        "status": certificate["status"],
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
