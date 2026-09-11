# \(p=233\) 三长八 \(m=3\) 九轨的 opposite-fibre 横截闭合

STATUS: **PROVED SUBBRANCH / SELF-CHECKED FINITE CERTIFICATE /
INDEPENDENT REVIEW CORRECT / GLOBAL INCOMPLETE**

## 1. 范围与冻结接口

本文只处理三个 singleton endpoint 都长八、singleton mask 为唯一
\(m=3\) 态的分支。沿既有记号

\[
Q_i=C\mathbin{\dot\cup}\{u_j,u_k,v_i\},
\qquad |C|=2p-5=461,
\tag{1}
\]

\[
w_1=e,\quad w_2=f,\quad w_3=-e-f,
\qquad \rho(v_i)=w_i+\delta.
\tag{2}
\]

本稿使用且只使用如下已审接口。

1. **UV gate 与共同 endpoint 核。** 六个
   \(\delta=w_j-w_i\) 已排除，故 \(\delta\) 遍历核曲线
   \[
   q_0(\delta)=3
   \tag{3}
   \]
   上的 228 个 generic 点。五位置共同 endpoint 核、fringe 实际等和
   及 complete pointing 均保留字面位置身份。
2. **共同核 signed 系数。** 生成积
   \[
   \Psi_C=\prod_{c\in C}(1-X^{\rho(c)})
   \tag{4}
   \]
   的系数函数为已证三次式 \(c_\delta(r)=[X^r]\Psi_C\)。本文只用
   \(c_\delta(r)\ne0\Rightarrow\) 至少一个真实位置子集表示 \(r\)，
   绝不把 \(c_\delta(r)\) 当作普通无符号计数。
3. **mixed separator。** 对 \(r\in\{s,-s\}\)，任何
   \(E\subseteq Q_i\setminus U\) 且 \(\rho(E)=r\) 的避尾表示满足
   \[
   1\le |E|\le2.
   \tag{5}
   \]
   正负两族还逐表示交叉相交：
   \[
   E_+\cap E_-\ne\varnothing.
   \tag{6}
   \]
4. **mixed height table。** 双点表示还满足完整实际
   \(2\leftrightarrow1\) 等式。该接口在本稿闭合前尚未用到；因此
   本稿没有给任何商投影表示伪造实际 \(q\)/height lift。
5. **completion pointing。** 至少一个 endpoint \(i\) 满足
   \(B_i=C\dot\cup\{u_j,u_k\}\) complete、至少 460 个 \(C\)-删点
   complete，并有 cancellation line 与 fixed-target kernel 门。本稿
   只保留这个 endpoint 的三选一 pointing；更深的 460 表示结构无需
   启动。
6. **自动短块与不交规则。** \(F_3\) 与每条短块相交，\(F_2\) 族内
   相交；但在 \(p=233\) 时，两条至多八项的块总长至多 16，不能触及
   中间禁区起点 \(p+2=235\)。本文在自动短闭包启动前已由 (5)--(6)
   关闭全部候选。

## 2. ordinary fibre 的 pointed 横截引理

固定 completion-pointed endpoint \(i\)。对
\(\varepsilon\in\{+1,-1\}\) 定义

\[
t_{\varepsilon,i}=\varepsilon s-(w_i+\delta),
\qquad
A_{\varepsilon,i}=\nu_{t_{\varepsilon,i}}(C).
\tag{7}
\]

此前的 fibre recovery 已严格证明

\[
A_{\varepsilon,i}
\equiv-c_\delta(t_{\varepsilon,i})
+\mathbf1_{t_{\varepsilon,i}=0}\pmod {233},
\qquad0\le A_{\varepsilon,i}\le229,
\tag{8}
\]

并且 (8) 的每个单位都对应 \(C\) 中一个字面位置，不是 signed
系数的形式单位。

**引理 1（opposite-fibre transversal）。** 若
\(r\in\{s,-s\}\) 且 \(c_\delta(r)\ne0\)，则

\[
\boxed{A_{-r,i}\le2.}
\tag{9}
\]

若 \(A_{-r,i}=2\)，还必须有

\[
\boxed{2t_{-r,i}=r.}
\tag{10}
\]

这里 \(t_{-r,i}=-r-(w_i+\delta)\)。

**证明。** 由 (4) 的定义，\(c_\delta(r)\ne0\) 只说明 signed 和中
至少有一项，故存在真实字面子集

\[
F_r\subseteq C,
\qquad \rho(F_r)=r.
\tag{11}
\]

因为 \(r\ne0\)，\(F_r\ne\varnothing\)。又
\(C\subseteq Q_i\setminus U\)，所以 mixed separator 逐个表示给

\[
|F_r|\le2.
\tag{12}
\]

对 \(C\) 中每个投影为 \(t_{-r,i}\) 的字面位置 \(c\)，都有

\[
\rho(\{v_i,c\})=(w_i+\delta)+t_{-r,i}=-r.
\tag{13}
\]

故 \(\{v_i,c\}\subseteq Q_i\setminus U\) 是相反符号的避尾双点
表示。(6) 迫使

\[
F_r\cap\{v_i,c\}\ne\varnothing.
\tag{14}
\]

但 \(F_r\subseteq C\) 且 \(v_i\notin C\)，所以 (14) 逐字面迫使
\(c\in F_r\)。因此该 fibre 的全部 \(A_{-r,i}\) 个不同位置都在
至多两点的 \(F_r\) 内，证明 (9)。若等号成立，\(F_r\) 恰为这两个
同投影 fibre 位置，比较其和值便得 (10)。证毕。

引理 1 比“\(A_{-r,i}\le2\)”单独容量门更强，因为保留了等号时的
共振式 (10)；相对于对三个 endpoint 同时使用的版本，本文只在被
pointing 选中的一个 endpoint 上施加，因而是严格较弱、但已足够的
版本。

## 3. 九轨与 27 pointed 角色的完整表

三次式采用已证参数

\[
G=(\alpha-\beta)^{-1},\quad
F={-2-G\beta\over3\alpha},\quad
I={-2+G\alpha\over3\beta},
\tag{15}
\]

\[
c_\delta(x,y)=1-x^2+xy-y^2
+F(x^3-x)+I(y^3-y)+G(x^2y-xy^2).
\tag{16}
\]

有限证书从九个代表重新计算 (7)--(8)、\(c_\delta(\pm s)\) 和
引理 1；六元 \(A\) 顺序为
\((A_{+,1},A_{+,2},A_{+,3},A_{-,1},A_{-,2},A_{-,3})\)：

\[
\begin{array}{c|c|c|c|c|c}
O&\delta&s&(c_\delta(s),c_\delta(-s))&A&\text{通过的 pointed }i\\ \hline
1&(10,193)&(69,197)&(157,5)&(3,49,73,22,11,89)&\varnothing\\
2&(12,25)&(12,25)&(230,232)&(0,0,0,229,151,68)&\varnothing\\
3&(18,181)&(18,181)&(230,232)&(0,0,0,51,5,159)&\varnothing\\
4&(29,78)&(1,2)&(225,4)&(198,0,2,7,8,0)&\varnothing\\
5&(29,184)&(8,199)&(0,47)&(38,20,77,0,0,0)&\varnothing\\
6&(33,168)&(29,191)&(225,53)&(114,3,1,7,3,1)&\{3\}\\
7&(44,154)&(39,33)&(152,0)&(0,0,0,126,65,26)&\varnothing\\
8&(56,128)&(56,128)&(230,232)&(0,0,0,26,60,129)&\varnothing\\
9&(66,142)&(3,60)&(124,10)&(9,0,0,7,4,143)&\varnothing.
\end{array}
\tag{17}
\]

27 个 pointed 轨中，25 个由 (9) 的 \(A>2\) 排除。唯一没有
\(A>2\) 见证但仍失败的是 \(O4/i=3\)：对 \(r=-s=(232,231)\)，

\[
A_{+,3}=2,\qquad t_{+,3}=(206,158),\qquad
2t_{+,3}=(179,83)\ne r,
\tag{18}
\]

违反 (10)。故基本门严格留下且只留下 \(O6/i=3\)。

## 4. 最后角色的四标签零和矛盾

现在固定

\[
\delta=(33,168),\qquad s=(29,191),\qquad i=3.
\tag{19}
\]

由 (17)，\(c_\delta(s)=225\ne0\)、
\(c_\delta(-s)=53\ne0\)，且相反两个 fibre 都恰有一个字面位置：

\[
t_{-,3}=(172,108),\quad A_{-,3}=1,
\qquad
t_{+,3}=(230,24),\quad A_{+,3}=1.
\tag{20}
\]

取 (11) 的两个真实表示 \(F_+,F_-\)。引理 1 的证明逐字面给

\[
t_{-,3}\in\rho(F_+),qquad
t_{+,3}\in\rho(F_-).
\tag{21}
\]

两者都不可能是单点，因为
\(t_{-,3}\ne s\)、\(t_{+,3}\ne-s\)。结合 \(|F_\pm|\le2\)，
它们被迫是双点，第二个位置的投影分别为

\[
s-t_{-,3}=(90,83),
\qquad
-s-t_{+,3}=(207,18).
\tag{22}
\]

四个投影标签

\[
(172,108),\ (90,83),\ (230,24),\ (207,18)
\tag{23}
\]

两两不同，所以对应四个实际位置两两不同。于是
\(F_+\cap F_-=\varnothing\)，直接违反 (6)。等价地，

\[
\rho(F_+\mathbin{\dot\cup}F_-)=s+(-s)=0
\tag{24}
\]

给出 \(C\) 内非空真投影零和四位置子序列，违反 \(C\) 的零和自由性。
最后一个角色亦被排除。

## 5. 量词分母与有限证书

generic 曲线点数、每点 admissible 有向 packing 方向数分别为

\[
228,\qquad 233^2-1-6=54\,282.
\tag{25}
\]

所以 fibre-recovery 前的完整作用域为

\[
228\cdot54\,282=12\,376\,296
\tag{26}
\]

个 \((\delta,s)\) 对；加入 completion 三选一 pointing 后为

\[
3\cdot12\,376\,296=37\,128\,888.
\tag{27}
\]

上一步完整普查留下 108 个有向 \((\delta,s)\) 对，即九个
\(S_3\times\{\pm1\}\) 轨；加入 pointing 后是 324 个形式对，即
27 个 pointed 轨。本文的新删减为

\[
27\xrightarrow{\text{引理 1}}1
\xrightarrow{\text{式 (20)--(24)}}0,
\tag{28}
\]

或在有向 pointed 形式对层

\[
324\longrightarrow12\longrightarrow0.
\tag{29}
\]

配套程序
`unique_tail_p233_three_h8_m3_nine_orbit_short_closure.py` 不导入旧的
候选分类模块。它从九个代表与 (15)--(16) 独立重算：

1. 234 个曲线点、六个例外点、228 个 generic 点及每点 54,282 个
   admissible 方向的分母；
2. 九个代表的六个 target、六个 ordinary fibre 重数及
   \(c_\delta(\pm s)\)；
3. 九个大小 12、两两不交的 unpointed 轨，其并恰有 108 个形式对；
4. 27 个大小 12、两两不交的 pointed 轨，其并恰有 324 个形式对；
5. 每个轨道所有 12 个像上的引理 1 判定协变；
6. 25 个容量失败、一个共振失败、唯一角色的四标签证书及最终零
   survivor。

程序写出同前缀 JSON 报告，保存全部 27 行逐符号检查，而不是只保存
九行结论。

## 6. 裁决与边界

\[
\boxed{\textbf{PROVED: }p=233\text{ 的三长八 singleton }m=3
\text{ 掩码分支为空。}}
\tag{30}
\]

六个 exceptional \(\delta\) 已由上游共同 endpoint 核闭合；本文关闭
余下 228 个 generic 点经完整 fibre recovery 后的全部九轨。因为
separator 层已经得到矛盾，原工作单要求加入的统一 \(q\)-高度、全部
自动短块、460 个 complete deletion 内部见证与 cancellation line
CSP 的定义域现为空，无需构造放宽 lift。

这严格强于“九轨参数进一步压缩”，但仍严格弱于排除其余
\(m=4,\ldots,14\) singleton mask，亦不单独证明固定 \(p=233\) 的
完整切片或一般 \(A_p\)。全局状态保持 **INCOMPLETE**。
