#!/usr/bin/env python3
"""Finite certificate for the rank-one singleton-tail fringe reduction.

This script audits only the frozen p=233, type-(3), |P|=2 slice.  It does
not solve the labelled position CSP and does not claim that any surviving
length pattern is realizable.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


P = 233
ROOT = Path(__file__).resolve().parent

DEPENDENCIES = {
    "proofs/unique_tail_four_edge_joint_csp.md":
        "87954d09a00aa74d3d43ce7d784deeff325965e61fca80e900d610371260201f",
    "proofs/unique_tail_all_packing_short_blocks.md":
        "7abe228fa70dabd8858a40507b11505bd9cee388aa89fd79cd7a22fb8ec68238",
    "proofs/unique_tail_remaining_long_complement_internal_sums.md":
        "311730df217f79659cf0d934b8c0df2e02489196208b9e699dc31d8b929d10d1",
    "proofs/unique_tail_type3_near_davenport_group_algebra.md":
        "705da14a4f7d8de60e2ad71f91b349bce277386090ba7611941d2a176b764b47",
    "proofs/unique_tail_type3_shared_endpoint_fringe.md":
        "a0168e71cc4ea7a5fe17f4343de61827eb50d1c9459a33b65d6a90e85beeffa4",
    "proofs/unique_tail_tail_anchoring.md":
        "a47995488262e820515dcda0ca7773a2c08dec54170da2a2da49f6e4e65f0421",
    "unique_tail_position_conflict_frontier.py":
        "6d994a130ee11a228c6714206ee9ce4f332c6f8bd8f41ed69655228784497506",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def augmentation_fringe_dimension(degree: int) -> int:
    """Dimension of I^degree in F_p[C_p^2]."""

    return sum(
        1
        for i in range(P)
        for j in range(P)
        if i + j >= degree
    )


def ell(coefficients: tuple[int, int], vector: tuple[int, int]) -> int:
    """Top coefficient of F(1-X^w) for F in I^(2p-3).

    In truncated coordinates u=1-X^e1, v=1-X^e2, write the degree
    2p-3 part of F as A*u^(p-1)v^(p-2)+B*u^(p-2)v^(p-1).  Only the
    linear part of 1-X^(a,b), namely a*u+b*v modulo I^2, survives.
    """

    a, b = vector
    A, B = coefficients
    return (b * A + a * B) % P


def audit_linearity() -> int:
    tested = 0
    coefficient_samples = ((1, 0), (0, 1), (7, 19), (P - 1, 31))
    vector_samples = tuple(itertools.product(range(7), repeat=2))
    for coefficients in coefficient_samples:
        for left in vector_samples:
            for right in vector_samples:
                total = ((left[0] + right[0]) % P, (left[1] + right[1]) % P)
                assert ell(coefficients, total) == (
                    ell(coefficients, left) + ell(coefficients, right)
                ) % P
                tested += 1
        for scalar in range(7):
            for vector in vector_samples:
                multiple = (scalar * vector[0] % P, scalar * vector[1] % P)
                assert ell(coefficients, multiple) == (
                    scalar * ell(coefficients, vector)
                ) % P
                tested += 1
    return tested


def coefficient_triples() -> tuple[tuple[int, int, int], ...]:
    rows = []
    for c1 in range(1, P):
        for c2 in range(1, P):
            c3 = (-c1 - c2) % P
            if c3:
                rows.append((c1, c2, c3))
    assert len(rows) == (P - 1) * (P - 2)
    return tuple(rows)


def length_pattern_records() -> list[dict[str, object]]:
    triples = coefficient_triples()
    records = []
    for lengths in itertools.product((7, 8), repeat=3):
        survivors = []
        for coefficients in triples:
            valid = True
            for endpoint in range(3):
                if lengths[endpoint] != 7:
                    continue
                other = [index for index in range(3) if index != endpoint]
                # The two deleted-tail identities give ell(w_j)=ell(w_k)=1.
                # On a rank-one tail this forces c_j=c_k.
                if coefficients[other[0]] != coefficients[other[1]]:
                    valid = False
                    break
            if valid:
                survivors.append(coefficients)
        records.append(
            {
                "endpoint_lengths": list(lengths),
                "delta_pattern": [length - 7 for length in lengths],
                "rank_one_coefficient_triples": len(survivors),
                "rank_one_projective_orbits": len(survivors) // (P - 1),
                "survives_rank_one_fringe": bool(survivors),
            }
        )
    return records


def main() -> None:
    actual_dependencies = {
        relative: sha256_file(ROOT / relative)
        for relative in DEPENDENCIES
    }
    assert actual_dependencies == DEPENDENCIES

    assert augmentation_fringe_dimension(2 * P - 2) == 1
    assert augmentation_fringe_dimension(2 * P - 3) == 3
    linearity_checks = audit_linearity()

    records = length_pattern_records()
    surviving = [row for row in records if row["survives_rank_one_fringe"]]
    eliminated = [row for row in records if not row["survives_rank_one_fringe"]]
    assert {tuple(row["endpoint_lengths"]) for row in surviving} == {
        (8, 8, 8),
        (7, 8, 8),
        (8, 7, 8),
        (8, 8, 7),
    }
    assert all(sum(length == 7 for length in row["endpoint_lengths"]) >= 2
               for row in eliminated)
    assert next(
        row for row in surviving if row["endpoint_lengths"] == [8, 8, 8]
    )["rank_one_projective_orbits"] == P - 2
    assert all(
        row["rank_one_projective_orbits"] == 1
        for row in surviving
        if row["endpoint_lengths"] != [8, 8, 8]
    )

    certificate = {
        "schema": "unique_tail_p233_singleton_tail_fringe_v1",
        "scope": {
            "p": P,
            "b": 4,
            "packing_type": "(3)",
            "P_size": 2,
            "packing_axis_defect": 1,
            "branch": "four-edge all-distinct traces; three singleton-trace endpoints",
            "tail_projection_rank": 1,
        },
        "algebra": {
            "I_2p_minus_2_dimension": 1,
            "I_2p_minus_3_dimension": 3,
            "length_7_Q_length": 2 * P - 1,
            "length_7_C_length": 2 * P - 3,
            "deleted_tail_products": "Psi_C Psi_{u_j}=Psi_C Psi_{u_k}=J",
            "consequence": "ell_C(w_j)=ell_C(w_k)=1, hence c_j=c_k in rank one",
        },
        "length_patterns": records,
        "conclusion": (
            "in quotient-rank one, at most one of the three singleton-trace "
            "endpoints has length seven; up to permutation only 888 and 788 remain"
        ),
        "all_length_seven_slice_corollary": (
            "the frozen 777 singleton-endpoint slice has quotient-rank two; "
            "after GL(2,p) normalization its ordered tail projection is "
            "((1,0),(0,1),(-1,-1))"
        ),
        "not_claimed": [
            "rank-two tails are excluded",
            "either surviving rank-one length pattern is realizable",
            "the p=233 labelled slice is UNSAT",
            "the global A_p statement is proved",
        ],
        "dependencies": actual_dependencies,
        "linearity_checks": linearity_checks,
        "status": "PROVED_REDUCTION__RANK_ONE_ONLY__GLOBAL_INCOMPLETE",
    }
    report = dict(certificate)
    report["certificate_sha256"] = canonical_hash(certificate)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
