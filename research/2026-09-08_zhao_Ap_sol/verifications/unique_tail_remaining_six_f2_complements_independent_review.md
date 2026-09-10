# 剩余十二赋值中的六项二族块及其极长补原子：全新独立审计

STATUS: **CORRECT**

## 1. 审计对象、冻结 SHA 与裁决边界

本审计只核验以下三个作者工件给出的局部结论：

- `unique_tail_remaining_six_f2_complements.py`，SHA-256
  `28791cbb0d9a117c710e6ac31e4e8fbf3202b3020bf6a6d40f2d60f361b8e0f2`；
- `unique_tail_remaining_six_f2_complements_report.json`，SHA-256
  `f64a708a0730372038eef23e5236a061da7053fd9b9dda154878cbb0182801d9`；
- `proofs/unique_tail_remaining_six_f2_complements.md`，SHA-256
  `5653c0286a5b8957eaee55c86ad55e87676b6b21f1a1301b44bf056a926a9bc1`。

适用参数只有

\[
(p,b)=(233,4),\qquad(1399,5),
\]

且只处理上一轮留下的非空 packing 型 \((2),(3)\) 的十二个实际
偏差赋值。结论是其中恰有三行自动给出六项实际和为 \(2a\) 的商零
块，并且这三行中该块的字面补集是商原子。这里没有证明任一幸存行
可实现，也没有关闭空 packing、唯一尾分支或全局 \(A_p\)。

## 2. 不导入作者模块的十二行重建

我以独立标准库检查程序硬编码上一轮报告已认证的最终 \((2),(3)\)
接口，只读取 JSON 作结果比对；主重建没有导入作者模块。记 packing
系数为 \(d\)，原子尺寸为 \(n=|P|\)，统一实际偏差为 \(k\)。对同一
批实际位置

\[
C=X_{b-d}\mathbin{\dot\cup}U\mathbin{\dot\cup}P
\]

上游接口为

\[
\bar x=q,\quad \bar\sigma(U)=-bq,\quad
\sigma(U)=3a-bx,\quad
\bar\sigma(P)=dq,\quad \sigma(P)=dx-ka.
\]

所以各部分既是两两不交的真实位置块，又逐式满足

\[
\bar\sigma(C)=(b-d)q-bq+dq=0,
\]

以及

\[
|C|=b-d+3+n,\qquad
\sigma(C)=(3-k)a,\qquad |X_{b-d}|=b-d.
\]

独立枚举的十二行如下；末列表示同时满足 \(|C|=6\) 与
\(\sigma(C)=2a\)。

| \(p\) | 型 | \(d\) | \(n\) | \(k\) | \(|C|\) | 实际系数 \(3-k\) | 强迫行 |
|---:|:---:|---:|---:|---:|---:|---:|:---:|
| 233 | (2) | 2 | 1 | 1 | 6 | 2 | 是 |
| 233 | (2) | 2 | 1 | 2 | 6 | 1 | 否 |
| 233 | (2) | 2 | 2 | 1 | 7 | 2 | 否 |
| 233 | (3) | 3 | 1 | 1 | 5 | 2 | 否 |
| 233 | (3) | 3 | 1 | 2 | 5 | 1 | 否 |
| 233 | (3) | 3 | 2 | 1 | 6 | 2 | 是 |
| 233 | (3) | 3 | 2 | 2 | 6 | 1 | 否 |
| 233 | (3) | 3 | 3 | 1 | 7 | 2 | 否 |
| 1399 | (2) | 2 | 1 | 1 | 7 | 2 | 否 |
| 1399 | (3) | 3 | 1 | 1 | 6 | 2 | 是 |
| 1399 | (3) | 3 | 1 | 2 | 6 | 1 | 否 |
| 1399 | (3) | 3 | 2 | 1 | 7 | 2 | 否 |

所以精确三行为

\[
(233,(2),n,k)=(233,(2),1,1),
\]

\[
(233,(3),n,k)=(233,(3),2,1),\qquad
(1399,(3),n,k)=(1399,(3),1,1).
\]

独立生成的十二个完整字段对象与报告
`remaining_nonempty_defect_assignments` 逐字段、逐顺序相同；没有第四行
满足判据。三行的正核心数分别为 \(2,1,2\)，且 \(P\ne\varnothing\)。

## 3. 字面补集与补核二分

固定上述任一强迫行。由 \(|Z|=3p+4\)、\(\sigma(Z)=0\) 以及
\(\bar\sigma(Z)=0\)，对字面位置补集

\[
B=Z\setminus C
\]

有

\[
|B|=3p-2,\qquad \bar\sigma(B)=0,
\qquad \sigma(B)=-2a.
\]

若 \(\pi(B)\) 不是原子，取一个非平凡商零分拆的较短边 \(E\)。
两边都是同一 \(B\) 内的真实位置块，故

\[
0<|E|\le\left\lfloor\frac{3p-2}{2}\right\rfloor<2p+2.
\]

冻结的中间商零禁窗 \([p+2,2p+2]\) 排除较长可能，得到
\(|E|\le p+1\)。又因 \(E\subseteq Z\subseteq R\)，短商零接口给出

\[
\sigma(E)=\mu a,\qquad \mu\in\{1,2,3\}.
\]

正系数长度界在这里可直接独立复算。若 \(|E|\ge6+\mu\)，则
\(Z\setminus E\) 与外部的 \(\mu\) 个 \(a\)-锚点组成非空实际零和，
其长度

\[
3p+4-|E|+\mu\le3p-2,
\]

违反冻结反例。所需锚点至多三个，两个参数下都由外部
\(a^{p-4}\) 提供。因此

\[
|E|\le5+\mu.
\]

若 \(\mu=2\) 或 \(3\)，块 \(C\dot\cup E\) 的实际和分别为
\(4a\) 或 \(5a\)。从与 \(R\) 不交的外部锚点分别取 \(p-4\) 或
\(p-5\) 项，数量均不超过现有的 \(p-4\) 项。所得非空实际零和的
长度至多

\[
6+(5+\mu)+p-(2+\mu)=p+9\le3p-2,
\]

矛盾。因此只能有 \(\mu=1\)。

此时 \(D=C\dot\cup E\) 是实际和为 \(3a\) 的商零块。上面的同一
字面补集加三锚点论证对 \(D\subsetneq Z\) 给出 \(|D|\le8\)，所以
\(6+|E|\le8\)。同时 \(|E|=1\) 会令 \(E\) 是位于 \(R\) 中的一个
额外 \(a\) 位置，违反冻结高度界 \(h(S)\le p-4\) 与已经存在的
外部 \(a^{p-4}\)；等价地，这就是一族窗口没有单项。因此

\[
|E|=2,
\]

而 \(D\) 是长度八的 \(F_3\) 块。完整 \(F_3\) 补原子接口适用于
这个同一实际位置块，故

\[
B'=Z\setminus D=B\setminus E
\]

的商投影是长度 \(3p-4\) 的原子。这证明了所需二分，而不是只匹配
长度的抽象原子：

\[
\pi(B)\text{ 是长度 }3p-2\text{ 的原子},
\]

或

\[
B=E\mathbin{\dot\cup}B',\quad |E|=2,\quad
\sigma(E)=a,\quad \pi(B')\text{ 是长度 }3p-4\text{ 的原子}.
\]

## 4. 唯一正核心尾确实删除第二支

三行均有

\[
b-d>0,\qquad P\ne\varnothing,
\qquad U\cap P=\varnothing.
\]

若二分第二支发生，则长度八 \(F_3\) 块

\[
D=C\mathbin{\dot\cup}E
\]

仍至少含 \(C\) 中的 \(b-d>0\) 个 \(X\)-位置，故有正核心；其
\(Y\)-尾至少包含互不相交的 \(U\dot\cup P\)，严格大于 \(U\)。
加入 \(E\) 只能再增加位置，不可能删去 \(P\)。这与冻结的“一切
正核心 \(F_3\) 块的尾恰为 \(U\)”接口正面矛盾。因此第二支不可能，
必有

\[
\boxed{\pi(Z\setminus C)\text{ 是长度 }3p-2\text{ 的原子}.}
\]

两参数下补长独立复算为

\[
3\cdot233-2=697,\qquad 3\cdot1399-2=4195.
\]

按商原子的定义，每个非空真位置子集
\(E\subsetneq Z\setminus C\) 都有 \(\bar\sigma(E)\ne0\)。报告在这里
保留的是补块的全部内部子集和约束，而不只是长度或纤维重数。

## 5. 依赖、证书与执行重放

报告列出的七个依赖 SHA-256 均以当前字节重算并逐项命中：

| 依赖 | SHA-256 |
|:---|:---|
| `assumptions.md` | `0e10138860269a18f0f7c0a02ab40204109efbb9a09688fc99da46983e390aed` |
| `proofs/middle_quotient_gap.md` | `d886a84857cd430455558266a2ab175f21f2de853eed08c6affcad0c14b3efcc` |
| `proofs/unique_tail_all_packing_short_blocks.md` | `7abe228fa70dabd8858a40507b11505bd9cee388aa89fd79cd7a22fb8ec68238` |
| `proofs/unique_tail_position_conflict_frontier.md` | `a30707af2f6ef04da720a8eb3c1e97b1c7c297eecc67cf6879ff1191ff9afa8b` |
| `unique_tail_all_packing_short_blocks_report.json` | `4dadb5a6fca18da42ccd95821cc176cd9fae1ce2653ddb2e14406e5e66694ceb` |
| `verifications/unique_tail_all_packing_short_blocks_independent_review.md` | `d22d9380a0dc98c21a691384901a9f826f88b72bab85042beafc053eed8124e3` |
| `verifications/unique_tail_position_conflict_frontier_independent_review.md` | `93381c12a56f32469d6dcb0d21c65b22509837484323e2ad1763a81218d771b5` |

移除报告的 `certificate_sha256` 字段后，以 UTF-8、键排序、无空白分隔
的规范 JSON 重算 SHA-256，得到

`7a26b7e09d3cb5c0c9f5a94249699ef94ef1328d11a2ea443f2c8bf5bc34f4ec`，

与报告证书完全相同。独立构造的报告有效载荷也逐字段匹配。作为次级
检查再执行作者构造器时，内存对象中的三条 `forced_keys` 是 tuple，
而落盘 JSON 必然将其正规化为数组；经过一次标准 JSON 序列化再解析
后，作者构造结果与冻结报告严格相等。这只是 Python 容器类型的正常
序列化差异，不改变证书或数学内容。

## 6. 严格停止线与最终裁决

本轮只认证三条自动六项 \(2a\) 块的长度 \(3p-2\) 字面补集为商
原子，及由此得到的全部非空真内部子集商和非零。它不声称：

- 三条强迫行中的任何一条可实现；
- 其余九个非空偏差赋值可实现或已被关闭；
- 空 packing 可实现；
- 唯一尾分支为空；
- 已证明全局 \(A_p\)。

未发现较短边选择、禁窗端点、正系数长度界、外部锚点数量或总长度、
\(F_3\) 字面补原子量词、唯一正核心尾删除、十二行枚举、依赖冻结、
规范证书或范围声明中的错误。最终裁决为 **CORRECT**。
