# 三种强制共同余部原子型的非空共同核：全新独立审计

STATUS: **CORRECT**

## 1. 审计对象与精确范围

本审计认证以下三个工件所陈述的子分支定理：

- `proofs/unique_tail_forced_kernel_nonempty.md`；
- `unique_tail_forced_kernel_nonempty.py`；
- `unique_tail_forced_kernel_nonempty_report.json`。

适用范围严格限于两个三点唯一尾参数

\[
(p,\ell,b,r)=(233,7,4,3),\qquad(1399,8,5,3),
\]

以及三个强制共同余部投影原子型

\[
(3),\qquad(1,2),\qquad(1,1,1).
\]

本轮没有使用后续 local closure 工件，也没有假设存在轴向覆盖端点对。

## 2. 上游依赖逐项核对

### 2.1 实际位置集与 \(|L|\le52\)

上游 `unique_tail_four_edge_joint_csp.md` 的构造给出四条共享同一实际
非轴位置 \(y\) 的边，端点集合 \(\mathcal A\) 有四至八个不同端点。
每个端点长度为六至八，含 \(y\) 且至少含一个 \(U\)-位置。因此每个
端点在 \(U\cup\{y\}\) 外至多贡献六个位置，故

\[
L=U\cup\bigcup_{E\in\mathcal A}E,
\qquad
|L|\le3+1+8\cdot6=52.
\]

同一上游还给出 \(X=x^{p-4}\subset Z\)、
\(Y=Z\setminus X\)、\(\bar x=q\ne0\) 以及
\(U\subseteq L\subseteq Y\)。所以 \(X\) 与 \(L\) 的实际位置不交。
由于 \(L\) 含至少一个长度六至八的端点，又有 \(|L|\ge6\)。

### 2.2 强制型余部、端点和与尾和

`unique_tail_common_R_next.md` 与 `unique_tail_seven_type_full_f3.md`
对三个强制型逐端点给出

\[
Q_E=K\mathbin{\dot\cup}(L\setminus E),
\qquad \bar\sigma(Q_E)=q,
\]

其中 \(K\subseteq R=Y\setminus L\) 是共同投影零和自由核。零核心
端点满足 \(\bar\sigma(E)=0\)，唯一尾满足

\[
|U|=3,\qquad \bar\sigma(U)=-bq.
\]

这些都是同一实际位置标签系统中的等式，不是给不同端点独立配置的
边缘和值。

### 2.3 连续禁窗确实适用于本块

当前唯一尾接口已经证明，\(Z\) 中不存在长度

\[
9\le n\le2p+2
\]

的非空商零实际位置块。其中 \([9,p+1]\) 来自完整短谱与三族短块
最大长度八，\([p+2,2p+2]\) 来自 `middle_quotient_gap.md` 的补集与
冻结 (SQ) 论证。目标证明构造的块位于 \(X\cup L\subseteq Z\)，故
正处在该禁窗的定义域内；证明没有把数字 9 错称为一般中间空档的
下端，也没有漏用短段来源。

### 2.4 交换门

`unique_tail_seven_type_full_f3.md` 对任意两个不同端点 \(H,J\) 已证明
双向等价

\[
\rho\bar\sigma(H\cap J)=0
\iff
K=\varnothing\ \text{且}\ L=H\cup J.
\]

该等价对三个强制型的所有不同端点成立，并不要求预先存在覆盖对。

## 3. \(K=\varnothing\) 的矛盾链

反设 \(K=\varnothing\)。对任意端点 \(E\)，余部公式变成

\[
Q_E=L\setminus E,
\qquad L=E\mathbin{\dot\cup}Q_E.
\]

因此

\[
\bar\sigma(L)=\bar\sigma(E)+\bar\sigma(Q_E)=q.
\]

令真实尾外位置块 \(O=L\setminus U\)。由 \(U\subseteq L\)，这是
实际集合差，并且

\[
\bar\sigma(O)=\bar\sigma(L)-\bar\sigma(U)=(b+1)q.
\]

同时

\[
3\le |O|=|L|-3\le49,
\]

所以 \(O\) 非空。

取

\[
c=p-b-1.
\]

两个参数下分别为 \(c=228\) 与 \(c=1393\)，且均满足
\(1\le c\le p-4\)。因此确实能从实际多重位置块 \(X=x^{p-4}\)
中选出 \(c\) 个位置。由于 \(X\cap O=\varnothing\)，

\[
B=X_c\mathbin{\dot\cup}O
\]

是非空、真实且无位置重复的 \(Z\)-子块，而非形式差。其商和为

\[
\bar\sigma(B)=cq+(b+1)q=pq=0.
\]

其长度为

\[
|B|=p-b-1+(|L|-3)=p-b+|L|-4.
\]

由 \(6\le|L|\le52\) 得到精确范围

\[
\begin{array}{c|c|c}
(p,b)&c&|B|\\
\hline
(233,4)&228&231\le|B|\le277\\
(1399,5)&1393&1396\le|B|\le1442.
\end{array}
\]

两段都完全包含于 \([9,2p+2]\)，与上游商零禁窗矛盾。故三个强制型
均有

\[
\boxed{K\ne\varnothing}.
\]

这条论证只需任选一个端点来求 \(\bar\sigma(L)\)，不需要两个端点
形成覆盖。

## 4. 所有不同端点交非轴

对任意不同端点 \(H,J\)，由于已证 \(K\ne\varnothing\)，交换门右端
必假。因此

\[
\boxed{\rho\bar\sigma(H\cap J)\ne0.}
\]

量词覆盖所有不同端点和所有尾迹型；结论不只是排除先前的不同双点迹
覆盖例外。

## 5. 94 行回归与证书

不导入作者脚本的替代实现直接遍历

\[
(p,b)\in\{(233,4),(1399,5)\},
\qquad 6\le|L|\le52.
\]

每个素数有 47 行，共 94 行。逐行独立重算并与报告比较了
\(|O|=|L|-3\)、\(c=p-b-1\)、\(c\le p-4\)、
\((b+1+c)\bmod p=0\)、长度及禁窗成员关系；全部字段一致。当前脚本
在内存中生成的对象也与存档 JSON 完全相同。

移除顶层 `certificate_sha256` 后，按 UTF-8、排序键与紧凑分隔符重新
规范序列化，得到

\[
\mathtt{2ae9da6ab822ad6c9c236d295e2f6a25299ba81dd3f6e2b3915b97ff34e9c2ff},
\]

与报告证书相同。

审计时文件字节 SHA-256：

```text
5b7a16f18165f07a2bc0ed76b97fff369b25ba86f6e0daa174bbef99f1d313d4  unique_tail_forced_kernel_nonempty.py
1d8ac44929ad217d46e514f35de6a092cbe6234bf53c75f39c0ad3f4060d7ff1  unique_tail_forced_kernel_nonempty_report.json
edda3f792101e205332f860d7baeaebf0810e3642527c41ad84515264e3e7e64  proofs/unique_tail_forced_kernel_nonempty.md
87954d09a00aa74d3d43ce7d784deeff325965e61fca80e900d610371260201f  proofs/unique_tail_four_edge_joint_csp.md
1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942  proofs/unique_tail_common_R_next.md
1cf95ee7bc431549108ee432955e21cd15ee58e00ba7ba5b05a0d96916d80b9d  proofs/unique_tail_seven_type_full_f3.md
d886a84857cd430455558266a2ab175f21f2de853eed08c6affcad0c14b3efcc  proofs/middle_quotient_gap.md
a30707af2f6ef04da720a8eb3c1e97b1c7c297eecc67cf6879ff1191ff9afa8b  proofs/unique_tail_position_conflict_frontier.md
```

## 6. 严格停止线

证明只删除三个强制 packing 型中的 \(K=\varnothing\) 子支，并推出
这些型中所有不同端点交非轴。它没有排除 \(K\ne\varnothing\) 子支，
没有关闭三个强制 packing 型，没有触及其余四个 packing 型，也没有
证明 \(A_p\)。脚本、报告和证明均保持
`FORCED_TYPES_REQUIRE_NONEMPTY_COMMON_KERNEL__GLOBAL_INCOMPLETE`，没有作
上述外推。

FINAL VERDICT: **CORRECT**
