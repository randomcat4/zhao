# \(p=233\) 单侧 singleton mixed 支的四支撑正规形

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 单侧输入

取当前型 \((3)\)、\(|P|=2\) 切片中的一个长七 singleton 端点。
其长补投影原子 \(Q\) 长 \(2p-1=465\)，含两个尾位置
\(u_e,u_f\)，其中

\[
\rho(u_e)=e,\qquad \rho(u_f)=f,\qquad e,f\text{ 独立}.
\tag{1}
\]

置

\[
S=Q\setminus\{u_e,u_f\},\qquad |S|=2p-3.
\tag{2}
\]

设 packing 的两个非零投影为 \(r,-r\)。考虑 mixed 高度交换引理的
“无双点交换”支：重新选取正负号后，可以假设

1. \(S\) 没有投影和为 \(-r\) 的位置子集；
2. \(S\) 中投影和为 \(r\) 的每个位置子集都是单点。

packing 尾标签排除还给

\[
r\notin\{\pm e,\pm f,\pm(-e-f)\}.
\tag{3}
\]

## 2. 带符号系数变成普通重数

定义

\[
c(t)=[X^t]\prod_{z\in S}(1-X^{\rho(z)}).
\tag{4}
\]

长七 singleton 的已审仿射签名说明：若
\(t=xe+yf\)，则

\[
c(t)=1+x+y.
\tag{5}
\]

写 \(r=\alpha e+\beta f\)。由 \(-r\) 纤维为空，

\[
0=c(-r)=1-\alpha-\beta,
\qquad \alpha+\beta=1.
\tag{6}
\]

于是

\[
c(r)=1+\alpha+\beta=2.
\tag{7}
\]

令 \(m=v_r(S)\)。按单侧假设，\(r\)-纤维的全部实际位置子集只有
\(m\) 个 singleton，每个在 (4) 中贡献 \(-1\)。因此

\[
-m=c(r)=2\pmod {233}.
\tag{8}
\]

最大原子内任一投影标签的重数至多 \(p-1=232\)，故
\(0\le m\le232\)。式 (8) 唯一给出

\[
\boxed{v_r(S)=p-2=231.}
\tag{9}
\]

这里正是因为所有双点表示已经被排除，带符号模 \(p\) 等式才合法地
恢复成普通重数；一般 mixed 纤维不能作这个替换。

## 3. Property B 强迫四支撑

由 Reiher 的 Property B，存在重标签 \(g\) 与一条仿射线
\(h+\langle g\rangle\)，使

\[
Q=g^{p-1}\prod_{j=1}^{p}(h+a_jg),
\qquad \sum_j a_j=1.
\tag{10}
\]

式 (9) 及 (3) 说明 \(r\) 在 \(Q\) 中的总重数恰为 \(p-2\)，所以
Property B 的 \(p-1\) 重标签 \(g\ne r\)。

还不可能有 \(g=e\)。否则 \(f,r\) 都是仿射线项，故
\(r-f\in\langle e\rangle\)。但由 (6)

\[
r-f=\alpha(e-f),
\tag{11}
\]

而 \(r\ne f\) 给 \(\alpha\ne0\)；式 (11) 会迫使
\(f\in\langle e\rangle\)，与 (1) 矛盾。同理 \(g\ne f\)。

因此 \(e,f,r\) 全是 (10) 的仿射线项。该线一共只有 \(p\) 个实际
位置，而 \(r^{p-2}\) 连同两个尾位置 \(e,f\) 已恰好占满 \(p\) 个。
所以

\[
\boxed{Q=g^{p-1}r^{p-2}ef.}
\tag{12}
\]

对 (12) 求总和得到

\[
\boxed{g=e+f-2r.}
\tag{13}
\]

结合 \(r=\alpha e+(1-\alpha)f\)，

\[
g=(1-2\alpha)(e-f).
\tag{14}
\]

因 \(g\ne0\) 且 \(r\ne e,f\)，参数满足

\[
\alpha\notin\{0,1,\tfrac12\}.
\tag{15}
\]

此外 \(g,r\) 独立：若 \(r\in\langle g\rangle\)，由于
\(e,f,r\) 同在方向为 \(g\) 的仿射线上，\(e,f\) 也会落入
\(\langle g\rangle\)，再次违反 (1)。

## 4. 单个端点上确实达到投影边界

删去两个尾位置后，

\[
S=g^{p-1}r^{p-2}.
\tag{16}
\]

因 \(g,r\) 是一组基，任一子集和唯一写成
\(ig+jr\)，其中

\[
0\le i\le p-1,\qquad0\le j\le p-2.
\tag{17}
\]

目标 \(r\) 只允许 \(i=0,j=1\)，所以全部表示恰为 \(p-2\) 个
singleton；目标 \(-r\) 需要 \(i=0,j=p-1\)，超出 (17) 的范围，
故完全没有表示。这反向核对了第 1 节的全部投影纤维条件。

因此 (12)--(16) 是这一层的尖边界，不是投影层自身的矛盾。

## 5. 共同核把单端点边界变成跨端点矛盾

令第三个尾标签为

\[
\gamma=-e-f.
\tag{18}
\]

当前 720 行的逐位置分解有同一个共同核

\[
K=R\setminus P,
\qquad
K\cap(U\cup P\cup\bigcup_jH_j)=\varnothing,
\qquad
K\subseteq Q_j\quad\text{对每个端点 }H_j,
\tag{19}
\]

并且逐行已有

\[
|K|\ge435.
\tag{20}
\]

对当前长七 singleton 端点，(12) 与 \(K\cap U=\varnothing\) 给出

\[
K\subseteq g^{232}r^{231}.
\tag{21}
\]

因此

\[
v_g(K)\ge435-231=204,
\qquad
v_r(K)\ge435-232=203.
\tag{22}
\]

特别地，可在 \(K\) 中选一个实际 \(g\)-位置和两个互异的实际
\(r\)-位置。

原长七端点的 singleton 尾是 \(\gamma\)，所以另外两个 singleton
端点的长补原子都含实际尾位置 \(u_\gamma\)，并由 (19) 同时含上述
三个 \(K\)-位置。在其中任取一条 \(Q_j\)，这四个互异位置的投影和为

\[
\rho(u_\gamma)+g+r+r
=-e-f+(e+f-2r)+2r=0.
\tag{23}
\]

它们组成 \(Q_j\) 的非空真零和子序列；而 \(|Q_j|\) 为 464 或 465，
所以四位置子序列不可能等于整个 \(Q_j\)。这与 \(\rho(Q_j)\) 是原子
直接矛盾。论证不要求另外两个 singleton 端点长七；在当前 720 个
survivor 中它们实际均长八。

## 6. 裁决

对全部 540 个含一个长七 singleton 的 outer rows，mixed 高度二分中的
“无 \(2\leftrightarrow1\) 交换”支不可能存在。因此每一行都被迫进入
真实双点--单点交换支。

本文关闭的是这 540 行的一整条分支，并未删除这些 outer rows：交换支
还须与交换后的近极值原子、统一实际高度、全部自动短块和另外两个
长补原子联立。固定 \(p=233\) 与全局 \(A_p\) 仍为
**INCOMPLETE**。
