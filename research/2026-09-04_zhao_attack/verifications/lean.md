# Lean实际检查记录

STATUS: LEAN_PARTIALLY_CHECKED。

工具链Lean4.30.0已实际运行。Rank3Core.lean的两个有限覆盖引理均退出码0，公理仅propext、Quot.sound；LowerBound18.lean退出码0，noShortZero18不依赖任何公理。另一个隔离验证者以其已安装4.32.0独立编译Rank3Core也成功。

自然语言对应：Fin4恰为四份候选核心中可取0..3的系数；Fin5为模5坐标。18项构造用四个Fin4、两个Fin2、两个Fin3精确匹配重数。没有把按位置计数的枚举改成去重集合；存在性只取决于各元素所用份数。

无sorry、admit、新增axiom或unsafe。没有形式化完整端点A/B，也没有形式化全部搜索树。具体命令与覆盖范围见 ../formal/README.md 和 ../formal/build.log。
