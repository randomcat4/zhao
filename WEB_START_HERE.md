# 网页版研究入口：不要重做已闭合的 (p=5)

更新时间：2026-09-05

## 已经完成并冻结

对仓库所用定义

\[
K(G)=\min\{M\in[\exp(G),D(G)-1]:
\forall m\in[M,D(G)-1],\ s_{\le m}(G)\le2D(G)-m\},
\]

已经证明并独立终审：

\[
\boxed{K(C_5^4)=10}.
\]

等价的两个最后端点均成立：

\[
s_{\le13}(C_5^4)\le21,
\qquad
s_{\le14}(C_5^4)\le20.
\]

主裁决是 `research/2026-09-05_zhao_completion/fresh_audit/HARVEST_VERDICT.md`。平方自由终支有两条已通过路线：独立投影证书证明和完整重放的稠密纤维搜索。不要重新搜索 (p=5) 反例，不要把历史 `INCOMPLETE` 文件当作当前状态。

赵文中的一般半值猜想已经有反例。以下无限族也已经证明：

\[
K(C_2^r\oplus C_n)=n=\exp(G)quad(r=2,3, 4\mid n),
\]

以及秩二族 (K(C_2\oplus C_{2t})=2t)。所以对全部有限阿贝尔群，下面三种形式都不能成立：

\[
K=(D+1)/2+o(1),\qquad K=(D+1)/2+O(1),\qquad K/D\to1/2.
\]

## 唯一优先目标

研究所有素数 (p\ge5) 的受限猜想

\[
\boxed{K(C_p^4)=2p}.
\]

已有符号归约：对每个素数 (p\ge5)，

\[
K(C_p^4)\in\{2p,3p-1,3p\}.
\]

只需证明以下两个端点：

### 端点 (A_p)

每个长度 (5p-4) 的 (C_p^4) 上序列，都有长度至多 (3p-2) 的非空零和子序列；即

\[
s_{\le3p-2}(C_p^4)\le5p-4.
\]

### 端点 (B_p)

每个长度 (5p-5) 的 (C_p^4) 上序列，都有长度至多 (3p-1) 的非空零和子序列；即

\[
s_{\le3p-1}(C_p^4)\le5p-5.
\]

两者都成立即推出 (K(C_p^4)=2p)。只证明一个固定素数、低支撑情形、平方自由情形或某个重数型均不算完成。

## 建议研究顺序

1. 从 `research/2026-09-04_zhao_exact/proofs/rank4_three_values.md` 核对一般 (p) 的三候选值归约。
2. 从 `research/2026-09-05_zhao_completion/fresh_audit/HARVEST_VERDICT.md` 读取 (p=5) 的最终覆盖，不读历史聊天来猜状态。
3. 制作“依赖于 (p=5)”与“对一般 (p) 成立”的引理表。优先检查增广理想次数、删除同余、投影轮廓、原子长度、平方自由常数及三维商群短零和界。
4. 先尝试得到对一般 (p) 的解析归约；计算 (p=7) 只用来发现反例或结构，不能替代全称证明。
5. 每个候选证明必须分别检查位置重数、补集长度、模 (p) 符号和有限搜索量词覆盖。

## 禁止外推

- 不得从 (p=5) 单点宣布所有 (p) 成立。
- 不得把 (K(C_p^4)=2p) 写成已知定理。
- 不得重新提出适用于所有有限阿贝尔群的半 (D(G)) 公式。
- 不得把“没有找到反例”写成证明。
- 不得把赵所说“照搬”唯一归于某篇论文；当前只确认可能的来源链。
- 不得把二元线性 \([12,5,5]\) 码不存在性称为新事实。

## 最短证据入口

- `README.md`
- `research/2026-09-05_zhao_completion/fresh_audit/HARVEST_VERDICT.md`
- `research/2026-09-05_zhao_completion/fresh_audit/projection_proof_review.md`
- `research/2026-09-05_zhao_completion/fresh_audit/B_endpoint_review.md`
- `research/2026-09-05_zhao_completion/fresh_audit/dense_fibre_ci_replay.md`
- `research/2026-09-04_zhao_exact/verifications/final_precision.md`
- `research/2026-09-04_zhao_exact/source_audit.md`

