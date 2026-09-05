# 形式检查范围

已实际运行 Lean +leanprover/lean4:v4.30.0 PairArithmetic.lean，退出码 0。

两个定理检查 n≥r、j<r、x≤n−1−j 下的算术：0<x+k<2n，以及已知 x+k=n 时子序列长度 x+2k≥n+j+1。

未编码群、子序列、模 n 等式或文献结果。因此仅 LEAN_PARTIALLY_CHECKED，不是完整自然语言定理的形式化。无 sorry、admit、新增 axiom 或 unsafe。公理依赖为标准 propext、Quot.sound；第二定理另依赖 Classical.choice。
