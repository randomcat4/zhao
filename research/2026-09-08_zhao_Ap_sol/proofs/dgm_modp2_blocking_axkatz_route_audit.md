# DGM、模 \(p^2\)、blocking set 与 Ax--Katz 路线审计

STATUS: **APPLICABLE CONDITIONAL LEMMAS / TWO HARD BOUNDARIES /
GLOBAL INCOMPLETE**

## 1. DGM 与 setpartition 的准确入口

DeVos--Goddyn--Mohar 定理的序列推论允许重复群元素；重复副本按不同
位置计数。若 \(L\) 是有限阿贝尔群 \(G\) 上的位置序列，
\(H=\operatorname{stab}\Sigma_n(L)\)，则

\[
|\Sigma_n(L)|\ge |H|
\left(1-n+\sum_{Q\in G/H}\min\{n,\nu_Q(L)\}\right).
\tag{1}
\]

来源为 DeVos--Goddyn--Mohar, Theorem 1.3 与 Corollary 1.5：
<https://www.sfu.ca/~mohar/Reprints/2009/BM09_AM220_DeVos_KneserAdditionTh.pdf>，
DOI <https://doi.org/10.1016/j.aim.2008.11.003>。

Grynkiewicz 的 Partition Theorem 要求选取 \(S'\mid S\) 且
\(h(S')\le n\le|S'|\)。每个 part 自身是集合，但同一个群元素可在
不同 parts 中出现，所以 underlying sequence 仍可有重。可核对
*Iterated Sumsets and Setpartitions*, Theorem E：
<https://diambri.org/IteratedSumsetsI-i.pdf>；其引用的书中版本为
*Structural Additive Theory*, Theorem 14.1：
<https://link.springer.com/book/10.1007/978-3-319-00416-7>。

对 \(C_p^2\) 中零和自由的 \(L\)，若 \(H\) 是一条线，则
\(0\notin\Sigma_n(L)\) 及 \(H\)-周期性给
\(|\Sigma_n(L)|\le p^2-p\)。由 (1)，

\[
\sum_{Q\in G/H}\min(n,\nu_Q(L))\le p+n-2,
\tag{2}
\]

即

\[
\boxed{
\sum_Q(\nu_Q(L)-n)_+\ge |L|-p-n+2.}
\tag{3}
\]

用于当前三类共同核序列，得到严格条件门：

\[
\begin{array}{c|c|c}
L&n&H\text{-陪集强迫容量}\\ \hline
|C|=2p-5&p-4&\ge p-3\\
|N_i|=2p-4&p-3&\ge p-2\\
|B_i|=2p-3&p-2&\ge p-1.
\end{array}
\tag{4}
\]

在 \(p=233\) 时三个阈值为 230、231、232。对完整长度
\(5p-4\) 的假想 \(A_p\) 反例，若
\(H=\operatorname{stab}\Sigma_{p+1}(S)\) 是三维超平面，同理至多一个
\(H\)-陪集达到截断值，而它必须含至少

\[
\boxed{4p-2}
\tag{5}
\]

个位置。

### DGM 的硬边界

式 (3)--(5) 都以“稳定子非平凡”为前提，现有 complete 性不能推出
该前提。仓库已经审计的无限族

\[
Q=f^{p-1}e^{p-3}(2e)(e+f)
\tag{6}
\]

删去 \(e+f\) 后得到长 \(2p-3\)、complete 且零和自由的

\[
B=f^{p-1}e^{p-3}(2e).
\tag{7}
\]

但

\[
\begin{aligned}
\Sigma_{p-2}(B)
={}&\{(a,p-2-a):0\le a\le p-3\}\\
&\cup\{(a+2,p-3-a):0\le a\le p-3\}
\end{aligned}
\tag{8}
\]

是两条截短平行线，平移稳定子严格平凡。故不能把“近最大 complete”
升级成 DGM 的非平凡稳定子分支。DGM 还只控制固定长度可达目标集合，
不直接给指定目标的表示次数或不同长度表示的粘合。

## 2. 模 \(p^2\) 的逐位置系数

对完整假想反例 \(S\) 的位置 \(i\)，令

\[
T_i=S\setminus\{g_i\},\qquad |T_i|=5(p-1),
\tag{9}
\]

并记

\[
d_{i,k}=\#\{W\subseteq S:i\in W, |W|=k, \sigma(W)=0\}.
\tag{10}
\]

从已经证明的

\[
F_{T_i}\equiv-pc(T_i)J\pmod {p^2}
\tag{11}
\]

取 \(X^{-g_i}\) 系数，严格得到

\[
\boxed{
\sum_{k=3p-1}^{4p-3}(-1)^{k-1}d_{i,k}
\equiv-pc(T_i)\pmod {p^2}.}
\tag{12}
\]

下端来自反例的短谱；若允许的零和非原子，它会分成两个长度至少
\(3p-1\) 的零和块，总长超过 \(5p-4\)，故它实际为原子，再由
\(D(C_p^4)=4p-3\) 得上端。

在 \(p=233\) 时，(12) 混合从 698 到 929 的全部 232 个长度层。
所以它的确第一次把非单位系数、逐位置和真实群元素接在一起，但不是
单独的“过位置 \(i\) 的 \(3p\)-atom 数”。当前商 \(C_p^2\) 标签也
不能决定依赖完整 \(C_p^4\) 向量的 \(c(T_i)\)。

## 3. projective blocking 的正确单向推论

令 \(\mathcal S(T)\subset PG(3,p)\) 为 projective support，

\[
H_t=\{[x]:\langle t,x\rangle=0\}.
\]

则

\[
c(T)=-\sum_{\substack{[t]\in PG(3,p)\\
H_t\cap\mathcal S(T)=\varnothing}}
\prod_j\langle t,g_j\rangle.
\tag{13}
\]

因此“只有避开支撑的平面有贡献”和

\[
\mathcal S(T)\text{ 阻塞全部平面}\Longrightarrow c(T)=0
\tag{14}
\]

都正确。Bose--Burton 只给 plane-blocking 点集至少有 \(p+1\) 点，
等号恰为 projective line：
<https://doi.org/10.1016/S0021-9800(66)80007-8>。因当前 \(T_i\) 至少
张成三维，等号支被排除后也只提升为支撑至少 \(p+2\)。这远未分类
任意大小、任意权的 blocking support。

反向

\[
c(T)=0\Longrightarrow\mathcal S(T)\text{ blocking}
\tag{15}
\]

为假。即使在 \(p=233\)、长度 1160、秩四、单个实际值重数至多
229 的放宽层，取

\[
\begin{aligned}
T={}&e_1^{229}(2e_1)^2e_2^{229}(2e_2)^4
e_3^{229}(2e_3)^3\\
&\cdot e_4^{229}(2e_4)^{229}(3e_4)^6.
\end{aligned}
\tag{16}
\]

四个 projective 方向的总指数为 \((231,233,232,464)\)，域内求和
使 \(c(T)=0\)；但平面 \(x_1+x_2+x_3+x_4=0\) 避开四个坐标支撑点。
因此必须显式保留不同避开平面的带权贡献及其抵消。

Minihyper 分类还要求已知最小平面权、minimality 或特殊
\(\{f,m;3,q\}\) 参数；当前只有总权 \(5(p-1)\)，不满足直接套用
条件。典型参数和定义可核对：
<https://lematematiche.dmi.unict.it/index.php/lematematiche/article/view/176>。

## 4. Ax--Katz 加细为何在 dense 五式仍只给一层

标准选择变量编码是

\[
f_0=\sum_i z_i^{p-1},\qquad
f_j=\sum_i(g_i)_jz_i^{p-1}\quad(1\le j\le4),
\tag{17}
\]

共有 \(N=5p-4\) 个变量和五个次数 \(p-1\) 的方程。Ax--Katz 指数为

\[
\left\lceil{N-5(p-1)\over p-1}\right\rceil=1.
\tag{18}
\]

Moreno--Moreno 的 \(p\)-weight 也因
\(\operatorname{wt}_p(p-1)=p-1\) 仍为一层。可核对
*Handbook of Finite Fields*, Theorems 7.1.46、7.1.48：
<https://archive.ymsc.tsinghua.edu.cn/pacm_download/672/12637-dingjt-p2.pdf>。

在反例短谱下，零点数为

\[
1+(p-1)^{3p}Z_{3p}(S),
\tag{19}
\]

所以 (18) 只重得 \(Z_{3p}(S)\equiv1\pmod p\)。dense Cayley--Newton
多面体的最小 dilation 为 6，Adolphson--Sperber 同样只给
\(p^{6-5}=p\)。原始 Newton 多面体界见
<https://www.numdam.org/articles/10.24033/asens.1543/>。

要多得一层，必须证明额外稀疏性。例如经五式的可逆行变换后，若
存在 \(r\) 条方程合计只触及

\[
s\le(r-1)(p-1)
\tag{20}
\]

个位置变量，则 Newton 参数可升到至少 7。最简单的特例是增广列
\((1,g_i)\) 行秩至多四，即 \(S\) 落入仿射超平面；当前冻结前提
并未给出这种退化。

## 5. 参数化 Farkas 的作用域

旧 \(p=5\) 投影证书的 214,758 次特征重算属于平方自由终支，并使用
无比例对、无三项等差、投影截面上界以及 \(p=5\) 专属局部下界。
到 \(p=7\)，假想反例仍可有三重实际值；比例、等值和 AP 修正项都
必须保留。现有一般重写只参数化了 18 个低阶特征族，并没有参数化
最终 Farkas 乘子，也没有提供与其相撞的一般局部下界。

所以重解 \(p=7\) 放宽 LP 仍有诊断价值，但“乘子对齐”之前必须先
统一合法轮廓域、修正项和目标下界。单纯比较 \(p=5,7\) 两组数值
乘子不能成为 \(A_p\) 的全称证书。

## 6. 可执行结论

1. DGM 只在候选的 \(\Sigma_n\) 稳定子被实际证明非平凡时启用
   (4)--(5)；complete 性不作替代。
2. 模 \(p^2\) 必须加载完整四维标签并保留 (12) 的整条交错长度向量。
3. blocking 编码必须同时记录全部避开平面及带权乘积，禁止使用
   错误逆推 (15)。
4. Ax--Katz 只继续搜索行变换后的真实稀疏 incidence；dense 五式
   已精确到达其一层边界。

四条路线均已形成可复用接口，但没有一条单独关闭当前 \(m=3\) 层或
全局 \(A_p\)。
