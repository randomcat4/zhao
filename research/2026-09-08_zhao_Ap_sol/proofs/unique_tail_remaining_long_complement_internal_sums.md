# 三个剩余型的全长补内部子集和压缩

STATUS: **PROVED_REDUCTION / PENDING_INDEPENDENT_REVIEW / GLOBAL_INCOMPLETE**

## 1. 范围与结论

在 \((p,b)=(233,4),(1399,5)\) 的唯一尾分支，七种共同 packing
已经压缩到

\[
\varnothing,\qquad(2),\qquad(3).
\tag{1}
\]

本文处理两个非空型。固定共同的实际位置原子 \(P\subset R\)，写

\[
\rho(\bar\sigma(P))=0,\qquad
\bar\sigma(P)=dq,\qquad d\in\{2,3\}.
\tag{2}
\]

对每个实际零核心端点 \(H\)，令

\[
Q_H=K\mathbin{\dot\cup}(L\setminus H),\qquad
W_H=P\mathbin{\dot\cup}Q_H.
\tag{3}
\]

相应的 \(F_3\) 长补原子为

\[
B_H=q^{p-4}W_H,
\qquad \bar\sigma(W_H)=4q.
\tag{4}
\]

把 (4) 的**每个内部位置子集和**同时施加在 \(S\) 与
\(P\dot\cup S\) 上，得到：

\[
\boxed{
\begin{array}{c|c}
d&Q_H\text{ 的全部非空真 }\rho\text{-零子集}\\ \hline
3&\text{不存在；故 }\rho(Q_H)\text{ 是原子},\\
2&\text{轴系数都恰为 }1，\text{且子集及其补集都是原子}.
\end{array}}
\tag{5}
\]

在 \(d=2\) 行，这些原子因子的长度都至少为二。再加上
\(P\) 的真子集与 \(Q_H\) 的目标纤维条件，就得到长补全部内部
子集和的充要压缩；没有截断到短长度，也没有把不同端点复制开。

## 2. 同一内部子集的系数平移

由已认证的完整轴向判据，(4) 是商原子当且仅当每个非空真位置子集
\(E\subsetneq W_H\) 都满足

\[
\rho(\bar\sigma(E))=0
\quad\Longrightarrow\quad
\bar\sigma(E)\in\{q,2q,3q\}.
\tag{6}
\]

现在任取

\[
\varnothing\ne S\subsetneq Q_H,
\qquad \rho(\bar\sigma(S))=0,
\qquad \bar\sigma(S)=cq.
\tag{7}
\]

因为 \(P\ne\varnothing\)，\(S\) 是 \(W_H\) 的非空真子集；
而因 \(S\ne Q_H\)，\(P\dot\cup S\) 也是非空真子集。两者的
\(\rho\)-和都为零。把 (6) 同时用于这两个**实际位置子集**，得到

\[
c\in\{1,2,3\},\qquad c+d\pmod p\in\{1,2,3\}.
\tag{8}
\]

这里 \(p\ge233\)，且 \(3+d\le6<p\)，没有模回绕。因此

\[
d=3\Longrightarrow\text{无解},
\qquad
d=2\Longrightarrow c=1.
\tag{9}
\]

又 \(\rho(Q_H)=0\)。所以 \(d=3\) 时 (9) 正是
\(Q_H\) 没有非空真零和子集，即 \(\rho(Q_H)\) 为原子。

## 3. 型 \((2)\) 中每个真零子集自身也是原子

现在令 \(d=2\)，并取 (7) 的任意 \(S\)。式 (9) 给

\[
\bar\sigma(S)=q,
\qquad
\bar\sigma(Q_H\setminus S)=q.
\tag{10}
\]

若 \(S\) 不是 \(C_p^2\) 中的原子，可取
\(\varnothing\ne T\subsetneq S\) 使 \(\rho(\bar\sigma(T))=0\)。
式 (9) 同时用于 \(T\) 与非空真子集 \(S\setminus T\)，迫使二者
轴系数都为一；但它们的并 \(S\) 也只有轴系数一，矛盾。故
\(S\) 是原子。同理 \(Q_H\setminus S\) 也是原子。

所以所有真 \(\rho\)-零子集形成一个对取补封闭的反链：

\[
S\longleftrightarrow Q_H\setminus S,
\tag{11}
\]

每一对都给出系数型 \((1,1)\) 的原子分解；若这样的 \(S\) 不存在，
则 \(Q_H\) 本身是系数二的原子。这不只是在某个任意分解中列出
\((2)\) 或 \((1,1)\)，而是刻画全部真零子集。

若 \(|S|=1\)，它是商标签恰为 \(q\) 的单点。长补 (4) 已含
\(p-4\) 个 \(q\)-位置，加入这个单点会使 \(q\)-纤维重数至少
\(p-3\)，违反每个 \(F_3\) 长补原子的统一上界 \(p-4\)。对
\(Q_H\setminus S\) 同理。因此 (11) 两侧都有

\[
\boxed{|S|\ge2,\qquad|Q_H\setminus S|\ge2.}
\tag{12}
\]

## 4. 混合目标纤维给出全判据

还需精确保留同时穿过 \(P\) 与 \(Q_H\) 的内部子集。任取

\[
\varnothing\ne A\subsetneq P.
\tag{13}
\]

因为 \(\rho(P)\) 是原子，\(\rho(\bar\sigma(A))\ne0\)。对每个
\(T\subset Q_H\) 满足

\[
\rho(\bar\sigma(T))=-\rho(\bar\sigma(A)),
\tag{14}
\]

完整判据 (6) 精确要求

\[
\boxed{
\bar\sigma(A)+\bar\sigma(T)
\in\{q,2q,3q\}.}
\tag{15}
\]

反过来，(5) 的 \(Q_H\) 内部规则加上对所有 (13)--(14) 的 (15)，
也足以恢复 (6)。事实上，对任意
\(E\subsetneq W_H\)，写成唯一的不交并

\[
E=A\mathbin{\dot\cup}T,
\qquad A\subseteq P,\quad T\subseteq Q_H.
\tag{16}
\]

- \(A=\varnothing\) 时由 (5) 处理真 \(Q_H\) 子集，而
  \(T=Q_H\) 的轴系数 \(4-d\in\{1,2\}\) 自动允许；
- \(A=P\) 时，\(T=\varnothing\) 的轴系数 \(d\) 自动允许，
  真 \(\rho\)-零 \(T\) 再由 (8)--(9) 处理；
- \(\varnothing\ne A\subsetneq P\) 时，\(E\) 的 \(\rho\)-和为零
  恰等价于 (14)，正由 (15) 处理。

这三类穷尽全部实际位置子集，故确为充要压缩。

条件 (15) 对 \(A\) 与 \(P\setminus A\) 互为补集：同时把
\(T\) 换成 \(Q_H\setminus T\)，两边的轴系数之和为四，而允许集
\(\{1,2,3\}\) 在 \(c\mapsto4-c\) 下不变。因此只需保留

\[
2^{|P|-1}-1
\tag{17}
\]

个补配对代表。当前 \(|P|=1,2,3\) 时，独立目标纤维数分别为

\[
\boxed{0,\qquad1,\qquad3.}
\tag{18}
\]

## 5. 八个剩余尺寸行与硬边界

将 (5)、(18) 应用于上一轮的八个非空尺寸行：

\[
\begin{array}{c|c|c|c|c}
p&\text{型}&|P|&Q_H\text{ 内部规则}&\text{独立混合目标数}\\ \hline
233&(2)&1&c=1\text{ 的原子补配对}&0\\
233&(2)&2&c=1\text{ 的原子补配对}&1\\
233&(3)&1&Q_H\text{ 原子}&0\\
233&(3)&2&Q_H\text{ 原子}&1\\
233&(3)&3&Q_H\text{ 原子}&3\\
1399&(2)&1&c=1\text{ 的原子补配对}&0\\
1399&(3)&1&Q_H\text{ 原子}&0\\
1399&(3)&2&Q_H\text{ 原子}&1.
\end{array}
\tag{19}
\]

特别地，型 \((3)\)、\(|P|=1\) 时没有混合目标；长补的全部内部
子集和判据严格等价于 \(Q_H\) 原子性。仅靠这一端点内部谱不能再
推出新矛盾。这是已经证明的硬边界，不是停止整个路线的理由：
下一步必须联立不同端点共享的同一 \(K,L,P\) 位置与 (15) 的目标纤维。

## 6. 边界

- 本文不声称表 (19) 任一行可实现，也没有关闭空 packing。
- (15) 是对实际位置子集的全称条件；报告只计数互补冗余后的目标
  纤维数，不枚举 \(C_p^2\) 标签模型。
- 本文没有把局部 \(Q_H\) 原子性提升为不同端点可独立选择。
- 全局 \(A_p\) 仍未完成。
