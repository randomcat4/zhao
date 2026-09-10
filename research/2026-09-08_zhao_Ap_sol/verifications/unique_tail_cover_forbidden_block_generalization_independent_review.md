# 强制共同余部覆盖禁块一般化：全新独立审计

STATUS: **CORRECT**

## 1. 审计对象与精确适用域

本审计只认证下列三个工件所陈述的局部结果：

- `unique_tail_cover_forbidden_block_generalization.py`；
- `unique_tail_cover_forbidden_block_generalization_report.json`；
- `proofs/unique_tail_cover_forbidden_block_generalization.md`。

适用域严格固定为

\[
(p,\ell,b,r)=(233,7,4,3),\qquad(1399,8,5,3),
\]

三点唯一尾 \(U\)、四边端点族 \(\mathcal A\)，以及三个强制共同
余部原子型 \((3),(1,2),(1,1,1)\)。还须已有一个不同双点迹覆盖对
\(H,J\)，从而

\[
K=\varnothing,\qquad L=H\cup J,\qquad Q_E=L\setminus E,
\]

每个 \(Q_E\) 都是 \(C_p^2\) 中按实际位置计数的投影零和原子，且

\[
\bar\sigma(Q_E)=q,\qquad \sigma(Q_E)=S,\qquad
\bar\sigma(U)=-bq,\qquad q\ne0.
\]

覆盖对的两个不同双点迹共享一个 \(U\)-位置，四边端点又共享非轴
位置 \(y\)，故 \(|L|\le 8+8-2=14\)。本文的所有 \(w\le14\)
结论都依赖这一覆盖对子分支，不能移到一般 \(|L|\le52\) 接口。

第 3 节的稠密形式按证明和程序的实际量词取
\(\varnothing\ne\mathcal S\subseteq\mathcal A\)、
\(k=|\mathcal S|\ge1\)、\(m\in\mathbb Z\)。若把空族也纳入，
\(k=0,m=-1\) 只给退化形式 \(U\)，是辅助句“自动有
\(0\le m\le k\)”的唯一空族例外；其 \(t=-b<4\)，既不进入大核门，
也不改变式 (25)。因此一般禁块结论的精确非退化适用域是 \(k\ge1\)。

## 2. 数学验缝

### 2.1 二余部的 26 个单位形式

对

\[
\alpha Q_E+\beta Q_F+\gamma U,qquad
(\alpha,\beta,\gamma)\in\{-1,0,1\}^3\setminus\{(0,0,0)\},
\]

逐 Venn 单元计算位置系数。独立实现使用三个 \(U\)-位置和四个彼此
独立赋值的尾外位置，检查了

\[
6^2\cdot16^2\cdot26=239,616
\]

行，比作者的 59,904 行回归使用更大的尾外测试域。恰有证明表 (11)
中的 12 个有向形式能够成为 \(0/1\) 指示子集；交换 \(E,F\) 后没有
遗漏形式。

形式的轴系数为

\[
t=\alpha+\beta-b\gamma.
\]

使用大 \(X\) 核须取 \(p-t\) 个 \(X\)-位置；因 \(|X|=p-4\)，
必须 \(t\ge4\)。在所有 26 个形式和全部合法非空真尾迹上，唯一仍能
在 \(U\) 的每个位置保持 \(0/1\) 系数者是

\[
(\alpha,\beta,\gamma)=(1,1,-1),
\]

即 \(Q_E+Q_F-U\)。差形式 \(Q_E-Q_F\) 或反向差若非空，则与两个
\(Q\) 的投影原子性及统一和值冲突；证明没有把它们误列为可用块。

### 2.2 覆盖对指示子集的充要条件与长度禁区

在 \(u\in U\) 上，\(Q_E+Q_F-U\) 的系数为

\[
1-\mathbf1_E(u)-\mathbf1_F(u),
\]

故为 \(0/1\) 当且仅当两个尾迹不交。在 \(z\in O=L\setminus U\)
上，系数为

\[
2-\mathbf1_E(z)-\mathbf1_F(z),
\]

故为 \(0/1\) 当且仅当 \(O\subseteq E\cup F\)。这逐位置证明了

\[
Q_E+Q_F-U\text{ 是实际子集}
\iff (E\cap U)\cap(F\cap U)=\varnothing,
\quad O\subseteq E\cup F.
\]

独立枚举另对 9,216 个端点对 incidence 直接核对了该充要条件。

若该块为 \(W_{EF}\)，则

\[
\bar\sigma(W_{EF})=(b+2)q,qquad
c=p-b-2\le p-4,qquad n=c+w.
\]

由 \(q\ne0\)、\(b+2<p\) 得 \(W_{EF}\ne\varnothing\)，而
\(W_{EF}\subseteq L\) 给 \(1\le w\le14\)。精确分段为

\[
\begin{cases}
w\le b+3 &\Longrightarrow 9\le n\le p+1,\\
w\ge b+4 &\Longrightarrow p+2\le n\le2p+2.
\end{cases}
\]

第一段使用唯一尾短谱所给的 \([9,p+1]\) 禁区，第二段使用一般中间
商零间隙 \([p+2,2p+2]\)；证明没有把二者混成同一来源。

### 2.3 任意非空端点子族的稠密形式

对

\[
W_{\mathcal S,m}=\sum_{E\in\mathcal S}Q_E-mU,
\]

尾外位置与尾位置的系数分别为

\[
k-d_{\mathcal S}(z),\qquad k-d_{\mathcal S}(u)-m.
\]

因此逐位置 \(0/1\) 的充要条件确为

\[
d_{\mathcal S}(z)\in\{k-1,k\}\ (z\in O),\qquad
d_{\mathcal S}(u)\in\{k-m-1,k-m\}\ (u\in U).
\]

独立小型实现把 \(m\) 扩展到证明范围之外的
\(-3\le m\le k+2\)，共检查 7,542 个族—参数实例，逐项得到直接
系数判定与度条件等价；对 \(k\ge1\) 的合法非空真尾迹，任何指示子集
均满足 \(0\le m\le k\)。统一标签给

\[
t=k+mb.
\]

四边图无孤立点，故端点数至多八；于是
\(t\le8+8b\le48<p\)。若 \(t\ge4\)，则 \(p-t\) 个 \(X\)-位置
可取，且

\[
n=p-t+w.
\]

由 \(1\le w\le14\) 分为 \(w\le t+1\) 与 \(w\ge t+2\) 两段，
分别落入 \([9,p+1]\) 与 \([p+2,2p+2]\)。所以式 (22) 与
\(k+mb\ge4\) 不能同时成立。这里既使用了 \(p\in\{233,1399\}\)，
也使用了覆盖对给出的 \(|L|\le14\)；没有一般素数或一般端点数外推。

### 2.4 保护块 \(D_{EF}\)

对尾迹不交的端点对，若

\[
D_{EF}=Q_E\cap Q_F\cap O=L\setminus(E\cup F\cup U)
\]

为空，则正好满足上一节大核指示条件，已经被禁区排除，故每个幸存
骨架必有 \(D_{EF}\ne\varnothing\)。取
\(u\in F\cap U\)，迹不交给 \(u\notin E\)，故
\(u\in Q_E\setminus D_{EF}\)；交换 \(E,F\) 得 \(D_{EF}\) 也是
\(Q_F\) 的真子集。两个 \(Q\) 的投影原子性遂给

\[
\rho(\bar\sigma(D_{EF}))\ne0.
\]

因此从双重系数中减去一份 \(D_{EF}\) 虽得到实际子集，其和值
\((b+2)q-\bar\sigma(D_{EF})\) 却非轴向，不能只靠 \(X\)-位置闭合。
这一步的非空性、真子集性和非轴性论证完整。

## 3. 作者证书重放与独立替代实现

使用 UTF-8 环境和 Python 3.12.14 直接运行作者脚本，退出码为 0；
标准输出解析后的对象与存档报告逐字段完全相同。移除
`certificate_sha256` 字段后，按排序键、紧凑分隔符和 ASCII 转义重新
序列化并独立计算 SHA-256，得到

\[
\mathtt{36ed4fe5bbc17e2e7706bc06c02bfc11b85ee321eccd053fad1b77fd2c9e3c10}.
\]

另写了不导入作者模块的替代枚举器，从所有四条边、无孤立点的简单图
重新按图同构归并，恰得 11 个图型；随后独立枚举六种非空真尾迹着色、
覆盖候选和定向迹签名，得到：

\[
\begin{array}{c|r}
\text{合法迹着色}&28,584\\
\text{含不同双点迹覆盖候选的着色}&13,512\\
\text{覆盖候选出现次数}&24,468\\
\text{定向规范覆盖迹类}&372.
\end{array}
\]

替代实现还按证明给出的私有位置 \(a_0,b_0\)、公共位置 \(y\) 与两侧
可共享位置构造全部 372 个迹类；对两个素数共 744 个规范实例逐一回溯
验证端点互异、长度、三片横截、全部单位形式和全部非空稠密形式。
按 24,468 个出现次数加权，精确复现：

\[
\begin{array}{c|r}
\text{多端点形式检查}&28,340,748\\
\text{迹不交二余部大核门检查}&317,826\\
\text{单位形式检查}&16,971,084.
\end{array}
\]

并复现每个素数 24,468 个 incidence 幸存出现、零个
\(t\ge4\) 稠密 \(0/1\) 形式、\(p=233\) 的 2,035,770 个单位指示
命中、\(p=1399\) 的 1,982,670 个单位指示命中，以及两者各
215,430 个稠密指示命中。故 28,584 / 13,512 / 24,468 / 372 /
28,340,748 / 317,826 / 16,971,084 七个指定计数和构造均已独立重放。

## 4. 工件完整性

- 作者脚本语法检查通过，仅依赖 Python 标准库：`argparse`、
  `collections`、`hashlib`、`itertools`、`json`、`math`、`pathlib`。
- 报告是合法 JSON，作者重跑对象与存档对象完全一致；规范证书已独立
  重算。
- 证明文件有 34 对 `\\[...\\]`、114 对 `\\(...\\)`；4 个
  `array`、1 个 `cases`、1 个 `aligned` 环境均成对闭合。没有未配对
  美元定界符，也没有除换行、回车、制表符外的 C0 控制字符或 Unicode
  格式控制字符。
- 当前研究目录没有这条结果的 Lean 陈述或钉死工具链。只完成了 Lean
  4.32.0 / Lake 5.0.0 的 L0 工具链探测；本审计不声称
  `LEAN_FULLY_CHECKED` 或 `LEAN_PARTIALLY_CHECKED`。

审计时文件字节 SHA-256：

```text
f9bda3577fbbdc08da9a9e78b325cab701054855d83b24db70fe50f40a8e884a  unique_tail_cover_forbidden_block_generalization.py
117f8df799b721800813140eb59ba064fd702b0c50349d81e047f8caa864e3d8  unique_tail_cover_forbidden_block_generalization_report.json
7b5a3cbadf006145c51666523a4d2274ae0e9385f098fcbeb850e93bff2f0e1e  proofs/unique_tail_cover_forbidden_block_generalization.md
eaa63014bd956f83cf2a5bf799df9d3a8d8bcfb9bfbc56115897c806f323da12  frozen_theorem_v1.md
0e10138860269a18f0f7c0a02ab40204109efbb9a09688fc99da46983e390aed  assumptions.md
08b9c742842306b771798e73faa0774fdd206db797b76bc64d5a8ed389a67afc  hazards.md
60384c64dee88487220f3fd7101a5d3abff1cb576fe3a8b43ec398fdd284ddce  proofs/unique_tail_labelled_position_next.md
87954d09a00aa74d3d43ce7d784deeff325965e61fca80e900d610371260201f  proofs/unique_tail_four_edge_joint_csp.md
1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942  proofs/unique_tail_common_R_next.md
1cf95ee7bc431549108ee432955e21cd15ee58e00ba7ba5b05a0d96916d80b9d  proofs/unique_tail_seven_type_full_f3.md
8b65afeb55a419abe980225d5c19024b80106157f0657055f13d84ccf40aac6c  proofs/unique_tail_forced_common_atoms_attack.md
02e0df5f1ef092644c21209aea26d944efb8194d3bd23a88d6bacb367c512277  proofs/unique_tail_cover_survivor_lift.md
```

审计开始与结束均保持 Git HEAD
`77c51458cdb943495d084ee3bfc82ebf810b3dcf`，未提交。

## 5. 结论边界

认证成立的是单位形式分类、覆盖禁块充要条件、稠密形式逐位置判据与
有限 incidence/迹/大小幸存构造。24,468 是按“迹着色—覆盖候选对”
计的出现次数，372 是保留覆盖对方向并压缩其余迹多重集后的规范类数；
它们都不是完整标号解数。

这些有限对象没有配置共同 \(R\) 上的统一商标签、实际高度、各
\(D_{EF}\) 的联合和值、全部自动短块、长补原子内部子集和、完整 Hasse
行或 \(Z\) 的实际原子性。因此不能推出任一 incidence 幸存者可满足
统一标签，不能推出三个强制 packing 型中任一型可实现或为空，也不能
关闭大素数唯一尾分支，更不能推出 \(A_p\)。证明与报告均明确保持了
这条停止线。

FINAL VERDICT: **CORRECT**
