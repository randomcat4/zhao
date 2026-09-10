# \(p=233\) 全长七秩二支的三泛函正规形与共同因子相容模型

STATUS: **PROVED EXACT FRINGE COMPATIBILITY / RELAXED BEYOND THE FRINGE / GLOBAL INCOMPLETE**

## 1. 精确范围与结论

固定型 \((3)\)、\(|P|=2\)、\(\kappa=1\) 的全长七首片，并只看
四边全异迹强制出的三个单点迹端点

\[
H_i\cap U=\{u_i\}\qquad(1\le i\le3).
\tag{1}
\]

已认证的秩一排除允许唯一规范化

\[
w_1=e,\qquad w_2=f,\qquad w_3=-e-f
\tag{2}
\]

于 \(C_{233}^2\)。本文先证明三个顶层线性泛函的唯一正规形，再给出
一套同一张逐位置标签表，精确同时实现这三个泛函以及三对端点的全部
共同字面因子—花瓣分解。结论是

\[
\boxed{
\text{三条 singleton-tail 顶层泛函与共同字面因子本身不矛盾。}}
\tag{3}
\]

这个相容模型没有声称三个长度 \(2p-1\) 的零和序列是原子，也没有
检查全自动短谱、Hasse 行或实际 \(Z\) 原子性；因此它是对指定代数
接口的精确模型，但相对于完整首片仍是放宽模型。

## 2. 三条泛函的唯一正规形

写

\[
C_i=Q_i\setminus\{u_j,u_k\},\qquad \{i,j,k\}=\{1,2,3\}.
\tag{4}
\]

由 singleton-tail 顶层引理，\(|C_i|=2p-3\)，并有线性泛函
\(\lambda_i:C_p^2\to\mathbb F_p\) 满足

\[
\Psi_{C_i}(1-X^w)=\lambda_i(w)J_G,
\qquad
\lambda_i(w_j)=\lambda_i(w_k)=1.
\tag{5}
\]

把 (2) 代入 (5)，线性性立即唯一给出

\[
\begin{array}{c|ccc}
 &w_1&w_2&w_3\\ \hline
\lambda_1&-2&1&1\\
\lambda_2&1&-2&1\\
\lambda_3&1&1&-2
\end{array}
=\mathbf1\mathbf1^{\mathsf T}-3I_3.
\tag{6}
\]

所以该矩阵秩为二，行和、列和都为零；等价地

\[
\boxed{\lambda_1+\lambda_2+\lambda_3=0.}
\tag{7}
\]

取截断坐标

\[
\mathbb F_p[C_p^2]\cong
\mathbb F_p[u,v]/(u^p,v^p),\qquad
u=1-X^e,\quad v=1-X^f.
\tag{8}
\]

若把 \(\Psi_{C_i}\) 的次数 \(2p-3\) 初始项写成

\[
A_i u^{p-1}v^{p-2}+B_i u^{p-2}v^{p-1},
\tag{9}
\]

则 \(\lambda_i(ae+bf)=bA_i+aB_i\)。式 (6) 因而等价于唯一的

\[
\begin{aligned}
\operatorname{in}\Psi_{C_1}
 &=u^{p-1}v^{p-2}-2u^{p-2}v^{p-1},\\
\operatorname{in}\Psi_{C_2}
 &=-2u^{p-1}v^{p-2}+u^{p-2}v^{p-1},\\
\operatorname{in}\Psi_{C_3}
 &=u^{p-1}v^{p-2}+u^{p-2}v^{p-1}.
\end{aligned}
\tag{10}
\]

特别地，三条初始项也相加为零。这里没有取消任何零因子。

## 3. 一张共同的逐位置标签表

以下所有系数都在 \(\mathbb F_{233}\) 中。取一个共同位置

\[
y=e+f.
\tag{11}
\]

令三个互不相交的五位置花瓣 \(A_i\) 的标签分别为

\[
\begin{aligned}
A_1={}&(3e,227e,43f,193f,e+229f),\\
A_2={}&(2e,229e,7f,130f,e+94f),\\
A_3={}&(3e,229e,69f,98f,e+66f).
\end{aligned}
\tag{12}
\]

直接相加得到

\[
\sigma(A_1)=(-2,-1),\qquad
\sigma(A_2)=(-1,-2),\qquad
\sigma(A_3)=(0,0).
\tag{13}
\]

因此六位置外部块

\[
E_i=\{y\}\mathbin{\dot\cup}A_i
\tag{14}
\]

满足

\[
\sigma(E_i)=-w_i,\qquad E_i\cap E_j=\{y\}\quad(i\ne j).
\tag{15}
\]

因此令

\[
H_i^{\mathrm{rel}}=\{u_i\}\mathbin{\dot\cup}E_i
\tag{15a}
\]

便得到三个长度七、投影和为零、尾迹分别为单点的字面端点块；它们
两两的实际位置交恰为 \(\{y\}\)，交投影非零。上标 “rel” 只表示
尚未把这三块宣称为完整首片自动闭包中的全部端点。

再取一个 453 位置共同核 \(G\)。其 \(e\)-向 227 个位置的标量为

\[
\underbrace{1,\ldots,1}_{224},2,107,135,
\tag{16}
\]

其 \(f\)-向 226 个位置的标量为

\[
\underbrace{1,\ldots,1}_{223},1,85,159.
\tag{17}
\]

这些标量全非零，并且

\[
|G|=453,qquad \sigma(G)=2e+2f=2y,
\tag{18}
\]

而次数 453 的初始积为

\[
\operatorname{in}\Psi_G=-2u^{227}v^{226}.
\tag{19}
\]

定义同一张 469 位置中间表

\[
M=G\mathbin{\dot\cup}\{y\}
 \mathbin{\dot\cup}A_1\mathbin{\dot\cup}A_2
 \mathbin{\dot\cup}A_3.
\tag{20}
\]

由 (13)、(18) 得

\[
|M|=469,\qquad\sigma(M)=0.
\tag{21}
\]

最后置

\[
C_i=M\setminus E_i
   =G\mathbin{\dot\cup}A_j\mathbin{\dot\cup}A_k.
\tag{22}
\]

于是 \(|C_i|=463=2p-3\)、\(\sigma(C_i)=w_i\)，且

\[
Q_i^{\mathrm{rel}}=C_i\mathbin{\dot\cup}\{u_j,u_k\}
\tag{23}
\]

有长度 \(465=2p-1\) 和总和零。上标 “rel” 提醒：这里只核对总和与
指定删除恒等式，不主张它是原子。

## 4. 三对共同因子和式 (10) 的同时实现

式 (12) 的五个线性初始因子分别相乘，得到

\[
\begin{aligned}
F_1&=204u^2v^2(u+229v),\\
F_2&=176u^2v^2(u+94v),\\
F_3&=173u^2v^2(u+66v).
\end{aligned}
\tag{24}
\]

结合 (19)，直接计算

\[
\operatorname{in}\Psi_{C_1}=\operatorname{in}\Psi_G F_2F_3,
\quad
\operatorname{in}\Psi_{C_2}=\operatorname{in}\Psi_G F_1F_3,
\quad
\operatorname{in}\Psi_{C_3}=\operatorname{in}\Psi_G F_1F_2,
\tag{25}
\]

恰好给出 (10)。因 \(I^{2p-1}=0\)，\(\Psi_{C_i}\in I^{2p-3}\)
乘以 \(1-X^w\) 时只有 (10) 和该因子的线性项能存活。因此 (5) 的
六个非对角等式在完整群代数中精确成立，而不只是形式最低次近似。

三对端点还同时保留真正的字面共同因子。若
\(\{i,j,k\}=\{1,2,3\}\)，则

\[
C_i\cap C_j=G\mathbin{\dot\cup}A_k,
\qquad |C_i\cap C_j|=458,
\tag{26}
\]

并且

\[
C_i\setminus C_j=A_j,qquad
C_j\setminus C_i=A_i.
\tag{27}
\]

所以每一对的精确逐位置分解都是

\[
\Psi_{C_i}=\Psi_{G\dot\cup A_k}\Psi_{A_j},
\qquad
\Psi_{C_j}=\Psi_{G\dot\cup A_k}\Psi_{A_i}.
\tag{28}
\]

三个式 (28) 来自同一张表 (20)，不是给三对独立选择抽象公共因子。

## 5. 得到什么，以及没有得到什么

本文得到两个严格结论。

1. 在 rank‑2 标准形下，三条 singleton-tail 泛函被唯一压成
   \(\mathbf1\mathbf1^{\mathsf T}-3I\)，不再有泛函搜索变量。
2. 这个唯一正规形可与三对真实共同字面因子、五位置交换花瓣、端点
   外部块和值和三个 \(Q_i^{\mathrm{rel}}\) 的总和同时实现。因此不能
   只从“\(\lambda_i\) 联立 + 共同因子不可取消”推出矛盾。

未核对且仍承重的是：每个 \(Q_i^{\mathrm{rel}}\) 的所有删点积、等价
的完整投影原子性；由这 469 个位置继续接入 \(P\) 和实际高度后的全部
自动短块；实际重数上界、Hasse 行及实际 \(Z\) 原子性。因此本文没有
给出首片 SAT 见证，也没有排除首片。

下一步不应再把三条 \(\lambda_i\) 当作独立未知量。严格求解器可直接
写入 (6)/(10)，但必须把本文没有实现的**每个 \(Q_i\) 全删点条件**和
完整短块闭包一起加入；新的矛盾若存在，只能来自这些更深层信息。

全局 \(A_p\) 保持 **INCOMPLETE**。
