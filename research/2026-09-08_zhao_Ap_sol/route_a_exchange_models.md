# ROUTE-A4：近 Davenport 原子的交换引理与商群反模型

## 状态

- 交换引理：PROVED_HERE。
- “单个近极值补原子配置必不相容”：DISPROVED。
- 一般 \(A_p\)：INCOMPLETE。

反模型只生活在 \(C_p^3\) 商群并实现命名块的局部接口；它不是冻结
\(C_p^4\) 反例，也不实现三族逐点/逐对带符号设计。

## 1. 删除交换引理

固定 \(p\ge7\)。在 (20) 的第一支中，令 \(C\) 是六项 \(2a\) 块，
\(A\in\mathcal F_3\) 是 (28) 第一支给出的 \(r\) 项 \(3a\) 块，
其中 \(r\in\{6,7,8\}\)、\(|A\cap C|\ge2\) 且
\(\bar\sigma(A\cap C)\ne0\)。写

\[
I=A\cap C,\quad J=A\setminus C,\quad K=C\setminus A,\quad
X=Z\setminus(A\cup C).
\]

则

\[
\bar\sigma(J)=\bar\sigma(K),\qquad
XJ=Z\setminus C,\qquad XK=Z\setminus A.
\tag{1}
\]

后两者分别是长度 \(3p-2\) 与
\(3p+4-r\in\{3p-2,3p-3,3p-4\}\) 的 \(C_p^3\) 原子。

取任意 \(J_0\subseteq J,K_0\subseteq K\)，满足

\[
\bar\sigma(J_0)=\bar\sigma(K_0).
\tag{2}
\]

交换所得位置块

\[
P=I\mathbin{\dot\cup}J_0
 \mathbin{\dot\cup}(K\setminus K_0)
\]

商和为零，且

\[
|P|=6+|J_0|-|K_0|\le6+|J|\le12.
\tag{3}
\]

这里最后一步使用 \(|I|\ge2,r\le8\)。\(P\) 非空且是真子集，
所以实际和不为零。若实际和为 \(-\mu a\)，
\(\mu\in\{1,2,3\}\)，原子线补集界会给
\(|P|\ge3p-4\ge17\)，也不可能。因此存在
\(\lambda\in\{1,2,3\}\)，并由原子线长度界得到

\[
\boxed{\sigma(P)=\lambda a,\qquad |P|\le5+\lambda.}
\tag{4}
\]

若取线性坐标 \(\ell:G\to\mathbb F_p\)、\(\ell(a)=1\)，则从
\(P=C-K_0+J_0\) 还得到

\[
\boxed{
\lambda=2+\ell(J_0)-\ell(K_0)\in\{1,2,3\},\qquad
6+|J_0|-|K_0|\le5+\lambda.}
\tag{5}
\]

空交换给回 \(C\)，全交换给回 \(A\)。任何真子交换都会强制一个
新的、长度受控的 \(a/2a/3a\) 块。精确剩余对象是小符号关系

\[
\mathcal R=J(-K).
\]

若 \(\mathcal R\) 本身是原子，就没有真子交换。
由 \(|J|+|K|=r+6-2|I|\) 及 \(J,K\ne\varnothing\)，其精确可能长度
范围是 \(2\) 至 \(10\)。

## 2. 纯商群不相容加强为假

令 \(e_1,e_2,e_3\) 是 \(C_p^3\) 的基，
\(g=e_1+e_2+e_3\)，并取标准极值原子

\[
B=e_1^{p-1}e_2^{p-1}e_3^{p-1}g.
\tag{6}
\]

以下构造对每个素数 \(p\ge7\) 成立。

先记 (6) 的原子性是逐坐标的：若一个零和子序列选了
\(\varepsilon\in\{0,1\}\) 份 \(g\)，则三个基向量计数都必须是
\(0\)（当 \(\varepsilon=0\)）或 \(p-1\)（当
\(\varepsilon=1\)），故只有空解与全解。

### 2.1 六项对六项

令 \(x=-g/3\)，并取

\[
J=e_1e_2e_3,\qquad K=e_1e_2e_3,\qquad I=x^3,
\]

其中 \(K\) 使用外部新位置。则 \(C=IK\)、\(A=IJ\) 都是六项
原子，\(\bar\sigma(I)=-g\ne0\)，且
\((B\setminus J)K\) 与 \(B\) 是同一多重序列。

原子性可逐坐标看出：若选取 \(t\in\{0,1,2,3\}\) 份 \(x\)，
三个基向量的选择指示量都必须等于 \(t/3\)；只有 \(t=0,3\)
给空解和全解。

### 2.2 六项对七项

令

\[
h=e_1+e_2,\quad q=-e_1-3e_2-2e_3,
\]
\[
J=e_1e_2,\qquad K=h,\qquad I=e_2^2e_3^2q.
\]

则

\[
C=h\,e_2^2e_3^2q,\qquad
A=e_1e_2^3e_3^2q
\]

分别是六项、七项原子，且
\(\bar\sigma(I)=-h\ne0\)。交换后的补原子为

\[
(B\setminus J)K
=e_1^{p-2}e_2^{p-2}e_3^{p-1}gh,
\tag{7}
\]

长度 \(3p-3\)。若 \(g,h\) 的选取数为
\(\varepsilon,\delta\in\{0,1\}\)，零和坐标方程为

\[
x_1+\varepsilon+\delta
=x_2+\varepsilon+\delta
=x_3+\varepsilon=0.
\]

在 \(0\le x_1,x_2\le p-2,\ 0\le x_3\le p-1\) 内只有空解和全解，
故 (7) 是原子。

为补齐小块自身的核验：在 \(C\) 或 \(A\) 的子序列中，令
\(q\) 的选取数为 \(\varepsilon\in\{0,1\}\)，并令首个特殊项
（\(h\) 或 \(e_1\)）的选取数为 \(\delta\in\{0,1\}\)。第一坐标
先强制 \(\delta=\varepsilon\)，其余坐标再强制所选的 \(e_2,e_3\)
计数分别为 \(2\varepsilon,2\varepsilon\)（对 \(C\)）或
\(3\varepsilon,2\varepsilon\)（对 \(A\)）。故也只有空解与全解。

### 2.3 六项对八项

令

\[
q=-e_1-3e_2-3e_3,\qquad
J=e_1e_2e_3,\qquad K=g,\qquad I=e_2^2e_3^2q.
\]

则

\[
C=g\,e_2^2e_3^2q,\qquad
A=e_1e_2^3e_3^3q
\]

分别是六项、八项原子，\(\bar\sigma(I)=-g\ne0\)。交换补原子为

\[
(B\setminus J)K
=e_1^{p-2}e_2^{p-2}e_3^{p-2}g^2,
\tag{8}
\]

长度 \(3p-4\)。若使用 \(t=0,1,2\) 份 \(g\)，三个基向量计数
都须为 \(0,p-1,p-2\) 中相应一个；中间值 \(p-1\) 超出可用重数，
故仍只有空解和全解。

小块自身同样可逐坐标核验：若 \(q\) 被选
\(\varepsilon\in\{0,1\}\) 次，则 \(C\) 中 \(g\) 的选取数、或
\(A\) 中 \(e_1\) 的选取数，都先被第一坐标强制为
\(\varepsilon\)；随后 \(e_2,e_3\) 的计数都被强制为
\(2\varepsilon\)（对 \(C\)）或 \(3\varepsilon\)（对 \(A\)）。
因此只有空解和全解。

## 3. 反模型的精确覆盖范围

在三种构造中令

\[
Z=B\mathbin{\dot\cup}I\mathbin{\dot\cup}K,\qquad
C=I\mathbin{\dot\cup}K,\qquad A=I\mathbin{\dot\cup}J.
\]

则

\[
|Z|=3p+4,\quad |C|=6,\quad |A|=6,7,8,
\]
\[
|A\cap C|\ge2,\qquad
\bar\sigma(A\cap C)=\bar\sigma(I)\ne0,
\]

而 \(Z\setminus C\) 是长度 \(3p-2\) 原子，
\(Z\setminus A\) 依次是长度 \(3p-2,3p-3,3p-4\) 原子。
七项、八项模型的交换关系

\[
e_1+e_2-h=0,\qquad e_1+e_2+e_3-g=0
\]

本身分别是三项、四项原子，故没有真子交换。

甚至命名块的锚点坐标总和可形式相容地指定为

\[
\ell(I)=0,\quad\ell(K)=2,\quad
\ell(J)=3,\quad\ell(X)=-5.
\]

于是 \(C,A,Z\setminus C,Z\setminus A,Z\) 的实际和依次为
\(2a,3a,-2a,-3a,0\)。

但这仍不是冻结反例：尚未统一提升为 \(C_p^4\) 的实际原子，也没有
实现全部七点系数、三族逐点/逐对带符号覆盖及所有六项块之间的同时
约束。它严格证伪的只是：

> 单个 \(3p-2\) 补原子与单个 \(3p-4\) 至 \(3p-2\) 补原子的
> 小交换配置本身必然矛盾。

## 4. 新的最小缺口

后续必须排除交换关系 \(\mathcal R=J(-K)\) 自身为二至十项小原子的
全局设计，并至少使用多块同时性、逐点/逐对带符号度或真实
\(a\)-坐标长度方向。继续分类单个近 Davenport 原子不可能闭合。
