# \(p=233\) 三长八 \(m=4\) 的 \(O_0\) 偶四次排除

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. \(m=4\) 的四个掩码轨道

沿三 singleton 掩码压缩记

\[
(a,b,c,d)=(n_{12},n_{13},n_{23},n_{123}),
\qquad
|C_\triangle|=450+a+b+c+2d.
\tag{1}
\]

\(m=|F_i|=4\) 等价于

\[
|C_\triangle|=460=2p-6,
\qquad
a+b+c+2d=10.
\tag{2}
\]

连同

\[
n_1=6-a-b-d,\quad
n_2=6-a-c-d,\quad
n_3=6-b-c-d\ge0,
\tag{3}
\]

及 \(a+d,b+d,c+d\le5\)，四整数枚举给八个带标号态、四个
\(S_3\) 轨道：

\[
\boxed{
O_0=(0,0,0,5),\quad
O_1=(0,1,1,4),\quad
O_2=(1,1,2,3),\quad
O_3=(2,2,2,2).
}
\tag{4}
\]

其 singleton-cell 重数依次可取

\[
(1,1,1),\quad(1,1,0),\quad(1,0,0),\quad(0,0,0).
\tag{5}
\]

令 \(D_i=F_i\setminus U\)。逐位置有

\[
\begin{aligned}
D_1&=A_2\mathbin{\dot\cup}A_3\mathbin{\dot\cup}A_{23},\\
D_2&=A_1\mathbin{\dot\cup}A_3\mathbin{\dot\cup}A_{13},\\
D_3&=A_1\mathbin{\dot\cup}A_2\mathbin{\dot\cup}A_{12},
\end{aligned}
\tag{6}
\]

所以 \(|D_i|=2\)，且

\[
F_i=(U\setminus\{u_i\})\mathbin{\dot\cup}D_i.
\tag{7}
\]

若把 461-completion 见证端点规范为 \(i=1\)，稳定子 \(S_2\) 下有
六个 pointed 掩码态；无条件至少 459 个共同核位置与 \(D_1\) 中
至少一个位置的删除 complete。以下排除 \(O_0\) 不使用这些删点
结论。

## 2. \(O_0\) 的 fringe 标签

反设 \(O_0\) 可实现。此时

\[
A_i=\{x_i\},
\tag{8}
\]

\[
D_1=\{x_2,x_3\},\qquad
D_2=\{x_1,x_3\},\qquad
D_3=\{x_1,x_2\}.
\tag{9}
\]

令

\[
\Omega=\sigma(F_1)=\sigma(F_2)=\sigma(F_3)
\tag{10}
\]

为完整实际群中的等式，置

\[
\Delta=\Omega-\sigma(U),\qquad
\delta=\rho(\Delta),\qquad
t=\delta/2,\qquad
r_i=\rho(\sigma(x_i)).
\tag{11}
\]

写

\[
w_1=e,\qquad w_2=f,\qquad w_3=-e-f.
\tag{12}
\]

三个 fringe 等和式给

\[
r_2+r_3=\delta+w_1,\quad
r_1+r_3=\delta+w_2,\quad
r_1+r_2=\delta+w_3.
\tag{13}
\]

相加减得到

\[
\boxed{r_i=t-w_i\qquad(i=1,2,3).}
\tag{14}
\]

又 \(F_i\) 是投影原子 \(Q_i\) 的非空真子序列，所以
\(\delta=\rho(\sigma(F_i))\ne0\)，从而 \(t\ne0\)。

## 3. 共同核给出中心偶四次式

写 \(C=C_\triangle\)、\(G=C_p^2\)，并定义

\[
\Psi_C
=\prod_{z\in C}(1-X^{\rho(\sigma(z))})
=\sum_{g\in G}c(g)X^g.
\tag{15}
\]

取尾基 \(e,f\)，令 \(u=1-X^e,\ v=1-X^f\)。因
\(|C|=2p-6\)，\(\Psi_C\in I^{2p-6}\)，它是

\[
u^{p-1-a}v^{p-1-b},
\qquad a,b\ge0,\quad a+b\le4
\tag{16}
\]

的线性组合。恒等式

\[
(-1)^x\binom{p-1-a}{x}=\binom{x+a}{a}\pmod p
\tag{17}
\]

说明 \(c(xe+yf)\) 是总次数至多四的多项式。

另一方面，\(\rho(\sigma(C))=-\delta\)，且 \(|C|\) 为偶数。对子集
取补给出

\[
c(g)=c(-\delta-g).
\tag{18}
\]

定义

\[
q(z)=c(z-t).
\tag{19}
\]

则 \(q(-z)=q(z)\)。因每变量次数小于 \(p\)，函数恒等式唯一提升为
多项式恒等式，所以 \(q\) 属于九维偶四次空间

\[
\mathcal E_4=
\langle
1,x^2,xy,y^2,x^4,x^3y,x^2y^2,xy^3,y^4
\rangle.
\tag{20}
\]

## 4. 原子性先给普通无表示，再给系数零

固定 \(i\) 及字面子集 \(A\subseteq F_i\)。若有 \(E\subseteq C\)
满足

\[
\rho(\sigma(E))=-\rho(\sigma(A)),
\tag{21}
\]

则 \(E\dot\cup A\) 是 \(\rho(Q_i)\) 的零和字面子序列。原子性说明
只可能是

\[
(E,A)=(\varnothing,\varnothing)
\quad\text{或}\quad
(E,A)=(C,F_i).
\tag{22}
\]

因此

\[
q(t-\rho(\sigma(A)))=
\begin{cases}
1,&A=\varnothing\text{ 或 }F_i,\\
0,&\varnothing\ne A\subsetneq F_i.
\end{cases}
\tag{23}
\]

中间值为零是因为对应普通位置子集根本不存在，不是把带符号系数零
反推成无表示；当 \(A=F_i\) 时唯一的 \(E=C\) 因 \(|C|\) 为偶贡献
\(+1\)。

在 \(O_0\) 中，(23) 逐字面给出

\[
\begin{array}{c|l}
\text{零点}&\text{可取的 }A\\ \hline
0&\{u_i,x_i\}\text{，取一个同时含二者的 }F_j\\
w_i&\{x_i\}\\
w_i-w_j&\{u_j,x_i\}\text{，取同时含二者的第三个 fringe}\\
t-w_i&\{u_i\}\\
t+w_i&F_i\text{ 中的尾对 }\{u_j,u_k\}.
\end{array}
\tag{24}
\]

另外空集给

\[
q(t)=1.
\tag{25}
\]

## 5. 七个固定零点只余二维

先取与 \(t\) 无关的七个零点

\[
0,\quad w_1,w_2,w_3,\quad
w_1-w_2,\ w_1-w_3,\ w_2-w_3.
\tag{26}
\]

它们在 (20) 上的评价矩阵秩为七；例如列

\[
1,x^2,xy,y^2,x^4,x^2y^2,xy^3
\tag{27}
\]

组成的 \(7\times7\) 子式为 \(144\not\equiv0\pmod{233}\)。
直接消元得到零空间的一组基

\[
q_1(x,y)
=\frac12x^2-xy-\frac12x^4+x^3y,
\tag{28}
\]

\[
q_2(x,y)
=2xy-y^2-2xy^3+y^4.
\tag{29}
\]

所以

\[
q=Aq_1+Bq_2.
\tag{30}
\]

## 6. 全部非零中心都与 \(q(t)=1\) 冲突

余下六个普通零点要求

\[
Aq_1(t\pm w_i)+Bq_2(t\pm w_i)=0
\qquad(i=1,2,3).
\tag{31}
\]

对 \(t=(x,y)\in\mathbb F_{233}^2\setminus\{0\}\) 作精确二列秩
分类：

- 若 \(xy(x-y)\ne0\)，共有
  \((p-1)(p-2)=53\,592\) 个 \(t\)，(31) 的六行秩为二，故
  \(A=B=0\)；
- 若 \(x=0\)、\(y=0\) 或 \(x=y\)，共有
  \(3(p-1)=696\) 个非零 \(t\)，六行秩为一，但该一维核中的每个
  \(Aq_1+Bq_2\) 仍满足
  \[
  Aq_1(t)+Bq_2(t)=0.
  \tag{32}
  \]

两类都强迫 \(q(t)=0\)，与 (25) 矛盾。因此

\[
\boxed{O_0=(0,0,0,5)\text{ 不可实现}.}
\tag{33}
\]

## 7. 作用域与余下三轨道

\(O_0\) 是原 73 个 singleton 掩码轨道中的恰一个，也是 \(m=4\)
层四轨道中的一个。排除后粗状态严格从 73 降到 72，\(m=4\) 层从
4 降到 3。若把 180 个 outer rows 与 singleton 状态作笛卡尔放宽，
则删去 180 个 row-state cells；每行仍有 \(O_1,O_2,O_3\)，所以
没有一条 outer row 被本引理单独关闭。

证明只在 (10) 调用完整实际等和；矛盾本体只用其投影后果、真实位置
incidence 与三个投影原子，不用 461-completion、统一 \(q\)-高度或
自动短谱。

余下三轨道分别有四、五、六个字面非尾 fringe 位置标签，可与同一个
九系数偶四次式建立有限系统；随机探针没有证明效力。下一步须接入 actual
\(q\)/高度、自动短块或 461 表示的 mandatory-overlap 门。剩余
180 行和全局 \(A_p\) 仍为 **INCOMPLETE**。
