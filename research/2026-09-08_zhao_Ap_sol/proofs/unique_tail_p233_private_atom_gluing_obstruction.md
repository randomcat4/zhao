# (p=233) 三极长原子的私有标签拼接障碍

STATUS: **EXPLICIT STRICT RELAXATION / PRIVATE ATOM TABLES DO NOT GLUE / EXACT GLUED VERSION EXCLUDED ELSEWHERE / GLOBAL INCOMPLETE**

## 1. 结论与严格范围

本文给出 `OPEN-RECTANGLE-233` 的一条严格边界结果。可以同时实现：

1. 同一批 (474) 个实际位置；
2. 三个长度七的单点迹端点 (H_i)，两两只交于同一个投影非零位置；
3. 三个长度 (465=2p-1) 的位置集 (Q_i)，三重公共核长 (453)，
   任意两者单向只换六个位置；
4. 标准秩二尾

   \[
   w_1=e,\qquad w_2=f,\qquad w_3=-e-f;
   \tag{1}
   \]
5. 一张统一的 (C_{233}^3) 标签表，使三个 (H_i) 都商零、
   \(\bar\sigma(P)=3q\)、\(\bar\sigma(Y)=4q\)，并且根本没有长度八的
   商零位置块；
6. 对每个 (Q_i)，另有一张**私有** (C_{233}^2) 标签表，使它是
   真正的最大零和原子，而且三张私有表在所有尾位置上与 (1) 一致。

唯一关键放宽是：三个原子预言机的私有标签在共同核上彼此不一致，
也不等于统一标签表的秩二投影。因此这不是精确首片实例。它证明的
是否定陈述是

\[
\boxed{
\text{位置共同核、近相同位置集、尾 rank--2 与逐原子可满足性，}
\text{若没有统一标签拼接，就不推出长度八矩形。}}
\tag{2}
\]

缺失条件可以精确写成

\[
\boxed{
\eta_i(v)=\rho(\bar\gamma(v))
\quad(1\le i\le3,\ v\in Q_i),}
\tag{GLUE}
\]

其中 \(\bar\gamma\) 必须是同一张全局 \(C_{233}^3\) 逐位置标签表，
(eta_i) 是第 (i) 个原子预言机使用的 (C_{233}^2) 标签。
精确 schema 已经要求 (GLUE)；本文说明它不能在实现时被三个彼此
独立的原子求解器代替。

## 2. 同一位置几何

取

\[
U=\{u_1,u_2,u_3\},\qquad P=\{p_1,p_2\},\qquad K=\{k_1,\ldots,k_{453}\}.
\tag{3}
\]

再取一个位置 (y) 和三个两两不交的五位置集 (A_1,A_2,A_3)，
它们都与 (3) 不交。令

\[
Y=U\mathbin{\dot\cup}P\mathbin{\dot\cup}K
  \mathbin{\dot\cup}\{y\}\mathbin{\dot\cup}A_1
  \mathbin{\dot\cup}A_2\mathbin{\dot\cup}A_3,
\tag{4}
\]

\[
H_i=\{u_i,y\}\mathbin{\dot\cup}A_i,
\qquad Q_i=Y\setminus(H_i\mathbin{\dot\cup}P).
\tag{5}
\]

于是

\[
|Y|=474,\quad |H_i|=7,\quad |Q_i|=465,
\quad\bigcap_iQ_i=K,\quad |K|=453,
\tag{6}
\]

并且对 (i\ne j)，

\[
H_i\cap H_j=\{y\},\qquad
|Q_i\setminus Q_j|=6,\qquad |Q_i\triangle Q_j|=12.
\tag{7}
\]

这比首片只保证的 (|K|\ge435) 更紧。

## 3. 统一标签表：端点成立而长度八全灭

写 (C_{233}^3=\langle q,e,f\rangle)，并令

\[
c=451^{-1}=31\pmod{233}.
\tag{8}
\]

所有不属于 (U\cup P) 的位置先赋 (q)-坐标 (c)，三个尾位置赋
(-6c)，而 (p_1,p_2) 分别赋 (4,-1)。秩二坐标按如下方式赋值：

- (u_i) 的秩二坐标是 (w_i)；
- (y) 的秩二坐标是 (e)；
- (A_i) 的一个指定位置赋 (-w_i-e)，其余四个赋零；
- (k_1) 赋 (2e)，其余 (K\cup P) 位置赋零。

于是逐项相加得到

\[
\bar\sigma(H_i)=0,
\qquad \rho(\bar y)=e\ne0,
\qquad \bar\sigma(P)=3q,
\qquad \bar\sigma(Y)=4q.
\tag{9}
\]

最后一个等式的 (q)-坐标使用

\[
451c+3=4,
\tag{10}
\]

秩二坐标则为

\[
(w_1+w_2+w_3)+e+\sum_i(-w_i-e)+2e=0.
\tag{11}
\]

更强地，这张统一表没有任何长度八商零块。一个八位置集若取了
(t\in\{0,1,2,3\}) 个尾位置，并分别以
\(\varepsilon_1,\varepsilon_2\in\{0,1\}\) 表示是否取 \(p_1,p_2\)，
则其 (q)-坐标为

\[
c(8-7t-\varepsilon_1-\varepsilon_2)
 +4\varepsilon_1-\varepsilon_2.
\tag{12}
\]

对全部 (4\cdot2\cdot2=16) 种选择，式 (12) 在
(mathbb F_{233}) 中都非零；配套程序列出了全部余数。因此

\[
\boxed{N_8^{\rm global}(0)=0.}
\tag{13}
\]

特别地，这张表不可能含有 `OPEN-RECTANGLE-233` 所需的任何一条
长度八边，更不可能含有某侧 (230) 个顶点的连通配对图。

## 4. 三个私有标签表中的真正最大原子

对

\[
(j,k)=(2,3),(1,3),(1,2)
\tag{14}
\]

依次处理 (Q_1,Q_2,Q_3)。在第 (i) 张私有表中令

\[
g_i=w_j,\qquad h_i=w_k,
\tag{15}
\]

并把尾位置 (u_j,u_k) 分别标成 (g_i,h_i)。剩余 (463) 个位置
任意固定排序后，前 (231) 个标成 (g_i)，再后 (231) 个标成
(h_i)，最后一个标成 (g_i+h_i)。所以第 (i) 张表上的序列是

\[
\eta_i(Q_i)=g_i^{232}h_i^{232}(g_i+h_i).
\tag{16}
\]

因为 (g_i,h_i) 是一组基，(16) 的子序列由计数
((a,b,d)) 描述，其中

\[
0\le a,b\le232,\qquad d\in\{0,1\}.
\tag{17}
\]

它零和当且仅当

\[
a+d\equiv b+d\equiv0\pmod{233}.
\tag{18}
\]

在 (17) 的范围内，(18) 只有

\[
(a,b,d)=(0,0,0),\qquad(232,232,1).
\tag{19}
\]

所以每个 (16) 都是真正的长度 (465) 最大零和原子。三张表在共同
出现的尾位置上严格一致；但在 (K) 上三对分别有

\[
222,\qquad453,\qquad232
\tag{20}
\]

个位置标签不同。因此 (GLUE) 明确失败，不是抽象地说“可能不相干”。

## 5. 拼接条件与 Property B 正规形

这里还能得到一个不调用 Property B 的条件式障碍。

**引理。** 设 (Q) 是 (C_p^2) 中长度 (2p-1) 的原子，某个标签
(g) 在 (Q) 中出现 (p-1) 次。则存在 (h\notin\langle g\rangle)，
使其余 (p) 个标签全在仿射线

\[
h+\langle g\rangle
\tag{21}
\]

上。

**证明。** 投影到 (C_p^2/\langle g\rangle\cong C_p)。余下的
(p) 项投影总和为零。若其中某个非空真子列投影和为零，则其实际和
属于 (langle g\rangle)，可用至多 (p-1) 个现有 (g) 抵消，
得到 (Q) 的非空真零和子列，矛盾。因此这 (p) 个投影构成
(C_p) 中长度 (p) 的原子，只能是同一个非零标签的 (p) 次重复。
这正是 (21)。证毕。

现在假设 (GLUE) 已补上、(K\ne\varnothing)，而三个 (Q_i) 都有
一个重数 (p-1) 的标签。对一对指定尾 (a,b)，由引理，包含这对
尾的标准支持域只可能是下列三类：

\[
\{a\}\cup(b+\langle a\rangle),\qquad
\{b\}\cup(a+\langle b\rangle),
\tag{22}
\]

或对某个 (c\ne0)，

\[
\{c(b-a)\}\cup(a+\langle b-a\rangle).
\tag{23}
\]

程序对三对尾

\[
(w_2,w_3),\qquad(w_1,w_3),\qquad(w_1,w_2)
\tag{24}
\]

分别生成全部 (234=p+1) 个可能域。三个可能域并集的共同交为空：

\[
\boxed{\mathcal D_1\cap\mathcal D_2\cap\mathcal D_3=\varnothing.}
\tag{25}
\]

式 (25) 是 \(p=233\) 上对 \(233^2-1\) 个非零候选标签的精确有限
几何检查。它给出的严格蕴含是：

\[
\boxed{
\text{若存在满足 (GLUE) 且 }K\ne\varnothing\text{ 的三个真实 }Q_i,
\text{则至少一个 }Q_i\text{ 的最大标签重数至多 }p-2.}
\tag{26}
\]

Christian Reiher 的 2010 年 Theorem 10.2 已经证明每个素数都有
Property B，故每个 \(C_{233}^2\) 长度 \(2p-1\) 原子事实上都有
\(p-1\) 重标签。把这一外部定理与 (26) 合并，会直接排除精确拼接的
三个原子；完整的容量加强证明另见
unique_tail_p233_property_b_three_atom_exclusion.md。本文主体仍只
把私有标签构造记为放宽模型。

## 6. 对 `OPEN-RECTANGLE-233` 的精确更新

这次结果排除了一个实现层面的伪捷径：三个原子预言机不能各自返回
一张满足原子性的标签表；它们必须在全部公共位置上通过 (GLUE)
逐位置相等。只共享位置索引、尾标签、长度和和值都不够。

一旦强制 (GLUE)，Reiher 定理和 (26) 已经矛盾。因此这份放宽模型
不是精确 CEGAR 的幸存根；三个全删点原子预言机必须回到同一组公共
标签变量上，而不能在三个私有坐标系里分别求解。

尚未加入本文放宽模型的条件包括混合 (P\)--(Q_i) 目标、完整自动
短谱与中间禁窗、Hasse 同余、实际 (C_{233}^4) 高度、重数上界和
(Z) 原子性。故本文不声称精确首片 `SAT` 或 `UNSAT`，全局
(A_p) 保持 **INCOMPLETE**。
