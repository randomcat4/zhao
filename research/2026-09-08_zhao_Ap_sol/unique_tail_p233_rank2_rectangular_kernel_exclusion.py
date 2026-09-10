#!/usr/bin/env python3
"""Finite certificate for the p=233 two-monochromatic kernel threshold."""

from __future__ import annotations

import hashlib
import json


P = 233
THRESHOLD = (P - 1) // 2
FIXED_E_COUNT = P - 6
FIXED_F_COUNT = P - 7


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def pair_partition(e_count: int, f_count: int) -> dict[str, int]:
    partition = {
        "Q3_e_tail_witness": 0,
        "Q3_f_tail_witness_after_e_gate": 0,
        "Q1_or_Q2_u3_tail_witness_after_both_gates": 0,
        "proof_gap_after_both_gates": 0,
    }
    for alpha in range(1, P):
        m = pow(alpha, P - 2, P)
        r0 = (-m) % P
        if r0 <= e_count:
            partition["Q3_e_tail_witness"] += P - 1
            continue

        for beta in range(1, P):
            n = pow(beta, P - 2, P)
            s0 = (-n) % P
            if s0 <= f_count:
                partition["Q3_f_tail_witness_after_e_gate"] += 1
                continue

            if m <= e_count and n <= f_count:
                # u_3=-e-f together with m copies of alpha*e and n copies
                # of beta*f is a proper zero-sum subsequence of Q_1,Q_2.
                assert (-1 + m * alpha) % P == 0
                assert (-1 + n * beta) % P == 0
                witness_size = 1 + m + n
                assert 3 <= witness_size < 2 * P - 1
                partition[
                    "Q1_or_Q2_u3_tail_witness_after_both_gates"
                ] += 1
            else:
                partition["proof_gap_after_both_gates"] += 1

    assert sum(partition.values()) == (P - 1) ** 2 == 53824
    return partition


def main() -> None:
    # Algebraic threshold audit.  If the one-tail witness is unavailable,
    # r0=-alpha^(-1) is at least count+1, hence
    # m=alpha^(-1)=p-r0 <= p-count-1 <= count for count>=116.
    threshold_scalar_checks = 0
    for count in range(THRESHOLD, P):
        for scalar in range(1, P):
            inverse = pow(scalar, P - 2, P)
            cancellation_count = (-inverse) % P
            if cancellation_count > count:
                assert inverse == P - cancellation_count
                assert inverse <= P - count - 1 <= count
            threshold_scalar_checks += 1

    boundary_partitions = {
        f"{e_count},{f_count}": pair_partition(e_count, f_count)
        for e_count in (THRESHOLD - 1, THRESHOLD)
        for f_count in (THRESHOLD - 1, THRESHOLD)
    }
    assert boundary_partitions == {
        "115,115": {
            "Q3_e_tail_witness": 26680,
            "Q3_f_tail_witness_after_e_gate": 13455,
            "Q1_or_Q2_u3_tail_witness_after_both_gates": 13225,
            "proof_gap_after_both_gates": 464,
        },
        "115,116": {
            "Q3_e_tail_witness": 26680,
            "Q3_f_tail_witness_after_e_gate": 13572,
            "Q1_or_Q2_u3_tail_witness_after_both_gates": 13340,
            "proof_gap_after_both_gates": 232,
        },
        "116,115": {
            "Q3_e_tail_witness": 26912,
            "Q3_f_tail_witness_after_e_gate": 13340,
            "Q1_or_Q2_u3_tail_witness_after_both_gates": 13340,
            "proof_gap_after_both_gates": 232,
        },
        "116,116": {
            "Q3_e_tail_witness": 26912,
            "Q3_f_tail_witness_after_e_gate": 13456,
            "Q1_or_Q2_u3_tail_witness_after_both_gates": 13456,
            "proof_gap_after_both_gates": 0,
        },
    }

    fixed_partition = pair_partition(FIXED_E_COUNT, FIXED_F_COUNT)
    assert fixed_partition == {
        "Q3_e_tail_witness": 52664,
        "Q3_f_tail_witness_after_e_gate": 1130,
        "Q1_or_Q2_u3_tail_witness_after_both_gates": 30,
        "proof_gap_after_both_gates": 0,
    }

    certificate = {
        "schema": "unique_tail_p233_rank2_rectangular_kernel_exclusion_v2",
        "scope": {
            "p": P,
            "tail_projection_normal_form": [[1, 0], [0, 1], [P - 1, P - 1]],
            "Q_i_length": 2 * P - 1,
            "common_two_monochromatic_core": {
                "alpha_e_position_count": f"r >= {THRESHOLD}",
                "beta_f_position_count": f"s >= {THRESHOLD}",
                "alpha_beta_quantifier": "all nonzero alpha,beta in F_p",
            },
        },
        "tail_incidence": {
            "Q1_contains": ["w2=f", "w3=-e-f"],
            "Q2_contains": ["w1=e", "w3=-e-f"],
            "Q3_contains": ["w1=e", "w2=f"],
        },
        "gate_consequences": {
            "Q3_atom_from_e_tail_requires": "m=alpha^(-1) <= p-r-1 <= r",
            "Q3_atom_from_f_tail_requires": "n=beta^(-1) <= p-s-1 <= s",
            "then_Q1_and_Q2_have_proper_zero_subsequence": (
                "{u3} plus alpha^(-1) copies of alpha*e plus "
                "beta^(-1) copies of beta*f"
            ),
            "witness_length_upper_bound": "1+m+n <= p < 2p-1",
        },
        "threshold": THRESHOLD,
        "threshold_scalar_checks": threshold_scalar_checks,
        "boundary_partitions": boundary_partitions,
        "parameter_pair_count": (P - 1) ** 2,
        "fixed_227_226_corollary": {
            "e_count": FIXED_E_COUNT,
            "f_count": FIXED_F_COUNT,
            "parameter_partition": fixed_partition,
            "final_witness_size_range": [3, 12],
        },
        "conclusion": (
            "three simultaneous length-(2p-1) atoms Q_i cannot share the "
            "two-monochromatic common core (alpha*e)^r (beta*f)^s when "
            "r,s >= (p-1)/2; in particular the fixed 227-by-226 core is excluded"
        ),
        "not_claimed": [
            "the threshold 115 failure of this proof is a realizable atom model",
            "an arbitrary common core has two monochromatic fibres of size 116",
            "all rank-two shared-factor skeletons are excluded",
            "the p=233 exact slice is UNSAT",
            "the global A_p statement is settled",
        ],
        "status": (
            "TWO_MONOCHROMATIC_COMMON_KERNEL_THRESHOLD_EXCLUDED"
            "__FIXED_227_226_COROLLARY__GLOBAL_INCOMPLETE"
        ),
    }
    report = dict(certificate)
    report["certificate_sha256"] = canonical_hash(certificate)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
