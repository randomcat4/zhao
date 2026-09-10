# unique-tail 覆盖固定骨架统一投影标签分类：全新独立审计

STATUS: **CORRECT**

## 1. 审计对象与裁决范围

本审计只认证以下工件所陈述的固定骨架投影层结论：

- `unique_tail_cover_unified_projection_labels.py`；
- `unique_tail_cover_unified_projection_labels_report.json`；
- `proofs/unique_tail_cover_unified_projection_labels.md`；
- 作为 incidence 来源的
  `unique_tail_cover_forbidden_block_generalization.py`、对应报告与证明。

这里的一个规范键是

\[
(p,\tau_H,\tau_J,\operatorname{sort}(\text{其余端点迹}))。
\]

独立枚举得到 372 个有向规范覆盖迹签名；分别放在
\(p=233\) 与 \(p=1399\) 两层后才得到

\[
744=2\cdot372.
\]

每个键只调用上游构造规则选定一个固定实际位置 incidence。因而
“210 个排除”只排除 210 个所选固定骨架，不排除对应迹类的其他
incidence；“162 个幸存”也只是在该固定骨架上满足统一商投影标签层，
不是完整标号 SAT。

## 2. 线性系统与精确强迫零判据

对一个固定骨架，令 \(L\) 有 \(n\) 个实际位置，端点为
\(E_1,\ldots,E_s\)，\(U\) 为三个尾位置。矩阵 \(M\) 的行依次是

\[
1_{E_1},\ldots,1_{E_s},1_U,1_L.
\]

两个非轴坐标 \(r,s\) 满足

\[
Mr=Ms=0,
\]

轴坐标 \(z\) 的右端则精确为

\[
Mz=(\underbrace{0,\ldots,0}_{s\text{ 个}},-b,1)^{\mathsf T},
\qquad b=4\ (p=233),\quad b=5\ (p=1399).
\]

因此每个端点和为 \((0,0,0)\)，\(U\) 和为 \((-b,0,0)\)，
\(L\) 和为 \((1,0,0)\)，并且

\[
Q_i=L\setminus E_i
\quad\Longrightarrow\quad
\sum_{x\in Q_i}(z_x,r_x,s_x)=(1,0,0).
\]

独立实现没有调用作者的 `rref_rows`，而是用按首个非零坐标维护的
有限域增量阶梯基底分别计算 \(M\) 与增广矩阵的秩，并用逐主元消去
测试行空间成员关系。744 个骨架的轴仿射系统全部相容，且逐行复现
报告中的秩、零空间维数及秩—零度分布。

对任意实际位置子集 \(T\subseteq L\)，标准配对下有

\[
\left(\forall v\in\ker M,\ 1_Tv=0\right)
\iff
1_T\in(\ker M)^\perp
=\operatorname{rowspan}M.
\]

这正是“在所有满足共同方程的投影标签下强迫为零”的充要条件，
不是只给出单向障碍。

## 3. 禁止族完整性与并集界

独立重建的禁止族为

\[
\mathcal B=
\{\varnothing\ne T\subsetneq Q_i:1\le i\le s\}
\cup
\{E_i\cap E_j:E_i\cup E_j\ne L\}.
\]

第一部分由每个 \(Q_i\) 的全部非零真子掩码生成，既不含空集也不含
\(Q_i\) 自身；第二部分遍历全部端点对并且只删除覆盖对。所有端点交
均非空。重复实际子集只合并为一个泛函，这不会遗漏坏事件。

若 \(E_i\cup E_j=L\)，则

\[
1_{E_i\cap E_j}=1_{E_i}+1_{E_j}-1_L,
\]

所以覆盖交的两个非轴坐标必为零，恰是允许的轴向例外。其余每个
非覆盖交都进入 \(\mathcal B\)。

独立行空间测试在每个素数上均得到：

\[
\begin{array}{c|r|r}
 &p=233&p=1399\\
\hline
\text{固定骨架数}&372&372\\
\text{有强迫零禁止泛函}&210&210\\
\text{无强迫零禁止泛函}&162&162\\
\text{强迫某个 }Q_i\text{ 真子集的骨架}&210&210\\
\text{强迫某个非覆盖交的骨架}&210&210\\
\min\dim\ker M&2&4\\
\max_{\text{全部 372 骨架}}|\mathcal B|&153&307
\end{array}
\]

所以每个被排除骨架实际上同时命中两类障碍；162 个幸存骨架则两类
都没有行空间命中。

对幸存骨架和每个 \(T\in\mathcal B\)，限制到
\(K=\ker M\) 的泛函 \(v\mapsto1_Tv\) 非零，故对独立均匀的
\(r,s\in K\)，

\[
\Pr(1_Tr=1_Ts=0)=p^{-2}.
\]

不同 \(T\) 的事件无需独立；并集界直接给出

\[
\Pr(\exists T\in\mathcal B:1_Tr=1_Ts=0)
\le |\mathcal B|/p^2<1.
\]

报告的全体骨架上界已经足够：

\[
153<233^2,\qquad307<1399^2.
\]

因此确实存在同一对 \((r,s)\) 同时避开全部 \(Q_i\) 真子集和全部
非覆盖交；这里没有把不同子集分别配标签。

## 4. 规范迹类、固定 incidence 与全量显式标签重放

不导入作者模块的替代枚举从十一幅四边图、六种非空真尾迹重新得到：

\[
\begin{array}{c|r}
\text{合法迹着色}&28,584\\
\text{含不同双点迹覆盖候选的着色}&13,512\\
\text{覆盖候选出现次数}&24,468\\
\text{有向规范覆盖迹签名}&372.
\end{array}
\]

随后按上游证明给出的 \(y,a_0,b_0\) 和两侧共享位置规则，独立重写
候选生成、确定排除与首次可行回溯，对两个素数的 744 个键全部重建
固定 incidence。每行的 `universe_names`、全部
`endpoint_position_indices` 均与存档报告逐项相同；这也确认报告研究的
只是每个迹签名所选的一套 incidence，而不是该迹类的 incidence
全集。

报告中 324 套显式标签（每个素数 162 套）全部逐实际位置重放。检查量
为：

\[
\begin{array}{c|r}
\text{显式标签骨架}&324\\
\text{端点、}U\text{、}L\text{ 方程检查}&2,808\\
\text{逐 }Q_i\text{ 的非空真子集检查}&99,360\\
\text{非覆盖端点交检查}&5,940\\
\text{覆盖交轴向检查}&324.
\end{array}
\]

所有标签值都在 \([0,p-1]^3\)；每个端点、\(U\)、\(L\) 和每个
\(Q_i\) 的三坐标和值均满足上一节方程；每个 \(Q_i\) 的全部非空
真子集的 \((r,s)\) 和非零；每个非覆盖交的 \((r,s)\) 和非零；
每个覆盖交的 \((r,s)\) 和为零。故这些显式对象逐项证明所有
\(Q_i\) 是 \(C_p^2\) 投影零和原子且全部所需非覆盖交非轴。

两个素数的所有幸存行均记录
`deterministic_label_search_attempt = 0`。作为只读来源一致性检查，另在
内存中调用当前作者生成逻辑；所得 744 行对象与存档 JSON 完全相同，
324 个幸存行的尝试集合恰为 \(\{0\}\)。分类裁决本身仍来自前述未
导入作者模块的替代消元与标签全量重放。

## 5. 证书与文件完整性

移除顶层 `certificate_sha256` 后，按脚本指定的 UTF-8、排序键与紧凑
分隔符重新规范序列化，得到

\[
\mathtt{52a6c801db860ee9b83fa50a4625e410e3c22f41f1b3f79eca6e216c1b8b21e0},
\]

与报告相同。`rows` 数组单独重算为

\[
\mathtt{91b05be9b54d9802ef87b89888d6fb4e6f35419bcedbc46e31b9ff0020ce6a87}.
\]

上游 generalization 报告也按其 ASCII 规范重算为

\[
\mathtt{36ed4fe5bbc17e2e7706bc06c02bfc11b85ee321eccd053fad1b77fd2c9e3c10}.
\]

审计时文件字节 SHA-256：

```text
2a5859b50a52058475708926140c6d378a0779714e61988ef866342d4152b58b  unique_tail_cover_unified_projection_labels.py
e00105a51c6bca7566b76d8bf589812fbf3ac36019222aa6dcf73be66f5a8921  unique_tail_cover_unified_projection_labels_report.json
4d44f9cccd2f4f017bd5e43e60d0ec6ee319273cfb895fa0c514b2667e91afb3  proofs/unique_tail_cover_unified_projection_labels.md
f9bda3577fbbdc08da9a9e78b325cab701054855d83b24db70fe50f40a8e884a  unique_tail_cover_forbidden_block_generalization.py
117f8df799b721800813140eb59ba064fd702b0c50349d81e047f8caa864e3d8  unique_tail_cover_forbidden_block_generalization_report.json
7b5a3cbadf006145c51666523a4d2274ae0e9385f098fcbeb850e93bff2f0e1e  proofs/unique_tail_cover_forbidden_block_generalization.md
```

证明文件有五处非关键排版笔误：第 57--59、168 行的 `qquad` 缺少
反斜杠，第 118 行第二个 `sum` 缺少反斜杠。上下文、程序和其余公式
唯一确定其数学含义，不影响本裁决。

## 6. 严格停止线

本结果没有加入实际 \(a\)-高度或 \(Z\) 在 \(C_p^4\) 中的原子性，
没有加入共同 \(R=P_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}P_t\)
及其标签，没有枚举统一标签自动诱导的新短零和块或 Hasse 行，也没有
检查新 \(F_3\) 的长补原子。它既没有关闭 210 个迹类，也没有把 162
个投影幸存提升为完整标号 SAT，更没有关闭任何 packing 型、唯一尾
分支或证明 \(A_p\)。

脚本、报告和证明均明确保留这些排除项及
`TRACE_CLASSES_AND_FULL_LABELLED_INTERFACE_OPEN` / `GLOBAL_INCOMPLETE`
状态，未作上述过度外推。

FINAL VERDICT: **CORRECT**
