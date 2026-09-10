# \(p=233\) 三长八 singleton 掩码压缩：独立复核

STATUS: **CORRECT / FINAL ARTIFACTS BOUND / GLOBAL INCOMPLETE**

绑定工件：

- 证明 proofs/unique_tail_p233_three_h8_singleton_mask_compression.md，
  SHA-256
  1539a7bc9b7e4f574d6889b137663110fcb6a5b9c35a801634d396dce8e62b03；
- 程序 unique_tail_p233_three_h8_singleton_mask_compression.py，
  SHA-256
  16834f3419e7df895ea6a69597817fe26136ca13305955bda75fe442043576b0。

独立核验确认：

1. 两个八位置 singleton 端点若交七点，两个差片只能分别是各自尾
   位置；端点完整等和随即迫使不同尾标签相等。因此每对端点交至多
   六点。
2. 去掉 \(U,P,y_0\) 后，四元组
   \((n_{12},n_{13},n_{23},n_{123})\) 完整参数化三个 singleton 的
   成员型重数。独立无导入循环复得 \(256/80\)、\(237/73\)、pointed
   147 及 450--461 的全部共同核分布；配套程序的 \(S_3/S_2\) 作用
   正确。
3. \(C_\triangle\) 与三个 fringe 的逐位置分解、共同大小三至十四、
   完整实际等和及 461 定理在共同核/非尾 fringe 上的数量下界均成立。
4. \(m=3\) 层唯一为 \((1,1,1,4)\)。三个 fringe 写成
   \(\{u_j,u_k,v_i\}\)，并有共同平移差 \(\Delta\)。原子性进一步
   强迫 \(\rho(\Delta)\ne0\)；否则任一 fringe 本身就是三位置真
   投影零和。

73 个轨道是匿名位置 membership-count 状态，不是统一标签实现。纯
mask 门不删除剩余 180 行；下一步须在 73 态上加载实际位置标签与
全部原子/删点/短块条件。
