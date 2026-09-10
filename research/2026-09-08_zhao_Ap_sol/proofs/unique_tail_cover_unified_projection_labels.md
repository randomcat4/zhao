# 覆盖 incidence 的统一投影标签层：210 个固定骨架排除与 162 个严格幸存

STATUS: **FIXED_SKELETON_PROJECTION_CLASSIFICATION /
TRACE_CLASSES_AND_FULL_LABELLED_INTERFACE_OPEN / GLOBAL_INCOMPLETE**

## 1. 精确范围

沿用 `proofs/unique_tail_cover_forbidden_block_generalization.md` 的两个
素数

\[
(p,b)=(233,4),(1399,5),
\tag{1}
\]

以及每个素数 372 个规范覆盖迹类。对每个迹类，只研究上游构造器
实际选出的**一个固定位置骨架**：位置全集为 \(L\)，三个尾位置组成
\(U\)，端点为 \(E_1,\ldots,E_s\)，覆盖对规范为 \(E_1,E_2\)，并令

\[
Q_i=L\setminus E_i.
\tag{2}
\]

本文把全部位置放进同一个 \(C_p^3\) 商标签系统，并同时恢复：

1. 每个 \(Q_i\) 的每个非空真内部子集和；
2. 每个非覆盖端点对的真实交；
3. 所有端点、\(U\) 与 \(L\) 共享的线性和值方程。

本文没有枚举同一迹类的其他 incidence，也没有加入实际 \(a\)-高度、
共同 \(R\) 的 \(P_i\) 分解、新诱导短块、Hasse 行或新 \(F_3\) 的长补
原子。因此下文 210 个排除只排除 210 个**固定骨架**，不排除对应
迹类；162 个幸存也不是完整标号候选。

## 2. 一套共同线性系统

把 \(L\) 的实际位置依次编号为 \(1,\ldots,n\)。令 \(M\) 的行是全部
端点示性向量，再加 \(U\) 与 \(L\) 的示性向量。每一个非轴投影坐标
\(v\in\mathbb F_p^n\) 都必须满足

\[
Mv=0.
\tag{3}
\]

轴坐标 \(z\) 则满足同一个左矩阵的仿射系统

\[
M z=(0,\ldots,0,-b,1)^{\mathsf T}.
\tag{4}
\]

式 (3)--(4) 精确表达

\[
\bar\sigma(E_i)=0,qquad
\bar\sigma(U)=-bq,qquad
\bar\sigma(L)=q,qquad
\bar\sigma(Q_i)=q.
\tag{5}
\]

程序在两个素数的全部 372 个固定骨架上逐一行化 (4)，全部相容。

## 3. 行空间给出精确的强迫零判据

对实际位置子集 \(T\subseteq L\)，其示性行记为 \(1_T\)。由线性代数，

\[
\boxed{
\sum_{x\in T}v_x=0\quad\text{对每个 }v\in\ker M
\iff 1_T\in\operatorname{rowspan}M.}
\tag{6}
\]

需要禁止的实际子集一次性取为

\[
\mathcal B=
\{\varnothing\ne T\subsetneq Q_i:\ 1\le i\le s\}
\cup
\{E_i\cap E_j:E_i\cup E_j\ne L\}.
\tag{7}
\]

第一族正是所有长余部原子 \(Q_i\) 的全部内部真子集；第二族是交换门
要求非轴的全部非覆盖端点交。覆盖交没有放入禁止族，因为

\[
1_{E_i\cap E_j}=1_{E_i}+1_{E_j}-1_L
\quad(E_i\cup E_j=L)
\tag{8}
\]

已经由 (3) 强迫为轴向，这与覆盖例外一致。

若某个 \(T\in\mathcal B\) 满足 (6)，任意统一投影标签都使它投影和
为零：第一种情形破坏某个 \(Q_i\) 的原子性，第二种情形破坏交换门。
这不是独立给不同 \(T\) 配值，而是在同一个 \(M\) 上的精确必要条件。

## 4. 联合避超平面同时实现全部内部子集和

反过来，假设没有 \(T\in\mathcal B\) 的示性行落入
\(\operatorname{rowspan}M\)。从 \(K:=\ker M\) 独立均匀选择
\(r,s\in K\)。对每个固定 \(T\in\mathcal B\)，式 (6) 的否定说明
线性泛函

\[
v\longmapsto\sum_{x\in T}v_x
\tag{9}
\]

在 \(K\) 上非零，所以

\[
\Pr\left(
\sum_{x\in T}r_x=sum_{x\in T}s_x=0
\right)=p^{-2}.
\tag{10}
\]

记 \(N=|\mathcal B|\)。只要 \(N<p^2\)，并集界给出

\[
\Pr(\text{某个 }T\in\mathcal B\text{ 同时两坐标为零})
\le \frac{N}{p^2}<1.
\tag{11}
\]

故存在同一对 \((r,s)\) 同时避开全部坏子集。再取 (4) 的任一解
\(z\)，给位置 \(x\) 赋统一商标签

\[
g_x=(z_x,r_x,s_x)\in C_p^3.
\tag{12}
\]

于是每个 \(Q_i\) 的投影总和为零，而每个非空真子集投影和非零，
所以全部 \(Q_i\) 同时为 \(C_p^2\) 投影原子；每个非覆盖端点交也
同时非轴。式 (11) 处理的是同一标签下的所有内部子集和，而不是逐块
独立的放宽变量。

## 5. 全量分类

配套程序
`unique_tail_cover_unified_projection_labels.py` 独立重建 744 个
“素数—规范迹类”固定骨架，并在各素数上得到：

\[
\begin{array}{c|r|r}
&p=233&p=1399\\
\hline
\text{固定骨架总数}&372&372\\
\text{轴仿射系统相容}&372&372\\
\text{存在强迫零坏泛函}&210&210\\
\text{通过且由并集界实现统一投影标签}&162&162\\
\max N&153&307\\
\min\dim\ker M&2&4
\end{array}
\tag{13}
\]

每个被排除的固定骨架既有被强迫为零的 \(Q_i\) 真子集，也有被强迫
为零的非覆盖端点交。对 162 个幸存骨架，分别有

\[
153<233^2,qquad 307<1399^2,
\tag{14}
\]

所以 (11) 严格成立。程序还从零空间基底作确定性赋值搜索，并把
162 个幸存骨架的每个实际位置三坐标标签全部写入报告；两素数上
第零次确定性尝试已经全部命中。逐骨架记录还保留方程秩、零空间维数、
三类禁止泛函数与行空间命中数。报告的规范证书 SHA-256 为

\[
\mathtt{52a6c801db860ee9b83fa50a4625e410e3c22f41f1b3f79eca6e216c1b8b21e0}.
\tag{15}
\]

## 6. 结论与下一缺口

**PROVED FOR FIXED SKELETONS：**上游每个规范迹类所选固定实际位置
骨架中，210/372 在统一投影方程上已经精确矛盾；其余 162/372 不仅
通过计数门，而且确实存在一套共同 \(C_p^3\) 商标签，使全部 \(Q_i\)
投影原子且全部非覆盖端点交非轴。

**NOT PROVED FOR TRACE CLASSES：**210 个迹类可能存在另一套实际位置
incidence 避开行空间障碍；162 个统一投影幸存也尚未加入所有其他
商零子集。故没有一个规范迹类或 packing 型在本文中关闭。

**NEXT EXACT LAYER：**对 162 个固定幸存骨架和 210 类的替代 incidence，
必须把 (12) 与同一个实际 \(R=P_1\dot\cup\cdots\dot\cup P_t\) 连接，
枚举由轴坐标和投影标签自动诱导的全部短零和块，并对每个新 \(F_3\)
长补原子检查全部内部子集和；随后才进入实际 \(a\)-高度、Hasse 行和
\(Z\) 的 \(C_p^4\) 原子性。全局状态继续为 **INCOMPLETE**。
