# \(p-4\) 单高度纤维：多尾偏序—全局计数接口

STATUS: **INCOMPLETE / PROVED_GLOBAL_SUBTHEOREMS / FORMAL_TAIL_INTERFACE_COMPATIBILITY**

## 1. 对象与量词

设 \(p\ge11\) 为素数，沿用冻结设置
\[
X=x^m\subset B,\quad m=p-4,\quad \bar x=q\ne0,\quad
Y=Z\setminus X ,
\tag{1}
\]
以及 \(T\in\mathcal F_3\)、\(6\le |T|\le8\)、\(B=Z\setminus T\)
在 \(C_p^3\) 中为原子。记全部正核心 \(F_3\) 实际余部为
\(\mathscr U=\mathscr U_3^+\)。每个 \(U\in\mathscr U\) 有唯一参数
\[
(\ell,b,r),\quad \ell\in\{6,7,8\},\quad1\le b\le\ell-2,\quad
r=|U|=\ell-b,
\tag{2}
\]
且
\[
\bar\sigma(U)=-bq,\qquad \sigma(U)=3a-bx.
\tag{3}
\]

偏序对象是实际位置子集。标签、和值和参数相同但使用不同位置副本的
余部仍是不同对象；只有位置子集相同才相等。
\(U'\subsetneq U\) 始终指位置意义下的真包含。

本文证明链长、宽度、可比对计数、三链实际菱形补全及 21 式聚合秩
五项严格结论。第 7 节只有形式尾接口相容性：它未重建所赋位置诱导
出的全部长度 \(2\)--\(8\) 商零块与短零和谱，故不登记为局部候选、
DISPROVED 或全局反例。原单高度分支仍为 INCOMPLETE。

## 2. 已证输入

固定 \(X\)-点的第三族点度及普通尾数提升是
\[
\sum_{U\in\mathscr U}(-1)^{\ell(U)-1}
\binom{m-1}{b(U)-1}=-\frac1{20}\quad(\mathbb F_p),
\tag{4}
\]
\[
K:=|\mathscr U|\ge\left\lceil\frac{p-1}{2520}\right\rceil.
\tag{5}
\]
已有嵌套方向定理给
\[
U'\subsetneq U\Longrightarrow
b(U')-b(U)\in\{1,2,3\}.
\tag{6}
\]
又因 \(X\) 已含 \(p-4\) 个实际值 \(x\) 的位置，而冻结高度至多
\(p-4\)，
\[
y\in Y\Longrightarrow y\ne x\quad\text{作为实际群值}.
\tag{7}
\]

## 3. 链长至多三与宽度下界

**定理 1。**
\[
\operatorname{height}(\mathscr U,\subseteq)\le3,\qquad
\operatorname{width}(\mathscr U,\subseteq)\ge
\left\lceil\frac{p-1}{7560}\right\rceil.
\tag{8}
\]

**证明。** 对 \(U'\subsetneq U\)，令
\[
d=b(U')-b(U),\qquad t=|U\setminus U'|.
\]
由 (3) 有
\[
\sigma(U\setminus U')=dx.
\tag{9}
\]
若 \((d,t)=(1,1)\)，差集唯一位置的实际值就是 \(x\)，违反 (7)。
故每步真包含满足
\[
d\ge1,\quad t\ge1,\quad(d,t)\ne(1,1).
\tag{10}
\]

若有四元素链
\(U_0\supsetneq U_1\supsetneq U_2\supsetneq U_3\)，令
\(d_i=b(U_i)-b(U_{i-1})\)。把 (6) 用于极端两尾，得
\[
d_1+d_2+d_3=b(U_3)-b(U_0)\le3.
\]
所以三个 \(d_i\) 全为一；(10) 又迫使三个尾大小降幅都至少为二。
于是 \(r(U_0)-r(U_3)\ge6\)，但 (2) 给该差至多 \(7-2=5\)，
矛盾。

按一个尾作为链底端时的最大链长将 \(\mathscr U\) 分成三层；每层
都是反链。最大层至少有 \(\lceil K/3\rceil\) 个尾，结合 (5) 得
第二式。\(\square\)

精确阈值形式为
\[
p>7560w+1\Longrightarrow\operatorname{width}(\mathscr U)\ge w+1
\quad(w\ge1).
\tag{11}
\]
特别地，\(p>7561\) 时全部尾不可能排成一条链；若 \(K\le R\)，
则 (5) 强制 \(p\le2520R+1\)。

当 \(p\ge17\) 时任意两尾核心数和至多 \(12\le m\)，故可选不交
\(X\)-核心。第三族自交和完整核心交数禁值给
\[
U\cap U'\ne\varnothing,\qquad
\bar\sigma(U\cap U')\ne0\quad(U\ne U').
\tag{12}
\]
所以 (8) 给出一个至少有 \(\lceil(p-1)/7560\rceil\) 个成员的
实际反链，其成员两两非零商交，且每个成员满足
\[
\varnothing\ne U\cap T\subsetneq T,\qquad
\bar\sigma(U\cap T)\ne0.
\tag{13}
\]
这是尾数、嵌套方向、可实现核心区间与 \(T\)-部分的严格全局联立。

## 4. 可比尾对至多线性多个

**定理 2。** 无序可比异尾对数 \(C\) 满足
\[
C\le112K.
\tag{14}
\]

**证明。** 每个可比对由较大的位置集唯一计数。若上尾大小至多六，
它至多含 \(\sum_{j=2}^{r-1}\binom rj\le56\) 个大小至少二的真
子集。唯一大小七的上尾类型是 \((\ell,b,r)=(8,1,7)\)。由 (6)，
它的下尾满足 \(b'\le4\)；大小六的下尾只能对应
\((b'-b,r-r')=(1,1)\)，已被 (7)--(10) 排除。因此只需计其大小
二至五的子集，共
\[
\binom72+\binom73+\binom74+\binom75=112.
\]
同一位置子集的 \(b\) 由 (3) 唯一，不会重复计数。求和即得结论。
\(\square\)

所以不嵌套尾对至少有
\[
\max\left(0,\binom K2-112K\right).
\tag{15}
\]
这里只计尾身份对，不声称不同尾对产生不同交换尾。

## 5. 三链被实际交换补成菱形

**定理 3。** 设
\[
U_0\supsetneq U_1\supsetneq U_2
\tag{16}
\]
是三条实际正核心 \(F_3\) 尾。写 \(b_i=b(U_i)\)，令
\[
A=U_0\setminus U_1,\qquad D=U_1\setminus U_2,\qquad
d=b_1-b_0.
\]
则还存在实际正核心 \(F_3\) 尾
\[
\widehat U_1=U_2\mathbin{\dot\cup}A,\qquad
\widehat b_1=b_2-d=b_0+(b_2-b_1),
\tag{17}
\]
且
\[
U_2\subsetneq\widehat U_1\subsetneq U_0,\qquad
\widehat U_1\ne U_1.
\tag{18}
\]

**证明。** 由 (3)，
\[
\bar\sigma(A)=dq,\qquad \sigma(A)=dx.
\tag{19}
\]
对极端两尾 \(U_0,U_2\) 使用已证的精确二尾交换，取
\(E=A,F=\varnothing\) 及核心差 \(d\)。若
\(k_0=\max(0,b_0+b_2-m)\)，压缩可实现区间为
\[
-b_0+k_0\le d\le b_2-k_0.
\]
左式显然；当 \(k_0>0\) 时右式等价于 \(b_1\le m\)，而
\(b_1\le6<m\)；当 \(k_0=0\) 更直接。因此确有实际父块核心实现
该交换。

式 (19) 使实际缺陷 \(\delta=0\)。精确交换定理先从两个实际父块
产生实际短块，再由 \(\delta=0\) 和长度窗将其识别为实际 \(F_3\)
块；同值替换给出完整正核心层。因此 \(\widehat U_1\) 不是形式尾，
而确实属于 \(\mathscr U\)。并且
\(\widehat b_1=b_0+(b_2-b_1)\ge2\)，所以它确为正核心尾。

\(A,D\) 都非空，故 (18) 成立。交换两个中间尾等价于在
\(U_0\setminus U_2=A\mathbin{\dot\cup}D\) 中取补集，形成无固定点
对合；每个三层包含区间的中间尾数因而为偶数。\(\square\)

十五种类型的精确有限审计给出：只用 (6)、(10) 时有 23 种三链
参数；代入 (17) 的新块长度窗后七种不可能，余下十六种强制合法
菱形。枚举只核对常数类型表；实际尾的存在来自上述全称交换证明。

## 6. 21 条安全聚合 Hasse 式的秩边界

记
\[
N_{\lambda,\ell,b}=|\mathcal U_{\lambda,\ell,b}|,\qquad
J_{\lambda,\ell,b}=
\sum_{U\in\mathcal U_{\lambda,\ell,b}}|U\cap T|.
\tag{20}
\]
考虑既有唯一尾 Hasse 稿中的 21 条安全聚合方程。任意固定全部
正核心第三族数据
\[
(N_{3,\ell,b},J_{3,\ell,b})\quad(b\ge1),
\tag{21}
\]
只保留第一、二族全部 \(N,J\) 及第三族三个零核心类型的 \(N,J\)
为九十个模 \(p\) 自由变量。

**定理 4（聚合秩定理）。** 对每个 \(p\ge11\) 和
\(|T|\in\{6,7,8\}\)，数据 (21) 可扩张为 21 式的
\(\mathbb F_p\) 解，当且仅当它满足第三族固定 \(X\)-点度 (4)。

**证明。** 自由变量在第三族 \(X\)-点度行的系数全为零，故 (4)
必要。删去该行。用
\[
\binom{p-c}{j}\equiv\binom{-c}{j}
=(-1)^j\binom{c+j-1}{j}\pmod p
\tag{22}
\]
后，余下二十行的自由系数矩阵与 \(p,|T|\) 均无关。取列
\[
\begin{aligned}
&(N_{1,2,0},J_{1,2,0},N_{1,2,1},J_{1,2,1},
N_{1,3,0},N_{1,3,1},N_{1,3,2},J_{1,3,2},\\
&N_{1,4,2},N_{1,4,3},
N_{2,4,0},J_{2,4,0},N_{2,4,1},J_{2,4,1},N_{2,4,2},\\
&N_{2,5,0},N_{2,5,1},
N_{3,6,0},J_{3,6,0},N_{3,7,0}),
\end{aligned}
\tag{23}
\]
对应 \(20\times20\) 小行列式为
\[
-512000=-2^{12}5^3.
\tag{24}
\]
它对 \(p\ge11\) 非零，故删行后的矩阵满行秩二十，可解任意右端。
唯一相容条件就是被删去的 (4)。\(\square\)

这一定理允许任意多条、任意类型及任意 \(T\)-入射的正核心第三族
数据，说明继续只在 \((N,J)\) 层叠加这 21 式不会排除多尾。所得
自由变量只是有限域元素，不是普通非负计数，也不保证实际位置入射。

## 7. FORMAL_TAIL_INTERFACE_COMPATIBILITY

本节只构造命名尾与列出接口的形式相容点，不构造实际
\(\mathscr U_3^+\)。

取商群基 \(e_1,e_2,e_3\)，令
\[
q=e_1,\quad x=(e_1;0),\quad w=(e_2;0),\quad z=(e_3;0).
\tag{25}
\]
给一个命名六项 \(T\)-块赋标签 \(w,z\) 及
\[
(2e_1;a),\quad(-2e_1-e_2-e_3;0),\quad
(2e_2;a),\quad(-2e_2;a).
\tag{26}
\]
这些标签的商和为零、实际和为 \(3a\)。这只核对命名 \(T\) 的和值，
不核对其补集原子或全诱导短块。

令 \(t\in\{1,\ldots,p-1\}\) 满足 \(700t\equiv1\pmod p\)，置
\[
n_5=\lfloor t/2\rfloor,\qquad n_4=t-2n_5\in\{0,1\}.
\tag{27}
\]
对 \(b=4,5\) 取 \(n_b\) 个不同形式位置副本
\[
r_{b,i}=(-be_1-e_2-e_3;3),\qquad
U_{b,i}=\{w,z,r_{b,i}\},
\tag{28}
\]
其类型分别为 \((\ell,b)=(7,4),(8,5)\)。则
\[
\bar\sigma(U_{b,i})=-bq,\quad
\sigma(U_{b,i})=3a-bx,\quad
U_{b,i}\cap T=\{w,z\},
\tag{29}
\]
且 \(e_2+e_3=\bar\sigma(\{w,z\})\ne0\)。命名尾都是三点不同位置
集，形成反链。又
\[
n_5\le(p-1)/2\le p-4,\qquad n_4\le1,
\]
所以命名位置的实际值重数未超界。

不同命名尾的交集是 \(\{w,z\}\)，故对每个可实现核心交数 \(k\)，
\[
\bar\sigma(U_{b,i}\cap U_{c,j})+kq=e_2+e_3+ke_1\ne0.
\tag{30}
\]
两侧差集各至多一个叶点，且
\[
\bar r_b-\bar r_c=(c-b)q,\qquad r_b-r_c=(c-b)x.
\tag{31}
\]
单边叶标签不在 \(\langle q\rangle\)。因此命名尾之间的二尾交换
条件只在
\[
(E,F,d)=(\varnothing,\varnothing,0)
\quad\text{或}\quad
(\{r_b\},\{r_c\},c-b)
\tag{32}
\]
成立，分别返回两个端点。

两种尾对固定 \(X\)-点度的一尾贡献分别为 \(-35,-70\)，所以
\[
-35n_4-70n_5=-35t=-\frac1{20}\pmod p.
\tag{33}
\]
命名尾数 \(K_0=n_4+n_5=\lceil t/2\rceil\)。正整数
\(700t-1\) 是 \(p\) 的倍数，于是
\[
p\le700t-1\le1400K_0-1,\qquad
K_0\ge\left\lceil\frac{p+1}{1400}\right\rceil
\ge\left\lceil\frac{p-1}{2520}\right\rceil.
\tag{34}
\]
固定
\[
N_{3,7,4}=n_4,\ J_{3,7,4}=2n_4,\qquad
N_{3,8,5}=n_5,\ J_{3,8,5}=2n_5
\tag{35}
\]
并令其余正核心第三族聚合数据为零。由定理 4，它对每个
\(|T|=6,7,8\) 都有一个 21 式有限域扩张。

但是，本节没有枚举并加入 (25)--(28) 所赋位置可能另外诱导的
\(F_3\) 块或其他长度 \(2\)--\(8\) 短零和子集，命名尾集不主张
等于真实 \(\mathscr U_3^+\)。所以本节只登记
FORMAL_TAIL_INTERFACE_COMPATIBILITY，不登记为局部反例、局部候选
或 DISPROVED。

## 8. 全局固定点度强制零核心横截块

令 \(\mathcal H_3^0\) 为全部与 \(X\) 不交的实际 \(F_3\) 块。
对每个 \(y\in Y\)，完整第三族固定点度是
\[
\boxed{
\sum_{\substack{H\in\mathcal H_3^0\\y\in H}}(-1)^{|H|-1}
+
\sum_{\substack{U\in\mathscr U\\y\in U}}
(-1)^{\ell(U)-1}\binom m{b(U)}
=-\frac1{20}.}
\tag{36}
\]
定义正核心尾在 \(y\) 的贡献和及亏损点集
\[
P_3^+(y)=
\sum_{\substack{U\in\mathscr U\\y\in U}}
(-1)^{\ell(U)-1}\binom m{b(U)},\qquad
\mathcal D=\{y\in Y:P_3^+(y)\ne-1/20\}.
\tag{37}
\]

**定理 5（亏损点横截覆盖）。** 每个 \(y\in\mathcal D\) 至少属于
一个 \(H\in\mathcal H_3^0\)，从而
\[
|\mathcal H_3^0|\ge
\left\lceil\frac{|\mathcal D|}{8}\right\rceil.
\tag{38}
\]
而且每个 \(H\in\mathcal H_3^0\) 都是 \(\mathscr U\) 的非零商交
横截：
\[
H\cap U\ne\varnothing,\qquad
\bar\sigma(H\cap U)\ne0
\quad(H\in\mathcal H_3^0,\ U\in\mathscr U).
\tag{39}
\]

**证明。** 若 \(y\in\mathcal D\)，(36) 的第一项不能是空和，故
\(y\) 属于某个零核心块。每个这种块大小至多八，普通入射计数给
(38)。固定 \(H,U\) 并取由 \(U\) 生成的任一正核心 \(F_3\) 块
\(V\mathbin{\dot\cup}U\)。因 \(H\cap X=\varnothing\)，两块交集
恰为 \(H\cap U\)。它们是不同 \(F_3\) 块，所以第三族自交及非零
商交分别给 (39)。\(\square\)

这把全局固定点度真正联立到了实际尾族，但 \(|\mathcal D|\) 尚无
正比例下界。还必须逐 \(y\) 保留两条混合二点式和一条混合三点式，
并让所有 \(H\in\mathcal H_3^0\) 真正成为 \(0/1\) 位置块；所有
由标签诱导的短块必须加入，每个 \(F_3\) 补集也必须是相应长度的
秩三原子。

定理 4 说明，把 (36) 只在 \(T,Q\) 上求和会完全丢掉这项障碍。
因此下一最小缺口是排除
\[
\boxed{\text{逐外点 }0/1\text{ Hasse 入射}
+\text{ 全诱导短块谱}
+\text{ 商交禁值}
+\text{ 补原子内部子和}}
\tag{40}
\]
的同时实现。局部集合或命名尾模型不能作为全局反例。

## 9. 复核与裁决

验证脚本是 research/2026-09-08_zhao_Ap_sol/verify_p_minus_four_multi_tail_global.py。
其精确作用域为：

- 十五种尾类型、链长三界；
- 23 种原始三链中七种被交换长度窗排除、十六种有合法菱形参数；
- 单个上尾至多 112 个允许下尾；
- (24) 的整数小行列式；
- \(p\le20000\) 的 2258 个素数上，第 7 节形式接口公式的回归。

有限素数回归只防实现错误；全称结论由第 3--7 节的整数与模 \(p\)
推导给出。

- **PROVED：**链长、宽度、可比对界、三链实际菱形、聚合秩定理。
- **PROVED：**亏损点集由至少 \(\lceil|\mathcal D|/8\rceil\) 个
  零核心非零商交横截块覆盖。
- **FORMAL_TAIL_INTERFACE_COMPATIBILITY：**未检查全诱导短块谱，
  不升级为反例。
- **INCOMPLETE：**未排除实际单高度 \(p-4\) 纤维；最小缺口是
  (40) 的逐外点 \(0/1\) 入射—全诱导短块—统一商标号—补原子联立。

\(p=7\) 不在本文量词中。
