# 2365项标量表的实际Lean核验

状态：LEAN_PARTIALLY_CHECKED。只检查有限标量选择表，未形式化整个H11工具、星结构或原A/B。

运行工具链：Lean 4.30.0，显式选择 `leanprover/lean4:v4.30.0`。2026-09-04实际编译退出码0。输出为：

```
'StarD2ScalarCertificate.all_patterns_covered' depends on axioms: [propext]
'StarD2ScalarCertificate.all_selections_valid' depends on axioms: [propext]
'StarD2ScalarCertificate.number_of_patterns' does not depend on any axioms
```

这里propext是Lean的标准命题外延公理，不能把前两个定理写成“无公理”。没有sorry、admit或用户添加的公理。

覆盖语义：715个九位置标量计数向量，其中全互异标记为5；另有1650个“一个重复对所在标量类r、n_r≥2”模式。每行选择五位置，标量和为0或2，并有一个被部分选取且包含至少两个不同实际值的类。最后一步“该类产生至少两个不同实际子和”的群论论证在自然语言证明中，不在此Lean文件内。

冻结文件SHA-256：

* formal/StarD2ScalarCertificate.lean：552b9515aca60855de078c76fb74b78c9c51e6b2fc542d1310ea0a0e0ae0374c
* evidence/root_continue_star_d2.json：2cd26a16f767815b540be55f678833e1bcafac4e0b87e5c23a79a393d7955fe6
* proofs/root_continue_star_d2.md：d0b68aec99ccf1a98e82615b8c82ed13bb8382633ee0436caf29480c7b056ea7

生成程序为 scripts/root_continue_star_d2_lean.py。该程序生成有限表，真实核验由Lean执行，不能把生成文件本身当成核验完成。
