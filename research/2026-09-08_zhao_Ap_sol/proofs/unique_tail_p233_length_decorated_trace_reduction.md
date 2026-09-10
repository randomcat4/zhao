# \(p=233\) 全异迹分片的 \(7/8\) 端点长度削减

STATUS: **EXACT OUTER LENGTH ENUMERATION / TWO-SINGLETON DEPENDENCY PENDING FRESH REVIEW / 720 SURVIVORS / GLOBAL INCOMPLETE**

## 1. 结论

固定

\[
p=233,\qquad \text{型 }(3),\qquad |P|=2,\qquad \kappa=1
\tag{1}
\]

以及已经认证的 36 个四边全异迹 outer shards。允许每个端点的长度
在 \(\{7,8\}\) 中独立变化。把每个 trace shard 的全部二元长度装饰
展开后共有

\[
\boxed{1440}
\tag{2}
\]

个 length-decorated shards。

每个全异迹 shard 恰含迹为 \(1,2,4\) 的三个 singleton 端点。新得到
的 Property B 双最大原子混合排除，加上已审正确的三域一般定理，
说明这三个端点中不能有两个同时长七。因此精确删除
singleton-\(h=7\) 数至少为二的全部装饰，得到

\[
\boxed{1440-720=720}
\tag{3}
\]

个 outer survivors。这里 survivor 只表示未被这一条外层定理删除，
不表示存在逐位置标签实现。

## 2. 为什么精确允许集是 \(\{7,8\}\)

型 \((3)\) 的共同 packing 块满足 \(|P|=2\)。对任一零核心端点
\(H\)，写 \(h=|H|\)，其长补投影原子为

\[
Q_H=K\mathbin{\dot\cup}(L\setminus H),
\qquad
|Q_H|=2p+8-h-|P|=2p+6-h.
\tag{4}
\]

由 \(D(C_p^2)=2p-1\)，原子长度上界给出

\[
2p+6-h\le2p-1,
\qquad h\ge7.
\tag{5}
\]

零核心 \(F_3\) 端点来自完整短谱，已有 \(h\le8\)。故

\[
\boxed{h\in\{7,8\},\qquad \delta_H=h-7\in\{0,1\}.}
\tag{6}
\]

这不是把旧的“全长七”schema 静默放宽：本文明确建立下一层二元
长度装饰，并且只复用与长度无关的四边图和六迹赋值。

## 3. 为什么仍然只有原来的 36 个 trace shards

36 分片的推导只使用：

1. 四条简单边没有孤立端点；
2. 每个端点迹是三点尾 \(U\) 的非空真子集；
3. 每条边两端迹不交；
4. 六个端点迹全异。

以上条件都不含 \(h\)。所以把端点长度从全七推广到 (6) 不会产生
新的图型或迹赋值。四种幸存图型及其固定代表赋值数仍为

\[
\begin{array}{c|rrrr}
\text{图型}&\mathrm{paw}&P_5&T_5&P_4\dot\cup K_2\\ \hline
\text{trace shards}&6&6&12&12.
\end{array}
\tag{7}
\]

它们的端点数分别为 \(4,5,5,6\)。因此装饰前总数为

\[
6\cdot2^4+6\cdot2^5+12\cdot2^5+12\cdot2^6=1440.
\tag{8}
\]

## 4. 两个 singleton 长七已经不可能

对迹为 \(\{u_i\}\) 的长七端点，\(Q_i\) 长 \(2p-1=465\)，因而是
\(C_{233}^2\) 中的最大零和原子。Property B 给它一个出现
\(p-1=232\) 次的重标签和相应单仿射线正规形。

设三个 singleton 端点为 \(H_1,H_2,H_3\)，并先取

\[
|H_1|=|H_2|=7,\qquad |H_3|=8.
\tag{9}
\]

三条相应长补原子满足

\[
Q_i=(K\mathbin{\dot\cup}L)\setminus H_i,
\qquad |K\mathbin{\dot\cup}L|=474-|P|=472.
\tag{10}
\]

所有端点都含同一个实际位置 \(y\)，所以

\[
|H_1\cup H_2\cup H_3|
\le 1+(7-1)+(7-1)+(8-1)=20.
\tag{11}
\]

因此三条补原子的**字面位置交集**至少为

\[
|Q_1\cap Q_2\cap Q_3|
=472-|H_1\cup H_2\cup H_3|
\ge452>435.
\tag{12}
\]

这里给混合定理使用的共同核可以直接取式 (12) 的交集，不应误取较小
的 packing 核。迹为三个不同 singleton，意味着每条 \(Q_i\) 恰含另
两个尾标签；经过保持三尾和为零的线性换基，两个长七补原子的尾对可
写成 \(\{f,t\}\)、\(\{e,t\}\)，第三条长八补原子含
\(\{e,f\}\)。于是
`unique_tail_property_b_two_max_mixed_exclusion.md` 的全部前提满足：前
两条长 \(465\)，第三条长 \(464>4\)，且统一字面共同核至少为
\(452\)。该定理穷尽 Property B 支撑方向后只剩四组重基对，每组都
在第三条原子内产生三项或四项真零和，故恰有两个 singleton 长七的
分支矛盾。

若三个 singleton 全部长七，则

\[
|H_1\cup H_2\cup H_3|
\le1+3(7-1)=19,
\qquad
|Q_1\cap Q_2\cap Q_3|\ge472-19=453>0.
\tag{13}
\]

三条 \(Q_i\) 都长 \(465\)，并含三个互补尾对。因此任选式 (13) 的
一个共同实际位置，其统一非零标签必须同时落入三个 Property B 支撑
域；已独立审为 `CORRECT` 的
`unique_tail_property_b_three_domain_general.md` 证明这三个域在
\(p=233\) 没有共同非零点。注意这里没有假设其他非 singleton 端点
也长七，因而没有越用“所有端点全长七”的旧冻结表述。合并两种情形
得到

\[
\boxed{
\#\{i\in\{1,2,3\}: |H_i|=7\}\le1.}
\tag{14}
\]

本文不重写两份承重证明。三域一般定理已有独立 `CORRECT` 复核；在
新混合定理的全新独立复核通过以前，(14) 与本削减仍保持“待审候选”
状态。

## 5. 精确计数

一个含 \(s\) 个端点的 trace shard 有三个 singleton 顶点及
\(s-3\) 个非 singleton 顶点。式 (14) 允许 singleton 长七数为零或
一，因此每个父分片保留

\[
\left(\binom30+\binom31\right)2^{s-3}=4\cdot2^{s-3}
\tag{15}
\]

个装饰，恰为全部 \(2^s\) 装饰的一半。逐图型计数为

\[
\begin{array}{c|r|r|r}
\text{图型}&\text{全部装饰}&\text{删除}&\text{保留}\\ \hline
\mathrm{paw}&96&48&48\\
P_5&192&96&96\\
T_5&384&192&192\\
P_4\dot\cup K_2&768&384&384\\ \hline
\text{合计}&1440&720&720.
\end{array}
\tag{16}
\]

幸存者按 singleton 长七数分成

\[
\begin{array}{c|rr}
\text{singleton 长七数}&0&1\\ \hline
\text{分片数}&180&540,
\end{array}
\tag{17}
\]

按全部端点中的长七总数分成

\[
\begin{array}{c|rrrrr}
\text{长七总数}&0&1&2&3&4\\ \hline
\text{分片数}&36&186&288&174&36.
\end{array}
\tag{18}
\]

配套报告逐行保存全部 720 个 survivor 的父 shard、边表、迹掩码、
端点长度、singleton 顶点及稳定 decorated shard 编号，而不只保存
汇总数字。

## 6. 图与 incidence 没有再强迫任何长七端点

每个父 trace shard 都有一个“所有端点全长八”的装饰。它满足本层
唯一使用的图、迹、长度允许集和式 (14)，所以共有精确的 36 个
all-\(8\) outer witnesses。因此

\[
\boxed{\text{纯 outer 图／迹 incidence 不强迫一个、两个或三个额外的
长七端点。}}
\tag{19}
\]

这只是外层反见证，不是 474 位置标签模型。进一步删除必须使用长
\(2p-2\) 原子的内部子集和、统一标签、混合目标、自动短块、Hasse
或实际高度，而不能继续从四边图本身索取长度七端点。

## 7. 停止线

- **精确枚举：** 36 个认证 trace shards 的全部 \(7/8\) 装饰为
  1440 个。
- **待独审削减：** 双 singleton Property B 定理删除 720 个，留下
  720 个。
- **严格外层边界：** 36 个 all-\(8\) 装饰证明图／迹层不强迫任何
  长七端点。
- **未实例化：** 端点实际位置掩码、统一 \(C_{233}^3/C_{233}^4\)
  标签、mixed-\(7/8\) 尾秩、十一项 CEGAR 预言机。
- **未宣称：** 任一 outer survivor 可实现、mixed-\(7/8\) 首片
  SAT/UNSAT、固定 \(p=233\) 全问题或全局 \(A_p\) 已闭合。
