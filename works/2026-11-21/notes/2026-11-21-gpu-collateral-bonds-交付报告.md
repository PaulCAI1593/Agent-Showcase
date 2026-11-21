# 《抵押在轨道上的算力》交付报告（证据重建补录）

> **本报告为总指挥指派的证据重建补录，非作品作者自述。**
> 报告人：知库（wisdom-keeper），补录时间 2026-11-21 20:55 起（北京）。
> 方法：只依据盘上已有文件（成品 HTML、过程脚本、素材简报、前作）逐条读取与实跑；作者设计意图与主观评价一律列入「未确认」，不代作者编写。

**原执行方失败记录**

| 单号 | 执行方 | 现象 |
|---|---|---|
| `task-8cfbe454101c` | 研析 | `Task timed out after 3600s`（3600s 包装层超时），交付报告未落 `notes/` |

**作品**：`works/2026-11-21/research/2026-11-21-gpu-collateral-bonds.html`
**署名**：研析（成品 `:376`「主责：研析」、`:931` 署名行）
**追踪线**：估值与资本（成品 `:7` `<meta name="showcase-beat" content="估值与资本">`）
**补录单**：#462，截止 2026-11-21 23:30 北京时间

## 目录

1. [结构实测](#1-结构实测)
2. [claims 7 条与 quote 命中核对](#2-claims-7-条与-quote-命中核对)
3. [三档口径对照](#3-三档口径对照)
4. [标签族对账（规则15 ④）](#4-标签族对账规则15-)
5. [实跑三条命令](#5-实跑三条命令)
6. [过程件清单](#6-过程件清单)
7. [缺陷与未确认清单](#7-缺陷与未确认清单)

## 1. 结构实测

实测命令（在 `/app/working/shared/showcase` 下执行，python3 去标签统计）：

```bash
python3 - <<'EOF'
import re
p='works/2026-11-21/research/2026-11-21-gpu-collateral-bonds.html'
s=open(p,encoding='utf-8').read()
print('bytes:',len(s.encode('utf-8')),'chars:',len(s))
body=re.sub(r'<(script|style)[\s\S]*?</\1>','',s)
text=re.sub(r'<[^>]+>','',re.sub(r'&[a-z]+;',' ',body))
print('visible_no_ws:',len(re.sub(r'\s','',text)))
for pat,name in [(r'<section\b','section'),(r'<button\b','button'),(r'addEventListener','addEventListener'),(r'<input\b','input'),(r'<svg\b','svg'),(r'<a\b','a')]:
    print(name,len(re.findall(pat,s)))
print('remote:',re.findall(r'(?:src|href)="https?://[^"]+"',s))
EOF
```

实测数字（2026-11-21 20:57 北京，本报告人亲跑）：

| 指标 | 实测值 |
|---|---|
| 文件字节 | **63,697 B**（UTF-8）；45,783 字符 |
| 可见文本（去标签、去 script/style、去空白） | 8,743 字 |
| `<section>` | 11（`verdict-band` / `metrics` / `stack` / `terms` / `scenarios` / `align` / `sequel` / `orbit` / `timeline` / `evidence` / `gaps`，`:387-876`） |
| `<button>` | **0**（本件为研究类长文，无按钮控件） |
| `addEventListener` | 1（在注入的 `showcase-backlink-js` 内，`:359`；作者正文无事件绑定） |
| `<input>` | 0 |
| `<svg>` | 2 |
| `<a>` | 2 |
| 远程依赖 `src|href="https?://…"` | **0 条**（派单「远程依赖 0」已验证） |
| `未确认` 出现次数（`grep -c`） | 25 |
| 标题序列 | H1 + 11×H2 + 3×H3（无 H4/H5 跳级，见第 5 节 QA 输出） |

派单称成品 63,741 B，盘上 `wc -c` 与 python `len(utf-8)` 双测均为 **63,697 B**，差 44 B，原因未确认（第 7 节 #1）。

## 2. claims 7 条与 quote 命中核对

7 条断言逐字照抄自 `works/2026-11-21/research/2026-11-21-gpu-collateral-bonds.html:941-979`（`id="claims"` JSON 块）：

| # | value（逐字） | label（逐字） | quote（逐字） |
|---|---|---|---|
| 1 | `430 亿美元` | `SpaceX 债务融资规模（11-20 金融时报口径）` | `430 亿美元 SpaceX 债务融资规模（11-20 金融时报口径）` |
| 2 | `250 亿美元` | `SpaceX GPU 租金支持债券额度（五年租金支持口径）` | `250 亿美元 SpaceX GPU 租金支持债券额度（五年租金支持口径）` |
| 3 | `6800 亿美元` | `先进计算基础设施相关债务发行额（截至 2026 年 10 月口径）` | `6800 亿美元 先进计算基础设施相关债务发行额（截至 2026 年 10 月口径）` |
| 4 | `1300 亿美元` | `2023 年全年同类债务发行额（同一出处对比值）` | `1300 亿美元 2023 年全年同类债务发行额（同一出处对比值）` |
| 5 | `2960 亿美元` | `超大规模数据中心运营商年内发债额（11-08来源口径）` | `2960 亿美元 超大规模数据中心运营商年内发债额（11-08来源口径）` |
| 6 | `1 个机架` | `轨道数据中心卫星单星算力当量（Project Suncatcher 口径）` | `1 个机架 轨道数据中心卫星单星算力当量（Project Suncatcher 口径）` |
| 7 | `2029 年` | `New Glenn 数据中心卫星发射计划年份（Google×Blue Origin 签约口径）` | `2029 年 New Glenn 数据中心卫星发射计划年份（Google×Blue Origin 签约口径）` |

**门工具核对（原文输出）**：

```
$ cd /app/working/shared/showcase && python3 tools/claim_gate.py --verify
重校验 1421 条断言
✓ 全部通过
```

**quote 对本件正文逐字命中（归一化子串匹配，本报告人亲跑，用 `claim_gate.py` 的 `normalize`/`verify_quote`）**：

```
HIT  1 430 亿美元 | SpaceX 债务融资规模（11-20 金融时报口径）
HIT  2 250 亿美元 | SpaceX GPU 租金支持债券额度（五年租金支持口径）
HIT  3 6800 亿美元 | 先进计算基础设施相关债务发行额（截至 2026 年 10 月口径）
HIT  4 1300 亿美元 | 2023 年全年同类债务发行额（同一出处对比值）
HIT  5 2960 亿美元 | 超大规模数据中心运营商年内发债额（11-08来源口径）
HIT  6 1 个机架 | 轨道数据中心卫星单星算力当量（Project Suncatcher 口径）
HIT  7 2029 年 | New Glenn 数据中心卫星发射计划年份（Google×Blue Origin 签约口径）
quote命中 7 / 7
```

**quote 对素材原文的命中（同法核对三份素材，本报告人亲跑）**：

```
1 430 亿美元   -> ['简报11-20']      （每日AI技术动态简报/2026-11-20.md:11）
2 250 亿美元   -> ['简报11-20']
3 6800 亿美元  -> ['简报11-17']      （每日AI技术动态简报/2026-11-17.md:35）
4 1300 亿美元  -> ['简报11-17']
5 2960 亿美元  -> ['热点11-10']      （每日热点新闻简报/2026-11-10.md:19，金融界 11-08）
6 1 个机架     -> 三份素材均未命中
7 2029 年      -> ['简报11-20']
```

**第 6 条如实说明**：素材原句是「每颗算力大致相当于**一个数据中心机架**」（`2026-11-20.md:10`），成品把它写成 `1 个机架`（`:445` metric-value、`:411` 分组说明），**是改写不是逐字**；`quote` 拼接串在本件正文内逐字存在（`:411` 有「1 个机架」、`:970` 有标签），故 G1 通过。素材逐字层面第 6 条为**未逐字命中**，改写是否被作者接受 → 未确认（第 7 节 #5）。

**quote 命中口径提醒**：`claim_gate` 的 G1 只证明「quote 在本件正文里」，不证明「标签与数值配对正确」（工具自述边界，`tools/claim_gate.py:40-43`）。本节因此额外做了素材侧核对，见上表。

## 3. 三档口径对照

派单要求：430 亿（金融时报口径）／250 亿（五年租金支持）／6800 亿三档不得混写，逐条写来源。成品的实际写法（行号均指本件，读出的原文）：

| 档 | 成品原文位置 | 成品原文 | 来源标注 |
|---|---|---|---|
| **430 亿** | `:415` | `430 亿美元`（metric-value），metric-label 为 `SpaceX 债务融资规模（11-20 金融时报口径）` | 表 3 `:641-647`：时点「截至 2026-11-20 报道」、主体「SpaceX 债务融资（SPE 发行）」、来源「金融时报 / 凤凰网科技 · 简报 2026-11-20 焦点 7」 |
| **250 亿** | `:425` | `250 亿美元`（metric-value），metric-label 为 `SpaceX GPU 租金支持债券额度（五年租金支持口径）` | 表 3 `:657-662`：性质「已售出部分中的单笔」、来源「金融时报 · 简报 2026-11-20 焦点 7」 |
| **6800 亿** | `:430` | `6800 亿美元`（metric-value），metric-label 为 `先进计算基础设施相关债务发行额（截至 2026 年 10 月口径）` | 表 3 `:665-670`：时点「截至 2026 年 10 月」、主体「先进计算基础设施发行人（全行业）」、来源「美联储《金融稳定报告》· 前作 11-18 沿用」 |

**混写检查（`grep` 实测）**：

- `:411` 明确分组：「这八个数分属三组：**本笔融资**（430 / 逾 300 / 250）、**行业存量**（6800 / 1300 / 2960，沿用前作标签）、**轨道侧**（1 个机架 / 2029 年）。」
- `:397` 嵌套关系：「430 亿、逾 300 亿、250 亿是三笔钱吗？**不是，是嵌套关系。**」
- `:456` 读法一：「430 亿美元 ⊃ 逾 300 亿美元 ⊃ 250 亿美元。三个数不能相加，只能取外层。」
- `:401` 跨组：「与前作的 6800 亿美元什么关系？同一存量的两层。两者口径是否重叠未确认，不相加。」
- `:457` 读法二：本笔 430 亿与 6800 亿是否重叠 **未确认**；2960 亿主体不同，「并列只作趋势参照」。
- 表 3 `:635` 列名即「**能否与 430 亿相加**」，六行分别标「不适用／否（包含于 430 亿）／否（包含于逾 300 亿）／未确认／否／否」。
- `:692`：「唯一可算的一格。430 ÷ 6800 ≈ 6.3%（研析推算），前提是本笔 430 亿已计入美联储口径；该前提未确认……其余各格一律不换算。」
- `:930` 页尾声明：「430 ÷ 6800 ≈ 6.3% 是由公开数字做的算术，不是来源给出的结论」。

**结论（已验证）**：430／250／6800 三档在成品中分属不同 metric 卡与表 3 不同行，各自带独立来源；全文无把三者相加或互相替代的写法；唯一比值 430÷6800 明确标注为「研析推算 + 前提未确认」。三档未混写。

**素材侧来源（本报告人亲读）**：

- 430 亿／250 亿 → `tasks/每日AI技术动态简报/2026-11-20.md:11`（焦点 7，来源：金融时报 / 凤凰网科技 11-20）
- 6800 亿／1300 亿 → `tasks/每日AI技术动态简报/2026-11-17.md:35`（美联储 11-13《金融稳定报告》，截至 2026 年 10 月超 6800 亿美元、约为 2023 年全年 1300 亿美元的五倍）
- 2960 亿 → `tasks/每日热点新闻简报/2026-11-10.md:19`（金融界 11-08，超大规模数据中心运营商今年已发行 2960 亿美元债券）

（本节 2026-11-21 21:10 落盘。）

## 4. 标签族对账（规则15 ④）

**对账方法**：用 `grep -rlF '"label": "<标签>"' works/` 在全库检索逐字同名标签；复用条目再与 11-18 前作的 `value`/`quote` 做程序化逐字比对（python 读两边 `id="claims"` JSON，本报告人亲跑）。

**比对程序输出（原文）**：

```
11-18 claims: 8  11-21 claims: 7
新建: SpaceX 债务融资规模（11-20 金融时报口径）
新建: SpaceX GPU 租金支持债券额度（五年租金支持口径）
复用: 先进计算基础设施相关债务发行额（截至 2026 年 10 月口径）
   value 一致
   quote 一致
复用: 2023 年全年同类债务发行额（同一出处对比值）
   value 一致
   quote 一致
复用: 超大规模数据中心运营商年内发债额（11-08来源口径）
   value 一致
   quote 一致
新建: 轨道数据中心卫星单星算力当量（Project Suncatcher 口径）
新建: New Glenn 数据中心卫星发射计划年份（Google×Blue Origin 签约口径）
```

**三条复用族标签的全库逐字检索结果**（每条 5 处命中）：

| 标签 | 命中文件 |
|---|---|
| `先进计算基础设施相关债务发行额（截至 2026 年 10 月口径）` | `works/2026-11-18/research/2026-11-18-ai-infra-credit-review.html`、其 `.bak.20261118-064111`、`works/2026-11-21/notes/enrich.json.bak-20261120-184957`、本件、本件 `.bak.20261121-004729` |
| `2023 年全年同类债务发行额（同一出处对比值）` | 同上 5 处 |
| `超大规模数据中心运营商年内发债额（11-08来源口径）` | 同上 5 处（另有 `works/2026-11-11/` 交付报告、口径台账、`429-口径裁定-总指挥.md` 以纯文本提及该指标名，非 claims 结构） |

**一致／分叉结论**：

- **一致**：三条标签在本件与 11-18《AI基建信用审查》之间，`label`、`value`、`quote` 三字段**全部逐字一致**，无数值漂移、无标签改写 → 属**复用既有族**，与派单描述相符。
- **分叉**：无。
- 本件正文亦自述复用：`:724`「三个标签**逐字复用**，数值与出处不变，只换本篇语境」；`:411`「沿用前作标签」。
- **新建 4 条**：`SpaceX 债务融资规模（11-20 金融时报口径）`、`SpaceX GPU 租金支持债券额度（五年租金支持口径）`、`轨道数据中心卫星单星算力当量（Project Suncatcher 口径）`、`New Glenn 数据中心卫星发射计划年份（Google×Blue Origin 签约口径）`——逐字检索各仅命中本件与本件 `.bak` 两处（无其他作品同名）→ **全库首次出现**。
- 命名格式沿用族约定「指标名（口径/日期）」，与复用三条同构。

**index 收录状态（只读核对）**：`index.html` 含本件条目（`"file": "works/2026-11-21/research/2026-11-21-gpu-collateral-bonds.html"`）；未跑 build_manifest（纪律）。

## 5. 实跑三条命令

三条命令均由本报告人于 2026-11-21 20:58–21:02 北京时间亲跑，原文输出如下。

**① claim_gate --verify**：

```
$ cd /app/working/shared/showcase && python3 tools/claim_gate.py --verify
重校验 1421 条断言
✓ 全部通过
```

**② design_scan（只扫本件，非全量）**：

```
$ cd /app/working/shared/showcase && python3 tools/design_scan.py --scope file:works/2026-11-21/research/2026-11-21-gpu-collateral-bonds.html
扫描 1 件作品 · findings 0 条 · 涉及 0 件
严重度分布: {}
规则 Top:

（非全量扫描：只报告，不比棘轮）
```

**③ audit_pages（真实加载 + 抓运行时错误）**：

```
$ cd /app/working/shared/showcase && python3 tools/audit_pages.py works/2026-11-21/research/2026-11-21-gpu-collateral-bonds.html
巡检 1 件作品（真实加载 + 抓运行时错误）


========================================================
巡检完成：1 件，0 件有问题
requestfailed 口径：策略拦截 0 次 / 导航中止 0 次 / 与本页无关 0 次（均不计为问题）；远程依赖未落定 0 件
✓ 全部作品页运行时健康
```

**④ 过程件 render-check 实跑**（派单未强制，本报告人加跑；脚本只读，不写任何文件）：

```
$ cd /app/working/shared/showcase && timeout 300 python3 works/2026-11-21/notes/2026-11-21-gpu-collateral-render-check.py
== 1440x900 ==
 overflowX(px): 0
 offenders: 0 []
 console: []
 contrast fail: 0 []
 headings: H1H2H2H2H2H2H2H2H2H2H2H3H3H3 | sections: 11 | claims: 7
 fonts: {'serif': True, 'num': True}

== 1024x800 ==
 overflowX(px): 0
 offenders: 0 []
 console: []
 contrast fail: 0 []
 headings: H1H2H2H2H2H2H2H2H2H2H2H3H3H3 | sections: 11 | claims: 7
 fonts: {'serif': True, 'num': True}

== 375x812 ==
 overflowX(px): 0
 offenders: 0 []
 console: []
 contrast fail: 0 []
 headings: H1H2H2H2H2H2H2H2H2H2H2H3H3H3 | sections: 11 | claims: 7
 fonts: {'serif': True, 'num': True}

heading sequence: ['H1', 'H2', 'H2', 'H2', 'H2', 'H2', 'H2', 'H2', 'H2', 'H2', 'H2', 'H2', 'H3', 'H3', 'H3']
QA: PASS
```

（该脚本 `sys.exit(1 if fail else 0)`，本次退出码 `EXIT=0`。）

**结论**：claim_gate 1421 条全通过；design_scan 本件 findings 0；audit_pages 1 件 0 问题、远程依赖未落定 0；render-check 三视口无横向溢出、无越界元素、无 console 错误、无对比度失败，标题序列合法，QA PASS。

## 6. 过程件清单

`ls -l --time-style=+%F %T` 实测（2026-11-21 21:19，`find . -name '*gpu-collateral*'`）：

```
----------+ 1 root root  19660 2026-11-21 01:19:24 ./thumbs/2026-11-21-research-2026-11-21-gpu-collateral-bonds-thumb.webp
----------+ 1 root root 124975 2026-11-21 01:19:24 ./_private/thumbs-src/2026-11-21-research-2026-11-21-gpu-collateral-bonds-thumb.png
-rw-r--r--+ 1 root root   5052 2026-11-21 00:44:48 ./works/2026-11-21/notes/2026-11-21-gpu-collateral-render-check.py
-rw-r--r--+ 1 root root  63697 2026-11-21 01:00:41 ./works/2026-11-21/research/2026-11-21-gpu-collateral-bonds.html
-rw-r--r--+ 1 root root  60293 2026-11-21 00:47:29 ./works/2026-11-21/research/2026-11-21-gpu-collateral-bonds.html.bak.20261121-004729
```

| 过程件 | 字节 | 说明 |
|---|---|---|
| `notes/2026-11-21-gpu-collateral-render-check.py` | 5,052 B | 三视口渲染 QA 脚本（Playwright/Chromium），只读 |
| `research/…gpu-collateral-bonds.html.bak.20261121-004729` | 60,293 B | 00:47:29 的备份快照 |
| `thumbs/…-thumb.webp` | 19,660 B | 缩略图 |
| `_private/thumbs-src/…-thumb.png` | 124,975 B | 缩略图源 |

**同目录 11-21 其它 gpu 相关文件**：`ls notes/ | grep -i gpu` 只返回 `2026-11-21-gpu-collateral-render-check.py` 与本报告文件——**本件没有截图、没有 render-check.json**（与 #463 的证据密度不同，见第 7 节 #4）。

**.bak diff 结论**（`diff research/….bak.20261121-004729 research/….html`，28 行变更：`<` 11 行、`>` 17 行）：

| # | 位置 | 改动事实 |
|---|---|---|
| 1 | CSS `:210` | `.layer-body .fact b{color:var(--seal)}` → `var(--forest)` |
| 2 | CSS `:218` | 删除 `.layer.flow .layer-tag .nm{color:var(--ink)}` 一行 |
| 3 | CSS `:257-260` | `.yes/.no/.half/.calc` 四条规则的限定域由 `table.tbl td` / `table.tbl` 放宽到全局选择器 |
| 4 | CSS `:323` | reduced-motion 段删除 `.rule-draw,` 限定，只保留 `h2::after` |
| 5 | `:353-360`（新增 8 行） | 插入 `<!-- showcase-backlink -->` 顶栏 `#showcase-bar`、固定返回按钮 `#showcase-backlink`、明暗检测脚本 `#showcase-backlink-js` |
| 6 | `:578` 表 2 导语 | 「第三列全部是素材未给」→「『素材是否给出处置结果』一列只有一格是部分，其余两格都是否」 |
| 7 | `:582` 表 2 caption | 「灰底格为素材未覆盖」→「标『否』『未确认』的格为素材未覆盖」 |
| 8 | `:781` SVG 文本 | `数据中心卫星` 标签 x=792,y=132 → x=742,y=126 |
| 9 | `:787` SVG 文本 | `2029 计划：New Glenn 发射` x=330,y=118 → x=308,y=96 |

第 5 项为带 `showcase-backlink` 标记的基础设施块（全馆收敛件特征），**注入者未确认**（第 7 节 #3）；其余各项只描述改动事实，不推断意图。

（本节 2026-11-21 21:22 落盘。）

## 7. 缺陷与未确认清单

| # | 事项 | 状态 | 确认方法 |
|---|---|---|---|
| 1 | 派单称成品 63,741 B，盘上 `wc -c` 与 python `len(utf-8)` 双测均为 63,697 B（差 44 B） | 未确认（差异原因） | 向总指挥核对 63,741 的数字来源 |
| 2 | claim #6 `1 个机架` 是对素材「每颗算力大致相当于一个数据中心机架」的改写，非逐字 | 未确认（改写是否被接受） | 问研析本人；素材原句见 `2026-11-20.md:10` |
| 3 | .bak diff 第 5 项 `showcase-backlink` 注入块的注入者（作者 or 收敛管道） | 未确认 | 查 autopublish/build_manifest 日志或提交记录（本单禁跑这两命令，未执行） |
| 4 | 本件无截图、无 render-check.json，只有 .py 脚本；脚本原本输出是否 PASS 当时未落盘 | 未确认（原运行结果） | 本报告已重跑该脚本得 QA PASS（第 5 节④），但不等同于作者当时的输出 |
| 5 | 作者设计意图与主观评价（为何把 `.yes/.no` 选择器放宽、为何移动 SVG 标签等） | 未确认 | 问研析本人；diff 只给改动事实（第 6 节） |
| 6 | 430 ÷ 6800 ≈ 6.3% 的前提「本笔 430 亿已计入美联储口径」 | 未确认（成品自身已标） | 读美联储《金融稳定报告》口径脚注与 SpaceX 发行文件 |
| 7 | `430 亿` 与 `6800 亿` 是否口径重叠 | 未确认（成品自身已标） | 同上 |
| 8 | 「周四 = 2026-11-19」的日期换算、四层结构图与情形矩阵的分析编排 | 未确认（非素材结论，成品 `:930` 已声明） | 问研析本人 |
| 9 | 派单称 claims 7 条 quote 7/7、beat=估值与资本、远程依赖 0、署名=研析 | 已验证（第 1、2 节命令与 `:7`/`:376`/`:931` 读出） | — |

## 验收自检

```bash
ls -l --time-style=+%F\ %T works/2026-11-21/notes/2026-11-21-gpu-collateral-bonds-交付报告.md
wc -l works/2026-11-21/notes/2026-11-21-gpu-collateral-bonds-交付报告.md
grep -c '未确认' works/2026-11-21/notes/2026-11-21-gpu-collateral-bonds-交付报告.md
grep -c 'design_scan' works/2026-11-21/notes/2026-11-21-gpu-collateral-bonds-交付报告.md
```

（输出随最终保存再跑一次，见交付回复。）

**未做**

- 未改作品、未改 claims、未改 `tools/*.py` — 按纪律。
- 未跑 autopublish / build_manifest / 全量 design_scan — 按纪律（design_scan 只用 `--scope file:` 单件）。
- 未 git push — 按派单。
- 未重跑会覆盖过程件的输出动作；`render-check.py` 只 print、不写文件，故可安全重跑。

**待确认**

- 第 7 节表中 #1–#8 项，交总指挥裁定。

（本节 2026-11-21 21:25 落盘。）
