# unique-tail 覆盖骨架的替代 incidence 搜索与统一投影候选

STATUS: **ALL 210 SOURCE-FIXED OBSTRUCTED CLASSES PER FIELD HAVE ALTERNATIVE INCIDENCE WITNESSES /**
**ALL 372 CANONICAL CLASSES PER FIELD COVERED AT THE UNIFIED-PROJECTION LAYER /**
**WEAKER INTERFACE SUPERSEDED FOR CLOSURE BY \(O=L\setminus U\) /**
**NO COMPLETE LABELLED SAT CLAIM /**
**GLOBAL INCOMPLETE**

## 1. 冻结范围

只考虑

\[
(p,\ell,b)=(233,7,4),\qquad (1399,8,5)
\tag{1}
\]

的三点 unique-tail 覆盖接口。规范迹类由一对不同双点迹
\(d_A,d_B\subset U\)、以及其余端点迹的多重集决定；每个有限域
恰有 372 类。

本搜索保留以下条件：

1. \(|U|=3\)，每个端点迹是 \(U\) 的非空真子集；
2. 规范覆盖对 \(A,B\) 满足 \(A\cup B=L\)，且
   \(A\cap B=(d_A\cap d_B)\mathbin{\dot\cup}\{y\}\)；
3. 每个端点含同一个尾外实际位置 \(y\)；第三端点横截覆盖对给出的
   \(A\setminus B,A\cap B,B\setminus A\) 三片；
4. 所有端点长度为 \(\ell\)，并按实际位置互异；
5. 保留 `unique_tail_cover_forbidden_block_generalization.py` 的全部
   单位二余部禁块门与全部稠密形式门。

搜索只改变第三端点在覆盖独占位置池中的实际位置选择。它不改变
\(U\)、覆盖并、端点长度、公共 \(y\) 或迹多重集。

## 2. 有限位置域

令覆盖对的两个独占尾外池分别为

\[
A_o=\{a_0,\ldots,a_{\ell-4}\},\qquad
B_o=\{b_0,\ldots,b_{\ell-4}\}.
\tag{2}
\]

于是

\[
L=U\mathbin{\dot\cup}\{y\}\mathbin{\dot\cup}A_o
 \mathbin{\dot\cup}B_o,
\qquad |L|=2\ell-2,
\tag{3}
\]

即 \(|L|=12\) 或 14。覆盖端点固定为

\[
A=d_A\cup\{y\}\cup A_o,
\qquad
B=d_B\cup\{y\}\cup B_o.
\tag{4}
\]

迹为 \(T\) 的第三端点从 \(A_o\cup B_o\) 中选择恰好

\[
\ell-|T|-1
\tag{5}
\]

个位置，再加上 \(T\cup\{y\}\)。候选只保留横截三片者。同迹端点
按位掩码递增排序，消去仅由同迹端点置换产生的重复。

旧统一构造要求每个第三端点同时漏掉两个私有位置；本搜索取消该
人为一致性要求。因此它确实搜索不同的实际位置 incidence，而不是
重命名旧骨架。

## 3. 保留的禁块门

对每对端点 \(E,F\)，程序逐一检查 26 个非零单位形式

\[
\alpha Q_E+\beta Q_F+\gamma U,
\qquad (\alpha,\beta,\gamma)\in\{-1,0,1\}^3\setminus\{0\}.
\tag{6}
\]

只要形式系数成为实际位置指标，便按其轴系数、中和所需的可用
\(X\)-位置数、冻结禁区 \([9,2p+2]\) 和长度八 unique-tail 门进行
与上游脚本相同的精确判定。

此外，对每个非空端点子族 \(\mathcal S\) 及
\(0\le m\le |\mathcal S|\)，检查

\[
W_{\mathcal S,m}=\sum_{E\in\mathcal S}Q_E-mU.
\tag{7}
\]

若 (7) 是实际位置指标且
\(t=|\mathcal S|+mb\ge4\)，候选被拒绝。这正是既有稠密禁块门。
该性质对部分端点族单调，故可安全用于回溯剪枝。

## 4. 行空间障碍的精确判据

固定一份完整 incidence，令 \(M\) 的行依次为全部端点、\(U\) 和
\(L\) 的位置指标。一个投影坐标 \(r\in\mathbb F_p^L\) 必须满足

\[
Mr=0.
\tag{8}
\]

禁用泛函族 \(\mathcal F\) 包含：

- 每个 \(Q_E=L\setminus E\) 的全部非空真子集指标；
- 每个非覆盖端点对 \(E,F\) 的交 \(E\cap F\) 的指标。

对 \(f\in\mathcal F\)，下述条件等价：

\[
f\in\operatorname{row}_{\mathbb F_p}(M)
\iff
f\cdot r=0\quad\text{对每个 }r\in\ker M.
\tag{9}
\]

因此 (9) 左侧正是 forced-zero obstruction。搜索要求所有
\(f\in\mathcal F\) 都不在行空间。

轴坐标另解仿射系统

\[
M a=(0,\ldots,0,-b,1)^\mathsf T,
\tag{10}
\]

其中端点右端全为零，最后两行分别对应 \(U,L\)。每份保留见证都
通过 (10) 的一致性检查。

最后，从 \(\ker M\) 独立均匀选择两个投影坐标。由 (9)，每个禁用
泛函在两个坐标上同时为零的概率恰为 \(p^{-2}\)。若
\(N=|\mathcal F|<p^2\)，联合界给出同时避开全部禁用泛函的选择。
这只证明该 incidence 支持统一投影层候选，不是完整标签 SAT。

## 5. 全量结果

旧固定构造在每个有限域的 372 类中恰有 210 类出现 forced-zero
obstruction，另 162 类没有。对前 210 类执行替代 incidence 搜索后：

| 有限域 | 目标类 | 找到替代见证 | 未解决 | 总访问节点 | 单类最大节点 |
|---:|---:|---:|---:|---:|---:|
| \(\mathbb F_{233}\) | 210 | 210 | 0 | 2,709 | 83 |
| \(\mathbb F_{1399}\) | 210 | 210 | 0 | 2,520 | 90 |

替代见证的线性系统统计为：

| 有限域 | \((\operatorname{rank}M,\dim\ker M)\) 分布 | \(N\) 范围 | \(p^2\) |
|---:|---|---:|---:|
| \(233\) | \((7,5):6,(8,4):40,(9,3):86,(10,2):78\) | 114--178 | 54,289 |
| \(1399\) | \((7,7):6,(8,6):41,(9,5):82,(10,4):81\) | 238--362 | 1,957,201 |

故每个替代见证都有非零核，且联合界严格成立。与旧构造已有的 162
类合并后，得到精确覆盖：

\[
\boxed{
\text{对 }p=233,1399\text{，每个 372 个规范迹类都至少有一份}
\text{无 forced-zero obstruction 的 incidence 骨架。}}
\tag{11}
\]

这 372 类只称为**统一投影标签候选类**。

在本计算完成后，上层又得到更强的普遍身份
\(O=L\setminus U\)，它已经关闭轴向覆盖对。该新门不否定本文在
较弱统一投影原子接口中列出的 420 份 incidence 见证及其行空间
计算，但意味着这些见证不再承重，也不能称为当前完整 unique-tail
分支的幸存者。

## 6. 证书、复核与边界

搜索报告保存全部 420 份替代实际位置见证、逐见证哈希、节点计数、
秩/零空间维数和禁用泛函计数。独立复核器不导入搜索器或旧统一投影
脚本；它重新枚举 744 个规范有限域类，重新识别每域 210/162 分裂，
并从报告中的位置掩码重算全部门。

独立实现共重检：

- 旧固定骨架的 15,780 个端点对和 525,336 个稠密
  \((\mathcal S,m)\) 行；
- 420 份替代见证的 9,516 个端点对和 339,612 个稠密行；
- 全部 420 个仿射轴系统、有限域行空间、\(Q_E\) 真子集泛函、
  非覆盖交泛函与联合界。

没有产生任何 UNSAT 结论；节点上限没有在任何类触发。因此本结果
不需要、也不声称对未找到见证的搜索域作穷尽否定。

明确未覆盖：实际 \(a\)-高度、\(C_p^4\) 中 \(Z\) 的原子性、共同
\(R=P_1\dot\cup\cdots\dot\cup P_t\) 及其标签、新诱导短块、Hasse
行、长补原子内部子和、完整标签 SAT、packing 型闭合或 \(A_p\)。
尤其未加入后来关闭轴向覆盖对的普遍身份 \(O=L\setminus U\)；因此
本文应保留为较弱接口的替代 incidence 分类与回归证书，而不是当前
闭合证明的一部分。
