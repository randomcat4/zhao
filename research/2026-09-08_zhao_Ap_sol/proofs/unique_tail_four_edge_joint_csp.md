# 三点唯一尾的四边联合 CSP：迹不交图、等和花瓣与共同外部谱

STATUS: PROVED_INTERFACE / EXACT_SURVIVOR_BRANCHES / JOINT_UNSAT_NOT_ESTABLISHED / GLOBAL_INCOMPLETE

## 1. 范围与结论

沿用冻结的唯一尾分支

\[
X=x^{p-4}\subset Z,\qquad Y=Z\setminus X,\qquad
\bar x=q\ne0,\qquad |Y|=2p+8,
\tag{1}
\]

并只考察两个三点尾型

\[
(p,\ell,b,r)=(233,7,4,3),\qquad(1399,8,5,3).
\tag{2}
\]

唯一正核心尾为 \(U=\{u_1,u_2,u_3\}\)，满足

\[
\bar\sigma(U)=-bq,\qquad \sigma(U)=3a-bx.
\tag{3}
\]

\(\mathcal H_0\) 表示全部零核心 \(F_3\) 块；每个
\(H\in\mathcal H_0\) 满足

\[
6\le |H|\le8,\qquad \bar\sigma(H)=0,\qquad
\sigma(H)=3a,\qquad
\varnothing\ne H\cap U\subsetneq U.
\tag{4}
\]

上一篇位置冲突前沿从 \(1628\) 与 \(9310\) 条真实尾迹不交边中，
分别抽出一个非轴向尾外位置 \(y\)，它同时属于四条不同边的两个
端点。本文把这四条边、至多八个端点块、全部自动诱导短块和每个
端点长补原子的全部内部子集和放进同一个接口。

得到两个严格结论。

1. 四边端点的尾迹满足一个穷尽二分支：
   - 两个不同端点块有相同尾迹，于是共享 \(y\) 的公共部分外出现
     两个非空、不交、实际和值相同的短花瓣；迹一时每个花瓣至多
     六点，迹二时至多五点；
   - 或所有端点尾迹不同，此时必有三个不同的单点迹块
     \(H_1,H_2,H_3\)，分别取迹 \(\{u_1\},\{u_2\},\{u_3\}\)，
     且三块都含同一非轴向位置 \(y\)。三对交集全部投影非零。
2. 令 \(L\) 为全部端点块与 \(U\) 的并、\(R=Y\setminus L\)。
   所有端点补原子的内部子集和由同一个精确外部谱
   \(M_R(k,g)\) 与有限局部因子卷积充要决定。这个共同
   \(M_R\) 是端点之间真正的联合耦合，不能替换成每个端点各自的
   独立可达表。

两个分支都没有被现有轴向判据单独排除；尤其，本文没有证明存在
实现 \(M_R\) 的实际外部序列，也没有证明不存在。因此裁决是

\[
\boxed{\mathsf{PROVED\_INTERFACE}/
\mathsf{EXACT\_SURVIVOR\_BRANCHES}/
\mathsf{JOINT\_UNSAT\_NOT\_ESTABLISHED}/
\mathsf{GLOBAL\_INCOMPLETE}.}
\tag{5}
\]

“幸存分支”只表示尚未被本文的联合必要条件排除，不是局部模型，
更不是原题反例。

## 2. 四条共享非轴位置的实际边

对尾迹不交的块对 \(e=\{H,H'\}\)，已有位置引理给

\[
I_e:=H\cap H'\subseteq Y\setminus U,\qquad
I_e\ne\varnothing,\qquad
\rho(\bar\sigma(I_e))\ne0,
\tag{6}
\]

其中

\[
\rho:C_p^3\longrightarrow C_p^3/\langle q\rangle\cong C_p^2.
\tag{7}
\]

故每个 \(I_e\) 至少含一个满足 \(\rho(\bar y)\ne0\) 的实际位置。
对每条边固定选择一个这样的见证位置。两个型的尾外位置数分别是

\[
|Y\setminus U|=471,\qquad 2803.
\tag{8}
\]

于是

\[
\left\lceil{1628\over471}\right\rceil=4,\qquad
\left\lceil{9310\over2803}\right\rceil=4.
\tag{9}
\]

在任一型中，都存在一个固定

\[
y\in Y\setminus U,\qquad \rho(\bar y)\ne0,
\tag{10}
\]

以及四条不同的实际边 \(e_1,\ldots,e_4\)，使

\[
y\in I_i:=I_{e_i},\qquad
\rho(\bar\sigma(I_i))\ne0\quad(1\le i\le4).
\tag{11}
\]

令 \(\mathcal A\) 是这四条边的所有不同端点块。简单图四条不同边
至少使用四个、至多使用八个顶点，所以

\[
4\le s:=|\mathcal A|\le8.
\tag{12}
\]

每个 \(A\in\mathcal A\) 都含 \(y\)。每个端点块还至少含一个
\(U\)-位置，故它至多含六个既不在 \(U\) 也不等于 \(y\) 的位置。
因此

\[
L:=U\cup\bigcup_{A\in\mathcal A}A,\qquad |L|\le3+1+8\cdot6=52.
\tag{13}
\]

因此共同外部序列满足

\[
R:=Y\setminus L,\qquad |R|\ge2p+8-52=2p-44,
\]

即 \(p=233,1399\) 时分别至少有 \(422,2754\) 个位置。

另一方面，每个 \(I_i\) 至多七点，且四者共享 \(y\)，所以

\[
S:=I_1\cup\cdots\cup I_4,\qquad |S|\le1+4(7-1)=25.
\tag{14}
\]

式 (14) 只控制四个真实交集；端点花瓣和
\(R=Y\setminus L\) 仍然存在，所以这不是一个自足的二十五变量 CSP。

## 3. 三点尾的六迹不交图

把六个非空真尾迹写成

\[
s_i=\{u_i\},\qquad d_i=U\setminus\{u_i\}\quad(1\le i\le3).
\tag{15}
\]

两个迹不交，当且仅当它们在下图所列六条边之一：

\[
s_1s_2,\ s_2s_3,\ s_3s_1,\qquad
s_1d_1,\ s_2d_2,\ s_3d_3.
\tag{16}
\]

也就是说，迹不交图是单点迹 \(s_1,s_2,s_3\) 组成的三角形，
并在每个 \(s_i\) 上悬挂补二点迹 \(d_i\)。

现在查看四边端点块到这六个迹类的映射。

**引理 1（四边尾迹二分支）。** 必有且仅需考虑以下两个分支。

1. 映射不单射：存在不同 \(H,K\in\mathcal A\) 满足
   \(H\cap U=K\cap U\)。
2. 映射单射：\(\mathcal A\) 中存在三个不同块
   \(H_1,H_2,H_3\)，满足
   \[
   H_i\cap U=\{u_i\},\qquad y\in H_1\cap H_2\cap H_3.
   \tag{17}
   \]

**证明。** 第一种情形就是映射不单射。若映射单射，则四条不同
块边映成 (16) 中四条不同迹边。若缺少某个单点顶点，例如 \(s_1\)，
不经过 \(s_1\) 的边只有

\[
s_2s_3,\qquad s_2d_2,\qquad s_3d_3,
\]

至多三条，矛盾。故四边迹子图含全部 \(s_1,s_2,s_3\)。
所有端点块都含 \(y\)，得到 (17)。证毕。

## 4. 重复尾迹分支：共享公共部外的等和花瓣

设引理 1 的第一分支发生，并写

\[
J=H\cap U=K\cap U,\qquad j=|J|\in\{1,2\},
\tag{18}
\]

\[
C=H\cap K,\qquad P=H\setminus C,\qquad Q=K\setminus C.
\tag{19}
\]

由于所有端点都含 \(y\)，

\[
\{y\}\mathbin{\dot\cup}J\subseteq C.
\tag{20}
\]

两个块实际和值相同，故

\[
\boxed{\sigma(P)=\sigma(Q)=3a-\sigma(C)},\qquad
\bar\sigma(P)=\bar\sigma(Q)=-\bar\sigma(C).
\tag{21}
\]

\(P,Q\) 按定义不交。它们都非空：若 \(P=\varnothing\)，则
\(H\subsetneq K\) 或 \(H=K\)；后一种违反块不同，前一种结合
\(\sigma(H)=\sigma(K)\) 给出 \(K\setminus H\) 的非空实际零和，
违反 \(Z\) 的实际原子性。对 \(Q\) 同理。

由 \(|H|,|K|\le8\) 与 (20)，

\[
1\le |P|,|Q|\le7-j=
\begin{cases}
6,&j=1,\\
5,&j=2.
\end{cases}
\tag{22}
\]

这比一般的等和花瓣碰撞更局部：两个花瓣来自同一固定非轴位置
\(y\) 上的四边端点，且共同部含完整的相同尾迹。

下面把它接到长补原子内部谱。若 \(C\) 轴向，则已有交集判据给

\[
\bar\sigma(C)=-tq,\qquad t\in\{1,2,3\},\qquad |C|+t\le8.
\tag{23}
\]

等号八会使 \(X_t\mathbin{\dot\cup}C\) 成为正核心 \(F_3\) 块；
其尾 \(C\) 含 \(y\notin U\)，违反唯一尾。因此实际有

\[
|C|+t\le7.                                                \tag{24}
\]

此时

\[
X_t\mathbin{\dot\cup}C
\tag{25}
\]

是一个长度至多七的自动诱导短块。它含 \(y\)，因而已经与
\(\mathcal A\) 中每个端点块相交。另一方面，(21) 给

\[
\bar\sigma(P)=\bar\sigma(Q)=tq,\qquad t\in\{1,2,3\}.
\tag{26}
\]

\(P\subset Z\setminus K\)、\(Q\subset Z\setminus H\)，而零核心
\(F_3\) 长补的完整轴向准则恰允许内部轴向系数 \(1,2,3\)。
所以 (26) 不违反两个端点补原子。

若 \(C\) 非轴向，则 (21) 中两个花瓣也非轴向；同一长补准则只限制
轴向内部子集，对这两个花瓣本身没有给出禁值。由此得到精确停止线：
重复迹分支在“公共部轴向”和“公共部非轴向”两支都未被现有端点
长补判据关闭；潜在矛盾只能来自花瓣与其他局部位置或共同外部
\(R\) 的进一步联合子和。

## 5. 全部尾迹不同分支：三个单点迹块

现在设引理 1 的第二分支成立。对 \(1\le i<j\le3\)，令

\[
C_{ij}=H_i\cap H_j,\qquad
P_{ij}=H_i\setminus C_{ij},\qquad
Q_{ij}=H_j\setminus C_{ij}.
\tag{27}
\]

两个单点尾迹 \(\{u_i\},\{u_j\}\) 不交，所以此前的外部交投影引理
逐对给出

\[
y\in C_{ij}\subseteq Y\setminus U,\qquad
\boxed{\rho(\bar\sigma(C_{ij}))\ne0}.
\tag{28}
\]

同和性又给

\[
\sigma(P_{ij})=\sigma(Q_{ij})=3a-\sigma(C_{ij}),\qquad
\rho(\bar\sigma(P_{ij}))=\rho(\bar\sigma(Q_{ij}))\ne0.
\tag{29}
\]

每对花瓣均非空且彼此不交，大小至多七。它们分别是另一端点长补的
内部子集，但 (29) 是非轴向值，所以完整轴向准则对这些花瓣本身
保持沉默。交集 (28) 也不能只用若干 \(X\)-位置闭合成自动商零短块。

这解释了为什么三块结构本身尚不产生联合矛盾：三对真实交和值已
被迫非轴向，而当前长补禁表只禁止轴向系数集合之外的值。它们仍可
与 \(L\) 中其他位置或共同 \(R\) 中的子集相加后落回轴上；这正由
第 6 节的共同谱处理。

还有两个长度强化。若上一篇的旧等和花瓣碰撞已经发生，则本轮已有
所需局部结构；在其否定分支中：

- \(p=233\) 的每个单点迹块长度属于 \(\{7,8\}\)，故
  \[
  |H_i\setminus(\{y\}\cup\{u_i\})|\in\{5,6\};
  \tag{30}
  \]
- \(p=1399\) 的每个单点迹块长度为八，故
  \[
  \boxed{|H_i\setminus(\{y\}\cup\{u_i\})|=6
  \quad(1\le i\le3).}
  \tag{31}
  \]

式 (31) 是三个不同六点余部，不断言它们的和值彼此相同；精确和值为
\(3a-y-u_i\)。真正相等的是每一对在 (29) 中相对于其公共交集
切出的交换花瓣。

## 6. 一个共同外部谱给出的精确联合接口

仅枚举 (14) 的二十五个交集位置会漏掉端点花瓣，也会漏掉每个
\(Y\setminus A\) 中的大部分位置。现在给出无此漏洞的接口。

把实际群写成 \(G=C_p^4\)，商映射为
\(\pi:G\to C_p^3\)，并沿用 \(a\in\ker\pi\) 与
\(\pi(x)=q\)。令

\[
R=Y\setminus L.
\tag{32}
\]

对 \(0\le k\le|R|\)、\(g\in G\)，定义同一个精确存在/计数谱

\[
M_R(k,g)=
\#\{F\subseteq R:|F|=k,\ \sigma(F)=g\}.
\tag{33}
\]

它等价于群代数中的平方自由生成式

\[
\Phi_R(z)=\prod_{r\in R}(1+z[r])
=\sum_{k=0}^{|R|}\sum_{g\in G}M_R(k,g)z^k[g].
\tag{34}
\]

因此任意声称已消去 \(R\) 的求解器，必须要求 (34) 来自同一个
实际位置序列 \(R\)。任意填一张满足边缘等式的表只是放宽模型。

### 6.1 每个端点长补的全部内部子和

固定端点 \(A\in\mathcal A\)。其商补原子是

\[
B_A=Z\setminus A=X\mathbin{\dot\cup}R
\mathbin{\dot\cup}(L\setminus A).
\tag{35}
\]

\(B_A\) 的任一位置子集唯一写成

\[
X_c\mathbin{\dot\cup}F\mathbin{\dot\cup}E,
\quad
0\le c\le p-4,\quad F\subseteq R,\quad E\subseteq L\setminus A.
\tag{36}
\]

它的长度与实际和值分别为

\[
n=c+k+|E|,\qquad cx+g+\sigma(E),
\tag{37}
\]

其中 \(k=|F|\)、\(g=\sigma(F)\)，也就是
\(M_R(k,g)>0\) 的一个条目。因此，排除空集与整个 \(B_A\) 后，

\[
\boxed{
B_A\text{ 是商零和原子}
\Longleftrightarrow
\pi(cx+g+\sigma(E))\ne0
}
\tag{38}
\]

对 (36) 的每个 \(c,E,k,g\) 且 \(M_R(k,g)>0\) 都成立。
这逐项遍历全部内部子集和，既不限长度，也不是只检查四个
\(I_i\)。

等价地，先去掉 \(X_c\) 后，对每个
\(\varnothing\ne F\mathbin{\dot\cup}E
\subsetneq R\mathbin{\dot\cup}(L\setminus A)\)，必须有

\[
\pi(g+\sigma(E))\in\langle q\rangle
\Longrightarrow
\pi(g+\sigma(E))\in\{q,2q,3q\}.
\tag{39}
\]

关键点是：所有 \(A\in\mathcal A\) 在 (38)--(39) 中共享同一张
\(M_R\)。只改变有限局部集合 \(L\setminus A\)。这正是八个端点
长补之间的联合耦合；分别为八个端点选择八张可达表会产生伪解。

### 6.2 共同外部序列自身的投影零子集 packing

共同 \(R\) 还满足一个不依赖局部花瓣的真实 packing 约束。
固定任一端点 \(A\)。因为 \(A\cap U\subsetneq U\)，
\(L\setminus A\) 非空，所以每个非空 \(F\subseteq R\) 都是
\(Y\setminus A\) 的真子集。若

\[
\rho(\bar\sigma(F))=0,
\]

则端点长补的完整轴向准则迫使存在唯一
\(d(F)\in\{1,2,3\}\) 使

\[
\bar\sigma(F)=d(F)q.
\]

若 \(F_1,F_2\subseteq R\) 非空且不交，它们的并仍是
\(Y\setminus A\) 的真子集。因此只要二者投影和都为零，就还必须有

\[
d(F_1)+d(F_2)\pmod p\in\{1,2,3\}.
\]

这里 \(p\ge233\)，普通和介于二和六，故无序系数型只能是

\[
(1,1),\qquad(1,2).
\]

同理，三个两两不交的非空投影零子集只能全取系数一；四个这样的
子集不可能两两不交。精确地，

\[
\begin{array}{c|c}
\text{两两不交的投影零子集数}&\text{轴系数型}\\ \hline
1&(1),(2),(3)\\
2&(1,1),(1,2)\\
3&(1,1,1)\\
\ge4&\varnothing.
\end{array}
\]

单张边缘谱 \(M_R(k,g)\) 只记录每个和值是否可达，不能从两个可达
条目判断见证子集是否不交。求解时必须从同一个实际 \(R\) 的因子式
(34) 提取相应的有色谱

\[
\prod_{r\in R}
\left(1+\sum_{\nu=1}^t z_\nu[r]_\nu\right)
\qquad(1\le t\le4),
\]

其系数恰计数有序、两两不交的 \(t\) 个子集；上述表就是这些共同
有色谱的禁支撑。不能给不同子集另配互不相关的 \(M_R\) 见证。

这个 packing 仍不产生纯长度矛盾：

\[
|R|\ge2p-44=D(C_p^2)-43,
\]

而 \(C_p^2\) 的零和自由序列可长至 \(2p-2\)。因此现有长度下界
没有强迫 \(R\) 内出现一个、更不用说四个互不相交的投影零子集；
要继续必须使用 \(R\) 的共同总和、局部卷积或 Hasse 位置行。

### 6.3 全部自动诱导短块与中间禁区

任取 \(E\subseteq L\)、\(M_R(k,g)>0\) 与
\(0\le c\le p-4\)。式 (36)--(37) 仍唯一描述
\(Z\) 中相应位置子集。若

\[
\pi(cx+g+\sigma(E))=0,                                   \tag{40}
\]

则：

- 当 \(n=1\) 时，该条目必须不存在；
- 当 \(2\le n\le8\) 时，实际和值必须是
  \(\lambda a\)，其中
  \[
  \begin{array}{c|ccccccc}
  n&2&3&4&5&6&7&8\\ \hline
  \lambda&1&1&1,2&1,2&1,2,3&2,3&3;
  \end{array}
  \tag{41}
  \]
  由此无遗漏地自动生成 \(F_1,F_2,F_3\) 短块；
- 当 \(9\le n\le2p+2\) 时，该条目必须不存在；
- 若 (41) 生成 \(F_3\)、\(c>0\)，唯一尾要求
  \(F=\varnothing\) 且 \(E=U\)；
- 每个生成的短块必须与每个选中端点 \(A\) 相交。由于
  \(X,R\) 都与 \(A\subseteq L\) 不交于相应位置部分，这一条件精确为
  \[
  E\cap A\ne\varnothing.
  \tag{42}
  \]

同一卷积还检查实际 \(Z\) 原子性：除空集与整个 \(Z\) 外，任何
\(c,E,k,g\) 满足

\[
cx+g+\sigma(E)=0\quad\text{于 }G                         \tag{43}
\]

都被拒绝。

式 (33)--(43) 是本轮所需“统一标签、全部自动短块、全部端点长补
内部子和”的充要联合接口。它没有把不同端点的外部位置复制开。

### 6.4 与严格统一标签核验器的边界

单张 \(M_R(k,g)\) 足以精确判定 (38)--(43)，也可通过卷积计算不带
外部固定点的块数。但它不记录两个不同外部子集彼此交了哪些具体
\(R\)-位置，因此不能单独替代严格核验器中的：

- 每个外部位置、位置对、位置三元组的 Hasse 行；
- 两个都含外部位置的自动短块之间的实际交集；
- 新自动生成的、未列入 \(\mathcal A\) 的每个 \(F_3\) 补原子。

要核验这些全局条件，必须保留 \(R\) 的逐位置标签并把完整
\(Y=L\mathbin{\dot\cup}R\) 送入现有严格统一标签核验器；或者提供
保留相应标记位置与成对子集交关系的更高阶共同谱。本文没有使用
单张 \(M_R\) 冒充这些更强数据。

## 7. 有限审计与哈希

配套程序 unique_tail_four_edge_joint_csp.py 做两层独立有限审计。

1. 穷举所有四边简单图并按连通分量正规化，确认无孤立端点的
   无标号图恰有十一型。
2. 对每个图型穷举每个端点的六种非空真尾迹，只保留每条边两迹
   不交的赋值；同时直接穷举 (16) 的十五个四边子图。
3. 核对 \(|R|\ge2p-44\)、Davenport 距离 \(43\)，以及共同外部
   投影零子集的 \(1/2/3\) 项不交 packing 系数表。
4. 在十二个小型完整位置实例上逐子集展开，并与
   \(M_R(k,g)\) 加局部因子的卷积逐长度、逐和值、逐多重数比较。

固定的十一幅代表图上共有 \(28584\) 个合法迹赋值，其中
\(28548\) 个有重复端点迹，\(36\) 个端点迹全异；后一类全部含
三个单点迹。这里的 \(28584\) 是对十一幅固定标号代表图的有限
审计分母，不是全局块系的模型数。

固定哈希为

\[
\begin{aligned}
\text{shape SHA-256}
&=\mathtt{5cdf95e68b0d842a90a07d06ffd42abb705a14579c4a4e6efc5cb9ec4a7c6afb},\\
\text{certificate SHA-256}
&=\mathtt{2f32fdd668cc854a33b499513f8a0336a67536d157a0ac1c03b29a2ce69dd051}.
\end{aligned}
\tag{44}
\]

验证命令：

    C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/2026-09-08_zhao_Ap_sol/unique_tail_four_edge_joint_csp.py

## 8. 精确停止线

**PROVED：**四边共享非轴位置、十一种端点图、六迹不交图以及
“重复迹等和短花瓣 / 全异迹三单点块”二分支；每条结论量化于
满足冻结唯一尾接口的每个实际反例及由 (9) 抽出的任意四条边。

**PROVED：**同一个可实现谱 \(M_R(k,g)\) 与有限局部卷积充要表示
每个选中端点补原子的全部内部子集和，并同时生成全部自动短块和
中间长度禁区；共同 \(R\) 的两两不交投影零子集系数型只可能为
\((1,1),(1,2)\)，三子集只可能 \((1,1,1)\)，四子集不可能。

**OPEN：**尚未证明任何实际 \(R\) 的共同谱必违反 (38)--(43)，
也未构造通过这些条件的实际 \(R\)。重复迹分支的轴向花瓣恰落在
允许系数 \(1,2,3\)，非轴向花瓣及三单点块的交换花瓣又不受当前
轴向表直接限制。这是联合 UNSAT 尚未闭合的精确原因。

因此本文既不把二十五位置分片当成自足 CSP，也不把有限图分支的
局部幸存者称为模型或反例。全局定理继续保持 INCOMPLETE。
