#!/usr/bin/env python3
"""Exact arithmetic certificate for the forced short-packing block.

The mathematical input is frozen to the two three-point unique-tail cases and
the three common packing coefficient types with total coefficient three.  The
script checks the complementary quotient-zero blocks, the forbidden-length
dichotomy, the positive-core length-eight gate, every surviving atom-size
vector, and the resulting lower bound for the common zero-sum-free kernel.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_forced_short_packing_block_report.json"
DEPENDENCY_PATHS = (
    HERE / "assumptions.md",
    HERE / "proofs" / "middle_quotient_gap.md",
    HERE / "proofs" / "unique_tail_common_R_next.md",
    HERE / "proofs" / "unique_tail_forced_kernel_nonempty.md",
    HERE / "proofs" / "unique_tail_labelled_position_next.md",
)

CASES = ((233, 4), (1399, 5))
PACKING_TYPES = (
    ("(3)", (3,)),
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


def canonical_size_vectors(
    coefficients: tuple[int, ...], cap: int
) -> list[tuple[int, ...]]:
    """Positive atom sizes, modulo permutations of equal-coefficient atoms."""

    rows = []
    for sizes in product(range(1, cap + 1), repeat=len(coefficients)):
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


def allowed_short_families(total_length: int) -> list[int]:
    """Families allowed by length after removing the wrong positive-core F3."""

    return [
        family
        for family, window in SHORT_WINDOWS.items()
        if total_length in window and family != 3
    ]


def build_case(p_value: int, b_value: int) -> dict[str, object]:
    x_multiplicity = p_value - 4
    d_x_core = b_value - 3
    b_x_core = p_value - b_value - 1
    z_length = 3 * p_value + 4

    assert d_x_core > 0
    assert d_x_core + b_x_core == x_multiplicity

    # Quotient coefficients: U=-bq, sum(P_i)=3q, sum(K+L)=q.
    d_quotient_coefficient = (d_x_core - b_value + 3) % p_value
    b_quotient_coefficient = (b_x_core + 1 + b_value) % p_value
    assert d_quotient_coefficient == 0
    assert b_quotient_coefficient == 0

    coarse_b_minimum = p_value - b_value + 3  # |K|>=1 and |L|>=6.
    assert coarse_b_minimum > 8

    complementary_length_survivors = []
    for d_length in range(1, z_length):
        b_length = z_length - d_length
        if b_length <= 8:
            continue
        d_forbidden = 9 <= d_length <= 2 * p_value + 2
        b_forbidden = 9 <= b_length <= 2 * p_value + 2
        if not d_forbidden and not b_forbidden:
            complementary_length_survivors.append(d_length)
    assert complementary_length_survivors == list(range(1, 9))

    # Length eight would have to be F3.  Its positive X-core b-3 and its
    # tail U union P_1 union ... union P_t are not the unique pair (b,U).
    short_length_survivors = complementary_length_survivors[:-1]
    assert short_length_survivors == list(range(1, 8))
    packing_size_cap = 7 - b_value

    packing_rows = []
    for name, coefficients in PACKING_TYPES:
        assert sum(coefficients) == 3
        vectors = canonical_size_vectors(coefficients, packing_size_cap)
        vector_rows = []
        for sizes in vectors:
            packing_size = sum(sizes)
            d_length = b_value + packing_size
            b_length = z_length - d_length
            assert d_length <= 7
            assert b_length > 2 * p_value + 2
            families = allowed_short_families(d_length)
            assert families
            k_lower = 2 * p_value + 8 - 52 - packing_size
            k_upper = 2 * p_value - 2
            l_minimum_from_k_upper = max(6, 10 - packing_size)
            assert k_lower >= 1
            assert l_minimum_from_k_upper <= 52
            vector_rows.append(
                {
                    "atom_sizes": list(sizes),
                    "packing_size": packing_size,
                    "D_length": d_length,
                    "B_length": b_length,
                    "D_allowed_actual_sum_coefficients": families,
                    "K_lower_bound_from_L_at_most_52": k_lower,
                    "K_upper_bound_from_zero_sum_free": k_upper,
                    "L_minimum_from_K_upper_bound": l_minimum_from_k_upper,
                }
            )

        all_singletons = bool(vector_rows) and all(
            all(size == 1 for size in row["atom_sizes"]) for row in vector_rows
        )
        packing_rows.append(
            {
                "packing_type": name,
                "axis_coefficients": list(coefficients),
                "atom_count": len(coefficients),
                "closed_by_size_bound": not vector_rows,
                "all_surviving_atoms_forced_singletons": all_singletons,
                "surviving_size_vector_count": len(vector_rows),
                "surviving_size_vectors": vector_rows,
            }
        )

    if p_value == 233:
        triple = next(
            row for row in packing_rows if row["packing_type"] == "(1,1,1)"
        )
        assert not triple["closed_by_size_bound"]
        assert triple["all_surviving_atoms_forced_singletons"]
        assert [row["atom_sizes"] for row in triple["surviving_size_vectors"]] == [
            [1, 1, 1]
        ]
    else:
        triple = next(
            row for row in packing_rows if row["packing_type"] == "(1,1,1)"
        )
        assert triple["closed_by_size_bound"]
        assert not triple["surviving_size_vectors"]

    worst_k_lower = 2 * p_value + b_value - 51
    assert worst_k_lower == min(
        row["K_lower_bound_from_L_at_most_52"]
        for packing in packing_rows
        for row in packing["surviving_size_vectors"]
    )

    return {
        "p": p_value,
        "b": b_value,
        "X_multiplicity": x_multiplicity,
        "D_X_core_size": d_x_core,
        "B_X_core_size": b_x_core,
        "D_quotient_sum_coefficient_mod_p": d_quotient_coefficient,
        "B_quotient_sum_coefficient_mod_p": b_quotient_coefficient,
        "Z_length": z_length,
        "coarse_B_minimum_from_K_nonempty_and_L_at_least_6": coarse_b_minimum,
        "complementary_D_lengths_after_forbidden_window": complementary_length_survivors,
        "D_lengths_after_wrong_positive_core_length_8_gate": short_length_survivors,
        "packing_total_size_upper_bound": packing_size_cap,
        "K_uniform_lower_bound_from_L_at_most_52": worst_k_lower,
        "K_zero_sum_free_upper_bound": 2 * p_value - 2,
        "K_maximum_deficit_from_2p_minus_2": 49 - b_value,
        "packing_rows": packing_rows,
    }


def build_report() -> dict[str, object]:
    cases = [build_case(p_value, b_value) for p_value, b_value in CASES]
    report: dict[str, object] = {
        "schema": "unique_tail_forced_short_packing_block_v1",
        "scope": {
            "assumptions": [
                "p,b are (233,4) or (1399,5)",
                "X=x^(p-4), Z=X disjoint_union Y, and |Z|=3p+4",
                "U is a three-position unique tail with quotient sum -bq",
                "R=P_1 disjoint_union ... disjoint_union P_t disjoint_union K and Y=L disjoint_union R",
                "K is nonempty and projection-zero-sum-free, L contains an endpoint, and |L|<=52",
                "sum(K disjoint_union L)=q and sum(P_1 disjoint_union ... disjoint_union P_t)=3q",
                "the quotient-zero forbidden window is [9,2p+2]",
                "a positive-core length-eight F3 block must be the unique pair (b,U)",
            ],
            "conclusion": "sum_i |P_i|<=7-b; p=1399 packing (1,1,1) is closed; p=233 packing (1,1,1) forces three singleton atoms",
            "not_concluded": [
                "the p=233 packing (1,1,1) type is empty",
                "either (3) or (1,2) is empty for either prime",
                "all three forced packing types are empty",
                "the four non-forced packing types are empty",
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
            "p1399_closed_packing_types": ["(1,1,1)"],
            "p233_forced_three_singleton_packing_types": ["(1,1,1)"],
            "total_packing_type_rows": sum(
                len(case["packing_rows"]) for case in cases
            ),
            "total_surviving_size_vectors": sum(
                row["surviving_size_vector_count"]
                for case in cases
                for row in case["packing_rows"]
            ),
        },
        "status": "P1399_THREE_SINGLETON_PACKING_CLOSED__OTHER_FORCED_PACKINGS_REDUCED__GLOBAL_INCOMPLETE",
    }
    assert report["summary"]["total_packing_type_rows"] == 6
    assert report["summary"]["total_surviving_size_vectors"] == 10
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
