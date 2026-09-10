# \(p=233\) 的 mixed 交换重分解：二点 packing 升为三点原子

STATUS: **PROVED REDUCTION / INDEPENDENT REVIEW CORRECT /
GLOBAL INCOMPLETE**

## 1. 输入

仍固定型 \((3)\)、\(|P|=2\) 的当前切片。对一个 singleton 端点
\(H\)，已有同一真实位置分解

\[
W_H=P\mathbin{\dot\cup}Q_H,\qquad
\bar\sigma(W_H)=4q,
\tag{1}
\]

其中

\[
P=\{z,z^\ast\},\qquad
\rho(P)\text{ 是长度二原子},\qquad
\bar\sigma(P)=3q,
\tag{2}
\]

而

\[
\rho(Q_H)\text{ 是原子},\qquad
\bar\sigma(Q_H)=q.
\tag{3}
\]

这些不是任意分解：\(q^{p-4}W_H\) 是相应 \(F_3\) 块的长商补原子，
所以 \(W_H\) 的每个非空真 \(\rho\)-零位置子集的轴系数都在
\(\{1,2,3\}\) 中。

假设 mixed 高度交换引理给出一个尾外双点集

\[
E=\{u,v\}\subseteq Q_H\setminus U,\qquad
\sigma(E)=\sigma(z^\ast).
\tag{4}
\]

## 2. 交换后的两个因子

定义

\[
P'=\{z,u,v\},\qquad
Q'_H=(Q_H\setminus E)\mathbin{\dot\cup}\{z^\ast\}.
\tag{5}
\]

由 \(P\cap Q_H=\varnothing\) 及 \(E\subseteq Q_H\)，式 (5) 确为
同一位置集 \(W_H\) 的新不交分解：

\[
W_H=P'\mathbin{\dot\cup}Q'_H.
\tag{6}
\]

式 (4) 还逐项给出

\[
\begin{aligned}
\rho(\bar\sigma(P'))&=0,
&\bar\sigma(P')&=3q,
&\sigma(P')&=\sigma(P)=3x-a,\\
\rho(\bar\sigma(Q'_H))&=0,
&\bar\sigma(Q'_H)&=q,
&\sigma(Q'_H)&=\sigma(Q_H).
\end{aligned}
\tag{7}
\]

## 3. \(P'\) 与 \(Q'_H\) 都是原子

先证 \(\rho(P')\) 是长度三原子。三个单点都非零：\(z\) 属于长度
二原子 \(P\)，而 \(u,v\) 属于原子 \(Q_H\)。又

\[
\rho(u)+\rho(v)=\rho(z^\ast)=-\rho(z)\ne0.
\tag{8}
\]

若 \(\rho(z)+\rho(u)=0\)，则
\(\rho(u)=\rho(z^\ast)\)，再由 (8) 得 \(\rho(v)=0\)，矛盾；
\(z,v\) 对称。故 \(P'\) 没有非空真零子集，确为原子。

现在任取 \(Q'_H\) 的一个原子分解。与 \(P'\) 合并后得到
\(\rho(W_H)\) 的原子分解。长补完整内部子集和判据说明每个因子的
轴系数都属于 \(\{1,2,3\}\)，而全部因子系数和为四。因 \(P'\) 的
系数为三，余下因子的普通系数和只能为一：因子总数至多四，故普通
和至多九，小于 \(p=233\)，没有模回绕。于是余部只能有唯一一个
系数一因子，即

\[
\boxed{\rho(Q'_H)\text{ 是原子}.}
\tag{9}
\]

等价地，也可直接调用已审的分解型
\((1,3),(2,2),(1,1,2),(1,1,1,1)\)：含系数三的分解只能是
\((1,3)\)。

## 4. 长度与新增三目标接口

当前 \(|Y|=474\)。由
\[
|Q_H|=|Y|-|H|-|P|=472-|H|
\tag{10}
\]
及 (5)，

\[
\boxed{
\begin{array}{c|c|c}
|H|&|Q_H|&|Q'_H|\\ \hline
7&465=2p-1&464=2p-2,\\
8&464=2p-2&463=2p-3.
\end{array}}
\tag{11}
\]

特别地，540 个含长七 singleton 的行若落在交换支，就从一个最大
投影原子严格产生一个长度 464 的近最大投影原子。因为 \(E\) 避开
\(U\)，\(Q'_H\) 仍含 \(Q_H\) 中原来的两个尾位置，并额外含
packing 位置 \(z^\ast\)。

原分解中 \(|P|=2\)，补配对后只有一个独立 mixed 目标。新分解中
\(|P'|=3\)，故有三个独立目标。具体地，对每个
\(w\in P'=\{z,u,v\}\) 以及每个实际位置子集 \(T\subseteq Q'_H\)
满足

\[
\rho(\bar\sigma(T))=-\rho(\bar w),
\tag{12}
\]

长补的完整内部子集和同时强制

\[
\boxed{\bar w+\bar\sigma(T)\in\{q,2q,3q\}.}
\tag{13}
\]

三个 singleton 与各自在 \(P'\) 中的 complementary doubleton
成补对，恰给 \(2^{3-1}-1=3\) 个独立目标代表。因此 (13) 没有遗漏
三点 packing 的 mixed 子集，也不是只检查“存在一个好 \(T\)”。

## 5. 双交换时的公共核

若正负两个 signed 纤维都各自含双点交换，记

\[
E_+=\{w,u\},\quad \sigma(E_+)=\sigma(z_+),\qquad
E_-=\{w,v\},\quad \sigma(E_-)=\sigma(z_-).
\tag{14}
\]

交叉相交及相反非零投影保证两双点不能相同；若它们只交于 \(w\)，
两次重分解给出的长度 \(|Q_H|-1\) 原子分别是

\[
Q'_+=\bigl(Q_H\setminus\{w,u\}\bigr)\dot\cup\{z_+\},
\qquad
Q'_-=\bigl(Q_H\setminus\{w,v\}\bigr)\dot\cup\{z_-\}.
\tag{15}
\]

它们共享同一字面子序列

\[
Q_H\setminus\{w,u,v\},
\qquad\text{长度 }|Q_H|-3.
\tag{16}
\]

在长七 singleton 情形中该公共核长度为 \(462=2p-4\)。式 (14)
还给出两个二位置花瓣的实际和相同：

\[
\sigma(\{v,z_+\})=\sigma(\{u,z_-\}).
\tag{17}
\]

本节是条件结论；前一引理只保证两个 signed 纤维同时非空时至少
一边出现双点，并不保证两边都出现双点。

## 6. 裁决

交换支现在不再只是一个局部高度等式，而被提升为：

1. 同一 \(W_H\) 的真实 \((3,1)\) 原子重分解；
2. 长七 singleton 下的一条新长度 464 原子；
3. 三条全称 mixed 目标纤维；
4. 双交换时两条近相同原子及长度 \(2p-4\) 的字面公共核。

下一步应对新 \(Q'_H\) 使用近最大删点二分、一般 mandatory-core
表示与逐目标 \(q\)-矩，再同原三个 singleton 中已经选出的 461 门、
Property B 补全、自动短块与 Hasse 分离器联立。本文没有把 461
删点定理直接套到这条新原子上。本文尚未
证明交换支矛盾，也没有删除 outer row；固定切片及全局 \(A_p\)
保持 **INCOMPLETE**。
