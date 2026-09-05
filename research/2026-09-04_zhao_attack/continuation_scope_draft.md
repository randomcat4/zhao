# 本次继续证明的最终范围

本文件用于最后一次独立范围审查；完整A/B仍不得写成已证。

原端点仍为 A：F5⁴ 任意21位置序列有≤13非空零和；B：任意20位置序列有≤14非空零和。原数值区间19≤s≤14≤s≤13≤22，K(C5⁴)∈{10,14,15}保持不变。

本轮已经拿到的审查：

* 七双重类：proofs/seven_doubles_continue.md + verifications/verify_seven_fresh.md，CORRECT。a=0时b≤6。
* 十九个互异元素与十八元核心追加：proofs/global_continue_squarefree_B.md、global_continue_support18_B.md + verify_global_continue_squarefree_support18.md，CORRECT；该审查报告附加一句有符号位置错误，需同时绑定 verifications/global_review_erratum_pending.md 的独立确认。候选正文只引用已排除16-atom，不使用错误附加句。
* 根实例两条商群工具及1881核：proofs/root_continue_dense19.md、root_continue_two_exceptions.md + proofs/verify_root_continue_core.md，CORRECT，独立按位置重建。

仍待最终报告：

* proofs/root_continue_all_H12.md 的五树完整归约与几何分支已由 proofs/verify_root_continue_all_H12.md 审核为CORRECT；A/B任意三维线性子空间H均有|S∩H|≤11。
* h11_continue_B_proof.md 已由全新上下文 evidence/verify_h11_final_fresh_report.md 审核为CORRECT；它仅排除B的三个三重值H11分支，所以B的a=3只能b=0且H占9或10位置。A的H11仍不可删。
* 16-atom 星形结构正文已交叉审为按范围正确；M=1分支已分别得到d2手证及d3/d4有限排除。原d3证据有共享数组别名错误，必须绑定continue_atom16_star_addendum_erratum.md与全新验证者的真实树，不能引用原错误表。修复后只留下M=0，不自动声称16-atom被排除。

若上面两个大局部分支通过，则反例重数的剩余范围为：

|a（三重实际值数）|A的b范围|B的b范围|
|---|---|---|
|0|0..6|4..6|
|1|0..5|2..5|
|2|0..3|0..3|
|3|0..1|0|

A的支持仍至少14；B的支持在13..16之间。B的a=3行支持恰14，其三重张成H只能占9或10项。B的支持17排除见root_continue_atom17_integrity.md、root_continue_support17_exclusion.md及三份独立交叉审核；短证明不依赖尚待解决的六边图。表未声称所有列出分型都能实现，也未用有限搜索没有命中来删行。

H≤11和B三重H≤10只是必要条件，剩下各分型和较稀疏子空间的全部序列仍未排除。16/17-atom在M0下等价且只余d4，但六边图局部闭合命题有显式九值反例；该反例不是17-atom或B反例。特别不能把168177个H12核心覆盖误写为全部F5⁴端点序列覆盖。

验证范围：H11的715计数选择证书已通过Lean4.30、无公理；完整A/B没有Lean证明。全体A/B没有真实反例。所有计算是本机小范围/完整有限归约，没有启动欧拉或付费外部运行，没有发送作者邮件。
