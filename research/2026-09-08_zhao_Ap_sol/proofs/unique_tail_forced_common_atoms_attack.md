# 三种强制共同余部原子型：交换门、覆盖对与显式局部幸存者

STATUS: **PROVED_EXCHANGE_GATE / LOCAL_COVER_SURVIVOR / GLOBAL_INCOMPLETE**

## 1. 冻结范围

只考虑

\[
(p,\ell,b,r)=(233,7,4,3),\qquad(1399,8,5,3)
\tag{1}
\]

的三点唯一尾分支，并沿用四边端点族 \(\mathcal A\)、
\(L=U\cup\bigcup_{H\in\mathcal A}H\)、\(R=Y\setminus L\) 以及一个
已经固定的最大不交投影零原子族

\[
R=P_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}P_t
\mathbin{\dot\cup}K.
\tag{2}
\]

本文只攻击三个强制型

\[
(d_1,\ldots,d_t)=(3),\qquad(1,2),\qquad(1,1,1).
\tag{3}
\]

它们共同满足 \(d:=\sum_i d_i=3\)。对每个端点 \(H\in\mathcal A\)，

\[
Q_H:=K\mathbin{\dot\cup}(L\setminus H)
\tag{4}
\]

在 \(C_p^2\) 中是投影零和原子，而且

\[
\bar\sigma(Q_H)=q,\qquad
\sigma(Q_H)=S:=4x-3a-G,\qquad G:=\sum_i\sigma(P_i).
\tag{5}
\]

每个端点本身满足

\[
\rho(\bar\sigma(H))=0,\qquad \bar\sigma(H)=0,\qquad
\sigma(H)=3a,\qquad 6\le |H|\le8.
\tag{6}
\]

以下所有“原子”若未特别说明，均指 \(C_p^2\) 中按实际位置计数的
投影零和原子。本文不改变上游量词，也不假定最大分解或核唯一。

## 2. 两端点交换门的精确当且仅当

取不同端点 \(H,J\in\mathcal A\)，并写

\[
C=H\cap J,\qquad A=H\setminus J,\qquad B=J\setminus H.
\tag{7}
\]

首先，\(A,B\) 都非空。若例如 \(A=\varnothing\)，则
\(H\subsetneq J\)，而

\[
\sigma(J\setminus H)=\sigma(J)-\sigma(H)=0
\]

给出 \(Z\) 的非空实际零和真位置子集，违反 \(Z\) 的实际原子性。
对 \(B\) 相同。

**引理 1（交换—整体例外）。** 对 (3) 中任一强制型及任意不同端点
\(H,J\)，有精确等价

\[
\boxed{
\rho(\bar\sigma(H\cap J))=0
\iff
K=\varnothing\ \text{且}\ L=H\cup J.}
\tag{8}
\]

当 (8) 成立时，还有

\[
A=Q_J,\qquad B=Q_H,
\tag{9}
\]

所以 \(A,B\) 是两个不交原子，并且

\[
\bar\sigma(A)=\bar\sigma(B)=q,\qquad
\bar\sigma(C)=-q,\qquad
\sigma(A)=\sigma(B)=S,\qquad
\sigma(C)=3a-S.
\tag{10}
\]

**证明。** 若 \(\rho(\bar\sigma(C))=0\)，由
\(H=C\dot\cup A\) 与 \(\rho(\bar\sigma(H))=0\) 得
\(\rho(\bar\sigma(A))=0\)。又

\[
\varnothing\ne A\subseteq L\setminus J\subseteq Q_J.
\]

因为 \(Q_J\) 是原子，\(A\) 不能是其非空真投影零子集，故
\(A=Q_J\)。式 (4) 是不交并，而 \(A\subseteq L\setminus J\)，
因此等号同时迫使

\[
K=\varnothing,\qquad L\setminus J=A=H\setminus J,
\]

后一式等价于 \(L=H\cup J\)。交换 \(H,J\) 同样得到
\(B=Q_H\)。这证明正向及 (9)。

反之，若 \(K=\varnothing\) 且 \(L=H\cup J\)，则
\(Q_J=L\setminus J=A\) 的投影和为零。由
\(H=C\dot\cup A\) 及 \(H\) 的投影和为零，立即得到 \(C\) 的投影
和为零。两方向均没有把“非空真子集”误用于整体例外。最后把 (5)--(6)
代入 (7)--(9)，即得 (10)。证毕。

两个立即后果是：

1. 若 \(K\ne\varnothing\)，则 \(\mathcal A\) 的**每一对**不同端点
   的交集都投影非零，而不只限于四条选中边；
2. 即使 \(K=\varnothing\)，所有非覆盖端点对的交集仍投影非零。

## 3. 覆盖对只可能来自两个不同双点迹

记端点的尾迹为

\[
s_i=\{u_i\},\qquad d_i=U\setminus\{u_i\}\quad(1\le i\le3).
\tag{11}
\]

若 (8) 左端成立，则 \(L=H\cup J\) 与 \(U\subseteq L\) 给出

\[
(H\cap U)\cup(J\cap U)=U.
\tag{12}
\]

若这两个迹不交，上游任意迹不交端点对的真实位置引理已经给出
\(\rho(\bar\sigma(H\cap J))\ne0\)，与假设矛盾。因此两迹还必须
相交。在三点集的六个非空真子集中，“并为 \(U\) 且交非空”的
无序对恰为

\[
\boxed{\{d_1,d_2\},\quad\{d_2,d_3\},\quad\{d_3,d_1\}.}
\tag{13}
\]

特别地：

- 两个重复迹的并仍是真子集，不满足 (12)，所以此前重复迹分支的
  “公共部轴向”整支在三种强制原子型中被删除；
- 单点迹之间以及互补的 \(s_i,d_i\) 已由迹不交交集引理删除；
- 唯一可能的轴向交，是两个**不同双点迹**端点组成的覆盖对。

对十一种固定四边图的全部 28,584 个合法迹着色重新枚举后：

\[
\begin{array}{c|r}
\text{没有两个不同双点迹，故逐迹门已强制端点完全图非轴交}&15072\\
\text{至少含一个不同双点迹候选对}&13512\\
\text{候选端点对出现次数（按着色与端点对计）}&24468
\end{array}
\tag{14}
\]

36 个全异着色中 30 个含候选对，六个不含。式 (14) 只枚举迹着色；
它不宣称 13,512 个着色都真有轴向覆盖对。

## 4. 覆盖例外的三片横截结构

现在固定一个幸存覆盖对 \(H,J\)，沿用 (7)。由 (8)--(10)，

\[
L=A\mathbin{\dot\cup}B\mathbin{\dot\cup}C,\qquad
A=Q_J,\quad B=Q_H,\quad K=\varnothing.
\tag{15}
\]

**引理 2（三片横截）。** 每个第三端点
\(E\in\mathcal A\setminus\{H,J\}\) 都满足

\[
\boxed{E\cap A\ne\varnothing,\qquad
E\cap B\ne\varnothing,\qquad E\cap C\ne\varnothing.}
\tag{16}
\]

**证明。** 若 \(E\cap A=\varnothing\)，则

\[
\varnothing\ne A\subseteq L\setminus E=Q_E.
\]

左边 \(A=Q_J\) 是投影零和原子，右边 \(Q_E\) 也是原子，故包含只能
取整体等号 \(A=Q_E\)。于是 \(E=L\setminus A=J\)，与
\(E\ne J\) 矛盾。故 \(E\) 命中 \(A\)；交换 \(A,B\) 得第二式。
所有端点都含共同位置 \(y\)，而 \(y\in H\cap J=C\)，得到第三式。
证毕。

所以 cover-pair 并非一个没有位置内容的整体例外：它把其余至多六个
端点全部压成对三片 \(A,B,C\) 的同时横截。特别地，后续严格 CSP
应保留这三片的实际位置身份，不能只保留三片大小。

## 5. 自动短块把覆盖对压成一行或两行

由 (10)，公共交 \(C\) 的商和为 \(-q\)，所以

\[
D:=X_1\mathbin{\dot\cup}C
\tag{17}
\]

是自动商零短块。上游轴向交集界在这里的系数为 \(t=1\)，并且长度
八已经由唯一正核心尾排除，故

\[
1\le |C|\le6,\qquad 2\le|D|\le7.
\tag{18}
\]

块 \(D\) 含 \(y\notin U\) 且使用一个 \(X\)-位置；因此它不能属于
\(F_3\)，否则产生第二个正核心 \(F_3\) 尾。把这一点代入完整短窗表，
得到精确允许值：

\[
\begin{array}{c|cccccc}
|C|&1&2&3&4&5&6\\ \hline
\sigma(D)/a&1&1&1,2&1,2&1,2&2.
\end{array}
\tag{19}
\]

记表中实际取值为 \(\lambda\)。由 (5)、(10) 与 (17)，

\[
\sigma(C)=3a-S=6a-4x+G,\qquad
\sigma(D)=6a-3x+G,
\]

所以所有覆盖对共享同一个全局和值条件

\[
\boxed{G=3x+(\lambda-6)a.}
\tag{20}
\]

因此多个覆盖对必须使用同一个 \(\lambda\)。例如一个交大小至多二的
覆盖对与一个交大小六的覆盖对不能同时存在。所有覆盖交还具有相同实际
和值 \(3a-S\)；若两个这样的交严格包含，差集会成为 \(Z\) 的非空
实际零和真子集。因此覆盖交族还是一个按包含的反链。

## 6. 显式十位置局部幸存者

引理 1--2 和表 (19) 仍没有自行产生矛盾。下面给出同时适用于
\(p=233,1399\) 的显式局部模型。所有坐标按模 \(p\) 计算；依次写

\[
(q\text{ 轴坐标},\ \rho_1,\ \rho_2,\ a\text{ 坐标}).
\]

取十个位置：

\[
\begin{array}{c|c@{\qquad}c|c}
u_1&(0,1,0,0)&u_2&(0,0,1,0)\\
u_3&(0,1,1,0)&v_1&(1,-1,-2,1)\\
v_2&(1,-2,-1,1)&v_3&(1,-1,-1,1)\\
w_1&(0,0,2,0)&w_2&(0,2,0,0)\\
y&(0,3,4,0)&z&(-2,-3,-4,1).
\end{array}
\tag{21}
\]

令 \(L\) 为这十个位置，并定义五个余部原子：

\[
\begin{array}{c|c|c}
\text{端点迹}&Q_H=L\setminus H&H\cap U\\ \hline
s_1&\{u_2,u_3,v_1\}&\{u_1\}\\
s_2&\{u_1,u_3,v_2\}&\{u_2\}\\
s_3&\{u_1,u_2,v_3\}&\{u_3\}\\
d_1&\{u_1,v_1,w_1\}&\{u_2,u_3\}\\
d_2&\{u_2,v_2,w_2\}&\{u_1,u_3\}.
\end{array}
\tag{22}
\]

直接检查得到：

- 每个 \(Q_H\) 的和都是 \(x+a=(1,0,0,1)\)，且它的三个投影位置
  构成原子；
- \(\sigma(L)=x+4a\)，故五个七位置端点均有实际和 \(3a\)、商和零，
  并都含非轴位置 \(y\)；
- 选择四条边
  \[
  s_1s_2,\quad s_2s_3,\quad s_1d_1,\quad s_2d_2
  \]
  时，它们共享 \(y\)，且四个实际交集的投影和值依次非零；
- \(d_1,d_2\) 两端点覆盖 \(L\)，其交
  \[
  C=\{u_3,v_3,y,z\}
  \]
  投影和为零、商和为 \(-q\)；
- \(X_1\dot\cup C\) 长五、实际和为 \(2a\)，恰是一条表 (19) 允许的
  \(F_2\) 短块，而不是被唯一尾删除的 \(F_3\) 块。

还可把三种 \(K=\varnothing\) packing 接在此局部模型外。令
\(e_1,e_2\) 是 \(C_p^2\) 的一组基：

\[
\begin{array}{c|c|c}
\text{型}&(|P_1|,\ldots,|P_t|)&\rho(R)\\ \hline
(3)&(2p-2)&e_1^{p-1}e_2^{p-2}(e_1+2e_2)\\
(1,2)&(p-1,p-1)&
\bigl(e_1^{p-2}(2e_1)\bigr)\dot\cup
\bigl(e_2^{p-2}(2e_2)\bigr)\\
(1,1,1)&(p-1,p-2,1)&
\bigl(e_1^{p-2}(2e_1)\bigr)\dot\cup
\bigl(e_2^{p-3}(3e_2)\bigr)\dot\cup\{0\}.
\end{array}
\tag{23}
\]

第一行本身是原子；第二行的两个独立坐标原子给出最大二原子分解；
第三行的两个独立坐标原子加零单点给出最大三原子分解。三行长度均为
\(2p-2\)，与 \(|L|=10\) 合并后恰有 \(|Y|=2p+8\)。给各完整原子
配置 (3) 中的轴系数，并使其 \(a\)-坐标总和为 \(-4\)，就有

\[
\sigma(R)=3x-4a,\qquad \sigma(L\dot\cup R)=4x.
\tag{24}
\]

因此这个构造同时实现：冻结长度与总和、三种最大 packing 型、
\(K=\varnothing\)、五个共同 \(Q_H\) 原子、四条共享位置边、一个轴向
双点迹覆盖对、三片横截以及其自动短块。

它**不是**原题候选，也不是完整接口的 SAT 见证。它没有核验：

1. 每个端点长补的所有替代投影原子分解及全部内部子集和；
2. 从完整 \(L\dot\cup R\) 自动生成的所有新 \(F_3\) 块、这些块的
   非零交和各自补原子；
3. 逐位置、逐位置对、逐三元组 Hasse 行；
4. \(Z\) 在 \(C_p^4\) 中的实际原子性。

所以它只严格反驳“若所有 \(Q_H\) 同时为投影原子，则三强制型已自动
矛盾”这一过强推断，并准确定位下一层缺失约束。

## 7. 有限证书与停止线

配套脚本 `unique_tail_forced_common_atoms_attack.py`：

- 枚举十一图的全部 28,584 个合法迹着色并复核 (14)；
- 在 \(p=233,1399\) 逐位置核对 (21)--(22) 的投影原子、实际和值、
  四边交及覆盖短块；
- 对两个素数核对 (23) 的长度、原子和值接口。

报告 `unique_tail_forced_common_atoms_report.json` 的规范 SHA-256 为

\[
\mathtt{4eebafc1497d110e25ac82fe8825f1579fc4957ddd666a5ebd83cdf3f5a749c3}.
\tag{25}
\]

**PROVED：**引理 1 的双向整体例外、(13) 的双点迹唯一性、重复迹轴向
支的删除、引理 2 的三片横截、表 (19) 与固定总和门 (20)。

**DISPROVED AS A LOCAL CLAIM：**“三种强制共同余部原子型本身已经
不相容”。式 (21)--(24) 是可逐项检查的局部反例。

**OPEN：**把所有替代端点分解、全部新 \(F_3\) 及其补原子、完整
Hasse 行与 \(Z\) 实际原子性同时加入后，三个型是否仍有幸存者。
因此全局状态仍为 **INCOMPLETE**。
