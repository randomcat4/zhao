# \(p=233\) mixed mandatory-core 与短表示门：独立审计

STATUS: **CORRECT**

本审计绑定

proofs/unique_tail_p233_mixed_core_separator.md

的最终 SHA-256

f2a750c04ac30221be0191e1925bae10c12802691e2a2b5ccbfe00e4117b3510。

配套有限回归程序 SHA-256 为
9c9fb6e719e02aa27492f793378ef97f1e9bb46470868d2cd24f25f5510941ee，
报告 SHA-256 为
a00e2a4a23c52d395126d66bcea49bf481281b01dd0ed735883b192ef54d50bd，
规范证书为
7c2516f23974f6f77fd2da3d92d9ec23b5a5627b8254053bddfda5ab4f9dd198。

逐项重推得到：

1. 长度 \(2p-2\) 投影原子的顶积 \(2J\) 保证每个非零目标有实际
   表示。非尾位置 \(x\) 属于目标纤维的 mandatory core，当且仅当
   删去 \(x\) 后该目标消失。因此 461 删点定理严格等价于全部非零
   目标的 mandatory-core 并至多一个位置。
2. 尾锚定构造
   \(D_A=X_{b-e}\dot\cup U\dot\cup A\) 只使用
   \(A\subseteq Y\setminus U\)、商零禁窗与唯一尾；不需要
   \(A\subseteq Q_H\)。所以它可合法用于
   \(A=\{\text{一个 }P\text{ 位置}\}\dot\cup E\)，并给出每个避尾
   mixed 表示 \(|E|\le2\)。
3. 正负目标的两个避尾表示若不交，其并是补原子的非空真投影零子集；
   故两族单点/双点表示交叉相交。若没有避尾表示，则对应纤维必由
   \(Q_i\) 中两个尾位置横截。
4. 对长七 singleton，删两尾积属于 \(I^{2p-3}\)，其系数函数由
   \(c(0)=1,c(-a)=c(-b)=0\) 唯一确定为
   \(c(xa+yb)=1+x+y\)。所以 \(c(s)\) 与 \(c(-s)\) 不会同时为零，
   必强制一个避尾单点/双点表示和一条长度六/七商零块。
5. 对长八 singleton，删两尾积的系数函数是二次函数，四个原子性值
   正确给出

   \[
   c(xa+yb)=1-(x-y)^2+A\,x(x+1)+B\,y(y+1).
   \]

   两个避尾 signed coefficient 同时为零的必要式及
   \(u=0,v=0,u=v\) 的退化分类均正确。零系数没有被反向解释成无
   普通表示。
6. 若 packing 投影 \(s\) 等于任一正负尾标签，整个
   \(Q_i\setminus U\) 已给出巨大避尾 mixed 表示，直接违反全局尾
   锚定。因此六个标签确实排除。

最终裁决为 **CORRECT**。这些门可删除具体统一标签实例；尚无真实
endpoint-label 枚举，所以不据此宣称整条 outer row 或全局
\(A_p\) 已闭合。
