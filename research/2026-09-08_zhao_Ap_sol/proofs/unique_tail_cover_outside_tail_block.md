# 强制共同余部原子型的覆盖例外关闭：尾外整体禁块

STATUS: **AXIAL_COVER_PAIR_BRANCH_CLOSED /
NO_PACKING_TYPE_CLOSED / GLOBAL_INCOMPLETE**

## 1. 冻结范围

只考虑

\[
(p,\ell,b,r)=(233,7,4,3),\qquad(1399,8,5,3)
\tag{1}
\]

的三点唯一尾分支，以及三个强制共同余部原子型

\[
(3),\qquad(1,2),\qquad(1,1,1).
\tag{2}
\]

沿用实际位置集 \(U\subseteq L\subseteq Y\)、\(|U|=3\)、
\(X=x^{p-4}\)，以及每个端点 \(E\) 的共同余部原子

\[
Q_E=K\mathbin{\dot\cup}(L\setminus E),qquad
\bar\sigma(Q_E)=q,qquad \bar\sigma(E)=0.
\tag{3}
\]

唯一尾满足

\[
\bar\sigma(U)=-bq.
\tag{4}
\]

此前交换门已经证明：不同端点 \(H,J\) 的交投影轴向，当且仅当

\[
K=\varnothing,qquad L=H\cup J.
\tag{5}
\]

本文关闭 (5) 的整个分支；不假定具体端点图、迹着色或 incidence
构造。

## 2. 尾外整体的统一商标签

假设反证地 (5) 成立。由 (3) 中任取一个端点 \(E\)，此时

\[
Q_E=L\setminus E.
\tag{6}
\]

由于 (6) 是实际位置不交差，(3) 立即给出

\[
\bar\sigma(L)
=\bar\sigma(E)+\bar\sigma(Q_E)
=q.
\tag{7}
\]

现在取真实尾外位置块

\[
O:=L\setminus U.
\tag{8}
\]

由 \(U\subseteq L\)、(4) 与 (7)，同一套统一标签强制

\[
\boxed{\bar\sigma(O)=(b+1)q.}
\tag{9}
\]

这一步正是只保留端点迹、大小或给各保护块独立赋值时会丢失的整体
位置关系。

## 3. 大 \(X\) 核落入冻结禁区

因为 \(b\ge4\)，可以从 \(X=x^{p-4}\) 中取

\[
c=p-b-1\le p-4
\tag{10}
\]

个实际位置。由 (9)，实际位置块

\[
B:=X_c\mathbin{\dot\cup}O
\tag{11}
\]

的商和为零。

覆盖端点满足 \(6\le|H|,|J|\le8\)，且上游已有
\(|L|=|H\cup J|\le14\)。因此

\[
6\le|L|\le14,qquad 3\le|O|=|L|-3\le11.
\tag{12}
\]

式 (11) 的长度为

\[
n=p-b-1+|O|=p-b+|L|-4.
\tag{13}
\]

两个素数分别得到

\[
\begin{array}{c|c|c}
(p,b)&c&n\text{ 的范围}\\
\hline
(233,4)&228&231\le n\le239\\
(1399,5)&1393&1396\le n\le1404.
\end{array}
\tag{14}
\]

两行都完全落在连续冻结禁区

\[
[9,p+1]\cup[p+2,2p+2]=[9,2p+2].
\tag{15}
\]

故 (11) 是不允许的商零实际块，与冻结谱矛盾。

## 4. 有限回归

`unique_tail_cover_local_quotient_closure.py` 对上游每个素数的 372 个
固定规范骨架逐位置重建 (8)--(14)，并进一步枚举 \(L\) 的每个非空
子集、每个可用 \(X\) 核、全部 \(Q_E\) 真内部子集与全部非覆盖端点
交。两个素数的 372/372 个固定骨架都包含 (11) 的强迫禁块；因此
有限报告没有把某个特定构造误当成一般证明的来源。报告规范证书
SHA-256 为

\[
\mathtt{01eb473629b2519e924f8ce6337867edbbdaff49cf05cc05ef01b5ce4d7bec6e}.
\tag{16}
\]

一般结论来自 (7)--(15)，不依赖 372 个构造的穷尽性。

## 5. 精确结论

**PROVED：**三个强制共同余部原子型中不存在轴向端点交。结合交换门，

\[
\boxed{
\rho\bar\sigma(H\cap J)\ne0
\quad\text{对每一对不同端点 }H,J.}
\tag{17}
\]

因此此前唯一可能的不同双点迹轴向覆盖例外也被完全删除；不再需要对
其 24,468 个覆盖候选出现逐一寻找 incidence。

**NOT PROVED：**端点族不存在；三个强制 packing 型任一为空；没有
轴向交的 28,584 个迹着色不能配置统一标签；其余四个 packing 型为空；
或 \(A_p\) 成立。后续应回到全非轴交分支，把实际位置、全部自动诱导
短块、共同 \(R\) 标签以及每个长补原子的内部子集和一次性联立。

全局状态继续为 **INCOMPLETE**。
