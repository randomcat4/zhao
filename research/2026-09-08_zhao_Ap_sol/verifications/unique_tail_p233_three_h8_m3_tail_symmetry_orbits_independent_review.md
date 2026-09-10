# \(p=233\) 三长八 \(m=3\) 尾对称轨道：独立复核

STATUS: **CORRECT / FINAL ARTIFACTS BOUND / GLOBAL INCOMPLETE**

绑定工件：

- 证明 proofs/unique_tail_p233_three_h8_m3_tail_symmetry_orbits.md，
  SHA-256
  c698713b4e6d1675fbe3f0b541a2dd646b8d31c6857a919b07cacb6039406431；
- 程序 unique_tail_p233_three_h8_m3_tail_symmetry_orbits.py，
  SHA-256
  495c2bed118f6b964472a9269443c8398a9f403e2db520a22ee9d6e35f0d0e30。

独立核验确认：

1. 这里使用的是整个 \(m=3\) 字面位置子系统的同构重命名：同步置换
   \(u_i,v_i,Q_i\)，并把尾平面上的 \(T_\pi\) 按恒等作用于轴/高度
   方向提升到完整实际群。它保持实际等和、长补原子性、普通零和与
   自动短块；没有把固定标签实例内部的纯参数替换误作对称。
2. 两个生成元在曲线参数上的作用为
   \((\alpha,\beta)\mapsto(\beta,\alpha)\) 与
   \((\alpha,\beta)\mapsto(\beta-\alpha,-\alpha)\)，并保持二次型
   \(X^2-XY+Y^2\)。
3. 三个换位的固定线正是
   \(\alpha=\beta\)、\(\alpha=0\)、\(\beta=0\)。因 3 在
   \(\mathbb F_{233}\) 中非平方，曲线与三线均不交；三循环只有原点
   固定，而原点不在曲线上。因此 234 点分成 39 个自由六点轨道。
4. 标出 complete-deletion 见证端点后，必须把指标一起作用。先归一
   到一个端点后只余无固定点的 \(S_2\) 稳定子，故 pointed 数目是
   \(234/2=117\)，不是 39。
5. 独立脚本重放输出 `PASS / 234 / 39 / 117 / 0`；最终页眉相对已审
   正文的哈希回滚绑定正确。

该结果只是同构去重，不删除轨道。下一步的 461 complete 删除必须在
117 个 pointed 候选上加载；剩余 180 行和全局 \(A_p\) 均保持
**INCOMPLETE**。
