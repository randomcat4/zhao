#!/usr/bin/env python3
"""Exact outer trace shards for the first p=233 type-(3) CEGAR slice.

This enumerates only the four-edge graph and its injective trace assignment.
It deliberately does not invent endpoint position masks or quotient labels.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_p233_type3_p2_trace_shards_report.json"

P = 233
TRACE_MASKS = tuple(range(1, 7))
SINGLETON_MASKS = frozenset((1, 2, 4))

SHAPES: dict[str, tuple[int, tuple[tuple[int, int], ...]]] = {
    "P5": (5, ((0, 1), (1, 2), (2, 3), (3, 4))),
    "K1_4": (5, ((0, 1), (0, 2), (0, 3), (0, 4))),
    "T5": (5, ((0, 1), (0, 2), (0, 3), (1, 4))),
    "C4": (4, ((0, 1), (1, 2), (2, 3), (3, 0))),
    "paw": (4, ((0, 1), (1, 2), (2, 0), (0, 3))),
    "P4_plus_K2": (6, ((0, 1), (1, 2), (2, 3), (4, 5))),
    "K1_3_plus_K2": (6, ((0, 1), (0, 2), (0, 3), (4, 5))),
    "K3_plus_K2": (5, ((0, 1), (1, 2), (2, 0), (3, 4))),
    "two_P3": (6, ((0, 1), (1, 2), (3, 4), (4, 5))),
    "P3_plus_two_K2": (7, ((0, 1), (1, 2), (3, 4), (5, 6))),
    "four_K2": (8, ((0, 1), (2, 3), (4, 5), (6, 7))),
}

EXPECTED_COUNTS = {
    "C4": (48, 48, 0),
    "K1_3_plus_K2": (1008, 1008, 0),
    "K1_4": (246, 246, 0),
    "K3_plus_K2": (72, 72, 0),
    "P3_plus_two_K2": (4320, 4320, 0),
    "P4_plus_K2": (864, 852, 12),
    "P5": (174, 168, 6),
    "T5": (198, 186, 12),
    "four_K2": (20736, 20736, 0),
    "paw": (18, 12, 6),
    "two_P3": (900, 900, 0),
}

DEPENDENCY_PATHS = (
    HERE / "unique_tail_four_edge_joint_csp.py",
    HERE / "proofs" / "unique_tail_four_edge_joint_csp.md",
    HERE / "verifications" / "unique_tail_four_edge_joint_csp_independent_review.md",
    HERE / "proofs" / "unique_tail_p233_singleton_tail_fringe.md",
    HERE / "verifications" / "unique_tail_p233_singleton_tail_fringe_independent_review.md",
)


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def dependency_hashes() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in DEPENDENCY_PATHS:
        result[path.relative_to(HERE).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def valid_trace_assignment(
    assignment: tuple[int, ...], edges: tuple[tuple[int, int], ...]
) -> bool:
    return all(not (assignment[left] & assignment[right]) for left, right in edges)


def full_count_table() -> dict[str, dict[str, int]]:
    table: dict[str, dict[str, int]] = {}
    for name, (vertex_count, edges) in SHAPES.items():
        total = repeated = distinct = 0
        for assignment in itertools.product(TRACE_MASKS, repeat=vertex_count):
            if not valid_trace_assignment(assignment, edges):
                continue
            total += 1
            if len(set(assignment)) == vertex_count:
                distinct += 1
                assert SINGLETON_MASKS <= set(assignment)
            else:
                repeated += 1
        assert (total, repeated, distinct) == EXPECTED_COUNTS[name]
        table[name] = {
            "valid": total,
            "repeated_trace": repeated,
            "all_distinct_trace": distinct,
        }
    assert sum(row["valid"] for row in table.values()) == 28584
    assert sum(row["repeated_trace"] for row in table.values()) == 28548
    assert sum(row["all_distinct_trace"] for row in table.values()) == 36
    return dict(sorted(table.items()))


def trace_shards() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for shape in sorted(SHAPES):
        vertex_count, edges = SHAPES[shape]
        for assignment in itertools.permutations(TRACE_MASKS, vertex_count):
            if not valid_trace_assignment(assignment, edges):
                continue
            assert SINGLETON_MASKS <= set(assignment)
            rows.append(
                {
                    "shape": shape,
                    "vertex_count": vertex_count,
                    "edges": [list(edge) for edge in edges],
                    "endpoint_trace_masks": list(assignment),
                }
            )
    rows.sort(
        key=lambda row: (
            str(row["shape"]),
            tuple(int(value) for value in row["endpoint_trace_masks"]),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["shard_id"] = f"trace-{index:02d}"
    assert len(rows) == 36
    assert Counter(row["shape"] for row in rows) == Counter(
        {"P4_plus_K2": 12, "P5": 6, "T5": 12, "paw": 6}
    )
    return rows


def build_report() -> dict[str, object]:
    table = full_count_table()
    shards = trace_shards()
    report: dict[str, object] = {
        "schema": "unique_tail_p233_type3_p2_trace_shards_v1",
        "fixed_slice": {
            "p": P,
            "unique_type": [7, 4],
            "packing_type": [3],
            "P_size": 2,
            "kappa": 1,
            "endpoint_length_stage": "length_7_only",
            "tail_projection_rank": 2,
        },
        "dependencies_sha256": dependency_hashes(),
        "full_eleven_shape_count_table": table,
        "trace_shards": shards,
        "scope": (
            "exhaustive only for the fixed representatives of the four-edge graph "
            "and their injective six-trace assignments; endpoint position masks, "
            "shared labels, heights, oracle results, SAT and UNSAT remain uninstantiated"
        ),
        "status": "EXACT_OUTER_TRACE_PARTITION/36_SHARDS/INCIDENCE_AND_LABELS_PENDING/GLOBAL_INCOMPLETE",
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
