# 完成丰富的近最大原子族：独立审计

STATUS: **CORRECT**

本审计绑定：

| 文件 | SHA-256 |
|---|---|
| proofs/unique_tail_completion_rich_near_max_atom_family.md | b7ce58d855a9f3e32bad4dedd0a8d6538f8519a974550f1c7598fa403054b511 |
| unique_tail_completion_rich_near_max_atom_family.py | 27890b89abe4977fdc7dfe8c042c8efb1de8b874ccfda18befd6148dfcab58fe |
| unique_tail_completion_rich_near_max_atom_family_report.json | 96ee5f09052e51845867aa09345afa54e51e9a22d49ab8c3ab377e91599df768 |

报告内嵌规范证书

b4691c4469b06788f31c7419f277a87479c18b31c20334776a489405e3cbc591

已经独立重算命中。

对交换 \(e,f\) 后的构造

\[
Q=f^{p-1}e^{p-3}(2e)(e+f)
\]

从坐标重新检查得到：

- \(Q\) 只有空位置集与全位置集为零和，故是长度 \(2p-2\) 原子；
- 删除任意 \(e\)、任意 \(f\) 或唯一的 \(e+f\) 后，普通子集和覆盖
  整个 \(C_p^2\)；
- 删除唯一的 \(2e\) 后，恰漏仿射线
  \(-e+\langle f\rangle\)，不是只漏一个目标。

所以恰有 \(2p-3\) 个 complete 删除。字面子集动态规划在
\(p=5,7\) 独立复核了 sumset 大小；配套脚本又在 \(p=5,7,233\)
检查了坐标分类、删点覆盖与缺失线。

令 \(q(2e)=1\)，其余 \(Q\) 位置的 \(q\)-坐标为零，再取 packing
高度 \(1,2\)。任意内部子集的 \(q\)-和都在 \(\{0,1\}\)，分别落在
两个 packing 单点允许的内部高度集合
\(\{0,1,2\}\) 与 \(\{-1,0,1\}\) 中。因此全部 mixed 蕴含逐实际
子集成立，不依赖投影方向 \(s\)。

最终裁决为 **CORRECT**。该构造只证明单个长补在投影/\(q\)-mixed
层有巨大余量；它不是多端点统一位置模型，也不满足或检查全部自动
短块、实际高度和全局 \(A_p\)。
