# (p=233) 混合长度外层行的共同核下界

## 裁决

**EXACT OUTER REDUCTION / PROPERTY-B CAPACITY ORACLE / GLOBAL INCOMPLETE。**

本结果只使用 720 个已认证长度装饰分片中的迹、端点长度和四边共同
非轴位置。它不生成真实端点掩码，也不声称任何 surviving row 可实现。

## 1. 逐行共同核下界

固定一行。尾 (U) 有三个位置。设端点为 (H_i)，其尾迹为
(T_i=H_icap U)，长度为 (ell_i)。四条指定边共享同一个尾外
位置 (y)，而端点图的全部顶点都出现在某条边上，所以每个 (H_i)
都含 (y)。因此

\[
L=U\cup\bigcup_i H_i
\]

满足

\[
|L|\le 3+1+\sum_i(\ell_i-|T_i|-1).
\]

型 ((3))、(|P|=2) 的逐位置分解给出

\[
R=Y\setminus L,\qquad K=R\setminus P,
\qquad |Y|=474,
\]

故

\[
\boxed{|K|\ge
468-\sum_i(\ell_i-|T_i|-1).}
\]

这一步只是集合并的上界；不同端点若还有额外交叠，只会使 (L) 更小、
(K) 更大，所以不需要猜测任何未生成的掩码。

对全部 720 行直接代入认证的 ((T_i,ell_i))，下界范围为
(435\) 至 (447)，精确分布为

\[
\begin{array}{c|rrrrrrrrrrrr}
|K|_{\min}&435&436&437&438&439&440&441&442&443&445&446&447\\
\hline
\#&12&72&144&120&36&18&90&126&54&6&24&18.
\end{array}
\]

## 2. Property B 支撑容量门

若 (ell_i=7)，则对应 (Q_{H_i}) 长 (2p-1=465)，是最大
(C_p^2) 原子。Property B 将它写成

\[
g^{p-1}\prod_{j=1}^{p}(h+a_jg),qquad \sum_j a_j=1.
\]

重标签 (g) 出现 (p-1) 次。任一仿射线标签若出现 (p) 次，
则所有 (a_j) 相等，从而 (sum_j a_j=pa_j=0)，与系数和为 (1)
矛盾。因此最大原子中每个标签的字面重数至多 (p-1=232)。

共同核 (K) 是每个展示 (Q_H) 的字面子序列，所以其标签必须落在
所有 length-seven 最大原子的 Property-B 支撑交中。由于每个适用行
都有 (|K|\ge435)，该公共支撑交至少含

\[
\left\lceil\frac{435}{232}\right\rceil=2
\]

个点。故得到一个无需端点掩码的严格分离器：

> 任意至少两条 length-seven 补原子的标准形支撑若公共点集至多为一，
> 则该 outer row 的这组支撑选择不可能提升为真实位置实例。

720 行中有 684 行至少含一条 length-seven 最大补原子，498 行至少含
两条，后者可直接调用这个多支撑容量分离器。36 个全长八行不在
Property B 的最大原子作用域内。

## 3. 边界

- “公共支撑至少两点”只是必要条件，不是可实现性结论。
- 本结果没有枚举共同点上的重数，也没有检查 (K) 零和自由、统一
  (q)/高度、自动短块、mixed targets、Hasse 或实际 (Z) 原子。
- 它没有删除某个 outer row；下一步须与 Property-B 支撑枚举及真实
  endpoint masks 联合。

可执行重放：`unique_tail_p233_kernel_lower_by_outer_row.py`。
