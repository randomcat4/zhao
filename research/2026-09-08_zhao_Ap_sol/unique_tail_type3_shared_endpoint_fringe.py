#!/usr/bin/env python3
"""Exact shared-factor fringe relations for pairs of type-(3) endpoints."""

from __future__ import annotations

from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "unique_tail_type3_near_davenport_group_algebra_report.json"
REPORT_PATH = HERE / "unique_tail_type3_shared_endpoint_fringe_report.json"
DEPENDENCY_PATHS = (
    INPUT_PATH,
    HERE / "proofs" / "unique_tail_type3_near_davenport_group_algebra.md",
    HERE / "verifications" / "unique_tail_type3_near_davenport_group_algebra_independent_review.md",
    HERE / "proofs" / "unique_tail_forced_common_atoms_attack.md",
    HERE / "verifications" / "unique_tail_seven_type_fresh_independent_review.md",
)


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def full_state(delta: int) -> str:
    return {
        0: "zero_in_I^(2p-1)",
        1: "2J_in_I^(2p-2)",
        2: "element_of_I^(2p-3)_with_identity_coefficient_0",
    }[delta]


def deleted_state(delta: int) -> str:
    return {
        0: "J",
        1: "nonzero_in_3_dimensional_I^(2p-3)_fringe_with_identity_coefficient_1",
        2: "nonzero_in_6_dimensional_I^(2p-4)_fringe_with_identity_coefficient_1",
    }[delta]


def pair_consequence(delta_low: int, delta_high: int) -> str:
    pair = (delta_low, delta_high)
    return {
        (0, 0): "D_k(Psi_A-Psi_B)=0 because both deleted endpoint products equal J",
        (0, 1): "D Psi_B=0, D Psi_A=2J, and D_k Psi_B=J",
        (0, 2): "D Psi_B=0 and D_k Psi_B=J; the A side remains in the delta-2 fringe",
        (1, 1): "D(Psi_A-Psi_B)=0 because both full endpoint products equal 2J",
        (1, 2): "D Psi_B=2J; the A side remains in the delta-2 fringe",
        (2, 2): "only the two shared-factor six-dimensional deleted fringes are forced",
    }[pair]


def build_rows() -> tuple[list[dict[str, object]], list[dict[str, int]]]:
    source = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    grouped: dict[tuple[int, int], list[dict[str, object]]] = {}
    for row in source["endpoint_rows"]:
        grouped.setdefault((row["p"], row["P_size"]), []).append(row)

    pair_rows: list[dict[str, object]] = []
    petal_rows: list[dict[str, int]] = []
    for (p, p_size), endpoints in sorted(grouped.items()):
        endpoints.sort(key=lambda row: row["endpoint_length"])
        for lower, upper in combinations_with_replacement(endpoints, 2):
            h_low = lower["endpoint_length"]
            h_high = upper["endpoint_length"]
            delta_low = lower["delta"]
            delta_high = upper["delta"]
            assert delta_high - delta_low == h_high - h_low
            intersections = list(range(1, h_low))
            petals = []
            for intersection_size in intersections:
                a_size = h_low - intersection_size
                b_size = h_high - intersection_size
                assert a_size >= 1 and b_size >= 1
                assert b_size - a_size == delta_high - delta_low
                petal = {
                    "p": p,
                    "P_size": p_size,
                    "delta_low": delta_low,
                    "delta_high": delta_high,
                    "intersection_size": intersection_size,
                    "A_size": a_size,
                    "B_size": b_size,
                }
                petals.append(petal)
                petal_rows.append(petal)
            pair_rows.append(
                {
                    "p": p,
                    "P_size": p_size,
                    "endpoint_lengths": [h_low, h_high],
                    "deltas": [delta_low, delta_high],
                    "proper_nonempty_petal_size_pairs": [
                        [row["A_size"], row["B_size"]] for row in petals
                    ],
                    "factorization": {
                        "D": "Psi_K Psi_(L minus (H union J))",
                        "D_k": "Psi_(K minus k) Psi_(L minus (H union J))",
                        "Q_H_full": "D Psi_B",
                        "Q_J_full": "D Psi_A",
                        "Q_H_deleted_k": "D_k Psi_B",
                        "Q_J_deleted_k": "D_k Psi_A",
                    },
                    "lower_full_state": full_state(delta_low),
                    "upper_full_state": full_state(delta_high),
                    "lower_deleted_state": deleted_state(delta_low),
                    "upper_deleted_state": deleted_state(delta_high),
                    "shared_factor_consequence": pair_consequence(
                        delta_low, delta_high
                    ),
                }
            )
    return pair_rows, petal_rows


def build_report() -> dict[str, object]:
    pair_rows, petal_rows = build_rows()
    pair_type_counts: dict[str, int] = {}
    for row in pair_rows:
        key = "-".join(str(value) for value in row["deltas"])
        pair_type_counts[key] = pair_type_counts.get(key, 0) + 1
    assert len(pair_rows) == 14
    assert len(petal_rows) == 86
    assert pair_type_counts == {
        "0-0": 5,
        "0-1": 3,
        "0-2": 1,
        "1-1": 3,
        "1-2": 1,
        "2-2": 1,
    }

    report: dict[str, object] = {
        "schema": "unique_tail_type3_shared_endpoint_fringe_v1",
        "scope": {
            "assumptions": [
                "all assumptions of the audited type-(3) near-Davenport group-algebra theorem",
                "H and J are distinct actual zero-core endpoints in the same instance",
                "all endpoints share an actual position y, so 1<=|H intersection J|",
                "actual atomicity of Z makes both exclusive petals nonempty",
            ],
            "conclusion": (
                "the full and common-k-deleted products of every endpoint pair factor through the same actual-position bases D and D_k; all six possible delta pairs have the stated exact top-fringe, annihilation, or separator relations"
            ),
            "not_concluded": [
                "a common group-algebra factor can be cancelled",
                "every length class occurs in one instance",
                "any pair row is realizable",
                "type (3) is empty",
                "A_p",
            ],
        },
        "dependencies_sha256": {
            str(path.relative_to(HERE)).replace("\\", "/"): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in DEPENDENCY_PATHS
        },
        "pair_rows": pair_rows,
        "summary": {
            "conditional_length_pair_row_count": len(pair_rows),
            "literal_petal_size_row_count": len(petal_rows),
            "delta_pair_counts": pair_type_counts,
            "all_delta_pairs": sorted(pair_type_counts),
            "delta_0_1_full_separator": "D Psi_B=0 while D Psi_A=2J",
            "same_delta_0_deleted_annihilator": "D_k(Psi_A-Psi_B)=0",
            "same_delta_1_full_annihilator": "D(Psi_A-Psi_B)=0",
        },
        "status": "TYPE_3_ALL_ENDPOINT_PAIRS_SHARE_EXACT_FRINGE_FACTORS__GLOBAL_INCOMPLETE",
    }
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
