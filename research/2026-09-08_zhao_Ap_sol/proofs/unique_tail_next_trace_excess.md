# 唯一正核心尾的迹盈余与诱导补原子前沿

STATUS: PROVED_HERE / STRICT_GLOBAL_STRENGTHENING / REMAINDER_INCOMPLETE

## 1. 范围与结论

设 \(p\ge11\) 为素数，处于 \(p-4\) 单高度纤维分支。沿用

\[
X=x^{p-4}\subset B\subset Z,\qquad
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

其中 \(\ell\in\{6,7,8\}\)、\(1\le b\le6\)。全部正核心
\(F_3\) 块为 \(V\mathbin{\dot\cup}U\)，
\(V\in\binom Xb\)。零核心实际位置族记为

\[
\mathcal H_0=\{H\in\mathcal F_3:H\cap X=\varnothing\}.
\tag{2}
\]

本文证明三项严格位置级加强。

1. 对每个实际 \(F_3\) 块 \(H\)，诱导补集
   \(\overline{Z\setminus H}\) 是 \(C_p^3\) 中的零和原子；因此
   \(H\) 横截 \(Z\) 内完整诱导的 \(F_1,F_2,F_3\) 短谱，而不只是
   一份预先命名的块表。不同 \(F_3\) 块的交集还有非零商和。
2. 令

   \[
   \mu_p=\|20^{-1}\|_p,\qquad
   \nu(p,r,b)=
   \left\|\frac{4-r(b+4)}{20b}\right\|_p.
   \tag{3}
   \]

   则零核心实际块数满足新的全局下界

   \[
   \boxed{
   |\mathcal H_0|\ge L^+(p,r,b):=
   \max\left\{
   \left\lceil
   \frac{(2p+8-r)\mu_p+\nu(p,r,b)}7
   \right\rceil,
   \left\lceil\frac{r\mu_p}{r-1}\right\rceil
   \right\}.}
   \tag{4}
   \]

   相比只用“每块至少命中一个尾点”的旧下界，(4) 保留每块额外
   尾迹所消耗的尾外容量。它在 13 个幸存型中的 11 个型上严格更强。
3. 当 \(b\ge4\) 时，每个零核心块的尾迹真包含于 \(U\)。除已排除
   的三个二点尾外，三个幸存型还满足：

   \[
   \begin{array}{c|c|c|c}
   (p,\ell,b)&|\mathcal H_0|\text{ 下界}
   &\text{强迫的多点迹块}&\text{附加交结构}\\ \hline
   (233,7,4)&2364&\#\{|H\cap U|=2\}\ge58
   &\ge1628\text{ 对尾迹不交、尾外商交非零的块对}\\
   (701,8,4)&7065&\#\{|H\cap U|\ge2\}\ge123&--\\
   (1399,8,5)&28076&\#\{|H\cap U|=2\}\ge322
   &\ge9310\text{ 对尾迹不交、尾外商交非零的块对}
   \end{array}
   \tag{5}
   \]

这些都是条件于假想冻结配置的实际位置结论，不是局部候选、形式
轨道解或反例。本文没有排除新的幸存类型。

## 2. 重建完整诱导短谱与每个 \(F_3\) 补原子

先不使用任何预先命名的尾表，直接考察 \(Z\) 的非空真位置子序列
\(K\)，满足 \(\bar\sigma(K)=0\)。锚点线支撑结论给

\[
\sigma(K)\in\{\pm a,\pm2a,\pm3a\}.
\tag{6}
\]

在本文使用的两种情形中负系数都不可能：其一是 \(|K|\le8\) 的
诱导短块；其二是后文补原子分拆中选取的较短边，此时先只需使用
已有低长度排除给出的 \(|H|\ge4\)，所以
\(|Z\setminus H|\le3p\)，故 \(|K|\le\lfloor3p/2\rfloor\)。若
\(\sigma(K)=-ta\)、\(1\le t\le3\)，给 \(K\) 补入
\(t\le p-4\) 个外部 \(a\)-锚点；在第二种情形其长度至多
\(\lfloor3p/2\rfloor+3\le3p-2\)，从而得到禁用实际零和。因此在
这两种使用点只剩
\(\sigma(K)=ta\)、\(t=1,2,3\)。正系数表示的锚点长度界给

\[
|K|\le5+t.
\tag{7}
\]

又因为 \(R\) 没有 \(H=\langle a\rangle\) 上的单点，且已有
\(N_k^R(2a)=N_k^R(3a)=0\)（\(1\le k\le3\)），三族完整诱导短谱
恰落在

\[
\mathcal F_1:2\text{--}6,\qquad
\mathcal F_2:4\text{--}7,\qquad
\mathcal F_3:6\text{--}8.
\tag{8}
\]

这里 \(F_3\) 的下界六还可直接由下述补原子与
\(D(C_p^3)=3p-2\) 得到。

固定任意实际 \(H\in\mathcal F_3\)，令 \(B_H=Z\setminus H\)。
由于 \(\sigma(Z)=0\)、\(\sigma(H)=3a\)，有
\(\bar\sigma(B_H)=0\)。若 \(\bar B_H\) 不是零和原子，则可写成
两个非空商零和位置块；取其中较短者 \(E\)。于是

\[
|E|\le|B_H|/2\le3p/2.
\]

由 (6) 及上一段的负系数排除，
\(\sigma(E)=\mu a\)、\(\mu\in\{1,2,3\}\)，再由 (7) 得
\(|E|\le8\)。集合 \(H\) 与 \(E\) 不交，故
\(H\mathbin{\dot\cup}E\) 的和是 \((3+\mu)a\)。补入
\(p-(3+\mu)\) 个外部锚点，得到长度至多

\[
8+8+p-4=p+12\le3p-2
\]

的非空实际零和，矛盾。因此

\[
\boxed{\overline{Z\setminus H}\text{ 是 }C_p^3\text{ 中的零和原子}}
\qquad(H\in\mathcal F_3).
\tag{9}
\]

现在任取 \(K\in\mathcal F_1\cup\mathcal F_2\cup\mathcal F_3\)。若
\(K\cap H=\varnothing\)，则 \(K\) 是 \(B_H\) 的非空真商零和
子序列；其长度至多八，而
\(|B_H|\ge3p-4>8\)。这违反 (9)。所以

\[
\boxed{
H\cap K\ne\varnothing
\quad
(H\in\mathcal F_3,
K\in\mathcal F_1\cup\mathcal F_2\cup\mathcal F_3).}
\tag{10}
\]

这一步重新生成了所有由给定位置值诱导出的商零和短块，而非只检查
一份命名块清单。

最后重建不同 \(F_3\) 块的非零商交。取
\(H\ne H'\in\mathcal F_3\)，由 (10) 其交集 \(I\) 非空。若
\(\bar\sigma(I)=0\)，则因 \(|I|\le8\)，短商零和接口给
\(\sigma(I)=\mu a\)、\(\mu\in\{1,2,3\}\)。当 \(\mu=1,2\) 时，
\(H\cup H'\) 分别和为 \(5a,4a\)，补入 \(p-5,p-4\) 个锚点会
产生禁用短零和；当 \(\mu=3\) 时，\(H\setminus I\) 是非空实际
零和，除非 \(I=H\)，而后一情形又使同和块严格包含并产生非空
零和差集。故

\[
\boxed{\bar\sigma(H\cap H')\ne0.}
\tag{11}
\]

## 3. 尾迹盈余恒等式

对 \(H\in\mathcal H_0\)，记

\[
\varepsilon_H=(-1)^{|H|-1},\qquad
k_H=|H\cap U|.
\tag{12}
\]

由唯一尾位置级 Hasse 式，

\[
\sum_{H\in\mathcal H_0}\varepsilon_H=-\frac1{5b},
\qquad
\sum_{\substack{H\in\mathcal H_0\\u\in H}}
\varepsilon_H=-\frac{b+4}{20b}\qquad(u\in U).
\tag{13}
\]

式 (10)--(11) 应用于任一正核心块
\(V\mathbin{\dot\cup}U\)，又给

\[
k_H\ge1,\qquad
\bar\sigma(H\cap U)\ne0.
\tag{14}
\]

把 (13) 的逐点式在 \(u\in U\) 上相加，再减零阶式，得到

\[
\boxed{
\sum_{H\in\mathcal H_0}(k_H-1)\varepsilon_H
=\frac{4-r(b+4)}{20b}\qquad\text{于 }\mathbb F_p.}
\tag{15}
\]

令普通非负整数

\[
W=\sum_{H\in\mathcal H_0}(k_H-1).
\tag{16}
\]

(15) 左端的整数绝对值不超过 \(W\)，而它模 \(p\) 属于 (3) 中的
剩余类，故

\[
\boxed{W\ge\nu(p,r,b).}
\tag{17}
\]

这是旧下界所丢弃的真实尾迹盈余。

## 4. 加权容量双计数

由逐个尾外位置的 Hasse 式，每个
\(y\in Y\setminus U\) 至少属于 \(\mu_p\) 个实际零核心块。因此
普通尾外入射总数 \(J\) 满足

\[
J\ge(2p+8-r)\mu_p.
\tag{18}
\]

另一方面，\(|H|\le8\)，所以逐块有

\[
|H\setminus U|\le8-k_H=7-(k_H-1).
\]

求和并使用 (17)，

\[
J\le7|\mathcal H_0|-W
\le7|\mathcal H_0|-\nu(p,r,b).
\tag{19}
\]

(18)--(19) 给出 (4) 的第一项。第二项仍来自：每个尾点至少被
\(\mu_p\) 个块避开，而每块因 (14) 至多避开 \(r-1\) 个尾点。
所以 (4) 是普通实际块数结论，不是有限域权重的非负解释。

对 13 个幸存型逐项计算如下。旧列是只使用七个尾外位置容量的下界，
新列是 (4)。

\[
\begin{array}{c|c|c|c|c|c}
p&\ell&b&r&\nu&L_{\rm old}\to L^+\\ \hline
11&7&2&5&1&18\to18\\
13&6&3&3&6&9\to10\\
13&8&3&5&1&9\to9\\
19&6&1&5&2&6\to7\\
19&8&1&7&7&6\to7\\
23&6&3&3&7&59\to60\\
23&8&3&5&6&56\to57\\
43&7&3&4&9&193\to195\\
101&6&2&4&50&148\to155\\
101&8&2&6&21&146\to149\\
233&7&4&3&58&2355\to2364\\
701&8&4&4&245&7030\to7065\\
1399&8&5&3&322&28030\to28076
\end{array}
\tag{20}
\]

## 5. \(b\ge4\) 的迹层与尾外非零商交

当 \(b\ge4\) 时，逐块锚点原子论证给

\[
1\le k_H\le r-1.
\tag{21}
\]

若 \(r=2\)，则 (21) 迫使 \(W=0\)，而 (15) 的剩余是
\(-(b+2)/(10b)\ne0\)，重新得到三个二点尾型的矛盾。

若 \(r\ge3\)，令 \(N_{\ge2}\) 为 \(k_H\ge2\) 的块数。每个这类
块对 (15) 的整数绝对值至多 \(r-2\)，故

\[
\boxed{
N_{\ge2}\ge
\left\lceil\frac{\nu(p,r,b)}{r-2}\right\rceil.}
\tag{22}
\]

这给 (5) 中 \((701,8,4)\) 的 \(123\) 个多点迹块。

在另外两个 \(r=3\) 型中，(21) 使 \(k_H\in\{1,2\}\)。令
\(S_i\) 是尾迹大小为 \(i\) 的块的带符号总和，则 (13)、(15) 精确
给出

\[
S_2=-\frac{3b+8}{20b},\qquad
S_1=\frac{3b+4}{20b}.
\tag{23}
\]

因此

\[
\begin{array}{c|c|c}
(p,b)&\#\{k_H=1\}&\#\{k_H=2\}\\ \hline
(233,4)&\ge\|1/5\|_{233}=93&\ge\|-1/4\|_{233}=58\\
(1399,5)&\ge\|19/100\|_{1399}=266&\ge\|-23/100\|_{1399}=322.
\end{array}
\tag{24}
\]

最后固定任一迹一块 \(H\)，写 \(H\cap U=\{u\}\)。由 (13) 的
避开式，至少有 \(\mu_p\) 个实际零核心块 \(H'\) 避开 \(u\)。由
(14)，\(H'\cap U\ne\varnothing\)，所以两块的尾迹不交。式 (11)
进一步给

\[
\varnothing\ne H\cap H'\subseteq Y\setminus U,\qquad
\bar\sigma(H\cap H')\ne0.
\tag{25}
\]

按有序对计数至少为 \(\#\{k_H=1\}\mu_p\)；一个无序块对最多由
两个方向计入。因此不同无序块对至少有

\[
\left\lceil
\frac{\#\{k_H=1\}\mu_p}{2}
\right\rceil.
\tag{26}
\]

代入 (24) 与 \(\mu_{233}=35,\mu_{1399}=70\)，分别得到
\(1628\) 与 \(9310\)，证明 (5) 的交结构列。

## 6. 停止线

- **PROVED：**完整诱导 \(F_1/F_2/F_3\) 短谱、每个实际 \(F_3\)
  补集的商原子性及不同 \(F_3\) 块的非零商交已在本文重建。
- **PROVED：**迹盈余恒等式 (15)、普通提升 (17) 与加强下界 (4)；
  13 个幸存型中 11 个下界严格提高。
- **PROVED：**三个 \(b\ge4\) 幸存型的多点迹下界；两个三点尾型
  还有 (24)--(26) 的大量尾外非零商交块对。
- **INCOMPLETE：**这些下界和交结构尚未排除新的幸存型。未构造
  统一商标号、完整补原子内部子和系统或冻结反例。

有限脚本只重建异常类型并复核有限域分式、最小剩余和表 (20)、
(24)--(26)；它不替代第 2--5 节的全称证明。
