# Zhao：短零和子序列猜想的独立核验档案

本仓库保存对赵凯文笔记、作者回复、Claude 回应及相关文献来源的独立核验。它同时保存后续针对 \(G=C_5^4\) 端点问题的证明尝试、有限计算证据、独立复核和已发现的勘误。

仓库是研究档案，不把尚未闭合的端点写成定理。截至 2026-09-04 已独立认证的完整猜想 A、B 均为 **INCOMPLETE**，已认证的数值范围为

\[
19\le s_{\le14}(C_5^4)\le s_{\le13}(C_5^4)\le22,
\qquad K(C_5^4)\in\{10,14,15\}.
\]

2026-09-05 新收到的抢救稿给出了 B 的候选闭合证明，一条新的自包含“三份锚点”论证则候选关闭 A 中所有含三重值的情形。二者均通过本轮逐行初审，但尚未升级为独立认证结论；A 的平方自由与仅双重值两大结构仍未关闭。详见 [2026-09-05 收件审计](research/2026-09-05_zhao_completion/README.md)。此前的已认证状态见 [最新进展](research/2026-09-04_zhao_attack/answer_continue.md) 和 [全新上下文独立终审](research/2026-09-04_zhao_attack/proofs/verify_continuation_final_fresh.md)。

## 快速入口

- [原始用户材料](source-material/user-provided/)：赵笔记 PDF 与作者通信文本的原始副本。
- [来源索引](SOURCE_INDEX.md)：原始文件、候选来源和出处链。
- [复现说明](REPRODUCIBILITY.md)：代码、证书和形式化文件的入口及环境要求。
- [首次核验](research/2026-09-04_zhao_audit/verdict.md)：对原猜想及相关回应的逐项审计。
- [作者回复后的重构](research/2026-09-04_zhao_response/answer.md)：对“照搬”、原猜想与更正方向的分析。
- [逐源追查](research/2026-09-04_zhao_exact/source_audit.md)：Schmid–Zhuang、Gao–Geroldinger、Gao–Zhou、Luo 等来源的精确核对。
- [攻坚总报告](research/2026-09-04_zhao_attack/answer_continue.md)：最新局部定理、反例范围、失败路线和投入判断。
- [2026-09-05 收件审计](research/2026-09-05_zhao_completion/README.md)：B 候选闭合、四条 PRO 回报、未闭分支和验证等级。

## 目录结构

```text
source-material/
  user-provided/                  用户提供的原始文件
  candidate-sources/              按论文分组的候选来源原文副本
research/
  2026-09-04_zhao_audit/         第一轮独立核验及原始论文副本
  2026-09-04_zhao_response/      作者回复后的分析、Sloane 来源及形式化材料
  2026-09-04_zhao_exact/         Claude 来源说法的逐条核查及候选来源原文
  2026-09-04_zhao_attack/        端点攻坚、证明、程序证据、复核与勘误
  2026-09-05_zhao_completion/    抢救稿、PRO 首轮输出与收件审计
```

四个研究阶段均完整保留，包括相互独立的验证报告、失败分支和反例记录。`local_deps`、解释器缓存及编译缓存未纳入版本库；它们是可重建的本机依赖，不属于数学证据。

## 当前来源结论

条件 \(D(G)\le2\exp(G)-1\) 与 \(\exp(G)\ge(D(G)+1)/2\) 等价。现有证据支持如下来源链：

1. Gao–Zhou 2005 已在等价的大指数条件下给出相应下界；
2. Schmid–Zhuang 改进上界并提出三项相等的 Conjecture 4.1；
3. Gao–Geroldinger 2006 综述收录该结果；
4. Luo 后来证明其中的 \(\eta\) 等式，但没有在该文中证明完整的 \(s\) 等式。

这条文献链只能说明赵的条件和推理可能来自哪些既有工作，**不能仅凭文本相似性断定他实际“照搬”自某一篇**。证据边界和页码见 [逐源追查](research/2026-09-04_zhao_exact/source_audit.md)。

## 证据纪律

- 报告中的 `CORRECT` 只针对相应文件明确列出的范围，不自动外推到完整猜想。
- 有限枚举只在证明已经严格归约到对应有限类时使用。
- 历史错误和勘误均保留。例如 D3 原始 C# 证据曾因共享数组产生错误表格；修复版和独立 Python 重建重新确认了排除结论，但旧表不得继续引用。
- 文献文件仅用于出处核验。版权归原作者或出版方所有；仓库保持私有，未经权利审查不应公开分发。
