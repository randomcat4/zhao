# 三点唯一尾的共同外部序列：三原子分解与零和自由核

STATUS: PROVED_DECOMPOSITION / FOURTH_BLOCK_NOT_FORCED / GLOBAL_INCOMPLETE

## 1. 范围与结论

只考虑

\[
(p,\ell,b,r)=(233,7,4,3),\qquad(1399,8,5,3)
\tag{1}
\]

的唯一尾分支。沿用

\[
X=x^{p-4}\subset Z,\qquad Y=Z\setminus X,\qquad
\bar x=q\ne0,\qquad |Y|=2p+8,
\tag{2}
\]

以及四边联合前沿抽出的端点族 \(\mathcal A\)。每个
\(H\in\mathcal A\) 是零核心 \(F_3\) 块：

\[
\bar\sigma(H)=0,\qquad \sigma(H)=3a,\qquad 6\le|H|\le8.
\tag{3}
\]

令

\[
L=U\cup\bigcup_{H\in\mathcal A}H,\qquad R=Y\setminus L.
\tag{4}
\]

已有

\[
|L|\le52,\qquad |R|\ge2p-44.
\tag{5}
\]

本轮把共同外部序列 \(R\) 进一步严格分解为

\[
\boxed{R=P_1\mathbin{\dot\cup}\cdots
\mathbin{\dot\cup}P_t\mathbin{\dot\cup}K,\qquad 0\le t\le3,}
\tag{6}
\]

其中每个 \(\rho(P_i)\) 是 \(C_p^2\) 的零和原子，而
\(\rho(K)\) 是零和自由序列。各 \(P_i\) 的轴系数只有七种主类型；
把它们固定放进每个端点的投影原子分解后，只剩十四个
“共同 packing—端点余部分解”行。三个主类型还强制

\[
K\mathbin{\dot\cup}(L\setminus H)
\]

对每个端点 \(H\) 本身都是一个投影零和原子。

这严格小于此前任意共同谱 \(M_R(k,g)\) 的接口，但仍没有强迫
第四个不交投影零块。裁决为

\[
\boxed{\mathsf{PROVED\_DECOMPOSITION}/
\mathsf{FOURTH\_BLOCK\_NOT\_FORCED}/
\mathsf{GLOBAL\_INCOMPLETE}.}
\tag{7}
\]

## 2. 极大不交原子族与零和自由核

在 \(R\) 中选择一个基数最大的两两不交位置子序列族

\[
\mathcal P=\{P_1,\ldots,P_t\},
\tag{8}
\]

要求每个 \(\rho(P_i)\) 是 \(C_p^2\) 中的非空零和原子。若
\(R\) 含非空投影零子集，其中必含一个按包含极小的零和子集，
所以 (8) 存在。令

\[
K=R\setminus\bigcup_{i=1}^tP_i.
\tag{9}
\]

由 \(\mathcal P\) 的最大性，\(\rho(K)\) 没有非空零和子序列；
否则该子序列内再取一个原子，就能给 (8) 增加一个不交成员。
所以 \(K\) 是投影零和自由核。这证明了 (6) 中除 \(t\le3\) 外的
全部断言。

固定任一端点 \(H\)。因为

\[
R\subseteq Y\setminus H
\]

且 \(L\setminus H\) 非空，所以 \(R\) 的每个非空子集都是
\(Y\setminus H\) 的真子集。端点长补的完整轴向判据于是给每个
\(P_i\) 一个唯一系数

\[
\bar\sigma(P_i)=d_iq,\qquad d_i\in\{1,2,3\}.
\tag{10}
\]

任意非空指标集 \(I\subseteq\{1,\ldots,t\}\) 的并仍是
\(Y\setminus H\) 的非空真子集，故

\[
\sum_{i\in I}d_i\pmod p\in\{1,2,3\}.
\tag{11}
\]

由于 \(p\ge233\)，任取四个系数时普通和介于四和十二，不能落在
\(\{1,2,3\}\)。故 \(t\le3\)。逐项使用 (11) 得到七种且仅七种
共同 packing 类型：

\[
\varnothing,\quad
(1),(2),(3),\quad
(1,1),(1,2),\quad
(1,1,1).
\tag{12}
\]

特别地，不交两块只能是 \((1,1)\) 或 \((1,2)\)，不交三块只能
全为一，第四块不可能。

## 3. 每个端点余部的十四行分解表

对每个 \(H\in\mathcal A\)，记

\[
W_H=Y\setminus H,\qquad
Q_H=K\mathbin{\dot\cup}(L\setminus H).
\tag{13}
\]

因为 \(W_H=R\mathbin{\dot\cup}(L\setminus H)\)，(6) 给

\[
W_H=P_1\mathbin{\dot\cup}\cdots
\mathbin{\dot\cup}P_t\mathbin{\dot\cup}Q_H.
\tag{14}
\]

\(\rho(W_H)\) 是投影零和序列。把 \(\rho(Q_H)\) 任意分解成投影
零和原子，再同固定的 \(\rho(P_i)\) 合并，就得到
\(\rho(W_H)\) 的一个原子分解。此前的完整端点分解定理说明，
每一种这样的分解的轴系数多重集只能为

\[
(1,3),\quad(2,2),\quad(1,1,2),\quad(1,1,1,1).
\tag{15}
\]

从 (15) 删去 (12) 的固定共同系数，得到：

\[
\begin{array}{c|c|c}
(d_1,\ldots,d_t)&
\text{\(\rho(Q_H)\) 的可能原子系数型}&
\bar\sigma(Q_H)\\ \hline
\varnothing&(1,3),(2,2),(1,1,2),(1,1,1,1)&4q\\
(1)&(3),(1,2),(1,1,1)&3q\\
(2)&(2),(1,1)&2q\\
(3)&(1)&q\\
(1,1)&(2),(1,1)&2q\\
(1,2)&(1)&q\\
(1,1,1)&(1)&q
\end{array}
\tag{16}
\]

表中共有

\[
4+3+2+1+2+1+1=14
\tag{17}
\]

个展开行。它对每个实际端点 \(H\) 分别成立；不同端点可在同一
主类型允许的余部行之间选择，但它们共享完全相同的
\(P_1,\ldots,P_t,K\)。

特别地，以下三个共同 packing 类型强制所有端点余部本身为原子：

\[
(3),\qquad(1,2),\qquad(1,1,1)
\Longrightarrow
\boxed{\rho(Q_H)\text{ 是 \(C_p^2\) 的零和原子 }
\quad\forall H\in\mathcal A.}
\tag{18}
\]

这是因为 (16) 的余部分解只有单因子型 \((1)\)。它不是说
\(Q_H\) 在实际群 \(C_p^4\) 中是零和原子。

## 4. 核长度与固定总和接口

记

\[
n_i=|P_i|,\qquad d=\sum_{i=1}^td_i,\qquad
g_i=\sigma(P_i)\in C_p^4.
\tag{19}
\]

由 \(D(C_p^2)=2p-1\) 与零和自由极值，

\[
1\le n_i\le2p-1,\qquad 0\le|K|\le2p-2,
\tag{20}
\]

并且

\[
|K|=|R|-\sum_i n_i
\ge\max\left\{0,\ 2p-44-\sum_i n_i\right\}.
\tag{21}
\]

冻结关系给 \(\sigma(Y)=4x\)。又
\(\sigma(H)=3a\)，所以共同核和每个端点余部的实际总和为

\[
\boxed{
\sigma(K)=4x-\sigma(L)-\sum_i g_i,}
\tag{22}
\]

\[
\boxed{
\sigma(Q_H)=4x-3a-\sum_i g_i
\quad\forall H\in\mathcal A.}
\tag{23}
\]

商总和相应为

\[
\bar\sigma(K)=(4-d)q-\bar\sigma(L),\qquad
\bar\sigma(Q_H)=(4-d)q.
\tag{24}
\]

特别地，\(\rho(\bar\sigma(K))=-\rho(\bar\sigma(L))\)，完全由有限
局部标签决定。

在 (18) 的三个强制原子类型中，Davenport 上界还逐端点给出

\[
|Q_H|=|K|+|L|-|H|\le2p-1,
\tag{25}
\]

即

\[
|K|\le2p-1-|L|+|H|
\quad\forall H\in\mathcal A.
\tag{26}
\]

式 (21)--(26) 是下一次接入统一标签核验器所需的精确核长度与
总和接口，而不只是“至多三个块”的口头分解。

## 5. 与共同子集和谱和端点局部差集的连接

对任意位置序列 \(S\subseteq C_p^4\)，写

\[
\Phi_S(z)=\prod_{s\in S}(1+z[s]).
\tag{27}
\]

分解 (6) 给出同一实际位置层面的恒等式

\[
\boxed{
\Phi_R(z)=\Phi_K(z)\prod_{i=1}^t\Phi_{P_i}(z).}
\tag{28}
\]

因此旧接口中的共同谱 \(M_R(k,g)\) 不再任意：它必须是一个
投影零和自由核谱与至多三个投影原子谱的卷积。核谱满足

\[
[z^k g]\Phi_K(z)>0,\quad \rho(\pi(g))=0
\Longrightarrow k=0.
\tag{29}
\]

固定端点 \(H\) 后，

\[
\Phi_{Q_H}(z)=\Phi_K(z)\Phi_{L\setminus H}(z).
\tag{30}
\]

所以 (16) 的余部分解型、(18) 的原子性以及端点补集的全部内部
子和，都由同一个 \(\Phi_K\) 与不同的有限局部差集
\(L\setminus H\) 卷积。对于 (18)，精确禁式是：

\[
\varnothing\ne F\mathbin{\dot\cup}E
\subsetneq K\mathbin{\dot\cup}(L\setminus H)
\Longrightarrow
\rho(\bar\sigma(F)+\bar\sigma(E))\ne0
\tag{31}
\]

对每个 \(F\subseteq K\)、\(E\subseteq L\setminus H\) 同时成立。
所有端点共享 \(F\) 所来自的同一个逐位置核 \(K\)；不能给每个
\(H\) 独立选择一个零和自由核。

式 (22)--(31) 可直接接入严格统一标签核验器：保留
\(P_i,K,L\) 的真实位置标签，从 (28) 卷积生成全部自动短块、
Hasse 行和长补内部子和。只保留未标记的 \(\Phi_K\) 边缘系数仍
不足以恢复两个外部短块的真实交集，故本文没有把谱因式分解冒充
完整逐位置实例。

## 6. 为什么当前仍不能强迫第四块

式 (5) 的长度下界只到

\[
|R|\ge2p-44=D(C_p^2)-43.
\tag{32}
\]

这个量级本身甚至不强迫第一个投影零块。取 \(C_p^2\) 的一组基
\(e_1,e_2\)，则

\[
e_1^{\,p-1}e_2^{\,p-43}
\tag{33}
\]

长度恰为 \(2p-44\)，且投影零和自由：任一零和子序列在两个独立
坐标上使用的项数都须被 \(p\) 整除，但两种重数都严格小于 \(p\)。
这只是对“纯长度推出零块”的显式反例，不满足也不声称满足本题
固定总和、端点局部差集、Hasse 行或实际原子条件。

若 \(|R|\ge2p-1\)，Davenport 只强迫一个 \(P_i\)，仍不强迫四个。
要从 (12) 推到矛盾，必须新增下列至少一项可验证输入：

1. 从固定总和 (22)--(24) 与零和自由核分类证明某个 \(K\) 不可能；
2. 从端点局部差集同时证明四个互不相交的核内投影零子集；
3. 用逐位置或逐对 Hasse 行证明 \(\Phi_K\) 必有违反 (29) 的系数；
4. 在 (18) 的三类中，证明共同 \(K\) 不可能使所有
   \(K\cup(L\setminus H)\) 同时为投影原子。

本文尚未得到其中任何一项。尤其不得调用未在本工作树自足证明的
近 Davenport 强逆定理来排除 (33) 一类核。

## 7. 有限证书

配套脚本 unique_tail_common_R_next.py 独立核对：

- 七个共同 packing 主类型与十四个展开余部分解行；
- 三个强制共同端点余部为原子的主类型；
- \(p=233,1399\) 的 \(R\) 下界、Davenport 距离 \(43\)；
- (33) 在两个素数处的长度与逐坐标零和自由性。

固定哈希为

\[
\begin{aligned}
\text{type SHA-256}
&=\mathtt{5f5f08a41a90fba288ba84b397dafa73f90028fb4982d421c297ab6f4af95027},\\
\text{certificate SHA-256}
&=\mathtt{24ffe43612df8927e3d192cf0dcde34629ed5de0dfa4ba1eaacc8080b8963169}.
\end{aligned}
\tag{34}
\]

验证命令：

    C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/2026-09-08_zhao_Ap_sol/unique_tail_common_R_next.py

## 8. 停止线

**PROVED：**对每个满足冻结接口且具有上述四边端点族的实际候选，
存在 (6) 的至多三原子加零和自由核分解；七个主类型、十四个端点
余部分解行及 (18)、(21)--(31) 对所有端点同时成立。

**NOT PROVED：**共同 \(R\) 必含四个不交投影零块；任何七个主类型
不可实现；或任何满足这些必要条件的实际 \(R\) 存在。

因此本轮是严格可复用的 survivor decomposition，不是 SAT 模型，
更不是全局反例。全局定理仍为 INCOMPLETE。
