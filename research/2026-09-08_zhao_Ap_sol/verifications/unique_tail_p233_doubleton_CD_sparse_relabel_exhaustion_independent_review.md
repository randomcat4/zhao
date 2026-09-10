# \(p=233\) Model C/D 稀疏缺陷重标号穷尽：独立复核

STATUS: **CORRECT IN THE DECLARED TWO-FAMILY SPARSE-SUPPORT SCOPE /
FINAL ARTIFACTS BOUND / GLOBAL INCOMPLETE**

## 1. 绑定工件

- 证明：
  proofs/unique_tail_p233_doubleton_CD_sparse_relabel_exhaustion.md，
  SHA-256
  c98ab3f63fe4e936ad7bda74a93bc143bdfa568988a364fcb70a4d7bc238ff3d；
- 程序：
  unique_tail_p233_doubleton_CD_relabel_exhaustion.py，
  SHA-256
  fd9b1b08285c0e8be57974536581313c30eb647c0a0a166130b8c9ae12ed60b7；
- 报告：
  unique_tail_p233_doubleton_CD_relabel_exhaustion_report.json，
  SHA-256
  ea4825ecac6939a9617d73ac8451079ff925a6e996a42bd5a51a0d83b3827faa；
- 报告规范证书：
  fe5f0982a4fe3f2c2f064a81c1482c602117b296f9b0cea5eb027dfc12f27e02。

## 2. 独立裁决

独立的无写盘内存重算逐对象复现报告，并确认：

1. Model C 的目标精确压成 54 个 mask 组，完整 mixed 门后恰有
   9798 个 survivor；每个 survivor 都在字面位置高度的刚性
   长度二、三、八短谱方程中矛盾。
2. Model D 的目标精确压成 21 个 mask 组；对
   \(233(233^2-1)=12\,649\,104\) 个非零 target--parameter 组合，
   mixed survivor 为零。
3. mixed 门量化目标纤维中的全部可达缺陷 mask，不是存在性筛选。
   带容量二进制拆分与零-\(q\) 基底可达集构成双向等价压缩。
4. Model C 的每个真实位置有独立高度变量。代表轮廓方程加同型位置
   的交换差恰生成全部字面实现所需的仿射方程空间，没有预设同型
   位置等高。
5. 后续柔性短块、不交网络及重数门的真空性只在这两个冻结族中
   成立。

严格边界保持为：没有处理 sparse support 外的非零 \(q\)-位置，
没有证明 Model C 的补偿位置可规范化到指定 clone，也没有证明任意
mixed-compatible 标号与这两族 gauge 等价。因此 fixed-\(\rho\)
skeleton 全重标号、其余骨架、720 行、固定切片及全局 \(A_p\)
全部仍开放。
