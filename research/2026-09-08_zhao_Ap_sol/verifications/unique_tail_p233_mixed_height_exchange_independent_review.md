# \(p=233\) mixed 高度交换：独立复核

STATUS: **CORRECT / FINAL PROOF BOUND / GLOBAL INCOMPLETE**

绑定证明
proofs/unique_tail_p233_mixed_height_exchange.md，
SHA-256
ab76d94d29ed1b028e07b3e03de2029ee75a56b6f0c2e0750b6c942aef866c24。

独立核验确认：

1. 自动块 \(D_A\) 的长度为 \(8-e+|E|\)，实际和为
   \(3a-ex+\sigma(A)\)，所有位置并均为字面不交并。
2. \(D_A\) 有非空 \(X\)-核心而尾严格包含 \(U\)，所以其 \(F_3\)
   身份违反唯一正核心尾。结合三族长度窗，恰余证明中的四个
   \((e,|E|,F_j)\) 分支。
3. 用 \(\sigma(P)=\sigma(z)+\sigma(z^\ast)=3x-a\) 回代，三个单点
   平移与双点的 \(\sigma(E)=\sigma(z^\ast)\) 都是完整
   \(C_{233}^4\) 等式。
4. 两个 signed 避尾族交叉相交；若两边都只取单点，共同位置会同时
   有投影 \(s,-s\)，与 \(s\ne0\) 及奇特征矛盾。因此两边都非空时
   至少有一个双点表示，双点只能落在 \(e=3,F_2\) 分支，并严格给出
   \(2\leftrightarrow1\) 实际和交换。
5. 作用域精确覆盖全部 540 个恰有一个长七 singleton 的行；另只
   条件覆盖 180 个“三个 singleton 均长八”的行中的尾方向分支。
   其中仅 36 行的全部端点都长八；证明没有覆盖一般方向。

初审指出的“把 180 行称为全长八”作用域缺口已修复。本文不删除
outer row，也不闭合固定 \(p=233\) 或全局 \(A_p\)。
