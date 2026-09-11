# \(p=233\) 三长八 \(m=4\) 的删点标签容量接口

STATUS: **PROVED REDUCTION / GLOBAL INCOMPLETE**

## 1. 统一设置

固定 \(p=233\)、\(G=C_p^2\)。在三个 singleton 均长八且共同 fringe
参数 \(m=4\) 的任一剩余掩码轨中，写

\[
Q_i=C\mathbin{\dot\cup}F_i,
\qquad |C|=2p-6=460,
\qquad |F_i|=4,
\tag{1}
\]

并有

\[
\rho\sigma(C)=-2\tau,\qquad
\rho\sigma(F_i)=2\tau.
\tag{2}
\]

每个 \(Q_i\) 都是 \(G\) 中的零和原子。本文把任一真实共同核位置
删去后必满足的全部低次条件，压成一个只含十二个线性未知量的接口。

## 2. 删点奇五次空间

任取真实位置 \(x\in C\)，记

\[
g=\rho\sigma(x),\qquad D=C\setminus\{x\},
\qquad
\Psi_D=\sum_{t\in G}d(t)X^t.
\tag{3}
\]

因 \(Q_i\) 是投影原子，\(g\ne0\)。又

\[
|D|=2p-7,\qquad \rho\sigma(D)=-2\tau-g.
\tag{4}
\]

增广理想顶次是 \(2p-2\)，故 \(d\) 是总次数至多五的多项式函数。
对子集取补并使用 \(|D|\) 为奇数，得到

\[
d(t)=-d(-2\tau-g-t).
\tag{5}
\]

因此

\[
R_g(r):=d(r-\tau-g/2)
\tag{6}
\]

属于十二维奇五次空间

\[
\mathcal O_5=
\langle x^ay^b:a+b\in\{1,3,5\}\rangle.
\tag{7}
\]

## 3. 全部 fringe 内部子集行

因为 \(D\) 是 \(Q_i\) 的真子序列，它零和自由，所以

\[
d(0)=1.
\tag{8}
\]

对任意 \(i\) 和任意非空字面子集 \(A\subseteq F_i\)，若存在
\(E\subseteq D\) 满足

\[
\rho\sigma(E)=-\rho\sigma(A),
\tag{9}
\]

则 \(E\dot\cup A\) 是 \(Q_i\) 的非空零和真子序列。即使
\(A=F_i\)，它仍遗漏被删位置 \(x\)。因此先有普通无表示，再有

\[
d(-\rho\sigma(A))=0.
\tag{10}
\]

在奇中心坐标中，式 (8)--(10) 等价于

\[
R_g(\tau+g/2)=1,
\tag{11}
\]

\[
R_g(\tau+g/2-\rho\sigma(A))=0
\quad
(i=1,2,3, \varnothing\ne A\subseteq F_i).
\tag{12}
\]

这是一组关于 \(\mathcal O_5\) 十二个系数的仿射线性方程。

## 4. 可行删点标签集

对固定的三个字面 fringe 定义

\[
\boxed{
\Gamma(F_1,F_2,F_3;\tau)
=\{g\in G\setminus\{0\}:\text{式 (11)--(12) 在 }
\mathcal O_5\text{ 中可解}\}.
}
\tag{13}
\]

任一实际共同核位置的投影标签都属于 \(\Gamma\)，所以

\[
\operatorname{supp}\rho\sigma(C)\subseteq\Gamma.
\tag{14}
\]

此外 \(C\) 本身投影零和自由。固定非零 \(g\) 若在 \(C\) 中出现
至少 \(p\) 次，这 \(p\) 个位置就形成投影零和，矛盾；故

\[
\nu_g(C)\le p-1=232.
\tag{15}
\]

由 \(|C|=460\) 得到严格必要条件

\[
\boxed{
|\Gamma(F_1,F_2,F_3;\tau)|
\ge \left\lceil\frac{2p-6}{p-1}\right\rceil=2.
}
\tag{16}
\]

所以，只要对一个固定 fringe 状态证明 \(|\Gamma|\le1\)，就已经排除
该状态；无需构造或穷尽 460 个真实核位置。

## 5. 该接口自动包含偶四次原子评价

式 (13) 表面上没有先引入共同偶四次 \(q\)，但没有丢掉相应的原子
评价。对任一可行 \(R_g\)，定义

\[
q_g(s)=R_g(s+g/2)-R_g(s-g/2).
\tag{17}
\]

则 \(q_g\) 是偶四次。取 \(A=F_i\)；由
\(\sigma(F_i)=2\tau\)，式 (12) 给

\[
R_g(-\tau+g/2)=0.
\tag{18}
\]

奇性再给 \(R_g(\tau-g/2)=0\)。连同 (11)，

\[
q_g(\tau)=1.
\tag{19}
\]

若 \(\varnothing\ne A\subsetneq F_i\)，令
\(A^c=F_i\setminus A\)。式 (12) 同时用于 \(A,A^c\)，再用奇性，
得到

\[
q_g(\tau-\rho\sigma(A))=0.
\tag{20}

\]

这正是原偶四次接口的全部 fringe 原子零点。故删点标签容量门是对
偶四次评价门的加强，而不是另一个丢失统一原子信息的放宽。

要注意：对不同 \(g\in\Gamma\)，式 (17) 暂时允许得到不同的
\(q_g\)。真实生成积要求它们其实是同一个 \(q\)，所以式 (13) 仍是
安全放宽；这只会多留候选，不会误删实际状态。

## 6. 与 \(O_1\) 闭合及余两轨的关系

在 \(O_1\) 的四个偶四次例外上，共同偶四次已经固定。对该固定
\(q\) 定义更强的标签集

\[
\Gamma_q=
\{g\in\Gamma:\text{可取式 (13) 的解 }R_g
\text{ 使 }\Delta_gR_g=q\}.
\tag{21}
\]

既有穷尽证明得到四个例外均有 \(\Gamma_q=\varnothing\)，从而关闭
整个 \(O_1\)。这里不能把这个结论误写成放宽集合
\(\Gamma\) 本身为空；\(O_1\) 所需的只是每个实际标签都必须属于
固定共同 \(q\) 对应的 \(\Gamma_q\)。

对 \(O_2,O_3\)，式 (13)--(16) 给出下一层的精确有限目标：

1. 先用偶四次评价或对称哈希生成 fringe-compatible 状态；
2. 对每个状态和全部 \(g\ne0\)，只解一个十二列仿射系统；
3. 只需证明每个状态的 \(|\Gamma|\le1\)，不必先重建完整 \(C\)。

这项归约本身尚未证明所有 \(O_2,O_3\) 状态都满足 \(|\Gamma|\le1\)。
固定 \(p=233\) 的 \(m=4\) 层和一般 \(A_p\) 均仍为
**INCOMPLETE**。
