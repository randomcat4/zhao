"""Finite regression checks for the p=233 mixed-core separator.

This script verifies only the exact finite arithmetic asserted in the
companion proof.  The structural implications themselves are proved there.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_REPORT = HERE / "unique_tail_p233_length_decorated_trace_reduction_report.json"
PROOF = HERE / "proofs" / "unique_tail_p233_mixed_core_separator.md"
REPORT = HERE / "unique_tail_p233_mixed_core_separator_report.json"
P = 233


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_outer_distribution() -> dict[str, object]:
    source = json.loads(SOURCE_REPORT.read_text(encoding="utf-8"))
    survivors = source["surviving_shards"]
    singleton_h7 = Counter(row["singleton_length_7_count"] for row in survivors)
    assert len(survivors) == 720
    assert singleton_h7 == Counter({1: 540, 0: 180})
    assert source["surviving_singleton_length_7_distribution"] == {
        str(key): value for key, value in sorted(singleton_h7.items())
    }
    return {
        "outer_survivors": len(survivors),
        "with_one_length_7_singleton": singleton_h7[1],
        "all_singletons_length_8": singleton_h7[0],
    }


def verify_length_7_affine_signature() -> dict[str, int]:
    counts: Counter[str] = Counter()
    for u in range(P):
        for v in range(P):
            if u == 0 and v == 0:
                continue
            c_plus = (1 + u + v) % P
            c_minus = (1 - u - v) % P
            assert c_plus != 0 or c_minus != 0
            counts["exactly_one_signed_coefficient_nonzero" if (c_plus == 0) ^ (c_minus == 0)
                   else "both_signed_coefficients_nonzero"] += 1
    assert counts == Counter(
        {
            "both_signed_coefficients_nonzero": P * P - 1 - 2 * P,
            "exactly_one_signed_coefficient_nonzero": 2 * P,
        }
    )
    return dict(sorted(counts.items()))


def verify_length_8_quadratic_signature() -> dict[str, int]:
    counts: Counter[str] = Counter()
    exact_signed_tail_labels = {
        (1, 0),
        (P - 1, 0),
        (0, 1),
        (0, P - 1),
        (1, 1),
        (P - 1, P - 1),
    }

    for u in range(P):
        for v in range(P):
            if u == 0 and v == 0:
                continue
            rhs = ((u - v) * (u - v) - 1) % P
            on_tail_direction = u == 0 or v == 0 or u == v

            if u == v:
                # Au+Bv=0 forces Au^2+Bv^2=0, whereas rhs=-1.
                assert rhs == P - 1
                counts["diagonal_no_solution"] += 1
                continue

            if u == 0:
                possible = v in {1, P - 1}
                assert (rhs == 0) == possible
                counts["axis_exception_possible" if possible else "axis_no_solution"] += 1
                continue

            if v == 0:
                possible = u in {1, P - 1}
                assert (rhs == 0) == possible
                counts["axis_exception_possible" if possible else "axis_no_solution"] += 1
                continue

            assert not on_tail_direction
            determinant = (u * v * (v - u)) % P
            assert determinant != 0
            inv_det = pow(determinant, -1, P)
            a_coeff = (-v * rhs * inv_det) % P
            b_coeff = (u * rhs * inv_det) % P
            assert (a_coeff * u + b_coeff * v) % P == 0
            assert (a_coeff * u * u + b_coeff * v * v) % P == rhs
            counts["generic_unique_candidate"] += 1

    assert counts == Counter(
        {
            "generic_unique_candidate": (P - 1) * (P - 2),
            "diagonal_no_solution": P - 1,
            "axis_no_solution": 2 * (P - 3),
            "axis_exception_possible": 4,
        }
    )

    nonzero_tail_direction = 3 * (P - 1)
    allowed_tail_direction = nonzero_tail_direction - len(exact_signed_tail_labels)
    forced_before_global_tail_exclusion = (
        counts["diagonal_no_solution"] + counts["axis_no_solution"]
    )
    assert nonzero_tail_direction == 696
    assert allowed_tail_direction == 690
    assert forced_before_global_tail_exclusion == 692
    return {
        **dict(sorted(counts.items())),
        "nonzero_points_on_three_tail_directions": nonzero_tail_direction,
        "globally_excluded_exact_signed_tail_labels": len(exact_signed_tail_labels),
        "allowed_tail_direction_points_forcing_a_short_representation": allowed_tail_direction,
        "forced_points_before_global_tail_exclusion": forced_before_global_tail_exclusion,
    }


def main() -> None:
    report: dict[str, object] = {
        "schema": "unique-tail-p233-mixed-core-separator-v1",
        "status": "FINITE_REGRESSION_FOR_AUDITED_PROOF/GLOBAL_INCOMPLETE",
        "p": P,
        "outer_distribution": verify_outer_distribution(),
        "length_7_affine_signature": verify_length_7_affine_signature(),
        "length_8_quadratic_signature": verify_length_8_quadratic_signature(),
        "source_sha256": {
            SOURCE_REPORT.name: sha256(SOURCE_REPORT),
            str(PROOF.relative_to(HERE)).replace("\\", "/"): sha256(PROOF),
        },
        "scope": {
            "verified": [
                "the 540/180 outer-row split",
                "the length-seven signed affine coefficient exhaustion",
                "the length-eight quadratic signature classification over all nonzero targets",
                "the exact 696/690/53592 target counts",
            ],
            "not_claimed": [
                "a concrete rho-label realization for any outer row",
                "elimination of an outer row",
                "the full p=233 slice or global A_p",
            ],
        },
    }
    canonical = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    report["certificate_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
