#!/usr/bin/env python3
"""Finite arithmetic for the p=233 Property-B three-atom exclusion.

The script verifies the tail-direction intersections and all numerical margins.
It does not verify Reiher's external Property B theorem.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


P = 233
HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_p233_property_b_three_atom_exclusion_report.json"


def sub(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return ((x[0] - y[0]) % P, (x[1] - y[1]) % P)


def smul(c: int, x: tuple[int, int]) -> tuple[int, int]:
    return ((c * x[0]) % P, (c * x[1]) % P)


def det(x: tuple[int, int], y: tuple[int, int]) -> int:
    return (x[0] * y[1] - x[1] * y[0]) % P


def punctured_span(x: tuple[int, int]) -> set[tuple[int, int]]:
    return {smul(c, x) for c in range(1, P)}


def main() -> None:
    w = {1: (1, 0), 2: (0, 1), 3: (P - 1, P - 1)}
    assert tuple((w[1][j] + w[2][j] + w[3][j]) % P for j in range(2)) == (0, 0)

    tail_pairs = {1: (w[2], w[3]), 2: (w[1], w[3]), 3: (w[1], w[2])}
    allowed_repeated = {}
    for i, (a, b) in tail_pairs.items():
        allowed_repeated[i] = {a, b} | punctured_span(sub(a, b))
        assert len(allowed_repeated[i]) == P + 1

    pair_intersections = {
        "1-2": allowed_repeated[1] & allowed_repeated[2],
        "1-3": allowed_repeated[1] & allowed_repeated[3],
        "2-3": allowed_repeated[2] & allowed_repeated[3],
    }
    assert pair_intersections == {"1-2": {w[3]}, "1-3": {w[2]}, "2-3": {w[1]}}
    assert set.intersection(*allowed_repeated.values()) == set()

    atom_length = 2 * P - 1
    repeated_count = P - 1
    max_outside_kernel = 30
    repeated_inside_kernel = repeated_count - max_outside_kernel
    assert atom_length == 465
    assert repeated_inside_kernel == 202
    assert 3 * repeated_inside_kernel > atom_length

    # If g_i=g_j is the shared tail forced by the pair intersections, the two
    # corresponding affine cosets are parallel.  The displayed determinant is
    # nonzero exactly when the cosets are distinct.
    parallel_coset_separations = {
        "g1=g2=w3": {
            "direction": w[3],
            "base_difference": sub(w[1], w[2]),
        },
        "g1=g3=w2": {
            "direction": w[2],
            "base_difference": sub(w[1], w[3]),
        },
        "g2=g3=w1": {
            "direction": w[1],
            "base_difference": sub(w[2], w[3]),
        },
    }
    determinants = {}
    for name, data in parallel_coset_separations.items():
        value = det(data["base_difference"], data["direction"])
        assert value != 0
        determinants[name] = value

    report = {
        "scope": "P233_ALL_LENGTH7_RANK2_THREE_SINGLETON_ENDPOINTS",
        "status": "FINITE_REDUCTION_VERIFIED/EXTERNAL_PROPERTY_B_DEPENDENCY/PENDING_INDEPENDENT_REVIEW/GLOBAL_INCOMPLETE",
        "p": P,
        "tail_normal_form": [list(w[i]) for i in range(1, 4)],
        "atom_length": atom_length,
        "property_b_repeated_count": repeated_count,
        "max_Qi_outside_K": max_outside_kernel,
        "minimum_repeated_occurrences_in_K": repeated_inside_kernel,
        "all_distinct_capacity_test": {
            "required_positions": 3 * repeated_inside_kernel,
            "available_upper_bound": atom_length,
            "contradiction": 3 * repeated_inside_kernel > atom_length,
        },
        "allowed_repeated_label_set_sizes": [len(allowed_repeated[i]) for i in range(1, 4)],
        "pair_intersections": {
            key: [list(x) for x in sorted(value)] for key, value in pair_intersections.items()
        },
        "triple_intersection": [],
        "equal_pair_parallel_coset_determinants": determinants,
        "external_dependency": {
            "author": "Christian Reiher",
            "title": "A Proof of the Theorem According to Which Every Prime Number Possesses Property B",
            "year": 2010,
            "result": "Theorem 10.2: Every prime number has property B.",
            "definition_used": "Every length 2p-1 minimal zero-sum sequence over F_p^2 is simple, hence has a term repeated p-1 times and all remaining terms in one affine coset of its span.",
            "url": "https://www.math.uni-rostock.de/math/pub/preprints/preprint/2010/pre10_01.pdf",
        },
        "conclusion": "The three Q_i cannot simultaneously be globally labelled C_233^2 maximal atoms with a common kernel and the certified rank-two tail normal form.",
        "not_claimed": [
            "other endpoint-length patterns are excluded",
            "the full p=233 problem is excluded",
            "global A_p",
        ],
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    report["certificate_sha256"] = hashlib.sha256(canonical).hexdigest()
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
