# (p=233) 的 Property B 混合迹统一标签放宽模型

STATUS: **THREE EXPLICIT UNIFIED (C_{233}^2) RELAXED SAT MODELS /
PROPERTY-B LAYER INSUFFICIENT / EXTERNAL PROPERTY B DEPENDENCY EXPLICIT /
GLOBAL INCOMPLETE**

## 1. 结论

固定

\[
p=233,\qquad e=(1,0),\qquad f=(0,1),\qquad t=-e-f
\tag{1}
\]

以及型 \((3)\)、\(|P|=2\)、\(\kappa=1\) 的 rank--2 尾正规形。
在只保留下列接口时，doubleton 迹上的多个长七端点并不会产生新
矛盾：

1. 一张统一的真实位置表 \(W=K\mathbin{\dot\cup}L\)，\(|W|=472\)；
2. 每个位置只有一个统一 \(C_{233}^2\) 标签；
3. 每个端点 \(H\subseteq L\) 长七、含同一非尾位置、具有规定尾迹，
   且 \(\rho(H)=0\)；
4. \(Q_H=K\mathbin{\dot\cup}(L\setminus H)\) 是长度
   \(2p-1=465\) 的最大零和原子；
5. \(K\) 是所有展示的 \(Q_H\) 的精确字面交，并且零和自由。

本文给出三个显式模型：

\[
\boxed{
\begin{array}{c|c|c|c}
\text{模型}&\text{长七迹}&|K|&|L|\\ \hline
\mathrm N&\{e\},\{e,f\},\{e,t\}&463&9\\
\mathrm C&\{e\},\{f,t\}&462&10\\
\mathrm D&\{f,t\},\{e,t\},\{e,f\}&456&16
\end{array}}
\tag{2}
\]

所以“至多一个 singleton 端点长七”之后，不能只继续联立
Property B 支撑域、固定尾点和共同 \(K\)：

\[
\boxed{
\text{一个 singleton 加 nested/complementary doubleton，乃至三个
doubleton，都在此放宽层可实现。}}
\tag{3}
\]

这些是统一字面位置模型，不是三张私有标签表。不过它们仍然没有
加入 \(q\)-坐标提升、\(P\) 的混合目标、全部自动短块、实际高度、
Hasse 同余及实际长原子 \(Z\)，所以绝不能称为完整首片实例。

## 2. 标准原子的本地核验

下列初等事实用于逐个核验三个模型中的每条 \(Q_H\)。若
\(g,h\) 线性无关，且

\[
A=g^{p-1}\prod_{j=1}^{p}(h+a_jg),
\qquad \sum_{j=1}^{p}a_j=1,
\tag{4}
\]

则 \(A\) 是长度 \(2p-1\) 的最小零和序列。事实上，模
\(\langle g\rangle\) 投影后，一个零和子列所取仿射线项数只能是
零或 \(p\)。前者再迫使不取任何 \(g\)；后者的 \(g\)-坐标为
\(1+k\)，其中 \(0\le k\le p-1\)，故只在 \(k=p-1\) 时为零。

这也说明每个模型的 \(K\) 零和自由：\(K\) 是一条已核验原子的真
字面子序列。

Christian Reiher 的外部定理
[*A Proof of the Theorem According to Which Every Prime Number Possesses
Property B*](https://www.math.uni-rostock.de/math/pub/preprints/preprint/2010/pre10_01.pdf)
说明每个素数上的任意长度 \(2p-1\) 最小零和序列都可归入 (4) 的
simple 标准域。该外部定理用于说明 Property B 攻击的穷尽域；三个
具体见证的正确性只需上一段的本地投影论证，并不反向依赖该外部
定理。

## 3. 模型 N：一个 singleton 与两个 nested doubleton

取最大原子

\[
A=f^{232}t^{232}(-e).
\tag{5}
\]

这是 (4) 中 \(g=f,h=t\) 且仿射线系数为
\(0^{232},1\) 的标准形。令共同核为

\[
K=f^{231}t^{231}(-e),
\qquad |K|=463,
\tag{6}
\]

其中所有幂都表示不同的实际位置。除尾位置
\(u_e,u_f,u_t\) 外，在 \(L\) 中再放两个克隆位置
\(x_f,x_t\)，标签分别为 \(f,t\)，以及四个公共位置

\[
C=\{y,e',e'',c\},
\qquad
(\rho(y),\rho(e'),\rho(e''),\rho(c))=(e,e,e,-3e).
\tag{7}
\]

于是 \(|L|=9\)，并定义

\[
\begin{aligned}
H_s&=\{u_e,x_f,x_t\}\mathbin{\dot\cup}C,\\
H_{ef}&=\{u_e,u_f,x_t\}\mathbin{\dot\cup}C,\\
H_{et}&=\{u_e,u_t,x_f\}\mathbin{\dot\cup}C.
\end{aligned}
\tag{8}
\]

三者都长七、都含 \(y\)，迹依次为
\(\{e\},\{e,f\},\{e,t\}\)，且由
\(e+f+t=0\) 与 \(\sum C=0\) 得 \(\rho(H)=0\)。三个字面补集
分别补回标签对

\[
\{f,t\},\qquad\{t,f\},\qquad\{f,t\},
\tag{9}
\]

所以三条 \(Q_H\) 虽使用不同位置，却都等于多重序列 (5)。此外
\(L=H_s\cup H_{ef}\cup H_{et}\)，故三个 \(Q_H\) 的精确交就是
(6)。

这已经覆盖一个 singleton-​\(h=7\) 与一个或两个 nested
doubleton-​\(h=7\) 的组合。

## 4. 模型 C：complementary singleton--doubleton 对

模型 N 没有覆盖互补迹 \(\{e\}\) 与 \(\{f,t\}\)。对此令

\[
g=t,
\qquad h=t-e,
\tag{10}
\]

并取

\[
\begin{aligned}
Q_s&=g^{232}h^{231}f(h+3g),\\
Q_d&=h^{232}g^{231}e(g+2h).
\end{aligned}
\tag{11}
\]

第一条以 \(g\) 为重基，因 \(f=h-2g\)，其线系数和为
\((-2)+3=1\)。第二条以 \(h\) 为重基，因 \(e=g-h\)，其线系数
和为 \((-1)+2=1\)。所以 (11) 都是 (4) 型最大原子，并共享

\[
K=g^{231}h^{231},
\qquad |K|=462.
\tag{12}
\]

在 \(L\) 中取两个三位置补块

\[
B_s=\{u_t,u_f,x_s\},
\qquad
B_d=\{x_h,u_e,x_d\},
\tag{13}
\]

其中

\[
\rho(x_s)=h+3g,\qquad
\rho(x_h)=h,\qquad
\rho(x_d)=g+2h.
\tag{14}
\]

再取四个公共位置 \(C\)，标签和为 \(6e+4f\)，并令

\[
H_s=B_d\mathbin{\dot\cup}C,
\qquad
H_d=B_s\mathbin{\dot\cup}C.
\tag{15}
\]

这里 \(B_s,B_d\) 的标签和都为 \(-6e-4f\)，故两端点都投影零
和；它们长七、共享 \(C\) 中的非尾位置，尾迹分别为
\(\{e\}\) 与 \(\{f,t\}\)。又

\[
K\mathbin{\dot\cup}B_s=Q_s,
\qquad
K\mathbin{\dot\cup}B_d=Q_d,
\tag{16}
\]

且 \(L=B_s\mathbin{\dot\cup}B_d\mathbin{\dot\cup}C\) 长十。
这给出 complementary singleton--doubleton 的统一标签见证。

## 5. 模型 D：三个 doubleton 同时长七

第三个模型甚至保留了三个 doubleton 端点。置

\[
g=e,\qquad h=2e+f,\qquad z=e+h=3e+f,\qquad
r=5e+f,\qquad y=-8e-3f.
\tag{17}
\]

把 \(472\) 个真实位置按其属于哪几条 \(Q_i\) 分成下表。表中
\(P_{ij}\) 表示只属于 \(Q_i,Q_j\)，\(E_i\) 表示只属于
\(Q_i\)，而 \(O\) 不属于任何 \(Q_i\)。

\[
\begin{array}{c|c|c}
\text{位置胞}&\text{个数}&\text{标签多重集}\\ \hline
K=Q_1\cap Q_2\cap Q_3&456&g^{229}h^{227}\\
P_{13}&4&h^4\\
P_{23}&4&g\,h\,z^2\\
P_{12}&4&g^2 f r\\
E_1&1&u_e:g\\
E_2&1&u_f:f\\
E_3&1&u_t:t\\
O&1&y
\end{array}
\tag{18}
\]

令 \(L\) 为除 \(K\) 外的十六个位置，并定义

\[
\begin{aligned}
H_1&=P_{23}\mathbin{\dot\cup}E_2\mathbin{\dot\cup}E_3
     \mathbin{\dot\cup}O,\\
H_2&=P_{13}\mathbin{\dot\cup}E_1\mathbin{\dot\cup}E_3
     \mathbin{\dot\cup}O,\\
H_3&=P_{12}\mathbin{\dot\cup}E_1\mathbin{\dot\cup}E_2
     \mathbin{\dot\cup}O.
\end{aligned}
\tag{19}
\]

三者长七、共享 \(O\)，尾迹依次为
\(\{f,t\},\{e,t\},\{e,f\}\)。直接求和得到每个端点在加入
\(y\) 前的标签和均为 \(8e+3f\)，所以

\[
\rho(H_1)=\rho(H_2)=\rho(H_3)=0.
\tag{20}
\]

三个补原子也可逐项写成标准形：

- \(Q_1\) 以 \(g=e\) 为重基。其 \(232\) 个重基为
  \(K\) 中的 \(229\) 个 \(g\)、\(P_{12}\) 中两个 \(g\) 与
  \(E_1\)。其余 \(233\) 项都在 \(f+\langle e\rangle\)，系数和
  \(231\cdot2+0+5=467\equiv1\pmod {233}\)。
- \(Q_2\) 同样以 \(g=e\) 为重基。仿射线系数和为
  \(228\cdot2+2\cdot3+0+5+0=467\equiv1\)。
- \(Q_3\) 以 \(h=2e+f\) 为重基。以 \(e\) 为线基点时，
  \(z=e+h\)、\(t=e-h\)，故其 \(233\) 个线项系数和为
  \(2\cdot1+(-1)=1\)。

因此三个 \(Q_i=W\setminus H_i\) 都是最大原子，且共同核正是表
(18) 的 \(K\)，长度 \(456\)。这排除了“第三条 \(Q\) 必有短零和”
作为纯 Property B 层论证：在该模型中第三条 \(Q\) 本身也是原子。

## 6. 第一次真正缺失的约束

三个见证不是完整 exact-slice 实例。配套程序也显式枚举了每个七点
端点内的真 \(\rho\)-零和子集。例如模型 D 的 \(H_1\) 含有

\[
\{P_{23}\text{ 中的 }g, u_f, u_t\},
\qquad g+f+t=e+f-e-f=0.
\tag{21}
\]

在二维投影层，这并不破坏任何 \(Q_H\) 的原子性；但在完整模型中，
它必须与统一 \(q\)-提升、轴系数、自动诱导短块和实际高度同时兼容。
因此下一刀应落在这些真位置子集上，而不是再做一次 Property B
支撑计数。

更精确地，三个模型尚未加入：

1. 两位置 packing \(P\) 及全部 mixed \(P\)--\(Q_H\) 目标；
2. 从 \(C_{233}^2\) 到统一商标签／实际标签的 \(q\)-坐标；
3. 所有自动诱导短零和块及长补原子的内部子集和；
4. 实际高度、重数上界、全部 Hasse 行与实际 \(Z\) 原子性；
5. 补全到某个 720 outer survivor 的全部端点与四条边。

所以本文的严格结论只是

\[
\boxed{
\text{Property B + 固定尾 + 共同核 + 统一字面补原子层不足以继续
删除 doubleton-​}h=7\text{。}}
\tag{22}
\]

这是一条放宽 SAT 边界，不是 fixed-slice SAT，更不是固定
\(p=233\) 或全局 \(A_p\) 的结论。

## 7. 证书

配套脚本
`unique_tail_p233_property_b_mixed_trace_relaxed_models.py` 从逐位置定义
重建三个模型，逐条检查：

- \(W=K\mathbin{\dot\cup}L\)、\(|W|=472\)；
- 端点长度、尾迹、共同位置及 \(\rho(H)=0\)；
- 字面恒等式 \(Q_H=K\mathbin{\dot\cup}(L\setminus H)\)；
- 每条 \(Q_H\) 的完整 simple 参数和系数和 \(1\)；
- \(K=\bigcap_HQ_H\) 与 \(L=\bigcup_HH\)；
- 每个七点端点的全部真 \(\rho\)-零和子集。

报告状态固定为
`UNIFIED_C2332_RELAXED_SAT/PROPERTY_B_LAYER_INSUFFICIENT/GLOBAL_INCOMPLETE`。
