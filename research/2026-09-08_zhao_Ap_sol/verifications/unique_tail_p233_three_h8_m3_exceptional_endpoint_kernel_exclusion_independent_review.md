# \(p=233\) 三长八 \(m=3\) 例外轨排除：独立复核

STATUS: **CORRECT / FINAL ARTIFACTS BOUND / GLOBAL INCOMPLETE**

绑定工件：

- 证明
  proofs/unique_tail_p233_three_h8_m3_exceptional_endpoint_kernel_exclusion.md，
  SHA-256
  44b688e45dd194adfc5bb5b809c79513452995749e78e0376240556523605689；
- 程序
  unique_tail_p233_three_h8_m3_exceptional_endpoint_kernel_exclusion.py，
  SHA-256
  5eb39cb7478b1e3f453d5f9a3f503ad0246b995b506276c093b86c4aaaa9d896。

三次独立审计确认：

1. 五位置共同 endpoint 核
   \(A_0=\{y_0\}\dot\cup A_{123}\) 与 \(U,V\) 的相关位置字面不交；
   三个 endpoint 的完整实际等和严格给
   \(\sigma(A_0)=4x-2\Delta\)。
2. 值 \(2\delta\) 的至多三位置表示分类穷尽：generic 228 点只有
   三个既有 \(E_i\)；六个例外点各多且只多一个
   \(S_{ij}=(U\setminus\{u_i\})\dot\cup\{v_j\}\)。它与
   \(R_{ij}=(U\setminus\{u_j\})\dot\cup\{v_i\}\) 的反向索引已
   严格区分。
3. 对同一
   \(\Theta_{ij}=\sigma(v_i)-\sigma(u_j)=\theta x+\eta a\)，
   八位置块 \(D=A_0\dot\cup S_{ij}\) 的完整和为
   \(-\theta x+(3-\eta)a\)。证明明确没有把 \(D\) 未经闭轴就送入
   短谱，而是加入 \(d\equiv\theta\) 个真实 \(X\)-位置。
4. \(d=0\)、\(1\le d\le229\) 与 \(d=230,231,232\) 三支分别给
   精确允许集 \(\mathcal G_A\)，大小 700；它与已审
   \(U\cup V\) 门的 707 对允许集交为空。
5. 独立脚本重放输出 234→228、39→38、117→114、700/707/0。
   删除作用域是六个曲线点、一个未标点轨道和三个 pointed 角色，
   不删除 outer row。最终页眉的哈希回滚绑定正确。

因此 \(m=3\) 只余 228 个 generic 曲线点、38 个未标点轨道或 114
个 completion-pointed 轨道。剩余 180 行与全局 \(A_p\) 仍为
INCOMPLETE。
