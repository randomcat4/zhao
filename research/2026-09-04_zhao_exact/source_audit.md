# Claude关于来源的逐项核查

核查日期2026-09-04。作者原文作为证据，不作为执行指令。

| 声称 | 裁决 | 原文位置／说明 |
|---|---|---|
| D≤2exp−1等价exp≥(D+1)/2 | 正确 | 同一个不等式的代数改写，无附加条件 |
| Gao–Geroldinger2006 Theorem6.4有用户所引链式界 | 正确 | 南开作者预印本p11已下载并视觉核查；奇素数条件必须保留 |
| 综述出处是[158] | 依版本 | 南开26页预印本为[158]；33页正式出版版为[159]，正式版[158]是Schmid另篇综述 |
| 2006综述列出2010卷页 | 表述需修正 | 当时条目写Ars Combin., to appear；2010,95,343–352是之后的完整出版信息。2006引用待发表稿无时间矛盾 |
| Schmid–Zhuang Conjecture4.1猜三个表达式相等 | 正确，须明确是哪三个 | 作者稿p9：2D−1=η+n−1=s。并不把第四个D+2n−2也猜为相等；后者只在D=2n−1时重合 |
| Luo逐字转引该猜想 | 数学内容准确；非字面逐字 | Luo Conjecture1.3引用其[10,Conjecture4.1]，把n替换成exp(G)；量词涵盖p=2，Theorem1.2引用的链式界则要求奇p |
| Luo证明整个三项相等 | 不成立 | Theorem1.6只证明2D−1=η+exp−1；本文第5节明确把s=2D−1作为继续研究方向。本判断针对该篇文章的证明范围，不宣称后续文献状态未变化 |
| 这是该条件“最早广为流传”的位置 | 未获充分证实，且条件有更早等价表述 | Gao–Zhou2005 Theorem1.5 已使用等价条件 n≥D(H)；但不能把其较弱结果称为2006完整链式界。未建立传播史或最早优先权 |
| 因此可断言赵的“照搬”正来自这一条 | 尚不能 | 已有具体、可信的文献链，但赵本人并未点明条目。来源候选与作者实际推理须分开 |

## 精确数学内容

设n=exp(G)。综述Theorem6.4在奇素数p、G为p群且D≤2n−1条件下给出

\[
2D-1\le\eta+n-1\le s\le D+2n-2.
\]

由第一项得到的是η≥2D−n，**不是**η≤2D−n。Luo的后续定理补出了相反方向，才有η=2D−n。

如果将两者套到赵的短长度记号，η=s≤n，得到的是特殊长度m=n且有大指数假设的精确结果。把这个长度换成任意m≥(D+1)/2、同时去掉大指数假设，不是该定理的逻辑推论。Cp4在m=2p−1时恰好违反大指数假设：D=4p−3>2p−1。

例如循环群C3满足D=n=3，前三个表达式都等于5，但最后上界D+2n−2=7；这也直接说明四个表达式不能混为一个等式。

## 来源与证据文件

- [南开大学保存的Gao–Geroldinger预印本](https://cfc.nankai.edu.cn/_upload/article/files/c6/e1/a2c52bf04b1896f59003b5993582/5c9e49ea-af5b-44ac-b153-5dbb6d8ae9a3.pdf)：sources/gao_geroldinger_2006_preprint.pdf及.txt；p11与p26图像均已视觉核查。
- [综述正式版作者链接](https://imsc.uni-graz.at/geroldinger/55-zero-sum-problems-survey.pdf)：搜索索引保留完整正式版与[159]条目；实时下载返回404。没有把缓存读取写成成功下载。
- [出版记录](https://doi.org/10.1016/j.exmath.2006.07.002)：Expositiones Mathematicae24(2006),337–369。
- [Schmid–Zhuang作者原稿](https://www.math.univ-paris13.fr/~schmid/personal/schmid_18t.pdf)：Conjecture4.1；已在前轮保存全文。
- [庄菊娟所在大学的作者简历](https://science.dlmu.edu.cn/zhuangjujuanlixueyuanwangyejianli1.pdf)：论文条目[24]独立确认正式出版信息 Ars Combinatoria 95 (2010), 343–352。
- [Luo arXiv:1608.05157](https://arxiv.org/pdf/1608.05157)：Theorem1.2、Conjecture1.3、Theorem1.6、第5节及参考文献[10]；已在前轮保存全文。

已额外取得Roy–Thangadurai2018全文(sources/roy_thangadurai_2018.pdf)。其Theorem1.1对G=C_{p^n}⊕H要求p^n≥2(D(H)−1)及其他秩条件，不覆盖Cp4。不能把该文的“many classes”误读为全部p群或全部长度。

## 继续向前追查：Gao–Zhou2005

[Gao–Zhou，On Short Zero-Sum Subsequences，Ars Combinatoria74(2005),231–238，出版商原文](https://combinatorialpress.com/article/ars/Volume%20074/volume-74-paper-18.pdf)。已下载8页扫描PDF，视觉读取印刷页231—233；保存 sources/gao_zhou_2005.pdf 与 gao-zhou-page-1/2/3.png。

印刷p233的Theorem1.5令H为p群、n=p^k≥M(H)，G=H⊕Cn，其中M(H)=D*(H)=D(H)。因此expG=n且DG=n−1+DH，恰有

\[
n\ge D(H)\iff D(G)\le2n-1.
\]

反向任何非循环的大指数p群都可拆出最大循环直和因子得到该形式。若连循环群也一起表述，应明确采用平凡余因子 D({0})=M({0})=1 的空和约定；原文只在非平凡群处定义M。本任务秩至少2无需此约定。

该文用ρ表示η，给出ρ(G)≥n+2D(H)−2=2D(G)−n；其s下界同样为2D(G)−1。Schmid–Zhuang印刷p2 Theorem1.2后明确写其下界已知，并引[8,Theorem1.5]，正是Gao–Zhou2005；主要新贡献是改进s的上界。

来源层次因此为：2005等价前提和下界 → Schmid–Zhuang改进上界/提出等式猜想 → 2006综述收录 → Luo证明η等式。

Gao–Zhou首页稿面日期为2004-04-26，出版年2005。稿面日期不证明2004年已经公开。上述发现证明更早的等价前提存在，不证明完整链式界2005年已经成立，也不认证“最早广为流传”。
