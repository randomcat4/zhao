# 一般 `B_p` 线程审计清单

本文件绑定本线程实际生成的本地成果包，并区分：

- **主证明稿**：承担文中声明的全称数学结论；
- **核对程序 / fixtures**：只做有限实现与局部恒等式检查；
- **本地执行结果**：记录一次已完成运行，不承担一般素数量词。

## 本地成果包 SHA-256

以下 SHA-256 来自本线程结束各轮时保存于 `/mnt/data` 的原始文件；它们用于证明来源绑定。GitHub 归档中的文本可能因手工落库、空白或注释规范化而与原始字节哈希不同，因此这些值**不应被误作当前 Git blob SHA**。

| 轮次 | 文件 | 字节 | 本地 SHA-256 |
|---|---|---:|---|
| R1 | `Bp_parameterized_review.md` | 23787 | `35c3097612f34c6a06845d1a16986a9665de90175c7edcd1ca07cf86da2ba7c1` |
| R1 | `verify_bp_candidate.py` | 5854 | `decb0fb4cc2318ee9a785d01b3f016c959233a855280222c5ba91506d4ad5c1e` |
| R1 | `check_local_lemmas.py` | 3564 | `09027b316b7f4a48e1a4820a8eefff12738bb32b4261d114a0494c5da5fe8da4` |
| R1 | `local_checks.json` | 626 | `21b3e5149cd8a87faa400f169d9e980c4d806ad70dc77c8935fa54c1347416b5` |
| R2 | `ROUND2_THEOREMS.md` | 16527 | `a67589afb3d425a28316ba55ccf540c16528f7cc788c63cb400ad9b9035b9954` |
| R2 | `audit_round2.py` | 9571 | `e9f1c5f130134699eb2076616b09ed6d8950187637571962f5ac8b89d43bca56` |
| R2 | `audit_results.json` | 39694 | `600e7494f7324bbd3914e8df6dfcf4a81fffd2b3cb88238c0e27e1522867d5dc` |
| R3 | `ROUND3_THEOREMS.md` | 19558 | `d54efb76b85b4ae68f0d5c077933e114dd2b694643a47d71ca611c24c325569d` |
| R3 | `audit_round3.py` | 13769 | `d6fd9e39172c8c0cee34ba3704e93bd9ce67ac3f48ab9fb982ee7b7871865b66` |
| R3 | `audit_results.json` | 27197 | `efe61664740663f8d8d66543c139e81928a47d055f83b34c4e4f2021205791c8` |
| R4 | `ROUND4_THEOREMS.md` | 14871 | `8bbfa2f1d0846b5b638e4812be45af9e7b8b019eb7d670e0197c6f3ef30a6837` |
| R4 | `audit_round4.py` | 10755 | `f42d060f5d4d1d6f6be25a39b16d156df760925e48197beacc67919bf5ec0d1c` |
| R4 | `audit_results.json` | 11966 | `74b42f683f323a2f5d07975d9951c10cda3acf47a1b3860cea7042036ea1988e` |
| R4 | `fixtures.json` | 5706 | `e7dc591d99af822aca5990be45e3cf9b4043ab66bebdbb1c690ea617797e22a9` |
| R4 | `INPUT_BINDINGS.json` | 307 | `66f1478ae2a2fb32c449a785294381b2885fa42fb47d8fade5a34262697edd86` |
| R4 | `isolated_replay.json` | 217 | `f4e8c176d8f5889143e4979538e8fd5dc72ad995028acce5665363e8b96f51d4` |

## 实际运行的关键统计

### Round 1

`local_checks.json`：`PASS`，但 endpoint 状态明确为 `NOT_PROVED_NO_COUNTEREXAMPLE`。

- 单位根/三点插值参数：1,577,056；
- 指数多重集相等实例：3,984；
- 近周期轨道：528；
- 三共线容量：252；
- 整数碰撞向量：120；
- 独立小行列式：11,520；
- 独立反例验证器自测：56 个实例。

### Round 2

本地 `audit_results.json`：`PASS`。

- 穷尽 `C_3^2` 中指定五位置多重集：504；其中最大原子 24 个，合法非零外部扩展检查 144 个；
- 秩四明示测试族：12 个；
- 稀疏谱 Vandermonde 矩阵：276 个，覆盖 `p=5,7,11` 的全部正偏移子集；
- 结果只核对 R2 的恒等式实现，不是 `B_p` 搜索。

### Round 3

本地 `audit_results.json`：`PASS`。

- 与 R3.2 结论相违的参数系统：5,643 个，全部精确不相容；
- 六位置简单图：32,768 个全部枚举；
- `p=7` 临界交叉图单独检查；
- 素数 `7..10000` 共 1,226 个，核对最终星计数与深度三补集递推；
- 明示偶原子：8 个；实际和值纤维总计 92,456；
- 不同值删除后的仿射系数函数：112 次；
- 这些数字不是全称证明的替代品。

### Round 4

本地 `audit_results.json`：`PASS_LOCAL_CHECKS_NOT_Bp_PROOF`。

- 明示 `4p-4` 原子共 11 个，检查实际和值纤维 99,659 个；
- 仿射线重数轮廓：`p=5` 时 611 个，`p=7` 时 37,605 个；
- 其中零和自由轮廓分别 185、3,934；没有非空高阶设计；
- 构造 Gram 模型的系数向量：`5^5=3125`、`7^5=16807`、`11^5=161051` 全部核对；
- `isolated_replay.json` 记录：除运行时间外的全部数学字段及输入/脚本绑定一致。

## Round 1 记号勘误

GitHub 归档的 `round1/Bp_parameterized_review.md` §7 定义行目前写成

```tex
\nu_i=\chi(a_i)
```

后文以及原始线程文件均使用 `u_i`。正确读法是

```tex
u_i=\chi(a_i).
```

这是纯记号抄写错误，不改变任何等式或量词。审阅时应按 `u_i` 读取；合并前如需字节级洁净，可直接用本地原始稿 SHA `35c309...` 替换该文件。

## 复现

```bash
cd research/2026-09-05_zhao_general_bp/round1
python verify_bp_candidate.py --self-test
python check_local_lemmas.py

cd ../round2
python audit_round2.py --output audit_results.json

cd ../round3
python audit_round3.py --output audit_results.json

cd ../round4
python audit_round4.py --output audit_results.json
```

Round 2–4 脚本需要 NumPy。`round4/fixtures.json` 是该轮脚本的输入，三条记录都是局部 `4p-4` 原子，不是 `B_7` 反例。

## 当前数学状态

这些审计材料不改变 `THREAD_STATUS.md` 的裁决：一般 `B_p` 仍未闭合；当前最集中、且尚未排除的顶端分支是非空零和长度仅属于 `{3p,4p-4}` 的情形。
