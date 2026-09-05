# 有限核心：独立验证索引

STATUS: CORRECT（带明确范围的完整有限整数计算）。报告位于 ../proofs/verify_finite_cores_fresh.md。

- 五三重五核、A/B共10树，全量独立复跑通过。
- 四独立三重34根、656175节点，全量独立复跑通过。
- 332核心113根、20707001节点，分阶段全量独立复跑通过；最终合并证据 ../evidence/verify_finite_332_resumed.json 的状态为 FULL_INDEPENDENT_REPLAY_PASS。

首次240秒中断日志仍以INCOMPLETE_DEADLINE保留；它不代表最终合并状态，也未被删除或篡改。独立验证使用精确长度位集合，没有从原最短距离程序导入DP。此为有限计算认证，非完整Lean认证，亦非完整端点A/B认证。
