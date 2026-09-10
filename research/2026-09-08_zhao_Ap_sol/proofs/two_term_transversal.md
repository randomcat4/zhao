# 二项 \(a\) 块强制的两点横截与共度

STATUS: PROVED_HERE

设 \(E=\{x,y\}\in\mathcal F_1\) 是任意二项、实际和为 \(a\) 的块。
由 \(\mathcal F_1\pitchfork\mathcal F_3\)，每个 \(3a\) 块都与
\(E\) 相交；所以 \(E\) 是 \(\mathcal F_3\) 的两点横截。

令 \(w(A)=(-1)^{|A|-1}\)，并按 \(A\cap E\) 把 \(\mathcal F_3\)
分成“只含 \(x\)”“只含 \(y\)”和“同时含 \(x,y\)”三类，其带符号
总数分别记为 \(s_x,s_y,s_{xy}\)。不存在与 \(E\) 不交的第四类。
由 \(c_Z(3a)=0\) 及逐点带符号度 \(-1/20\)，

\[
s_x+s_y+s_{xy}=0,\qquad
s_x+s_{xy}=s_y+s_{xy}=-\frac1{20}.
\]

解得

\[
\boxed{s_x=s_y=\frac1{20},\qquad s_{xy}=-\frac1{10}.}
\]

三类因此都非空。由整数剩余类的绝对值提升，只含 \(x\) 与只含
\(y\) 的 \(3a\) 块各至少有 \(\lceil(p-1)/20\rceil\) 个，同时含
二者的至少有 \(\lceil(p-1)/10\rceil\) 个。

对位置对 \((x,y)\)，第三族共度是

\[
d_3(x,y)=\sum_{A\supset E}(-1)^{|A|}=-s_{xy}=\frac1{10}.
\]

代入两条二点删除恒等式得到

\[
\boxed{d_1(x,y)=1,\qquad d_2(x,y)=-\frac12,\qquad
d_3(x,y)=\frac1{10}.}
\]

事实上可以把三族相对 \(E\) 的全部四格带符号交分布写完。列依次
表示与 \(E\) 不交、只含 \(x\)、只含 \(y\)、同时含二者：

\[
\boxed{
\begin{array}{c|rrrr}
 &\varnothing&x&y&xy\\ \hline
\mathcal F_1&\frac12&\frac14&\frac14&-1\\
\mathcal F_2&-\frac1{10}&-\frac15&-\frac15&\frac12\\
\mathcal F_3&0&\frac1{20}&\frac1{20}&-\frac1{10}
\end{array}}
\]

每一行只用该族总带符号和为零、两个逐点度及上述逐对度求得。
\(\mathcal F_1\) 的 \(xy\) 格确实只有 \(E\)：同和块构成反链，
任何更大的 \(a\) 块都不能包含 \(E\)。

表中两条对角格还有真实的加块双射：

\[
\boxed{
\{D\in\mathcal F_1:D\cap E=\varnothing\}
\xleftrightarrow{\ D\mapsto D\dot\cup E\ }
\{C\in\mathcal F_2:E\subset C\},}
\]

\[
\boxed{
\{D\in\mathcal F_2:D\cap E=\varnothing\}
\xleftrightarrow{\ D\mapsto D\dot\cup E\ }
\{A\in\mathcal F_3:E\subset A\}.}
\]

例如第一条中若 \(|D|=6\)，则 \(D\dot\cup E\) 会是八项 \(2a\)
块，违反 \(2a\) 的七项上界，所以这种 \(D\) 不存在；第二条同理
排除与 \(E\) 不交的七项 \(2a\) 块。逆映射只是删去 \(E\)，实际
和分别下降一个 \(a\)。

特别地，至少有 \(\lceil(p-1)/2\rceil\) 个不同的 \(2a\) 短块
包含 \(E\)。每个这样的块 \(C\) 都唯一写成

\[
C=E\mathbin{\dot\cup}D,\qquad D\in\mathcal F_1,\quad2\le|D|\le5,
\]

故还强制至少 \(\lceil(p-1)/2\rceil\) 个与 \(E\) 不交的
\(a\) 块；同时至少有 \(\lceil(p-1)/10\rceil\) 个与 \(E\)
不交的 \(2a\) 块，并与同时含 \(E\) 的 \(3a\) 块一一对应。

令后一族为

\[
\mathcal D_E={D\in\mathcal F_2:D\cap E=\varnothing\}.
\]

则

\[
|\mathcal D_E|\ge\left\lceil\frac{p-1}{10}\right\rceil,
\qquad 4\le|D|\le6.
\]

每个 \(D\in\mathcal D_E\) 给出 \(A_D=E\dot\cup D\in\mathcal F_3\)，
故 \(Z\setminus A_D\) 是长度 \(3p-2,3p-3\) 或 \(3p-4\) 的
\(C_p^3\) 原子。若 \(D\ne D'\)，由不同 \(3a\) 块的交集商和非零，

\[
0\ne\bar\sigma(A_D\cap A_{D'})
=\bar\sigma(E)+\bar\sigma(D\cap D')
=\bar\sigma(D\cap D').
\]

因此 \(\mathcal D_E\) 是一族线性多个、两两有非零商交的 4--6 项
\(2a\) 块，并同时产生同样多个近 Davenport 补原子。这把第二支
从单个补原子接口推进到了真实的多补原子交换系统。

最后，所有二项 \(a\) 块组成的图 \(\Gamma_a\) 的匹配数至多三。
否则四条位置不交的边之并实际和为 \(4a\)，再加入冻结序列中的
\(p-4\) 个锚点就得到长度

\[
8+(p-4)=p+4\le3p-2
\]

的非空实际零和。按实际群值分层，\(\Gamma_a\) 是若干完全二部图
\(K_{m_g,m_{a-g}}\) 与半值 \(g=a/2\) 上的完全图之不交并；每个
值类大小至多 \(p-4\)。每个分量的边数至多 \((p-4)\) 乘其匹配数，
因此

\[
\boxed{\nu(\Gamma_a)\le3,\qquad |E(\Gamma_a)|\le3(p-4).}
\]

若六项 \(2a\) 块走 (20) 的第二支，则该支给出的二项块正是这样的
\(E\)，所以整个两点横截、精确共度和线性多的分解块结构都被强制。
