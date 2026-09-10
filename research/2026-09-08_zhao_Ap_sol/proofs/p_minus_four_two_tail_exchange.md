# \(p-4\) 单高度纤维的二余部交换闭包

STATUS: INCOMPLETE

## 1. 范围

设 \(p\ge 11\) 为素数，\(Z\) 是长度 \(3p+4\) 的实际零和原子。
固定

\[
T\in\mathcal F_3,\qquad 6\le |T|\le 8,
\qquad B=Z\setminus T,
\]

其中 \(\bar B\) 是 \(C_p^3\) 中的原子。设

\[
X=x^m\subset B,\qquad m=p-4,\qquad \bar x=q\ne0,
\qquad Y=Z\setminus X,
\]

这里 \(X\) 的全部位置具有同一个实际值 \(x\)。短块族的长度窗为

\[
I_1=[2,6],\qquad I_2=[4,7],\qquad I_3=[6,8].
\tag{1}
\]

对 \(\ell\in I_3\)、\(1\le b\le\ell-1\)，称
\(U\subset Y\) 是一个参数为 \((\ell,b)\) 的 \(F_3\)-余部，若

\[
|U|=\ell-b,\qquad
\bar\sigma(U)=-bq,\qquad
\sigma(U)=3a-bx.
\tag{2}
\]

于是对每个 \(V\in\binom Xb\)，集合 \(V\mathbin{\dot\cup}U\)
都是 \(\mathcal F_3\) 中的 \(\ell\) 项块。本文研究两个不同余部
\(U,U'\)，给出一个不经过加权矩的精确二尾交换闭包，并排除全部
“错误方向或核心差至少四”的真包含余部对。现有接口仍允许一个
显式命名二尾形式赋值，故本文不宣称排除整个 \(m=p-4\) 分支；该
赋值未重建全诱导短谱，不登记为局部候选。

## 2. 原子给出的纤维补零引理

**引理 1（\(X\)-补零）。** 若
\(\varnothing\ne P\subsetneq Y\) 且

\[
\sigma(P)=c x\qquad(c\in\mathbb F_p),
\tag{3}
\]

则 \(c\in\{1,2,3\}\)。

**证明。** 若 \(c=0\)，则 \(P\) 本身是 \(Z\) 的非空真零和
子序列。若把 \(c\) 取为 \(\{4,5,\ldots,p-1\}\) 中的整数代表，
则 \(1\le p-c\le p-4=m\)，所以可从 \(X\) 取 \(p-c\) 个位置
组成 \(V\)。于是

\[
\sigma(P\mathbin{\dot\cup}V)=cx+(p-c)x=0.
\]

由于 \(P\subsetneq Y\)，该子序列仍是真子序列，矛盾。只余
\(c=1,2,3\)。\(\square\)

若只假设 \(P\subseteq Y\)，唯一须另列的边界是
\((P,c)=(Y,4)\)：此时补上全部 \(X\) 得到的是 \(Z\) 自身。
后文只把引理用于至多七项的真差集，所以不会碰到此边界。

## 3. 两个余部的全部核心交数

取参数分别为 \((\ell,b)\)、\((\ell',b')\) 的不同
\(F_3\)-余部 \(U,U'\)。写成不交并

\[
W=U\cap U',\qquad R=U\setminus U',
\qquad S=U'\setminus U.
\tag{4}
\]

两个核心 \(V\in\binom Xb\)、\(V'\in\binom X{b'}\) 的交数
恰可取遍

\[
J_m(b,b')=\{k_0,k_0+1,\ldots,\min(b,b')\},\qquad
k_0=\max(0,b+b'-m).
\tag{5}
\]

对每个这样的 \(k\)，相应两个不同 \(F_3\) 块的交集是
\((V\cap V')\mathbin{\dot\cup}W\)。冻结的 \(F_3\) 商交非零
因此给出已有但必须完整保留的条件

\[
\boxed{\bar\sigma(W)\ne-kq\quad
       (k\in J_m(b,b')).}
\tag{6}
\]

另一方面，把任意含 \(X\) 的短块按 \(T\mid(B\setminus X)\)
分开，并使用 \(\bar B\) 的原子性，得到

\[
\boxed{
\varnothing\ne U\cap T\subsetneq T,\quad
\bar\sigma(U\cap T)\ne0,
}
\qquad
\boxed{
\varnothing\ne U'\cap T\subsetneq T,\quad
\bar\sigma(U'\cap T)\ne0.
}
\tag{7}
\]

式 (6) 与 (7) 分别保留全部可实现核心交数及两个尾的非零
\(T\)-部分；下面的交换闭包会把 (7) 同时施加到每个新生尾。

## 4. 精确二尾交换闭包

固定 \(k\in J_m(b,b')\)，选择核心使 \(|V\cap V'|=k\)。令

\[
C=V\cap V',\quad P=V\setminus V',\quad P'=V'\setminus V.
\]

故 \(|P|=b-k\)、\(|P'|=b'-k\)。再取

\[
E\subseteq R,\quad F\subseteq S,\quad
0\le\alpha\le b-k,\quad0\le\beta\le b'-k,
\]

并从 \(P,P'\) 分别选 \(\alpha,\beta\) 个位置。记

\[
d=\beta-\alpha.
\tag{8}
\]

这两个被选子序列商和相等，当且仅当

\[
\bar\sigma(E)-\bar\sigma(F)=dq.
\tag{9}
\]

在 (9) 下，存在唯一 \(\delta\in\mathbb F_p\) 使

\[
\sigma(E)-\sigma(F)-dx=\delta a.
\tag{10}
\]

由两个 \(F_3\) 块的补原子交换，或者直接在它们的并集中删换，
得到新尾及其核心数

\[
U^*=W\mathbin{\dot\cup}E
       \mathbin{\dot\cup}(S\setminus F),
\qquad b^*=b'-d.
\tag{11}
\]

相应新块的长度为

\[
L^*=b^*+|U^*|
=\ell'-d+|E|-|F|,
\tag{12}
\]

且

\[
\bar\sigma(U^*)=-b^*q,\qquad
\sigma(U^*)=(3+\delta)a-b^*x.
\tag{13}
\]

这里新块非空，因为原来两块的交集商和非零；它是真子集，因为
两块并集至多 \(15\) 项，而 \(|Z|=3p+4\)。又
\(15\le2p+2\) 对全部 \(p\ge11\) 成立。因此 (SQ) 可用，并迫使
存在唯一 \(\lambda^*\in\{1,2,3\}\) 满足

\[
\lambda^*\equiv3+\delta\pmod p,
\qquad L^*\in I_{\lambda^*}.
\tag{14}
\]

同值替换进一步说明：\(U^*\) 与每个
\(V^*\in\binom X{b^*}\) 都生成同族同长块。故还必须有

\[
U^*\cap T\ne\varnothing,
\qquad
b^*\ge1\Longrightarrow
\bar\sigma(U^*\cap T)\ne0.
\tag{15}
\]

若 \(\lambda^*=3\) 且 \(U^*\ne U\)，则再次应用全部核心交数
禁值，得到

\[
\bar\sigma(W)+\bar\sigma(E)\ne-jq
\quad(j\in J_m(b^*,b)).
\tag{16}
\]

若 \(\lambda^*=3\) 且 \(U^*\ne U'\)，则同理

\[
\bar\sigma(W)+\bar\sigma(S\setminus F)\ne-jq
\quad(j\in J_m(b^*,b')).
\tag{17}
\]

若 \(\lambda^*\in\{1,2\}\)，相应的交叉相交接口至少给出

\[
\begin{aligned}
b^*+b\le m&\Longrightarrow W\cup E\ne\varnothing,\\
b^*+b'\le m&\Longrightarrow W\cup(S\setminus F)\ne\varnothing.
\end{aligned}
\tag{18}
\]

式 (11)--(18) 是逐二尾的真实闭包，不是计数同余。

### 核心变量的精确压缩

对固定 \(k\)，可实现的 \(d\) 恰为

\[
-(b-k)\le d\le b'-k.
\tag{19}
\]

这些区间随 \(k\) 增大而嵌套。因此只问某个交换尾能否由某对核心
实现时，可以完全消去 \(k,\alpha,\beta\)：恰须

\[
\boxed{-b+k_0\le d\le b'-k_0,}
\tag{20}
\]

其中 \(k_0\) 由 (5) 给出。输出 (11)--(18) 只依赖
\((E,F,d)\)，不依赖实现它的 \(\alpha,\beta,k\)。空尾交换
\((E,F,d)=(\varnothing,\varnothing,0)\) 给回 \(U'\)，全尾交换
\((R,S,b'-b)\) 给回 \(U\)；除此之外恰得到第三个尾集。

## 5. 一个严格的新排除：真包含只能差一至三层核心

**定理 2（嵌套方向定理）。** 设 \(U,U'\) 是不同的
\(F_3\)-余部。

1. 若 \(U'\subsetneq U\)，则
   \[
   b'=b+d\qquad\text{其中 }d\in\{1,2,3\}.
   \tag{21}
   \]
2. 若 \(U\subsetneq U'\)，则
   \[
   b=b'+d\qquad\text{其中 }d\in\{1,2,3\}.
   \tag{22}
   \]

换言之，较大的余部必须具有较小的核心数，且核心数之差只能为
一、二或三。所有同核心数嵌套、反向嵌套及核心差至少四的嵌套对
都不可能出现。

**证明。** 若 \(U'\subsetneq U\)，则 \(R=U\setminus U'\)
非空、\(S=\varnothing\)。由 (2)

\[
\sigma(R)=\sigma(U)-\sigma(U')=(b'-b)x.
\tag{23}
\]

又 \(|R|\le7<|Y|\)，故引理 1 适用。由于
\(|b'-b|\le6<p\)，(23) 的系数落在 \(\{1,2,3\}\) 当且仅当
\(b'-b\in\{1,2,3\}\)。这给出 (21)；交换两个尾即得 (22)。
\(\square\)

注意，对 (21) 的幸存情形，\(W=U'\) 且
\(\bar\sigma(W)=-b'q\)，而 (5) 中 \(k\le b<b'\)。所以旧禁值
(6) 自动成立。也就是说，嵌套方向定理严格补充了 (6)，但幸存的
三层核心差不能再由 (6) 单独排除；其余限制确实需要 (9)--(18)
中的差集子和数据。

## 6. 不用加权矩的最小二尾状态

对当前全部二尾接口，一个有限的精确状态可压缩为

\[
\mathfrak S(U,U')=
\bigl(
\ell,b,\ell',b';
|W|,|W_T|,|S|,|S_T|;
\bar\sigma(W),\bar\sigma(W_T),
\bar\sigma(S),\bar\sigma(S_T);
\Xi_{R,S}
\bigr),
\tag{24}
\]

其中 \(W_T=W\cap T,S_T=S\cap T\)，而 \(\Xi_{R,S}\) 对每对
\(E\subseteq R,F\subseteq S\) 精确记录

\[
\bigl(
|E|,|E\cap T|,|F|,|F\cap T|,
\bar\sigma(E),\bar\sigma(F),
\bar\sigma(E\cap T),\bar\sigma(F\cap T),
\sigma(E)-\sigma(F)
\bigr).
\tag{25}
\]

因 \(|R|+|S|\le14\)，表 (25) 至多有 \(2^{14}\) 行。给定
(24)--(25)：

- (5)--(7) 可直接判定；
- (9)--(10) 决定所有可交换的 \(d,\delta\)；
- (11)--(15) 的新尾长度、族别及 \(T\)-部分可直接判定；
- (16)--(18) 只再使用已记录的交集大小和商和。

因此在本轮所用接口下，(24)--(25) 是一个不含块数、点度或加权
矩的精确二尾有限 CSP；核心位置只留下区间 (5)、(20)。继续只记
\(|U\cap U'|\) 或 \(|U\cap T|\) 会丢失 (9)、(15)--(17)，因而
不足以表达交换闭包。

## 7. 二尾接口本身仍相容

下面给出一个对每个 \(p\ge11\) 都形式相容的命名二尾赋值。它只
检查上述成对接口，不枚举所赋位置诱导的全部短商零和。只在坐标
\(C_p^3\oplus\langle a\rangle\) 中取

\[
q=(1,0,0),\quad x=(1,0,0;0),
\]

并取三个不同位置，其实际标签为

\[
w=(-4,-1,0;3),\qquad
r=s=(0,1,0;0).
\tag{26}
\]

令 \(w\in T\)、\(r,s\notin T\)，并置

\[
U=\{w,r\},\qquad U'=\{w,s\},
\qquad (\ell,b)=(\ell',b')=(6,4).
\tag{27}
\]

则两个尾都满足 (2)，共同 \(T\)-部分为 \(\{w\}\)，其商和
非零。对每个可实现的 \(k\)，

\[
\bar\sigma(U\cap U')+kq=(-4+k,-1,0)\ne0.
\]

在 \(R=\{r\},S=\{s\}\) 的四对子集中，商差落在
\(\langle q\rangle\) 的只有两个零差端点：空对给回 \(U'\)，
满对给回 \(U\)。故全部交换闭包、长度窗和新尾 \(T\)-部分条件
都成立。相同实际标签只用了两个位置，而 \(2\le p-4\)。

这只实现 (24)--(25) 的 FORMAL_PAIR_INTERFACE_COMPATIBILITY；它
没有重建所赋位置诱导的全部长度二至八商零块或短零和谱，也没有
构造完整 \(T,B,Z\)。因此它不是局部候选或冻结命题反例，只说明
列出的命名二尾方程本身允许“同值双位置换尾”形式退化。

## 8. 结论边界

- **PROVED：**纤维补零引理 1；精确交换闭包 (9)--(18)；核心
  压缩 (20)；嵌套方向定理 2。
- **PROVED：**当前二尾接口可精确降为至多 \(2^{14}\) 行的状态
  (24)--(25)，无需重复任何 Hasse 加权矩。
- **INCOMPLETE：**未排除整个 \(m=p-4\) 单高度分支。形式赋值
  (26)--(27) 只证明命名二尾接口仍有代数退化解；下一步必须加入
  全诱导短谱与第三个
  余部的一致性，或加入完整补原子的内部子和结构，而不能只继续
  消元点度、对度、三点度。

全部结论的量词是素数 \(p\ge11\)。有限脚本只核对核心区间、长度
公式、嵌套边界与形式赋值；它不替代上述全称证明，也不认证局部
候选。
