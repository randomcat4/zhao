# 非空共同核强制出的互补短 packing 块

STATUS: **PROVED_SHORT_PACKING_BOUND /
P1399_THREE_SINGLETON_PACKING_CLOSED / GLOBAL_INCOMPLETE**

## 1. 冻结范围与输入

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

沿用实际位置不交分解

\[
X=x^{p-4},\qquad Z=X\mathbin{\dot\cup}Y,
\qquad |Z|=3p+4,\qquad |Y|=2p+8,
\tag{3}
\]

\[
Y=L\mathbin{\dot\cup}R,qquad
R=P_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}P_t
\mathbin{\dot\cup}K.
\tag{4}
\]

这里每个 \(P_i\) 是 \(C_p^2\) 中按实际位置计数的非空投影零和原子，
\(K\) 是投影零和自由核。前一条已独立认证的结果给出

\[
K\ne\varnothing.
\tag{5}
\]

三个强制型的轴系数总和都为三。记相应系数为 \(d_i\)，则

\[
\bar\sigma(P_i)=d_iq,\qquad
\sum_{i=1}^t d_i=3,
\qquad
\bar\sigma(P_1\dot\cup\cdots\dot\cup P_t)=3q.
\tag{6}
\]

共同核总和接口在 \(d=3\) 时为

\[
\bar\sigma(K)=q-\bar\sigma(L),
\qquad
\boxed{\bar\sigma(K\dot\cup L)=q.}
\tag{7}
\]

唯一尾满足

\[
U\subseteq L,\qquad |U|=3,
\qquad \bar\sigma(U)=-bq.
\tag{8}
\]

还沿用 \(6\le|L|\le52\)、\(q\ne0\)、商零禁窗
\([9,2p+2]\)，以及长度八的正核心 \(F_3\) 块只能是核心—尾对
\((b,U)\)。本文不输入任何实际高度，也不假定某个尺寸向量可实现。
这里的 \(Z\) 仍是 `assumptions.md` 中全局余序列的实际子序列，故冻结
(SQ) 可用于 \(Z\) 的短子块；式 (4) 的 \(R\) 只是 \(Y\) 内的共同外部
位置集，不改变 (SQ) 的定义域。

## 2. 两个互补商零实际块

从 \(X\) 中先取 \(b-3\) 个实际位置，记作 \(X_D\)，并令

\[
X_B:=X\setminus X_D.
\tag{9}
\]

两个参数下 \(b-3\in\{1,2\}\)，而

\[
|X_B|=(p-4)-(b-3)=p-b-1.
\tag{10}
\]

定义

\[
D:=X_D\mathbin{\dot\cup}U
\mathbin{\dot\cup}P_1\mathbin{\dot\cup}\cdots
\mathbin{\dot\cup}P_t,
\tag{11}
\]

\[
B:=X_B\mathbin{\dot\cup}K
\mathbin{\dot\cup}(L\setminus U).
\tag{12}
\]

这些是不交实际位置并，而非形式线性组合：\(X\cap Y=\varnothing\)、
\(U\subseteq L\)、\(K,P_i\subseteq R=Y\setminus L\)，且 (4) 中各项
两两位置不交。式 (3)--(4) 与 (9) 逐项给出

\[
\boxed{Z=D\mathbin{\dot\cup}B.}
\tag{13}
\]

由 (6) 与 (8)，

\[
\bar\sigma(D)
=(b-3)q-bq+3q=0.
\tag{14}
\]

由 (7)--(8) 与 (10)，

\[
\begin{aligned}
\bar\sigma(B)
&=(p-b-1)q+\bar\sigma(K)+\bar\sigma(L)-\bar\sigma(U)\\
&=(p-b-1)q+q+bq=pq=0.
\end{aligned}
\tag{15}
\]

因此 (11)--(12) 是一对互补商零实际块。特别地，这里没有把
\(K\dot\cup L\) 的商和误写成零，也没有漏掉从 \(L\) 中删除 \(U\)
所带来的 \(+bq\)。

## 3. 长补块迫使 \(D\) 落入短谱

由 (5)、\(|L|\ge6\) 与 (12)，

\[
|B|
=(p-b-1)+|K|+(|L|-3)
\ge p-b+3.
\tag{16}
\]

右端在两个参数下分别为 232 与 1397，所以总有 \(|B|>8\)。商零禁窗
说明任何非空商零 \(Z\)-子块的长度只能至多八，或至少 \(2p+3\)。
故 (15)--(16) 给

\[
|B|\ge2p+3.
\tag{17}
\]

再由 (13) 与 \(|Z|=3p+4\)，

\[
|D|=3p+4-|B|\le p+1.
\tag{18}
\]

若 \(|D|\ge9\)，则 (14) 与 (18) 会使 \(D\) 落入短段禁窗
\([9,p+1]\)，矛盾。因此

\[
|D|\le8.
\tag{19}
\]

式 (19) 使冻结 (SQ) 可以用于 \(D\)，从而其实际和属于
\(\{a,2a,3a\}\)，并落入三族短块长度窗

\[
I_1=[2,6],\qquad I_2=[4,7],\qquad I_3=[6,8].
\tag{20}
\]

若 \(|D|=8\)，前两族由 (20) 排除，所以 \(D\in\mathcal F_3\)。
但 \(D\) 使用正数 \(b-3\) 个 \(X\)-位置，其尾为

\[
U\mathbin{\dot\cup}P_1\mathbin{\dot\cup}\cdots
\mathbin{\dot\cup}P_t.
\]

这既有核心数 \(b-3\ne b\)，又因 \(t\ge1\) 及每个 \(P_i\ne\varnothing\)
而有不同于 \(U\) 的尾，违反正核心长度八块的唯一性。故精确得到

\[
\boxed{|D|\le7.}
\tag{21}
\]

实际高度只在 (SQ) 之后被动产生；论证没有预先指定 \(D\) 属于哪个
短块族。进一步说，当前 \(D\) 不可能属于 \(F_3\)，所以长度五、六时
实际系数只能在 \(\{1,2\}\) 中，长度七时必须为二。

## 4. 三种 packing 的精确尺寸后果

记

\[
n_i:=|P_i|\ge1,\qquad N:=\sum_i n_i.
\tag{22}
\]

由 \(|U|=3\) 和 (11)，

\[
|D|=(b-3)+3+N=b+N.
\tag{23}
\]

结合 (21)，得到统一的短 packing 界

\[
\boxed{N\le7-b.}
\tag{24}
\]

逐型枚举所有正整数尺寸向量如下；相同轴系数的原子只按尺寸非降序记录，
不同轴系数则保留其顺序。

\[
\begin{array}{c|c|c|c|c}
(p,b)&\text{packing 型}&(n_i)\text{ 幸存向量}&|D|&
\sigma(D)/a\text{ 的必要值}\\
\hline
(233,4)&(3)&(1),(2),(3)&5,6,7&\{1,2\},\{1,2\},\{2\}\\
&(1,2)&(1,1),(1,2),(2,1)&6,7,7&\{1,2\},\{2\},\{2\}\\
&(1,1,1)&(1,1,1)&7&\{2\}\\
\hline
(1399,5)&(3)&(1),(2)&6,7&\{1,2\},\{2\}\\
&(1,2)&(1,1)&7&\{2\}\\
&(1,1,1)&\varnothing&-&-
\end{array}
\tag{25}
\]

于是得到两个精确结论：

1. 当 \((p,b)=(1399,5)\) 时，(24) 给 \(N\le2\)，而
   \((1,1,1)\) 型含三个非空原子，必有 \(N\ge3\)。因此
   \[
   \boxed{p=1399\text{ 的 }(1,1,1)\text{ packing 型为空}.}
   \tag{26}
   \]
2. 当 \((p,b)=(233,4)\) 时，(24) 给 \(N\le3\)。同型三个非空原子
   已给 \(N\ge3\)，故
   \[
   \boxed{|P_1|=|P_2|=|P_3|=1,\qquad |D|=7,\qquad
   \sigma(D)=2a.}
   \tag{27}
   \]
   这只强迫三个 \(C_p^2\) 投影原子都是单点，并没有证明该型为空。

同理，\(p=1399\) 的 \((1,2)\) 型强迫两个原子均为单点且 \(D\) 是
长度七的 \(F_2\) 块；这些是必要条件，不是可实现性声明。

## 5. 共同核的近极值下界

由 (3)--(4)，

\[
|K|=|Y|-|L|-N=2p+8-|L|-N.
\tag{28}
\]

把 \(|L|\le52\) 与 (24) 代入，所有尚未被 (26) 删除的强制型都满足

\[
\boxed{|K|\ge2p+8-52-(7-b)=2p+b-51.}
\tag{29}
\]

另一方面，\(K\) 在 \(C_p^2\) 投影中零和自由，所以 Davenport 上界给

\[
|K|\le2p-2.
\tag{30}
\]

数值上即

\[
\begin{array}{c|c|c}
(p,b)&|K|\text{ 的统一范围}&(2p-2)-|K|\text{ 的最大亏损}\\
\hline
(233,4)&419\le|K|\le464&45\\
(1399,5)&2752\le|K|\le2796&44.
\end{array}
\tag{31}
\]

对 (25) 中某个精确尺寸向量，还可用
\(|K|\ge2p-44-N\) 得到对应的逐行更强值；配套报告逐项保存了这些值。

## 6. 有限证书与停止线

`unique_tail_forced_short_packing_block.py` 不导入任何作者模块，只使用
Python 标准库。它完成：

1. 核对 (9)--(15) 的两个商和值与 \(X\)-位置数；
2. 遍历 \(1\le|D|<3p+4\)，在 \(|B|>8\) 及两侧禁窗下只留下
   \(|D|=1,\ldots,8\)，再由错误正核心长度八门留下
   \(|D|=1,\ldots,7\)；
3. 枚举 (2) 的全部正整数原子尺寸向量，恰得到 (25) 的十个幸存向量；
4. 对每个向量核对 \(D,B\) 的互补长度、短块族必要值、共同核上下界
   与 \(|L|\) 的可用整数范围。

报告 `unique_tail_forced_short_packing_block_report.json` 的规范证书为

\[
\mathtt{bc44e4961893a6c731cd18a4e35f8542ee21f0b8517f18b35a6760bfb3e1d39f}.
\tag{32}
\]

生成时工件 SHA-256 为

```text
d3e25042ff486ed0663d896601457a5fcc3930f3938f5d05364d769270411d27  unique_tail_forced_short_packing_block.py
5d8a3f1b434a4b85581afa5416b71b2e5120a81c35edd6c6a984b27d3e5173ad  unique_tail_forced_short_packing_block_report.json
edda3f792101e205332f860d7baeaebf0810e3642527c41ad84515264e3e7e64  proofs/unique_tail_forced_kernel_nonempty.md
1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942  proofs/unique_tail_common_R_next.md
60384c64dee88487220f3fd7101a5d3abff1cb576fe3a8b43ec398fdd284ddce  proofs/unique_tail_labelled_position_next.md
d886a84857cd430455558266a2ab175f21f2de853eed08c6affcad0c14b3efcc  proofs/middle_quotient_gap.md
0e10138860269a18f0f7c0a02ab40204109efbb9a09688fc99da46983e390aed  assumptions.md
```

**PROVED：**互补商零块 (11)--(12)、短 packing 界 (24)、
\(p=1399\) 的 \((1,1,1)\) 型删除、\(p=233\) 同型的三个单点结论，
以及共同核下界 (29)。

**NOT PROVED：**\(p=233\) 的 \((1,1,1)\) 型为空；任一 \((3)\) 或
\((1,2)\) 型为空；三个强制型全部为空；其余四个 packing 型为空；
唯一尾分支为空；或 \(A_p\) 成立。表 (25) 没有使用商标签 \(q\) 的
额外位置排除、实际高度 Hasse 系统或长补原子的进一步内部结构。

全局状态继续为 **INCOMPLETE**。
