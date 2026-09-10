# 三点删除的定量短块覆盖

STATUS: PROVED_HERE

设 \(p\ge7\)，\(Z\subset R\) 是长度 \(3p+4\) 的实际零和原子，
\(\mathcal F_r\) 是 \(Z\) 中实际和为 \(ra\) 的短块族，\(r=1,2,3\)。
其长度范围分别是 \(2\)--\(6\)、\(4\)--\(7\)、\(6\)--\(8\)。

## 1. 删除--Hasse 三角形

对 \(W\subset Z\)、\(|W|=t\le3\)，以及 \(q\ge0,t+q\le3\)，定义

\[
H_{W,q}(X)=
\sum_{\substack{E\subset Z\setminus W\\
\sigma(E)=-\sigma(W)+Xa}}
(-1)^{|E|}\binom{|E|}{q}.
\]

把 \(W\) 加回每个被计数的 \(E\)，原子线限制说明该函数只支撑在
\(0,\pm1,\pm2,\pm3\)。群环次数界及第 \(q\) 个 Hasse 阴影给出

\[
\deg H_{W,q}\le p-8+t+q.
\]

在 \(X=0\) 处，若 \(W\ne\varnothing\)，原子性说明唯一表示为
\(E=Z\setminus W\)；若 \(W=\varnothing,q>0\)，空集项权重为零，
故唯一非零贡献仍来自 \(Z\)。由于 \(|Z|=3p+4\) 为奇数，并在
\(\mathbb F_p\) 中约去 \(3p\)，对 \((t,q)\ne(0,0)\) 有

\[
H_{W,q}(0)=(-1)^{t+1}\binom{4-t}{q}.
\]

唯一例外是 \((t,q)=(0,0)\)：空集与 \(Z\) 的贡献相消，故
\(H_{\varnothing,0}(0)=0\)。后续承重情形为 \((t,q)=(3,0)\)，
不受此例外影响。

令

\[
Q(X)=\prod_{c\notin\{0,\pm1,\pm2,\pm3\}}(X-c).
\]

除上述例外零函数外，于是

\[
H_{W,q}(X)=Q(X)P_{W,q}(X),\qquad
\deg P_{W,q}\le t+q-1.
\]

这统一包含已有的一点、二点关系。关键的新边界是 \(t=3,q=0\)：
此时余因子至多二次，能由 \(X=0,1,2,3\) 的四个值消去。

## 2. 每个三点集都有许多短块

固定三点集 \(W\subset Z\)，记

\[
\delta_r(W)=
\sum_{\substack{A\in\mathcal F_r\\W\subset A}}
(-1)^{|A|-1}.
\]

把上节的二次余因子在 \(1,2,3\) 处取值并消去两个自由系数，得到

\[
\boxed{4\delta_1(W)+10\delta_2(W)+20\delta_3(W)=-1}
\qquad\text{于 }\mathbb F_p.
\]

令 \(D_r(W)\) 是包含 \(W\) 的 \(\mathcal F_r\) 块的普通非负计数。
整数

\[
4\delta_1(W)+10\delta_2(W)+20\delta_3(W)+1
\]

是 \(p\) 的倍数；它又是奇数，故不为零且绝对值至少为 \(p\)。因而

\[
\boxed{
D_1(W)+D_2(W)+D_3(W)
\ge\left\lceil\frac{p-1}{20}\right\rceil.}
\]

特别地，每个三位置集都包含在某个实际和为 \(a,2a\) 或 \(3a\) 的
短块中。这里使用的是带符号和的绝对值，因此没有把模 \(p\) 剩余类
误当作正计数。

## 3. 一点、二点与六项块的真实计数下界

同一整数提升应用于已有的一点和二点同余，给出

\[
\begin{aligned}
D_1(v)&\ge\left\lceil\frac{p-3}{4}\right\rceil,&
D_2(v)&\ge\left\lceil\frac{p-3}{10}\right\rceil,&
D_3(v)&\ge\left\lceil\frac{p-1}{20}\right\rceil,\\
D_1(u,v)+D_2(u,v)&\ge\left\lceil\frac{p-3}{10}\right\rceil,&
D_1(u,v)+D_3(u,v)&\ge\left\lceil\frac{p-1}{10}\right\rceil.
\end{aligned}
\]

此外，\(5N_6^Z(2a)\equiv1\pmod p\) 与 \(N_6^Z(2a)\ge0\) 给出

\[
\boxed{N_6^Z(2a)\ge\left\lceil\frac{p+1}{5}\right\rceil.}
\]

## 4. 极值补原子支中的跨边界质量

再固定六项 \(2a\) 块 \(C\)，令 \(B=Z\setminus C\)，并假设
\(\bar B\) 是 \(C_p^3\) 中长度 \(3p-2\) 的原子。任何短块
\(A\in\mathcal F_1\cup\mathcal F_2\cup\mathcal F_3\) 都必须与
\(C\) 相交；否则 \(A\subset B\) 会给出 \(\bar B\) 的非空真商
零和子序列。

所以每个 \(W\in\binom B3\) 都被至少
\(m=\lceil(p-1)/20\rceil\) 个跨越 \(B\mid C\) 的短块覆盖，并且

\[
\boxed{
\sum_A\binom{|A\cap B|}{3}
\ge m\binom{3p-2}{3}.}
\]

每个这样的短块与 \(C\) 相交且总长至多 \(8\)，故
\(|A\cap B|\le7\)。从而不同跨界短块的总数至少为

\[
\boxed{
\left\lceil
\frac{m}{35}\binom{3p-2}{3}
\right\rceil.}
\]

这把极值补原子的高度边缘真正转化为一族数量为四次量级的常长度
跨界表示，但尚未单独推出矛盾。

## 5. 方法的精确停止线

当 \(t+q=4\) 时，余因子变成常数项固定、其余三系数自由的三次
多项式。因 \(p\ge7\) 时 \(1,2,3\) 的 Vandermonde 矩阵可逆，
这三个点的值可任意指定。因此只靠七点支撑和次数界不会再产生新的
四点关系；后续必须输入补原子、统一商标号或跨块交换信息。
