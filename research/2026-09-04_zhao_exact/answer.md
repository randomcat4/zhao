# 来源追查与精确上下界：本轮结果

日期：2026-09-04。核心状态：来源链条已核实；两个非秩二无限族的整个尾曲线已得到匹配公式；Cp4 的精确阈值仍未确定。不能将本报告称为赵原主猜想的全面精确求解。未启动欧拉，未发送作者邮件。

## 1. Claude 的来源声称，哪些准确

令 n=exp(G)。D≤2n−1 与 n≥(D+1)/2 完全等价。[Gao–Geroldinger 2006 综述的作者预印本](https://cfc.nankai.edu.cn/_upload/article/files/c6/e1/a2c52bf04b1896f59003b5993582/5c9e49ea-af5b-44ac-b153-5dbb6d8ae9a3.pdf) Theorem6.4 确有用户引出的链式界，且要求 G 是奇素数 p 的 p 群。

有四个需要写准的细节：

1. [158] 是26页预印本的编号；正式出版版的对应编号为[159]。预印本条目写 to appear；2010年的卷页是后来的出版信息，不能描述成2006年已经写出2010卷页。
2. [Schmid–Zhuang 原文](https://www.math.univ-paris13.fr/~schmid/personal/schmid_18t.pdf) Conjecture4.1 猜的是三个最左表达式相等，即 2D−1=η+n−1=s，并不把最后那个上界 D+2n−2 也猜成相等。
3. [Luo 原文](https://arxiv.org/pdf/1608.05157) Conjecture1.3 明确转述并引用该猜想；Theorem1.6 证明 η=2D−n，涵盖 p=2。这篇文章没有证明整个三个表达式相等，第5节仍在讨论 s 的剩余部分。此处只说明该文覆盖范围，不据此断言2026年的所有后续进展。
4. 还追到了更早的等价前提：[Gao–Zhou2005，Theorem1.5，印刷p233](https://combinatorialpress.com/article/ars/Volume%20074/volume-74-paper-18.pdf) 使用 G=H⊕Cn、n=p^k≥D(H)。因 D(G)=n−1+D(H)，这恰好等价于 D(G)≤2n−1；对本任务非循环p群，反向也直接成立。该文已有 η≥2D−n 的下界；Schmid–Zhuang在Theorem1.2之后明确引用它，并说明自己的新贡献是改进s的上界。因此2006是可靠的综述入口，不能当成这个前提最早出现的证明。也不能把2005的较弱结果说成已有2006那条完整链式界。

尤其要注意不等号方向：综述第一段不等式只给 η≥2D−n；Luo 补出相反方向后才得到等号。

**归属结论：这确实是“半值条件”的具体可信来源链；赵本人是否从此处照搬，以及具体哪一步，仍没有作者的明确确认。** 已有文献得到的是大指数条件下的特定长度 m=n。把 exp(G) 改成任意 m，同时舍弃对群指数的限制，不是合法推论。Cp4（p≥5）满足 D=4p−3>2p−1，根本不在该大指数假设之内。

逐条证据与版本说明见 [source_audit.md](C:/game/gameproject/showa100/math/2026-09-04_zhao_exact/source_audit.md)。

## 2. 真正匹配的上下界：两个非秩二无限族

沿用原定义：K(G) 是最小的 M≥exp(G)，使所有整数 m∈[M,D(G)−1] 均满足 s≤m(G)≤2D(G)−m。

对 r∈{2,3}、4|n、G=C2^r⊕Cn，有

\[
\boxed{D(G)=n+r,\quad s_{\le n+j}(G)=n+2r-j\ (0\le j\le r-1),\quad K(G)=n.}
\]

这两族的群秩分别为3和4，不是此前的秩二例子。允许 n 含奇素因子。

| 群 | 全部尾点的精确值 | 精确阈值 |
|---|---|---|
| C2²⊕Cn，4|n | s≤n=n+4；s≤(n+1)=n+3 | K=n |
| C2³⊕Cn，4|n | s≤n=n+6；s≤(n+1)=n+5；s≤(n+2)=n+4 | K=n |

例如 C2³⊕C4 的 D=7，三个值依次为 10、9、8，K=4；C2³⊕C8 的 D=11，三个值依次为 14、13、12，K=8。

### 下界证书

明确选定直和基 G=〈h1〉⊕…⊕〈hr〉⊕〈e〉，ord(hi)=2，ord(e)=n。对各 j 取

\[
S_j=e^{n-1-j}\prod_{i=1}^{r}h_i(h_i+e),\qquad |S_j|=n+2r-j-1.
\]

任何零和子序列在每个 hi 坐标上必须成对选择。若选 k 对及 x 个 e 项，则其和为 (x+k)e。非空零和迫使 0<x+k<2n，因此 x+k=n。由 x≤n−1−j 得 k≥j+1，所以子序列长度 x+2k=n+k≥n+j+1。故 S_j 没有长度≤n+j的非空零和，给出所需下界。

### 上界逐点闭合

写 n=qb，q=2^a≥4，b 奇。P=C2^r⊕Cq 满足 D(P)=q+r≤2q−1。Luo Theorems2.3/4.1 给 D(G)=n+r、η(G)=n+2r，从而覆盖 j=0。

余下两个尾点来自已核对条件的 [Zhao–Hong 2026](https://doi.org/10.4064/cm9599-7-2026)：Lemma2.1 给 s≤(D−1)=D+1；Theorem1.1 给 s≤(D−2)≤D+2。例外 C2³、C2⁴ 因指数2排除，例外 C2⊕C2t 因秩2排除。这些点已穷尽 r=2,3 的整个尾区间，逐点与上述构造相等。

由此还得到一个直接回答赵渐近问题的结论：固定 r=2 或3，沿4的倍数 n→∞，

\[
K-\frac{D+1}{2}=\frac{n-r-1}{2}\longrightarrow\infty,
\qquad\frac KD\longrightarrow1.
\]

所以即使去掉所有秩二群，普遍的“半值加有界误差”或“半值加o(1)”描述依然不成立。这不是对仅有上分支的出版版猜想的新反例；本节区分 K 等式与单向上界。

完整证明及适用条件见 [alternative_families.md](C:/game/gameproject/showa100/math/2026-09-04_zhao_exact/proofs/alternative_families.md)。这些是已发表定理的合成推论，不声明首创。

## 3. Cp4：确定到三个候选值，仍不冒充解出

前轮已独立核验：p≥5 为素数时，K≥2p，且从2p到D−1的全部尾点仅剩两孔：

\[
A:\quad s_{\le3p-2}(C_p^4)\le5p-4,
\qquad
B:\quad s_{\le3p-1}(C_p^4)\le5p-5.
\]

因此可以把原区间进一步写成

\[
\boxed{K(C_p^4)\in\{2p,3p-1,3p\}.}
\]

若 A、B 均成立，K=2p；若 A 失败而 B 成立，K=3p−1；若 B 失败，K=3p。对应相对半值 (D+1)/2=2p−1 的误差仅可能为1、p、p+1。不能选定其中任何一个作为已知精确值。

最小未闭合参数 p=5 对应

\[
K(C_5^4)\in\{10,14,15\},\quad
s_{\le13}(C_5^4)\stackrel{?}{\le}21,\quad
s_{\le14}(C_5^4)\stackrel{?}{\le}20.
\]

本轮新增的可复核研究信息：

- 标量同余路线已算到完整删除层系统：假想反例的零和计数只能满足 Z(3p)≡1，其余允许长度的计数≡0（模p）；这个形式向量确实满足所有这些同余。因而继续线性组合相同的同余不能补洞。它是该方法的障碍，不是真实反例。
- 结构路线证明反例必须满秩，所有非空零和都是长的极小零和序列。p=5时，支撑至多6的全部情形已由精确计算排除，主实例检查参数化和程序并重跑一致；支撑至少7仍未覆盖。因此不声称已经排除全部反例。

文献核查也未找到可直接补孔的定理；这不等于认证该问题目前开放。具体证明与未完成记录见 [三候选值推论](C:/game/gameproject/showa100/math/2026-09-04_zhao_exact/proofs/rank4_three_values.md)、[同余断点](C:/game/gameproject/showa100/math/2026-09-04_zhao_exact/proofs/algebra.md)、[结构和计算范围](C:/game/gameproject/showa100/math/2026-09-04_zhao_exact/proofs/structural.md)。

另一个接近闭合的族是 C2⁴⊕Cn、8|n：已知 K∈{n,n+2}，恰缺 s≤(n+1)≤n+7。这里同样只报告二择一，不称精确求解。

## 4. 验缝与投入判断

首轮验缝抓到了辅助引理遗漏“直和独立性”的真实字面漏洞：n=2、r=1、e=h1会产生零项。这个反例保留在 [首审报告](C:/game/gameproject/showa100/math/2026-09-04_zhao_exact/verifications/families_fresh.md)。最终陈述 [v3](C:/game/gameproject/showa100/math/2026-09-04_zhao_exact/frozen_theorem_v3.md) 明确直和基，主体两族未改，修订稿已经两份新上下文审查通过：[修订后首审](C:/game/gameproject/showa100/math/2026-09-04_zhao_exact/verifications/families_v3_fresh.md)、[最终精度核查](C:/game/gameproject/showa100/math/2026-09-04_zhao_exact/verifications/final_precision.md)。Lean只实际检查了下界证明的两条自然数算术引理，不代表群论证明和外部文献均已形式化。

**现有证据不足以建议直接启动一次64实例欧拉。** 来源核查和上述精确族已经不需要这种投入；真正值得单独评估的是两个 Cp4 端点。若继续投入，应把交付目标限定为 p=5 的全体证明或一个可复核反例，再据此决定全素数推广。当前没有证据支持承诺成功率、保证精确式 K=2p，或把局部计算包装成全体证明。
