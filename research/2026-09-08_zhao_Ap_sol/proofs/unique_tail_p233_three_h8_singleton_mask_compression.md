# \(p=233\) 三个长八 singleton 的 73 态掩码压缩

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. singleton 对不能交七点

剩余 180 个 outer rows 的三个 singleton 端点记为

\[
H_i\cap U=\{u_i\},
\qquad |H_i|=8,
\qquad \sigma(H_i)=3a
\quad (i=1,2,3).
\tag{1}
\]

三者都含同一个尾外实际位置 \(y_0\)，而三个尾投影
\(e,f,-e-f\) 两两不同。

若 \(|H_i\cap H_j|=7\)，则两个八位置集各自只剩一个差位置。因
\(u_i\in H_i\setminus H_j\)、\(u_j\in H_j\setminus H_i\)，必有

\[
H_i\setminus H_j=\{u_i\},
\qquad
H_j\setminus H_i=\{u_j\}.
\tag{2}
\]

但 (1) 的完整实际和值相同，故 (2) 给
\(\sigma(u_i)=\sigma(u_j)\)，投到 \(\rho\) 后与三个尾标签两两不同
矛盾。因此

\[
\boxed{|H_i\cap H_j|\le6\quad(i\ne j).}
\tag{3}
\]

等价地，每个有序差片至少含两个位置，且
\(|H_i\mathbin\triangle H_j|\ge4\)。这是比 containment 与“完全相同
余部”更细的纯 mask 门。

## 2. 四整数穷尽全部 singleton 掩码

去掉固定的 \(U,P,y_0\) 后，按一个实际位置属于
\(H_1,H_2,H_3\) 中哪几者，把位置分成成员型 \(A_S\)
（\(S\subseteq\{1,2,3\}\)）。置

\[
a=n_{12},\qquad b=n_{13},\qquad c=n_{23},\qquad d=n_{123}.
\tag{4}
\]

每个端点除自己的尾和 \(y_0\) 外还含六个位置，所以三个 singleton
成员型的重数被唯一恢复为

\[
\begin{aligned}
n_1&=6-a-b-d,\\
n_2&=6-a-c-d,\\
n_3&=6-b-c-d.
\end{aligned}
\tag{5}

因此初始掩码恰由非负四元组 \((a,b,c,d)\) 参数化，并只需 (5)
非负。式 (3) 进一步等价于

\[
a+d\le5,
\qquad b+d\le5,
\qquad c+d\le5.
\tag{6}

直接有限枚举得到

\[
\begin{array}{c|cc}
&\text{有标号四元组}&S_3\text{ 轨道}\\ \hline
\text{仅 (5)}&256&80\\
\text{再加 (6)}&237&73.
\end{array}
\tag{7}
\]

若把 461 complete-deletion 的见证端点规范为 \(H_1\)，只商稳定它的
\(S_2\) 后有 147 个 pointed 状态；实现时也可保留 73 个无标号状态，
再附加三选一见证变量。

## 3. 450--461 点共同核与三个小等和 fringe

令

\[
C_\triangle=Q_1\cap Q_2\cap Q_3=A_\varnothing.
\tag{8}
\]

去掉 \(U,P,y_0\) 后共有 468 个环境位置。由 (4)--(5)，三个端点的
额外位置并大小为

\[
18-a-b-c-2d,
\tag{9}
\]

故

\[
\boxed{|C_\triangle|=450+a+b+c+2d.}
\tag{10}
\]

在 (5)--(6) 下，73 个轨道按 \(|C_\triangle|=450,\ldots,461\) 的
分布依次为

\[
1,1,3,4,7,9,13,12,11,7,4,1.
\tag{11}
\]

每个 \(Q_i\) 长 464，并可逐位置写成

\[
Q_i=C_\triangle\mathbin{\dot\cup}F_i,
\qquad
F_i=\{u_j,u_k\}\mathbin{\dot\cup}
A_j\mathbin{\dot\cup}A_k\mathbin{\dot\cup}A_{jk},
\tag{12}
\]

其中 \(\{i,j,k\}=\{1,2,3\}\)。所以三个 fringe 具有共同大小

\[
\boxed{m=|F_i|=464-|C_\triangle|,qquad3\le m\le14.}
\tag{13}
\]

三个 \(H_i\) 的完整实际和相同，而 \(Q_i=(Y\setminus P)\setminus H_i\)，
故三个 \(Q_i\)、继而三个 fringe 也有相同的完整实际和：

\[
\boxed{\sigma(F_1)=\sigma(F_2)=\sigma(F_3).}
\tag{14}
\]

因 \(C_\triangle\) 是每个投影原子的真子序列，它本身投影零和自由。
若 \(Q_i\) 是 461 定理选出的端点，则它的非尾位置恰分成

\[
N_i=C_\triangle\mathbin{\dot\cup}(F_i\setminus U).
\tag{15}
\]

至多一个非尾删点不 complete，因此 \(C_\triangle\) 中至少
\(|C_\triangle|-1\) 个、\(F_i\setminus U\) 中至少 \(m-3\) 个删点
complete。

## 4. 唯一的 \(m=3\) 状态

式 (11) 的 \(|C_\triangle|=461\)、即 \(m=3\) 层只有一个轨道：

\[
(a,b,c,d)=(1,1,1,4).
\tag{16}
\]

此时 \(n_1=n_2=n_3=0\)，并存在三个不同成员型的实际位置
\(v_i\in A_{jk}\)，使

\[
F_i=\{u_j,u_k,v_i\}.
\tag{17}
\]

由 (14) 及 \(\sigma(U)=\sigma(u_1)+\sigma(u_2)+\sigma(u_3)\)，存在
同一个完整实际标签差 \(\Delta\)，满足

\[
\boxed{\sigma(v_i)-\sigma(u_i)=\Delta\quad(i=1,2,3).}
\tag{18}
\]

事实上必须有更强的

\[
\boxed{\rho(\Delta)\ne0.}
\tag{19}
\]

因为 (17)--(18) 给
\(\rho(\sigma(F_i))=\rho(\Delta)\)。若它为零，则三位置
\(F_i\) 是长 464 投影原子 \(Q_i\) 的非空真零和子序列，直接矛盾。
特别地 \(\Delta\ne0\)；在更弱的完整标签层，\(\Delta=0\) 也会使
三个不同的尾外位置 \(v_i\) 逐一复制三个尾标签，形成第二个字面
三位置尾。

## 5. 裁决与执行接口

新 pair 门把 singleton 掩码从 80 个轨道压到 73 个，但没有单独删除
outer row；例如 \((a,b,c,d)=(0,0,0,0)\) 的三组私有六位置花瓣可嵌入
每一行。后续不应穷举所有四至六端点的完整 Venn 图，而应先在这 73 个
singleton 状态上加载统一 \(\rho,q\)、三个长补原子、461 删点、全部
自动短块与实际 \(Z\) 原子；只有幸存时才懒加入其余端点。

第一解析目标是唯一的 \(m=3\) 状态，其次是 \(m=4\)。聚合计数可以
保留 (4)，但 complete 删除和内部子集和仍必须引用每个实际位置。
剩余 180 行、固定 \(p=233\) 切片及全局 \(A_p\) 保持
**INCOMPLETE**。
