# 三点密集覆盖与常数横截的组合边界

STATUS: PROVED_HERE / METHOD_BOUNDARY

设 \(Z\) 是任意 ROUTE-A4 的 \(3p+4\) 原子，
\(\mathcal F=\mathcal F_1\cup\mathcal F_2\cup\mathcal F_3\)，并令

\[
m=\left\lceil\frac{p-1}{20}\right\rceil.
\]

取任一 \(T\in\mathcal F_3\)。已有的自交与交叉相交关系说明
\(T\) 与 \(\mathcal F\) 中每个块都相交，故

\[
\boxed{\tau(\mathcal F)\le|T|\le8.}
\]

对每个 \(W\in\binom{Z\setminus T}{3}\)，三点删除引理给出至少
\(m\) 个包含 \(W\) 的短块。每个这样的块与 \(T\) 相交且总长至多
八，所以至多含七个 \(Z\setminus T\) 中的位置。双计数得到

\[
m\binom{|Z|-|T|}{3}
\le\sum_{A\in\mathcal F}\binom{|A\setminus T|}{3}
\le35|\mathcal F|.
\]

因 \(|Z|-|T|\ge3p-4\)，

\[
\boxed{
|\mathcal F|\ge
\left\lceil\frac{m}{35}\binom{3p-4}{3}\right\rceil
=\Omega(p^4).}
\]

这个四次量级下界不需要极值补原子支；`proofs/triple_cover.md` 在该
支中用六项截集 \(C\) 把 \(3p-4\) 进一步提高为 \(3p-2\)。

锚点补零还给出普通匹配界。若 \(p\ge11\)，四个两两不交的
\(\mathcal F_1\) 块连同 \(p-4\) 个锚点形成长度至多
\(p+20\le3p-2\) 的零和，故 \(\nu(\mathcal F_1)\le3\)。当
\(p=7\) 时，任意四个互不交块的总长至少 \(17\)；若有六个互不交
块，按长度排序后总长至少 \(27>|Z|=25\)，故
\(\nu(\mathcal F_1)\le5\)。

这些普通覆盖与相交条件本身不会产生矛盾。对任意
\(n=3p+4\) 元集合取固定三点集 \(Q\)，令

\[
\mathcal F_1^*=\left\{A\in\binom X5:|A\cap Q|\ge2\right\},\qquad
\mathcal F_2^*=\left\{A\in\binom X6:|A\cap Q|\ge2\right\},\qquad
\mathcal F_3^*=\left\{A\in\binom X8:|A\cap Q|\ge2\right\}.
\]

三族均无公共点、任意两块相交、横截数为二；每个三点集属于至少
\(3p-2\) 个 \(\mathcal F_2^*\) 块。因此即使保留普通三点覆盖数与
常数横截，也必须重新使用带符号同余、固定群和、补原子交换或统一
商标号，才能继续推进。
