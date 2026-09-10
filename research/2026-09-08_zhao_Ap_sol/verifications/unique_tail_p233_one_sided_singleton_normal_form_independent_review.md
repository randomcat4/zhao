# \(p=233\) 单侧 singleton 支闭合：独立复核

STATUS: **CORRECT / FINAL PROOF BOUND / GLOBAL INCOMPLETE**

绑定证明
proofs/unique_tail_p233_one_sided_singleton_normal_form.md，
SHA-256
0a1f76a3389577540f08601c6d7a026bd8062f8408eccb33a2f481e734277dd5。

独立核验确认：

1. 长七删双尾的仿射签名与空 \(-r\)-纤维给
   \(c(r)=2\)。单侧支中 \(r\) 的全部表示恰为 \(m\) 个 singleton，
   所以 \(-m=2\pmod{233}\)；结合最大原子标签容量，唯一得到
   \(m=231\)。
2. Property B 重标签不等于 \(r,e,f\)。\(r^{231}ef\) 恰耗尽标准形
   的 233 个线位置，故
   \(Q=g^{232}r^{231}ef\) 且 \(g=e+f-2r\)。
3. 共同核避开三尾并满足 \(|K|\ge435\)，所以其中至少有 204 个
   \(g\)-位置和 203 个 \(r\)-位置。
4. 另外任一 singleton 长补原子同时含第三尾
   \(\gamma=-e-f\) 与同一 \(K\)。一个 \(g\)-位置、两个互异
   \(r\)-位置和该尾位置组成四位置真零和，因为
   \(\gamma+g+2r=0\)。这严格违反该长补的投影原子性；其长度七或八
   不影响论证。

因此 540 个含长七 singleton 的 outer rows 中，无双点交换支全部
关闭；各行仍可能进入真实 \(2\leftrightarrow1\) 交换支，故没有删除
outer row，也没有完成固定 \(p=233\) 切片或全局 \(A_p\)。
