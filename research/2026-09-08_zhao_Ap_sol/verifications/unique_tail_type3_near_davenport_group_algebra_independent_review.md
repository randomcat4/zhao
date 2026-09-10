# 型 (3) 近 Davenport 群代数边缘：全新独立审计

STATUS: **CORRECT**

## 1. 对象、隔离方法与裁决边界

本审计只裁决冻结的作者脚本、报告与证明：

- unique_tail_type3_near_davenport_group_algebra.py；
- unique_tail_type3_near_davenport_group_algebra_report.json；
- proofs/unique_tail_type3_near_davenport_group_algebra.md。

读取时的文件 SHA-256 为：

    d1bef7d31f8506710672bbf2e582b6be0b513496ff5daf3d0e564130d7b7c3fa  unique_tail_type3_near_davenport_group_algebra.py
    c7bc5ea0aef9b5d1ed771b8621fa43d6c9d2522a13808b742f628cc3337bbcca  unique_tail_type3_near_davenport_group_algebra_report.json
    705da14a4f7d8de60e2ad71f91b349bce277386090ba7611941d2a176b764b47  proofs/unique_tail_type3_near_davenport_group_algebra.md

审计没有导入或执行作者模块。独立核验器只读取冻结的上游 packing
报告，从定义重新筛出型 (3) 尺寸、枚举端点长度、计算原子长度与
增广理想单项式维数，再逐字段同目标报告比较。群代数恒等式另作手证
核查，并以自行实现的有限群卷积在小素数处作符号回归。

裁决为 **CORRECT**，但只针对证明声明的必要群代数边缘。它没有排除
型 (3)，没有证明九行中任何一行可实现，没有取消共同因子，也没有
关闭唯一尾分支或一般 \(A_p\)。

## 2. 上游依赖及适用域

冻结的 unique_tail_all_packing_short_blocks_report.json 在全部
子族短块与统一 \(q\)-纤维门之后，对 packing 型 (3) 留下

\[
(p,b)=(233,4):\quad s=|P|\in\{1,2,3\},
\]

\[
(p,b)=(1399,5):\quad s=|P|\in\{1,2\}.
\]

型 (3) 恰有一个共同投影零原子 \(P\)，且
\(\bar\sigma(P)=3q\)。这些尺寸只是必要条件，不是可实现性证书。

unique_tail_common_R_next.md 的十四行余部分解表对型 (3) 只允许
单因子余部型 (1)。因此，对每个零核心端点 \(H\)，

\[
Q_H=K\mathbin{\dot\cup}(L\setminus H)
\]

在 \(C_p^2\) 投影中是零和原子。其独审已核对“每一种端点原子
分解”的量词；这里没有把投影原子偷换成 \(C_p^4\) 实际原子。

unique_tail_forced_kernel_nonempty.md 只在三个强制余部原子型
\((3),(1,2),(1,1,1)\) 中证明 \(K\ne\varnothing\)。当前工件固定
的恰是型 (3)，故可以选择同一个实际位置 \(k\in K\) 供所有端点
使用。证明没有把核非空推广到其余 packing 型。

冻结端点族满足 \(h=|H|\in\{6,7,8\}\)。由
\(|Y|=2p+8\) 及逐位置分解
\(Y=L\mathbin{\dot\cup}P\mathbin{\dot\cup}K\)，

\[
|Q_H|=|K|+|L|-h=2p+8-s-h.
\tag{1}
\]

所以 \(Q_H\) 原子性、共同核非空与端点长度三项承重依赖的素数、
packing 型、群别和量词均适用于当前证明。

## 3. 九个端点行的独立重建

定义

\[
\delta=h+s-9.
\tag{2}
\]

由 (1)，

\[
|Q_H|=2p-1-\delta.
\tag{3}
\]

因为 \(Q_H\) 是 \(C_p^2\) 零和原子，且
\(D(C_p^2)=2p-1\)，必有 \(\delta\ge0\)。独立枚举上述五个
\((p,s)\) 选择及 \(h=6,7,8\)，只保留 \(\delta\ge0\)，得到：

| \(p\) | \(b\) | \(s\) | \(h\) | \(\delta\) | \(|Q_H|\) | 删除次数 | 边缘维数 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 233 | 4 | 1 | 8 | 0 | 465 | 464 | 1 |
| 233 | 4 | 2 | 7 | 0 | 465 | 464 | 1 |
| 233 | 4 | 2 | 8 | 1 | 464 | 463 | 3 |
| 233 | 4 | 3 | 6 | 0 | 465 | 464 | 1 |
| 233 | 4 | 3 | 7 | 1 | 464 | 463 | 3 |
| 233 | 4 | 3 | 8 | 2 | 463 | 462 | 6 |
| 1399 | 5 | 1 | 8 | 0 | 2797 | 2796 | 1 |
| 1399 | 5 | 2 | 7 | 0 | 2797 | 2796 | 1 |
| 1399 | 5 | 2 | 8 | 1 | 2796 | 2795 | 3 |

九行逐字段等于目标报告的 endpoint_rows。\(\delta=0,1,2\) 分别
出现五、三、一次；报告没有把其中任何一行解释成实际候选必然存在。

## 4. 截断多项式环与增广幂

取 \(C_p^2\) 的基 \(e_1,e_2\)，在
\(A=\mathbb F_p[C_p^2]\) 中令

\[
u=X^{e_1}-1,\qquad v=X^{e_2}-1.
\]

特征 \(p\) 下 \((1+u)^p=(1+v)^p=1\)，故

\[
A\cong\mathbb F_p[u,v]/(u^p,v^p),\qquad I=(u,v).
\tag{4}
\]

截断单项式 \(u^iv^j\)（\(0\le i,j\le p-1\)）构成一组基，
\(I^m\) 由其中 \(i+j\ge m\) 的单项式张成。因此

\[
I^{2p-1}=0,\qquad
I^{2p-2}=\mathbb F_pu^{p-1}v^{p-1}.
\tag{5}
\]

又因模 \(p\) 二项式系数给出

\[
(X^{e_i}-1)^{p-1}=\sum_{a=0}^{p-1}X^{ae_i},
\]

所以精确地

\[
u^{p-1}v^{p-1}
=\sum_{g\in C_p^2}X^g=:J.
\tag{6}
\]

对目标范围 \(0\le\delta\le2<p\)，直接枚举指数对给出

\[
\begin{aligned}
\dim I^{2p-2-\delta}
&=\#\{(i,j):0\le i,j\le p-1,\ i+j\ge2p-2-\delta\}\\
&=\#\{(\alpha,\beta)\in\mathbb Z_{\ge0}^2:
\alpha+\beta\le\delta\}\\
&=\binom{\delta+2}{2}.
\end{aligned}
\tag{7}
\]

故三层维数确为 \(1,3,6\)。作者的三角数函数虽不显含 \(p\)，但
只在已断言的 \(\delta=0,1,2\) 与两个大素数上调用，适用域正确。

## 5. 删除共同位置后的非零积

对位置序列 \(T\) 定义

\[
\Psi_T=\prod_{z\in T}(1-X^{\rho(\bar z)}).
\]

每个因子属于增广理想 \(I\)。固定已确认存在的共同位置
\(k\in K\subseteq Q_H\)。因为 \(Q_H\) 是原子，
\(Q_H\setminus\{k\}\) 零和自由；否则其中的非空零和位置子集就是
\(Q_H\) 的真零和子集。

展开 \(\Psi_{Q_H\setminus\{k\}}\) 时，群单位元系数为

\[
\sum_{\substack{E\subseteq Q_H\setminus\{k\}\\
\sum_{z\in E}\rho(\bar z)=0}}(-1)^{|E|}.
\]

零和自由性使唯一贡献来自空集，故该系数恰为一，乘积非零。结合
(3)，

\[
0\ne\Psi_{Q_H\setminus\{k\}}
\in I^{|Q_H|-1}=I^{2p-2-\delta}.
\tag{8}
\]

实际位置不交分解同时给出

\[
\Psi_{Q_H\setminus\{k\}}
=\Psi_{K\setminus\{k\}}\Psi_{L\setminus H}.
\tag{9}
\]

这里 \(k\) 与 \(K\) 对所有 \(H\) 相同，没有给不同端点独立选择
抽象核。

## 6. \(\delta=0\) 与 \(\delta=1\) 的归一化

若 \(\delta=0\)，式 (8) 是一维空间
\(I^{2p-2}=\mathbb F_pJ\) 中的非零元。设它为 \(cJ\)。
由 (6)，\(J\) 的单位元系数为一；删除积的单位元系数也为一，
所以 \(c=1\)，即对每个 \(k\in K\)，

\[
\boxed{\Psi_{K\setminus\{k\}}\Psi_{L\setminus H}=J.}
\tag{10}
\]

若 \(\delta=1\)，则 \(|Q_H|=2p-2\) 为偶数。原子性说明
\(Q_H\) 的零和位置子集只有空集和全集，故完整积的单位元系数为

\[
1+(-1)^{2p-2}=2.
\]

同时 \(\Psi_{Q_H}\in I^{2p-2}=\mathbb F_pJ\)。目标素数均为奇数，
所以 \(2\ne0\)；再次以单位元系数归一化，得到

\[
\boxed{\Psi_K\Psi_{L\setminus H}=2J.}
\tag{11}
\]

这一步正确使用完整积，而不是删除积；删除积仍只被断言为三维
边缘中的非零元。

## 7. \(\delta=2\) 停止线与共同因子

当 \(\delta=2\) 时，删除积在六维 \(I^{2p-4}\) 中非零。完整原子
长度 \(2p-3\) 为奇数，故其单位元处空集与全集贡献相消。更重要的
是，完整积只保证属于三维 \(I^{2p-3}\)，不落在一维顶层；不能由
一个单位元系数把它确定成非零的 \(J\) 倍数。作者在此停止，没有
伪造第三个顶端恒等式。

式 (10)、(11) 的共同因子也不能一般地取消。环 (4) 的极大理想
\(I\) 幂零，任一非零 \(I\)-元都是零因子。
\(\Psi_K\in I^{|K|}\)，且由 \(K\) 零和自由知它非零。若
\(|K|>1\)，则 \(\Psi_{K\setminus\{k\}}\) 同样是非零 \(I\)-元，
故仍是零因子；若 \(|K|=1\)，该特定删除因子是单位元一，但这不
产生适用于所有候选的取消定理。作者只保留共同因子，并明确不作
一般取消，逻辑正确。

## 8. 独立小素数符号回归

为排除 \(1-X^g\) 的符号或 \(J\) 的归一化错误，另在
\(C_p^2\) 群基上直接卷积，不使用作者多项式代码。对
\(p=5,7\) 及 \(\delta=0,1,2\)，取显式原子

\[
Q_\delta=
e_1^{\,p-1}e_2^{\,p-1-\delta}
\mathbin{\dot\cup}\{e_1+(\delta+1)e_2\}.
\]

逐个枚举其位置子集，确认唯一非空零和子集是全集。群代数卷积复得：

- \(\delta=0\)：删除一个 \(e_1\) 后，全部 \(p^2\) 个群基元
  系数均为一，即恰为 \(J\)；
- \(\delta=1\)：完整积的全部 \(p^2\) 个群基元系数均为二，
  即恰为 \(2J\)；
- \(\delta=2\)：删除积非零，而完整积的单位元系数为零，并非
  \(2J\)。

这只是一般手证的独立有限回归，不替代目标大素数的证明。

## 9. 依赖哈希、规范证书与报告范围

目标报告列出的七个依赖 SHA-256 均与当前文件字节一致：

    1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942  proofs/unique_tail_common_R_next.md
    35f355d2fe1b3dc7a98e3011e44f0e3cdea17cfdd104c026042081b00c4539d3  verifications/unique_tail_common_R_next_independent_review.md
    edda3f792101e205332f860d7baeaebf0810e3642527c41ad84515264e3e7e64  proofs/unique_tail_forced_kernel_nonempty.md
    8e29620ff316804ab0f095c370587e4d12d85823da33426463c0f2326bc35355  verifications/unique_tail_forced_kernel_nonempty_independent_review.md
    7abe228fa70dabd8858a40507b11505bd9cee388aa89fd79cd7a22fb8ec68238  proofs/unique_tail_all_packing_short_blocks.md
    d22d9380a0dc98c21a691384901a9f826f88b72bab85042beafc053eed8124e3  verifications/unique_tail_all_packing_short_blocks_independent_review.md
    4dadb5a6fca18da42ccd95821cc176cd9fae1ce2653ddb2e14406e5e66694ceb  unique_tail_all_packing_short_blocks_report.json

移除报告顶层 certificate_sha256，再按 UTF-8、键排序与紧凑分隔符
规范序列化，独立得到

    9c9088938792fbb33159ece1725107e372f126079ae8df4b4622611f26ca4037

与报告所载证书相同。九行、delta_counts、维数映射、两个 \(J\)
恒等式、共享因子和状态字段也都与证明一致。报告明确列出未证明：
共同因子可取消、带符号系数是非负计数、端点行可实现、型 (3) 为空、
唯一尾分支为空或 \(A_p\)。

## 10. 最终裁决

**已证明：**在两个目标素数、共同 packing 型 (3)、全部冻结零核心
端点及同一个非空共同核的范围内，九个可能的
\((p,s,h,\delta)\) 行穷尽；删除共同 \(k\) 后的乘积分别落在维数
\(1,3,6\) 的增广边缘且非零；\(\delta=0\) 给出精确 \(J\) 恒等式，
\(\delta=1\) 的完整原子积给出精确 \(2J\) 恒等式。

**没有证明：**共同因子可一般取消；带符号系数是非负表示数；九行
中任一行可实现或不可实现；型 (3) 为空；唯一尾分支为空；或
\(A_p\) 成立。

作者证明、脚本和报告的量词、依赖与停止线一致。最终裁决为
**CORRECT**；全局状态保持 **INCOMPLETE**。
