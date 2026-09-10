# \(p=233\) 的 Model C/D 稀疏缺陷重标号穷尽

STATUS: **PROVED FINITE EXHAUSTION / INDEPENDENT REVIEW CORRECT /
TWO FROZEN SPARSE-SUPPORT FAMILIES ONLY / GLOBAL INCOMPLETE**

## 1. 精确结论与边界

固定 unique_tail_property_b_doubleton_intersection_attack.py 中的两个
逐位置 \(\rho\)-骨架 Model C、Model D，并进一步把可能非零的
\(q\)-坐标限制在配套程序明列的 sparse-defect 支撑上。则：

\[
\boxed{
\begin{array}{c|c|c}
&\text{完整 mixed 门后}&\text{刚性全短高度门后}\\ \hline
\text{Model C}&9798&0\\
\text{Model D}&0&0
\end{array}}
\tag{1}
\]

这里 Model C 穷尽

\[
233^5(233^2-1)=37\,280\,647\,563\,863\,184
\tag{2}
\]

个原始参数组合；Model D 的原始分母为

\[
233^2(233^2-1)=2\,947\,241\,232.
\tag{3}
\]

结论严格只属于这两个冻结的稀疏 \(q\)-支撑族。本文没有证明任意
mixed-compatible \(q\)-标号都能规范化到该支撑，也没有穷尽固定
\(\rho\)-骨架的全部重标号。

## 2. 固定骨架与一阶降维

程序从真实位置重建两个骨架。每条长补投影序列都具有

\[
g^{p-1}\prod_{i=1}^{p}(h+a_i g),
\qquad \sum_i a_i=1,
\tag{4}
\]

的 Property B 标准形；程序逐条检查长度、重数、标准域归属及线系数
和，所以这些确为长度 \(2p-1\) 的最大投影原子。

Model C 只在七个明列位置保留自由 \(q\)-坐标，另有一个公共补偿
坐标。端点、\(U\) 与 \(W\) 的一阶和给

\[
k+f+t+x_s=1,\qquad
k+e+x_h+x_d=1,\qquad
e+f+t=-4,
\tag{5}
\]

故七变量仿射空间维数为四。Model D 的六位置 sparse support 经同样
的一阶方程降成一个参数 \(c\)。所有未列位置的 \(q\)-坐标冻结为零。

两个 packing 位置统一写成

\[
(-r,\alpha),\qquad(r,3-\alpha),
\qquad r\in C_{233}^2\setminus\{0\},\quad
\alpha\in\mathbb F_{233}.
\tag{6}
\]

## 3. 完整 mixed 目标纤维

对每条长补 \(Q_H\)，把至多四个可能带非零 \(q\) 的缺陷位置记为
\(\Delta_H\)，其余零-\(q\) 部分记为 \(B_H\)。程序按 \(\rho\)-标签
重数作二进制拆分，精确计算

\[
\Sigma_\rho(B_H)
=\{\rho(\sigma(E)):E\subseteq B_H\}.
\tag{7}
\]

因此一个缺陷掩码 \(M\subseteq\Delta_H\) 能出现在目标 \(r\) 的真实
子集里，当且仅当

\[
r-\rho(\sigma(M))\in\Sigma_\rho(B_H).
\tag{8}
\]

式 (8) 是带重数位置子集和的双向等价压缩，不是只保留若干代表。
对给定 packing 坐标 \(\alpha\)，完整 mixed 条件正是对每个可达掩码
同时要求

\[
q(M)+\alpha\in\{1,2,3\}.
\tag{9}
\]

另一 packing 单点由互补对称性同时覆盖。也就是说，程序检查的是
目标纤维中的所有真实子集，不是“存在一个好子集”。

Model C 的全部目标被精确压成 54 个 mask 组（含零目标）。在每组
中，式 (5) 的三条独立行再加四条独立 membership 行张满七变量；
枚举四条右端并回查该组所有 mask，得到八种 survivor 组，共恰好
9798 个 \((r,\alpha,q)\) survivor。Model D 的 21 个 mask 组则对
每个 \(c\) 和每个非零 \(r\) 完整检查；总计

\[
233(233^2-1)=12\,649\,104
\tag{10}
\]

个非零 target--parameter 检查，没有 survivor。

## 4. Model C 的刚性短谱高度矛盾

对 9798 个 Model C mixed survivors，给每个真实位置各设一个独立
高度变量；同一 \((q,\rho)\) 型的位置不预设等高。程序枚举总长度
至多八的全部 \((q,\rho)\)-零计数轮廓。

短窗为

\[
I_1=[2,6],\qquad I_2=[4,7],\qquad I_3=[6,8].
\tag{11}
\]

其中长度二、三只能有实际高度和一，长度八只能有实际高度和三。
对每个刚性轮廓，程序加入一条字面代表方程；对该轮廓中部分选取的
每个同型位置胞，再加入所有位置交换差方程。代表方程与交换差恰好
生成该轮廓全部字面实现的仿射方程空间，因此没有偷偷假设同型等高。

联立 \(U,W,P\)、端点的一阶高度和后，9798 个系统全部产生非零约化
右端，故全部矛盾。因为候选在必要的早期门已归零，长度四至七的柔性
短块、块间不交约束和实际标签重数门在这两个冻结族内成为真空条件；
这种真空性不能外推到 sparse support 之外。

## 5. 可复现性与下一缺口

配套程序为
unique_tail_p233_doubleton_CD_relabel_exhaustion.py，报告为
unique_tail_p233_doubleton_CD_relabel_exhaustion_report.json。

程序 SHA-256 为
fd9b1b08285c0e8be57974536581313c30eb647c0a0a166130b8c9ae12ed60b7，
报告 SHA-256 为
ea4825ecac6939a9617d73ac8451079ff925a6e996a42bd5a51a0d83b3827faa，
内嵌规范证书为
fe5f0982a4fe3f2c2f064a81c1482c602117b296f9b0cea5eb027dfc12f27e02。

尚未处理：

1. sparse support 外的非零 \(q\)-位置；
2. Model C 的公共补偿位置能否总移到指定 clone；
3. 任意 mixed-compatible 标号是否与本文两族 gauge 等价；
4. 因而固定 Model C/D \(\rho\)-骨架的全重标号、其余 incidence
   骨架、720 行、固定切片及全局 \(A_p\) 均仍开放。

下一承重点不是再增加同类计数，而是证明长 Property B 原子上的
mixed-compatible \(q\)-支撑压缩定理，或系统扩大这里的 exact defect
support。
