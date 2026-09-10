# Property B 的 singleton/doubleton 公共核攻击

STATUS: **PROVED_REDUCTION / INDEPENDENT_REVIEW CORRECT /
GLOBAL_INCOMPLETE**

## 1. 主结论

设 \(p\ge 5\) 为具有 Property B 的素数，\(G=C_p^2\)。令
\(Q_1,\ldots,Q_m\) 为长度 \(2p-1\) 的最小零和序列，同一列真实
位置 \(K\) 是每条 \(Q_i\) 的字面子序列，并且

\[
|K|>p.
\tag{1}
\]

则各条 Property B 标准支撑只有以下二择一：

1. 所有标准域完全相同；
2. 存在一组基 \(g,h\)，所有标准域都等于下列两域之一，且两种都
   实际出现：

\[
\mathcal D_g=\{g\}\cup(h+\langle g\rangle),\qquad
\mathcal D_h=\{h\}\cup(g+\langle h\rangle).
\tag{2}
\]

第二种情形中

\[
\bigcap_i\mathcal D_i=\{g,h,g+h\},\qquad
\operatorname{supp}\rho(K)\subseteq\{g,h,g+h\}.
\tag{3}
\]

若再假设 \(K\subsetneq Q_i\) 对至少一条 \(Q_i\) 成立，则 \(K\)
零和自由，并且在式 (3) 的交叉情形中还满足下文式 (12)。这个附加
假设对第 5、6 节的实际尾应用自动成立，因为那里的 \(K\) 与每条
补原子所保留的尾位置不交；它不属于纯粹的双域分类 (2)--(3)。

所以大共同核下，公共支撑交不可能恰有 \(1\)、\(2\) 或 \(p\) 个点；
不同标准域一旦相容，就只能组成式 (2) 的“三角交”。这严格加强了
现有的“公共支撑至少两点”容量门。

对三尾位置

\[
\rho(u_e)=e,\qquad \rho(u_f)=f,\qquad
\rho(u_t)=t=-e-f,\qquad e,f\text{ 独立},
\tag{4}
\]

若共同字面子序列 \(K\) 还满足
\(K\cap\{u_e,u_f,u_t\}=\varnothing\)，则有两个直接可用的上界：

\[
\boxed{
\begin{aligned}
Q_s\supset\{u_e,u_f\},\quad Q_d\supset\{u_t\}
   &\Longrightarrow |K|\le 2p-4,\\
Q_e\supset\{u_e\},\quad Q_f\supset\{u_f\},\quad
Q_t\supset\{u_t\}
   &\Longrightarrow |K|\le 2p-4.
\end{aligned}}
\tag{5}
\]

第一行是 complementary singleton--doubleton 对；第二行是三个
doubleton 端点的三个补原子。固定 \(p=233\) 时，右端为 \(462\)。
第一行是尖的：逐位置统一的模型 C 达到 \(|K|=462\)。

 blanket 命题“mixed trace 或 three-doubleton 自动矛盾”则是假的。
逐位置模型 N 给出一个 singleton 加两个 nested doubleton、
\(|K|=463\)；模型 D 给出三个 doubleton、\(|K|=456\)。真正成立的
是式 (2)--(5) 的结构结论。

## 2. 标准域与基本容量

Property B 把每条最大原子写成

\[
Q=g^{p-1}\prod_{j=1}^{p}(h+a_jg),\qquad
\sum_{j=1}^{p}a_j=1,
\tag{6}
\]

其中 \(g,h\) 是 \(G\) 的一组基。定义

\[
\mathcal D(g,h)=\{g\}\cup(h+\langle g\rangle).
\tag{7}
\]

仿射线基点 \(h\) 可以沿 \(g\) 平移而不改变域；孤立点 \(g\) 是
实际重标签，不能只按射影方向商掉。

式 (6) 的原子性可直接验证。零和子序列所取仿射线项数在
\(h\)-坐标上只能是 \(0\) 或 \(p\)。前者迫使所取 \(g\) 项数为零；
后者再由系数和 \(1\) 迫使取满 \(p-1\) 个 \(g\)。故只有空子序列
与全序列零和。

最大原子内每个标签的重数至多 \(p-1\)：若某标签出现 \(p\) 次，
这 \(p\) 个位置本身就是一个真零和子序列。以下结构引理只需
Property B；由 Reiher 的定理，它适用于所有素数。本文的实际切片
仍只实例化 \(p=233\)。

## 3. 大共同核的双域刚性

设 \(Q_i\) 的重标签为 \(g_i\)。由

\[
|Q_i\setminus K|=2p-1-|K|<p-1,
\tag{8}
\]

\(p-1\) 个 \(g_i\) 不可能全在 \(Q_i\setminus K\)，故

\[
g_i\in\operatorname{supp}\rho(K)
\subseteq\bigcap_j\mathcal D_j.
\tag{9}
\]

若所有重标签都等于同一 \(g\)，取 \(K\) 中另一标签 \(h\)。这样的
\(h\) 必存在，因为 \(|K|>p-1\) 而单标签容量至多 \(p-1\)。任何
\(g\)-重标准域若包含 \(h\)，其仿射线只能是
\(h+\langle g\rangle\)，故所有域相同。

否则取不同重标签 \(g,h\)。由 (9)，\(h\) 落在 \(g\)-重域的仿射
线上，\(g\) 落在 \(h\)-重域的仿射线上。二者不可能线性相关，因为
仿射线与其方向的过原点直线不交。因此两域正是 (2)，且

\[
(h+\langle g\rangle)\cap(g+\langle h\rangle)=\{g+h\}.
\tag{10}
\]

第三个域的重标签仍由 (9) 落在 \(\{g,h,g+h\}\)。重标签为 \(g\)
或 \(h\) 时唯一恢复出式 (2) 的相应域。若重标签为 \(g+h\)，要同时
包含 \(g,h\)，就需 \(g-h\in\langle g+h\rangle\)，这在奇特征下与
\(g,h\) 独立矛盾。任意多条域同理，式 (2)--(3) 得证。

交叉情形写

\[
\rho(K)=g^a h^b(g+h)^c.
\tag{11}
\]

若 \(K\subsetneq Q_i\) 对至少一条 \(Q_i\) 成立，则 \(K\) 是该最大
原子的真子序列，因而零和自由。逐坐标可得精确条件

\[
\boxed{c+\min(a,b)\le p-1.}
\tag{12}
\]

确实，含 \(r,s,q\) 个 \(g,h,g+h\) 的子序列零和，当且仅当
\(r+q\equiv s+q\equiv0\pmod p\)。在各重数小于 \(p\) 时，非空解
存在当且仅当某个 \(1\le q\le c\) 满足 \(p-q\le a,b\)。

若两种重域都出现，令 \(k=|K|\)、\(n=2p-1-k\)，则

\[
k-p\le a,b\le p-1,\qquad c=k-a-b.
\tag{13}
\]

余部数据也被完全压缩为

\[
\begin{array}{c|cc}
&\text{重项数}&\text{线项数}\\ \hline
g\text{-重余部}&p-1-a&p-k+a\\
h\text{-重余部}&p-1-b&p-k+b
\end{array}
\qquad
\sum(\text{余部线系数})\equiv1-c.
\tag{14}
\]

这是后续逐位置求解器可直接使用的三标签正规形。

## 4. 一个标准域不能同时含三尾

对 \(p\ge5\)，不存在标准域同时包含 \(e,f,t\)。若三点都在仿射
线上，则

\[
\det(f-e,t-e)=3\det(e,f)\ne0.
\tag{15}
\]

若某个尾点是孤立重标签，则另两个尾点之差必须平行于它。三个选择
分别要求

\[
f-t=e+2f\parallel e,\qquad
e-t=2e+f\parallel f,\qquad
e-f\parallel -e-f,
\tag{16}
\]

都因 \(e,f\) 独立且 \(p\ne2\) 而不可能。故只要一族最大补原子
合计包含三个尾标签，第 3 节的同域分支就被排除，只剩三点交叉域。

## 5. complementary singleton--doubleton 的尖上界

设 \(Q_s\) 含实际尾位置 \(u_e,u_f\)，\(Q_d\) 含 \(u_t\)，共同
字面子序列 \(K\) 与三尾位置不交。反设 \(|K|\ge2p-3\)。因为
\(Q_s\setminus K\) 至少含两个不同尾位置，

\[
|K|=2p-3,\qquad
|Q_s\setminus K|=|Q_d\setminus K|=2.
\tag{17}
\]

第 4 节排除同域。定向记交叉域为

\[
\mathcal D_x=\{x\}\cup(y+\langle x\rangle),\qquad
\mathcal D_y=\{y\}\cup(x+\langle y\rangle),
\tag{18}
\]

其中 \(e,f\in\mathcal D_x\)、\(t\in\mathcal D_y\)。所有可能性恰为
\(p+1\) 个：

\[
\begin{array}{c|c}
x&y\\ \hline
f&e+2f\\
e&2e+f\\
d(f-e),\ d\in\mathbb F_p^\times&
\dfrac{1-d}{2}e+\dfrac{1+d}{2}f.
\end{array}
\tag{19}
\]

穷尽性如下。若 \(x=e\) 或 \(f\)，另一尾点必须在
\(y+\langle x\rangle\)，而 \(t\in x+\langle y\rangle\) 唯一给出
前两行。否则 \(e,f\) 都在该仿射线上，故 \(x=d(f-e)\)；写
\(y=e+\lambda x\)，条件 \(t-x\in\langle y\rangle\) 给
\(\lambda=(d+1)/(2d)\)。

写 \(K=x^a y^b(x+y)^c\)。在第一行 \(x=f,y=e+2f\) 中，
\(Q_s\setminus K=\{e,f\}\)。重项计数给 \(a=p-2\)，而
\(e=y-2x\) 与标准形系数和给

\[
c-2\equiv1\pmod p,\qquad c=3.
\tag{20}
\]

故 \(b=p-4\)。但 \(Q_d\setminus K\) 只有两个位置，却需补足
\(p-1-b=3\) 个重标签 \(y\)，矛盾。第二行对称。

第三行中 \(e,f\) 都是 \(x\)-域线项，故余部没有重标签，迫使
\(a=p-1\)，从而 \(b+c=p-2\)。又

\[
t=x-2y.
\tag{21}
\]

\(Q_d\) 的二位置余部必须留一个线项位置给 \(t\)，所以
\(p-1-b\le1\)，即 \(b=p-2,c=0\)。此时唯一余部线系数为
\(-2\)，却必须等于 \(1\)，除非 \(p=3\)。矛盾证明
\(|K|\le2p-4\)。

模型 C 在 \(p=233\) 给出逐位置统一的等号见证

\[
K=g^{231}h^{231},\qquad |K|=462,
\tag{22}
\]

所以不能仅靠这一层继续降低。

## 6. three-doubleton 的上界

设三条最大补原子 \(Q_e,Q_f,Q_t\) 分别含实际尾位置
\(u_e,u_f,u_t\)，且共同字面子序列
\(K\cap\{u_e,u_f,u_t\}=\varnothing\)。若 \(|K|=2p-2\)，每条
\(Q_u\setminus K\)
只有对应尾位置，三条零和式给 \(e=f=t=-\sigma(K)\)，矛盾。

只需排除 \(|K|=2p-3\)。此时每个余部为

\[
\{u,s-u\},\qquad s=-\sigma(K),\qquad u\in\{e,f,t\}.
\tag{23}
\]

三尾合计覆盖 \(e,f,t\)，故标准域必须交叉。写

\[
K=g^{p-1-\alpha}h^{p-1-\beta}(g+h)^r,\qquad
r=\alpha+\beta-1,\qquad 0\le\alpha,\beta\le2.
\tag{24}
\]

\(\alpha,\beta\) 是相应二位置余部内重标签 \(g,h\) 的个数，并且

\[
s=(2-\beta)g+(2-\alpha)h.
\tag{25}
\]

在基 \((g,h)\) 中，分配给 \(g\)-重域的尾标签只能落在

\[
\begin{array}{c|c}
\alpha&u\\ \hline
0&(\lambda,1)\\
1&(1,0)\text{ 或 }(1-\beta,1)\\
2&(1,0),\text{ 且必须 }\beta=0,
\end{array}
\tag{26}
\]

而分配给 \(h\)-重域的尾标签只能落在

\[
\begin{array}{c|c}
\beta&u\\ \hline
0&(1,\mu)\\
1&(0,1)\text{ 或 }(1,1-\alpha)\\
2&(0,1),\text{ 且必须 }\alpha=0.
\end{array}
\tag{27}
\]

例如 \(\alpha=0\) 时余部两个点都在线
\(h+\langle g\rangle\)，(25) 保证一个在线当且仅当另一个也在线；
\(\alpha=1\) 时二者恰有一个等于 \(g\)。其余同理。

要求两种域都出现后，仅余

\[
(\alpha,\beta)=(0,1),(0,2),(1,0),(1,1),(2,0).
\tag{28}
\]

前两组中三个尾标签第二坐标全为 \(1\)，其和的第二坐标为
\(3\ne0\)。后两组中第一坐标全为 \(1\)，同样矛盾。
\((1,1)\) 只允许两个点 \((1,0),(0,1)\)，却要容纳三个互异尾
标签。故 \(p\ge5\) 时无解，证明 \(|K|\le2p-4\)。

这个 three-doubleton 上界目前不宣称尖。模型 D 只证明统一位置、
三个最大原子和共同核 \(456\) 可以同时存在；\(457\) 到 \(462\)
是否有统一位置见证不由本文决定。

## 7. 720 行表首个 ID 行

长度装饰表按 ID 的首个 survivor 是 decorated-0011：

\[
\text{迹掩码 }(3,4,1,6,2,5),\qquad
\text{端点长度 }(7,7,8,7,8,7),
\tag{29}
\]

外层容量桥给 \(|K|\ge439\)。掩码 \(4\) 是 singleton
\(\{t\}\)，其长七补原子含 \(\{e,f\}\)；掩码 \(3\) 是互补
doubleton \(\{e,f\}\)，其长七补原子含 \(t\)。第 5 节给

\[
\boxed{439\le |K|\le462.}
\tag{30}
\]

该行另有掩码 \(6,5\) 的两个长七 doubleton，所以四条最大补原子
全部落入同一个交叉域对。把 singleton 补原子的域定向为
\(\mathcal D_x\)，全部候选恰压成式 (19) 的 \(234\) 个有序域对。
其余两条补原子只需包含 \(e\) 或 \(f\)，而 \(\mathcal D_x\) 已
同时包含二者，所以纯支撑元数据不矛盾。

加入余部重数、线槽与系数和后，配套程序得到

\[
\begin{array}{c|ccc}
|K|&463&462&461\\ \hline
\text{仍可逐原子完成的有序域对数}&0&2&234.
\end{array}
\tag{31}
\]

这里“逐原子完成”没有量化同一 \(L\) 上四个余部位置胞的粘合，
不是该 outer row 的统一位置 SAT 见证。严格结论只有 (30) 与交叉
三点正规形；本节删除零行。

## 8. 当前真实掩码前沿

更深的 endpoint-mask 工件选择 decorated-1356，其迹与长度为

\[
(1,2,4,6),\qquad(8,7,8,8).
\tag{32}
\]

该工件展示的首个 literal mask survivor 满足

\[
|K|=446,\qquad
(|Q_0|,|Q_1|,|Q_2|,|Q_3|)=(464,465,464,464).
\tag{33}
\]

配套程序独立重建了展示的四端点、\(L,K\) 与四个补集，核对了
(33)。但本文没有复跑上游 27,172 个轨道枚举，故不把“它是当前
第一个真实掩码前沿”作为本文定理的依赖。

唯一实际长七补原子 \(Q_1\) 对应 singleton 迹 \(\{f\}\)，故含尾
\(e,t\)。其余三条长 \(2p-2\)，不能直接冒充三个 Property B 最大
原子，所以第 3--6 节不能无条件套用。

第 9 节给出条件性入口。对 \(Q_0\) 或 \(Q_2\) 选尾外的
\(x\in Q_i\setminus K\)。若 \(Q_i\setminus\{x\}\) 缺少某个非零
子集和，补全出的最大原子仍含 \(K\)，并分别保留尾对
\(\{f,t\}\) 或 \(\{e,f\}\)。它与实际 \(Q_1\) 合计覆盖三尾，
故标准域进入交叉三点正规形。此时

\[
\rho(K)=g^a h^b(g+h)^c,\qquad
a,b\ge213,\qquad c\le20,\qquad c+\min(a,b)\le232.
\tag{34}
\]

若相关长八分支覆盖全部非零子集和，第 9 节不给标准域；即便进入
(34)，整数条件也仍有解。因此对这个 mask 前沿，本攻击删除零行，
只给出可交给标签求解器的条件性三标签压缩。

## 9. 长八原子的补全二择一

令 \(Q\) 为长度 \(2p-2\) 的原子，取位置 \(x\in Q\)，置
\(T=Q\setminus\{x\}\)。若某个非零 \(b\in G\) 不是 \(T\) 的任何
非空子序列和，则

\[
S=T\mathbin{\dot\cup}\{-b\}
\tag{35}
\]

零和自由。添入

\[
y=-\sigma(S)=x+b
\tag{36}
\]

后，\(S\dot\cup\{y\}\) 是长度 \(2p-1\) 的最小零和序列。不含
\(y\) 的零和子序列违反 \(S\) 零和自由；含 \(y\) 的真零和子序列
取补后又给出 \(S\) 的非空零和子序列。

故有严格二择一：

1. \(T\) 的非空子序列和覆盖 \(G\setminus\{0\}\)；
2. \(T\) 嵌入某个最大 Property B 原子，支撑落在一个标准域，且
   \(T\) 内至少有 \(p-3\) 个该原子的重标签。

在 \(p=233\)、\(|K|\ge435\) 的 outer row 中选
\(x\in Q\setminus K\)，有 \(K\subset T\)。第二分支的重标签在
\(K\) 内至少出现

\[
(p-3)-|T\setminus K|
=230-(463-|K|)=|K|-233\ge202
\tag{37}
\]

次，其人工补全域必须与所有实际长七补原子的域共同服从第 3 节。
但第一分支尚未排除；当前 720 行也没有普遍的真实端点掩码。因此
二择一本身删除零行。下一缺口是证明某个 \(x\) 必有缺失目标，或
直接用“覆盖全部非零目标”产生实际短块或 mixed 矛盾。

## 10. 反例边界与裁决

配套脚本从真实位置重建三个见证：

- 模型 N：singleton 加两个 nested doubleton，三条最大补原子，
  精确字面交 \(|K|=463\)，所有标准域相同；
- 模型 C：complementary singleton--doubleton，精确字面交
  \(|K|=462\)，达到第 5 节上界；
- 模型 D：three-doubleton，三条最大补原子，精确字面交
  \(|K|=456\)，两个域的公共支撑为 \(\{g,h,g+h\}\)。

程序逐项核验端点投影和为零、补序列长度 \(2p-1\)、重数 \(p-1\)、
仿射线归属、线系数和 \(1\) 以及精确字面交。这些仍只是二维投影 /
Property B 层见证，不含完整 \(q\)-提升、全部自动短块、mixed
targets、Hasse、高度或实际 \(Z\) 原子性。

因此本文裁决为

\[
\boxed{\textbf{PROVED REDUCTION; INDEPENDENT REVIEW CORRECT}.}
\tag{38}
\]

已审证明内容是双域刚性、两个 \(462\) 上界和长八补全二择一；不声称任一
outer survivor 可实现，也不声称固定 \(p=233\) 或全局 \(A_p\)
已闭合。

## 11. 可复现性

运行 unique_tail_property_b_doubleton_intersection_attack.py。程序不
导入旧作者模块，独立重建三模型、枚举 234 个有序交叉域、核对式
(31)、穷尽 three-doubleton 的边界坐标情形，并生成同名前缀的
JSON 报告。
