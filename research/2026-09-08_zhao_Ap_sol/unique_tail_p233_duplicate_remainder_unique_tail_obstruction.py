#!/usr/bin/env python3
"""Duplicate-remainder separation oracle for the p=233 unique-tail slice.

The mathematical obstruction is label-semantic: equal endpoint sums plus
equal remainder sums force an outside petal to have the same actual label as a
tail position.  The executable oracle implements the strongest purely literal
incidence specialization, where the two remainders are the identical position
set.

The 720 upstream rows do not contain endpoint position masks.  Accordingly the
script reports candidate pair slots but deletes no abstract row.  It also
constructs, for every row, a private-petal literal mask skeleton satisfying the
currently instantiated trace/length/common-position/edge-incidence data and
avoiding the motif.  These skeletons are not label realizations.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_REPORT = HERE / "unique_tail_p233_length_decorated_trace_reduction_report.json"
REPORT_PATH = HERE / "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_report.json"
TAIL_BY_BIT = {1: "u_e", 2: "u_f", 4: "u_t"}
TAIL_POSITIONS = frozenset(TAIL_BY_BIT.values())


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
            "ascii"
        )
    ).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source_rows() -> tuple[dict[str, object], list[dict[str, object]]]:
    source = json.loads(SOURCE_REPORT.read_text(encoding="utf-8"))
    claimed = source.pop("certificate_sha256")
    assert canonical_hash(source) == claimed
    assert source["counts"]["surviving_outer_shards"] == 720  # type: ignore[index]
    rows = source["surviving_shards"]
    assert isinstance(rows, list) and len(rows) == 720
    return {
        "file_sha256": file_sha256(SOURCE_REPORT),
        "canonical_certificate": claimed,
    }, rows


def tail_set(trace_mask: int) -> frozenset[str]:
    assert 1 <= trace_mask <= 6
    return frozenset(name for bit, name in TAIL_BY_BIT.items() if trace_mask & bit)


def candidate_pair_slots(
    traces: list[int], lengths: list[int]
) -> list[dict[str, object]]:
    """Pairs on which an identical-remainder one-tail swap is possible."""
    answers: list[dict[str, object]] = []
    for left, right in itertools.combinations(range(len(traces)), 2):
        if lengths[left] != lengths[right]:
            continue
        left_trace = traces[left]
        right_trace = traces[right]
        if left_trace & right_trace == left_trace and left_trace ^ right_trace in TAIL_BY_BIT:
            small, large = left, right
        elif left_trace & right_trace == right_trace and left_trace ^ right_trace in TAIL_BY_BIT:
            small, large = right, left
        else:
            continue
        bit = traces[small] ^ traces[large]
        answers.append(
            {
                "small_trace_vertex": small,
                "large_trace_vertex": large,
                "small_trace_mask": traces[small],
                "large_trace_mask": traces[large],
                "swapped_tail_position": TAIL_BY_BIT[bit],
                "common_endpoint_length": lengths[small],
            }
        )
    return answers


def literal_duplicate_remainder_oracle(
    endpoint_masks: list[set[str]], traces: list[int], lengths: list[int]
) -> list[dict[str, object]]:
    """Reject a concrete incidence whenever one-tail duplicate remainders occur."""
    assert len(endpoint_masks) == len(traces) == len(lengths)
    for index, endpoint in enumerate(endpoint_masks):
        assert len(endpoint) == lengths[index]
        assert endpoint & TAIL_POSITIONS == tail_set(traces[index])

    motifs: list[dict[str, object]] = []
    for slot in candidate_pair_slots(traces, lengths):
        small = int(slot["small_trace_vertex"])
        large = int(slot["large_trace_vertex"])
        u = str(slot["swapped_tail_position"])
        small_only = endpoint_masks[small] - endpoint_masks[large]
        large_only = endpoint_masks[large] - endpoint_masks[small]
        if large_only != {u} or len(small_only) != 1:
            continue
        v = next(iter(small_only))
        assert v not in TAIL_POSITIONS
        small_remainder = endpoint_masks[small] - {v}
        large_remainder = endpoint_masks[large] - {u}
        assert small_remainder == large_remainder
        motifs.append(
            {
                **slot,
                "outside_replacement_position": v,
                "common_remainder": sorted(small_remainder),
                "forced_actual_label_equality": f"gamma({v})=gamma({u})",
                "forced_second_tail": sorted((TAIL_POSITIONS - {u}) | {v}),
                "decision": "REJECT_CONCRETE_INCIDENCE",
            }
        )
    return motifs


def model_n_fixture() -> dict[str, object]:
    common = {"y", "e_prime", "e_double_prime", "c"}
    endpoint_masks = [
        common | {"u_e", "x_f", "x_t"},
        common | {"u_e", "u_f", "x_t"},
        common | {"u_e", "u_t", "x_f"},
    ]
    traces = [1, 3, 5]
    lengths = [7, 7, 7]
    motifs = literal_duplicate_remainder_oracle(endpoint_masks, traces, lengths)
    assert len(motifs) == 2
    assert {
        (row["swapped_tail_position"], row["outside_replacement_position"])
        for row in motifs
    } == {("u_f", "x_f"), ("u_t", "x_t")}
    return {
        "endpoint_masks": [sorted(endpoint) for endpoint in endpoint_masks],
        "trace_masks": traces,
        "lengths": lengths,
        "oracle_motifs": motifs,
        "note": "either one of the two returned motifs already contradicts unique tail",
    }


def private_petal_skeleton(row: dict[str, object]) -> list[set[str]]:
    """A motif-free literal mask witness for the row's current outer data."""
    traces = [int(value) for value in row["endpoint_trace_masks"]]  # type: ignore[index]
    lengths = [int(value) for value in row["endpoint_lengths"]]  # type: ignore[index]
    row_id = str(row["decorated_shard_id"])
    endpoints: list[set[str]] = []
    for vertex, (trace, length) in enumerate(zip(traces, lengths)):
        endpoint = {"y"} | set(tail_set(trace))
        filler_count = length - len(endpoint)
        assert filler_count >= 4
        endpoint.update(
            f"{row_id}:v{vertex}:private:{index}" for index in range(1, filler_count + 1)
        )
        endpoints.append(endpoint)

    assert all(len(endpoint) == length for endpoint, length in zip(endpoints, lengths))
    assert all("y" in endpoint for endpoint in endpoints)
    for left, right in row["edges"]:  # type: ignore[index]
        left = int(left)
        right = int(right)
        assert not (traces[left] & traces[right])
        assert endpoints[left] & endpoints[right] == {"y"}
    assert not literal_duplicate_remainder_oracle(endpoints, traces, lengths)
    return endpoints


def scan_rows(rows: list[dict[str, object]]) -> dict[str, object]:
    pair_count_distribution: Counter[int] = Counter()
    shape_rows: defaultdict[str, Counter[str]] = defaultdict(Counter)
    candidate_rows: list[dict[str, object]] = []
    total_pair_slots = 0
    maximum_skeleton_universe = 0

    for row in rows:
        traces = [int(value) for value in row["endpoint_trace_masks"]]
        lengths = [int(value) for value in row["endpoint_lengths"]]
        slots = candidate_pair_slots(traces, lengths)
        pair_count = len(slots)
        total_pair_slots += pair_count
        pair_count_distribution[pair_count] += 1
        shape = str(row["shape"])
        shape_rows[shape]["rows"] += 1
        shape_rows[shape]["candidate_rows"] += bool(slots)
        shape_rows[shape]["candidate_pair_slots"] += pair_count
        if slots:
            candidate_rows.append(
                {
                    "decorated_shard_id": row["decorated_shard_id"],
                    "parent_shard_id": row["parent_shard_id"],
                    "shape": shape,
                    "candidate_pair_slots": slots,
                }
            )

        skeleton = private_petal_skeleton(row)
        universe = set().union(*skeleton) | set(TAIL_POSITIONS)
        maximum_skeleton_universe = max(maximum_skeleton_universe, len(universe))
        assert len(universe) <= 474

    assert pair_count_distribution == Counter({0: 42, 1: 96, 2: 300, 3: 72, 4: 198, 6: 12})
    assert len(candidate_rows) == 678
    assert total_pair_slots == 1776
    expected_shape = {
        "P4_plus_K2": {"rows": 384, "candidate_rows": 372, "candidate_pair_slots": 1152},
        "P5": {"rows": 96, "candidate_rows": 90, "candidate_pair_slots": 192},
        "T5": {"rows": 192, "candidate_rows": 180, "candidate_pair_slots": 384},
        "paw": {"rows": 48, "candidate_rows": 36, "candidate_pair_slots": 48},
    }
    normalized_shape = {
        shape: dict(counts) for shape, counts in sorted(shape_rows.items())
    }
    assert normalized_shape == expected_shape

    return {
        "abstract_survivor_rows_scanned": len(rows),
        "rows_with_at_least_one_literal_motif_candidate_pair": len(candidate_rows),
        "rows_with_no_candidate_pair": pair_count_distribution[0],
        "candidate_pair_slots": total_pair_slots,
        "candidate_pair_count_distribution": {
            str(key): pair_count_distribution[key] for key in sorted(pair_count_distribution)
        },
        "by_shape": normalized_shape,
        "candidate_rows": candidate_rows,
        "literal_motif_hits_without_position_masks": 0,
        "abstract_rows_deleted": 0,
        "motif_free_private_petal_skeletons_constructed": len(rows),
        "maximum_positions_used_by_one_skeleton": maximum_skeleton_universe,
        "skeleton_scope": (
            "literal endpoint masks satisfying the stored lengths and tail traces, a common "
            "non-tail position y, and edge intersections exactly {y}; quotient labels, endpoint "
            "sums, Q atoms, short blocks, and actual Z atomicity are not supplied"
        ),
    }


def build_report() -> dict[str, object]:
    source, rows = load_source_rows()
    scan = scan_rows(rows)
    report: dict[str, object] = {
        "schema": "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_v1",
        "p": 233,
        "source_length_decoration_report": source,
        "theorem": {
            "semantic_hypotheses": [
                "U is the unique literal tail of the prescribed positive-core F3 block X_4 union U",
                "u is a literal position in U and v is a literal position in Y minus U, hence outside the selected X_4 union U",
                "H_u=R_u union {u} and H_v=R_v union {v} are endpoint blocks with equal actual sums",
                "the two remainder actual sums satisfy sigma(R_u)=sigma(R_v)",
            ],
            "conclusion": (
                "gamma(u)=gamma(v), so (U minus {u}) union {v} is a distinct literal tail "
                "with the same actual sum as U, contradicting uniqueness"
            ),
            "literal_incidence_specialization": (
                "R_u=R_v as literal position sets; this is the implemented separation oracle"
            ),
            "sufficient_not_necessary": True,
        },
        "fixed_model_N_fixture": model_n_fixture(),
        "length_decorated_scan": scan,
        "quantifier_boundary": {
            "concrete_incidence": (
                "every future position-mask realization hit by the oracle is rigorously rejected"
            ),
            "current_720_rows": (
                "the rows contain only graph, trace, and length data, so candidate slots are not hits"
            ),
            "deletion_count_now": 0,
            "not_claimed": [
                "that any of the 678 candidate-bearing rows is itself eliminated",
                "that the literal duplicate-remainder motif is a necessary obstruction",
                "that the 720 private-petal mask skeletons admit compatible labels",
                "a complete enumeration of semantic equal-remainder-sum motifs",
            ],
        },
        "status": (
            "PROVED_SUFFICIENT_DUPLICATE_REMAINDER_OBSTRUCTION/"
            "PARAMETERIZED_INCIDENCE_ORACLE/0_OF_720_ABSTRACT_ROWS_DELETED/"
            "REAL_POSITION_MASKS_PENDING/GLOBAL_INCOMPLETE"
        ),
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    report = build_report()
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    scan = report["length_decorated_scan"]
    print("PASS fixed Model N fixture yields two literal duplicate-remainder motifs")
    print(
        "PASS 720 rows scanned:",
        scan["rows_with_at_least_one_literal_motif_candidate_pair"],
        "candidate-bearing rows and",
        scan["candidate_pair_slots"],
        "candidate pair slots",
    )
    print("PASS motif-free private-petal incidence skeleton built for every abstract row")
    print("ABSTRACT ROWS DELETED 0 (endpoint position masks are not instantiated)")
    print("CERTIFICATE", report["certificate_sha256"])


if __name__ == "__main__":
    main()
