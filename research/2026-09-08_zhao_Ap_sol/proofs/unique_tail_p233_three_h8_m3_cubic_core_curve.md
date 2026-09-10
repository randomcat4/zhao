# \(p=233\) 三长八 \(m=3\) 态的三次核曲线

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 唯一最高重叠态

取三个长八 singleton 掩码压缩中的唯一 \(m=3\) 状态

\[
(a,b,c,d)=(1,1,1,4).
\tag{1}
\]

写

\[
C=C_\triangle,
\qquad |C|=461=2p-5,
\qquad
Q_i=C\mathbin{\dot\cup}\{u_j,u_k,v_i\}.
\tag{2}
\]

令三个尾投影为

\[
w_1=e,qquad w_2=f,qquad w_3=-e-f.
\tag{3}
\]

fringe 等和给出同一个非零投影平移

\[
\rho(\sigma(v_i))=w_i+\delta,
\qquad
\delta=\alpha e+\beta f,
\qquad
\rho(\sigma(C))=-\delta.
\tag{4}
\]

其中 \(\delta\ne0\) 已由每个 \(Q_i\) 的原子性得到。

## 2. 461 点共同核避开六个尾目标

删去 \(v_i\) 后的序列

\[
B_i=C\mathbin{\dot\cup}\{u_j,u_k\}=Q_i\setminus\{v_i\}
\tag{5}
\]

投影零和自由。特别地，\(C\) 本身零和自由。若 \(C\) 的某个子集和
等于 \(-w_j\)，把它与尾位置 \(u_j\) 合并就在某个 (5) 中产生
零和；若子集和等于 \(w_i\)，把它与
\(u_j,u_k\) 合并，并用 \(w_j+w_k=-w_i\)，同样产生零和。因此

\[
\boxed{\pm e,\ \pm f,\ \pm(e+f)\notin\Sigma(\rho(\sigma(C))).}
\tag{6}
\]

定义带符号系数函数

\[
c(r)=[X^r]\prod_{z\in C}(1-X^{\rho(\sigma(z))}).
\tag{7}
\]

零和自由与 (6) 给

\[
c(0)=1,
\qquad
c(\pm e)=c(\pm f)=c(\pm(e+f))=0.
\tag{8}
\]

## 3. 六零点把三次式压到三个参数

因 \(|C|=2p-5\)，顶层增广理想的系数--多项式对应说明
\(c(xe+yf)\) 是总次数至多三的多项式。对一般三次式在 (8) 的七个
点作直接插值，唯一得到

\[
\boxed{
\begin{aligned}
c(x,y)={}&1-x^2+xy-y^2\\
&+F(x^3-x)+I(y^3-y)+G(x^2y-xy^2)
\end{aligned}}
\tag{9}
\]

其中只余 \(F,I,G\in\mathbb F_p\)。右端三个三次基函数恰在 (8) 的
七点全为零；七个评价条件秩为七，所以 (9) 也穷尽全部解。

## 4. 补集反射强迫非退化二次曲线

由 \(|C|\) 为奇数及 \(\rho(\sigma(C))=-\delta\)，位置补集双射给出
全称恒等式

\[
\boxed{c(-\alpha-x,-\beta-y)=-c(x,y).}
\tag{10}
\]

换言之，(9) 关于中心 \((-\alpha/2,-\beta/2)\) 是奇函数。其 Hessian
在该中心为零，逐项给出

\[
3F\alpha+G\beta=-2,
\qquad
3I\beta-G\alpha=-2,
\qquad
G(\alpha-\beta)=1.
\tag{11}
\]

三式自动排除

\[
\alpha=0,qquad \beta=0,qquad \alpha=\beta.
\tag{12}
\]

所以 \(F,I,G\) 被 \((\alpha,\beta)\) 唯一确定。把 (11) 代回中心
常数项，直接化简为

\[
c(-\alpha/2,-\beta/2)
=\frac{3-(\alpha^2-\alpha\beta+\beta^2)}6.
\tag{13}
\]

中心也必须取零，故得到必要条件

\[
\boxed{\alpha^2-\alpha\beta+\beta^2=3.}
\tag{14}
\]

## 5. \(p=233\) 只余 234 个平移

在 \(\mathbb F_{233}\) 中，\(3\) 与 \(-3\) 都是非平方元。非退化二次
型 \(X^2-XY+Y^2\) 的判别式为 \(-3\)，所以非零水平集 (14) 恰有

\[
p+1=234
\tag{15}
\]

个点。\(3\) 非平方还说明这些点没有一个落在
\(\alpha=0\)、\(\beta=0\) 或 \(\alpha=\beta\) 上，与 (12) 一致。
直接有限域枚举独立复现 234。

对每个曲线点，(11) 唯一给出

\[
G=(\alpha-\beta)^{-1},
\quad
F=\frac{-2-G\beta}{3\alpha},
\quad
I=\frac{-2+G\alpha}{3\beta}.
\tag{16}
\]

因此唯一的 \(m=3\) 掩码态不再需要搜索任意 \(\delta\) 或任意三次
系数轮廓，而只余 234 个完全显式的候选。

## 6. 边界与下一步

式 (14) 是必要条件，不是实际长补原子或 complete-deletion 的构造。
本文没有从三个 \(Q_i\) 的完整顶积三阶差分宣称额外排除；带符号系数
为零也不能解释为普通表示不存在。

下一承重点是对 234 个候选逐一接入至少一枚 \(Q_i\) 的 461 个普通
complete 删除、统一 \(q\)-高度、三个三位置 fringe 的完整实际等和
与全部自动短块。\(m=3\) 状态、剩余 180 行和全局 \(A_p\) 均保持
**INCOMPLETE**。
