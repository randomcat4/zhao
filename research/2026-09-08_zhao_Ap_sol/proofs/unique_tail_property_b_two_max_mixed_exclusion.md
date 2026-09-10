# Property B 下两条最大原子与第三条近极值原子的混合排除

STATUS: **P233 TWO-MAX MIXED BRANCH EXCLUDED AT THE UNIFIED \(C_p^2\)
ATOM LAYER / TWO-ATOM-ONLY RELAXATION EXPLICITLY FEASIBLE /
PENDING FRESH INDEPENDENT AUDIT / GLOBAL INCOMPLETE**

## 1. 冻结范围与结论

令 \(p=233\)，在

\[
C_p^2=\langle e,f\rangle,
\qquad t=-e-f
\tag{1}
\]

中取三条共享同一位置标签表的序列 \(Q_1,Q_2,Q_3\)。假设：

1. \(Q_1,Q_2\) 是长度 \(2p-1=465\) 的最小零和序列；
2. \(Q_1\) 含尾对 \(\{f,t\}\)，\(Q_2\) 含尾对
   \(\{e,t\}\)；
3. 每个方向只换至多六个位置：
   \(|Q_1\setminus Q_2|,|Q_2\setminus Q_1|\le6\)；
4. \(Q_3\) 是含 \(\{e,f\}\) 的最小零和序列；在目标混合支中
   \(|Q_3|=2p-2=464\)；
5. 存在共同字面位置核
   \(K\subseteq Q_1\cap Q_2\cap Q_3\)，且 \(|K|\ge435\)。

则这些条件不相容：

\[
\boxed{\text{上述统一 }C_{233}^2\text{ 三原子模型不存在。}}
\tag{2}
\]

三条单点迹端点中任意两条长度七、一条长度八时，可用保持
\(e+f+t=0\) 的线性自同构重排三尾，所以 (1) 的编号不失一般性。

外部输入仍只有 Reiher 的定理：每个素数具有 Property B。原始来源
及其与长度 \(2p-1\) 最小零和序列的语义对应，见
`unique_tail_property_b_three_domain_general.md`。特别地，每个
\(Q_i\)（\(i=1,2\)）都有标准支持

\[
\operatorname{supp}(Q_i)\subseteq\{g_i\}\cup L_i,
\qquad
L_i=h_i+\langle g_i\rangle,\quad 0\notin L_i,
\tag{3}
\]

其中 \(g_i\) 恰出现 \(p-1=232\) 次。

## 2. 大共同核把两个重基都送进第三条原子

对 \(i=1,2\)，Property B 重基 \(g_i\) 在 \(Q_i\) 中恰出现
\(p-1=232\) 次。另一方面

\[
|Q_i\setminus K|=|Q_i|-|K|\le465-435=30.
\tag{4}
\]

故无论这三十个外部位置怎样选，\(K\) 中仍至少有

\[
v_{g_i}(K)\ge(p-1)-30=435-p=202
\tag{5}
\]

个标签为 \(g_i\) 的位置。特别地，统一标签条件同时给出

\[
g_1\in\operatorname{supp}(Q_2)\cap\operatorname{supp}(Q_3),
\qquad
g_2\in\operatorname{supp}(Q_1)\cap\operatorname{supp}(Q_3).
\tag{6}
\]

这一步比“每对至多换六位置”更强：本证明实际不需要第 3 条前提，
只用 \(|K|\ge435\) 与统一逐位置标签。

## 3. 两尾对只允许四个重基对

含 \(\{f,t\}\) 的标准支持只有三类基：

\[
g_1=f,\qquad g_1=t,\qquad
g_1=c(t-f)\quad(c\ne0),
\tag{9}
\]

相应仿射线分别为

\[
t+\langle f\rangle,\qquad
f+\langle t\rangle,\qquad
f+\langle t-f\rangle.
\tag{10}
\]

同理，含 \(\{e,t\}\) 的第二个支持只有

\[
g_2=e,\qquad g_2=t,\qquad
g_2=d(t-e)\quad(d\ne0).
\tag{11}
\]

把九类组合逐一代入 (6)，在特征不为 \(2,3\) 时恰余四个重基对：

\[
\begin{array}{c|c|c|c}
 &g_1&g_2&g_1+g_2\\ \hline
\mathrm 0&t&t&2t\\
\mathrm I&t&t-e&2t-e\\
\mathrm {II}&t-f&t&2t-f\\
\mathrm {III}&\dfrac{t-f}{3}&\dfrac{t-e}{3}&t
\end{array}
\tag{12}
\]

配套脚本不是抽样：它分别生成两尾对的全部
\(p+1=234\) 个 Property-B 支持方向，检查全部
\(234^2=54,756\) 对，复得互相支持的重基恰四对，即 (12)。

## 4. 第三条原子立即给出三项或四项真零和

因为 \(Q_3\) 同时含 \(e,f\)，它不能含任何标签为 \(t=-e-f\) 的
位置；否则 \(e,f,t\) 三个位置已经组成非空真零和子序列。

表 (12) 的前三行都有 \(g_1=t\) 或 \(g_2=t\)。由 (5)，相应
重基至少有 \(202\) 个位置已经位于 \(K\subseteq Q_3\)，所以
\(Q_3\) 确实含 \(t\)，立即与上一段矛盾。

最后一行的两个重基不同，且各自在 \(K\) 中至少出现 \(202\) 次。
故 \(Q_3\) 可各取一个 \(g_1,g_2\) 位置，而

\[
e+f+g_1+g_2=e+f+t=0.
\tag{13}
\]

这是长度四的非空真零和子序列，仍与 \(Q_3\) 的原子性矛盾。四种
情形全部关闭，证明 (2)。注意这里甚至没有
使用 \(Q_3\) 的精确长度 \(464\)；只需它是长度大于四的原子并含
\(e,f\)。

## 5. 两条最大原子本身确实相容

不能把上面的结论误写成“两条最大原子已经矛盾”。令

\[
g=t=-e-f,\qquad h=t-e=-2e-f.
\tag{14}
\]

定义

\[
\begin{aligned}
Q_1^{\rm rel}&=g^{p-1}h^{p-2}\,f\,(h+3g),\\
Q_2^{\rm rel}&=h^{p-1}g^{p-2}\,e\,(g+2h).
\end{aligned}
\tag{15}
\]

第一条以 \(g\) 为重基，其余 \(p\) 项都在
\(h+\langle g\rangle\) 上；两项异常系数为 \(-2,3\)，因为

\[
f=h-2g,\qquad (-2)+3=1.
\tag{16}
\]

所以它是标准最大原子。第二条以 \(h\) 为重基，且

\[
e=g-h,\qquad (-1)+2=1,
\tag{17}
\]

故也为标准最大原子。

逐位置把 \(p-2=231\) 个 \(g\) 位置和 \(231\) 个 \(h\) 位置
分别对齐，便得到

\[
|Q_1^{\rm rel}\cap Q_2^{\rm rel}|=462,\qquad
|Q_1^{\rm rel}\setminus Q_2^{\rm rel}|
=|Q_2^{\rm rel}\setminus Q_1^{\rm rel}|=3.
\tag{18}
\]

因此两条最大原子共享 \(435\) 位置的放宽模型不但存在，而且离六换
上限还有余量。程序另外穷尽这两个四支撑多重序列的全部压缩子多重集，
每条都只出现空零和与完整零和，独立核对了最小性。

这个模型不能添加所需的第三条近极值原子：它的任意 \(435\) 位置
共同核必须含许多 \(g=t\) 位置，而含 \(e,f\) 的第三条原子禁止
\(t\)。它也没有声称满足全部自动短谱、\(q\)-提升、混合目标、
Hasse 或实际 \(Z\) 原子。

## 6. 证书与边界

`unique_tail_property_b_two_max_mixed_exclusion.py` 给出的当前语义证书为

```text
615b56257a20220b8850e14cb8e84de919f8a5841331268c74ee392ab4fe2c26
```

- **解析排除：** 两条最大原子、第三条近极值原子、统一共同核与
  六位置近邻的联立在 \(p=233\) 已矛盾。
- **严格放宽 SAT：** 删除第三条原子接口后，式 (15) 是完整统一
  \(C_p^2\) 双原子模型。
- **外部依赖：** Reiher 的全素数 Property B 定理；本文没有重证。
- **未外推：** 没有处理只有一条或零条长度 \(465\) 原子的端点型，
  也没有据此宣布全局 \(A_p\) 完成。
- **审计状态：** 在全新独立审核前保持
  `PENDING FRESH INDEPENDENT AUDIT / GLOBAL INCOMPLETE`。
