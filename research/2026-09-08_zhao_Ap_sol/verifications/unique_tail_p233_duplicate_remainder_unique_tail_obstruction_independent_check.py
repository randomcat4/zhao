#!/usr/bin/env python3
"""Fresh no-import audit of the duplicate-remainder obstruction.

This verifier never imports or executes the author program.  It reads the
frozen JSON inputs, verifies their hashes and canonical certificates, and
independently reconstructs the theorem regressions, Model N motifs, all 720
candidate-slot counts, and 720 motif-free private-petal mask witnesses.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path


VERIFICATION_DIR = Path(__file__).resolve().parent
ROOT = VERIFICATION_DIR.parent
SOURCE_PATH = ROOT / "unique_tail_p233_length_decorated_trace_reduction_report.json"
AUTHOR_PROOF = ROOT / "proofs" / "unique_tail_p233_duplicate_remainder_unique_tail_obstruction.md"
AUTHOR_SCRIPT = ROOT / "unique_tail_p233_duplicate_remainder_unique_tail_obstruction.py"
AUTHOR_REPORT = ROOT / "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_report.json"
REPORT_PATH = VERIFICATION_DIR / "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_independent_report.json"

EXPECTED_SHA256 = {
    "proofs/unique_tail_p233_duplicate_remainder_unique_tail_obstruction.md": (
        "10c0277cbbabff192123183292cd7f1dc2c3a6825759d116361f8c851db1714c"
    ),
    "unique_tail_p233_duplicate_remainder_unique_tail_obstruction.py": (
        "b113cb6fc380b46bbefc64fed264b3176c4a4a7f45fe6acd0e4053f2ae86cce6"
    ),
    "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_report.json": (
        "ae5089e75a8f8ed7eb4de43f9fd7cac3e031286d1be9dc16618a99bbe7844a37"
    ),
    "unique_tail_p233_length_decorated_trace_reduction_report.json": (
        "3c2f2c0405842b75c47fbf7fcedf09f0ef5275e9fe2a0339e1e9e71d47e4df47"
    ),
}

TAIL_BY_BIT = {1: "u_e", 2: "u_f", 4: "u_t"}
TAIL = frozenset(TAIL_BY_BIT.values())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
            "ascii"
        )
    ).hexdigest()


def verify_frozen_files() -> dict[str, str]:
    paths = {
        "proofs/unique_tail_p233_duplicate_remainder_unique_tail_obstruction.md": AUTHOR_PROOF,
        "unique_tail_p233_duplicate_remainder_unique_tail_obstruction.py": AUTHOR_SCRIPT,
        "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_report.json": AUTHOR_REPORT,
        "unique_tail_p233_length_decorated_trace_reduction_report.json": SOURCE_PATH,
    }
    actual = {name: file_sha256(path) for name, path in paths.items()}
    assert actual == EXPECTED_SHA256
    return actual


def load_certified_json(path: Path) -> tuple[dict[str, object], str]:
    value = json.loads(path.read_text(encoding="utf-8"))
    claimed = value.pop("certificate_sha256")
    assert isinstance(claimed, str)
    assert canonical_hash(value) == claimed
    value["certificate_sha256"] = claimed
    return value, claimed


def tail_set(mask: int) -> frozenset[str]:
    assert 1 <= mask <= 6
    return frozenset(name for bit, name in TAIL_BY_BIT.items() if mask & bit)


def independent_candidate_slots(
    traces: list[int], lengths: list[int]
) -> list[dict[str, object]]:
    """Set-theoretic reconstruction, independent of the author implementation."""

    slots: list[dict[str, object]] = []
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
        swapped = next(iter(tail_set(traces[large]) - tail_set(traces[small])))
        slots.append(
            {
                "small_trace_vertex": small,
                "large_trace_vertex": large,
                "small_trace_mask": traces[small],
                "large_trace_mask": traces[large],
                "swapped_tail_position": swapped,
                "common_endpoint_length": lengths[small],
            }
        )
    return slots


def independent_literal_oracle(
    endpoints: list[set[str]], traces: list[int], lengths: list[int]
) -> list[dict[str, object]]:
    assert len(endpoints) == len(traces) == len(lengths)
    for endpoint, trace, length in zip(endpoints, traces, lengths):
        assert len(endpoint) == length
        assert endpoint & TAIL == tail_set(trace)

    motifs: list[dict[str, object]] = []
    for slot in independent_candidate_slots(traces, lengths):
        small = int(slot["small_trace_vertex"])
        large = int(slot["large_trace_vertex"])
        u = str(slot["swapped_tail_position"])
        small_only = endpoints[small] - endpoints[large]
        large_only = endpoints[large] - endpoints[small]
        if len(small_only) != 1 or large_only != {u}:
            continue
        v = next(iter(small_only))
        assert v not in TAIL
        small_remainder = endpoints[small] - {v}
        large_remainder = endpoints[large] - {u}
        assert small_remainder == large_remainder
        motifs.append(
            {
                **slot,
                "outside_replacement_position": v,
                "common_remainder": sorted(small_remainder),
                "forced_actual_label_equality": f"gamma({v})=gamma({u})",
                "forced_second_tail": sorted((TAIL - {u}) | {v}),
                "decision": "REJECT_CONCRETE_INCIDENCE",
            }
        )
    return motifs


def cancellation_regression() -> int:
    """Finite cyclic regression for the cancellation step; the proof is algebraic."""

    checked = 0
    for modulus in range(2, 20):
        for remainder_sum in range(modulus):
            for u_value in range(modulus):
                for v_value in range(modulus):
                    if (remainder_sum + u_value) % modulus != (
                        remainder_sum + v_value
                    ) % modulus:
                        continue
                    assert u_value == v_value
                    checked += 1
    return checked


def audit_model_n(author_report: dict[str, object]) -> dict[str, object]:
    common = {"y", "e_prime", "e_double_prime", "c"}
    endpoints = [
        common | {"u_e", "x_f", "x_t"},
        common | {"u_e", "u_f", "x_t"},
        common | {"u_e", "u_t", "x_f"},
    ]
    traces = [1, 3, 5]
    lengths = [7, 7, 7]
    motifs = independent_literal_oracle(endpoints, traces, lengths)
    assert len(motifs) == 2
    assert {
        (row["swapped_tail_position"], row["outside_replacement_position"])
        for row in motifs
    } == {("u_f", "x_f"), ("u_t", "x_t")}
    fixture = author_report["fixed_model_N_fixture"]
    assert fixture["endpoint_masks"] == [sorted(endpoint) for endpoint in endpoints]
    assert fixture["trace_masks"] == traces
    assert fixture["lengths"] == lengths
    assert fixture["oracle_motifs"] == motifs
    return {
        "endpoint_count": 3,
        "candidate_pair_count": 2,
        "literal_motif_count": 2,
        "motifs": motifs,
        "decision": "PASS",
    }


def private_petal_masks(row: dict[str, object]) -> list[set[str]]:
    traces = [int(value) for value in row["endpoint_trace_masks"]]
    lengths = [int(value) for value in row["endpoint_lengths"]]
    row_id = str(row["decorated_shard_id"])
    endpoints: list[set[str]] = []
    for vertex, (trace, length) in enumerate(zip(traces, lengths)):
        endpoint = {"audit_common_y"} | set(tail_set(trace))
        needed = length - len(endpoint)
        assert needed >= 4
        endpoint.update(
            f"audit:{row_id}:vertex:{vertex}:petal:{index}"
            for index in range(needed)
        )
        endpoints.append(endpoint)
    return endpoints


def audit_720_rows(source: dict[str, object], author_report: dict[str, object]):
    rows = source["surviving_shards"]
    assert isinstance(rows, list) and len(rows) == 720
    assert source["counts"]["surviving_outer_shards"] == 720

    distribution: Counter[int] = Counter()
    by_shape: defaultdict[str, Counter[str]] = defaultdict(Counter)
    candidate_rows: list[dict[str, object]] = []
    total_slots = 0
    motif_free_rows = 0
    maximum_universe = 0
    minimum_candidate_side_difference = 10**9

    for row in rows:
        traces = [int(value) for value in row["endpoint_trace_masks"]]
        lengths = [int(value) for value in row["endpoint_lengths"]]
        slots = independent_candidate_slots(traces, lengths)
        slot_count = len(slots)
        distribution[slot_count] += 1
        total_slots += slot_count
        shape = str(row["shape"])
        by_shape[shape]["rows"] += 1
        by_shape[shape]["candidate_rows"] += int(bool(slots))
        by_shape[shape]["candidate_pair_slots"] += slot_count
        if slots:
            candidate_rows.append(
                {
                    "decorated_shard_id": row["decorated_shard_id"],
                    "parent_shard_id": row["parent_shard_id"],
                    "shape": shape,
                    "candidate_pair_slots": slots,
                }
            )

        endpoints = private_petal_masks(row)
        assert all(
            len(endpoint) == length
            and endpoint & TAIL == tail_set(trace)
            and "audit_common_y" in endpoint
            for endpoint, trace, length in zip(endpoints, traces, lengths)
        )
        for left, right in row["edges"]:
            left = int(left)
            right = int(right)
            assert tail_set(traces[left]).isdisjoint(tail_set(traces[right]))
            assert endpoints[left] & endpoints[right] == {"audit_common_y"}

        motifs = independent_literal_oracle(endpoints, traces, lengths)
        assert not motifs
        motif_free_rows += 1
        universe = set().union(*endpoints) | set(TAIL)
        maximum_universe = max(maximum_universe, len(universe))
        assert len(universe) <= 474

        for slot in slots:
            small = int(slot["small_trace_vertex"])
            large = int(slot["large_trace_vertex"])
            minimum_candidate_side_difference = min(
                minimum_candidate_side_difference,
                len(endpoints[small] - endpoints[large]),
                len(endpoints[large] - endpoints[small]),
            )

    expected_distribution = Counter({0: 42, 1: 96, 2: 300, 3: 72, 4: 198, 6: 12})
    expected_by_shape = {
        "P4_plus_K2": {"rows": 384, "candidate_rows": 372, "candidate_pair_slots": 1152},
        "P5": {"rows": 96, "candidate_rows": 90, "candidate_pair_slots": 192},
        "T5": {"rows": 192, "candidate_rows": 180, "candidate_pair_slots": 384},
        "paw": {"rows": 48, "candidate_rows": 36, "candidate_pair_slots": 48},
    }
    normalized_by_shape = {shape: dict(counts) for shape, counts in sorted(by_shape.items())}
    assert distribution == expected_distribution
    assert normalized_by_shape == expected_by_shape
    assert len(candidate_rows) == 678
    assert total_slots == 1776
    assert motif_free_rows == 720
    assert maximum_universe == 37
    assert minimum_candidate_side_difference >= 5

    author_scan = author_report["length_decorated_scan"]
    assert author_scan["candidate_pair_count_distribution"] == {
        str(key): distribution[key] for key in sorted(distribution)
    }
    assert author_scan["by_shape"] == normalized_by_shape
    assert author_scan["candidate_rows"] == candidate_rows
    assert author_scan["candidate_pair_slots"] == total_slots
    assert author_scan["rows_with_at_least_one_literal_motif_candidate_pair"] == 678
    assert author_scan["rows_with_no_candidate_pair"] == 42
    assert author_scan["motif_free_private_petal_skeletons_constructed"] == 720
    assert author_scan["maximum_positions_used_by_one_skeleton"] == 37
    assert author_scan["literal_motif_hits_without_position_masks"] == 0
    assert author_scan["abstract_rows_deleted"] == 0

    return {
        "rows_scanned": 720,
        "candidate_rows": 678,
        "candidate_pair_slots": 1776,
        "pair_count_distribution": {
            str(key): distribution[key] for key in sorted(distribution)
        },
        "by_shape": normalized_by_shape,
        "motif_free_private_petal_masks": motif_free_rows,
        "maximum_positions_in_one_mask_universe": maximum_universe,
        "minimum_symmetric_difference_side_over_candidate_pairs": (
            minimum_candidate_side_difference
        ),
        "abstract_rows_deleted_by_literal_motif": 0,
        "decision": "PASS",
    }


def build_report() -> dict[str, object]:
    frozen_hashes = verify_frozen_files()
    source, source_certificate = load_certified_json(SOURCE_PATH)
    author_report, author_certificate = load_certified_json(AUTHOR_REPORT)
    assert source_certificate == "37a86e2606fe21329a1cfb663d70528420648b042817600ecf0e62e18a548c02"
    assert author_certificate == "fa9707c2dd84d484bb7dd23d91f05262d1b687660e92bb70f2aa6b8a5b86c4b9"
    assert author_report["source_length_decoration_report"] == {
        "file_sha256": frozen_hashes[
            "unique_tail_p233_length_decorated_trace_reduction_report.json"
        ],
        "canonical_certificate": source_certificate,
    }

    model_n = audit_model_n(author_report)
    row_audit = audit_720_rows(source, author_report)
    cancellation_checks = cancellation_regression()
    assert any(
        "Y minus U" in hypothesis
        for hypothesis in author_report["theorem"]["semantic_hypotheses"]
    )
    assert author_report["quantifier_boundary"]["deletion_count_now"] == 0
    assert "0_OF_720_ABSTRACT_ROWS_DELETED" in author_report["status"]

    report: dict[str, object] = {
        "schema": "unique_tail_p233_duplicate_remainder_unique_tail_obstruction_independent_audit_v1",
        "status": "CORRECT/NO_IMPORT/0_OF_720_DELETED_CONFIRMED",
        "frozen_sha256": frozen_hashes,
        "canonical_certificates": {
            "source_length_decoration_report": source_certificate,
            "author_obstruction_report": author_certificate,
        },
        "no_import_attestation": (
            "the author Python file was hashed and read as a frozen artifact but was never imported or executed"
        ),
        "general_lemma_audit": {
            "decision": "CORRECT",
            "group_argument": (
                "from sigma(R_u)+gamma(u)=sigma(R_v)+gamma(v) and sigma(R_u)=sigma(R_v), "
                "group cancellation gives gamma(u)=gamma(v); replacing u by the distinct Y-position v "
                "preserves cardinality and actual sum of the tail"
            ),
            "ambient_scope_note": (
                "the final author theorem now explicitly requires v in Y minus U, hence outside the "
                "chosen X_4 core; the second-tail cardinality step is fully typed"
            ),
            "finite_cyclic_cancellation_regression_count": cancellation_checks,
            "sufficient_not_necessary": True,
        },
        "model_N_audit": model_n,
        "outer_720_row_audit": row_audit,
        "strict_deletion_verdict": {
            "deleted_rows": 0,
            "reason": (
                "candidate trace/length slots do not instantiate literal endpoint masks, while each of the 720 "
                "stored outer rows has an explicit common-y/private-petal mask refinement satisfying every stored "
                "trace, length, and edge-intersection condition and avoiding the literal motif"
            ),
            "candidate_slots_do_not_imply_real_motifs": True,
            "private_petal_masks_are_not_label_realisations": True,
        },
        "not_certified": [
            "that any motif-free private-petal mask admits compatible quotient or actual labels",
            "that the 42 rows without a literal candidate slot avoid semantic equal-remainder-sum motifs",
            "that the duplicate-remainder obstruction is necessary",
            "any elimination beyond a future concrete endpoint-mask incidence hit",
            "the fixed p=233 slice or global A_p",
        ],
        "conclusion": (
            "The proof, executable counts, Model N fixture, and zero-deletion boundary are correct in their stated "
            "scope.  The 1,776 slots are scheduling metadata only and cannot be promoted to 678 real motif hits."
        ),
    }
    report["certificate_sha256"] = canonical_hash(report)
    return report


def main() -> None:
    report = build_report()
    with REPORT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    outer = report["outer_720_row_audit"]
    print("PASS no-import frozen hashes and canonical certificates")
    print("PASS general equal-remainder lemma and two Model N motifs")
    print(
        "PASS 720 rows:",
        outer["candidate_pair_slots"],
        "candidate slots; distribution",
        outer["pair_count_distribution"],
    )
    print("PASS all 720 common-y/private-petal masks are literal-motif-free")
    print("CONFIRMED strict abstract-row deletion count = 0")
    print("CERTIFICATE", report["certificate_sha256"])


if __name__ == "__main__":
    main()
