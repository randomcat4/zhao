# \(O_1\) 删点奇五次排除独立审计

STATUS: **CORRECT / PROVED SUBBRANCH / GLOBAL INCOMPLETE**

## 1. 审计对象

- proof：
  `proofs/unique_tail_p233_three_h8_m4_O1_single_deletion_quintic_exclusion.md`
- certificate：
  `unique_tail_p233_three_h8_m4_O1_single_deletion_quintic_search.py`
- report：
  `unique_tail_p233_three_h8_m4_O1_single_deletion_quintic_search_report.json`

冻结 SHA-256 为：

\[
\begin{array}{c|l}
\text{proof}&
\texttt{cb1683f5ad1692dd84908182aeed9fed8b485f802b32de02bc39edf6fc23b1ea}\\
\text{script}&
\texttt{7fcfa617a390d3157baf020cad8b03a83c156e9f636cdafbaa34b7744567648b}\\
\text{report}&
\texttt{e8c5c55208b7d1e92c60b49d00a4405e225fa1ee68a7182e900963dcd7e00e2d}
\end{array}
\tag{1}
\]

## 2. 逻辑量词审计

审计从生成积重新推导，而没有把旧 mixed 方向扫描当作输入。对任一
真实共同核位置 \(x\) 的标签 \(g\ne0\)，置
\(D=C\setminus\{x\}\)。严格有

\[
c(t)=d(t)-d(t-g),\qquad c(t)=q(t+\tau).
\tag{2}
\]

\(|D|=459=2p-7\) 给 \(d\) 的总次数至多五；奇数长度补集反射给

\[
d(t)=-d(-2\tau-g-t).
\tag{3}
\]

因此中心平移

\[
D_g(r)=d(r-\tau-g/2)
\tag{4}
\]

确为奇五次，并满足

\[
D_g(s+g/2)-D_g(s-g/2)=q(s).
\tag{5}
\]

特别核对了证明中最容易错的三个符号：式 (2) 的 \(t-g\)、式 (3)
的总和 \(-2\tau-g\)，以及式 (4) 的中心 \(-\tau-g/2\)，全部正确。

## 3. 普通无表示先于 signed 零

审计逐独立端点复核了

\[
d(0)=1,
\qquad
d(-\rho\sigma(A))=0
\quad
(\varnothing\ne A\subseteq F_i).
\tag{6}
\]

第二式的方向没有倒置。若存在 \(E\subseteq D\) 表示相反目标，则
\(E\dot\cup A\) 是 \(Q_i\) 的非空真零和字面子序列。对
\(A=F_i\) 仍然如此，因为它遗漏了被删位置 \(x\)。所以这里先有
普通表示不存在，再推出带符号系数为零；不存在由模 \(p\) 抵消反推
普通不存在的问题。

三个 fringe 各有十五个非空字面子集。四个例外中，每个状态的 45
条行均合并成 23 个不同目标；字面位置只在评价目标相同时合并，没有
被错误识别为同一位置。

## 4. 两份独立线性代数实现

主证书使用三参数通解。取 \(X(g)=1,Y(g)=0\)，中心差分

\[
\Delta_g:\mathcal O_5\longrightarrow\mathcal E_4
\tag{7}
\]

的秩为九，核恰为

\[
\langle Y,Y^3,Y^5\rangle.
\tag{8}
\]

证书逐 \(g\) 由五个显式中心反差分公式构造特解，并重新展开验证
\(\Delta_gD_g^{(0)}=q\)，随后只对三个核参数消元。

两名独立审计者没有调用该三参数程序，而是在十二维奇五次单项式空间
直接重建式 (5)--(6) 的矩阵。对四个状态以及每个
\(g\in\mathbb F_{233}^2\setminus\{0\}\)，都得到

\[
(\operatorname{rank}M,\operatorname{rank}[M\mid b])=(12,13).
\tag{9}
\]

故每个状态的独立秩对直方图均为

\[
\{(12,13):54\,288\}.
\tag{10}
\]

第二份审计还把差分右端符号和半平移符号的四种常见误置组合全部
复扫；所有组合仍为零幸存。这不是主证明的一部分，但确认最终空集
不是偶然依赖一个未察觉的符号约定。

## 5. 计数与裁决

主报告给出的顺序幸存数为

\[
\begin{array}{c|c|r|r|r|r}
z&\tau&d(0)=1&F_1&F_1,F_2&F_1,F_2,F_3\\ \hline
(58,174)&(59,174)&54\,060&1&1&0\\
(58,174)&(174,59)&54\,060&235&1&0\\
(60,176)&(59,174)&54\,060&1&1&0\\
(60,176)&(174,59)&54\,060&236&1&0.
\end{array}
\tag{11}
\]

四行在 \(F_1,F_2\) 后的唯一标签都为 \((-1,-1)\)，最后均被
\(F_3\) 的字面尾对 \(\{u_1,u_2\}\) 删除。总分母为

\[
4(233^2-1)=217\,152,
\tag{12}
\]

最终幸存数为零。

因此，结合已审定的四例外归约，固定 \(p=233,m=4\) 的
\(O_1=(0,1,1,4)\) 轨道严格不可实现。证明没有任意选择实际未知的
packing 方向，也不依赖 completion 定理。它不处理 \(O_2,O_3\)，
不关闭 180 个 outer rows，更不证明一般 \(A_p\)。
