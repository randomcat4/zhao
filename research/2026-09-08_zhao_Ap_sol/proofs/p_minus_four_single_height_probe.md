# \(p-4\) 重纤维的单高度退化与余部系统

STATUS: PROVED_HERE

## 1. 设置与本页结论

设 \(p\ge11\) 为素数，并沿用 ROUTE-A4 的冻结反例
\[
S=a^{p-4}R,
\]
长度 \(3p+4\) 的实际零和原子 \(Z\subset R\)，以及
\(T\in\mathcal F_3\)。写
\[
s=|T|\in\{6,7,8\},\qquad \sigma(T)=3a,\qquad
B=Z\setminus T,
\]
并假设 \(\bar B\) 是 \(C_p^3\) 中的原子。

本页研究首个真正退化的商纤维：某个非零商值 \(q\) 在 \(B\) 中
恰有
\[
m=p-4
\]
个位置 \(X\)，而这些位置全部代表同一个实际群元素 \(x\)：
\[
X=x^{p-4},\qquad \bar x=q.
\tag{1}
\]

这里实际值重数恰好等于冻结上界 \(p-4\)。所得严格结论是：

1. 每个与 \(X\) 相交的短块都由一个余部 \(U\subset Z\setminus X\)
   生成完整的 \(\binom Xb\)；每个这样的 \(U\) 必须与 \(T\)
   相交。
2. 一点、二点、三点 Hasse 关系化成第 3 节的精确余部计数系统。
3. 纯落在 \(T\) 中的余部受到第 5 节的锚点排除；特别地，
   \(F_3\) 的单点余部完全不可能，并得到所有单点余部的显式重数
   上界。
4. 这些条件尚未排除 (1)。第 6 节给出一个无单点余部、同时满足
   全部纯 \(X\) 一点、二点、三点模 \(p\) Hasse 方程的显式相容
   参数。

因此本页登记的是新必要结构和严格停止线，不把单高度纤维误报为
已经闭合。

## 2. 同商替换在单高度处完全退化

固定含 \(b\ge1\) 个 \(X\)-位置的短块 \(A\)，并令
\[
\ell=|A|,\qquad U=A\setminus X.
\]
因为 \(A\) 商零和，
\[
\bar\sigma(U)=-bq.
\tag{2}
\]
若 \(U\cap T=\varnothing\)，则
\(U\subset B\setminus X\)。对任意 \(V\in\binom Xb\)，
\[
V\mathbin{\dot\cup}U\subset B
\]
都是长度至多八的非空真商零和子序列，与 \(\bar B\) 的原子性
矛盾。因此
\[
\boxed{U\cap T\ne\varnothing.}
\tag{3}
\]
特别地 \(U\ne\varnothing\)、\(b\le\ell-1\)。

反过来，一旦固定 \(U\) 且
\[
\bar\sigma(U)=-bq,\qquad \sigma(U)+bx=\lambda a,
\tag{4}
\]
则每个 \(V\in\binom Xb\) 都产生同一个族中的短块：
\[
\sigma(V\mathbin{\dot\cup}U)=\lambda a.
\tag{5}
\]
这是一整个完全 \(b\)-均匀层，而不是一个偶然表示。

在重数 \(p-1\) 与 \(p-2\) 的非退化高度论证中，不同 \(V\) 的
高度和必须挤入一至三元长度窗，从而产生矛盾。此处所有
\(h(V)=bh(x)\) 完全相同；更重要的是，一点高度支撑的重数正好是
\(p-4\)，并不违反高度上界。这正是此前缺族论证第一次失效的
位置。

## 3. 精确余部计数系统

对 \(\lambda=1,2,3\)、允许的短块长度 \(\ell\)，以及
\(1\le b\le\ell-1\)，定义
\[
N_{\ell,b}^{(\lambda)}
=
\#\left\{
U\subset Z\setminus X:
\begin{array}{l}
|U|=\ell-b,\\
\bar\sigma(U)=-bq,\\
\sigma(U)+bx=\lambda a
\end{array}
\right\}.
\tag{6}
\]
由 (3)，这里每个被计数的 \(U\) 都与 \(T\) 相交。长度范围是
\[
\lambda=1:\ 2\le\ell\le6,\qquad
\lambda=2:\ 4\le\ell\le7,\qquad
\lambda=3:\ 6\le\ell\le8.
\tag{7}
\]
不存在的指标约定其 \(N\) 为零。

固定 \(t=1,2,3\) 个 \(X\)-位置。由 (5)，一个余部 \(U\) 产生的
含这 \(t\) 个位置的块数恰为
\[
\binom{m-t}{b-t}.
\tag{8}
\]
因此逐点带符号度给出三个精确关系
\[
\boxed{
\sum_{\ell,b}
(-1)^{\ell-1}
\binom{p-5}{b-1}N_{\ell,b}^{(\lambda)}
=e_\lambda,}
\tag{9}
\]
其中
\[
(e_1,e_2,e_3)=
\left(-\frac34,\frac3{10},-\frac1{20}\right).
\]

按原有二点共度的符号约定，令
\[
d_\lambda=
\sum_{\ell,b}
(-1)^\ell
\binom{p-6}{b-2}N_{\ell,b}^{(\lambda)}.
\tag{10}
\]
则
\[
\boxed{
8d_1+10d_2=3,\qquad
2d_1-10d_3=1.}
\tag{11}
\]

再令
\[
\delta_\lambda=
\sum_{\ell,b}
(-1)^{\ell-1}
\binom{p-7}{b-3}N_{\ell,b}^{(\lambda)}.
\tag{12}
\]
三点 Hasse 方程变成
\[
\boxed{4\delta_1+10\delta_2+20\delta_3=-1.}
\tag{13}
\]
所有等式均在 \(\mathbb F_p\) 中。式 (13) 的左边不为零，所以
至少有一个 \(b\ge3\) 的余部；这重新得到三点覆盖，但没有强迫
\(|U|=1\)。

## 4. 余部继承短块相交性

设 \(U,U'\) 分别生成与 \(X\) 交数为 \(b,b'\) 的短块，并且对应
的实际和系数 \((\lambda,\mu)\) 满足
\[
(\lambda,\mu)\in
\{(1,3),(2,2),(2,3),(3,3)\}.
\tag{14}
\]
这些正是已有相交定理覆盖的族对。若
\[
U\cap U'=\varnothing,\qquad b+b'\le p-4,
\]
就可以从 \(X\) 中取不交的 \(V\in\binom Xb\)、
\(V'\in\binom X{b'}\)。由 (5)，
\(V\dot\cup U\) 与 \(V'\dot\cup U'\) 是两个位置不交的相应
短块，违反族间或族内相交性。因此
\[
\boxed{
b+b'\le p-4\Longrightarrow U\cap U'\ne\varnothing
\quad\text{对 (14) 中的族对成立。}}
\tag{15}
\]

由于 \(F_1,F_2,F_3\) 块的 \(X\)-交数分别至多 \(5,6,7\)，
当 \(p\ge19\) 时 (15) 对 (14) 中任意两个余部自动适用。单高度
纤维因而把原短块相交网络完整地下推到余部网络；但小集合的相交
族可以存在，所以这还不是矛盾。

## 5. 纯 \(T\) 余部的锚点排除

先给一个统一拼接。设
\(U_1,\ldots,U_k\subset T\) 是两两不交的余部，且都具有同一
\((b,\lambda)\)，即
\[
\sigma(U_i)+bx=\lambda a.
\]
令
\[
T_0=T\setminus\bigcup_{i=1}^kU_i.
\]
则
\[
\sigma(T_0)=(3-k\lambda)a+kb\,x.
\tag{16}
\]
取
\[
n\equiv-kb\pmod p,\qquad
\rho\equiv k\lambda-3\pmod p,
\qquad 0\le n,\rho\le p-1.
\tag{17}
\]
若
\[
n\le p-4,\qquad \rho\le p-4,
\tag{18}
\]
便可从 \(X=x^{p-4}\) 取 \(n\) 个位置，并从外部
\(a^{p-4}\) 取 \(\rho\) 个锚点。它们与 \(T_0\) 按位置不交，
且由 (16)--(17) 总和为零。其长度至多
\[
s+(p-4)+(p-4)\le2p<3p-2.
\tag{19}
\]
下列应用中所得子序列都非空。

对 \(\lambda=3\)，一个余部在 \(b\ge4\) 时已有
\[
(k,n,\rho)=(1,p-b,0),
\]
满足 (18)。因此
\[
\boxed{
\lambda=3,\ b\ge4\Longrightarrow U\nsubseteq T.}
\tag{20}
\]
当 \(\lambda=3,b=3\) 时，两个不交的纯 \(T\) 余部取
\((k,n,\rho)=(2,p-6,3)\)，同样产生短零和。

特别地，若 \(U=\{y\}\) 是单点余部，则商原子性已由 (3) 给
\(y\in T\)，而所有固定 \((b,\lambda)\) 的这种位置都等于同一个
实际值
\[
y=\lambda a-bx.
\tag{21}
\]
对 (16)--(18) 枚举最小 \(k\)，得到
\[
\begin{array}{c|c|c}
\lambda&\text{允许的单点 }b&
N_{b+1,b}^{(\lambda)}\text{ 的上界}\\ \hline
3&5,6,7&0\\
2&3,4,5&1\\
2&6&1\ (p\ne11),\quad2\ (p=11)\\
1&1&3\\
1&2,3&2\\
1&4&2\ (p\ne11),\quad3\ (p=11)\\
1&5&2\ (p\ne13),\quad3\ (p=13).
\end{array}
\tag{22}
\]

例如 \(\lambda=2\) 通常取 \(k=2\)，此时
\(\rho=1\)；唯一失败的允许参数是
\((p,b)=(11,6)\)，因为 \(2b\equiv1\pmod{11}\) 会要求
\(n=p-1\)，改取 \(k=3\) 即可。对 \(\lambda=1\) 通常取
\(k=3,\rho=0\)；\(b=1\) 以及例外
\((p,b)=(11,4),(13,5)\) 改取 \(k=4,\rho=1\)。
这逐项证明 (22)，而不是把模 \(p\) 的计数剩余类当成实际重数。

## 6. 全部纯 \(X\) 低阶 Hasse 关系仍相容

以下显式参数说明 (9)、(11)、(13) 与“没有单点余部”同时相容。
令未列出的 \(N\) 全为零，并在 \(\mathbb F_p\) 中置
\[
\begin{array}{c|ccc}
\lambda&N_{\ell,1}^{(\lambda)}
&N_{\ell,2}^{(\lambda)}
&N_{\ell,3}^{(\lambda)}\\ \hline
1,\ \ell=5&-\dfrac92&-\dfrac32&-\dfrac14\\[1mm]
2,\ \ell=6&\dfrac65&\dfrac3{10}&0\\[1mm]
3,\ \ell=7&\dfrac9{20}&\dfrac1{10}&0.
\end{array}
\tag{23}
\]
所有列出的余部大小 \(\ell-b\) 至少为二，所以
\[
N_{b+1,b}^{(\lambda)}=0
\]
对每个 \((b,\lambda)\) 成立。分母只含 \(2,5\)，故对所有
\(p\ge11\) 有定义；取各剩余类在 \(0,\ldots,p-1\) 中的整数
代表，便得到普通非负计数参数。

直接代入 (9)：
\[
\begin{aligned}
-\frac92-5\left(-\frac32\right)
+15\left(-\frac14\right)&=-\frac34,\\
-\frac65+5\left(\frac3{10}\right)&=\frac3{10},\\
\frac9{20}-5\left(\frac1{10}\right)&=-\frac1{20}.
\end{aligned}
\]
式 (10) 给
\[
(d_1,d_2,d_3)=\left(0,\frac3{10},-\frac1{10}\right),
\]
恰满足 (11)。式 (12) 则给
\[
(\delta_1,\delta_2,\delta_3)=
\left(-\frac14,0,0\right),
\]
恰满足 (13)。此外
\(N_{5,3}^{(1)}=-1/4\ne0\)，所以每个 \(X\)-三元组仍有普通
短块覆盖。

对每个出现的余部大小 \(2,\ldots,6\)，与 \(T\) 相交的候选位置集
数都远大于 \(p-1\)，故单纯容量上界不会排除 (23)。但是 (23)
只是固定点集完全落在 \(X\) 时的一点、二点、三点 Hasse 相容参数；
它不处理含 \(Z\setminus X\) 位置的混合 Hasse 方程，也不构造统一
商标号、余部相交网络或完整实际原子。

## 7. 精确停止线

单高度退化绕过前述论证的原因不是缺少三点覆盖，而是每个余部一旦
出现就自动生成完整的 \(X\)-均匀层，同时所有替换块具有完全相同的
实际和。高度子集和不再提供第二个值，实际重数又恰未越过
\(p-4\) 上界。

现有接口已经迫使：

- 每个余部都命中 \(T\)；纯落在 \(T\) 中的余部另受第 5 节限制；
- 余部满足精确矩系统 (9)--(13)；
- 大素数时余部继承四种短块相交关系；
- 纯 \(T\) 余部和所有单点余部满足 (20)--(22) 的强限制。

但 (23) 证明低阶 Hasse 关系不能强迫单点余部，因而锚点拼接还
不能闭合 (1)。下一步必须排除 (23) 所代表的多位置余部相交网络，
最直接的新增接口是同时控制 \(U\cap T\) 与
\(U\cap(B\setminus X)\) 的大小，或把补原子交换施加到两个不同
余部；不能继续仅靠同商高度变化。
