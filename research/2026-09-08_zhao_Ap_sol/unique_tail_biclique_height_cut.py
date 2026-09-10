#!/usr/bin/env python3
"""Audit the general biclique height cut and the p=233 thresholds.

This is an arithmetic/linear-algebra certificate.  It does not instantiate the
exact p=233 labelled slice and does not claim SAT or UNSAT for that slice.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


P = 233
CAP = P - 4
Y_SIZE = 2 * P + 8
P_SIZE = 2
ENDPOINT_LENGTH = 7
MAX_ENDPOINT_COUNT = 6
ROOT = Path(__file__).resolve().parent
REPORT_PATH = ROOT / "unique_tail_biclique_height_cut_report.json"


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def rank_mod_p(matrix: list[list[int]], prime: int) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    pivot_row = 0
    for col in range(col_count):
        pivot = next(
            (r for r in range(pivot_row, row_count) if rows[r][col] % prime),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][col] % prime, -1, prime)
        rows[pivot_row] = [(inverse * value) % prime for value in rows[pivot_row]]
        for r in range(row_count):
            if r == pivot_row:
                continue
            factor = rows[r][col] % prime
            if factor:
                rows[r] = [
                    (x - factor * y) % prime
                    for x, y in zip(rows[r], rows[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def complete_bipartite_matrix(left: int, right: int) -> list[list[int]]:
    matrix: list[list[int]] = []
    for i in range(left):
        for j in range(right):
            row = [0] * (left + right)
            row[i] = 1
            row[left + j] = 1
            matrix.append(row)
    return matrix


def star_matrix(left: int, right: int) -> list[list[int]]:
    matrix: list[list[int]] = []
    for i in range(left):
        row = [0] * (left + right)
        row[i] = 1
        row[left] = 1
        matrix.append(row)
    for j in range(1, right):
        row = [0] * (left + right)
        row[0] = 1
        row[left + j] = 1
        matrix.append(row)
    return matrix


def add_labels(labels: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    return tuple(sum(label[k] for label in labels) % P for k in range(3))


def local_max_atom_boundary() -> dict[str, object]:
    # All field elements once, with 0 replaced by a second 1: p scalars, sum 1.
    scalars = list(range(1, P)) + [1]
    assert len(scalars) == P
    assert sum(scalars) % P == 1

    # Lift the p-1 repeated projection-e positions with distinct q coordinates.
    e_lifts = [(t, 1, 0) for t in range(P - 1)]
    affine_lifts = [(0, scalar, 1) for scalar in scalars]
    quotient_sequence = e_lifts + affine_lifts
    assert len(quotient_sequence) == 2 * P - 1
    assert add_labels(quotient_sequence) == (1, 0, 0)

    exact_counts: dict[tuple[int, int, int], int] = {}
    for label in quotient_sequence:
        exact_counts[label] = exact_counts.get(label, 0) + 1
    assert max(exact_counts.values()) == 2

    projection_counts: dict[tuple[int, int], int] = {}
    for _, e_coord, f_coord in quotient_sequence:
        label = (e_coord, f_coord)
        projection_counts[label] = projection_counts.get(label, 0) + 1
    assert max(projection_counts.values()) == P - 1
    assert sorted(projection_counts.values(), reverse=True)[:2] == [P - 1, 2]

    # Delete 30 affine positions.  The result has the exact lower-bound size of
    # the p=233 common kernel and is zero-sum-free as a proper subsequence of
    # the symbolically certified atom.
    kernel = e_lifts + affine_lifts[30:]
    assert len(kernel) == 2 * P - 31

    # Symbolic minimality cases for e^(p-1) prod(ae+f), sum(a)=1.
    minimality_cases = {
        "affine_count_0": "e-count must be 0",
        "affine_count_between_1_and_p_minus_1": "f-coordinate is nonzero",
        "affine_count_p": "all affine positions and all p-1 e positions are forced",
    }
    return {
        "p": P,
        "projection_atom_length": len(quotient_sequence),
        "projection_total": [0, 0],
        "C_p3_total": [1, 0, 0],
        "largest_projection_fibres": [P - 1, 2],
        "largest_exact_C_p3_fibre": max(exact_counts.values()),
        "zero_sum_free_proper_subsequence_length": len(kernel),
        "symbolic_minimality_cases": minimality_cases,
        "scope": "single-Q local boundary example only",
    }


def main() -> None:
    allowed_coefficients = {
        2: [1],
        3: [1],
        4: [1, 2],
        5: [1, 2],
        6: [1, 2, 3],
        7: [2, 3],
        8: [3],
    }
    assert allowed_coefficients[8] == [3]

    rank_checks: list[dict[str, int]] = []
    for left, right in [(1, 1), (2, 3), (P - 2, P - 2)]:
        star = star_matrix(left, right)
        star_rank = rank_mod_p(star, P)
        expected = left + right - 1
        assert len(star) == expected
        assert star_rank == expected
        # The full matrix is small only in the first two regression cases.
        if left * right <= 20:
            full_rank = rank_mod_p(complete_bipartite_matrix(left, right), P)
            assert full_rank == expected
        rank_checks.append(
            {
                "left": left,
                "right": right,
                "forcing_rows": len(star),
                "forcing_rank": star_rank,
                "solution_dimension": left + right - star_rank,
            }
        )

    l_upper = 1 + (ENDPOINT_LENGTH - 1) * MAX_ENDPOINT_COUNT
    k_lower = Y_SIZE - l_upper - P_SIZE
    q_minus_k_upper = l_upper - ENDPOINT_LENGTH
    assert l_upper == 37
    assert k_lower == 435 == 2 * P - 31
    assert q_minus_k_upper == 30
    assert CAP + 1 == P - 3 == 230

    certificate = {
        "schema": "unique_tail_biclique_height_cut_v1",
        "general_lemma": {
            "hypothesis": (
                "fixed disjoint base C and nonempty disjoint sides A,B; every "
                "C union {u,v} has quotient sum zero and the same actual sum lambda*a"
            ),
            "conclusion": (
                "all positions on each side have one common quotient label and "
                "one common actual label"
            ),
            "connected_graph_variant": True,
            "forcing_rank": "|A|+|B|-1 per connected component",
        },
        "short_spectrum": allowed_coefficients,
        "p233_threshold": {
            "actual_multiplicity_cap": CAP,
            "one_side_contradiction_threshold": CAP + 1,
            "both_sides_contradiction_threshold": CAP + 1,
            "fixed_skeleton_side_size": P - 2,
        },
        "p233_static_geometry": {
            "selected_endpoint_count_range": [4, MAX_ENDPOINT_COUNT],
            "common_position_union_upper_bound": l_upper,
            "common_kernel_lower_bound": k_lower,
            "Q_minus_K_upper_bound": q_minus_k_upper,
            "Q_length": 2 * P - 1,
            "directed_pair_edit_upper_bound": ENDPOINT_LENGTH - 1,
            "symmetric_difference_upper_bound": 2 * (ENDPOINT_LENGTH - 1),
        },
        "rank_checks": rank_checks,
        "local_boundary_example": local_max_atom_boundary(),
        "missing_statement": {
            "name": "OPEN_RECTANGLE_233",
            "required_output": (
                "a fixed six-position base and a connected bipartite automatic "
                "length-eight block graph with at least 230 vertices on one side"
            ),
            "not_implied_by": [
                "the length of K alone",
                "one maximal C_p^2 atom alone",
                "a large C_p^2 projection fibre without q-lift coherence",
            ],
        },
        "not_claimed": [
            "the exact p=233 slice is SAT",
            "the exact p=233 slice is UNSAT",
            "the three simultaneous maximal atoms admit the local boundary example",
            "the global A_p statement is proved",
        ],
        "status": "PROVED_GENERAL_LEMMA__OPEN_RECTANGLE_233__GLOBAL_INCOMPLETE",
    }
    report = dict(certificate)
    report["certificate_sha256"] = canonical_hash(certificate)
    rendered = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    REPORT_PATH.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
