# 双侧补集线陷阱对抗验缝

STATUS: CORRECT

ROUTE STATUS: DEDUPLICATED。此票只认证下述自足推导正确；后续公共
审计已识别该推导为 `A_exterior_double_sum_obstruction` 的直接推论，
所以不能据此登记第二条独立路线或第二份数学进展。

JUSTIFICATION: 对每个 \(\lambda\)，(CONST) 的非零带符号系数确实保证至少一个实际位置子集 \(A\)。即使 \(C,C'\) 重叠，仍有

\[
|B|+|B'|=4p-4+|C|+|C'|\le4p+4,
\]

故至少一侧不超过 \(2p+2\)；两侧非空时完全满足 (SQ)，从而把全部 \(p\) 个 \(\lambda\) 压入至多六元素集合，\(p=7\) 仍严格矛盾。长度和、和值及补集符号正确，也未要求 \(B,B'\) 彼此不交。

\(p\ge11\) 的空侧加强版同样成立：\(B=\varnothing\) 仅可能在 \(C=\varnothing,\lambda=0\)，\(B'=\varnothing\) 仅可能在 \(C'=\varnothing,\lambda=\kappa\)，至多两个例外；其余系数仍落入六元素集合，合计至多八个，小于 \(p\)。证明没有从 \(\Lambda_i\) 推导未加权总和，也没有复活已撤回的 \(\theta=-1\Rightarrow\sigma(R)=0\)。

验证边界：只认证 `proofs/double_line_trap.md` 与 `route_a_double_line_trap.md` 中该引理及推论；不认证完整 \(A_p\)。
