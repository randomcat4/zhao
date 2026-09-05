# 非秩二精确族：完整尾曲线及 K

状态：**PROVED（下述 r=2,3 的族）**；r=4 的唯一中间点 **INCOMPLETE**。本文保持原 K 定义；没有把 η 的单点等式当成尾阈值。外部定理为已发表结果，本文的推论不主张新颖性。独立验缝由主实例另行安排。

## 1. 冻结的定义与结论

序列允许重复；零和子序列必须非空。记

\[
s_{\le m}(G)=\min\{L:\text{每个长度 }L\text{ 的 }G\text{ 上序列有长度}\le m\text{的非空零和子序列}\},
\]

\[
K(G)=\min\{M\in[\exp(G),D(G)-1]\cap\mathbb Z:
\forall m\in[M,D(G)-1]\cap\mathbb Z,\ s_{\le m}(G)\le2D(G)-m\}.
\]

**定理 A。** 若 \(r\in\{2,3\}\)、\(4\mid n\)、\(G=C_2^r\oplus C_n\)，则 \(D(G)=n+r\)，且对每个整数 \(j\in[0,r-1]\)，

\[
\boxed{s_{\le n+j}(G)=n+2r-j=2D(G)-(n+j)}.
\]

因而

\[
\boxed{K(C_2^r\oplus C_n)=n\qquad(r=2,3,\ 4\mid n).}
\]

这里两族的群秩分别为 3 和 4，均非秩二；特别包含任务指定的所有 \(C_2^2\oplus C_{2^a}\)、\(C_2^3\oplus C_{2^a}\)，\(a\ge2\)。允许 n 含奇因子，因此结论不局限于 2 群。

## 2. 已核查的外部引理

1. **KNOWN：p 群 Davenport 公式。** 有限阿贝尔 p 群满足 \(D=D^*=1+\sum_i(n_i-1)\)。见 Luo 原文 Theorem 2.2，或 Zhao–Hong Lemma 2.7(b)。
2. **KNOWN：Luo 大指数定理及扩展。** 若有限阿贝尔 p 群 P 满足 \(D(P)\le2\exp(P)-1\)，则 \(\eta(P)=2D(P)-\exp(P)\)。这里允许 \(p=2\)。若 b 与 p 互素，则 \(Q=C_b\oplus P\) 也满足 \(D(Q)=D^*(Q)\) 及 \(\eta(Q)=2D(Q)-\exp(Q)\)。前者使用原文 Theorem 2.3，η 等式使用 Theorems 1.6、4.1。原始来源：Sammy Luo, *Short zero-sum sequences over abelian p-groups of large exponent*, J. Number Theory 177 (2017), 28–36；[原文 PDF](https://arxiv.org/pdf/1608.05157)，[正式发表页面](https://doi.org/10.1016/j.jnt.2017.01.021)。此处仅用已证明定理，不用该文关于 s(G) 的猜想。
3. **KNOWN：倒数第一个点。** 若群秩至少 2，则 \(s_{\le D(G)-1}(G)=D(G)+1\)。Zhao–Hong Lemma 2.1，引自 Wang–Zhao 2017, Lemma 8。
4. **KNOWN：倒数第二个点。** 对群秩至少 2 且不同构于 \(C_2^3,C_2^4,C_2\oplus C_{2t}\) 的群，有 \(s_{\le D(G)-2}(G)\le D(G)+2\)。Zhao–Hong Theorem 1.1。

Zhao–Hong 原文：Kevin Zhao and Siao Hong, *On zero-sum subsequences over finite abelian groups of length not exceeding a given number*, Colloquium Mathematicum, online 1 September 2026, [DOI](https://doi.org/10.4064/cm9599-7-2026)。工作区核查文本为 `math/2026-09-04_zhao_response/proofs/zhao_hong_2026.txt`，对应 PDF 同名；Theorem 1.1 在 PDF 第 3 页，Lemma 2.1 在第 4 页。

## 3. 下界构造：逐个 j 的显式证书

**PROVED_HERE（亦与 Zhao–Hong Lemma 2.9 相容）。** 设 n 为偶数、\(n\ge r\ge1\)，明确选定直和分解 \(G=\langle h_1\rangle\oplus\cdots\oplus\langle h_r\rangle\oplus\langle e\rangle\)，其中 \(\operatorname{ord}(h_i)=2\)、\(\operatorname{ord}(e)=n\)。因此 e 是最后一个循环直和因子的生成元，不能取成任一 h_i。对 \(0\le j\le r-1\)，定义

\[
S_j=e^{\,n-1-j}\prod_{i=1}^{r}h_i(h_i+e).
\]

e 的重数非负。此序列长

\[
|S_j|=n-1-j+2r=n+2r-j-1.
\]

考察其中非空零和子序列 T。投影到 \(C_2^r\) 后，每个 h_i 坐标独立，故每对 \(h_i,h_i+e\) 必须同时选择或同时不选。设选了 k 对，并选了 x 个独立的 e 项。那么

\[
0\le k\le r,\quad0\le x\le n-1-j,\quad\sigma(T)=(x+k)e.
\]

因为每个 h_i 的阶为 2，\(h_i+(h_i+e)=e\)，上述等式无额外符号约定。若 k=0，则非空要求 \(1\le x<n\)，不可能零和。因此 k≥1。又 \(0<x+k\le n-1-j+r<2n\)，于是 \(x+k=n\)。因此

\[
k=n-x\ge j+1,\qquad |T|=x+2k=n+k\ge n+j+1.
\]

所以 S_j 没有长度至多 n+j 的非空零和子序列，从而

\[
s_{\le n+j}(C_2^r\oplus C_n)\ge |S_j|+1=n+2r-j.
\]

这里没有假定 T 必然存在：证明只分类任何可能的 T，已足以证明下界。包括 j=r−1、n=r 时 e 重数为零的边界；不要求元素必须各不相同以外的额外序列条件。

## 4. 定理 A 的完整上界证明

将 \(n=2^a b\) 写成 \(a\ge2\)、b 奇数，令 \(q=2^a\)、\(P=C_2^r\oplus C_q\)。则

\[
D(P)=q+r\le2q-1
\]

因为 \(q\ge4\) 且 \(r\le3\)。此外 \(G\cong C_b\oplus P\)。Luo 的扩展给出

\[
D(G)=D^*(G)=n+r,\qquad s_{\le n}(G)=\eta(G)=n+2r.
\]

现在逐点检查全部尾区间；不能只使用这个 η 等式。

| r | j | m=n+j | 上界的依据 | 上界值 |
|---|---|---|---|---|
| 2 | 0 | n=D−2 | Luo Theorem 4.1（也可用 Zhao–Hong Theorem 1.1） | n+4 |
| 2 | 1 | n+1=D−1 | Zhao–Hong Lemma 2.1 | n+3 |
| 3 | 0 | n=D−3 | Luo Theorem 4.1 | n+6 |
| 3 | 1 | n+1=D−2 | Zhao–Hong Theorem 1.1 | n+5 |
| 3 | 2 | n+2=D−1 | Zhao–Hong Lemma 2.1 | n+4 |

Theorem 1.1 的例外确实全部排除：G 的指数 n≥4，故不是指数为 2 的两个例外；G 的秩为 r+1≥3，故不是秩二例外 \(C_2\oplus C_{2t}\)。

表中上界与第 3 节下界逐点相等。因 \([n,D-1]=[n,n+r-1]\)，该表已经穷尽 K 定义中的每个整数 m。故 n 本身是可行阈值；定义又要求 M≥n，因此 K=n。证明完成。

## 5. r=4：严格区分已知点与未闭合点

令 \(G=C_2^4\oplus C_n\)，\(8\mid n\)。同样用 q=2^{v_2(n)}≥8，\(D(P)=q+4\le2q-1\)，得 \(D(G)=n+4\)、η=n+8。结合第 3 节下界与两个尾端点定理：

\[
s_{\le n}=n+8,\qquad
n+7\le s_{\le n+1}\le n+8,\qquad
s_{\le n+2}=n+6,\qquad s_{\le n+3}=n+5.
\]

中间上界仅由关于 m 的单调性 \(s_{\le n+1}\le s_{\le n}\) 得到。由于 s 是整数，其值只有 n+7 或 n+8 两种可能。于是有严格的二择一：

\[
K(G)=\begin{cases}
n,&s_{\le n+1}=n+7,\\
n+2,&s_{\le n+1}=n+8.
\end{cases}
\]

所以本单元对 r=4 只证明 \(K\in\{n,n+2\}\)，**未得到其精确值**。要闭合这个族，恰缺

\[
s_{\le n+1}(C_2^4\oplus C_n)\le n+7.
\]

这也说明 K 不可能等于 n+1：该点若成立，已知的 n 点也成立，整个尾区间从 n 开始；该点若失败，阈值必须越过它。

任务指定的 r=4,a=2，即 \(C_2^4\oplus C_4\)，满足 D=8>2·4−1，**不能套用 Luo 大指数定理**。这里只由两个尾端点得 K≤6，且定义给 K≥4；本文不给该群额外的精确判断。

## 6. 审计与贡献边界

- 真正精确闭合的是定理 A 的两个无限族及它们的整个尾曲线。
- 下界序列可逐项人工核查，覆盖全部 j，并非依赖有限计算。
- r=4 的结论只有上述二择一及缺口，不把它标记为 PROVED 精确族。
- 对 n 的奇因子扩展已核查 Luo 原文 Theorem 4.1；r=4 用 8|n，r=2,3 用 4|n，不混淆它们的大指数条件。
- 本文没有证明原先全群主猜想，也没有证明 Cp4 的两个缺口。
- 首轮独立验缝指出 v2 的单独构造引理漏写 e 与 h_i 的直和独立性；n=2,r=1,e=h1 是字面反例。最终 v3 明确该直和分解；主体定理 A/B 未改。此修订稿必须重新独立审查。
- 这些精确族是已发表引理的直接合成推论；尚未做该 K 表述的完整先行工作检索，因此不宣称新定理优先权或独立论文贡献。
