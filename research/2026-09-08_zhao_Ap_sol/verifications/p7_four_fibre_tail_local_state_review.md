# \(p=7\) 四重纤维尾标签路线独立验缝

STATUS: CORRECT_AFTER_FIX

## 1. 裁决

独立审计对象为：

- `proofs/p7_four_fibre_refinement.md`；
- `verify_p7_four_fibre_refinement.py`；
- `verify_p7_four_fibre_induced_labels.py`；
- `proofs/p7_four_fibre_tail_local_state.md`；
- `verify_p7_four_fibre_tail_local_state.py`。

现行结论正确，裁决为 `CORRECT_AFTER_FIX`：

1. 四重商纤维的 29 个高度轨道投影未变。28 个非例外轨道满足
   \(N_6-N_7+N_8=6\pmod7\)；例外轨道 \(0^3 1\) 在禁止全核心
   \(F_3\) 列后，仍强迫 \(b=1,2,3\) 三个含 \(F_3\) 的低迹层。
2. 最初的例外三尾标签候选真实诱导出两个嵌套 \(F_3\) 块及零商交，
   现行 `EXPECTED REJECTION` 正确。
3. 后续 16 位置候选虽通过 44 个合法窗内诱导块的全部 946 个交
   检查，并无非空实际零和子集且满足实际重数上限三，但严格闭包
   发现 31 个非法短商零谱及已指定 \(B=X\dot\cup Q\) 内的 93 个
   非空商零子集。现稿已撤回其 `DISPROVED` 结论并改为
   `REJECTED_AFTER_STRICT_CLOSURE_AUDIT`，这一修正必要且充分。
4. 没有得到例外轨道的带标签正证书；完整 84 标量 CSP、商补原子
   \(B\)、全局 Hasse 设计及 ROUTE-A4 仍未解。

## 2. 29 轨道投影复核

大小四的高度多重集共有 \(\binom{10}{4}=210\) 个。实际值重数至多
三排除七个常值型，剩余 203 个。非零平移不能稳定大小四的多重集，
故平移作用自由，轨道数为

\[
(210-7)/7=29.
\]

脚本继续枚举

\[
2\le\ell\le8,
\qquad1\le b\le\min(4,\ell-1),
\qquad c\in\mathbb F_7,
\]

并对固定星的全部 \(b\)-迹检查相应长度窗。逐位置、逐对、逐三点
系统仍有 \(12+12+4=28\) 行，族别、符号和右端与既有证明一致。

除重放原验证器外，本审计另用独立高斯消元，对每个轨道穷举全部
\(7^3=343\) 个全核心目标三元组。例外 \(0^3 1\) 的 343 个三元组
全部可延拓，故投影为空；其余 28 轨道各恰有 49 个可延拓三元组，
且恰为

\[
n_6-n_7+n_8=6
\]

的全部解。例外轨道的六个低迹目标列仍精确投影为正文 (3) 的三条
关系，选择 \((0,1,0,1,0,1)\) 可延拓为形式 Hasse 解。新增严格
拒绝没有改变这些投影结论。

## 3. 第一个旧候选的碰撞

`verify_p7_four_fibre_induced_labels.py` 对旧候选的全部二至八元子集
重建出

\[
(|F_1|,|F_2|,|F_3|)=(24,125,97).
\]

其中

\[
A=\{x_3,y_0,y_5,y_9\},
\qquad
A'=A\mathbin{\dot\cup}\{y_3,y_4\}
\]

是两个不同 \(F_3\) 块，但 \(A\cap A'=A\) 的商和为零。差集
\(\{y_3,y_4\}\) 的完整实际和本身也为零。因此该碰撞是真实位置
碰撞，不是尾聚合中的重复计数，旧候选必须拒绝。

独立诱导脚本在无碰撞时只打印 `NO_COLLISION` 而仍以零码退出，作为
回归保护略弱；不过 `verify_p7_four_fibre_refinement.py` 对上述具体
两块及零商交使用断言，现行结论仍由失败即非零退出的检查覆盖。

## 4. 16 位置候选中仍正确的有限计算

三个命名尾的和逐坐标为

\[
\sigma(U_1)=(-q,2),\qquad
\sigma(U_2)=(-2q,2),\qquad
\sigma(U_3)=(-3q,2).
\]

它们只在位置 15 命中已指定 \(T\)，该点的商标签非零。位置 4--14
的已指定 \(Q\) 标签均非零且不等于 \(q\)。16 个完整实际值的最大
重数为三。

验证器枚举了全部 \(2^{16}-1=65535\) 个非空位置子集，确实没有
完整实际和为零者。它又穷举每个二至八元子集，把商和为零且高度落入
允许窗者全部重建，得到

\[
(|F_1|,|F_2|,|F_3|)=(0,17,27).
\]

对这 44 个块，程序检查了

\[
\binom{17}{2}=136,
\qquad17\cdot27=459,
\qquad\binom{27}{2}=351
\]

个 \(F_2\)--\(F_2\)、\(F_2\)--\(F_3\)、\(F_3\)--\(F_3\)
块对，合计 \(946=\binom{44}{2}\)。前两类全部交非空，第三类全部
交非空且交集商和非零；\(F_1\)--\(F_3\) 因 \(F_1\) 为空而为空。
独立位掩码重建得到相同块数与零个交约束违规。

这些有限断言本身都正确；候选失败的原因是验证量词原先少了
“所有商零短集必须落入允许窗”以及固定 \(B\) 的商原子性。

## 5. 31 个非法短商零谱

定义

\[
\mathcal I=
\left\{P\subseteq\{0,\ldots,15\}:
1\le |P|\le8,\ \bar\sigma(P)=0,\
h(P)\notin L_{|P|}\right\}.
\tag{1}
\]

本例没有长度一至四的商零子集。独立穷举得到长度至多八的商零子集
总数为 75，其中 44 个落入允许窗，故

\[
|\mathcal I|=75-44=31.
\]

31 个非法子集按 \((|P|,h(P))\) 的精确分布为

\[
\begin{array}{c|rrrrrrrrr}
(|P|,h(P))&(5,5)&(6,4)&(6,5)&(7,1)&(7,4)&(7,5)&(8,2)&(8,4)&(8,5)\\ \hline
\#P&1&7&4&2&7&1&2&6&1
\end{array}.
\]

首个例子是

\[
P_0=\{7,9,11,14,15\},
\qquad |P_0|=5,
\qquad \sigma(P_0)=(0,0,0,5).
\]

长度五只允许高度一或二，故该子集直接违反冻结 (SQ) 与长度窗。
“没有非空实际零和子集”不能排除它，因为它的高度五非零。

## 6. 已指定 \(B\) 内的完整商零分母

按候选指定，位置 0--3 属于 \(X\subset B\)，位置 4--14 属于
\(Q=B\setminus X\)，位置 15 属于 \(T\)。对
\(X\cup Q=\{0,\ldots,14\}\) 的全部非空子集穷举得到

\[
\boxed{
\#\{P\subseteq X\cup Q:P\ne\varnothing,
\bar\sigma(P)=0\}=93.}
\]

按长度的完整分布为

\[
\begin{array}{c|rrrrrrr}
|P|&6&7&8&9&10&11&13\\ \hline
\#P&7&3&4&36&38&4&1
\end{array}.
\]

其中长度至多八者共有 \(7+3+4=14\) 个；恰有 8 个落入允许窗，
即四个 \(F_2\) 块与四个 \(F_3\) 块。另 6 个非法窗子集的分布为

\[
(6,4):1,
\qquad(7,4):2,
\qquad(8,4):3.
\]

例如 \(\{0,1,6,9,11,13\}\) 是商和零、高度二的六项块，完全位于
已指定的 \(B\) 中。追加未赋值位置不能消除任何既有商零真子集，
所以该候选不可能延拓成商原子 \(B\)。

现行证明与验证器已把这两个严格失败写成 `EXPECTED REJECTION`，
不再保留原来的 `DISPROVED_AT_TAIL_LOCAL_INTERFACE`。

## 7. 可复现命令

在研究目录执行：

```powershell
$py = 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py .\verify_p7_four_fibre_refinement.py
& $py .\verify_p7_four_fibre_induced_labels.py
& $py .\verify_p7_four_fibre_tail_local_state.py
```

三条命令均退出零。第三条关键输出为：

```text
ILLEGAL_SHORT_QUOTIENT_ZEROS=31
ASSIGNED_B_QUOTIENT_ZEROS=93 SHORT=14 VALID_WINDOW=8
STATUS rejected by SQ length windows and fixed-B quotient atomicity
```

首个非法谱还可直接复核：

```powershell
& $py -c "import importlib.util as u; s=u.spec_from_file_location('m','verify_p7_four_fibre_tail_local_state.py'); m=u.module_from_spec(s); s.loader.exec_module(m); print(m.subset_sum((7,9,11,14,15)))"
```

输出为 `(0, 0, 0, 5)`。

## 8. 最终边界

- **CORRECT_AFTER_FIX：**29 轨道投影与两个旧局部候选的严格拒绝。
- **有限弱计算仍正确：**16 点候选的 44 个合法窗块、946 个交约束、
  65535 个非空实际子集和重数上限检查。
- **REJECTED：**两个例外三尾标签候选都不是带标签正证书；第二个
  还被 31 个非法短谱和 \(B\) 内 93 个商零子集双重否证。
- **INCOMPLETE：**例外轨道的完整 84 标量 CSP、商原子 \(B\)、全局
  Hasse 设计以及 ROUTE-A4 仍未闭合。
