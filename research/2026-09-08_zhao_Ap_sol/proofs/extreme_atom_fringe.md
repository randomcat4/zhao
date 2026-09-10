# 极值秩三补原子的双边短表示恒等式

STATUS: PROVED_HERE

设 \(p\ge7\)，\(Z\subset R\) 是长度 \(3p+4\) 的实际零和原子，
\(C\subset Z\) 满足 \(|C|=6,\sigma(C)=2a\)。令
\(B=Z\setminus C\)，并假设 \(\bar B=\pi(B)\) 是
\(\bar G=G/\langle a\rangle\cong C_p^3\) 中长度 \(3p-2\) 的原子。

固定 \(b\in B\)，写 \(U_b=B\setminus\{b\}\)。则 \(\bar U_b\)
零和自由且长度 \(3p-3\)。在 \(\mathbb F_p[\bar G]\) 中，增广理想
顶次数为 \(3p-3\)，顶次部分由全和元 \(J_{\bar G}\) 张成，故

\[
\prod_{u\in U_b}(1-X^{\bar u})=\gamma_bJ_{\bar G}.
\]

左端零元系数只有空集贡献，等于 \(1\)；右端零元系数为
\(\gamma_b\)。所以 \(\gamma_b=1\)，即每个商目标的全部子集表示
带符号和都为 \(1\)。

取非空真子集 \(T\subset C\)，令 \(t=|T|\)。任取
\(E\subseteq U_b\) 满足
\(\bar\sigma(E)=-\bar\sigma(T)\)。两块

\[
K=E\mathbin{\dot\cup}T,\qquad
K'=(U_b\setminus E)\mathbin{\dot\cup}\{b\}
   \mathbin{\dot\cup}(C\setminus T)
\]

非空、商和均为零，并分割 \(Z\)。至少一块长度不超过
\((3p+4)/2\le2p+2\)。由 (SQ)，该块实际和是
\(a,2a,3a\) 之一；长原子锚点线长度界继而给该块长度至多 \(8\)。
因此

\[
|E|\le8-t\quad\text{或}\quad|U_b\setminus E|\le t+1.
\]

两种情形互斥，因为 \(|U_b|=3p-3>9\)。定义

\[
L_{\le m}^{U}(x)=
\sum_{\substack{F\subseteq U,\ |F|\le m\\
\bar\sigma(F)=x}}(-1)^{|F|}.
\]

在第二类表示中令 \(F=U_b\setminus E\)。由于 \(|U_b|\) 为偶数且
\(\bar\sigma(U_b)=-\bar b\)，全纤维带符号和为 \(1\) 变成

\[
\boxed{
L_{\le8-t}^{U_b}(-\bar\sigma(T))
+
L_{\le t+1}^{U_b}(\bar\sigma(T)-\bar b)=1.}
\]

特别地，对每个 \(b\in B,c\in C\)，

\[
L_{\le7}^{U_b}(-\bar c)+L_{\le2}^{U_b}(\bar c-\bar b)=1,
\qquad
L_{\le3}^{U_b}(\bar c)+L_{\le6}^{U_b}(-\bar c-\bar b)=1.
\]

所有等式均在 \(\mathbb F_p\) 中。它们保证至少一项非零并给出真实
常数长度表示，但不声称计数为正或表示唯一。
