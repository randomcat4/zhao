#!/usr/bin/env python3
"""Exact instance counts for the extreme fringe on the three forced complements."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "unique_tail_remaining_six_f2_complements_report.json"
REPORT_PATH = HERE / "unique_tail_remaining_six_f2_extreme_fringe_report.json"
DEPENDENCY_PATHS = (
    HERE / "proofs" / "extreme_atom_fringe.md",
    HERE / "verifications" / "extreme_exchange_review.md",
    HERE / "proofs" / "unique_tail_remaining_six_f2_complements.md",
    HERE / "verifications" / "unique_tail_remaining_six_f2_complements_independent_review.md",
    INPUT_PATH,
)


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def build_report() -> dict[str, object]:
    source = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    forced = [
        row
        for row in source["remaining_nonempty_defect_assignments"]
        if row["forces_length_3p_minus_2_quotient_atom_complement"]
    ]
    assert len(forced) == 3
    threshold_pairs = [
        {
            "T_size": t_value,
            "first_truncation_bound": 8 - t_value,
            "complement_truncation_bound": t_value + 1,
        }
        for t_value in range(1, 6)
    ]
    assert [
        (row["first_truncation_bound"], row["complement_truncation_bound"])
        for row in threshold_pairs
    ] == [(7, 2), (6, 3), (5, 4), (4, 5), (3, 6)]

    rows = []
    for forced_row in forced:
        complement_length = 3 * forced_row["p"] - 2
        proper_nonempty_C_subsets = (1 << forced_row["induced_block_length"]) - 2
        assert proper_nonempty_C_subsets == 62
        rows.append(
            {
                "p": forced_row["p"],
                "packing_type": forced_row["packing_type"],
                "P_size": forced_row["atom_size"],
                "defect": forced_row["defect"],
                "C_length": forced_row["induced_block_length"],
                "B_length": complement_length,
                "proper_nonempty_C_subset_count": proper_nonempty_C_subsets,
                "truncated_identity_instances_per_actual_C": (
                    complement_length * proper_nonempty_C_subsets
                ),
                "full_signed_target_coefficients_per_deleted_B": (
                    forced_row["p"] ** 3
                ),
            }
        )
    assert [row["B_length"] for row in rows] == [697, 697, 4195]
    assert sum(
        row["truncated_identity_instances_per_actual_C"] for row in rows
    ) == 346_518

    report: dict[str, object] = {
        "schema": "unique_tail_remaining_six_f2_extreme_fringe_v1",
        "scope": {
            "assumptions": [
                "the three audited automatic six-item 2a blocks and their literal length-(3p-2) quotient-atom complements",
                "the audited extreme-atom group-algebra fringe identity",
            ],
            "conclusion": (
                "for every complement position z and every nonempty proper subset T of the corresponding actual six-item block C, the exact two-sided truncated signed representation identity holds; the deleted complement product equals the full group-sum element"
            ),
            "not_concluded": [
                "the signed representation sums are nonnegative counts",
                "any of the three packing assignments is realizable",
                "any remaining packing type is empty",
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
        "threshold_pairs": threshold_pairs,
        "forced_rows": rows,
        "summary": {
            "forced_row_count": len(rows),
            "proper_nonempty_C_subsets_per_row_and_z": 62,
            "truncated_identity_instances_across_one_actual_C_per_row": 346_518,
            "singleton_threshold_pair": [7, 2],
            "five_item_threshold_pair": [3, 6],
            "restored_information": [
                "every deleted long-complement position",
                "every nonempty proper subset of the literal six-item block",
                "all signed target coefficients of the deleted quotient atom",
                "two complementary constant-length representation fringes",
            ],
        },
        "status": "THREE_EXTREME_COMPLEMENTS_GAIN_FULL_SIGNED_FRINGE__GLOBAL_INCOMPLETE",
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
