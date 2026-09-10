# \(p=7\) 极大商原子的群代数逃逸约束

STATUS: **PROVED_HERE / NECESSARY PRUNING ONLY / GLOBAL INCOMPLETE**

本文固定

\[
G=C_7^3=\mathbb F_7^3,
\qquad
B=(b_1,\ldots,b_{19}),
\]

其中 \(B\) 是长度 19 的零和原子。所有“子集”均指位置指标的子集；
即使 \(b_i=b_j\)，位置 \(i,j\) 仍是两个不同副本。记

\[
\sigma(J)=\sum_{j\in J}b_j,
\qquad
\Sigma_k(B)=\{\sigma(J):J\subseteq[19],\ |J|=k\}.
\]

本文证明三个可用于支撑至少八之规范增广的必要条件：删点群代数
恒等式、逃逸表示的逐位置交错恒等式，以及三/四重纤维的缺口梯。
这些条件不构成长支撑原子分类，也不关闭 \(p=7,m=3\) 分支。

## 1. 增广理想的顶层

令

\[
A=\mathbb F_7[G],
\qquad
X^gX^h=X^{g+h},
\qquad
\Omega=\sum_{g\in G}X^g,
\]

并令 \(I\) 为 \(A\) 的增广理想。取 \(G\) 的一组基
\(e_1,e_2,e_3\)，置

\[
Y_r=1-X^{e_r}\quad(1\le r\le3).
\]

### 引理 1（顶层恰为全和元）

在 \(A\) 中有

\[
\boxed{I^{18}=\mathbb F_7\Omega,\qquad I^{19}=0.}
\tag{1}
\]

**证明。** 特征为 7，故

\[
Y_r^7=(1-X^{e_r})^7=1-X^{7e_r}=0.
\]

映射

\[
\mathbb F_7[Y_1,Y_2,Y_3]/(Y_1^7,Y_2^7,Y_3^7)
\longrightarrow A
\tag{2}
\]

是满射：\(X^{e_r}=1-Y_r\) 均在像中。两边维数同为 \(7^3\)，
所以 (2) 是同构，且 \(I=(Y_1,Y_2,Y_3)\)。截断单项式的各指数
至多为 6，最大总次数为 18；总次数至少 18 的单项式只有
\(Y_1^6Y_2^6Y_3^6\)。因此

\[
I^{18}=\mathbb F_7Y_1^6Y_2^6Y_3^6,
\qquad I^{19}=0.
\]

最后，在 \(\mathbb F_7[Z]/(Z^7-1)\) 中

\[
(1-Z)^6=1+Z+\cdots+Z^6.
\]

所以

\[
Y_1^6Y_2^6Y_3^6
=\prod_{r=1}^3\sum_{a=0}^6X^{ae_r}
=\sum_{g\in G}X^g
=\Omega.
\]

这里没有遗漏负号或非零标量，(1) 得证。\(\square\)

### 引理 2（每个删点积都恰为 \(\Omega\)）

对每个位置 \(i\in[19]\)，令

\[
P_i=\prod_{j\ne i}(1-X^{b_j}).
\]

则

\[
\boxed{P_i=\Omega.}
\tag{3}
\]

**证明。** 因每个因子都属于 \(I\)，有
\(P_i\in I^{18}=\mathbb F_7\Omega\)，故 \(P_i=\gamma_i\Omega\)。
删除位置 \(i\) 后得到零和自由序列：否则其中的非空零和位置子集
就是 \(B\) 的非空真零和位置子集。展开乘积后，\(X^0\) 的系数为

\[
\sum_{\substack{J\subseteq[19]\setminus\{i\}\\\sigma(J)=0}}
(-1)^{|J|}=1,
\tag{4}
\]

因为只有空集贡献。\(\Omega\) 的 \(X^0\) 系数也是 1，故
\(\gamma_i=1\)。

式 (4) 是按位置展开的：若两个位置标签相同，乘积中仍有两个相同
因子，并产生两次独立的二择一选择。因此重复标签不会使论证退化成
支撑集合的错误计数。\(\square\)

### 推论 3（支撑射影简单）

\(0\notin\operatorname{supp}B\)，且同一一维子空间中不能出现两个
不同的支撑标签。换言之，自然映射

\[
\operatorname{supp}B\longrightarrow\mathbb P^2(\mathbb F_7)
\tag{5}
\]

是单射。这里允许同一个标签在 \(B\) 中重复多次；结论不是
“所有位置标签互异”。

**证明。** 零标签本身就是一项零和真子序列，所以不能出现。假设
两个不同支撑标签满足 \(b_i=cb_j\)，其中
\(c\in\{2,3,4,5,6\}\)。置 \(a=b_j\) 以及

\[
Q_{ij}=\prod_{k\ne i,j}(1-X^{b_k}),
\qquad
S_c=1+X^a+\cdots+X^{(c-1)a}.
\]

注意 \(i,j\) 是选取的两个位置；其余位置中即使还有标签 \(a\)
或 \(ca\) 的副本，也都仍保留在 \(Q_{ij}\) 中。由引理 2，

\[
P_i=(1-X^a)Q_{ij}=\Omega,
\]

而

\[
P_j=(1-X^{ca})Q_{ij}
=S_c(1-X^a)Q_{ij}
=S_c\Omega
=c\Omega.
\tag{6}
\]

最后一步使用 \(X^{ra}\Omega=\Omega\)。另一方面引理 2 又给出
\(P_j=\Omega\)。因 \(c\ne1\) 且 \(\Omega\ne0\)，矛盾。
\(\square\)

## 2. 逃逸点的逐位置交错恒等式

以下固定非零元素 \(t\in G\)，并假设

\[
\boxed{t\notin\bigcup_{k=4}^{11}\Sigma_k(B).}
\tag{7}
\]

由于 \(|B|=19\) 且 \(\sigma(B)=0\)，取位置补集给出

\[
\Sigma_k(B)=-\Sigma_{19-k}(B).
\]

所以 (7) 严格等价于

\[
-t\notin\bigcup_{k=8}^{15}\Sigma_k(B).
\tag{8}
\]

这也说明本文的 \(t\) 与既有“完整单点逃逸集”的方向一致：若该
逃逸集定义为 \(-t\) 避开 8--15 层，则它恰等价于 (7)，而不是只
检查 8--11 层。

### 2.1 两个位置表示族

定义

\[
\begin{aligned}
\mathcal R(t)
&=\{R\subseteq[19]:\sigma(R)=t,\ 1\le|R|\le3\},\\
\mathcal C(t)
&=\{C\subseteq[19]:\sigma(C)=-t,\ 1\le|C|\le7\}.
\end{aligned}
\tag{9}
\]

这里 \(R\) 是低长度的 \(t\)-表示，\(C\) 是低长度的
\((-t)\)-表示。它们都允许为空族；“非空”修饰的是族中每个位置
子集。所有交、补、含点条件都发生在位置集合上。

在 \(\mathbb F_7\) 中记

\[
\begin{aligned}
\rho&=\sum_{R\in\mathcal R(t)}(-1)^{|R|},
&\rho_i&=\sum_{\substack{R\in\mathcal R(t)\\i\in R}}(-1)^{|R|},\\
\kappa&=\sum_{C\in\mathcal C(t)}(-1)^{|C|},
&\kappa_i&=\sum_{\substack{C\in\mathcal C(t)\\i\in C}}(-1)^{|C|}.
\end{aligned}
\tag{10}
\]

### 引理 4（逐删点恒等式）

对每个位置 \(i\in[19]\)，有

\[
\boxed{
\rho-\rho_i-\kappa_i=1,
\qquad
\kappa-\kappa_i-\rho_i=1.}
\tag{11}
\]

特别地，

\[
\boxed{\rho=\kappa,
\qquad
\rho_i+\kappa_i=\rho-1\quad(1\le i\le19).}
\tag{12}
\]

**证明。** 先取 (3) 两边的 \(X^t\) 系数。删点积 \(P_i\) 中的
位置子集都不含 \(i\)。由 (7)，和值为 \(t\) 的这种子集，其大小
只能落在 \(1\)--\(3\) 或 \(12\)--\(18\)。低端的带符号和是
\(\rho-\rho_i\)。高端存在逐位置双射

\[
\begin{aligned}
&\{J\subseteq[19]\setminus\{i\}:\sigma(J)=t,\ 12\le|J|\le18\}\\
&\hspace{20mm}\longleftrightarrow
\{C\in\mathcal C(t):i\in C\},
\qquad C=[19]\setminus J.
\end{aligned}
\tag{13}
\]

被删位置为何必须属于 \(C\) 在 (13) 中是显式的：\(i\notin J\)
当且仅当 \(i\in[19]\setminus J\)。又因 \(|J|=19-|C|\) 且 19
为奇数，

\[
(-1)^{|J|}=(-1)^{19-|C|}=-(-1)^{|C|}.
\tag{14}
\]

所以高端贡献是 \(-\kappa_i\)。\(P_i=\Omega\) 的每个群元素系数
都是 1，得到 (11) 的第一式。

再取 \(X^{-t}\) 系数。由 (8)，其大小只能落在 \(1\)--\(7\)
或 \(16\)--\(18\)。低端贡献 \(\kappa-\kappa_i\)，而高端双射为

\[
\begin{aligned}
&\{J\subseteq[19]\setminus\{i\}:\sigma(J)=-t,\ 16\le|J|\le18\}\\
&\hspace{20mm}\longleftrightarrow
\{R\in\mathcal R(t):i\in R\},
\qquad R=[19]\setminus J.
\end{aligned}
\tag{15}
\]

同一个奇补符号 (14) 给出高端贡献 \(-\rho_i\)，故得第二式。
两式相减得到 \(\rho=\kappa\)，再代回即得 (12)。\(\square\)

对 (12) 在所有位置求和，还得到可用于审计的第一矩恒等式

\[
\boxed{
\sum_{R\in\mathcal R(t)}|R|(-1)^{|R|}
+\sum_{C\in\mathcal C(t)}|C|(-1)^{|C|}
=19(\rho-1)=5(\rho-1)\pmod7.}
\tag{16}
\]

### 引理 5（\(\mathcal R\)--\(\mathcal C\) 交叉相交）

任意 \(R\in\mathcal R(t)\) 和 \(C\in\mathcal C(t)\) 都满足

\[
\boxed{R\cap C\ne\varnothing.}
\tag{17}
\]

**证明。** 若二者按位置不交，则

\[
\sigma(R\mathbin{\dot\cup}C)=t-t=0,
\qquad
1\le|R\mathbin{\dot\cup}C|\le10<19.
\]

这给出 \(B\) 的非空真零和位置子集，与原子性矛盾。注意两个集合
含有相同标签的不同副本并不算相交；证明需要且只使用真实位置交集。
\(\square\)

## 3. 三/四重纤维的缺口梯

固定非零支撑标签 \(x\)，设它在 \(B\) 中出现 \(m\) 次，其中
\(m\in\{3,4\}\)，并把这些位置删除后所得序列记为 \(Q\)。约定
\(\Sigma_0(Q)=\{0\}\)，越界的固定基数层为空。

### 引理 6（缺口梯的充要分层式）

对任意 \(t\in G\)，有严格等价

\[
\boxed{
t\notin\bigcup_{k=4}^{11}\Sigma_k(B)
\iff
\forall b\in\{0,\ldots,m\},\quad
t-bx\notin
\bigcup_{\ell=\max(0,4-b)}^{\min(|Q|,11-b)}\Sigma_\ell(Q).}
\tag{18}
\]

**证明。** 任一 \(B\) 的位置子集唯一地选择 \(b\) 个 \(x\)-纤维
位置和一个 \(Q\)-位置子集 \(U\)。其大小与和值分别为

\[
b+|U|,
\qquad
bx+\sigma(U).
\]

存在大小 \(4\)--\(11\)、和值为 \(t\) 的位置子集，当且仅当存在
\(0\le b\le m\) 及允许的 \(\ell=|U|\)，使
\(t-bx\in\Sigma_\ell(Q)\)。对这一存在命题取否定便是 (18)。
同一标签的 \(m\) 个副本只影响表示的重数，不影响“该层是否存在”
的充要性。\(\square\)

当 \(m=3\) 时，(18) 展开为

\[
\begin{array}{c|c}
b&\text{必须缺失的 }Q\text{ 层}\\ \hline
0&t\notin\Sigma_{4..11}(Q)\\
1&t-x\notin\Sigma_{3..10}(Q)\\
2&t-2x\notin\Sigma_{2..9}(Q)\\
3&t-3x\notin\Sigma_{1..8}(Q).
\end{array}
\tag{19}
\]

当 \(m=4\) 时，除 (19) 的前四行外还必须有

\[
t-4x\notin\Sigma_{0..7}(Q).
\tag{20}
\]

因此四重纤维立即给出

\[
\boxed{t\ne4x,}
\tag{21}
\]

因为 \(0\in\Sigma_0(Q)\)。三重纤维中 \(t=3x\) 只由三项纤维
表示，尚未进入禁用的 4--11 层，所以不能从 (19) 单独排除；这正是
三重与四重梯在底层的差别。

### 推论 7（完整纤维星的交叉相交门）

设 \(U,V\subseteq Q\) 是位置尾，并满足

\[
\begin{aligned}
&|U|\le3-b, &&\sigma(U)=t-bx,\\
&|V|\le7-c, &&\sigma(V)=-t-cx,
\end{aligned}
\tag{22}
\]

其中 \(0\le b\le\min(3,m)\)、\(0\le c\le m\)。固定尾 \(U\)
并任选 \(b\) 个纤维位置，会得到完整的 \(\binom mb\) 个
\(\mathcal R(t)\) 成员；固定尾 \(V\) 同理得到完整的
\(\binom mc\) 个 \(\mathcal C(t)\) 成员。这两颗完整星两两相交
当且仅当

\[
\boxed{U\cap V\ne\varnothing\quad\text{或}\quad b+c>m.}
\tag{23}
\]

故由引理 5，若 \(b+c\le m\)，则必有 \(U\cap V\ne\varnothing\)。

特别地，若 \(t=bx\) 且 \(1\le b\le\min(3,m)\)，可取空尾
\(U=\varnothing\)。于是每个 \(C\in\mathcal C(t)\) 必须使用至少

\[
m-b+1
\tag{24}
\]

个 \(x\)-纤维位置。因此三重纤维依次给出

\[
t=x,2x,3x\quad\Longrightarrow\quad
|C\cap x^3|\ge3,2,1,
\tag{25}
\]

四重纤维在尚未被 (21) 排除的三种情形给出

\[
t=x,2x,3x\quad\Longrightarrow\quad
|C\cap x^4|\ge4,3,2.
\tag{26}
\]

### 3.1 带符号的纤维分层式

为把逐位置恒等式直接接入规范增广，定义

\[
\begin{aligned}
\alpha_b&=
\sum_{\substack{U\subseteq Q,\ |U|\le3-b\\\sigma(U)=t-bx}}
(-1)^{b+|U|},\\
\beta_b&=
\sum_{\substack{U\subseteq Q,\ |U|\le7-b\\\sigma(U)=-t-bx}}
(-1)^{b+|U|},
\end{aligned}
\tag{27}
\]

其中越界和为空，特别约定 \(b>3\) 时 \(\alpha_b=0\)。于是

\[
\rho=\sum_b\binom mb\alpha_b,
\qquad
\kappa=\sum_b\binom mb\beta_b.
\tag{28}
\]

对固定的一个纤维位置，含该位置的带符号次数分别为
\(\sum_{b\ge1}\binom{m-1}{b-1}\alpha_b\) 和
\(\sum_{b\ge1}\binom{m-1}{b-1}\beta_b\)。将其代入 (11)，并用
Pascal 恒等式，三重纤维得到

\[
\boxed{
\begin{aligned}
\alpha_0+2\alpha_1+\alpha_2
-(\beta_1+2\beta_2+\beta_3)&=1,\\
\beta_0+2\beta_1+\beta_2
-(\alpha_1+2\alpha_2+\alpha_3)&=1,
\end{aligned}}
\tag{29}
\]

四重纤维得到

\[
\boxed{
\begin{aligned}
\alpha_0+3\alpha_1+3\alpha_2+\alpha_3
-(\beta_1+3\beta_2+3\beta_3+\beta_4)&=1,\\
\beta_0+3\beta_1+3\beta_2+\beta_3
-(\alpha_1+3\alpha_2+3\alpha_3)&=1.
\end{aligned}}
\tag{30}
\]

所有等式都在 \(\mathbb F_7\) 中。(29)--(30) 是 (11) 对纤维位置
的精确压缩，不是仅凭层大小作出的近似；但它们仍只是必要条件，不能
替代完整的真实位置交叉相交网络。

## 4. 可执行证书

验证器为
`verify_p7_maximal_atom_escape_algebra.py`。它冻结并检查七个已知
长度 19 原子：一个既有支撑九原子、支撑六分类的两个轨道，以及
支撑七非空逃逸前沿的四个轨道。所有检查均以 19 个真实位置运行。

验证器执行以下互相独立的有限审计：

1. 直接在 \(343\) 维群代数中重算每个原子的 19 个删点积，确认
   每个都逐系数等于 \(\Omega\)，完整 19 因子积为零；
2. 用固定基数位置 DP 检查总和、原子性、支撑射影简单性与完整
   4--11 层逃逸集；原子性只需查 1--9 层，因为任一大小 10--18
   的真零和子集都有大小 1--9 的非空零和补集；
3. 对每个非空逃逸代表枚举全部 \(2^{19}\) 个位置子集，逐删点核对
   (13)、(15) 两个集合级补双射、奇补符号、(11)、(12)、(16) 与
   (17)；
4. 对每个三/四重纤维和全部 342 个非零目标逐层核对 (18)，并对
   逃逸目标核对 (23)--(30)。

四个非空逃逸轨道的枚举摘要为

| 轨道 | 逃逸 \(t\) | \(|\mathcal R(t)|\) | \(|\mathcal C(t)|\) | \(\rho=\kappa\) |
|---|---:|---:|---:|---:|
| support7_escape_1 | \((6,5,6)\) | 0 | 469 | 0 |
| support7_escape_2 | \((6,6,6)\) | 0 | 345 | 0 |
| support7_escape_3 | \((6,5,6)\) | 0 | 480 | 0 |
| support7_escape_4 | \((6,0,0)\) | 0 | 345 | 0 |

注意 \(|\mathcal C(t)|\) 是普通整数计数，而 \(\kappa\) 是模 7 的
交错和；二者不应混淆。冻结报告哈希为

```text
4460a569e44cf7753af45550098191611e0ca33db943059c3332eb1f2262592c
```

运行方式：

```text
python verify_p7_maximal_atom_escape_algebra.py
```

脚本通过时会明确输出
`finite regression for general necessary lemmas; no support>=8 closure claim`。

## 5. 搜索接口与停止线

对支撑至少八的规范增广，可以安全加入以下必要剪枝：

- 同一射影点只允许一个支撑标签，但该标签仍可有多重位置；
- 对三/四重纤维用 (18)--(21) 在 \(Q\) 的固定基数层上提前排除
  不可能的逃逸点；
- 对幸存逃逸点施加 (11)--(17) 的逐位置交错和交叉相交约束，并可
  用 (23)--(30) 压缩同纤维的对称位置。

停止线仍是：这些引理只缩小支撑至少八的候选空间。本文没有枚举该
空间，没有证明所有长度 19 原子的逃逸集为空，也没有证明全部
\(p=7,m=3\) 尾系统不可能。
