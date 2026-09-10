# 唯一尾覆盖对的尾外整体禁块：全新独立审计

STATUS: **CORRECT**

## 1. 审计对象、适用域与停止线

本审计只认证以下局部结论及其有限回归：

- `proofs/unique_tail_cover_outside_tail_block.md`；
- `unique_tail_cover_local_quotient_closure.py`；
- `unique_tail_cover_local_quotient_closure_report.json`。

适用域严格固定为

\[
(p,\ell,b,r)=(233,7,4,3),\qquad(1399,8,5,3),
\]

三点唯一尾、三个强制共同余部原子型

\[
(3),\qquad(1,2),\qquad(1,1,1),
\]

以及上游四边端点族。本文认证的是：这三个型中不可能出现不同端点的
轴向交；等价地，交换门中唯一剩余的整体覆盖例外被关闭。

本裁决不关闭端点族，不关闭三个强制 packing 型，不关闭全非轴交分支，
不关闭其余四个 packing 型，也不推出大素数唯一尾分支为空或 \(A_p\)
成立。全局状态仍为 **INCOMPLETE**。

## 2. 上游接口核对

### 2.1 三个强制型确实给共同余部原子

上游固定一个共同外部分解

\[
R=P_1\dot\cup\cdots\dot\cup P_t\dot\cup K
\]

并对每个端点 \(E\) 定义

\[
Q_E=K\dot\cup(L\setminus E).
\]

端点长补的任意投影原子分解，其轴系数型只能是

\[
(1,3),\ (2,2),\ (1,1,2),\ (1,1,1,1).
\]

从中删除共同 packing 型 \((3),(1,2),(1,1,1)\) 后，余部都只剩单因子
型 \((1)\)。因此对这三个型及每个端点，\(Q_E\) 本身确为
\(C_p^2\) 中按实际位置计数的投影零和原子，并且

\[
\bar\sigma(Q_E)=q.
\]

这一结论只在 \(C_p^2=C_p^3/\langle q\rangle\) 投影中使用；证明没有
把它误升格为 \(C_p^4\) 原子性。

### 2.2 交换门的当且仅当完整

对不同端点 \(H,J\)，令

\[
C=H\cap J,\qquad A=H\setminus J,\qquad B=J\setminus H.
\]

端点有相同实际和且都是真实原子 \(Z\) 的真位置子集，故 \(A,B\)
均非空；否则两个不同端点的非空差集会成为 \(Z\) 的实际零和真子集。
若 \(\rho\bar\sigma(C)=0\)，由 \(H=C\dot\cup A\) 得
\(\rho\bar\sigma(A)=0\)，而

\[
\varnothing\ne A\subseteq L\setminus J\subseteq Q_J.
\]

\(Q_J\) 的投影原子性迫使 \(A=Q_J\)。由于左端不含 \(K\) 位置，
这又迫使

\[
K=\varnothing,\qquad L\setminus J=H\setminus J,
\]

即 \(L=H\cup J\)。反向在
\(K=\varnothing,L=H\cup J\) 时有
\(Q_J=L\setminus J=A\)，于是 \(A,H\) 的投影和均为零，故
\(C\) 的投影和为零。两方向均成立，且没有把整个 \(Q_J\) 错当成
被原子性禁止的真子集。

因此上游接口

\[
\rho\bar\sigma(H\cap J)=0
\iff K=\varnothing\text{ 且 }L=H\cup J
\]

可以无附加假设地用于当前三个强制型。

## 3. 尾外整体禁块的逐步验缝

反设出现交换门的轴向整体例外。此时对任一端点 \(E\)，

\[
Q_E=L\setminus E
\]

是实际位置不交差。端点本身满足 \(\bar\sigma(E)=0\)，故

\[
\bar\sigma(L)
=\bar\sigma(E)+\bar\sigma(L\setminus E)
=\bar\sigma(E)+\bar\sigma(Q_E)=q.
\]

唯一尾给出 \(|U|=3\)、\(U\subseteq L\) 与
\(\bar\sigma(U)=-bq\)。因此真实尾外位置块

\[
O=L\setminus U
\]

满足

\[
\bar\sigma(O)=\bar\sigma(L)-\bar\sigma(U)=(b+1)q.
\]

这里没有非空性或真子集漏洞：\(|L|\ge |H|\ge6\)，所以
\(|O|=|L|-3\ge3\)；又 \(U\ne\varnothing\)，故 \(O\subsetneq L\)。
另外 \(q\ne0\) 且 \(b+1\in\{5,6\}<p\)，也独立说明
\(\bar\sigma(O)\ne0\)，所以 \(O\) 不可能是空块。

令

\[
c=p-b-1.
\]

对两个参数分别有 \(c=228,1393\)。由于 \(|X|=p-4\) 且 \(b\ge4\)，

\[
0<c<p-4+1,\qquad c\le p-4,
\]

故可从 \(X=x^{p-4}\) 取 \(c\) 个不同实际位置。于是

\[
B=X_c\dot\cup O\subseteq X\dot\cup Y=Z\subseteq R
\]

是实际位置块，且

\[
\bar\sigma(B)=cq+(b+1)q=pq=0.
\]

它也是真子集：\(|X|-c=b-3\) 分别为一和二，至少还有一个未使用的
\(X\)-位置，所以 \(B\subsetneq Z\)。虽然冻结短商零接口只要求
\(B\ne\varnothing\)，并不要求它是真子集，这项检查仍排除了整体块
偷渡的可能。

轴向覆盖对只能是两个不同双点尾迹；两迹共享一个尾位置，且所有端点
共享同一非轴位置 \(y\)。所以

\[
6\le |L|=|H\cup J|\le8+8-2=14.
\]

不需要额外下界。由此

\[
|B|=p-b-1+(|L|-3)=p-b+|L|-4,
\]

并得到精确范围

\[
\begin{array}{c|c|c}
(p,b)&c&|B|\\ \hline
(233,4)&228&231\le |B|\le239,\\
(1399,5)&1393&1396\le |B|\le1404.
\end{array}
\]

两行均包含于 \([9,2p+2]\)。适用来源必须分成两段：

- \([9,p+1]\) 由冻结 (SQ) 把商零块的实际和压到
  \(\{a,2a,3a\}\)，再由三族短块最大长度八排除；
- \([p+2,2p+2]\) 由长 \(3p+4\) 零和块的中间商零空档排除。

当前 \(B\subseteq Z\subseteq R\)、非空、商和为零且长度不超过
\(2p+2\)，所以两段接口均在其精确量词内。不能把整个区间误称为
一般 middle gap，但其并确为当前分支的连续禁区。因此 \(B\) 给出矛盾。

交换门说明任何不同端点的轴向交都必须进入上述整体例外，而该例外现已
排除；故对所有不同端点

\[
\rho\bar\sigma(H\cap J)\ne0.
\]

该结论对整个轴向覆盖对分支成立，不依赖某个特定 incidence 骨架。

## 4. 作者脚本、报告与独立算术回归

### 4.1 无写入重跑

使用 Python 3.12.14 导入作者脚本并直接调用 `build_report()`，没有调用
写报告的 `main()`。完整重建耗时约 77 秒，得到：

\[
744=372+372
\]

行；两个素数的 372 行均有
`exact_fixed_skeleton_obstruction=true`，且均含尾外整体阻塞。重建值与
存档值的承重字段一致：

```text
rows_sha256 = c799164045bab478834502b500285646ddc230f03a0d70be2aac39a6cbc256fe
certificate_sha256 = 01eb473629b2519e924f8ce6337867edbbdaff49cf05cc05ef01b5ce4d7bec6e
```

逐行从存档 JSON 独立检查 `universal_outside_tail_obstruction`，得到：

\[
\begin{array}{c|c|c|c|c}
p&\#\text{行}&|O|&c&|B|\\ \hline
233&372&9&228&237,\\
1399&372&11&1393&1404.
\end{array}
\]

每行的 `axis_sum=b+1`、`x_core_size=p-b-1`、实际位置名恰为
\(L\setminus U\)，依赖文件 SHA-256 也与报告记录完全一致。脚本把
\(L\) 的每个非空位置子集都扫描；对固定子集，因为
\(0\le c\le p-4<p\)，能闭合轴向和值的 \(X\) 核数至多一个，所以用
`core=(-axis_sum) mod p` 与“枚举每个可用核心”完全等价。

### 4.2 不依赖作者模块的短回归

另用独立的九行整数循环，只输入
\(p,b,6\le|L|\le14,|U|=3,|X|=p-4\)，不导入任何作者模块。它对
每个 \(|L|=6,\ldots,14\) 同时核验：\(O\ne\varnothing\)、
\(O\subsetneq L\)、\(0\le c\le|X|\)、至少一个 \(X\) 位置未使用、
商和模 \(p\) 为零及长度落入禁区。全部通过；更精确地：

```text
p=233:  |L|=6..9 落入 [9,p+1]，|L|=10..14 落入 [p+2,2p+2]
p=1399: |L|=6..10 落入 [9,p+1]，|L|=11..14 落入 [p+2,2p+2]
```

### 4.3 非承重的证书序列化注记

`first_forced_forbidden_total_length_distribution` 在 Python 生成对象中
使用整数键；写成 JSON 后键按规范变成字符串。因此，把存档 JSON 先
解析、删除 `certificate_sha256`、再对读回对象调用同一排序序列化时，
整数键的数值排序变为字符串的字典序排序，所得哈希不是上列证书。直接
从当前作者生成对象重建则稳定复得 `01eb...`，行哈希也稳定复得
`c799...`。这是 JSON round-trip 后键类型丢失造成的自验证包装限制，
不改变任何行、计数或数学结论；需要绑定存档字节时应使用下节给出的
文件 SHA-256。

## 5. 工件 SHA-256 与最终裁决

审计读取版本：

```text
47629698984151f1c79b9b057caa3aa112a7d4a97a736672f391df575e39b55e  proofs/unique_tail_cover_outside_tail_block.md
9008ff0b9646815b51d10adbb3eb56fefc9e7fcc6eeb23ac590ef562673b94fb  unique_tail_cover_local_quotient_closure.py
882bd62729878c15085df6f22190aef3256dbf3d3616bb1c9e28e6ad2fc564e8  unique_tail_cover_local_quotient_closure_report.json
1c805f0c1b2402e50317712cf5f8341e82ba6c882b3ee02ffab7e901f5614942  proofs/unique_tail_common_R_next.md
8b65afeb55a419abe980225d5c19024b80106157f0657055f13d84ccf40aac6c  proofs/unique_tail_forced_common_atoms_attack.md
d886a84857cd430455558266a2ab175f21f2de853eed08c6affcad0c14b3efcc  proofs/middle_quotient_gap.md
0e10138860269a18f0f7c0a02ab40204109efbb9a09688fc99da46983e390aed  assumptions.md
```

审计期间 Git HEAD 为
`77c51458cdb943495d084ee3bfc82ebf810b3dcf`。研究目录没有
`lean-toolchain` 或 Lake 项目；本审计不声称 Lean 机械核验。

最终裁决：**CORRECT**。轴向交的当且仅当、共同余部和值、尾外整体块、
可用 \(X\) 核、真子集与禁窗量词均闭合；不存在需要新增下界或隐藏
原子性假设的关键缺口。认证范围严格止于三个强制型的轴向覆盖分支。
