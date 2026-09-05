# 本轮本机重放记录

日期：2026-09-05

本文件只记录本轮在当前仓库副本上的实际重放；数学范围以相邻审核报告为准。

## 三重值统一定理

独立接口检查器退出零，主要计数为：

```text
INDEPENDENT_AUDIT: PASS
signed_identity_subsets=294912
deletion_actual_rows=11232
graphs_n7=2097152; counterexamples=0
partitions=385
anchor_rows=50; split_rows=19
```

## 平方自由 L15 分支

证明算术检查器与独立结构计数器均退出零。结构计数的精确分母为：

```text
860662922414727068051994283870582495183777624400448
```

Gray-code 负控检查了 2,097,152 个子集；冻结模型含短零和及 238 个完整 \(C_7\) 块，正确判为不是候选反例。

## 仅双重值统一定理

仓库模式检查器在避免并发写同一 JSON 后顺序重放通过：

```text
REPOSITORY_FINITE_INTERFACE_CHECK_PASS
manifest_files=9
deleted_position_records=8400
n15_branches=5
```

两个辅助检查器分别输出：

```text
ARITHMETIC_AUDIT_OK
POSITIONAL_AUDIT_OK
```

机器可读结果保存为 `double_only_repo_check.json`。

## 平方自由投影证书

独立标准库检查器由主审再次完整运行，退出码为 0。它实际重算：

```text
raw_checked=11931
R_values_recomputed=214758
projective_functional_representatives=156
independent_unordered_pair_count_checked=193440
positive_profile_count=0
maximum_P=0
K=-978253109306
```

完整机器可读输出为 `projection_recheck.json`。

## 稠密纤维第二路线

下列快速检查在当前提交通过：

```text
verify_farkas.py: 9590/9590 profiles; min score 0; rhs -2844400
audit_interfaces.py: 3125 residue tuples; 7547 deletion sets; 9364 equations
audit_legacy_models.py: PASS
```

`negative_controls.py` 因 PR 包漏交 `rank3_roots.txt` 而失败。完整补救重放移至 GitHub Actions 33987370459；其状态单独记录，不把快速检查外推为整条有限搜索通过。
