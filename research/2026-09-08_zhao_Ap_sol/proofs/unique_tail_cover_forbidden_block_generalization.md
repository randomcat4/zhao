# 强制共同余部原子型的覆盖禁块推广：全单位形式与全部 incidence 幸存类

STATUS: **PROVED_GENERAL_FORBIDDEN_BLOCK_GATE /**
**EXACT_UNIT_FORM_CLASSIFICATION /**
**ALL_COVER_TRACE_SIZE_INCIDENCE_CLASSES_SURVIVE /**
**NO_PACKING_TYPE_CLOSED / GLOBAL_INCOMPLETE**

## 1. 冻结范围

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

沿用四边端点族 \(\mathcal A\)、

\[
L=U\cup\bigcup_{E\in\mathcal A}E,
\qquad R=Y\setminus L,
\qquad |U|=3,
\tag{3}
\]

以及强制型中的共同余部

\[
Q_E=K\mathbin{\dot\cup}(L\setminus E).
\tag{4}
\]

若存在轴向覆盖对 \(H,J\)，上游交换门已经给出

\[
K=\varnothing,\qquad L=H\cup J,\qquad
Q_E=L\setminus E\quad(E\in\mathcal A),
\tag{5}
\]

而且每个 \(Q_E\) 都是 \(C_p^2\) 中按实际位置计数的投影零和原子，
并共享统一标签

\[
\bar\sigma(Q_E)=q,\qquad \sigma(Q_E)=S.
\tag{6}
\]

唯一尾满足

\[
\bar\sigma(U)=-bq.
\tag{7}
\]

覆盖对的迹是两个不同双点迹，所以 \(H\cap J\) 至少含一个共同
\(U\)-位置和共同非轴位置 \(y\)。由 \(|H|,|J|\le8\)，

\[
\boxed{|L|=|H\cup J|\le14.}
\tag{8}
\]

本文只使用 (5)--(8)、实际位置 incidence、冻结短窗与中间禁区。
有限幸存对象没有配置商标签或实际高度，因而不是放宽反例。

## 2. 两个余部与唯一尾的全部单位系数形式

固定不同端点 \(E,F\)，记

\[
A=Q_E,\qquad B=Q_F,
\qquad O=L\setminus U.
\tag{9}
\]

考察全部 26 个非零单位形式

\[
\alpha A+\beta B+\gamma U,
\qquad \alpha,\beta,\gamma\in\{-1,0,1\}.
\tag{10}
\]

“形成实际子集”是指 (10) 在 \(L\) 的每个实际位置上的形式系数都
属于 \(\{0,1\}\)。逐个 Venn 单元检查后，除交换 \(A,B\) 外，
全部可能行如下。

\[
\begin{array}{c|c|c}
\text{形式}&\text{成为实际子集的充要条件}&q\text{ 轴系数}\\
\hline
A&\text{恒成立}&1\\
U&\text{恒成立}&-b\\
A+B&A\cap B=\varnothing&2\\
A-B&B\subseteq A&0\\
A+B-U&U\subseteq A\cup B,\ (A\cap B)\cap O=\varnothing&b+2\\
U-A&A\subseteq U&-(b+1)\\
U-A-B&A\cup B\subseteq U,\ A\cap B=\varnothing&-(b+2)\\
U+A-B&B\cap O\subseteq A\cap O,\ A\cap U\subseteq B\cap U&-b.
\end{array}
\tag{11}
\]

其余单位形式都在某个 \(U\)-位置产生负系数或至少二的系数。这里
使用了每个端点迹都是 \(U\) 的非空真子集。表中 \(A-B\) 一行在
强制原子接口内也不可能非空：若 \(B\subseteq A\)，两个投影原子
只能相等；或者直接用 (6) 得 \(\sigma(A\setminus B)=0\)，违反
\(Z\) 的实际原子性。

表 (11) 还是精确的集合分类，不是只列必要条件。配套程序在三点
\(U\) 和四个尾外测试位置上遍历全部迹、全部尾外 Venn 占用和 26
个形式，共核对 59,904 行；恰有表中的十二个有向形式出现过
0/1 incidence。

### 2.1 唯一的大 \(X\) 核单位形式

若 (10) 的轴系数为正数 \(t\)，要由 \(X=x^{p-4}\) 中的同标签位置
把它闭成商零块，只能取 \(p-t\) 个 \(X\)-位置；这要求 \(t\ge4\)。
表 (11) 及 \(U\)-位置系数立即给出：

\[
\boxed{
\text{全部单位二余部形式中，唯一可能使用大 }X\text{ 核的是 }
Q_E+Q_F-U.}
\tag{12}
\]

把 (11) 的条件改写成端点 incidence，得到精确判据

\[
\boxed{
Q_E+Q_F-U\text{ 是实际子集}
\iff
(E\cap U)\cap(F\cap U)=\varnothing
\ \text{且}\ O\subseteq E\cup F.}
\tag{13}
\]

第一项保证三个 \(U\)-位置的系数非负，第二项恰好删除尾外的双重
余部位置。若 (13) 成立，把该实际位置集记为 \(W_{EF}\)，并令
\(w=|W_{EF}|\)。由统一标签，

\[
\bar\sigma(W_{EF})=(b+2)q.
\tag{14}
\]

因 \(b+2<p\)，\(W_{EF}\) 非空。取

\[
c=p-b-2\le p-4
\tag{15}
\]

个实际 \(X\)-位置，便得到商零块，长度为

\[
n=p-b-2+w.
\tag{16}
\]

由 (8)，\(1\le w\le14\)。更精确地，

\[
\begin{cases}
w\le b+3&\Longrightarrow 9\le n\le p+1,\\
w\ge b+4&\Longrightarrow p+2\le n\le2p+2.
\end{cases}
\tag{17}
\]

两行分别落入短谱禁区和中间商零禁区。因此

\[
\boxed{\text{满足 (13) 的任意端点对都被精确排除。}}
\tag{18}
\]

十位置旧骨架的两条单点迹正是 (13) 的特例；证明并不依赖那十个
位置的坐标、端点数或具体 packing 形状。

## 3. 任意多个端点的稠密覆盖禁块

单位二余部形式还有一个对全部 incidence 骨架有用的推广。取
\(\mathcal S\subseteq\mathcal A\)，令 \(k=|\mathcal S|\)，并考察

\[
W_{\mathcal S,m}=\sum_{E\in\mathcal S}Q_E-mU.
\tag{19}
\]

对 \(z\in L\)，记

\[
d_{\mathcal S}(z)=\#\{E\in\mathcal S:z\in E\}.
\tag{20}
\]

于是 (19) 在尾外位置和尾位置的系数分别是

\[
k-d_{\mathcal S}(z),\qquad
k-d_{\mathcal S}(u)-m.
\tag{21}
\]

故得到一个不丢实际位置的充要判据：

\[
\boxed{
\begin{aligned}
W_{\mathcal S,m}\text{ 是实际子集}
\iff{}&d_{\mathcal S}(z)\in\{k-1,k\}
&&\forall z\in O,\\
&d_{\mathcal S}(u)\in\{k-m-1,k-m\}
&&\forall u\in U.
\end{aligned}}
\tag{22}
\]

若 (22) 成立，则自动有 \(0\le m\le k\)。唯一看似可能的
\(m=-1\) 会迫使 \(\mathcal S\) 中每个端点都含整个 \(U\)，与
端点迹为非空真子集矛盾。统一标签给

\[
\bar\sigma(W_{\mathcal S,m})=tq,\qquad t=k+mb.
\tag{23}
\]

当前端点数至多八，所以 \(t\le8+8b\le48<p\)。若 \(t\ge4\)，
则 \(X_{p-t}\dot\cup W_{\mathcal S,m}\) 是商零实际块。记
\(w=|W_{\mathcal S,m}|\)。由 (8)，\(1\le w\le14\)，并且

\[
n=p-t+w.
\tag{24}
\]

精确地，\(w\le t+1\) 时 \(n\in[9,p+1]\)，\(w\ge t+2\) 时
\(n\in[p+2,2p+2]\)。于是

\[
\boxed{
(22)\text{ 与 }k+mb\ge4\text{ 不能同时成立。}}
\tag{25}
\]

这包括三单点迹的
\(Q_{s_1}+Q_{s_2}+Q_{s_3}-U\)、四个两两不交余部的并，以及任意
更高端点稠密覆盖形式。配套程序另在 11,732 个小实例上从定义复核
(22)，并在全部覆盖 incidence 幸存骨架上检查 (25)。

## 4. 小 \(X\) 核形式的精确长度窗

表 (11) 中轴系数为负的形式用少量 \(X\)-位置闭合。令“支撑大小”
为相应 0/1 形式的实际位置数。冻结长度窗给出以下不含实际高度假设的
精确结论；交换 \(E,F\) 的行省略。

\[
\begin{array}{c|c|c|c}
\text{形式}&\text{0/1 条件}&p=233& p=1399\\
\hline
U&\text{恒成立}&c=4,n=7&c=5,n=8\\
U-Q_E&Q_E\subseteq U&c=5,n=5+|E\cap U|&c=6,n=6+|E\cap U|\\
U-Q_E-Q_F&Q_E,Q_F\subseteq U,\ Q_E\cap Q_F=\varnothing
&c=6&c=7\\
U+Q_E-Q_F&\text{表 (11) 的双包含条件}
&c=4&c=5.
\end{array}
\tag{26}
\]

由长度八只能属于 \(F_3\)，且正核心 \(F_3\) 必须恰为 \((b,U)\)，
还得到：

1. 在 \(p=1399\) 时，若 \(Q_E\subseteq U\) 且 \(|E\cap U|=2\)，
   则 \(U-Q_E\) 给出核心数六、长度八的错误正核心 \(F_3\)，故排除。
2. \(U-Q_E-Q_F\) 非空时，其支撑是
   \((E\cap U)\cap(F\cap U)\)。它只能来自两个不同双点迹并且支撑
   大小为一；\(p=233\) 时得到长度七的未定高度短块，\(p=1399\)
   时得到核心数七、长度八的错误 \(F_3\)，故排除。
3. 对 \(U+Q_E-Q_F\)，\(p=233\) 时支撑大小至少四便被排除：大小
   四触发非唯一长度八 \(F_3\)，更大进入 \([9,2p+2]\)；
   \(p=1399\) 的精确阈值是支撑大小至少三。

阈值以下的行还需要实际 \(a\)-高度才能判断落入 \(F_1,F_2\) 的哪一
族；本文没有把“长度允许”误写成可实现。

## 5. 非空余部重叠是精确的保护层

对迹不交端点对定义真实尾外重叠块

\[
D_{EF}:=Q_E\cap Q_F\cap O=L\setminus(E\cup F\cup U).
\tag{27}
\]

式 (13) 与 (18) 立即说明，每个幸存骨架必须满足

\[
\boxed{D_{EF}\ne\varnothing
\quad\text{对每个迹不交端点对 }E,F.}
\tag{28}
\]

而且 \(D_{EF}\) 是 \(Q_E,Q_F\) 的真子集。事实上，取
\(u\in F\cap U\)；迹不交给 \(u\notin E\)，所以
\(u\in Q_E\setminus D_{EF}\)。交换两端点得到另一边。由两个
\(Q\) 的投影原子性，

\[
\boxed{\rho(\bar\sigma(D_{EF}))\ne0.}
\tag{29}
\]

从形式和中减去双重出现的一份 \(D_{EF}\)，总能得到实际子集

\[
\widetilde W_{EF}
=Q_E+Q_F-U-D_{EF}.
\tag{30}
\]

但其统一标签是

\[
\bar\sigma(\widetilde W_{EF})
=(b+2)q-\bar\sigma(D_{EF}),
\tag{31}
\]

由 (29) 非轴向，不能再只靠若干 \(X\)-位置闭合。这准确解释了旧
十位置机制为何不能仅凭迹和大小推广成全覆盖矛盾：真正缺失的数据是
各个 \(D_{EF}\) 的实际位置身份、统一商标签，以及不同
\(D_{EF}\) 之间的重叠与联合子集和。

## 6. 全部四边覆盖迹类的有限 incidence 审计

配套程序
`unique_tail_cover_forbidden_block_generalization.py` 重新枚举十一幅
固定四边图的全部合法迹着色，得到

\[
\begin{array}{c|r}
\text{合法迹着色}&28584\\
\text{含不同双点迹覆盖候选的着色}&13512\\
\text{覆盖候选对出现次数}&24468.
\end{array}
\tag{32}
\]

程序对每一个覆盖候选对分别建立 incidence 骨架；多个候选对不被
错误地要求在同一个骨架中同时轴向。按覆盖对方向和其余迹多重集压缩
后，每个素数恰有 372 个规范覆盖迹类。

构造可概括如下。把覆盖对规范成迹 \(d_1,d_2\)，并把三片中的
\(U\)-位置分别记作 \(A_U,B_U,C_U\)。在 \(A\) 片放一个私有位置
\(a_0\)，在 \(B\) 片放一个私有位置 \(b_0\)，公共片放 \(y\)。
另外：

- 对 \(p=233\)，在 \(A,B\) 各放三个可共享位置；覆盖端点以及全部
  第三端点均取长度七。单点迹有 \(\binom65=6\) 个尾外选择，双点迹
  有 \(\binom64=15\) 个尾外选择。
- 对 \(p=1399\)，在 \(A,B\) 各放四个可共享位置；全部端点均取
  长度八。单点迹有 \(\binom86=28\) 个尾外选择，双点迹有
  \(\binom85=56\) 个尾外选择。

每个第三端点都含 \(y\)、命中 \(A,B,C\) 三片，并同时漏掉
\(a_0,b_0\)。同迹端点选择不同尾外子集；四边图无孤立点保证任一
迹在第三端点中至多出现四次，故上述候选数足够。程序用回溯逐规范类
检查端点互异及表 (11) 的全部确定排除行。

两个私有位置还给出 (25) 的统一保护：任何含至少两个第三端点的
端点子族，在 \(a_0,b_0\) 至少一处产生余部系数至少二；只含零个或
一个第三端点的剩余子族由程序直接遍历。因此，按 24,468 个出现次数
加权，每个素数都得到

\[
\begin{array}{c|r}
\text{单位形式检查}&16971084\\
\text{迹不交二余部大核门检查}&317826\\
\text{多端点形式检查}&28340748\\
\text{被全部已定单位长度门拒绝的构造}&0\\
\text{含 }t\ge4\text{ 的多端点 0/1 形式}&0\\
\text{incidence/迹/长度幸存出现次数}&24468.
\end{array}
\tag{33}
\]

\(p=233\) 与 \(1399\) 的单位 0/1 命中数分别为 2,035,770 与
1,982,670；差异来自第 4 节的长度八唯一尾门。报告的规范证书
SHA-256 为

\[
\mathtt{36ed4fe5bbc17e2e7706bc06c02bfc11b85ee321eccd053fad1b77fd2c9e3c10}.
\tag{34}
\]

## 7. 精确结论与下一缺口

**PROVED：**式 (13) 把十位置的两单点迹禁块推广到任意端点
incidence；式 (22)--(25) 又推广到任意端点子族。全部长度结论都
明确分开使用 \([9,p+1]\) 与 \([p+2,2p+2]\)。

**PROVED：**表 (11) 穷尽全部单位二余部形式；表 (26) 给出所有
小核心形式仅凭长度和唯一尾可以达到的精确排除窗。

**EXACT INCIDENCE SURVIVORS：**十一图、28,584 个迹着色中的
24,468 个不同双点迹覆盖候选出现次数，全部仍有通过上述实际位置
incidence、三片横截、强化单点迹长度和全部已定单位长度门的骨架。
这是一个穷尽的有限局部分类，不是商标签 SAT。

**MINIMAL MISSING POSITION DATA：**每条迹不交边都必须携带非空
保护块 \(D_{EF}\)，且 (29) 只知道它逐块非轴向。下一层必须把所有
\(D_{EF}\) 放在同一组实际 \(L\)-位置上，保留它们的统一商标签、
两两交和与同 \(R=P_1\dot\cup\cdots\dot\cup P_t\) 的联合子集和；
再从这些标签自动生成全部短块、新 \(F_3\) 及每个长补原子的内部
子集和。只记录 \(|D_{EF}|\) 或给每条边独立分配一个“非轴值”仍是
放宽。

**NOT PROVED：**任一 24,468 incidence 幸存者可配置统一标签；三个
强制 packing 型中任一型为空；大素数唯一尾分支为空；或 \(A_p\)
成立。故全局状态继续为 **INCOMPLETE**。
