# (p=233)、型 ((3))、(|P|=2) 的第一版精确切片接口

STATUS: **INSTANCE_SCHEMA / EXACT_CEGAR_INTERFACE / CERTIFIED RANK-TWO REDUCTION / NO INSTANCE LOADED / GLOBAL INCOMPLETE**

## 1. 本文实际完成了什么

本文冻结第一个非平凡的统一标签切片

\[
p=233,\qquad (\ell,b)=(7,4),\qquad |U|=3,
\tag{1}
\]

\[
R=P\mathbin{\dot\cup}K,\qquad
\bar\sigma(P)=3q,\qquad |P|=2,
\qquad \sigma(P)=3x-a.
\tag{2}
\]

最后一个等式就是统一实际轴偏差 \(\kappa=1\)。第一版只接受长度七
的零核心端点；长度八端点将在下一版 schema 加入，不能在本版中
静默放宽。

本版还使用新稿 `unique_tail_p233_singleton_tail_fringe.md` 的结论：
三个单点迹端点都长七时，尾投影秩一不可能。因此首片加入派生硬门

\[
\boxed{\dim\langle\rho(\bar u):u\in U\rangle=2.}
\tag{3}
\]

这一步已经由
`verifications/unique_tail_p233_singleton_tail_fringe_independent_review.md`
从头独立重推并判为 `CORRECT`；审计文件 SHA-256 为
`8487137667255b49f74ce8a0fe79c2d12222e45d54776eb5c8458bce00aed5d1`。
因此式 (3) 现在是本切片的已认证派生硬门，不再是待审前提。

配套程序
`unique_tail_p233_type3_p2_exact_slice.py` 完成两件事：

1. 给出一个严格的逐位置实例 schema，并检查所有可直接检查的总和、
   分区、重数、尾迹和四边 incidence 条件；
2. 把尚需搜索的全称条件拆成十一项精确分离预言机契约，并能独立
   复核其中十类预言机返回的具体违反见证。

本轮没有收到一套完整的 474 位置标签和端点 incidence。因此报告
状态是 `INSTANCE_SCHEMA`，不是 `SAT`，更不是 `UNSAT`。

## 2. 唯一共享的逐位置对象

规范化

\[
q=(1,0,0)\in C_{233}^3,
\qquad a=(0,0,0,1)\in C_{233}^4,
\qquad x=(q,h_x).
\tag{4}
\]

输入只有一张

\[
Y=(y_0,\ldots,y_{473})\in(C_{233}^4)^{474}
\tag{5}
\]

和这张表上的实际位置索引集。所有命名块

\[
T,U,H_1,\ldots,H_s,L,R,P,K
\tag{6}
\]

都必须引用 (5) 的同一批位置。schema 不接受端点私有标签，不接受
为不同长补分别复制的 \(K\)，也不接受只匹配长度或和值的抽象原子。

总和条件为

\[
\sum_Y y=4x,
\qquad
\sum_U y=3a-4x,
\qquad
\sum_{H_i}y=3a,
\qquad
\sum_Py=3x-a.
\tag{7}
\]

此外 \(T\) 是长度六至八的固定零核心 \(F_3\) 块，并保留
\(Y\setminus T\) 中没有新商标签 \(q\) 的原接口。这里不偷加
“\(T\) 必须属于选定端点族”或“\(T\) 必须不属于端点族”：它可以
等于某个端点，也可以不是；两者的实际位置仍来自同一张 (5)。

## 3. 四边全异迹 incidence

输入包含四条不同简单边，其非孤立顶点恰为全部选定端点
\(H_1,\ldots,H_s\)，所以

\[
4\le s\le6.
\tag{8}
\]

本版要求每个 \(|H_i|=7\)，且六个可能的非空真尾迹中，各端点使用
不同的迹。每条选定边 \(H_iH_j\) 满足

\[
(H_i\cap U)\cap(H_j\cap U)=\varnothing.
\tag{9}
\]

四条边还共享一个同一实际位置

\[
y\in Y\setminus U,
\qquad \rho(\bar y)\ne0,
\qquad y\in H_i\cap H_j
\tag{10}
\]

并逐边检查

\[
\rho\bigl(\bar\sigma(H_i\cap H_j)\bigr)\ne0.
\tag{11}
\]

因此 schema 本身保存的是实际交，而不是只有四边图型和迹颜色。
程序还直接检查三个单点迹

\[
\{u_1\},\qquad\{u_2\},\qquad\{u_3\}
\tag{12}
\]

都在选定端点迹中出现。这不是额外猜测：六迹不交图的任意四边
子图都含三个单点迹；显式检查用于防止 incidence 编码器漏掉这条
全异迹分支结论。三个相应端点在本版都长七，所以才可调用上面的
秩一排除并检查 (3)。

令

\[
L=U\cup\bigcup_iH_i,
\qquad R=Y\setminus L,
\qquad K=R\setminus P.
\tag{13}
\]

程序从索引重新计算右边，并拒绝任何与输入声明不一致的 \(L,R,K\)。
还显式要求 \(K\ne\varnothing\)。所以先前那个空核的
“不同双点迹覆盖 witness”不属于本切片，不能拿来固定当前 incidence。

## 4. 型 ((3)) 的逐端点长补

对每个选定端点定义

\[
Q_H=K\mathbin{\dot\cup}(L\setminus H)
=Y\setminus(H\mathbin{\dot\cup}P).
\tag{14}
\]

因为本版 \(|H|=7,|P|=2\)，所以

\[
|Q_H|=474-7-2=465=2p-1,
\qquad \bar\sigma(Q_H)=q.
\tag{15}
\]

型 \((3)\) 的完整长补内部谱要求

\[
\boxed{\rho(Q_H)\text{ 是 }C_{233}^2\text{ 中的原子}}
\tag{16}
\]

并且对 \(P\) 的每个非空真子集 \(A\) 和每个 \(S\subseteq Q_H\)，

\[
\rho(\bar\sigma(S))=-\rho(\bar\sigma(A))
\Longrightarrow
\bar\sigma(A)+\bar\sigma(S)\in\{q,2q,3q\}.
\tag{17}
\]

由于 \(|P|=2\)，互补对称后 (17) 只有一个独立的 \(P\)-子集轨道。
预言机仍量化全部实际 \(S\subseteq Q_H\)，而不是只记录“一个目标”。

## 5. 自动六项块和两个不同的长补预言机

由 (1)--(2) 自动得到实际位置块

\[
C=X_1\mathbin{\dot\cup}U\mathbin{\dot\cup}P,
\qquad |C|=6,
\qquad \bar\sigma(C)=0,
\qquad \sigma(C)=2a.
\tag{18}
\]

因此必须单独检查极长补

\[
B_C=Z\setminus C
=X^{228}\mathbin{\dot\cup}\bigl(Y\setminus(U\cup P)\bigr),
\qquad |B_C|=697=3p-2
\tag{19}
\]

的每个内部位置子集：

\[
\varnothing\ne E\subsetneq B_C
\Longrightarrow \bar\sigma(E)\ne0.
\tag{20}
\]

这和自动生成的每个 \(F_3\) 块的补原子预言机是两项不同义务。
程序没有把 (20) 错套成 \(F_3\) 的 \(p-4\) 纤维论证。

## 6. 十一项精确分离预言机

报告冻结下列十一项全称条件。

1. \(K\) 的全部非空子集在 \(\rho\) 下非零；
2. 每个 \(Q_H\) 的全部非空真子集在 \(\rho\) 下非零；
3. 每个端点的完整混合目标 (17)；
4. 从同一张 \(Y\) 自动重建全部长度一至八的商零块，并施加完整
   \(F_1,F_2,F_3\) 长度窗；
5. 排除全部长度九至 \(2p+2\) 的商零子集；
6. 每个正核心 \(F_3\) 块必须恰为 \(X_4\dot\cup U\)，每个
   \(F_3\) 尾必须命中 \(U\)；
7. 全部自动短块之间的实际交网络和不同 \(F_3\) 块的交商和；交网络
   只接受两边都属于允许短谱的块，并把不交并长落在
   \(9,\ldots,2p+2\) 的情形作为违反；
8. 每个自动 \(F_3\) 块的字面补集的全部内部子集和；
9. (20) 的全部内部子集和；
10. 全部零阶、一位置、二位置、三位置 Hasse 同余；
11. 实际序列 \(Z=X^{229}\dot\cup Y\) 的原子性。

第 10 项在 \(|Y|=474\) 时共有

\[
17,976,380
\tag{21}
\]

条同余，其中包括固定若干 \(X\)-位置的行。这个数只是待核验行数，
不是已经通过的计数。

第 1--9、11 项若找到违反，只需返回相应的实际位置子集，脚本的
`--violation` 模式会从原始标签重新核对该见证。第 10 项是聚合条件；
单报一个声称的余数不能自证，必须附完整短星支撑/计数证书。因此
本版故意不接受一行式的 Hasse “违反见证”。

## 7. CEGAR 状态语义

对一套载入且通过静态检查的实例，若尚有任何预言机未精确返回
`CLEAR`，状态只能是

`RELAXED_STATIC_INSTANCE_ONLY/EXACT_ORACLES_PENDING/GLOBAL_INCOMPLETE`。

只有十一项预言机都按原量词精确清空时，单个实例才可以标记
`VERIFIED_INTERFACE_SURVIVOR`。这仍只表示它通过这个固定的
\(p=233\) 局部接口，不是 \(A_p\) 的反例。

反过来，只有一个**另行冻结并证明穷尽**的 incidence 生成器覆盖本
切片全部允许的四边图、迹着色、位置掩码与标签，再逐一给出可检查的
排除证书，才可以写本切片 `UNSAT`。当前既没有这个生成器，也没有
具体实例，故没有任何 UNSAT 主张。

## 8. 可运行审计

运行

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research/2026-09-08_zhao_Ap_sol/unique_tail_p233_type3_p2_exact_slice.py
```

会刷新报告并执行两项小规模独立算术审计：

- 在 48 个小实例上，把轴向补原子压缩判据与逐子集原子定义直接比较；
- 用五条域/边界回归核对交网络分类，特别拒绝把一个 \(F_3\) 块的
  非短全补误当成“不交短块”见证，并接受并长恰为九的短块对；
- 核对 \(|P|=2\) 的独立混合目标数为一，以及 (21) 的逐层行数。

这些小审计只验证接口实现，不验证任何 \(p=233\) 标签实例。

## 9. 精确停止线

**已完成：**第一版固定切片的逐位置 schema、所有共享集合的派生关系、
型 \((3)\) 的 \(Q_H\) 与混合目标、六项 \(F_2\) 极长补、全自动短块、
Hasse 和实际 \(Z\) 原子性的精确 CEGAR 契约；并用已经独审为
`CORRECT` 的秩一削减，把全长七首片收紧为尾投影秩二。

**未完成：**当前型的 incidence 穷尽器、任何 474 位置候选、十一项
预言机的完整 `CLEAR` 运行、固定切片 SAT/UNSAT，以及全局 \(A_p\)。
