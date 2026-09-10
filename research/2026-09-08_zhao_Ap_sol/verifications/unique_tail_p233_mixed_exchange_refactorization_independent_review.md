# \(p=233\) mixed 交换重分解：独立复核

STATUS: **CORRECT / FINAL PROOF BOUND / GLOBAL INCOMPLETE**

绑定证明
proofs/unique_tail_p233_mixed_exchange_refactorization.md，
SHA-256
a666a78e8318ff756f5e83644a559fb1808c3f2b78f929977bc0ff2b47eb2d27。

独立核验确认：

1. 从 \(\sigma(E)=\sigma(z^\ast)\) 出发，交换后的 \(P'\) 与原 \(P\)、
   \(Q'_H\) 与原 \(Q_H\) 分别保持完整四维和；轴系数为 \(3,1\)，
   \(\rho\)-和均为零。
2. \(P'\) 的三个单点及三个二点真子集都非零，故它确为长度三
   \(\rho\)-原子。
3. 任取 \(Q'_H\) 的原子分解并与 \(P'\) 合并，就得到 \(W_H\) 的
   原子分解。已审分解型中含系数三者只能是 \((1,3)\)，因此
   \(Q'_H\) 本身是唯一的系数一原子。
4. 长度严格为 \(465\to464\) 与 \(464\to463\)。三点 packing 的
   三个 singleton 代表与其 complementary doubleton 穷尽六个
   非空真子集的三个补轨道；每个目标条件都量化全部实际 \(T\)。
5. 双交换时两个双点表示必不同且恰共享一点；两条新原子共享
   \(Q_H\setminus\{w,u,v\}\)。长七 singleton 情形公共核长度为
   \(462\)，两个二点花瓣的完整实际和相等。

最终稿已明确：原来的 461 complete-deletion 定理不直接套到新
\(Q'_H\)，而只与新原子的一般 near-max completion、mandatory-core
表示及 \(q\)-矩联立。本文不删除 outer row，不证明固定切片或全局
\(A_p\)。
