# 三个极长补原子的全带符号边缘

STATUS: **PROVED_COROLLARY / PENDING_INDEPENDENT_REVIEW / GLOBAL_INCOMPLETE**

## 1. 范围

上一条已独立认证的定理在三个剩余偏差行中给出实际位置块

\[
|C|=6,\qquad \sigma(C)=2a,
\tag{1}
\]

以及它的字面补集

\[
B=Z\setminus C,
\qquad |B|=3p-2,
\tag{2}
\]

其中 \(\pi(B)\) 是 \(C_p^3\) 中的原子。三行是

\[
\begin{array}{c|c|c|c}
p&\text{packing 型}&|P|&|B|\\ \hline
233&(2)&1&697\\
233&(3)&2&697\\
1399&(3)&1&4195.
\end{array}
\tag{3}
\]

本文把已认证的极值原子边缘逐字接到这三个**实际补集**上，因而获得
每个删点、每个 \(C\) 内部真子集及每个商目标的带符号恒等式。

## 2. 删除长补任一位置

固定任意 \(z\in B\)，令

\[
U_z=B\setminus\{z\}.
\tag{4}
\]

因为 \(B\) 是长度 \(3p-2=D(C_p^3)\) 的原子，\(U_z\) 是长度
\(3p-3\) 的零和自由序列。在
\(\mathbb F_p[C_p^3]\) 中，增广理想的顶非零次数为 \(3p-3\)，
且该层由群全和元

\[
J=\sum_{g\in C_p^3}X^g
\tag{5}
\]

张成。故

\[
\prod_{u\in U_z}(1-X^{\bar u})=\gamma_zJ.
\tag{6}
\]

左侧单位元系数只有空子集贡献，等于一，所以
\(\gamma_z=1\)。于是

\[
\boxed{
\prod_{u\in U_z}(1-X^{\bar u})=J
\qquad(z\in B).}
\tag{7}
\]

等价地，对每个 \(g\in C_p^3\)，

\[
\boxed{
\sum_{E\subseteq U_z\atop\bar\sigma(E)=g}(-1)^{|E|}=1.}
\tag{8}
\]

这是删去长补中任一实际位置后的全部内部子集和，不是有限长度近似。

## 3. 六项块每个真子集的双边截断式

取任意

\[
\varnothing\ne T\subsetneq C,\qquad t=|T|.
\tag{9}
\]

对满足 \(\bar\sigma(E)=-\bar\sigma(T)\) 的
\(E\subseteq U_z\)，两块

\[
E\mathbin{\dot\cup}T,
\qquad
(U_z\setminus E)\mathbin{\dot\cup}\{z\}
\mathbin{\dot\cup}(C\setminus T)
\tag{10}
\]

分割 \(Z\) 且均为商零。由冻结短谱、商禁窗与长原子的正系数长度界，
其中恰有一边落入短层。因此令

\[
L_{\le m}^{U}(g)=
\sum_{\substack{F\subseteq U,\ |F|\le m\\
\bar\sigma(F)=g}}(-1)^{|F|},
\tag{11}
\]

已认证的极值边缘恒等式逐位置给出

\[
\boxed{
L_{\le8-t}^{U_z}(-\bar\sigma(T))
+
L_{\le t+1}^{U_z}(\bar\sigma(T)-\bar z)=1.}
\tag{12}
\]

这里 \(t=1,\ldots,5\)，两个截断界依次为

\[
(7,2),\quad(6,3),\quad(5,4),\quad(4,5),\quad(3,6).
\tag{13}
\]

每个六项 \(C\) 有 \(2^6-2=62\) 个非空真位置子集；所以 (12)
不是给预选一个 \(T\) 的模板，而是对全部 62 个 \(T\) 与全部
\(z\in B\) 同时成立。三个行实例合计给

\[
62(697+697+4195)=346\,518
\tag{14}
\]

条 \((z,T)\) 恒等式。

特别地，对每个 \(c\in C,z\in B\)，分别取
\(T=\{c\}\) 与 \(T=C\setminus\{c\}\)，得到

\[
\boxed{
L_{\le7}^{U_z}(-\bar c)+L_{\le2}^{U_z}(\bar c-\bar z)=1,}
\tag{15}
\]

\[
\boxed{
L_{\le3}^{U_z}(\bar c)+L_{\le6}^{U_z}(-\bar c-\bar z)=1.}
\tag{16}
\]

## 4. 边界

- (7)--(16) 都是 \(\mathbb F_p\) 中的带符号恒等式，不能解释为
  普通表示数等于一。
- 它们保证相应两侧至少有一个模 \(p\) 非零的常长度表示，但没有
  单独制造矛盾。
- 本文没有使用 \(F_3\) 补原子专属的 \(p-4\) 纤维上界；这里的
  \(B\) 是六项 \(F_2\) 块的补集。
- 三个偏差行仍未证明可实现或不可实现，全局 \(A_p\) 仍未完成。
