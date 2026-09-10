# 七种共同外部 packing 型的全自动短块、新 (F_3) 与真实交接口

STATUS: PROVED_EXACT_MARKED_INTERFACE /
FORCED_TYPES_REPEATED_TRACE_AXIS_BRANCH_CLOSED /
NO_PACKING_TYPE_CLOSED / FOURTH_BLOCK_NOT_FORCED / GLOBAL_INCOMPLETE

## 1. 范围与本轮结论

只考虑已经冻结的两个三点唯一尾型

\[
(p,\ell,b,r)=(233,7,4,3),\qquad(1399,8,5,3).
\tag{1}
\]

沿用

\[
X=x^{p-4}\subset Z,\qquad Y=Z\setminus X,
\qquad \bar x=q\ne0,\qquad |Y|=2p+8,
\tag{2}
\]

四边端点族 \(\mathcal A\)、有限局部位置集和共同外部位置集

\[
L=U\cup\bigcup_{H\in\mathcal A}H,
\qquad R=Y\setminus L,
\tag{3}
\]

以及一个固定的最大不交投影原子族所给分解

\[
R=P_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}P_t
\mathbin{\dot\cup}K,
\qquad t\le3.
\tag{4}
\]

这里

\[
\rho:C_p^3\longrightarrow C_p^3/\langle q\rangle\cong C_p^2,
\tag{5}
\]

每个 \(\rho(P_i)\) 是零和原子，\(\rho(K)\) 零和自由，并写

\[
\bar\sigma(P_i)=d_iq.
\tag{6}
\]

上一篇已经证明 \((d_i)\) 只有七型

\[
\varnothing,(1),(2),(3),(1,1),(1,2),(1,1,1),
\tag{7}
\]

且对应十四个端点余部分解行。本文不再把外部位置压成一张边缘子集
和表，而恢复自动短块所用的外部位置、补原子内部子集所用的外部位置，
以及两个自动块之间的完整 Venn 单元。

得到三项新结论。

1. 一个三状态逐位置谱精确、同时表示任一自动块的外部部分
   \(F\subseteq R\) 与任一补原子内部子集的外部部分
   \(G\subseteq R\setminus F\)。因此每个新生成的 \(F_3\) 长补原子
   的**全部**内部子集和都可从同一实际 \(R\) 检验，不需要为不同
   \(F_3\) 另配边缘表。
2. 一个四状态逐位置谱精确表示两个自动块的外部部分
   \(F,F'\subseteq R\) 以及 \(F\cap F'\) 的位置、大小和实际和值。
   因此所有含外部位置的块对之间的真实交，以及不同 \(F_3\) 交集
   商和非零条件，都能在同一标签系统内检查。
3. 在三个强制
   \(Q_H=K\dot\cup(L\setminus H)\) 为投影原子的 packing 型
   \((3),(1,2),(1,1,1)\) 中，得到一个严格局部门，并删除旧重复迹
   分支的整个轴向公共交子支。七个 packing 主类型本身均未被关闭。

精确标号接口没有给两个大素数的全部位置赋值，也没有得到联合
UNSAT。因此本稿不宣称第四个不交投影零块必现。

## 2. 全部自动诱导短块

把实际群写为 \(G=C_p^4\)，商映射为

\[
\pi:G\longrightarrow C_p^3,
\tag{8}
\]

并把 \(a\) 规范成核方向。任一 \(Z\)-位置子集唯一写成

\[
D(c,F,E)=X_c\mathbin{\dot\cup}F\mathbin{\dot\cup}E,
\tag{9}
\]

其中

\[
0\le c\le p-4,\qquad F\subseteq R,\qquad E\subseteq L.
\tag{10}
\]

记

\[
n(D)=c+|F|+|E|,\qquad
s(D)=cx+\sigma(F)+\sigma(E).
\tag{11}
\]

统一商标签自动生成的短块不是额外变量，而是所有满足

\[
2\le n(D)\le8,\qquad \pi(s(D))=0
\tag{12}
\]

的三元组。每个这样的三元组必须落入已经冻结的实际和值和长度窗：

\[
s(D)=\lambda a,\qquad
\begin{array}{c|c}
\lambda&I_\lambda\\ \hline
1&[2,6]\\
2&[4,7]\\
3&[6,8].
\end{array}
\tag{13}
\]

若 (12) 成立而 (13) 不成立，实例被拒绝。所有长度

\[
9\le n(D)\le2p+2
\tag{14}
\]

的商零三元组同样被拒绝。这里 \([9,p+1]\) 来自短谱，
\([p+2,2p+2]\) 来自中间商零间隙；两段来源仍保持区分。

若 \(D\) 属于 \(F_3\) 且 \(c>0\)，唯一尾条件给出

\[
\boxed{c=b,\quad F=\varnothing,\quad E=U.}
\tag{15}
\]

所以任何使用共同外部位置的新 \(F_3\) 都必为零核心：

\[
c=0,\qquad6\le|F|+|E|\le8,\qquad
\bar\sigma(F)+\bar\sigma(E)=0,\qquad
\sigma(F)+\sigma(E)=3a.
\tag{16}
\]

式 (9)--(16) 遍历了全部短块，不依赖预选块清单。

## 3. 三状态谱：每个新 (F_3) 补原子的全部内部子和

固定一个自动生成的 \(F_3\) 块 \(D=D(c,F,E)\)。其长商补集为

\[
Z\setminus D
=q^{\,p-(c+4)}W_D,
\qquad
W_D=(R\setminus F)\mathbin{\dot\cup}(L\setminus E).
\tag{17}
\]

前述完整轴向判据说明：该商补集为零和原子，当且仅当对每个

\[
\varnothing\ne
G\mathbin{\dot\cup}J
\subsetneq
(R\setminus F)\mathbin{\dot\cup}(L\setminus E)
\tag{18}
\]

都有

\[
\bar\sigma(G)+\bar\sigma(J)\in\langle q\rangle
\Longrightarrow
\bar\sigma(G)+\bar\sigma(J)
\in\{q,2q,\ldots,(c+3)q\}.
\tag{19}
\]

要同时知道 \(F\) 与 \(G\subseteq R\setminus F\)，每个
\(r\in R\) 必须有且只有三种状态：不用、属于块 \(F\)、属于补原子
内部子集 \(G\)。令每个位置使用独立标记变量，定义

\[
\Theta_R
=\prod_{r\in R}
\left(1+u_r[\gamma(r)]_{F}+v_r[\gamma(r)]_{G}\right),
\tag{20}
\]

其中 \(\gamma(r)\in G\) 是该位置的实际标签，两个群代数坐标分别
累加 \(F,G\) 的和值。因为同一因子中没有 \(u_rv_r\) 项，任一单项式
恰对应且仅对应一个有序不交对

\[
(F,G),\qquad F\subseteq R,\quad G\subseteq R\setminus F.
\tag{21}
\]

独立位置变量又保留了具体支持，而不只是大小与和值。把 (20) 与有限
局部选择 \(E\subseteq L,J\subseteq L\setminus E\) 卷积，便逐项
得到 (18)--(19)。空集与整个 \(W_D\) 由位置单项式唯一识别，因此
两个原子性例外不会和别的同大小、同和值子集混淆。

分解 (4) 在逐位置层面给

\[
\boxed{\Theta_R=\Theta_K\prod_{i=1}^t\Theta_{P_i}.}
\tag{22}
\]

所以七个 packing 型中的所有新 \(F_3\) 共享同一个
\(K,P_1,\ldots,P_t\)，且每个块使用的 \(F\) 与其补原子内部使用的
\(G\) 自动不交。为每个新 \(F_3\) 独立选择一张未标记可达表会丢失
(21)，不是本接口的模型。

## 4. 四状态谱：两个外部块的真实交

取两个自动块

\[
D=D(c,F,E),\qquad D'=D(c',F',E').
\tag{23}
\]

为了知道 \(F,F'\) 的真实交，每个 \(R\)-位置需要四种 Venn 状态：
两块都不用、只属于第一块、只属于第二块、同时属于两块。定义

\[
\Psi_R^{(2)}=
\prod_{r\in R}
\left(
1+\alpha_r[\gamma(r)]_{10}
+\beta_r[\gamma(r)]_{01}
+\chi_r[\gamma(r)]_{11}
\right).
\tag{24}
\]

一个单项式唯一给出三块两两不交的 Venn 单元

\[
R_{10},R_{01},R_{11},
\tag{25}
\]

并恢复

\[
F=R_{10}\dot\cup R_{11},\qquad
F'=R_{01}\dot\cup R_{11},\qquad
F\cap F'=R_{11}.
\tag{26}
\]

故两个尾部的实际交为

\[
(F\cap F')\mathbin{\dot\cup}(E\cap E'),
\tag{27}
\]

其实际和与商和都由 (24) 和有限局部交精确给出。仍有逐位置因式分解

\[
\boxed{\Psi_R^{(2)}=
\Psi_K^{(2)}\prod_{i=1}^t\Psi_{P_i}^{(2)}.}
\tag{28}
\]

在当前两个大素数处，任意两个长度至多八的核心数之和小于
\(p-4\)，所以总能把二者的 \(X\)-位置选成不交。于是冻结的块交
条件要求：

- 每个 \(F_3\) 与每个自动短块的尾部交非空；
- 两个 \(F_2\) 自动块的尾部交非空；
- 两个不同 \(F_3\) 的交集商和非零。

对两个含外部位置的零核心 \(F_3\)，最后一条精确写为

\[
\boxed{
\pi\!\left(
\sigma(R_{11})+\sigma(E\cap E')
\right)\ne0.}
\tag{29}
\]

特别地，对新零核心 \(F_3=D(0,F,E)\) 与选中端点
\(H\subseteq L\)，有

\[
D\cap H=E\cap H,
\tag{30}
\]

所以必须对**每一个** \(H\in\mathcal A\) 检查

\[
E\cap H\ne\varnothing,\qquad
\boxed{\pi(\sigma(E\cap H))\ne0.}
\tag{31}
\]

旧式只要求普通非空交；(31) 补回了新 \(F_3\) 与全部端点之间的
非零商交。对两个都使用外部位置的新块，则必须使用 (24)，不能从
两张边缘谱推断 \(R_{11}\) 存在或不存在。

## 5. 三个强制 (Q_H) 原子型的局部门

在 packing 型

\[
(3),\qquad(1,2),\qquad(1,1,1)
\tag{32}
\]

中，上一篇已经证明对每个端点 \(H\in\mathcal A\)，

\[
Q_H=K\mathbin{\dot\cup}(L\setminus H)
\tag{33}
\]

是 \(C_p^2\) 的投影零和原子，且

\[
\bar\sigma(Q_H)=q.
\tag{34}
\]

**引理 1（有限局部零子集门）。** 若
\(\varnothing\ne E\subseteq L\setminus H\) 且

\[
\rho(\bar\sigma(E))=0,
\tag{35}
\]

则必有

\[
\boxed{K=\varnothing,\qquad E=L\setminus H.}
\tag{36}
\]

反之，(36) 时 \(E=Q_H\) 是允许的整个原子，而不是真零和子集。

**证明。** \(E\) 是投影原子 \(Q_H\) 的非空投影零子集。原子定义
迫使 \(E=Q_H\)。但 \(E\subseteq L\setminus H\) 不含任何
\(K\)-位置，所以 \(K=\varnothing\)，继而
\(E=L\setminus H\)。反向由定义立即成立。证毕。

这个整体例外必须在投影层保留。若它进一步与若干 \(X\)-位置组成
长度至多八的实际自动短块，则该短块的尾仍与零核心端点 \(H\) 不交，
会被第 4 节的真实块交条件另行拒绝；不能在证明引理 1 时提前把两种
不同层级混为一谈。

引理 1 还给新零核心 \(F_3\) 一个条件门。设
\(D=D(0,F,E)\ne H\)，并且它不使用任何 \(P_i\)-位置，即

\[
F\subseteq K.
\tag{37}
\]

若

\[
\rho(\bar\sigma(D\cap H))=0,
\tag{38}
\]

则 \(D\setminus H\subseteq Q_H\) 是非空投影零子集，故

\[
\boxed{D\setminus H=Q_H.}
\tag{39}
\]

因此

\[
F=K,\qquad E\setminus H=L\setminus H,\qquad
|Q_H|\le7,\qquad
\bar\sigma(D\cap H)=-q.
\tag{40}
\]

若 \(D\) 使用某个 \(P_i\) 的位置，\(D\setminus H\) 不再包含于
\(Q_H\)，不得套用 (39)。完整接口仍由 (20)--(31) 检查这种分支。

## 6. 端点交换门与重复迹轴向支的删除

**引理 2（强制型端点交换门）。** 处于 (32) 的任一型。对不同
端点 \(H,J\in\mathcal A\)，有双向等价

\[
\boxed{
\rho(\bar\sigma(H\cap J))=0
\Longleftrightarrow
K=\varnothing\text{ 且 }L=H\cup J.}
\tag{41}
\]

在任一方向成立时，并且

\[
\rho(H\setminus J),\ \rho(J\setminus H)
\text{ 都是系数一的投影原子},
\tag{42}
\]

\[
\bar\sigma(H\setminus J)=
\bar\sigma(J\setminus H)=q,\qquad
\bar\sigma(H\cap J)=-q.
\tag{43}
\]

**证明。** 令 \(C=H\cap J\)。因为两个不同块有相同实际和值，
且 \(Z\) 是实际原子，所以 \(H\setminus J,J\setminus H\) 均非空。
由 \(\rho(\bar\sigma(C))=0\) 和 \(\bar\sigma(H)=0\)，

\[
\rho(\bar\sigma(H\setminus J))=0.
\]

又 \(H\setminus J\subseteq L\setminus J\subseteq Q_J\)。
\(Q_J\) 是投影原子，故

\[
H\setminus J=Q_J=K\dot\cup(L\setminus J).
\]

左端不含 \(K\)-位置，所以 \(K=\varnothing\)，且
\(L\setminus J=H\setminus J\)，即 \(L=H\cup J\)。交换
\(H,J\) 得到另一花瓣等式。最后 (34) 给两花瓣商和均为 \(q\)，
再由端点总商和为零得到公共交商和 \(-q\)。这证明正向。反之，若
\(K=\varnothing,L=H\cup J\)，则
\(H\setminus J=L\setminus J=Q_J\)，由 (34) 得其商和为 \(q\)；
再减去 \(\bar\sigma(H)=0\)，得到
\(\bar\sigma(H\cap J)=-q\)，故其 \(\rho\)-投影为零。证毕。

若 \(H,J\) 有相同尾迹

\[
H\cap U=J\cap U\subsetneq U,
\tag{44}
\]

则 \((H\cup J)\cap U\subsetneq U\)。但 \(U\subseteq L\)，这与
(41) 矛盾。因此三个强制 packing 型中

\[
\boxed{
H\cap U=J\cap U
\Longrightarrow
\rho(\bar\sigma(H\cap J))\ne0.}
\tag{45}
\]

旧四边二分支把重复迹公共部进一步分成轴向和非轴向。轴向恰等价于
其 \(\rho\)-投影为零，故 (45) 删除了三个强制型里的整个重复迹
轴向子支。重复迹非轴向支仍存活；其他四个 packing 型也不能使用
引理 2。

更一般地，强制型中任何轴向端点对都必须满足尾迹并覆盖 \(U\)，
且只能取 (43) 的系数 \(-1\)。若两迹不交，已有外部交投影引理又
强迫公共交非轴向，所以单点迹 \(s_i=\{u_i\}\) 与其补二点迹
\(d_i=U\setminus\{u_i\}\) 的覆盖对也被排除。在六种非空真迹中，
轴向端点对唯一仍可能的尾迹型是

\[
\boxed{d_i,d_j\quad(i\ne j).}
\tag{46}
\]

式 (46) 只是精确幸存迹型，不是可实现性证明。

## 7. 可执行接口与有限回归

配套程序为
`unique_tail_seven_type_full_f3_interface.py`。默认运行做四件事。

1. 独立重建七个 packing 型、十四个端点余部分解行和三个强制
   \(Q_H\) 原子型。
2. 在十二个小型实际位置序列上，逐三状态展开 (20)，并与直接穷举
   全部有序不交对 \((F,G)\) 逐位置、逐大小、逐和值比较。
3. 在同十二例上，逐四状态展开 (24)，并与直接穷举全部有序子集对
   \((F,F')\) 的两个支持、交支持、三个大小和三个和值比较。
4. 在 \(C_3^2\) 中穷举长度至多五的全部有序投影原子，遍历
   \(Q=K\dot\cup E_0\) 的所有位置分区，直接核对引理 1 的整体例外。

默认输出为

```text
packing_type_count = 7
expanded_endpoint_row_count = 14
forced_q_type_count = 3
marked_spectrum_small_case_count = 12
forced_local_gate_atom_count = 1073
type_sha256 = ab485b1affe4916404af0fe0d659f709a6f85eb98a7beccf14bc6091f672301a
certificate_sha256 = 9dfe70ad3c9693d5048b3deb4ec28d12c990e98bf62aff6612494ed65d11ccd5
```

三状态与四状态累计分别检查 4,212 与 21,504 个逐位置记录。局部门
穷举 1,073 个原子、27,057 个允许的 \(K\)-局部分区；出现的 1,073
个局部投影零子集全部且仅为 \(K=\varnothing\) 时的整个 \(Q\)。
这些小例只回归一般乘法恒等式和原子定义；一般证明分别是第 3--6 节
的逐位置乘法与原子极小性论证。

程序的 `--instance FILE` 模式要求提供两个大素数之一的全部统一
\(Y\)-标签、端点、四条边、\(L,R,P_i,K\) 和 packing 系数。它先
检查：

- 四条实际边共享同一非轴位置；
- 每个端点确为零核心 \(F_3\)；
- \(P_i,K\) 是同一 \(R\) 的实际位置分区；
- 每个 \(P_i\) 为投影原子、\(K\) 投影零和自由；
- 三个强制型中的每个 \(Q_H\) 确为投影原子。

随后调用已经独立审计通过的严格标号核验器，从同一标签重新生成
全部长度二至八短块，并检查全部一点、二点、三点 Hasse 行、中间
禁区、实际 \(Z\) 原子、每对真实块交以及每个派生 \(F_3\) 的长补
原子全部内部子和。因此 `--instance` 若终止并通过，得到的是一个
`EXACT_LABELLED_LOCAL_CANDIDATE`，仍不是冻结反例。

本轮没有提供也没有运行一个完整 \(p=233\) 或 \(p=1399\) 实例；
这两个规模上的直接组合枚举预计极大。默认有限证书绝不能解释成这
两个素数上的 SAT 或 UNSAT。

## 8. 精确停止线

**PROVED：**式 (20) 的三状态逐位置谱对每个新 \(F_3\) 同时保留
其外部支持与补原子内部外部支持；式 (24) 的四状态谱同时保留两个
外部块及其真实交。两者都按同一个 \(K,P_i\) 分解因式化。

**PROVED：**式 (31) 补齐每个新零核心 \(F_3\) 与每个端点的非零
商交；式 (29) 补齐两个外部 \(F_3\) 之间的真实交。式 (18)--(19)
逐块检查每个新 \(F_3\) 长补原子的全部内部子和。

**PROVED：**三个强制 packing 型满足局部门和端点交换门；其中重复
迹公共交轴向子支不可能。整体例外
\(K=\varnothing,E=L\setminus H\) 已在投影层显式保留。

**NOT PROVED：**七个 packing 主类型中的任一型不可实现；共同
\(R\) 必含第四个不交投影零块；或存在通过完整标号接口的实际
\(R\)。外部逐位置 Hasse 约束虽由 `--instance` 核验器保留，但没有
进行两个大素数的全量求解。

**OUT OF SCOPE：**\(Z\) 外位置、承重删除 (TOP)/(CONST) 和最终
\(S\) 的全部窗口。

因此本轮把旧接口遗漏的三类真实位置信息全部补回，并严格删除一个
强制型子支，但没有得到联合 UNSAT。全局状态继续为 **INCOMPLETE**。
