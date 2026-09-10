#!/usr/bin/env python3
"""Exact coefficient certificate for every remaining zero-core long complement."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "unique_tail_all_packing_short_blocks_report.json"
REPORT_PATH = HERE / "unique_tail_remaining_long_complement_internal_sums_report.json"
DEPENDENCY_PATHS = (
    HERE / "proofs" / "unique_tail_labelled_position_next.md",
    HERE / "verifications" / "unique_tail_labelled_position_next_independent_review.md",
    HERE / "proofs" / "unique_tail_common_R_next.md",
    HERE / "verifications" / "unique_tail_common_R_next_independent_review.md",
    HERE / "proofs" / "unique_tail_all_packing_short_blocks.md",
    HERE / "verifications" / "unique_tail_all_packing_short_blocks_independent_review.md",
    INPUT_PATH,
)
ALLOWED = (1, 2, 3)


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def complement_orbit_representatives(size: int) -> list[list[int]]:
    full = (1 << size) - 1
    representatives = []
    for mask in range(1, full):
        complement = full ^ mask
        if mask < complement:
            representatives.append(
                [index + 1 for index in range(size) if mask & (1 << index)]
            )
    assert len(representatives) == (0 if size == 0 else (1 << (size - 1)) - 1)
    return representatives


def remaining_size_rows() -> list[dict[str, object]]:
    source = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    for case in source["cases"]:
        for packing in case["packing_rows"]:
            if packing["packing_type"] not in ("(2)", "(3)"):
                continue
            coefficient = packing["axis_coefficients"][0]
            assert coefficient in (2, 3)
            for vector in packing["vectors"]:
                if not vector["survives_q_fibre_gate"]:
                    continue
                assert len(vector["atom_sizes"]) == 1
                atom_size = vector["atom_sizes"][0]
                proper_q_zero_coefficients = [
                    c_value
                    for c_value in ALLOWED
                    if (c_value + coefficient) % case["p"] in ALLOWED
                ]
                representatives = complement_orbit_representatives(atom_size)
                rows.append(
                    {
                        "p": case["p"],
                        "b": case["b"],
                        "packing_type": packing["packing_type"],
                        "P_axis_coefficient": coefficient,
                        "P_size": atom_size,
                        "Q_H_axis_coefficient": 4 - coefficient,
                        "proper_rho_zero_Q_H_subset_allowed_axis_coefficients": (
                            proper_q_zero_coefficients
                        ),
                        "Q_H_forced_rho_atom": not proper_q_zero_coefficients,
                        "proper_rho_zero_Q_H_subsets_are_atoms": (
                            proper_q_zero_coefficients == [1]
                        ),
                        "proper_rho_zero_Q_H_subsets_have_size_at_least_two": (
                            proper_q_zero_coefficients == [1]
                        ),
                        "independent_mixed_target_fibre_representatives": (
                            representatives
                        ),
                        "independent_mixed_target_fibre_count": len(representatives),
                    }
                )
    return rows


def build_report() -> dict[str, object]:
    rows = remaining_size_rows()
    assert len(rows) == 8
    assert sum(row["Q_H_forced_rho_atom"] for row in rows) == 5
    assert sum(
        row["proper_rho_zero_Q_H_subsets_are_atoms"] for row in rows
    ) == 3
    assert {
        row["P_axis_coefficient"]: row[
            "proper_rho_zero_Q_H_subset_allowed_axis_coefficients"
        ]
        for row in rows
    } == {2: [1], 3: []}
    counts_by_size = {
        size: sorted(
            {
                row["independent_mixed_target_fibre_count"]
                for row in rows
                if row["P_size"] == size
            }
        )
        for size in (1, 2, 3)
    }
    assert counts_by_size == {1: [0], 2: [1], 3: [3]}

    report: dict[str, object] = {
        "schema": "unique_tail_remaining_long_complement_internal_sums_v1",
        "scope": {
            "assumptions": [
                "p,b are (233,4) or (1399,5)",
                "a common maximal packing leaves only one rho-atom P of q-axis coefficient d=2 or d=3, plus the rho-zero-sum-free kernel K",
                "for every actual zero-core endpoint H, W_H=P disjoint_union Q_H and q^(p-4) W_H is a quotient atom",
                "the complete axial subset-sum criterion is used for every literal subset of W_H",
                "every nonzero quotient fibre in an F3 complement has multiplicity at most p-4",
            ],
            "conclusion": (
                "for d=3 every Q_H is a rho-atom; for d=2 every nonempty proper rho-zero subset of Q_H has q-axis coefficient one, is itself a rho-atom, has an atomic complement, and neither factor is a singleton; together with the listed mixed target fibres this is equivalent to the full long-complement internal subset-sum criterion"
            ),
            "not_concluded": [
                "any remaining row is realizable",
                "the empty packing is realizable",
                "the mixed target fibres are nonempty",
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
        "remaining_nonempty_size_rows": rows,
        "summary": {
            "remaining_nonempty_size_row_count": len(rows),
            "type_3_Q_H_atom_rows": 5,
            "type_2_Q_H_coefficient_one_atomic_split_rows": 3,
            "independent_mixed_target_fibre_counts_by_P_size": counts_by_size,
            "type_3_P_size_one_boundary": (
                "the full long-complement criterion is exactly Q_H rho-atomicity"
            ),
            "restored_information": [
                "literal subsets of the common position atom P",
                "literal subsets of every endpoint remainder Q_H",
                "their unified q-axis coefficients",
                "every mixed target fibre rho(T)=-rho(A)",
                "the complete internal subset-sum criterion of q^(p-4)(P disjoint_union Q_H)",
            ],
        },
        "status": "ALL_REMAINING_NONEMPTY_LONG_COMPLEMENT_INTERNAL_SUMS_COMPRESSED__GLOBAL_INCOMPLETE",
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
