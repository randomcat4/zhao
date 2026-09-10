# 尾位置锚定及型 (2)/空型推论：全新独立审计

STATUS: **CORRECT**

## 1. 裁决、对象与有限范围

本审计只检查两个三点唯一正核心尾参数

\[
(p,b)=(233,4),\qquad(1399,5)
\]

中，尾位置锚定引理及其对共同 packing 型 (2)、空型、不同零核心
端点交和混合目标的必要推论。审计对象的字节 SHA-256 为：

    1d05d568b7e830030508c27add077145f0d8c986b3b5d22ded8eb1ef6f9f36c4  unique_tail_tail_anchoring.py
    80b094b8b22b2af3c574b6054c9edc755bc8482d3f6e0ceba8be349f99bf2932  unique_tail_tail_anchoring_report.json
    a47995488262e820515dcda0ca7773a2c08dec54170da2a2da49f6e4e65f0421  proofs/unique_tail_tail_anchoring.md

结论始终以冻结上游为前提：

\[
Y=L\mathbin{\dot\cup}P\mathbin{\dot\cup}K,\qquad
|Y|=2p+8,\qquad |L|\le52,
\]

其中 \(K\) 在
\(C_p^3/\langle q\rangle\cong C_p^2\) 中零和自由；每个端点
\(H\) 是长度六至八的实际零核心 \(F_3\) 块，且
\(\varnothing\ne H\cap U\subsetneq U\)、\(|U|=3\)。还使用已经
冻结的环境中实际 \(Z\) 的零和原子性、长补原子完整轴向判据、商零
长度禁窗、完整短谱、唯一正核心 \(F_3\) 尾、真实交引理及端点
\(F_3\) 长补的非零商纤维 \(p-4\) 上界。

本裁决不证明空型、型 (2) 或型 (3) 可实现或不可能，不证明混合
目标碰撞存在，也不完成统一标签 SAT、实际 \(Z\) 原子性、Hasse/
高度层或 \(A_p\)。

审计没有导入作者模块；有限表由定义和冻结输入 JSON 在独立内存代码
中重建。没有修改作者文件或共享总账，也没有提交。

## 2. 冻结依赖与规范证书

作者报告绑定的十四份依赖均与当前字节逐项一致：

| 依赖 | SHA-256 |
|:---|:---|
| proofs/unique_tail_labelled_position_next.md | 60384c64dee88487220f3fd7101a5d3abff1cb576fe3a8b43ec398fdd284ddce |
| verifications/unique_tail_labelled_position_next_independent_review.md | 7cc525664dbbf7eeb23d04b3e061f0c4feac07100c7b6c294ee018ad658f20dd |
| proofs/unique_tail_common_R_next.md | 1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942 |
| verifications/unique_tail_common_R_next_independent_review.md | 35f355d2fe1b3dc7a98e3011e44f0e3cdea17cfdd104c026042081b00c4539d3 |
| proofs/unique_tail_all_packing_short_blocks.md | 7abe228fa70dabd8858a40507b11505bd9cee388aa89fd79cd7a22fb8ec68238 |
| verifications/unique_tail_all_packing_short_blocks_independent_review.md | d22d9380a0dc98c21a691384901a9f826f88b72bab85042beafc053eed8124e3 |
| unique_tail_all_packing_short_blocks_report.json | 4dadb5a6fca18da42ccd95821cc176cd9fae1ce2653ddb2e14406e5e66694ceb |
| proofs/unique_tail_remaining_long_complement_internal_sums.md | 311730df217f79659cf0d934b8c0df2e02489196208b9e699dc31d8b929d10d1 |
| verifications/unique_tail_remaining_long_complement_internal_sums_independent_review.md | 44f191264d4505dbeb4803978d86b3101c8207951e41f7d1edd34d4ba40b204a |
| unique_tail_remaining_long_complement_internal_sums_report.json | b6b3de4097627d26a492f4d1034a1f753bc0d58b83edd92bd100815dd8fc3cae |
| proofs/unique_tail_position_conflict_frontier.md | a30707af2f6ef04da720a8eb3c1e97b1c7c297eecc67cf6879ff1191ff9afa8b |
| verifications/unique_tail_position_conflict_frontier_independent_review.md | 93381c12a56f32469d6dcb0d21c65b22509837484323e2ad1763a81218d771b5 |
| proofs/unique_tail_four_edge_joint_csp.md | 87954d09a00aa74d3d43ce7d784deeff325965e61fca80e900d610371260201f |
| verifications/unique_tail_four_edge_joint_csp_independent_review.md | 3ddd10c87c6f0de70a67e0cd630f3e2b3075200a8356c491eb4ad0f4b5359f3c |

报告去掉 certificate_sha256 字段后，按 UTF-8、键排序和紧凑分隔符
规范序列化，独立复得

    d66287f2f8327519da85b7b5c87913c938e26f9b90fd9e72bfcda22c0e0ced13

与冻结证书相同。两个被读取的上游 JSON 规范证书也分别复算命中：

    b08b3afd002535bc946da3fad778281cd640d8d1c37fda05fca48631e29f2463
    fe15a00d8235419ac0a68144fdb892b0ded20f4e133da0cc6cf9fd1ed009eb9e

## 3. 主界的双侧禁窗与唯一尾步骤

固定端点 \(H\)，取非空实际位置块 \(A\subseteq Q_H\)，满足

\[
\rho(\bar\sigma(A))=0,\qquad
\bar\sigma(A)=e q,\qquad e\in\{1,2,3\},\qquad A\cap U=\varnothing.
\]

因为 \(Q_H\) 含非空的 \(U\setminus H\)，避开 \(U\) 的 \(A\)
必为 \(Q_H\) 的真子集。块

\[
D_A=X_{b-e}\mathbin{\dot\cup}U\mathbin{\dot\cup}A
\]

确为实际商零块；其补块的 \(X\)-位置数为

\[
p-4-(b-e)=p-b+e-4>8.
\]

故补块长度大于八。冻结商零禁窗 \([9,2p+2]\) 先迫使补块长度
至少 \(2p+3\)，从 \(|Z|=3p+4\) 得 \(|D_A|\le p+1\)。若
\(|D_A|\ge9\)，它本身又落在同一禁窗的 \([9,p+1]\) 部分，矛盾。
因此 \(|D_A|\le8\)。

若等号为八，完整短谱把 \(D_A\) 送入 \(F_3\)。但其正
\(X\)-核心数为 \(b-e>0\)，而其 \(Y\)-尾为
\(U\mathbin{\dot\cup}A\supsetneq U\)，会产生不同于冻结唯一尾的
第二个正核心 \(F_3\) 块。因此等号也排除，得到

\[
|D_A|\le7,\qquad
\boxed{|A|\le4-b+e}.
\]

这里两次禁窗的方向、补集长度以及唯一尾的严格包含条件都正确。

对 \(e=1\)，\(b=5\) 给出 \(|A|\le0\)，立即排除；\(b=4\)
只剩一个商标签为 \(q\) 的单点。该单点位于端点长补
\(B_H=Z\setminus H\) 中，而 \(B_H\) 已含 \(X\) 的 \(p-4\)
个 \(q\)-位置，于是 \(v_q(B_H)\ge p-3\)，违反
\(v_q(B_H)\le p-4\)。这是对实际端点 \(F_3\) 长补使用专属
纤维界；证明没有把该界外推到普通商零块。

所以每个 \(Q_H\) 原子分解中的系数一因子都必须含
\(U\setminus H\) 的位置；不同因子位置不交，故

\[
m_1(H)\le |U\setminus H|=3-|H\cap U|\le2.
\]

## 4. 型 (2)：\(V_H\) 零和自由及十八行状态

型 (2) 中 \(|P|=n\in\{1,2\}\)，且

\[
V_H=Q_H\setminus U
=K\mathbin{\dot\cup}((L\setminus H)\setminus U).
\]

若 \(V_H\) 含非空投影零子集，从中取一个投影原子。它避开
\(U\) 且是 \(Q_H\) 的真子集；冻结型 (2) 内部判据迫使其轴系数
为一，与上一节矛盾。因此 \(\rho(V_H)\) 零和自由。

写 \(h=|H|\)、\(r=|H\cap U|\)、\(m=3-r\)。由
\(D(C_p^2)=2p-1\) 得

\[
|V_H|=2p+8-n-h-m\le2p-2,
\]

即单点迹要求 \(h+n\ge8\)，双点迹要求 \(h+n\ge9\)。独立枚举
三条型 (2) 尺寸行、三个 \(h\) 值及两个迹大小，得到十八个状态、
十一个幸存状态：

| \((p,n)\) | \(h=6\) | \(h=7\) | \(h=8\) |
|:---:|:---|:---|:---|
| \((233,1)\) | 两迹均删 | 单点迹强制 \((1,1)\)，双点迹删 | 单点迹原子/分裂，双点迹系数二原子 |
| \((233,2)\) | 单点迹强制 \((1,1)\)，双点迹删 | 单点迹原子/分裂，双点迹系数二原子 | 单点迹原子/分裂，双点迹系数二原子 |
| \((1399,1)\) | 两迹均删 | 单点迹强制 \((1,1)\)，双点迹删 | 单点迹原子/分裂，双点迹系数二原子 |

双点迹只留下一个缺失尾位置，不能锚定 \((1,1)\) 分裂中的两个
系数一因子，故幸存时 \(Q_H\) 必为系数二原子。单点迹且
\(h+n=8\) 时，\(|Q_H|=2p>D(C_p^2)\)，不能为原子，故强制
\((1,1)\) 分裂。其他幸存单点迹只得到“原子或分裂”的必要
二择一。表中“幸存”绝不表示这些状态已经构造或可实现。

## 5. 型 (2) 的不同端点交必非轴

取不同端点 \(H,J\)，反设 \(I=H\cap J\) 投影零，并写

\[
D=J\setminus H,\quad E=H\setminus J,\quad
M=K\mathbin{\dot\cup}(L\setminus(H\cup J)).
\]

实际原子性保证 \(D,E\ne\varnothing\)，共同核界保证
\(M\ne\varnothing\)，且

\[
Q_H=D\mathbin{\dot\cup}M,\qquad
Q_J=E\mathbin{\dot\cup}M.
\]

型 (2) 的完整内部判据分别迫使 \(D,M\) 与 \(E,M\) 成为系数一
投影原子。尾锚定于是要求

\[
(J\cap U)\setminus H\ne\varnothing,\quad
(H\cap U)\setminus J\ne\varnothing,\quad
U\setminus(H\cup J)\ne\varnothing.
\]

在三点尾上，这恰好迫使两个迹为不同单点，因而迹不交；冻结真实交
引理却说迹不交端点的交投影非零，矛盾。所以

\[
\rho(\bar\sigma(H\cap J))\ne0
\]

对型 (2) 的每对不同端点成立。这只关闭轴向交子支，不关闭型 (2)。

## 6. 空型的原子分解、\(V_H\) 与长度强制

空型有 \(Q_H=Y\setminus H\)，其每种投影原子分解的轴系数型只能为

\[
(1,3),\quad(2,2),\quad(1,1,2),\quad(1,1,1,1).
\]

系数一因子数不能超过缺失尾位置数 \(m\le2\)，故
\((1,1,1,1)\) 删除；其余锚定后果为：

| 迹大小 | 仍未被锚定删除的型 | 被迫避开 \(U\) 的因子 |
|---:|:---|:---|
| 1 | \((1,3),(2,2),(1,1,2)\) | \((1,1,2)\) 中的系数二因子 |
| 2 | \((1,3),(2,2)\) | 前者的系数三因子；后者至少一个系数二因子 |

这只是必要分解表，不断言任一行可实现。

仍令

\[
V_H=K\mathbin{\dot\cup}((L\setminus H)\setminus U).
\]

若其中有两个不交投影零原子，它们因避开 \(U\) 而不可能有轴系数
一，所以系数各为二或三。二者之并仍是 \(Q_H\) 的非空真子集，
普通轴系数和为四、五或六；因 \(p\ge233\) 没有模回绕，与完整
端点判据只允许一、二、三矛盾。因此 \(V_H\) 至多含一个不交
投影零原子。

若 \(|V_H|>2p-2\)，Davenport 定理给一个原子 \(A_H\subset V_H\)。
其余部必须零和自由，否则能再取一个与它不交的原子。故

\[
|A_H|\ge |V_H|-(2p-2)=10-h-m.
\]

又因 \(A_H\) 避开 \(U\)，其轴系数只能为二或三，主界给

\[
\boxed{10-h-m\le |A_H|\le7-b}.
\]

而 \(K\) 自身零和自由，所以 \(A_H\) 必须命中
\((L\setminus H)\setminus U\)。式中下界仅在它为正、即
\(|V_H|>2p-2\) 时强制原子；报告对其他行只记录零下界，没有把
不存在的原子当作已实现对象。

## 7. 空型十二行与真实短块传播

对 \(h=6,7,8\) 和 \(r=1,2\) 独立代入上一节，得到：

| \(p\) | \(h\) | \(r=1\)：下界/结论 | \(r=2\)：下界/结论 |
|---:|---:|:---|:---|
| 233 | 6 | 2；系数二或三 | 3；系数三，长度三，生成 \(F_2\) |
| 233 | 7 | 1；系数二或三 | 2；系数二或三 |
| 233 | 8 | 0；不强制原子 | 1；系数二或三 |
| 1399 | 6 | 2；系数三，长度二，生成 \(F_2\) | 3；超过上界二，删除 |
| 1399 | 7 | 1；系数二或三 | 2；系数三，长度二，生成 \(F_2\) |
| 1399 | 8 | 0；不强制原子 | 1；系数二或三 |

因此只有 \((1399,h,r)=(1399,6,2)\) 被本层删除；三个系数三等号行
恰为

\[
(233,6,2),\qquad(1399,6,1),\qquad(1399,7,2).
\]

这些行中 \(|D_{A_H}|=7\)。长度七短谱允许实际和 \(2a\)，而不同
正核心尾排除实际和 \(3a\)。利用

\[
\sigma(U)=3a-bx,\qquad
\sigma(D_{A_H})=3a-3x+\sigma(A_H)=2a
\]

得到

\[
\boxed{\sigma(A_H)=3x-a}.
\]

所以三行确实各产生一个实际长度七 \(F_2\) 块，不只是形式标签。

若 \(p=1399\) 出现避尾的系数二单点 \(z\)，则
\(X_3\mathbin{\dot\cup}U\mathbin{\dot\cup}\{z\}\) 长度七、商和
为零且不是唯一 \(F_3\) 尾，故属于 \(F_2\)。从

\[
3a-2x+\sigma(z)=2a
\]

得到 \(\bar z=2q\)、\(\sigma(z)=2x-a\)。这是一条条件传播，
证明和报告均没有声称该单点必须存在。

## 8. 空型轴向交的迹分类与花瓣

设不同端点的交 \(I=H\cap J\) 轴向。完整上游判据写成

\[
\bar\sigma(I)=-tq,\qquad t\in\{1,2,3\}.
\]

此时

\[
D=J\setminus H,\quad E=H\setminus J,\quad
M=K\mathbin{\dot\cup}(L\setminus(H\cup J))
\]

的轴系数分别为 \(t,t,4-t\)。若 \(t=1\)，\(D,E\) 是系数一
原子，锚定迫使两迹不可比较。迹不交情形已由真实交引理删除，只剩
两个不同双点迹；此时 \(M\) 避开 \(U\)。若 \(M\) 非原子，其
系数三原子分解只能含系数一因子，仍违反锚定；若为原子，则
\(M\supset K\) 的长度远超系数三上界。故 \(t=1\) 不可能。

若迹为两个不同双点，\(t=2\) 时 \(M\) 是避尾系数二零和块，
\(t=3\) 时是避尾系数一零和块；两者都因 \(M\supset K\) 与主界
矛盾。结合迹不交对已非轴，轴向交只能满足

\[
\boxed{t\in\{2,3\},\qquad H\cap U, J\cap U\text{ 可比较}.}
\]

六个非空真尾迹组成二十一个无序可重复迹对。独立分类得到：

| 迹关系 | 对数 | 允许的轴向 \(t\) |
|:---|---:|:---:|
| 相同单点 | 3 | \(2,3\) |
| 相同双点 | 3 | \(2,3\) |
| 单点严格包含于双点 | 6 | \(2,3\) |
| 不同单点 | 3 | 无 |
| 互补的单点—双点 | 3 | 无 |
| 不同双点 | 3 | 无 |

前三类正是十二个可比迹对。这里“允许”只表示尚未被本轮必要条件
排除，不是可实现证书。

在 \(t=2\) 支，两个交换花瓣 \(D,E\) 都必须为系数二原子：若有
\((1,1)\) 分裂，两个系数一因子必须分别锚定两个缺失尾位置，但
可比迹的对应花瓣至多含一个这样的尾位置。对 \(t=3\)，可比迹相同
时两花瓣都避尾，严格嵌套时至少一个花瓣避尾；一个避尾系数三块若
非原子，其分解 \((1,2)\) 或 \((1,1,1)\) 含避尾系数一因子，
不可能。因此至少一个避尾花瓣是系数三原子，并通过主界构造出相应
真实短块。这些仍是条件性的花瓣结构，不声称轴向交存在。

## 9. 混合目标式 (24) 的符号和方向

对型 (2) 或型 (3)，取不同端点 \(H,J\) 与
\(\varnothing\ne S\subsetneq P\)，并假设

\[
\rho(\bar\sigma(S))=\rho(\bar\sigma(H\cap J)).
\]

令 \(I=H\cap J\)、\(T=J\setminus H\)。因
\(\bar\sigma(J)=0\)，有

\[
\bar\sigma(T)=-\bar\sigma(I),\qquad
\rho(\bar\sigma(T))=-\rho(\bar\sigma(S)).
\]

而 \(T\ne\varnothing\)，且共同非空核使
\(T\subsetneq Q_H\)。把冻结完整混合目标条件用于同一实际子集对
\((S,T)\)，方向正确地给出

\[
\bar\sigma(S)+\bar\sigma(T)
=\bar\sigma(S)-\bar\sigma(H\cap J)
\in\{q,2q,3q\}.
\]

所以式 (24) 的减号、端点方向和目标纤维方向均正确。它是碰撞一旦
发生后的必要约束，既不保证碰撞存在，也不把型 (3) 的局部余部
原子性误写成全局可满足性。

## 10. 共同核与无导入有限重建

对十个剩余 packing 尺寸行，令 \(n=|P|\)。分割式直接给

\[
|K|=2p+8-|L|-n\ge2p-44-n.
\]

十行的最小下界是 \(419\)，故本文每次使用 \(K\ne\varnothing\)
都合法。再由投影零和自由序列的 \(|K|\le2p-2\) 得

\[
|L|+n\ge10.
\]

独立程序没有导入作者模块，逐字段复得：

- 十个剩余行及对应共同核界；
- 六个 \((p,e)\) 锚定行；
- 型 (2) 的十八个状态与十一个幸存状态；
- 空型四个整数分拆在两种迹大小上的八行，其中
  \((1,1,1,1)\) 两行均删除；
- 空型十二个端点状态、唯一删除状态和三个精确系数三 \(F_2\) 行；
- 六个非空真迹的二十一个无序可重复迹对，其中十二对可比；
- 八个非空尺寸行的混合目标数 \(0,1,0,1,3,0,0,1\)。

所有重建对象与冻结报告逐字段、逐顺序相同。没有把有限表中标为
survives 或 allowed 的必要状态称为构造、存在或可实现结果。

## 11. 最终裁决

未发现主界量词缺失、双侧禁窗方向错误、唯一尾等号漏删、系数一
锚定不成立、型 (2) 状态漏项、空型分解或长度强制错误、轴向迹对
漏分支、花瓣原子性偷用、混合目标符号反转、共同核为空、依赖漂移、
规范证书错误或作用域越界。

因此，对本文第 1 节的冻结有限范围，作者脚本、报告与证明的独立审计
裁决为 **CORRECT**。这仍只是两个大素数唯一尾分支中的必要结构
归约，不能推出空型、型 (2)、型 (3)、完整唯一尾分支或一般
\(A_p\) 的结论。
