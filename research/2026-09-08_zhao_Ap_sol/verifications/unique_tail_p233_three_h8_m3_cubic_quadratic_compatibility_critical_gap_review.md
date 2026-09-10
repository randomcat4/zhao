# 三次核—二次兼容性初稿独立审计

STATUS: **CRITICAL_GAPS / OVERCLAIM WITHDRAWN**

审计绑定：

- 初稿 proof SHA-256：
  `467adf6ab6e1a85291708d0bd833ce22cfb7a47898994a619d357bb1fc0814ba`
- 初稿 script SHA-256：
  `b0dab3d5319c8d06932abdd4ecbc52e7adf20181ba1772667f923b09375837b3`

## 判定

初稿关于有限差分与固定域求交的计算正确，但其关键量词错误，不能
推出 \(m=3\) 层为空。

既有结果只证明：若某个端点 \(i\) 的 \(s,-s\) 两个避尾普通表示族
都为空，则必要地

\[
n_i(s)=n_i(-s)=0.
\]

`unique_tail_p233_three_h8_quadratic_joint_boundary.md` 只分类三个端点
碰巧同时满足上述六零式的形式支，并未证明所有剩余 outer rows 都
必须落入该支。既有 `unique_tail_p233_mixed_height_exchange.md` 还
明确保留真实 \(2\leftrightarrow1\) 交换和单点／双尾横截支。

461-completion 也不能补上这个缺口：它只选择一个端点并控制普通覆盖；
其中 complete 的序列是

\[
B_i=C\mathbin{\dot\cup}\{u_j,u_k\},
\]

而二次式来自

\[
N_i=C\mathbin{\dot\cup}\{v_i\}.
\]

前者的 complete 性不蕴含 \(n_i(\pm s)=0\)，更不蕴含另外两个端点
也同时为零。

## 通过的部分

独立审计确认：

1. \(N_i=C\dot\cup\{v_i\}\) 的实际位置量词正确；
2. 生成积严格给
   \(n_i(r)=c(r)-c(r-w_i-\delta)\)，符号正确；
3. 三个 \(n_i\) 确属对应尾基下的 canonical quadratic 族；
4. 曲线恰有 234 点，全部分母非零，eligible 有向方向恰有 53,592 个；
5. 独立方法把六零式的奇部化为三行二列线性系统，在全部 234 个
   曲线点上秩均为二，故 simultaneous-six-zero 子支确实为空。

因此可保留的严格结论只有

\[
\text{曲线条件}+\text{eligible }s+
[n_i(\pm s)=0\ \forall i]\Longrightarrow\bot.
\]

它不能删除 114 个 pointed generic 候选。修订稿已经撤回该过强结论，
并把正确计算改写为真实表示与交换支的 reduction；修订稿必须另行
独立审计。
