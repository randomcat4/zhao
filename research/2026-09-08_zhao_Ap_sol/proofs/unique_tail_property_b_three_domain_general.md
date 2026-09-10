# Property B 下三个尾对支持域的全素数排除

STATUS: **PROVED FOR EVERY PRIME \(p\ge7\) USING REIHER'S PROPERTY B /
PENDING FRESH INDEPENDENT AUDIT / GLOBAL INCOMPLETE**

## 1. 冻结命题

令 \(p\ge7\) 为素数，固定

\[
C_p^2=\langle e,f\rangle,
\qquad w_1=e,\qquad w_2=f,\qquad w_3=-e-f.
\tag{1}
\]

假设 \(Q_1,Q_2,Q_3\) 都是长度 \(2p-1\) 的最小零和位置序列，
并分别含有尾对

\[
\{f,-e-f\},\qquad
\{e,-e-f\},\qquad
\{e,f\}.
\tag{2}
\]

则三个序列不可能有非空共同字面子序列：

\[
\boxed{Q_1\cap Q_2\cap Q_3=\varnothing.}
\tag{3}
\]

这里的交指实际位置交；同一共同位置在三条序列中当然携带同一个
\(C_p^2\) 标签。于是 \(p=233\) 时，要求共同核长度至少 \(435\)
的放宽三原子模型已经矛盾。“每对至多换六位置”是冗余前提。

## 2. 唯一外部输入：Reiher 的 Property B 定理

Christian Reiher 在 *A Proof of the Theorem According to Which Every
Prime Number Possesses Property B*（Rostock preprint 10/01, 2010）中证明：
每个素数都具有 Property B。原文把长度 \(2p-1\)、总和为零且没有
非空真零和子序列的序列称为 “cloudy sequence”，并在第 1 节把
Property B 等价表述为每个这样的序列都是 simple：经线性自同构后
具有

\[
g^{p-1}\prod_{t=1}^{p}(h+a_tg),
\qquad h\notin\langle g\rangle,
\qquad \sum_{t=1}^{p}a_t=1.
\tag{4}
\]

原始来源：
<https://www.math.uni-rostock.de/math/pub/preprints/preprint/2010/pre10_01.pdf>。

式 (4) 与本文的“长度 \(2p-1\) 最小零和序列”语义完全一致；没有
把零和自由序列、集合或支撑误当成位置序列。下文只使用 (4) 的支持
后果：存在非零基标签 \(g\) 和不过原点的仿射线

\[
L=h+\langle g\rangle
\tag{5}
\]

使

\[
\operatorname{supp}(Q)\subseteq \{g\}\cup L.
\tag{6}
\]

也可以只从 Property B 给出的 \(g^{p-1}\mid Q\) 推出 (6)：把其余
\(p\) 项投影到 \(C_p^2/\langle g\rangle\cong C_p\)，它们必须组成
长度 \(p\) 的循环群原子，故投影全为同一个非零值。

## 3. 一个指定尾对允许哪些支持域

设 \(a,b\) 线性无关，而标准支持 \(\{g\}\cup L\) 同时含 \(a,b\)。
因为 \(g\notin L\)，恰有三类可能：

1. \(g=a\)，且 \(L=b+\langle a\rangle\)；
2. \(g=b\)，且 \(L=a+\langle b\rangle\)；
3. \(a,b\in L\)，故
   \(g=c(b-a)\)、\(L=a+\langle b-a\rangle\)，其中
   \(c\in\mathbb F_p^\times\)。

因此，一个可能出现在此类原子中的非零标签，必落在上述可能支持的
并集中。把一般标签写成 \(z=xe+yf\)，对 (2) 的三个尾对，这三个
可能域分别包含在下列四直线并中：

\[
\begin{aligned}
\mathcal D_1&:\quad
 x=-1\quad\text{或}\quad y=x+1\quad\text{或}\quad
 y=2x\quad\text{或}\quad y=2x+1,\\
\mathcal D_2&:\quad
 y=-1\quad\text{或}\quad y=x-1\quad\text{或}\quad
 x=2y\quad\text{或}\quad x=2y+1,\\
\mathcal D_3&:\quad
 y=1\quad\text{或}\quad x=1\quad\text{或}\quad
 x+y=0\quad\text{或}\quad x+y=1.
\end{aligned}
\tag{7}
\]

例如对第一对 \((f,-e-f)\)，前三类标准支持依次贡献

\[
\{f\}\cup(-e-f+\langle f\rangle),
\quad
\{-e-f\}\cup(f+\langle-e-f\rangle),
\tag{8}
\]

以及基点直线 \(\langle-e-2f\rangle\) 与过两尾的仿射线
\(f+\langle-e-2f\rangle\)。这正给出 \(\mathcal D_1\) 的四行；
其余两对同理。原点不属于任何最小零和序列的支持，故必须从这些
直线并中删掉。

## 4. 三个域没有共同非零点

先在 \(\mathbb Q^2\) 中求 \(\mathcal D_1\) 的四条线与
\(\mathcal D_2\) 的四条线的交。除一对恒平行直线及重复项外，
只有以下十个候选：

\[
\begin{array}{c|c}
z=(x,y)&x+y\\ \hline
(-1,-1)&-2\\
(-1,-2)&-3\\
(-1,-\tfrac12)&-\tfrac32\\
(-2,-1)&-3\\
(-3,-2)&-5\\
(-\tfrac12,-1)&-\tfrac32\\
(0,0)&0\\
(-\tfrac13,-\tfrac23)&-1\\
(-2,-3)&-5\\
(-\tfrac23,-\tfrac13)&-1
\end{array}
\tag{9}
\]

当特征 \(p\ge7\) 时，分母 \(2,3\) 都可逆，所有非零候选均满足

\[
x\ne1,\qquad y\ne1,\qquad x+y\notin\{0,1\}.
\tag{10}
\]

所以它们全不属于 \(\mathcal D_3\)。唯一满足第三域某条方程的
有理候选是 \((0,0)\)，但原点已被原子性排除。因此

\[
\boxed{\mathcal D_1\cap\mathcal D_2\cap\mathcal D_3=\varnothing
\quad(p\ge7).}
\tag{11}
\]

从 (9)--(10) 还可精确看到，小特征异常只可能来自
\(2,3,5\)。配套证书逐条保留全部 \(16\) 个直线对，并在
\(p=2,3,5,7,11,233\) 上直接重算；前三个特征确有非零三交，后三个
为空。这里没有把小素数实验用于证明一般结论；一般结论来自分母和
非零分子的素因子只有 \(2,3,5\)。

## 5. 应用于共同核

若存在非空共同位置集 \(K\subseteq Q_1\cap Q_2\cap Q_3\)，取任意
\(k\in K\)，令其统一标签为 \(z\)。因为含零标签的序列立即有长度
一的真零和子序列，\(z\ne0\)。由三个 \(Q_i\) 的指定尾对与
Property B 标准形，依次有

\[
z\in\mathcal D_1,\qquad z\in\mathcal D_2,\qquad z\in\mathcal D_3,
\tag{12}
\]

与 (11) 矛盾。这证明 (3)。

特别地，\(p=233\) 的目标放宽模型不仅不能有 \(|K|\ge435\)，甚至
不能有一个共同位置。若首片的三个 \(Q_i\) 确实由同一张位置标签表
派生且分别为长度 \(465\) 的投影原子，那么这一投影层矛盾已足够；
无需调用 \(q\)-提升、\(P\) 混合目标、短谱、Hasse 或实际高度。

## 6. 证书与严格边界

配套脚本
`unique_tail_property_b_three_domain_general.py` 从直线方程重新生成
全部交点、异常素因子与有限域三交。当前语义证书为

```text
93e58bc3fe408bf3990c6fb85d4b82449a5eb59f749d342a071ad4e687ae5ce8
```

- **外部承重依赖：** Reiher 对所有素数的 Property B 定理。本文
  核对了原始来源中的对象定义和蕴含方向，但没有在仓库内重证其
  29 页证明。
- **本文已证：** 在该定理下，三个指定尾对的标准支持域对每个
  \(p\ge7\) 都没有共同非零标签。
- **不声称：** 对长度小于 \(2p-1\) 的近极值原子有相同分类；对
  没有统一字面标签的三张私有表有矛盾；或全局 \(A_p\) 已证。
- **当前裁决：** 这是解析排除，不是“有限 \(p=233\) UNSAT”外推；
  但在全新独立审计完成前仍标记 `PENDING FRESH INDEPENDENT AUDIT`。
