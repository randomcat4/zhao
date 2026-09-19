# 一般 A_p：本轮结果与重放索引

更新时间：2026-09-19 07:18 UTC。相对于固定提交 `77c51458cdb943495d084ee3bfc82ebf810b3dcf` 的归档输入。

## 已完成的主要条件结论

对所有素数p≥149，若S是长度5p−4、禁止非空实际零和长度≤3p−2的假想反例，并且a恰出现p−4次，写S=a^(p−4)R，则

\[
\boxed{Z_{3p}(R)=0.}
\]

这是整数不存在性。结合原删除正规形，θ=−1。**没有推出σ(R)=0，没有推出h≤p−5，也没有证明一般A_p。**

## 证明依赖

|步骤|证明文件|核验/性质|
|---|---|---|
|归档x_0>0归约为四元块族和两/三叶横截星|源仓库round3—round5|继承输入，p≥149|
|三叶星归约、排除|`three_leaf_general_reduction.md`、`three_leaf_large_prime_exclusion.md`|81种重合结构；9,823个精确有理矛盾证书及残余手证|
|两叶星配对图覆盖数=2，W商群零和自由|`two_leaf_reduction.md`|手证|
|排除单个K_(2,L)|`two_leaf_K2L_exclusion.md`|20,230个整数行组合证书|
|排除双星固定两星心覆盖|`two_leaf_unique_cover_exclusion.md`|4,340,848种路径；独立覆盖、全素数容量检查|
|小星M=2和M=1的完整分型|`two_leaf_small_star_models.md`|手证，保留重合情况|
|排除四个常数边界模型|`two_leaf_small_star_constant_exclusion.md`|四个完整路径目录及全素数容量界|
|排除M=1双活跃末支|`two_leaf_M1_generic_exclusion.md`|72,599,826种路径独立重放；剩余分量全部排除|

精确整数/有理数证书覆盖所有p≥149，不是有限素数未命中的外推。本轮核验尚未经外部独立审稿或形式化内核认证。

## 重放入口

在本目录运行：

```sh
python3 verify_two_active_exact.py
python3 verify_K2L_paths.py
python3 verify_double_star_catalogue.py
python3 verify_double_star_survivors.py
python3 verify_small_star_constant.py
python3 verify_M1_generic_catalogue.py
python3 audit_M1_generic_survivors.py
python3 complete_M1_components.py
```

这些重放程序及所需压缩证书/目录已保存。均使用标准库和精确算术；部分生成器另用SciPy寻找证书，重放不依赖浮点求解器。最后的大目录重放本轮耗时约16分钟。

## 当前开放前沿

`x0_first_long_atom_reduction.md`：从x_0=0强制存在的3p+1原子出发，排除二位置和a的短块，得到四类交叉相交族、固定模计数，以及极长商群最小零和补序列。此模型仍开放。

`x0_mixed_transversal_structure.md`：四族共同二点横截图进一步缩为9种图形、至多5个非孤立位置，附端点实际重数限制。运行 `python3 catalogue_mixed_H.py` 重建有限图形目录；它验证图形覆盖，不排除剩余实际序列实现。

`x0_star_reduction.md`：继续手证排除三角形和两条不交横截边，横截图仅剩一叶、两叶、三叶星。单边两端同值、三叶全部同值亦排除；两同一异的三叶星要求两种叶值投影线性无关。图形目录现在同时记录此前9种与新归约的3种星；计数证明本身尚无形式化内核认证。早先 `x0_star_reduction_PENDING_REVIEW.md` 保留为工作过程快照，以新文件的完整配对图分类和状态为准。

`x0_anchor_shift_multiplicity.md`：相差a的两个实际值若都存在，重数总和≤3且分别≤2；推出三叶星的非星心C/D数量只能为(1,0)或(0,(p−1)/2)。

`x0_projection_fiber_structure.md`：每个非零商群投影纤维最多两种实际值；若有重复且有第二实际值，只能为两份r加一份r±a。单实际值纤维仍允许原有重数界。

`x0_two_leaf_first_reduction.md`：两叶星中非星心B数量m≤3；m>0时两叶投影不同；m=3时进一步得到唯一附加位置及非星心C/D数量二分。以上均为手证的必要条件，剩余星形仍开放。

`Ap_progress_2026-09-19.md` 记录持续进展和截止时间。小素数p<149、其他低高度情形及整个一般A_p仍未完成。
