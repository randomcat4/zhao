# 型 (3) 余部原子的近 Davenport 群代数边缘

STATUS: **PROVED_REDUCTION / PENDING_INDEPENDENT_REVIEW / GLOBAL_INCOMPLETE**

## 1. 范围与结论

固定剩余共同 packing 型 \((3)\)。于是存在同一个实际位置块
\(P\subset R\)，使

\[
\rho(\bar\sigma(P))=0,\qquad
\bar\sigma(P)=3q,\qquad s:=|P|\in\{1,2,3\},
\tag{1}
\]

而对每个零核心端点 \(H\)，

\[
Q_H=K\mathbin{\dot\cup}(L\setminus H)
\tag{2}
\]

是 \(C_p^2\) 中的零和原子。已经认证的共同核定理还给出

\[
K\ne\varnothing.
\tag{3}
\]

若 \(h=|H|\)，则

\[
|Q_H|=2p+8-h-s=2p-1-\delta_H,
\qquad \delta_H:=h+s-9.
\tag{4}
\]

原子上界 \(|Q_H|\le D(C_p^2)=2p-1\) 迫使
\(\delta_H\ge0\)。当前全部端点因此只落在

\[
\boxed{\delta_H\in\{0,1,2\}.}
\tag{5}
\]

本文把这些近 Davenport 原子的**全部带符号内部子集和**放入同一个
群代数边缘，并保留所有端点共享的 \(K\)-因子。

## 2. 增广理想的顶端三层

令

\[
A=\mathbb F_p[C_p^2],\qquad
I=\ker(A\longrightarrow\mathbb F_p)
\tag{6}
\]

为增广理想。选取 \(C_p^2\) 的基后有

\[
A\cong\mathbb F_p[u,v]/(u^p,v^p),
\qquad I=(u,v).
\tag{7}
\]

因此

\[
I^{2p-1}=0,\qquad
I^{2p-2}=\mathbb F_pJ,
\qquad
J:=\sum_{g\in C_p^2}X^g=u^{p-1}v^{p-1}.
\tag{8}
\]

更一般地，对 \(0\le\delta\le2\)，

\[
\dim I^{2p-2-\delta}
=\#\{(i,j):0\le i,j\le p-1, i+j\ge2p-2-\delta\}
=\binom{\delta+2}{2}.
\tag{9}
\]

所以这三层维数依次为

\[
\boxed{1,\quad3,\quad6.}
\tag{10}
\]

## 3. 删除共同核位置后的非零积

对带位置序列 \(T\) 定义

\[
\Psi_T:=\prod_{z\in T}(1-X^{\rho(\bar z)})\in A.
\tag{11}
\]

固定任意共同位置 \(k\in K\)。因为 \(Q_H\) 是原子，删除
\(k\) 后的 \(Q_H\setminus\{k\}\) 零和自由。展开 (11) 时，单位元
系数只有空子集的贡献，恰为一；所以

\[
0\ne\Psi_{Q_H\setminus\{k\}}
\in I^{|Q_H|-1}=I^{2p-2-\delta_H}.
\tag{12}
\]

实际位置分解 (2) 同时给出

\[
\boxed{
\Psi_{Q_H\setminus\{k\}}
=\Psi_{K\setminus\{k\}}\Psi_{L\setminus H}.}
\tag{13}
\]

式 (13) 对所有端点使用同一个 \(\Psi_{K\setminus\{k\}}\)，而右侧
分别落在 (10) 的一维、三维或六维边缘。这不是给不同端点独立选择
一个抽象原子。

当 \(\delta_H=0\) 时，(8)、(12) 与单位元系数一进一步给出精确式

\[
\boxed{
\Psi_{K\setminus\{k\}}\Psi_{L\setminus H}=J.}
\tag{14}
\]

换言之，对每个目标 \(g\in C_p^2\)，

\[
\sum_{E\subseteq Q_H\setminus\{k\}\atop
      \rho(\bar\sigma(E))=g}(-1)^{|E|}=1.
\tag{15}
\]

这是全部内部子集的带符号恒等式，不是非负表示数等式。

## 4. \(\delta=1\) 的完整原子积

若 \(\delta_H=1\)，则 \(|Q_H|=2p-2\) 为偶数。因 \(Q_H\) 是
原子，其零和子集只有空集与全集。因此完整积 \(\Psi_{Q_H}\) 的
单位元系数为

\[
1+(-1)^{2p-2}=2.
\tag{16}
\]

另一方面 \(\Psi_{Q_H}\in I^{2p-2}=\mathbb F_pJ\)。由 (2) 得到

\[
\boxed{\Psi_K\Psi_{L\setminus H}=2J.}
\tag{17}
\]

删除积仍由 (13) 给出一个三维非零边缘条件。式 (17) 则把该层进一步
压回一条所有端点共享 \(\Psi_K\) 的精确恒等式。

当 \(\delta_H=2\) 时，(12)--(13) 只给六维非零边缘；奇长度完整
原子的单位元处空集与全集贡献相消，不能仿照 (16) 把完整积误写成
非零的 \(J\) 倍数。

## 5. 九个端点长度行

结合 \(6\le h\le8\) 与 \(\delta_H=h+s-9\ge0\)，全部可能性为

\[
\begin{array}{c|c|c|c}
p&s&h&\delta_H\\ \hline
233&1&8&0\\
233&2&7,8&0,1\\
233&3&6,7,8&0,1,2\\
1399&1&8&0\\
1399&2&7,8&0,1.
\end{array}
\tag{18}
\]

共九个行实例，其中 \(\delta=0,1,2\) 分别出现五、三、一次。脚本
`unique_tail_type3_near_davenport_group_algebra.py` 从冻结的剩余尺寸
报告重建 (18)，并独立计数 (9) 的顶端单项式。

## 6. 边界与下一步

- \(J\) 是群代数中的带符号恒等式，不能解释为每个目标恰有一个
  普通子集表示。
- \(A\) 有零因子；即使 (14) 或 (17) 共享同一 \(K\)-因子，也不能
  直接取消该因子。
- 本文没有证明表 (18) 任一行可实现，也没有关闭型 \((3)\)。
- 下一步应把不同端点的 (14)、(17) 与它们共享的实际
  \(K,L,P\) 标签、短块闭包及端点交叠同时联立；不能把九行拆成
  独立余部模型。
- 全局 \(A_p\) 仍未完成。
