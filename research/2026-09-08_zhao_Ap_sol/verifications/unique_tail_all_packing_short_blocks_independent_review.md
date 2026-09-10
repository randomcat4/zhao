# 七种共同 packing 的互补块、全部子族短谱与统一纤维压缩：全新独立审计

STATUS: **CORRECT**

## 1. 审计对象与冻结范围

本审计只认证以下三个作者工件所陈述的局部一般化：

- `unique_tail_all_packing_short_blocks.py`；
- `unique_tail_all_packing_short_blocks_report.json`；
- `proofs/unique_tail_all_packing_short_blocks.md`。

适用范围严格限于

\[
(p,b)=(233,4),\qquad(1399,5),
\]

以及共同外部序列的七种 packing 系数型

\[
\varnothing,(1),(2),(3),(1,1),(1,2),(1,1,1).
\]

本轮独立检查实际位置量词、商和值、禁窗、唯一正核心例外、全部原子
子族短谱、统一实际偏差及长补原子商纤维。有限筛选只认证必要条件，
不把幸存行解释成完整标号可满足性或可实现性证明。

## 2. 七型的真实互补块与商和

冻结的同一实际位置分解为

\[
X=x^{p-4},\qquad Z=X\mathbin{\dot\cup}Y,
\qquad Y=L\mathbin{\dot\cup}R,
\]

\[
R=P_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}P_t
\mathbin{\dot\cup}K.
\]

记

\[
d=\sum_i d_i,\qquad N=\sum_i|P_i|,
\qquad P=\mathbin{\dot\bigcup}_iP_i,
\]

其中 \(0\le d\le3\)、\(\bar\sigma(P_i)=d_iq\)。共同总和与唯一尾
接口分别给出

\[
\bar\sigma(K\dot\cup L)=(4-d)q,
\]

\[
U\subseteq L,qquad |U|=3,qquad
\bar\sigma(U)=-bq.
\]

取实际 \(X\)-位置并定义

\[
D=X_{b-d}\mathbin{\dot\cup}U\mathbin{\dot\cup}P,
\]

\[
B=X_{p-b+d-4}\mathbin{\dot\cup}K
\mathbin{\dot\cup}(L\setminus U).
\]

七型均有 \(1\le b-d\le5\le p-4\)，而另一侧核心数也处于
\([0,p-4]\)。由于 \(X\cap Y=\varnothing\)、\(U\subseteq L\)、
\(P,K\subseteq R=Y\setminus L\)，且共同分解逐位置不交，故

\[
\boxed{Z=D\mathbin{\dot\cup}B}
\]

是真实位置恒等式。商和逐项为

\[
\bar\sigma(D)=(b-d)q-bq+dq=0,
\]

\[
\begin{aligned}
\bar\sigma(B)
&=(p-b+d-4)q+\bar\sigma(K)+\bar\sigma(L)-\bar\sigma(U)\\
&=(p-b+d-4)q+(4-d)q+bq=pq=0.
\end{aligned}
\]

后一式正确使用了 \(K\dot\cup L\) 的共同商和并计入删除 \(U\) 后
的 \(+bq\)，没有把端点余部分解的特殊原子性偷用于非强制型。

## 3. 双侧禁窗与空型例外

\(B\) 的 \(X\)-部分已有 \(p-b+d-4\) 个位置。十四个素数—类型行中
其最小值为 \(p=233,b=4,d=0\) 时的 \(225\)，所以单靠该核心即有

\[
|B|>8.
\]

这一步不需要 \(K\ne\varnothing\)。由商零禁窗，\(|B|\ge2p+3\)；
再由 \(|Z|=3p+4\) 得 \(|D|\le p+1\)。若 \(|D|\ge9\)，商零块
\(D\) 落入 \([9,p+1]\) 的短段禁窗，故

\[
|D|\le8.
\]

空 packing 的边界处理正确且必不可少。此时 \(d=N=0\)，

\[
D=X_b\mathbin{\dot\cup}U
\]

正是原来的唯一正核心 \(F_3\) 块，在两个参数下长度分别为七和八。
因此不能对空型施加“第二个错误 \(F_3\)”矛盾；报告把它单独记为
`unique_tail_exception`，没有生成非空子族或 \(k_i\)。

若 packing 非空，则 \(d\ge1\)、\(P\ne\varnothing\)。此时 \(D\) 的
核心数 \(b-d<b\)，尾 \(U\dot\cup P\) 严格大于 \(U\)。所以
\(|D|=8\) 会成为不同于唯一对 \((b,U)\) 的第二个正核心 \(F_3\)
块，必须排除。由

\[
|D|=b-d+3+N
\]

得到只适用于非空 packing 的精确界

\[
\boxed{N\le4-b+d}.
\]

作者证明和报告均没有把该不等式错误套到 \(p=1399\) 的空型。

## 4. 十七个互补块尺寸候选

独立按正整数原子尺寸枚举上一节的不等式；相同系数的原子只保留
非降序尺寸，不同系数保留次序。结果为

\[
\begin{array}{c|c|c}
(p,b)&\text{型}&(|P_i|)\\ \hline
(233,4)&\varnothing&()\\
&(1)&(1)\\
&(2)&(1),(2)\\
&(3)&(1),(2),(3)\\
&(1,1)&(1,1)\\
&(1,2)&(1,1),(1,2),(2,1)\\
&(1,1,1)&(1,1,1)\\ \hline
(1399,5)&\varnothing&()\\
&(1)&\varnothing\\
&(2)&(1)\\
&(3)&(1),(2)\\
&(1,1)&\varnothing\\
&(1,2)&(1,1)\\
&(1,1,1)&\varnothing
\end{array}
\]

连同两个空型恰有十七个尺寸候选。特别地，\(p=1399\) 的
\((1),(1,1),(1,1,1)\) 是被尺寸上界删除，而不是被后续子族短谱
重复删除。

## 5. 全部非空子族与统一偏差

对每个非空 \(I\subseteq\{1,\ldots,t\}\)，令

\[
d_I=\sum_{i\in I}d_i,qquad n_I=\sum_{i\in I}|P_i|,
\]

并取实际位置块

\[
D_I=X_{b-d_I}\mathbin{\dot\cup}U
\mathbin{\dot\cup}\mathop{\dot\bigcup}_{i\in I}P_i.
\]

七型中每个非空子族都有 \(1\le d_I\le3\)，所以
\(1\le b-d_I\le4\le p-4\)，所需 \(X\)-位置确实存在。各部分仍在
\(X\mid L\mid R\) 的同一实际位置分区中，且

\[
\bar\sigma(D_I)=(b-d_I)q-bq+d_Iq=0.
\]

对十七个尺寸候选中的全部非空子族作无导入枚举，共得到二十四个
结构行；其长度全部在五至八之间，因而当然落在声明的二至八范围内。
每个 \(D_I\) 的尾严格包含 \(U\)，核心数小于 \(b\)，所以不是唯一
正核心 \(F_3\)。故长度五、六只允许实际和 \(a,2a\)，长度七只允许
\(2a\)，长度八没有允许值。

由 \(\bar\sigma(P_i)=d_iq\) 与 \(\bar x=q\)，存在唯一
\(c_i\in\mathbb F_p\) 使

\[
\sigma(P_i)=d_ix+c_ia.
\]

单原子子族在可存活时迫使 \(c_i=-k_i\)、\(k_i\in\{1,2\}\)。同一
实际原子在全部子族中必须使用同一个 \(k_i\)，于是

\[
\boxed{\sigma(D_I)=\left(3-\sum_{i\in I}k_i\right)a}.
\]

由于 \(\sum k_i\le6<p\)，不存在模回绕歧义。穷尽所有非空 \(I\) 后
的精确幸存表为

\[
\begin{array}{c|c|c|c}
(p,b)&\text{型}&(|P_i|)&(k_i)\\ \hline
(233,4)&\varnothing&()&()\\
&(1)&(1)&(1)\\
&(2)&(1)&(1),(2)\\
&&(2)&(1)\\
&(3)&(1)&(1),(2)\\
&&(2)&(1),(2)\\
&&(3)&(1)\\
&(1,2)&(1,1)&(1,1)\\ \hline
(1399,5)&\varnothing&()&()\\
&(2)&(1)&(1)\\
&(3)&(1)&(1),(2)\\
&&(2)&(1)
\end{array}
\]

因此全部子族短谱把十七个尺寸候选精确筛到十二个，其中含两个空型；
非空行此时共有十四个偏差赋值。

删除行的原因也逐项闭合：

- \(p=233\) 的 \((1,1)\) 中，两个单原子长度七块分别迫使
  \(k_1=k_2=1\)，但双原子块也长七，其实际和却为 \(a\)，违反
  长度七只能属于 \(F_2\)；
- \(p=1399\) 的 \((1,2)\) 中，系数一单原子块长八，但其核心—尾
  不是唯一 \(F_3\)，故没有允许实际和；
- \(p=233\) 的 \((1,2)\) 只有尺寸 \((1,1)\)、偏差 \((1,1)\)
  暂留；\((1,2)\) 尺寸在全子族长度七处给出 \(a\)，\((2,1)\)
  尺寸则在系数一单原子的错误长度八块处失败；
- \(p=233\) 的 \((1,1,1)\) 不能让所有单点、二点及全子族长度七
  块共享同一组 \(k_i\)，故无偏差赋值。

## 6. 系数一单点的长补商纤维门

子族短谱后仍含系数一原子的只有 \(p=233\) 的

\[
(1):(1),\qquad(1,2):(1,1).
\]

两行都强制某个 \(P_i=\{y\}\subseteq R\) 且
\(\bar y=\bar\sigma(P_i)=q\)。每个选中零核心端点
\(H\in\mathcal F_3\) 都满足 \(H\subseteq L\subseteq Y\)，所以
\(y\notin H\) 且 \(H\cap X=\varnothing\)。因此同一个实际长补

\[
B_H=Z\setminus H
\]

包含 \(X\) 的全部 \(p-4\) 个 \(q\)-标签和额外位置 \(y\)，从而

\[
v_q(B_H)\ge p-3.
\]

上游定理对每个 \(T\in\mathcal F_3\) 的实际补集
\(B_T=Z\setminus T\) 证明其商投影为原子，并对每个非零商值 \(s\)
给出

\[
v_s(B_T)\le p-4.
\]

这里 \(H\in\mathcal F_3\) 且 \(q\ne0\)，故其量词确实覆盖同一个
\(B_H\) 与同一个商值 \(q\)。于是上述两行都被严格删除。该论证不
声称一般的 \(R\) 中不存在轴向点；它只排除筛选后被迫出现的系数一
单点。系数二、三单点分别标为 \(2q,3q\)，不能误套此 \(q\)-纤维门。

## 7. 最终接口 (28)--(32)

纤维门后，两素数均只剩必要类型

\[
\boxed{\varnothing,(2),(3)}.
\]

十个最终尺寸中有两个空型，余下八个非空尺寸及十二个偏差赋值为：

\[
\begin{array}{c|c|c|c}
(p,b)&\text{型}&|P|&k\\ \hline
(233,4)&(2)&1&1,2\\
&&2&1\\
&(3)&1&1,2\\
&&2&1,2\\
&&3&1\\ \hline
(1399,5)&(2)&1&1\\
&(3)&1&1,2\\
&&2&1
\end{array}
\]

等价地，空型满足 \(R=K\)；\((2)\) 型满足
\(R=P\dot\cup K\)、\(\bar\sigma(P)=2q\)、
\(\sigma(P)=2x-ka\)；\((3)\) 型满足
\(R=P\dot\cup K\)、\(\bar\sigma(P)=3q\)、
\(\sigma(P)=3x-ka\)。相应短块长度与证明的 (30)、(32) 逐行一致。

若 \(|P|\ge2\)，其投影原子性仍要求每个非空真位置子集在
\(C_p^2=C_p^3/\langle q\rangle\) 中和非零；若 \(|P|=1\)，唯一位置
商标签分别为 \(2q\)、\(3q\)。作者没有丢掉这些内部位置条件，也
没有声称 (28)--(32) 已构成完整标号或长补原子实现。

## 8. 独立计算、脚本回归与证书

主核验器没有导入目标模块，并独立完成：

- 重建十四个素数—packing 行的两个核心数、实际互补关系和商和值；
- 独立枚举十七个互补块尺寸候选；
- 枚举全部二十四个非空子族结构行和每个统一
  \((k_i)\in\{1,2\}^t\)，复得十二个短谱尺寸及十四个非空偏差；
- 独立施加系数一单点纤维门，复得十个最终尺寸、八个非空尺寸与
  十二个非空偏差；
- 将所有结构行、尺寸、偏差、通过标志与汇总字段逐项同报告比较。

独立生成的 `cases` 与报告完全一致。另在内存中执行作者脚本的
`build_report()`，所得完整对象与存档 JSON 完全相同，未重写报告。

移除顶层 `certificate_sha256` 后，按 UTF-8、排序键与紧凑分隔符重新
规范序列化，得到

\[
\mathtt{b08b3afd002535bc946da3fad778281cd640d8d1c37fda05fca48631e29f2463},
\]

与报告证书一致；报告列出的六个依赖 SHA 均与当前文件字节一致。

审计时冻结文件 SHA-256：

```text
20a0f36731e75b9882840ff64dce63f98f029c803a3a6908fcb3314176e368b2  unique_tail_all_packing_short_blocks.py
4dadb5a6fca18da42ccd95821cc176cd9fae1ce2653ddb2e14406e5e66694ceb  unique_tail_all_packing_short_blocks_report.json
7abe228fa70dabd8858a40507b11505bd9cee388aa89fd79cd7a22fb8ec68238  proofs/unique_tail_all_packing_short_blocks.md
0e10138860269a18f0f7c0a02ab40204109efbb9a09688fc99da46983e390aed  assumptions.md
d886a84857cd430455558266a2ab175f21f2de853eed08c6affcad0c14b3efcc  proofs/middle_quotient_gap.md
1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942  proofs/unique_tail_common_R_next.md
35f355d2fe1b3dc7a98e3011e44f0e3cdea17cfdd104c026042081b00c4539d3  verifications/unique_tail_common_R_next_independent_review.md
a30707af2f6ef04da720a8eb3c1e97b1c7c297eecc67cf6879ff1191ff9afa8b  proofs/unique_tail_position_conflict_frontier.md
93381c12a56f32469d6dcb0d21c65b22509837484323e2ad1763a81218d771b5  verifications/unique_tail_position_conflict_frontier_independent_review.md
```

## 9. 精确停止线

本结论只把两个目标素数处的七种共同 packing 必要类型压到空型、
\((2)\)、\((3)\)，并给出 (28)--(32) 的小原子必要接口。它没有证明
三个幸存型中任何一个可实现或为空，没有关闭唯一尾分支，也没有证明
\(A_p\)。十个最终尺寸与十二个非空偏差只是必要有限边缘，不是完整
位置标号 SAT、同一 \(K\) 的全端点余部分解、实际 Hasse 系统或全部
长补原子内部子集和证书。作者证明、脚本与报告的停止线一致，没有
发生上述越界外推。

FINAL VERDICT: **CORRECT**
