# 引理依赖账

| ID | 精确内容 | 状态 | 相对A/B | 证据/依赖 |
|---|---|---|---|---|
| D | D(C5^r)=4r+1 | KNOWN | 基础 | p群Davenport公式 |
| H3 | 坏A/B每个元素至多3份 | PROVED_HERE | STRICTLY_WEAKER | atom_structure §1；已发表C5³短零和常数 |
| LINE | 每条过原点直线至多3项，若3项则相同 | PROVED_HERE | STRICTLY_WEAKER | atom_structure；商群与短零和 |
| PLANE | 每个二维子空间至多7项 | PROVED_HERE | STRICTLY_WEAKER | atom_structure；C5²常数 |
| FIVE3 | 坏A/B不能有五种三重元素 | FINITE_EXHAUSTIVE_VERIFIED | STRICTLY_WEAKER | 五核10全树；独立全量位集复跑 |
| FOUR3-I | 坏A/B不能有四独立三重元素 | FINITE_EXHAUSTIVE_VERIFIED | STRICTLY_WEAKER | 34根656175节点；独立全量位集复跑 |
| FOUR3-H | 坏A/B不能有四种秩三三重元素 | PROVED_HERE | STRICTLY_WEAKER | four_triples_rank3.md；新上下文CORRECT；核心Lean |
| FOUR3 | 坏A/B至多三种三重元素 | PROVED_HERE_WITH_FINITE_COMPONENTS | STRICTLY_WEAKER | H3+FIVE3+FOUR3-I+FOUR3-H |
| 332 | 恰三种三重元素时，其三维张成之外无二重元素 | FINITE_EXHAUSTIVE_VERIFIED | STRICTLY_WEAKER | 113根20707001节点，最长18；独立全回放PASS |
| H12 | 三三重核心补足十二项H后，A/B对应准则排除 | VERIFIED_CORRECT | STRICTLY_WEAKER | 两份hyperplane_core证明；独立891核与抽象准则审计 |
| DOUBLE7 | 坏A/B的a+b≤7 | FINITE_EXHAUSTIVE_VERIFIED | STRICTLY_WEAKER | 2222全树10196叶逐一至多一种安全单项；h≤3；新上下文接口CORRECT |
| DOUBLE6 | a≥2时坏A/B的a+b≤6 | FINITE_EXHAUSTIVE_VERIFIED | STRICTLY_WEAKER | 3322全树15684叶、全部8709四项扩展与真实见证；新上下文全量复核 |
| COUNT126 | B的Z15≥126及两条整数不等式 | VERIFIED_CORRECT | STRICTLY_WEAKER | stronger_algebra §3；H3+CW；verify_count_cuts_fresh.md |
| P2 | p²群环恒等式 | VERIFIED_CORRECT | STRICTLY_WEAKER | stronger_algebra §2；综合验证§7；没有据此闭合A/B |
| LOWER18 | s≤13(C5^4)≥19 | PROVED_HERE_AS_CONSTRUCTION | 下界 | 显式18项，36多重数模式，位置枚举，Lean无公理依赖 |
| LOWER18-B | s≤14(C5^4)≥19；p≥5时s≤(3p−1)(Cp⁴)≥4p−1 | VERIFIED_CORRECT | 下界 | 基四重加g²，3种系数，独立全部位置枚举；一般p手证 |
| DENSE12 | 含零和自由H核心V12、除σ外dV≤6的20项序列必有≤13零和 | VERIFIED_CORRECT | STRICTLY_WEAKER | C5八位置手证；verify_dense12_fresh.md；九核全125距离独立重算 |
| SINGLE6 | 坏A/B不可能a=1,b=6 | FINITE_EXHAUSTIVE_VERIFIED | STRICTLY_WEAKER | 107656核心全重建；107647图排除+9个DENSE12核心；verify_single_extensions_fresh.md |
| H12-S8 | E10≤3、E9≤5等条件下，H外九位置支撑至少8的A准则 | VERIFIED_CORRECT | STRICTLY_WEAKER | hyperplane_core_A_support8.md；新上下文手证、7260候选对及75核全距离 |
| TWO4 | 坏A/B不可能a=2,b=4 | FINITE_EXHAUSTIVE_VERIFIED | STRICTLY_WEAKER | 8461核=7439图+958完整树+64 H12；全部独立重建与接口绑定 |
| EXCESS7 | 坏A/B有2a+b≤7，支撑至少A14/B13 | VERIFIED_CORRECT | STRICTLY_WEAKER | 旧完整条件+SINGLE6+TWO4；最终综合接口独立CORRECT |
| END-A | s≤13(C5^4)≤21 | OPEN | EQUIVALENT | v1 |
| END-B | s≤14(C5^4)≤20 | OPEN | EQUIVALENT | v1 |
| SQ19 | F5^4任意19个互异元素有≤14零和 | VERIFIED_CORRECT_WITH_ERRATUM | STRICTLY_WEAKER | global_continue_squarefree_B；错误审查附句已单独勘误，正文证明不受影响 |
| SUP18 | 18互异元素追加任意一项即有≤14零和 | VERIFIED_CORRECT_WITH_ERRATUM | STRICTLY_WEAKER | global_continue_support18_B；同一勘误绑定 |
| H12-ALL | 坏A/B任意三维子空间占用≤11 | FINITE_EXHAUSTIVE_VERIFIED | STRICTLY_WEAKER | 新五树15099890节点/168177记录及旧891核，独立重建 |
| DOUBLE7-EXACT | 坏A/B不可能a=0,b=7 | FINITE_EXHAUSTIVE_VERIFIED | STRICTLY_WEAKER | 166195核，166180着色+15稠密H12；全新复核 |
| H11-A3-B | B的a=3时三重张成H不能占11位置 | LEAN_PARTIALLY_CHECKED | STRICTLY_WEAKER | 738/131核心；715标量表Lean无公理；全新自然语言审核 |
| STAR16 | B中16-atom为共同中心二/三星；平方自由者不存在 | VERIFIED_CORRECT | STRICTLY_WEAKER | continue_atom16_star及交叉审核，line3按真实位置复证 |
| STAR16-M1 | B中16-atom的M=1全部排除 | VERIFIED_CORRECT_AFTER_ERRATUM | STRICTLY_WEAKER | d2手证+2365表；d3真实两树；d4三图表；原d3数表撤销 |
| SUPPORT16-B | 坏B支持≤16，即4≤2a+b≤7 | VERIFIED_CORRECT | STRICTLY_WEAKER | atom17_integrity+support17_exclusion，两轮审核 |
| ATOM16-17 | 在坏B中16-atom与17-atom同时存在或同时不存在，若存在只余d4M0 | VERIFIED_CORRECT | STRICTLY_WEAKER | 三份原子完整性手证，无循环依赖 |
| RAINBOW17-FAIL | 六边三色局部条件不足以排除17-atom | DISPROVED_LOCALLY | 失败断点 | 九值511非空子集全非零；不是17-atom/B反例 |

两项追加局部扩展均已完成独立终审。未完成的旧H11外部树及低重数大支撑整类仍保持INCOMPLETE，不将局部计算倒填为完整A/B。

所有新颖性均未认证。FINITE_EXHAUSTIVE_VERIFIED是带可重复整数计算的有限排除，不能标为完整一般定理或完整Lean认证。

相对原命题：以上 STRICTLY_WEAKER 均只表示必要条件或局部类排除。EQUIVALENT_BLOCKER 是完整剩余低重数群序列的实际实现问题，不把它重命名成已证引理。外部定理条件核验：小群短零和数值、Davenport公式、全尾归约的版本及使用范围分别在 assumptions.md、prior_art.md 和指定独立审计中记录。
