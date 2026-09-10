# Route A4：±2 坐标模板的三点排除与二点高度系统

STATUS: DISPROVED

固定标准商原子

\[
B=e_1^{p-1}e_2^{p-1}e_3^{p-1}g,\qquad g=e_1+e_2+e_3,
\]

以及六点商标号

\[
C=(2e_1,-2e_1,2e_2,-2e_2,2e_3,-2e_3).
\]

对每个素数 \(p\ge 11\)，这个具体的 \((B,C)\) 模板与三点覆盖引理
矛盾，故已被严格排除。主排除完全不依赖高度。后文保留二点高度系统，
用于说明：若暂时忘掉更强的三点接口，二点接口仍给出每个方向的支撑
缺口、支撑上界、两个卷积必要式，以及若干严格有限排除。

## 1. 商零和块与高度公式

记

\[
\alpha_i=h(2e_i),\qquad
\beta_i=h(-2e_i),\qquad
P_i=\alpha_i+\beta_i.
\]

在 \(B_{e_i}\) 中固定一对 \(u,v\)，令 \(z=h_u+h_v\) 及
\(\lambda=z+\beta_i\)。若
\(\{j,k\}=\{1,2,3\}\setminus\{i\}\)，则所有含 \(u,v\) 的长度
至多八的商零和块只有以下五类：

\[
\begin{array}{c|c|c}
 &\{u,v,-2e_i\}\text{ 外增加的部分}&\text{长度}\\ \hline
A&\varnothing&3\\
B_\ell&\{2e_\ell,-2e_\ell\}&5\\
C_\ell&\{x_\ell,y_\ell,-2e_\ell\}&6\\
D&\{\pm2e_j,\pm2e_k\}&7\\
E_{j\to k}&\{2e_j,-2e_j,x_k,y_k,-2e_k\}&8.
\end{array}
\]

这里 \(x_\ell,y_\ell\) 是不同的 \(B_{e_\ell}\) 位置；不存在含
\(B_g\) 的类型。

令 \(m_i(t)\) 是 \(B_{e_i}\) 中高度 \(t\) 的重数，并令

\[
R_i(s)=\#\{\{x,y\}\subset B_{e_i}:h_x+h_y=s\}.
\]

则

\[
R_i(s)=\frac12\left(
\sum_t m_i(t)m_i(s-t)-m_i(s/2)
\right).
\]

长度窗口和符号给出

\[
\begin{aligned}
d_1^{(i)}(z)
={}&-[\lambda=1]
-\sum_{\ell=j,k}[\lambda+P_\ell=1]
+\sum_{\ell=j,k}R_\ell(1-\lambda-\beta_\ell),\\
d_2^{(i)}(z)
={}&-\sum_{\ell=j,k}[\lambda+P_\ell=2]
+\sum_{\ell=j,k}R_\ell(2-\lambda-\beta_\ell)
-[\lambda+P_j+P_k=2],\\
d_3^{(i)}(z)
={}&\sum_{\ell=j,k}R_\ell(3-\lambda-\beta_\ell)
-[\lambda+P_j+P_k=3]\\
&+R_k(3-\lambda-P_j-\beta_k)
+R_j(3-\lambda-P_k-\beta_j).
\end{aligned}
\]

对每个满足 \(R_i(z)>0\) 的实际配对和值，必须同时有

\[
8d_1^{(i)}(z)+10d_2^{(i)}(z)=3,\qquad
2d_1^{(i)}(z)-10d_3^{(i)}(z)=1.
\tag{1}
\]

## 2. 主结论：三点覆盖直接排除模板

**定理。** 对任意素数 \(p\ge11\)，上述 \((B,C)\) 模板不满足
三点覆盖：每个三点位置集包含于某个长度至多八的商零和短块。

**证明。** 固定一个方向 \(i\)，从 \(p-1\) 个 \(B_{e_i}\) 位置中
任取三个不同位置。设一个包含这三点的候选短块还总共取了
\(b_i\) 个 \(B_{e_i}\) 位置，并以

\[
\varepsilon,\gamma_i^+,\gamma_i^-\in\{0,1\}
\]

分别表示它是否取了唯一的 \(B_g\) 位置、\(C\) 中的 \(2e_i\)
位置和 \(-2e_i\) 位置。其他方向的 \(B\) 与 \(C\) 位置对第
\(i\) 坐标贡献均为零。于是该块商和的第 \(i\) 坐标具有整数代表

\[
q_i=b_i+\varepsilon+2\gamma_i^+-2\gamma_i^-.
\tag{2}
\]

其中 \(b_i\ge3\)，且长度至多八给出

\[
b_i+\varepsilon+\gamma_i^++\gamma_i^-\le8.
\tag{3}
\]

由 (2)--(3)，\(q_i\ge3-2=1\)。若 \(\gamma_i^+=0\)，则
\(q_i\le b_i+\varepsilon\le8\)；若 \(\gamma_i^+=1\)，则由 (3)

\[
q_i\le b_i+\varepsilon+2\le9.
\]

所以始终有 \(1\le q_i\le9\)。当 \(p\ge11\) 时，
\(q_i\not\equiv0\pmod p\)，故任何长度至多八、包含所选三点的块
都不可能商零和。这与三点覆盖矛盾。证毕。

这个论证只排除这里固定的 \(\pm2e_i\) 六点模板；它没有分类任意
六点 \(C\)，也没有处理 \(p=7\)。

## 3. 非对称二点接口：每个方向都有支撑缺口

以下结论不使用三方向对称。因为每个 \(B_{e_i}\) 类恰有 \(p-1\)
个位置，恒有

\[
\sum_{z\in\mathbb F_p}R_i(z)=\binom{p-1}{2}\equiv1\pmod p.
\tag{4}
\]

固定任意方向 \(i\)。假设 \(R_i(z)>0\) 对所有
\(z\in\mathbb F_p\) 成立，则 (1) 对全部 \(z\) 都成立，可以逐
\(z\) 求和。平移 \(z\mapsto z+c\) 置换 \(\mathbb F_p\)，故每个
指示函数的和为 \(1\)，而 (4) 对另外两个方向 \(j,k\) 都成立。
直接从第 1 节公式得到

\[
\begin{aligned}
\sum_z d_1^{(i)}(z)&=-1-1-1+1+1=-1,\\
\sum_z d_2^{(i)}(z)&=-1-1+1+1-1=-1.
\end{aligned}
\tag{5}
\]

将第一条 (1) 对全部 \(z\) 求和，左端由 (5) 为
\(8(-1)+10(-1)=-18\)，右端为 \(3p=0\)。对素数 \(p\ge11\)，
\(-18\ne0\pmod p\)，矛盾。因此量词化结论为

\[
\boxed{\ \forall i\in\{1,2,3\},\quad
\operatorname{supp}R_i\ne\mathbb F_p.\ }
\tag{6}
\]

令 \(A_i=\operatorname{supp}m_i\)。若
\(|A_i|\ge(p+3)/2\)，则对每个 \(z\)

\[
|A_i\cap(z-A_i)|\ge2|A_i|-p\ge3.
\]

反射 \(x\mapsto z-x\) 至多有一个不动点 \(z/2\)，所以交集中必有
一对不同的 \(x,z-x\)。对应两个不同位置给出 \(R_i(z)>0\)。于是
\(R_i\) 全支撑，与 (6) 矛盾。因此

\[
\boxed{\ \forall i\in\{1,2,3\},\quad
|\operatorname{supp}m_i|\le\frac{p+1}{2}.\ }
\tag{7}
\]

## 4. 三方向对称压缩

附加有限探针的对称假设

\[
m_1=m_2=m_3=m,\qquad
\alpha_1=\alpha_2=\alpha_3=\alpha,\qquad
\beta_1=\beta_2=\beta_3=\beta.
\]

由 \(\sigma(C)=2a\)，

\[
P:=\alpha+\beta=\frac23.
\]

若把 \(m\) 的所有高度平移 \(c\)，同时令

\[
\beta\longmapsto\beta-2c,\qquad
\alpha\longmapsto\alpha+2c,
\]

则 \(P\) 不变，所有块高度及 (1) 不变。取 \(c=\beta/2\)，可无损令

\[
\beta=0,\qquad\alpha=P=2/3.
\]

所以只需枚举

\[
\sum_{t\in\mathbb F_p}m(t)=p-1,\qquad
0\le m(t)\le p-4.
\tag{8}
\]

对称情形中，对每个 \(R(z)>0\)，公式化为

\[
\begin{aligned}
d_1(z)&=-[z=1]-2[z+P=1]+2R(1-z),\\
d_2(z)&=-2[z+P=2]+2R(2-z)-[z+2P=2],\\
d_3(z)&=2R(3-z)-[z+2P=3]+2R(3-z-P).
\end{aligned}
\tag{9}
\]

## 5. 两个卷积必要式

定义循环卷积

\[
K(c)=\sum_{z\in\mathbb F_p}R(z)R(c-z).
\]

因为 (1) 在 \(R(z)>0\) 时成立，而 \(R(z)=0\) 的项乘上 \(R(z)\)
后消失，所以可将两条 (1) 分别乘以 \(R(z)\) 并对全部 \(z\) 求和。
由 \(\sum_zR(z)=1\)，逐项得到必要条件

\[
\begin{aligned}
&8\{-R(1)-2R(1-P)+2K(1)\}\\
&\qquad+10\{-2R(2-P)+2K(2)-R(2-2P)\}=3
\pmod p,
\end{aligned}
\tag{10}
\]

以及

\[
\begin{aligned}
&2\{-R(1)-2R(1-P)+2K(1)\}\\
&\qquad-10\{2K(3)-R(3-2P)+2K(3-P)\}=1
\pmod p.
\end{aligned}
\tag{11}
\]

脚本把两边展开为 \(R(0),\ldots,R(p-1)\) 的稀疏二次多项式并逐
单项式比较，不依赖随机代入。(10)--(11) 目前只是必要式；尚未从
它们单独推出一般无解。

## 6. 严格有限二点结论

脚本总以整数值判定实际条件 \(R(z)>0\)，没有把
\(R(z)\bmod p\ne0\) 偷换成实际支撑。完全枚举 (8) 得到

\[
\begin{array}{c|c|c}
p&\text{满足 (8) 的全部 }m&\text{满足全部 (1) 的 }m\\ \hline
11&184030&0\\
13&2702973&0.
\end{array}
\]

所以 \(p=11,13\) 时不存在三方向对称的实际高度解。此外，在附加
\(|\operatorname{supp}m|\le4\) 后，严格穷尽结果为

\[
\begin{array}{c|c|c}
p&\text{满足 (8) 且支撑至多 4 的全部 }m&\text{满足全部 (1) 的 }m\\ \hline
17&1153756&0\\
19&2766780&0\\
23&12148048&0.
\end{array}
\]

其中 \(p=23\) 的计数可再拆为支撑至多三的 \(370898\) 个与支撑
恰为四的 \(11777150\) 个。这三个较大素数的结论只排除对称且支撑
至多四的二点高度模板；不得提升为无支撑限制的无解证明。

给定 \(m\) 后，
\(B\) 的总高度 \(-2\) 总可由唯一的 \(B_g\) 位置补足：

\[
h(B_g)=-2-3\sum_t t\,m(t).
\]

## 7. 随机探针与严格停止线

固定种子的非对称随机探针可由脚本的 `--random-probe` 单独运行。
随机未命中在任何样本数下都不是无解证明，也不参与上面的
`STATUS: DISPROVED`；该状态只由第 2 节的确定性三点矛盾支撑。

严格结论的边界如下：

1. 第 2 节排除固定标准 \(B\) 与固定 \(C=(\pm2e_i)_{i=1}^3\) 的
   整个模板，对全部素数 \(p\ge11\) 成立。
2. 第 3 节的 (6)--(7) 不要求三方向高度对称，但仍以第 1 节的
   固定 \(\pm2e_i\) 商零和块分类为前提。
3. (10)--(11) 与第 6 节有限穷举均属于三方向对称二点接口。
4. 本文不分类任意六点 \(C\)、任意极值原子，也不处理 \(p=7\)。

默认快速复核三点障碍、符号恒等式、卷积展开及 \(p=11,13\) 全枚举：

    python verify_standard_pair_system.py

加入 \(p=17,19,23\) 的支撑至多四穷举：

    python verify_standard_pair_system.py --extended

随机非对称探针（明确为非证明）：

    python verify_standard_pair_system.py --random-probe
