# 有限算术回归检查

STATUS: CORRECT

JUSTIFICATION: 使用 `verify.py` 检查了三类有限接口：

1. 对所有 \(7\le p\le500\) 的素数及 \(0\le d\le4\)，显式矩阵 (2) 确为四个允许长度层到 \(q=0,1,2,3\) Hasse 阴影矩阵的逆；
2. 对同一批素数，双侧补集推论中的允许系数集合大小始终至多 6，
   且严格小于 \(p\)；同时核对
   \([0,p-4]+[0,p-4]=\mathbb F_p\)，以及 \(p\ge11\) 时
   \([1,p-4]+[1,p-4]=\mathbb F_p\)，而后式在 \(p=7\) 确实失败；
3. 对 \(p=29,31,37,101,499\)，核对实际族 \(U_p\) 的非零顶积常数、目标最短表示长度 \(4p-28\) 及其自身长度 \(p-3\) 的短零和。
4. 对 \(149\le p\le2000\) 的全部素数，核对路线 B 修订稿所用的特殊类型表：选定承重类型不能配普通类、不满足半值自反，其倒置类型也不在完整特殊表内。
5. `verify_atom_hasse.py` 对 \(7\le p\le500\) 的全部 92 个素数核对七点支撑多项式的三个比值、\(3p+3\) 零阶值、\(3p+4\) 一次 Hasse 值、二点删除的两条共度恒等式及三点删除恒等式；同时核对由奇偶性/非负性得到的普通计数下界。脚本还确认前者 11 个小表示变量上的系统相容且秩为 9，后者 12 个变量上的系统相容且秩为 11，并核对隔离坐标 \(N_6^Z(2a)=1/5\) 的十项有理线性证书。加入一个固定位置的分长度计数后，合并系统在 24 个全局/局部变量上秩为 20，仍余四个局部自由变量。
6. `verify_exchange_models.py` 对同一批 92 个素数逐一核对
   \(r=6,7,8\) 三个商群交换模型的坐标和、小块原子性及长度
   \(3p-2,3p-3,3p-4\) 补原子方程。
7. `verify_abstract_design_model.py` 以确定性随机种子与有限域消元重建
   \(p=7\) 弱加权超图，并核对它有 \(492\) 个未覆盖三点集、
   \(2025\) 个三点同余失败以及满 \(25\) 列秩，故只是否定旧弱公理。
8. `verify_triple_kernel_model.py` 重建 \(p=7\) 的三点同余完备、核维
   恰三模型；并核对核只在六个位置非零、不能支撑长度 \(17\) 的
   补原子，且全部 \(29890\) 个不同 \(F_3\) 交集商和为零。
9. `verify_second_branch_models.py` 对全部 \(7\le p\le500\) 素数
   核对三项/四项特殊删除插值、固定二项块的分长度参数式、长度
   \(3p-4\) 标准补原子的原子性，以及共横截菱形局部模型的和值、
   高度与商交接口。
10. `verify_standard_atom_templates.py` 在 \(p=7\) 从头重建两个固定
    六点模板的轨道矩阵、秩差及十三项证书；另对所有
    \(11\le p\le500\) 素数回归强模板的同值位置对最短商零和长度
    为八。一般 \(p\ge11\) 的排除由符号整数提升证明承担。
11. `verify_standard_pair_system.py` 穷尽标准
    \(C=(\pm2e_1,\pm2e_2,\pm2e_3)\) 模板在 \(p=11,13\) 的全部
    三方向对称高度重数向量，分别检查 \(184030\) 与 \(2702973\)
    个合法向量均不满足完整两组类内二点方程；非对称固定种子样本
    只记为探针。
12. `verify_standard_coordinate_pairs.py` 对 \(p\le101\) 回归全部
    三轴非零幅度模板的典范短块、有限值子集和与大幅度三点障碍。
13. `verify_standard_axial_subset_avoidance.py` 核对任意六点轴向
    子集和的四个精确例外，并穷举 \(11\le p\le53\) 的
    \(668880\) 个规范化高度支撑样例。
14. `verifications/verify_standard_atom_triple_filter_review.py` 核对
    一般六点块的三点候选过滤器、\(\pm3e_i\) 模板高度塌缩及边界。
15. `verify_short_exchange_models.py` 对全部 \(7\le p\le500\)
    素数核对长度三、四交换度局部模型及每块 \((p-4)^2\) 个邻块。
16. `verifications/verify_standard_atom_full_exclusion.py` 核对满商
    纤维排除的 \(1365\) 个参数边界、\(83892\) 个二值高度案例、
    \(7809477\) 个三值高度案例及全部碰撞素数。
17. `verify_p_minus_two_height_fibre.py` 对 \(p=11,13,17,19,23\)
    穷举临界高度分类，复算三个三点共度矩阵及 \(p<500\) 的整数
    提升，精确留下三个 \(p=11,19\) 中间余支。
18. `verify_p_minus_two_residual_degree_system.py` 核对
    \(X\)-交数一、二的完整允许族、有限余支的点度贡献及异常位置
    对的共度矛盾。
19. `verify_p_minus_two_survivors.py` 核对三个余支的独立锚点
    证书：群和系数、位置资源与长度 \(10\)--\(12\)、
    \(16\)--\(18\)、\(34\)--\(36\) 均正确。
20. `verify_p_minus_three_height_frontier.py` 穷举
    \(p=11,13\) 的全部次临界高度轮廓与异常点允许族，并显式覆盖
    \(p=11,b=7,\ell=8\) 端点。
21. `verify_p_minus_four_monochromatic_frontier.py` 核对 51 个完整余部
    变量、28 个三点覆盖类型、五个素数阈值上的单点余部消失数，及
    只使用五点余部的稀疏标量矩解。
22. `verify_p_minus_four_single_height_probe.py` 核对 1968 个锚点
    单点容量界、820 个纯 \(T\) 三倍余部资源参数及 1148 个纯
    \(X\) 矩代表；输出明确限定为 Hasse 层相容性。
23. `verify_p_minus_four_star_design.py` 对十个素数核对负二项式统一
    系数、点/对/三点标量解与全部可实现核心交数区间端点；不构造
    实际尾集或群值标号。
24. `verify_p_minus_four_height_reduction.py` 穷举 \(p=13\) 的全部
    二值、三值高度轮廓和异常点允许族，并显式核对 \(p=11\) 的
    长度八、七点全核心确实不给高度分类。
25. `verify_p_minus_four_mixed_hasse.py` 以精确有理数核对逐外点求和
    尾长矩、旧六变量证书的失效，以及 \(s=6,7,8\) 三张分别满足
    21 条零阶/纯 \(X\)/\(T\)-点/\(Q\)-点方程的加权证书。
26. `verify_p7_six_fibre_exclusion.py` 在 \(\mathbb F_7\) 中重建
    六重纤维 104 个高度轨道的逐位置 Hasse 矩和九个稀疏证书；
    再对五重 59 个轨道逐一枚举至多 \(4^4\) 个单点 cap 赋值。
    五、六重全部排除，重数三、四的 41 个放宽轨道仍相容。
27. `verify_p11_seven_fibre_star_exclusion.py` 重建全部 1768 个七点
    高度轨道与 98 行逐位置 Hasse 星系统；精确消元只留下单高度和
    负单异常，再核对两行投影强制五个同值尾点及八项锚点零和。
28. `verify_p_minus_four_two_tail_exchange.py` 对 91 个素数核对二尾
    核心压缩区间、交换长度、嵌套方向及同值双位置形式赋值；后者
    未重建全诱导短谱，不认证局部候选。
29. `verify_p_minus_four_cross_family_tails.py` 核对三族非零点度、
    两组跨族交换、\(p\ge17\) 尾交阈值及三尾形式赋值；后者未重建
    全诱导短谱。
30. `verify_p_minus_four_unique_f3_tail_arithmetic.py` 分解十五个唯一尾
    固定整数，得到十一项异常素数；并核对普通尾数下界
    \(\lceil(p-1)/2520\rceil\) 及三个二点尾参数。
31. `verify_p7_four_fibre_refinement.py` 对 29 个四重高度轨道作精确
    仿射投影，核对 28 个全核心强迫型与唯一低迹例外；修订后还复现
    旧例外标签候选诱导的两个嵌套 \(F_3\) 块及零商交。
32. `verify_p_minus_four_unique_f3_tail_hasse.py` 对唯一尾异常表的
    16 个 \((p,\ell,b)\) 类型及全部允许 \((s,j)\) 重建 21 条聚合
    Hasse 式；每个系统系数秩与增广秩均为 20，并逐式回代规范见证。
33. `verify_p7_three_fibre_refinement.py` 对 12 个三重高度轨道作精确
    仿射投影，核对 11 个全核心强迫型、单高度九列投影、单点尾全零
    形式切片与容量；同时复现旧三尾标签候选诱导的零商交碰撞，按
    EXPECTED REJECTION 处理。
34. `verify_p7_four_fibre_induced_labels.py` 枚举四重例外旧候选的
    全部已赋值二至八元子集，重建 24 个 \(F_1\)、125 个 \(F_2\)
    与 97 个 \(F_3\) 块，并给出首个零商交的嵌套 \(F_3\) 块对。
35. `verify_p_minus_four_unique_tail_position_frontier.py` 核对 16 个
    唯一尾异常型的逐位置分式、实际零核心块数下界及三个二点尾型
    的非零迹入射矛盾；输出 3 型排除、13 型幸存。
36. `verify_p_minus_four_multi_tail_global.py` 核对 15 个尾参数型、
    链长至多三、23 个三链候选中的 16 个实际菱形型、可比对常数
    112 及 20 阶小行列式 \(-512000\)。形式尾回归未重建全诱导
    短谱，不认证局部候选。
37. `verify_p7_four_fibre_tail_local_state.py` 严格拒绝第二个 16 点
    候选：除重放 44 个合法窗块及 946 对交检查外，找出 31 个非法
    短商零谱和已指定 \(B\) 内 93 个非空商零子集。
38. `verify_p7_three_fibre_labelled_csp.py` 提供完整 25 位置赋值核验
    入口，重建全部 \(b=0\) 在内的短谱、零阶/点/对/三点 Hasse、
    固定 \(B\)、实际 \(Z\) 与每个 \(F_3\) 补原子。默认重放商原子
    骨架；JSON 抬升按预期被高度五的二项 \(b=0\) 商零块拒绝。
39. `verify_p7_heavy_quotient_fibre_context_exclusion.py` 对同一三重
    纤维商赋值作高度无关预传播：四个 \((1,0,1)\) 位置之外的两个
    \(T\) 标签之和为 \(-(1,0,1)\)，故四条三项短谱方程秩为三并
    强制四个高度相同；整副 22 外点商赋值不存在严格高度抬升。
40. `p7_m3_next_heavy_fibre_solver.py` 使用长度 \(2,3,8\) 单值窗
    建立四重商纤维的六类禁尾，并对式 (16) 的固定 \(B=q^3Q\)
    穷举全部六位置非零零和 \(T\) 商标签多重集。72,306 个合法
    五位置前缀的唯一闭合全被拒绝，存活 \(S_6\) 轨道为零。
41. `verify_unique_tail_next_trace_excess.py` 重建 16 个唯一尾异常型，
    删除三个已排除二点型，并复核 13 型的迹盈余、加强块数下界及
    三个 \(b\ge4\) 结构行；11 型严格提高，块对下界为 1628、9310。
42. `verify_p7_m4_next_csp.py` 对唯一 \(0001\) 四重轨道重放固定
    \(B=q^4Q\) 的三目标原子判据、六类商迹窗、零核心剩余与
    84→68 规范化；完整赋值入口重建全部二至八元短块，并以 12+13
    折半 oracle 精确拒绝九至十二元商零集。显式固定 \(B+T\) 商
    赋值按预期被一对和为 \(-q\) 的外点拒绝，其他 \(T\) 仍保留。
43. `verify_middle_quotient_gap.py` 对 92 个素数核对取补端点、
    \(1,2,3\) 系数不可能互为负元、首次越过 \(p+1\) 的多块容量，
    并精确列出四个小素数的二块长度表。
44. 修复后的 `verify_p7_three_fibre_labelled_csp.py` 用 12+13 折半
    oracle 排除 9--12 元商零集；独立动态规划复得默认实例四层计数
    4166、6541、8559、10392，并在 203 组差分输入上与折半判定一致。
45. `p7_m4_unified_quotient_search.py` 复算固定 \(B\) 的四层谱大小
    305、312、312、305，覆盖全部 342 个非零值；342 份规范见证的
    首大小分布为 305、23、11、3，哈希固定。
46. `p7_m3_other_B_solver.py` 核对三个新固定长度 19 原子的原子性、
    四层谱与逃逸集；两个逃逸集为空，一个只余 \(\pm(1,6,1)\) 并
    被四条二元高度窗排除。
47. `verify_unique_tail_labelled_position_next.py` 在 72 个小实例上
    对照轴向原子判据与直接定义，扫描投影分解系数型，并重建 13 型
    逐迹表；`--instance` 入口保留为精确但未提供通过样例的本地核验器。
48. `verify_p7_fixed_B_orbit_deduplication.py` 核对
    \(A(x,y,z)=(x,y,x+z)\) 的逐值重数像、四层谱线性像与指定纤维
    位置数 4/3 的差异。
49. `p7_length19_pair_mutation_frontier.py` 穷尽旧三重 \(B\) 的
    6840 个一步等和二位置变异多重集，留下 8 个原子；独立 9+10
    折半与基运输复核两组哈希、8976/10304 次轨道试验、两个旧轨道
    匹配、三个高纤维覆盖及三个新低纤维谱排除。
50. `verify_p13_unique_tail_labelled_attack.py` 核对三点尾轴向系数
    \(\{1,2\}\)、三个秩一与一个秩二投影正规型、42/534 覆盖模板
    界，以及五点尾无轴向点和二加三分解系数
    \(\{0,1,2,3,4,5,12\}\)；独立枚举未导入目标模块并复得同表。
51. `verify_p7_tail_conditioned_middle_spectrum.py` 核对完整尾条件化
    9--16 层判据、补集对称和尾子集大小 1--3 的缩减；现有十二个
    固定原子均在单点行或高纤维定理处退出。
52. `p7_length19_second_pair_frontier.py` 穷尽七个低纤维源的一步
    邻域并复得 39,276 个候选、十个原子、三个新轨及全部空逃逸集。
53. `p7_length19_canonical_augmentation.py` 穷尽指定三重纤维的支撑
    五、六前沿：支撑五无原子，支撑六有 24 个规范命中、两个稳定子
    轨，二者中层谱均覆盖全部非零值。
54. `p7_length19_support7_escape_search.py` 穷尽 170 个重数型，得到
    381,309 个完整零和候选、16 个非空逃逸原子命中、四个稳定子轨；
    四轨的六点零和逃逸尾数均为零。
55. `p7_m4_68_layered_solver.py` 穷尽固定代表的实际多重集图半径二，
    原子层数为 1/8/530，指定四重分支数 2/10/8，全部为空逃逸。
56. `p13_three_tail_internal_spectrum_slice_unique13.py` 把三点尾含高度
    覆盖从 534 缩到 511，把五点尾可分解投影从 91 缩到九个模式。
57. `p13_unique_tail_exterior_coupling_frontier.py` 核对 14 个外部
    轴系数型、118/83 个长度前沿和 60,298/747 个待填充分片；坏尾
    输入由严格核验器按预期拒绝。
58. `verify_p7_maximal_atom_escape_algebra.py` 在七个冻结原子上逐位置
    核对删点顶积、射影简单性、全部 \(2^{19}\) 子集补双射、交错
    恒等式、交叉相交与每个三/四重纤维的缺口梯。
59. `unique_tail_position_conflict_frontier.py` 复算 13 型轴向尾点、
    \(q\)-标签容量、503 个多迹块、10,938 条不交迹边，以及
    471/2,803 个尾外位置上的四重拥塞证书。
60. `p7_m3_full_support7_mutation_probe.py` 核对四个支撑七源的
    234,612 个位置替换、17,936 个逐源一步邻域并集、69 个含零自动
    非原子及最终 12,615 个支撑至少八候选全为非原子。
61. `p7_m3_full_support8_frontier.py` 穷尽 462 个规范重数型，两次正式
    重放与独立实现均复得 1,846 个完整零和候选全被六尾门删除。
62. `p7_m4_full68_short_support_search.py` 与
    `p7_m4_full68_support8_verify.py` 核对无三重纤维的 42 个短支撑型、
    66 个支撑八型、三个命中、两个轨道及零六尾，并验证与三重支撑八
    定理的条件拼接元数据。
63. `p7_support9_structure_pruning.py` 与
    `p7_plane_projective_zero_sum_free.py` 用两个独立状态实现复得
    (C_7^2) 射影简单零和自由序列最大长度 11，并核对 77 个最大
    剖面轨道、(PG(2,7)) 最大 arc 八、完整 pointed profile 表及
    18 个明确非原子的粗门骨架。
64. `p7_m34_support9_search.py` / `p7_m34_support9_verify.py` 穷尽
    ((3,2^8))、((4,2^7,1)) 两个 support-9 签名的八个规范入口；
    166,345,680 个五层前缀仅有两个完整候选且逃逸域都空，并核对
    修正后的 5,741 共线覆盖分母。
65. `unique_tail_four_edge_joint_csp.py` 核对 11 个端点图型、15 个
    四边迹子图、28,584 个迹赋值、共同外部谱 packing，以及 12 个
    逐子集与局部卷积完全一致的小位置例。
66. `unique_tail_common_R_next.py` 核对共同 (R) 的七个 packing 型、
    14 个端点余部分解行、三个强制共同余部原子型与两个素数上的
    (D(C_p^2)-43) 零和自由长度见证。
67. `unique_tail_seven_type_full_f3_interface.py` 在 12 个小位置例上把
    4,212 个三状态记录、21,504 个四状态 Venn 记录分别与直接子集
    穷举逐项比对，并在 (C_3^2) 复核 1,073 个原子的整体例外；证书
    哈希为 `9dfe70ad3c9693d5048b3deb4ec28d12c990e98bf62aff6612494ed65d11ccd5`。
68. `unique_tail_forced_common_atoms_attack.py` 独立复得 28,584 个迹
    着色、15,072 个无双点迹覆盖候选着色和 24,468 个候选对出现，
    并在 (p=233,1399) 逐位置核对十位置局部幸存者及三种 packing；
    证书哈希为 `4eebafc1497d110e25ac82fe8825f1579fc4957ddd666a5ebd83cdf3f5a749c3`。
69. `unique_tail_cover_survivor_lift.py` 以两种独立枚举重建十位置固定
    标签的 14 条局部商零短块（13 条合法、1 条坏行），并核对六个
    派生 (F_3) 的 38 个局部补内子集、72 个短块交门、15 个
    (F_3) 对；位置重数核另复得三条长度 (p-b+1) 禁区块。证书哈希为
    `4d5da443323c68e487a8f98b898d6aa3bd649a1fa9b2edbf369bb5e822b0295c`。
70. `p7_support9_collinear_real_search.py` /
    `p7_support9_collinear_real_verify.py` 完整核对四个新支撑九签名的
    56/118/197/282 个共线入口、945/1,908/3,636/5,382 个全签名
    换基代表及 23,508 个原始标架。第一/第三签名无完整候选；第二/
    第四签名的 1,498/2 个候选单点逃逸域全空。四个报告 SHA-256
    依次为 `01a9dbe0...4505`、`c655c8b5...ff86`、
    `2d7bfacf...df57`、`cbdd1604...a87a`。
71. `p7_support9_collinear_real_remaining.py` 完整核对签名
    \((3,3,3,2,2,2,2,1,1)\) 的 410 个入口、14,760 个原始标架和
    8,685 个换基代表；3,064 个完整候选全部在单点逃逸门排空，零
    原子/六尾/位置尾幸存。报告文件 SHA-256 为
    `b92fed7d...23a20`，独审裁决 CORRECT。
72. `unique_tail_cover_forbidden_block_generalization.py` 核对全部 26 个
    单位二余部形式、11,732 个逐位置度小实例、28,584 个迹着色、
    13,512 个含覆盖候选的着色和 24,468 个覆盖对出现；两个素数上
    分别检查 28,340,748 个稠密形式、317,826 个迹不交大核门及
    16,971,084 个单位形式。规范证书为 `36ed4fe5...c10`，全新独审
    裁决 CORRECT。
73. `p7_support9_collinear_real_remaining.py` 的第二个完整签名运行核对
    \((3,3,3,3,2,2,1,1,1)\) 的 410 个入口、14,760 个原始标架和
    8,685 个换基代表；217 个完整候选全部在单点逃逸门排空，零六尾
    与零 25 位置骨架。报告文件 SHA-256 为 `c21687a2...5bf4`，全新
    独审裁决 CORRECT。
74. `unique_tail_cover_unified_projection_labels.py` 重建两个素数各 372
    个固定 incidence；每域 210 个有行空间强迫零障碍，162 个以
    (N<p^2) 并集界及显式逐位置标签通过。独审全量复核 324 套标签、
    99,360 个 (Q_E) 真内部子集与 5,940 个非覆盖交。规范证书为
    `52a6c801...21e0`，独审裁决 CORRECT。
75. `unique_tail_cover_local_quotient_closure.py` 对每素数 372 个固定
    覆盖骨架枚举全部非空 (L) 子集及可用 (X) 核；372/372 都含
    \(X_{p-b-1}\dot\cup(L\setminus U)\) 的统一尾外禁块。规范证书为
    `01eb4736...ec6e`，覆盖子支独审裁决 CORRECT。
76. `unique_tail_forced_kernel_nonempty.py` 对两个参数及全部 94 个
    “素数—\(|L|\)”行核对空核禁块：核心数 228/1,393，长度范围
    231--277/1,396--1,442，全部落入连续禁窗。规范证书为
    `2ae9da6a...c2ff`，全新独审裁决 CORRECT。
77. `unique_tail_forced_short_packing_block.py` 独立枚举两个真实互补
    商零块、双侧禁窗、十个强制型尺寸向量与共同核界；复得
    \(N\le7-b\)、(p=1399) 的 \((1,1,1)\) 空集及十个幸存尺寸。
    规范证书为 `bc44e496...d39f`，全新独审裁决 CORRECT。
78. `unique_tail_forced_atom_subset_blocks.py` 对十个尺寸中的全部 24 个
    非空原子子族块联立同一轴偏差；10 个尺寸降为 6 个、9 个偏差
    赋值，再由系数一单点长补纤维门只留 (3) 的 5 个尺寸、8 个偏差。
    规范证书为 `c582ddc8...a7fe`，全新独审裁决 CORRECT。
79. `unique_tail_all_packing_short_blocks.py` 对十四个素数—packing 行
    统一核对真实互补块、17 个初始尺寸、全部 24 个非空子族块和
    长补 (q)-纤维门；尺寸计数为 17→12→10（最后含两个空型），
    两素数均只余 \(\varnothing,(2),(3)\)。规范证书为
    `b08b3afd...2463`，全新独审裁决 CORRECT。
80. `p7_support9_collinear_real_remaining.py --signature 6` 完整核对
    \((4,4,2,2,2,2,1,1,1)\) 的 410 个入口、14,760 个原始标架、
    8,685 个换基代表和 80,482 个空逃逸完整候选。两次空检查点全跑
    均逐字节复得报告 SHA-256 `49f60367...dd16`，全新独审裁决
    CORRECT。
81. `unique_tail_remaining_six_f2_complements.py` 重放十二个剩余非空
    偏差，恰识别三条六项 \(2a\) 块，并逐行验证其字面补集必须为
    长度 \(3p-2\) 的商原子。规范证书为
    `7a26b7e0...34f4ec`，全新独审裁决 CORRECT。
82. `unique_tail_remaining_long_complement_internal_sums.py` 对八个非空
    尺寸行枚举每个 \(Q_H\) 真投影零子集和全部混合
    \(P\)--\(Q_H\) 目标；复得型 (3) 原子、型 (2) 系数一原子补
    反链及 \(0/1/3\) 个混合代表。规范证书为
    `fe15a00d...09eb9e`，全新独审裁决 CORRECT。
83. `unique_tail_remaining_six_f2_extreme_fringe.py` 核对三个长度
    \(3p-2\) 补原子的删点 \(J\) 恒等式、五组截断阈值及
    \(62(697+697+4195)=346,518\) 条 \((z,T)\) 带符号公式。
    规范证书为 `b48d1106...34a9a`，全新独审裁决 CORRECT。
84. `unique_tail_type3_near_davenport_group_algebra.py` 重建型 (3) 的
    九个端点行、亏损计数 \(5/3/1\)、增广边缘维数 \(1/3/6\)
    及亏损零/一的 \(J,2J\) 恒等式。规范证书为
    `9c908893...4037`，全新独审裁决 CORRECT。
85. `p7_support9_collinear_real_remaining.py --signature 3` 完整核对
    \((4,3,2,2,2,2,2,1,1)\) 的 543 个入口、19,548 个原始标架、
    10,638 个换基代表与 56,587 个空逃逸完整候选。报告 SHA-256
    为 `f0a92bf8...684a`，全新独审裁决 CORRECT。
86. `p7_support9_collinear_real_remaining.py --signature 5` 完整核对
    \((4,3,3,3,2,1,1,1,1)\) 的 785 个入口、28,260 个原始标架
    与 17,160 个换基代表；41,757 个第四层前缀恰由
    33,466+8,291 个强制点拒绝清空。作者两次和独审一次从空全跑
    语义一致，冻结报告 SHA-256 为 `e5e9b652...4863b`，全新独审
    裁决 CORRECT。
87. `unique_tail_type3_shared_endpoint_fringe.py` 把九个型 (3) 端点行
    联立为 14 个条件长度对、86 个实际交/花瓣尺寸行与六种共同因子
    边缘关系；亏损对计数为 \(5/3/1/3/1/1\)。规范证书为
    `d6ccad1a...560a`，全新独审裁决 CORRECT。
88. `unique_tail_tail_anchoring.py` 无导入重建六个避尾轴向长度界、
    十个共同核界、型 (2) 的 18 个端点状态与 11 个幸存状态、空型
    八个分解行与十二个端点行、21 个迹对和八个混合目标门。规范
    证书为 `d66287f2...ed13`，全新独审裁决 CORRECT；审计 SHA-256
    为 `cc79e537...8b31e`。

实际输出：

```text
PASS: four-layer inverse for p<=500 and d=0..4; double-line six-coefficient bound and anchor-sumset deduplication; U_p formulas; route-B type tables
PASS: seven-point line values for 92 primes, 7<=p<=500
PASS: two-point deletion identities and all three absence cases for primes 7<=p<=500
PASS: three-point deletion identity and integer count lifts for primes 7<=p<=500
PASS: two-term transversal residues, value-pair graph bound, affine-rank coefficients, and cubic height blind spot for primes 7<=p<=500
PASS: the first six Hasse/deletion constraints are consistent of rank 9; they do not by themselves prove A_p
PASS: (3p+4)-atom Hasse system has rank 11 and forces N_6(2a)=1/5
PASS: length-refined one-point system has rank 20 of 24 for all primes 7<=p<=500; four local variables remain
PASS: all three quotient exchange models and their atom equations for 92 primes, 7<=p<=500
PASS: deterministically reconstructed the weak p=7 weighted model and its expected rejection by triple cover and quotient-label rank
PASS: triple-complete p=7 weighted model with incidence nullity 3, with expected rejection by long-atom support and nonzero F3 intersections
PASS: t=3/4 interpolation, fixed-E length coordinates, B' atomicity, and common-E local models
PASS: both fixed p=7 standard-atom templates are inconsistent; the strong-template 13-term certificate has left side 0 and right side 1
PASS: p>=11 strong-template pair bound checked for all primes through 500
PASS p=11: rejected all 184030 symmetric multiplicity vectors after normalizing beta=0
PASS p=13: rejected all 2702973 symmetric multiplicity vectors after normalizing beta=0
PASS: standard coordinate-pair finite regression
PASS: exact (t,k) exception table and 668880 normalized axial-support cases
PASS: general triple-candidate filter and the +/-3 height collapse
PASS: short-exchange degree models for 92 primes, 7<=p<=500
PASS: full-fiber exclusion checks; parameter cases=1365, two-value cases=83892, three-value cases=7809477, collision primes=91
PASS: exact p-2 height profiles, triple-codegree systems, and the three p=11,19 intermediate survivors
PASS: p-2 exceptional-family supports contradict the point/pair identities
PASS: exact p-2 survivor arithmetic and anchor resource bounds
PASS: p-3 height profiles and exceptional-point family exclusions at p=11,13
PASS: 51 p-4 residual variables, 28 triple-cover types, singleton-tail thresholds, and a five-point-tail scalar solution
PASS p-4 single-height probe: singleton bounds=1968, pure-T F3 cases=820, moment representatives=1148
PASS: exact negative-binomial identities, p-4 residual-star scalar solution, and feasible-core overlap intervals
PASS: p=13 p-4 height reduction and exceptional-point missing-family checks; p=11 full-core endpoint retained
PASS: p-4 mixed-Hasse tail moments and all three 21-equation T/Q weighted certificates
PASS: p=7 five- and six-fold quotient fibres excluded; 41 lower-multiplicity relaxed height orbits retained
PASS: p=11 every multiplicity-seven quotient fibre is monochromatic; the unique relaxed negative-exception orbit is anchor-excluded
PASS: p-4 two-tail and mandatory cross-family exchange formulas, with their local stopping states
PASS: p-4 unique F3-tail arithmetic, eleven exceptional primes, and K>=ceil((p-1)/2520)
PASS: p=7 four-fibre affine projections and expected rejection of the old exceptional labelled-tail candidate
EXPECTED REJECTION: the old p=7 four-fibre labels induce 97 F3 blocks and a nested pair with zero intersection quotient sum
PASS: all 16 exceptional unique-F3-tail types are compatible with the 21 aggregate Hasse equations
PASS: p=7 three-fibre affine projections, singleton-zero formal slices, and raw capacities
EXPECTED REJECTION: the old p=7 three-fibre three-tail labels induce two F3 blocks with zero intersection quotient sum
PASS: unique-tail actual-position arithmetic; excluded types=3, surviving types=13
PASS: p-4 multi-tail height<=3, 16 diamond types, comparable-pair cap 112, aggregate minor -512000
EXPECTED REJECTION: second p=7 four-fibre assignment has 31 illegal short spectra and 93 assigned-B quotient zero sums
PASS: exact p=7,m=3 fixed-B atom reduction, 000,s=6 normalization, and strict 25-position verifier
EXPECTED REJECTION: p=7,m=3 lifted actual atom has a b=0 two-point quotient zero sum of height 5
PASS: p=7 heavy quotient-fibre context exclusion; the fixed 22-position quotient assignment has no height lift
PASS: p=7,m=3 fixed length-19 B skeleton has no six-position T quotient lift
PASS: unique-tail trace-excess arithmetic; 11 of 13 survivor bounds strictly improved
PASS: p=7,m=4 fixed-B reduction, quotient propagation, zero-core residue, 68-scalar normalization, and exact length-9--12 quotient-zero oracle
PASS: middle quotient-zero gap for 92 primes 7<=p<=500; disjoint-short support <=p+1
PASS: repaired p=7,m=3 exact length-9--12 quotient-zero oracle
PASS: p=7,m=4 fixed length-19 B has complete nonzero middle spectrum
PASS: three other fixed p=7,m=3 length-19 atom spectra and escape sets
PASS: unique-tail complete axial complement-atom criterion and thirteen trace tables
PASS: old p=7,m=3 and m=4 fixed B atoms are one unpointed GL(3,7) orbit
PASS: old-m=3 one-step pair-mutation frontier has 6840 candidates, eight atoms, and three new low-fibre fixed-skeleton exclusions
PASS: p=13 unique-tail labelled reduction; quotient/actual cover bounds 42/534 and decomposable five-tail coefficients 0,1,2,3,4,5,12
PASS: p=7 tail-conditioned middle spectrum; singleton, pair, and triple tail rows are exact
PASS: seven-source second pair-mutation frontier has 39276 candidates, ten atoms, and three new empty-escape orbits
PASS: p=7,m=3 support<=6 canonical classification; support five empty and support six has two empty-escape orbits
PASS: p=7,m=3 support-seven extension frontier; four singleton-escape orbits and no zero-sum six-tail
PASS: p=7,m=4 fixed-representative radius-two frontier; 20 pointed branches and no escape labels
PASS: p=13 unique-tail internal spectrum refinements 534->511 and 91->9
PASS: p=13 unique-tail exterior coupling frontiers 118/83 and strict shard counts 60298/747
PASS: p=7 maximal-atom group-algebra escape identities and fibre gap ladders on seven frozen atoms
PASS: unique-tail labelled position congestion; 503 multi-trace blocks, 10938 edges, and two four-edge witnesses
PASS: p=7,m=3 support-seven four-source per-source mutation union; zero support-at-least-eight atoms after the verified zero-label gate
PASS: p=7,m=3 support-eight complete 462-profile frontier; 1846 complete candidates and zero six-tail survivors
PASS: p=7,m=4 no-three short/support-eight frontiers and the exact-three dependency splice; support at most eight closed at the quotient layer
PASS: p=7 support-nine structural pruning; plane maximum 11, PG(2,7) arc maximum 8, and exact prefix tail gates
PASS: p=7 support-nine light signatures (3,2^8) and (4,2^7,1) closed; eleven signatures remain
PASS: unique-tail four-edge joint interface; 11 graph shapes, 28584 trace assignments, and one shared exterior spectrum
PASS: unique-tail common-R decomposition; seven packing types, fourteen endpoint remainder rows, and no forced fourth block
PASS: unique-tail forced short packing; ten size vectors, N<=7-b, and p=1399 type (1,1,1) closed
PASS: unique-tail forced atom subfamilies; 24 induced blocks and only forced type (3) remains
PASS: unique-tail all-packing short blocks; 17->12->10 size vectors and only empty,(2),(3) remain
PASS: p=7 support-nine remaining signature step 3; 410 profiles, 80482 empty-escape complete candidates, and zero exact six-tail survivors
PASS: unique-tail three automatic six-term F2 blocks force length-(3p-2) quotient-atom complements
PASS: unique-tail all remaining nonempty long-complement internal subset sums; type-(2) atom antichains and type-(3) endpoint atoms
PASS: unique-tail three extreme complements; 346518 signed deleted-position fringe identities
PASS: unique-tail type-(3) near-Davenport group-algebra edge; nine rows, delta counts 5/3/1, and fringe dimensions 1/3/6
PASS: p=7 support-nine remaining signature step 4; 543 profiles, 56587 empty-escape complete candidates, and zero exact six-tail survivors
PASS: p=7 support-nine remaining signature step 5; 785 profiles, 41757 forced-endpoint rejections, and zero complete candidates
PASS: unique-tail type-(3) shared endpoint-pair fringes; 14 conditional length pairs and 86 literal petal rows
PASS: unique-tail tail anchoring; type-(2) endpoint states 18->11 with all axial intersections removed, and empty-packing decomposition/trace compression
PASS: p=233 type-(3) singleton-tail fringe; rank-one length patterns reduce to 888 and 788, while the all-length-seven slice has the unique ordered rank-two normalization (e,f,-e-f)
PASS: p=233 fixed shared-factor quotient skeleton; 53361 automatic length-eight blocks compress to a 461-row rank-461 height cut and force multiplicity 231>229
PASS: p=233 type-(3), |P|=2 exact-slice interface; 11 oracle contracts, 17976380 Hasse rows, 48 atom regressions, and 5 adversarial short-intersection classifier rows
PASS: p=233 type-(3), |P|=2 all-distinct outer trace partition; 28584 valid assignments split as 28548 repeated plus 36 exact shards with shape counts 6/6/12/12
PASS: p=233 rank-two three-functional compatibility; the unique 1*1^T-3I evaluation matrix, one 469-position literal model, six exact deleted-tail J products, and three shared 458-position factors
PASS: general connected-bipartite automatic-short-block height cut; tree rank |A|+|B|-1, p=233 threshold 230, static 37/435/30/6 geometry, and a q-lift boundary atom with exact-fibre maximum 2
PASS: p=233 rank-two two-monochromatic common-kernel threshold; 27144 capacity-scalar checks, exact 115/116 proof-gap rows, and the 52664/1130/30 fixed 227-by-226 partition
PASS: Property-B three-tail support domains; four lines per tail pair, empty triple intersection for every characteristic outside 2,3,5, and the p=233 common-position exclusion
PASS: p=233 Property-B two-max mixed-length exclusion; 54756 heavy-domain pairs reduce to four explicit proper-zero-sum witnesses
PASS: p=233 length-decorated trace reduction; 1440 outer decorations split into 720 eliminated and 720 retained, with singleton-seven distribution 180/540
PASS RELAXED: three unified-position C_233^2 doubleton models; exact K/L/Q_H incidence and maximal-atom checks, with q-lift, automatic short closure, P-mixed targets, Hasse and actual Z explicitly omitted
PASS RELAXED: fixed Model-D endpoint-internal q-lift; 384 endpoint subsets, actual multiplicity cap 229, three F3(7), one F1(5), and one row requiring 232 unavailable X positions
PASS WITH SPLIT QUANTIFIERS: fixed Model N all-lifts unique-tail exclusion; one displayed Model-C lift passes endpoint-internal and four mixed-target fibres but has an explicit global length-three short-spectrum violation
PASS ORACLE / ZERO CURRENT DELETIONS: duplicate-remainder unique-tail separator; 1776 candidate slots in 678 of 720 rows, with 720 motif-free private-petal masks proving 0/720 deleted at the outer layer
PASS FIXED-RELABEL REJECTION: displayed Model-D lift; 162225 capacity vectors, 252=75+177 short profiles, 53 disjoint-profile conflicts, and six mixed-target witnesses; all other relabels remain open
```

此报告只认证有限算术与显式公式，不把有限检查提升为一般 \(A_p\) 证明，也不独立认证低次系数函数对偶这一手证接口。
其中第 2 项只复核公共外部双和障碍之双侧推论的旧自足证明；该表述
已路线去重，不另计一份数学进展。
