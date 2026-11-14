# 《33 年的掌舵，14 个点的崩跌》交付报告 · 选题 435（研究类）

> 成品：`works/2026-11-13/research/2026-11-13-nvidia-succession-power-shift.html`（55,850 B，单文件，零远程依赖）
> sha256：`fb84145a8df1f46378d46e6d7a38b530c2c9e66268ffd975fab13cfeb476f9f8`
> mtime：终稿 2026-11-14 03:4x（Asia/Shanghai）；档案条由展厅守护进程于 02:29 注入，注入前快照 `notes/…html.bak.20261113-182944`
> 追踪线 beat：`厂商与算力权力`（`<meta name="showcase-beat">` 与抬头 `<dt>追踪线</dt>` 一致）
> 执行：研析（research-analyst）· 协作：数析（行情核对表）· 派单：总指挥 2026-11-14 00:05
> 配套台账（同目录）：`435-核源台账-研析.md`、`435-口径台账-研析.md`、`435-行情核对表-数析.md`
> 截止：2026-11-15 02:00 · 实际初稿落盘：2026-11-14 02:5x（派单后约 2.8 小时，满足 12h 约束）

---

## 一、结论先行

已完成：研究类作品 1 件 + 过程台账 3 份。断言 8 条全部过闸；`impeccable detect` 0 findings；渲染复验无资源 404、无 console 错误、375px 无横向滚动。

作品回答派单主问「谁在英伟达缺席时接单」，结构为：**四天时间轴 → 一天的投票（16 行供应商对照表）→ 权力层级图（人/股权/采购/产能/管制五层）→ 三种接单分开读（8 行接单者清单）→ 接下来三件事 → 10 条逐字证据**。

---

## 二、impeccable 已执行（规则 14 留痕）

工具：`/app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable`，版本 **4.7.1**。
该发行版 CLI 只有 `detect / ignores / help / install / link / update / check / telemetry`；**`audit` 与 `polish` 是 agent 侧作业手册**（`reference/audit.md`、`reference/polish.md`），下表分开记录。

### 2.1 动手前：context（装载既有视觉权威）

```bash
cd /app/working/shared/showcase
…/skills/impeccable/scripts/impeccable context \
  --target works/2026-11-13/research/2026-11-13-nvidia-succession-power-shift.html
```

退出码 **0**。要点：

| 字段 / 指令 | 值与处置 |
|---|---|
| NO_PRODUCT_MD | 本仓库无 PRODUCT.md，但**存在既有视觉实现** → 不新造视觉世界 |
| SCOPED_EXISTING_ALLOWED | 以既有实现为权威推进；`init` 只作后续选项，不阻塞交付 |
| EXISTING_VISUAL_SYSTEM | 权威 = `templates/work.html`「档案卷宗」世界（冷调档案纸 + 墨色 + 陈铜 + 衬线 + 发丝线） |
| RESOLVED_CONTEXT | targetExists=true · projectRoot=`/app/working/shared/showcase` · productPath=null · designPath=null · hasVisualImplementation=true |
| MANUAL_DETECTOR_REQUIRED | 本会话无自动 hook → 交付前手动跑 `detect --json`（已执行，见 2.3） |

同时读取 `skills/impeccable/reference/craft-floor.md`（UI 改写前必读）与 `reference/audit.md`、`reference/polish.md`。
派单要求「起步但不套壳」：沿用模板的 token 与封闭语义词汇表，**版面结构按本篇内容重排**（新增权力层级 ladder、16 行对照表、接单者清单），模板占位文案全部替换，未照搬任何 `{{ }}`。

### 2.2 detect（机械探测器）

```bash
…/scripts/impeccable detect works/2026-11-13/research/2026-11-13-nvidia-succession-power-shift.html
…/scripts/impeccable detect works/2026-11-13/research/2026-11-13-nvidia-succession-power-shift.html --json
```

- 退出码 **0**，无输出（= 0 anti-patterns、0 advisory）。
- `--json` 复跑：`findings: 0`，规则分布为空集。
- 对照基线：同法跑 #432（11-12 作品）亦为 0 findings；展厅棘轮 `tools/design_scan.py` 的规则集（28 条）无一上升。

### 2.3 audit（agent 侧五维，按 reference/audit.md）

| # | 维度 | 分 | 关键发现与证据 |
|---|---|---|---|
| 1 | Accessibility | **3/4** | 已实测计算样式对比度（Playwright + `getComputedStyle`）：`.mast-meta dt` 4.63:1、`.metric-source` 5.03:1、`.note` 4.63:1、`.evidence-source` 4.63:1、`.timeline-detail` 6.47:1、`.cap` 6.47:1、`.rung-line` 6.47:1、涨色 `num up` 4.97:1、跌色 `num down` 5.56:1 —— 全部 ≥4.5:1。标题层级 h1→h2→h3 无跳级；`lang="zh-CN"`、`<main>/<header>/<footer>` 地标齐备；两张表均有 `<caption>` 与 `scope="col"`；涨跌除颜色外另有 +/− 符号（不单靠颜色传义）；`prefers-reduced-motion` 有降级。缺口：未写自定义 `:focus-visible` 与跳转链接（页面无可交互控件，仅展厅注入的返回链自带样式）。 |
| 2 | Performance | **3/4** | 单文件、零远程请求、无图片；动效只有一个 IntersectionObserver + 一次 transform 过渡。遗留：`.rule-draw` 静止态仍挂 `will-change`（模板原样继承，非本篇新增）。 |
| 3 | Theming | **3/4** | 全部颜色走 `:root` token；`:root` 外仅 6 处硬编码色值，**全部位于展厅守护进程注入的 `#showcase-bar` / `#showcase-backlink`**，非本篇所写。 |
| 4 | Responsive | **3/4** | 375px 实测 `scrollWidth==clientWidth==375`，无横向溢出；断点 640 / 900 / 980；宽表在 `.tbl-wrap`（`overflow-x:auto`）内滚动，`min-width:660px` 保证列不塌。缺口：手机端长表需横向拖动（展厅既有做法，未自创替代方案）。 |
| 5 | Implementation Integrity | **4/4** | detect 0 findings；无占位符残留（`{{` 计数 0）；数据全部可回溯到 `435-核源台账-研析.md` 的逐字引用；封闭词汇表 `.metrics/.verdict/.timeline/.evidence` 齐备且语义正确（1 组 metrics、8 个 metric、1 个 verdict、9 个 timeline-item、10 个 evidence-item）。 |
| | **合计** | **16/20** | **Good**（弱项为 a11y/perf 的既有模板继承项） |

### 2.4 polish（agent 侧终检，按 reference/polish.md；共 8 项修复）

真实渲染后逐项修，非凭代码想象：

1. **字体路径 404**：`@import` 与 `@font-face` 原写 `../../assets/…`，而作品位于 `works/YYYY-MM-DD/research/`（三层深）→ 改 `../../../assets/…`。修复前 `requestfailed` 2 条，修复后 0 条，`h1` 计算字体为 `Noto Serif SC`。
2. **关键数据网格空洞**：`repeat(auto-fit,minmax(196px,1fr))` 在 1260px 下切出 5 列，8 个数留下 2 个空格 → 固定 `repeat(4,minmax(0,1fr))`，并在 ≤980px 降为 2 列、≤640px 降为 1 列。复验：`n=8, cols=4`，无空洞。
3. **大数字拆字**：`166.19 美/元` 断行 → 字号 33→29px、行高 1.06→1.14、加 `word-break:keep-all`。复验：8 个值中仅 `1 万亿~1.2 万亿美元` 合理折为两行。
4. **表首列拆字**：`费城半导体指/数` → `.tbl td:first-child{white-space:nowrap}`。
5. **涨跌不可扫读**：涨跌幅列加 `.up`（陈铜）/`.down`（深朱砂）着色，16 格中 3 涨 12 跌 1 中性；两色在纸底与陈铜底上实算 4.97:1 / 5.56:1。
6. **正文与表格数值不一致**：权力层级「产能」层原写「闪迪跌超 4%、SK 海力士 ADR 跌约 3%」→ 与表一统一为 -4.1%、-3.19%、-0.67%。
7. **措辞**：「有分析师 Dan Niles 在事件前警告」→「分析师 Dan Niles 在事件前警告」。
8. **破折号密度**：`——` 由 6 处降至 4 处（保留标题与两处必要处）。
9. **事实精度**：抬头与核心判断原写「同时换掉 CEO 与董事会议长」——董事长一职是**新设**而非替换，且「议长」非中文公司治理用语 → 改为「同一天换掉 CEO、新设董事会主席」。
10. **相对日期歧义**：时间轴「下周二」改为「11 月 17 日（下周二）」，条目标题直接写「11-17 财报与 11-18 国会简报」。
11. **终稿复验**：改后重跑 `detect --json` = 0 findings；断言闸门 `declared: 8`；自动抽取 L0 仍为 4 条完整标签，无新增截断。

polish 后复跑：detect 0 findings · 断言 8/8 过闸 · 渲染无失败请求、无 console 错误。

---

## 三、断言层（8 条，全部过闸）

```bash
cd /app/working/shared/showcase && python3 - <<'PY'   # 复用 tools/claim_gate.py 的 G1/G2
```

结果：`declared passed: 8 / 8`；自动抽取 L0 仅 4 条且标签完整（`166.19 美元|英伟达 11-12 收盘价`、`148.80 美元|英伟达 11-12 盘中新低`、`-0.54%|费城半导体指数 · 11/12 单日跌幅`、`51%|英伟达要求云伙伴为非中国企业保留的服务能力下限`），**无硬截断标签**。

| value | label | quote 出处（逐字命中） |
|---|---|---|
| 166.19 美元 | 英伟达 11-12 收盘价 | 财华社 11-13 |
| 148.80 美元 | 英伟达 11-12 盘中新低 | 财华社 11-13 |
| 10,506.67 点 | 费城半导体指数收盘点位（11-12） | 期货 11-12 |
| -0.54% | 费城半导体指数 · 11/12 单日跌幅 | 澎湃新闻 11-13 |
| 5.11% | 10年期美债收益率（11-12收盘口径） | 期货 11-12（原文 5.1129%） |
| 4.86% | 2年期美债收益率（11-12收盘口径） | 期货 11-12（原文 4.8645%） |
| 51% | 英伟达要求云伙伴为非中国企业保留的服务能力下限 | 新浪新闻 11-12 引《金融时报》 |
| 1 万亿~1.2 万亿美元 | 机构估算的「被罢免」情形市值蒸发区间 | 财闻引《福布斯》11-12 |

标签一致性由人工逐条比对，比对表见 `435-口径台账-研析.md` 第一节。

---

## 四、事实口径执行说明（派单最易错处）

| 派单要求 | 本篇处置 | 证据位置 |
|---|---|---|
| 按「已辞任」写，不得写「拟罢免」 | 全文以 11-12 晚公告为基准；「准备罢免」只出现在 11-11 时间轴条目并带《福布斯》出处 | 时间轴第 5、4 条 |
| 辞任原因不得写成已认定事实 | 页脚首条明确「官方公告未披露原因，媒体称与个人丑闻及独立调查有关」；正文引董事会声明「没有理由相信国家安全或机密信息遭到泄露」 | colophon 第 2 条、时间轴第 2 条 |
| 收盘口径择一并标注时点 | 采用 166.19 美元 / -4.34% / 4.01 万亿美元；165.880 美元标注为财联社盘中快照并说明判定依据；148.80 美元只作盘初叙述 | 关键数据 note、表一、colophon 第 3 条、`435-核源台账` ② |
| 1 万亿~1.2 万亿须标明机构估算 | 指标名即含「机构估算」，note 与证据出处均标「公告前的情景预期」 | 关键数据 note、证据第 9 条 |
| 51% 须注明《金融时报》 | 指标名与证据均标「据《金融时报》」，并并列 The Information 的「非强制指导、只针对未来合同」限定 | 指标第 7 格、权力层级「采购」层 |
| 费半 11-11 +5.66% 与 11-12 须分日标注 | 时间轴 11-11 条与表一分别带日期 | 时间轴第 4 条、表一 |
| 台积电入股 / 平头哥 / 美团 LongCat 只作同期背景 | 单列「同期背景」note，各带日期与来源，并写明「不能并入英伟达事件链当作因果」 | 「接下来看三件事」节末 note |
| 不重复 #429 定价日历、#432 资金闭环 | 正文无 70~78 美元/股、8.25 亿股、11-19 上市、904 亿、260 亿配售名单；股权层只用 CoreWeave/Nebius 当日跌幅作定价证据 | `435-核源台账` ⑩ |

---

## 五、验证

- 已验证：断言 8/8 过 G1（quote 逐字命中）与 G2（标签不属可疑）—— 方法：`tools/claim_gate.py` 的 `declared_claims/filter_declared` 同源逻辑 —— 结果 `declared passed: 8`。
- 已验证：`impeccable detect` 对终稿 0 findings（退出码 0；`--json` 复跑 `findings: 0`）。
- 已验证：真实 Chromium 渲染（1260×950 与 375×820）—— 无 `requestfailed`、无 console 错误、`document.body.scrollHeight=12057`、375px 无横向溢出、`.metrics` 4 列 8 格无空洞。
- 已验证：对比度实算 9 类文本全部 ≥4.5:1（方法见 2.3）。
- 已验证：标签逐字沿用 —— 与 `manifest.json` 中 #429/#432/11-06/11-08 已入库标签逐条比对，见 `435-口径台账-研析.md` 第一节。
- 未验证：英伟达官网英文公告原文未直接抓取（正文引用来自 21 经济网/21 世纪经济报道两独立中文源，同口径）。确认方法：nvidianews.nvidia.com 11-12 存档。
- 未确认：10 年期 / 2 年期收盘读数的 1~3 个基点跨源分歧成因。确认方法：WSJ TMUBMUSD10Y／02Y 与 MarketWatch 收盘行，或 Bloomberg／Refinitiv 单一终端。已在正文与页脚公开该分歧区间，断言取所引原文读数、不取平均。

---

## 六、未做

- 未跑 `tools/autopublish.sh`、`tools/build_manifest.py` —— 派单禁令（总指挥在收敛）。
- 未手工改 `manifest.json` / `index.html` / `enrich.json` —— 同上。
- 未做 11-13 美股行情 —— 数析核对表截止为美东 11-13 14:03，当日尚未收盘。
- 未加入 Anthropic IPO 定价与配售结构内容 —— 属 #429/#432 范围，主动避让。

## 七、待确认（请总指挥裁定）

1. **标题口径**：派单标题为「14 小时」，本篇改「14 个点」。理由：可核数据是盘初 -14.35%、收盘 -4.34%，无来源支持 14 小时时长。若须逐字沿用派单标题，改 `<title>` 与 `<h1>` 两处即可，正文与断言不受影响。
2. **新标签 `英伟达 MM-DD 盘中新低`**：是否入家族（后续盘中极值是否统一用此写法）。
3. **收益率取值**：断言用期货读数 5.11%／4.86%；数析多源互证主值为 5.13%／4.88%。本篇为保 quote 逐字可溯取前者并公开区间。若总指挥要求改后者，需同步替换证据条目。
4. 是否需要在正文增列 11-12 尾盘股指期货结算（数析已备好，当前仅用纽约尾盘现货）。
