# \(p=233\) 混合首片：一个长八补原子有至少 461 个完全覆盖删点

STATUS: **PROVED_REDUCTION / INDEPENDENT_REVIEW CORRECT /
GLOBAL_INCOMPLETE**

## 1. 精确陈述

固定

\[
p=233,\qquad\text{型 }(3),\qquad |P|=2,
\tag{1}
\]

以及 720 个 length-decorated outer survivors 中任意一行。三个
singleton 尾迹端点记为 \(H_1,H_2,H_3\)，尾标签在秩二标准形下为

\[
w_1=e,\qquad w_2=f,\qquad w_3=-e-f.
\tag{2}
\]

相应 \(Q_i\) 分别含有另外两个实际尾位置，其投影标签为

\[
\{f,-e-f\},\qquad
\{e,-e-f\},\qquad
\{e,f\}.
\tag{3}
\]

三个 singleton 端点中至多一个长七，故

\[
I_8=\{i:|H_i|=8\},\qquad |I_8|\in\{2,3\}.
\tag{4}
\]

对 \(i\in I_8\)，令 \(N_i=Q_i\setminus U\) 为 \(Q_i\) 中的非尾
位置，并定义

\[
\mathcal C_i=
\left\{x\in N_i:
\Sigma\bigl(\rho(Q_i\setminus\{x\})\bigr)
=C_{233}^2\setminus\{0\}\right\}.
\tag{5}
\]

因为 \(|Q_i|=464\) 且 \(Q_i\) 恰含两个尾位置，

\[
|N_i|=462.
\tag{6}
\]

则存在一个统一的 \(i\in I_8\) 使

\[
\boxed{|N_i\setminus\mathcal C_i|\le1,\qquad
|\mathcal C_i|\ge461.}
\tag{7}
\]

特别地，共同核 \(K\subseteq N_i\) 上仍有

\[
|K\cap\mathcal C_i|\ge |K|-1\ge434.
\tag{8}
\]

这严格加强旧版的鸽巢下界 \(145/218\)。

## 2. 三个允许支持域

对第 \(i\) 个尾对，记 \(\mathcal D_i\) 为 Property B 标准域在
所有可能重标签上取并后得到的四直线并。已经独立审定的三域定理给出

\[
\mathcal D_1\cap\mathcal D_2\cap\mathcal D_3=\varnothing
\qquad(p\ge7),
\tag{9}
\]

其中原点也因原子性被排除。

若 \(|H_i|=7\)，则 \(Q_i\) 是长度 \(2p-1=465\) 的投影原子；
Property B 直接给

\[
\operatorname{supp}\rho(Q_i)\subseteq\mathcal D_i.
\tag{10}
\]

若 \(|H_i|=8\)，则 \(Q_i\) 是长度 \(2p-2=464\) 的投影原子。对任意
\(x\in N_i\setminus\mathcal C_i\)，删点序列缺少某个非零投影目标。
已经独立审定的近最大原子完成二分把
\(\rho(Q_i\setminus\{x\})\) 嵌入一个 Property B 最大原子。由于
\(x\) 不是尾位置，两个指定尾位置都仍在删点序列内，所以该完成原子的
标准域属于第 \(i\) 个尾对的允许族，因而

\[
\operatorname{supp}\rho(Q_i\setminus\{x\})
\subseteq\mathcal D_i.
\tag{11}
\]

式 (11) 不把被删位置 \(x\) 偷塞进 \(\mathcal D_i\)。

## 3. 两个坏删点会补回彼此的例外

令

\[
B_i=N_i\setminus\mathcal C_i.
\tag{12}
\]

若同一个 \(i\in I_8\) 有两个不同坏删点 \(x,y\in B_i\)，则分别由
(11) 得

\[
\operatorname{supp}\rho(Q_i\setminus\{x\})\subseteq\mathcal D_i,
\qquad
\operatorname{supp}\rho(Q_i\setminus\{y\})\subseteq\mathcal D_i.
\tag{13}
\]

两个实际位置删点序列的并就是完整 \(Q_i\)：

\[
(Q_i\setminus\{x\})\cup(Q_i\setminus\{y\})=Q_i.
\tag{14}
\]

所以

\[
|B_i|\ge2
\Longrightarrow
\operatorname{supp}\rho(Q_i)\subseteq\mathcal D_i.
\tag{15}
\]

反设每个 \(i\in I_8\) 都有 \(|B_i|\ge2\)。对长八 singleton，
(15) 给出 \(K\) 的每个投影标签属于对应 \(\mathcal D_i\)；若存在
唯一长七 singleton，则 (10) 给出剩余的第三个域。于是任取
\(k\in K\) 并置 \(z=\rho(k)\)，都有

\[
z\in\mathcal D_1\cap\mathcal D_2\cap\mathcal D_3.
\tag{16}
\]

\(K\) 零和自由，故 \(z\ne0\)，这与 (9) 矛盾。因此至少一个
\(i\in I_8\) 满足 \(|B_i|\le1\)，证明 (7)。式 (8) 由
\(|K|\ge435\) 立即得到。

这里不要求两个删点完成后得到同一个标准域：每个具体标准域只需包含于
同一个四直线并 \(\mathcal D_i\)，(13)--(15) 就成立。

## 4. 得到的精确接口与硬边界

选取 (7) 中的统一 \(Q_i\)。除至多一个非尾位置外，每个
\(x\in N_i\) 与每个非零目标 \(r\in C_{233}^2\) 都存在实际位置子集

\[
E_{x,r}\subseteq Q_i\setminus\{x\},
\qquad \rho(\sigma(E_{x,r}))=r.
\tag{17}
\]

因此下一层求解器必须在同一套 \(q\)-标签上维持至少 461 份
“删点后全目标可达”，同时满足两个 packing 单点的 mixed 高度、
全部自动短块、其他端点长补和实际高度。

但 (17) 不控制表示长度、\(q\)-系数或不同 \((x,r)\) 见证的相交。
配套的完成丰富反例族还表明：单个长度 \(2p-2\) 原子甚至可以对
\(2p-3=463\) 个删点完全覆盖，并通过单端点全部 mixed 条件。因此
(7) 本身不删除 outer row；它把承重点推进到多个近相同长补的统一
位置/\(q\)/短块粘合。全局 \(A_p\) 仍为 **INCOMPLETE**。
