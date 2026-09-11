# \(p=233\) 三长八 \(O_3\) 的仿射子空间全扫设计

STATUS: **PROVED_ALGORITHM / PROTOTYPE / GLOBAL_INCOMPLETE**

## 1. 目标与作用域

固定

\[
p=233,
\qquad
w_1=(1,0),\quad w_2=(0,1),\quad w_3=(-1,-1),
\tag{1}
\]

以及三个 singleton 均长八、\(m=4\) 的掩码轨

\[
O_3=(2,2,2,2).
\tag{2}
\]

已有的联合删点前沿把共同核写成 \(|C|=460\)，并把三个二位置
fringe 参数化为

\[
F_i=\{w_j,w_k,\tau-z_i,\tau+w_i+z_i\},
\qquad \{i,j,k\}=\{1,2,3\}.
\tag{3}
\]

若固定完整 quartic 状态

\[
(\tau,z_1,z_2,z_3,q),
\tag{4}
\]

并记使完整联合删点系统相容的标签集合为 \(\Gamma_q\)，则

\[
\operatorname{supp}\rho(C)\subseteq\Gamma_q,
\qquad
460\le232|\Gamma_q|.
\tag{5}
\]

所以 \(|\Gamma_q|\le1\) 会严格排除式 (4)。

本文给出一个不展开高维 \(q\)-纤维、也不枚举
\(z_1\times z_2\times z_3\) 的全扫设计。它包含两个已经实际运行的
精确原型：

1. 在 \(\tau=(17,31)\) 上，用十二次 minor 的逐 \(x\) 切片恢复三个
   端点的全部 \(9,11,13\) 个定向 \(z\)；
2. 在 \(\tau=(0,1)\) 上，把全部 \(54\,288\) 个非零删点标签
   \(g\) 对偶成 \(q\)-平面中的仿射子空间，精确得到
   empty/point/line/plane 分布
   \(54\,058/224/4/2\)。

本文证明算法接口和两个原型，不声称已经运行全部 generic
\(\tau\)，不声称关闭 \(O_3\)。

## 2. generic 尾层是一个归一化仿射 \(q\)-平面

按基

\[
\mathcal E_4=
\langle1,x^2,xy,y^2,x^4,x^3y,x^2y^2,xy^3,y^4\rangle
\tag{6}
\]

记 \(T_\tau\) 为六个尾邻点

\[
\tau\pm w_1,\quad\tau\pm w_2,\quad\tau\pm w_3
\tag{7}
\]

的评价矩阵。已经穷尽得到：\(54\,276\) 个非零 \(\tau\) 满足
\(\operatorname{rank}T_\tau=6\)，只有十二个点降到秩五；降秩点已在
联合删点前沿中单列处理。因此本设计把

\[
\operatorname{rank}T_\tau=6,
\qquad
\operatorname{rank}\binom{T_\tau}{L_\tau}=7
\tag{8}
\]

称为 generic 尾层。

取

\[
V_\tau=\ker T_\tau,
\qquad \dim V_\tau=3.
\tag{9}
\]

在 \(V_\tau\) 中选 \(q_0,q_1,q_2\)，使

\[
L_\tau q_0=1,
\qquad
L_\tau q_1=L_\tau q_2=0.
\tag{10}
\]

所有满足尾六点及 \(q(\tau)=1\) 的偶四次恰写成

\[
\boxed{q(u,v)=q_0+u q_1+v q_2,\qquad (u,v)\in\mathbb F_{233}^2.}
\tag{11}
\]

关键是始终把式 (11) 保持为二维仿射空间，而不是对每个四点块展开
其中的 \(233\) 或 \(233^2\) 个 \(q\)。

尾 \(S_3\) 作用把这 \(54\,276\) 个 generic 点压成

\[
9\,161\text{ 个轨：}qquad
8\,931\text{ 个六点轨}+230\text{ 个三点轨}.
\tag{12}
\]

三个独立内部换位

\[
z_i\longmapsto-w_i-z_i
\tag{13}
\]

还可在每个端点把定向 \(z_i\) 两两配对；其唯一不动点为
\(-w_i/2\)。

## 3. 每个四点块保存为规范仿射子空间

固定端点 \(i\)，并写

\[
Z_i(z)=\{z,z+w_i,z-w_j,z-w_k\}.
\tag{14}
\]

把式 (11) 代入四个条件 \(q|_{Z_i(z)}=0\)，得到

\[
A_i(z)\binom uv=b_i(z),
\tag{15}
\]

其中 \(A_i(z)\) 有两列、四行。对增广矩阵

\[
B_i(z)=
\begin{pmatrix}
q_1(t)&q_2(t)&-q_0(t)
\end{pmatrix}_{t\in Z_i(z)}
\tag{16}
\]

作规范 RREF。式 (15) 的解集只能是以下四型之一：

\[
\boxed{
\varnothing,\quad
\text{一点 }(u,v),\quad
\text{一条仿射线 }\alpha u+\beta v=c,\quad
\mathbb A^2.}
\tag{17}
\]

算法保存式 (17) 的 RREF 键及产生它的所有字面 \(z\)，不展开线或
整平面中的点。点型分支也可用 Plücker 形式实现：若
\(\operatorname{rank}B_i(z)=2\)，取两条独立行的叉积；只有其第三
坐标非零时式 (15) 相容，再把第三坐标归一化为一，所得前两坐标就是
\((u,v)\) 的唯一哈希键。

generic quartic 子层指式 (17) 中所有 compatible 四点块均为点型。
在该层，三个端点只需对 point key 作三路哈希交。相同 \(q\) 下可以
保存三张 \(z\)-列表，完全不需要展开它们的笛卡尔积。

下文简记

\[
\mathcal Z_i(q):=\{z\in\mathbb F_{233}^2:q|_{Z_i(z)}=0\},
\]

以免把固定共同 \(q\) 的可行中心集合与四点块 \(Z_i(z)\) 混淆。

## 4. 十二次 minor 的逐 \(x\) 切片

直接枚举每个 \(\tau\) 的全部 \(p^2\) 个 \(z\) 仍然偏重。式 (16)
的四个 \(3\times3\) minor 记为

\[
m_1(z_x,z_y),\ldots,m_4(z_x,z_y).
\tag{18}
\]

每个矩阵元是 \(z\) 的总次数至多四的多项式，所以

\[
\deg m_a\le12.
\tag{19}
\]

式 (15) 相容必先满足

\[
m_1=m_2=m_3=m_4=0.
\tag{20}
\]

因此固定一个 \(x\in\mathbb F_{233}\) 后，只需在十三个不同的
\(y\) 上评价式 (18)，即可精确插值得到四个次数至多十二的一元
多项式。取其最大公因式

\[
h_x(Y)=\gcd(m_1(x,Y),\ldots,m_4(x,Y)).
\tag{21}
\]

所有候选 \(y\) 都是 \(h_x\) 的有限域根。生产版可计算

\[
\gcd(h_x(Y),Y^{233}-Y)
\tag{22}
\]

并用 Berlekamp 或 Cantor--Zassenhaus 精确分解这个次数至多十二的
多项式。得到根后仍须回到式 (15)，逐点检查

\[
\operatorname{rank}A_i(z)=\operatorname{rank}B_i(z),
\tag{23}
\]

因为仅有 \(\operatorname{rank}B_i(z)\le2\) 还不保证仿射相容。

若四个切片 minor 全部是零多项式，则把该 \(x\) 标成
all-zero slice，并对它的 233 个 \(y\) 作式 (23)；不得把零
多项式的 gcd 当成“无根”。大量 all-zero slice 意味着正维
\(z\)-退化簇，应退出 generic 通道并输出异常证书。

### 4.1 已运行的切片原型

在 \(\tau=(17,31)\) 上，三个端点分别得到

\[
\boxed{9,\quad11,\quad13}
\tag{24}
\]

个 compatible oriented \(z\)，并且三个端点的 all-zero vertical
slice 数均为零。具体坐标已完整写入 JSON 报告；它们逐项等于此前
直接扫描 \(233^2\) 个 \(z\) 的目录。

当前最小原型为保持简单，在得到 \(h_x\) 后直接测试 233 个
\(y\)，但 determinant 只在十三个插值点上计算；这不影响精确性。
生产版采用式 (22) 才得到按 \(p\) 渐近的切片加速。

## 5. 三路点/线/平面的符号交

不能假定所有 compatible 块永远是点型。对式 (17) 的四类键可按
以下规则作三路交。

1. 平面键是交运算的单位元。
2. 对每个点键，查询另两个端点的点表以及包含该点的线键。
3. 两条不平行线产生一个点；把该点拿到第三个端点作 membership
   查询。
4. 两条相同线的交仍是该线。它与第三端点的不平行线产生点；与
   相同线或平面相交时，保留为一条符号 \(q\)-线。

线键统一规范成

\[
au+bv=c,
\quad\text{其中 }(a,b)\text{ 的首个非零坐标归一化为一}.
\tag{25}
\]

从而相同线可直接哈希。若三个端点留下共同 \(q\)-线，可写

\[
q(\lambda)=q_*+\lambda q_1
\tag{26}
\]

并把 \(\lambda\) 作为后续线性系统中的一个变量，而不是展开 233
个 \(q\)。共同 \(q\)-平面亦同理保留 \((u,v)\)。

线族两两求交的严格最坏复杂度是输出敏感的。若某端点出现
\(\Theta(p^2)\) 条不同 compatible 线，直接 line-pair join 可达到
\(\Theta(p^4)\) 每 \(\tau\)。因此实现必须记录线型数量，并把大线
族列作异常层；没有额外结构定理时不能把它隐藏在统一
\(O(p^3)\) 声明中。

## 6. 把删点标签对偶成 \(q\)-平面中的子空间

固定非零候选核标签 \(g\)。删除一个标签为 \(g\) 的共同核位置后，
奇五次 \(D\) 满足

\[
D(s+g/2)-D(s-g/2)=q(s).
\tag{27}
\]

在以 \(g\) 为第一坐标方向、\(Y\) 为横向坐标的基下，中心差分的
核为

\[
\langle Y,Y^3,Y^5\rangle.
\tag{28}
\]

因式 (11) 中 \(q\) 对 \((u,v)\) 线性，可以选择同样线性依赖于
\((u,v)\) 的特解：

\[
D=D_{00}+uD_{01}+vD_{02}+AY+BY^3+CY^5.
\tag{29}
\]

先只加入与 \(z_i\) 无关的七个删点行：

\[
D(\tau+g/2)=1,
\qquad
D(\tau+g/2\pm w_i)=0\quad(i=1,2,3).
\tag{30}
\]

这是变量 \((u,v,A,B,C)\) 的 \(7\times5\) 仿射线性系统。把
\((A,B,C)\) 消去后，得到

\[
\mathcal H_{\tau,g}
=\{(u,v):\exists A,B,C\text{ 使式 (30) 成立}\}
\subseteq\mathbb A^2.
\tag{31}
\]

线性空间的投影仍是仿射子空间，所以式 (31) 同样只有
empty/point/line/plane 四型。一个稳定的实现不需要对五列作变量
顺序敏感的消元：令 \(M_K\) 为式 (30) 的 \((A,B,C)\) 三列，取
\(M_K^T\) 的零空间。每个左零向量作用到 \((u,v)\) 两列和右端，
即得到式 (31) 的完整规范方程。

对固定共同 \(q=q(u,v)\)，纯尾删点候选集合是

\[
\Gamma_q^{\rm tail}
=\{g:(u,v)\in\mathcal H_{\tau,g}\}.
\tag{32}
\]

完整集合满足 \(\Gamma_q\subseteq\Gamma_q^{\rm tail}\)。因此

\[
|\Gamma_q^{\rm tail}|\le1
\Longrightarrow
|\Gamma_q|\le1
\tag{33}
\]

会一次删除该 \(q\) 下的所有 \(z_1,z_2,z_3\)，甚至无需读取非尾
fringe 行。

这里始终固定同一个共同 \(q\)。若尚未固定 \(q\)，式 (31) 是
\(q\)-平面中的 incidence 目录；不能把不同 \(q\) 所允许的两个
\(g\) 合并成同一 \(\Gamma_q\)。

### 6.1 已运行的对偶原型

在 \(\tau=(0,1)\) 上，对全部 \(54\,288\) 个非零 \(g\) 精确建立
式 (31)，得到

\[
\boxed{
\begin{array}{c|rrrr}
\mathcal H_{\tau,g}\text{ 类型}
&\varnothing&\text{point}&\text{line}&\text{plane}\\ \hline
\#g&54\,058&224&4&2.
\end{array}}
\tag{34}
\]

该层的两个共同归一化 quartic 为

\[
\begin{aligned}
q_A&=(0,39,115,79,194,195,232,156,155),\\
q_B&=(0,0,193,79,0,117,232,156,155),
\end{aligned}
\tag{35}
\]

系数顺序如式 (6)。对式 (34) 的子空间作 membership 查询，两个
quartic 都恰命中

\[
\boxed{g=(1,2),\quad(-1,1)=(232,1).}
\tag{36}
\]

这只与**纯尾限制**下逐 \(q\)、逐 \(g\) 的直接 fixed-\(q\) 扫描
一致，并没有为四个 line 键或两个 plane 键展开其中的所有 \(q\)。
式 (36) 只是纯尾必要门，不能冒充完整 fringe 扫描：加入完整 fringe
行后，两个对应具体状态分别只余一个 \(g\)，再由式 (5) 删除。

## 7. 固定 \(q\) 后不展开三重 \(z\) 的容量搜索

通过式 (33) 后，只处理满足

\[
|\Gamma_q^{\rm tail}|\ge2
\tag{37}
\]

的固定共同 \(q\)。对每个 \(g\in\Gamma_q^{\rm tail}\)、端点 \(i\)
和 \(z\in\mathcal Z_i(q)\)，把该端点 fringe 的十五个非空字面子集行加入
式 (30)。在 generic deletion 子层，这些行把 \((A,B,C)\) 唯一
固定成一点，记为

\[
a_{i,z,g}\in\mathbb F_{233}^3;
\tag{38}
\]

不相容时记为空。

要判断某个三块状态是否同时允许两个不同标签 \(g,h\)，定义

\[
R_i(g,h)=
\{(a,b):\exists z\in\mathcal Z_i(q),
a=a_{i,z,g},\ b=a_{i,z,h}\}.
\tag{39}
\]

则有严格等价

\[
\boxed{
\exists(z_1,z_2,z_3)\text{ 同时允许 }g,h
\iff
R_1(g,h)\cap R_2(g,h)\cap R_3(g,h)\ne\varnothing.}
\tag{40}
\]

右向左时，交中的同一个 \((a,b)\) 分别在三个端点选出
\(z_1,z_2,z_3\)；\(a\) 保证标签 \(g\) 的同一奇五次在三个端点
成立，\(b\) 对 \(h\) 同理。左向右立即给出这个公共 \((a,b)\)。

所以寻找 \(|\Gamma_q|\ge2\) 的状态只需对 \((g,h)\) 建三张关系
哈希表，不必物化 \(\mathcal Z_1(q)\times\mathcal Z_2(q)\times
\mathcal Z_3(q)\)。若某个
端点删点系统留下 line/plane 型 \((A,B,C)\) 纤维，则把式 (38)
替换成其规范仿射子空间并转入异常 join；不得任取一个解点。

共同 \(q\)-线也可保持符号参数 \(\lambda\)。对固定 \(g\)，线性
系统投影到 \(\lambda\) 后只能是 empty、一个点或整条线；由此可以
按 \(\lambda\) 桶计数允许标签，而不先展开 233 个 \(q\)。

## 8. 实现顺序、复杂度与最坏风险

一个可恢复、可并行的全扫器应按 \(\tau\) 轨分片：

1. 建立式 (11) 的归一化 \(q\)-平面。
2. 对三个端点运行第 4 节切片器，把 compatible \(z\) 保存为式
   (17) 的规范键。
3. 用第 5 节规则求共同 \(q\) 点/线/平面。
4. 没有共同 \(q\) 时立即结束该 \(\tau\)。共同点很少时可直接逐
   \(q\) 扫 \(g\)；共同键较多时，一次建立第 6 节的对偶
   \(\mathcal H_{\tau,g}\) 目录。
5. 用式 (33) 删除绝大多数 \(q\)。仅对至少两个纯尾候选标签的
   \(q\) 执行式 (39)--(40)。

在没有 all-zero slice 的零维 minor 层，每个 \(x\) 至多输出十二
个候选 \(y\)。按式 (12) 计，三个端点共有

\[
9\,161\cdot3\cdot233=6\,403\,539
\tag{41}
\]

个一元切片。使用次数至多十二的有限域分解时，quartic 目录阶段约为
\(O(p^3\log p)\) 个小次数域运算；这里把多项式次数十二视为常数。
配套纯 Python 原型仍直接测试每个 \(y\)，但一次完整运行两个小原型
只需数秒，且所有结果为精确模运算。

若对每个 generic \(\tau\) 都无条件建立对偶删点目录，需要

\[
9\,161\cdot54\,288=497\,332\,368
\tag{42}
\]

个 \(7\times5\) 小系统。实现应先做 quartic 键交，并在“逐少数
\(q\) 扫 \(g\)”与“一次建立 dual catalogue”之间自适应选择。
任务可按 \(\tau\) 完全并行；每个 worker 只需保存当前 \(\tau\) 的
目录，普通内存界为 \(O(p^2)\)。

必须显式记录以下最坏 output-sensitive 风险。

1. 许多 all-zero vertical slice，或 minor 有正维公共因子，可能
   输出 \(\Theta(p^2)\) 个 \(z\)。
2. 三个端点可能留下共同 \(q\)-线或整平面。
3. 一个固定 \(q\) 可能对应 \(\Theta(p^2)\) 个 \(z\)，同时又有
   \(\Theta(p^2)\) 个纯尾候选 \(g\)。
4. 式 (39) 的标签对分支最坏可达
   \(O(|\Gamma_q^{\rm tail}|^2\sum_i|\mathcal Z_i(q)|)\)。
5. 非点型 quartic 或 deletion 纤维需要仿射子空间 join；若把它们
   展开成域点，会重新引入被本设计禁止的 \(p\) 或 \(p^2\) 因子。

因此严格的复杂度陈述是：generic 零维点型主干具有式 (41) 的
切片规模，并且算法从不显式枚举 \(z_1\times z_2\times z_3\)；总
运行时间还必须加上异常子空间和实际输出 incidence 的成本。没有对
这些退化层另证上界前，不能声称整个 \(O_3\) 无条件为
\(O(p^3)\) 或 \(O(p^4)\)。

## 9. 当前状态

第 3--7 节给出一个严格、可实现且保持共同 \(q\) 量词的算法。两个
最小原型已经精确通过：

\[
\tau=(17,31):\quad9/11/13,\quad0/0/0\text{ all-zero slices},
\tag{43}
\]

\[
\tau=(0,1):\quad
54\,058/224/4/2,
\quad q_A,q_B\text{ 在纯尾限制下均命中式 (36)}.
\tag{44}
\]

但脚本没有运行全部 \(9\,161\) 个 generic \(\tau\) 轨，也没有关闭
所有 output-sensitive 异常。因此状态严格为

\[
\boxed{\text{PROVED ALGORITHM / PROTOTYPE / GLOBAL INCOMPLETE}.}
\tag{45}
\]
