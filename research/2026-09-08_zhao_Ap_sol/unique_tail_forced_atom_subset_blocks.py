#!/usr/bin/env python3
"""Exact certificate for all atom-subfamily short blocks in the forced types.

The input is the audited short-packing bound for the three forced common-R
types.  For every nonempty subfamily of the packed projection atoms, this
script builds the automatically induced positive-core quotient-zero block,
checks its true length window, and enumerates the possible a-axis defects.
It then applies the audited q-fibre capacity of every F3 long complement.
"""

from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_forced_atom_subset_blocks_report.json"
DEPENDENCY_PATHS = (
    HERE / "assumptions.md",
    HERE / "proofs" / "unique_tail_forced_short_packing_block.md",
    HERE / "verifications" / "unique_tail_forced_short_packing_block_independent_review.md",
    HERE / "proofs" / "unique_tail_position_conflict_frontier.md",
    HERE / "verifications" / "unique_tail_position_conflict_frontier_independent_review.md",
    HERE / "proofs" / "unique_tail_common_R_next.md",
)

SHORT_WINDOWS = {
    1: range(2, 7),
    2: range(4, 8),
    3: range(6, 9),
}

# These are exactly the ten size vectors in the audited short-packing report.
INPUT_ROWS = {
    (233, 4): {
        "(3)": ((3,), ((1,), (2,), (3,))),
        "(1,2)": ((1, 2), ((1, 1), (1, 2), (2, 1))),
        "(1,1,1)": ((1, 1, 1), ((1, 1, 1),)),
    },
    (1399, 5): {
        "(3)": ((3,), ((1,), (2,))),
        "(1,2)": ((1, 2), ((1, 1),)),
        "(1,1,1)": ((1, 1, 1), ()),
    },
}


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def nonempty_index_subsets(count: int) -> list[tuple[int, ...]]:
    return [
        subset
        for size in range(1, count + 1)
        for subset in combinations(range(count), size)
    ]


def allowed_actual_coefficients(length: int) -> list[int]:
    """The wrong positive-core F3 family is removed by unique-tail rigidity."""

    return [
        family
        for family, window in SHORT_WINDOWS.items()
        if length in window and family != 3
    ]


def enumerate_vector(
    p_value: int,
    b_value: int,
    coefficients: tuple[int, ...],
    sizes: tuple[int, ...],
) -> dict[str, object]:
    subsets = nonempty_index_subsets(len(coefficients))
    structural_rows = []
    for subset in subsets:
        d_sum = sum(coefficients[index] for index in subset)
        n_sum = sum(sizes[index] for index in subset)
        core_size = b_value - d_sum
        block_length = core_size + 3 + n_sum
        assert 1 <= core_size <= p_value - 4
        assert 2 <= block_length <= 8
        structural_rows.append(
            {
                "indices_one_based": [index + 1 for index in subset],
                "axis_coefficient_sum": d_sum,
                "atom_size_sum": n_sum,
                "X_core_size": core_size,
                "block_length": block_length,
                "allowed_actual_sum_coefficients_after_unique_F3_gate": (
                    allowed_actual_coefficients(block_length)
                ),
            }
        )

    surviving_defects = []
    for defects in product((1, 2), repeat=len(coefficients)):
        induced_rows = []
        valid = True
        for structural in structural_rows:
            subset = tuple(index - 1 for index in structural["indices_one_based"])
            defect_sum = sum(defects[index] for index in subset)
            actual_coefficient = (3 - defect_sum) % p_value
            allowed = structural[
                "allowed_actual_sum_coefficients_after_unique_F3_gate"
            ]
            if actual_coefficient not in allowed:
                valid = False
            induced_rows.append(
                {
                    **structural,
                    "defect_sum": defect_sum,
                    "actual_sum_coefficient_mod_p": actual_coefficient,
                    "passes_short_spectrum": actual_coefficient in allowed,
                }
            )
        if valid:
            surviving_defects.append(
                {
                    "atom_defects": list(defects),
                    "atom_actual_sums": [
                        f"{coefficient}x-{defect}a"
                        for coefficient, defect in zip(coefficients, defects)
                    ],
                    "induced_blocks": induced_rows,
                }
            )

    has_forced_q_singleton = any(
        coefficient == 1 and size == 1
        for coefficient, size in zip(coefficients, sizes)
    )
    fibre_gate_reason = None
    if surviving_defects and has_forced_q_singleton:
        fibre_gate_reason = (
            "a coefficient-one singleton has quotient label q, lies in R, "
            "and raises every endpoint F3-complement q-fibre from p-4 to p-3"
        )

    survives_fibre_gate = bool(surviving_defects) and not has_forced_q_singleton
    return {
        "atom_sizes": list(sizes),
        "structural_induced_blocks": structural_rows,
        "surviving_defect_assignments_after_all_subfamily_blocks": surviving_defects,
        "surviving_defect_assignment_count": len(surviving_defects),
        "has_forced_coefficient_one_singleton": has_forced_q_singleton,
        "fibre_gate_reason": fibre_gate_reason,
        "survives_long_complement_q_fibre_gate": survives_fibre_gate,
    }


def build_report() -> dict[str, object]:
    cases = []
    for (p_value, b_value), packing_types in INPUT_ROWS.items():
        packing_rows = []
        for name, (coefficients, size_vectors) in packing_types.items():
            vector_rows = [
                enumerate_vector(p_value, b_value, coefficients, sizes)
                for sizes in size_vectors
            ]
            packing_rows.append(
                {
                    "packing_type": name,
                    "axis_coefficients": list(coefficients),
                    "input_size_vector_count": len(size_vectors),
                    "vectors": vector_rows,
                    "surviving_size_vectors_after_subfamily_blocks": [
                        row["atom_sizes"]
                        for row in vector_rows
                        if row["surviving_defect_assignment_count"]
                    ],
                    "surviving_size_vectors_after_q_fibre_gate": [
                        row["atom_sizes"]
                        for row in vector_rows
                        if row["survives_long_complement_q_fibre_gate"]
                    ],
                }
            )
        cases.append(
            {
                "p": p_value,
                "b": b_value,
                "packing_rows": packing_rows,
            }
        )

    by_key = {
        (case["p"], row["packing_type"]): row
        for case in cases
        for row in case["packing_rows"]
    }
    assert by_key[(233, "(1,1,1)")][
        "surviving_size_vectors_after_subfamily_blocks"
    ] == []
    assert by_key[(1399, "(1,2)")][
        "surviving_size_vectors_after_subfamily_blocks"
    ] == []
    assert by_key[(233, "(1,2)")][
        "surviving_size_vectors_after_subfamily_blocks"
    ] == [[1, 1]]
    assert by_key[(233, "(1,2)")][
        "surviving_size_vectors_after_q_fibre_gate"
    ] == []
    for p_value in (233, 1399):
        assert by_key[(p_value, "(3)")][
            "surviving_size_vectors_after_q_fibre_gate"
        ] == ([[1], [2], [3]] if p_value == 233 else [[1], [2]])

    input_vectors = sum(
        row["input_size_vector_count"]
        for case in cases
        for row in case["packing_rows"]
    )
    subset_surviving_vectors = sum(
        len(row["surviving_size_vectors_after_subfamily_blocks"])
        for case in cases
        for row in case["packing_rows"]
    )
    final_vectors = sum(
        len(row["surviving_size_vectors_after_q_fibre_gate"])
        for case in cases
        for row in case["packing_rows"]
    )
    final_defect_assignments = sum(
        vector["surviving_defect_assignment_count"]
        for case in cases
        for row in case["packing_rows"]
        for vector in row["vectors"]
        if vector["survives_long_complement_q_fibre_gate"]
    )

    report: dict[str, object] = {
        "schema": "unique_tail_forced_atom_subset_blocks_v1",
        "scope": {
            "assumptions": [
                "p,b are (233,4) or (1399,5)",
                "the audited forced short-packing bound and its ten size vectors",
                "each P_i is a nonempty projected atom with total quotient-axis coefficient d_i",
                "X=x^(p-4), U has three positions and quotient sum -bq",
                "all quotient-zero blocks of length at most eight obey the frozen short spectrum",
                "the only positive-core F3 tail is U with core size b",
                "each endpoint F3 complement is a quotient atom with every fibre multiplicity at most p-4",
            ],
            "conclusion": (
                "the forced common-R packing types (1,2) and (1,1,1) are empty "
                "for p=233 and p=1399; only type (3) remains among the three forced types"
            ),
            "not_concluded": [
                "the forced packing type (3) is empty",
                "any of the four non-forced packing types is empty",
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
        "cases": cases,
        "summary": {
            "input_size_vectors": input_vectors,
            "size_vectors_after_all_atom_subfamily_short_blocks": subset_surviving_vectors,
            "size_vectors_after_long_complement_q_fibre_gate": final_vectors,
            "final_defect_assignments": final_defect_assignments,
            "closed_forced_packing_types": ["(1,2)", "(1,1,1)"],
            "remaining_forced_packing_type": "(3)",
            "remaining_size_vectors": {
                "233": [[1], [2], [3]],
                "1399": [[1], [2]],
            },
        },
        "status": "TWO_OF_THREE_FORCED_PACKING_TYPES_CLOSED__TYPE_3_REMAINS__GLOBAL_INCOMPLETE",
    }
    assert input_vectors == 10
    assert subset_surviving_vectors == 6
    assert final_vectors == 5
    assert final_defect_assignments == 8
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
