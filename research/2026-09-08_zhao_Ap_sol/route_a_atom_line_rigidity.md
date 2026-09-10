# 路线 A：长原子的锚点线刚性与秩三极长补核

## 总状态

**PROVED_HERE；完整 \(x_0=0\) 仍为 INCOMPLETE。** 本文只使用冻结反例、
\(x_0=0\) 的五层正规形、群环次数界与
\(D(C_p^3)=3p-2\)。它不使用已撤回的总和推论，也不假设
\(\sigma(R)\in\langle a\rangle\)。

## 1. 共同设置

固定素数 \(p\ge7\)，令

\[
G=C_p^4,\qquad H=\langle a\rangle,\qquad \bar G=G/H\cong C_p^3.
\]

在 \(x_0=0\) 分支，

\[
Z_{3p+j}(R)\equiv-\binom4j\pmod p,\qquad 1\le j\le4.
\]

特别地，\(3p+1,3p+3,3p+4\) 三层都存在实际零和位置子序列。
任取其中一个并记为 \(Z\)。它是实际零和原子：若它有非空真实际零和
子序列，则该子序列及其非空补集都是 \(S\) 的实际零和，而二者总长小于
\(6p-2=2(3p-1)\)，与冻结的最短零和长度矛盾。

记

\[
c_Z(x)=\sum_{A\subseteq Z,\ \sigma(A)=x}(-1)^{|A|}.
\]

若 \(|Z|=3p+j\le4p-4\)，则 \(c_Z\) 是 \(G\) 上总次数至多

\[
4p-4-(3p+j)=p-4-j
\tag{1}
\]

的多项式函数。对 \(j=4\)，当 \(p\ge11\) 时零阶次数界是 \(p-8\)，
但奇长原子在零点的两项贡献相消；当 \(p=7\) 时乘积超过顶次数。
下文统一改用一次 Hasse 阴影，其次数界都是 \(p-7\)。

## 2. 锚点线只能支撑七个系数

设 \(A\subset Z\) 且 \(\sigma(A)=\lambda a\)，其中把
\(\lambda\) 取为 \(1,\ldots,p-1\) 的整数代表。若
\(4\le\lambda\le p-4\)，则 \(A\) 可加 \(p-\lambda\) 个锚点，
\(Z\setminus A\) 可加 \(\lambda\) 个锚点。冻结反例迫使

\[
|A|\ge2p-1+\lambda,\qquad
|Z\setminus A|\ge3p-1-\lambda.
\tag{2}
\]

两式相加至少为 \(5p-2\)，严格大于本文所用的所有
\(|Z|\le3p+4\)。所以

\[
\sigma(A)\in\{0,\pm a,\pm2a,\pm3a\}.
\tag{3}
\]

若 \(\sigma(A)=\lambda a\)、\(\lambda\in\{1,2,3\}\)，对补集使用
第二个不等式给出

\[
|A|\le j+1+\lambda.
\tag{4}
\]

此外 \(R\) 没有落在 \(H\) 上的实际值，且既有局部排除给出

\[
N_k^R(2a)=N_k^R(3a)=0\qquad(1\le k\le3).
\tag{5}
\]

## 3. \(3p+3\) 原子的唯一线多项式

现在令 \(|Z|=3p+3\)。该长度为偶数，原子性给

\[
c_Z(0)=1+(-1)^{3p+3}=2.
\]

由 (1)，限制多项式

\[
f(\lambda)=c_Z(\lambda a)
\]

的次数至多 \(p-7\)。由 (3)，它在
\(\mathbb F_p\setminus\{0,\pm1,\pm2,\pm3\}\) 上为零；这些已经是
\(p-7\) 个根。故

\[
f(X)=\frac{2Q(X)}{Q(0)},\qquad
Q(X)=\prod_{t\notin\{0,\pm1,\pm2,\pm3\}}(X-t).
\tag{6}
\]

利用

\[
X^p-X=Q(X)X(X^2-1)(X^2-4)(X^2-9)
\]

在七个简单根处求值，得到

\[
\frac{Q(1)}{Q(0)}=-\frac34,\qquad
\frac{Q(2)}{Q(0)}=\frac3{10},\qquad
\frac{Q(3)}{Q(0)}=-\frac1{20}.
\]

因此

\[
\boxed{
c_Z(a)=-\frac32,\qquad
c_Z(2a)=\frac35,\qquad
c_Z(3a)=-\frac1{10}}
\quad\text{于 }\mathbb F_p.
\tag{7}
\]

三个值对每个 \(p\ge7\) 都非零。结合 (4)、(5)，每个这样的 \(Z\)
都含实际位置子序列

\[
\begin{array}{c|c}
\text{实际和}&\text{可能长度}\\ \hline
a&2,3,4,5\\
2a&4,5,6\\
3a&4,5,6,7.
\end{array}
\tag{8}
\]

若记相应位置子序列数为 \(n_{\lambda,k}(Z)\)，(7) 还给出精确同余

\[
\begin{aligned}
\sum_{k=2}^5(-1)^k n_{1,k}(Z)&=-3/2,\\
\sum_{k=4}^6(-1)^k n_{2,k}(Z)&=3/5,\\
\sum_{k=4}^7(-1)^k n_{3,k}(Z)&=-1/10.
\end{aligned}
\tag{9}
\]

## 4. \(3a\) 表示的补集必为秩三原子

设 \(A\subset Z\)、\(\sigma(A)=3a\)，并令 \(B=Z\setminus A\)。则
\(\pi(B)\) 在 \(\bar G\) 中总和为零。

若 \(\pi(B)\) 不是最小零和序列，可把 \(B\) 分成两个非空商零和位置
子序列。取较短者 \(E\)，则

\[
|E|\le |B|/2<3p-4.
\]

由第 2 节，任何这么短的商零和子序列都必须满足
\(\sigma(E)=\mu a\)、\(\mu\in\{1,2,3\}\)，并且
\(|E|\le8\)。于是 \(A\cup E\) 的实际和为
\((3+\mu)a\)，长度至多 \(16\)。再加
\(p-(3+\mu)\) 个锚点，得到长度至多

\[
16+p-4=p+12\le3p-2
\]

的非空实际零和；\(p=7\) 时也是等号边界。矛盾。因此

\[
\boxed{\pi(B)\text{ 是 }C_p^3\text{ 中的最小零和位置序列}.}
\tag{10}
\]

由 \(D(C_p^3)=3p-2\)，有 \(|B|\le3p-2\)。对本节的
\(|Z|=3p+3\)，这排除 (8) 中的四项 \(3a\) 表示，并最终得到

\[
\boxed{5\le|A|\le7,\qquad3p-4\le|B|\le3p-2.}
\tag{11}
\]

所以每个 \(3p+3\) 原子都强制产生一个长度只差 Davenport 极值至多
两项的秩三原子；这不是抽象余数模型，而是实际位置子序列。

## 5. \(3p+4\) 层的一次 Hasse 刚性

令 \(|Z|=3p+4\)。此时 \(Z\) 为奇长原子，故 \(c_Z(0)=0\)，不能直接
使用零阶系数。改定义

\[
H_1(x)=\sum_{A\subseteq Z,\ \sigma(A)=x}
(-1)^{|A|+1}|A|.
\]

它是次数至多

\[
4p-4-(|Z|-1)=p-7
\]

的多项式函数，仍由 (3) 支撑在同一七点集上。原子性给

\[
H_1(0)=(-1)^{|Z|+1}|Z|=4\pmod p.
\]

故同样的唯一性论证给出

\[
\boxed{
H_1(a)=-3,\qquad H_1(2a)=6/5,\qquad H_1(3a)=-1/5.}
\tag{12}
\]

特别地，每个 \(3p+4\) 原子也含 \(3a\) 位置子序列。由 (4)、(5) 与
第 4 节相同的补原子论证，精确得到

\[
\boxed{6\le|A|\le8,\qquad3p-4\le|Z\setminus A|\le3p-2.}
\tag{13}
\]

### 5.1 强制的六项 \(2a\) 块

对这个 \(3p+4\) 原子，记

\[
n_{\lambda,k}
=|\{A\subseteq Z:|A|=k,\ \sigma(A)=\lambda a\}|.
\]

由 (4)、(5)、(13)，只需保留

\[
\begin{aligned}
\lambda=1:&\quad 2\le k\le6,\\
\lambda=2:&\quad 4\le k\le7,\\
\lambda=3:&\quad 6\le k\le8.
\end{aligned}
\tag{14}
\]

置

\[
M_q(\lambda)=\sum_k(-1)^k\binom{k}{q}n_{\lambda,k}.
\]

因为 \(|Z|\equiv4\pmod p\) 且 \(|Z|\) 为奇数，补集对应给出

\[
M_q(-\lambda)
=-\sum_k(-1)^k\binom{4-k}{q}n_{\lambda,k},
\tag{15}
\]

而原子性给

\[
M_q(0)=\mathbf1_{q=0}-\binom4q.
\tag{16}
\]

第 \(q\) 个 Hasse 阴影的次数至多 \(p-8+q\)。因此对
\(0\le q\le6\)、\(0\le m\le6-q\)，

\[
\sum_{\lambda\in\mathbb F_p}\lambda^mM_q(\lambda)=0.
\tag{17}
\]

这里 \(p=7,q=0\) 时 \(M_0\) 是零函数，仍满足 (17)。

把 (14)--(16) 代入 (17) 得 28 条显式线性等式。高斯消元给出秩
11；唯一自由变量可取 \(n_{3,8}\)，但下列坐标与它无关：

\[
\boxed{n_{2,6}=\frac15\pmod p.}
\tag{18}
\]

为使 (18) 可逐项复核，令 \(\mathcal E_{q,m}\) 表示把 (16) 的零点项
移到右侧后的 (17)。以下线性组合的左端恰为 \(n_{2,6}\)，右端为
\(1/5\)：

\[
\begin{aligned}
&\frac54\mathcal E_{0,1}
+\frac5{12}\mathcal E_{0,5}
-\frac9{20}\mathcal E_{1,0}
+\frac76\mathcal E_{1,2}
-\frac56\mathcal E_{1,3}
-\frac{43}{60}\mathcal E_{1,4}\\
&\qquad
-\frac56\mathcal E_{2,1}
+\frac56\mathcal E_{2,3}
+\frac12\mathcal E_{3,0}
-\frac12\mathcal E_{3,2}.
\end{aligned}
\tag{19}
\]

所有分母只含 \(2,3,5\)，故对 \(p\ge7\) 可逆。特别地，每个
\(3p+4\) 原子都实际含一个六项 \(C\subset Z\)，满足
\(\sigma(C)=2a\)。

令 \(B=Z\setminus C\)，所以 \(|B|=3p-2\) 且
\(\sigma(B)=-2a\)。若 \(\pi(B)\) 不是原子，取一个真商零和分拆的
较短边 \(E\)。与第 4 节相同，\(E\) 必是至多八项、实际和为
\(\mu a\) 的短块。若 \(\mu\in\{2,3\}\)，则 \(C\cup E\) 加锚点立即
给出禁用短零和。故只能有 \(\mu=1\)。

此时 \(C\cup E\) 是 \(3a\) 块；由 (13)，其长度至多 8。因
\(|C|=6\)、\(E\ne\varnothing\) 且 \(R\) 没有 \(H\) 上的单项，
必有 \(|E|=2\)。第 4 节再说明
\(B\setminus E=Z\setminus(C\cup E)\) 是长度 \(3p-4\) 的秩三原子。
因此得到严格二分：

\[
\boxed{
\begin{array}{l}
\pi(B)\text{ 是长度 }3p-2\text{ 的秩三原子};\quad\text{或}\\
B=E\mathbin{\dot\cup}B',\
|E|=2,\ \sigma(E)=a,\
\pi(B')\text{ 是长度 }3p-4\text{ 的秩三原子}.
\end{array}}
\tag{20}
\]

### 5.2 三族小块形成无公共点的带符号覆盖

固定任意位置 \(v\in Z\)，并在仿射线 \(-v+H\) 上定义

\[
g_v(X)=c_{Z\setminus\{v\}}(-v+Xa).
\]

若 \(g_v(\lambda)\ne0\)，相应子集加回 \(v\) 后是 \(Z\) 中实际和为
\(\lambda a\) 的子集，所以 \(g_v\) 仍只支撑在
\(\{0,\pm1,\pm2,\pm3\}\)。它的次数至多

\[
4p-4-(|Z|-1)=p-7.
\]

在 \(X=0\) 处，唯一表示是完整的 \(Z\setminus\{v\}\)：任何别的表示
加回 \(v\) 都会成为 \(Z\) 的真实际零和。因为 \(|Z|-1\) 为偶数，
\(g_v(0)=1\)。七点唯一性因此逐点给出

\[
g_v(X)=\frac{Q(X)}{Q(0)}.
\tag{21}
\]

特别地，对每个位置 \(v\) 同时有

\[
\boxed{
\begin{aligned}
\sum_{\substack{A\subseteq Z,\ v\in A\\ \sigma(A)=a}}
(-1)^{|A|-1}&=-\frac34,\\
\sum_{\substack{A\subseteq Z,\ v\in A\\ \sigma(A)=2a}}
(-1)^{|A|-1}&=\frac3{10},\\
\sum_{\substack{A\subseteq Z,\ v\in A\\ \sigma(A)=3a}}
(-1)^{|A|-1}&=-\frac1{20}.
\end{aligned}}
\tag{22}
\]

记实际和为 \(ra\) 的短块族为 \(\mathcal F_r\)。由先前的长度界，

\[
\mathcal F_1:2\text{--}6\text{ 项},\qquad
\mathcal F_2:4\text{--}7\text{ 项},\qquad
\mathcal F_3:6\text{--}8\text{ 项}.
\]

于是每个位置都分别属于 \(\mathcal F_1,\mathcal F_2,\mathcal F_3\)
中的某个块；这不是普通的存在性，而是三个逐点恒定的非零带符号度。

三个块族都没有公共位置。事实上，对 \(r=1,2,3\) 都有
\(c_Z(ra)=0\)：当 \(p\ge11\) 时，其次数至多 \(p-8\)，却在七点集外
有 \(p-7\) 个根；当 \(p=7\) 时，\(|Z|=4p-3\) 已超过群环顶次数，
整个乘积为零。若某个 \(v\) 属于 \(\mathcal F_r\) 的全部块，则
(22) 中相应的带符号度就是 \(-c_Z(ra)=0\)，与其非零常数矛盾。

还有一个纯粹来自锚点预算的交叉相交约束。若
\(A\in\mathcal F_r,B\in\mathcal F_s\) 不交且 \(r+s\ge4\)，则
\(A\cup B\) 加上 \(p-r-s\) 个锚点给出实际零和；四种相关配对的
总长度都不超过 \(p+10\le3p-2\)。因此

\[
\boxed{
\mathcal F_2\text{ 与 }\mathcal F_3\text{ 各自相交，且 }
\mathcal F_1\pitchfork\mathcal F_3,\quad
\mathcal F_2\pitchfork\mathcal F_3,}
\tag{23}
\]

其中 \(\pitchfork\) 表示两个族中的任意两块相交。每个 \(\mathcal F_r\)
内部还是反链：两个同和块若严格包含，差集就是非空实际零和。

对 \(\mathcal F_3\) 还可排除“交集在商群中为零”。若两个不同
\(3a\) 块 \(A,B\) 的交集 \(I\) 满足 \(\pi(I)=0\)，则小集 \(I\)
的实际和只能是 \(\mu a\)，\(\mu\in\{1,2,3\}\)。当 \(\mu=1,2\)
时，\(A\cup B\) 的实际和分别为 \(5a,4a\)，可用锚点补成禁用短
零和；当 \(\mu=3\) 时，\(A\setminus I\) 是非空实际零和，除非
\(I=A\)，而后者再由同和反链排除。因此

\[
A\ne B\in\mathcal F_3\quad\Longrightarrow\quad
\pi(A\cap B)\ne0.
\tag{24}
\]

故每个 \(3p+4\) 原子都携带三个覆盖全部位置、无公共核心的固定和
带符号设计；其中后两族及其交叉配对均相交，而 \(3a\) 族的不同块
甚至不能有商零和交集。

### 5.3 二点删除给出共度二分

固定两个不同位置 \(u,v\in Z\)，定义

\[
g_{u,v}(X)=c_{Z\setminus\{u,v\}}(-u-v+Xa).
\]

同样的加回论证说明它只支撑在七点集，而次数至多

\[
4p-4-(3p+2)=p-6.
\]

在 \(X=0\) 处，唯一表示是完整补集；它的长度 \(3p+2\) 为奇数，
故 \(g_{u,v}(0)=-1\)。因此存在依赖于 \((u,v)\) 的
\(\alpha_{u,v}\)，使

\[
g_{u,v}(X)=Q(X)\left(\alpha_{u,v}X-\frac1{Q(0)}\right).
\tag{25}
\]

记三族中包含 \(u,v\) 的带符号共度为

\[
d_r(u,v)=
\sum_{\substack{A\in\mathcal F_r\\u,v\in A}}(-1)^{|A|}.
\]

把 (25) 在 \(X=1,2,3\) 取值并消去 \(\alpha_{u,v}\)，利用 (6) 得

\[
\boxed{
8d_1(u,v)+10d_2(u,v)=3,\qquad
2d_1(u,v)-10d_3(u,v)=1.}
\tag{26}
\]

所以没有一对位置能同时避开三族的全部块。更精确地，若该对位置
不共同属于任何 \(3a\) 块，则 \(d_3=0\)，从而

\[
d_1=\frac12,\qquad d_2=-\frac1{10};
\]

它必同时共同属于某个 \(a\) 块与某个 \(2a\) 块。类似地，缺席
\(\mathcal F_2\) 会强制 \((d_1,d_3)=(3/8,-1/40)\)，缺席
\(\mathcal F_1\) 会强制 \((d_2,d_3)=(3/10,-1/10)\)。

### 5.4 三点删除给出定量覆盖

一点、二点公式属于同一个删除--Hasse 三角形。对
\(W\subset Z,|W|=t\le3\) 及 \(q\ge0,t+q\le3\)，定义

\[
H_{W,q}(X)=
\sum_{\substack{E\subset Z\setminus W\\
\sigma(E)=-\sigma(W)+Xa}}
(-1)^{|E|}\binom{|E|}{q}.
\]

它只支撑七点，次数至多 \(p-8+t+q\)。若 \((t,q)\ne(0,0)\)，
原子性给出

\[
H_{W,q}(0)=(-1)^{t+1}\binom{4-t}{q}.
\tag{26a}
\]

在唯一例外 \((t,q)=(0,0)\) 中，空集与 \(Z\) 的贡献相消，故值为
零。若 \(W\ne\varnothing\)，(26a) 的非零贡献唯一来自
\(Z\setminus W\)；若 \(W=\varnothing,q>0\)，空集权重为零。

除该例外零函数外，故 \(H_{W,q}=QP_{W,q}\)、
\(\deg P_{W,q}\le t+q-1\)。取
\(t=3,q=0\)，记

\[
\delta_r(W)=
\sum_{\substack{A\in\mathcal F_r\\W\subset A}}(-1)^{|A|-1},
\]

并在 \(1,2,3\) 处消去二次余因子的两个自由系数，得到

\[
\boxed{4\delta_1(W)+10\delta_2(W)+20\delta_3(W)=-1.}
\tag{26b}
\]

若 \(D_r(W)\) 表示普通非负覆盖数，则 (26b) 左边加一是非零奇数倍
\(p\)。因此每个三位置集不仅被短块覆盖，而且

\[
\boxed{D_1(W)+D_2(W)+D_3(W)
\ge\left\lceil\frac{p-1}{20}\right\rceil.}
\tag{26c}
\]

同一整数提升还把 (19)、(22)、(26) 加强为

\[
\begin{gathered}
D_1(v)\ge\left\lceil\frac{p-3}{4}\right\rceil,
\quad D_2(v)\ge\left\lceil\frac{p-3}{10}\right\rceil,
\quad D_3(v)\ge\left\lceil\frac{p-1}{20}\right\rceil,\\
D_1(u,v)+D_2(u,v)\ge\left\lceil\frac{p-3}{10}\right\rceil,
\quad D_1(u,v)+D_3(u,v)\ge\left\lceil\frac{p-1}{10}\right\rceil,\\
N_6^Z(2a)\ge\left\lceil\frac{p+1}{5}\right\rceil.
\end{gathered}
\tag{26d}
\]

任取 \(T\in\mathcal F_3\)。由 (23)，\(T\) 横截三族全部短块。
对 \(Z\setminus T\) 中三元组双计数，(26c) 进一步给出无条件的

\[
\#(\mathcal F_1\cup\mathcal F_2\cup\mathcal F_3)
\ge\left\lceil
\frac{m}{35}\binom{3p-4}{3}
\right\rceil,\qquad
m=\left\lceil\frac{p-1}{20}\right\rceil.
\tag{26e}
\]

特别地，在 (20) 的极值补原子支中，任何短块都必须与六项块
\(C\) 相交，否则它是 \(B=Z\setminus C\) 的真商零和子序列。
于是每个 \(W\in\binom B3\) 都被至少
\(m=\lceil(p-1)/20\rceil\) 个跨界短块覆盖，并有

\[
\sum_A\binom{|A\cap B|}{3}\ge m\binom{3p-2}{3},
\qquad
\#\{\text{跨界短块}\}\ge
\left\lceil\frac{m}{35}\binom{3p-2}{3}\right\rceil.
\tag{26f}
\]

四点删除正好是该方法的边界：此时余因子为固定常数项的任意三次
多项式，\(1,2,3\) 三值可自由指定，不能再靠次数单独产生新关系。

### 5.5 六项 \(2a\) 块必须与 \(3a\) 块厚交叠

取任意 \(C\in\mathcal F_2\) 且 \(|C|=6\)；这类块由 (19) 保证存在。
令 \(w(A)=(-1)^{|A|-1}\)。由 (23)，每个
\(A\in\mathcal F_3\) 都与 \(C\) 相交；又由
\(c_Z(3a)=0\) 和逐点恒度 (22)，

\[
\sum_{A\in\mathcal F_3}w(A)=0,\qquad
\sum_{A\in\mathcal F_3}|A\cap C|w(A)
=6\left(-\frac1{20}\right)=-\frac3{10}.
\]

相减得到

\[
\boxed{
\sum_{A\in\mathcal F_3}(|A\cap C|-1)w(A)=-\frac3{10}\ne0.}
\tag{27}
\]

因此必有某个 \(A\in\mathcal F_3\) 满足 \(|A\cap C|\ge2\)。
对 \(I=A\cap C\) 再考察商和。若 \(\pi(I)=0\)，则小集 \(I\)
的实际系数仍只能是 \(\mu\in\{1,2,3\}\)。当 \(\mu=1\) 时，
\(A\cup C\) 的和为 \(4a\)，可用锚点补成短零和；当 \(\mu=3\)
时，\(C\setminus I\) 的和为 \(-a\)，也可补成短零和。
故只能有 \(\mu=2\)，而 \(C\setminus I\) 不得是非空实际零和，
所以 \(I=C\)。此时 \(A\setminus C\) 的和为 \(a\)，且因 \(R\)
没有 \(H\)-值单点，结合 \(6\le|A|\le8\) 得
\(|A|=8,|A\setminus C|=2\)。

于是对每个六项 \(2a\) 块 \(C\)，都存在 \(3a\) 块 \(A\) 满足

\[
\boxed{
|A\cap C|\ge2,\quad
\pi(A\cap C)\ne0;
\qquad\text{或}\qquad
A=C\mathbin{\dot\cup}E,\ |E|=2,\ \sigma(E)=a.}
\tag{28}
\]

后一情形恰落入 (20) 的第二支，因为
\(Z\setminus A\) 是长度 \(3p-4\) 的秩三原子。特别地，若
\(\pi(Z\setminus C)\) 本身是长度 \(3p-2\) 的原子，则 (28)
只能走第一支。

### 5.6 二项 \(a\) 块强制两点横截

若存在二项 \(a\) 块 \(E=\{x,y\}\)，则 (23) 说明它横截整个
\(\mathcal F_3\)。按 \(3a\) 块与 \(E\) 的交分成“只含 \(x\)”、
“只含 \(y\)”和“同时含二者”三类，记其 \((-1)^{|A|-1}\) 带符号
总数为 \(s_x,s_y,s_{xy}\)。由总带符号和为零及逐点度 (22)，

\[
\boxed{s_x=s_y=\frac1{20},\qquad s_{xy}=-\frac1{10}.}
\tag{28a}
\]

所以三类均非空；前两类各至少有
\(\lceil(p-1)/20\rceil\) 个块，第三类至少有
\(\lceil(p-1)/10\rceil\) 个块。再将
\(d_3(x,y)=-s_{xy}=1/10\) 代入 (26)，得到

\[
\boxed{d_1(x,y)=1,\qquad d_2(x,y)=-\frac12,\qquad
d_3(x,y)=\frac1{10}.}
\tag{28b}
\]

结合各族总带符号和与两个逐点度，三族相对 \(E\) 的
“不交/只含 \(x\)/只含 \(y\)/同时含二者”四格分布完整为

\[
\begin{array}{c|rrrr}
 &\varnothing&x&y&xy\\ \hline
\mathcal F_1&\frac12&\frac14&\frac14&-1\\
\mathcal F_2&-\frac1{10}&-\frac15&-\frac15&\frac12\\
\mathcal F_3&0&\frac1{20}&\frac1{20}&-\frac1{10}.
\end{array}
\]

其中加上/删去 \(E\) 给出两条真实双射：与 \(E\) 不交的
\(\mathcal F_1\) 块对应包含 \(E\) 的 \(\mathcal F_2\) 块；与
\(E\) 不交的 \(\mathcal F_2\) 块对应包含 \(E\) 的
\(\mathcal F_3\) 块。相应长度上界自动排除前者的六项块和后者的
七项块。

故至少 \(\lceil(p-1)/2\rceil\) 个 \(2a\) 块包含 \(E\)；每个都
唯一分解为 \(E\mathbin{\dot\cup}D\)，其中 \(D\) 是与 \(E\)
不交的 2--5 项 \(a\) 块；另有至少
\(\lceil(p-1)/10\rceil\) 个 \(2a\) 块与 \(E\) 不交。全部二项
\(a\) 块组成的值配对图还满足

\[
\boxed{\nu(\Gamma_a)\le3,\qquad |E(\Gamma_a)|\le3(p-4).}
\tag{28c}
\]

第一式来自“四条不交边加 \(p-4\) 个锚点”的禁用短零和；第二式
再用值配对图分解成完全二部图与半值完全图，并输入高度 \(p-4\)。
更重要地，记与 \(E\) 不交的 \(2a\) 块族为 \(\mathcal D_E\)。
加上 \(E\) 后每个 \(D\in\mathcal D_E\) 都成为 \(3a\) 块，故其
补集是长度 \(3p-4\) 至 \(3p-2\) 的秩三原子；对不同 \(D,D'\)，

\[
\bar\sigma(D\cap D')
=\bar\sigma((E\dot\cup D)\cap(E\dot\cup D'))\ne0.
\tag{28d}
\]

所以第二支强制至少 \(\lceil(p-1)/10\rceil\) 个两两非零商交的
4--6 项 \(2a\) 块，以及同样多的同时近 Davenport 补原子。
因此 (20) 的第二支不只是一个孤立二项块，而会强制精确两点横截、
线性多的同点对 \(2a/3a\) 块、稀疏的全局值配对图与一个多补原子
交换系统。

### 5.7 极值补原子的双边短表示恒等式

现在进入 (20) 的第一支：固定六项 \(2a\) 块 \(C\)，令
\(B=Z\setminus C\)，并假设 \(\bar B=\pi(B)\) 是
\(\bar G=G/H\cong C_p^3\) 中长度 \(3p-2\) 的原子。
对任意位置 \(b\in B\)，写

\[
U_b=B\setminus\{b\},\qquad |U_b|=3p-3.
\]

\(\bar U_b\) 是极大长度的零和自由序列。在
\(\mathbb F_p[\bar G]\) 中，增广理想的顶次数为 \(3p-3\)，顶次
部分一维，由全和元 \(J_{\bar G}\) 张成。因此

\[
\prod_{u\in U_b}(1-X^{\bar u})=\gamma_bJ_{\bar G}.
\]

左端在零元处的系数为 \(1\)，因为 \(\bar U_b\) 没有非空零和
子序列；而 \(J_{\bar G}\) 在零元处的系数也是 \(1\)。故

\[
\boxed{\prod_{u\in U_b}(1-X^{\bar u})=J_{\bar G}.}
\tag{29}
\]

特别地，每个商目标的全部子集表示带符号和都恰为 \(1\)。

任取非空真位置子集 \(T\subset C\)，令 \(t=|T|\in\{1,\ldots,5\}\)。
对任意满足

\[
E\subseteq U_b,\qquad \bar\sigma(E)=-\bar\sigma(T)
\]

的表示，令

\[
K=E\mathbin{\dot\cup}T,\qquad
K'=(U_b\setminus E)\mathbin{\dot\cup}\{b\}
   \mathbin{\dot\cup}(C\setminus T).
\]

两者非空、商和为零，并恰好分割 \(Z\)。其中至少一侧长度不超过
\((3p+4)/2\le2p+2\)，故由 (SQ) 其实际和属于
\(\{a,2a,3a\}\)。第 2 节的原子线长度界再把该侧长度压到至多
\(8\)。于是每个 \(E\) 必且只可能落在两个互不相交的长度边缘之一：

\[
\boxed{
|E|\le8-t
\qquad\text{或}\qquad
|U_b\setminus E|\le t+1.}
\tag{30}
\]

记

\[
L_{\le m}^{U}(x)=
\sum_{\substack{F\subseteq U,\ |F|\le m\\\bar\sigma(F)=x}}(-1)^{|F|}.
\]

在第二个边缘中以 \(F=U_b\setminus E\) 换元。由于
\(|U_b|=3p-3\) 为偶数、\(\bar\sigma(U_b)=-\bar b\)，(29)--(30)
给出逐位置、逐真子集的精确恒等式

\[
\boxed{
L_{\le8-t}^{U_b}(-\bar\sigma(T))
+
L_{\le t+1}^{U_b}(\bar\sigma(T)-\bar b)=1.}
\tag{31}
\]

这已经把无界的群环表示真正压到常数长度。特别地，对每个
\(b\in B,c\in C\)，分别取 \(T=\{c\}\) 与
\(T=C\setminus\{c\}\)，得到

\[
\begin{aligned}
L_{\le7}^{U_b}(-\bar c)+L_{\le2}^{U_b}(\bar c-\bar b)&=1,\\
L_{\le3}^{U_b}(\bar c)+L_{\le6}^{U_b}(-\bar c-\bar b)&=1.
\end{aligned}
\tag{32}
\]

所以每个位置对 \((b,c)\) 都强制一个“七项表示/二项交换”二分，
并同时强制一个“三项表示/六项交换”二分。这里的等式是
\(\mathbb F_p\) 中的带符号等式；非零项给真实短表示，但不能偷换成
正计数或唯一表示。

### 5.8 二次量级补原子与四次量级交换网络

逐点真实度下界还无条件强制大量 \(3a\) 块。令
\(m_3=\lceil(p-1)/20\rceil\)。由

\[
(3p+4)m_3\le\sum_{A\in\mathcal F_3}|A|le8|\mathcal F_3|,
\]

得到

\[
\boxed{|\mathcal F_3|\ge
M_p:=\left\lceil\frac{(3p+4)m_3}{8}\right\rceil.}
\tag{32a}
\]

每个块的补集都是长度 \(3p-4\) 至 \(3p-2\) 的秩三原子，所以每个
\(Z\) 实际同时携带 \(\Omega(p^2)\) 个近 Davenport 补原子。

对不同 \(A,A'\in\mathcal F_3\)，写
\(I=A\cap A'\)、\(J=A\setminus A'\)、\(K=A'\setminus A\)。
则 \(J,K\ne\varnothing\)、\(\bar\sigma(I)\ne0\)，且

\[
\bar\sigma(J)=\bar\sigma(K),
\qquad2\le|J|+|K|\le14.
\tag{32b}
\]

任取 \(J_0\subseteq J,K_0\subseteq K\) 具有相同商和，交换块

\[
P=I\dot\cup J_0\dot\cup(K\setminus K_0)
\]

满足 \(|P|\le15\le2p+2\)。由 (SQ) 及正系数长度界，

\[
\boxed{\sigma(P)=\lambda a,\qquad
\lambda\in\{1,2,3\},\qquad |P|\le5+\lambda.}
\tag{32c}
\]

所以每个块对的二至十四项差关系要么自身是商群原子，要么每个真
零和子关系都会产生第三个受控短块。这形成至少
\(\binom{M_p}{2}=\Omega(p^4)\) 个块对索引的交换实例；不主张对应
有符号序列彼此不同。

### 5.9 已有三项、四项 \(a\) 块的特殊删除线

任取 \(D\in\mathcal F_1\)、\(|D|=t\)，考虑

\[
g_D(X)=c_{Z\setminus D}((X-1)a).
\]

除原子性给出的 \(g_D(0)=(-1)^{t+1}\)、\(g_D(1)=1\) 外，
\(D\) 横截全部 \(3a\) 块还给出额外零点 \(g_D(-3)=0\)。把七点
支撑的公共因子除去后，余因子次数至多 \(t-1\)。当 \(t=3\) 时
三个数据唯一确定余因子，因而

\[
\boxed{
\sum_{\substack{A\in\mathcal F_2\\D\subset A}}(-1)^{|A|-1}
=-\frac32,
\qquad
\sum_{\substack{A\in\mathcal F_3\\D\subset A}}(-1)^{|A|-1}
=\frac12.}
\tag{32d}
\]

所以每个三项 \(a\) 块至少包含于

\[
\left\lceil\frac{p-3}{2}\right\rceil
\quad\text{个 }2a\text{ 块，及}\quad
\left\lceil\frac{p-1}{2}\right\rceil
\quad\text{个 }3a\text{ 块。}
\tag{32e}
\]

当 \(t=4\) 时只剩一个混合关系。若

\[
d_r(D)=\sum_{\substack{A\in\mathcal F_r\\D\subset A}}(-1)^{|A|},
\]

则

\[
\boxed{3d_2(D)+5d_3(D)=-1.}
\tag{32f}
\]

当 \(t\ge5\) 时，同一三点插值数据允许在 \(2,3\) 处自由赋值，
不再产生关系。完整推导及固定二项块后的分长度 Hasse 系统见
`proofs/special_f1_deletion.md`；后者仍有两个自由参数，不能单独
强迫含该二项块的六项 \(2a\) 块。

### 5.10 第二支的共横截菱形

固定二项 \(a\) 块 \(E\)，若多个六项块写成

\[
C_i=E\mathbin{\dot\cup}D_i\in\mathcal F_2,
\qquad |D_i|=4,
\]

则不同花瓣 \(D_i,D_j\) 必相交，而且
\(\bar\sigma(D_i\cap D_j)\ne0\)。若 \(C_i\) 走 (20) 的第二支，
伴随二项块 \(P_i\) 形成

\[
C_i'=D_i\mathbin{\dot\cup}P_i\in\mathcal F_2,
\qquad
A_i=E\mathbin{\dot\cup}C_i'\in\mathcal F_3,
\qquad |A_i|=8,
\tag{32g}
\]

且 \(Z\setminus A_i\) 是长度 \(3p-4\) 的商群原子。仅当
\(A_i\ne A_j\) 时，才可由不同 \(3a\) 块的商交定理推出
\(\bar\sigma(C_i'\cap C_j')\ne0\)。全部伴随边 \(P_i\) 在
\(Z\setminus E\) 上的匹配数至多二、边数至多 \(2(p-4)\)；固定
\(C_i\) 的两条不同伴随边必须相交，但不必唯一。

`route_a_second_branch_models.md` 对每个 \(p\ge7\) 构造了线性多个
共 \(E\) 菱形的实际群值局部模型：补原子、非零商交及高度
\(p-4\) 均相容，而任意花瓣交换差都只是两个相同实际值位置形成的
小原子。该模型不实现完整 \(Z\) 原子或 Hasse 设计，因此只说明
“共 \(E\) 菱形加局部补核”仍不足，下一步必须输入全局设计。

### 5.11 标准极值商原子的固定六点模板

若极值补原子的商标号恰为

\[
B=e_1^{p-1}e_2^{p-1}e_3^{p-1}g,
\qquad g=e_1+e_2+e_3,
\]

则已有一个真正的无限固定模板排除。对 \(p\ge11\) 取

\[
C=(e_1,e_2,e_3,g,g,-3g).
\]

同一 \(B_{e_i}\) 值类内任意位置对都不可能共同落入长度至多七的
商零和块，故 \(d_1=d_2=0\)，与
\(8d_1+10d_2=3\) 矛盾。\(p=7\) 时对同一模板的完整轨道系统有
秩差 \(66<67\)，十三项稀疏证书给出 \(0=1\)；另一个模板
\((\pm e_1,\pm e_2,\pm e_3)\) 也有秩差 \(54<55\)。

这些结论只排除所列标准 \(B\) 与固定 \(C\)，不分类任意六点
\(C\) 或任意极值原子。详见 `route_a_standard_atom_templates.md`。

### 5.12 二/三项小块与纯四项—八项分岔

把全局长度 Hasse 系统改用 \(N_{1,2}\) 作自由参数，可得

\[
N_{1,3}=\frac23N_{1,2},\qquad
N_{1,4}=-\frac52-\frac32N_{1,2},\qquad
N_{3,8}=\frac7{10}+\frac12N_{1,2}
\pmod p.
\tag{32h}
\]

若实际没有三项 \(a\) 块，则 \(N_{1,2}\equiv0\pmod p\)，并有

\[
N_{1,4}\ge\frac{p-5}{2}.
\tag{32i}
\]

每个四项 \(a\) 块 \(D\) 只能向六项 \(2a\) 块或八项 \(3a\) 块
扩张。若两种扩张数分别为 \(x_D,z_D\)，特殊删除关系化为

\[
3x_D+5z_D\equiv-1\pmod p,
\qquad
x_D+z_D\ge\left\lceil\frac{p-1}{5}\right\rceil.
\tag{32j}
\]

故四项到六项/八项层已有平方级合计关联。若进一步没有二项
\(a\) 块，则所有 \(x_D=0\)，从而

\[
N_{3,8}\ge
\left\lceil
\frac{(p-5)\lceil(p-1)/5\rceil}{140}
\right\rceil;
\tag{32k}
\]

\(p=7\) 时还可提升为 \(N_{3,8}\ge7\)。同一无二/三项假设使所有
强制六项 \(2a\) 块都走长度 \(3p-2\) 的极值补原子第一支，数量
至少 \(\lceil(p+1)/5\rceil\)。完整三支分岔见
proofs/small_a_block_dichotomy.md。

### 5.13 绝大多数 \(F_3\) 块对不能退化为单点替换

称两个 \(F_3\) 块二位置退化，若它们只把一个位置替换成承载同一
实际群值的另一个位置。固定一个块时，这样的邻块至多
\(8(p-5)\) 个，因为每个实际值重数至多 \(p-4\)。所以全部退化
块对至多

\[
4(p-5)|\mathcal F_3|.
\tag{32l}
\]

结合 \(|\mathcal F_3|\ge M_p\)，任取 \(M_p\) 个块，其中至少

\[
\binom{M_p}{2}-4(p-5)M_p
=\frac9{51200}p^4+O(p^3)
\tag{32m}
\]

个块对非二位置退化；显式左端对 \(p\ge431\) 为正。更小的存在
阈值来自 Johnson 图团分类：若全部块对都是单点替换，则无公共点
迫使块数至多九；故 \(p\ge23\) 时已经至少有一个非退化块对。

这排除了局部菱形模型作为真实四次量级网络的主导机制：渐近上只有
\(O(p^{-1})\) 比例的块对可如此退化。但其余三至十四项交换关系仍
可能整体是有符号原子，尚未得到真子交换。详见
proofs/f3_nondegenerate_pairs.md。

### 5.14 标准原子的三点过滤器与 \((\pm2e_i)\) 模板关闭

对标准 \(B\) 和任意六点商零和 \(C\)，三点覆盖给出一个精确必要
过滤器。固定方向 \(i\)，令 \(A\subset C\)、\(|A|=k\le5\)，并写
\(\bar\sigma(A)=\sum_jt_je_j\)。要覆盖同一 \(B_{e_i}\) 值类内的
三个位置，至少必须有下列一种情形：

\[
\begin{array}{ll}
\varepsilon=0:&
t_i\ge3,\quad t_j\ge0,\quad \sum_jt_j\le k+2;\\
\varepsilon=1:&
t_i\ge4,\quad t_j\ge1\ (j\ne i),\quad \sum_jt_j\le k+4.
\end{array}
\tag{32n}
\]

该条件在商候选层也是充分的。对

\[
C=(\pm2e_1,\pm2e_2,\pm2e_3),
\]

它却失败：任何含三个 \(B_{e_i}\) 位置、长度至多八的候选块，其
第 \(i\) 个整数坐标落在 \([1,9]\)，对 \(p\ge11\) 不可能模 \(p\)
为零。因此这个六点模板已经被三点覆盖对所有 \(p\ge11\) 完整排除，
不需要高度对称假设。

二点接口本身仍值得作为方法审计：它可压成三个循环群上的高度
pair-sum 方程；三方向对称时 \(p=11,13\) 的全部重数向量均无解。
但这个有限结论现已被上述全称三点证书严格加强。三点候选过滤器
也未分类任意 \(C\)：模板
\((\pm3e_1,\pm3e_2,\pm3e_3)\) 可同时越过三个方向，下一步必须输入
高度三元和及带符号三点方程。详见
proofs/standard_atom_triple_filter.md 与
route_a_standard_atom_pair_system.md。

这一步现已完成：八项候选先排除 \(\pm3e_i\)，继而同一高度纤维
机制与大幅度三点无候选相结合，排除了任意非零且彼此可以不同的
三轴幅度模板

\[
C=(\pm k_1e_1,\pm k_2e_2,\pm k_3e_3).
\]

详见 proofs/standard_atom_coordinate_pairs.md。该结论仍未分类不支撑
在三条基轴上的任意六点 \(C\)。

### 5.15 全部近极值补原子的满商纤维排除

对任意 \(A\in\mathcal F_3\)，令 \(B=Z\setminus A\)。已有结论说明
\(\bar B\) 的长度属于 \(\{3p-4,3p-3,3p-2\}\)，且是商群原子。若
\(p\ge11\) 且某个非零商值 \(q\) 在 \(B\) 中恰出现 \(p-1\) 次，
从该纤维任取三个位置并用三点覆盖得到短块 \(E\)。原子性迫使
\(E\) 跨越 \(B\mid A\)，故若 \(b\) 是其中的 \(q\)-位置数，则

\[
4\le |E|\le8,
\qquad3\le b\le |E|-1.
\]

固定其余位置并任意替换这 \(b\) 个同商位置，仍得到同长度商零和
块。实际长度窗把全部 \(b\)-位置高度和压入大小依次为

\[
2,2,3,2,1\qquad(|E|=4,5,6,7,8)
\]

的集合。另一方面，这 \(p-1\) 个位置中每个高度的重数至多
\(p-4=(p-1)-3\)。有限值子集和引理对上述全部参数给出矛盾。因此

\[
\boxed{v_q(B)\le p-2
\quad\text{对每个 }A\in\mathcal F_3\text{、每个商值 }q.}
\tag{32o}
\]

特别地，标准极值商原子含有重数 \(p-1\) 的值，所以对 \(p\ge11\)
它与任意六点 \(C\) 都不可能；这里已经不再需要分类 \(C\)。该结论
同时约束交换网络中的全部 \(\Omega(p^2)\) 个近 Davenport 补原子。
详见 proofs/standard_atom_full_exclusion.md。

### 5.16 临界 \(p-2\) 商纤维分类与锚点闭合

继续设 \(p\ge11\)，固定任意 \(T\in\mathcal F_3\)，并令
\(B=Z\setminus T\) 为相应近 Davenport 商原子。若某个商值 \(q\)
在 \(B\) 中出现 \(p-2\) 次，把该位置纤维记为 \(X\)。从
\(\binom X3\) 中任取三点；同商替换与实际长度窗排除长度
\(4,5,7,8\) 的覆盖块，所以每个覆盖块都恰有六项，其中
\(X\)-位置数 \(b\in\{3,4,5\}\)。

六项块把全部 \(b\)-位置高度和限制在一个循环连续三值集内。高度
重数上界 \(p-4\) 与有限子集和分类于是只允许

\[
h^{p-4}(h+1)^2,\qquad
h^{p-4}(h-1)^2,\qquad
h^{p-4}(h-1)(h+1).
\tag{32p}
\]

令 \(M_b\) 为长度 \(6-b\)、商和 \(-bq\) 且位于
\(Z\setminus X\) 的余部数。逐三点带符号 Hasse 方程分别唯一给出

\[
(M_3,M_4,M_5)\equiv
\frac{(21,7,1)}{20},\quad
\frac{(21,7,1)}4,\quad
\frac{(21,7,1)}{10}
\pmod p.
\tag{32q}
\]

\(b=5\) 的余部是 \(T\) 中承载同一实际群值的单点，故
\(1\le M_5\le\min\{|T|,p-4\}\le8\)。当 \(p\ge13\) 且
\(M_5\ge2\) 时，可在两个不同余部点上构造不交的一倍、三倍六项
块，违反 \(\mathcal F_1\pitchfork\mathcal F_3\)。因此全部
\(p\ge11\) 情形只剩

\[
\begin{array}{c|c|c}
p&X\text{ 的高度型}&(M_3,M_4,M_5)\pmod p\\ \hline
11&h^7(h+1)^2&(6,2,5)\\
11&h^7(h-1)^2&(8,10,3)\\
19&h^{15}(h+1)^2&(2,7,1).
\end{array}
\tag{32r}
\]

事实上无需先筛到 (32r)。对正异常型，任一含异常点的短块在
\(X\)-交数一、二及至少三的全部情形中都只能属于
\(\mathcal F_2\cup\mathcal F_3\)，故该点的
\(\mathcal F_1\) 带符号点度为零，与 \(-3/4\) 矛盾。负异常型
同理缺失 \(\mathcal F_3\)，与点度 \(-1/20\) 矛盾；对称异常型
同时含这两种缺族点。等价地，取两个异常点后，所有含该对的短块
只落在单一倍数族，直接违反两条逐对共度恒等式。

作为独立交叉验证，(32r) 的三个余支还能使用冻结反例中外置的
\(a^{p-4}\) 锚点闭合。令
\(Y\subset T\) 为全部 \(b=5\) 的单点余部，\(T_0=T\setminus Y\)。
三行中 \(Y\) 的实际值分别是 \(a-5x,3a-5x,a-5x\)。精确选择给出：

\[
\begin{array}{c|c|c}
(p,\text{型})&\text{加入 }T_0\text{ 的位置}&\text{总和}\\ \hline
(11,+)&7x+(x+a)+a&33x=0\\
(11,-)&7x+6a&22x=0\\
(19,+)&12x+2(x+a)+15a&19x+19a=0.
\end{array}
\tag{32s}
\]

三条位置子序列的长度分别至多 \(12,18,36\)，均严格小于对应的
\(3p-2\)，与冻结反例矛盾。因此

\[
\boxed{v_q(B)\le p-3
\quad(p\ge11,\ T\in\mathcal F_3,\ B=Z\setminus T).}
\tag{32t}
\]

详见 proofs/p_minus_two_height_fibre.md、
proofs/p_minus_two_residual_degree_system.md 与
proofs/p_minus_two_survivor_refinement.md。

### 5.17 临界 \(p-3\) 商纤维也被异常点度关闭

继续假设某个商值在 \(B\) 中出现 \(m=p-3\) 次。此时实际高度
重数上界恰为 \(p-4=m-1\)。任取纤维三点并固定其覆盖短块的余部，
同商替换给出如下完整高度清单：

\[
\begin{array}{c|c}
\text{覆盖块长度}&\text{可能高度多重集}\\ \hline
4,5,7&h^{p-4}(h\pm1)\\
6&h^{p-4}(h+d),\ d\in\{\pm1,\pm2\};\\
 &h^{p-5}(h+1)^2,\ h^{p-5}(h-1)^2,
   h^{p-5}(h-1)(h+1)\\
8&\text{无}.
\end{array}
\tag{32u}
\]

再固定清单中的任一异常位置，枚举任意短块与该纤维的交数
\(c=1,\ldots,7\)。正异常位置从不属于 \(\mathcal F_1\)，负异常
位置从不属于 \(\mathcal F_3\)；差为 \(\pm2\) 时甚至只能落入
长度六的极端倍数族。这分别与固定点度
\(-3/4\) 和 \(-1/20\) 矛盾。因此

\[
\boxed{v_q(B)\le p-4
\quad(p\ge11,\ T\in\mathcal F_3,\ B=Z\setminus T).}
\tag{32v}
\]

这里 \(p=11,b=7,|E|=8\) 的端点也被单值长度窗排除。下一层
\(v_q(B)=p-4\) 与冻结的实际重数上界相等，允许整个商纤维只有
一个实际高度；这正是有限子集和方法首次真正失去异常点的边界。
详见 proofs/p_minus_three_height_frontier.md。

### 5.18 首个退化边界：\(p-4\) 单高度纤维的余部设计

继续固定 \(T\in\mathcal F_3\)、\(B=Z\setminus T\)，并设某个非零
商值 \(q\) 在 \(B\) 中恰有 \(m=p-4\) 个位置。对 \(p\ge13\)，
三点覆盖的同商替换先把任何非单高度轮廓压成一个或两个距离至多二
的异常点，随后异常点再次缺失 \(\mathcal F_1\) 或
\(\mathcal F_3\)。\(p=11\) 的 1768 个七点高度轨道则由完整
98 行逐位置 Hasse 星系统压到 \(0^7\) 与 \(0^6(-1)\)；唯一负异常
型强制五个同值单点尾 \(y=-7x+4a\)，而
\(3x+2y+3a=0\) 是八项锚点零和。故对所有 \(p\ge11\)，等号纤维
必代表同一实际值 \(x\)，可记为 \(X=x^{p-4}\)。这是实际重数
上界首次允许的饱和情形。

若短块 \(A\in\mathcal F_\lambda\) 与 \(X\) 的交数为 \(b\)，写
\(\ell=|A|\)、\(U=A\setminus X\)。补原子性和单高度替换给出

\[
U\cap T\ne\varnothing,\qquad
|U|=\ell-b,\qquad
\bar\sigma(U)=-bq,\qquad
\sigma(U)+bx=\lambda a,
\tag{32w}
\]

并且同一个 \(U\) 生成全部 \(\binom Xb\) 个块
\(V\mathbin{\dot\cup}U\)。令 \(N_{\lambda,\ell,b}\) 为满足
(32w) 的余部数，则逐 \(X\)-点、对、三元组的 Hasse 恒等式化成

\[
\sum_{\ell,b}(-1)^{\ell-1}
 \binom{p-5}{b-1}N_{\lambda,\ell,b}
=\left(-\frac34,\frac3{10},-\frac1{20}\right)_\lambda,
\tag{32x}
\]

\[
8D_1+10D_2=3,\qquad 2D_1-10D_3=1,
\qquad
4\Delta_1+10\Delta_2+20\Delta_3=-1,
\tag{32y}
\]

其中 \(D_\lambda\)、\(\Delta_\lambda\) 分别使用系数
\((-1)^\ell\binom{p-6}{b-2}\) 与
\((-1)^{\ell-1}\binom{p-7}{b-3}\)。特别地，含固定
\(X\)-三元组的全部块只有

\[
\begin{array}{c|c|c}
\lambda&\ell&b\\ \hline
1&4,5,6&3\le b\le\ell-1\\
2&4,5,6,7&3\le b\le\ell-1\\
3&6,7,8&3\le b\le\ell-1.
\end{array}
\tag{32z}
\]

余部还继承短块相交性：若相应族对属于
\((1,3),(2,2),(2,3),(3,3)\) 且 \(b+b'\le p-4\)，则
\(U\cap U'\ne\varnothing\)。更精确地，对两个不同的三倍余部，
若 \(k\) 遍历两个 \(X\)-核心的全部可实现交数，则
\(\bar\sigma(U\cap U')\ne-kq\)；这同时记录了所有可能的核心
交叠，而不只记录 \(k=0\)。事实上每个 \(b\ge1\) 的三族余部都有
\(\varnothing\ne U\cap T\subsetneq T\) 且
\(\bar\sigma(U\cap T)\ne0\)。若 \(b\le p-12\)，余部 \(U\) 必须横截整个
\(\mathcal F_3\)；这在 \(p\ge19\) 时排除了所有单点余部。

外置 \(a^{p-4}\) 锚点还能严格加强小余部限制。纯落在 \(T\) 中的
三倍余部在 \(b\ge4\) 时不存在，\(b=3\) 时不能有两个不交者；
所有三倍单点余部均不存在。二倍单点余部通常至多一个，唯一例外
\((p,b)=(11,6)\) 时至多两个；一倍单点余部的上界为二或三，精确
例外见 proofs/p_minus_four_single_height_probe.md。

混合 Hasse 进一步逐外点 \(y\in Z\setminus X\) 强制一点、
\(\{x,y\}\) 二点和 \(\{x_1,x_2,y\}\) 三点方程；它排除了最初的
六变量稀疏证书，并证明每个外点都进入某个 \(b\ge2\)、大小至多六
的余部。对 \(p\ge19\)，这些余部全是 \(\mathcal F_3\) 横截，故
至少有 \(\lceil(2p+8)/6\rceil\) 个不同余部。

对两个不同三倍余部 \(U,U'\)，令
\(k_0=\max(0,b+b'-(p-4))\)。两个 \(X\)-核心的全部交换自由度可
无损压缩为

\[
-b+k_0\le d\le b'-k_0.
\tag{32za}
\]

每个满足等商差条件的尾差子集交换都会生成第三个短块余部，并再次
满足正确族别、长度窗、非零 \(T\)-部分及全部可实现核心交数禁值。
由 \(Z\) 的原子性还有一个不经过 Hasse 矩的新排除：若
\(U'\subsetneq U\)，则 \(b'-b\in\{1,2,3\}\)；反向包含同理。
因此较大余部必须有严格更小的核心，且差只能为一至三。

这并非只对“碰巧存在的两条尾”施加条件。固定任一 \(X\)-位置，
三族非零带符号点度各自强迫一条正核心余部；商和先唯一确定核心数，
实际和再唯一确定族别，所以可选到三个身份两两不同的余部
\(U_1,U_2,U_3\)。当 \(p\ge17\) 时，核心数上界
\(b_1\le5,b_2\le6,b_3\le7\) 与跨族相交性还给出

\[
U_1\cap U_3\ne\varnothing,
\qquad U_2\cap U_3\ne\varnothing.
\tag{32zb}
\]

两组必需的 \(F_1/F_2\)--\(F_3\) 交换也有与 (32za) 同样的精确
核心、尾和长度公式；新块的实际缺陷只能为 \(-2,-1,0\)，分别决定
其进入 \(F_1,F_2,F_3\)，并继承 \(T\)-部分与商交约束。这里已单列
\(b^*=0\) 以及新块恰为 \(T\) 时不能误用非零交的边界。

正核心三倍余部本身还不能稀少。若其普通实际尾数为 \(K\)，固定
一个 \(X\)-点的第三族点度同余可提升为一个非零整数 \(p\) 倍数；
删除已排除的单点尾后，每尾整数权绝对值至多 126，因此

\[
\boxed{K\ge\left\lceil\frac{p-1}{2520}\right\rceil.}
\tag{32zc}
\]

若更强地假设 \(K=1\)，十五个可能尾型的固定整数分解把素数精确
限制到

\[
\{11,13,19,23,43,101,233,467,701,1399,2521\}.
\tag{32zd}
\]

所以在 (32zd) 外至少有两条不同三倍余部，(32za) 的二尾闭包不再
是条件命题。唯一尾若存在，还必须横截整个 \(F_3\) 族，而每个尾点
都被某个零核心 \(F_3\) 块避开。位置级加强进一步证明：若
\(b\ge4\)，任何零核心块都不能包含整个唯一尾；二点尾因而与逐点
总迹入射矛盾。故
\[
(467,7,5),\quad(701,6,4),\quad(2521,8,6)
\tag{32ze}
\]
三型全部排除，16 型余 13 型，(32zd) 的十一项素数余
\(11,13,19,23,43,101,233,701,1399\) 九项。

把十一项异常素数对应的 16 个 \((p,\ell,b)\) 类型逐一代入零阶、
纯 \(X\)、在 \(T\) 求和及在 \(Q=Y\setminus T\) 求和的全部 21 条
安全聚合 Hasse 必要式，仍没有排除任何类型。对每个允许的
\((s,j)\)，代入唯一尾后 90 个自由 \(N,J\) 变量的系数秩与增广秩
都为 20，故解空间维数 70。这里从未除以 \(|Q|\)，特别覆盖
\(s=8\) 时 \(|Q|\equiv0\pmod p\) 的边界。规范解只是有限域聚合
证书，不实现普通非负入射、实际尾位置或补原子；它本身没有排除
类型，但随后的位置级论证已排除 (32ze)。

这些条件仍未闭合单高度纤维。事实上，按
\((\lambda,\ell,b)\) 聚合的纯 \(X\) 点、对、三点方程即使删除全部
单点余部仍有显式模 \(p\) 解；另一个五点余部稀疏解还同时避开
大素数的单点横截禁令。这些只是非负计数剩余类，不实现统一商标号、
逐余部相交网络或补原子，故也不是反例；而尊重 \(T\mid Q\) 分区、
全部逐外点混合方程且无单点余部的加权解也仍存在。两个不同三倍
余部的交换闭包现已逐差集完整写出，但一个同值双位置形式赋值仍
满足命名二尾接口；它没有重建全诱导短谱或构造 \(T,B,Z\)，故不是
局部候选。三条必需跨族余部也有一个共 \(T\)-点形式赋值，使两组
命名交换只剩空/满端点；它同样未重建全短谱或补原子。即使
(32zc) 已强迫线性多个三倍余部，单个二尾接口的退化仍须在全局中
同时排除。实际尾包含偏序现已证明链长至多三、宽度至少
\(\lceil(p-1)/7560\rceil\)、可比异尾对至多 \(112K\)，每条三链
还补成实际菱形；但 21 条聚合 Hasse 对任意固定多尾只余原有第三族
\(X\)-点度条件。严格停止线因此推进为逐外点 \(0/1\) 入射、全诱导
短块谱、统一商标号与完整补原子内部子和的联立，并另处理余下 13 个
唯一尾型。固定同一余部内部的替换只产生二位置同值退化，不会给出
新矛盾。

详见 proofs/p_minus_four_height_reduction.md、
proofs/p11_seven_fibre_star_exclusion.md、
proofs/p_minus_four_monochromatic_frontier.md、
proofs/p_minus_four_single_height_probe.md 与
proofs/p_minus_four_star_design.md、
proofs/p_minus_four_mixed_hasse_frontier.md、
proofs/p_minus_four_two_tail_exchange.md、
proofs/p_minus_four_cross_family_tails.md、
proofs/p_minus_four_unique_f3_tail_arithmetic.md、
proofs/p_minus_four_unique_f3_tail_hasse.md、
proofs/p_minus_four_unique_tail_position_frontier.md 与
proofs/p_minus_four_multi_tail_global.md。

### 5.19 \(p=7\) 的高纤维排除与三、四重投影

在 \(p=7\) 时，前述大素数有限值引理缺少交换位置，不能直接套用。
但纤维大小至多六、每个实际高度重数至多三，可以对高度多重集按
整体平移与位置置换作完全轨道化。

对六重纤维共有 104 个高度轨道。每个实际余部按
\((\ell,b,c)\) 生成完整同商替换星；把三族逐点方程、两条逐对式
和逐三点式同时保留，得到 68 行 \(\mathbb F_7\) 线性系统。
95 个轨道只有吞下几乎整个纤维的列，直接缺失 \(\mathcal F_1\)
点入射；其余九个轨道均有逐列核对的稀疏 \(0=1\) 证书。因此六重
纤维不存在。

五重纤维有 59 个高度轨道。放宽的 Hasse 星系统本身均相容，但
每个解都迫使某个单点余部变量取模 \(7\) 剩余 \(4,5,6\)。固定
\((\ell,b,c)\) 的单点余部全是 \(T\) 中同一个实际群值，普通重数
至多三，所以其余部数只能取 \(0,1,2,3\)，再次矛盾。故

\[
\boxed{
p=7\Longrightarrow
\max_q v_q(Z\setminus T)\le4
\quad(T\in\mathcal F_3).}
\tag{32aa}
\]

重数三、四仍有 12+29=41 个高度轨道；把全部单点余部形式变量
置零后，对应的放宽星系统也都相容（这只是形式切片，不是真实
必要条件）。四重的 29 个轨道还能继续精确二分：
除 \(0^3 1\) 外的 28 型都强迫全核心 \(F_3\) 余部，且
\(N_6-N_7+N_8\equiv6\pmod7\)；例外型若无全核心块，则
\(b=1,2,3\) 三个迹层各强迫至少一个余部。第一个旧例外标签候选
因同批位置诱导两个零商交的嵌套 \(F_3\) 块而被撤回；第二个 16 点
候选又诱导 31 个非法短谱和 93 个已指定 \(B\)-内商零子集。两个
候选均拒绝，仿射投影不受影响。
三重的 12 个轨道中，
11 型都强迫全核心 \(F_3\) 余部并满足同一关系；单高度型不强迫
全核心尾，但九列精确投影仍强迫某个 \(F_3\) 尾。故 \(p=7\) 的
剩余对象分别收紧为四重的 21 个外部位置、84 个标量和三重的
22 个外部位置、88 个标量的带标签有限 CSP。三重层已有严格 25
位置赋值核验器与一个固定 \(B\) 商原子骨架；其实际 \(Z\)-原子
抬升被二项 \(b=0\)、高度五的非法短谱拒绝，尚非全空间无解证书。
详见 proofs/p7_six_fibre_exclusion.md、
proofs/p7_four_fibre_refinement.md、
proofs/p7_four_fibre_tail_local_state.md、
proofs/p7_three_fibre_refinement.md 与
proofs/p7_three_fibre_labelled_csp.md。

## 6. \(3p+1\) 层的二选一结构

若 \(|Z|=3p+1\)，则 \(c_Z|_H\) 次数至多 \(p-5\)、为偶函数、在七点集
外消失且在零点取值 2。因此

\[
c_Z(Xa)=Q(X)(\alpha X^2+\beta),\qquad \beta Q(0)=2.
\tag{33}
\]

二次偶因子至多在 \(1^2,2^2,3^2\) 中消去一个，所以
\(c_Z(a),c_Z(2a),c_Z(3a)\) 至少两个非零。对应的小表示范围为

\[
a:2\text{--}3,\qquad2a:4,\qquad3a:4\text{--}5.
\tag{34}
\]

每个出现的 \(3a\) 表示仍有秩三原子补集。

## 7. 当前最小缺口

路线 A 已从“任意目标需要长度控制”推进到一个有限宽度的实际结构问题：

> 对每个 \(3p+3\) 原子，必须同时实现 (9)，且每个被计数的
> \(3a\) 五至七项表示，其补集都是长度 \(3p-4,3p-3\) 或
> \(3p-2\) 的 \(C_p^3\) 原子。

此外，每个 \(3p+4\) 原子必须同时承载 (22)--(24) 的三族带符号
覆盖、(26) 的逐对共度二分、(26b)--(26f) 的三点定量覆盖与跨界
短块质量，以及 (20)、(28) 的六项 \(2a\) 块补核与厚交叠二分。
若走 (20) 的极值原子支，还必须对每个
\(b\in B\) 和每个非空真 \(T\subset C\) 满足 (31) 的双边短表示
恒等式。

尚缺的是把 (26e)--(26f)、(28a)--(28d)、(31)--(32g) 的大量
常数长度表示、特殊小块扩张与第二支菱形，同四次量级交换网络及
统一商标号核、
高度 \(p-4\) 和 (22)--(28) 的交叠限制结合，排除极值原子支；
并对 (20) 的 \(3p-4\) 原子支建立对应接口。这里已经不再缺任意
目标的长度控制，而只缺把已得到的真短表示组织成实际零和的
交换/重叠定理。

唯一正核心 \(F_3\) 尾的原十一项异常素数也已再经 21 条安全聚合
Hasse 方程逐型测试：16 个 \((p,\ell,b)\) 类型在每个允许的
\((s,j)\) 下均相容，秩为 20、90 个自由坐标中余 70 维。这个
精确负结果说明继续增加只记录尾数与 \(T\)-入射总数的聚合矩不会
关闭异常表；位置级零核心块随后排除三个二点型，余 13 型。多尾
偏序链长三界与聚合秩定理又说明下一层必须保留逐外点实际位置块、
全诱导短谱与补原子。详见
proofs/p_minus_four_unique_f3_tail_hasse.md、
proofs/p_minus_four_unique_tail_position_frontier.md 与
proofs/p_minus_four_multi_tail_global.md。

标准极值商原子对 \(p\ge11\) 已由第 5.15 节对任意六点补块全部
排除；第 5.16 节又先把等号 \(v_q(B)=p-2\) 压到三个
\(p=11,19\) 的局部余支，再由显式锚点短零和全部关闭。故每个
\(p\ge11\) 的近极值补原子先满足 \(v_q(B)\le p-3\)；第 5.17 节
又用同一替换接口和异常点度排除等号，所以最终得到
\(v_q(B)\le p-4\)。第 5.18 节又证明 \(p\ge13\) 的等号纤维必
单高度，并把它压成逐余部设计；纯 \(X\) 及逐外点混合 Hasse 都
仍有加权松弛解，所以当前承重对象已经是两个不同余部之间的统一
商和值、交集禁值与补原子交换。第 5.19 节则把 \(p=7\) 的逐商值
重数压到四，只留下 41 个重数三、四高度轨道的有限多补原子 CSP；
其中四重与三重已分别投影到 21 外点/84 标量和 22 外点/88 标量的
带标签层。
后续不再停留在标准模板分类或单纤维标量矩。

本文没有证明一般 \(A_p\)，也没有排除全部 \(x_0=0\)。
