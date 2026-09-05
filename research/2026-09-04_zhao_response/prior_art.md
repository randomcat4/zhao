# 本轮文献核查

核查日期：2026-09-04。旧轮详见 ../2026-09-04_zhao_audit/prior_art.md。

## 出版版本更新

Kevin Zhao, Siao Hong, *On zero-sum subsequences over finite abelian groups of length not exceeding a given number*, Colloquium Mathematicum, online 2026-09-01，DOI 10.4064/cm9599-7-2026。

- 原始出版页：https://www.impan.pl/en/publishing-house/journals-and-series/colloquium-mathematicum/online/116530/on-zero-sum-subsequences-over-finite-abelian-groups-of-length-not-exceeding-a-given-number
- 出版PDF：https://www.impan.pl/shop/en/publication/transaction/download/product/116530
- 已下载全文至 proofs/zhao_hong_2026.pdf，正文p29已渲染并人工视觉核查。
- 新猜想6.1保留旧猜想6.2的上半分支。原来另一个猜想6.1的一般等式、下半分支与K等号表述未保留为猜想。不能把旧编号直接用于新版本，也不能称整个问题已撤回。

## [12,5,5]的明确早期记载

N. J. A. Sloane, *Covering Arrays and Intersecting Codes*, J. Combinatorial Designs 1 (1993), 51–63；亦为DIMACS TR93-48。

- 作者书目：https://neilsloane.com/doc/code.html
- 作者原文：https://neilsloane.com/doc/3surj.ps
- 官方档案：https://archive.dimacs.rutgers.edu/TechnicalReports/1993.html
- 已下载作者PostScript、转为PDF并视觉核查。作者稿编号p6（转换后PDF第12页；原文件倒序）明确写“no [12,5,5] linear code exists [6]”。文献[6]为A. E. Brouwer, personal communication。
- 可确认“至少1993年已公开记载”；这里不根据一个私人通信引用推断首次证明年份，也不继续沿用未经核实的“1970年代”断言。
- Sidorenko2020的N(7,5)=11和Grassl表是独立较晚交叉证据。附件证明可称自包含重证；其证明新颖性没有确证。

## 二元渐近上界

L. A. Bassalygo, *New Upper Bounds for Error Correcting Codes*, 1965；俄文原刊1(4),41–44，英译32–35。https://www.mathnet.ru/eng/ppi762 。证明者核查了原版p41–42，式(5),(7),(8)。我们的闭球有限式已独立重证，不依赖OCR。

现代作者教材交叉核对：https://cse.buffalo.edu/faculty/atri/courses/coding-theory/book/chapters/chap8.pdf 。0.49只是为可复核性保留余量的常数，没有声称最优，也没有声称新的编码界。

## “照搬”可能来源（推断，不是作者确认）

- Schmid–Zhuang2010, *On short zero-sum subsequences over p-groups*, Thm1.2与Conj4.1；https://www.math.univ-paris13.fr/~schmid/personal/schmid_18t.pdf 。原预印本讨论猜想时明确引用该文。
- Luo2017, *Short zero-sum sequences over abelian p-groups of large exponent*, Thm1.6；https://arxiv.org/pdf/1608.05157 。p群D≤2exp−1时η=2D−exp。
- 旧适用条件等价于exp≥(D+1)/2，解释了相同半值形式可能如何出现；不能据此断定作者确实由哪一个定理推广，也不能认为经典定理有错。
- Roy–Thangadurai2018及Wang–Zhao2017提供更一般短长度/秩二背景。没有找到允许把特定m或大指数假设直接推广为全部m、全部群的现成定理。

## 未认证的研究状态

C_p^4的两项剩余上界及完整K精确式，本轮没有找到可直接覆盖的文献；只能标记“本轮未解决、文献状态未充分认证”，不能写成经认证的新开放问题。一般二元最优码的困难也不能自动等同于这个特定阈值问题的难度。
