# (p=233) 共同因子显式商骨架高度排除：全新独立审计

STATUS: **CORRECT**

## 1. 冻结对象与字节绑定

本审计只裁决 `unique_tail_type3_p233_shared_factor_attack.md` 给出的那一个
显式商标签骨架能否抬升为同时满足完整诱导短谱与实际值重数上界
(p-4) 的对象；不把结论推广到其他商标签骨架或整个
(p=233)、型 ((3))、|P|=2 切片。

审计所针对的三个作者文件及 SHA-256 为：

```text
4f12aa5b86e0f6d36ef9362884fcb19ab3d37380c8f39ca8b1b2ee1de43f4b75  proofs/unique_tail_p233_shared_factor_skeleton_rejection.md
17a0066810a62205def47946e7e88ad73b076df4b774e44682aa1a1238c3593a  unique_tail_p233_shared_factor_skeleton_rejection.py
5030ec397ee293e57af1837163f861d043597684f893c2b04d5cff70dd50c764  unique_tail_p233_shared_factor_skeleton_rejection_report.json
```

## 2. 53,361 个自动块的逐位置检查

固定 (X=x^{p-4}) 中四个不同位置组成的 (X_4)。攻击骨架中

\[
K=\{e_2,\ldots,e_{p-1},f_2,\ldots,f_{p-1}\},
\]

故 (e)-位置和 (f)-位置各有 (p-2=231) 个。对每个
((i,j)\in\{2,\ldots,p-1\}^2)，

\[
C_{ij}=X_4\mathbin{\dot\cup}\{d,u_3,e_i,f_j\}
\]

恰有八个不同位置。映射 ((i,j)\mapsto C_{ij}) 是单射：从块中唯一的
(e)-族命名位置和 (f)-族命名位置可分别恢复 (i,j)。所以字面不同
的位置块数恰为

\[
231^2=53\,361.
\]

逐坐标相加给

\[
4q+(q+e+f)+(-5q-2e-2f)+e+f=0.
\]

独立枚举全部 53,361 对索引，得到

```text
unique_literal_blocks = 53361
len8_blocks            = 53361
quotient_zero_blocks   = 53361
```

这里固定一份 (X_4) 已足够；无需再乘以从 (X) 选择四位置的方式数。

## 3. 长度八短谱确实只允许 (3a)

冻结的 (SQ) 接口适用于每个非空、商和为零且长度至多
(2p+2=468) 的位置块。(C_{ij}) 长度为八，故其实际和值先被限制在
({a,2a,3a})。已认证的三个正系数长度窗为

\[
\begin{array}{c|c}
\text{实际和}&\text{允许长度}\\ \hline
a&2\text{--}6\\
2a&4\text{--}7\\
3a&6\text{--}8.
\end{array}
\]

因此长度八排除 (a,2a)，逐块强制

\[
\sigma(C_{ij})=3a.
\]

该步使用的是完整短谱的必要条件，没有把商零误写成实际零和，也没有
把有限枚举当作长度窗的证明。

## 4. 高度方程、秩与解空间

在 (G=\langle a\rangle\oplus\bar G) 中写

\[
h(e_i)=\alpha_i,\qquad h(f_j)=\beta_j.
\]

由于 (X) 是同一个实际值 (x) 的 (p-4) 个位置，每个 (C_{ij})
的高度方程在 \(\mathbb F_{233}\) 中为

\[
\alpha_i+\beta_j
=3-4h_x-h(d)-h(u_3)=:c.
\]

(c) 可为任意域元素。固定 (j_0) 并相减，得到所有
(\alpha_i) 相等；固定 (i_0) 同理得到所有 (\beta_j) 相等。
因而完整解集恰为

\[
\alpha_i=\alpha,\qquad \beta_j=c-\alpha,
\]

只有一个自由参数。

作者保存的星形子系统有 (231+230=461) 行、462 个变量。其行独立性
可直接从唯一坐标看出：除基准行外，每条 (e_i)-星行含一个不在其他
行出现的 \(\alpha_i\) 坐标，每条 (f_j)-星行含一个不在其他行出现的
(\beta_j\) 坐标；这些系数依次归零后只剩非零基准行。因此秩恰为
461。独立构造矩阵并在 \(\mathbb F_{233}\) 上做高斯消元也复得

```text
forcing_rows      = 461
forcing_rank      = 461
solution_dimension = 1
```

## 5. 实际重数矛盾

同一商标签加同一 (a)-高度唯一确定同一个实际 (C_p^4) 值。因此
(e_2,\ldots,e_{p-1}) 是同一实际值的 231 个位置，所有 (f_j) 也
形成另一个 231 重实际值。无论两族是否还与其他位置同值，重数都至少为
231，而冻结分支的实际值重数上界为

\[
p-4=229.
\]

故每一族单独已经超界 (231-229=2)，矛盾成立。

## 6. 高度量词与结论边界

论证未使用攻击文档式 (29) 的特定高度赋值。任意选择
(h_x,h(d),h(u_3)) 只会改变常数 (c)；其他命名位置的高度根本不
进入承重方程。因此它确实覆盖该固定商标签骨架的全部实际高度抬升，
而不只是原先的零高度赋值或若干样本。

反之，证明没有量化其他商标签骨架，也没有证明每个共同因子相容骨架
都含有同样的 (231\times231) 笛卡尔块族。作者正文的
`FIXED_QUOTIENT_SKELETON_REJECTED / GLOBAL_INCOMPLETE`、报告中的
`not_claimed` 以及结尾的停止线一致，均未把结果误称为整个切片 UNSAT
或一般 (A_p) 证明。

## 7. 证书重放

在 Python 3.12.14、UTF-8 模式下运行作者脚本，退出码为零，三个依赖
哈希断言全部通过。脚本输出与保存报告逐字段相同，并复得

```text
status             = FIXED_QUOTIENT_SKELETON_REJECTED__GLOBAL_INCOMPLETE
block_count        = 53361
forcing_rank       = 461
solution_dimension = 1
certificate_sha256 = e811a39bdfc9a502dde5edf651dc528e9f8bcdcf173514fc906ae83926c2d575
```

去掉 `certificate_sha256` 字段后，独立按排序键、紧凑 JSON 编码重算
SHA-256，仍得到
`e811a39bdfc9a502dde5edf651dc528e9f8bcdcf173514fc906ae83926c2d575`。
作者脚本用索引对称性压缩检查而不保存 53,361 条记录；本审计另作上述
全索引枚举及模 233 消元，结果完全一致。

综上，未发现量词弱化、长度窗误用、位置去重失败、秩错误、重数误算或
全局范围越界。最终裁决为 **STATUS: CORRECT**。
