#!/usr/bin/env python3
"""Exact certificate for the rank-two three-functional fringe interface.

The construction is exact for the three singleton-tail top functionals and
their shared literal-factor/petal decompositions.  It deliberately does not
claim that the three length-(2p-1) zero-sum sequences are atoms.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


P = 233
ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Position:
    name: str
    value: tuple[int, int]


def add(*vectors: tuple[int, int]) -> tuple[int, int]:
    return (
        sum(vector[0] for vector in vectors) % P,
        sum(vector[1] for vector in vectors) % P,
    )


def neg(vector: tuple[int, int]) -> tuple[int, int]:
    return (-vector[0] % P, -vector[1] % P)


def scalar_vector(scalar: int, vector: tuple[int, int]) -> tuple[int, int]:
    return (scalar * vector[0] % P, scalar * vector[1] % P)


def sequence_sum(sequence: list[Position]) -> tuple[int, int]:
    return add(*(position.value for position in sequence))


def leading_product(sequence: list[Position]) -> dict[int, int]:
    """Product of the linear initial forms a*u+b*v in the truncated ring.

    The dictionary key is the u exponent.  Terms with either exponent at
    least p are zero in F_p[u,v]/(u^p,v^p).
    """

    coefficients = {0: 1}
    degree = 0
    for position in sequence:
        a, b = position.value
        updated: dict[int, int] = {}
        for u_exp, coefficient in coefficients.items():
            v_exp = degree - u_exp
            if a and u_exp + 1 < P:
                updated[u_exp + 1] = (
                    updated.get(u_exp + 1, 0) + coefficient * a
                ) % P
            if b and v_exp + 1 < P:
                updated[u_exp] = (
                    updated.get(u_exp, 0) + coefficient * b
                ) % P
        coefficients = {key: value for key, value in updated.items() if value}
        degree += 1
    return coefficients


def lambda_from_fringe(coefficients: dict[int, int], vector: tuple[int, int]) -> int:
    """Coefficient of J after multiplying a degree-(2p-3) fringe by w."""

    assert set(coefficients).issubset({P - 2, P - 1})
    a, b = vector
    # A*u^(p-1)v^(p-2) + B*u^(p-2)v^(p-1).
    A = coefficients.get(P - 1, 0)
    B = coefficients.get(P - 2, 0)
    return (b * A + a * B) % P


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_positions() -> tuple[
    list[Position], list[list[Position]], list[Position], list[Position]
]:
    e = (1, 0)
    f = (0, 1)
    y = Position("y", (1, 1))

    # Each A_i has five literal positions.  Its linear initial-form product is
    # c_i*u^2*v^2*(u+t_i*v), with
    # (t_1,t_2,t_3)=(-4,4/5,-4/7) and
    # (c_1,c_2,c_3)=(1/8,5/4,-7/4) in F_233.
    petals = [
        [
            Position("a1e1", scalar_vector(3, e)),
            Position("a1e2", scalar_vector(227, e)),
            Position("a1f1", scalar_vector(43, f)),
            Position("a1f2", scalar_vector(193, f)),
            Position("a1m", (1, 229)),
        ],
        [
            Position("a2e1", scalar_vector(2, e)),
            Position("a2e2", scalar_vector(229, e)),
            Position("a2f1", scalar_vector(7, f)),
            Position("a2f2", scalar_vector(130, f)),
            Position("a2m", (1, 94)),
        ],
        [
            Position("a3e1", scalar_vector(3, e)),
            Position("a3e2", scalar_vector(229, e)),
            Position("a3f1", scalar_vector(69, f)),
            Position("a3f2", scalar_vector(98, f)),
            Position("a3m", (1, 66)),
        ],
    ]

    # The 453-position common core has initial form
    # -2*u^227*v^226 and sum 2e+2f.
    e_scales = [1] * 224 + [2, 107, 135]
    f_scales = [1] * 223 + [1, 85, 159]
    common = [
        Position(f"ge{index}", scalar_vector(scale, e))
        for index, scale in enumerate(e_scales, start=1)
    ] + [
        Position(f"gf{index}", scalar_vector(scale, f))
        for index, scale in enumerate(f_scales, start=1)
    ]

    tails = [
        Position("u1", e),
        Position("u2", f),
        Position("u3", (-1 % P, -1 % P)),
    ]
    return common, petals, [y], tails


def main() -> None:
    common, petals, shared, tails = build_positions()
    y = shared[0]
    assert len(common) == 2 * P - 13 == 453
    assert sequence_sum(common) == (2, 2)
    assert all(position.value != (0, 0) for position in common)

    expected_petal_sums = [(P - 2, P - 1), (P - 1, P - 2), (0, 0)]
    assert [sequence_sum(petal) for petal in petals] == expected_petal_sums
    assert all(
        position.value != (0, 0)
        for petal in petals
        for position in petal
    )

    endpoint_exteriors = [[y] + petal for petal in petals]
    assert [len(exterior) for exterior in endpoint_exteriors] == [6, 6, 6]
    assert [sequence_sum(exterior) for exterior in endpoint_exteriors] == [
        neg(tail.value) for tail in tails
    ]
    endpoints = [
        [tails[i]] + endpoint_exteriors[i]
        for i in range(3)
    ]
    assert [len(endpoint) for endpoint in endpoints] == [7, 7, 7]
    assert [sequence_sum(endpoint) for endpoint in endpoints] == [(0, 0)] * 3
    assert all(
        {position.name for position in endpoint_exteriors[i]}
        & {position.name for position in endpoint_exteriors[j]}
        == {"y"}
        for i in range(3)
        for j in range(i + 1, 3)
    )
    assert all(
        {position.name for position in endpoints[i]}
        & {position.name for position in endpoints[j]}
        == {"y"}
        for i in range(3)
        for j in range(i + 1, 3)
    )

    middle = common + [y] + [position for petal in petals for position in petal]
    assert len(middle) == 2 * P + 3 == 469
    assert sequence_sum(middle) == (0, 0)

    fringes: list[list[Position]] = []
    long_zero_sequences: list[list[Position]] = []
    fringe_coefficients: list[dict[int, int]] = []
    lambda_matrix: list[list[int]] = []
    pair_records = []
    for i in range(3):
        fringe = common + [
            position
            for j, petal in enumerate(petals)
            if j != i
            for position in petal
        ]
        q_i = fringe + [tails[j] for j in range(3) if j != i]
        assert len(fringe) == 2 * P - 3 == 463
        assert len(q_i) == 2 * P - 1 == 465
        assert sequence_sum(fringe) == tails[i].value
        assert sequence_sum(q_i) == (0, 0)
        coefficients = leading_product(fringe)
        assert set(coefficients).issubset({P - 2, P - 1})
        row = [lambda_from_fringe(coefficients, tail.value) for tail in tails]
        fringes.append(fringe)
        long_zero_sequences.append(q_i)
        fringe_coefficients.append(coefficients)
        lambda_matrix.append(row)

    expected_coefficients = [
        {P - 1: 1, P - 2: P - 2},
        {P - 1: P - 2, P - 2: 1},
        {P - 1: 1, P - 2: 1},
    ]
    expected_lambda_matrix = [
        [P - 2, 1, 1],
        [1, P - 2, 1],
        [1, 1, P - 2],
    ]
    assert fringe_coefficients == expected_coefficients
    assert lambda_matrix == expected_lambda_matrix
    assert [sum(row) % P for row in lambda_matrix] == [0, 0, 0]
    assert [sum(lambda_matrix[i][j] for i in range(3)) % P for j in range(3)] == [
        0,
        0,
        0,
    ]

    for i in range(3):
        for j in range(i + 1, 3):
            k = 3 - i - j
            common_names = {
                position.name for position in common + petals[k]
            }
            left_names = {position.name for position in fringes[i]}
            right_names = {position.name for position in fringes[j]}
            assert left_names & right_names == common_names
            assert left_names - right_names == {
                position.name for position in petals[j]
            }
            assert right_names - left_names == {
                position.name for position in petals[i]
            }
            pair_records.append(
                {
                    "endpoints": [i + 1, j + 1],
                    "shared_literal_factor_length": len(common_names),
                    "left_petal": j + 1,
                    "right_petal": i + 1,
                    "petal_length": len(petals[i]),
                }
            )

    certificate = {
        "schema": "unique_tail_p233_rank2_three_functional_compatibility_v1",
        "scope": {
            "p": P,
            "packing_type": "(3)",
            "P_size": 2,
            "kappa": 1,
            "endpoint_pattern": "three singleton traces, all endpoint lengths seven",
            "tail_projection_normal_form": [[1, 0], [0, 1], [P - 1, P - 1]],
        },
        "forced_functional_normal_form": {
            "evaluation_matrix_rows_lambda_i_columns_w_j": lambda_matrix,
            "integer_representatives": [[-2, 1, 1], [1, -2, 1], [1, 1, -2]],
            "matrix_formula": "all_ones_matrix - 3*identity_matrix",
            "rank": 2,
            "row_sum": 0,
            "column_sum": 0,
        },
        "explicit_literal_model": {
            "middle_sequence_length": len(middle),
            "middle_sequence_sum": list(sequence_sum(middle)),
            "common_core_length": len(common),
            "common_core_sum": list(sequence_sum(common)),
            "endpoint_exterior_lengths": [len(exterior) for exterior in endpoint_exteriors],
            "endpoint_exterior_sums": [
                list(sequence_sum(exterior)) for exterior in endpoint_exteriors
            ],
            "fringe_lengths": [len(fringe) for fringe in fringes],
            "fringe_sums": [list(sequence_sum(fringe)) for fringe in fringes],
            "long_zero_sequence_lengths": [len(q_i) for q_i in long_zero_sequences],
            "long_zero_sequence_sums": [
                list(sequence_sum(q_i)) for q_i in long_zero_sequences
            ],
            "degree_2p_minus_3_coefficients": [
                {
                    "u^(p-1)v^(p-2)": coefficients.get(P - 1, 0),
                    "u^(p-2)v^(p-1)": coefficients.get(P - 2, 0),
                }
                for coefficients in fringe_coefficients
            ],
            "pairwise_factorizations": pair_records,
        },
        "exact_conclusion": (
            "the three forced singleton-tail top functionals and every pairwise "
            "shared literal-factor/petal identity are simultaneously realizable "
            "by one labelled C_p^2 position sequence"
        ),
        "not_claimed": [
            "any of the three length-(2p-1) zero-sum sequences is an atom",
            "all deletion products for those sequences equal J",
            "the complete automatic short-block spectrum is satisfied",
            "a 474-position exact-slice instance is loaded",
            "the p=233 exact slice is SAT or UNSAT",
            "the global A_p statement is settled",
        ],
        "status": (
            "PROVED_EXACT_COMPATIBILITY_OF_THREE_FUNCTIONAL_SHARED_LITERAL_INTERFACE"
            "__RELAXED_BEYOND_THIS_INTERFACE__GLOBAL_INCOMPLETE"
        ),
    }
    report = dict(certificate)
    report["certificate_sha256"] = canonical_hash(certificate)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
