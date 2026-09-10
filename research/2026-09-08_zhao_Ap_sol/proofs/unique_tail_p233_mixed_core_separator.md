# \(p=233\) 混合目标核分离：至多一个强制非尾点与短表示二分

STATUS: **PROVED_REDUCTION / INDEPENDENT_REVIEW CORRECT /
GLOBAL_INCOMPLETE**

## 1. 目标纤维的强制位置核

仍固定型 \((3)\)、\(|P|=2\) 的 720 个混合长度 outer survivors。
取已经证明存在的 singleton 长八端点 \(Q_i\)，使其 462 个非尾位置

\[
N_i=Q_i\setminus U
\tag{1}
\]

中至少 461 个删点后仍覆盖全部非零 \(\rho\)-目标。

对 \(r\in C_{233}^2\setminus\{0\}\)，定义普通表示族与其非尾强制核

\[
\mathscr R_i(r)=
\{E\subseteq Q_i:\rho(\sigma(E))=r\},
\qquad
\operatorname{Core}_i(r)=
N_i\cap\bigcap_{E\in\mathscr R_i(r)}E.
\tag{2}
\]

长度 \(2p-2\) 投影原子的顶积等于 \(2J\)，故每个 \(r\) 至少有一个
实际表示，(2) 不是空族交。对 \(x\in N_i\)，有

\[
x\in\operatorname{Core}_i(r)
\Longleftrightarrow
r\notin\Sigma\bigl(\rho(Q_i\setminus\{x\})\bigr).
\tag{3}
\]

因此 461 删点定理等价地给出

\[
\boxed{
\left|\bigcup_{r\ne0}\operatorname{Core}_i(r)\right|\le1.}
\tag{4}
\]

这比逐目标“有一个表示”更强：同一个端点的全部非零目标纤维合计
至多有一个强制非尾位置。

## 2. 尾锚定的全局化

当前 \(p=233,b=4\)。下述论证把原尾锚定引理从
\(A\subseteq Q_H\) 扩到任意实际块 \(A\subseteq Y\setminus U\)。

若非空 \(A\subseteq Y\setminus U\) 满足

\[
\rho(\bar\sigma(A))=0,\qquad
\bar\sigma(A)=e q,\qquad e\in\{1,2,3\},
\tag{5}
\]

构造

\[
D_A=X_{b-e}\mathbin{\dot\cup}U\mathbin{\dot\cup}A.
\tag{6}
\]

它是实际商零块，而其补块至少含

\[
p-4-(b-e)=p-b+e-4>8
\tag{7}
\]

个 \(X\)-位置。商零禁窗先迫使补块长度至少 \(2p+3\)，故
\(|D_A|\le p+1\)；若 \(|D_A|\ge9\)，则 \(D_A\) 自身又落入禁窗，
矛盾。所以 \(|D_A|\le8\)。

若 \(|D_A|=8\)，完整短谱把它送入正核心 \(F_3\)。但它的 \(Y\)-尾
为 \(U\mathbin{\dot\cup}A\supsetneq U\)，违反三位置尾的字面唯一性。
因此

\[
|D_A|\le7,\qquad
\boxed{|A|\le4-b+e=e.}
\tag{8}
\]

原证明使用 \(A\subseteq Q_H\) 只为后续原子分解应用；(6)--(8)
本身只需 \(A\subseteq Y\setminus U\)，所以这里没有把端点内部结论
无依据地外推。

## 3. packing 投影不能等于任一尾标签

写两个 packing 位置为

\[
z_+=(c,s),\qquad z_-=(3-c,-s),\qquad s\ne0,
\tag{9}
\]

其中坐标依次为 \((q,\rho)\)。因 \(P\cap Q_i=\varnothing\)，对任意
singleton 端点，设它遗漏的尾标签为 \(w\)，所以对应 \(Q_i\) 内两
尾之和为 \(-w\)。删掉这两个尾位置得到

\[
S_i=Q_i\setminus U\subseteq Y\setminus U,\qquad
\rho(\sigma(S_i))=w.
\tag{10}
\]

若 \(s=\pm w\)，取投影为 \(-w\) 的那个 packing 位置并与整个
\(S_i\) 合并。mixed 条件使这个避尾实际块的商和等于某个
\(e q\)、\(e\in\{1,2,3\}\)，但它有至少 \(2p-4\) 个位置，违反
(8)。三个 singleton 遗漏的尾标签依次为 \(e,f,-e-f\)，故

\[
\boxed{s\notin\{\pm e,\pm f,\pm(-e-f)\}.}
\tag{11}
\]

## 4. mixed 目标只能短表示或被双尾横截

仍取 (9) 中的 \(z_+,z_-\)。因 \(P\cap Q_i=\varnothing\)，对任意

\[
E\in\mathscr R_i(-s),\qquad E\cap U=\varnothing,
\tag{12}
\]

完整 mixed 条件使

\[
\bar\sigma(\{z_+\}\mathbin{\dot\cup}E)=e q
\quad\text{对某个 }e\in\{1,2,3\}.
\tag{13}
\]

把 \(A=\{z_+\}\dot\cup E\) 代入 (8)，得到

\[
\boxed{|E|\le e-1\le2.}
\tag{14}
\]

同理，每个避开 \(U\) 的 \(s\)-表示也至多含两个位置。因此对
\(r\in\{s,-s\}\) 有严格二分：

1. \(r\) 有一个避开 \(U\) 的单点或双点表示；
2. \(Q_i\) 中的两个尾位置横截 \(\mathscr R_i(r)\)，即每个
   \(r\)-表示都至少使用其中一个尾位置。

记两个避尾短表示族为

\[
\mathscr S_i(r)=
\{E\in\mathscr R_i(r):E\cap U=\varnothing\}.
\tag{15}
\]

若 \(\mathscr S_i(s)\) 与 \(\mathscr S_i(-s)\) 都非空，则它们必须
交叉相交：

\[
\boxed{
E\cap F\ne\varnothing
\quad
(E\in\mathscr S_i(s),\ F\in\mathscr S_i(-s)).}
\tag{16}
\]

否则 \(E\dot\cup F\) 是 \(Q_i\) 的非空真投影零子集，违反
\(\rho(Q_i)\) 的原子性。由 (14)，(16) 是两族单点/双点之间的有限
交叉相交约束。

最后，(4) 对两个实际 mixed 目标特别给出

\[
\boxed{
|\operatorname{Core}_i(s)\cup\operatorname{Core}_i(-s)|\le1.}
\tag{17}
\]

## 5. 长七 singleton 强迫一个避尾短表示

若 \(Q_i\) 来自长七 singleton 端点，则 \(|Q_i|=2p-1\)。记它所含
的两个尾标签为基 \(a,b\)，并令

\[
S=Q_i\setminus\{u_a,u_b\},\qquad |S|=2p-3.
\tag{18}
\]

写

\[
c(r)=[X^r]\prod_{z\in S}(1-X^{\rho(z)}).
\tag{19}
\]

该积属于 \(I^{2p-3}\)，故 \(c(xa+yb)\) 是仿射函数。原子性与实际
位置给

\[
c(0)=1,\qquad c(-a)=c(-b)=0,
\tag{20}
\]

从而唯一得到

\[
\boxed{c(xa+yb)=1+x+y.}
\tag{21}
\]

写 \(s=ua+vb\)。于是

\[
c(-s)=1-u-v,\qquad c(s)=1+u+v.
\tag{22}
\]

特征为奇数，所以二者不可能同时为零。非零带符号系数保证存在实际
位置子集；故 \(\mathscr S_i(s)\) 与 \(\mathscr S_i(-s)\) 至少一族
非空。由 (14)，该表示只有一个或两个位置。

把它与对应 packing 单点合并，再按 (6) 加上 \(X_{4-e}\) 与 \(U\)，
会强制产生一条实际商零的长度六或七块：\(e=1\) 因 (14) 与表示非空
不可能；\(e=2\) 时表示恰为单点且总块长七；\(e=3\) 时表示长一或
二，总块长六或七。因此 540 个含一个 singleton 长七的 outer rows
都必须在完整自动短块闭包中携带这类新块。

## 6. 长八 singleton 的二次签名

若 \(Q_i\) 来自长八 singleton，仍令其两尾标签为基 \(a,b\)，但此时

\[
S=Q_i\setminus\{u_a,u_b\},\qquad |S|=2p-4.
\tag{23}
\]

式 (19) 的系数函数现在为二次函数。原子性给

\[
c(0)=c(-a-b)=1,\qquad c(-a)=c(-b)=0.
\tag{24}
\]

所以存在 \(A,B\in\mathbb F_p\) 使

\[
\boxed{
c(xa+yb)=
1-(x-y)^2+A\,x(x+1)+B\,y(y+1).}
\tag{25}
\]

对 \(s=ua+vb\)，若正、负两个目标都没有避尾表示，则必要地
\(c(-s)=c(s)=0\)。把 (25) 分别代入 \((-u,-v)\) 与 \((u,v)\)，
等价于

\[
A u+B v=0,\qquad
A u^2+B v^2=(u-v)^2-1.
\tag{26}
\]

因此：

- 若 \(u=v\ne0\)，(26) 无解；
- 若 \(u=0\)，只有 \(v=\pm1\) 时可能；若 \(v=0\)，只有
  \(u=\pm1\) 时可能；
- 若 \(u,v,u-v\) 都非零，(26) 一般有唯一候选 \((A,B)\)，不能由
  这一层排除。

式 (11) 已经删去坐标 \((0,\pm1),(\pm1,0)\) 的例外。故只要 \(s\)
落在

\[
\langle a\rangle\cup\langle b\rangle\cup\langle a+b\rangle,
\tag{27}
\]

至少一个 mixed 目标就有避尾表示，再由 (14) 压成单点或双点。
对三个 singleton 尾对，(27) 始终就是三条尾方向
\(\langle e\rangle,\langle f\rangle,\langle-e-f\rangle\)。

这没有排除一般位置的 \(s\)：当 \(u,v,u-v\ne0\) 时，二次参数
\((A,B)\) 仍可能同时杀掉两个避尾 signed coefficients。这里非零
系数只作“必有表示”的单向判据；零系数不被误当作“无表示”。

## 7. 可执行分离器

固定真实 endpoint mask 与统一 \(\rho\)-标签后，可以按以下任一见证
拒绝候选：

- 若每个 singleton 长八端点都有至少两个非尾坏删点，则违反 461
  删点定理；
- 对该定理选出的端点，若两个 mixed 纤维的强制非尾核并含至少两个
  位置，则违反 (17)；
- 若 \(s\) 等于任一正负尾标签，则违反 (11)；
- 若某个避尾 mixed 表示长度大于二，则违反 (14)；
- 若正负目标各有一个不交的避尾表示，则违反 (16)；
- 含长七 singleton 的行若没有强制的长度六/七商零块，则违反
  (18)--(22)；三个 singleton 均长八的行中，若 \(s\) 在三条尾
  方向上时同理。这里不要求其余非-singleton 端点也长八。

若这些门都通过，剩余候选被压成“单点/双点交叉相交”或“双尾横截”
两支，再接全部自动短块的实际高度与不交网络。本文尚未载入 720 行的
真实标签实例，因而没有声称删除 outer row；全局 \(A_p\) 仍为
**INCOMPLETE**。
