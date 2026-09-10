#!/usr/bin/env python3
"""Enumerate {7,8}-decorations of the 36 p=233 all-distinct trace shards.

The exact reduction removes precisely those outer decorations in which at
least two singleton-trace endpoints have length seven.  It does not instantiate
literal endpoint masks or labels and does not call any deeper CEGAR oracle.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_REPORT = HERE / "unique_tail_p233_type3_p2_trace_shards_report.json"
REPORT_PATH = HERE / "unique_tail_p233_length_decorated_trace_reduction_report.json"
SINGLETON_MASKS = frozenset((1, 2, 4))

DEPENDENCY_PATHS = (
    SOURCE_REPORT,
    HERE / "proofs" / "unique_tail_p233_singleton_tail_fringe.md",
    HERE / "verifications" / "unique_tail_p233_singleton_tail_fringe_independent_review.md",
    HERE / "proofs" / "unique_tail_property_b_two_max_mixed_exclusion.md",
    HERE / "unique_tail_property_b_two_max_mixed_exclusion.py",
    HERE / "unique_tail_property_b_two_max_mixed_exclusion_report.json",
    HERE / "proofs" / "unique_tail_property_b_three_domain_general.md",
    HERE / "unique_tail_property_b_three_domain_general.py",
    HERE / "unique_tail_property_b_three_domain_general_report.json",
    HERE / "verifications" / "unique_tail_property_b_three_domain_general_independent_review.md",
    HERE / "verifications" / "unique_tail_property_b_three_domain_general_independent_check.py",
    HERE / "verifications" / "unique_tail_property_b_three_domain_general_independent_report.json",
)


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def dependency_hashes() -> dict[str, str]:
    return {
        path.relative_to(HERE).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in DEPENDENCY_PATHS
    }


def load_source_shards() -> list[dict[str, object]]:
    source = json.loads(SOURCE_REPORT.read_text(encoding="utf-8"))
    claimed = source.pop("certificate_sha256")
    assert canonical_hash(source) == claimed
    assert source["status"].startswith("EXACT_OUTER_TRACE_PARTITION/36_SHARDS")
    shards = source["trace_shards"]
    assert isinstance(shards, list) and len(shards) == 36
    return shards


def build_report() -> dict[str, object]:
    shards = load_source_shards()
    all_rows: list[dict[str, object]] = []
    surviving_rows: list[dict[str, object]] = []
    eliminated_rows: list[dict[str, object]] = []

    for shard in shards:
        traces = tuple(int(value) for value in shard["endpoint_trace_masks"])
        singleton_vertices = tuple(i for i, trace in enumerate(traces) if trace in SINGLETON_MASKS)
        assert len(singleton_vertices) == 3
        for lengths in itertools.product((7, 8), repeat=len(traces)):
            singleton_lengths = tuple(lengths[i] for i in singleton_vertices)
            singleton_length_7_count = singleton_lengths.count(7)
            eliminated = singleton_length_7_count >= 2
            row = {
                "parent_shard_id": shard["shard_id"],
                "shape": shard["shape"],
                "vertex_count": shard["vertex_count"],
                "edges": shard["edges"],
                "endpoint_trace_masks": list(traces),
                "endpoint_lengths": list(lengths),
                "singleton_vertices": list(singleton_vertices),
                "singleton_length_pattern": list(singleton_lengths),
                "singleton_length_7_count": singleton_length_7_count,
                "non_singleton_length_7_count": sum(
                    length == 7 for i, length in enumerate(lengths) if i not in singleton_vertices
                ),
                "total_length_7_count": lengths.count(7),
                "decision": (
                    "ELIMINATED_AT_LEAST_TWO_SINGLETONS_LENGTH_7"
                    if eliminated
                    else "SURVIVES_THIS_OUTER_REDUCTION_ONLY"
                ),
            }
            all_rows.append(row)
            (eliminated_rows if eliminated else surviving_rows).append(row)

    for index, row in enumerate(all_rows, start=1):
        row["decorated_shard_id"] = f"decorated-{index:04d}"

    assert len(all_rows) == 1440
    assert len(eliminated_rows) == 720
    assert len(surviving_rows) == 720

    shape_counts: dict[str, dict[str, int]] = {}
    for shape in sorted({str(row["shape"]) for row in all_rows}):
        shape_all = [row for row in all_rows if row["shape"] == shape]
        shape_eliminated = [row for row in eliminated_rows if row["shape"] == shape]
        shape_counts[shape] = {
            "decorated_total": len(shape_all),
            "eliminated": len(shape_eliminated),
            "surviving": len(shape_all) - len(shape_eliminated),
        }
    assert shape_counts == {
        "P4_plus_K2": {"decorated_total": 768, "eliminated": 384, "surviving": 384},
        "P5": {"decorated_total": 192, "eliminated": 96, "surviving": 96},
        "T5": {"decorated_total": 384, "eliminated": 192, "surviving": 192},
        "paw": {"decorated_total": 96, "eliminated": 48, "surviving": 48},
    }

    singleton_seven_distribution = Counter(
        int(row["singleton_length_7_count"]) for row in surviving_rows
    )
    total_seven_distribution = Counter(int(row["total_length_7_count"]) for row in surviving_rows)
    assert singleton_seven_distribution == Counter({0: 180, 1: 540})
    assert total_seven_distribution == Counter({0: 36, 1: 186, 2: 288, 3: 174, 4: 36})

    all_eight_rows = [row for row in surviving_rows if row["total_length_7_count"] == 0]
    assert len(all_eight_rows) == 36
    assert {row["parent_shard_id"] for row in all_eight_rows} == {
        shard["shard_id"] for shard in shards
    }

    report: dict[str, object] = {
        "schema": "unique_tail_p233_length_decorated_trace_reduction_v1",
        "fixed_slice": {
            "p": 233,
            "packing_type": [3],
            "P_size": 2,
            "kappa": 1,
            "allowed_endpoint_lengths": [7, 8],
            "length_defect_formula": "delta_H=h+|P|-9=h-7",
        },
        "dependencies_sha256": dependency_hashes(),
        "counts": {
            "parent_trace_shards": len(shards),
            "all_length_decorated_shards": len(all_rows),
            "eliminated_at_least_two_singletons_length_7": len(eliminated_rows),
            "surviving_outer_shards": len(surviving_rows),
        },
        "counts_by_shape": shape_counts,
        "surviving_singleton_length_7_distribution": {
            str(key): singleton_seven_distribution[key] for key in sorted(singleton_seven_distribution)
        },
        "surviving_total_length_7_distribution": {
            str(key): total_seven_distribution[key] for key in sorted(total_seven_distribution)
        },
        "all_eight_witness": {
            "count": len(all_eight_rows),
            "one_for_every_parent_trace_shard": True,
            "decorated_shard_ids": [row["decorated_shard_id"] for row in all_eight_rows],
            "consequence": "The outer graph/trace incidence alone forces no length-seven endpoint, hence does not force two or three additional length-seven endpoints.",
        },
        "elimination_rule": {
            "condition": "at least two endpoints among trace masks 1,2,4 have length seven",
            "cases": {
                "exactly_two": (
                    "the two length-seven singleton complements are maximal atoms; together with the "
                    "length-eight singleton complement they share at least 452 literal positions and are "
                    "excluded by the Property-B two-max mixed theorem"
                ),
                "exactly_three": (
                    "the three length-seven singleton complements are maximal atoms, share at least "
                    "453 literal positions, and are excluded by the audited Property-B three-domain theorem"
                ),
            },
            "review_status": (
                "the three-domain dependency is independently audited CORRECT; the two-max mixed "
                "dependency remains pending fresh independent review"
            ),
        },
        "surviving_shards": surviving_rows,
        "scope": (
            "exact for the binary endpoint-length decoration of the 36 certified outer trace shards; "
            "literal endpoint masks, shared labels, rank in the mixed 7/8 cases, and all deeper CEGAR oracles remain uninstantiated"
        ),
        "status": "EXACT_OUTER_LENGTH_REDUCTION/PENDING_TWO_SINGLETON_PROPERTY_B_REVIEW/720_SURVIVORS/GLOBAL_INCOMPLETE",
        "not_claimed": [
            "any surviving outer shard has a label realization",
            "the mixed 7/8 slice is SAT or UNSAT",
            "the full p=233 problem is solved",
            "global A_p",
        ],
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
