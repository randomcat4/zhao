# 非空共同核强制出的互补短 packing 块：全新独立审计

STATUS: **CORRECT**

## 1. 审计对象与冻结范围

本审计只认证以下三个作者工件所陈述的局部结论：

- `proofs/unique_tail_forced_short_packing_block.md`；
- `unique_tail_forced_short_packing_block.py`；
- `unique_tail_forced_short_packing_block_report.json`。

适用范围严格限于两个三点唯一尾参数

\[
(p,\ell,b,r)=(233,7,4,3),\qquad(1399,8,5,3),
\]

以及三个强制共同余部原子型

\[
(3),\qquad(1,2),\qquad(1,1,1).
\]

核验只调用已冻结的共同实际位置分解、已审计的 \(K\ne\varnothing\)、
短谱、商零中间禁区及唯一正核心 \(F_3\) 接口，不引入实际高度、Hasse
方程或长补原子的额外内部结构。

## 2. 上游接口与实际互补块

上游共同分解在同一实际位置集上给出

\[
X=x^{p-4},\qquad Z=X\mathbin{\dot\cup}Y,\qquad |Z|=3p+4,
\]

\[
Y=L\mathbin{\dot\cup}R,\qquad
R=P_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}P_t
\mathbin{\dot\cup}K.
\]

三个目标型都有 \(t\ge1\)，每个 \(P_i\) 是非空的实际位置块；同时

\[
\bar\sigma(P_1\dot\cup\cdots\dot\cup P_t)=3q,
\qquad
\bar\sigma(K\dot\cup L)=q,
\]

\[
U\subseteq L,\qquad |U|=3,qquad
\bar\sigma(U)=-bq,qquad q\ne0.
\]

从 \(X\) 取 \(b-3\) 个实际位置为 \(X_D\)，令
\(X_B=X\setminus X_D\)。于是

\[
|X_B|=p-b-1.
\]

目标证明定义

\[
D=X_D\mathbin{\dot\cup}U
  \mathbin{\dot\cup}P_1\mathbin{\dot\cup}\cdots
  \mathbin{\dot\cup}P_t,
\]

\[
B=X_B\mathbin{\dot\cup}K\mathbin{\dot\cup}(L\setminus U).
\]

这些并确为实际位置不交并：\(X\cap Y=\varnothing\)，
\(U\subseteq L\)，而 \(K,P_i\subseteq R=Y\setminus L\)，且共同分解
中的 \(P_i,K\) 两两不交。因此逐位置恰有

\[
\boxed{Z=D\mathbin{\dot\cup}B}.
\]

商和值也逐项闭合：

\[
\bar\sigma(D)=(b-3)q-bq+3q=0,
\]

\[
\begin{aligned}
\bar\sigma(B)
&=(p-b-1)q+\bar\sigma(K)+\bar\sigma(L)-\bar\sigma(U)\\
&=(p-b-1)q+q+bq=pq=0.
\end{aligned}
\]

后一式正确使用的是 \(\bar\sigma(K\dot\cup L)=q\)，不是把该和误写
为零；从 \(L\) 删除 \(U\) 所贡献的 \(+bq\) 也没有遗漏。

## 3. 双侧禁窗与错误正核心门

已审计的非空共同核结论给出 \(|K|\ge1\)，而 \(L\) 含至少一个长度
六至八的端点，故 \(|L|\ge6\)。因此

\[
|B|=(p-b-1)+|K|+(|L|-3)\ge p-b+3.
\]

两个参数下右端分别为 \(232\) 与 \(1397\)，均严格大于八。由于
\(B\) 是商零实际块，冻结禁窗 \([9,2p+2]\) 迫使
\(|B|\ge2p+3\)。再由 \(|D|+|B|=3p+4\)，

\[
|D|\le p+1.
\]

若 \(|D|\ge9\)，则商零块 \(D\) 落入短段禁窗 \([9,p+1]\)，矛盾；
所以 \(|D|\le8\)。这里确实同时使用了短段与中间段，且禁窗的作用
对象始终是 \(Z\) 的实际位置子块。

若 \(|D|=8\)，冻结 (SQ) 迫使它属于 \(F_3\)。但它有正核心数
\(b-3\ne b\)，尾为

\[
U\mathbin{\dot\cup}P_1\mathbin{\dot\cup}\cdots
\mathbin{\dot\cup}P_t,
\]

而 \(t\ge1\) 且每个 \(P_i\ne\varnothing\)，故该尾也不等于 \(U\)。
这与正核心 \(F_3\) 只能是唯一核心—尾对 \((b,U)\) 矛盾，从而

\[
\boxed{|D|\le7}.
\]

同一唯一性还排除了当前 \(D\) 在长度六或七时属于 \(F_3\) 的可能。
因此长度五、六时其实际和系数只能为 \(1\) 或 \(2\)，长度七时只能
为 \(2\)。实际高度是在得到商零与短长度后由 (SQ) 被动确定，证明
没有预先输入高度或使用 Hasse 系统。

## 4. 尺寸界、十个向量与两个边界结论

令 \(n_i=|P_i|\ge1\)、\(N=\sum_i n_i\)。由实际不交并直接得到

\[
|D|=(b-3)+3+N=b+N,
\]

故

\[
\boxed{N\le7-b}.
\]

不导入作者模块的替代枚举按正整数 \(n_i\) 穷举；相同轴系数的原子
只保留非降序尺寸，不同轴系数的原子保留次序。所得十个且仅十个
幸存向量为

\[
\begin{array}{c|c|c}
(p,b)&\text{packing 型}&(n_i)\\ \hline
(233,4)&(3)&(1),(2),(3)\\
&(1,2)&(1,1),(1,2),(2,1)\\
&(1,1,1)&(1,1,1)\\ \hline
(1399,5)&(3)&(1),(2)\\
&(1,2)&(1,1)\\
&(1,1,1)&\varnothing
\end{array}
\]

逐向量重算的 \(|D|\)、\(|B|\)、允许实际和系数与报告完全一致。
特别地：

1. \(p=1399\) 的 \((1,1,1)\) 型要求三个非空原子，故 \(N\ge3\)，
   与 \(N\le2\) 精确矛盾；该型确为 UNSAT。
2. \(p=233\) 的 \((1,1,1)\) 型只能有
   \((n_1,n_2,n_3)=(1,1,1)\)，且 \(|D|=7\)、
   \(D\in F_2\)、\(\sigma(D)=2a\)。这没有证明该型为空。
3. \(p=1399\) 的 \((1,2)\) 型只能有 \((n_1,n_2)=(1,1)\)，且
   \(|D|=7\)、\(D\in F_2\)、\(\sigma(D)=2a\)。这同样只是必要条件。

## 5. 共同核下界

由 \(Y=L\dot\cup P_1\dot\cup\cdots\dot\cup P_t\dot\cup K\)，

\[
|K|=2p+8-|L|-N.
\]

代入上游 \(|L|\le52\) 与 \(N\le7-b\)，得到统一下界

\[
\boxed{|K|\ge2p+8-52-(7-b)=2p+b-51}.
\]

又因 \(K\) 在 \(C_p^2\) 中投影零和自由，Davenport 上界给
\(|K|\le2p-2\)。数值范围因此为

\[
(p,b)=(233,4):\ 419\le|K|\le464,
\]

\[
(p,b)=(1399,5):\ 2752\le|K|\le2796.
\]

逐尺寸向量的更强下界 \(|K|\ge2p-44-N\) 也与报告每一行一致。

## 6. 独立枚举、脚本回归与证书

替代核验器没有导入作者模块，并独立完成以下计算：

- 对每个参数穷举全部正互补长度 \(1\le|D|<3p+4\)，施加
  \(|B|>8\) 与两侧禁窗，只留下 \(|D|=1,\ldots,8\)；
- 独立应用唯一正核心门删除长度八；
- 穷举三个 packing 型的正整数尺寸向量并施加 \(N\le7-b\)，得到
  上述十个向量；
- 对每一行重算 \(|D|\)、\(|B|\)、短块族必要实际和、\(K\) 上下界
  及由 \(|K|\le2p-2\) 导出的 \(|L|\) 最小值。

独立生成的两个 `cases` 对象与报告逐字段相同。另在内存中执行作者
脚本的 `build_report()`，所得完整对象与存档 JSON 完全相同，未重写
作者报告。

移除顶层 `certificate_sha256` 后，按 UTF-8、排序键和紧凑分隔符重新
规范序列化，得到

\[
\mathtt{bc44e4961893a6c731cd18a4e35f8542ee21f0b8517f18b35a6760bfb3e1d39f},
\]

与报告证书一致；报告列出的五个依赖 SHA 也均与磁盘字节一致。

审计时冻结文件 SHA-256：

```text
d3e25042ff486ed0663d896601457a5fcc3930f3938f5d05364d769270411d27  unique_tail_forced_short_packing_block.py
5d8a3f1b434a4b85581afa5416b71b2e5120a81c35edd6c6a984b27d3e5173ad  unique_tail_forced_short_packing_block_report.json
f3c03628690b5b88a4252e3a4347e2b5fa0436dc2a1c52d8eed1398f3e1feddc  proofs/unique_tail_forced_short_packing_block.md
edda3f792101e205332f860d7baeaebf0810e3642527c41ad84515264e3e7e64  proofs/unique_tail_forced_kernel_nonempty.md
1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942  proofs/unique_tail_common_R_next.md
60384c64dee88487220f3fd7101a5d3abff1cb576fe3a8b43ec398fdd284ddce  proofs/unique_tail_labelled_position_next.md
1cf95ee7bc431549108ee432955e21cd15ee58e00ba7ba5b05a0d96916d80b9d  proofs/unique_tail_seven_type_full_f3.md
d886a84857cd430455558266a2ab175f21f2de853eed08c6affcad0c14b3efcc  proofs/middle_quotient_gap.md
0e10138860269a18f0f7c0a02ab40204109efbb9a09688fc99da46983e390aed  assumptions.md
```

## 7. 精确停止线

本结论只给出三个强制型中的短 packing 尺寸必要条件，删除
\(p=1399\) 的 \((1,1,1)\) 型，并固定两条边界 \(F_2\) 情形及共同核
下界。它没有证明 \(p=233\) 的 \((1,1,1)\) 型为空，没有证明任一
\((3)\) 或 \((1,2)\) 型为空，没有关闭全部三个强制型或其余四个
packing 型，也没有关闭唯一尾分支或证明 \(A_p\)。表中幸存向量只是
必要尺寸向量，不是完整标号 SAT 或可实现性证书；实际高度、Hasse
方程、额外 \(q\)-标签排除和长补内部结构均未加入。作者证明、脚本与
报告的停止线一致，没有发生上述过度外推。

FINAL VERDICT: **CORRECT**
