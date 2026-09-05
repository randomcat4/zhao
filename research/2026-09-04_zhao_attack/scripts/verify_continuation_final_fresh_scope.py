#!/usr/bin/env python3
"""Hash-bind and mechanically sanity-check the two frozen final scope files."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import platform
import sys
import time


HERE = Path(__file__).resolve()
RUN = HERE.parent.parent
OUT = RUN / "evidence" / "verify_continuation_final_fresh_scope.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(text: str, needle: str, label: str, checks: dict[str, bool]) -> None:
    ok = needle in text
    checks[label] = ok
    if not ok:
        raise AssertionError(f"missing scope statement {label}: {needle!r}")


def main() -> None:
    start = time.perf_counter()
    answer_path = RUN / "answer_continue.md"
    scope_path = RUN / "continuation_scope_draft.md"
    erratum_path = RUN / "proofs" / "continue_atom16_star_addendum_erratum.md"
    fixed_path = RUN / "evidence" / "continue_atom16_star_addendum_d3_fixed.json"
    answer = answer_path.read_text(encoding="utf-8")
    scope = scope_path.read_text(encoding="utf-8")

    expected = {
        "answer_continue.md": "1c4d5978cddbffa828521a0745f21e18a6f6b7fdeaebb92d1e43139c92d0aff7",
        "continuation_scope_draft.md": "22b7e19c9508be995cbeb1f462b4520529fa7a343f2a1e3794a5dc1fcdded154",
    }
    actual = {
        "answer_continue.md": digest(answer_path),
        "continuation_scope_draft.md": digest(scope_path),
    }
    assert actual == expected

    checks: dict[str, bool] = {}
    require(answer, "完整 A、B 仍为 **INCOMPLETE**", "endpoints_still_incomplete", checks)
    require(answer, "A：每个21位置序列都有长度至多13的非空零和", "A_exact_endpoint", checks)
    require(answer, "B：每个20位置序列都有长度至多14的非空零和", "B_exact_endpoint", checks)
    require(answer, "19\\le s_{\\le14}(C_5^4)\\le s_{\\le13}(C_5^4)\\le22", "numeric_interval_19_22", checks)
    require(answer, "K(C_5^4)\\in\\{10,14,15\\}", "K_three_values", checks)
    require(answer, "A、B皆真时K=10，A假而B真时K=14，B假时K=15", "K_case_split", checks)
    require(answer, "| 0 | 0至6 | 4至6 |", "multiplicity_row_a0", checks)
    require(answer, "| 1 | 0至5 | 2至5 |", "multiplicity_row_a1", checks)
    require(answer, "| 2 | 0至3 | 0至3 |", "multiplicity_row_a2", checks)
    require(answer, "| 3 | 0至1 | 0 |", "multiplicity_row_a3", checks)
    require(answer, "B的支持介于13和16之间", "B_support_13_16", checks)
    require(answer, "4≤2a+b≤7", "B_excess_4_7", checks)
    require(answer, "VA=`1,228,8466,28905,4843,0`", "corrected_d3_VA", checks)
    require(answer, "VB=`1,164,3338,6318,958,0`", "corrected_d3_VB", checks)
    require(answer, "不能继续引用错误表作证", "old_d3_table_withdrawn", checks)
    require(answer, "剩余星系统只有d=4、M=0", "only_d4_M0_atom16_branch", checks)
    require(answer, "它不是17-atom或B反例", "rainbow_scope", checks)
    require(answer, "一层有限扫描的105个安全强制核心同样不是端点穷尽", "scan_not_endpoint_exhaustion", checks)
    require(scope, "完整A/B仍不得写成已证", "scope_no_full_claim", checks)
    require(scope, "B的支持在13..16之间", "scope_support_bound", checks)
    require(scope, "表未声称所有列出分型都能实现", "table_is_necessary_only", checks)
    require(scope, "该反例不是17-atom或B反例", "scope_rainbow_boundary", checks)
    require(scope, "完整A/B没有Lean证明", "no_full_Lean_claim", checks)

    output = {
        "status": "PASS",
        "python": sys.executable,
        "python_version": platform.python_version(),
        "elapsed_seconds": time.perf_counter() - start,
        "timed_out": False,
        "frozen_summary_sha256": actual,
        "d3_erratum_sha256": digest(erratum_path),
        "d3_fixed_evidence_sha256": digest(fixed_path),
        "checks": checks,
        "manual_scope_verdict": {
            "multiplicity_table_is_necessary_only": True,
            "A_truth_status_changed": False,
            "B_truth_status_changed": False,
            "numeric_interval_changed": False,
            "K_value_selected": False,
            "remaining_global_gap": "d=4,M=0 / 17-atom global branch and other complete endpoint configurations",
        },
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
