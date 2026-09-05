# `continue_atom16_star_addendum.md` 的 d=3 证据勘误

日期：2026-09-04。

**STATUS: OLD_D3_TABLE_WITHDRAWN；D3_M1_EXCLUSION_REVALIDATED。**

本勘误不修改已经冻结的
`proofs/continue_atom16_star_addendum.md`，只替换其中第 3 节的两行 d=3
搜索计数及其旧证据文件。原附录第 3 节表中的两行均在此正式撤销，
旧文件 `evidence/continue_atom16_star_addendum_d3.json` 不得再作为这两行
计数的证据。修正后，两类仍都在加入第五个 W 位置之前灭绝，所以
原附录的 **d=3、M=1 排除结论仍成立**。本勘误不改变原附录的 d=4
结果，也不把一般 16-atom 分支标为已排除。

## 1. 原证据的精确错误

旧源码 `scripts/continue_atom16_star_addendum_d3.cs` 中，搜索节点计数器
是一个静态可变数组：

```text
static long[] nodes=new long[8];
```

`RunCore` 返回匿名对象时使用了

```text
nodes_by_W_length=nodes
```

而没有复制数组。第一次 `RunCore` 返回的对象因此仍引用这个静态数组。
第二次 `RunCore` 开头执行 `Array.Clear(nodes,...)`，随后把同一数组写成
第二个核心的计数。两个对象直到第二次运行结束后才一起序列化，所以
旧 JSON 的两行 `nodes_by_W_length` 实际引用同一份最终数组，错误地都
显示成第二个核心的行。

这是证据对象所有权错误，不是搜索树把两个核心识别为同一核心。旧表
第一行的数值是假的；第二行数值虽恰好等于第二次运行的真实计数，但
由于旧证据没有保存两个独立快照，本勘误仍整体撤销旧表的两行，再用
修正后的成对证据替换。

冻结旧对象的识别哈希为：

| 旧文件 | SHA-256 |
|---|---|
| `proofs/continue_atom16_star_addendum.md` | `3f6747de90bc560396604ed588c6efa57f01485a4ad3cfb28ad94e7fbaf10e79` |
| `scripts/continue_atom16_star_addendum_d3.cs` | `b7a8e15cbcfa28434522e74e3552582d3fc63c4ce845a4ffa8c9d82fe93c383e` |
| `scripts/continue_atom16_star_addendum_d3.ps1` | `25b466f12556caf6291e2c9446f987b1beb7effeed41f41de4a8160bc0552a54` |
| `evidence/continue_atom16_star_addendum_d3.json` | `44107ff946e70143e887f07cedbfecef663d6b790173b37156b33f1b3695079d` |
| `evidence/continue_atom16_star_addendum_frozen_manifest.json` | `f10b521ac4a9cbb08901a9ba5aeadb657c8d742c985ecae3a96012f04f7d453c` |

## 2. 修正及搜索边界

新源码另存为
`scripts/continue_atom16_star_addendum_d3_fixed.cs`，关键修正是

```text
nodes_by_W_length=(long[])nodes.Clone()
```

因此每次 `RunCore` 返回时都拥有自己的不可别名快照。新脚本没有改写
旧源码或旧证据。

搜索对象仍是原附录的两个十三位置规范核心

```text
VA = x g1^3 y1^3 g2 y2^2 g3 y3^2,
VB = x g1^2 y1^3 g2^2 y2^2 g3 y3^2,
```

其中 `x=e1, y1=e2, y2=e3, y3=e4` 且 `gi=x+yi`。W 长七。
正式搜索施加原证明给出的真实限制：

* W 的值不属于七个已经强制出现的支撑值；
* W 或七值互异，或恰有一个值出现两次；
* 每加入一个位置，都用全部 625 个群和的精确最短子序列长度检查新序列
  是否出现长度至多 14 的非空零和；
* W 按非降编码生成，所以每个许可多重集恰走一条路径。

设旧状态中和为 z 的最短子序列长度为 d(z)。加入值 g 后，新出现的
零和必须使用这个位置，故安全的充要条件是 `d(-g)≥14`。更新
`d(z)` 时同时保留不用 g 的旧距离及使用 g 的 `d(z-g)+1`，因此上述
逐层判断没有启发式截断。

## 3. 修正后的真实行

`nodes_by_W_length[j]` 是通过所有上述过滤后，安全的长度 j 的 W
前缀多重集数，包括 j=0 的根。修正结果为：

| 核心 | W 长0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| VA | 1 | 228 | 8,466 | 28,905 | 4,843 | 0 | 0 | 0 |
| VB | 1 | 164 | 3,338 | 6,318 | 958 | 0 | 0 | 0 |

作为支撑过滤方向的交叉检查，新程序还保留相同的 W 重数容量限制，
但暂时允许 W 使用全部 625 个群值，包括强制支撑值。这个严格更大的
候选树得到：

| 核心 | W 长0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| VA，全 625 值 | 1 | 233 | 9,220 | 39,942 | 15,691 | 0 | 0 | 0 |
| VB，全 625 值 | 1 | 169 | 3,838 | 10,342 | 3,507 | 0 | 0 | 0 |

正式过滤树逐层不超过对应的放宽树，两组数均在长度 5 处为零。尤其，
任何一个核心都无法安全加入所需的七个 W 位置。搜索没有走到长度 7，
所以排除甚至不依赖 W 的规定总和；证据中的 `leaf_sum_tests=0` 正好
记录这一点。

因此修正后的逻辑结论仍是：

> B20 假想反例中，d=3、M=1 的两个重数放置都不可能发生。

## 4. 新证据与替换规则

重放命令为

```text
powershell -File scripts/continue_atom16_star_addendum_d3_fixed.ps1 -Seconds 30
```

新 JSON 同时保存正式支撑过滤树和全 625 值放宽树。输出去掉了运行
耗时字段，因而在相同输入和完整运行下是确定的。冻结的新文件及哈希
由 `evidence/continue_atom16_star_addendum_erratum_frozen_manifest.json`
绑定。

使用规则是：凡引用原附录第 3 节 d=3 计数表或旧 d3 JSON，必须改引
本勘误和 `evidence/continue_atom16_star_addendum_d3_fixed.json`；原附录
其余部分继续按各自证据审查。
