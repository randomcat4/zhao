# (p=233,m=4) 的 (O_2/O_3) 删点前沿复核

STATUS: **CORRECT PROVED REDUCTIONS / CORRECT PROTOTYPE / GLOBAL INCOMPLETE**

## 1. 复核范围

本次独立重放并审计以下三层。

1. 通用删点标签容量接口；
2. (O_2) 特殊秩层及 932 个继承态排除；
3. (O_3) 四代表联合删点探针与仿射子空间全扫原型。

所有有限域计算均在 (mathbb F_{233}) 中精确进行。未读取或改写
`2026-09-05_zhao_Ap_general` 下的既有用户报告。

## 2. 逻辑审计

- 对删点序列 (D=C\setminus\{x\})，补集反射的中心与符号正确；
  中心奇五次满足
  (D_g(s+g/2)-D_g(s-g/2)=q(s))。
- 三个 fringe 的每个非空字面子集先由原子性给普通无表示，再给
  系数零。满 fringe 仍遗漏已删位置，因此也是合法真子序列条件。
- q-free 存在型集合、固定共同 (q) 的 (Gamma_q) 及只使用部分
  fringe 的 (Gamma_{\rm known}) 已分开。容量论证只使用实际支撑
  包含关系与单标签重数至多 232，故
  (460\le232|\Gamma_q|)；没有跨不同 (q) 拼接标签。
- (O_3) 主探针先固定共同归一化 (q)，再对具体三块状态计算
  (Gamma_q)。正文已修正早期把 q-free 65 行系统写成 fixed-(q)
  系统的歧义，并把全量复杂度改为“块测试加输出敏感成本”。
- 仿射子空间原型中的 (54\,058/224/4/2) 是纯尾必要门的目录；
  两个冻结 (q) 都命中两个 base labels，不冒充完整 fringe 后各余
  一个标签的结论。

## 3. 独立重放结果

- (O_2)：`PASS`；共享块秩分布
  (4:4,5:7,6:54\,278)，低秩 compatible 对 14 个，异常尾中心
  (6+6) 个，继承态 (932\to0)。
- (O_3) 联合删点：`PASS`；全尾秩
  (6:54\,276,5:12)，四代表定向态
  (16,0,217\,172,24)，均被 quartic 空交或容量门排除。
- (O_3) 仿射原型：`PASS`；
  (	au=(17,31)) 的端点目录为 (9/11/13)，全零竖切片为
  (0/0/0)；(	au=(0,1)) 的纯尾对偶目录为
  (54\,058/224/4/2)。

## 4. 文件哈希

- 通用接口：
  `05dab6a99f936a9cc21cfc222b3c6d1aa13fc2758426d7c8125afb0f8a23a162`。
- (O_2) proof/script/report：
  `88a2ef3850b6d4435d20e18a2ccfc8d9664986c67c8b2747dcfad3d4046c4367`、
  `8784ec48ba779504754217afd3db2360c24558a2a820b3ef5a64c3f6a40432c0`、
  `d3538976b57597e62532e38a9b6d7da1637b2a96775242bb27983996a686ea7c`。
- (O_3) representative proof/script/report：
  `cb38c9f9a7944057eff23904226e228a2128912a2585287317084bd44738e063`、
  `9e1ec133305d21a79d18a0500a52820de8d4705fb07e6b2b124ddab43a88aba0`、
  `125712d329881c55a033815290b82ffc11dbe61954f0f275cad60899220fb523`。
- (O_3) affine design/script/report：
  `5e091a26de9d5e443bd5ab43aa8a49cf5bd46d46bda994ba2c924f7a7611a693`、
  `48d63b8516f4649ba70f0f3f8d333fb8856aefd2b7a0c01bf554d6d46859717c`、
  `aed1b0255ea59aa2a294d5a6046427c6dee1c3f42fca9c5f958fbfc0e9940d74`。

## 5. 边界

审计不关闭 generic (O_2) 或 generic (O_3)。仿射子空间设计
避免展开高维 (q)-纤维和三重 (z) 笛卡尔积，但正维 minor 簇、
共同 (q)-线／平面及大标签对关系仍须单列。故 (m=4)、180 个
outer rows 与一般 (A_p) 继续为 **INCOMPLETE**。
