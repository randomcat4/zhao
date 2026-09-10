# 独立审计：\(p=233,m=3\) 共同核纤维恢复与九轨归约

STATUS: **INDEPENDENT REVIEW CORRECT**

## 工件绑定

- proof SHA256:
  `9AD9D159CB516FD890C4130A3FA97E1C809DD7BD5CF1491D9B678FC39B71D88C`
- script SHA256:
  `08B34388492C5B7EBD1AFF80845777A41B17AB6589AA23C2C419E76B7CEEE79B`
- report SHA256:
  `6F231807D87918DDF9550FA112AD01675E75C9207D97C70038460CBEE35C1088`

## 1. 独立实现

审计实现没有调用候选脚本，也没有导入其规范二次型或有限表。它从
全局 \((e,f)\) 坐标重新完成：

1. 枚举 \(\alpha^2-\alpha\beta+\beta^2=3\) 的 234 点，并只删去
   已由独立定理排除的六个 \(\delta=w_j-w_i\)，得到 228 个 generic
   点；
2. 直接评价共同三次式 \(c_\delta(t)\)；
3. 对每点枚举全部 54,282 个 admissible \(s\)，包括 690 个尾线残余；
4. 独立枚举 determinant-kernel 的全部非零缩放；
5. 另写完整 bounded meet-in-the-middle，逐个复验见证的非零性、
   上下界及两个坐标和值；
6. 独立生成尾标号 \(S_3\) 线性作用和 \(s\mapsto-s\) 后重算轨道。

## 2. 数学接口

对

\[
t_{\varepsilon,i}=\varepsilon s-(w_i+\delta)
\]

及任意 \(F\subseteq C\) 满足 \(\rho\sigma(F)=t_{\varepsilon,i}\)，
\(F\dot\cup\{v_i\}\subseteq N_i\) 是 mixed 目标 \(\varepsilon s\) 的
表示。逐表示 separator 给 \(|F|+1\le2\)，所以指定目标的 signed
系数已穷尽为 empty/singleton 贡献：

\[
A_{\varepsilon,i}
\equiv-c_\delta(t_{\varepsilon,i})
+\mathbf1_{t_{\varepsilon,i}=0}pmod {233}.
\]

高度表逐个作用于每个 singleton \(F\)，使同一投影纤维中的位置具有
同一完整标签。实际值重数界给 \(0\le A\le229\)，故 230--232 的
剩余类严格不可能。相同投影标签先合并，容量按 unique 标签计：

\[
\sum_tA_t\le461.
\]

若非零整数向量满足

\[
0\le k_t\le A_t,
\qquad\sum_tk_tt=0,
\]

就能从互不相交的字面纤维中实际取出这些位置，得到 \(C\) 内非空
投影零和子序列。故三纤维门和最终 bounded subset-sum 的排除方向
均正确。重复标签、零标签 \(A=0\)、秩一关系和 empty--empty 配对均
已单独处理。

## 3. 独立复算结果

完整作用域为

\[
228\cdot54\,282=12\,376\,296.
\]

独立复得

\[
12\,376\,296
\longrightarrow11\,449\,560
\longrightarrow974\,628
\longrightarrow480
\longrightarrow108.
\]

具体地：

- 余数门排除 926,736；
- unique-fibre 容量门再排除 10,474,932；
- determinant-kernel 门再排除 974,148；
- 完整 bounded subset-sum 再排除 372。

方向分层为

\[
\begin{array}{c|ccc}
&\text{容量门后}&\text{三纤维门后}&\text{最终}\\ \hline
\text{非尾线}&962\,076&468&108\\
\text{尾线残余}&12\,552&12&0.
\end{array}
\]

最终集合恰分成九个互不相交的
\(S_3\times\{\pm1\}\) 轨道，每轨 12 点；九个代表与正文式 (20)
完全一致。228 个 \(\delta\) 中，174 个无幸存者，54 个各有
\(s,-s\) 两个幸存方向。

六个 exceptional \(\delta\) 不应重加，因为它们已由共同 endpoint
核定理独立排除。若孤立运行本门，那六点仍会给 48 个形式幸存；这不
是当前剩余作用域。

## 4. 双交换边界

对最终 108 个形式候选，正负侧的 endpoint 支撑数分布为

\[
\begin{array}{c|rrrrrr}
(\#E_+,\#E_-)&(0,3)&(3,0)&(3,3)&(2,2)&(1,3)&(3,1)\\ \hline
\text{数量}&30&30&24&12&6&6.
\end{array}
\]

所以只有 48 个候选存在同一 endpoint 的正负双交换，其中只有 24 个
在三个 endpoint 都有双交换。其余 60 个不能由该机制继续。

即使存在同端点双交换，新长 463 原子给出的四个缺失投影目标

\[
a_i+s,\quad -s,\quad a_i-s,\quad s
\]

也已包含于原 \(Q_i\) 三位置花瓣的六目标中；普通投影系数层没有新
零点。原 \(Q_i\) 的 460/461-complete 删除覆盖也不能自动继承到新
原子。

## 5. 裁决

审计支持“228 个 generic 曲线点的全部形式对严格缩为 108 个，即九
个未标点轨道；114 个 completion-pointed 轨至多余 27 个”。这些
108 个是必要条件幸存者，不是已构造的完整四维提升。

本结果没有排空 \(m=3\)，没有删除任何 outer row，也不证明固定
\(p=233\) 或全局 \(A_p\)。下一步必须恢复 completion 表示的内部位置
结构、完整高度或自动短块，不能把双交换或普通投影计数继续外推。
