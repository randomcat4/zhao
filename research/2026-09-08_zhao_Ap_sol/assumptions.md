# 冻结前提与继承接口

## 共同约定

- \(p\ge7\) 为素数，\(G=C_p^4=\mathbb F_p^4\)。
- 序列均按位置计数；相同群元素的不同副本是不同位置。
- \(\sigma(A)\) 表示位置子序列 \(A\) 的群和。
- \(H=\langle a\rangle\)，\(\pi:G\to G/H\) 为商映射。

## 假想反例边界

反设存在长度 \(5p-4\) 的序列 \(S\)，没有长度至多 \(3p-2\) 的非空零和位置子序列。既有高度归约给 \(h(S)\le p-4\)；本轮冻结边界

\[
S=a^{p-4}R,\qquad |R|=4p.
\]

继承的短商零和接口是：若 \(B\subseteq R\) 非空、\(\pi(\sigma(B))=0\) 且 \(|B|\le2p+2\)，则

\[
\sigma(B)\in\{a,2a,3a\}.
\tag{SQ}
\]

## \(x_0=0\) 分支

令 \(x_j=Z_{3p+j}(R)\)。继承的实际零和窗口及删除正规形为

\[
Z_k(R)=0\quad(k\notin\{3p,3p+1,3p+2,3p+3,3p+4\}),
\]

\[
(x_0,x_1,x_2,x_3,x_4)\equiv(1+\theta,4\theta,6\theta,4\theta,\theta)\pmod p.
\]

冻结 \(x_0=0\)，故 \(\theta=-1\)。Round 6 的过删除余数给出一个四位置集 \(D\subset R\)，使

\[
U=R\setminus D,\quad |U|=4p-4,
\quad \prod_{u\in U}(1-X^u)=\omega J_G,
\quad \omega\in\mathbb F_p^\times.
\tag{TOP}
\]

等价地，对每个 \(x\in G\)，

\[
c_U(x):=\sum_{A\subseteq U,\ \sigma(A)=x}(-1)^{|A|}=\omega.
\tag{CONST}
\]

此外 \(U\) 可分成 \(p-1\) 个四元基。这个基分块只提供表示存在性，未冻结任何长度控制结论。

## 公共去重接口

公共独立审计已认证派生接口
`A_exterior_double_sum_obstruction`：不能在 \(D a^{p-4}\) 中
取两个非空外侧位置块 \(H_1,H_2\)（允许两块重叠），使

\[
\sigma(U)+\sigma(H_1)+\sigma(H_2)=0.
\tag{EXT2}
\]

本接口不是新增假设；它由冻结前提导出。原“双侧补集线陷阱”已与
(EXT2) 去重合并。

## ROUTE-A4 的派生第三族接口

以下两条不是新增假设，而是 `route_a_atom_line_rigidity.md` 已从上述
冻结反例推出、供后续候选调用的派生接口。若
\(Z\subseteq R\) 是长度 \(3p+4\) 的实际零和原子，并令
\(\mathcal F_3\) 为其中全部六至八项、实际和为 \(3a\) 的位置块，则

\[
\bigcap_{A\in\mathcal F_3}A=\varnothing,
\qquad
\pi(Z\setminus A)\text{ 对每个 }A\in\mathcal F_3
\text{ 都是 }C_p^3\text{ 中的原子。}
\tag{F3-NET}
\]

第一条来自逐点第三族带符号度非零而第三族总带符号和为零；第二条
来自第三族块长度窗与补集分拆会制造冻结禁长零和的论证。后续所谓
“完整 \(F_3\) 网络”均指至少同时保留这两条接口，而不是任意裸商
标签多重集。

## 明确排除

不假设 \(\sigma(R)=0\)，也不假设 \(\sigma(R)\in H\)。后者将在本轮作为反设子分支被排除。
