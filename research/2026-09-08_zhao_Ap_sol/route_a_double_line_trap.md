# 共享外部双和障碍的推论：双侧补集线陷阱（去重稿）

## 状态

**PROVED；ROUTE_DEDUPLICATED。** 数学陈述与下述自足证明有效，但独立
去重审计指出，它是公共承重引理
`A_exterior_double_sum_obstruction` 的直接推论，不再作为一条
独立路线或独立进展计数。它严格弱于完整 \(h=p-4\) 排除，也不证明
一般 \(A_p\)。

## 与公共障碍的直接拼接

公共障碍在本处所需的形式是：不能从 \(D a^{p-4}\) 中取两个非空
外侧位置块 \(H_1,H_2\)，使

\[
\sigma(U)+\sigma(H_1)+\sigma(H_2)=0.
\tag{E}
\]

这里两块不要求彼此位置不交；两份锚点选择也可共享同一锚点位置，
与原双侧论证允许 \(C,C'\) 重叠的接口一致。

若本文件定理的前提成立，写

\[
\sigma(U)+\sigma(C)+\sigma(C')=\kappa a.
\]

令 \(I=\{0,1,\ldots,p-4\}\subseteq\mathbb F_p\)。当 \(p\ge7\) 时，
\(|I|=p-3\)，故 \(I+I=\mathbb F_p\)；也可直接逐个剩余选取
\(r,r'\in I\)，使 \(r+r'=-\kappa\)。于是

\[
H_1=C a^r,\qquad H_2=C'a^{r'}
\]

均非空，并触发 (E)。因此双侧补集线陷阱是公共障碍的直接推论。

若 \(p\ge11\)，即使 \(C\) 或 \(C'\) 为空，也可要求
\(1\le r,r'\le p-4\)。区间
\(I_*=\{1,\ldots,p-4\}\) 满足 \(I_*+I_*=\mathbb F_p\)，所以两侧
各预留至少一个锚点后，公共障碍与允许空侧的商群版本等价。
当 \(p=7\) 时 \(I_*+I_*\ne\mathbb F_7\)，故这里只保留两侧
\(C,C'\) 非空的版本；它严格弱于允许空侧的完整商群版本。

以下保留原自足证明作为本地核验，不赋予第二份证明路线的信用。

## 定理（双侧补集线陷阱）

采用 `assumptions.md` 的 \(x_0=0\) 冻结接口。令 \(D=R\setminus U\) 为满足 (TOP) 的四位置集。若存在两个非空位置子集 \(C,C'\subseteq D\)，使

\[
\sigma(U)+\sigma(C)+\sigma(C')\in H=\langle a\rangle,
\tag{1}
\]

则假想反例不存在。该结论对每个素数 \(p\ge7\) 成立；不要求 \(C,C'\) 不交或互异。

## 证明

写

\[
\sigma(U)+\sigma(C)+\sigma(C')=\kappa a
\]

其中 \(\kappa\in\mathbb F_p\)。固定任意 \(\lambda\in\mathbb F_p\)。由 (CONST)，

\[
c_U(-\sigma(C)+\lambda a)=\omega\ne0.
\]

因此至少存在一个位置子集 \(A\subseteq U\)，满足

\[
\sigma(A)=-\sigma(C)+\lambda a.
\tag{2}
\]

定义两个位置子序列

\[
B=A\cup C,\qquad B'=(U\setminus A)\cup C'.
\]

因 \(C,C'\) 均非空，\(B,B'\) 都非空。由 (1)、(2)，

\[
\sigma(B)=\lambda a,
\qquad
\sigma(B')=(\kappa-\lambda)a.
\tag{3}
\]

故两者都是 \(R\) 中的商零和位置子序列。其长度满足

\[
|B|+|B'|=|U|+|C|+|C'|
\le(4p-4)+4+4=4p+4.
\tag{4}
\]

于是至少一个长度不超过 \(2p+2\)。对这个非空短商零和应用 (SQ)：

- 若 \(|B|\le2p+2\)，则 \(\lambda\in\{1,2,3\}\)；
- 若 \(|B'|\le2p+2\)，则 \(\kappa-\lambda\in\{1,2,3\}\)。

因此每个 \(\lambda\in\mathbb F_p\) 都必须属于

\[
\{1,2,3\}\cup\{\kappa-1,\kappa-2,\kappa-3\},
\]

右侧至多有六个元素。这与 \(p\ge7\) 矛盾。证毕。

## 推论 1：正确排除 \(\sigma(R)\in H\)

**PROVED。** 在同一分支中必有

\[
\boxed{\sigma(R)\notin\langle a\rangle.}
\]

证明：在四位置集 \(D\) 中任取非空真子集 \(C\)，令 \(C'=D\setminus C\)。两者非空，且

\[
\sigma(U)+\sigma(C)+\sigma(C')=\sigma(U)+\sigma(D)=\sigma(R).
\]

若 \(\sigma(R)\in H\)，即触发定理矛盾。

这不是撤回命题 \(\theta=-1\Rightarrow\sigma(R)=0\) 的复活：这里从未由 \(\theta\) 或 \(\Lambda_i\) 推导总和；只是在额外假设 \(\sigma(R)\in H\) 下，用 (CONST)、互补长度和 (SQ) 排除该子分支。

## 补充：允许空侧的 \(p\ge11\) 版本

若 \(p\ge11\)，定理中的 \(C,C'\) 可以是任意子集，包括空集。证明完全相同；区别只在于 \(B\) 可能在 \(C=\varnothing\) 时对至多一个 \(\lambda\) 为空，\(B'\) 也可能在 \(C'=\varnothing\) 时对至多一个 \(\lambda\) 为空。故全部 \(p\) 个系数至多落在原来的六元素集合再加两个例外中，总数至多八，仍小于 \(p\)。

## 推论 2：四点商像的三值盒规避

令

\[
\mathcal A_D^+=\{\pi(\sigma(C)): \varnothing\ne C\subseteq D\}\subseteq G/H.
\]

则每个承重四点删除 \(D\) 都满足

\[
\boxed{-\pi(\sigma(U))\notin \mathcal A_D^++\mathcal A_D^+.}
\tag{5}
\]

否则存在非空 \(C,C'\) 满足 (1)。等价地，\(\pi(\sigma(R))\) 不能由 \(D\) 的四个商像以适当的 \(\{-1,0,1\}\) 系数表示（须同时满足两侧子集非空的接口）。

当 \(p\ge11\) 时还可把空子集加入，得到更强的

\[
-\pi(\sigma(U))\notin \mathcal A_D+\mathcal A_D,
\qquad
\mathcal A_D=\{\pi(\sigma(C)):C\subseteq D\}.
\tag{6}
\]

## 边界核对

- \(p=7\)：两侧非空时六个允许系数仍严格少于七个，证明有效；允许空侧的加强版没有越过该退化。
- 重复值：全程按位置取补集；\(C,C'\) 可重叠，不使用平方自由。
- 长度端点：等号 \(|B|=2p+2\) 被 (SQ) 覆盖。
- 空集：由 \(C,C'\ne\varnothing\) 排除，故没有把空子序列误送入 (SQ)。
- 带符号计数：只用“非零带符号总数蕴含至少一个实际子集”，未把符号和当作正计数或长度分布。

## 最小缺口

要由这条公共引理闭合全部 \(x_0=0\)，仍须证明：对至少一个满足
(TOP) 的四点删除 \(D\)，有

\[
-\pi(\sigma(U))\in\mathcal A_D^++\mathcal A_D^+.
\]

现有顶积、基分块及 \(F_4=1\) 只保证某个 \(D\) 的权非零，尚未给出这个商群三值盒命中性质。
这只是公共障碍的激活条件，本文不再把它登记为独立路线；活动的路线 A
前沿已转到长原子短块设计与秩三补核的不相容问题。
