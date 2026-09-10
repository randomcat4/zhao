# \(p=233\) 全长七秩二支的 Property B 三原子排除

STATUS: **FIXED-SLICE UNSAT CANDIDATE / EXTERNAL THEOREM CHECKED / PENDING FRESH INDEPENDENT REVIEW / GLOBAL INCOMPLETE**

## 1. 结论

固定 \(p=233\)、型 \((3)\)、\(|P|=2\)、\(\kappa=1\) 的全长七首片。
设四边全异迹给出的三个单点迹端点对应于

\[
w_1=e,\qquad w_2=f,\qquad w_3=-e-f
\tag{1}
\]

这一已认证的 rank--2 标准形。令

\[
Q_i=K\mathbin{\dot\cup}(L\setminus H_i),
\qquad |Q_i|=2p-1=465,
\tag{2}
\]

并假设三个 \(\rho(Q_i)\) 都是 \(C_{233}^2\) 中的零和原子。则这些
条件已经矛盾。换言之，

\[
\boxed{
\text{\(p=233\) 的全长七、rank--2、三 singleton 端点首片为 UNSAT。}}
\tag{3}
\]

这比 OPEN-RECTANGLE-233 所要求的长度八矩形更强：本证明在矩形
出现以前就排除了三个极长原子。它不使用混合 \(P\)--\(Q_i\) 目标、
自动短块、Hasse 同余、实际高度或实际 \(Z\) 原子性。

## 2. 外部定理的精确接口

Christian Reiher 的博士论文／Rostock 预印本
[*A Proof of the Theorem According to Which Every Prime Number Possesses
Property B*](https://www.math.uni-rostock.de/math/pub/preprints/preprint/2010/pre10_01.pdf)
在第 2--3 页把 cloudy sequence 定义为 \(\mathbb F_p^2\) 上长度
\(2p-1\)、除空列和全列外没有零和子列的序列，并把 simple 定义为
在线性自同构及位置置换下具有形式

\[
g^{p-1}\prod_{t=1}^{p}(h+x_tg),
\qquad
h\notin\langle g\rangle,
\qquad
\sum_{t=1}^{p}x_t=1.
\tag{4}
\]

该文 Theorem 10.2 明确断言每个素数都有 Property B，即每个 cloudy
sequence 都是 simple。这里的同构只使用向量空间自同构与位置置换，
不含仿射平移。2020 年的后续论文
[*Inverse Problems Associated with Subsequence Sums in
\(C_p\oplus C_p\)*](https://math.colgate.edu/~integers/u3/u3.pdf)
Definition 2 和 Lemma 8 也以标准零和序列语言记录同一接口：长度
\(2n-1\) 的最小零和序列含某项 \(n-1\) 次，并具有 (4) 的完整正规形。

本首片的 \(\rho(Q_i)\) 长 \(2p-1\)、总和为零且没有非空真零和子列，
所以正是 Reiher 的 cloudy sequence。于是对每个 \(i\) 存在标签
\(g_i\ne0\) 和一条不经过零点、方向为 \(\langle g_i\rangle\) 的仿射线
\(\Lambda_i\)，满足

\[
v_{g_i}(Q_i)=p-1=232,
\qquad
\operatorname{supp}(Q_i)\subseteq\{g_i\}\cup\Lambda_i.
\tag{5}
\]

因此本文没有把 Property B 当作猜想或未证分类；只调用已经给出完整
证明的 prime case。余下论证是本地的有限几何。

## 3. 巨大共同核把每个重标签压入 \(K\)

已证的首片静态几何给出

\[
|Q_i\setminus K|=|L|-7\le30.
\tag{6}
\]

由 (5)--(6)，每个 \(g_i\) 在共同位置集 \(K\) 中至少出现

\[
(p-1)-30=232-30=202
\tag{7}
\]

次。这里必须使用统一的逐位置商标签：同一个 \(k\in K\) 在三个
\(Q_i\) 中携带同一个 \(C_{233}^2\) 标签。

如果 \(g_1,g_2,g_3\) 两两不同，则 \(K\) 至少含有

\[
3\cdot202=606
\tag{8}
\]

个位置；但 \(K\subseteq Q_1\) 且 \(|Q_1|=465\)，矛盾。所以至少
两个 \(g_i\) 相等。

数值 \(233\) 在这一步没有偶然魔法：若仍有 (6)，相同容量论证只需

\[
3(p-31)>2p-1,
\quad\text{即}\quad p>92.
\tag{9}
\]

## 4. 哪两个重标签能够相等

\(Q_i\) 包含另外两个尾位置。若其两个尾标签记为 \(a,b\)，则由
(5) 只有三种可能：

- \(g_i=a\)；
- \(g_i=b\)；
- \(a,b\in\Lambda_i\)，因而 \(g_i\) 平行于 \(a-b\)。

所以三个重标签分别落在

\[
\begin{aligned}
R_1&=\{w_2,w_3\}\cup
     (\langle w_2-w_3\rangle\setminus\{0\}),\\
R_2&=\{w_1,w_3\}\cup
     (\langle w_1-w_3\rangle\setminus\{0\}),\\
R_3&=\{w_1,w_2\}\cup
     (\langle w_1-w_2\rangle\setminus\{0\}).
\end{aligned}
\tag{10}
\]

代入 (1)，直接解两个一次齐次方程得到

\[
R_1\cap R_2=\{w_3\},\qquad
R_1\cap R_3=\{w_2\},\qquad
R_2\cap R_3=\{w_1\},
\tag{11}
\]

且 \(R_1\cap R_2\cap R_3=\varnothing\)。配套程序在
\(\mathbb F_{233}^2\) 中逐项重算了 (10)--(11)；每个 \(R_i\) 有
\(p+1=234\) 个候选标签。

因此三个 \(g_i\) 不可能全相等。若恰有一对相等，只剩以下三种情况：

\[
g_1=g_2=w_3,
\qquad g_1=g_3=w_2,
\qquad g_2=g_3=w_1.
\tag{12}
\]

## 5. 平行仿射线矛盾

先看 \(g_1=g_2=w_3\)。由 \(w_2\ne w_3\) 且 \(w_2\in Q_1\)，
(5) 迫使

\[
\Lambda_1=w_2+\langle w_3\rangle.
\tag{13}
\]

同理由 \(w_1\in Q_2\) 得

\[
\Lambda_2=w_1+\langle w_3\rangle.
\tag{14}
\]

第三个重标签 \(g_3\ne w_3\)，并由 (7) 至少有一个实际位置
\(k\in K\) 携带标签 \(g_3\)。这个同一位置同时属于 \(Q_1,Q_2\)。
它在两者中都不是重标签 \(w_3\)，故

\[
g_3\in\Lambda_1\cap\Lambda_2.
\tag{15}
\]

但两条线同向，而

\[
\det(w_1-w_2,w_3)=\det(e-f,-e-f)=-2\ne0\pmod{233},
\tag{16}
\]

所以它们是不同的平行仿射线，交为空，与 (15) 矛盾。

其余两种情况完全对称，但为避免隐藏符号，逐项写出：

\[
\begin{array}{c|c|c|c}
\text{相等重标签}&\text{第一条线的基点}&\text{第二条线的基点}
&\text{判别行列式}\\ \hline
g_1=g_3=w_2&w_3&w_1&\det(w_1-w_3,w_2)=2\\
g_2=g_3=w_1&w_3&w_2&\det(w_2-w_3,w_1)=-2
\end{array}
\tag{17}
\]

两个行列式在 \(\mathbb F_{233}\) 中都非零。未相等的第三个重标签在
\(K\) 中至少出现 \(202\) 次，故同样必须落入两条互不相交的平行线，
均得矛盾。结合第 3--4 节，所有重标签相等型都已穷尽，证明 (3)。

## 6. 对 OPEN-RECTANGLE-233 与全局状态的影响

OPEN-RECTANGLE-233 原先试图从三个近相同最大原子推出一个长度八
连通配对图。本文表明在当前全长七 rank--2 首片中不需要这座桥：
Reiher 的 Property B 正规形、共同核容量和三尾几何已经直接矛盾。

这也精确解释了此前私有标签放宽模型为何能够存在：它让三个原子
分别使用不同的 \(C_{233}^2\) 标签表，破坏了第 3 节把三个重标签同时
计入同一个 \(K\) 的关键拼接。精确首片的统一标签条件恢复后，该模型
立即失效。

本文只排除第一版 exact schema 的全长七 rank--2 子片。长度八端点、
rank--1 的 \(888/788\) 剩余型、其余 \(|P|\)、\(\kappa\)、迹图分支及其他
素数仍未由本文处理。因而固定 \(p=233\) 的完整问题和全局 \(A_p\)
仍为 **INCOMPLETE**。在全新独立复核通过以前，(3) 只记为
**FIXED-SLICE UNSAT CANDIDATE**。
