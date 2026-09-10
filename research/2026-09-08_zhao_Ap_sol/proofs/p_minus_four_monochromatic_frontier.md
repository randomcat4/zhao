# \(p-4\) 单高度同商纤维前沿

STATUS: INCOMPLETE

## 1. 冻结对象

设 \(p\ge11\) 为素数。沿用 ROUTE-A4 的冻结设置：\(Z\) 是长度
\(3p+4\) 的实际零和原子，\(T\in\mathcal F_3\) 长度为
\(6,7\) 或 \(8\)，且 \(B=Z\setminus T\) 的商像是长度
\(3p-4,3p-3\) 或 \(3p-2\) 的 \(C_p^3\) 原子。

设非零商值 \(q\) 在 \(B\) 中有 \(m=p-4\) 个位置，并假设这些
位置的实际高度全等于 \(h\)。记该位置集为

\[
X,\qquad |X|=m=p-4.
\tag{1}
\]

这是实际重数上界 \(p-4\) 首次不再排除的单高度纤维。本文给出
所有包含 \(X\)-三元组的短块类型、完整点/对/三点余部方程以及
\(T\)-交叉相交的严格后果；现有接口尚未排除 (1)。

## 2. 含 \(X\)-三元组的全部类型

任取 \(W\in\binom X3\)。三点覆盖定理给出包含 \(W\) 的短块
\(A\in\mathcal F_\lambda\)。写

\[
b=|A\cap X|,\qquad U=A\setminus X,\qquad \ell=|A|.
\]

因为 \(\ell\le8<p\)、\(q\ne0\)，若 \(U=\varnothing\) 就会有
\(\bar\sigma(A)=bq\ne0\)。又若 \(U\cap T=\varnothing\)，则
\(A\subset B\) 是 \(\bar B\) 的非空真商零和子序列。因此

\[
U\ne\varnothing,\qquad U\cap T\ne\varnothing,\qquad
3\le b\le\ell-1.
\tag{2}
\]

固定 \(U\) 后，每个 \(V\in\binom Xb\) 都给出同一实际和的短块
\(V\mathbin{\dot\cup}U\)，因为 \(X\) 中所有位置具有相同商值与
高度。故这里没有上一层的子集和扩张障碍。

全部允许型恰为

\[
\begin{array}{c|c|c|c}
\lambda&\ell&b&|U|=\ell-b\\ \hline
1&4&3&1\\
1&5&3,4&2,1\\
1&6&3,4,5&3,2,1\\ \hline
2&4&3&1\\
2&5&3,4&2,1\\
2&6&3,4,5&3,2,1\\
2&7&3,4,5,6&4,3,2,1\\ \hline
3&6&3,4,5&3,2,1\\
3&7&3,4,5,6&4,3,2,1\\
3&8&3,4,5,6,7&5,4,3,2,1.
\end{array}
\tag{3}
\]

相应余部满足精确的商值和高度条件

\[
\boxed{
|U|=\ell-b,\qquad
\bar\sigma(U)=-bq,\qquad
h(U)=\lambda-bh,\qquad U\cap T\ne\varnothing.}
\tag{4}
\]

反之，每个满足 (4) 的位置子集 \(U\) 同时生成全部
\(\binom mb\) 个 \(V\mathbin{\dot\cup}U\)。

## 3. 最小有限余部变量

为同时写点、对、三点方程，需要允许 \(b=1,2\)。定义

\[
\mathcal U_{\lambda,\ell,b}
=\left\{U\subset Z\setminus X:
\begin{array}{l}
|U|=\ell-b,\ \bar\sigma(U)=-bq,\\
h(U)=\lambda-bh,\ U\cap T\ne\varnothing
\end{array}\right\},
\qquad
N_{\lambda,\ell,b}=|\mathcal U_{\lambda,\ell,b}|.
\tag{5}
\]

指标范围是

\[
\begin{aligned}
I_1&=\{(\ell,b):2\le\ell\le6,\ 1\le b\le\ell-1\},\\
I_2&=\{(\ell,b):4\le\ell\le7,\ 1\le b\le\ell-1\},\\
I_3&=\{(\ell,b):6\le\ell\le8,\ 1\le b\le\ell-1\}.
\end{aligned}
\tag{6}
\]

共有 \(15+18+18=51\) 个非负整数变量；其中 \(b\ge3\) 的
28 个变量正是 (3)。

以下 (7)--(9) 都是 \(\mathbb F_p\) 中的等式；只有 (10) 是普通
非负整数计数不等式。

固定 \(x,y,z\in X\) 两两不同。每个余部 \(U\) 生成的、包含固定
\(k\)-位置集的替换块数为

\[
\binom{m-k}{b-k}.
\]

所以一点方程为

\[
\boxed{
\sum_{(\ell,b)\in I_\lambda}
(-1)^{\ell-1}\binom{m-1}{b-1}N_{\lambda,\ell,b}
=
\begin{cases}
-3/4,&\lambda=1,\\
3/10,&\lambda=2,\\
-1/20,&\lambda=3.
\end{cases}}
\tag{7}
\]

令

\[
D_\lambda=
\sum_{\substack{(\ell,b)\in I_\lambda\\b\ge2}}
(-1)^\ell\binom{m-2}{b-2}N_{\lambda,\ell,b}.
\]

二点 Hasse 方程恰为

\[
\boxed{8D_1+10D_2=3,\qquad 2D_1-10D_3=1.}
\tag{8}
\]

再令

\[
\Delta_\lambda=
\sum_{\substack{(\ell,b)\in I_\lambda\\b\ge3}}
(-1)^{\ell-1}\binom{m-3}{b-3}N_{\lambda,\ell,b}.
\]

三点 Hasse 方程及普通覆盖下界分别为

\[
\boxed{4\Delta_1+10\Delta_2+20\Delta_3=-1,}
\tag{9}
\]

\[
\boxed{
\sum_{\lambda=1}^3
\sum_{\substack{(\ell,b)\in I_\lambda\\b\ge3}}
\binom{m-3}{b-3}N_{\lambda,\ell,b}
\ge \left\lceil\frac{p-1}{20}\right\rceil.}
\tag{10}
\]

式 (7)--(10) 对每个固定点、对、三元组相同，这是单高度替换带来
的真实均匀性，不是平均化假设。

## 4. \(T\) 与交叉相交给出的余部几何

式 (4) 的 \(U\cap T\ne\varnothing\) 只用了 \(\bar B\) 原子性。
还可进一步得到以下全称约束。

取 \(U\in\mathcal U_{\lambda,\ell,b}\) 和任意
\(F\in\mathcal F_3\)。所有 \(V\mathbin{\dot\cup}U\) 都与 \(F\)
相交。若 \(F\cap U=\varnothing\)，则 \(F\cap X\) 必须命中
\(X\) 的每个 \(b\)-位置集，所以

\[
|F\cap X|\ge m-b+1.
\]

因此只要

\[
b\le m-8=p-12,
\tag{11}
\]

\(U\) 就是整个 \(\mathcal F_3\) 的横截集。特别地，若同时
\(|U|=1\)，它会成为 \(\mathcal F_3\) 的公共点，与已知“无公共
点”矛盾。因此

\[
\boxed{
N_{\lambda,\ell,\ell-1}=0
\quad\text{只要}\quad \ell-1\le p-12.}
\tag{12}
\]

边界具体为：

- \(p\ge19\) 时，所有十二个单点余部变量都为零；
- \(p=17\) 时，九个满足 \(b\le5\) 的单点余部变量为零；
- \(p=13\) 时，只强制 \(N_{1,2,1}=0\)；
- \(p=11\) 时，(11) 不给单点消失。

类似地，若
\[
U\in\mathcal U_{\lambda,\ell,b},\qquad
U'\in\mathcal U_{3,\ell',b'},\qquad b+b'\le m,
\]
则
\[
U\cap U'\ne\varnothing;
\tag{13}
\]
否则可取不交的 \(V\in\binom Xb,V'\in\binom X{b'}\)，得到不交的
\(\mathcal F_\lambda\) 与 \(\mathcal F_3\) 块。若
\(\lambda=3\)，不同三倍块交集的商和非零还给出

\[
\bar\sigma(U\cap U')\ne0.
\tag{14}
\]

对每个 \(U\in\mathcal U_{3,\ell,b}\)，拿生成块与原来的 \(T\)
比较也得到

\[
\bar\sigma(U\cap T)\ne0.
\tag{15}
\]

当 \(p\ge19\) 时，所有 \(b,b'\le7\) 都满足 \(b+b'\le m\)，所以
(13)--(15) 施加在全部余部族上。

## 5. 标量 Hasse 系统仍相容

即使加入 \(p\ge19\) 时的全部单点余部消失，(7)--(9) 仍不矛盾。
在 \(\mathbb F_p\) 中使用

\[
\binom{m-k}{b-k}
=\binom{p-4-k}{b-k}
\equiv\binom{-4-k}{b-k},
\]

下列六个变量给出一个对每个 \(p\ge11\) 都合法的形式解：

\[
\begin{array}{c|c}
(\lambda,\ell,b)&N_{\lambda,\ell,b}\\ \hline
(1,6,1)&3/4\\
(2,6,1)&6/5\\
(2,7,2)&-3/10\\
(3,6,1)&3/10\\
(3,7,2)&-1/5\\
(3,8,3)&1/20,
\end{array}
\qquad
\text{其余变量取 }0.
\tag{16}
\]

所有非零变量的余部大小都是五，因此 (16) 不使用任何被 (12)
排除的变量。直接代入得到

\[
(P_1,P_2,P_3)=(-3/4,3/10,-1/20),
\]
\[
(D_1,D_2,D_3)=(0,3/10,-1/10),
\qquad
(\Delta_1,\Delta_2,\Delta_3)=(0,0,-1/20),
\]

恰满足 (7)--(9)。把分数解释为模 \(p\) 剩余类后都可取非负整数
代表；特别地 \(20N_{3,8,3}\equiv1\)，其最小正代表自动满足
(10) 的数量级下界。

式 (16) 不是实际余部族构造，因为它没有实现 (4) 的商值/高度目标
和 (13)--(15) 的逐集合交型。它只严格证明：点、对、三点的聚合
Hasse 方程，即使再删去全部单点余部，仍不足以排除单高度纤维。

纯集合层面的停顿也是真实的：六点集的全部五点子集两两相交且总
交为空，所以“余部大小五、交叉相交、无公共点”本身没有矛盾。

## 6. 最小新变量与停止线

- **PROVED：**类型表 (3)、余部条件 (4)、51 变量方程
  (7)--(10)、横截阈值 (11)--(12) 及交型 (13)--(15)。
- **INCOMPLETE：**尚未从这些条件排除 \(X=x^{p-4}\)。
- 下一步不能只增加按 \((\lambda,\ell,b)\) 聚合的标量矩。必须保留
  每个实际余部 \(U\) 的身份，并联立：
  1. \(U\cap T\) 与 \(U\cap U'\) 的非零商和；
  2. 当 \(|U|=2\) 且 \(U\) 为 \(\mathcal F_3\) 横截时强制的
     \(d_3(U)=1/10\) 及完整二点共度；
  3. 对 \(\lambda=3\) 的余部，
     \(Z\setminus(V\mathbin{\dot\cup}U)\) 的近 Davenport 原子性。

\(p=7\) 不在本文量词内。有限计算只核对矩阵与边界，不替代全称
证明。
