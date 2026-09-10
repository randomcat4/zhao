# \(p-4\) 单高度纤维的余部星矩系统

STATUS: INCOMPLETE

## 1. 精确范围

设 \(p\ge11\) 为素数，\(Z,T,B\) 沿用近 Davenport 补原子接口：

\[
|Z|=3p+4,\qquad T\in\mathcal F_3,\qquad
6\le |T|\le8,\qquad B=Z\setminus T,
\]

且 \(\bar B\) 是 \(C_p^3\) 中的原子。设非零商值 \(q\) 在 \(B\)
中的位置纤维 \(X\) 满足

\[
m:=|X|=p-4.
\]

本文只研究首个实际高度单值退化：\(X\) 中全部位置代表同一个实际
群元素 \(x\)，其中 \(\bar x=q\). 这与冻结高度上界相容，因为
实际值 \(x\) 恰出现 \(p-4\) 次。

三族短块的允许长度是

\[
I_1=\{2,3,4,5,6\},\quad
I_2=\{4,5,6,7\},\quad
I_3=\{6,7,8\}.
\tag{1}
\]

目标是把所有含 \(X\) 的短块按余部星精确聚合，输入一点、二点、
三点 Hasse 方程及相交接口。结论是：逐尾集限制可以严格写出，但
相应标量矩系统对每个 \(p\ge11\) 都有显式解；因此本稿没有排除
该单高度退化。

## 2. 余部星的精确分解

对 \(\lambda\in\{1,2,3\}\)、\(\ell\in I_\lambda\) 及

\[
1\le b\le\ell-1,
\]

定义

\[
\mathcal U_{\lambda,\ell,b}
=
\left\{
U\subset Z\setminus X:
\begin{array}{l}
|U|=\ell-b,\\
\bar\sigma(U)=-bq,\\
\sigma(U)=\lambda a-bx
\end{array}
\right\},
\qquad
N_{\lambda,\ell,b}=|\mathcal U_{\lambda,\ell,b}|.
\tag{2}
\]

因为 \(\ell\le8<p\)、\(q\ne0\)，任何含 \(b\ge1\) 个 \(X\)-位置
的商零和短块都有非空余部。反过来，每个
\(U\in\mathcal U_{\lambda,\ell,b}\) 与每个
\(V\in\binom Xb\) 唯一生成

\[
A=U\mathbin{\dot\cup}V\in\mathcal F_\lambda.
\tag{3}
\]

因此 (2)--(3) 是双射分类，不只是必要条件。若 \(U\cap T\) 为空，
则 (3) 位于 \(B\) 内，是 \(\bar B\) 的非空真商零和子序列；
故每个实际余部都满足

\[
U\cap T\ne\varnothing.
\tag{4}
\]

不同三元组 \((\lambda,\ell,b)\) 的余部族不重叠：集合大小确定
\(\ell-b\)，商和在 \(1\le b<p\) 中确定 \(b\)，而实际和再确定
\(\lambda\)。

## 3. 点、对、三点矩的统一系数

定义带符号的 \(b\)-层余部数

\[
z_{\lambda,b}
=
\sum_{\substack{\ell\in I_\lambda\\b\le\ell-1}}
(-1)^{\ell+b}N_{\lambda,\ell,b}
\quad\in\mathbb F_p,
\qquad 1\le b\le7.
\tag{5}
\]

固定 \(X\) 中一个点、一对不同点或一个三点集。一个
\((\lambda,\ell,b)\) 星包含它们的块数分别为

\[
\binom{m-1}{b-1}N_{\lambda,\ell,b},\quad
\binom{m-2}{b-2}N_{\lambda,\ell,b},\quad
\binom{m-3}{b-3}N_{\lambda,\ell,b}.
\tag{6}
\]

在 \(m=p-4\) 下，负二项式恒等式给出

\[
\begin{aligned}
\binom{m-1}{b-1}
&\equiv(-1)^{b-1}\binom{b+3}{4},\\
\binom{m-2}{b-2}
&\equiv(-1)^{b-2}\binom{b+3}{5},\\
\binom{m-3}{b-3}
&\equiv(-1)^{b-3}\binom{b+3}{6}.
\end{aligned}
\pmod p
\tag{7}
\]

点度、对度、三点度的符号分别是
\((-1)^{\ell-1},(-1)^\ell,(-1)^{\ell-1}\)。乘入 (7) 后三行
都留下 (5) 的同一符号。于是令

\[
\begin{aligned}
P_\lambda&=\sum_{b=1}^7\binom{b+3}{4}z_{\lambda,b},\\
D_\lambda&=\sum_{b=2}^7\binom{b+3}{5}z_{\lambda,b},\\
E_\lambda&=\sum_{b=3}^7\binom{b+3}{6}z_{\lambda,b}.
\end{aligned}
\tag{8}
\]

一点、二点、三点 Hasse 接口精确化为

\[
(P_1,P_2,P_3)
=
\left(-\frac34,\frac3{10},-\frac1{20}\right),
\tag{9}
\]

\[
8D_1+10D_2=3,\qquad
2D_1-10D_3=1,
\tag{10}
\]

\[
4E_1+10E_2+20E_3=-1.
\tag{11}
\]

这些等式对 \(X\) 中每个点、每对及每个三点集相同；这里使用的是
实际位置替换对称，而不是假设一个抽象正则超图。

## 4. 相交性给出的逐尾集条件

令

\[
J_m(b,b')
=
\{\max(0,b+b'-m),\ldots,\min(b,b')\}.
\tag{12}
\]

这是两个 \(X\)-位置集 \(V\in\binom Xb\)、
\(V'\in\binom X{b'}\) 的全部可实现交数。

### 4.1 \(\mathcal F_1\)--\(\mathcal F_3\) 与
\(\mathcal F_2\)--\(\mathcal F_3\)

若 \(U\in\mathcal U_{\lambda,\ell,b}\)，
\(U'\in\mathcal U_{3,\ell',b'}\)，其中 \(\lambda=1\) 或 \(2\)，
且

\[
b+b'\le m,
\]

则必有

\[
U\cap U'\ne\varnothing.
\tag{13}
\]

否则可取不交的 \(V,V'\subset X\)，使 (3) 生成一条
\(\mathcal F_\lambda\) 边和一条 \(\mathcal F_3\) 边完全不交，
违反冻结的交叉相交性。

### 4.2 两条 \(\mathcal F_3\) 星

若 \(U\in\mathcal U_{3,\ell,b}\)、
\(U'\in\mathcal U_{3,\ell',b'}\) 且 \(U\ne U'\)，则对每个可实现
的核心交数 \(k\in J_m(b,b')\) 都必须有

\[
\boxed{\bar\sigma(U\cap U')\ne-kq.}
\tag{14}
\]

否则选择 \(|V\cap V'|=k\) 后，两条不同 \(\mathcal F_3\) 边的
交集商和为零，违反冻结的 \(\mathcal F_3\) 交集非零接口。

当 \(b+b'\le m\) 时 \(0\in J_m(b,b')\)，故 (14) 特别推出

\[
U\cap U'\ne\varnothing,\qquad
\bar\sigma(U\cap U')\ne0.
\tag{15}
\]

若 \(U=U'\)，则其商和迫使 \(b=b'\)。此时 \(k=b\) 只对应同一
块，不在“两个不同块”的接口内；两块不同时 \(k\le b-1\)，而
\(\bar\sigma(U)+kq=(k-b)q\ne0\)，所以 (14) 自动成立。
真正新增的信息在 \(U\ne U'\) 的尾集对。

### 4.3 单点尾的推论

若两个不同的 \(\mathcal F_3\) 余部都是单点，核心数分别为
\(b,b'\)，且 \(b+b'\le m\)，则它们作为集合不相交，与 (15)
矛盾。因此这种单点尾不能并存。

特别地，\(\mathcal F_3\) 的单点尾只可能来自

\[
(\ell,b)=(6,5),(7,6),(8,7).
\]

当 \(p\ge19\) 时 \(m=p-4\ge15>14\)，上述三个层中的全部不同
单点尾合计至多一个。更一般地，一个单点
\(\mathcal F_3\) 尾 \(y\) 会强制每个满足 \(b+b'\le m\) 的
\(\mathcal F_1\) 或 \(\mathcal F_2\) 余部包含 \(y\)。这严格强于
单纯的单点容量界，但仍未把 (9)--(11) 闭成矛盾。

## 5. 标量矩系统的全素数稀疏解

以下解说明，仅靠 (9)--(11) 不可能排除本分支。先取

\[
(E_1,E_2,E_3)=\left(-\frac14,0,0\right),
\qquad
(D_1,D_2,D_3)=\left(\frac12,-\frac1{10},0\right).
\tag{16}
\]

令所有 \(b\ge4\) 的 \(z_{\lambda,b}\) 为零，并置

\[
\begin{array}{c|ccc}
&b=1&b=2&b=3\\ \hline
\lambda=1&-7&2&-1/4\\
\lambda=2&4/5&-1/10&0\\
\lambda=3&-1/20&0&0.
\end{array}
\tag{17}
\]

因为

\[
\binom44=1,\quad
\binom54=5,\quad
\binom64=15,\quad
\binom55=1,\quad
\binom65=6,\quad
\binom66=1,
\]

(17) 逐行给出 (9)，并给出 (16) 的 \(D,E\)；(16) 又直接满足
(10)--(11)。

它可由允许长度上的普通非负计数实现。记
\([r]_p\in\{0,\ldots,p-1\}\) 为 \(r\in\mathbb F_p\) 的最小代表，
取唯一非零的计数为

\[
\begin{array}{c|c}
(\lambda,\ell,b)&N_{\lambda,\ell,b}\\ \hline
(1,3,1)&[-7]_p\\
(1,4,2)&[2]_p\\
(1,5,3)&[-1/4]_p\\
(2,5,1)&[4/5]_p\\
(2,4,2)&[-1/10]_p\\
(3,7,1)&[-1/20]_p.
\end{array}
\tag{18}
\]

六种类型均满足 \(\ell\in I_\lambda\)、\(1\le b\le\ell-1\)，且
\((-1)^{\ell+b}=1\)。对 \(p\ge11\)，(18) 的六个数都在
\(\{1,\ldots,p-1\}\) 中。因此 (18) 是每个允许素数上的显式非负
整数标量解。

例如 \(p=11\) 时六个计数依次为

\[
4,\ 2,\ 8,\ 3,\ 1,\ 6.
\tag{19}
\]

注意 (18) 只实现矩方程及长度、非空余部的标量条件。它没有声称
存在真实位置子集 \(U\) 同时实现这些计数、(4)、(13)--(15) 与
全部实际和值。因此它不是群值反模型，也不是冻结命题的反例。

## 6. 最小剩余障碍

本轮得到的新信息是逐尾集的 (14)，以及它对单点尾的容量推论；
这比已有矩方程和单点总数界更强。然而标量矩系统有 (18) 的全素数
解，所以继续只消元 \(N_{\lambda,\ell,b}\) 不会闭合。

下一步必须保留至少一个真实接口：

1. 每个余部作为 \(Z\setminus X\) 中的实际位置子集及其与
   \(T\) 的具体交集；
2. 对每对 \(\mathcal F_3\) 余部同时施加 (14) 的全部
   \(k\)-禁值，而不是只记是否相交；
3. 把 (13) 的交叉横截要求与 \(|T|\le8\)、余部长度
   \(\ell-b\le7\) 联立；
4. 同时保持 \(\bar B\) 原子性，排除由若干余部差集产生的
   \(B\) 内商零和。

未完成之处不是一个剩余标量未知数，而是从星数矩到带实际商和值的
交叉相交尾集系统的实现问题。本文因此严格标为 INCOMPLETE，不把
(18) 当作群值反例，也不声称关闭 \(m=p-4\) 分支。
