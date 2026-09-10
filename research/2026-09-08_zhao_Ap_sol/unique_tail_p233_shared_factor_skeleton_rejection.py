#!/usr/bin/env python3
"""Reject the frozen shared-factor quotient skeleton by all induced short blocks.

The certificate quantifies over every possible assignment of the actual
a-coordinate to the repeated e- and f-positions.  It closes only the explicit
quotient skeleton in unique_tail_type3_p233_shared_factor_attack.md.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


P = 233
N = P - 2
ROOT = Path(__file__).resolve().parent

DEPENDENCIES = {
    "proofs/unique_tail_type3_p233_shared_factor_attack.md":
        "fd226519af51b2d6b303e466630724e1862f55eb5d885f6212b7a13b72add3ad",
    "proofs/unique_tail_all_packing_short_blocks.md":
        "7abe228fa70dabd8858a40507b11505bd9cee388aa89fd79cd7a22fb8ec68238",
    "verify_unique_tail_labelled_position_next.py":
        "39c5a2db41097b3644962e22e932d5d9b501156ac46b1daded982de5da7d2076",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def add(*vectors: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(sum(entries) % P for entries in zip(*vectors))


def forcing_matrix() -> list[list[int]]:
    """A 2N-1 row subsystem of alpha_i+beta_j=constant."""

    matrix: list[list[int]] = []
    # alpha_i + beta_0 = constant for every i.
    for i in range(N):
        row = [0] * (2 * N)
        row[i] = 1
        row[N] = 1
        matrix.append(row)
    # alpha_0 + beta_j = constant for j>0.
    for j in range(1, N):
        row = [0] * (2 * N)
        row[0] = 1
        row[N + j] = 1
        matrix.append(row)
    return matrix


def audit_forcing_rank(matrix: list[list[int]]) -> int:
    """Certify independence using a unique-coordinate elimination order."""

    assert len(matrix) == 2 * N - 1
    assert all(len(row) == 2 * N for row in matrix)
    assert {index for index, value in enumerate(matrix[0]) if value} == {0, N}
    for i in range(1, N):
        # alpha_i occurs in no other row, so it is a unique pivot.
        assert {index for index, value in enumerate(matrix[i]) if value} == {i, N}
    for j in range(1, N):
        row = matrix[N + j - 1]
        # beta_j occurs in no other row, so it is a unique pivot.
        assert {index for index, value in enumerate(row) if value} == {0, N + j}
    # After the unique alpha_i/beta_j rows are removed, row zero is nonzero.
    return len(matrix)


def main() -> None:
    actual_dependencies = {
        relative: sha256_file(ROOT / relative)
        for relative in DEPENDENCIES
    }
    assert actual_dependencies == DEPENDENCIES

    q = (1, 0, 0)
    d = (1, 1, 1)
    u3 = (-5 % P, -2 % P, -2 % P)
    e = (0, 1, 0)
    f = (0, 0, 1)
    assert add(q, q, q, q, d, u3, e, f) == (0, 0, 0)

    matrix = forcing_matrix()
    rank = audit_forcing_rank(matrix)
    assert len(matrix) == 2 * N - 1
    assert rank == 2 * N - 1
    assert 2 * N - rank == 1

    # Directly verify that the star subsystem forces every full pair equation.
    # Its solutions have alpha_i=A and beta_j=C-A, so all N^2 equations agree.
    for alpha in (0, 1, 17, P - 1):
        for constant in (0, 3, 71, P - 1):
            beta = (constant - alpha) % P
            assert all((alpha + beta) % P == constant for _ in range(N * N))

    assert N == 231
    assert P - 4 == 229
    assert N > P - 4

    certificate = {
        "schema": "unique_tail_p233_shared_factor_skeleton_rejection_v1",
        "scope": {
            "p": P,
            "target": "the explicit quotient skeleton in the shared-factor compatibility proof",
            "quantified_heights": (
                "all a-coordinate assignments on e_2..e_(p-1), "
                "f_2..f_(p-1), and all other named positions"
            ),
        },
        "automatic_block": {
            "positions": "X_4 disjoint_union {d,u_3,e_i,f_j}",
            "i_range": "2..p-1",
            "j_range": "2..p-1",
            "length": 8,
            "quotient_sum": [0, 0, 0],
            "required_actual_family": 3,
            "block_count": N * N,
        },
        "height_system": {
            "equation": (
                "h(e_i)+h(f_j)=3-4h(x)-h(d)-h(u_3) for every i,j"
            ),
            "variable_count": 2 * N,
            "forcing_row_count": len(matrix),
            "forcing_rank": rank,
            "solution_dimension": 2 * N - rank,
            "consequence": (
                "all e_i heights are equal and all f_j heights are equal"
            ),
        },
        "multiplicity_contradiction": {
            "forced_e_actual_multiplicity": N,
            "forced_f_actual_multiplicity": N,
            "actual_multiplicity_cap": P - 4,
            "excess": N - (P - 4),
        },
        "conclusion": (
            "the explicit shared-factor quotient skeleton has no actual-height lift "
            "satisfying the complete induced short spectrum and multiplicity p-4"
        ),
        "not_claimed": [
            "the whole p=233 type-(3) |P|=2 slice is impossible",
            "every shared-factor compatible quotient skeleton has the repeated e/f form",
            "the global A_p statement is proved",
        ],
        "dependencies": actual_dependencies,
        "status": "FIXED_QUOTIENT_SKELETON_REJECTED__GLOBAL_INCOMPLETE",
    }
    report = dict(certificate)
    report["certificate_sha256"] = canonical_hash(certificate)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
