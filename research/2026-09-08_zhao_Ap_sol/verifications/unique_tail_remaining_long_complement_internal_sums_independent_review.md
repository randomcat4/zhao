# 剩余非空型的长补全部内部子集和：全新独立审计

STATUS: **CORRECT**

## 1. 审计对象、冻结 SHA 与严格范围

本审计只认证以下三个作者工件的局部压缩结论：

- `unique_tail_remaining_long_complement_internal_sums.py`，SHA-256
  `009addb164b7784a839ffcb2ca3bbbea41c3d3ad105d0728634282da4737fcd5`；
- `unique_tail_remaining_long_complement_internal_sums_report.json`，SHA-256
  `b6b3de4097627d26a492f4d1034a1f753bc0d58b83edd92bd100815dd8fc3cae`；
- `proofs/unique_tail_remaining_long_complement_internal_sums.md`，SHA-256
  `311730df217f79659cf0d934b8c0df2e02489196208b9e699dc31d8b929d10d1`。

参数只包括

\[
(p,b)=(233,4),\qquad(1399,5),
\]

以及已经通过上游筛选的非空 packing 型 \((2),(3)\)。本轮检查的是
每个实际零核心端点 \(H\) 的同一真实位置分解与长补内部子集和；不把
不同端点的 \(Q_H\) 当作可独立选择的对象，也不证明任一尺寸行可实现。

## 2. 完整轴向判据的复算

固定一个实际零核心端点 \(H\)，写

\[
Q_H=K\mathbin{\dot\cup}(L\setminus H),\qquad
W_H=P\mathbin{\dot\cup}Q_H,
\]

其中 \(P\) 是固定的 \(C_p^2\) 投影零和原子，

\[
\bar\sigma(P)=dq,\qquad d\in\{2,3\},
\]

并且

\[
\rho(\bar\sigma(Q_H))=0,\qquad
\bar\sigma(Q_H)=(4-d)q,\qquad
\bar\sigma(W_H)=4q.
\]

相应长补商序列为

\[
B_H=q^{p-4}W_H.
\]

任一位置子序列唯一写成 \(q^tE\)，其中
\(0\le t\le p-4\)、\(E\subseteq W_H\)。若
\(\rho(\bar\sigma(E))=0\) 且 \(\bar\sigma(E)=cq\)，则它商零当且仅当

\[
t+c=0\pmod p.
\]

对 \(E=\varnothing\)，唯一解给出空集；对 \(E=W_H\)，唯一允许解
\(t=p-4\) 给出整个 \(B_H\)。对非空真 \(E\subsetneq W_H\)，存在
\(0\le t\le p-4\) 的解恰当且仅当

\[
c\in\{0,4,5,\ldots,p-1\}.
\]

因此 \(B_H\) 为商原子等价于完整的、未截断长度的判据

\[
\boxed{
\varnothing\ne E\subsetneq W_H,
\quad\rho(\bar\sigma(E))=0
\Longrightarrow
\bar\sigma(E)\in\{q,2q,3q\}.}
\]

这一步同时证明必要性与充分性，并正确保留了空集和全集两个边界。

## 3. 对 \(A\subseteq P\) 的三类分解确实穷尽

每个 \(E\subseteq W_H\) 唯一写成

\[
E=A\mathbin{\dot\cup}T,\qquad
A\subseteq P,\quad T\subseteq Q_H.
\]

完整判据按 \(A\) 有且只有以下三类。

### 3.1 \(A=\varnothing\)

此时 \(E=T\)。若 \(E\) 是非空真子集，则 \(T\ne\varnothing\)。

- 对 \(T\subsetneq Q_H\) 的 \(\rho\)-零子集，正是报告记录的
  \(Q_H\) 内部规则；
- \(T=Q_H\) 仍是 \(W_H\) 的真子集，因为 \(P\ne\varnothing\)，其
  轴系数为 \(4-d\in\{1,2\}\)，自动允许；
- \(T=\varnothing\) 只给出空集，不属于判据量词。

### 3.2 \(A=P\)

此时 \(E\) 为真子集恰要求 \(T\subsetneq Q_H\)。

- \(T=\varnothing\) 给出 \(E=P\)，轴系数
  \(d\in\{2,3\}\)，自动允许；
- 对非空真 \(\rho\)-零 \(T\)，轴系数从 \(c\) 平移成 \(c+d\)，
  正由下一节的同时判据处理；
- \(T=Q_H\) 给出整个 \(W_H\)，正确地不属于非空真子集量词。

### 3.3 \(\varnothing\ne A\subsetneq P\)

因为 \(P\) 是 \(\rho\)-原子，\(\rho(\bar\sigma(A))\ne0\)。所以

\[
\rho(\bar\sigma(E))=0
\quad\Longleftrightarrow\quad
\rho(\bar\sigma(T))=-\rho(\bar\sigma(A)).
\]

对该目标纤维内的每个实际位置子集 \(T\subseteq Q_H\)，完整判据恰为

\[
\bar\sigma(A)+\bar\sigma(T)\in\{q,2q,3q\}.
\]

由于目标值非零，\(T=\varnothing\) 和 \(T=Q_H\) 实际上都不会命中；
但把量词写成全部 \(T\subseteq Q_H\) 是正确且更整洁的。三类合起来
既无遗漏也无重叠，故作者所称“充要压缩”成立。

## 4. \(d=2,3\) 的轴系数平移

任取

\[
\varnothing\ne S\subsetneq Q_H,\qquad
\rho(\bar\sigma(S))=0,\qquad
\bar\sigma(S)=cq.
\]

因为 \(P\ne\varnothing\) 且 \(S\ne Q_H\)，\(S\) 与
\(P\dot\cup S\) 都是 \(W_H\) 的非空真实际位置子集。完整轴向判据
同时给出

\[
c\in\{1,2,3\},\qquad c+d\pmod p\in\{1,2,3\}.
\]

这里 \(p\ge233\) 且 \(c+d\le6<p\)，不存在模回绕。直接枚举得

\[
d=3:\quad c\text{ 无解},
\]

\[
d=2:\quad c=1\text{ 是唯一解}.
\]

又 \(\rho(Q_H)=0\) 且上游保证 \(Q_H\ne\varnothing\)。所以型
\((3)\) 中 \(Q_H\) 没有非空真 \(\rho\)-零位置子集，即
\(\rho(Q_H)\) 是原子；型 \((2)\) 中每个这样的真零子集轴系数恰为
一。

## 5. 型 \((2)\) 的原子补配对、反链与非单点

令 \(d=2\)，并取任一上述 \(S\)。由

\[
\bar\sigma(Q_H)=2q,\qquad\bar\sigma(S)=q
\]

可得

\[
\bar\sigma(Q_H\setminus S)=q.
\]

若 \(S\) 不是 \(C_p^2\) 中的零和原子，可取非空真
\(T\subsetneq S\) 且 \(\rho(\bar\sigma(T))=0\)。则
\(T,S\setminus T\) 都是 \(Q_H\) 的非空真 \(\rho\)-零位置子集，
上一节迫使二者的轴系数都为一；它们的并 \(S\) 就有轴系数二，与
\(\bar\sigma(S)=q\) 矛盾。故 \(S\) 是原子；把同一论证用于
\(Q_H\setminus S\) 得到补因子也为原子。

因此全部非空真 \(\rho\)-零子集对取补封闭，并且任一成员都不能真含
另一个成员，所以形成反链。若根本没有这样的 \(S\)，则 \(Q_H\)
本身是系数二原子；正文没有错误地断言必须存在一次分裂。

若 \(|S|=1\)，其唯一位置的完整商标签就是 \(q\)。但
\(B_H=q^{p-4}W_H\) 已有 \(p-4\) 个 \(q\)-位置，于是
\(v_q(B_H)\ge p-3\)，严格违反每个长补原子中任一非零商纤维的
统一上界 \(p-4\)。补因子的轴系数同样为一，所以
\(|Q_H\setminus S|=1\) 也以相同理由被排除。故每个实际发生的补配对
两侧都至少有两个位置。

报告在型 \((3)\) 行中把
`proper_rho_zero_Q_H_subsets_are_atoms` 与
`proper_rho_zero_Q_H_subsets_have_size_at_least_two` 置为 `false`，其
语义是“型 \((2)\) 的非平凡原子分裂规则未启用”，不是断言存在反例；
型 \((3)\) 根本没有这类真子集，相关裸全称命题在逻辑上当然是空真。
按报告的分支分类与 scope 读取时不存在数学矛盾，但不得把这两个
`false` 反读成存在非原子或单点真零子集。

## 6. 补冗余与 \(0,1,3\) 个独立目标

对任意非空真 \(A\subsetneq P\)，同时取补

\[
(A,T)\longmapsto(P\setminus A,Q_H\setminus T).
\]

由于 \(\rho(P)=\rho(Q_H)=0\)，该映射把

\[
\rho(\bar\sigma(T))=-\rho(\bar\sigma(A))
\]

精确送到补侧的相应目标纤维。又因
\(\bar\sigma(W_H)=4q\)，若原侧总轴系数为 \(c\)，补侧就是
\(4-c\pmod p\)。集合 \(\{1,2,3\}\) 在
\(c\mapsto4-c\) 下不变，所以一对互补条件完全等价。

非空真子集与其补集不可能相同，故轨道数严格为

\[
\frac{2^{|P|}-2}{2}=2^{|P|-1}-1.
\]

对 \(|P|=1,2,3\) 分别得到

\[
0,\qquad1,\qquad3.
\]

报告采用位置位掩码较小者作代表，精确为

\[
|P|=1:\ \varnothing;\qquad
|P|=2:\ \{1\};\qquad
|P|=3:\ \{1\},\{2\},\{1,2\}.
\]

最后一组三个集合分别代表与
\(\{2,3\},\{1,3\},\{3\}\) 的补配对，确实每轨道恰取一次。代表的
具体选择只是规范约定，\(0,1,3\) 的计数及充要性不依赖该约定。

## 7. 八个尺寸行的无导入重建

我没有导入作者模块，而是从上一轮冻结的幸存尺寸接口独立抄录八个
\((p,b,\text{型},d,|P|)\) 五元组，再按前述公式重建全部字段：

| \(p\) | \(b\) | 型 | \(d\) | \(|P|\) | \(Q_H\) 规则 | 独立目标数 |
|---:|---:|:---:|---:|---:|:---|---:|
| 233 | 4 | (2) | 2 | 1 | 真零子集系数一、原子补配对、非单点 | 0 |
| 233 | 4 | (2) | 2 | 2 | 真零子集系数一、原子补配对、非单点 | 1 |
| 233 | 4 | (3) | 3 | 1 | \(Q_H\) 为原子 | 0 |
| 233 | 4 | (3) | 3 | 2 | \(Q_H\) 为原子 | 1 |
| 233 | 4 | (3) | 3 | 3 | \(Q_H\) 为原子 | 3 |
| 1399 | 5 | (2) | 2 | 1 | 真零子集系数一、原子补配对、非单点 | 0 |
| 1399 | 5 | (3) | 3 | 1 | \(Q_H\) 为原子 | 0 |
| 1399 | 5 | (3) | 3 | 2 | \(Q_H\) 为原子 | 1 |

结果为八行、五个型 \((3)\) 原子行、三个型 \((2)\) 原子补配对行；
生成的 `remaining_nonempty_size_rows` 与冻结报告逐字段、逐顺序相同。
特别地，型 \((3)\)、\(|P|=1\) 没有混合目标，完整长补判据恰退化为
\(Q_H\) 原子性；从这一硬边界本身不能推出新矛盾。

## 8. 依赖、证书与执行核验

报告列出的七个依赖 SHA-256 均按当前文件字节重算并命中：

| 依赖 | SHA-256 |
|:---|:---|
| `proofs/unique_tail_all_packing_short_blocks.md` | `7abe228fa70dabd8858a40507b11505bd9cee388aa89fd79cd7a22fb8ec68238` |
| `proofs/unique_tail_common_R_next.md` | `1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942` |
| `proofs/unique_tail_labelled_position_next.md` | `60384c64dee88487220f3fd7101a5d3abff1cb576fe3a8b43ec398fdd284ddce` |
| `unique_tail_all_packing_short_blocks_report.json` | `4dadb5a6fca18da42ccd95821cc176cd9fae1ce2653ddb2e14406e5e66694ceb` |
| `verifications/unique_tail_all_packing_short_blocks_independent_review.md` | `d22d9380a0dc98c21a691384901a9f826f88b72bab85042beafc053eed8124e3` |
| `verifications/unique_tail_common_R_next_independent_review.md` | `35f355d2fe1b3dc7a98e3011e44f0e3cdea17cfdd104c026042081b00c4539d3` |
| `verifications/unique_tail_labelled_position_next_independent_review.md` | `7cc525664dbbf7eeb23d04b3e061f0c4feac07100c7b6c294ee018ad658f20dd` |

移除报告的 `certificate_sha256` 字段后，以 UTF-8、键排序、紧凑分隔
的规范 JSON 重算 SHA-256，得到

`fe15a00d8235419ac0a68144fdb892b0ded20f4e133da0cc6cf9fd1ed009eb9e`，

与报告完全相同。无导入独立程序还检查了八行、\(5/3\) 分支计数、
\(0/1/3\) 补轨道数、所有报告字段及源文件语法，全部通过。

## 9. 停止线与最终裁决

本轮只把每个剩余非空型、每个实际零核心端点的完整长补内部子集和
压缩为：型 \((3)\) 的 \(Q_H\) 原子性；型 \((2)\) 的全部真零子集
系数一原子补配对及非单点性；以及每个非空真 \(A\subsetneq P\) 的
混合目标纤维全称条件。报告只计互补冗余后的 \(A\)-轨道，不枚举也
不声称目标 \(T\)-纤维非空，更没有构造 \(C_p^2\) 标签模型。

未证明、也没有被本文声称证明的是：任一八行可实现；空 packing 可
实现；不同端点可独立选择各自 \(Q_H\)；唯一尾分支为空；或全局
\(A_p\)。

未发现完整轴向判据、三类子集量词、\(d=2,3\) 平移、型 \((2)\)
原子补反链与非单点论证、补冗余、八行枚举、依赖冻结、规范证书或
scope 中的实质错误。最终裁决为 **CORRECT**。
