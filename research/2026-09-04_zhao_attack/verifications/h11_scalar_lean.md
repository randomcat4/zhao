# H11 标量计数表的 Lean 核验

状态：LEAN_PARTIALLY_CHECKED。只覆盖715个计数向量及其选择证书，不是整个H11证明，更不是原A/B端点。

实际工具链：Lean 4.30.0（显式调用已安装的 leanprover/lean4:v4.30.0）。文件 formal/H11ScalarCertificate.lean，仅 import Std。

成功命令的退出码为0。实际输出：

    H11ScalarCertificate.all_counts_covered does not depend on any axioms
    H11ScalarCertificate.all_selections_valid does not depend on any axioms
    H11ScalarCertificate.number_of_counts does not depend on any axioms

三个定理分别检查：证书的n列表恰好等于全部非负五分量且和为9的规范枚举；每行k均逐分量不超过n、和为5，并满足零标量纤维的“一个至少3点的部分选择类/两个部分选择类”条件，或标量2纤维的“至少一个部分选择类”条件；总计715行。

表由 h11_continue_scalar_egz_v2.json 生成，生成器 scripts/root_continue_h11_lean.py。成功版本不含 sorry、admit、新增axiom或unsafe。

保留一次实现错误的记录：最初把布尔函数取名 partial，与Lean保留字冲突，编译退出1，并在失败的声明显示sorryAx；已改为isPartial后重新生成并实际成功。失败运行不是有效核验，不用于任何数学结论。

未形式化部分：从部分选择类到不同群子和数量的手工论证、H11两差分结构、二维投影与几何排除，以及输入序列的自然语言含义。它们须由独立逻辑审查承担，不能借此局部Lean证书跳过。
