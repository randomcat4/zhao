# \(p=233\) 长七交换星重数排除：独立复核

STATUS: **CORRECT / FINAL PROOF BOUND / GLOBAL INCOMPLETE**

绑定证明
proofs/unique_tail_p233_exchange_star_multiplicity_exclusion.md，
SHA-256
6bd9cfa49b6070801d0b3822d0856417c89e561b9010c0bf6f8c0fb874154f3f。

两次独立量词核验确认：

1. 单交换正规形的两个尾位置都在 Property-B 仿射线上，所以全部
   \(p-1\) 个重投影 \(g\) 的实际位置都避开 \(U\)。固定交换中的同一
   实际线位置 \(y\) 后，每个重项位置 \(x\) 都给合法的避尾双点表示
   \(E_x=\{x,y\}\)，且目标始终为同一个 \(s\)。
2. mixed 高度引理量化任意实际避尾表示，不只量化最初选定的
   \(E_0\)。对每个 \(E_x\)，\(|E_x|=2\) 逐点强迫轴系数 \(e=3\)；
   相应长度七自动块因尾严格包含唯一正核心尾而不能属于 \(F_3\)，故
   只能是 \(F_2\)。
3. 因而每个 \(x\) 都满足完整四维等式
   \(\sigma(x)+\sigma(y)=\sigma(z^\ast)\)。固定 \(y,z^\ast\) 后，
   \(p-1=232\) 个不同重项位置携带同一实际标签，严格违反当前假想
   反例中最大实际重数 \(p-4=229\)。
4. 结合已审的无交换单侧支闭合，540 个含长七 singleton 的 outer
   rows 全部删除，720 行精确降到 180 行。剩余行只是三个 singleton
   端点均长八；非 singleton 端点仍可长七或八。

本结论不处理剩余 180 行的 generic packing 方向，不完成固定
\(p=233\) 切片或全局 \(A_p\)。
