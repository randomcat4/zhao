# `p_minus_four_cross_family_tails` 独立验缝

STATUS: CORRECT

## 1. 裁决与范围

本审计逐式核对
`proofs/p_minus_four_cross_family_tails.md` 的以下结论：三族非零点度
强迫三条互异正核心尾，(p\ge17) 时两条必需跨族尾交，
(F_1/F_2\)--(F_3) 的交换公式及全部父尾边界，以及三尾有限局部
状态。证明在其声明的局部作用域内正确；它没有把局部相容状态提升为
完整 Hasse 设计、补原子或 ROUTE-A4 反例。

## 2. 三族点度确实强迫三条互异尾

对固定 (v\in X)，三族带符号点度为

\[
-3/4,\qquad 3/10,\qquad -1/20\pmod p.
\]

当 (p\ge11) 时分母 (4,10,20) 均可逆，分子也非零。因此每个
带符号和非零；若某族没有含 (v) 的块，其左端会是空和零，矛盾。
这里没有把模 (p) 的带符号度误当成正整数计数。

把所得块写成 (A_\lambda=V_\lambda\dot\cup U_\lambda)，其中
(v\in V_\lambda\subset X)，则 (b_\lambda=|V_\lambda|\ge1)。
若 (U_\lambda=\varnothing)，商零和给
(b_\lambda q=0)。但 (b_\lambda\le8<p) 且 (q\ne0)，不可能。
故 (1\le b_\lambda\le\ell_\lambda-1)，且

\[
\bar\sigma(U_\lambda)=-b_\lambda q,
\qquad
\sigma(U_\lambda)=\lambda a-b_\lambda x.
\]

若 (U_\lambda=U_\mu)，商和值先给
((b_\lambda-b_\mu)q=0)。由于
(|b_\lambda-b_\mu|<p)，必有 (b_\lambda=b_\mu)；实际和值再给
((\lambda-\mu)a=0)。(a) 的阶为 (p)，而
(0<|\lambda-\mu|\le2<p)，所以只能 (\lambda=\mu)。因此三条
所选尾的身份确实两两不同。

## 3. (p\ge17) 的交叉相交阈值

固定尾后，(X) 内相同实际值的位置可任意替换，所以任意
(V_\lambda\in\binom X{b_\lambda}) 都生成同族同长块。若
(U_\lambda\cap U_3=\varnothing) 且
(b_\lambda+b_3\le m)，可在 (X) 中选择不交核心，得到一条
(F_\lambda) 块与一条 (F_3) 块不交，违反冻结的跨族相交接口。

因尾非空，三个核心数满足

\[
b_1\le5,\qquad b_2\le6,\qquad b_3\le7.
\]

当 (p\ge17) 时 (m=p-4\ge13)，故
(b_1+b_3\le12\le m) 且
(b_2+b_3\le13\le m)。这恰好推出两条尾交。对素数边界
(p=11,13)，最大核心和可以超过 (m)，主稿正确地没有外推。

## 4. 跨族交换公式

固定 (\lambda\in\{1,2\})，从父块
(A_3=V'\dot\cup U') 出发。令

\[
C=V\cap V',\quad P=V\setminus V',\quad
P'=V'\setminus V,
\]

\[
W=U\cap U',\quad R=U\setminus U',\quad
S=U'\setminus U,
\]

并取 (P_0\subseteq P,P'_0\subseteq P')、
(|P_0|=\alpha,|P'_0|=\beta)，以及
(E\subseteq R,F\subseteq S)。写 (d=\beta-\alpha)。删去
(P'_0\dot\cup F) 并加入 (P_0\dot\cup E) 后保持商和为零，当且
仅当

\[
\bar\sigma(E)-\bar\sigma(F)=dq.
\]

此时商差落在核 (\langle a\rangle) 中，故存在唯一
(\delta\in\mathbb F_p) 使

\[
\sigma(E)-\sigma(F)-dx=\delta a.
\]

新核心与新尾为

\[
V^*=C\dot\cup(P'\setminus P'_0)\dot\cup P_0,
\qquad
U^*=W\dot\cup E\dot\cup(S\setminus F).
\]

逐项计数、求商和及求实际和给

\[
b^*=b'-d,
\qquad
L^*=\ell'-d+|E|-|F|,
\]

\[
\bar\sigma(U^*)=-b^*q,
\qquad
\sigma(A^*)=(3+\delta)a,
\qquad
\sigma(U^*)=(3+\delta)a-b^*x.
\]

这些等式的符号和方向均正确。

两个父块属于跨族且必相交，其交集正是
(C\dot\cup W\subseteq A^*)，所以 (A^*\ne\varnothing)。同时
(A^*\subseteq A_\lambda\cup A_3)，故

\[
|A^*|\le15<|Z|,
\qquad 15\le2p+2.
\]

因此 (SQ) 适用并把实际和值系数压到唯一的
(\mu\in\{1,2,3\})；再调用已经继承的正系数长度界，才得到
(L^*\in I_\mu)。主稿第 193--199 行把这两个接口合写为“(SQ)
迫使”，是非承重的引用压缩，不是新增假设或证明缺口。

固定核心交数 (k) 时，

\[
-(b-k)\le d\le b'-k,
\]

恰是 (\beta-\alpha) 的全部整数值，因而
(0\le b^*=k+(b'-k-\beta)+\alpha\le m)。空交换给回
(U')，全交换 (E=R,F=S,d=b'-b) 给回 (U)。反过来，
(U^*=U') 强迫 (E=F=\varnothing,d=0)，而 (U^*=U) 强迫
(E=R,F=S,d=b'-b)；所以除此两端点外确实产生第三个尾身份。

## 5. (b^*=0)、(A^*=T) 与父尾约束

记 (U_T^*=U^*\cap T)。若它为空，则非空商零和集
(A^*\subset B)，且 (|A^*|\le15<|B|)，违反
(\bar B) 的原子性。因此 (U_T^*\ne\varnothing)。

若 (b^*>0) 且 (\bar\sigma(U_T^*)=0)，则

\[
V^*\dot\cup(U^*\cap B)
\]

是 (\bar B) 的非空真商零和子序列，仍矛盾。若 (b^*=0)，该
论证只推出 (U^*\cap B=\varnothing)，即 (A^*=U^*\subseteq T)；
主稿没有在这里多推出矛盾。若此时 (\mu=3) 且 (A^*\ne T)，
则 (A^*,T) 是两个不同 (F_3) 块，其交集就是商零和的 (A^*)，
违反 (F_3) 非零商交。唯一真正例外正是同块 (A^*=T)。

与两个父尾的约束无漏项：

- (\mu\in\{1,2\}) 时，新块只需与父 (F_3) 块交；在核心可取
  不交的条件 (b^*+b'\le m) 下，这给 (18)。
- (\mu=3) 时，新块须与父 (F_\lambda) 块交；条件
  (b^*+b\le m) 给 (19)。
- (\mu=3) 且 (U^*\ne U') 时，它与父 (F_3) 块在每个可实现
  核心交数 (j\in J_m(b^*,b')) 上都必须有非零商交，正是 (20)。
- 当 (U^*=U') 时商和迫使 (b^*=b')。若 (j<b')，两个生成块
  不同且交商和为 ((j-b')q\ne0)；(j=b') 是同一核心、同一块，
  不能施加“不同块”的禁值。主稿准确保留了这个端点。

第 282--288 行的“更一般地”是在前一项 (\mu=3) 的语境下，把
父 (U') 推广成任意另一条 (F_3) 尾 (H)。如此读取时 (21)
正确；若脱离该语境用于 (\mu=1,2)，则只能推出普通相交，不能
推出非零商交。建议后续引用时显式保留条件 (\mu=3)，但这不影响
本文当前推导。

## 6. 三尾局部状态和相容见证

每条尾大小至多相应最大块长减一，因此

\[
|U_1\cup U_2\cup U_3|\le5+6+7=18.
\]

每个位置的三条成员位、(T)-成员位、商标签和高度，连同六个
((\ell_\lambda,b_\lambda)) 参数，足以重建两组
(W,R,S)，枚举每个 (E\subseteq R,F\subseteq S)，并计算商差、
实际缺陷、长度、族别、(T)-部分和所有父尾交集。因此第 6 节只
声称这是当前两组交换接口的有限局部状态；它明确没有包含全局
Hasse 计数、第三尾递归闭包或 (B) 的全部子和。

显式状态中

\[
q=e_1,\quad x=(e_1;0),\quad w=(e_2;0),\quad
r_\lambda=(-4e_1-e_2;\lambda),
\]

\[
U_\lambda=\{w,r_\lambda\},\qquad
(\ell_\lambda,b_\lambda)=(6,4).
\]

每条尾的和为 (\lambda a-4x)，共同 (T)-部分
(\{w\}) 商和非零，且三个 (r_\lambda) 是不同实际标签。对同一
(U_3) 的两个不同核心，核心交数 (j<4)，交商和为
((j-4)q\ne0)。在每对 (U_\lambda,U_3) 中，两个单点差的商标签
相同但不在 (\langle q\rangle)，所以只有空--空与满--满两个端点
满足交换商等式。它们分别返回 (U_3) 和 (U_\lambda)。该状态确实
只证明局部接口相容，没有构造全局对象，主稿的停止线没有过度宣称。

第 347--348 行的指标函数已随审计建议统一写成
`\mathbf{1}_{U_i}`；这只是排版修正，不影响数学。

## 7. 程序复核

实际运行 `verify_p_minus_four_cross_family_tails.py`，退出码为零，
用时约 (2.918) 秒。脚本核对全部 91 个
(11\le p\le500) 的素数、三族点度非零、核心交数和长度恒等式、
(p\ge17) 阈值及显式三尾局部状态。一般 (p\ge11) 的结论仍由
上述符号证明承担；脚本没有把有限扫描提升为全称证明。
