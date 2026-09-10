# \(p=233\) 三长八 \(m=3\) 核曲线的尾对称轨道

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 输入

沿用三长八唯一 \(m=3\) 掩码态的记号：

\[
w_1=e,\qquad w_2=f,\qquad w_3=-e-f,
\qquad
\delta=\alpha e+\beta f.
\tag{1}
\]

已经证明每个候选满足

\[
\mathcal K:
\quad
\alpha^2-\alpha\beta+\beta^2=3.
\tag{2}
\]

在 \(\mathbb F_{233}\) 上，\(\mathcal K\) 有 234 个点，且没有点落在
\(\alpha=0\)、\(\beta=0\) 或 \(\alpha=\beta\) 上。

## 2. 这是字面位置子系统的同构，而不只是形式换基

任取 \(\pi\in S_3\)，同时重命名

\[
u_i\mapsto u_{\pi(i)},
\qquad
v_i\mapsto v_{\pi(i)},
\qquad
Q_i\mapsto Q_{\pi(i)}.
\tag{3}
\]

三个尾向量中任意两个都是一组基，所以存在唯一
\(T_\pi\in\operatorname{GL}_2(\mathbb F_{233})\) 使

\[
T_\pi(w_i)=w_{\pi(i)}
\qquad (i=1,2,3).
\tag{4}
\]

把所有投影标签同时施以 \(T_\pi\)，则

\[
w_i+\delta
\longmapsto
w_{\pi(i)}+T_\pi(\delta).
\tag{5}
\]

将 \(T_\pi\) 按恒等作用于轴与高度方向提升到完整实际群。于是三个
长补的字面位置成员关系、原子性、普通零和与自动短块、三个 fringe
的完整实际等和都被同构保持。这里的操作是 (3)--(4) 的联合重命名；
没有声称在一个固定标签实例内部只替换参数。

在坐标 \((\alpha,\beta)\) 上，\(S_3\) 可由

\[
\tau(\alpha,\beta)=(\beta,\alpha),
\qquad
\kappa(\alpha,\beta)=(\beta-\alpha,-\alpha)
\tag{6}
\]

生成，分别对应一个换位和一个三循环。直接代入可见二次型
\(X^2-XY+Y^2\) 在两者下不变，所以 (2) 被保持。

## 3. 作用在曲线上自由

三个换位在参数平面上的固定线依次是

\[
\alpha=\beta,
\qquad
\alpha=0,
\qquad
\beta=0.
\tag{7}
\]

把任一固定线代入 (2) 都得到某个坐标平方等于 3。因为 3 在
\(\mathbb F_{233}\) 中是非平方元，曲线上没有换位固定点。

非平凡三循环的固定点只可能是 \((0,0)\)：例如由
\((\beta-\alpha,-\alpha)=(\alpha,\beta)\) 得
\(3\alpha=0\)，进而 \(\alpha=\beta=0\)。该点不在 (2) 上。故
\(S_3\) 对 234 个曲线点的作用完全自由，每个轨道大小为六：

\[
\boxed{|\mathcal K/S_3|=234/6=39.}
\tag{8}
\]

## 4. 标出 complete-deletion 端点后的数目

若下一层同时标出由 461 定理选中的端点 \(i\)，则必须把见证指标
连同曲线点一起作用。利用 \(S_3\) 先把它归一到 \(i=1\) 后，剩余
稳定子群是交换另外两个尾的 \(S_2\)。该换位仍没有曲线固定点，故

\[
\boxed{|\{(i,\alpha,\beta):(\alpha,\beta)\in\mathcal K\}/S_3|
=234/2=117.}
\tag{9}
\]

所以不标端点的 \(m=3\) 标签搜索只需 39 个曲线轨道；标出一个
complete-deletion 端点后只需 117 个 pointed 轨道。

## 5. 边界

轨道压缩不排除任何曲线轨道，也不构造实际长补原子。下一步仍须在
117 个 pointed 候选上加载 461 个普通 complete 删除、统一
\(q\)-高度、真实 fringe 等和、全部自动短块及每个长补的内部子集
和。剩余 180 行和全局 \(A_p\) 仍为 **INCOMPLETE**。
