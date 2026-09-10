# \(p=233\) 三长八 \(m=3\) 的三次核—端点差与 fringe 交换

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
TWO EARLIER OVERCLAIMS REJECTED / GLOBAL INCOMPLETE**

## 1. 三张二次签名来自同一个三次核

在唯一的 \(m=3\) singleton 掩码态中，已有逐位置分解

\[
Q_i=C\mathbin{\dot\cup}\{u_j,u_k,v_i\},
\qquad |C|=2p-5,
\tag{1}
\]

其中

\[
w_1=e,\qquad w_2=f,\qquad w_3=-e-f,
\qquad \rho(v_i)=w_i+\delta.
\tag{2}
\]

三次核曲线定理已经证明

\[
\delta=\alpha e+\beta f,
\qquad \alpha^2-\alpha\beta+\beta^2=3,
\tag{3}
\]

并且共同核的带符号系数函数严格为

\[
\begin{aligned}
c_\delta(x,y)={}&1-x^2+xy-y^2\\
&+F(x^3-x)+I(y^3-y)+G(x^2y-xy^2),
\end{aligned}
\tag{4}
\]

\[
G=(\alpha-\beta)^{-1},\qquad
F={-2-G\beta\over3\alpha},\qquad
I={-2+G\alpha\over3\beta}.
\tag{5}
\]

删去 \(Q_i\) 中的两个尾位置后，剩余的实际位置序列是

\[
N_i=C\mathbin{\dot\cup}\{v_i\}.
\tag{6}
\]

所以它的带符号系数函数由同一个 \(c_\delta\) 唯一决定：

\[
\boxed{
n_i(r)=c_\delta(r)-c_\delta(r-w_i-\delta).
}
\tag{7}
\]

式 (7) 是生成积
\(\Psi_{N_i}=\Psi_C(1-X^{w_i+\delta})\) 的逐目标系数恒等式。

式 (4) 的有限差分总次数至多二。分别在 \(Q_i\) 所含的两个尾标签基

\[
(w_2,w_3),\qquad(w_1,w_3),\qquad(w_1,w_2)
\tag{8}
\]

中书写，每个 \(n_i\) 恰属于已经审计的规范族

\[
C_{A,B}(u,v)
=1-(u-v)^2+A u(u+1)+B v(v+1).
\tag{9}
\]

## 2. packing 方向的完整作用域

令 packing 方向为 \(s=xe+yf\)。既有六尾排除严格只给

\[
s\ne0,\qquad
s\notin\{\pm e,\pm f,\pm(-e-f)\}.
\tag{10}
\]

它不排除三条尾方向上的其他标量倍数。故每个曲线点必须检查的实际
admissible 有向方向数为

\[
p^2-1-6=54\,282.
\tag{11}
\]

其中

\[
\begin{aligned}
x,y,x-y\ne0 &: 53\,592,\\
x y(x-y)=0\text{ 但满足 (10)} &:3(p-3)=690.
\end{aligned}
\tag{12}
\]

初稿曾错误地从六尾排除推出 \(x,y,x-y\ne0\)，遗漏了第二行的 690
个方向；第一次修订的独立审计已否决该作用域。本文的有限普查包含
(11) 的全部方向。

作为较弱但有用的交叉核验，对每个 \(i\)，

\[
\ell_i(s):={n_i(s)-n_i(-s)\over2}
\tag{13}
\]

是关于 \((x,y)\) 的齐次线性式。核验器在曲线 (3) 的全部 234 点
上直接构造三行二列奇部矩阵，并得到

\[
\boxed{\operatorname{rank}L_\delta=2
\quad\hbox{对全部 234 个 }\delta.}
\tag{14}
\]

所以任意非零 \(s\) 都有某个 \(i\) 满足
\(n_i(s)\ne n_i(-s)\)，特别地 simultaneous-six-zero 条件子支为空。
这里不把该条件子支误写成所有 outer rows 的全称条件。

## 3. 跨端点系数差看见 fringe-touching 二点表示

固定一个实际 packing 目标

\[
r\in\{s,-s\}.
\tag{15}
\]

mixed 核分离器证明：\(N_i\) 中和为 \(r\) 的每个普通位置表示都
至多含两个位置。记

\[
\begin{aligned}
S_C(r)&=\nu_r(C),\\
D_C(r)&=\#\{\{c,c'\}\subset C:\rho(c)+\rho(c')=r\},\\
A_i(r)&=\nu_{r-w_i-\delta}(C),\\
\varepsilon_i(r)&=\mathbf1_{w_i+\delta=r}.
\end{aligned}
\tag{16}
\]

这里 \(A_i(r)\) 精确计数所有包含 fringe 位置 \(v_i\) 的二点表示
\(\{v_i,c\}\)。因为 \(r\ne0\)，空集没有贡献；所有表示至多二点，
故 signed 系数在 \(\mathbb F_{233}\) 中严格满足

\[
\boxed{
n_i(r)=D_C(r)-S_C(r)+A_i(r)-\varepsilon_i(r).
}
\tag{17}
\]

共同核内部的单点、二点贡献与端点 \(i\) 无关。于是

\[
n_i(r)-n_k(r)
=A_i(r)-A_k(r)-\varepsilon_i(r)+\varepsilon_k(r).
\tag{18}
\]

若 \(A_i(r)=A_k(r)=0\)，右端必属于 \(\{0,\pm1\}\)。取逆否得到

\[
\boxed{
n_i(r)-n_k(r)\notin\{0,\pm1\}
\Longrightarrow
A_i(r)+A_k(r)>0.
}
\tag{19}
\]

这一步只在式 (15) 的两个 mixed 目标上使用至多二点定理，没有对
任意其他非零目标作无依据外推，也没有把 signed 零解释成普通表示空。

式 (19) 右侧给出一个真实 fringe-touching 二点表示

\[
E=\{v_i,c\}\subset N_i,qquad \rho(\sigma(E))=r.
\tag{20}
\]

既有 mixed 高度表逐个二点表示给出完整四维等式

\[
\boxed{|E|=2,qquad \sigma(E)=\sigma(z_r^\ast),}
\tag{21}
\]

其中 \(z_r^\ast\) 是与目标 \(r\) 配对的另一个 packing 实际位置。
因此 (19) 直接强制一条触碰 \(v_i\) 的真实 \(2\leftrightarrow1\)
交换，不需要先证明正负两侧表示族都非空。

## 4. \(p=233\) 的完整端点差普查

方程 (3) 在 \(\mathbb F_{233}^2\) 中恰有 234 点，且每一点都满足
\(\alpha\beta(\alpha-\beta)\ne0\)，所以 (5) 全部有定义。对每个
曲线点及 (10) 的每个 admissible 方向，核验器直接计算六个
\(n_i(\pm s)\)，并检查六个跨端点差

\[
n_i(r)-n_k(r),qquad r\in\{s,-s\},\quad 1\le i<k\le3.
\tag{22}
\]

全部

\[
234\cdot54\,282=12\,701\,988
\tag{23}
\]

个有向形式对中，每一对至少有一个式 (22) 不属于
\(\{0,\pm1\}\)。每对的六个差中，“坏差”的个数分布为

\[
\begin{array}{c|rrrrr}
\text{坏差数}&2&3&4&5&6\\ \hline
\text{形式对数}&132&4\,236&20\,688&929\,628&11\,747\,304.
\end{array}
\tag{24}
\]

特别地，坏差数从不为零或一。把 (24) 接到 (19)--(21)，得到本轮
严格候选结论：

\[
\boxed{
\text{每个实际 admissible }(\delta,s)
\Longrightarrow
\text{至少一条 fringe-touching 的真实 }2\leftrightarrow1\text{ 交换}.}
\tag{25}
\]

## 5. 裁决与下一承重点

初稿错误地把 simultaneous-six-zero 当成全称必要条件并宣称
\(m=3\) 层为空；第一次修订又把六尾排除错误扩大到避开三条尾方向。
两次独立审计都已判 **CRITICAL_GAPS**，相应过强结论在本文中明确
撤回。它们不影响 (17)--(25) 的端点差证明；修复稿的新量词和完整
54,282 方向现已由独立实现复算并判 **CORRECT**。

式 (25) 比“存在某个任意交换”更强：交换二点必含一个已知 fringe
位置。交换后可写出新的长 \(2p-3=463\) 投影原子

\[
Q'_i=(C\setminus\{c\})
\mathbin{\dot\cup}\{u_j,u_k,z_r^\ast\},
\tag{26}
\]

它与另外两个 \(Q_k\) 仍共享 461 个字面位置。下一承重点是把这张
强共享图与 complete-deletion、fringe 完整等和及自动短块联立，
迫使第二条兼容交换或重数矛盾。

本文没有排除 \(m=3\) 掩码态，没有删除任何 outer row，也不证明
固定 \(p=233\) 或全局 \(A_p\)。
