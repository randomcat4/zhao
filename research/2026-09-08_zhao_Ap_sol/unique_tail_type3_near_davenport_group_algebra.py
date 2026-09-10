#!/usr/bin/env python3
"""Exact endpoint and augmentation-fringe certificate for remaining type (3)."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "unique_tail_all_packing_short_blocks_report.json"
REPORT_PATH = HERE / "unique_tail_type3_near_davenport_group_algebra_report.json"
DEPENDENCY_PATHS = (
    HERE / "proofs" / "unique_tail_common_R_next.md",
    HERE / "verifications" / "unique_tail_common_R_next_independent_review.md",
    HERE / "proofs" / "unique_tail_forced_kernel_nonempty.md",
    HERE / "verifications" / "unique_tail_forced_kernel_nonempty_independent_review.md",
    HERE / "proofs" / "unique_tail_all_packing_short_blocks.md",
    HERE / "verifications" / "unique_tail_all_packing_short_blocks_independent_review.md",
    INPUT_PATH,
)


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def augmentation_fringe_dimension(delta: int) -> int:
    # Count u^i v^j with 0<=i,j<=p-1 and i+j>=2p-2-delta.
    # Writing deficits alpha=p-1-i, beta=p-1-j gives alpha+beta<=delta.
    return sum(delta - alpha + 1 for alpha in range(delta + 1))


def build_endpoint_rows() -> list[dict[str, int | str]]:
    source = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    rows: list[dict[str, int | str]] = []
    for case in source["cases"]:
        type_three = next(
            row for row in case["packing_rows"] if row["packing_type"] == "(3)"
        )
        for vector in type_three["vectors"]:
            if not vector["survives_q_fibre_gate"]:
                continue
            size = vector["atom_sizes"][0]
            for endpoint_length in (6, 7, 8):
                delta = endpoint_length + size - 9
                if delta < 0:
                    continue
                q_length = 2 * case["p"] + 8 - endpoint_length - size
                assert q_length == 2 * case["p"] - 1 - delta
                assert q_length <= 2 * case["p"] - 1
                deleted_degree = q_length - 1
                deleted_fringe_dimension = augmentation_fringe_dimension(delta)
                assert deleted_fringe_dimension == (delta + 1) * (delta + 2) // 2
                rows.append(
                    {
                        "p": case["p"],
                        "b": case["b"],
                        "P_size": size,
                        "endpoint_length": endpoint_length,
                        "Q_H_length": q_length,
                        "delta": delta,
                        "deleted_product_augmentation_degree": deleted_degree,
                        "deleted_product_fringe_dimension": deleted_fringe_dimension,
                        "deleted_product_nonzero": "by zero-sum-freeness after deleting k",
                        "full_product_top_identity_coefficient": (
                            2 if delta == 1 else "not_used"
                        ),
                    }
                )
    return rows


def build_report() -> dict[str, object]:
    rows = build_endpoint_rows()
    assert len(rows) == 9
    delta_counts = {
        delta: sum(row["delta"] == delta for row in rows) for delta in (0, 1, 2)
    }
    assert delta_counts == {0: 5, 1: 3, 2: 1}
    assert {row["delta"] for row in rows} == {0, 1, 2}
    assert {
        row["delta"]: row["deleted_product_fringe_dimension"] for row in rows
    } == {0: 1, 1: 3, 2: 6}

    report: dict[str, object] = {
        "schema": "unique_tail_type3_near_davenport_group_algebra_v1",
        "scope": {
            "assumptions": [
                "p,b are (233,4) or (1399,5)",
                "the remaining common packing has type (3) with one rho-atom P",
                "for every zero-core endpoint H, Q_H=K disjoint_union (L minus H) is a rho-atom",
                "the common rho-zero-sum-free kernel K is nonempty",
                "zero-core endpoint lengths are six, seven, or eight",
            ],
            "conclusion": (
                "all possible Q_H lengths are within delta=0,1,2 of the C_p^2 Davenport maximum; deleting a common k in K gives a nonzero product in an augmentation fringe of dimension 1,3,6, with exact J identities at delta zero and for the full product at delta one"
            ),
            "not_concluded": [
                "the common augmentation factor can be cancelled",
                "the signed coefficients are nonnegative counts",
                "any endpoint row is realizable",
                "type (3) is empty",
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
        "endpoint_rows": rows,
        "summary": {
            "endpoint_row_count": len(rows),
            "delta_counts": delta_counts,
            "deleted_product_fringe_dimensions": {"0": 1, "1": 3, "2": 6},
            "delta_zero_identity": (
                "Psi_(K minus k) Psi_(L minus H) = J for every k in K"
            ),
            "delta_one_full_identity": "Psi_K Psi_(L minus H) = 2J",
            "shared_factors": ["Psi_(K minus k)", "Psi_K"],
        },
        "status": "TYPE_3_NEAR_DAVENPORT_SHARED_AUGMENTATION_FRINGE__GLOBAL_INCOMPLETE",
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
