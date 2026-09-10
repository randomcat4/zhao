# ROUTE-A4 第二支：共 \(E\) 菱形与局部模型

## 状态

- 六项第二支菱形及其交叠结论：PROVED_HERE。
- “线性多个共 \(E\) 的第二支块必产生真子交换”：DISPROVED
  at the local-interface level。
- 一般 \(A_p\)：INCOMPLETE。

本文最后的模型只实现命名块、补核、商交和高度接口。它不是完整
\(Z\) 原子，不枚举全部 \(\mathcal F_r\)，也不实现一点、二点、
三点 Hasse 设计。

## 1. 固定二项横截后的四项花瓣

固定二项 \(a\) 块 \(E\in\mathcal F_1\)。设

\[
C_i=E\mathbin{\dot\cup}D_i\in\mathcal F_2,\qquad |C_i|=6.
\]

则每个 \(D_i\) 都是与 \(E\) 不交的四项 \(a\) 块。若
\(i\ne j\)，则

\[
D_i\cap D_j\ne\varnothing.
\tag{1}
\]

否则 \(D_i\dot\cup D_j\) 是八项 \(2a\) 块，违反
\(\mathcal F_2\) 的七项长度上界。

事实上交集的商和不能为零：

\[
\boxed{\bar\sigma(D_i\cap D_j)\ne0.}
\tag{2}
\]

证明如下。令 \(I=D_i\cap D_j\)。由 (1) 及两个不同四项块的
反链性，\(1\le|I|\le3\)。若 \(\bar\sigma(I)=0\)，则
\(\sigma(I)=\mu a\)，其中
\(\mu\in\{0,\pm1,\pm2,\pm3\}\)。

- \(\mu=0\) 时，\(I\) 是非空真实零和真子集。
- \(\mu=-1,-2,-3\) 时，加至多三个冻结锚点得到禁用短零和。
- \(\mu=1\) 时，\(D_i\setminus I\) 是非空真实零和。
- \(\mu=2\) 时，\(D_i\cup D_j\) 是非空真实零和。
- \(\mu=3\) 时，\(D_i\cup D_j\) 的和为 \(-a\)，再加一个锚点
  得到禁用短零和。

所有长度在 \(p=7\) 时也不超过冻结的禁用界，故没有边界例外。

## 2. 六项第二支的菱形

再假设 \(C_i\) 走补核二分的第二支。于是存在二项 \(a\) 块
\(P_i\)，满足

\[
P_i\cap C_i=\varnothing,\qquad
Z\setminus C_i=P_i\mathbin{\dot\cup}B_i',
\]

其中 \(\bar B_i'\) 是长度 \(3p-4\) 的 \(C_p^3\) 原子。定义

\[
C_i'=D_i\mathbin{\dot\cup}P_i,\qquad
A_i=E\mathbin{\dot\cup}D_i\mathbin{\dot\cup}P_i
    =E\mathbin{\dot\cup}C_i'.
\]

则

\[
\boxed{
C_i'\in\mathcal F_2,\ |C_i'|=6,\ C_i'\cap E=\varnothing;
\qquad A_i\in\mathcal F_3,\ |A_i|=8.}
\tag{3}
\]

而且 \(Z\setminus A_i=B_i'\)。这给出菱形

\[
D_i\longrightarrow C_i=E\dot\cup D_i,\qquad
D_i\longrightarrow C_i'=D_i\dot\cup P_i,\qquad
A_i=E\dot\cup C_i'=C_i\dot\cup P_i.
\]

若 \(i\ne j\) 且 \(A_i\ne A_j\)，不同 \(3a\) 块的非零商交定理
才可应用，并给出

\[
\boxed{\bar\sigma(C_i'\cap C_j')\ne0.}
\tag{4}
\]

这里
\[
A_i\cap A_j=E\mathbin{\dot\cup}(C_i'\cap C_j'),\qquad
\bar\sigma(E)=0.
\]
如果 \(A_i=A_j\)，即同一个八项块出现多个菱形分解，则不能由
“不同 \(3a\) 块”定理推出 (4)；本文不对这种多分解越界声称。

所有 \(P_i\) 都是 \(Z\setminus E\) 上的 \(\Gamma_a\) 边。
该诱导图的匹配数至多二：三条两两不交的边再加上 \(E\)，会在
全图中形成四匹配。因此

\[
\nu(\Gamma_a[Z\setminus E])\le2,\qquad
|E(\Gamma_a[Z\setminus E])|\le2(p-4).
\tag{5}
\]

对固定 \(C_i\)，两条不同的伴随边 \(P,Q\) 不可能彼此不交。
否则 \(C_i\dot\cup P\) 与 \(C_i\dot\cup Q\) 是两个不同
\(3a\) 块，其交恰为 \(C_i\)，商和为零，违反非零商交定理。
但这不推出伴随边唯一：两条边仍可共用一个位置。

## 3. 共 \(E\) 的局部相容模型

以下构造对每个素数 \(p\ge7\) 成立。令

\[
m=\frac{p-1}{2}\le p-4,
\]

并在 \(\bar G=C_p^3\) 中取基 \(e_1,e_2,e_3\) 及
\(g=e_1+e_2+e_3\)。先取

\[
B'=e_1^{p-2}e_2^{p-2}e_3^{p-2}g^2.
\tag{6}
\]

它是长度 \(3p-4\) 的原子。确实，若一个零和子序列选取
\(t=0,1,2\) 份 \(g\)，则三个基向量的选取数都必须为
\(0,p-1,p-2\) 中相应的值；\(t=1\) 所需的 \(p-1\) 份不可用，
故只有空子序列和完整子序列。

取 \(m\) 个不同位置 \(z_1,\ldots,z_m\)，但令它们具有相同实际
群值，商像均为 \(e_1\)。令

\[
T=(e_2,e_3,-e_1-e_2-e_3),
\qquad
D_i=T\mathbin{\dot\cup}\{z_i\}.
\]

再取两个位置不交的商零和二项块 \(E,P\)，并令

\[
X=e_1^m e_2^{p-2}e_3^{p-2}g^2,\qquad
A_0=E\mathbin{\dot\cup}T\mathbin{\dot\cup}P,
\]

\[
Z=A_0\mathbin{\dot\cup}\{z_1,\ldots,z_m\}
  \mathbin{\dot\cup}X.
\tag{7}
\]

对每个 \(i\)，置

\[
B_i'=X\mathbin{\dot\cup}
      \{z_j:j\ne i\}.
\]

于是 \(\bar B_i'\) 的多重序列正好都是 (6)，并且

\[
\begin{aligned}
C_i&=E\mathbin{\dot\cup}D_i,& |C_i|&=6,\\
A_i&=C_i\mathbin{\dot\cup}P,& |A_i|&=8,\\
Z\setminus C_i&=P\mathbin{\dot\cup}B_i',&
Z\setminus A_i&=B_i'.
\end{aligned}
\tag{8}
\]

可以统一选择 \(a\)-坐标，使

\[
\sigma(E)=\sigma(P)=\sigma(D_i)=a,\qquad
\sigma(C_i)=2a,\qquad \sigma(A_i)=3a,\qquad
\sigma(B_i')=-3a,\qquad \sigma(Z)=0.
\tag{9}
\]

而且可以让整个命名位置多重集满足真实值高度至多 \(p-4\)。
一种逐式可查的选法如下。把每个实际值写成
\((\bar x,h)\in\bar G\oplus\langle a\rangle\)：

- 所有 \(z_i=(e_1,0)\)；
- \(E\) 取商像 \(\pm2e_1\)，高度坐标为 \(0,1\)；
- \(P\) 取商像 \(\pm3e_1\)，高度坐标为 \(0,1\)；
- \(T\) 的三项高度坐标取 \(0,0,1\)；
- \(X\) 的 \(e_1^m\) 全取高度 \(1\)；
- \(X\) 的每个 \(e_2^{p-2}\)、\(e_3^{p-2}\) 分成
  \(p-5\) 个高度 \(0\) 与三个高度 \(1\)；
- \(X\) 的两份 \(g\) 高度取 \(0\) 与
  \(\delta=-m-9\)。

这样 \(X\) 的高度总和为 \(-3\)，而 \(T\) 中的 \(e_2,e_3\)
各补一个高度 \(0\) 后，相应实际值的重数恰为 \(p-4\)；
其余命名实际值的重数也都不超过 \(p-4\)。特别地，重复花瓣点
\((e_1,0)\) 的真实高度为

\[
m=\frac{p-1}{2}\le p-4.
\tag{10}
\]

对 \(i\ne j\)，这里的 \(A_i\) 确实是不同的位置块，并且

\[
A_i\cap A_j=A_0,\qquad
\bar\sigma(A_0)=-e_1\ne0.
\tag{11}
\]

然而 \(D_i,D_j\) 的交换差只有两个位置
\(z_i-z_j\)。因为两位置具有相同非零实际值，这个有符号关系本身
是长度二的原子，除空交换和全交换外没有真子交换。所有菱形甚至
可以共用同一伴随边 \(P\)；命名伴随边 \(E,P\) 的匹配数只是二。

因此，线性多个六项 \(2a\) 块共用同一个 \(E\)、每个走
\(3p-4\) 补原子第二支、不同八项块具有非零商交、且重复值高度
不超过 \(p-4\)，这些局部条件仍不足以强制真子交换。

## 4. 模型的精确停止线

构造 (6)--(11) 是实际群值层面的局部相容模型，并验证所有命名
块的和、长度、补核原子性、商交和高度。但它没有证明 (7) 中的
\(Z\) 是实际零和原子，也没有断言命名块就是全部
\(\mathcal F_1,\mathcal F_2,\mathcal F_3\)。它同样不实现群环
七点支撑、逐点/逐对/逐三点 Hasse 等式，因而不是冻结
\(C_p^4\) 反例。

模型严格划出的停止线是：仅把共 \(E\) 菱形、补核二分、
\(\mathcal F_3\) 的非零商交及高度 \(p-4\) 拼在一起，不能排除
所有交换差本身都是二项原子。继续推进必须输入完整设计约束，
或证明同一实际值花瓣无法与那些全局约束同时出现。
