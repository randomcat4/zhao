# Property B 三尾支持域排除：全新独立复核

STATUS: **CORRECT**

JUSTIFICATION: Reiher 原文中的 cloudy sequence 与本项目的
长度 \(2p-1\) 最小零和位置序列完全同义，Theorem 10.2 确实证明每个
素数具有 Property B，因而每个 \(Q_i\) 都有 simple 支持正规形。
从该正规形独立重建的三类支持域恰好给出证明中的三组四直线；不导入
作者程序的有理数与有限域复算得到 15 个有限线对交、10 个不同候选，
唯一异常特征为 \(2,3,5\)，所以每个素数 \(p\ge7\) 的三域非零交为空。
共同位置的统一投影不可能为零，故 \(p=233\) 精确首片中
\(|K|\ge435\) 立即矛盾。附带的 \(p=233\) 容量—平行仿射线证明也
逐项正确，但已被一般三域定理严格加强。

## 1. 绑定工件

本审计绑定以下冻结字节版本：

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| `proofs/unique_tail_property_b_three_domain_general.md` | 6380 | `f47e796eb2b81611f1fa613539db25e8b137c16cdea4ca22f551d63dd1633016` |
| `unique_tail_property_b_three_domain_general.py` | 6761 | `9fb85c608adaff1a129e2953e85cd886115c1839222b837174832391fed8702f` |
| `unique_tail_property_b_three_domain_general_report.json` | 6542 | `7695f082bf8ee1d6d00db60677377ecea2a2876177055132caaad49eb55963cb` |
| `proofs/unique_tail_p233_property_b_three_atom_exclusion.md` | 6518 | `fd365df8d47f1968c917220e247d5b4644113163857a14aef1006dc0fdfa3eb9` |
| `unique_tail_p233_property_b_three_atom_exclusion.py` | 5082 | `29b85a1012049d00c6fbcf1bed9f2ce13359bc82f0e39d9fe64d218cb2a63217` |
| `unique_tail_p233_property_b_three_atom_exclusion_report.json` | 1979 | `7e78759e6e64039a29a83b0932eae23b3255b97d4adb1f301e6f250caad1e9d6` |
| `verifications/unique_tail_property_b_three_domain_general_independent_check.py` | 7168 | `a3e9afcf4e6c19d07217e894c423458c82bde2c76060d985fb6b1b699e3b5df0` |
| `verifications/unique_tail_property_b_three_domain_general_independent_report.json` | 1907 | `57cb3ff7ba019964b3bafdbeb455edfa677f1a1b8bc2066f094b6d290848c329` |

作者的一般几何报告、\(p=233\) 容量报告和独立报告去掉
`certificate_sha256` 后重新作规范 JSON 哈希，分别复得

```text
93e58bc3fe408bf3990c6fb85d4b82449a5eb59f749d342a071ad4e687ae5ce8
c479944e27b8d76032e8423256a28de784a2190af46550ec666561423eace882
ee9e2ae1deb068f5b58e7ee37fa2dd1c21e0e83bb04fe6a27fad29f9fd27af11
```

与三个文件的内嵌值一致。独立检查器没有导入两个作者模块。

## 2. Reiher 外部定理的对象和方向

独立读取 Christian Reiher 的
[*A Proof of the Theorem According to Which Every Prime Number Possesses
Property B*](https://www.math.uni-rostock.de/math/pub/preprints/preprint/2010/pre10_01.pdf)：

1. 第 2 页先把对象定义为允许重复点的**序列**，不是集合；位置置换与
   \(\mathbb F_p^2\) 的线性自同构保持所讨论性质。这里没有仿射平移。
2. 第 2--3 页把 cloudy sequence 定义为长度 \(2p-1\)、除空位置集和
   全位置集外没有零和位置子列的序列。Fact 3 保证其全列和为零。因此
   它正是 \(C_p^2\) 中长度 \(2p-1=D(C_p^2)\) 的最小零和序列。
3. 同处把 simple 明确定义为经上述线性同构后含 \(p-1\) 个同一标签，
   其余 \(p\) 项全形如 \(h+a_tg\)，其中
   \(h\notin\langle g\rangle\)，且这些项的和为 \(g\)。
4. Theorem 10.2 的结论确为“每个素数具有 Property B”；其证明开头
   明确把这解释为每个奇素数上的 cloudy sequence 都 simple。

因此作者使用的蕴含方向正确：每个 \(Q_i\) 是 cloudy，故存在
\(g_i\ne0\) 与不过原点的仿射线

\[
\Lambda_i=h_i+\langle g_i\rangle,
\qquad
\operatorname{supp}(Q_i)\subseteq\{g_i\}\cup\Lambda_i.
\]

这里 \(g_i\notin\Lambda_i\)，因为前者在子空间
\(\langle g_i\rangle\) 中而后者是该子空间的非零陪集。证明没有把
初始线性因子、射影方向或近极值原子误作这个字面的 \(p-1\) 重标签。
本审计核对了外部定理的陈述、定义和蕴含方向，但没有在仓库中重证
Reiher 的 29 页论证；它仍是明确列出的外部承重依赖。

## 3. 指定尾对的三类支持域确实穷尽

设线性无关的两个指定尾标签为 \(a,b\)，而 simple 支持
\(\{g\}\cup\Lambda\) 同时含它们。由于 \(g\notin\Lambda\)，只有：

1. \(g=a\)，此时 \(b\in\Lambda\)，故
   \(\Lambda=b+\langle a\rangle\)；
2. \(g=b\)，对称地
   \(\Lambda=a+\langle b\rangle\)；
3. \(g\notin\{a,b\}\)，于是 \(a,b\in\Lambda\)，故
   \(b-a\in\langle g\rangle\)，即
   \(g=c(b-a)\) 且
   \(\Lambda=a+\langle b-a\rangle\)，其中 \(c\ne0\)。

这也覆盖了重标签等于某个尾点以及重标签沿两尾差方向的退化。没有
遗漏“重标签也落在仿射线”这一情况，因为 simple 正规形本身排除了
\(g\in\Lambda\)；也没有遗漏 \(g\) 的其他非一倍标量，因为
\(\langle g\rangle=\langle b-a\rangle\) 时已由全部 \(c\ne0\)
穷尽。若某尾标签只是 \(g\) 的非一倍标量，它既不是 \(g\)，又不在
非零陪集 \(\Lambda\)，所以根本不能出现在该 simple 支持中。

对

\[
w_1=e=(1,0),\qquad w_2=f=(0,1),\qquad w_3=(-1,-1)
\]

逐类代入，独立得到

\[
\begin{aligned}
\mathcal D_1&:\ x=-1\ \text{或}\ y=x+1\ \text{或}\
 y=2x\ \text{或}\ y=2x+1,\\
\mathcal D_2&:\ y=-1\ \text{或}\ y=x-1\ \text{或}\
 x=2y\ \text{或}\ x=2y+1,\\
\mathcal D_3&:\ y=1\ \text{或}\ x=1\ \text{或}\
 x+y=0\ \text{或}\ x+y=1.
\end{aligned}
\]

这与作者证明逐行一致。四直线并会形式上包含原点，但原点必须删掉：
若 \(0\) 是任何 \(Q_i\) 的一个位置标签，该单位置就是非空真零和
子列，与最小零和性矛盾。

## 4. 三域空交的独立算术

独立检查器从上面的三类支持构造重新生成支持并，再与四直线方程逐点
比较。它没有读取作者报告中的候选表。\(\mathcal D_1\) 与
\(\mathcal D_2\) 的 16 个线对中，一对在有理数域上平行，其余给出
15 个有限交点；去重后恰有证明式 (9) 的 10 个候选。

对每个非零候选，把 \(\mathcal D_3\) 的四个线性式分别代入；同时
记录前两域交点分母和退化行列式。全部可能异常素因子的并恰为

\[
\{2,3,5\}.
\]

因此当 \(p\ge7\) 时，每个非零候选都避开第三域。唯一落在第三域的
一般候选是 \((0,0)\)，已由原子性排除。直接有限域交叉检查进一步
得到：

| \(p\) | 2 | 3 | 5 | 7 | 11 | 233 |
|---:|---:|---:|---:|---:|---:|---:|
| 非零三交点数 | 3 | 5 | 6 | 0 | 0 | 0 |

特别地，\(p=233\) 时每个支持并有 926 个点，两两交各有 9 个点，
三交为空。这些小素数重算只是对解析异常特征账的交叉检查；一般
\(p\ge7\) 结论来自有理交点和异常素因子审计，不是从有限样本外推。

## 5. 与 \(p=233\) 精确首片的映射

全长七、秩二首片中的三个单点迹端点给出三条长度 465 的投影原子，
并分别字面含尾位置对

\[
(u_2,u_3),\qquad(u_1,u_3),\qquad(u_1,u_2),
\]

其统一投影标签正是
\((f,-e-f),(e,-e-f),(e,f)\)。精确 schema 不是为三个原子另选
私有标签表；同一个实际位置在所有包含它的 \(Q_i\) 中使用同一个
\(C_{233}^2\) 投影标签。

静态首片已有共同字面位置集

\[
K\subseteq Q_1\cap Q_2\cap Q_3,
\qquad |K|\ge435.
\]

任选 \(k\in K\)，其统一标签 \(z\ne0\)，并须同时属于
\(\mathcal D_1,\mathcal D_2,\mathcal D_3\)，与第 4 节矛盾。因此
该子片在投影原子层已经 UNSAT。\(|K|\ge435\) 只用于保证非空；
三泛函矩阵、两两六位置交换、初始二元积、长度八矩形、混合目标、
Hasse 和实际高度在这条闭合中都不是必要前提。

这不推出近极值长度 \(2p-2\) 或 \(2p-3\) 原子的同类分类，也不处理
其他端点长度型；所以它关闭的是当前全长七秩二首片，不是全局
\(A_p\)。

## 6. \(p=233\) 容量证明的交叉审计

`proofs/unique_tail_p233_property_b_three_atom_exclusion.md` 给出一条
更依赖 \(p=233\) 数值、但逻辑独立可读的备份：

1. 每条 \(Q_i\) 的 \(p-1=232\) 重标签在
   \(Q_i\setminus K\) 至多 30 个位置，因此至少 202 个位置落在同一
   \(K\) 中。若三个重标签不同，需要 \(606>465\) 个共同位置，矛盾。
2. 对第 \(i\) 个指定尾对，重标签只能等于某个尾，或平行于尾差。
   独立重算得到三个候选集各长 234，两两交分别仅为
   \(\{w_3\},\{w_2\},\{w_1\}\)，三交为空。
3. 若恰有一对重标签相等，未相等的第三个重标签仍在 \(K\) 中至少
   出现 202 次，因而必须同时落在两条同方向仿射线。三个情形的
   基点差—方向行列式依次为
   \(231,2,231\pmod{233}\)，全非零，所以两线平行且不同，矛盾。

数值界、不等式方向、候选重标签集合、三个行列式和共同位置的统一
标签使用均正确。该证明的结论与一般三域证明一致；后者进一步表明
容量 435 与 \(p=233\) 特定阈值其实都是冗余的。

## 裁定

一般证明及其 \(p=233\) 容量备份均未发现量词弱化、序列与集合混用、
仿射平移偷入、零投影逃逸、支持域漏分支或有限样本外推。相对于明确
列出的 Reiher 外部定理，三尾支持域排除为 **CORRECT**。
