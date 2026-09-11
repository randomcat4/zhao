# \(p=233\) 三长八 \(m=4\) 余三轨的偶四次有限前沿

STATUS: **INCOMPLETE / EXACT FINITE FRONTIER / GLOBAL INCOMPLETE**

## 1. 范围与记号

固定

\[
p=233,\qquad
w_1=e,\quad w_2=f,\quad w_3=-e-f.
\tag{1}
\]

在三个 singleton 均长八且 \(m=4\) 的层中，共同核与三个 fringe
逐位置写成

\[
Q_i=C\mathbin{\dot\cup}F_i,
\qquad |C|=2p-6=460,
\tag{2}
\]

\[
F_i=(U\setminus\{u_i\})\mathbin{\dot\cup}D_i,
\qquad |D_i|=2.
\tag{3}
\]

三个 \(F_i\) 的完整实际和相同。置

\[
\Omega=\sigma(F_i),\qquad
\Delta=\Omega-\sigma(U),\qquad
\delta=\rho(\Delta),\qquad
\tau={\delta\over2}.
\tag{4}
\]

于是

\[
\rho\sigma(D_i)=\delta+w_i=2\tau+w_i.
\tag{5}
\]

每个 \(F_i\) 都是投影原子 \(Q_i\) 的非空真子序列，所以
\(\delta\ne0\)，从而 \(\tau\ne0\)。已经排除的
\(O_0=(0,0,0,5)\) 不再讨论。余下三个无标号轨为

\[
O_1=(0,1,1,4),\qquad
O_2=(1,1,2,3),\qquad
O_3=(2,2,2,2).
\tag{6}
\]

下文所有 \(A_S\) 均表示真实的成员型位置集；不同成员型中的位置
始终按不同字面位置处理，即使它们在 \(C_p^2\) 中投影相同。

## 2. 三个掩码轨的全部非尾 fringe 标签

把

\[
D_i=\{d_i,d_i'\},\qquad
\rho(d_i)=\tau-z_i,qquad
\rho(d_i')=\tau+w_i+z_i
\tag{7}
\]

作为每个二位置 \(D_i\) 的定向参数化。式 (5) 自动成立。交换
\(d_i,d_i'\) 只把

\[
z_i\longmapsto-w_i-z_i
\tag{8}
\]

而不改变相应的字面二位置集。

### 2.1 轨道 \(O_1=(0,1,1,4)\)

此时存在四个不同字面位置

\[
x_1\in A_1,\quad x_2\in A_2,\quad
y_{13}\in A_{13},\quad y_{23}\in A_{23},
\tag{9}
\]

并且

\[
D_1=\{x_2,y_{23}\},\qquad
D_2=\{x_1,y_{13}\},\qquad
D_3=\{x_1,x_2\}.
\tag{10}
\]

取 \(z=\tau-\rho(x_1)\)。由三个式 (5) 唯一得到

\[
\boxed{
\begin{aligned}
\rho(x_1)&=\tau-z,\\
\rho(x_2)&=\tau+w_3+z,\\
\rho(y_{13})&=\tau+w_2+z,\\
\rho(y_{23})&=\tau+w_1-w_3-z.
\end{aligned}}
\tag{11}
\]

在式 (7) 的参数中，这等价于

\[
\boxed{z_2=z_3=z,\qquad z_1=-w_3-z.}
\tag{12}
\]

### 2.2 轨道 \(O_2=(1,1,2,3)\)

此时有五个不同字面位置

\[
x_1\in A_1,\quad y_{12}\in A_{12},\quad
y_{13}\in A_{13},\quad p,q\in A_{23},\quad p\ne q,
\tag{13}
\]

且

\[
D_1=\{p,q\},\qquad
D_2=\{x_1,y_{13}\},\qquad
D_3=\{x_1,y_{12}\}.
\tag{14}
\]

取 \(z=\tau-\rho(x_1)\)，再用独立参数 \(z_1\) 定向
\(\{p,q\}\)，则

\[
\boxed{
\begin{aligned}
\rho(x_1)&=\tau-z,\\
\rho(y_{13})&=\tau+w_2+z,\\
\rho(y_{12})&=\tau+w_3+z,\\
\rho(p)&=\tau-z_1,\\
\rho(q)&=\tau+w_1+z_1.
\end{aligned}}
\tag{15}
\]

即

\[
\boxed{z_2=z_3=z,\qquad z_1\text{ 自由}.}
\tag{16}
\]

这里 \(p,q\) 是两个不同实际位置；不得从它们同属 \(A_{23}\)
推出 \(\rho(p)=\rho(q)\)。

### 2.3 轨道 \(O_3=(2,2,2,2)\)

三个 \(D_i\) 两两字面不交，分别是 \(A_{23},A_{13},A_{12}\)
中的二位置集。三个参数 \(z_1,z_2,z_3\) 相互独立，并且

\[
\boxed{
\begin{aligned}
\rho(D_1)&=\{\tau-z_1,\ \tau+w_1+z_1\},\\
\rho(D_2)&=\{\tau-z_2,\ \tau+w_2+z_2\},\\
\rho(D_3)&=\{\tau-z_3,\ \tau+w_3+z_3\}.
\end{aligned}}
\tag{17}
\]

式 (17) 描述六个不同字面位置，但没有假定其六个投影标签两两不同。

## 3. 共同核的偶四次式

定义

\[
\Psi_C=\prod_{c\in C}(1-X^{\rho\sigma(c)})
=\sum_{g\in C_p^2}c(g)X^g.
\tag{18}
\]

由 \(|C|=2p-6\)，系数函数 \(c\) 是总次数至多四的多项式函数。
又因

\[
\rho\sigma(C)=-\delta=-2\tau,
\tag{19}
\]

且 \(|C|\) 为偶数，补集反射给

\[
c(g)=c(-2\tau-g).
\tag{20}
\]

置

\[
q(z)=c(z-\tau).
\tag{21}
\]

则 \(q(-z)=q(z)\)，所以

\[
q\in\mathcal E_4
=\langle1,x^2,xy,y^2,x^4,x^3y,x^2y^2,xy^3,y^4\rangle.
\tag{22}
\]

空集给

\[
\boxed{q(\tau)=1.}
\tag{23}
\]

由偶性也有 \(q(-\tau)=1\)，它对应每个 fringe 的完整子集。

## 4. 原子性给出的完整 quartic 零点

固定 \(\{i,j,k\}=\{1,2,3\}\)。在式 (7) 下，

\[
F_i=\{w_j,w_k,\tau-z_i,\tau+w_i+z_i\}
\tag{24}
\]

是四个字面位置组成的投影序列，总和为 \(2\tau\)。若
\(\varnothing\ne A\subsetneq F_i\)，则不存在 \(E\subseteq C\)
使

\[
\rho\sigma(E)=-\rho\sigma(A),
\tag{25}
\]

否则 \(E\dot\cup A\) 会成为 \(Q_i\) 的非空真投影零和子序列。
因此先有普通无表示，再有

\[
q(\tau-\rho\sigma(A))=0.
\tag{26}
\]

对子集与其补集配对，并使用 \(q\) 的偶性，每个 \(F_i\) 恰给下面
七个可能带重合的评价零点：

\[
\boxed{
\begin{aligned}
q(\tau-w_j)&=q(\tau-w_k)=q(\tau+w_i)=0,\\
q(z_i)&=q(z_i+w_i)=q(z_i-w_j)=q(z_i-w_k)=0.
\end{aligned}}
\tag{27}
\]

前三点分别来自两个尾 singleton 与尾对；后四点分别来自一个
\(D_i\) singleton 及两个 tail--\(D_i\) cross pair。其余非空真
子集由补集给出同一个偶评价点，所以 (27) 已穷尽式 (26)，没有漏掉
字面子集。

三个端点合起来，第一行正好给统一六点

\[
\boxed{
q(\tau\pm w_1)=q(\tau\pm w_2)=q(\tau\pm w_3)=0.}
\tag{28}
\]

第二行记为

\[
Z_i(z_i)=\{z_i,z_i+w_i,z_i-w_j,z_i-w_k\}.
\tag{29}
\]

于是三个轨的 quartic 原子性系统统一为

\[
q|_{\{\tau\pm w_1,\tau\pm w_2,\tau\pm w_3\}
\cup Z_1(z_1)\cup Z_2(z_2)\cup Z_3(z_3)}=0,
\qquad q(\tau)=1,
\tag{30}
\]

再分别加入 (12)、(16) 或 (17) 的 incidence 关系。

式 (30) 中若不同字面子集给出相同评价点，只合并线性评价条件，不
合并原来的实际位置。若某个零点恰等于 \(\tau\) 或 \(-\tau\)，则
它与 (23) 直接矛盾。

## 5. 第一个精确可证伪门：评价矩阵

按式 (22) 的九个基函数，把 (30) 的不同零点评价行组成矩阵
\(M_{\mathrm{atom}}\)，并把 \(\tau\) 的评价行记为
\(L_\tau\)。固定 \(\tau,z_i\) 后，存在满足原子性条件的 \(q\)
当且仅当线性系统

\[
M_{\mathrm{atom}}\mathbf q=0,
\qquad L_\tau\mathbf q=1
\tag{31}
\]

在 \(\mathbb F_{233}\) 上可解。等价地，必须有

\[
\boxed{
\operatorname{rank}
\begin{pmatrix}M_{\mathrm{atom}}\\L_\tau\end{pmatrix}
=\operatorname{rank}(M_{\mathrm{atom}})+1.}
\tag{32}
\]

特别地，\(M_{\mathrm{atom}}\) 满秩九，或 \(L_\tau\) 已在其行空间
中，都会严格排除该参数。式 (32) 是下一核验器应最先执行的门；它
只使用原子性普通无表示和有限域线性代数。

## 6. mixed 纤维恢复

现在固定 461-completion 定理标记出的 pointed endpoint \(i\)，其
非尾位置序列为

\[
N_i=C\mathbin{\dot\cup}D_i.
\tag{33}
\]

取实际 admissible packing 方向

\[
s\ne0,
\qquad s\notin\{\pm w_1,\pm w_2,\pm w_3\},
\tag{34}
\]

以及 \(\varepsilon\in\{+,-\}\) 和字面位置 \(d\in D_i\)。置

\[
h_{\varepsilon,d}=\varepsilon s-\rho(d),
\qquad
A_{\varepsilon,d}=\nu_{h_{\varepsilon,d}}(C).
\tag{35}
\]

任意 \(F\subseteq C\) 若和为 \(h_{\varepsilon,d}\)，则
\(F\dot\cup\{d\}\subseteq N_i\) 是目标 \(\varepsilon s\) 的
tail-free 表示。已证 separator 对每个这样的表示给

\[
1+|F|\le2.
\tag{36}
\]

故 \(h_{\varepsilon,d}\ne0\) 时只有 singleton 贡献；当
\(h_{\varepsilon,d}=0\) 时，\(C\) 的投影零和自由性说明只有空集。
结合 \(c(h)=q(\tau+h)\)，得到精确恢复式

\[
\boxed{
A_{\varepsilon,d}
\equiv-q(\tau+\varepsilon s-\rho(d))
+\mathbf1_{\varepsilon s=\rho(d)}
\pmod {233}.}
\tag{37}
\]

当 \(A_{\varepsilon,d}>0\) 时，每个相应的 \(C\)-位置与字面位置
\(d\) 组成一个 mixed 双点表示。高度表逐表示把该 \(C\)-纤维的
全部位置锁定到同一个完整实际标签。实际值最大重数 \(p-4\) 因而给

\[
\boxed{0\le A_{\varepsilon,d}\le229.}
\tag{38}
\]

式 (37) 的最小非负剩余类为 230、231 或 232 时严格不可实现。

不同的 \((\varepsilon,d)\) 可能给同一个投影标签 \(h\)。这时它们
引用同一个 \(C\)-纤维，容量只能计算一次，并且若该纤维非空，各次
height 恢复得到的完整实际标签还必须一致。因此必要条件为

\[
\boxed{
\sum_{h\ {\rm distinct}}\nu_h(C)\le460.}
\tag{39}
\]

若只运行投影求解器而尚未加载完整标签，可以暂不删除“完整恢复值
不一致”的状态，但必须把它标成放宽幸存者，不能把它称为实际模型。

同样地，强制纤维还必须共同满足 \(C\) 的投影零和自由性：不存在

\[
(k_h)_h\ne0,
\qquad 0\le k_h\le\nu_h(C),
\qquad \sum_hk_hh=0.
\tag{40}
\]

重复标签先合并，零标签的容量必为零；式 (40) 中的全零向量必须显式
排除。

## 7. 共同核短表示与 fringe 纤维的交叉容量门

记

\[
B_\varepsilon=c(\varepsilon s)=q(\tau+\varepsilon s).
\tag{41}
\]

若 \(B_\varepsilon\ne0\)，则 signed 非零严格保证存在
\(E_\varepsilon\subseteq C\) 和为 \(\varepsilon s\)。它在
\(N_i\) 中是 tail-free mixed 表示，所以

\[
1\le|E_\varepsilon|\le2.
\tag{42}
\]

对另一符号 \(-\varepsilon s\)，任取 \(d\in D_i\) 及
\(c\in C\) 满足

\[
\rho(c)=-\varepsilon s-\rho(d),
\tag{43}
\]

都有 fringe 双点表示 \(\{d,c\}\)。正负两个 tail-free 表示族
必须交叉相交，而 \(E_\varepsilon\subseteq C\) 不含 \(d\)，故每个
这样的 \(c\) 都必须属于 \(E_\varepsilon\)。将重复投影标签合并后，
得到新的必要条件

\[
\boxed{
M_{-\varepsilon,i}:=
\sum_{h\ {\rm distinct}\atop
h=-\varepsilon s-\rho(d),\ d\in D_i}
\nu_h(C)\le2.}
\tag{44}
\]

此外，若 \(D_i\) 自身含有 \(-\varepsilon s\) 的 singleton 或二点
表示，它与 \(E_\varepsilon\) 字面不交，也会直接违反交叉相交。因此

\[
\boxed{
\rho(d)\ne-\varepsilon s\quad(d\in D_i),
\qquad
\rho(D_i)=2\tau+w_i\ne-\varepsilon s.}
\tag{45}
\]

若 (44) 等号成立，则 \(E_\varepsilon\) 恰由这些被迫位置组成，
还必须逐坐标满足

\[
\boxed{
\sum_{h} \nu_h(C)h=\varepsilon s,}
\tag{46}
\]

其中求和只取式 (44) 中的 distinct 强制纤维。若左侧容量为一，则
唯一被迫标签要么本身等于 \(\varepsilon s\)，要么
\(E_\varepsilon\) 还必须含一个投影标签为
\(\varepsilon s-h\) 的额外 \(C\)-位置。

式 (44)--(46) 只在 \(B_\varepsilon\ne0\) 时使用。若
\(B_\varepsilon=0\)，不得反推 \(C\) 中没有
\(\varepsilon s\)-表示。

## 8. 下一核验器的精确接口

一个不改变本问题量词的有限核验器应按以下顺序运行。

1. 枚举 \(\tau\ne0\)，并按轨道分别枚举
   \(O_1\) 的 \(z\)、\(O_2\) 的 \((z,z_1)\)、\(O_3\) 的
   \((z_1,z_2,z_3)\)。字面位置身份按 (9)、(13)、(17) 保存，
   不因投影标签相同而合并。
2. 由 (28)--(30) 建立九列评价矩阵，先用 (32) 删除原子性不相容
   状态。若零空间维数大于一，必须保留其全部 \(q\)-参数，不能任取
   一个代表替代全称搜索。
3. 对每个仍可能的 \(q\)，枚举全部
   \(233^2-1-6=54,282\) 个 admissible 有向 \(s\)，包括三条尾线
   上除六个尾标签外的 690 个方向。
4. 对 pointed endpoint 的两个字面 \(D_i\)-位置分别应用
   (37)--(38)，再按投影标签合并执行 (39)--(40)。同一投影纤维由
   不同字面 fringe 恢复时，另行记录完整标签一致性义务。
5. 只在 (41) 非零的一侧执行 (44)--(46)，并逐个重验所产生的普通
   表示、字面相交和坐标和值。
6. 对三个可能的 pointing roles 分别计数，再按各掩码轨的稳定子
   去重。有限计算只能排除所枚举的固定 \(p=233\) 状态，不能外推
   到一般 \(p\)。

每次排除至少输出

\[
(O_r,\tau,z_i,\mathbf q,s,i)
\tag{47}
\]

及首先失败的式号；每个幸存者则必须输出完整的评价矩阵秩、\(q\)
参数、恢复纤维、重复标签表和 bounded subset-sum 结果。这样才能
区分“投影放宽幸存”与“真实四维可实现”。

## 9. 当前边界

式 (7)--(17) 已精确解出三个掩码轨的真实字面 incidence 与全部
fringe 投影标签参数；式 (27)--(32) 是共同偶四次的完整原子性有限
系统；式 (37)--(46) 给出 mixed 纤维恢复、实际重数、共同核容量、
bounded 零和自由和短表示交叉容量门。

当前尚未对式 (31) 的全部有限参数作穷尽，也没有证明
\(O_1,O_2,O_3\) 中任何一个轨道或 pointed role 为空。因此本稿状态
严格为 **INCOMPLETE**。最小剩余缺口是：先完成式 (32) 的全部
rank-stratified 解集，再在每个非空 \(q\)-族上执行
(37)--(46)。在此之前，随机秩探针、单个 \(q\) 代表或 signed 零值
都没有排除效力。

本稿不声称关闭 \(m=4\)、固定 \(p=233\) 或全局 \(A_p\)。
