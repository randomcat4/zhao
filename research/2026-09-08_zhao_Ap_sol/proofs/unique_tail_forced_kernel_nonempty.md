# 三种强制共同余部原子型必须有非空共同核

STATUS: **FORCED_TYPES_REQUIRE_NONEMPTY_COMMON_KERNEL /
ALL_ENDPOINT_INTERSECTIONS_NONAXIAL / GLOBAL_INCOMPLETE**

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

沿用实际位置集

\[
U\subseteq L\subseteq Y,qquad |U|=3,qquad |L|\le52,
\tag{3}
\]

以及 \(X=x^{p-4}\)。每个端点 \(E\) 满足

\[
6\le|E|\le8,qquad \bar\sigma(E)=0,
\tag{4}
\]

而三个强制型共同给出

\[
Q_E=K\mathbin{\dot\cup}(L\setminus E),qquad
\bar\sigma(Q_E)=q.
\tag{5}
\]

唯一尾满足

\[
\bar\sigma(U)=-bq.
\tag{6}
\]

本文证明 (5) 中的共同零和自由核 \(K\) 不可能为空。这里不假定存在
覆盖端点对，也不固定迹着色或 incidence。

## 2. 空共同核强制尾外整体和值

假设反证地 \(K=\varnothing\)。由 (5)，对任意端点 \(E\) 都有实际
位置不交分解

\[
L=E\mathbin{\dot\cup}Q_E.
\tag{7}
\]

结合 (4)--(5)，

\[
\bar\sigma(L)=\bar\sigma(E)+\bar\sigma(Q_E)=q.
\tag{8}
\]

令真实尾外位置块

\[
O:=L\setminus U.
\tag{9}
\]

则由 (6) 与 (8)，

\[
\boxed{\bar\sigma(O)=(b+1)q.}
\tag{10}
\]

这只使用同一组实际位置上的统一标签；若把不同端点余部或保护块分开
赋值，式 (8)--(10) 就会丢失。

## 3. 禁区商零块

从 \(X\) 中取

\[
c=p-b-1
\tag{11}
\]

个实际位置。两个目标参数上分别有 \(c=p-5,p-6\)，故总有
\(0<c\le p-4\)。由 (10)，

\[
B:=X_c\mathbin{\dot\cup}O
\tag{12}
\]

是商零实际块。

由 (3)--(4)，\(L\) 至少包含一个六位置端点，所以

\[
6\le|L|\le52,qquad3\le|O|=|L|-3\le49.
\tag{13}
\]

块 (12) 的长度为

\[
n=p-b-1+|O|=p-b+|L|-4.
\tag{14}
\]

因此

\[
\begin{array}{c|c|c}
(p,b)&c&n\text{ 的范围}\\
\hline
(233,4)&228&231\le n\le277\\
(1399,5)&1393&1396\le n\le1442.
\end{array}
\tag{15}
\]

两行都包含于冻结禁区

\[
[9,p+1]\cup[p+2,2p+2]=[9,2p+2].
\tag{16}
\]

这与 (12) 的存在矛盾，故

\[
\boxed{K\ne\varnothing.}
\tag{17}
\]

## 4. 所有端点交都非轴

上游交换门已经给出，对不同端点 \(H,J\)，

\[
\rho\bar\sigma(H\cap J)=0
\iff K=\varnothing\text{ 且 }L=H\cup J.
\tag{18}
\]

式 (17) 删除了 (18) 右端的第一项，所以三个强制型中

\[
\boxed{
\rho\bar\sigma(H\cap J)\ne0
\quad\text{对每一对不同端点 }H,J.}
\tag{19}
\]

此前唯一尚可能的不同双点迹轴向覆盖例外因而一并关闭；更强地，任何
迹型都不再有轴向端点交。

## 5. 有限回归与停止线

`unique_tail_forced_kernel_nonempty.py` 对两个参数及全部整数
\(6\le|L|\le52\) 核对 (11)、(14)--(16)。报告规范证书 SHA-256 为

\[
\mathtt{2ae9da6ab822ad6c9c236d295e2f6a25299ba81dd3f6e2b3915b97ff34e9c2ff}.
\tag{20}
\]

**PROVED：**三个强制共同余部原子型都必须满足 \(K\ne\varnothing\)，
且全部不同端点交投影非轴。

**SUBSUMED：**此前对不同双点迹覆盖对的 incidence 构造、固定骨架
统一投影标签搜索以及十位置局部幸存者，都位于现已关闭的
\(K=\varnothing\) 子支；它们仍是识别旧放宽接口边界的正确有限记录，
但不再是承重开放路线。

**NOT PROVED：**三个强制 packing 型为空；\(K\ne\varnothing\) 子支
为空；其余四个 packing 型为空；或 \(A_p\) 成立。下一步应在非空
共同核上恢复同一实际 \(R\) 的全部自动短块、统一标签及每个长补原子
的内部子集和。

全局状态继续为 **INCOMPLETE**。
