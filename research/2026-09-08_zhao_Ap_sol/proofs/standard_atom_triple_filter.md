# 标准极值商原子的三点候选过滤器

STATUS: PROVED_HERE

固定素数 \(p\ge11\)、标准极值商群原子

\[
B=e_1^{p-1}e_2^{p-1}e_3^{p-1}g,
\qquad g=e_1+e_2+e_3,
\]

以及六点非零商标号序列 \(C\)，满足 \(\bar\sigma(C)=0\)。

## 1. 任意六点 \(C\) 的必要子集和条件

固定方向 \(i\)，并取 \(B_{e_i}\) 值类内三个不同位置。三点覆盖
定理迫使某个长度至多八的统一商零和块 \(E\) 包含这三个位置。

令 \(D=E\cap C\)。因为 \(B\) 是原子而 \(E\) 是短真子块，
\(D\ne\varnothing\)。写

\[
A=C\setminus D,\qquad k=|A|\le5.
\]

设 \(b_j\) 是 \(E\cap B\) 中 \(e_j\) 的重数，
\(\varepsilon\in\{0,1\}\) 表示是否使用 \(B\) 中唯一的 \(g\)，并令

\[
t_j=b_j+\varepsilon.
\]

由 \(\bar\sigma(C)=0\) 及 \(\bar\sigma(E)=0\)，

\[
\bar\sigma(A)=t_1e_1+t_2e_2+t_3e_3.
\tag{1}
\]

另一方面，

\[
|E|=\sum_jb_j+\varepsilon+6-k
=\sum_jt_j-2\varepsilon+6-k\le8.
\tag{2}
\]

再用 \(b_i\ge3\)，得到以下必要条件：

\[
\boxed{
\begin{array}{ll}
\varepsilon=0:&
1\le k\le5,\quad
t_j\ge0,\quad t_i\ge3,\quad
t_1+t_2+t_3\le k+2;\\[2mm]
\varepsilon=1:&
2\le k\le5,\quad
t_i\ge4,\quad t_j\ge1\ (j\ne i),\quad
t_1+t_2+t_3\le k+4.
\end{array}}
\tag{3}
\]

式 (1) 是 \(C_p^3\) 中的等式，而 (3) 中的 \(t_j\) 是所列范围内的
普通非负整数。

反向在商候选层也成立。第一种情形取
\(b_j=t_j,\varepsilon=0\)，第二种取
\(b_j=t_j-1,\varepsilon=1\)，并取 \(D=C\setminus A\)。因为
\(t_j\le9<p-1\)（在 \(p=11\) 时仍不超过九），标准 \(B\) 中有足够
位置可选；所得块满足 (1)--(2)，并含指定的三个 \(e_i\) 位置。
所以 (3) 精确刻画“该方向存在长度至多八的三点商零和候选”。

真实三点覆盖比 (3) 更强：每个具体三位置集须被至少
\(\lceil(p-1)/20\rceil\) 个实际短块覆盖，并满足带符号三共度关系。
本节只抽取最先可用的商候选必要条件。

## 2. \((\pm2e_i)\) 模板被全部排除

取

\[
C=(\pm2e_1,\pm2e_2,\pm2e_3).
\]

更直接地看，任何含三个 \(B_{e_i}\) 位置、长度至多八的候选块，其
第 \(i\) 个整数坐标为

\[
b_i+\varepsilon+2\gamma_i^+-2\gamma_i^-,
\]

其中 \(b_i\ge3\)、\(\varepsilon,\gamma_i^\pm\in\{0,1\}\)。由于总长
至多八，这个整数落在 \([1,9]\)，对 \(p\ge11\) 不可能模 \(p\)
为零。因此不存在任何覆盖这组三位置的短商零和块，与三点覆盖定理
矛盾。

\[
\boxed{\text{标准 }B\text{ 与 }C=(\pm2e_1,\pm2e_2,\pm2e_3)
\text{ 对每个 }p\ge11\text{ 都不可能。}}
\tag{4}
\]

这比二点高度 pair-sum 探针更强，且不需要任何高度对称假设。

## 3. 过滤器的边界与后续高度闭合

三方向条件 (3) 本身仍可同时满足。例如

\[
C=(\pm3e_1,\pm3e_2,\pm3e_3).
\]

对每个方向 \(i\)，取

\[
D_i=\{-3e_i\},\qquad A_i=C\setminus D_i.
\]

则 \(k=5\)、\(\bar\sigma(A_i)=3e_i\)，满足 (3) 的
\(\varepsilon=0\) 情形；显式候选是三个 \(B_{e_i}\) 位置加上
\(-3e_i\) 点，长度四。

因此，三点候选过滤器关闭了 \((\pm2e_i)\) 模板，却没有分类任意
六点 \(C\)。下一非平凡标准模板是 \((\pm3e_i)\)，必须输入实际
高度的三元和函数及带符号三点方程，而不能再停在候选存在性。

这一步现已完成：八项候选迫使每个标准值类的三元高度和恒定，继而
全部高度相同，违反实际值重数至多 \(p-4\)。详见
`verifications/standard_atom_triple_filter_review.md`。更一般地，
`proofs/standard_atom_coordinate_pairs.md` 已将同一机制扩张到任意
三个非零、彼此可以不同的轴向幅度。仍未解决的是不支撑在三条基轴
上的一般六点 \(C\)。
