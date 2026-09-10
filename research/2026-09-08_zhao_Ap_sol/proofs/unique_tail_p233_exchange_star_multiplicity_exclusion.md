# \(p=233\) 长七交换星强迫实际重数超界

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 已审输入

固定 720 个 mixed-length outer survivors 中一个含长七 singleton 的行。
其长补投影原子 \(Q\) 是 Property-B 最大原子。已审单交换正规形给出
一组基 \((g,h)\) 及

\[
Q=g^{p-1}\prod_{j=1}^{p}\ell_{a_j},
\qquad
\ell_t=h+tg,
\qquad
\sum_j a_j=1,
\tag{1}
\]

使 \(Q\) 中的两个尾位置都在线上，并存在实际位置

\[
x_0,y\in Q\setminus U,
\qquad
\rho(\sigma(x_0))=g,
\qquad
\rho(\sigma(y))=\ell_a,
\tag{2}
\]

满足

\[
E_0=\{x_0,y\},
\qquad
\rho(\sigma(E_0))=s=\ell_{a+1}.
\tag{3}
\]

若 \(z^\ast\in P\) 是投影为 \(s\) 的 complementary packing 位置，
另一个 packing 位置记为 \(z\)，则已审 mixed 高度交换引理对任意
避尾双点表示 \(E\) 给出完整实际等式

\[
\sigma(E)=\sigma(z^\ast).
\tag{4}
\]

当前假想反例分支的最大完整实际标签重数为

\[
\max_v v_v(Z)=p-4=229.
\tag{5}
\]

## 2. 同一线位置产生 \(p-1\) 条交换边

式 (1) 中恰有 \(p-1\) 个互异的实际位置投影为 \(g\)。因两个尾位置
都在线 \(h+\langle g\rangle\) 上，这 \(p-1\) 个重项位置全都避开
\(U\)。

固定 (2) 中的同一个实际线位置 \(y\)。对每个投影为 \(g\) 的实际
位置 \(x\)，都有

\[
E_x=\{x,y\}\subseteq Q\setminus U,
\qquad
|E_x|=2,
\qquad
\rho(\sigma(E_x))=g+\ell_a=s.
\tag{6}
\]

这不是把一个投影重数当作同一实际位置：\(x\) 遍历的是 \(Q\) 中
\(p-1\) 个不同的字面位置，而 \(y\) 固定；且
\(g\ne\ell_a\)，所以 \(x\ne y\)。又因 \(P\cap Q=\varnothing\)，
所有 (6) 都是 mixed 高度引理量词内合法的实际位置子集。

对每个 \(E_x\) 分别应用该引理。若
\(A_x=\{z\}\dot\cup E_x\) 的轴系数为 \(e\)，则
\(|E_x|\le e-1\) 与 \(e\in\{1,2,3\}\) 强迫 \(e=3\)。相应自动块
长七；它不能属于正核心 \(F_3\)，因为其尾严格包含字面唯一尾 \(U\)，
所以只能落入该引理表中的
\((e,|E|,F)=(3,2,F_2)\) 一行。于是 (4) 对每个 \(x\) 都成立：

\[
\sigma(x)+\sigma(y)=\sigma(z^\ast).
\tag{7}
\]

## 3. 实际重数矛盾

式 (7) 的右端及 \(y\) 都是固定的真实位置标签。因此在完整群中可消去
\(\sigma(y)\)，得到

\[
\sigma(x)=\sigma(z^\ast)-\sigma(y)
\quad\text{对全部 }p-1\text{ 个重项位置 }x.
\tag{8}
\]

所以同一个完整实际值至少出现

\[
p-1=232
\tag{9}
\]

次，与 (5) 的上界 \(p-4=229\) 矛盾。

## 4. 裁决

540 个含长七 singleton 的 outer rows 中，双点
\(2\leftrightarrow1\) 交换支全部不可能。此前已审单侧 singleton
闭合又排除了无双点交换支。因此

\[
\boxed{540\text{ 个含长七 singleton 的 outer rows 全部删除。}}
\tag{10}
\]

720 行只余 180 个“三个 singleton 端点均长八”的 outer rows；其中
只有 36 行的全部端点都长八。本文没有处理这 180 行的一般 packing
方向，也没有完成固定 \(p=233\) 切片或全局 \(A_p\)。
