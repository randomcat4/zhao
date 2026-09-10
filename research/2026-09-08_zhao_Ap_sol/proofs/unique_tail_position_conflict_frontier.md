# 唯一尾的位置冲突前沿：轴单点、标签容量与尾迹不交边

STATUS: PROVED_REDUCTION / NO_TYPE_CLOSED / GLOBAL_INCOMPLETE

## 1. 范围与三态裁决

设 \(p\ge 11\) 为素数，处于冻结的 \(p-4\) 单高度纤维唯一尾分支：

\[
X=x^{p-4}\subset Z,\qquad Y=Z\setminus X,\qquad
\bar x=q\ne0,\qquad |Y|=2p+8.
\tag{1}
\]

唯一正核心 \(F_3\) 尾为 \(U\subset Y\)，类型记为

\[
(p,\ell,b,r),\qquad r=|U|=\ell-b,\qquad
\bar\sigma(U)=-bq,\qquad \sigma(U)=3a-bx.
\tag{2}
\]

本文只讨论此前留下的十三型：

\[
\begin{split}
&(11,7,2,5),\\
&(13,6,3,3),(13,8,3,5),\\
&(19,6,1,5),(19,8,1,7),\\
&(23,6,3,3),(23,8,3,5),\\
&(43,7,3,4),\\
&(101,6,2,4),(101,8,2,6),\\
&(233,7,4,3),(701,8,4,4),(1399,8,5,3).
\end{split}
\tag{3}
\]

记 \(\mathcal H_0\) 为全部零核心 \(F_3\) 块，并令

\[
\rho:C_p^3\longrightarrow C_p^3/\langle q\rangle\cong C_p^2.
\tag{4}
\]

本轮不再加入聚合 Hasse 方程。它把统一商标签、全部自动短块、
每个 \(F_3\) 长补的内部轴向子和及真实位置相交性联立，得到：

1. \(U\) 中轴向单点被压到一个唯一例外：仅当 \(\ell=6\) 时，
   仍可能有 \(\bar u=2q\)；当 \(\ell=7,8\) 时完全没有轴向单点。
2. \(Y\) 中标号恰为 \(q\) 的位置，在 \(b\ne4\) 的十一型中不存在；
   在 \(b=4\) 的两型中至多三个，且全部是每个零核心块的公共点。
3. 两个零核心块若尾迹不交，则其尾外交集不只商和非零，事实上
   其 \(C_p^2\) 投影和也非零。已有的 \(1628,9310\) 条块对因此
   全部成为真正的非轴向交边。
4. 每条这样的边都含一个非轴向标号的尾外位置；在两个大边数型中，
   至少存在一个具体尾外非轴向位置，同时落入至少四条此类边的交集。
5. \(p=233,1399\) 的全部非空真尾迹都非轴向；\(p=701\) 的
   \(123\) 个多点迹块则满足一个精确二分支。

这些是原问题的严格必要条件，但没有排除十三型中的任何一型。
三态裁决为

\[
\boxed{\mathsf{PROVED\_REDUCTION}/\mathsf{NO\_TYPE\_CLOSED}/
\mathsf{GLOBAL\_INCOMPLETE}.}
\tag{5}
\]

## 2. 已冻结的输入

只使用下列已证接口。

- 短商零和谱：长度至多八的商零位置块自动属于相应的
  \(F_1,F_2,F_3\)；不存在长度 \(9,\ldots,2p+2\) 的商零位置子集。
- 每个零核心 \(F_3\) 块命中 \(U\)，任意两个 \(F_3\) 块相交，
  任意 \(F_3\) 块与任意自动诱导短块相交，且 \(F_3\) 公共核心为空。
- 正核心 \(F_3\) 实际尾唯一：一切正核心 \(F_3\) 块的尾都是 \(U\)。
- 对每个 \(T\in\mathcal F_3\)，商补原子 \(B_T=Z\setminus T\)
  中任一商值的重数满足
  \[
  v_s(B_T)\le p-4.                                      \tag{6}
  \]
  这是 route_a_atom_line_rigidity.md 的 (32v)，不是本轮的新假设。
- 对 \(u\in U\) 与 \(y\in Y\setminus U\)，此前的实际带符号点度给出
  \[
  \sum_{H\in\mathcal H_0:u\notin H}\varepsilon_H={1\over20},
  \qquad
  \sum_{H\in\mathcal H_0:y\notin H}\varepsilon_H={b-4\over20b}.
  \tag{7}
  \]
  特别地，每个 \(u\in U\) 被某个实际 \(H\in\mathcal H_0\) 避开；
  当 \(b\ne4\) 时，每个 \(y\in Y\setminus U\) 也被某个实际块避开。
- 对不同 \(H,H'\in\mathcal H_0\)，令 \(I=H\cap H'\)。若
  \(\bar\sigma(I)\in\langle q\rangle\)，则
  \[
  \bar\sigma(I)\in\{-q,-2q,-3q\},\qquad
  |I|+t\le8\quad(\bar\sigma(I)=-tq).
  \tag{8}
  \]

十三型逐一满足

\[
b+3\le p-4.                                               \tag{9}
\]

## 3. 轴向单点完全分类

**引理 1（轴单点）。** 对任意十三型及任意 \(u\in U\)，

\[
\rho(\bar u)=0
\Longrightarrow
\begin{cases}
\bar u=2q,&\ell=6,\\
\bot,&\ell=7\text{ 或 }8.
\end{cases}
\tag{10}
\]

**证明。** 写 \(\bar u=\alpha q\)，并取唯一
\(c\in\{0,1,\ldots,p-1\}\) 使 \(c\equiv-\alpha\pmod p\)。

若 \(c=0\)，则单点 \(u\) 已是商零和，违反短谱。若 \(1\le c\le6\)，

\[
K=X_c\mathbin{\dot\cup}\{u\}                             \tag{11}
\]

是长度 \(2,\ldots,7\) 的自动短块。由 \(F_3\) 公共核心为空，存在
某个 \(F_3\) 块避开 \(u\)；正核心块都含 \(U\)，故这个块属于
\(\mathcal H_0\)。它同时避开 \(X\)，于是与 (11) 不交，矛盾。
若 \(c=7\)，(11) 是另一个长度八正核心 \(F_3\) 尾，违反唯一尾。
若 \(8\le c\le p-4\)，(11) 的长度处于
\(9,\ldots,p-3\subset[9,2p+2]\)，也矛盾。因此只剩

\[
c\in\{p-3,p-2,p-1\},\qquad \alpha\in\{3,2,1\}.           \tag{12}
\]

现在考察 \(U\setminus\{u\}\)。它的商和是
\(-(b+\alpha)q\)，可从 \(X\) 取 \(b+\alpha\) 个位置；(9) 保证
核心可取。所得商零块长度为

\[
|U|-1+b+\alpha=\ell-1+\alpha.                             \tag{13}
\]

- 若 \(\ell=6\)，则 \(\alpha=3\) 令 (13) 等于八，产生第二个
  正核心 \(F_3\) 尾；先只剩 \(\alpha=1,2\)。
- 若 \(\ell=7\)，则 \(\alpha=2\) 产生第二个长度八尾，
  \(\alpha=3\) 产生禁用长度九；先只剩 \(\alpha=1\)。
- 若 \(\ell=8\)，三个值分别产生长度八、九、十，全部矛盾。

最后排除 \(\alpha=1\)。若 \(\bar u=q\)，取一个避开 \(u\) 的
\(H\in\mathcal H_0\)。补原子 \(B_H=Z\setminus H\) 含有
\(X=x^{p-4}\) 的 \(p-4\) 个 \(q\)-位置以及 \(u\) 这个额外
\(q\)-位置，故 \(v_q(B_H)\ge p-3\)，与 (6) 矛盾。于是
\(\ell=6\) 只剩 \(\alpha=2\)，而 \(\ell=7\) 也无剩余。证毕。

若 \(\ell=6\) 且 \(\bar u=2q\)，(13) 是长度七的自动短块；
唯一尾排除了 \(F_3\) 身份，所以它实际属于 \(F_2\)。特别地，

\[
U\setminus\{u\}\text{ 命中每个 }H\in\mathcal H_0.       \tag{14}
\]

此外，四个 \(\ell=6\) 型都不满足
\(2r\equiv-b\pmod p\)。因此 \(U\) 不可能全部由 \(2q\)-位置组成；
若有 \(r-1\) 个轴向点，则总投影和为零又迫使最后一点轴向，仍矛盾。
故其轴向位置数至多 \(r-2\)。其余九型的轴向位置数为零。

## 4. 商标签 \(q\) 的位置容量

**引理 2（\(q\)-标签公共核与三点容量）。** 令

\[
W_q=\{y\in Y:\bar y=q\}.
\tag{15}
\]

则

\[
\boxed{
b\ne4\Longrightarrow W_q=\varnothing;\qquad
b=4\Longrightarrow W_q\subseteq Y\setminus U,\quad
|W_q|\le3,\quad W_q\subseteq\bigcap_{H\in\mathcal H_0}H.}
\tag{16}
\]

**证明。** 若 \(y\in Y\) 标号为 \(q\)，任何避开 \(y\) 的
\(H\in\mathcal H_0\) 都使 \(B_H\) 含至少 \(p-3\) 个 \(q\)-位置，
与 (6) 矛盾。因此每个 \(q\)-位置属于全部零核心块。

式 (7) 的第一式说明 \(U\) 中每一点都可被某个零核心块避开，故
\(W_q\cap U=\varnothing\)。当 \(b\ne4\) 时，(7) 的第二式说明
\(Y\setminus U\) 中每一点也可被某个零核心块避开，所以 \(W_q\) 为空。

只剩 \(b=4\)。若 \(w=|W_q|\ge4\)，则 \(W_q\) 已属于每个长度至多八
的零核心块，故 \(4\le w\le8\)。从 \(X\) 取 \(p-w\le p-4\) 个位置，

\[
X_{p-w}\mathbin{\dot\cup}W_q                             \tag{17}
\]

是长度 \(p\) 的商零位置子集。这落在禁用区间 \([9,2p+2]\)，矛盾。
因此 \(w\le3\)。证毕。

所以十三型中恰有十一型完全不允许 \(Y\) 上出现 \(q\)-标签；
只有 \((233,7,4,3)\) 与 \((701,8,4,4)\) 允许一个至三个这样的
公共位置。

## 5. 尾迹不交边必为非轴向交边

**引理 3（外部交投影）。** 对任意十三型，若
\(H,H'\in\mathcal H_0\) 且

\[
(H\cap U)\cap(H'\cap U)=\varnothing,                     \tag{18}
\]

则令 \(I=H\cap H'\)，有

\[
\varnothing\ne I\subseteq Y\setminus U,\qquad
\boxed{\rho(\bar\sigma(I))\ne0}.                         \tag{19}
\]

**证明。** 非空性来自 \(F_3\)-\(F_3\) 相交，(18) 给出
\(I\subseteq Y\setminus U\)。反设 \(I\) 轴向。由 (8)，存在
\(t\in\{1,2,3\}\) 使

\[
\bar\sigma(I)=-tq,\qquad K=I\mathbin{\dot\cup}X_t,\qquad |K|\le8.
\tag{20}
\]

若 \(|K|=8\)，短谱迫使 \(K\) 是 \(F_3\)；它的正核心尾 \(I\ne U\)，
直接违反唯一尾。若 \(|K|\le7\)，(9) 允许在 \(X\setminus X_t\)
中再取一个 \(b\)-核心 \(X_b'\)。正核心块

\[
X_b'\mathbin{\dot\cup}U                                  \tag{21}
\]

与 \(K\) 不交：两核心不交，且 \(I\subseteq Y\setminus U\)。这违反
每个 \(F_3\) 块与每个自动短块相交。故反设不成立。证毕。

因此 unique_tail_next_trace_excess.md 中已有的真实块对下界加强为

\[
\begin{array}{c|c}
(p,\ell,b,r)&
\#\{\{H,H'\}:\text{尾迹不交且 }\rho(\bar\sigma(H\cap H'))\ne0\}\\ \hline
(233,7,4,3)&\ge1628\\
(1399,8,5,3)&\ge9310.
\end{array}
\tag{22}
\]

这些共 \(1628+9310=10938\) 条边是实际块交图的边。每条边的交集
大小至多七，且其投影和非零，所以交集中至少有一个满足
\(\rho(\bar y)\ne0\) 的尾外位置。对每条边任选一个这样的见证位置，
鸽巢原理给出精确的有标签拥塞分母：

\[
\left\lceil{1628\over |Y\setminus U|}\right\rceil
=\left\lceil{1628\over471}\right\rceil=4,\qquad
\left\lceil{9310\over2803}\right\rceil=4.                 \tag{23}
\]

故在 \(p=233\) 与 \(p=1399\) 两型中，各存在一个具体
\(y\in Y\setminus U\)，满足 \(\rho(\bar y)\ne0\)，并且至少四个
尾迹不交块对 \(\{H,H'\}\) 同时满足 \(y\in H\cap H'\) 和 (19)。
这是带真实商标签的四边位置拥塞，不是无标签的普通相交族容量界。

更精确地，任选其中四条不同边，记交集为 \(I_1,\ldots,I_4\)，并令
\[
S=I_1\cup\cdots\cup I_4.
\]
每个端点块至少含一个尾位置，故 \(|I_i|\le7\)。四个交集共享 \(y\)，
从而
\[
|S|\le1+4(7-1)=25.
\]
这给出一个至多二十五个尾外位置、至多八个端点块的必要标号 CSP
分片。它同时承担四条真实约束
\[
y\in I_i,\qquad \rho(\bar y)\ne0,\qquad
\rho(\bar\sigma(I_i))\ne0\quad(1\le i\le4),
\]
并且对每个出现的端点块 \(A\)，仍必须保留完整长补内部条件
\[
\varnothing\ne E\subsetneq Y\setminus A,\quad
\bar\sigma(E)\in\langle q\rangle
\Longrightarrow
\bar\sigma(E)\in\{q,2q,3q\}.
\]
所以该二十五位置分片直接连接统一标号与最多八个长补原子，不是把
四条边孤立成抽象图。本文没有证明这四个非轴向交和值彼此不相容；
它们与上述长补内部条件是下一次严格局部求解必须同时保留的约束。

## 6. 轴向尾切割与三个大素数型

**引理 4（轴向尾切割）。** 设
\(\varnothing\ne C\subsetneq U\)，且
\(\bar\sigma(C)=-tq\)，其中 \(0\le t\le p-4\)。令
\(L=|C|+t\)。则：

\[
\begin{array}{c|l}
L=1&\text{不可能；}\\
2\le L\le7&C\text{ 命中每个 }H\in\mathcal H_0;\\
L=8,\ t=0&C\text{ 是零核心 }F_3\text{，仍命中每个 }H\in\mathcal H_0;\\
L=8,\ t>0&\text{不可能；}\\
9\le L\le2p+2&\text{不可能。}
\end{array}
\tag{24}
\]

**证明。** \(X_t\mathbin{\dot\cup}C\) 是统一标签自动诱导的商零位置块。
\(L=1\) 是商零单点；\(2\le L\le7\) 时它是短块，而零核心块避开
\(X\)，故短块相交性迫使它命中 \(C\)；\(L=8,t=0\) 用
\(F_3\)-\(F_3\) 相交；\(L=8,t>0\) 产生不同于 \(U\) 的正核心
\(F_3\) 尾；最后一行就是商零中间长度禁区。证毕。

### 6.1 \((233,7,4,3)\)

引理 1 说明 \(U\) 无轴向单点。又
\(\rho(\bar\sigma(U))=0\) 且 \(|U|=3\)：若二点真子迹轴向，
它的补单点也轴向；故每个非空真 \(C\subset U\) 都满足

\[
\rho(\bar\sigma(C))\ne0.                                 \tag{25}
\]

因此此前至少 \(58\) 个二点迹块的真实尾迹全部非轴向；至少
\(93\) 个单点迹块的真实尾迹也全部非轴向。再结合 (16)、(22)，
此型的严格必要条件是

\[
\begin{gathered}
|W_q|\le3,\quad W_q\subseteq\bigcap\mathcal H_0,\\
\#\{H:|H\cap U|=2,\ \rho(\bar\sigma(H\cap U))\ne0\}\ge58,\\
\#\{H:|H\cap U|=1,\ \rho(\bar\sigma(H\cap U))\ne0\}\ge93,\\
\#\{\{H,H'\}:\text{满足 (18)--(19)}\}\ge1628.
\end{gathered}
\tag{26}
\]

### 6.2 \((701,8,4,4)\)

引理 1 同样排除全部轴向单点。此前至少 \(123\) 个块满足
\(|H\cap U|\ge2\)。对其中每个块，令 \(J=H\cap U\)：

- 若 \(|J|=3\)，则 \(J\) 轴向会迫使补单点 \(U\setminus J\) 轴向，
  所以 \(J\) 非轴向；
- 若 \(|J|=2\)，则严格逐迹表只允许
  \(\bar\sigma(J)=-(4+1)q=-5q\)。在这个轴向分支中，
  \(|J|+5=7\)，故引理 4 迫使 \(J\) 命中每个零核心块。

所以这 \(123\) 个块逐个满足精确二分支

\[
\boxed{
\rho(\bar\sigma(J))\ne0
\quad\text{或}\quad
\bigl(|J|=2,\ \bar\sigma(J)=-5q,\
J\cap H'\ne\varnothing\ \forall H'\in\mathcal H_0\bigr).}
\tag{27}
\]

同时仍有 \(|W_q|\le3\) 且 \(W_q\subseteq\bigcap\mathcal H_0\)。
式 (27) 不能被读成“至少 \(123\) 个非轴向迹”；同一个轴向二点
横截可能被多个块共同使用。

### 6.3 \((1399,8,5,3)\)

与 (25) 同理，每个非空真尾迹都非轴向。并且这里 \(b\ne4\)，
故 \(W_q=\varnothing\)。已有盈余因此严格化为

\[
\begin{gathered}
\#\{H:|H\cap U|=2,\ \rho(\bar\sigma(H\cap U))\ne0\}\ge322,\\
\#\{H:|H\cap U|=1,\ \rho(\bar\sigma(H\cap U))\ne0\}\ge266,\\
\#\{\{H,H'\}:\text{满足 (18)--(19)}\}\ge9310.
\end{gathered}
\tag{28}
\]

因此 \(58+123+322=503\) 个多点迹块都已获得逐块二分支或非轴向
约束，而 \(10938\) 个尾迹不交块对都已获得逐边非轴向交约束。

## 7. 单点迹块的等和花瓣碰撞

记

\[
\mu_p=\|20^{-1}\|_p.
\tag{29}
\]

固定一个单点迹块 \(H\in\mathcal H_0\)，令
\(H\cap U=\{u\}\)，并写 \(O=H\setminus U\)。由 (7)，至少有
\(\mu_p\) 个实际块 \(H'\in\mathcal H_0\) 避开 \(u\)。每个这样的
\(H'\) 与 \(H\) 尾迹不交，引理 3 给

\[
\varnothing\ne H\cap H'\subseteq O,\qquad
\rho(\bar\sigma(H\cap H'))\ne0.                           \tag{30}
\]

若

\[
\mu_p>2^{|O|}-1=2^{|H|-1}-1,                              \tag{31}
\]

则鸽巢原理给出两个不同块 \(H'_1,H'_2\)，使
\(H\cap H'_1=H\cap H'_2=:I\)。令 \(D_i=H'_i\setminus H\)。
同和性给

\[
\sigma(D_1)=\sigma(D_2)=3a-\sigma(I),\qquad
\bar\sigma(D_1)=\bar\sigma(D_2).                         \tag{32}
\]

两个花瓣非空、不同且不可比较；否则严格包含之差会给出 \(Z\) 的
非空实际零和真子集。这里

\[
\mu_{233}=35,\qquad \mu_{1399}=70.                        \tag{33}
\]

所以若不出现 (32) 的等和花瓣菱形，则：

- \(p=233\) 的每个单点迹块长度只能是七或八；
- \(p=1399\) 的每个单点迹块长度只能是八。

结合已有单点迹下界，可写成精确分支：前者的至少 \(93\) 个块要么
全长七/八，要么出现 (32)；后者的至少 \(266\) 个块要么全长八，
要么出现 (32)。这仍是必要 CSP 分支，不是矛盾。

## 8. 有限证书、量词边界与停止线

配套脚本 unique_tail_position_conflict_frontier.py 独立重算：

- 十三型及每型的轴向单点候选、轴向位置上界和 \(q\)-标签容量；
- 十一型 \(W_q=\varnothing\)、两型 \(|W_q|\le3\)；
- \(58,123,322,1628,9310\) 的接入记录及总数 \(503,10938\)；
- 有标签外位置拥塞的分母 \(471,2803\) 与下界四；
- \(\mu_{233}=35,\mu_{1399}=70\) 与 (31) 的长度阈值；
- 按规范 JSON 排序后的 SHA-256，防止有限表静默漂移。

固定哈希为

\[
\begin{aligned}
\text{type-table SHA-256}
&=\mathtt{d10bcffce8e708eda4165b329d2dc9ba94852db32535acc035141a1a11da3b37},\\
\text{certificate SHA-256}
&=\mathtt{5d4f96f4f03be57ac0cba9c6dd170955a300eba15e833567e72ebcaa9f1da6f3}.
\end{aligned}
\tag{34}
\]

验证命令为

    python research/2026-09-08_zhao_Ap_sol/unique_tail_position_conflict_frontier.py

所有结论的量词都是“对每个满足冻结接口的真实唯一尾反例、对其中
每个被点名的实际块或块对”。脚本只核对有限算术与证书哈希；
它不替代冻结接口的证明，也不枚举完整标号实例。

精确停止线如下：本轮没有证明任何十三型不可行。尤其，(16) 的
公共 \(q\)-位置、(27) 的二点横截、(23) 的四边拥塞和 (32) 的
等和花瓣都可能作为必要结构幸存；幸存结构不是原题反例。下一步
若要关闭类型，仍须把每个实际位置的 \(C_p^2\) 标签、全部诱导短块
以及每个长补原子的所有内部子集和同时送入严格统一标签核验器，
不能把本文的局部约束单独升级为全局 UNSAT。
