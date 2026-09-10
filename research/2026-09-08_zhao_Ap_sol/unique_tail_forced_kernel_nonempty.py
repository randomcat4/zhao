#!/usr/bin/env python3
"""Finite arithmetic regression for the forced-type K-nonempty theorem."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / "unique_tail_forced_kernel_nonempty_report.json"


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def build_report() -> dict[str, object]:
    rows = []
    for p_value, b_value in ((233, 4), (1399, 5)):
        core = p_value - b_value - 1
        assert 0 <= core <= p_value - 4
        local_rows = []
        for l_size in range(6, 53):
            outside_tail_size = l_size - 3
            total_length = core + outside_tail_size
            assert 9 <= total_length <= 2 * p_value + 2
            local_rows.append(
                {
                    "L_size": l_size,
                    "outside_tail_size": outside_tail_size,
                    "axis_coefficient": b_value + 1,
                    "X_core_size": core,
                    "quotient_sum_coefficient_mod_p": (
                        b_value + 1 + core
                    )
                    % p_value,
                    "total_length": total_length,
                    "forbidden": True,
                }
            )
        rows.append(
            {
                "p": p_value,
                "b": b_value,
                "X_multiplicity": p_value - 4,
                "X_core_size": core,
                "minimum_forbidden_length": local_rows[0]["total_length"],
                "maximum_forbidden_length": local_rows[-1]["total_length"],
                "L_size_rows": local_rows,
            }
        )
    report: dict[str, object] = {
        "schema": "unique_tail_forced_kernel_nonempty_v1",
        "scope": {
            "assumptions": [
                "p,b are (233,4) or (1399,5)",
                "the unique tail U has three actual positions and quotient sum -bq",
                "at least one endpoint E has size 6..8 and quotient sum zero",
                "L contains U and all endpoints and has size at most 52",
                "in a forced common-remainder atom type K is empty, so Q_E=L\\E has quotient sum q",
            ],
            "conclusion": "K empty forces the forbidden quotient-zero actual block X_(p-b-1) disjoint_union (L\\U)",
            "not_concluded": [
                "the three forced packing types are empty",
                "the K nonempty subbranch is empty",
                "any of the other four packing types is empty",
                "A_p",
            ],
        },
        "rows": rows,
        "status": "FORCED_TYPES_REQUIRE_NONEMPTY_COMMON_KERNEL__GLOBAL_INCOMPLETE",
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
