# \(p=233\) mixed 短表示的高度提升与 \(2\leftrightarrow1\) 交换

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 范围

固定型 \((3)\)、\(|P|=2\)、\((p,b)=(233,4)\) 的当前切片。写

\[
X=x^{p-4},\qquad
P=\{z,z^\ast\},\qquad
\sigma(P)=3x-a,
\tag{1}
\]

以及三位置唯一正核心尾

\[
|U|=3,\qquad \sigma(U)=3a-4x.
\tag{2}
\]

取一个 singleton 端点的长补投影原子 \(Q_i\)，并假设
\(P\cap Q_i=\varnothing\)。设

\[
E\subseteq Q_i\setminus U,\qquad
\rho(\sigma(E))=-\rho(z)
\tag{3}
\]

是一个避尾 mixed 表示。因为 packing 投影非零，所以
\(E\ne\varnothing\)。令

\[
A=\{z\}\mathbin{\dot\cup}E,\qquad
\bar\sigma(A)=e q,\qquad e\in\{1,2,3\}.
\tag{4}
\]

此前已审的 mixed 核分离器给

\[
|E|\le e-1\le2.
\tag{5}
\]

本文把 (5) 提升到完整实际高度，并抽出一个新的交换电路。

## 2. 四种且仅四种高度分支

构造自动商零块

\[
D_A=X_{4-e}\mathbin{\dot\cup}U\mathbin{\dot\cup}A.
\tag{6}
\]

由 (2)、(4)，它的长度与实际和分别为

\[
|D_A|=8-e+|E|,
\qquad
\sigma(D_A)=3a-ex+\sigma(A).
\tag{7}
\]

由于 \(E\ne\varnothing\)，式 (5) 先排除 \(e=1\)。当 \(e=2\)
时，必有 \(|E|=1\) 且 \(|D_A|=7\)；当 \(e=3\) 时，
\(|E|\in\{1,2\}\)，相应长度为六或七。

块 (6) 具有正 \(X\)-核心，而其 \(Y\)-尾为
\(U\dot\cup A\supsetneq U\)。所以它不能属于 \(F_3\)，否则违反
正核心 \(F_3\) 尾的字面唯一性。结合

\[
F_1:2\text{--}6,\qquad
F_2:4\text{--}7,\qquad
F_3:6\text{--}8,
\tag{8}
\]

只剩下表中四种分支：

\[
\begin{array}{c|c|c|c|c}
e&|E|&|D_A|&D_A\text{ 的族}&\sigma(A)\\ \hline
2&1&7&F_2&2x-a\\
3&1&6&F_1&3x-2a\\
3&1&6&F_2&3x-a\\
3&2&7&F_2&3x-a
\end{array}
\tag{9}
\]

证明只需把 \(\sigma(D_A)=a\) 或 \(2a\) 代回 (7)。表 (9) 不把
长度六的柔性窗误判成单值；它完整保留 \(F_1/F_2\) 两支。

由 (1) 与 \(A=\{z\}\dot\cup E\)，表 (9) 等价地给出

\[
\boxed{
\sigma(E)=
\begin{cases}
\sigma(z^\ast)-x,&(e,|E|,F)=(2,1,F_2),\\
\sigma(z^\ast)-a,&(3,1,F_1),\\
\sigma(z^\ast),&(3,1,F_2)\text{ 或 }(3,2,F_2).
\end{cases}}
\tag{10}
\]

这些是同一张真实位置表上的完整 \(C_{233}^4\) 等式，不只是商标签
或聚合计数。

## 3. 两个 signed 纤维同时避尾时必有交换电路

设 packing 两点的投影分别为 \(s,-s\)，其中 \(s\ne0\)。此前已审
结论还给出：任取

\[
E_+\subseteq Q_i\setminus U,\quad
\rho(\sigma(E_+))=s,
\qquad
E_-\subseteq Q_i\setminus U,\quad
\rho(\sigma(E_-))=-s,
\tag{11}
\]

只要二者都存在，就有

\[
E_+\cap E_-\ne\varnothing.
\tag{12}
\]

二者不可能同时为单点。否则 (12) 迫使
\(E_+=E_-=\{w\}\)，继而
\(\rho(w)=s=-s\)，即 \(2s=0\)，与 \(p=233\) 及 \(s\ne0\)
矛盾。

故两个 signed 纤维若都存在避尾表示，任取一对表示时至少一个是
双点。由 (5)，双点表示必有 \(e=3\)；再由表 (9)，它必属于最后
一行。若该双点表示与 packing 点 \(z\) 配对，则

\[
\boxed{|E|=2,\qquad \sigma(E)=\sigma(z^\ast).}
\tag{13}
\]

式 (13) 是一个真实的 \(2\leftrightarrow1\) 加法交换电路：两个
长补内部位置的完整实际和等于另一个 packing 单点。

## 4. 对适用 outer rows 的严格二分

对 540 个含一个长七 singleton 的 outer rows，仿射 signed 系数已
保证至少一个目标纤维有避尾表示。对余下 180 个“三个 singleton
端点均长八”的行，当 packing 方向落在三条尾方向上时，二次签名给出
同一结论。这里没有声称这 180 行的所有非-singleton 端点也都长八；
事实上其中只有 36 行的全部端点均长八。因此在上述适用行的选定
singleton 端点上，必有下列二择一：

1. 存在式 (13) 的真实两点--单点交换电路；
2. 所有避尾表示都是单点。此时只有一个 signed 目标能避尾，另一个
   目标的每个表示都使用两个尾位置之一；存在的单点表示还必须满足
   式 (10) 的三个单点高度签名之一。

第二支中“另一个目标没有避尾表示”来自第 3 节：若两边都非空，
就会强迫一个双点表示。这里没有把 signed 系数为零误当成“没有
表示”；横截结论只在全部避尾表示确实为空时使用。

## 5. 下一承重点

式 (13) 应作为统一标签求解器的新硬门：枚举真实 endpoint mask 后，
每个两点集合必须引用 \(Q_i\setminus U\) 中的字面位置，并与对应
packing 单点满足完整四维和相等。单点支则同时加载式 (10)、另一
signed 目标的双尾横截、全部自动短块、每个长补原子的内部子集和与
Hasse 行。

本文尚未载入 720 行的统一 \(\rho,q\)、高度标号，因而没有删除
outer row；固定 \(p=233\) 切片及全局 \(A_p\) 仍为
**INCOMPLETE**。
