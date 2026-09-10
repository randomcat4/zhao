# \(p=233\) 三长八 \(m=3\) 的 \(U\cup V\) 门：独立复核

STATUS: **CORRECT / FINAL ARTIFACTS BOUND / GLOBAL INCOMPLETE**

绑定工件：

- 证明 proofs/unique_tail_p233_three_h8_m3_UV_short_gate.md，
  SHA-256
  bf91a55d892d84fe99455470e7183676cb6e8db2e71938616d8b58515a842475；
- 程序 unique_tail_p233_three_h8_m3_UV_short_gate.py，
  SHA-256
  7839416689b6534e56a5355d404b8c2a504d6936c5f8632ea5e0878fefa07bb。

独立核验确认：

1. 六位置任意子集的投影和公式正确。按 \(V\)-位置数一、二、三分层
   的有限表逐项复得式 (7)；在核曲线上只有六个
   \(\delta=w_j-w_i\) 例外点。
2. 程序对每个有序 \(i\ne j\) 精确核对唯一额外零和掩码就是
   \(R_{ij}=(U\setminus\{u_j\})\dot\cup\{v_i\}\)，而不只检查长度。
   其余 228 点没有额外 \(U\cup V\) 投影零和；六点组成一个自由
   \(S_3\) 轨道。
3. 对例外点的实际 lift，\(c\le229\) 时所需 \(X_c\) 字面位置确实
   存在。短谱、长禁窗及唯一正核心 \(F_3\) 块逐行给出式 (17)，
   允许对数恰为 \(8+3\cdot233=707\)。
4. 当标出 completion 端点时，例外轨道必须分成三个 pointed 角色；
   证明已明确保留，未把未标点的一个轨道误套到 pointed 问题。
5. 独立重放输出 PASS / 228 / 6 / 1 / 707；最终轴商措辞、正核心块
   类型与 pointed 边界的哈希绑定正确。

该工件本身不删除六点轨道；它给后续加载真实 endpoint 共同核时使用
的精确 lift 门。剩余 180 行与全局 \(A_p\) 仍保持 INCOMPLETE。
