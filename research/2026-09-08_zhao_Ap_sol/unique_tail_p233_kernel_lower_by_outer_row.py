#!/usr/bin/env python3
"""Exact common-kernel lower bounds for the 720 mixed-length outer rows.

This is an outer-incidence reduction only.  It uses the certified endpoint
traces, endpoint lengths, the one common non-tail witness, |Y|=474 and |P|=2.
It does not instantiate endpoint masks or labels.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path


P = 233
Y_SIZE = 474
PACKING_SIZE = 2
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "unique_tail_p233_length_decorated_trace_reduction_report.json"
REPORT = HERE / "unique_tail_p233_kernel_lower_by_outer_row_report.json"


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def trace_size(mask: int) -> int:
    if mask <= 0 or mask >= 7:
        raise AssertionError(f"invalid nonempty proper tail trace {mask}")
    return mask.bit_count()


def row_lower_bound(row: dict[str, object]) -> dict[str, object]:
    traces = [int(value) for value in row["endpoint_trace_masks"]]
    lengths = [int(value) for value in row["endpoint_lengths"]]
    if len(traces) != len(lengths):
        raise AssertionError("trace/length arity mismatch")

    # U contributes three positions.  Every endpoint has the certified common
    # non-tail witness y.  Beyond U and y, endpoint i can add at most
    # |H_i|-|H_i intersect U|-1 new positions.
    private_slot_upper = sum(
        length - trace_size(trace) - 1 for trace, length in zip(traces, lengths)
    )
    l_upper = 4 + private_slot_upper

    # In type (3), R=Y\L and K=R\P with |Y|=474 and |P|=2.
    k_lower = Y_SIZE - PACKING_SIZE - l_upper
    length_seven_count = sum(length == 7 for length in lengths)
    common_support_point_lower = (
        (k_lower + (P - 2)) // (P - 1) if length_seven_count else None
    )
    return {
        "decorated_shard_id": row["decorated_shard_id"],
        "parent_shard_id": row["parent_shard_id"],
        "shape": row["shape"],
        "endpoint_count": len(lengths),
        "endpoint_trace_masks": traces,
        "endpoint_lengths": lengths,
        "length_seven_maximal_complement_count": length_seven_count,
        "private_slot_upper": private_slot_upper,
        "L_size_upper": l_upper,
        "K_size_lower": k_lower,
        "property_b_common_support_point_lower": common_support_point_lower,
    }


def build_report() -> dict[str, object]:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = source["surviving_shards"]
    if len(rows) != 720:
        raise AssertionError("expected the certified 720 outer survivors")

    bounds = [row_lower_bound(row) for row in rows]
    k_distribution = Counter(int(row["K_size_lower"]) for row in bounds)
    h7_distribution = Counter(
        int(row["length_seven_maximal_complement_count"]) for row in bounds
    )
    joint: dict[int, Counter[int]] = defaultdict(Counter)
    for row in bounds:
        joint[int(row["length_seven_maximal_complement_count"])][
            int(row["K_size_lower"])
        ] += 1

    if sum(k_distribution.values()) != 720:
        raise AssertionError("kernel distribution lost rows")
    if h7_distribution != Counter({2: 288, 1: 186, 3: 174, 0: 36, 4: 36}):
        raise AssertionError("unexpected length-seven distribution")
    if min(k_distribution) != 435 or max(k_distribution) != 447:
        raise AssertionError("unexpected common-kernel range")
    if any(
        row["property_b_common_support_point_lower"] != 2
        for row in bounds
        if int(row["length_seven_maximal_complement_count"]) > 0
    ):
        raise AssertionError("every Property-B-applicable row must require two support points")

    core: dict[str, object] = {
        "schema": "unique_tail_p233_kernel_lower_by_outer_row/v1",
        "p": P,
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "status": "EXACT_OUTER_KERNEL_LOWER_BOUND/PROPERTY_B_CAPACITY_ORACLE/GLOBAL_INCOMPLETE",
        "derivation": {
            "L_upper": "4 + sum_i(|H_i|-|trace_i|-1)",
            "K_identity": "|K|=|Y|-|P|-|L|=472-|L|",
            "K_lower": "468-sum_i(|H_i|-|trace_i|-1)",
            "maximal_atom_label_capacity": (
                "in a Property-B standard atom of length 2p-1, every literal label "
                "has multiplicity at most p-1"
            ),
        },
        "counts": {
            "outer_survivors": len(bounds),
            "rows_with_at_least_one_length_seven_maximal_complement": sum(
                count for h7, count in h7_distribution.items() if h7 >= 1
            ),
            "rows_with_at_least_two_length_seven_maximal_complements": sum(
                count for h7, count in h7_distribution.items() if h7 >= 2
            ),
            "K_size_lower_distribution": {
                str(key): k_distribution[key] for key in sorted(k_distribution)
            },
            "length_seven_maximal_complement_distribution": {
                str(key): h7_distribution[key] for key in sorted(h7_distribution)
            },
            "joint_h7_K_lower_distribution": {
                str(h7): {str(k): rows for k, rows in sorted(counter.items())}
                for h7, counter in sorted(joint.items())
            },
        },
        "property_b_capacity_consequence": {
            "applicable_rows": 684,
            "multi_support_intersection_rows": 498,
            "required_common_support_points": 2,
            "reason": (
                "K lies in every maximal complement support and |K|>=435, while one "
                "support label contributes at most p-1=232 literal positions"
            ),
            "oracle": (
                "reject any Property-B support tuple whose common point set has size at most one"
            ),
        },
        "rows": bounds,
        "scope_boundary": [
            "the K lower bound is exact as a consequence of outer data, but need not be attained",
            "the report does not enumerate actual endpoint masks",
            "support tuples with at least two common points are not claimed realizable",
            "no p=233 mixed-length slice and no global A_p conclusion is claimed",
        ],
    }
    report = dict(core)
    report["certificate_sha256"] = canonical_hash(core)
    return report


def main() -> None:
    report = build_report()
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    counts = report["counts"]
    print("PASS 720 exact outer kernel lower bounds")
    print("K LOWER RANGE 435..447")
    print("PROPERTY-B MULTI-SUPPORT ROWS 498 REQUIRE >=2 COMMON POINTS")
    print(f"CERTIFICATE {report['certificate_sha256']}")


if __name__ == "__main__":
    main()
