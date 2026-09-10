# 匿名自足复核：公共外部双和障碍的双侧补集推论

状态：PROVED；ROUTE_DEDUPLICATED。该证明验证陈述，但独立去重审计
已确认其结论是公共 `A_exterior_double_sum_obstruction` 的直接推论，
不再作为独立路线计数。

设 \(C,C'\subseteq D\) 非空，且 \(\sigma(U)+\sigma(C)+\sigma(C')=\kappa a\)。对任意 \(\lambda\in\mathbb F_p\)，常数非零纤维给出 \(A\subseteq U\)，使 \(\sigma(A)=-\sigma(C)+\lambda a\)。令

\[
B=A\cup C,\qquad B'=(U\setminus A)\cup C'.
\]

两者均非空，群和分别为 \(\lambda a\) 与 \((\kappa-\lambda)a\)，故都是 \(R\) 中的商零和。又

\[
|B|+|B'|=4p-4+|C|+|C'|\le4p+4,
\]

所以至少一个长度不超过 \(2p+2\)。短商零和三系数限制遂给

\[
\lambda\in\{1,2,3\}\quad\text{或}\quad
\kappa-\lambda\in\{1,2,3\}.
\]

这要求 \(\mathbb F_p\) 被至多六个元素覆盖，与 \(p\ge7\) 矛盾。

取任意非空真子集 \(C\subset D\) 及 \(C'=D\setminus C\)，若 \(\sigma(R)\in\langle a\rangle\)，就满足上述触发条件。因此 \(x_0=0\) 假想反例必有 \(\sigma(R)\notin\langle a\rangle\)。
