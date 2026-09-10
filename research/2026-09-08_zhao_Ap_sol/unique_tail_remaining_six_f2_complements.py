#!/usr/bin/env python3
"""Exact certificate for six-item F2 blocks in the remaining packing rows."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "unique_tail_all_packing_short_blocks_report.json"
REPORT_PATH = HERE / "unique_tail_remaining_six_f2_complements_report.json"
DEPENDENCY_PATHS = (
    HERE / "assumptions.md",
    HERE / "proofs" / "middle_quotient_gap.md",
    HERE / "proofs" / "unique_tail_position_conflict_frontier.md",
    HERE / "verifications" / "unique_tail_position_conflict_frontier_independent_review.md",
    HERE / "proofs" / "unique_tail_all_packing_short_blocks.md",
    HERE / "verifications" / "unique_tail_all_packing_short_blocks_independent_review.md",
    INPUT_PATH,
)


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def remaining_assignments() -> list[dict[str, object]]:
    source = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    for case in source["cases"]:
        p_value = case["p"]
        b_value = case["b"]
        for packing in case["packing_rows"]:
            if packing["packing_type"] not in ("(2)", "(3)"):
                continue
            coefficient = packing["axis_coefficients"][0]
            assert len(packing["axis_coefficients"]) == 1
            for vector in packing["vectors"]:
                if not vector["survives_q_fibre_gate"]:
                    continue
                assert len(vector["atom_sizes"]) == 1
                assert len(vector["induced_blocks"]) == 1
                atom_size = vector["atom_sizes"][0]
                block = vector["induced_blocks"][0]
                for defect in vector["surviving_defect_assignments"]:
                    assert len(defect) == 1
                    actual_sum_coefficient = 3 - defect[0]
                    assert actual_sum_coefficient in block[
                        "allowed_actual_sum_coefficients"
                    ]
                    length = b_value - coefficient + 3 + atom_size
                    assert length == block["length"]
                    forces_extreme_complement_atom = (
                        length == 6 and actual_sum_coefficient == 2
                    )
                    rows.append(
                        {
                            "p": p_value,
                            "b": b_value,
                            "packing_type": packing["packing_type"],
                            "axis_coefficient": coefficient,
                            "atom_size": atom_size,
                            "defect": defect[0],
                            "actual_sum_coefficient": actual_sum_coefficient,
                            "induced_block_length": length,
                            "positive_X_core_size": b_value - coefficient,
                            "tail_strictly_contains_U": True,
                            "forces_length_3p_minus_2_quotient_atom_complement": (
                                forces_extreme_complement_atom
                            ),
                            "internal_proper_quotient_zero_subset_forbidden": (
                                forces_extreme_complement_atom
                            ),
                        }
                    )
    return rows


def build_report() -> dict[str, object]:
    rows = remaining_assignments()
    forced = [
        row
        for row in rows
        if row["forces_length_3p_minus_2_quotient_atom_complement"]
    ]
    forced_keys = [
        (
            row["p"],
            row["packing_type"],
            row["atom_size"],
            row["defect"],
        )
        for row in forced
    ]
    assert len(rows) == 12
    assert forced_keys == [
        (233, "(2)", 1, 1),
        (233, "(3)", 2, 1),
        (1399, "(3)", 1, 1),
    ]
    assert all(row["positive_X_core_size"] > 0 for row in forced)
    assert all(row["tail_strictly_contains_U"] for row in forced)

    report: dict[str, object] = {
        "schema": "unique_tail_remaining_six_f2_complements_v1",
        "scope": {
            "assumptions": [
                "p,b are (233,4) or (1399,5)",
                "only the already-certified remaining packing types empty, (2), and (3) are considered",
                "for a nonempty packing P is a genuine position block disjoint from the unique tail U",
                "all quotient-zero proper subblocks obey the frozen middle gap and short positive-sum windows",
                "the complement of every F3 block is a quotient atom",
                "every positive-core F3 block has the unique tail U",
            ],
            "conclusion": (
                "exactly three of the twelve remaining nonempty defect assignments contain an automatic six-item 2a block; in each, its length-(3p-2) complement is a quotient atom and hence has no nonempty proper quotient-zero internal subset"
            ),
            "not_concluded": [
                "any of the three assignments is realizable",
                "the other nine assignments are realizable",
                "the empty packing is realizable",
                "the unique-tail branch is empty",
                "A_p",
            ],
        },
        "dependencies_sha256": {
            str(path.relative_to(HERE)).replace("\\", "/"): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in DEPENDENCY_PATHS
        },
        "remaining_nonempty_defect_assignments": rows,
        "summary": {
            "remaining_nonempty_defect_assignment_count": len(rows),
            "automatic_six_item_2a_block_count": len(forced),
            "forced_extreme_complement_atom_rows": forced_keys,
            "forced_complement_lengths": {
                str(row["p"]): 3 * row["p"] - 2 for row in forced
            },
            "restored_information": [
                "actual position block C=X_(b-d) disjoint_union U disjoint_union P",
                "the automatically induced short block C",
                "one unified quotient labelling for C and its literal complement B",
                "all internal subset sums of B through quotient atomicity",
            ],
        },
        "status": "THREE_EXTREME_COMPLEMENT_ATOM_ROWS_FORCED__GLOBAL_INCOMPLETE",
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
