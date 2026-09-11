# 引理依赖账

外部定理条件核验：本轮没有新增外部文献定理；所有承重接口只从仓库
冻结证明或公共独立审计继承，并在各条目中写明适用范围。去重审计已
确认原记 LEMMA-DLT 是 `A_exterior_double_sum_obstruction` 的
直接推论，现已合并，不再把等价重述记作独立进展。LEMMA-INVERSE-U
仍明确登记为 `STRICTLY_WEAKER` 且 OPEN。

`EQUIVALENT_BLOCKER`：无。上述合并是路线去重，不是把未解等价命题
伪装成引理。

## LEMMA-SQ：短商零和三系数限制

- 精确陈述：`assumptions.md` 的 (SQ)。
- 状态：KNOWN。
- 相对原命题：STRICTLY_WEAKER。
- 来源：`research/2026-09-05_zhao_Ap_general/round3/research_note.md` 第 4 节。
- 条件核验：仅用于 \(R\) 中非空、长度至多 \(2p+2\) 的商零和位置子序列。

## LEMMA-TOP：四点过删除顶积

- 精确陈述：`assumptions.md` 的 (TOP)/(CONST)。
- 状态：KNOWN。
- 相对原命题：STRICTLY_WEAKER。
- 来源：`research/2026-09-05_zhao_Ap_general/round6/research_note.md`。
- 风险：不含统一长度控制。

## LEMMA-EXT-DLT：外部双和障碍及双侧补集推论

- 精确陈述：`route_a_double_line_trap.md` 的定理。
- 状态：KNOWN/PROVED；ROUTE_DEDUPLICATED。
- 相对原命题：STRICTLY_WEAKER。
- 依赖：公共 `A_exterior_double_sum_obstruction`；本地自足证明另由 LEMMA-SQ、LEMMA-TOP 给出。
- 使用路线：路线 A 的共同前件，不再单列为一条竞争路线。
- 反例/缺口：若四点商像的非空子集和二重和集未命中 \(-\pi(\sigma(U))\)，本引理不触发。
- 去重拼接：若总和为 \(\kappa a\)，取
  \(0\le r,r'\le p-4\)、\(r+r'=-\kappa\)，以
  \(C a^r,C'a^{r'}\) 触发公共障碍。
- 边界：\(p\ge11\) 时可要求 \(r,r'\ge1\)，所以与允许空侧的商群
  版本等价；\(p=7\) 只保留非空侧版本，严格更弱。

## LEMMA-R-NONLINE：总和不在锚点线

- 精确陈述：在 \(h=p-4,x_0=0\) 假想反例中，\(\sigma(R)\notin\langle a\rangle\)。
- 状态：PROVED_HERE。
- 相对原命题：STRICTLY_WEAKER；严格关闭 \(\sigma(R)\in\langle a\rangle\) 整个子分支。
- 依赖：LEMMA-EXT-DLT。
- 风险：不得误写为 \(\sigma(R)=0\) 或由 \(\Lambda_i\) 推出。

## LEMMA-HASSE4：前四长度阴影只恢复正规形

- 精确陈述：`route_a_length_residue_audit.md` 第 1 节。
- 状态：PROVED_HERE。
- 相对原命题：STRICTLY_WEAKER；它是方法边界，不是排除定理。
- 依赖：零和窗口、LEMMA-TOP、增广理想与低次系数函数对偶。
- 结论：纯 \(q\le3\) 次数路线 RETIRED。

## LEMMA-POINTSHORT：顶积与基分块推出点态短表示

- 精确陈述：每个目标都有长度至多 \(3p-2\) 的子集表示。
- 状态：DISPROVED。
- 相对原命题：原拟议版本虽更弱，但为假。
- 反例：`route_a_length_residue_audit.md` 的 \(U_p\)，\(p\ge29\)。
- 边界：该族自身有长度 \(p-3\) 零和，故不反驳冻结原题。

## LEMMA-INVERSE-U：顶积、低高度、长零和禁区不相容

- 精确陈述：不存在长度 \(4p-4\)、高度至多 \(p-4\)、顶积非零且无长度至多 \(3p\) 非空零和的 \(U\subset C_p^4\)。
- 状态：OPEN。
- 相对原命题：STRICTLY_WEAKER。
- 使用路线：A2 的逆结构修订版。
- 已排除捷径：不能删去长零和禁区；不能只用模 \(p\) 长度余数。

## LEMMA-REFLECT-TYPE：固定和值配对图的类型倒置

- 精确陈述：非半值反射对的类型满足 \((m,d)\leftrightarrow(d,m)\)；半值类满足 \(d=m-1\)。
- 状态：PROVED_HERE（直接来自完整固定和值图定义）。
- 相对原命题：STRICTLY_WEAKER。
- 使用路线：路线 B 的同值双叶排除。
- 风险：普通类只固定 \(d=1/4\)，不是先验固定重数；特殊类与普通类配对时必须额外有特殊类重数 \(m=1/4\)。

## LEMMA-K12-SAME：同值双叶排除

- 精确陈述：冻结的 \(x_0>0\) 四元块末支中，对每个 \(p\ge149\)，横截图的 \(K_{1,2}\) 分量不能有两个同值叶。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 相对原命题：STRICTLY_WEAKER；严格关闭一个完整子支。
- 依赖：Round 5 的星形归约、LEMMA-REFLECT-TYPE、`route_b_star_reduction.md` 的覆盖数二分类。
- 外部定理条件核验：无新增外部定理；固定和值图分量分类在证明中展开。

## LEMMA-K13-ACTIVE：互异三叶活跃类归约

- 精确陈述：\(p\ge149\) 的互异三叶 \(K_{1,3}\) 中，至多两个 \(M_i\) 非零；一活跃与二活跃的精确重数见 `route_b_star_reduction.md` 第 5 节。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 相对原命题：STRICTLY_WEAKER。
- 最小缺口：尚未排除一活跃和二活跃反射系统。

## LEMMA-ATOM-LINE：长原子的七点线刚性

- 精确陈述：`route_a_atom_line_rigidity.md` 第 3--6 节。
- 状态：PROVED_HERE；独立文本审稿调用超时，尚无外部 CORRECT 票。
- 相对原命题：STRICTLY_WEAKER，但直接作用于每个实际 \(3p+3\) 与 \(3p+4\) 零和原子，不依赖承重四点删除集。
- 结论：每个 \(3p+3\) 原子满足
  \[
  \bigl(c_Z(a),c_Z(2a),c_Z(3a)\bigr)=(-3/2,3/5,-1/10),
  \]
  并含一个 5--7 项、实际和为 \(3a\) 的子序列；其补集是长度 \(3p-4\) 至 \(3p-2\) 的 \(C_p^3\) 原子。\(3p+4\) 层的一次 Hasse 阴影给出对应 6--8 项表示与同一补原子范围。
- 依赖：五层正规形、短零和下界、锚点可用数、群环次数界、\(D(C_p^3)=3p-2\)。
- 进一步结论：每个 \(3p+4\) 原子都满足
  \(N_6^Z(2a)\equiv1/5\pmod p\)。相应六项块的补集要么是长度
  \(3p-2\) 的秩三原子，要么恰分解为一个二项、实际和为 \(a\)
  的块与一个长度 \(3p-4\) 的秩三原子。
- 逐点加强：在每个 \(3p+4\) 原子中，实际和分别为 \(a,2a,3a\)
  的短块族在每个位置的带符号度恒为
  \(-3/4,3/10,-1/20\)。三族都覆盖全部位置且都无公共点；
  \(2a,3a\) 两族各自相交，\(a\) 与 \(3a\)、\(2a\) 与 \(3a\)
  交叉相交；不同 \(3a\) 块的交集不可能在商群中为零。
- 二点加强：任意位置对的三种带符号共度满足
  \(8d_1+10d_2=3\)、\(2d_1-10d_3=1\)。特别地，不共同落入
  \(3a\) 块的位置对必同时共同落入某个 \(a\) 块和某个 \(2a\) 块。
- 三点加强：任意三位置集 \(W\) 满足
  \(4\delta_1(W)+10\delta_2(W)+20\delta_3(W)=-1\)，并被至少
  \(\lceil(p-1)/20\rceil\) 个实际短块覆盖；相应的一点、二点同余
  也提升为 `proofs/triple_cover.md` 中的真实计数下界。
- 六项块耦合：每个六项 \(2a\) 块与某个 \(3a\) 块至少交两点；
  该交集要么商和非零，要么前者整个包含在一个八项 \(3a\) 块中，
  差集恰为二项 \(a\) 块。若六项块的补集本身是 \(3p-2\) 原子，
  只能发生商和非零的第一种情形。
- 最小缺口：排除上述无核心交叉相交设计与长度
  \(3p-4,3p-3,3p-2\) 的秩三补原子同时存在。

## LEMMA-EXTREME-FRINGE：极值补原子的双边短表示

- 精确陈述：`proofs/extreme_atom_fringe.md`。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 量词：每个素数 \(p\ge7\)，每个走 (20) 第一支的
  \(3p+4\) 原子、每个六项 \(2a\) 块 \(C\)、每个 \(b\in B\)
  及每个非空真 \(T\subset C\)。
- 结论：
  \[
  L_{\le8-|T|}^{B\setminus b}(-\bar\sigma(T))+
  L_{\le|T|+1}^{B\setminus b}(\bar\sigma(T)-\bar b)=1.
  \]
  因此每个 \((b,c)\) 同时满足“七项/二项”和“三项/六项”两个
  真实短表示二分。
- 依赖：LEMMA-ATOM-LINE、LEMMA-SQ、\(C_p^3\) 群环增广理想顶层
  一维，以及 \(\bar B\) 为长度 \(3p-2\) 原子。
- 相对原命题：STRICTLY_WEAKER，但首次把极值补原子的无界目标表示
  压到常数长度。
- 最小缺口：用高度 \(p-4\) 或固定和交叠把这些逐对短表示拼成
  实际短零和。

## LEMMA-NEAR-ATOM-EXCHANGE：近原子删除交换

- 精确陈述：`proofs/near_atom_exchange.md`。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 量词：\(p\ge7\)，(28) 第一支中的每对六项 \(2a\) 块 \(C\)
  与 6--8 项 \(3a\) 块 \(A\)。
- 结论：若 \(J_0\subseteq A\setminus C\) 与
  \(K_0\subseteq C\setminus A\) 商和相同，则交换块的实际和为
  \(\lambda a\)、长度至多 \(5+\lambda\)，其中
  \(\lambda\in\{1,2,3\}\)。
- 相对原命题：STRICTLY_WEAKER。
- 最小缺口：交换关系 \(J(-K)\) 可能自身是二至十项原子。

## LEMMA-TRIPLE-COVER：三点删除的定量短块覆盖

- 精确陈述：`proofs/triple_cover.md`。
- 状态：PROVED_HERE；独立验缝在修正 \((t,q)=(0,0)\) 的非承重
  端点量词后 CORRECT。
- 量词：每个素数 \(p\ge7\)、每个长度 \(3p+4\) 的实际零和原子
  \(Z\)、每个三位置集 \(W\subset Z\)。
- 结论：
  \[
  4\delta_1(W)+10\delta_2(W)+20\delta_3(W)=-1,
  \qquad
  D_1(W)+D_2(W)+D_3(W)\ge\left\lceil\frac{p-1}{20}\right\rceil.
  \]
  在极值补原子支中，所有这些覆盖块都跨越 \(B\mid C\)，故不同
  跨界短块至少有
  \(\left\lceil\binom{3p-2}{3}\lceil(p-1)/20\rceil/35\right\rceil\)
  个。
- 依赖：LEMMA-ATOM-LINE 的七点支撑、删除--Hasse 次数界及原子在
  零点的唯一表示。
- 相对原命题：STRICTLY_WEAKER；它提供常长度表示的全局数量质量，
  尚未把这些块拼成实际短零和。
- 方法边界：四点删除余因子为三次，单靠七点支撑不再有新关系。

## LEMMA-SHORT-TRANSVERSAL：常数横截与全局四次块数

- 精确陈述：`proofs/short_block_transversal.md`。
- 状态：PROVED_HERE；普通组合停止线由独立实例给出。
- 结论：任一 \(3a\) 块横截三族全部短块；结合三点覆盖，任意
  \(3p+4\) 原子的不同短块总数至少为
  \[
  \left\lceil\binom{3p-4}{3}\lceil(p-1)/20\rceil/35\right\rceil.
  \]
  对 \(p\ge11\)，\(\nu(\mathcal F_1)\le3\)；对 \(p=7\)，
  \(\nu(\mathcal F_1)\le5\)。
- 相对原命题：STRICTLY_WEAKER。
- 停止线：固定三点核心的显式抽象族同时具有常数横截和更强的普通
  三点覆盖，故普通覆盖/匹配信息仍不足，必须保留符号与群值。

## LEMMA-TWO-TERM-TRANSVERSAL：二项块的精确两点结构

- 精确陈述：`proofs/two_term_transversal.md`。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 量词：每个 \(3p+4\) 原子中的任意二项 \(a\) 块
  \(E=\{x,y\}\)；特别适用于 (20) 第二支。
- 结论：\(E\) 横截 \(\mathcal F_3\)，三种交类带符号总数为
  \((1/20,1/20,-1/10)\)，且
  \((d_1,d_2,d_3)=(1,-1/2,1/10)\)。至少
  \(\lceil(p-1)/2\rceil\) 个 \(2a\) 块包含 \(E\)，并分解出同样
  多个与 \(E\) 不交的 \(a\) 块；加上/删去 \(E\) 还在“不交的
  \(\mathcal F_1\) 与包含的 \(\mathcal F_2\)”以及“不交的
  \(\mathcal F_2\) 与包含的 \(\mathcal F_3\)”之间给出双射。
  全部二项 \(a\) 块图满足
  \(\nu\le3\)、边数至多 \(3(p-4)\)。
- 相对原命题：STRICTLY_WEAKER；它显著收紧第二支但尚无矛盾。

## LEMMA-F3-EXCHANGE-NETWORK：多补原子交换网络

- 精确陈述：`proofs/f3_exchange_network.md`。
- 状态：PROVED_HERE；独立验缝在修正“不同关系”量词后 CORRECT。
- 结论：
  \[
  |\mathcal F_3|\ge
  M_p=\left\lceil\frac{(3p+4)\lceil(p-1)/20\rceil}{8}\right\rceil.
  \]
  因而同时有 \(\Omega(p^2)\) 个近 Davenport 补原子。每对不同
  \(F_3\) 块给一个二至十四项等商和差关系；若它有真零和子关系，
  相应交换必产生新的长度至多八的短块。
- 规模：至少 \(\binom{M_p}{2}=\Omega(p^4)\) 个块对索引的关系
  实例；不声称所得有符号序列彼此不同。
- 相对原命题：STRICTLY_WEAKER；把剩余对象从单原子分类升级为真实
  多原子网络。

## LEMMA-SPECIAL-F1-DELETION：已有小 \(a\) 块的特殊删除线

- 精确陈述：`proofs/special_f1_deletion.md`。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 结论：每个三项 \(a\) 块至少包含于
  \(\lceil(p-3)/2\rceil\) 个 \(2a\) 块和
  \(\lceil(p-1)/2\rceil\) 个 \(3a\) 块；每个四项 \(a\) 块
  满足 \(3d_2+5d_3=-1\)。
- 新机制：删除的集合本身是 \(a\) 块，除原子端点外还可用它横截
  \(\mathcal F_3\) 得到余因子的第三个零点。
- 方法边界：五项以上的 \(a\) 块有两个自由插值参数；固定二项
  \(a\) 块的零至二阶分长度系统也有两个自由参数，不能仅由这些
  方程强迫六项 \(2a\) 扩张。

## LEMMA-SECOND-BRANCH-DIAMOND：二项横截的第二支菱形

- 精确陈述：`route_a_second_branch_models.md` 第 1--2 节。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 结论：若六项 \(2a\) 块 \(C_i=E\dot\cup D_i\) 共用二项
  \(a\) 块 \(E\)，则不同四项花瓣相交且商交和非零。走第二支时
  伴随二项块 \(P_i\) 产生两个六项 \(2a\) 块和一个八项
  \(3a\) 块组成的菱形；伴随边在 \(Z\setminus E\) 上匹配数至多
  二、边数至多 \(2(p-4)\)。不同菱形的商交结论只在
  \(A_i\ne A_j\) 时使用。
- 停止线：同文件第 3 节对每个 \(p\ge7\) 构造线性多个菱形的
  实际群值局部相容模型；它不实现完整原子/Hasse 设计，因而只证伪
  “局部菱形必产生真子交换”的加强。

## LEMMA-STANDARD-ATOM-FIXED-TEMPLATES：标准极值原子的固定模板排除

- 精确陈述：`route_a_standard_atom_templates.md`。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 结论：对标准
  \(B=e_1^{p-1}e_2^{p-1}e_3^{p-1}g\)，固定六点模板
  \(C=(e_1,e_2,e_3,g,g,-3g)\) 对每个素数 \(p\ge7\) 都不可能：
  \(p\ge11\) 由同一 \(B_{e_i}\) 值类内一个位置对的二点方程
  直接矛盾，\(p=7\) 由完整轨道矩阵及十三项证书排除。另在
  \(p=7\) 排除 \(C=(\pm e_1,\pm e_2,\pm e_3)\)。
- 相对原命题：STRICTLY_WEAKER；这是固定 \(B,C\) 的真无限子模板，
  不分类任意六点 \(C\) 或任意极值原子。

## LEMMA-SMALL-A-DICHOTOMY：二/三项块与纯四项—八项分岔

- 精确陈述：proofs/small_a_block_dichotomy.md。
- 状态：PROVED_HERE；独立验缝在补入 \(p=7\) 所需的全局
  \(N_{3,8}\) 消参式后 CORRECT。
- 结论：若没有三项 \(a\) 块，则
  \(N_{1,4}\ge(p-5)/2\)，且四项块到六项 \(2a\) 块、八项
  \(3a\) 块的包含关联为 \(\Omega(p^2)\)。若再没有二项 \(a\)
  块，则八项 \(3a\) 层单独为 \(\Omega(p^2)\)，而至少
  \(\lceil(p+1)/5\rceil\) 个六项 \(2a\) 块全部走长度
  \(3p-2\) 极值补原子第一支。
- \(p=7\) 边界：纯四项支强制 \(N_{3,8}\ge7\)。
- 方法边界：一点至三点标量系统有显式有限域相容点，可同时令
  二项、三项层及六项第二支为零；位置交叠与商标签不可省略。

## LEMMA-F3-NONDEGENERATE-PAIRS：交换网络的非单点替换主体

- 精确陈述：proofs/f3_nondegenerate_pairs.md。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 结论：二位置相同实际值替换的 \(F_3\) 块对至多
  \(4(p-5)|\mathcal F_3|\)。因此它们只占全部块对的
  \(O(p^{-1})\)；对 \(p\ge431\) 已强制 \(\Omega(p^4)\) 个
  非退化块对。Johnson 图团分类另给 \(p\ge23\) 至少一个非退化
  块对。
- 相对原命题：STRICTLY_WEAKER；非退化交换关系长度三至十四，仍
  可能整体是有符号原子。

## LEMMA-STANDARD-PM2：标准 \(\pm2e_i\) 模板排除与二点高度系统

- 精确陈述：route_a_standard_atom_pair_system.md。
- 状态：DISPROVED_TEMPLATE；三点排除独立复核 CORRECT。
- 结论：固定标准 \(B\) 与
  \(C=(\pm2e_1,\pm2e_2,\pm2e_3)\) 对每个 \(p\ge11\) 被三点覆盖
  直接排除；任一候选的指定坐标落在整数区间 \([1,9]\)。二点系统
  另给每方向高度支撑至多 \((p+1)/2\)，并在对称情形穷尽排除
  \(p=11,13\) 及 \(p=17,19,23\) 的支撑至多四子类。
- 边界：主排除仍只针对固定 \(\pm2e_i\) 商模板；随机非对称未命中
  不作证明。更强的全轴向族结论登记在下一条。

## LEMMA-STANDARD-AXIAL-PAIRS：标准原子的全部轴向对模板排除

- 精确陈述：proofs/standard_atom_coordinate_pairs.md。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 结论：对每个素数 \(p\ge7\) 及任意非零、彼此可以不同的
  \(k_1,k_2,k_3\)，标准 \(B\) 与
  \(C=(\pm k_1e_1,\pm k_2e_2,\pm k_3e_3)\) 不可能共存于冻结
  \(3p+4\) 原子。最小绝对幅度至多七时，典范长度 \(k_i+1\) 商零和
  块把所有 \(k_i\)-位置高度和压入一至三个值，与高度 \(p-4\)
  矛盾；幅度至少八时，三点覆盖没有商候选。
- 相对原命题：STRICTLY_WEAKER；仍未分类不支撑在三条基轴上的一般
  六点 \(C\)，也未分类一般极值秩三原子。

## LEMMA-FULL-QUOTIENT-FIBER：近极值补原子的满商纤维排除

- 精确陈述：proofs/standard_atom_full_exclusion.md。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 结论：对 \(p\ge11\)，每个 \(A\in\mathcal F_3\) 的商原子补集
  \(B=Z\setminus A\) 都满足 \(v_q(B)\le p-2\)。证明从重数
  \(p-1\) 的商纤维取三点，用三点覆盖产生跨界短块，再在该纤维内
  任意替换；长度窗把所有三至七项高度子集和压入一至三个值，与
  实际值重数至多 \(p-4\) 矛盾。
- 推论：标准极值商原子含重数 \(p-1\) 的值，故对 \(p\ge11\)
  与任意六点补块都不可能；固定 \(C\) 分类已不再需要。
- 相对原命题：STRICTLY_WEAKER，但同时约束 \(\Omega(p^2)\) 个
  近 Davenport 补原子。当前缺口收紧为商值重数至多 \(p-2\) 的
  近极值逆结构及 \(p=7\) 边界。

## LEMMA-P-MINUS-TWO-FIBER：临界商纤维分类与锚点闭合

- 精确陈述：proofs/p_minus_two_height_fibre.md、
  proofs/p_minus_two_residual_degree_system.md 与
  proofs/p_minus_two_survivor_refinement.md。
- 状态：PROVED_HERE；分类、点/对度闭合与锚点证书的三阶段独立
  验缝均为 CORRECT。
- 结论：若 \(p\ge11\) 且某个 \(F_3\) 补原子的商值重数等于
  \(p-2\)，则覆盖该纤维三点的短块全为六项块，高度多重集只能是
  \(h^{p-4}(h+1)^2\)、\(h^{p-4}(h-1)^2\) 或
  \(h^{p-4}(h-1)(h+1)\)。逐三点带符号方程和
  \(\mathcal F_1\pitchfork\mathcal F_3\) 先只留下 \(p=11\)
  的前两型与 \(p=19\) 的第一型。更直接地，正/负异常点分别缺失
  \(\mathcal F_1/\mathcal F_3\)，违反固定非零点度；异常位置对
  也给独立的逐对共度矛盾。三条显式锚点短零和另行交叉排除有限
  余支。
- 结论：对每个 \(p\ge11\)，每个近极值补原子的逐商值重数至多
  \(p-3\)。
- 边界：不处理 \(p=7\)，也不分类重数 \(p-3\) 或更低的近
  Davenport 原子。
- 相对原命题：STRICTLY_WEAKER。

## LEMMA-P-MINUS-THREE-FIBER：次临界商纤维排除

- 精确陈述：proofs/p_minus_three_height_frontier.md。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 结论：若 \(p\ge11\) 且某个 \(F_3\) 补原子的商值重数等于
  \(p-3\)，同商替换把高度多重集压成一个主高度加一或两个距离
  至多二的异常高度；长度八无型。对任意含异常点的短块再次替换，
  正异常点永不进入 \(\mathcal F_1\)，负异常点永不进入
  \(\mathcal F_3\)，与固定非零点度矛盾。
- 结论提升：对每个 \(p\ge11\)，每个近极值补原子的逐商值重数
  至多 \(p-4\)。
- 边界：\(p=7\) 未覆盖；重数 \(p-4\) 时允许单高度纤维，旧的
  异常点机制真正停止。
- 相对原命题：STRICTLY_WEAKER。

## LEMMA-P-MINUS-FOUR-HEIGHT：等号纤维的单高度归约

- 精确陈述：proofs/p_minus_four_height_reduction.md 与
  proofs/p11_seven_fibre_star_exclusion.md。
- 状态：PROVED_HERE；\(p\ge13\) 与 \(p=11\) 两部分独立验缝均
  为 CORRECT。
- 结论：对 \(p\ge13\)，重数恰为 \(p-4\) 的商纤维若非单高度，
  三点覆盖与同商替换把全纤维高度压成一个主高度加一或两个距离
  至多二的异常高度；每个轮廓又含缺失 \(\mathcal F_1\) 或
  \(\mathcal F_3\) 的异常点。\(p=11\) 的完整 1768 轨道星系统
  仅余单高度和负单异常；后者强制五个同值尾点，并由八项锚点零和
  排除。因此对每个 \(p\ge11\)，等号纤维必为 \(X=x^{p-4}\)。
- 边界：不处理 \(p=7\)；该端点由 LEMMA-P7-HIGH-FIBRE 另行降到
  重数至多四。
- 相对原命题：STRICTLY_WEAKER，但把 \(p\ge11\) 的整个等号层
  归约到下一条有限余部设计。

## LEMMA-P-MINUS-FOUR-MONO-FRONTIER：饱和单高度余部设计

- 精确陈述：proofs/p_minus_four_monochromatic_frontier.md、
  proofs/p_minus_four_single_height_probe.md 与
  proofs/p_minus_four_star_design.md、
  proofs/p_minus_four_mixed_hasse_frontier.md、
  proofs/p_minus_four_two_tail_exchange.md、
  proofs/p_minus_four_cross_family_tails.md、
  proofs/p_minus_four_unique_f3_tail_arithmetic.md、
  proofs/p_minus_four_unique_tail_position_frontier.md 与
  proofs/p_minus_four_multi_tail_global.md。
- 状态：必要条件 PROVED_HERE；二余部、跨族交换与唯一尾算术稿的
  独立验缝均为 CORRECT；
  单高度纤维排除 INCOMPLETE。
- 结论：若某个 \(F_3\) 补原子含实际同值纤维
  \(X=x^{p-4}\)，每个与 \(X\) 相交的短块都由必命中 \(T\) 的
  有限余部 \(U\) 生成整个
  \(\binom Xb\) 层。全部余部满足逐 \(X\)-点、对、三元组的精确
  Hasse 矩系统、四种族对的下推相交约束。两个不同三倍余部还对
  两个 \(X\)-核心的每个可实现交数 \(k\) 满足
  \(\bar\sigma(U\cap U')\ne-kq\)，而非只满足零交数特例。
- 混合加强：每个 \(b\ge1\) 余部的 \(T\)-部分非空、真包含于
  \(T\) 且商和非零。逐外点混合 Hasse 排除了最初的六变量证书，
  并迫使每个外点进入某个 \(b\ge2\)、大小至多六的余部；
  \(p\ge19\) 时这些余部全为 \(\mathcal F_3\) 横截。
- 新锚点限制：纯 \(T\) 三倍余部在 \(b\ge4\) 时不存在，
  \(b=3\) 时不能有两个不交者；三倍单点余部全零，二倍和一倍
  单点余部有显式常数上界。
- 二余部加强：两个不同三倍余部的全部核心交换可无损压缩到
  \(-b+k_0\le d\le b'-k_0\)，每个等商差集交换都强制一个满足
  正确长度窗、\(T\)-部分条件与新交集禁值的第三尾。若两尾真包含，
  则较大余部的核心数严格更小，且只能相差一、二或三；同核心、
  反向及差至少四的嵌套均不可能。
- 跨族加强：三族非零逐点度必强迫三个两两不同的正核心余部；
  \(p\ge17\) 时必需的一倍、二倍余部分别与必需三倍余部相交。
  两组跨族交换均已完整写出，并保留 \(b^*=0\) 与新块等于 \(T\)
  的边界。
- 三倍尾数量：若 \(K\) 是正核心三倍余部数，则
  \(K\ge\lceil(p-1)/2520\rceil\)。若 \(K=1\)，素数只能属于
  \(\{11,13,19,23,43,101,233,467,701,1399,2521\}\)；其他素数
  至少有两条不同三倍余部，故二尾交换不是条件性接口。唯一尾还
  横截整个 \(F_3\) 族；三个可能的二点尾有精确分区和共度。
- 唯一尾异常探针：十一项异常素数对应的 16 个
  \((p,\ell,b)\) 类型，在全部允许的 \((s,j)\) 下都满足完整
  21 条安全聚合 Hasse 必要式。代入唯一尾后有 90 个自由
  \(N,J\) 变量，系数秩与增广秩恒为 20，故解空间维数为 70。
  独立验缝 CORRECT；这些有限域聚合解不实现非负入射、统一商标号
  或补原子。
- 唯一尾位置级推进：实际零核心 \(F_3\) 块横截唯一尾，并满足逐
  位置精确带符号入射与普通块数下界。若 \(b\ge4\)，任何零核心块
  都不能包含整个唯一尾；当 \(|U|=2\) 时这与总迹入射矛盾。因此
  \((467,7,5),(701,6,4),(2521,8,6)\) 三型排除，16 型余 13 型，
  十一项异常素数余九项。
- 唯一尾迹盈余：令
  \(\nu=\|(4-r(b+4))/(20b)\|_p\)，则
  \(|\mathcal H_0|\ge
  \lceil((2p+8-r)\mu_p+\nu)/7\rceil\)，并与原避尾下界取最大。
  13 型中 11 型严格提高；三个 \(b\ge4\) 幸存型分别至少有
  58、123、322 个多点尾迹块，两个三点尾型还有至少 1628、9310
  对尾迹不交且尾外商交非零的块对。精确陈述见
  `proofs/unique_tail_next_trace_excess.md`；独立验缝 CORRECT。
- 多尾全局推进：实际尾包含偏序链长至多三，宽度至少
  \(\lceil(p-1)/7560\rceil\)，可比异尾对至多 \(112K\)，每条
  实际三链被极端交换补成菱形。任意固定多尾数据在 21 条聚合式中
  只受第三族固定 \(X\)-点度约束；删除该行后的 20 阶小行列式为
  \(-512000\)。这严格证明聚合层停止，不能替代逐外点实际块族。
- 严格停止线：即使删除全部单点余部，纯 \(X\) 低阶矩仍有显式
  非负模剩余类解；进一步加入 \(T\mid Q\) 分区及全部逐外点混合
  Hasse 后仍有加权解。二余部交换虽已完整化，但一个同值双位置
  局部状态仍满足其全部接口；三条共 \(T\)-点的必需跨族尾也可使
  所有真交换在形式接口中退化为端点；该形式模型没有重建全诱导
  短谱，不能登记为局部反例。下一步必须联立逐外点 \(0/1\) 入射、
  全诱导短块、统一商标号与补原子内部子和；余下 13 个唯一尾型也
  必须继续使用位置级横截，不能再只叠加聚合矩。
- 边界：对 \(p\ge11\)，前一引理已证明任意 \(p-4\) 等号纤维
  都单高度；\(p=7\) 不处理。
- 相对原命题：STRICTLY_WEAKER。

## LEMMA-P7-HIGH-FIBRE：高重数排除与三、四重商纤维投影

- 精确陈述：proofs/p7_six_fibre_exclusion.md 与
  proofs/p7_four_fibre_refinement.md、
  proofs/p7_four_fibre_tail_local_state.md、
  proofs/p7_m4_next_frontier.md、
  proofs/p7_three_fibre_refinement.md、
  proofs/p7_three_fibre_labelled_csp.md、
  proofs/p7_heavy_quotient_fibre_context_exclusion.md、
  proofs/p7_m3_next_heavy_fibre_propagation.md。
- 状态：PROVED_HERE / FINITE_LABELLED_REMAINDER；高纤维与三重
  仿射投影验缝通过。四重旧审计对预选尾的检查已被新的全子集闭包
  反例取代；修订稿保留仿射投影并撤回例外标签候选，等待新审计。
- 结论：在 \(p=7\) 的 ROUTE-A4 冻结接口下，对每个
  \(T\in\mathcal F_3\)，补原子 \(B=Z\setminus T\) 的每个商值
  重数至多四。六重纤维的 104 个高度轨道全部被 68 行逐位置
  点/对/三点 Hasse 星系统排除；五重纤维的 59 个轨道在加入每个
  单点余部实际重数至多三后也全部排除。
- 严格停止线：重数三、四共有 41 个高度轨道；同一放宽星系统在
  全部单点余部为零时仍相容。四重的 29 轨道又精确分成：28 型
  强迫全核心三倍余部并满足 \(N_6-N_7+N_8\equiv6\pmod7\)；唯一
  例外 \(0^3 1\) 若无全核心块，则在 \(b=1,2,3\) 各强迫余部。
  第一个旧例外标签候选会诱导两个嵌套 \(F_3\) 块及零商交；第二个
  16 点候选虽通过 44 个合法窗块的交检查，却产生 31 个非法短谱和
  93 个已指定 \(B\)-内商零子集。两者均拒绝，只保留投影；剩余成为
  21 个外部位置、84 个 \(\mathbb F_7\) 标量的带标签有限 CSP。
  唯一例外的纯商迹窗进一步禁止外点标签 \(-q,-2q\)、外点对和
  \(-q\) 及三类长度八尾；若无全核心尾，则
  \(H_6^0-H_7^0+H_8^0=1\)，且 \(s=7\) 至少有三条零核心
  \(F_3\) 块。固定 \(B\) 原子性有三目标精确判据，连续自由标量
  经规范化降为 68。完整赋值入口重建二至八元短块、全部 Hasse 与
  补原子，并用 12+13 折半 oracle 精确拒绝九至十二元商零集；该
  中间层是独立审计发现并修补的缺口，终审为 CORRECT_AFTER_FIX。
  三重的 12 轨道中，
  11 型强迫全核心三倍尾并满足同一关系；单高度型的九列投影仍
  强迫某个三倍尾。它们留下 22 个外部位置、88 个标量的直接 CSP。
  单点尾全零只是形式切片；严格 25 位置核验器现会自动重建所有
  \(b=0\) 块、Hasse 与多补原子约束。\(000,s=6\) 的显式固定
  \(B\) 商原子及实际 \(Z\)-原子抬升，先被一个高度五的二项
  \(b=0\) 商零块拒绝。更强地，该 22 外点商赋值含四重商纤维
  \(g=(1,0,1)\)，而纤维外两个 \(T\) 标签之和为 \(-g\)；全诱导
  三项短谱强制四个纤维高度相同，故这副商赋值不存在任何高度抬升。
  继续对式 (16) 的固定 \(B=q^3Q\) 骨架枚举全部六位置非零零和
  \(T\) 商标签，72,306 个五位置前缀的唯一闭合全部被单值窗禁尾
  拒绝，故该 \(B\) 骨架本身没有任何 \(T\) 商抬升。这仍未分类
  其他长度 19 商原子，也未穷尽完整 88 标量空间。
- 相对原命题：STRICTLY_WEAKER；不是完整 \(p=7\) 证明。

## LEMMA-MIDDLE-QUOTIENT-GAP：中间商零长度空档

- 精确陈述：`proofs/middle_quotient_gap.md`。
- 状态：PROVED_SUBTHEOREM；独立审计 CORRECT。
- 结论：若 \(Z\subseteq R\)、\(|Z|=3p+4\)、\(\sigma(Z)=0\)，则
  不存在长度 \([p+2,2p+2]\) 的商零位置子集。任意两两不交、长度
  2--8 的自动短商零块总支撑至多 \(p+1\)。
- 作用：为 \(p=7\) 的 9--16 层、\(p=11\) 的新短块交约束及长
  补原子内部谱传播提供统一承重接口；不单独给出商标签。

## LEMMA-UNIQUE-TAIL-LABELLED：唯一尾的完整长补原子轴向判据

- 精确陈述：`proofs/unique_tail_labelled_position_next.md`。
- 状态：结构引理与精确 CSP 接口 CORRECT；类型排除 INCOMPLETE。
- 结论：若 \(F_3\) 块含 \(c\) 个单高度核心位置，则其长商补原子
  性等价于余部每个非空真内部子集的轴向和值只落在
  \(q,2q,\ldots,(c+3)q\)。零核心补集投影到 \(C_p^2\) 后的任意
  原子分解只有二至四因子，轴系数型仅为
  \((1,3)/(2,2),(1,1,2),(1,1,1,1)\)。
- 位置传播：13 个唯一尾幸存型均有逐真实迹轴向禁值；统一验证器
  自动重建全部短块、低阶 Hasse、交网络、实际 \(Z\) 原子和每个
  \(F_3\) 补原子的全部内部子集和。没有新类型因此被排除。

## LEMMA-P7-LENGTH19-MIDDLE-SPECTRUM：固定长原子的逃逸集排除

- 精确陈述：`proofs/p7_m4_unified_quotient_search.md` 与
  `proofs/p7_m3_other_B_frontier.md`。
- 状态：两个固定骨架工作单元均经独立审计 CORRECT；全
  \(p=7\) 分支 INCOMPLETE。
- 结论：对长度 19 商原子
  \(B\)，令 \(D_B=\bigcup_{k=8}^{11}\Sigma_k(B)\)。完整
  \(F_3\) 网络中的每个外位置标签 \(t\ne0\) 必满足
  \(-t\notin D_B\)。四重旧固定 \(B\) 的 \(D_B\) 覆盖全部非零
  值，故整个固定骨架无扩张；三重路线三个新固定轨道中两个也全
  覆盖，一个只余 \(\{\pm f\}\) 并被二元高度窗排除。
- 去重：`proofs/p7_fixed_B_orbit_deduplication.md` 的显式
  \(A(x,y,z)=(x,y,x+z)\) 证明三重/四重旧 \(B\) 是同一未标记
  原子轨道；指定 \(X\) 的位置数 3 与 4 仍区分带标记分支。

## LEMMA-P7-LENGTH19-PAIR-MUTATION-FRONTIER：一步等和变异邻域

- 精确陈述：`proofs/p7_length19_pair_mutation_frontier.md`。
- 状态：PROVED_FINITE_NEIGHBOURHOOD；独立审计 CORRECT；全长度 19
  原子分类 INCOMPLETE。
- 结论：从三重旧 \(B\) 移去两个位置并换入同和值的两个位置，精确
  多重集去重后有 6840 个非平凡候选，其中恰有 8 个零和原子且
  两两 \(GL(3,7)\) 不等价。两个与既有 \(B_1,B_2\) 重复；余下六
  个新轨道中三个违反商纤维重数至多四，三个新的低纤维骨架由
  第 8--11 层逃逸集与二元高度窗排除。
- 停止线：只分类一步二位置等和变异邻域，不覆盖两步变异或一般
  长度 19 原子。

## LEMMA-P13-UNIQUE-TAIL-LABELLED-ATTACK：两个三点核心尾型的有限正规化

- 精确陈述：`proofs/p13_unique_tail_labelled_attack.md`。
- 状态：PROVED_REDUCTION；独立审计 CORRECT；两个类型与全局均
  INCOMPLETE。
- 三点尾 \((p,\ell,b)=(13,6,3)\)：轴向位置至多一个且系数只能为
  1 或 2；投影原子分为三个秩一型与一个秩二型，连轴向分解型后
  得到至多 42 个商标签模板、534 个含高度覆盖模板。
- 五点尾 \((13,8,3)\)：没有轴向单点；非原子投影必为二项原子与
  三项原子之和，二项侧轴系数恰限于
  \(\{0,1,2,3,4,5,12\}\)，并给出零核心 \(F_3\) 块必须命中的
  一侧/两侧表。
- 停止线：非轴向投影原子仍可能存在，尚未联立尾外 31/29 个位置、
  全诱导短谱和每个长补原子的完整内部子集和。

## LEMMA-P7-TAIL-CONDITIONED-MIDDLE：尾条件化完整中层谱

- 精确陈述：`proofs/p7_tail_conditioned_middle_spectrum.md`。
- 状态：PROVED_EXACT_INTERFACE；独立审计 CORRECT；全原子空间
  INCOMPLETE。
- 结论：若 \(|B|=19,|T|=6\)，则不存在长度 9--16 的商零位置
  子集，当且仅当每个尾 \(j\)-子集和避开相应的
  \(D_j(B)\)。由补集对称和 \(B\) 的原子性，只需核对
  \(j=1,2,3\)，对应 \(B\) 的 8--15、7--14、6--13 层。
- 作用：把旧单点逃逸提升为全部尾位置的精确接口；现有十二个固定
  原子都已由单点行或旧高纤维定理排除。

## LEMMA-P7-SHORT-SUPPORT-CANONICAL：支撑至多七的扩张闭合

- 精确陈述：`proofs/p7_length19_canonical_support_frontier.md` 与
  `proofs/p7_length19_support7_escape_frontier.md`。
- 状态：PROVED_FINITE_CLASSIFICATION / EXTENSION_CLOSED；独立审计
  CORRECT；支撑至少八 OPEN。
- 结论：指定 \(q\) 恰三重、其他纤维至多四时，支撑五没有原子；
  支撑六只有两个 \(GL(3,7)_q\) 轨道且均为空逃逸。支撑七的 170 个
  规范重数型中，非空逃逸原子只有 16 个、合为四轨，每轨逃逸集
  均为单点，故不能承载六点零和尾。
- 边界：支撑七搜索安全剪除了空逃逸原子，所以不是全部支撑七原子
  的无条件轨道表；结论完备的是“可扩张性排除”。

## LEMMA-P7-MUTATION-SECOND-AND-M4-RADIUS：同一路线的两个有限前沿

- 精确陈述：`proofs/p7_length19_second_pair_frontier.md` 与
  `proofs/p7_m4_68_layered_radius_two.md`。
- 状态：PROVED_FINITE_NEIGHBOURHOODS；独立审计 CORRECT；全图
  INCOMPLETE。
- 结论：七个低纤维源各走一步的邻域并集含 39,276 个候选、十个
  原子，除七源外新增三轨且均为空逃逸。固定四重代表的实际多重集
  图距离至多二邻域逐层含 \((1,8,530)\) 个原子；其中指定四重
  分支为 \((2,10,8)\)，20 支均为空逃逸。
- 去重与边界：两项都使用等和二位置变异图，作为两个精确量词范围
  登记，但不算两条全局分类路线；530 是实际多重集图顶点数，不是
  商轨道数。

## LEMMA-P13-UNIQUE-TAIL-INTERNAL-EXTERIOR：内部短谱与外部位置分片

- 精确陈述：`proofs/p13_unique_tail_internal_spectrum_refinement_unique13.md`
  与 `proofs/p13_unique_tail_exterior_coupling_frontier.md`。
- 状态：PROVED_FINITE_SLICES / EXACT_SHARD_INTERFACE；两项独立
  审计 CORRECT；类型排除 INCOMPLETE。
- 结论：三点尾含高度模板 534→511；五点尾可分解投影 91→9。
  尾外 \(31/29\) 个真实位置的投影原子分解只有 14 个轴系数型，
  长度条件留下 118/83 个前沿，组成 60,298/747 个确定分片。
- 核验接口：填充分片后会统一重建全部自动短块、9--28 禁层、统一
  商标签、Hasse/交网络、实际 \(Z\) 原子及所有长补内部子集和。
- 停止线：分片尚未填充；五点尾投影原子支、\(Z\) 外 TOP/CONST
  均未覆盖。

## LEMMA-P7-MAXIMAL-ATOM-ESCAPE-ALGEBRA：极大原子的逃逸代数

- 精确陈述：`proofs/p7_maximal_atom_escape_algebra.md`。
- 状态：PROVED_NECESSARY_PRUNING；独立审计 CORRECT；支撑至少八
  分类 OPEN。
- 结论：在 \(\mathbb F_7[C_7^3]\) 中 \(I^{18}=\mathbb F_7\Omega\)、
  \(I^{19}=0\)，且长度 19 原子逐删点积均为 \(\Omega\)。不同支撑
  标签不能落在同一射影点，但同标签仍允许多个位置副本。每个逃逸
  目标的短正表示与短负表示满足逐位置交错恒等式并彼此按真实位置
  相交；三/四重纤维还满足逐副本数分层的精确缺口梯。
- 边界：这些都是规范增广的安全必要条件，不证明所有极大原子为空
  逃逸，也不关闭 \(p=7,m=3\)。

## STRENGTHENING-SHORT-EXCHANGE-LOW-DEGREE

- 陈述：每个 \(3a\) 块的长度三或长度四原子交换邻块数为
  \(o(p^2)\)。
- 状态：DISPROVED_AT_LOCAL_INTERFACE。
- 反模型：route_a_short_exchange_degree_models.md；独立验缝
  CORRECT_AFTER_CLARIFICATION。
- 结论：两个显式实际群值局部模型分别给 \((p-4)^2\) 个命名邻块，
  同时满足高度界、两两相交、无公共位置和非零商交。
- 边界：扩充模型不是完整零和原子，不实现 Hasse 设计或长补原子；
  因而只关闭逐块度数策略，不反驳冻结命题。

## STRENGTHENING-NEAR-ATOM-INCOMPATIBLE

- 陈述：单个 \(3p-2\) 补原子与单个长度
  \(3p-4,3p-3,3p-2\) 的交换补原子配置必然矛盾。
- 状态：DISPROVED。
- 反模型：`route_a_exchange_models.md` 第 2--3 节；对每个
  \(p\ge7\) 显式实现 \(r=6,7,8\) 三种块长。
- 边界：反模型只在 \(C_p^3\) 商群实现单块接口，不是 \(A_p\)
  反例，也不实现全局逐点/逐对带符号设计。

## LEMMA-DESIGN-KERNEL：统一商标号核条件

- 精确陈述：`proofs/design_kernel.md`。
- 状态：PROVED_HERE。
- 量词：每个 ROUTE-A4 的 \(3p+4\) 原子及其全部
  \(a,2a,3a\) 短块。
- 结论：短块位置关联矩阵 \(M\) 满足
  \(\dim\ker M\ge3\)、\(\operatorname{rank}M\le3p+1\)；三个独立
  核向量正是统一 \(C_p^3\) 商标号。实际 \(a\)-坐标还必须解
  \(Mh=\rho\)，且四坐标相同列的重数至多 \(p-4\)。
- 相对原命题：STRICTLY_WEAKER；它把“真实群和值”转成可审计的
  全局线性必要条件。
- 最小缺口：在带符号点度/共度与补原子条件下，证明该核/仿射系统
  不可实现，或构造低秩相容反模型以继续红队。

## LEMMA-DESIGN-AFFINE-SPAN：实际标签仿射满秩

- 精确陈述：`proofs/design_tensor_boundary.md`。
- 状态：PROVED_HERE；独立验缝 CORRECT。
- 结论：
  \[
  \operatorname{rank}[\mathbf1,q^{(1)},q^{(2)},q^{(3)},h]=5,
  \]
  即 \(Z\) 的实际标签仿射张满 \(\mathbb F_p^4\)。
- 相对原命题：STRICTLY_WEAKER。
- 方法边界：一点、二点、三点关系可封装为完整三阶张量恒等式，但
  对核/实际坐标的一至三次收缩全部回到已有关系；低阶矩不能识别
  高度，下一步必须使用精确纤维计数或交换。

## STRENGTHENING-WEAK-DESIGN-SUFFICIENT

- 陈述：逐点、逐对带符号关系及抽象自交/交叉相交条件已经足以推出
  ROUTE-A4 的群值矛盾。
- 状态：DISPROVED。
- 反模型：`route_a_abstract_design_countermodel.md` 的确定性
  \(p=7\) 加权超图；`verify_abstract_design_model.py` 从头重建。
- 精确边界：该模型有 \(492\) 个未覆盖三点集，三点同余失败
  \(2025/2300\)；支撑关联矩阵秩为 \(25\)，不能承载非零统一商
  标号。因此它只证伪旧弱公理，既不反驳 LEMMA-TRIPLE-COVER，
  也不是原题反模型。

## STRENGTHENING-TRIPLE-NULLITY-SUFFICIENT

- 陈述：在旧点/对/相交公理上再加入全部三点同余和关联矩阵核维
  至少三，已经足以推出 ROUTE-A4 矛盾。
- 状态：DISPROVED。
- 反模型：`route_a_triple_kernel_probe.md` 的确定性 \(p=7\) 加权
  超图；支撑 \(3028\) 条边，全部 \(2300\) 个三点同余成立，关联
  矩阵秩 \(22\)、核维恰三。
- 精确边界：整个核在 \(19\) 个位置上恒为零，故不能支撑长度至少
  \(17\) 的商群补原子；全部 \(29890\) 个不同 \(F_3\) 边对交集
  商和也为零。该模型不反驳补原子或非零商交条件，更不是原题反例。
- 后续要求：核维条件必须升级为“某个长补集在核坐标下形成实际
  \(C_p^3\) 原子”，并保留不同 \(F_3\) 交集商和非零。

## LEMMA-UNIQUE-TAIL-POSITION-CONFLICT：唯一尾的有标签位置拥塞

- 精确陈述：`proofs/unique_tail_position_conflict_frontier.md`。
- 状态：PROVED_REDUCTION；独立审计 CORRECT；NO_TYPE_CLOSED，
  GLOBAL_INCOMPLETE。
- 结论：13 型中九型没有轴向尾单点，四个 \(\ell=6\) 型只可能有
  \(2q\) 单点；11 型的尾外没有 \(q\)-标签，另两型至多三个且为
  所有零核心块的公共位置。503 个多点迹块满足逐块非轴/横截分支，
  10,938 条迹不交边的尾外交集投影和非零。对 \(p=233,1399\)，
  各存在一个具体非轴位置承载至少四条边，得到至多 25 个交集见证
  位置、至多八个端点长补原子的必要分片。
- 边界：25 个位置不构成自足 CSP；每个端点仍须在完整
  \(Y\setminus A\) 上调用长补内部子集和 oracle。四个交和值尚未
  证明互斥，故没有任何唯一尾型被排除。

## LEMMA-P7-M3-SUPPORT8-FRONTIER：三重纤维支撑八闭合

- 精确陈述：`proofs/p7_m3_full_support8_frontier.md`。
- 状态：PROVED_FINITE_CLASSIFICATION；独立审计 CORRECT；完整
  \(p=7,m=3\) 与一般命题仍 INCOMPLETE。
- 量词：长度 19 商原子中指定 \(q\) 恰三重、其他商值重数至多四、
  支撑恰八，并要求可接一个六位置零和尾。
- 结论：462 个规范重数型只产生 1,846 个完整零和候选，全部不满足
  六次完整单点逃逸集含零；六尾可行候选为零。与已审计的支撑至多
  七分类拼接后，最小剩余支撑为至少九。

## LEMMA-P7-M4-SUPPORT8-SPLICE：四重纤维支撑至多八闭合

- 精确陈述：`proofs/p7_m4_full68_support_frontier.md`。
- 状态：PROVED_FINITE_CLASSIFICATION；完整 68 标量系统
  INCOMPLETE。
- 结论：无三重纤维时，支撑至多七的 42 个规范型没有非空逃逸原子；
  支撑八的 66 个规范型在 224,101 个完整候选中只有三个非空逃逸
  原子、两个定点轨道，三者的单点逃逸集均不能组成六尾。含三重
  纤维时，把该纤维改作 distinguished 值，严格拼接
  LEMMA-P7-M3-SUPPORT8-FRONTIER。因此指定 \(q^4\) 分支的支撑至多
  八全部关闭，下一边界为支撑至少九。
- 边界：这是先于高度的商层排除，不是完整 68 标量 UNSAT；支撑至少
  九的长度 19 商原子仍未分类。

## FINITE-P7-M3-SUPPORT7-MUTATION-UNION：四源逐步邻域并集

- 精确陈述：`proofs/p7_m3_full_support7_mutation_frontier.md`。
- 状态：PROVED_FINITE_FRONTIER；独立审计 FIX VERIFIED / CORRECT；
  不另计全局分类路线。
- 结论：234,612 个位置级替换去重为 17,936 个逐源非平凡一步邻域
  并集；字面重数门为 12,945/12,684，安全删除 69 个含零自动非原子
  后为 12,876/12,615，最终支撑至少八长度 19 原子为零。
- 边界：两个源彼此一步相邻，所以该并集不是四源集合的严格图距离
  一层；没有任何连通性结论，且此有限范围已被完整支撑八分类吸收。

## LEMMA-P7-SUPPORT9-STRUCTURE：支撑九以上的二维剖面与真实尾谱门

- 精确陈述：`proofs/p7_support9_structure_pruning.md` 与
  `proofs/p7_plane_projective_zero_sum_free.md`。
- 状态：PROVED_STRUCTURAL_PRUNING；独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 结论：射影简单、单标签重数至多四的 (C_7^2) 零和自由序列最大
  长度恰为 11；16 个基重数入口均达到 11，最大剖面有 77 个
  (GL(2,7)) 轨道。故任意目标长度 19 原子的二维加权剖面至多 11。
  (PG(2,7)) 最大 arc 为 8，所以 support 9 必含共线三点，并有过
  (q) 拥挤平面/八商方向全占的严格二分。实际位置前缀的
  (L_1,L_2,L_3) 单调谱及
  (0\in6E\Longleftrightarrow3E\cap(-3E)\ne\varnothing) 给出安全六尾门。
- 边界：18 个重数签名粗门骨架全部非原子，只证明总和、射影简单与
  平面容量不足以删除整签名；本引理没有分类 support 9 原子。

## FINITE-P7-M34-SUPPORT9-LIGHT：两个支撑九重数签名闭合

- 精确陈述：`proofs/p7_m34_support9_frontier.md`。
- 状态：PROVED_FINITE_CLASSIFICATION；独立审计 CORRECT；FULL SUPPORT-9
  INCOMPLETE。
- 量词：长度 19、射影支撑简单、逐值重数至多四、支撑恰九并要求可接
  六位置零和尾的商原子。
- 结论：13 个无标号重数签名中的
  ((3,2^8)) 与 ((4,2^7,1)) 完整关闭。互斥未指点规范分母为
  (358+476=834)，本次覆盖 (1+7=8) 个入口；166,345,680 个
  五层前缀只留下两个完整零和候选，二者的完整单点逃逸域都为空。
- 后续接口：共线三点规范覆盖修正为 5,741 型；已闭合两签名占 50 型，
  其余 11 个签名、5,691 个低 DFS 入口仍开放。

## FINITE-P7-SUPPORT9-COLLINEAR-REAL：四个新完整签名闭合

- 精确陈述：`proofs/p7_support9_collinear_real_frontier.md`。
- 状态：PROVED_FINITE_CLASSIFICATION；四个有限空结论均有全新独立
  审计 CORRECT；FULL SUPPORT-9 INCOMPLETE。
- 量词：长度 19、射影支撑简单、逐值重数至多四、支撑恰九，并要求
  可接精确六位置商零尾的 (C_7^3) 商原子。
- 结论：完整关闭
  \((3^5,1^4),(3,3,2^6,1),(4,4,4,2,1^5),(4,4,3,3,1^5)\)
  四个无标号签名，分母依次 56、118、197、282。前两类中第一类与
  第三类没有完整零和候选；第二类的 1,498 个、第四类的 2 个完整
  候选均有空单点逃逸域，故无原子或六尾幸存。
- 覆盖：全签名模式的等重共线换基把 23,508 个原始 (C)-标架压为
  11,871 个代表；partial 分片严格恢复全部 36 个标架。加旧两签名后
  已闭合 6/13 个签名、703/5,741 个共线入口；剩 7 个签名、5,038
  个入口。
- 边界：四签名都在后置 25 位置短块/高度层之前排空；没有 Hasse 或
  实际 (C_7^4) 结论。

## FINITE-P7-SUPPORT9-COLLINEAR-REAL-REMAINING-1：第五个完整签名闭合

- 精确陈述：`proofs/p7_support9_collinear_real_remaining.md`。
- 状态：PROVED_FINITE_CLASSIFICATION；全新独立审计 CORRECT；其余
  SUPPORT-9 INCOMPLETE。
- 量词：签名 \((3,3,3,2,2,2,2,1,1)\) 的全部 410 个共线入口，
  完整枚举 14,760 个原始 (C)-标架及 8,685 个全签名换基代表，并在
  每个真实位置前缀保留投影原子性、平面负载和精确
  \(L_1/L_2/L_3\) 六尾谱。
- 结论：3,064 个完整商零候选的单点逃逸域全部为空，故该签名没有
  精确六尾扩张；没有原子、位置尾或高度幸存。
- 累计：已闭合 7/13 个签名、1,113/5,741 个共线入口；剩 6 个
  签名、4,628 个入口。
- 边界：仍只关闭商层六尾问题；没有 Hasse、实际 (C_7^4) 或一般
  \(A_7\) 结论。

## FINITE-P7-SUPPORT9-COLLINEAR-REAL-REMAINING-2：第六个完整签名闭合

- 精确陈述：`proofs/p7_support9_collinear_real_remaining_sig2.md`。
- 状态：PROVED_FINITE_CLASSIFICATION；全新独立审计 CORRECT；其余
  SUPPORT-9 INCOMPLETE。
- 量词：签名 \((3,3,3,3,2,2,1,1,1)\) 的全部 410 个共线入口、
  14,760 个原始 (C)-标架和 8,685 个全签名换基代表。
- 结论：217 个完整商零候选的完整单点逃逸域全部为空；没有原子、
  六尾或 25 位置骨架幸存。
- 累计：已闭合 8/13 个签名、1,523/5,741 个共线入口；剩 5 个
  签名、4,218 个入口。仍只关闭商层六尾问题。

## LEMMA-UNIQUE-TAIL-FOUR-EDGE-JOINT：四边端点与共同外部谱

- 精确陈述：`proofs/unique_tail_four_edge_joint_csp.md`。
- 状态：PROVED_INTERFACE / EXACT_SURVIVOR_BRANCHES；独立审计 CORRECT；
  JOINT_UNSAT_NOT_ESTABLISHED / GLOBAL_INCOMPLETE。
- 结论：对 (p=233,1399) 的三点唯一尾，四条共享同一非轴位置的边
  只有“重复迹产生不交等和短花瓣”或“全异迹强制三个单点迹块”两支。
  十一种端点图、15 个四边迹子图与 28,584 个迹赋值已穷尽。
  端点局部并 (L) 至多 52 点，共同外部 (R) 至少 (2p-44) 点；
  同一个可实现 (M_R(k,g)) 与局部因子卷积精确检查所有选中端点补
  原子的内部子和，并给出 (R) 内不交投影零子集的系数 packing。
- 边界：单张边缘谱不能恢复使用外部位置的自动块之间的真实交，亦未
  检查所有新诱导 (F_3) 的非零交与补原子；没有关闭任何唯一尾型。

## LEMMA-UNIQUE-TAIL-COMMON-R：共同外部序列的三原子分解

- 精确陈述：`proofs/unique_tail_common_R_next.md`。
- 状态：PROVED_DECOMPOSITION；独立审计 CORRECT；FOURTH_BLOCK_NOT_FORCED /
  GLOBAL_INCOMPLETE。
- 结论：可取
  (R=P_1\dot\cup\cdots\dot\cup P_t\dot\cup K)，其中 (t\le3)，
  每个 (P_i) 是 (C_p^2) 投影零原子，(K) 投影零和自由。共同
  packing 仅有七型，并在每个端点的完整投影原子分解中给出 14 个
  余部行；((3),(1,2),(1,1,1)) 三型强制所有
  (K\cup(L\setminus H)) 本身为 (C_p^2) 原子。共同谱进一步因式
  分解为 (Phi_R=\Phi_K\prod_i\Phi_{P_i})，并有精确长度与总和接口。
- 边界：纯长度下界 (D(C_p^2)-43) 甚至不强迫第一个投影零块；七型
  尚未排除，也未构造实际共同 (R)。

## LEMMA-UNIQUE-TAIL-MARKED-F3：全自动短块与逐位置补原子谱

- 精确陈述：`proofs/unique_tail_seven_type_full_f3.md`。
- 状态：PROVED_EXACT_MARKED_INTERFACE；独立审计 CORRECT；
  NO_PACKING_TYPE_CLOSED / GLOBAL_INCOMPLETE。
- 结论：三状态逐位置谱同时标记自动块的外部部分 (F) 与其长补原子
  内部的任意 (G\subseteq R\setminus F)；四状态 Venn 谱同时标记
  两个外部块和真实交。与局部 (L) 卷积后，统一枚举全部长度 2--8
  商零短块、每个新 (F_3) 与端点的非零商交、两个外部 (F_3) 的
  真实交，以及每个新长补原子的全部内部子集和。
- 边界：这是同一实际标签上的精确接口恒等式，没有枚举
  (p=233,1399) 的完整标号实例；逐位置 Hasse 与 (Z) 实际原子只在
  `--instance` 严格核验模式中保留，七个 packing 型均未关闭。

## LEMMA-UNIQUE-TAIL-FORCED-EXCHANGE：强制余部原子的交换门

- 精确陈述：`proofs/unique_tail_forced_common_atoms_attack.md`。
- 状态：PROVED_EXCHANGE_GATE / LOCAL_COVER_SURVIVOR；独立审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 结论：在 ((3),(1,2),(1,1,1)) 三型中，对不同端点 (H,J)，
  \(\rho\bar\sigma(H\cap J)=0\) 当且仅当
  \(K=\varnothing,L=H\cup J\)。此时两差片分别是 (Q_J,Q_H)；
  轴向覆盖对只可能是两个不同双点迹，重复迹轴向子支完全删除。
  28,584 个迹着色中，15,072 个已在此门上强制全部端点对非轴，
  13,512 个仍含双点迹覆盖候选。
- 反过强声明：两个目标素数上都存在可逐项核验的十位置、五端点局部
  幸存者，并可接三种 (K=\varnothing) packing；它不是完整
  \(A_p\) 候选。故“强制 (Q_H) 原子本身已矛盾”被严格反驳。

## FINITE-UNIQUE-TAIL-TEN-SKELETON：十位置覆盖骨架不可提升

- 精确陈述：`proofs/unique_tail_cover_survivor_lift.md`。
- 状态：TEN_POSITION_SKELETON_NOT_LIFTABLE；全新独立审计 CORRECT；
  NO_PACKING_TYPE_CLOSED / GLOBAL_INCOMPLETE。
- 固定坐标核：全部长度 2--8 局部商零闭包恰有 14 行；唯一坏行为
  \(X_2\dot\cup\{u_2,u_3,w_1,w_2,z\}\)，长度 7、实际和 (a)，
  不在长度 7 的 (F_2/F_3) 窗内。原构造的 (U) 和值也不满足唯一尾
  标签式。
- 重标不变量核：保留三条单点迹余部的 incidence 与统一商标签时，
  任取两条 (Q_{s_i},Q_{s_j}) 都强制一个三位置尾，其商和为
  ((b+2)q)；加入 (p-b-2) 个 (X) 位置得到长度 (p-b+1) 的商零块，
  对 (p=233,1399) 分别为 230、1395，均落入冻结禁区 ([9,p+1])。
- 精确量词：排除该十命名位置关联骨架的所有重标与所有外部 (R)
  补全；不排除其他端点 incidence 骨架，也不排除任一 packing 主型。

## LEMMA-UNIQUE-TAIL-COVER-FORBIDDEN-GENERAL：全单位形式与稠密覆盖门

- 精确陈述：`proofs/unique_tail_cover_forbidden_block_generalization.md`。
- 状态：PROVED_GENERAL_FORBIDDEN_BLOCK_GATE /
  EXACT_UNIT_FORM_CLASSIFICATION；全新独立审计 CORRECT；
  NO_PACKING_TYPE_CLOSED / GLOBAL_INCOMPLETE。
- 单位形式：穷尽 \(\alpha Q_E+\beta Q_F+\gamma U\) 的 26 个非零
  单位系数组合；唯一可使用大 (X) 核的二余部形式是
  \(Q_E+Q_F-U\)，且它成为实际 0/1 块当且仅当两迹不交并由
  \(E\cup F\) 覆盖全部尾外位置。
- 稠密推广：\(\sum_{E\in\mathcal S}Q_E-mU\) 的 0/1 性由每个实际
  位置的端点度精确刻画；轴系数 \(k+mb\ge4\) 时必落入冻结禁窗。
- 保护层：每个迹不交幸存对都必须有
  \(D_{EF}=Q_E\cap Q_F\cap(L\setminus U)\ne\varnothing\)，且其投影
  和非轴。只记录大小或给每条边独立分配非轴值仍是放宽。
- 穷尽边界：28,584 个迹着色、13,512 个含覆盖候选的着色及 24,468
  个覆盖对出现全部重放；每个素数 372 个规范迹类都存在通过当前
  incidence/迹/长度门的固定骨架。它们没有配置统一标签，故不是
  商标签 SAT，也没有关闭三个强制 packing 型。

## FINITE-UNIQUE-TAIL-COVER-UNIFIED-PROJECTION：固定骨架统一标签分类

- 精确陈述：`proofs/unique_tail_cover_unified_projection_labels.md`。
- 状态：FIXED_SKELETON_PROJECTION_CLASSIFICATION；全新独立审计
  CORRECT；TRACE CLASSES / FULL LABELLED INTERFACE OPEN。
- 共同系统：对每个素数的 372 个规范迹类所选**固定** incidence，
  同一矩阵同时约束每个端点、(U) 和 (L) 的和值；禁止族包含每个
  (Q_E) 的全部非空真内部子集及每个非覆盖端点交。
- 精确分岔：210/372 个固定骨架的行空间强迫一个禁用子集投影为零；
  162/372 个无此障碍。后者以 (N<p^2) 的联合避超平面论证和报告内
  显式逐位置 (C_p^3) 标签同时实现全部 (Q_E) 原子及非覆盖交非轴。
  两素数共核验 324 套标签、99,360 个真内部子集和 5,940 个交。
- 边界：210 只排除构造器选定的骨架，不关闭对应迹类；162 也未加入
  (R)、全部自动短块、长补原子、实际高度或 Hasse，故不是完整 SAT。

## LEMMA-UNIQUE-TAIL-FORCED-KERNEL-NONEMPTY：三强制型共同核非空

- 精确陈述：`proofs/unique_tail_forced_kernel_nonempty.md`。
- 状态：FORCED_TYPES_REQUIRE_NONEMPTY_COMMON_KERNEL /
  ALL_ENDPOINT_INTERSECTIONS_NONAXIAL；全新独立审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 统一整体块：若 \(K=\varnothing\)，由
  \(L=E\dot\cup Q_E\)、\(\bar\sigma(E)=0\)、
  \(\bar\sigma(Q_E)=q\) 得 \(\bar\sigma(L)=q\)。唯一尾
  \(\bar\sigma(U)=-bq\) 遂使 \(O=L\setminus U\) 的商和恒为
  \((b+1)q\)。
- 禁区：加入 \(p-b-1\le p-4\) 个 (X) 位置。由
  \(6\le|L|\le52\)，所得商零块长度在 (p=233) 时为 231--277，
  在 (p=1399) 时为 1,396--1,442，均落入 [9,2p+2]。
- 结论：三个强制 packing 型都必须有 \(K\ne\varnothing\)；结合交换
  充要门，每一对不同端点交都投影非轴。此前所有轴向覆盖 incidence、
  固定统一投影标签和十位置模型均位于已关闭的空核子支，只保留为旧
  接口边界记录。
- 边界：没有关闭三个型的非空核支，也没有关闭其余四个 packing 型。

## LEMMA-UNIQUE-TAIL-FORCED-SHORT-PACKING：非空核的互补短块

- 精确陈述：`proofs/unique_tail_forced_short_packing_block.md`。
- 状态：PROVED_SHORT_PACKING_BOUND；全新独立审计 CORRECT；
  后被下述七型一般化吸收。
- 真实互补块：
  \(D=X_{b-3}\dot\cup U\dot\cup\mathop{\dot\bigcup}_iP_i\) 与
  \(B=X_{p-b-1}\dot\cup K\dot\cup(L\setminus U)\) 分割 (Z)，
  且商和均为零。由 \(K\ne\varnothing,|L|\ge6\) 知 \(|B|>8\)，
  双侧禁窗与唯一正核心 (F_3) 门给 \(|D|\le7\)。
- 尺寸后果：\(N=\sum_i|P_i|\le7-b\)；因此 (p=1399) 的
  \((1,1,1)\) 强制型为空，(p=233) 同型先压成三个单点；所有存活
  强制型还有 \(|K|\ge2p+b-51\)。
- 边界：这一层尚未使用所有原子子族，也没有关闭其他型。

## LEMMA-UNIQUE-TAIL-FORCED-ATOM-SUBFAMILIES：强制型只余 (3)

- 精确陈述：`proofs/unique_tail_forced_atom_subset_blocks.md`。
- 状态：TWO_OF_THREE_FORCED_PACKING_TYPES_CLOSED；全新独立审计
  CORRECT；后被七型一般化吸收。
- 对每个非空指标集 (I)，真实块
  \(D_I=X_{b-d_I}\dot\cup U\dot\cup\mathop{\dot\bigcup}_{i\in I}P_i\)
  自动商零。写
  \(\sigma(P_i)=d_ix-k_ia\)，则同一实际标签必须对全部 (I) 同时满足
  \(k_i\in\{1,2\}\) 与
  \(\sigma(D_I)=(3-\sum_{i\in I}k_i)a\) 的真实长度窗。
- 十个尺寸向量经 24 个子族块压到六个尺寸、九个偏差赋值；
  \((1,1,1)\) 消失，\((1,2)\) 只暂留 (p=233) 的两个单点。
  后者的系数一单点位于 (R) 且标签为 (q)，使每个端点长补原子的
  (q)-纤维至少为 (p-3)，违反统一上界 (p-4)。故三个强制型只余
  \((3)\)，其 (P) 长度至多三。
- 边界：没有关闭 (3) 或非强制型。

## LEMMA-UNIQUE-TAIL-ALL-PACKING-SHORT-BLOCKS：七型压到三型

- 精确陈述：`proofs/unique_tail_all_packing_short_blocks.md`。
- 状态：SEVEN_TYPES_REDUCED_TO_EMPTY_2_3；全新独立审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 七型统一互补：若 \(d=\sum d_i,N=\sum|P_i|\)，则
  \[
  D=X_{b-d}\dot\cup U\dot\cup\mathop{\dot\bigcup}_iP_i,
  \qquad
  B=X_{p-b+d-4}\dot\cup K\dot\cup(L\setminus U)
  \]
  是 (Z) 的真实互补商零块。仅凭 (B) 的 (X) 核已有 \(|B|>8\)；
  对非空 packing，双侧禁窗与唯一尾给
  \(N\le4-b+d\)。空型正确保留为原唯一尾例外。
- 精确筛选：十四个素数—型行先给 17 个尺寸；全部 24 个非空原子
  子族块及统一偏差降到 12 个尺寸（含两个空型）；长补 (q)-纤维门
  再删 (p=233) 的 (1) 与 (1,2)。最终两个素数共同只余
  \[
  \boxed{\varnothing,(2),(3)}.
  \]
  非空余八个尺寸、十二个偏差赋值；(2) 的 (P) 长度至多二，(3)
  的 (P) 长度至多三，且每个非空真内部子集投影非零。
- 边界：三种幸存型只是必要接口，未证明可实现或为空；下一步须把
  同一个近极值核 (K)、端点余部分解、长补内部子集和与 Hasse 联立。

## FINITE-P7-SUPPORT9-REMAINING-SIG3：第三个 410-profile 签名为空

- 精确陈述：`proofs/p7_support9_collinear_real_remaining_sig3.md`。
- 状态：ONE FURTHER COMPLETE SIGNATURE COMPUTED EMPTY；全新独立审计
  CORRECT；仅为商层有限 UNSAT。
- 完整范围：签名 \((4,4,2,2,2,2,1,1,1)\) 的 410 个共线 profile、
  14,760 个原始标架与 8,685 个全签名换基代表；80,482 个完整候选
  的单点逃逸域全部为空。两次空检查点全跑逐字节复得报告哈希。
- 累计：support 9 已闭合 9/13 个签名、1,933/5,741 个共线入口，
  余 4 个签名、3,808 个入口。
- 边界：没有高度、Hasse、实际 \(C_7^4\)、\(A_7\) 或一般
  \(A_p\) 外推。

## LEMMA-UNIQUE-TAIL-SIX-F2-COMPLEMENTS：三行强制极长补原子

- 精确陈述：proofs/unique_tail_remaining_six_f2_complements.md。
- 状态：THREE_EXTREME_COMPLEMENT_ATOM_ROWS_FORCED；全新独立审计
  CORRECT；GLOBAL_INCOMPLETE。
- 十二个剩余非空偏差赋值中，恰有三行使
  \(C=X_{b-d}\dot\cup U\dot\cup P\) 成为六项 \(2a\) 块：
  \(p=233\) 的 \((2),|P|=1,k=1\) 与 \((3),|P|=2,k=1\)，以及
  \(p=1399\) 的 \((3),|P|=1,k=1\)。
- 若 \(Z\setminus C\) 可分，则较短商零边只能是二项 \(a\) 块；
  它与 \(C\) 合成长度八的正核心 \(F_3\) 块，尾严格包含
  \(U\)，违反唯一正核心尾。因此
  \(\pi(Z\setminus C)\) 是长度 \(3p-2\) 原子，其全部非空真内部
  子集商和都非零。
- 边界：这里只强制三行的补原子，不删除这些偏差行；也不对该
  \(F_2\) 补集误用 \(F_3\) 补集专属的 \(p-4\) 纤维界。

## LEMMA-UNIQUE-TAIL-ALL-INTERNAL-SUMS：剩余非空型的全长补判据

- 精确陈述：proofs/unique_tail_remaining_long_complement_internal_sums.md。
- 状态：ALL_REMAINING_NONEMPTY_LONG_COMPLEMENT_INTERNAL_SUMS_COMPRESSED；
  全新独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 对每个端点，写 \(W_H=P\dot\cup Q_H\) 与
  \(\bar\sigma(P)=dq\)。完整轴向判据同时施加在
  \(S\subsetneq Q_H\) 和 \(P\dot\cup S\) 上，给
  \(c(S),c(S)+d\in\{1,2,3\}\)。
- 型 (3) 因而强制每个 \(Q_H\) 为 \(C_p^2\) 原子。型 (2) 中，
  每个非空真投影零 \(S\subset Q_H\) 都恰有轴系数一，且
  \(S,Q_H\setminus S\) 都是长度至少二的原子；全部真零子集形成
  对取补封闭的反链。
- 穿过 \(P,Q_H\) 的其余内部子集由目标纤维
  \(\rho\bar\sigma(T)=-\rho\bar\sigma(A)\) 精确刻画；对
  \(|P|=1,2,3\)，去掉补集冗余后分别有 \(0,1,3\) 个独立目标。
  三类 \(A=\varnothing,A=P,0<A<P\) 穷尽全部位置，故这是充要
  压缩，不是短长度近似。
- 边界：型 (3)、\(|P|=1\) 时完整长补条件严格等价于 \(Q_H\)
  原子性；下一步必须联立不同端点共享的 \(K,L,P\)。

## LEMMA-UNIQUE-TAIL-SIX-F2-FRINGE：三个极长补的全带符号边缘

- 精确陈述：proofs/unique_tail_remaining_six_f2_extreme_fringe.md。
- 状态：THREE_EXTREME_COMPLEMENTS_GAIN_FULL_SIGNED_FRINGE；全新独立
  审计 CORRECT；GLOBAL_INCOMPLETE。
- 对三行中每个 \(z\in B=Z\setminus C\)，删点序列
  \(U_z=B\setminus\{z\}\) 满足
  \(\prod_{u\in U_z}(1-X^{\bar u})=J\)，故每个商目标的全部内部
  子集带符号和均为一。
- 对六项 \(C\) 的全部 62 个非空真位置子集 \(T\)，有精确双边
  截断式
  \[
  L_{\le8-|T|}^{U_z}(-\bar\sigma(T))+
  L_{\le|T|+1}^{U_z}(\bar\sigma(T)-\bar z)=1.
  \]
  三行共 \(62(697+697+4195)=346\,518\) 条 \((z,T)\) 恒等式。
- 边界：这些是模 \(p\) 带符号恒等式，不是非负计数；它们尚未
  单独删除三行。

## LEMMA-UNIQUE-TAIL-TYPE3-GROUP-ALGEBRA：近极值余部的共享顶端边缘

- 精确陈述：proofs/unique_tail_type3_near_davenport_group_algebra.md。
- 状态：TYPE_3_NEAR_DAVENPORT_SHARED_AUGMENTATION_FRINGE；全新独立
  审计 CORRECT；GLOBAL_INCOMPLETE。
- 型 (3) 中若 \(s=|P|,h=|H|\)，则
  \(|Q_H|=2p-1-\delta_H\)、\(\delta_H=h+s-9\in\{0,1,2\}\)；
  两素数共九个端点长度行，三种亏损出现次数为 \(5,3,1\)。
- 共同核 \(K\ne\varnothing\)。固定 \(k\in K\)，删点原子的积
  \[
  \Psi_{K\setminus\{k\}}\Psi_{L\setminus H}
  \]
  非零并落入 \(\mathbb F_p[C_p^2]\) 增广理想维数分别为
  \(1,3,6\) 的顶端边缘。亏损零时它恰为 \(J\)；亏损一时完整积
  \(\Psi_K\Psi_{L\setminus H}=2J\)。
- 边界：群代数有零因子，共同 \(K\)-因子不可直接取消；亏损二只
  得六维非零边缘，尚未关闭型 (3)。

## FINITE-P7-SUPPORT9-REMAINING-SIG4：第四个 543-profile 签名为空

- 精确陈述：proofs/p7_support9_collinear_real_remaining_sig4.md。
- 状态：ONE FURTHER COMPLETE SIGNATURE COMPUTED EMPTY；全新独立审计
  CORRECT；仅为商层有限 UNSAT。
- 完整范围：签名 \((4,3,2,2,2,2,2,1,1)\) 的 543 个共线
  profile、19,548 个原始标架与 10,638 个全签名换基代表；
  56,587 个完整候选的单点逃逸域全部为空，精确六尾为零。
- 累计：support 9 已闭合 10/13 个签名、2,476/5,741 个共线入口，
  余 3 个签名、3,265 个入口。
- 边界：没有高度、Hasse、实际 \(C_7^4\)、\(A_7\) 或一般
  \(A_p\) 外推。

## FINITE-P7-SUPPORT9-REMAINING-SIG5：第五个 785-profile 签名为空

- 精确陈述：proofs/p7_support9_collinear_real_remaining_sig5.md。
- 状态：ONE FURTHER COMPLETE SIGNATURE COMPUTED EMPTY；全新独立审计
  CORRECT；仅为商层有限 UNSAT。
- 完整范围：签名 \((4,3,3,3,2,1,1,1,1)\) 的 785 个共线
  profile、28,260 个原始标架与 17,160 个全签名换基代表。第四层
  41,757 个幸存前缀恰分成 33,466 个固定端点拒绝与 8,291 个射影
  重复拒绝，故没有完整候选或精确六尾。
- 确定性：作者两次从空全跑的全部语义字段与 profile 流哈希一致；
  独审再从空全跑 785/785，并无导入重放两个携带 profile，均复得
  同一空结论。
- 累计：support 9 已闭合 11/13 个签名、3,261/5,741 个共线入口，
  只余分母 1,370 与 1,110 的两个签名，共 2,480 个入口。
- 边界：没有高度、Hasse、实际 \(C_7^4\)、\(A_7\) 或一般
  \(A_p\) 外推。

## LEMMA-UNIQUE-TAIL-TYPE3-ENDPOINT-PAIRS：全端点对共享边缘因子

- 精确陈述：proofs/unique_tail_type3_shared_endpoint_fringe.md。
- 状态：TYPE_3_ALL_ENDPOINT_PAIRS_SHARE_EXACT_FRINGE_FACTORS；全新
  独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 对任意不同端点 \(H,J\)，实际花瓣
  \(A=H\setminus J,B=J\setminus H\) 与共同外部
  \(C=L\setminus(H\cup J)\) 给出同一
  \(D=\Psi_K\Psi_C,D_k=\Psi_{K\setminus k}\Psi_C\) 因子。
  因而两个 \(Q_H,Q_J\) 的完整积与共同删点积不再能逐端点独立选择。
- 六种亏损对全部分类；特别地 \((0,1)\) 强制
  \(D\Psi_B=0,D\Psi_A=2J\)，同亏损零给
  \(D_k(\Psi_A-\Psi_B)=0\)，同亏损一给
  \(D(\Psi_A-\Psi_B)=0\)。14 个条件长度对展开为 86 个实际
  交/花瓣尺寸行。
- 边界：共同因子仍不可取消；条件长度对不保证在同一实例出现，
  亏损二完整积也未被宣称非零，故尚未关闭型 (3)。

## LEMMA-UNIQUE-TAIL-TAIL-ANCHORING：避尾原子长度与端点交压缩

- 精确陈述：proofs/unique_tail_tail_anchoring.md。
- 状态：TAIL_ANCHORING_PROVED_REDUCTION；全新独立审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 任一 \(A\subseteq Q_H\) 若避开 \(U\)、投影零且轴系数为
  \(e\in\{1,2,3\}\)，则真实互补块与唯一尾给
  \[
  |A|\le4-b+e.
  \]
  系数一原子因此必须消耗 \(U\setminus H\) 的不同位置。
- 型 (2) 中 \(V_H=Q_H\setminus U\) 零和自由，18 个端点状态只余
  11 个；任意两个不同端点的交都投影非零，故轴向端点交子支关闭。
- 空型删除 \((1,1,1,1)\) 分解；避尾余部至多含一个不交原子，
  十二个端点状态中删除 \(p=1399,h=6\) 双点迹，并强制三个
  系数三长度二/三原子产生真实长度七 \(F_2\) 块。轴向端点交只能
  有 \(t=2,3\) 且尾迹可比较。
- 边界：没有关闭空型或型 (2)；混合目标共享端点门也不强迫目标
  碰撞，尚未加入完整标签、Hasse 或 \(Z\) 原子求解。

## LEMMA-P233-SINGLETON-TAIL-FRINGE：全长七首片必为秩二

- 精确陈述：proofs/unique_tail_p233_singleton_tail_fringe.md。
- 状态：PROVED_RANK_REDUCTION；全新独立审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 在 \(p=233\)、型 (3)、\(|P|=2\)、\(\kappa=1\) 的四边全异迹支，
  三个单点迹端点 \(H_i\) 若长七，则从最大 \(Q_i\) 原子删去另两个
  尾位置会产生线性泛函 \(\lambda_i\)，满足
  \(\lambda_i(w_j)=\lambda_i(w_k)=1\)。
- 尾投影秩一时，一个长七端点强迫另外两个尾系数相等；两个长七
  端点就强迫三个系数全等，与非零三系数和为零矛盾。因此秩一支只余
  \((8,8,8)\) 与 \((7,8,8)\)，全长七首片必为秩二，并有唯一有序
  \(GL(2,233)\) 规范形 \((e,f,-e-f)\)。
- 有限证书复得秩一 \((8,8,8)\) 的 231 个公共伸缩轨道及每个
  \((7,8,8)\) 排列的一个轨道；这不是对秩二支的排除。

## MODEL-P233-TYPE3-SHARED-FACTOR：共同因子接口仍可相容

- 精确陈述：proofs/unique_tail_type3_p233_shared_factor_attack.md。
- 状态：PROVED_LOCAL_COMPATIBILITY / DISPROVED_SHARED_FACTOR_ONLY_CLOSURE；
  全新独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 显式共享位置模型同时实现非空零和自由核 \(K\)、一条长七与一条
  长八端点、两个近 Davenport 原子、\(|P|=2\) 的完整混合目标、
  六项 \(F_2\) 极长补原子及同一因子下的 \(0/2J\) 分离。
- 独审进一步给出四个 \(K\)-内高度的最小扰动，使实际值重数也降到
  \(p-4\)，而不改变上述接口。故“共享因子加重数门”仍不能闭合；
  该模型没有满足全部自动短块、Hasse、唯一尾全称或实际 \(Z\) 原子。

## LEMMA-P233-SHARED-FACTOR-SKELETON-REJECTION：自动短块高度割

- 精确陈述：proofs/unique_tail_p233_shared_factor_skeleton_rejection.md。
- 状态：FIXED_QUOTIENT_SKELETON_REJECTED；全新独立审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 上述相容商骨架自动产生 \((p-2)^2=53,361\) 个字面长度八商零块
  \(X_4\dot\cup\{d,u_3,e_i,f_j\}\)。完整短谱把它们的实际和全锁为
  \(3a\)，从而对全部 \(i,j\) 强制 \(\alpha_i+\beta_j=c\)。
- 一个 461 行、462 变量、模 233 秩 461 的子系统已足够强迫两侧
  高度各自恒定，于是产生 231 重实际值，超过 \(p-4=229\)。这关闭
  固定商骨架的所有高度提升，不关闭其他商标签骨架或全长七首片。

## INTERFACE-P233-TYPE3-P2-EXACT-SLICE：首个统一逐位置精确接口

- 精确陈述：proofs/unique_tail_p233_type3_p2_exact_slice.md。
- 状态：INSTANCE_SCHEMA / EXACT_CEGAR_INTERFACE；修复对抗审计找到的
  交网络证书域漏洞后，全新复审 CORRECT；GLOBAL_INCOMPLETE。
- 接口只接受一张共享的 474 行 \(C_{233}^4\) 标签表，并从真实位置
  派生 \(T,U,H_i,L,R,P,K,Q_{H_i}\)。首版固定全长七、全异迹、
  \(|P|=2,\kappa=1\) 及已认证秩二尾投影。
- 十一项精确分离预言机覆盖 \(K\) 与全部 \(Q_H\) 内部子和、混合
  目标、完整短谱、中间禁层、唯一尾、交网络、每个 \(F_3\) 长补、
  六项 \(F_2\) 极长补、17,976,380 条 Hasse 同余及实际 \(Z\) 原子。
- 当前未载入任何 474 位置实例，故只报告
  `INSTANCE_SCHEMA/CEGAR_ORACLES_UNINSTANTIATED/GLOBAL_INCOMPLETE`；
  没有 SAT 或 UNSAT 主张。

## INTERFACE-P233-TRACE-SHARDS：36 个全异迹外层分片

- 精确陈述：proofs/unique_tail_p233_type3_p2_trace_shards.md。
- 状态：EXACT_OUTER_TRACE_PARTITION；无导入独立审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 十一幅四边无孤立图的全部 28,584 个合法六迹赋值严格分成
  28,548 个重复迹赋值和 36 个全异迹赋值。后者只落在
  paw、\(P_5\)、\(T_5\)、\(P_4\dot\cup K_2\)，固定代表计数为
  \(6,6,12,12\)。
- 报告逐行保存图型、边表、端点迹掩码和稳定 shard 编号。这只穷尽
  外层迹选择；474 位置端点掩码、统一标签与全部预言机仍待生成。

## MODEL-P233-RANK2-THREE-FUNCTIONAL：三泛函共同字面相容

- 精确陈述：proofs/unique_tail_p233_rank2_three_functional_compatibility.md。
- 状态：PROVED_EXACT_FRINGE_COMPATIBILITY / RELAXED_BEYOND_THE_FRINGE；
  全新独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 在 \((w_1,w_2,w_3)=(e,f,-e-f)\) 下，三个顶层泛函唯一为
  \[
  (\lambda_i(w_j))=\mathbf1\mathbf1^{\mathsf T}-3I_3,
  \]
  秩二且 \(\lambda_1+\lambda_2+\lambda_3=0\)。
- 一张 469 位置表同时实现三个长 463 的 \(C_i\)、六个非对角删尾
  积 \(\Psi_{C_i}(1-X^{w_j})=J\)，以及三对 458 位置共同字面因子和
  五位置交换花瓣。故“三泛函加共同因子”本身仍不矛盾。
- 放宽边界：模型不满足或不主张三个 \(Q_i\) 的完整原子性、全短谱、
  实际重数、Hasse 或 \(Z\) 原子；它不是首片幸存者。

## LEMMA-UNIQUE-TAIL-BICLIQUE-HEIGHT-CUT：连通短块图强迫同值

- 精确陈述：proofs/unique_tail_biclique_height_cut.md。
- 状态：PROVED_GENERAL_LEMMA / OPEN_RECTANGLE_233；全新独立审计
  CORRECT；GLOBAL_INCOMPLETE。
- 若固定位置基底 \(C\) 与二部图每条边 \((u,v)\) 都给同长商零块
  \(C\dot\cup\{u,v\}\)，且短谱将其实际和锁为同一 \(\lambda a\)，
  则每个连通分量两侧的实际标签分别恒定。生成树方程秩为
  \(|A|+|B|-1\)，统一标签闭包还会自动补全该分量的完整二部积。
- 对 \(p=233\)，任一侧达到 230 个位置就超过实际重数上界 229；
  固定骨架的 231×231 高度割是该一般引理的特例。
- 首片静态几何目前只给 \(|K|\ge435\)、\(|Q_i\setminus K|\le30\)
  和端点间至多六位置单向改动，不能推出所需矩形。显式单原子边界例
  还表明大投影纤维可被 \(q\)-坐标拆成精确商标签重数至多二。
- 当前承重缺口命名为 `OPEN-RECTANGLE-233`：需从三个近相同最大
  原子、共同核、混合目标和统一提升中强迫一个固定六位置基底及某侧
  至少 230 个顶点的连通长度八配对图。

## LEMMA-P233-RANK2-TWO-MONOCHROMATIC-KERNEL：双尾方向 116 阈值

- 精确陈述：proofs/unique_tail_p233_rank2_rectangular_kernel_exclusion.md。
- 状态：TWO_MONOCHROMATIC_COMMON_KERNEL_THRESHOLD_EXCLUDED；全新
  独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 在尾规范形 \((e,f,-e-f)\) 中，若三个 \(Q_i\) 的三重公共部分含
  \((\alpha e)^R(\beta f)^S\) 且 \(R,S\ge116=(p-1)/2\)，则三者
  不可能同时为原子。
- \(Q_3\) 中的尾点 \(e,f\) 先把逆元代表压到
  \(m\le p-R-1\le R,n\le p-S-1\le S\)；于是 \(Q_1,Q_2\) 中的
  \(-e-f\) 与相应 \(m+n\) 个公共核位置组成长度至多 \(p<2p-1\)
  的真零和子列。
- 116 是这套容量论证的精确边界：四个 115/116 行在 116/116 时
  proof gap 为零，含 115 时分别留下 464、232、232 个参数缺口；
  这不声称 115 行可实现。固定 227×226 核是直接推论。
- 该引理只禁止沿两个规范尾方向的两个大单色投影纤维；没有分类一般
  453 位置共同核或关闭首片。

## THEOREM-EXTERNAL-PROPERTY-B：秩二极长原子的简单形

- 外部承重来源：Reiher，*A proof of the theorem according to which every
  prime number possesses Property B*，Theorem 10.2；原文的 cloudy/simple
  定义在第 2--3 页。
- 使用范围：每个 (C_p^2) 中长度 (2p-1) 的最小零和序列含某个
  重数至少 (p-1) 的元素，并可写成
  (g^{p-1}\prod_{t=1}^{p}(h+a_tg))，其中
  \(\sum_ta_t=1\)。这是外部定理，不记作仓库内新证明。

## LEMMA-PROPERTY-B-THREE-DOMAIN：三个尾对的共同标签域为空

- 精确陈述：proofs/unique_tail_property_b_three_domain_general.md。
- 状态：PROVED_APPLICATION_OF_EXTERNAL_THEOREM；全新无导入独审
  CORRECT；GLOBAL_INCOMPLETE。
- 对每个素数 (p\ge7)，若三个长度 (2p-1) 的 (C_p^2) 原子
  分别含尾对
  \((f,-e-f),(e,-e-f),(e,f)\)，则 Property B 把任一共同非零标签
  压入三组各四条射影/仿射直线；三组交为空。穷尽消元表明仅特征
  (2,3,5) 会退化。
- 因此，只要三条补原子共享一个真实位置，它们就不能同时存在。
  首个 (p=233) 全长七秩二切片有非空共同核，故该切片已排除；
  `OPEN-RECTANGLE-233` 不再是这条切片的承重缺口。

## LEMMA-P233-PROPERTY-B-TWO-MAX-MIXED：两个长七 singleton 已足够

- 精确陈述：proofs/unique_tail_property_b_two_max_mixed_exclusion.md。
- 状态：PROVED_P233_MIXED_LENGTH_EXCLUSION；全新无导入独审 CORRECT；
  GLOBAL_INCOMPLETE。
- 两个 singleton 长七端点给两条最大原子，第三条只需是长度大于四、
  含 (e,f) 的原子；共同字面核至少 435。两条 Property B 重基在
  共同核中各至少出现 202 次，故必须互落对方支撑。
- 对 (234^2=54,756) 个标准域对的独立枚举只余四对：前三对令
  第三原子含 (e+f+(-e-f)=0)，最后一对令其含
  (e+f+g_1+g_2=0)。所以三个 singleton 端点中至多一个长七。
- 一个只保留两条最大原子的统一标签放宽例仍然存在，说明第三条原子
  及其内部子集和是承重条件。

## REDUCTION-P233-LENGTH-DECORATED-TRACE：1440 降至 720

- 精确陈述：proofs/unique_tail_p233_length_decorated_trace_reduction.md。
- 状态：EXACT_OUTER_LENGTH_PARTITION / PROVED_REDUCTION；全新无导入
  独审 CORRECT；GLOBAL_INCOMPLETE。
- 36 个全异迹父分片按所有端点长度 (7/8) 装饰共有 1440 行。
  由三域引理和两-max 混合引理删去 singleton 长七数至少二的 720 行，
  精确留下 720 行；按图型为 (48,96,192,384)，按 singleton 长七数
  为 (0:180,1:540)。
- 其中 36 行为全长八外层见证，只证明纯图/迹/长度层不能强迫长七；
  它们没有端点掩码、统一标签或原子预言机，不能称为可实现实例。

## MODEL-P233-PROPERTY-B-DOUBLET-BOUNDARY：doubleton 长七仍穿过当前层

- 精确陈述：proofs/unique_tail_p233_property_b_mixed_trace_relaxed_models.md。
- 状态：RELAXED_SAT_BOUNDARY；全新无导入独审 CORRECT；
  GLOBAL_INCOMPLETE。
- 三个逐位置统一 (C_{233}^2) 标签模型分别实现 singleton 加两个
  nested doubleton、singleton 加 complementary doubleton、三个
  doubleton；其 ((|K|,|L|)) 为 ((463,9),(462,10),(456,16))。
- 每个展示的 (Q_H=K\dot\cup(L\setminus H)) 都是长度 465 的最大
  最小零和序列，且 (K) 是精确公共交并零和自由。
- 这些模型故意未加入 (q)-坐标提升、两位置 packing (P) 及混合
  目标、完整自动短块闭包、实际高度/Hasse/(Z) 原子。模型 D 已在
  一个端点内部出现三位置投影零子集，因此下一层必须恢复这些条件，
  不能把该放宽 SAT 提升为精确切片 SAT。

## MODEL-P233-DOUBLET-D-ENDPOINT-LIFT：端点内部 (q)-闭包仍 SAT

- 精确陈述：proofs/unique_tail_p233_doubleton_D_q_lift_attack.md。
- 状态：RELAXED_ENDPOINT_INTERNAL_Q_LIFT_SAT；全新无导入独审
  CORRECT；GLOBAL_INCOMPLETE。
- 固定 three-doubleton Model D 的 472 个 (W) 位置，加入统一
  (q)-坐标/高度、两点 (P)、全部一阶总和和实际重数上界 229。
  三个端点的 (3\cdot2^7=384) 个位置子集全枚举只给
  (3\times F_3(7)+F_1(5)) 及一个需 232 个 (X) 而不可闭合的行。
- 这证明单端点内部短闭包还不够；它未覆盖跨端点的全 (Y) 短谱、
  不交短块、mixed (P)--(Q_H)、Hasse 或实际 (Z) 原子。

## REDUCTION-P233-DOUBLET-NC-LIFT：N 全称死，C 当前 lift 死

- 精确陈述：proofs/unique_tail_p233_doubleton_NC_lift_attack.md。
- 状态：FIXED_N_ALL_LIFTS_UNSAT / DISPLAYED_C_LIFT_REJECTED；全新
  无导入独审 CORRECT；GLOBAL_INCOMPLETE。
- 固定 Model N 中三个端点同和 (3a) 强制
  (gamma(x_f)=gamma(u_f)) 与 (gamma(x_t)=gamma(u_t))；任一单交换
  已产生字面不同但同和的第二条唯一尾。因此该固定 incidence 对所有
  实际提升都排除，不依赖 Property B、(P) 或核标签。
- 固定 Model C 有一套统一 lift 与 \(P\) 通过首矩、两条最大
  \(\rho\)-原子、重数门、四组 mixed targets 和两个端点内部的全部
  \(\rho\)-零子集；但它含一个长度三、商零、实际和 \(2a\) 的全局
  短谱坏块。故只排展示 lift；同一 \(\rho\)-骨架的其他重标仍 OPEN。
- 初版报告的哈希种子非确定排序由独审发现并修复；最终双进程输出
  逐字节相同。

## LEMMA-P233-DUPLICATE-REMAINDER-TAIL：等和余部强迫第二尾

- 精确陈述：proofs/unique_tail_p233_duplicate_remainder_unique_tail_obstruction.md。
- 状态：PROVED_SEPARATION_ORACLE；全新无导入独审 CORRECT；
  GLOBAL_INCOMPLETE。
- 若 (u\in U,v\in Y\setminus U)，两个等和端点写成
  (H_u=R_u\dot\cup\{u\})、(H_v=R_v\dot\cup\{v\})，且
  (sigma(R_u)=sigma(R_v))，则 (gamma(u)=gamma(v))，从而
  (U-u+v) 是第二条字面尾。相同字面余部是无需标签即可检查的充分
  条件；Model N 恰含两个这样的 motif。
- 720 个外层行中有 678 行、共 1,776 个“同长嵌套迹”候选槽；但
  上游没有真实端点掩码。每一行都存在 common-(y)+private-petal 的
  motif-free 掩码，所以当前层严格删除 (0/720)，不能把候选槽提升
  为真实 motif。

## REDUCTION-P233-DOUBLET-D-FULL-SHORT：展示的 D lift 被三层分离

- 精确陈述：proofs/unique_tail_p233_doubleton_D_full_short_closure.md。
- 状态：DISPLAYED_D_Q_LIFT_REJECTED / SKELETON_RELABEL_OPEN；全新
  无导入独审 CORRECT；GLOBAL_INCOMPLETE。
- 474 个 (Y) 位置按完整实际标签精确压成 17 类；162,225 个容量
  向量给 252 个短轮廓，其中 75 允许、177 禁止。最短坏块由三真实
  位置组成，商和与实际和都为零，同时也直接违反实际 (Z) 原子性。
- 75 个允许轮廓的 2,850 对中有 62 对可位置不交，其中 53 对违反
  (F_3)-全短相交或 (F_2)-内部相交；共同 (T\subset K) 还对
  三个 (Q_H) 与两个 (P) 单点给出六个 mixed-target 反例。
- 这只排上一节展示的 \(q\)/高度/\(P\) 重标；没有穷尽固定
  \(\rho\)-骨架的所有重新标号，因此不得写成 Model D 骨架 UNSAT。

## LEMMA-NEAR-MAX-ATOM-COMPLETION：长度 \(2p-2\) 原子的删点二分

- 精确陈述：proofs/unique_tail_near_max_atom_completion_dichotomy.md。
- 状态：PROVED_REDUCTION；独立审计 CORRECT（条件于 Reiher 的
  Property B）；GLOBAL_INCOMPLETE。
- 对任意删点 \(x\)，\(Q\setminus\{x\}\) 要么覆盖全部非零目标，
  要么嵌入最大 Property-B 原子，并在删点序列中出现至少 \(p-3\)
  个重标签。被删点本身允许落在点线域外。

## LEMMA-P233-SINGLETON-461-COVER：统一长八端点的 461 个 complete 删除

- 精确陈述：proofs/unique_tail_p233_singleton_completion_cover.md。
- 状态：PROVED_REDUCTION；独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 720 个 mixed-length outer survivors 的三个 singleton 中，存在一个
  长八端点，使其 462 个非尾位置至多一个删点缺失非零目标；故至少
  461 个 complete 删除，其中至少 434 个位于 \(K\)。
- 证明以两个坏删点的并恢复完整 \(Q_i\)，再用三个尾对允许域空交；
  不要求两次 Property-B 完成选择同一具体标准域。

## BOUNDARY-COMPLETION-RICH-NEAR-MAX-ATOM：463 个 complete 删除仍可 mixed

- 精确陈述：proofs/unique_tail_completion_rich_near_max_atom_family.md。
- 状态：PROVED_BOUNDARY；独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 对每个 \(p\ge5\)，原子
  \(f^{p-1}e^{p-3}(2e)(e+f)\) 除 \(2e\) 外的 \(2p-3\) 个删点
  全部 complete；坏删点恰漏 \(-e+\langle f\rangle\)。
- 稀疏 \(q\)-spike 与 packing 高度 \(1,2\) 还使单端点全部 mixed
  蕴含成立，故纯投影覆盖与单端点 mixed 不能承担闭片。

## LEMMA-LENGTH464-Q-FIBRE-MOMENT：逐目标一阶 \(q\)-矩

- 精确陈述：proofs/unique_tail_length464_q_fibre_linear_moment.md。
- 状态：PROVED_REDUCTION；独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 对长度 \(2p-2\) 投影原子及总 \(q\)-和一的统一提升，
  \(M_1(r)=1+\lambda(r)\)，其中 \(\lambda\) 为唯一线性泛函。
  所有等式在 \(\mathbb F_p\) 中；signed coefficient 只作普通表示
  存在性的单向判据。

## LEMMA-P233-MIXED-CORE-SEPARATOR：mandatory core、短表示与二次签名

- 精确陈述：proofs/unique_tail_p233_mixed_core_separator.md。
- 状态：PROVED_REDUCTION；独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 存在一个长八 singleton，使全部非零目标的非尾 mandatory-core 并
  至多一个位置。任一避尾 mixed 表示长至多二，正负目标的避尾短
  表示族交叉相交；否则该目标族由两个尾位置横截。
- packing 方向排除六个正负尾标签。长七 singleton 的删双尾顶积为
  仿射签名 \(1+x+y\)，强制长度六/七商零块；长八的删双尾顶积为
  \(1-(x-y)^2+A x(x+1)+B y(y+1)\)，三条尾方向强制短块，generic
  方向只留下显式二次参数支。

## LEMMA-PROPERTY-B-DOUBLET-INTERSECTION：大共同核的横截三点正规形

- 精确陈述：proofs/unique_tail_property_b_doubleton_intersection_attack.md。
- 状态：PROVED_REDUCTION；独立审计在发现并修复两个量词缺口后判
  CORRECT（条件于 Reiher 的 Property B）；GLOBAL_INCOMPLETE。
- 若最大 \(C_p^2\) 原子共享字面 \(K\) 且 \(|K|>p\)，其标准域要么
  全同，要么只取 canonical transverse 两域，公共支撑恰为
  \(\{g,h,g+h\}\)。当 \(K\) 避开三尾时，complementary
  singleton--doubleton 与 three-doubleton 均给
  \(|K|\le2p-4\)；Model C 在第一上界取等。
- 长八补全分支只约束删点序列；首个 mask 前沿仍需统一标签，本文
  没有删除 outer row。

## FRONTIER-P233-ENDPOINT-MASK-1356：首条真实掩码轨道

- 精确陈述：proofs/unique_tail_p233_endpoint_mask_frontier.md。
- 状态：ONE-ROW EXACT MASK ENUMERATION；独立不同顺序重算 CORRECT；
  SHARED LABELS PENDING；GLOBAL_INCOMPLETE。
- decorated-1356 的 raw/containment/duplicate-overlap/net/survivor
  计数为 \(27172/206/(567-12)/555/26411\)。四边交严格为同一位置
  \(y\) 的原始/幸存计数为 \(21/19\)。
- 26,411 只是掩码轨道，不是统一 \(\rho,q\)、高度、全短闭包与
  原子预言机下的 SAT 实现；另 719 行尚未作同级枚举。

## FINITE-P233-CD-SPARSE-RELABEL：两族稀疏缺陷重标号归零

- 精确陈述：
  proofs/unique_tail_p233_doubleton_CD_sparse_relabel_exhaustion.md。
- 状态：PROVED FINITE EXHAUSTION；独立内存重算 CORRECT；严格限于
  两个冻结 sparse-support 族；GLOBAL_INCOMPLETE。
- Model D 的 21 个目标 mask 组与 12,649,104 个非零
  target--parameter 检查在 mixed 门归零。Model C 的 54 组恰余
  9798 个 mixed 候选，全部在字面位置高度的长度二、三、八刚性
  短谱方程归零。
- 没有支撑压缩定理把任意 mixed-compatible \(q\)-标号送入这两族，
  故不得升级为固定 Model C/D \(\rho\)-骨架全重标 UNSAT。

## LEMMA-P233-MIXED-HEIGHT-EXCHANGE：短表示的真实交换电路

- 精确陈述：proofs/unique_tail_p233_mixed_height_exchange.md。
- 状态：PROVED_REDUCTION；独立审计在修正 180 行作用域措辞后判
  CORRECT；GLOBAL_INCOMPLETE。
- 任一避尾 mixed 表示只余四个 \((e,|E|,F_j)\) 高度分支。若正负
  两目标都能避尾表示，交叉相交排除两边同时为单点，故至少一边是
  双点；该双点的完整实际和恰等于另一个 packing 单点。
- 若没有双点交换，则只有一边能避尾且只能单点，另一边由双尾横截；
  单点实际和只余相差 \(x,a,0\) 的三个签名。尚未载入具体统一标签，
  未删除 outer row。

## LEMMA-P233-MIXED-EXCHANGE-REFACTORIZATION：二点 packing 升三点

- 精确陈述：proofs/unique_tail_p233_mixed_exchange_refactorization.md。
- 状态：PROVED_REDUCTION；独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 若 mixed 双点表示 \(E\subset Q_H\) 的完整实际和等于 packing
  单点 \(z^\ast\)，则
  \(P'=(P-z^\ast)\dot\cup E\) 是长度三投影原子，
  \(Q'_H=(Q_H-E)\dot\cup\{z^\ast\}\) 也是原子，并保持轴系数
  \(3+1=4\) 与完整实际和。
- 长七 singleton 给 \(|Q'_H|=464\)，新三点 packing 触发三个补
  轨道的全称 mixed 目标。若两边都有双点交换，两条新原子共享
  \(2p-4=462\) 个字面位置，两个二点花瓣实际和相等。
- 新 \(Q'_H\) 只直接调用一般近最大删点二分、mandatory-core 表示
  与 \(q\)-矩；原 461 定理不被无条件外推到它。

## LEMMA-P233-ONE-SIDED-SINGLETON-CLOSURE：单侧 singleton 支闭合

- 精确陈述：proofs/unique_tail_p233_one_sided_singleton_normal_form.md。
- 状态：PROVED_REDUCTION；独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 长七 singleton 若没有双点交换，则删双尾仿射签名强迫
  \(Q=g^{232}r^{231}ef\) 与 \(g=e+f-2r\)。共同核下界给至少一个
  \(g\) 和两个互异 \(r\) 位置；它们与第三尾在另一 singleton 长补
  内组成四位置真零和。因此 540 行的无交换支全部关闭，但 outer row
  仍可进入双点交换支。

## LEMMA-P233-SINGLE-EXCHANGE-PROPERTY-B：长七单交换正规形

- 精确陈述：
  proofs/unique_tail_p233_single_exchange_property_b_normal_form.md。
- 状态：PROVED_REDUCTION；独立审计 CORRECT；GLOBAL_INCOMPLETE。
- Property-B 标准支撑没有长度小于 \(p\) 的带重复零和关系，故正负
  signed 纤维不能同时避尾。任一幸存双点交换严格为
  \(U_Q=\{\ell_c,\ell_d\}\)、\(E=\{g,\ell_a\}\)、
  \(s=\ell_{a+1}\)，两个尾均在线上。
- 交换后 \(Q'=g^{p-2}L'\)，其中 \(L'\) 的 \(p\) 个线位置是
  \(-g\)-纤维的完整强制核，非尾部分恰为 \(p-2=231\) 个位置。
  双交换共享 462 核的条件支在长七情形为空；新 \(Q'\) 不在原 461
  端点定理的直接量词内。
- 显式 \(|K|=435\) 局部模型证明 \(K+\gamma\) 投影子集和门仍不足；
  该模型故意违反完整尾锚定，不是当前分支的 SAT 见证。

## LEMMA-P233-EXCHANGE-STAR-MULTIPLICITY：长七交换星超重排除

- 精确陈述：
  proofs/unique_tail_p233_exchange_star_multiplicity_exclusion.md。
- 状态：PROVED_REDUCTION；两次独立量词审计 CORRECT；
  540_OUTER_ROWS_EXCLUDED / GLOBAL_INCOMPLETE。
- 单交换正规形中固定线位置 \(y\)，遍历最大原子的全部 \(p-1\) 个
  重项实际位置 \(x\)。每个 \(\{x,y\}\) 都是同一 mixed 目标的避尾
  双点表示，故完整高度交换逐位置强迫
  \(\sigma(x)+\sigma(y)=\sigma(z^\ast)\)。于是 \(p-1=232\) 个
  重项位置的实际标签全同，违反最大实际重数 \(p-4=229\)。
- 与单侧 singleton 支闭合合并，720 个 mixed-length outer survivors
  精确删去含长七 singleton 的 540 行，只余 180 个三个 singleton
  端点均长八的行；其中只有 36 行的全部端点均长八。

## BOUNDARY-P233-THREE-H8-QUADRATICS：三二次签名联合形式解

- 精确陈述：
  proofs/unique_tail_p233_three_h8_quadratic_joint_boundary.md。
- 状态：PROVED_BOUNDARY；独立全域代回 CORRECT；GLOBAL_INCOMPLETE。
- 对 \(s=xe+yf\)、\(x,y,x-y\ne0\)，三个 singleton 尾基下同时消去
  \(\pm s\) 的六个二次参数被唯一确定；\(p=233\) 有 53,592 个有向
  解、26,796 个 \(\pm\)-轨道。故三张 signed 二次式与六尾排除本身
  不能关闭剩余 180 行；形式参数没有被提升为实际长补原子。

## LEMMA-P233-H8-REFLECTION-FIBRE：长八交换反射纤维高度割

- 精确陈述：proofs/unique_tail_p233_h8_reflection_fibre_height_cut.md。
- 状态：PROVED_REDUCTION；独立审计 CORRECT；GLOBAL_INCOMPLETE。
- 对 mixed 目标 \(s\)，任一非空反射纤维对
  \(N_r,N_{s-r}\) 的全部笛卡尔积都满足同一完整高度等式，故每侧
  实际值相同并至多含 \(p-4=229\) 个位置；自反纤维同样成立。
- 461 complete 删除不自动增加避尾反射边。显式完成丰富模型只见证
  461、mandatory-core、两条 signed mixed 窗与一阶矩的选定放宽系统
  相容；它以 \(p-3>p-4\) 的精确商标签重数提前失败，不是完整
  \(q\) 层模型。

## LEMMA-P233-THREE-H8-MASK-COMPRESSION：三 singleton 的 73 态压缩

- 精确陈述：
  proofs/unique_tail_p233_three_h8_singleton_mask_compression.md。
- 状态：PROVED_REDUCTION；独立枚举与证明审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 三个长八 singleton 端点的任意一对交至多六点。去掉固定
  \(U,P,y_0\) 后，四个成员型重数完整参数化三端点掩码；80 个
  \(S_3\) 轨道经 pair 门压到 73 个，指定 461 见证端点时有 147 个
  pointed 状态。
- 三长补写成共同零和自由核 \(C_\triangle\) 加三个等和 fringe，
  \(450\le|C_\triangle|\le461\)、\(3\le|F_i|\le14\)。唯一
  \(m=3\) 态为 \((1,1,1,4)\)，共同平移差满足
  \(\rho(\Delta)\ne0\)。纯 mask 门仍不删除 outer row。

## LEMMA-P233-THREE-H8-M3-CUBIC-CURVE：461 核的三次系数曲线

- 精确陈述：
  proofs/unique_tail_p233_three_h8_m3_cubic_core_curve.md。
- 状态：PROVED_REDUCTION；独立代数与有限域审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 唯一 \(m=3\) 掩码态有长 461 的共同零和自由核 \(C\)。三个长补
  的删点原子性强迫 \(C\) 的普通子集和避开六个尾目标；相应带符号
  系数函数是式 (9) 的三参数三次式。
- 奇数长度共同核的补集反射强迫
  \(\alpha^2-\alpha\beta+\beta^2=3\)。在 \(\mathbb F_{233}\) 中
  该非退化二次曲线恰有 234 个点，均避开三个退化直线，且每一点
  唯一决定 \(F,I,G\)。这是必要条件，不是实际长补原子的构造；
  234 点仍须加载 461 complete 删除、统一高度及全短块闭包。

## LEMMA-P233-THREE-H8-M3-TAIL-SYMMETRY：核曲线的 39/117 轨道

- 精确陈述：
  proofs/unique_tail_p233_three_h8_m3_tail_symmetry_orbits.md。
- 状态：PROVED_REDUCTION；独立同构与有限域审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 同步置换 \(u_i,v_i,Q_i\) 并施以对应的商平面自同构，给出整个
  字面位置子系统的合法 \(S_3\) 同构。三个换位的固定线均不交
  \(\alpha^2-\alpha\beta+\beta^2=3\)，三循环也无曲线上固定点，
  所以 234 点严格分成 39 个自由轨道。
- 标出 461-complete 见证端点后必须把指标一起作用；其 \(S_2\)
  稳定子仍自由，故恰余 117 个 pointed 轨道。这里只做同构去重，
  不删除任何候选轨道。

## LEMMA-P233-THREE-H8-M3-COMPLETE-WITNESS：fringe 删除排除

- 精确陈述：
  proofs/unique_tail_p233_three_h8_m3_complete_witness_cancellation_line.md。
- 状态：PROVED_REDUCTION；两次独立代数与量词审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 461-completion 见证端点中的 fringe 点 \(v_i\) 必 complete。
  否则删去它的长 \(2p-3\) 序列进入近 Property-B 支；重因子三次
  门和两尾分类只余一个统一标准原子，而该原子删任一仿射线位置都
  漏目标 \((1-a_0)g-h\)，与全部 461 个共同核删除 complete 矛盾。
- 因此 \(B_i=C\dot\cup\{u_j,u_k\}\) complete，坏删除若有只能在
  \(C\)，故至少 460 个 \(C\)-位置逐点 complete。普通和集满足
  \(\Sigma_0(\rho\sigma(C))+\{0,w_j,w_k,-w_i\}=G\)，且三个固定
  core 目标的所有普通表示公共交至多一。
- \(B_i\) 的带符号系数是仿射函数，唯一零线为
  \(-\delta/2+\langle w_i\rangle\)。线外非零目标由非零系数自动
  认证；剩余普通量词精确为零线上的 233 个目标。

## LEMMA-P233-THREE-H8-M3-UV-GATE：六位置自动短块门

- 精确陈述：proofs/unique_tail_p233_three_h8_m3_UV_short_gate.md。
- 状态：PROVED_REDUCTION；独立枚举与 lift 审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 核曲线 234 点中，228 点在 \(U\cup V\) 内除原尾外无投影零和；
  六个例外点恰为 \(\delta=w_j-w_i\)，每点唯一额外关系为
  \((U\setminus\{u_j\})\dot\cup\{v_i\}\)，并组成一个 \(S_3\)
  轨道。
- 六个例外点的轴/高度 lift 经真实短谱与唯一正核心尾门从
  \(233^2\) 压到 707 对。未标点时是一个轨道；标出 completion
  端点后分裂成三个 pointed 角色。该门本身不删除例外轨道。

## LEMMA-P233-THREE-H8-M4-O0-EXCLUSION：首个偶四次轨道排除

- 精确陈述：
  proofs/unique_tail_p233_three_h8_m4_O0_even_quartic_exclusion.md。
- 状态：PROVED_REDUCTION；三次独立量词、代数与有限域审计
  CORRECT；GLOBAL_INCOMPLETE。
- \(m=4\) 的八个带标号态组成四个 \(S_3\) 轨道。轨道
  \(O_0=(0,0,0,5)\) 的完整 fringe 等和将三个非尾标签固定为
  \(t-w_i\)。
- 长 460 共同核的系数函数平移后是九维偶四次式。三个投影原子的
  普通无表示先给十三个零点；七个固定点将空间压到显式二维核，而
  全部 53,592 个线外与 696 个尾线上非零中心都迫使 \(q(t)=0\)，
  违背空集给出的 \(q(t)=1\)。
- 因此 singleton mask 状态严格 \(73\to72\)，\(m=4\) 层
  \(4\to3\)。这删的是每条 outer row 的一个状态，不是整条 row。

## LEMMA-P233-THREE-H8-M3-EXCEPTIONAL-EXCLUSION：共同五核删例外轨

- 精确陈述：
  proofs/unique_tail_p233_three_h8_m3_exceptional_endpoint_kernel_exclusion.md。
- 状态：PROVED_REDUCTION；三次独立实际和值、短谱与枚举审计
  CORRECT；GLOBAL_INCOMPLETE。
- \(m=3\) 的五位置共同 endpoint 核满足
  \(\sigma(A_0)=4x-2\Delta\)。六个例外点上存在与
  \(R_{ij}\) 反向索引的三点集 \(S_{ij}\)，使
  \(A_0\dot\cup S_{ij}\) 导出大小 700 的实际 lift 允许集。
- 该允许集与已审 \(U\cup V\) 门的 707 对允许集交为空，故六个
  例外点全部排除。严格削减为 228 个曲线点、38 个未标点轨道和
  114 个 completion-pointed 轨道；outer row 尚未关闭。

## LEMMA-P233-THREE-H8-M3-FRINGE-EXCHANGE：端点差强制 fringe 二点交换

- 精确陈述：
  proofs/unique_tail_p233_three_h8_m3_cubic_quadratic_compatibility.md。
- 状态：PROVED_REDUCTION；独立全局坐标与量词审计 CORRECT；
  GLOBAL_INCOMPLETE。
- 三个删双尾序列严格为
  \(N_i=C\dot\cup\{v_i\}\)，其 signed 二次式由同一个三次核的
  有限差分给出。对 mixed 目标 \(r\in\{s,-s\}\)，全部普通表示
  至多二点，故
  \[
  n_i(r)=D_C(r)-S_C(r)+A_i(r)-\varepsilon_i(r),
  \]
  其中 \(A_i(r)\) 逐字面计数 fringe--核二点表示。
- 若某个跨端点差不属于 \(\{0,\pm1\}\)，便有
  \(A_i(r)+A_k(r)>0\)，从而存在真实 fringe-touching 二点表示；
  mixed 高度表把它提升为完整等式
  \(\sigma(\{v_i,c\})=\sigma(z_r^\ast)\)。
- 六尾排除后每个曲线点有 \(p^2-1-6=54,282\) 个 admissible
  有向方向，其中 53,592 个不在三条尾方向、690 个是尾方向残余。
  全部 \(234\cdot54,282=12,701,988\) 对均至少有两个坏端点差；
  独立实现复算直方图 CORRECT。
- 每个形式候选因而强制至少一条触碰 \(v_i\) 的真实
  \(2\leftrightarrow1\) 交换。交换后的长 463 原子分别与另外两条
  原子共享 461 个字面位置；没有据此宣称三者共同 461 核、
  complete-deletion 继承或 \(m=3\) 层为空。

## LEMMA-P233-THREE-H8-M3-CORE-FIBRE-RECOVERY：六纤维恢复与九轨归约

- 精确陈述：
  proofs/unique_tail_p233_three_h8_m3_core_fibre_recovery.md。
- 状态：PROVED_REDUCTION；独立全局坐标、bounded subset-sum 与轨道
  审计 CORRECT；GLOBAL_INCOMPLETE。
- 对六个 mixed 目标，\(C\) 中所有表示至多为 singleton，故共同三次
  系数恢复精确普通纤维重数
  \[
  A_{\varepsilon,i}
  \equiv-c_\delta(t_{\varepsilon,i})+\mathbf1_{t=0}\pmod {233}.
  \]
  mixed 高度使同一投影纤维中的位置具有同一完整标签；实际重数界
  给 \(0\le A\le229\)，不同纤维总容量至多 461。
- 任意 bounded 非零关系
  \(0\le k_t\le A_t,\ \sum k_tt=0\) 都真实选出 \(C\) 内投影零和，
  与共同核零和自由矛盾。三纤维 determinant 门及完整 MITM 对全部
  \(228\cdot54,282\) 对给出
  \[
  12,376,296\to974,628\to480\to108.
  \]
- 108 个最终点恰为九个 \(S_3\times\{\pm1\}\) 轨，全部非尾方向；
  38 个 generic 未标点轨缩为 9，114 个 completion-pointed 轨至多
  余 27。没有据此宣称完整四维 lift 存在或 \(m=3\) 已空。

## ROUTE-AUDIT-DGM-MODP2-AXKATZ

- 精确记录：proofs/dgm_modp2_blocking_axkatz_route_audit.md。
- DGM/setpartition 允许重位置，并在固定长度和集的稳定子非平凡时给
  严格陪集容量门；但 complete 近最大无限族可有平凡稳定子。
- 模 \(p^2\) 的 \([X^{-g_i}]\) 系数给
  \(\sum_{k=3p-1}^{4p-3}(-1)^{k-1}d_{i,k}\equiv-pc(T_i)\pmod {p^2}\)，
  不能隔离单独 \(3p\) 层。
- projective blocking 只给 `blocking => c=0`；反向被显式秩四、重数
  有界模型否定。dense 五对角方程的 Ax--Katz、Newton 与
  \(p\)-weight 界均仍只有一层，除非先证明额外行稀疏/仿射退化。

## LEMMA-P233-THREE-H8-M3-OPPOSITE-FIBRE-CLOSURE：九轨横截闭合

- 精确陈述：
  `proofs/unique_tail_p233_three_h8_m3_nine_orbit_short_closure.md`。
- 状态：PROVED_SUBBRANCH；有限证书 SELF-CHECKED；独立审计
  CORRECT；GLOBAL_INCOMPLETE。
- 对 completion-pointed 端点 \(i\) 与 \(r\in\{s,-s\}\)，若
  \(c_\delta(r)\ne0\)，则 signed 非零、mixed 长度门和正负短块的
  交叉相交共同给出
  \[
  A_{-r,i}\le2,\qquad A_{-r,i}=2\Longrightarrow 2t_{-r,i}=r.
  \]
  这是把有限域系数、普通位置重数与字面短块交叉结构接在一起的
  `ordinary opposite-fibre transversal` 引理。
- 九轨的 27 个 pointed 角色中，25 个违反容量门，一个违反容量二的
  共振条件。唯一余项强制两个互不相交的二位置表示，其四个标签和为
  零，矛盾。故 324 个 pointed 形式对由 \(324\to12\to0\)，先前
  108 个未指点形式对全部排除。
- 连同 exceptional 六点的 endpoint-kernel 排除，这闭合固定
  \(p=233\)、三 singleton 长八块、fringe size \(m=3\) 的完整掩码
  分支；不删除其他 \(m=4,\ldots,14\) 掩码，不关闭 180 个 outer
  rows，也不证明一般 \(A_p\)。

## FRONTIER-P233-THREE-H8-M4-EVEN-QUARTIC：余三轨有限接口

- 精确记录：
  `proofs/unique_tail_p233_three_h8_m4_three_orbit_quartic_frontier.md`。
- 状态：EXACT_FINITE_FRONTIER；INCOMPLETE；尚未排除三个轨中的任何
  一个。
- 写 \(\tau=\delta/2\) 与
  \(D_i=\{\tau-z_i,\tau+w_i+z_i\}\)。三个剩余掩码轨分别给
  \(z_2=z_3=z,z_1=-w_3-z\)、\(z_2=z_3=z,z_1\) 自由，以及
  三个 \(z_i\) 全自由；字面位置不因投影标签相等而合并。
- 平移共同核系数得到九维偶四次 \(q\)，原子性穷尽为六个统一尾
  零点与每端点四个 \(Z_i\) 零点，同时 \(q(\tau)=1\)。下一核验器
  先解九列评价矩阵的 rank 分层，再执行 mixed 纤维恢复、普通重数
  上界、去重容量、bounded 零和自由与相反 fringe 纤维横截。

## LEMMA-P233-THREE-H8-M4-O1-FOUR-EXCEPTION：偶四次四例外归约

- 精确陈述：
  `proofs/unique_tail_p233_three_h8_m4_O1_quartic_four_exception_reduction.md`。
- 状态：PROVED_REDUCTION；GLOBAL_INCOMPLETE；不排除 \(O_1\)。
- 八点 fringe 评价矩阵在全部 54,289 个 \(z\) 上的秩
  \(5,6,7,8\) 分布为 \(3,233,237,53,816\)。对每个核空间再穷尽
  54,288 个非零 \(\tau\) 的六尾零点与 \(q(\tau)\ne0\)，完整分母
  \(2,947,241,232\) 恰余四对。
- 四对为
  \(z=(58,174),(60,176)\) 与
  \(\tau=(59,174),(174,59)\) 的笛卡尔积；归一化 \(q\) 唯一，系数
  为 \((74,201,35,201,109,146,189,146,109)\)，并有显式三因子
  分解。
- 现有 mixed 必要门在四状态乘三个 pointed roles 乘 54,282 个方向
  中余 4,576 个；每个 pointed role 至少有 230 个共同对角方向使
  所有恢复纤维为空。下一矛盾必须使用完整生成积实现、逐删点
  completion 见证或新自动短块，不能重复同一纤维容量门。
