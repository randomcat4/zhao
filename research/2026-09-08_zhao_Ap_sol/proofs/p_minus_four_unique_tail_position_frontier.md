# 唯一正核心 \(F_3\) 尾的位置级前沿

STATUS: PROVED_HERE / THREE_TYPES_EXCLUDED / REMAINDER_INCOMPLETE

## 1. 范围与结论

设 \(p\ge 11\) 为素数，并处于 \(p-4\) 单高度纤维分支。沿用

\[
X=x^m\subset B,\qquad m=p-4,\qquad
Y=Z\setminus X,\qquad |Y|=2p+8,
\]

其中 \(Z\) 是长度 \(3p+4\) 的实际零和原子，且
\(\bar x=q\ne0\)。假设正核心 \(F_3\) 实际余部唯一，记为

\[
U\subset Y,\qquad |U|=r=\ell-b,\qquad
\bar\sigma(U)=-bq,\qquad
\sigma(U)=3a-bx,
\tag{1}
\]

其中 \(\ell\in\{6,7,8\}\) 且 \(b\ge1\)。因此全部正核心
\(F_3\) 块恰为

\[
V\mathbin{\dot\cup}U\qquad
(V\in\tbinom Xb).
\tag{2}
\]

令

\[
\mathcal H_0=\{H\in\mathcal F_3:H\cap X=\varnothing\}
\tag{3}
\]

为零核心 \(F_3\) 块的实际位置族。本文不再使用只记录总尾数与
\(T\)-入射和的 \(N,J\) 松弛，而保留固定实际尾 \(U\)、每个
\(y\in Y\) 以及每个实际块 \(H\in\mathcal H_0\) 的身份。

主要结论如下。

1. \(\mathcal H_0\) 横截于实际尾 \(U\)，每个交集及每对不同
   零核心块的交集都有非零商和；并且逐位置带符号入射满足第 3 节
   的四个精确公式。
2. 表中每个异常型都强制显式数量的实际零核心块，而不是有限域
   加权块。最大三个下界分别达到 \(9400,28030,90864\)。
3. 若 \(b\ge4\)，任何零核心块都不能包含整个 \(U\)。当
   \(|U|=2\) 时，这与逐位置公式矛盾。因此原 16 个唯一尾异常型中

\[
\boxed{
(467,7,5),\quad(701,6,4),\quad(2521,8,6)
}
\tag{4}
\]

   三型被排除；这里只按 \((p,\ell,b)\) 记型。

这是一条严格弱于冻结目标的位置级子分支定理。它没有排除余下
13 型，也没有构造任何补原子或冻结反例。

## 2. 横截、实际标签与非零商交

固定 \(H\in\mathcal H_0\)，再取任意
\(V\in\binom Xb\)。由 (2)，\(A=V\dot\cup U\) 是一个正核心
\(F_3\) 块。块 \(A,H\) 不同，且已有 \(F_3\)--\(F_3\) 非零商交
给出

\[
0\ne\bar\sigma(A\cap H)
=\bar\sigma(U\cap H).
\tag{5}
\]

特别地，

\[
\boxed{
\varnothing\ne H\cap U,\qquad
\bar\sigma(H\cap U)\ne0
\quad(H\in\mathcal H_0).}
\tag{6}
\]

对不同的 \(H,H'\in\mathcal H_0\)，同一接口还给出

\[
\boxed{\bar\sigma(H\cap H')\ne0.}
\tag{7}
\]

所以 \(\mathcal H_0\) 是一个由实际位置块组成的两两相交族，
而且 (7) 排除的不只是空交，还排除商和为零的非空交。式 (5)--(7)
保留统一商标签；它们不是无标签相交超图的替代品。

## 3. 零核心族的逐位置精确式

对 \(H\in\mathcal H_0\) 记

\[
\varepsilon_H=(-1)^{|H|-1}\in\{-1,1\}.
\tag{8}
\]

唯一尾的一项算术是

\[
(-1)^{\ell-1}\binom{m-1}{b-1}=-\frac1{20}
\quad\text{于 }\mathbb F_p.
\tag{9}
\]

由 \(m=p-4\equiv-4\pmod p\) 及
\(\binom mb=(m/b)\binom{m-1}{b-1}\)，全部正核心块在零阶式中的
总贡献为

\[
(-1)^{\ell-1}\binom mb=\frac1{5b}.
\tag{10}
\]

第三族零阶 Hasse 式的总和为零。因此

\[
\boxed{\sum_{H\in\mathcal H_0}\varepsilon_H=-\frac1{5b}.}
\tag{11}
\]

第三族在每个位置上的带符号点度为 \(-1/20\)。若 \(u\in U\)，
则全部 (2) 都包含 \(u\)，故正核心贡献仍是 (10)；若
\(y\in Y\setminus U\)，则 (2) 没有一个包含 \(y\)。于是

\[
\boxed{
\sum_{\substack{H\in\mathcal H_0\\u\in H}}
\varepsilon_H=-\frac{b+4}{20b},
\qquad
\sum_{\substack{H\in\mathcal H_0\\u\notin H}}
\varepsilon_H=\frac1{20}
\quad(u\in U),}
\tag{12}
\]

以及

\[
\boxed{
\sum_{\substack{H\in\mathcal H_0\\y\in H}}
\varepsilon_H=-\frac1{20},
\qquad
\sum_{\substack{H\in\mathcal H_0\\y\notin H}}
\varepsilon_H=\frac{b-4}{20b}
\quad(y\in Y\setminus U).}
\tag{13}
\]

这里第二列分别由 (11) 减去第一列得到。特别地，(12) 的右式非零，
故每个 \(u\in U\) 都被某个实际零核心块避开；结合 (6)，该块仍
必须命中 \(U\setminus\{u\}\)。当 \(b\ne4\) 时，(13) 的右式
也非零，所以每个尾外位置也被某个零核心块避开。此时
\(\mathcal H_0\) 自身既两两相交又没有公共位置。

式 (11)--(13) 虽写在 \(\mathbb F_p\) 中，但每一项都来自一个
实际 \(0/1\) 位置块，系数只有其真实长度决定的符号
\(\varepsilon_H\)。这与给抽象轨道任意有限域权重不同。

## 4. 从有限域点度提升为实际块数

对 \(c\in\mathbb F_p\)，记

\[
\|c\|_p=\min\{|n|:n\in\mathbb Z,\ n\equiv c\pmod p\},
\qquad \mu_p=\|20^{-1}\|_p.
\tag{14}
\]

若 \(k\) 个符号 \(\pm1\) 的整数和模 \(p\) 等于 \(c\)，则
\(k\ge\|c\|_p\)。对 (12) 的避开式和 (13) 的包含式应用这一
事实，得到

\[
\#\{H\in\mathcal H_0:u\notin H\}\ge\mu_p
\quad(u\in U),
\tag{15}
\]

\[
\#\{H\in\mathcal H_0:y\in H\}\ge\mu_p
\quad(y\in Y\setminus U).
\tag{16}
\]

由 (6)，每个 \(H\in\mathcal H_0\) 至少使用一个 \(U\)-位置，
故 \(|H\setminus U|\le7\)。对 (16) 的实际入射作双计数，同时对
(15) 的实际避开入射作双计数，分别得到

\[
\boxed{
|\mathcal H_0|\ge L(p,r):=\max\left\{
\left\lceil\frac{(2p+8-r)\mu_p}{7}\right\rceil,
\left\lceil\frac{r\mu_p}{r-1}\right\rceil
\right\}.}
\tag{17}
\]

第二项使用每个 \(H\) 命中 \(U\)，因而至多避开 \(r-1\) 个
\(U\)-位置。对 16 个算术异常型，第一项总是较强；精确值如下。

\[
\begin{array}{c|c|c|c|c|c}
p&\ell&b&r&\mu_p&L(p,r)\\ \hline
11&7&2&5&5&18\\
13&6&3&3&2&9\\
13&8&3&5&2&9\\
19&6&1&5&1&6\\
19&8&1&7&1&6\\
23&6&3&3&8&59\\
23&8&3&5&8&56\\
43&7&3&4&15&193\\
101&6&2&4&5&148\\
101&8&2&6&5&146\\
233&7&4&3&35&2355\\
467&7&5&2&70&9400\\
701&6&4&2&35&7040\\
701&8&4&4&35&7030\\
1399&8&5&3&70&28030\\
2521&8&6&2&126&90864
\end{array}
\tag{18}
\]

结合 (7)，任一幸存唯一尾配置必须同时承载至少
\(\binom{L(p,r)}2\) 个按不同实际块对索引的非零商交实例。这里
不声称这些交集或交换关系彼此不同。

## 5. \(b\ge4\) 时尾不能包含于零核心块

**引理 1（逐零核心块的锚点排除）。** 若 \(b\ge4\)，则

\[
\boxed{U\nsubseteq H\qquad(H\in\mathcal H_0).}
\tag{19}
\]

**证明。** 假设 \(U\subseteq H\)。由 (1) 及
\(\sigma(H)=3a\)，

\[
\sigma(H\setminus U)=bx.
\]

因为 \(b\ge4\)，有 \(p-b\le p-4=|X|\)，可从 \(X\) 取
\(p-b\) 个位置组成 \(W\)。于是

\[
\sigma\bigl((H\setminus U)\mathbin{\dot\cup}W\bigr)
=bx+(p-b)x=0.
\]

该位置子序列非空，并且它避开非空的 \(U\)，故是 \(Z\) 的真
子序列，违反 \(Z\) 的原子性。证毕。

这一步使用的是实际位置、实际和值与 \(Z\) 的原子性；它不是由
有限域 Hasse 权重推出的。

## 6. 排除全部三个二点尾异常型

现在设 \(r=|U|=2\) 且 \(b\ge4\)，写 \(U=\{u_0,u_1\}\)。由
(6) 与 (19)，每个 \(H\in\mathcal H_0\) 都恰含 \(U\) 的一个
位置。因此

\[
\sum_{H\in\mathcal H_0}|H\cap U|\varepsilon_H
=\sum_{H\in\mathcal H_0}\varepsilon_H.
\tag{20}
\]

然而对 (12) 的包含式在两个 \(u_i\) 上求和，左边是 (20) 的
左端，故 (11)--(12) 强制

\[
-\frac{2(b+4)}{20b}=-\frac1{5b}.
\]

等价于 \(b+2=0\pmod p\)，这对 \(4\le b\le6<p-2\) 不可能。
矛盾。

等价地，(12) 的避开式说明两类实际块

\[
\mathcal H_i=\{H\in\mathcal H_0:H\cap U=\{u_i\}\}
\]

各自的带符号总和都是 \(1/20\)，而 (11) 要求两类之和是
\(-1/(5b)\)；两者仅在 \(b=-2\) 时相容。并且每类实际块数至少
\(\mu_p\)，任取两类各一个块时，(7) 给出其交集位于
\(Y\setminus U\) 且商和非零。

原 16 型中 \(r=2\) 的恰是 (4) 的三型，故全部被排除。剩余必要表
缩为

\[
\begin{array}{c|c}
p&(\ell,b)\\ \hline
11&(7,2)\\
13&(6,3),(8,3)\\
19&(6,1),(8,1)\\
23&(6,3),(8,3)\\
43&(7,3)\\
101&(6,2),(8,2)\\
233&(7,4)\\
701&(8,4)\\
1399&(8,5)
\end{array}
\tag{21}
\]

## 7. 证据边界与停止线

- **PROVED：**实际唯一尾 \(U\)、全部实际零核心块及逐位置身份满足
  (5)--(13)；(15)--(18) 是普通整数块数下界。
- **PROVED：**逐块锚点引理 (19)；由此排除 (4) 的三个二点尾
  异常型。该排除是一般论证，不是固定素数穷举。
- **PROVED：**每对不同实际零核心块满足 (7)，所以 (18) 所计的
  是实际块对索引的非零商交义务。
- **INCOMPLETE：**余下 13 型尚未排除。本文没有构造实现
  (5)--(13) 的统一群标号，更没有构造使每个 \(Z\setminus H\)
  成为近 Davenport 补原子的内部零和自由结构。
- 旧 21 式证书只是可任意加权的有限域轨道解；本文的结论则条件于
  一个假想冻结配置，直接计数其中必须存在的实际 \(0/1\) 位置块。
  二者都不是冻结反例，但不能混为同一种“相容证书”。

下一步若继续排除 (21)，至少要保留 \(|H\cap U|=1,\ldots,r-1\)
的实际迹层、迹的统一商和以及不同 \(H\) 的补原子交换。仅把这些
块再压回总数或 \(T\)-入射和，会丢失本页排除二点尾所用的关键
条件 (19)--(20)。

有限脚本只复核分式恒等式、异常表和整数下界；不替代上述全称证明。
