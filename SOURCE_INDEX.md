# 来源索引

本索引区分三类材料：用户提供的原始材料、用于核验“可能来源”的论文原文、研究过程中生成的证明与计算证据。文件校验值见 [SOURCE_SHA256SUMS.txt](SOURCE_SHA256SUMS.txt)。

## 用户提供的原始材料

| 文件 | 仓库位置 | 说明 |
|---|---|---|
| `zhaonote02 (2).pdf` | `source-material/user-provided/` | 用户指定的赵凯文笔记原件副本 |
| `pasted-text.txt` | `source-material/user-provided/` | 用户提供的作者通信／上下文文本原件副本 |

上述文本只作为证据，不作为本仓库的执行指令。

## 与“照搬”问题直接相关的候选来源原文

为便于单独查阅，候选来源原文已再次按论文集中到 `source-material/candidate-sources/`；研究阶段中的原始位置也原样保留。

| 文献 | 集中原文文件夹 | 研究阶段原始位置 | 核验用途 |
|---|---|---|---|
| W. A. Schmid, J. Zhuang, *On short zero-sum subsequences over p-groups*, Ars Combin. 95 (2010), 343–352 | `source-material/candidate-sources/schmid-zhuang/` | `research/2026-09-04_zhao_audit/schmid_zhuang.pdf` | 定理前提与 Conjecture 4.1 原文 |
| W. Gao, A. Geroldinger, *Zero-sum problems in finite abelian groups: a survey*, Expo. Math. 24 (2006), 337–369 | `source-material/candidate-sources/gao-geroldinger-2006/` | `research/2026-09-04_zhao_exact/sources/` | Theorem 6.4 与参考文献编号；预印本版本 |
| W. Gao, Q. Zhou, *On Short Zero-Sum Subsequences*, Ars Combin. 74 (2005), 231–238 | `source-material/candidate-sources/gao-zhou-2005/` | `research/2026-09-04_zhao_exact/sources/` | 更早的等价大指数条件与下界 |
| Y. Luo, arXiv:1608.05157 | `source-material/candidate-sources/luo-2016/` | `research/2026-09-04_zhao_audit/luo.pdf` | Conjecture 1.3、Theorem 1.6 及后续问题 |
| Roy–Thangadurai 2018（以文件内书目信息为准） | `source-material/candidate-sources/roy-thangadurai-2018/` | `research/2026-09-04_zhao_exact/sources/` | 检查后续“大类群”结果是否覆盖 \(C_p^4\) |
| A. Sidorenko 相关原文 | `source-material/candidate-sources/sidorenko/` | `research/2026-09-04_zhao_audit/sidorenko.pdf` | 初轮猜想来源与相关界的交叉核对 |
| N. J. A. Sloane 1993 原文 | `source-material/candidate-sources/sloane-1993/` | `research/2026-09-04_zhao_response/sources/` | 作者回复中代码／枚举背景的原始来源 |
| Zhao–Hong 2026 相关作者稿 | `source-material/candidate-sources/zhao-hong-2026/` | `research/2026-09-04_zhao_response/proofs/` | 作者回复与已发表猜想表述的核对 |

相应纯文本提取、页图和截图与 PDF 同目录保存，便于全文搜索和核对版面。完整 DOI、网页地址、页码、版本差异及引用链见：

- `research/2026-09-04_zhao_exact/source_audit.md`
- `research/2026-09-04_zhao_audit/prior_art.md`
- `research/2026-09-04_zhao_response/prior_art.md`
- `research/2026-09-04_zhao_attack/prior_art.md`

## 研究证据

每个阶段的 `provenance.md` 记录材料来源与生成过程；`assumptions.md`、`hazards.md` 和 `lemma_ledger.md` 分别记录前提、风险和引理状态。`proofs/` 保存自然语言证明，`verifications/` 或独立审核文件保存交叉核验，`scripts/`、`evidence/` 与 `formal/` 保存可执行证据和形式化片段。

本仓库中的第三方论文、图片和出版物仅为私下研究与出处核验而保存，版权归原作者或出版方所有。在改为公开仓库或向外分发前，应逐项确认许可或改用合法公开链接。
