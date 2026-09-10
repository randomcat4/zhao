#!/usr/bin/env python3
"""Exact certificate for complementary and subfamily blocks in all seven types."""

from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_all_packing_short_blocks_report.json"
DEPENDENCY_PATHS = (
    HERE / "assumptions.md",
    HERE / "proofs" / "middle_quotient_gap.md",
    HERE / "proofs" / "unique_tail_common_R_next.md",
    HERE / "verifications" / "unique_tail_common_R_next_independent_review.md",
    HERE / "proofs" / "unique_tail_position_conflict_frontier.md",
    HERE / "verifications" / "unique_tail_position_conflict_frontier_independent_review.md",
)

CASES = ((233, 4), (1399, 5))
PACKING_TYPES = (
    ("empty", ()),
    ("(1)", (1,)),
    ("(2)", (2,)),
    ("(3)", (3,)),
    ("(1,1)", (1, 1)),
    ("(1,2)", (1, 2)),
    ("(1,1,1)", (1, 1, 1)),
)
SHORT_WINDOWS = {
    1: range(2, 7),
    2: range(4, 8),
    3: range(6, 9),
}


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def canonical_vectors(coefficients: tuple[int, ...], cap: int) -> list[tuple[int, ...]]:
    if not coefficients:
        return [()]
    rows = []
    for sizes in product(range(1, max(cap, 0) + 1), repeat=len(coefficients)):
        if sum(sizes) > cap:
            continue
        if any(
            coefficients[index] == coefficients[index + 1]
            and sizes[index] > sizes[index + 1]
            for index in range(len(coefficients) - 1)
        ):
            continue
        rows.append(sizes)
    return rows


def nonempty_subsets(count: int) -> list[tuple[int, ...]]:
    return [
        subset
        for size in range(1, count + 1)
        for subset in combinations(range(count), size)
    ]


def allowed_non_f3_coefficients(length: int) -> tuple[int, ...]:
    return tuple(
        family
        for family, window in SHORT_WINDOWS.items()
        if length in window and family != 3
    )


def vector_row(
    p_value: int,
    b_value: int,
    coefficients: tuple[int, ...],
    sizes: tuple[int, ...],
) -> dict[str, object]:
    if not coefficients:
        return {
            "atom_sizes": [],
            "induced_blocks": [],
            "surviving_defect_assignments": [[]],
            "surviving_defect_assignment_count": 1,
            "forced_q_singleton": False,
            "survives_q_fibre_gate": True,
        }

    induced_blocks = []
    subsets = nonempty_subsets(len(coefficients))
    for subset in subsets:
        d_sum = sum(coefficients[index] for index in subset)
        n_sum = sum(sizes[index] for index in subset)
        core_size = b_value - d_sum
        length = core_size + 3 + n_sum
        assert 1 <= core_size <= p_value - 4
        assert 2 <= length <= 8
        induced_blocks.append(
            {
                "indices_one_based": [index + 1 for index in subset],
                "axis_coefficient_sum": d_sum,
                "atom_size_sum": n_sum,
                "X_core_size": core_size,
                "length": length,
                "allowed_actual_sum_coefficients": list(
                    allowed_non_f3_coefficients(length)
                ),
            }
        )

    assignments = []
    for defects in product((1, 2), repeat=len(coefficients)):
        if all(
            (3 - sum(defects[index - 1] for index in block["indices_one_based"]))
            % p_value
            in block["allowed_actual_sum_coefficients"]
            for block in induced_blocks
        ):
            assignments.append(list(defects))

    forced_q_singleton = any(
        coefficient == 1 and size == 1
        for coefficient, size in zip(coefficients, sizes)
    )
    survives_q_fibre_gate = bool(assignments) and not forced_q_singleton
    return {
        "atom_sizes": list(sizes),
        "induced_blocks": induced_blocks,
        "surviving_defect_assignments": assignments,
        "surviving_defect_assignment_count": len(assignments),
        "forced_q_singleton": forced_q_singleton,
        "survives_q_fibre_gate": survives_q_fibre_gate,
    }


def build_case(p_value: int, b_value: int) -> dict[str, object]:
    packing_rows = []
    for name, coefficients in PACKING_TYPES:
        d_total = sum(coefficients)
        if not coefficients:
            cap = 0
            vectors = [()]
            d_length = b_value + 3
            unique_tail_exception = True
        else:
            cap = 4 - b_value + d_total
            vectors = canonical_vectors(coefficients, cap)
            d_length = None
            unique_tail_exception = False

        x_d = b_value - d_total
        x_b = (p_value - 4) - x_d
        assert x_d + x_b == p_value - 4
        assert (x_d - b_value + d_total) % p_value == 0
        assert (x_b + b_value + 4 - d_total) % p_value == 0
        assert x_b > 8

        rows = [
            vector_row(p_value, b_value, coefficients, sizes) for sizes in vectors
        ]
        packing_rows.append(
            {
                "packing_type": name,
                "axis_coefficients": list(coefficients),
                "axis_coefficient_total": d_total,
                "D_X_core_size": x_d,
                "B_X_core_size": x_b,
                "nonempty_packing_size_upper_bound": cap,
                "unique_tail_exception": unique_tail_exception,
                "unique_tail_D_length": d_length,
                "candidate_vectors_after_complementary_block": [
                    list(vector) for vector in vectors
                ],
                "vectors": rows,
                "vectors_after_all_subfamily_blocks": [
                    row["atom_sizes"]
                    for row in rows
                    if row["surviving_defect_assignment_count"]
                ],
                "vectors_after_q_fibre_gate": [
                    row["atom_sizes"] for row in rows if row["survives_q_fibre_gate"]
                ],
            }
        )

    return {"p": p_value, "b": b_value, "packing_rows": packing_rows}


def build_report() -> dict[str, object]:
    cases = [build_case(p_value, b_value) for p_value, b_value in CASES]
    lookup = {
        (case["p"], row["packing_type"]): row
        for case in cases
        for row in case["packing_rows"]
    }

    expected_final = {
        (233, "empty"): [[]],
        (233, "(2)"): [[1], [2]],
        (233, "(3)"): [[1], [2], [3]],
        (1399, "empty"): [[]],
        (1399, "(2)"): [[1]],
        (1399, "(3)"): [[1], [2]],
    }
    for p_value in (233, 1399):
        for name, _ in PACKING_TYPES:
            actual = lookup[(p_value, name)]["vectors_after_q_fibre_gate"]
            assert actual == expected_final.get((p_value, name), [])

    complementary_vectors = sum(
        len(row["candidate_vectors_after_complementary_block"])
        for case in cases
        for row in case["packing_rows"]
    )
    subfamily_vectors = sum(
        len(row["vectors_after_all_subfamily_blocks"])
        for case in cases
        for row in case["packing_rows"]
    )
    final_vectors = sum(
        len(row["vectors_after_q_fibre_gate"])
        for case in cases
        for row in case["packing_rows"]
    )
    final_nonempty_defects = sum(
        vector["surviving_defect_assignment_count"]
        for case in cases
        for row in case["packing_rows"]
        if row["packing_type"] != "empty"
        for vector in row["vectors"]
        if vector["survives_q_fibre_gate"]
    )

    report: dict[str, object] = {
        "schema": "unique_tail_all_packing_short_blocks_v1",
        "scope": {
            "assumptions": [
                "p,b are (233,4) or (1399,5)",
                "the seven common-R packing coefficient types",
                "X=x^(p-4), U has three positions and quotient sum -bq",
                "Y=L disjoint_union R and R=P_1 disjoint_union ... disjoint_union P_t disjoint_union K",
                "all quotient-zero blocks of length at most eight obey the frozen short spectrum",
                "the only positive-core F3 tail is U with core size b",
                "each endpoint F3 complement has every nonzero quotient fibre of multiplicity at most p-4",
            ],
            "conclusion": (
                "for both primes the seven packing types reduce exactly to the necessary survivors empty, (2), and (3)"
            ),
            "not_concluded": [
                "any of empty, (2), or (3) is realizable",
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
        "cases": cases,
        "summary": {
            "packing_rows": 14,
            "candidate_vectors_after_complementary_block_including_empty": complementary_vectors,
            "vectors_after_all_subfamily_blocks_including_empty": subfamily_vectors,
            "vectors_after_q_fibre_gate_including_empty": final_vectors,
            "final_nonempty_defect_assignments": final_nonempty_defects,
            "closed_types_both_primes": ["(1)", "(1,1)", "(1,2)", "(1,1,1)"],
            "remaining_types_both_primes": ["empty", "(2)", "(3)"],
            "remaining_nonempty_vectors": {
                "233": {"(2)": [[1], [2]], "(3)": [[1], [2], [3]]},
                "1399": {"(2)": [[1]], "(3)": [[1], [2]]},
            },
        },
        "status": "SEVEN_PACKING_TYPES_REDUCED_TO_EMPTY_2_3__GLOBAL_INCOMPLETE",
    }
    assert complementary_vectors == 17
    assert subfamily_vectors == 12
    assert final_vectors == 10
    assert final_nonempty_defects == 12
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
