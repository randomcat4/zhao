# \(p=233\) 三个长八 singleton 二次签名的联合边界

STATUS: **PROVED BOUNDARY / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 三组尾基

在删去 540 个含长七 singleton 的 outer rows 后，余下 180 行的三个
singleton 端点均长八。固定尾基

\[
e,f,\qquad \gamma=-e-f,
\tag{1}
\]

并写 packing 方向

\[
s=xe+yf.
\tag{2}
\]

三个 singleton 长补所含的有序尾对依次取为

\[
B_\gamma=(e,f),\qquad
B_e=(f,\gamma),\qquad
B_f=(e,\gamma).
\tag{3}
\]

于是 \(s\) 在三组基下的坐标分别为

\[
(x,y),\qquad (y-x,-x),\qquad (x-y,-y).
\tag{4}
\]

## 2. 单张二次式的双消零条件

长八删双尾的带符号系数函数为

\[
C_{A,B}(u,v)=
1-(u-v)^2+A\,u(u+1)+B\,v(v+1).
\tag{5}
\]

直接相加、相减 \(C_{A,B}(u,v)=C_{A,B}(-u,-v)=0\)，得到等价条件

\[
Au+Bv=0,
\qquad
Au^2+Bv^2=(u-v)^2-1.
\tag{6}
\]

若 \(u,v,u-v\ne0\)，其唯一解为

\[
A=\frac{(u-v)^2-1}{u(u-v)},
\qquad
B=-\frac{(u-v)^2-1}{v(u-v)}.
\tag{7}
\]

若 \(u=0\) 或 \(v=0\)，(6) 只可能落在相应的正负尾标签；若
\(u=v\ne0\)，(6) 无解。因此结合已审的六个正负尾标签排除，三张
二次式同时消去 \(\pm s\) 时自动有

\[
x\ne0,\qquad y\ne0,\qquad d:=x-y\ne0.
\tag{8}
\]

## 3. 三张签名的全部形式解

把 (4) 逐一代入 (7)，三组参数被唯一确定为

\[
\boxed{
\begin{aligned}
A_\gamma&=\frac{d^2-1}{xd},
&B_\gamma&=-\frac{d^2-1}{yd},\\
A_e&=-\frac{y^2-1}{dy},
&B_e&=\frac{y^2-1}{xy},\\
A_f&=\frac{x^2-1}{dx},
&B_f&=\frac{x^2-1}{xy}.
\end{aligned}}
\tag{9}
\]

反之，对每个满足 (8) 的 \((x,y)\)，式 (9) 代回 (5) 都使三张
签名同时满足

\[
C_i(s)=C_i(-s)=0.
\tag{10}
\]

故 \(p=233\) 时共有

\[
(p-1)(p-2)=232\cdot231=53592
\tag{11}
\]

个有向形式解；只商去 \(s\leftrightarrow-s\) 后有 26796 个
\(\pm\)-轨道（不是商去全部非零标量的射影方向）。

一个显式回归点是

\[
(x,y,d)=(2,3,-1),
\tag{12}
\]

此时

\[
(A_\gamma,B_\gamma)=(0,0),
\quad
(A_e,B_e)=(158,79),
\quad
(A_f,B_f)=(115,117)
\pmod{233}.
\tag{13}
\]

在三组坐标 \((2,3),(1,-2),(-1,-3)\) 中，(13) 均使正负两个值
为零，且 (12) 不是六个正负尾标签之一。

## 4. 边界与下一承重点

式 (9) 是签名层形式解，不声称存在实现这些参数的三个实际长补原子。
461 complete-deletion 定理约束普通表示族及其共同必经非尾位置；
式 (10) 只表示偶、奇子集数之差在 \(\mathbb F_p\) 中为零。它既允许
表示族为空，也允许非空表示发生带符号抵消，所以 mandatory-core
上界不会自动给 (9) 新方程。

因此纯三二次签名加六尾排除不能关闭剩余 180 行。下一步必须从三个
长补共享的真实 \(K\)-因子与七位置删集推出跨端点参数关系，或把
complete 表示见证的统一 \(q\)-高度及自动短块接入。固定
\(p=233\) 与全局 \(A_p\) 仍为 **INCOMPLETE**。
