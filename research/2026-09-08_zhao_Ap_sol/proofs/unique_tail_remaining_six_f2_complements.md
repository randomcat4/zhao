# 剩余型中的六项二族块与极长补原子

STATUS: **PROVED_REDUCTION / PENDING_INDEPENDENT_REVIEW / GLOBAL_INCOMPLETE**

## 1. 范围与结论

沿用已经认证的唯一尾共同位置分解

\[
X=x^{p-4},\qquad Z=X\mathbin{\dot\cup}Y,
\qquad Y=L\mathbin{\dot\cup}R,
\tag{1}
\]

\[
U\subseteq L,\quad |U|=3,\qquad
R=P\mathbin{\dot\cup}K,
\qquad \bar\sigma(P)=dq,
\tag{2}
\]

其中只剩空型、型 \((2)\) 与型 \((3)\)。本文不增加新的聚合计数；
它固定同一批实际位置及同一套商标签，考察自动诱导块

\[
C=X_{b-d}\mathbin{\dot\cup}U\mathbin{\dot\cup}P.
\tag{3}
\]

十二个剩余非空偏差赋值中，恰有三行使 (3) 成为六项
\(2a\) 块：

\[
\boxed{
\begin{array}{c|c|c|c|c}
(p,b)&\text{型}&|P|&\sigma(P)&|C|\\ \hline
(233,4)&(2)&1&2x-a&6\\
(233,4)&(3)&2&3x-a&6\\
(1399,5)&(3)&1&3x-a&6.
\end{array}}
\tag{4}
\]

对 (4) 的每一行，字面补集

\[
B=Z\setminus C
\tag{5}
\]

在 \(C_p^3\) 商投影中都是长度 \(3p-2\) 的原子。因此

\[
\boxed{
\varnothing\ne E\subsetneq B
\quad\Longrightarrow\quad
\bar\sigma(E)\ne0.}
\tag{6}
\]

式 (6) 一次性保留了每个长补原子的全部内部子集和，而不是只保留
长度或纤维重数。

## 2. 六项 \(2a\) 块的补核二分

先给出本轮所需的自包含二分，不把未经独立认证的旧路线稿当作黑箱。
设一般地 \(C\subset Z\) 满足

\[
|C|=6,\qquad \bar\sigma(C)=0,
\qquad \sigma(C)=2a,
\tag{7}
\]

并令 \(B=Z\setminus C\)。于是

\[
|B|=3p-2,\qquad \bar\sigma(B)=0,
\qquad \sigma(B)=-2a.
\tag{8}
\]

若 \(\pi(B)\) 不是原子，就在一个真商零和分拆中取较短边
\(E\)。有

\[
0<|E|\le\left\lfloor{3p-2\over2}\right\rfloor<2p+2.
\tag{9}
\]

中间商零禁窗排除 \(|E|\ge p+2\)，而冻结的短正和谱继而给出

\[
\sigma(E)=\mu a,\qquad \mu\in\{1,2,3\},
\qquad |E|\le5+\mu.
\tag{10}
\]

若 \(\mu=2\) 或 \(3\)，则 \(C\dot\cup E\) 的实际和分别为
\(4a\) 或 \(5a\)。从外部的 \(a^{p-4}\) 锚点中分别补入
\(p-4\) 或 \(p-5\) 项，就得到非空实际零和。其长度至多

\[
6+(5+\mu)+p-(2+\mu)=p+9\le3p-2,
\tag{11}
\]

与冻结反例矛盾。因此 \(\mu=1\)。这时
\(C\dot\cup E\) 是 \(3a\) 块。正系数长度界给

\[
6+|E|\le8.
\tag{12}
\]

而一族短块没有单项，故 \(|E|=2\)。于是存在严格二分：

\[
\boxed{
\begin{array}{l}
\pi(B)\text{ 是长度 }3p-2\text{ 的原子};\quad\text{或}\\
B=E\mathbin{\dot\cup}B',\quad
|E|=2,\quad\sigma(E)=a,\\
\pi(B')=\pi\bigl(Z\setminus(C\dot\cup E)\bigr)
\text{ 是长度 }3p-4\text{ 的原子}.
\end{array}}
\tag{13}
\]

最后一行使用已认证的完整 \(F_3\) 补原子接口，因为
\(C\dot\cup E\) 是长度八的实际 \(3a\) 块。注意 (13) 证明的是
同一实际位置补集，不是一个只匹配长度的抽象原子。

## 3. 唯一正核心尾删除第二支

现在回到 (4)。三行都有

\[
b-d>0,\qquad P\ne\varnothing,
\qquad U\cap P=\varnothing.
\tag{14}
\]

若 (13) 的第二支发生，则

\[
D=C\mathbin{\dot\cup}E
\tag{15}
\]

是长度八的 \(F_3\) 块。由 (3) 与 \(E\cap C=\varnothing\)，其
\(X\)-核心至少含有既定的 \(X_{b-d}\)，所以是正核心；其
\(Y\)-尾至少含有严格大于 \(U\) 的 \(U\dot\cup P\)。这与
“一切正核心 \(F_3\) 块的尾恰为 \(U\)”矛盾。因此第二支不能发生，
只剩

\[
\boxed{\pi(Z\setminus C)\text{ 是长度 }3p-2\text{ 的原子}.}
\tag{16}
\]

原子定义立即给出 (6)。这正是后续逐位置闭包可直接调用的长补内部
子集和接口。

## 4. 十二行的精确枚举

上一轮留下八个非空尺寸行、十二个实际偏差赋值。对单原子型写

\[
\sigma(P)=dx-ka,
\tag{17}
\]

则 (3) 满足

\[
|C|=b-d+3+|P|,
\qquad \sigma(C)=(3-k)a.
\tag{18}
\]

逐行代入即知，\(|C|=6\) 与 \(\sigma(C)=2a\) 等价于
\(|C|=6,k=1\)，恰好给出表 (4) 的三行。脚本
`unique_tail_remaining_six_f2_complements.py` 从上一轮已冻结报告中
重放全部十二个赋值，并断言没有第四行被漏入。

## 5. 边界

- 本文只强制 (4) 三行的极长补原子，不声称这三行可实现。
- 其余九个非空偏差赋值没有被本文关闭；它们需要继续接入内部
  子集和、统一商标签与全部自动短块。
- 空 packing 没有非空 \(P\)，不在本文范围内。
- 全局 \(A_p\) 仍未完成。
