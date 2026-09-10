STATUS: CORRECT

# `unique_tail_biclique_height_cut` 独立对抗审计

审计日期：2026-09-09

## 审计范围与裁决

本审计只把以下三份最终文件作为待验证对象：

- `proofs/unique_tail_biclique_height_cut.md`；
- `unique_tail_biclique_height_cut.py`；
- `unique_tail_biclique_height_cut_report.json`。

结论是 **CORRECT**。这里通过的是条件性的二部积/连通图高度割、(p=233) 的阈值与静态几何、以及单个最大原子的局部边界例。它不证明 `OPEN-RECTANGLE-233`，不判定 exact (p=233) slice 为 SAT 或 UNSAT，也不证明全局 (A_p)。

## 1. 固定基底的完整二部积

设每个块 (C\dot\cup\{u_i,v_j\}) 的实际和都是同一个元素
(lambda a)。固定 (j) 并比较 ((i,j)) 与 ((i',j))，公共的 (C) 和
(v_j) 消去，得到

\[
\gamma(u_i)-\gamma(u_{i'})=0.
\]

所以 (A) 侧的实际标签恒定；固定 (i) 同理得到 (B) 侧恒定。投影到商群即得两侧商标签也分别恒定。论证比较的是位置携带的标签，并未把不同位置误认为同一位置。

## 2. 连通二部图、补全与秩

对连通二部图的每条边写

\[
x_u+y_v=s,
\]

其中 (s) 是固定基底和统一实际轴系数决定的同一元素。沿交替路，相邻两条边相减；每段长二的路分别迫使两个 (A) 顶点标签相等或两个 (B) 顶点标签相等。因此一个连通分量的每一侧都恒定。

把 (B) 侧列乘以 (-1) 后，系数矩阵成为该连通图的定向关联矩阵。若分量两侧顶点集为 (A_0,B_0)，其秩为

\[
|A_0|+|B_0|-1.
\]

生成树的同样多行已经线性无关，常数右端系统因而只有一维自由度。标签恒定后，任意非边 ((u,v)\in A_0\times B_0) 与原边具有相同的商和与实际和；在长度八情形，自动短谱的唯一允许系数又是 (3)。因此只要 exact-slice 系统按统一标签重建这些短块，连通分量确实补成完整二部积。文件没有把这个秩公式错误地用于跨越多个连通分量的整体矩阵。

## 3. (p=233) 重数阈值

实际标签重数上界为

\[
M=p-4=229.
\]

因为高度割分别使每一侧成为同一实际标签，所以任意一侧含 (M+1=230) 个位置就已经违反重数上界；不需要两侧同时达到 230。固定骨架的侧大小 (p-2=231) 因而足够。

## 4. exact-slice 静态几何

按最终文件使用的 exact-slice 接口，选中 (s\in\{4,5,6\}) 个七位置端点 (H_i)，所有 (H_i) 含共同位置 (y)，单点尾迹给出 (U\subseteq\bigcup_iH_i)，故 (L=\bigcup_iH_i)。于是

\[
|L|\le 1+s(7-1)\le37.
\]

又由 (|Y|=474)、(|P|=2)、(K=Y\setminus(P\cup L)) 得

\[
|K|=474-|L|-2\ge435.
\]

对 (Q_i=Y\setminus(P\cup H_i)=K\dot\cup(L\setminus H_i))，有

\[
|Q_i\setminus K|=|L|-7\le30,
\qquad |Q_i|=474-2-7=465.
\]

最后，共同位置 (y\in H_i\cap H_j) 给出

\[
|Q_i\setminus Q_j|=|H_j\setminus H_i|\le6,
\qquad |Q_i\triangle Q_j|\le12.
\]

因此文件列出的四个承重数值 (37,435,30,6) 都是这些 exact-slice 条件的直接推论，没有把它们升级成未证的纤维分类。

## 5. 单个最大 (C_p^2) 原子的边界例

在 (C_p^2=\langle e,f\rangle) 中令

\[
Q=e^{p-1}\prod_{t=1}^{p}(a_te+f),
\qquad \sum_ta_t=1.
\]

其总和为 (((p-1)+1)e+pf=0)。任一零和子序列若取 (k) 个第二族位置，则 (f) 坐标迫使 (k=0) 或 (k=p)。当 (k=0) 时，至多 (p-1) 个 (e) 中只有取零个才可能零和；当 (k=p) 时，(e) 坐标为 (1+r)，其中 (0\le r\le p-1)，故必须 (r=p-1)。所以唯一非空零和子序列是整个 (Q)，它确为长度 (2p-1) 的最大原子。

当 (p=233) 时，取全部域元素一次并把 (0) 替换为第二个 (1)，得到 233 个标量、总和 (1)，第二族最大重数为 2。给 232 个投影为 (e) 的位置分别赋 (q) 坐标 (0,1,\ldots,231)，并令第二族 (q) 坐标全为 0；因为

\[
\sum_{r=0}^{231}r=26796\equiv1\pmod{233},
\]

抬升序列总和恰为 (q)。这 232 个标签彼此不同，第二族只有标量 (1) 重复一次，且两族由 (f) 坐标区分，所以最大精确 (C_{233}^3) 纤维恰为 2。从第二族删除 30 个位置后长度为

\[
465-30=435;
\]

所得 (K_0) 是原子的真子序列，故在 (C_p^2) 中零和自由；其任意抬升在 (C_p^3) 中也零和自由。

这个构造只排除了“从单个 (Q_i) 的最大原子和长核尺寸推出两个大精确纤维”的局部推理。它没有实现三个同时的 (Q_i)、混合目标或全短谱，因此不能充当 exact slice 的相容模型。

## 6. 停止线审计

正文把 `OPEN-RECTANGLE-233` 明列为尚缺结构命题，并在结尾明确列出 `OPEN`、`GLOBAL INCOMPLETE` 与 `NOT CLAIMED`。脚本说明和 JSON 的 `missing_statement`、`not_claimed`、`status` 与此一致。三份文件都没有把该开放矩形命题、首片 UNSAT 或全局 (A_p) 误报为已证。

## 7. 程序、报告与文件完整性

使用工作区 Python 3.12.14 独立运行 `unique_tail_biclique_height_cut.py`，退出码为 0；重生成报告后，三份文件的字节哈希均未改变。独立删除报告中的 `certificate_sha256` 字段，再按 UTF-8、键排序、紧凑分隔符规范化 JSON，得到

```text
39b91428cdc53d814ea762f0b40771ec56b0f1aba7b0ce4c6c56125605203024
```

与报告声明完全一致。程序可被 Python AST 解析，报告可被严格 JSON 解析。三文件均为有效 UTF-8，未发现 NUL 或除换行/回车/制表符以外的 ASCII 控制字符。Markdown 中 `\[`/`\]` 各 22 个，`\begin{array}`/`\end{array}` 各 1 个，花括号计数平衡；未发现明显 LaTeX 分隔符损坏。

最终三文件 SHA-256（按当前字节）：

```text
c99bd797d23494db12b8d29121994d5a7a56e0c94d18c06fb451cf7ee6b6b554  proofs/unique_tail_biclique_height_cut.md
b3b4babacb6014985ba48512841299358b4624c9c2a3b97296142374114e20d2  unique_tail_biclique_height_cut.py
5e3a55b75bdacb9f577a778dda6bb526e40e166607d195ca141d4a25e33f4e36  unique_tail_biclique_height_cut_report.json
```
