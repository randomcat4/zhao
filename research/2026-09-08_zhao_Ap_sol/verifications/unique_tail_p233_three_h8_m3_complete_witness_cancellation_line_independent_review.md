# \(p=233\) 三长八 \(m=3\) 完成见证：独立复核

STATUS: **CORRECT / FINAL ARTIFACTS BOUND / GLOBAL INCOMPLETE**

绑定工件：

- 证明
  proofs/unique_tail_p233_three_h8_m3_complete_witness_cancellation_line.md，
  SHA-256
  e39e83a4a2497e774a023a8dbb07c4712a983c7185f04be358c4f89d9f2a9167；
- 程序
  unique_tail_p233_three_h8_m3_complete_witness_cancellation_line.py，
  SHA-256
  dd89e4b49e361ebdab883c616eeeef0ef4b8f24ee447a022fc0a00c38da28783。

两次独立审计确认：

1. 若 \(v_i\) 是唯一坏非尾删除，则共同核 \(C\) 的全部 461 个实际
   位置删除都 complete，而
   \(B_i=Q_i\setminus\{v_i\}\) 是长 \(2p-3\) 的非 complete
   零和自由序列；近最大完成二分的 Property-B 支量词适用。
2. 两尾都在仿射线时，重因子引理给
   \(H_3(w_j-w_k)=0\)，但代入核曲线后需要判别式 96 为平方；
   \((6/233)=-1\) 排除此支。
3. 一尾为重项时，\(m=p-3,p-2,p-1\) 的长度、线坐标和总系数分类
   只余两支。加回 \(v_i\) 后两者都化为
   \(g^{p-2}\prod_{t=1}^p(h+a_tg)\)、\(\sum a_t=2\)。
4. 删任一线位置 \(h+a_0g\) 都漏掉非零目标
   \((1-a_0)g-h\)。两个残支的 \(C\) 至少含 \(p-2\) 个线位置，
   与全部 \(C\)-删除 complete 矛盾。因此 \(v_i\) 必 complete，
   坏点若存在只能在 \(C\)。
5. 式 (20) 的代表区间、式 (34) 的非空普通表示族及公共交量词、
   式 (36) 的有限差分符号均已逐项复核。\(B_i\) 的带符号系数唯一
   零集确为
   \(-\delta/2+\langle w_i\rangle\)，恰含 233 个目标。
6. 独立脚本重放输出 PASS / 234 / 0 / 2 / 233；最终投影记号、
   “非零线外”限定和状态页眉的哈希回滚绑定正确。

严格剩余缺口是 cancellation line 上 233 个普通表示与至少 460 个
共同核逐点 complete 删除、统一高度及全短块的相容性；没有宣称删除
一个 \(m=3\) 曲线轨道或关闭全局 \(A_p\)。
