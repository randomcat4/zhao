# \(p=233\) singleton 长八删点覆盖：独立审计

STATUS: **CORRECT / 461 NON-TAIL COMPLETE DELETIONS / GLOBAL INCOMPLETE**

本审计绑定

proofs/unique_tail_p233_singleton_completion_cover.md

的 SHA-256

ade124bf213dfb0cec48731b7c2c49414bf2d121fb341678d97d70db668e4653。

外部承重仍是 Reiher 的 Property B；仓库内依赖的近最大原子完成二分
与三个尾对允许域空交均已有独立审计。

独立解析 720 行报告得到：singleton 长七端点数只可能为零
（180 行）或一（540 行），所以至少两个 singleton 端点长八。对长八
端点 \(i\)，令 \(B_i\) 为它的非尾坏删点集。若
\(x,y\in B_i\) 且 \(x\ne y\)，两次近最大完成分别给

\[
\operatorname{supp}\rho(Q_i\setminus\{x\})\subseteq\mathcal D_i,
\qquad
\operatorname{supp}\rho(Q_i\setminus\{y\})\subseteq\mathcal D_i.
\]

具体 Property-B 标准域可以随删点改变；这里只把它们放入固定尾对的
总允许域 \(\mathcal D_i\)。两删点序列之并为完整 \(Q_i\)，故

\[
|B_i|\ge2\Longrightarrow
\operatorname{supp}\rho(Q_i)\subseteq\mathcal D_i.
\]

若所有长八 singleton 都有至少两个坏删点，则它们把共同核放入对应
允许域；若另有一个长七 singleton，Property B 直接提供第三个域。
于是任一共同核非零标签同时落入三个允许域，违反三域空交。因此

\[
\min_{i\in I_8}|B_i|\le1.
\]

每个 singleton \(Q_i\) 长 464 且恰含两个尾位置，所以有 462 个非尾
位置，得到一个统一端点至少有 461 个 complete 删除；限制回
\(|K|\ge435\) 则至少有 434 个共同核 complete 删除。

审计特别核对：被删位置的例外没有被偷塞回单次完成域；两次不同删点
恰好补回彼此例外。最终裁决为 **CORRECT**。该结论不控制 \(q\)、
表示长度或实际高度，因而不单独删除 outer row。
