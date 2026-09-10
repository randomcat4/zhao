# \(p=233\) 三长八 \(m=3\) 的 \(U\cup V\) 自动短块门

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 六位置子系统

写

\[
W=\{w_1,w_2,w_3\}
=\{e,f,-e-f\},
\qquad
U=\{u_1,u_2,u_3\},
\qquad
V=\{v_1,v_2,v_3\},
\tag{1}
\]

\[
\rho(\sigma(u_i))=w_i,
\qquad
\rho(\sigma(v_i))=w_i+\delta.
\tag{2}
\]

共同核曲线已经给出

\[
q_0(\delta)=3,
\qquad
q_0(\alpha e+\beta f)=\alpha^2-\alpha\beta+\beta^2.
\tag{3}
\]

对 \(I,J\subseteq[3]\)，令

\[
R(I,J)=\{u_i:i\in I\}
\mathbin{\dot\cup}
\{v_j:j\in J\}.
\tag{4}
\]

则

\[
\rho(\sigma(R(I,J)))
=w(I)+w(J)+|J|\delta.
\tag{5}
\]

若 \(J=\varnothing\)，三个尾是原子，所以除空集外只有
\(I=[3]\) 给出原尾 \(U\)。若 \(J\ne\varnothing\)，投影零和强迫

\[
\delta=-\frac{w(I)+w(J)}{|J|}.
\tag{6}
\]

逐一枚举 \(I\) 与固定大小的 \(J\)，候选 (6) 的 \(q_0\)-值分布为

\[
\begin{array}{c|l}
|J|&q_0(\delta)\text{ 的值与重数}\\ \hline
1&0\times3,\ 1\times12,\ 3\times6,\ 4\times3\\
2&0\times3,\ \frac14\times12,\ \frac34\times6,\ 1\times3\\
3&0\times2,\ \frac19\times6.
\end{array}
\tag{7}
\]

在 \(\mathbb F_{233}\) 中，(7) 除显示的六个值 3 外均不等于 3。
因此曲线上的额外 \(U\cup V\) 零和只可能发生在

\[
\boxed{\delta=w_j-w_i\qquad(i\ne j).}
\tag{8}
\]

每个 (8) 恰有一条额外关系

\[
\boxed{
R_{ij}=(U\setminus\{u_j\})\mathbin{\dot\cup}\{v_i\},
\qquad |R_{ij}|=3.
}
\tag{9}
\]

六个点与关系是

\[
\begin{array}{c|c}
\delta&R_{ij}\\ \hline
(-1,1)&\{u_1,u_3,v_1\}\\
(-2,-1)&\{u_1,u_2,v_1\}\\
(1,-1)&\{u_2,u_3,v_2\}\\
(-1,-2)&\{u_1,u_2,v_2\}\\
(2,1)&\{u_2,u_3,v_3\}\\
(1,2)&\{u_1,u_3,v_3\}.
\end{array}
\tag{10}
\]

故其余 228 个曲线点除 \(U\) 外没有 \(U\cup V\) 内的投影零和；
六个例外点也各自只有 (9)，没有额外长度二、四、五或六关系。
六点在尾 \(S_3\) 下构成单个轨道。

## 2. 六个例外点的实际 lift 门

在 (8) 上有
\(\rho(\sigma(v_i))=\rho(\sigma(u_j))\)，故唯一写

\[
\sigma(v_i)-\sigma(u_j)=\theta x+\eta a,
\qquad \theta,\eta\in\mathbb F_{233}.
\tag{11}
\]

已审唯一尾关系为

\[
\sigma(U)=3a-4x.
\tag{12}
\]

因此

\[
\sigma(R_{ij})=(\theta-4)x+(\eta+3)a.
\tag{13}
\]

令

\[
c\equiv4-\theta\pmod p,
\qquad 0\le c\le p-1.
\tag{14}
\]

当 \(c\le p-4=229\) 时，字面位置块

\[
D=X_c\mathbin{\dot\cup}R_{ij}
\tag{15}
\]

实际存在，长 \(3+c\)，在相关轴商中的和为零，完整和为
\((\eta+3)a\)。把已审短谱

\[
\begin{array}{c|c|c}
&\text{长度}&\text{完整和}\\ \hline
F_1&2\text{--}6&a\\
F_2&4\text{--}7&2a\\
F_3&6\text{--}8&3a
\end{array}
\tag{16}
\]

与长度 \(9\) 至 \(2p+2\) 的禁窗逐行应用。又因唯一正核心
\(F_3\) 块为 \(X_4\dot\cup U\)（等价地，唯一 \(Y\)-尾为
\(U\)），任何 \(c>0\) 且字面尾 \(R_{ij}\ne U\) 的 \(F_3\)
选择都被排除。得到精确表

\[
\begin{array}{c|c|c|c}
c&\theta&3+c&\eta\text{ 的允许值}\\ \hline
0&4&3&\{-2\}\\
1&3&4&\{-2,-1\}\\
2&2&5&\{-2,-1\}\\
3&1&6&\{-2,-1\}\\
4&0&7&\{-1\}\\
5&-1&8&\varnothing\\
6\text{--}229&4-c&9\text{--}232&\varnothing\\
230\text{--}232&7,6,5&233\text{--}235&\mathbb F_{233}.
\end{array}
\tag{17}
\]

最后三行不是实际长块许可：它们只表示现有 \(X\)-纤维没有足够位置
组成 (15)，所以这一局部门不能约束 \(\eta\)。

因此每个例外曲线点的轴/高度 lift 从 \(233^2\) 个压到

\[
\boxed{1+2+2+2+1+3\cdot233=707.}
\tag{18}
\]

特别地，\(\theta=-1\)、\(c=5\) 的整列也被第二正核心尾排除。

## 3. 严格边界

未标点的 39 个曲线轨道中，(8) 的六点恰组成一个例外轨道；其余
38 个轨道在 \(U\cup V\) 内没有原尾之外的自动投影零和。形式上的
\(\delta\mapsto-\delta\) 不保持字面尾三角 \(W\)，不能再把 39
错误压成 20。

若同时标出 completion 见证端点，则这个例外 \(S_3\) 轨道分裂成
三个 pointed 角色：见证指标分别可等于 (9) 中的 \(v\)-索引、被
替换的尾索引或第三个索引。后续求解器必须保留这三个角色，不能把
例外轨道在 pointed 问题里仍只算作一个状态。

本门不删除六点例外轨道，只把它的实际 lift 压到 707 个；其余 38
轨道仍须通过 cancellation line、逐点 complete 删除、共同核真实
标签与自动短块继续攻击。剩余 180 行和全局 \(A_p\) 均保持
**INCOMPLETE**。
