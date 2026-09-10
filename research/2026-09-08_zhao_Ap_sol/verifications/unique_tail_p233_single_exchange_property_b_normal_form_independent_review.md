# \(p=233\) 长七 singleton 单交换正规形：独立复核

STATUS: **CORRECT / FINAL PROOF BOUND / GLOBAL INCOMPLETE**

绑定证明
proofs/unique_tail_p233_single_exchange_property_b_normal_form.md，
SHA-256
9d072382e69f2df4a8ef3aafcc59f9fcc1d089baedd8218b342c3eb2055bc51f。

独立核验确认：

1. Property-B 点加仿射线支撑不存在长度小于 \(p\) 的带重复非空
   零和关系。因此正负两个 signed mixed 目标不可能同时有长度至多二
   的避尾表示；长七情形恰有一侧避尾。
2. 双点表示按线项数 \(0,1,2\) 的分类完整。零线项和双线项都会以
   足够的实际位置容量制造长度大于二的反向避尾表示；单线项且一个尾
   为重项时亦如此，唯一容量例外恰违反 packing--尾标签排除。
3. 任一幸存交换因此严格取形
   \(U_Q=\{\ell_c,\ell_d\}\)、
   \(E=\{g,\ell_a\}\)、\(s=\ell_{a+1}\)，且反向目标需要
   \(p-1\) 个线位置，而非尾线位置只有 \(p-2\) 个。
4. 交换后 \(Q'=g^{p-2}L'\)，\(L'\) 有 \(p\) 个线位置且系数和二。
   全部 \(-g\)-表示恰为“全取 \(L'\)，再取 \(p-3\) 个重项”，所以
   强制核为 \(L'\)，非尾部分恰有 \(p-2=231\) 个位置。
5. 文末显式模型确为最大原子，且 \(K\cup\{\gamma\}\) 零和自由；
   它同时明确违反完整尾锚定，只用于否定更弱的共同核投影推断，没有
   被冒充为完整 outer-row 实现。

结合已审的单侧 singleton 支闭合，540 个含长七 singleton 的 outer
rows 全部被迫进入上述单侧双点交换正规形。本文不删除 outer row，
也不完成固定 \(p=233\) 切片或全局 \(A_p\)。
