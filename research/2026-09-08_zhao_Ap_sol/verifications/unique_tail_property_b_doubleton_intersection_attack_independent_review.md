# Property B singleton/doubleton 公共核攻击：独立复核

STATUS: **CORRECT / FINAL ARTIFACTS BOUND / GLOBAL \(A_p\) INCOMPLETE**

## 1. 绑定工件

- 证明：proofs/unique_tail_property_b_doubleton_intersection_attack.md，
  SHA-256
  99389d96a72a78a47fe9df9125cc02bbd7a22d4cc01eb82c67b64de03c2ee2ac；
- 程序：unique_tail_property_b_doubleton_intersection_attack.py，
  SHA-256
  9d6b643bc4031364e48326070466d4c82299ab41cb55ea396baa78492740255b；
- 报告：unique_tail_property_b_doubleton_intersection_attack_report.json，
  SHA-256
  0200f5fad0aa28be8c2c22e9527e3147a2a34fcba58af9037d880f07b192e16c；
- 报告规范证书：
  99ea267be21c8400d482ea315812c581e36c42ad70593c0e9352d40088b5a42e。

## 2. 独立裁决

独立重推确认：

1. 当共同字面子序列 \(K\) 满足 \(|K|>p\) 时，Property B 标准域
   要么全部相同，要么恰为 canonical transverse 两域；后一情形的
   公共支撑严格等于 \(\{g,h,g+h\}\)。
2. 在明写
   \(K\cap\{u_e,u_f,u_t\}=\varnothing\) 后，
   complementary singleton--doubleton 与 three-doubleton 两种应用
   都严格给出 \(|K|\le2p-4\)；固定 \(p=233\) 即 \(|K|\le462\)。
3. 交叉域中的
   \(c+\min(a,b)\le p-1\) 只在 \(K\) 至少是一个最大原子的真子序列
   时使用。最终稿已经补齐这个量词；实际尾应用自动满足它。
4. 长 \(2p-2\) 原子的补全二择一只约束删点后的序列，没有把人工
   Property B 域错误外推到原原子或被删位置。
5. 配套程序的模型 N/C/D 公共核分别为 \(463,462,456\)，并复现
   文中有限边界计数。

此前独审曾指出“真子序列”及“共同核避开三尾”两个陈述缺口；最终
绑定稿均已修复。该结论条件于 Reiher 的全素数 Property B 定理，
且不完成位置粘合、不删除 720 行、也不证明固定切片或全局 \(A_p\)。
