# 型 (3) 全端点对的共同因子边缘关系

STATUS: **PROVED_REDUCTION / PENDING_INDEPENDENT_REVIEW / GLOBAL_INCOMPLETE**

## 1. 从单端点边缘进入实际端点对

沿用型 (3) 的已审计记号。共同位置块 \(P\) 满足
\(\bar\sigma(P)=3q\)，而每个零核心端点 \(H\in\mathcal A\) 都给出

\[
Q_H=K\mathbin{\dot\cup}(L\setminus H),\qquad
|Q_H|=2p-1-\delta_H,\qquad \delta_H\in\{0,1,2\},
\tag{1}
\]

其中 \(Q_H\) 是 \(C_p^2\) 的零和原子，且共同核 \(K\ne\varnothing\)。
上一轮只把各个 \(Q_H\) 分别放入增广理想顶端三层。本文固定同一实例
中的两个不同实际端点 \(H,J\)，保留它们共享的每一个位置。

令

\[
A=H\setminus J,\qquad B=J\setminus H,\qquad
C=L\setminus(H\cup J).
\tag{2}
\]

全部端点含共同位置 \(y\)，故 \(|H\cap J|\ge1\)。另一方面，\(A,B\)
都非空：若例如 \(A=\varnothing\)，则 \(H\subsetneq J\)，而
\(\sigma(J\setminus H)=\sigma(J)-\sigma(H)=0\) 给出 \(Z\) 的非空
实际零和真子集，违反实际原子性。

对位置序列 \(T\)，写

\[
\Psi_T=\prod_{z\in T}(1-X^{\rho(\bar z)})
\in\mathbb F_p[C_p^2].
\tag{3}
\]

固定任意 \(k\in K\)，并定义两个真正共享的实际位置因子

\[
D=\Psi_K\Psi_C,
\qquad
D_k=\Psi_{K\setminus\{k\}}\Psi_C.
\tag{4}
\]

于是四个端点积不是独立对象，而严格分解为

\[
\begin{array}{ll}
\Psi_{Q_H}=D\Psi_B,&
\Psi_{Q_J}=D\Psi_A,\\
\Psi_{Q_H\setminus\{k\}}=D_k\Psi_B,&
\Psi_{Q_J\setminus\{k\}}=D_k\Psi_A.
\end{array}
\tag{5}
\]

式 (5) 是逐位置恒等式；展开后覆盖两个长补原子的全部内部子集带符号
和，并强制它们通过同一 \(K\) 与同一局部公共外部 \(C\) 耦合。

## 2. 三种长度层的完整积与删点积

令 \(J_G=\sum_{g\in C_p^2}X^g\)。已审计的增广理想结构给出：

\[
\begin{array}{c|c|c}
\delta&\Psi_{Q_H}&\Psi_{Q_H\setminus\{k\}}\\ \hline
0&0&J_G\\
1&2J_G&
\text{三维 }I^{2p-3}\text{ 边缘中的非零元，单位元系数为 }1\\
2&
I^{2p-3}\text{ 中单位元系数为 }0\text{ 的元}&
\text{六维 }I^{2p-4}\text{ 边缘中的非零元，单位元系数为 }1.
\end{array}
\tag{6}
\]

第一行完整积为零是因为 \(I^{2p-1}=0\)。第二行完整积为 \(2J_G\)，
因为长度 \(2p-2\) 为偶数，而原子的零和子集只有空集和全集。第三行
长度 \(2p-3\) 为奇数，空集与全集在单位元系数处相消；这不保证整个
积非零。删点后原子变成零和自由序列，所以单位元系数只有空集贡献，
恰为一。

## 3. 六种端点对关系

先按 \(h=|H|\le |J|\) 排序。由
\(\delta_H=h+|P|-9\)，有

\[
\delta_J-\delta_H=|J|-|H|.
\tag{7}
\]

若 \(c=|H\cap J|\)，则

\[
|A|=h-c,\qquad |B|=|J|-c,\qquad
|B|-|A|=\delta_J-\delta_H,
\tag{8}
\]

且 \(1\le c\le h-1\)。把 (6) 代入同一个分解 (5)，得到全部六种
可能的亏损对：

\[
\begin{array}{c|l}
(\delta_H,\delta_J)&\text{共同因子关系}\\ \hline
(0,0)&D_k(\Psi_A-\Psi_B)=0,\\
(0,1)&D\Psi_B=0,\quad D\Psi_A=2J_G,\quad D_k\Psi_B=J_G,\\
(0,2)&D\Psi_B=0,\quad D_k\Psi_B=J_G,
          \quad A\text{ 侧留在亏损二边缘},\\
(1,1)&D(\Psi_A-\Psi_B)=0,\\
(1,2)&D\Psi_B=2J_G,
          \quad A\text{ 侧留在亏损二边缘},\\
(2,2)&\text{只强制两个共享 }D_k\text{ 的六维非零删点边缘}.
\end{array}
\tag{9}
\]

特别地，混合 \((0,1)\) 对给出一个真正的共同因子分离式：同一个
\(D\) 把较长端点的花瓣积送到零，却把另一花瓣积送到 \(2J_G\)。
这比“两个端点各自满足某个近极值原子条件”严格保留了更多信息。

## 4. 完整有限表

当前允许的 \((p,|P|,|H|)\) 九行产生 14 个条件长度对。亏损对的
出现次数为

\[
\begin{array}{c|rrrrrr}
(\delta_H,\delta_J)&(0,0)&(0,1)&(0,2)&(1,1)&(1,2)&(2,2)\\ \hline
\text{行数}&5&3&1&3&1&1.
\end{array}
\tag{10}
\]

对每个长度对再穷尽式 (8) 的实际交大小，共有 86 个字面花瓣尺寸行。
这里“条件长度对”只表示：若同一实例出现相应的两个不同端点，则
(8)--(9) 必须成立；并不声称每种长度在同一实例中都出现。

配套脚本 unique_tail_type3_shared_endpoint_fringe.py 从上一轮冻结报告
重建九个端点行，枚举式 (7)--(10)，并把每一行的 \(D,D_k,A,B\)
分解及边缘状态写入机器可读报告。

## 5. 边界与下一接口

- 群代数含零因子；(9) 中任何 \(D\) 或 \(D_k\) 都不能取消。
- 带符号系数不能解释为非负子集计数。
- 本文没有证明任一条件端点对必须出现，也没有关闭型 (3)。
- 下一轮统一位置求解器不应再为每个 \(Q_H\) 创建独立的“原子”布尔
  标志；它应直接复用 \(K,L,H,J\) 的位置标签，生成 \(A,B,C\)，并
  同时核验 (5)、全部自动短块、实际交、Hasse 行和 \(Z\) 原子性。
- 全局 \(A_p\) 仍为 **INCOMPLETE**。
