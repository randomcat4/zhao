# 强制共同原子型的全部子族短块与长补纤维闭合：全新独立审计

STATUS: **CORRECT**

## 1. 审计对象与精确范围

本审计只认证以下三个作者工件所陈述的局部结论：

- `unique_tail_forced_atom_subset_blocks.py`；
- `unique_tail_forced_atom_subset_blocks_report.json`；
- `proofs/unique_tail_forced_atom_subset_blocks.md`。

适用范围严格限于

\[
(p,b)=(233,4),\qquad(1399,5),
\]

以及共同实际位置分解中的三个强制 packing 型

\[
(3),\qquad(1,2),\qquad(1,1,1).
\]

输入是上一条已独立审计的短 packing 界及其十个尺寸向量。本轮没有
修改作者工件，没有把有限筛选解释成完整标号可满足性，也没有引入
新的高度、Hasse 或长补结构假设。

## 2. 每个非空原子子族产生真实商零块

冻结的同一实际位置分解为

\[
X=x^{p-4},\qquad U\subseteq L\subseteq Y,
\]

\[
R=P_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}P_t
  \mathbin{\dot\cup}K,\qquad R=Y\setminus L,
\]

其中每个 \(P_i\) 非空，且

\[
\bar\sigma(P_i)=d_iq,\qquad
\bar\sigma(U)=-bq,\qquad |U|=3.
\]

固定任意非空指标集 \(I\subseteq\{1,\ldots,t\}\)，记

\[
d_I=\sum_{i\in I}d_i,qquad
n_I=\sum_{i\in I}|P_i|,qquad
P_I=\mathbin{\dot\bigcup}_{i\in I}P_i.
\]

三个目标型都是正整数分拆 \(3\)，故 \(1\le d_I\le3\)。由于
\(b\in\{4,5\}\)，

\[
1\le b-d_I\le4\le p-4.
\]

因此可以从实际多重位置块 \(X\) 选出 \(b-d_I\) 个位置，并定义

\[
D_I=X_{b-d_I}\mathbin{\dot\cup}U\mathbin{\dot\cup}P_I.
\]

这里 \(X\cap Y=\varnothing\)，而 \(U\subseteq L\)、
\(P_I\subseteq R=Y\setminus L\)，所以这是实际位置不交并，不是形式
线性组合。其商和逐项为

\[
\bar\sigma(D_I)
=(b-d_I)q-bq+d_Iq=0.
\]

对十个输入尺寸逐个枚举全部非空 \(I\)，得到下列完整长度表；括号
内按单点子族、二点子族、全子族的自然次序列出：

\[
\begin{array}{c|c|c|c}
(p,b)&\text{型}&(|P_i|)&(|D_I|)_{\varnothing\ne I}\\ \hline
(233,4)&(3)&(1),(2),(3)&5;\ 6;\ 7\\
&(1,2)&(1,1)&7,6,6\\
&&(1,2)&7,7,7\\
&&(2,1)&8,6,7\\
&(1,1,1)&(1,1,1)&7,7,7,7,7,7,7\\ \hline
(1399,5)&(3)&(1),(2)&6;\ 7\\
&(1,2)&(1,1)&8,7,7
\end{array}
\]

所以全部二十四个派生块长度均在 \([2,8]\) 内；事实上都在
\([5,8]\) 内。每个块都处于冻结短谱的适用范围。它们有正核心
\(b-d_I\ne b\)，尾为 \(U\dot\cup P_I\ne U\)，故绝不可能是唯一
正核心 \(F_3\) 对 \((b,U)\)。因此允许实际和族恰为：长度五、六取
\(\{a,2a\}\)，长度七只取 \(\{2a\}\)，长度八无允许值。

## 3. 同一组实际轴偏差

由 \(\bar\sigma(P_i)=d_iq\) 及 \(\bar x=q\)，差
\(\sigma(P_i)-d_ix\) 位于商映射的核 \(\langle a\rangle\)。因此存在
唯一 \(c_i\in\mathbb F_p\) 使

\[
\sigma(P_i)=d_ix+c_ia.
\]

对单元素子族 \(I=\{i\}\)，

\[
\sigma(D_{\{i\}})=(3+c_i)a.
\]

一个尺寸向量若能通过全部子族短谱，则该值只能是 \(a\) 或 \(2a\)，
所以恰可写成

\[
c_i=-k_i,qquad k_i\in\{1,2\}.
\]

这些 \(k_i\) 是同一实际原子 \(P_i\) 的固定偏差，不能针对不同
\(D_I\) 重新选择。对每个非空 \(I\)，直接相加得到

\[
\sigma(D_I)=\left(3-\sum_{i\in I}k_i\right)a.
\]

因为 \(t\le3\)、\(k_i\le2\)，总和至多六，而两个素数都远大于六，
比较短谱允许系数时没有模 \(p\) 回绕歧义。

## 4. 十个尺寸向量的完整筛选

不导入作者模块的替代枚举从 \(N\le7-b\) 独立重建十个输入尺寸，
再对每个非空 \(I\) 同时施加上一节的固定 \((k_i)\)。结果为

\[
\begin{array}{c|c|c|c}
(p,b)&\text{型}&(|P_i|)&\text{幸存 }(k_i)\\ \hline
(233,4)&(3)&(1)&(1),(2)\\
&&(2)&(1),(2)\\
&&(3)&(1)\\
&(1,2)&(1,1)&(1,1)\\
&&(1,2),(2,1)&\varnothing\\
&(1,1,1)&(1,1,1)&\varnothing\\ \hline
(1399,5)&(3)&(1)&(1),(2)\\
&&(2)&(1)\\
&(1,2)&(1,1)&\varnothing
\end{array}
\]

于是全部子族短谱把十个尺寸向量精确筛到六个，并留下九个偏差赋值。
具体地：

- \(p=233\) 的 \((1,1,1)\) 型被删除；三个单原子约束先迫使
  \(k_i=1\)，而二原子或全原子子族随即违反长度七只允许 \(2a\)；
- \(p=1399\) 的 \((1,2)\) 型被删除；系数一单原子子族本身已有
  长度八，而错误正核心 \(F_3\) 门不给任何允许实际和；
- \(p=233\) 的 \((1,2)\) 型只剩尺寸 \((1,1)\) 与固定偏差
  \((k_1,k_2)=(1,1)\)。此时两个单原子块分别为长度七、六的
  \(F_2\) 块，全子族块为长度六的 \(F_1\) 块。

\(p=1399\) 的 \((1,1,1)\) 型没有输入尺寸向量，因为它已经由上一条
短 packing 界精确删除。这一事实没有被重复计作新的子族短谱排除。

## 5. 长补原子的商层量词

最后暂留的 \(p=233\)、\((1,2)\)、尺寸 \((1,1)\) 行含一个
系数一单点原子 \(P_1=\{y\}\)。由同一实际商标签等式

\[
\bar\sigma(P_1)=q
\]

立即得到 \(\bar y=q\)。位置量词也严格吻合：

- \(y\in P_1\subseteq R=Y\setminus L\)；
- 每个选定零核心端点 \(H\) 都是 \(F_3\) 块且满足 \(H\subseteq L\)；
- 因而 \(y\notin H\)，并且零核心性还给出 \(H\cap X=\varnothing\)。

所以对每个这样的端点，实际补集

\[
B_H=Z\setminus H
\]

都同时包含 \(X=x^{p-4}\) 的全部 \(p-4\) 个 \(q\)-标签和额外位置
\(y\)。于是

\[
v_q(B_H)\ge p-3.
\]

上游长补原子定理的量词是：对每个 \(T\in\mathcal F_3\)，其实际
补集 \(B_T=Z\setminus T\) 在商群 \(C_p^3\) 中是原子，且对每个
非零商值 \(s\) 都有

\[
v_s(B_T)\le p-4.
\]

这里 \(H\in\mathcal F_3\)、\(q\ne0\)，所以该定理确实适用于同一个
\(B_H\) 和同一个商值 \(q\)，给出矛盾。证明没有把实际群值与商值
混淆，也没有把“某个端点”偷换成“每个端点”。由此删除最后一条
\((1,2)\) 行。

剩余 \((3)\) 型的单点若存在，其商标签是 \(3q\) 而非 \(q\)，因此
上述与 \(X\) 的 \(q\)-纤维叠加论证不能误用于该型。

## 6. 最终剩余接口

两个素数的三个强制型中最终只剩 \((3)\)。其五个尺寸向量与八个
偏差赋值恰为

\[
\begin{array}{c|c|c}
(p,b)&|P|&k\\ \hline
(233,4)&1&1,2\\
&2&1,2\\
&3&1\\
(1399,5)&1&1,2\\
&2&1
\end{array}
\]

等价地，\(\sigma(P)=3x-ka\)。当 \(|P|\ge2\) 时，投影原子定义仍
要求每个非空真位置子集在 \(C_p^2=C_p^3/\langle q\rangle\) 中和
非零；目标证明明确保留了这项尚待统一标签核验的内部条件。

## 7. 独立计算、脚本回归与证书

替代核验没有导入目标模块。它独立完成并核对：

- 由 \(N\le7-b\) 重建十个输入尺寸向量；
- 枚举每个向量的全部非空原子指标子集，共二十四个结构行；
- 穷举同一组 \((k_i)\in\{1,2\}^t\)，逐行比较实际系数与长度窗；
- 复得“十个输入向量 \(\to\) 六个短谱向量、九个偏差赋值
  \(\to\) 五个长补门后向量、八个偏差赋值”；
- 将每个结构行、偏差行、通过标志及汇总字段与报告逐字段比较。

独立生成的 `cases` 与报告完全一致。另在内存中执行作者脚本的
`build_report()`，所得完整对象与存档 JSON 完全相同，未重写作者
报告。

移除顶层 `certificate_sha256` 后，按 UTF-8、排序键和紧凑分隔符重新
规范序列化，得到

\[
\mathtt{c582ddc8f37ad47b2e892084c0a6a95c13a2c5d106c5057da23dc62833d4a7fe},
\]

与报告证书一致。报告所列六个依赖文件 SHA 也均与当前磁盘字节一致。

审计时冻结文件 SHA-256：

```text
c3307a43095c32289b43d34f7a75814012e19cba940e8e770b798e218f4e3ade  unique_tail_forced_atom_subset_blocks.py
24fc2586cb3cfab976f8626310b04fd4c3c32348f87870f1c6ad8f2b55416ac7  unique_tail_forced_atom_subset_blocks_report.json
9b1a383f137849ed8a6eb42c7700a65f0a309688b2a6cd55c758b7a2ecdde686  proofs/unique_tail_forced_atom_subset_blocks.md
f3c03628690b5b88a4252e3a4347e2b5fa0436dc2a1c52d8eed1398f3e1feddc  proofs/unique_tail_forced_short_packing_block.md
61d099730afb9a9d81c96251c63e4ef3b2a1b4ee04e16ceb1b3caeecc525e647  verifications/unique_tail_forced_short_packing_block_independent_review.md
a30707af2f6ef04da720a8eb3c1e97b1c7c297eecc67cf6879ff1191ff9afa8b  proofs/unique_tail_position_conflict_frontier.md
93381c12a56f32469d6dcb0d21c65b22509837484323e2ad1763a81218d771b5  verifications/unique_tail_position_conflict_frontier_independent_review.md
1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942  proofs/unique_tail_common_R_next.md
4c18fe34b713ca0bd38ab8b0f5d37d815952301bbbf8bd6359b1a6fa139c847a  route_a_atom_line_rigidity.md
0e10138860269a18f0f7c0a02ab40204109efbb9a09688fc99da46983e390aed  assumptions.md
```

## 8. 精确停止线

本结论只关闭两个目标素数处三个强制 packing 型中的 \((1,2)\) 与
\((1,1,1)\)，并把剩余 \((3)\) 型压到五个尺寸向量、八个实际偏差。
它没有证明 \((3)\) 型为空，没有关闭四个非强制 packing 型，没有
证明唯一尾分支为空，也没有证明 \(A_p\)。五个剩余尺寸与八个偏差
只是必要边缘接口，不是完整位置标号 SAT、长补原子实现或反例证书。
作者证明、脚本及报告的停止线一致，没有发生上述过度外推。

FINAL VERDICT: **CORRECT**
