# 替代 incidence 证书的独立实现复核

STATUS: **EXECUTABLE REPLAY PASSED /**
**FINITE-FIELD AND INCIDENCE SCOPE ONLY /**
**SUPERSEDED FOR GLOBAL CLOSURE BY \(O=L\setminus U\) /**
**FRESH-CONTEXT MATHEMATICAL REVIEW STILL WELCOME**

## 复核隔离

`unique_tail_cover_projection_incidence_search_verify.py` 不导入搜索器，
也不导入 `unique_tail_cover_unified_projection_labels.py`。它独立实现：

- 11 幅四边图的迹着色与规范覆盖类去重；
- \(\mathbb F_{233}\)、\(\mathbb F_{1399}\) 上的行最简形、秩、仿射
  一致性和行空间成员判定；
- 全部 26 个单位形式的实际指标与长度门；
- 全部非空端点子族及 \(m=0,\ldots,k\) 的稠密门；
- 每个 \(Q_E\) 的全部非空真子集，以及每个非覆盖端点交；
- 逐见证、行数组与整份报告的规范 JSON 哈希。

它只调用上游 incidence 构造器来重建“旧固定构造”本身，从而独立
重算目标分母 210；替代见证的验收完全从报告位置掩码开始。

## 实际结果

运行通过并得到：

\[
744=2\times372\text{ 个规范有限域类},
\qquad 420=2\times210\text{ 个替代见证}.
\]

每个有限域中，旧固定骨架的分裂均重算为 210 个受阻类和 162 个
无障碍类。420 份替代见证全部满足：

1. 迹、长度、公共 \(y\)、覆盖并、三片横截和端点互异；
2. 全部单位门和稠密门；
3. 轴坐标仿射一致；
4. 禁用泛函中没有任何一个落入公共方程行空间；
5. 禁用泛函数严格小于 \(p^2\)。

机器报告状态为
`VERIFIED_ALL_420_ALTERNATIVE_INCIDENCE_WITNESSES`。

复核没有编码后来得到的更强普遍身份 \(O=L\setminus U\)。该身份已
关闭轴向覆盖对，所以本复核只认证较弱接口中 420 份有限见证的真伪，
不认证它们是完整分支幸存者，也不让它们继续承重。

## 独审注意点

新的审稿上下文应优先核对以下三项语义，而不是只重跑程序：

1. “三片横截”只要求第三端点横截三片；覆盖端点本身分别是
   \((A\setminus B)\cup(A\cap B)\) 与
   \((B\setminus A)\cup(A\cap B)\)。
2. 覆盖端点交允许投影为轴向；禁用交只包含并不等于 \(L\) 的端点
   对。这与旧统一投影层的口径一致。
3. 联合界只构造两个公共投影坐标，不构造实际高度或共同 \(R\)
   标签；因此“统一投影标签候选”是最大允许结论。
