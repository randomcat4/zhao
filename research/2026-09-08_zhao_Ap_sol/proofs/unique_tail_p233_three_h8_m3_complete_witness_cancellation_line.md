# \(p=233\) 三长八 \(m=3\) 完成见证与 cancellation line

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 设置

令 \(p=233\)、\(G=C_p^2\)，并取
\(\{i,j,k\}=\{1,2,3\}\)。沿唯一 \(m=3\) 态写

\[
Q_i=C\mathbin{\dot\cup}\{u_j,u_k,v_i\},
\qquad |C|=2p-5,
\tag{1}
\]

\[
\rho(u_t)=w_t,\qquad
w_1+w_2+w_3=0,\qquad
\rho(v_i)=w_i+\delta.
\tag{2}
\]

任意两个 \(w_t\) 成基，\(Q_i\) 是长 \(2p-2\) 的投影原子。其非尾
位置恰为

\[
N_i=C\mathbin{\dot\cup}\{v_i\},
\qquad |N_i|=2p-4.
\tag{3}
\]

取 461-completion 定理给出的见证端点 \(i\)，则 \(N_i\) 中至多一个
位置 \(z\) 使 \(Q_i\setminus\{z\}\) 不能表示 \(G\) 的某个非零
目标。

## 2. 反设 fringe 点是坏删除

反设 \(v_i\) 不 complete，并令

\[
B_i=Q_i\setminus\{v_i\}
=C\mathbin{\dot\cup}\{u_j,u_k\}.
\tag{4}
\]

\(B_i\) 长 \(2p-3\) 且零和自由。近最大原子的完成二分给出一组基
\((g,h_0)\)，使

\[
\operatorname{supp}\rho(B_i)
\subseteq \{g\}\cup(h_0+\langle g\rangle),
\qquad
m:=\nu_g(B_i)\ge p-3.
\tag{5}
\]

零和自由又给 \(m\le p-1\)，故

\[
m\in\{p-3,p-2,p-1\},
\qquad
n:=2p-3-m\in\{p,p-1,p-2\}.
\tag{6}
\]

由于 \(v_i\) 已占至多一个坏删除，反设还强迫每个 \(x\in C\) 的
\(Q_i\setminus\{x\}\) 都 complete。

## 3. 重因子对三次齐次部的限制

设共同核的带符号系数函数为 \(c\)，其齐次三次部为

\[
H_3(xe+yf)
=Fx^3+Iy^3+G(x^2y-xy^2).
\tag{7}
\]

若 \(\nu_g(C)=r\ge p-3\)，则

\[
\boxed{H_3(g)=0.}
\tag{8}
\]

事实上，取群代数坐标
\(u=1-X^g,\ v=1-X^h\)。因
\(\Psi_C=u^rR(u,v)\)，任一存活单项 \(u^av^b\) 都有 \(a\ge r\)。
群基系数函数关于目标的 \(g\)-坐标次数至多
\(p-1-a\le p-1-r\le2\)，所以其三次齐次部在 \(g\) 方向消失。

## 4. 两个尾都在仿射线上

若 \(w_j,w_k\ne g\)，则二者都在
\(h_0+\langle g\rangle\)，所以

\[
g\parallel w_j-w_k,
\qquad
\nu_g(C)=m\ge p-3.
\tag{9}
\]

由尾 \(S_3\) 对称可取

\[
(w_i,w_j,w_k)=(e,f,-e-f).
\tag{10}
\]

于是 \(g\parallel e+2f\)，(8) 给

\[
H_3(e+2f)=F+8I-2G=0.
\tag{11}
\]

在已证核曲线

\[
\alpha^2-\alpha\beta+\beta^2=3
\tag{12}
\]

及其式 (11) 的 \(F,I,G\) 参数下，

\[
H_3(e+2f)
=\frac{\beta^2+8\alpha\beta-8\alpha^2}
{3\alpha\beta(\alpha-\beta)}.
\tag{13}
\]

分母非零。令 \(t=\alpha/\beta\)，分子为零将给
\(8t^2-8t-1=0\)，其判别式为
\(96=16\cdot6\)。但

\[
\left(\frac6{233}\right)
=\left(\frac2{233}\right)\left(\frac3{233}\right)
=1\cdot(-1)=-1,
\tag{14}
\]

故 (13) 不可能为零。此支为空。

## 5. 一个尾等于重项

至多一个尾能等于 \(g\)。不妨 \(g=w_j\)，并把另一尾取为
\(h=w_k\)。仍用 (10)，再取 \(g=f,\ h=-e-f\)。若
\(\delta=\alpha e+\beta f\)，因 \(e=-g-h\)，

\[
\delta=(\beta-\alpha)g-\alpha h.
\tag{15}
\]

写 \(A=\beta-\alpha,\ B=-\alpha\)。由
\(\rho(\sigma(v_i))=(A-1)g+(B-1)h\) 及
\(\rho(\sigma(B_i))=-\rho(\sigma(v_i))\)，比较 \(h\)-坐标得到

\[
n\equiv1-B=1+\alpha\pmod p.
\tag{16}
\]

现在逐一处理 (6)。

### 5.1 \(m=p-1\)

此时 \(n=p-2\equiv-2\)，故 (16) 给 \(\alpha=-3\)。
又 \(\nu_g(C)=m-1\ge p-3\)，所以
\(H_3(f)=I=0\)。曲线与核参数式给

\[
I=0
\quad\Longleftrightarrow\quad
(\alpha,\beta)\in\{(2,1),(-2,-1)\},
\tag{17}
\]

与 \(\alpha=-3\) 不相容。

### 5.2 \(m=p-2\)

此时 \(n=p-1\equiv-1\)，故 \(\alpha=-2\)。同理由 \(I=0\)，
(17) 只余

\[
(\alpha,\beta)=(-2,-1),
\qquad
\delta=w_k-w_i,
\qquad
v_i=w_k=h.
\tag{18}
\]

### 5.3 \(m=p-3\)

此时 \(n=p\equiv0\)，故 \(\alpha=-1\)。曲线给

\[
\beta\in\{1,-2\}.
\tag{19}
\]

把 \(p\) 个线位置写成 \(h+a_tg\)，并记
\(S=\sum_ta_t\)。若 \(S\notin\{1,2\}\)，则取全部 \(p\) 个线
位置，再取唯一满足
\[
r\equiv-S\pmod p,\qquad 0\le r\le p-3
\tag{20}
\]
的 \(g\)-位置，便得到非空零和，违背 \(B_i\) 零和自由。因此
\(S\in\{1,2\}\)。另一方面总和比较给
\[
S=3-\beta.
\tag{21}
\]

\(\beta=-2\) 会给 \(S=5\)，故只余

\[
\beta=1,\qquad S=2,\qquad
\delta=w_j-w_i,\qquad v_i=w_j=g.
\tag{22}
\]

交换 \(j,k\) 给出完全对称的另外两支。所有幸存可能因而只有

\[
\begin{array}{c|c|c}
m&\delta&v_i\\ \hline
p-3&w_j-w_i&w_j\\
p-2&w_k-w_i&w_k.
\end{array}
\tag{23}
\]

## 6. 两个残支统一成同一个标准原子

在 (23) 的两支中，\(Q_i\) 都严格写成

\[
Q_i
=g^{p-2}\prod_{t=1}^{p}(h+a_tg).
\tag{24}
\]

由 \(\sigma(Q_i)=0\)，

\[
\sum_{t=1}^{p}a_t=2.
\tag{25}
\]

第一支的 \(C\) 含 \(p-4\) 个 \(g\)-位置和 \(p-1\) 个线位置；
第二支含 \(p-3\) 个 \(g\)-位置和 \(p-2\) 个线位置。

任取 (24) 的线位置 \(z=h+a_0g\)。删去它后只余 \(p-1\) 个线
位置及 \(p-2\) 个 \(g\)-位置。考虑目标

\[
\tau=(1-a_0)g-h.
\tag{26}
\]

其 \(h\)-坐标为 \(-1\)，所以任何表示都必须取全部 \(p-1\) 个
剩余线位置；它们的 \(g\)-坐标和为 \(2-a_0\)。再取
\(0\le r\le p-2\) 个 \(g\)-位置只能得到

\[
2-a_0+r,
\tag{27}
\]

而 \(1-a_0\) 需要 \(r=p-1\)，不可用。因此每个线位置删除都不
complete。可是两个残支的 \(C\) 分别含 \(p-1\) 或 \(p-2\) 个线
位置，而反设要求全部 \(x\in C\) 删除 complete，矛盾。

## 7. 完成见证的严格正规形

所以 \(v_i\) 必须 complete。于是

\[
\boxed{B_i=C\mathbin{\dot\cup}\{u_j,u_k\}
\text{ 是 complete 零和自由序列}.}
\tag{28}
\]

唯一可能的坏非尾删除若存在，只能位于 \(C\)；故至少
\(2p-6=460\) 个 \(x\in C\) 还满足

\[
Q_i\setminus\{x\}\text{ complete}.
\tag{29}
\]

若 \(\Sigma_0\) 包含空集和，则 (28) 等价于普通和集式

\[
\boxed{
\Sigma_0(\rho(\sigma(C)))+\{0,w_j,w_k,-w_i\}=G.
}
\tag{30}
\]

对每个 (29) 的位置还有

\[
\Sigma_0(\rho(\sigma(C\setminus\{x\})))
+\Sigma_0(\rho(\sigma(\{u_j,u_k,v_i\})))=G.
\tag{31}
\]

## 8. 三个固定 core 目标的逐位置门

对任一满足 (29) 的 \(x\)，在
\(Q_i\setminus\{x\}\) 中表示目标 \(w_i\)。若表示含 \(v_i\) 而
不含尾，其 \(C\)-部分和值必须为 \(-\delta\)，零和自由迫使它是
整个 \(C\)，不能避开 \(x\)。若还含非空尾集 \(T\)，则 \(C\)-部分
的补集将表示

\[
\sigma(T)\in\{w_j,w_k,-w_i\},
\tag{32}
\]

与共同核已证的六个普通禁值矛盾。因此表示不含 \(v_i\)，且必须含
非空尾集。它的 \(C\)-部分和值落在

\[
\boxed{
\mathcal A_i=\{w_i-w_j,\ w_i-w_k,\ 2w_i\}.
}
\tag{33}
\]

故 \(C\) 中和值属于 \(\mathcal A_i\) 的全部普通表示之公共交至多
含唯一坏 \(C\)-位置：

\[
\left|
\bigcap_{\substack{E\subseteq C\\
\rho(\sigma(E))\in\mathcal A_i}}E
\right|\le1.
\tag{34}
\]

这是逐位置的 ordinary-subsum 约束，不是聚合计数。

## 9. 唯一 cancellation line

令

\[
b_i(r)=[X^r]\Psi_{B_i}.
\tag{35}
\]

固定 \(i=1\)，使 \((w_i,w_j,w_k)=(e,f,-e-f)\)。由共同核三次式作
二阶有限差分，

\[
b_i(x,y)
=\Delta_f\Delta_{-e-f}c(x,y)
=1+2(G-3I)y
=1+\frac{2y}{\beta}.
\tag{36}
\]

最后一个等号由核曲线参数式得到。因此 \(b_i\) 的唯一零集为

\[
\boxed{
L_i=-\frac{\delta}{2}+\langle w_i\rangle,
\qquad |L_i|=p=233.
}
\tag{37}
\]

每个非零线外目标的 \(b_i(r)\ne0\) 已自动认证至少一个普通表示；又
\(0\notin L_i\)，所以 (28) 剩余的普通内容恰是：

\[
\boxed{
L_i\subseteq\Sigma(B_i).
}
\tag{38}
\]

这 233 个目标的带符号系数模 \(p\) 全为零，不能从 (36) 恢复普通
存在性。已有长 464 的 \(q\)-一阶矩只控制 \(Q_i\) 上的带符号
\(q\)-汇总，也不能直接替代长 463 序列 \(B_i\) 的 (38)。

## 10. 下一承重点

反设中的近 Property-B 支已经被彻底排除；当前精确缺口不再是
“461 个删点是否 complete”，而是 cancellation line 上 233 个普通
表示如何同时满足 (29)、(34)、统一 \(q\)-高度、三个真实 fringe
等和与全部自动短块。

本文没有排除一个 \(m=3\) 曲线轨道，也没有关闭剩余 180 行。全局
\(A_p\) 仍为 **INCOMPLETE**。
