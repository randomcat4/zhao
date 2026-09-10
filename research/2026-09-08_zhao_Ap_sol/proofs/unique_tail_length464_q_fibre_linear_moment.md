# 长度 464 补原子的统一 \(q\)-纤维一阶矩

STATUS: **PROVED_REDUCTION / INDEPENDENT_REVIEW CORRECT / GLOBAL_INCOMPLETE**

## 1. 结论

令 \(p\) 为奇素数，\(G=C_p^2\)。设带位置序列

\[
Q=((g_z,h_z))_{z\in\Omega},\qquad
g_z\in G,\quad h_z\in\mathbb F_p
\tag{1}
\]

满足

\[
|Q|=2p-2,\qquad
(g_z)_{z\in\Omega}\text{ 是 }G\text{ 中的原子},\qquad
\sum_{z\in\Omega}h_z=1.
\tag{2}
\]

对 \(r\in G\) 定义全部内部位置子集的带符号一阶 \(q\)-矩

\[
M_1(r)=
\sum_{\substack{E\subseteq\Omega\\ \sum_{z\in E}g_z=r}}
(-1)^{|E|}\sum_{z\in E}h_z
\quad\in\mathbb F_p.
\tag{3}
\]

则存在唯一线性泛函 \(\lambda:G\to\mathbb F_p\)，使

\[
\boxed{M_1(r)=1+\lambda(r)\qquad(r\in G).}
\tag{4}
\]

特别地，

\[
M_1(0)=1,\qquad M_1(-r)=2-M_1(r).
\tag{5}
\]

这不是端点总和的一阶矩，而是对每个 \(\rho\)-目标分别汇总该目标
纤维中全部内部位置子集的 \(q\)-坐标。它保留了部分统一 \(q\) 信息，
但仍是模 \(p\) 的带符号必要条件，不能替代普通表示或完整目标纤维。

## 2. 带 \(q\) 变量的共同生成积

在 \(\mathbb F_p[C_p\oplus G]\) 中用 \(Y\) 和 \(X^g\) 分别记录
\(q\)-坐标与 \(G\)-坐标，置

\[
\Phi_Q(Y,X)=\prod_{z\in\Omega}(1-Y^{h_z}X^{g_z}).
\tag{6}
\]

令 \(w=1-Y\)。因为

\[
1-Y^hX^g=(1-X^g)+h\,wX^g+O(w^2),
\tag{7}
\]

\(w\) 的一次系数为

\[
F_1(X)=
\sum_{z\in\Omega}h_zX^{g_z}
\prod_{y\ne z}(1-X^{g_y}).
\tag{8}
\]

若 \(I\subset\mathbb F_p[G]\) 是增广理想，则每个删点积含
\(2p-3\) 个增广因子；左乘群环单位不改变理想次数，所以

\[
F_1\in I^{2p-3}.
\tag{9}
\]

直接展开 (6) 又表明，\(X^rw\) 的系数恰为 \(-M_1(r)\)；负号来自
\(Y^h=(1-w)^h=1-hw+O(w^2)\)。

## 3. 顶端三维边缘就是仿射函数

取 \(G\) 的基 \((e,f)\)，并写

\[
u=1-X^e,\qquad v=1-X^f.
\tag{10}
\]

则

\[
\mathbb F_p[G]\cong\mathbb F_p[u,v]/(u^p,v^p),
\tag{11}
\]

且

\[
I^{2p-3}=
\left\langle
u^{p-1}v^{p-1},
u^{p-2}v^{p-1},
u^{p-1}v^{p-2}
\right\rangle.
\tag{12}
\]

对 \(r=ae+bf\)，这三个基元素在 \(X^r\) 处的系数分别为

\[
1,\qquad a+1,\qquad b+1.
\tag{13}
\]

这里使用

\[
(-1)^a\binom{p-2}{a}=a+1
\quad\text{于 }\mathbb F_p,
\tag{14}
\]

且 \(a=p-1\) 时两边都为零。因此 \(I^{2p-3}\) 中每个元素的群基
系数函数都是仿射线性函数，结合 (8)--(9)，\(M_1(r)\) 也仿射线性。

因 \((g_z)\) 是原子，\(\rho\)-和为零的位置子集只有空集与全集。
长度 \(2p-2\) 为偶数，而二者的 \(q\)-和分别为零与一，故

\[
M_1(0)=1.
\tag{15}
\]

于是常数项为一，余下部分是唯一线性泛函 \(\lambda\)，证明 (4)。

零阶带符号纤维恒等式是

\[
\prod_z(1-X^{g_z})=2J_G
\quad\text{于 }\mathbb F_p[G],
\tag{16}
\]

所以每个目标的零阶带符号和在 \(\mathbb F_p\) 中等于 \(2\)，而非
整数意义的精确计数。补集映射把 \((r,h)\) 送到 \((-r,1-h)\)，并因
总长度为偶数而保持符号；故

\[
M_1(-r)=2-M_1(r).
\tag{17}
\]

## 4. 对 \(|P|=2\) mixed target 的必要门

在当前型 \((3)\)、\(|P|=2\) 中，写两个 \(P\)-位置的
\((q,\rho)\)-标签为

\[
(c,s),\qquad(3-c,-s),\qquad s\ne0.
\tag{18}
\]

对长度八端点 \(Q_H\)，完整 mixed-target 条件要求

\[
\rho(E)=-s
\Longrightarrow
h(E)\in\{1-c,2-c,3-c\}.
\tag{19}
\]

令

\[
d_j=
\sum_{\substack{E\subseteq Q_H\\
\rho(E)=-s,\ h(E)=j-c}}
(-1)^{|E|}
\quad\in\mathbb F_p,\qquad j=1,2,3.
\tag{20}
\]

式 (4) 与零阶恒等式给出

\[
\boxed{
d_1+d_2+d_3=2,\qquad
\sum_{j=1}^3(j-c)d_j=1-\lambda(s).}
\tag{21}
\]

这两式通常仍给 \((d_1,d_2,d_3)\) 留下一个自由参数；唯一的是
\(\lambda\)，不是三个 \(d_j\)。另一个 \(P\)-位置的条件由补集对称
得到，不应误作独立的第三组变量。

更一般地，任意在 (19) 三个允许高度上消失的多项式 \(P(t)\) 都给出

\[
\sum_{E:\rho(E)=-s}(-1)^{|E|}P(h(E))=0.
\tag{22}
\]

最低次数可取

\[
P(t)=(t-(1-c))(t-(2-c))(t-(3-c)).
\tag{23}
\]

当 \(p>3\)，特别是当前 \(p=233\) 时，(22)--(23) 可由三阶 Hasse
\(q\)-矩计算，而无需枚举普通意义的全部 \(2^{2p-2}\) 个子集。它仍
只是必要剪枝：同一禁高度上的偶奇表示可能在带符号计数中抵消。

## 5. 边界

- (4) 真正使用统一 \(q\)-标签并逐 \(\rho\)-目标保留内部子集信息，
  不是端点总和方程。
- 它没有恢复普通表示数、表示长度、实际第四坐标或 Hasse 全系统。
- (21)--(23) 可作为真实 endpoint-mask CEGAR 的低成本必要门；通过者
  仍须运行完整 mixed-target 与全短谱预言机。
- 本文没有关闭 outer row 或固定骨架。全局 \(A_p\) 仍为
  **INCOMPLETE**。
