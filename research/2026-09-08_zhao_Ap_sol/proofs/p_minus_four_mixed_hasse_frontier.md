# \(p-4\) 单高度纤维的混合 Hasse 前沿

STATUS: INCOMPLETE

## 1. 设置与结论

设 \(p\ge11\) 为素数。沿用 ROUTE-A4 的冻结设置：\(Z\) 是长度
\(3p+4\) 的实际零和原子，\(T\in\mathcal F_3\) 的长度
\(s\in\{6,7,8\}\)，且 \(B=Z\setminus T\) 的商像是
\(C_p^3\) 中的原子。设

\[
X=x^{p-4}\subset B,
\qquad m=|X|=p-4,
\qquad \bar x=q\ne0,
\tag{1}
\]

即 \(X\) 的位置具有同一商值和同一实际高度。再记

\[
Y=Z\setminus X,
\qquad Q=Y\setminus T=B\setminus X.
\tag{2}
\]

于是

\[
|Y|=2p+8,
\qquad |Q|=2p+8-s.
\]

本文证明三件事。

1. 固定 \(y\in Y\) 的一点、一个 \(X\)-点加 \(y\) 的二点、两个
   \(X\)-点加 \(y\) 的三点 Hasse 方程，给出第 3 节的完整混合
   余部系统。它严格排除
   `p_minus_four_monochromatic_frontier.md` 的六变量形式解。
2. 每个 \(y\in Y\) 都属于某个 \(X\)-交数至少二的余部。若
   \(p\ge19\)，这些余部都是大小至多六的
   \(\mathcal F_3\)-横截集。
3. 混合线性系统仍不矛盾。第 7 节对每个
   \(s=6,7,8\) 给出一个无单点余部、尊重
   \(T\mid Q\) 分区并满足全部 21 条零至三阶方程的显式
   \(\mathbb F_p\)-加权证书。

第三项不是实际块族：它没有实现余部的统一商和、高度、非零商交或
补原子性。因此本页给出新的全称必要条件和严格停止线，但尚未排除
(1)。

## 2. 逐外点余部变量

对任意短块 \(A\in\mathcal F_\lambda\)，写

\[
V=A\cap X,
\qquad U=A\cap Y,
\qquad b=|V|,
\qquad \ell=|A|.
\]

因为 \(\bar B\) 是原子，\(A\cap T=\varnothing\) 会使
\(A\subset B\) 成为非空真商零和子序列。因此每个短块都满足

\[
U\cap T\ne\varnothing,
\qquad 0\le b\le\ell-1.
\tag{3}
\]

对 \(b\ge1\) 还能保留更强的逐余部商信息。写
\(P=U\cap T\)、\(U_Q=U\cap Q\)。若
\(\bar\sigma(P)=0\)，则

\[
V\mathbin{\dot\cup}U_Q\subset B,
\qquad
\bar\sigma(V\mathbin{\dot\cup}U_Q)=0.
\]

左边因 \(V\ne\varnothing\) 而非空，且长度至多八，故是
\(\bar B\) 的非空真商零和子序列，矛盾。因此

\[
\boxed{b\ge1\Longrightarrow
\varnothing\ne P\subsetneq T,\qquad\bar\sigma(P)\ne0.}
\tag{3a}
\]

这里 \(P\subsetneq T\) 还用到 \(\bar\sigma(T)=0\)。这条结论对
三族余部都成立，比只对 \(\mathcal F_3\) 块比较交集更强。

当 \(b\ge1\) 时，同值替换说明固定一个余部 \(U\) 后，所有
\(V'\in\binom Xb\) 都生成同族同长短块。令

\[
\mathcal U_{\lambda,\ell,b}
=\{U\subset Y:V\mathbin{\dot\cup}U\in\mathcal F_\lambda
\text{ 对每个 }V\in\tbinom Xb\},
\]

其中 \(b=0\) 时按 \(V=\varnothing\) 理解。记

\[
N_{\lambda,\ell,b}=|\mathcal U_{\lambda,\ell,b}|,
\qquad
M_{\lambda,\ell,b}(y)
=|\{U\in\mathcal U_{\lambda,\ell,b}:y\in U\}|.
\tag{4}
\]

长度窗为

\[
\begin{aligned}
\lambda=1 &: 2\le\ell\le6,\\
\lambda=2 &: 4\le\ell\le7,\\
\lambda=3 &: 6\le\ell\le8.
\end{aligned}
\]

这里的 \(N,M\) 是普通非负整数，并有精确的关联恒等式

\[
\boxed{
\sum_{y\in Y}M_{\lambda,\ell,b}(y)
=(\ell-b)N_{\lambda,\ell,b}.}
\tag{5}
\]

## 3. 固定 \(y\) 的完整混合方程

记

\[
(e_1,e_2,e_3)=
\left(-\frac34,\frac3{10},-\frac1{20}\right).
\]

下列等式都在 \(\mathbb F_p\) 中成立。固定 \(y\in Y\)。一点
方程逐族为

\[
\boxed{
P_\lambda(y):=
\sum_{\ell,b}(-1)^{\ell-1}
\binom mbM_{\lambda,\ell,b}(y)=e_\lambda.}
\tag{6}
\]

这里一个含 \(y\) 的余部生成 \(\binom mb\) 个含 \(y\) 的块，
所以 (6) 包括了 \(b=0\) 的块，并无漏项。

再固定 \(x_1\in X\)，令

\[
D_\lambda(y)=
\sum_{\ell,b\ge1}(-1)^\ell
\binom{m-1}{b-1}M_{\lambda,\ell,b}(y).
\tag{7}
\]

这是位置对 \(\{x_1,y\}\) 的带符号共度，故

\[
\boxed{
8D_1(y)+10D_2(y)=3,
\qquad
2D_1(y)-10D_3(y)=1.}
\tag{8}
\]

最后固定不同的 \(x_1,x_2\in X\)，令

\[
\Delta_\lambda(y)=
\sum_{\ell,b\ge2}(-1)^{\ell-1}
\binom{m-2}{b-2}M_{\lambda,\ell,b}(y).
\tag{9}
\]

这是三位置集 \(\{x_1,x_2,y\}\) 的带符号共度，故

\[
\boxed{
4\Delta_1(y)+10\Delta_2(y)+20\Delta_3(y)=-1.}
\tag{10}
\]

由于单高度替换，(7)--(10) 不依赖所选的 \(x_1,x_2\)，但必须对
每个 \(y\in Y\) 分别成立；这比只看纯 \(X\) 点、对、三点严格更强。

## 4. 求和后的新尾长矩

对 (6)、(8)、(10) 在 \(y\in Y\) 上求和并使用 (5)。令

\[
R_\lambda=
\sum_{\ell,b\ge1}(-1)^\ell(\ell-b)
\binom{m-1}{b-1}N_{\lambda,\ell,b},
\]

\[
S_\lambda=
\sum_{\ell,b\ge2}(-1)^{\ell-1}(\ell-b)
\binom{m-2}{b-2}N_{\lambda,\ell,b}.
\]

因为 \(|Y|=2p+8\equiv8\pmod p\)，得到

\[
\boxed{
8R_1+10R_2=24,
\qquad
2R_1-10R_3=8,}
\tag{11}
\]

\[
\boxed{
4S_1+10S_2+20S_3=-8.}
\tag{12}
\]

一点式还给出

\[
\boxed{
\sum_{\ell,b}(-1)^{\ell-1}(\ell-b)
\binom mbN_{\lambda,\ell,b}=8e_\lambda.}
\tag{13}
\]

这些是旧纯 \(X\) 方程没有记录的尾长矩。

例如，`p_minus_four_monochromatic_frontier.md` 的六变量解代入
(11)--(12) 后，三个左端依次为

\[
(15,5,-5),
\]

而所需值是 \((24,8,-8)\)。差分别为 \(-9,-3,3\)，对任何
素数 \(p\ge11\) 都非零。因此该特定形式解被混合 Hasse 方程严格
排除。

另一方面，`p_minus_four_single_height_probe.md` 的参数 (23)
给出恰好

\[
(24,8,-8).
\]

所以求和后的三条新式仍不能排除单高度纤维。

## 5. 真实覆盖与 \(T\mid Q\) 分区后果

令 \(C_\lambda(x_1,y)\) 与
\(C_\lambda(x_1,x_2,y)\) 分别表示包含所示位置集的普通块数。
同一个余部的替换数给出

\[
C_\lambda(x_1,y)=
\sum_{\ell,b\ge1}\binom{m-1}{b-1}
M_{\lambda,\ell,b}(y),
\]

\[
C_\lambda(x_1,x_2,y)=
\sum_{\ell,b\ge2}\binom{m-2}{b-2}
M_{\lambda,\ell,b}(y).
\]

整数提升后的二点、三点覆盖界逐 \(y\) 给出

\[
\begin{aligned}
C_1(x_1,y)+C_2(x_1,y)
&\ge\left\lceil\frac{p-3}{10}\right\rceil,\\
C_1(x_1,y)+C_3(x_1,y)
&\ge\left\lceil\frac{p-1}{10}\right\rceil,\\
\sum_{\lambda=1}^3C_\lambda(x_1,x_2,y)
&\ge\left\lceil\frac{p-1}{20}\right\rceil.
\end{aligned}
\tag{14}
\]

特别地，最后一式证明

\[
\boxed{
\forall y\in Y\ \exists(\lambda,\ell,b,U):
b\ge2,\quad y\in U\in\mathcal U_{\lambda,\ell,b}.}
\tag{15}
\]

这些余部的大小至多六。由 (3)，覆盖 \(Q\) 的每个余部至多含五
个 \(Q\)-位置。因此 (15) 至少强制

\[
\left\lceil\frac{|Y|}{6}\right\rceil
\quad\text{个不同余部，且其中至少}\quad
\left\lceil\frac{|Q|}{5}\right\rceil
\quad\text{个余部覆盖 }Q.
\tag{16}
\]

当 \(p\ge19\) 时，所有允许的 \(b\le7\) 都满足
\(b\le m-8\)。若某个生成余部 \(U\) 不命中
\(F\in\mathcal F_3\)，则 \(F\cap X\) 必须命中 \(X\) 的每个
\(b\)-集，迫使 \(|F\cap X|\ge m-b+1\ge9\)，与
\(|F|\le8\) 矛盾。因此

\[
\boxed{
p\ge19\Longrightarrow
Y\text{ 被大小至多六且均与 }T\text{ 相交的 }
\mathcal F_3\text{-横截余部覆盖}.}
\tag{17}
\]

若其中某个余部恰有两点，则仅由它是二点横截便可推出该位置对的
完整带符号共度

\[
(d_1,d_2,d_3)=\left(1,-\frac12,\frac1{10}\right).
\tag{18}
\]

事实上，把 \(\mathcal F_3\) 按与该二点集不交、只含第一点、只含
第二点、同时含两点分成四格。横截性使第一格为零；族总带符号和为
零，而两个点度均为 \(-1/20\)，故同时含两点一格为 \(-1/10\)，
即 \(d_3=1/10\)。代入两条二点方程即得 (18)。

这是新的真实结构约束，但横截数二本身尚未被已有接口排除。

## 6. 容量和同余块内交换为何尚不闭合

原始位置容量远大于 (14) 的需要。对固定 \(y\in Q\)，含 \(y\)、
大小为 \(r\) 且命中 \(T\) 的候选余部数为

\[
\binom{|Y|-1}{r-1}-\binom{|Q|-1}{r-1};
\]

对 \(y\in T\) 则为 \(\binom{|Y|-1}{r-1}\)。尤其一个
\((\lambda,\ell,b,r)=(1,5,3,2)\) 余部已经生成

\[
\binom{m-2}{1}=p-6
\]

个包含固定 \(\{x_1,x_2,y\}\) 的块，并生成
\(\binom{m-1}{2}=\binom{p-5}{2}\) 个包含固定
\(\{x_1,y\}\) 的块，均超过 (14) 所需量级。因此普通容量不能
迫使大量不同余部通过同一个 \(y\)。

集合层面甚至可同时保留横截结构。取一个二点横截
\(E\subset T\) 及 \(z_0\in Y\setminus E\)。对 \(y\notin E\) 置
\(U_y=E\cup\{y\}\)，而用同一个 \(U_E=E\cup\{z_0\}\) 覆盖
\(E\) 的两点。把这些三点余部都配上 \(b=3,\ell=6\)。它们覆盖
\(Y\)、全部命中 \(T\)，生成的 \(a\)-块等长，且全是
\(\mathcal F_3\)-横截。这样的无公共点、两两相交
\(\mathcal F_3\) 抽象族也确实存在：

- \(s=6\) 时，在 \(T\) 加一点所得七点集上取全部六点集；
- \(s=7\) 时，取 \(T\) 的全部六点集并加入 \(T\)；
- \(s=8\) 时，在 \(T\) 内取一个含 \(E\) 的七点集，取其全部
  六点集并加入 \(T\)。

这只是集合容量模型；统一商和条件会要求
\(\bar\sigma(U_y)=-3q\)，该模型没有实现这一条件。

补原子交换也不能区分同一个余部产生的完整替换层。若
\(U\in\mathcal U_{3,\ell,b}\) 且
\(V,V'\in\binom Xb\) 不同，令
\(A=V\dot\cup U,A'=V'\dot\cup U\)。则

\[
\bar\sigma(A\cap A')
=(-b+|V\cap V'|)q\ne0,
\tag{19}
\]

因为 \(1\le b-|V\cap V'|\le7<p\)。所以不同
\(3a\) 块的非零商交在同余部层自动满足。另一方面，交换差只由
\(V\setminus V'\) 与 \(V'\setminus V\) 组成；两边全是实际值
\(x\)。任何等商和子交换因两边项数小于 \(p\) 而必须取相同项数，
从而也有相同实际和。相应有符号关系完全分解为二位置同值退化。
因此补原子交换若只在固定 \(U\) 的替换层内使用，不会给出新矛盾；
必须比较两个不同余部。

## 7. 完整混合线性系统的显式相容证书

最后说明逐 \(y\) 方程本身仍相容，而且可同时保留 (3) 和“无单点
余部”。固定 \(s=|T|\)，对
\(r=\ell-b\ge2\) 及 \(1\le j\le r\)，令

\[
\mathcal O_{r,j}
=\{U\subset Y:|U|=r,\ |U\cap T|=j\}.
\]

给每个 \(U\in\mathcal O_{r,j}\) 同一形式权
\(c_{\lambda,\ell,b,j}\in\mathbb Q\)，未列出的权为零。每个
余部再生成全部 \(b\)-元 \(X\)-替换。模 \(p\) 的总权及固定点度
分别为

\[
N_{\lambda,\ell,b}
=\sum_jc_{\lambda,\ell,b,j}
\binom sj\binom{2p+8-s}{r-j},
\tag{20}
\]

\[
M^T_{\lambda,\ell,b}
=\sum_jc_{\lambda,\ell,b,j}
\binom{s-1}{j-1}\binom{2p+8-s}{r-j},
\tag{21}
\]

\[
M^Q_{\lambda,\ell,b}
=\sum_jc_{\lambda,\ell,b,j}
\binom sj\binom{2p+7-s}{r-j-1}.
\tag{22}
\]

由于所有下指标至多八且 \(p\ge11\)，可在 \(\mathbb F_p\) 中把
上指标分别约为 \(8-s\) 与 \(7-s\)。下表给出三个证书。

### \(s=6\)

\[
\begin{array}{c|c|c|c|c@{\qquad}c|c|c|c|c}
\lambda&\ell&b&j&c&\lambda&\ell&b&j&c\\ \hline
1&2&0&1&-203/18&1&2&0&2&4699/1440\\
1&3&0&1&-233/18&1&3&1&1&1381/1152\\
1&3&1&2&-37/60&1&4&1&1&2245/1152\\
1&4&2&1&-53/576&1&4&2&2&257/2880\\
1&5&2&1&-161/576&1&5&3&1&-1/48\\
2&4&0&2&23/50&2&4&0&3&509/4800\\
2&4&1&1&1/60&2&4&1&2&-7/1440\\
2&4&2&1&-7/2880&2&5&0&3&8/15\\
2&5&1&2&2/75&3&6&0&4&43/7200\\
3&6&0&5&-1/360&3&6&1&3&-37/19200\\
3&6&2&2&-17/14400&&&&
\end{array}
\tag{23}
\]

### \(s=7\)

\[
\begin{array}{c|c|c|c|c@{\qquad}c|c|c|c|c}
\lambda&\ell&b&j&c&\lambda&\ell&b&j&c\\ \hline
1&2&0&1&-6221/672&1&2&0&2&-37/36\\
1&3&0&2&-233/63&1&3&1&1&493/672\\
1&4&1&2&2245/4032&1&4&2&1&15/448\\
1&5&2&2&-23/288&1&5&3&1&-1/28\\
2&4&0&3&71/280&2&4&0&4&34/525\\
2&4&1&2&-11/5040&2&4&2&1&-1/240\\
2&5&0&4&32/105&2&5&1&3&2/175\\
3&6&0&5&1/288&3&6&0&6&-1/420\\
3&6&1&4&-37/33600&3&6&2&3&-17/33600
\end{array}
\tag{24}
\]

### \(s=8\)

\[
\begin{array}{c|c|c|c|c@{\qquad}c|c|c|c|c}
\lambda&\ell&b&j&c&\lambda&\ell&b&j&c\\ \hline
1&2&0&1&21/32&1&2&0&2&-8293/2688\\
1&3&0&3&-233/168&1&3&1&1&-7/32\\
1&3&1&2&493/2688&1&4&1&3&2245/10752\\
1&4&2&1&1/32&1&4&2&2&15/1792\\
1&5&2&3&-23/768&1&5&3&2&-1/112\\
2&4&0&1&-7/80&2&4&0&4&191/1200\\
2&4&1&1&1/80&2&4&1&3&-11/13440\\
2&4&2&2&-1/960&2&5&0&5&4/21\\
2&5&1&4&1/175&3&6&0&1&1/160\\
3&6&0&6&9/4480&3&6&1&5&-37/53760\\
3&6&2&4&-17/67200&&&&
\end{array}
\tag{25}
\]

所有分母的素因子都在 \(\{2,3,5,7\}\)，所以对每个
\(p\ge11\) 都可约入 \(\mathbb F_p\)。把 (20)--(22) 代入，
三张表逐一满足以下 21 条等式：

- 每个 \(\lambda\) 的零阶带符号总权为零；
- 三条纯 \(X\) 一点式、两条纯 \(X\) 二点式和一条纯 \(X\)
  三点式；
- 对 \(y\in T\) 的三条 (6)、两条 (8) 和一条 (10)；
- 对 \(y\in Q\) 的同样六条式。

每个表还含非零的 \(b=3\) 项，所有出现的余部都有
\(r\ge2,j\ge1\)。因此证书既没有单点余部，也没有不命中 \(T\)
的余部。精确代入由
`verify_p_minus_four_mixed_hasse.py` 用有理数运算复核。

这些 \(c\) 是有限域加权松弛，不是 \(0/1\) 块指标。它不保证：

1. 同一余部只能落入实际允许的商和/高度类；
2. 普通计数的整数非负性与全部容量同时实现；
3. 不同余部间的交叉相交和非零商交；
4. 每个 \(3a\) 块补集的近 Davenport 原子性。

故该证书不构成冻结反例；它只严格证明，即使加入
\(T\mid Q\) 分区、禁止单点余部、全部逐外点混合 Hasse 方程以及
全局零阶式，线性有限域层仍相容。

## 8. 精确停止线

- **PROVED：**逐 \(y\) 混合方程 (6)--(10)、尾长矩
  (11)--(13)、逐余部非零 \(T\)-部分 (3a)、覆盖横截定理
  (15)--(18)，以及固定余部内补原子交换必退化为同值二位置关系。
- **PROVED：**旧六变量证书对每个 \(p\ge11\) 都被排除。
- **INCOMPLETE：**尚未排除实际单高度纤维 \(X=x^{p-4}\)。三张
  加权证书证明混合 Hasse 线性层本身不能闭合。
- 下一步最小的新变量必须同时记录两个不同余部
  \(U,U'\) 的实际身份、固定商和值条件、\(U\cap U'\) 与
  \(U\cap T\) 的非零商和，以及相应两个补原子的交换关系；只记录
  \(|U\cap T|\) 或逐点度仍会落入 (23)--(25) 的松弛。

\(p=7\) 不在本文量词内。有限计算只核对显式有理证书，不替代
全称推导。
