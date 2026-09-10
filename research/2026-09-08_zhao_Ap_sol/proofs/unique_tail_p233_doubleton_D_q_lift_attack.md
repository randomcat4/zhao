# (p=233) 三 doubleton 模型 D 的局部 (q)-提升攻击

STATUS: **FIXED MODEL-D ENDPOINT-INTERNAL (q)-LIFT SAT /
ACTUAL MULTIPLICITY CAP VERIFIED / RELAXED / GLOBAL INCOMPLETE**

## 1. 结论

固定

\[
p=233,\qquad X=x^{p-4}=x^{229},\qquad
e=(1,0),\quad f=(0,1),\quad t=-e-f
\tag{1}
\]

以及 `unique_tail_p233_property_b_mixed_trace_relaxed_models.md` 的
three-doubleton 模型 D。本文不改动它的任何真实位置或
\(C_{233}^2\) 标签，并保持三条

\[
\rho(Q_H)
\tag{2}
\]

都是长度 \(465\) 的最大零和原子。

在此固定骨架上加入：

1. 每个真实位置统一的 \(q\)-坐标和实际高度；
2. 三个 \(H\) 的商和为零、实际和为 \(3a\)；
3. 唯一尾、\(W\)、两位置型 \((3)\) packing、\(Y\) 与 \(Z\) 的
   一阶总和；
4. 整个 \(X\mathbin{\dot\cup}Y\) 上每个实际标签的重数至多
   \(p-4=229\)；
5. 每个 \(H\) 内全部 \(\rho\)-零位置子集所自动诱导的短长度窗，
   并排除这些子集产生的整个中间商零禁区。

所得局部系统仍然可满足：

\[
\boxed{
\text{固定 Model D 存在统一的 endpoint-internal (q)/height lift。}}
\tag{3}
\]

唯一非平凡的自动新短块是一个长度五的 \(F_1\) 块。Model D 中的
\(\rho\)-零三子集被赋予轴系数 \(+1\)，需要 \(232\) 个 \(X\)
位置才可商零，超过现有的 \(229\) 个；它的四点补集轴系数为
\(-1\)，与一个 \(X\) 位置组成允许的长度五 \(F_1\)。

因此，端点内部短闭包本身不能排除 Model D。本文没有检查不包含在
单个 \(H\) 中的 \(Y\)-子集、全局自动短谱、mixed \(P\)--\(Q_H\)
目标、Hasse 行或实际 \(Z\) 原子性，故 (3) 是严格标记的
**RELAXED SAT**，不是完整首片 SAT。

## 2. 固定的 Model-D 位置骨架

置

\[
g=e,\qquad h=2e+f,\qquad z=e+h=3e+f,
\qquad r=5e+f,
\qquad y=-8e-3f.
\tag{4}
\]

位置胞保持为

\[
\begin{array}{c|c|c}
\text{位置胞}&\text{个数}&\rho\text{-标签多重集}\\ \hline
K&456&g^{229}h^{227}\\
P_{13}&4&h^4\\
P_{23}&4&g\,h\,z^2\\
P_{12}&4&g^2 f r\\
E_1&1&u_e:g\\
E_2&1&u_f:f\\
E_3&1&u_t:t\\
O&1&y.
\end{array}
\tag{5}
\]

这里 \(L\) 为除 \(K\) 外的十六个位置，\(W=K\dot\cup L\) 长
\(472\)。三个长七端点是

\[
\begin{aligned}
H_1&=P_{23}\mathbin{\dot\cup}E_2\mathbin{\dot\cup}E_3
     \mathbin{\dot\cup}O,\\
H_2&=P_{13}\mathbin{\dot\cup}E_1\mathbin{\dot\cup}E_3
     \mathbin{\dot\cup}O,\\
H_3&=P_{12}\mathbin{\dot\cup}E_1\mathbin{\dot\cup}E_2
     \mathbin{\dot\cup}O.
\end{aligned}
\tag{6}
\]

它们的迹依次为 \(\{f,t\},\{e,t\},\{e,f\}\)，都含同一非尾位置
\(O\)，且 \(\rho(H_i)=0\)。逐位置定义

\[
Q_i=K\mathbin{\dot\cup}(L\setminus H_i).
\tag{7}
\]

原证书已经核验 \(|Q_i|=465\)、\(K=Q_1\cap Q_2\cap Q_3\)，以及
三个 \(\rho(Q_i)\) 的完整 simple 参数。本文的脚本不导入旧作者
模块，而是从 (4)--(7) 重建并重新核验三条最大原子。

## 3. 统一 (q)-坐标与高度见证

把商标签写成

\[
\bar v=c_vq+\rho(v),
\]

并把实际标签的第四坐标记为 \(d_v\)。规范化

\[
x=(q,0),\qquad a=(0,1),qquad h_x=0.
\tag{8}
\]

下表列出 \(W\) 中所有非零的 \(c_v,d_v\)；未列位置两坐标均取
零。下标 `001` 等表示该多重胞中的一个固定真实位置。

\[
\begin{array}{c|r|r}
v&c_v&d_v\\ \hline
u_e&-4&3\\
P_{23}\text{ 中的 }g&1&2\\
O=y&-1&1\\
P_{13}:h_{001}&5&-1\\
P_{13}:h_{002}&0&1\\
P_{13}:h_{003}&0&-1\\
P_{12}:g_{1}&5&-1\\
K:g_{001}&-5&0\\
K:h_{001}&0&-3.
\end{array}
\tag{9}
\]

所有数均在 \(\mathbb F_{233}\) 中理解。为同时闭合型 \((3)\)、
\(|P|=2\)、\(\kappa=1\) 的一阶总和，再加入两个 packing 位置

\[
\begin{array}{c|c|r|r}
 &\rho&c&d\\ \hline
p_1&(7,11)&0&0\\
p_2&(-7,-11)&3&-1.
\end{array}
\tag{10}
\]

于是 \(\rho(P)\) 是二项原子，且

\[
\bar\sigma(P)=3q,
\qquad
\sigma(P)=3x-a.
\tag{11}
\]

直接求和得到

\[
\begin{array}{c|c|c|c}
\text{位置集}&q\text{-坐标和}&\rho\text{-和}&\text{高度和}\\ \hline
U&-4&0&3\\
W&1&0&1\\
P&3&0&-1\\
Y=W\dot\cup P&4&0&0\\
X\dot\cup Y&0&0&0\\
H_i&0&0&3\\
Q_i&1&0&-2.
\end{array}
\tag{12}
\]

所以唯一尾满足

\[
\bar\sigma(U)=-4q,
\qquad
\sigma(U)=3a-4x,
\tag{13}
\]

三条 \(H_i\) 都仍是零核心 \(F_3\) 块，且所有 \(Q_i\) 的轴系数
都是一。

## 4. 实际重数上界

实际标签记作

\[
(c_v,\rho(v),d_v)\in C_{233}^4.
\tag{14}
\]

式 (9) 特意拆开了两个大投影纤维。完整重数表的最大值为

\[
\boxed{229}.
\tag{15}
\]

恰好达到上界的只有两类：

\[
(1,0,0,0)^{229}=X,
\qquad
(0,e,0)^{229}.
\tag{16}
\]

第二类由 \(K\) 中 \(228\) 个未改动的 \(g=e\) 位置和
\(P_{12}\) 中另一个 \(g\) 位置组成。\(h\) 的默认实际标签只出现
\(228\) 次；其余实际标签的重数更低。因此该见证不是靠违反
\(p-4\) 重数上界存活。

## 5. 每个端点内部的全部 ρ-零子集

对每个七点 \(H_i\)，程序独立枚举全部 \(2^7\) 个位置子集。除空集
与完整端点外，\(H_2,H_3\) 没有真 \(\rho\)-零子集；\(H_1\) 恰有
一对互补的真零子集：

\[
S=\{P_{23}\text{ 中的 }g,u_f,u_t\},
\tag{17}
\]

\[
C=H_1\setminus S
=\{P_{23}\text{ 中的 }h,z_1,z_2,y\}.
\tag{18}
\]

它们在 (9) 中的轴坐标和与高度和分别是

\[
\begin{array}{c|c|c|c|c}
 &|\cdot|&q\text{-坐标和}&\text{高度和}&
 \text{商零所需 }X\text{ 数}\\ \hline
S&3&1&2&232\\
C&4&-1&1&1.
\end{array}
\tag{19}
\]

因为 \(X\) 只有 \(229\) 个位置，\(S\) 没有纯 \(X\)-核心的商零
闭合。另一方面

\[
X_1\mathbin{\dot\cup}C
\tag{20}
\]

长五，实际和值为 \(a\)，正落在

\[
I_1=[2,6]
\tag{21}
\]

的允许窗中，所以它是一条合法自动诱导 \(F_1\) 短块。三个完整
\(H_i\) 都是长度七、实际和值 \(3a\) 的 \(F_3\) 块。因而全部
非空端点内部 \(\rho\)-零子集的决定精确为

\[
\boxed{
3\times F_3(7),qquad 1\times F_1(5),qquad
1\times\text{无可用 }X\text{ 闭合}.}
\tag{22}
\]

没有任何可用闭合落入长度
\(9,\ldots,2p+2\) 的中间禁区。这里不是抽样：程序逐端点枚举了
所有子集，并对每个 \(\rho\)-零子集唯一计算

\[
c_X=-\sum c_v\pmod p,
\qquad 0\le c_X\le p-4
\tag{23}
\]

是否可取，再施加完整短长度窗。

## 6. 严格停止线

本文证明的是一个真正统一的局部提升见证，而不是为不同端点分别
挑坐标：同一实际位置在所有 \(H_i,Q_i\) 中始终使用 (9) 的同一
标签。它同时保留逐位置补关系、三个最大 \(\rho\)-原子、一阶总和和
实际重数上界。

但量词只覆盖“包含在某一个展示端点中的 \(\rho\)-零子集”。尚未
检查：

1. 不包含在单个 \(H_i\) 中的 \(Y\)-子集所诱导的全部短块；
2. 两条自动短块的不交并长度门；
3. \(P\) 的一个真位置与每个 \(Q_i\) 的 mixed target fibre；
4. Hasse 同余、四边／全部端点补全；
5. 实际 \(Z=X\dot\cup Y\) 的原子性。

特别地，(10) 只证明 packing 的原子型与一阶总和相容，没有检查
第三项中的混合目标。因此最终裁决必须写成

\[
\boxed{
\texttt{FIXED\_MODEL\_D\_ENDPOINT\_INTERNAL\_Q\_LIFT\_SAT /
RELAXED / GLOBAL\_INCOMPLETE}.}
\tag{24}
\]

下一承重层应直接检查全局自动短谱或唯一的 mixed
\(P\)--\(Q_i\) 目标；继续只在三个 \(H_i\) 内增加同类条件不会产生
新矛盾。

## 7. 证书

`unique_tail_p233_doubleton_D_q_lift_attack.py` 不导入旧作者模块。它
重新构造 Model D 的全部真实位置和 \(\rho\)-标签，并核验旧工件的
固定哈希；随后逐位置保存 (9)--(10) 的 lift，重算：

- 三条 \(\rho(Q_i)\) 的 simple 最大原子参数；
- (12)--(13) 的全部一阶总和；
- \(X\dot\cup Y\) 的完整实际标签重数表；
- 三个端点的全部 \(2^7\) 子集及 (19)--(23)；
- 报告的规范 SHA-256 语义证书。

它不把本地 SAT 外推成完整首片 SAT。
