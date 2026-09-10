# \(p-4\) 单高度纤维的必需跨族余部与交换闭包

STATUS: PROVED_HERE / LOCAL_STOPPING_LINE

## 1. 设定与新结论

设 \(p\ge11\) 为素数，\(Z\) 是长度 \(3p+4\) 的实际零和原子，
固定

\[
T\in\mathcal F_3,\qquad 6\le |T|\le8,\qquad
B=Z\setminus T,
\]

其中 \(\bar B\) 是 \(C_p^3\) 中的原子。设

\[
X=x^m\subset B,\qquad m=p-4,\qquad \bar x=q\ne0,
\qquad Y=Z\setminus X.
\]

本文只考虑 \(X\) 的单高度情形。短块三族的长度窗是

\[
I_1=[2,6],\qquad I_2=[4,7],\qquad I_3=[6,8].
\tag{1}
\]

本页证明：必然存在三个两两不同的正核心余部

\[
U_\lambda\in\mathcal U_{\lambda,\ell_\lambda,b_\lambda},
\qquad \lambda=1,2,3,
\tag{2}
\]

其中 \(\ell_\lambda\in I_\lambda\)、\(1\le b_\lambda\le
\ell_\lambda-1\)。因此先前的二余部交换公式必然至少施加在一对
\(F_1\)--\(F_3\) 尾和一对 \(F_2\)--\(F_3\) 尾上，不再只是
“若存在两个 \(F_3\) 尾”的条件命题。

当 \(p\ge17\) 时还有

\[
\boxed{U_1\cap U_3\ne\varnothing,\qquad
U_2\cap U_3\ne\varnothing.}
\tag{3}
\]

下文给出这两对尾的完整交换公式及边界。所得局部系统仍有显式
相容状态，所以尚未排除整个单高度 \(p-4\) 分支。

## 2. 非零逐族点度强迫三个不同余部

固定任意位置 \(v\in X\)。三族逐点带符号度分别为

\[
d_1=-\frac34,\qquad d_2=\frac3{10},\qquad
d_3=-\frac1{20}\quad\text{于 }\mathbb F_p.
\tag{4}
\]

因为 \(p\ge11\)，三个分母可逆，三个分子也都非零，故
\(d_1,d_2,d_3\ne0\)。若某一族没有包含 \(v\) 的块，则相应带符号
度左端是空和零，与 (4) 矛盾。因此对每个
\(\lambda\in\{1,2,3\}\)，可选

\[
A_\lambda=V_\lambda\mathbin{\dot\cup}U_\lambda
\in\mathcal F_\lambda,
\qquad v\in V_\lambda\subseteq X,
\]

并记 \(|V_\lambda|=b_\lambda\ge1\)。余部非空：若
\(U_\lambda=\varnothing\)，则
\(b_\lambda q=0\)，但 \(1\le b_\lambda\le8<p\) 且 \(q\ne0\)。
于是

\[
\bar\sigma(U_\lambda)=-b_\lambda q,
\qquad
\sigma(U_\lambda)=\lambda a-b_\lambda x.
\tag{5}
\]

若 \(U_\lambda=U_\mu\)，先比较 (5) 的商和。因
\(|b_\lambda-b_\mu|<p\)，得到 \(b_\lambda=b_\mu\)。再比较实际
和，得到 \((\lambda-\mu)a=0\)。由于 \(a\) 的阶为 \(p\) 且
\(1\le|\lambda-\mu|\le2<p\)，必有 \(\lambda=\mu\)。所以 (2)
中的三个尾身份两两不同。这里没有把三个非零模 \(p\) 点度误读为
正整数下界；只用了“非零有限和不可能是空和”。

已有跨族相交接口说明任意 \(F_1/F_2\) 块都与任意 \(F_3\) 块
相交。同值替换允许为固定尾任取相应大小的 \(X\)-核心。若
\(b_\lambda+b_3\le m\)，可以选不交核心，故必须有

\[
U_\lambda\cap U_3\ne\varnothing
\qquad(\lambda=1,2).
\tag{6}
\]

而 \(b_1\le5,b_2\le6,b_3\le7\)。当 \(p\ge17\) 时
\(m=p-4\ge13\)，两组核心和都不超过 \(m\)，故 (6) 给出 (3)。
在边界 \(p=11,13\) 上，\(b_\lambda+b_3>m\) 可以发生，不能无条件
声称尾相交。

## 3. 一条下族尾与一条 \(F_3\) 尾的交换

固定 \(\lambda\in\{1,2\}\)，写

\[
U=U_\lambda,\quad U'=U_3,\quad
(\ell,b)=(\ell_\lambda,b_\lambda),\quad
(\ell',b')=(\ell_3,b_3).
\]

取核心 \(V\in\binom Xb,V'\in\binom X{b'}\)，并记

\[
W=U\cap U',\quad R=U\setminus U',\quad
S=U'\setminus U,
\]

\[
C=V\cap V',\quad P=V\setminus V',\quad
P'=V'\setminus V,\qquad k=|C|.
\]

可实现的 \(k\) 恰为

\[
J_m(b,b')=
\{\max(0,b+b'-m),\ldots,\min(b,b')\}.
\tag{7}
\]

从 \(P,P'\) 分别选 \(\alpha,\beta\) 个位置，再取
\(E\subseteq R,F\subseteq S\)，并令 \(d=\beta-\alpha\)。可以从
第二个父块中删去所选 \(P'\)-位置及 \(F\)，换入所选 \(P\)-位置
及 \(E\)，当且仅当

\[
\boxed{\bar\sigma(E)-\bar\sigma(F)=dq.}
\tag{8}
\]

在 (8) 下定义唯一的 \(\delta\in\mathbb F_p\) 使

\[
\sigma(E)-\sigma(F)-dx=\delta a.
\tag{9}
\]

新核心、尾和块分别是

\[
\begin{aligned}
V^*&=C\mathbin{\dot\cup}(P'\setminus P'_0)
       \mathbin{\dot\cup}P_0,\\
U^*&=W\mathbin{\dot\cup}E
       \mathbin{\dot\cup}(S\setminus F),\\
A^*&=V^*\mathbin{\dot\cup}U^*,
\end{aligned}
\tag{10}
\]

其中 \(|P_0|=\alpha,|P'_0|=\beta\)。直接计算给出

\[
\boxed{
b^*:=|V^*|=b'-d,
\qquad |A^*|=L^*=\ell'-d+|E|-|F|,}
\tag{11}
\]

\[
\boxed{
\bar\sigma(U^*)=-b^*q,
\qquad \sigma(A^*)=(3+\delta)a,
\qquad \sigma(U^*)=(3+\delta)a-b^*x.}
\tag{12}
\]

原来的跨族相交保证 \(C\dot\cup W=A_\lambda\cap A_3\ne
\varnothing\)，而它包含在 \(A^*\) 中，故新块非空。又

\[
|A^*|\le|A_\lambda\cup A_3|\le15<|Z|,
\qquad15\le2p+2.
\]

所以 (SQ) 对 \(A^*\) 可用，迫使实际和系数属于唯一的
\(\mu\in\{1,2,3\}\)；继承的正系数长度界再给

\[
\boxed{\mu\equiv3+\delta\pmod p,
\qquad L^*\in I_\mu.}
\tag{13}
\]

等价地，只有 \(\delta=-2,-1,0\) 分别产生
\(F_1,F_2,F_3\) 新块；其他缺陷值立即排除该交换数据。

固定 \(k\) 时 \(d\) 的可实现区间是

\[
-(b-k)\le d\le b'-k.
\tag{14}
\]

在此区间内 (10) 的核心确实是 \(X\) 的位置子集，所以
\(0\le b^*\le m\)。空交换
\((E,F,d)=(\varnothing,\varnothing,0)\) 给回尾 \(U'\)，且
\(\delta=0,\mu=3\)。全交换
\((E,F,d)=(R,S,b'-b)\) 给回尾 \(U\)，且
\(\delta=\lambda-3,\mu=\lambda\)。即使核心位置发生同值替换，
这两个端点也不是新尾身份。除这两种尾端点外，(10) 产生第三个尾。

## 4. \(T\)-部分、跨族相交与 \(F_3\) 禁值

新尾的 \(T\)-部分是逐位置精确式

\[
U_T^*=W_T\mathbin{\dot\cup}E_T
\mathbin{\dot\cup}(S_T\setminus F_T).
\tag{15}
\]

补原子性首先给

\[
\boxed{U_T^*\ne\varnothing.}
\tag{16}
\]

否则 \(A^*\subset B\) 是 \(\bar B\) 的非空真商零和子序列。若
\(b^*>0\)，再有

\[
\boxed{\bar\sigma(U_T^*)\ne0.}
\tag{17}
\]

否则 \(V^*\dot\cup(U^*\cap B)\) 是 \(\bar B\) 的非空真商零和
子序列。若 \(b^*=0\)，(17) 的补原子证明有一个真实边界：
\(\bar\sigma(U_T^*)=0\) 只迫使 \(U^*\cap B=\varnothing\)，即
\(A^*=U^*\subseteq T\)，并不自动矛盾。

若新块属于 \(F_3\) 且 \(A^*\ne T\)，则它与固定块 \(T\) 的
非零商交再次给 (17)，包括 \(b^*=0\)。唯一未覆盖的是
\(A^*=T\) 这个同块边界。

下面列出与两个父尾直接相关的全部相交约束。

- 若 \(\mu\in\{1,2\}\) 且 \(b^*+b'\le m\)，则新块与原
  \(F_3\) 星的核心可取不交，故
  \[
  W\cup(S\setminus F)=U^*\cap U'\ne\varnothing.
  \tag{18}
  \]

- 若 \(\mu=3\) 且 \(b^*+b\le m\)，则新 \(F_3\) 星与原
  \(F_\lambda\) 星的核心可取不交，故
  \[
  W\cup E=U^*\cap U\ne\varnothing.
  \tag{19}
  \]

- 若 \(\mu=3\) 且 \(U^*\ne U'\)，则对全部
  \(j\in J_m(b^*,b')\)，\(F_3\)--\(F_3\) 非零商交给
  \[
  \boxed{
  \bar\sigma(W)+\bar\sigma(S\setminus F)\ne-jq.}
  \tag{20}
  \]

当 \(U^*=U'\) 时必有 \(b^*=b'\)。同尾的两个不同生成块只有
\(j<b'\)，交商和为 \((j-b')q\ne0\)；\(j=b'\) 是同一块边界，
故不能把 (20) 不加区别地施加到端点。

仍在 \(\mu=3\) 情形下，更一般地，若 \(H\) 是任意另一条
\(F_3\) 尾，核心数为 \(c\)，
且 \(U^*\ne H\)，则必须逐个检查

\[
\bar\sigma(U^*\cap H)\ne-jq
\qquad(j\in J_m(b^*,c)).
\tag{21}
\]

式 (15)--(21) 清楚地区分了普通相交、非零商交和
\(b^*=0,A^*=T\) 边界。

## 5. 为什么尚未得到排除

上述必需三尾和两组交换接口本身仍相容。对每个 \(p\ge11\)，在
\(C_p^3\oplus\langle a\rangle\) 中取

\[
q=e_1,\qquad x=(e_1;0),\qquad w=(e_2;0),
\]

并取三个不同的非 \(T\) 位置

\[
r_\lambda=(-4e_1-e_2;\lambda),
\qquad\lambda=1,2,3.
\tag{22}
\]

令 \(w\in T\)，并置

\[
U_\lambda=\{w,r_\lambda\},
\qquad(\ell_\lambda,b_\lambda)=(6,4).
\tag{23}
\]

则 \(U_\lambda\) 满足 (5)，三个尾实际身份不同，共同
\(T\)-部分是商和非零的 \(\{w\}\)。所有跨族父块因而相交。
同一 \(U_3\) 生成的两个不同 \(F_3\) 块，其核心交数
\(j\le3\)，交商和是 \((j-4)q\ne0\)。

对 \(U_\lambda,U_3\) 的对称差只有两个单点
\(r_\lambda,r_3\)。它们有相同商标签
\(-4e_1-e_2\)，而该标签不在 \(\langle q\rangle\)。因此 (8)
只在空对和满对成立：空对返回 \(U_3\)，满对返回
\(U_\lambda\)，没有真交换需要额外闭合。配套脚本对
\(11\le p\le500\) 的全部素数逐项验证这些式子。

这只是三条命名尾的 FORMAL_CROSS_FAMILY_INTERFACE_COMPATIBILITY。
它不枚举所赋位置诱导的全部短商零和，不实现 Hasse 方程所需的全部
尾计数，也不构造 \(T\)、\(\bar B\) 原子或 \(Z\) 原子，因而不是
局部候选或全局反例。

## 6. 最小形式接口与停止线

同时表达两条必需跨族交换而不重复记录共同的 \(U_3\)，可取有限集

\[
\Omega=U_1\cup U_2\cup U_3,
\qquad |\Omega|\le(6-1)+(7-1)+(8-1)=18,
\tag{24}
\]

并为每个位置记录：

\[
\bigl(\mathbf{1}_{U_1},\mathbf{1}_{U_2},\mathbf{1}_{U_3},
\mathbf{1}_T;\ \bar g\in C_p^3,\ h\in\mathbb F_p\bigr),
\tag{25}
\]

再记录六个整数参数 \((\ell_\lambda,b_\lambda)_{\lambda=1}^3\)。
由 (25) 可重建两对尾的 \(W,R,S\)，以及每个
\(E\subseteq R,F\subseteq S\) 的商差、实际缺陷和 \(T\)-部分，
从而逐项判定 (7)--(21)。不需要另设抽象交换尾变量或块数变量。

这是本轮新接口的最小自然形式状态：若删去三个成员位，就会丢失
尾身份；删去 \(T\) 位会丢失 (15)--(17)；删去商标签或高度会分别
丢失 (8)、(9)。但该状态不含全局 Hasse 计数和 \(B\) 内部所有
子和或全诱导短谱，所以相容只表示命名接口的代数停止线。

继续推进必须把 (24)--(25) 与三族点度所需的全部余部数、或与
\(\bar B\) 的完整原子子和系统联立。仅把两尾 \(F_3\)--\(F_3\)
交换公式改写成跨族版本，不会自动产生矛盾。

## 7. 复核

运行

```text
python verify_p_minus_four_cross_family_tails.py
```

脚本核验三族点度在所有允许素数上非零、全部核心计数与长度恒等式、
\(p\ge17\) 的自动尾相交阈值，以及 (22)--(23) 的三尾形式交换
赋值。有限运行不替代第2--4节的全称代数证明，也不认证局部候选。
