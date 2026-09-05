# 复现与审计入口

本仓库以“先读证明范围，再运行对应证据”为原则。不要把某个脚本成功运行等同于完整猜想已被证明。

## 建议阅读顺序

1. `research/2026-09-04_zhao_attack/problem.md`
2. `research/2026-09-04_zhao_attack/assumptions.md`
3. `research/2026-09-04_zhao_attack/answer_continue.md`
4. 对应的 `proofs/*.md`
5. 对应的独立审核与 `verifications/`
6. 最后检查脚本、证书和原始输出

最新全局范围核查入口为：

```powershell
python research/2026-09-04_zhao_attack/scripts/verify_continuation_final_fresh.py
python research/2026-09-04_zhao_attack/scripts/verify_continuation_final_fresh_scope.py
```

不同证明分支使用的具体入口记录在各证明文件、`route_registry.md`、`rounds.md` 与独立审核报告中。大型 JSON/JSONL 文件是已保存的有限枚举结果或证书，不应在不了解其生成脚本和归约范围时单独引用。

## 运行环境

- Python 3；多数脚本只使用标准库，少数探索脚本可能需要额外数学／优化包。
- PowerShell 7，用于 `.ps1` 枚举和流水线。
- .NET SDK／C#，用于若干高吞吐有限搜索。
- Node.js，用于个别 JavaScript 独立核验。
- Lean 4.30，用于 `research/2026-09-04_zhao_attack/formal/` 中的局部证书。

本机安装目录、包缓存、编译缓存和 `local_deps` 未提交。正式复现前，请先阅读目标脚本顶部的参数和相邻证明文件；部分完整搜索耗时和磁盘占用较大。

## 关键独立审核

- `research/2026-09-04_zhao_attack/proofs/verify_continuation_final_fresh.md`
- `research/2026-09-04_zhao_attack/verifications/verify_seven_fresh.md`
- `research/2026-09-04_zhao_attack/evidence/verify_h11_final_fresh_report.md`
- `research/2026-09-04_zhao_attack/proofs/verify_root_continue_all_H12.md`
- `research/2026-09-04_zhao_attack/proofs/verify_root_continue_support17_exclusion.md`

若证明正文、历史审核与勘误冲突，以明确标记的最新勘误及其独立重建为准。D3 分支必须同时查阅：

- `research/2026-09-04_zhao_attack/proofs/continue_atom16_star_addendum.md`
- `research/2026-09-04_zhao_attack/proofs/continue_atom16_star_addendum_erratum.md`
- `research/2026-09-04_zhao_attack/evidence/verify_h11_final_fresh_d3_independent.json`

## 原始材料完整性

`SOURCE_SHA256SUMS.txt` 保存用户原始材料及候选来源原文／页图的 SHA-256。可在 PowerShell 中抽查：

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath "source-material/user-provided/zhaonote02 (2).pdf"
```

校验文件用于确认仓库副本未在整理过程中被修改；它不认证第三方网站上的未来版本。

