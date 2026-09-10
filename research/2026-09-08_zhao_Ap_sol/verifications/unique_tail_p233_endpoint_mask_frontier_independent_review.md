# \(p=233\) 单行 endpoint-mask 前沿：独立复核

STATUS: **CORRECT IN THE DECLARED ONE-ROW MASK-ONLY SCOPE /
FINAL ARTIFACTS BOUND / GLOBAL INCOMPLETE**

## 1. 绑定工件

- 证明：proofs/unique_tail_p233_endpoint_mask_frontier.md，
  SHA-256
  0d4c032cf6b4ef05dc766eb52be540c866aa8f9af6c37fe66dcd90339ce4773b；
- 程序：unique_tail_p233_endpoint_mask_frontier.py，
  SHA-256
  2cc050182863e0ca85f24b72052095cebf6857159ec70bdad323f95405068df6；
- 报告：unique_tail_p233_endpoint_mask_frontier_report.json，
  SHA-256
  3a39fcc32b439c4a6d75a2ad1a50ca3e832ff2d1a98d11c7e9abe11e4f64b6a7；
- 报告规范证书：
  a622d427568cd8bc7082ee898602c6a6759237a97762b98193ce6e1c680dc107。

## 2. 独立裁决

独立使用不同 numeric-pattern 顺序重算，确认
decorated-1356 在 720 行中唯一，迹为 \((1,2,4,6)\)、长度为
\((8,7,8,8)\)，并严格复现

\[
27172,\ 206,\ 567,\ 12,\ 555,\ 26411
\]

这组原始轨道、containment 删除、duplicate 候选、重叠、净删除及
幸存轨道数。四条边交严格为 \(\{y\}\) 的原始/幸存计数也独立复现为
\(21/19\)。匿名位置的十五种非空成员型与残余度数方程一一对应；
零成员型由余数唯一确定，未被漏掉。首个 survivor 的
\(|K|=446\) 及四条补序列长度 \((464,465,464,464)\) 正确。

严格边界是：这里只枚举 720 行中的一行；26,411 个对象只是
mask 轨道，不是统一 \(\rho,q\)、高度、原子性和全短闭包下的 SAT
实现。因此不推出该行、720 行、固定 \(p=233\) 切片或全局 \(A_p\)
的 SAT/UNSAT。
