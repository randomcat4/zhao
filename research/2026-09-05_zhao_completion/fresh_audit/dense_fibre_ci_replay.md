# 稠密纤维路线补救重放

状态：**PASS / NORMAL**

## 运行绑定

- GitHub Actions run：<https://github.com/randomcat4/zhao/actions/runs/33987370459>
- 工作流提交：`3a60099933320e638e20ec27407b57a726c51b6b`
- 运行环境：Ubuntu 24.04 runner，Python 3.12.3，G++ 13.3.0，4 线程
- 工件 ID：`9975793626`
- GitHub 工件摘要：`sha256:4908773b0759180b68da6b69a8daede17d483e9384be88e017be026439e741de`
- 工作流结论：`success`
- 全链耗时：940.641981535 秒

工作流先从已提交的 `generate_roots.cpp` 重建 PR #1 漏交的 `rank3_roots.txt`，得到与执行链所需固定文件逐字节相同的根表，再运行 `run_all.py`。16 个编译、生成、审计、负控、两套搜索和日志核对命令全部返回 0；`execution_report.json` 记录 `exit=NORMAL` 和 `all_commands_exit_zero=true`。

## 完整分母

最终 `verify_logs.py` 重算并核对：

```text
root_denominator=1786
reference_roots_closed=1786
independent_roots_closed=1786
raw_extension_denominator=17972093794219884182340301482
raw_extensions_closed=17972093794219884182340301482
reference_nodes=34000509
independent_nodes=24371246
independent_maximum_depth=12
normalized_rank3_objects=406416
profile_denominator=9590
profile_rhs=-2844400
m_values_total=23253
all_denominators_equal=true
exit=NORMAL
```

参考搜索和独立搜索分别耗时约 534.18 秒与 381.58 秒。根生成器还复得 1,786 个轨道代表和 406,416 个规范化三维对象；所有大小 10、11、12 的残余计数均为零。

## 保存范围

下载的工件保存在 `dense_ci_artifact/`，包括：

- 重建的 `rank3_roots.regenerated.txt`；
- 两套完整逐根搜索日志；
- 每个命令的标准输出、标准错误和退出码；
- `execution_report.json`；
- `verify_logs.log`；
- 本次 runner 生成的五个临时可执行文件。

这些文件补上了原 PR 包缺少根表和逐根日志的复现缺口。`dense_fibre_review.md` 中对原 PR 包的三个批评仍作为历史审计事实保留；在补救工作流成功并保存工件后，稠密纤维路线的当前裁决转为 **CORRECT**。端点 A 同时还有不依赖此搜索的投影证书证明。
