# 型 (3) 全端点对共同因子边缘：全新独立审计

STATUS: **CORRECT**

## 1. 裁决对象、方法与边界

本审计只裁决以下三份冻结作者工件：

- unique_tail_type3_shared_endpoint_fringe.py；
- unique_tail_type3_shared_endpoint_fringe_report.json；
- proofs/unique_tail_type3_shared_endpoint_fringe.md。

读取时的 SHA-256 为：

    761612436270869c9aa289af786fa6e35a15e1433586ada9799fe2b376a7216d  unique_tail_type3_shared_endpoint_fringe.py
    59aeb39447d8a33843499086e7d486e6fbdf7935fc12855f0830d555ebc45d6c  unique_tail_type3_shared_endpoint_fringe_report.json
    a0168e71cc4ea7a5fe17f4343de61827eb50d1c9459a33b65d6a90e85beeffa4  proofs/unique_tail_type3_shared_endpoint_fringe.md

三者与委托给出的冻结哈希完全一致。审计没有导入作者模块，也没有
执行会重写冻结报告的作者主程序。独立核验器从允许的
\((p,|P|,|H|)\) 行、位置集合恒等式与增广理想三层状态重新生成
全部端点对及花瓣行，再与目标 JSON 逐字段比较。群代数符号另以自行
实现的有限群卷积作小素数回归。

最终裁决为 **CORRECT**。该裁决只认证同一型 (3) 实例内两个不同
实际端点的共同因子必要关系；不认证任何条件长度类必然出现，不认证
任一行可实现，更不排除型 (3) 或证明全局 \(A_p\)。

## 2. 上游假设与逐位置分解

上游已审定的型 (3) 输入给出同一个实际位置块 \(P\)、同一个
\(K,L\)，并且对每个端点 \(H\in\mathcal A\)

\[
Q_H=K\mathbin{\dot\cup}(L\setminus H)
\]

是 \(C_p^2\) 中按实际位置计数的零和原子。共同核定理给出
\(K\ne\varnothing\)，所以可先固定同一个 \(k\in K\)，再同时用于
全部端点。端点族中的每个端点都含同一实际位置 \(y\)，故任意不同
\(H,J\) 满足 \(|H\cap J|\ge1\)。

令

\[
A=H\setminus J,\qquad B=J\setminus H,\qquad
C=L\setminus(H\cup J).
\]

若 \(A=\varnothing\)，则 \(H\subsetneq J\)，而所有端点实际和均为
\(3a\)，所以非空差集 \(J\setminus H\) 的实际和为零，成为实际原子
\(Z\) 的真零和位置子集；矛盾。交换 \(H,J\) 同理排除
\(B=\varnothing\)。因此这里确有

\[
1\le |H\cap J|\le\min(|H|,|J|)-1.
\]

逐位置而非仅按和值，有

\[
L\setminus H=B\mathbin{\dot\cup}C,\qquad
L\setminus J=A\mathbin{\dot\cup}C.
\]

于是，写

\[
D=\Psi_K\Psi_C,\qquad D_k=\Psi_{K\setminus\{k\}}\Psi_C,
\]

便严格得到

\[
\begin{array}{ll}
\Psi_{Q_H}=D\Psi_B,&\Psi_{Q_J}=D\Psi_A,\\
\Psi_{Q_H\setminus\{k\}}=D_k\Psi_B,&
\Psi_{Q_J\setminus\{k\}}=D_k\Psi_A.
\end{array}
\]

方向没有颠倒：\(A\) 是属于 \(H\) 的独占花瓣，但它进入
\(L\setminus J\) 和 \(Q_J\)；\(B\) 是属于 \(J\) 的独占花瓣，
但它进入 \(L\setminus H\) 和 \(Q_H\)。

## 3. 三种亏损的完整积与共同删点积

置

\[
n_H=|Q_H|=2p-1-\delta_H,\qquad \delta_H\in\{0,1,2\}.
\]

每个因子 \(1-X^g\) 属于增广理想 \(I\)，故完整积属于
\(I^{n_H}\)，删点积属于 \(I^{n_H-1}\)。原子性说明完整原子的
零和位置子集只有空集与全集；删去 \(k\) 后为零和自由序列，所以
删点积的单位元系数恰为一，特别地它非零。

结合

\[
I^{2p-1}=0,\qquad I^{2p-2}=\mathbb F_pJ_G,
\]

以及相应三层维数 \(1,3,6\)，逐行得到：

| \(\delta\) | 完整积 | 共同 \(k\) 删点积 |
|---:|---|---|
| 0 | 位于 \(I^{2p-1}\)，故为零 | 位于一维 \(I^{2p-2}\)，单位元系数一，故恰为 \(J_G\) |
| 1 | 位于一维 \(I^{2p-2}\)，单位元系数 \(1+(-1)^{2p-2}=2\)，故恰为 \(2J_G\) | 三维 \(I^{2p-3}\) 中单位元系数一的非零元 |
| 2 | 只知位于 \(I^{2p-3}\)，且单位元系数 \(1+(-1)^{2p-3}=0\) | 六维 \(I^{2p-4}\) 中单位元系数一的非零元 |

特别地，\(\delta=2\) 的完整积没有被断言为非零。零元本身也满足
“属于 \(I^{2p-3}\) 且单位元系数为零”；作者证明第 84--85 行及
报告的状态字符串都保留了这一点，没有把它误写成非零 \(J_G\) 倍数。

作为符号回归，审计在 \(p=5,7\) 上自行取

\[
Q_\delta=e_1^{p-1}e_2^{p-1-\delta}
\mathbin{\dot\cup}\{e_1+(\delta+1)e_2\},
\]

直接枚举位置子集并在群基上卷积。六个实例均确认为原子；分别复得：
\(\delta=0\) 的完整积为零且删点积为 \(J_G\)；
\(\delta=1\) 的完整积为 \(2J_G\)；
\(\delta=2\) 的完整积单位元系数为零，而删点积非零且单位元系数为
一。该有限回归只检查符号和归一化，一般结论仍由上述增广理想手证
给出。

## 4. 六种端点对关系与 0--1 分离式

按 \(h=|H|\le j=|J|\) 排序。同一实例的 \(|P|\) 固定，故

\[
\delta_J-\delta_H=j-h.
\]

若 \(c=|H\cap J|\)，则

\[
|A|=h-c,\qquad |B|=j-c,\qquad
|B|-|A|=\delta_J-\delta_H.
\]

把第 3 节的状态代入第 2 节的正确花瓣方向，六个非降亏损对恰给出：

\[
\begin{array}{c|l}
(\delta_H,\delta_J)&\text{共同因子后果}\\ \hline
(0,0)&D_k\Psi_A=D_k\Psi_B=J_G,\ \text{故 }D_k(\Psi_A-\Psi_B)=0,\\
(0,1)&D\Psi_B=0,\ D\Psi_A=2J_G,\ D_k\Psi_B=J_G,\\
(0,2)&D\Psi_B=0,\ D_k\Psi_B=J_G,\ A\text{ 侧只有亏损二状态},\\
(1,1)&D\Psi_A=D\Psi_B=2J_G,\ \text{故 }D(\Psi_A-\Psi_B)=0,\\
(1,2)&D\Psi_B=2J_G,\ A\text{ 侧只有亏损二状态},\\
(2,2)&D_k\Psi_A,D_k\Psi_B\text{ 分别是共享 }D_k\text{ 的六维非零边缘元}.
\end{array}
\]

因此混合 \((0,1)\) 的符号和方向准确：较长端点 \(J\) 的独占花瓣
是 \(B\)，但 \(D\Psi_B\) 是较短端点 \(H\) 的完整补原子积，故为
零；较短端点的独占花瓣 \(A\) 进入 \(Q_J\)，故
\(D\Psi_A=2J_G\)。这里不存在正负号反转。

最后一行没有把两个六维非零元误判为相等；前三层所在的群代数含
零因子，作者也从未取消 \(D\) 或 \(D_k\)。同亏损 0、1 行得到的
只是乘积差被公共因子湮灭，不能推出 \(\Psi_A=\Psi_B\)。

## 5. 14 个条件长度对与 86 个花瓣行

独立枚举使用的允许端点长度只有：

\[
\begin{array}{c|c|c}
p&|P|&|H|\\ \hline
233&1&8\\
233&2&7,8\\
233&3&6,7,8\\
1399&1&8\\
1399&2&7,8.
\end{array}
\]

同一实例必须固定 \(p,|P|\)，所以每一行长度集只取有重复二组合。
各组的“长度对数／花瓣行数”分别为

\[
(1,7),\quad(3,19),\quad(6,34),\quad(1,7),\quad(3,19).
\]

总数因而为

\[
1+3+6+1+3=14,\qquad
7+19+34+7+19=86.
\]

对每个 \(h\le j\)，公共位置给 \(c\ge1\)，两个独占花瓣非空给
\(c\le h-1\)。逐一取 \(c=1,\ldots,h-1\) 后，花瓣大小恰为
\((h-c,j-c)\)，且其差恒为 \(j-h\)。按亏损对汇总的 14 行计数
精确为

\[
\begin{array}{c|rrrrrr}
(\delta_H,\delta_J)&(0,0)&(0,1)&(0,2)&(1,1)&(1,2)&(2,2)\\ \hline
\text{行数}&5&3&1&3&1&1.
\end{array}
\]

这里 86 行只是所有上述必要字面尺寸，并非 86 个实现。证明和报告
都将 14 行明确称为条件长度对，也明确声明不保证任一长度类在一个
实例中出现。

## 6. 报告、依赖哈希与规范证书

不导入作者代码的独立重建得到：

    independent_pair_rows_equal = true
    summary_equal = true
    conditional_length_pair_row_count = 14
    literal_petal_size_row_count = 86
    delta_pair_counts = 5,3,1,3,1,1

报告列出的五个依赖哈希均与当前字节一致：

    c7bc5ea0aef9b5d1ed771b8621fa43d6c9d2522a13808b742f628cc3337bbcca  unique_tail_type3_near_davenport_group_algebra_report.json
    705da14a4f7d8de60e2ad71f91b349bce277386090ba7611941d2a176b764b47  proofs/unique_tail_type3_near_davenport_group_algebra.md
    9d3d9b45234b91b9190b579155c28071133d020dfe71dddb71261cd339f0afb4  verifications/unique_tail_type3_near_davenport_group_algebra_independent_review.md
    8b65afeb55a419abe980225d5c19024b80106157f0657055f13d84ccf40aac6c  proofs/unique_tail_forced_common_atoms_attack.md
    cb4d9794b3f7277609e331a7cd674dc6d347e81c0eff1e6885e75924d78fd240  verifications/unique_tail_seven_type_fresh_independent_review.md

移除报告顶层 certificate_sha256 后，按 UTF-8、键排序、紧凑分隔符
规范序列化，独立得到

    d6ccad1a67221224d75c96766d992c9b456b7ad05c409cbe8482afbe5579560a

与报告所载规范证书完全一致。

## 7. 最终结论

**已证明：**在冻结型 (3) 假设下，同一实例的每一对不同实际端点
都通过同一实际位置因子 \(D,D_k\) 耦合；三种亏损的完整积和共同
删点积状态准确；六种非降亏损对关系、14 个条件长度对、86 个字面
花瓣尺寸行以及 \(5,3,1,3,1,1\) 计数均完整且可独立复现。

**未证明：**任何公共因子可取消；任何条件长度类或端点对必然出现；
任何表行可实现；型 (3) 为空；唯一尾分支关闭；或 \(A_p\) 成立。

作者证明、脚本与报告在量词、花瓣方向、符号、依赖和停止线上一致。
最终裁决为 **CORRECT**；全局状态保持 **INCOMPLETE**。
