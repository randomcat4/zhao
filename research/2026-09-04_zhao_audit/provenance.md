# 来源与分工

- 用户提供：邮件文字、Claude 回应、9页 PDF。
- 主实例：原文和先行工作检索；逐条解释审计；PDF 全页图像核读；复原附录检查程序；另写独立子集动态规划及 Golay 核空间检查；综合报告。
- independent_math_audit：新上下文独立检查附录 A、群族反例、小维阈值表与 Type II 限制。初始未收到 Claude 回答。后续收到主实例提出的秩二群族，独立核对。
- 有限计算：check_certificates.py 是从附件恢复缩进的原程序；independent_certificates.py 为不同算法的独立检查。结果在 independent_results.json。
- 未执行：Claude 声称的658304节点系统型码穷举；附件记载的50万/10万随机搜索；Lean形式化。
- 已知材料不主张新颖性。所有原附件与远端仓库保持原样。
