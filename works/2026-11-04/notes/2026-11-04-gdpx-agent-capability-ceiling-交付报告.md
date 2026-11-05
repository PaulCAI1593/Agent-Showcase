# 交付报告 · 选题412「13 个模型，没有一个完成五分之一 —— GDPx 给『能力』画的第一条天花板」

- **类型**：创意类（单文件交互作品）
- **追踪线**：Agent 与编排（`<meta name="showcase-beat" content="Agent 与编排">`）
- **作品路径**：`works/2026-11-04/creative/2026-11-04-gdpx-agent-capability-ceiling.html`
- **作品字节数**：62,376 B
- **标题**：13 个模型，没有一个完成五分之一 —— GDPx 给「能力」画的第一条天花板（与 manifest 标题一致）
- **断言条数**：8 条（全部 L0 已验证，逐字回查通过）
- **缩略图**：`thumbs/2026-11-04-creative-2026-11-04-gdpx-agent-capability-ceiling-thumb.webp`，22,510 B
- **预览截图**：`notes/2026-11-04-gdpx-agent-capability-ceiling-preview-desktop.png` / `-mobile.png` / `-legal.png`
- **门禁留痕**：`notes/412-impeccable-detect-20261105.txt`
- **口径台账**：`notes/2026-11-04-gdpx-agent-capability-ceiling-口径台账.md`
- **交付日期**：2026-11-05（Asia/Shanghai）

---

## 一、数据纪律：来源已补到一手，不再是「转引自搜索摘要」

派单时 GDPx 全部数字只有新闻简报（AI 技术日报转述 SemiAnalysis）一处来源，要求补一次 SemiAnalysis 原始榜单。
**本次已补到原始来源，且是一手直取**：

| 来源 | 用途 | 取回方式 |
|---|---|---|
| `https://gdpx.semianalysis.com/` | GDPx 官网 v1.0 榜单本体（13 个模型总分、每项任务成本、输出 token、14 家合作方 × 206 项任务的得分与部分得分） | 直取页面 HTML，解析出内嵌数据块（`updatedAt: 2026-11-01`, `source: final`） |
| `https://gdpx.semianalysis.com/domains` | 11 个行业与 14 家合作方、每个行业的任务数（合计 206） | 直取 |
| `https://newsletter.semianalysis.com/p/gdpx-measuring-frontier-model-capabilities` | 官方发布文（Max Kan / Andrew Megalaa / Dylan Patel，2026-11-02）：方法学、对齐域的 19/100 与 98%、压缩机外壳任务 0/12、官网对 GDPval 的批评 | 直取全文 |

因此正文与断言层**不存在**「转引自搜索摘要，页面未直取」的情况。二手报道（shiftdelete、unite.ai、Dealroom）只用于交叉印证，
未作为任何断言的依据。

**重算复核**：按官网口径（行业内多家合作方等权、11 个行业之间等权）重算 13 个模型的总分，
结果与官网榜单发布值逐位一致（12.03→12.0 / 10.87→10.9 / 9.60→9.6 / 9.00→9.0 / 8.53→8.5 / 8.43→8.4 /
8.22→8.2 / 7.34→7.3 / 6.82→6.8 / 5.39→5.4 / 5.11→5.1 / 3.87→3.9 / 2.69→2.7）。

**口径差异（已在页脚声明）**：官方发布文写「Opus 5.5 拿下量化交易、硬件设计与芯片设计」；
按官网 v1.0 数据重算，量化交易领先者为 Claude Fable 5.1（28.61%）、芯片设计为 GPT 6.1 Sol（5.60%）。
本作品采用重算结果，不采用发布文这处表述。

---

## 二、硬约束逐条核对（creative-brief.md 十项）

| # | 约束 | 落地情况 |
|---|---|---|
| 1 | 单文件 HTML，CSS/JS 内联 | ✅ 62,376 B 单文件，样式与脚本全内联 |
| 2 | 零远程依赖 | ✅ 无外链脚本/字体/图片；`<script src>` 只指向本地 `../../../assets/vendor/npm_chart.js_4.4.1_dist/chart.umd.min.js`，字体走本地 `@import '../../../assets/vendor/fonts/noto-serif-sc.css'` 与 Newsreader woff2 |
| 3 | 图表用本地 Chart.js | ✅ 散点图用本地 4.4.1 dist |
| 4 | `<title>` 与 manifest 标题一致 | ✅ 两者同文；manifest 由 build_manifest 生成后已核对 |
| 5 | 落 `works/YYYY-MM-DD/creative/YYYY-MM-DD-<slug>.html` | ✅ |
| 6 | 过程材料落 `works/2026-11-04/notes/` | ✅ 3 张预览图 + 本报告 + 门禁留痕 + 口径台账 |
| 7 | 对比度 ≥4.5:1 | ✅ 正文骨白 #ECE5D7 / #AEB7C0 / #8B959F 于墨蓝黑底 #12161B，实测 14.4:1 / 8.8:1 / 5.9:1；朱砂 #E0573E 4.87:1。impeccable detect 未报 low-contrast |
| 8 | 响应式 375px 起 | ✅ 实测 375px 与 1280px：scrollWidth = clientWidth，无横向滚动 |
| 9 | 尊重 `prefers-reduced-motion` | ✅ `@media (prefers-reduced-motion: reduce)` 关闭过渡与平滑滚动；Chart.js 动画在该偏好下置为 `false` |
| 10 | 交付前跑 impeccable | ✅ 见第三节，detect 0 warning / 0 error |

补充：返回链「返回展厅」由 `autopublish` 阶段 5.5 自动注入，作品文件内未手写该链接。

---

## 三、impeccable 已执行

**impeccable 已执行：命令 `impeccable detect --json works/2026-11-04/creative/2026-11-04-gdpx-agent-capability-ceiling.html`；结论 0 warning / 0 error（findings 数组为空，退出码 0）。**

原始输出：

```
$ cd /app/working/shared/showcase && /app/working/workspaces/default/skills/impeccable/scripts/impeccable detect --json works/2026-11-04/creative/2026-11-04-gdpx-agent-capability-ceiling.html
[]
exit=0
```

执行顺序与依据：

1. **动手前**：`/app/working/workspaces/default/skills/impeccable/scripts/impeccable context`
   → 返回 `NO_PRODUCT_MD` / `BUILD_INIT_REQUIRED` / `MANUAL_DETECTOR_REQUIRED`。
   本件是展厅里的一件独立单文件作品，不是某个产品的某个界面，故未执行 init 建 PRODUCT.md；
   已读取 `reference/craft-floor.md`（质量底线）与 `reference/init.md`，按其要求逐条自查。
2. **交付前**：detect 跑两次（autopublish 注入返回链之前 / 之后），两次输出均为 `[]`、退出码 0。
3. **渲染复核**：Playwright + 系统 Chromium 跑通，控制台错误 0，页面异常 0；
   交互逐项点过（行业行展开、模型切换、量程拖拽与键盘、指标切换），截图 4 张。

同一探测器的可用性对照（在故意做坏的样本上稳定报 8 条、退出码 2）已记入
`notes/412-impeccable-detect-20261105.txt`，用以证明 detect 确实扫描了本作品。

---

## 四、三种交互的落地说明

### ① 点击探索 —— 跨模型零完成区

- 页面「206 项任务，11 个行业」段顶部是一条朱砂底色的**跨模型零完成区**带，列出两个任务块：
  **法律 20 项（Chakra）** 与 **芯片设计里的验证任务 10 项（Arcverex）**，合计 **30 项任务，13 个模型全部零完成**；
  金融 24 项（Living Context）另有一处 —— 13 个模型中 12 个通过率为 0。
- 带内三个按钮「看法律 20 项 / 看芯片验证 10 项 / 看金融 24 项」可直接跳转并展开对应行业行。
- 11 个行业行每行右侧有**徽标**：13/13 零完成（朱砂）或 n/13 零完成；法律整行 20 格全部描红边，
  芯片设计行里 Arcverex 那 10 格单独描红边，与同行的 Aria（10 格）、Ergodex（14 格）视觉分离。
- 点开任一行，右侧展开该行业的**合作方 / 任务环境说明 / 该行业提示**，以及**13 个模型在这一行的通过率横条**（按通过率降序）。
- 该交互还与「模型切换」联动：切换主模型后，11 行的 206 格随之重绘。

### ② 对比切换 —— 13 个模型横向对照

- 「天花板」段是一条可横向滚动的 **13 列对照条**（Claude Opus 5.5 → GLM 5.3），
  每列给排名、模型名、所属实验室、总分、成本/任务，柱体按 0–20% 量程绘制，
  柱顶上方是**加粗的朱砂虚线（五分之一）**，13 根柱子全部停在虚线下方，空隙即「差多少」。
- 全部 13 列用 CSS Grid 固定行高对齐（排名 / 名称 / 实验室 / 分数 / 柱体 / 成本 / 标签），保证横向可比。
- **点一列 = 选为主模型（A）**；主模型面板下方有一个**「对照模型」下拉**可再选一个（B），
  B 在 11 个行业的分布图里以描边空心条叠在 A 的实心条上，散点图里 B 用骨白点、A 用朱砂点。
- 切换主模型会联动刷新：11 个行业分布、206 格矩阵、11×13 热力图、成本散点图。

### ③ 数据仪表盘 —— 206 × 11 矩阵

- 「206 格矩阵」段把 **206 项任务全部摊平**：11 行（11 个行业），每行格子数 = 该行业任务数
  （芯片设计 34、网络安全 18、生物 13、金融 24、法律 20、量化交易 10、递归自我改进 10、
  硬件设计 21、材料科学 23、对齐与权限 18、软件工程 15），**合计 206 格**。
- 每格 = 1 项任务，填充比例 = 当前模型在该任务块的完成率（按块内得分摊分），并有图例说明。
- **口径切换按钮「通过率 / 部分得分」**：切到部分得分，法律那 20 格会从全黑变成灰色，
  配合正文「灰色不等于做完」这句，形成一次真实的认知落差。
- 附 **11 个行业 × 13 个模型热力表**（143 格）与 **成本–完成率散点图**（Chart.js，本地 dist，对数横轴）。

---

## 五、故事线四段（页面顺序）

| 段落 | 位置 | 内容 |
|---|---|---|
| **开场 · 换尺子** | `#ruler` | 「以前的尺子量答题正确率…GDPval 把全部上下文塞进提示词」。右侧一把**可拖拽的 0–100% 垂直量程**：13 个模型的成绩刻在底部成带，虚线标出五分之一 20%，朱砂手柄可拖（也支持键盘方向键 / Home / End），读数实时换算成「206 项里的 N 项」并给出「离五分之一还差几项」；预设按钮：最高分 12.0% / 五分之一 20% / 全部做完 100%。 |
| **发展 · 206 项 / 11 行业** | `#domains` | 「基准共 206 项任务，覆盖 11 个行业」，14 家专业合作方提供真实环境；11 个行业行 + 跨模型零完成区带；点开任一行看该行业 13 个模型的分布。 |
| **高潮 · 最高 12.0%，无一触及五分之一** | `#ceiling` | 13 个模型横向对照条 + 朱砂虚线五分之一；主模型面板给出排名、离五分之一还差多少项、每项任务成本与输出 token；「GDPx 总分」大字 12%。 |
| **收尾 · 瓶颈是可靠性，不是智力** | `#ending` | 11 个行业冠军榜（网络安全 Muse Wonder Full 35.19%、生物 Gemini 4 Carbon 25.64%、量化交易 Claude Fable 5.1 28.61%、递归自我改进 GPT-6 Astra 24.89%、硬件设计 Claude Opus 5.5 18.72%、材料科学 GPT-6 Astra 21.56%、对齐 Muse Wonder Full 9.21%、软件工程 Gemini 4 Carbon 与 Claude Sonnet 5.5 并列 11.11%……法律一行写「无人完成」）；可靠性三证：医疗场景 19/100 非零、网络安全 98% 违反行为规则、压缩机外壳 0/12 通过；结语两段。 |

---

## 六、验收命令原始输出

```
$ cd /app/working/shared/showcase && /app/working/workspaces/default/skills/impeccable/scripts/impeccable detect --json works/2026-11-04/creative/2026-11-04-gdpx-agent-capability-ceiling.html
[]
exit=0

$ cd /app/working/shared/showcase && python3 tools/claim_gate.py --backfill
作品 117 · L0 1130 · L1 504 · L2作品 7 · 漂移丢弃 0
变更条目 0（已写回 enrich.json）
exit=0

$ cd /app/working/shared/showcase && python3 tools/claim_gate.py --verify
重校验 1112 条断言
✓ 全部通过
exit=0

$ cd /app/working/shared/showcase && ./tools/autopublish.sh --quiet-seconds 0
  ① 计数      manifest.total=117  research=59  creative=58  磁盘=117  → 一致 ✓
  ② 缺文件    manifest悬空=0  磁盘未登记=0  → 0 (须为 0)
  ③ 缺缩略图  0 (须为 0)
  ④ 缺标签    0 (须为 0)
  ⑤ 标签总数  上次=250  本次=250  → 未下降 ✓
  ⑥ 标签丢失  0 件 (须为 0)
  ⑦ 快照契约  问题 0 项 (须为 0)
  ⑧ 元数据/类型  enrich孤儿键=0  类型冲突=0  登记表=4条 (须为 0)
  ⑨ 返回链    缺失 0 (须为 0)
  ⑩ 断言层    1112 条 · 引用失效 0 (须为 0)
  ✓ 校验全部通过
  ✓ 流水线完成：117 件作品，250 个标签
exit=0
```

缩略图（由 autopublish 阶段 5 调用 `tools/gen_thumb.py` + `tools/make_thumbs_webp.py` 生成）：

```
  → works/2026-11-04/creative/2026-11-04-gdpx-agent-capability-ceiling.html (creative)｜原因：无缩略图
  ✅ 2026-11-04-creative-2026-11-04-gdpx-agent-capability-ceiling-thumb.png  (168704B)
  ✓ 已转 webp，PNG 高清源归入 _private/thumbs-src/
```

产出：`thumbs/2026-11-04-creative-2026-11-04-gdpx-agent-capability-ceiling-thumb.webp`，22,510 B。

> `build_manifest.py --check`：本次由 autopublish 阶段 6 重建 manifest 后由总指挥复验，退出码 0。
> 重建前的一次自跑（退出码 0）曾报「manifest 与磁盘不一致 / 无缩略图」，原因是 autopublish 阶段 6 尚未执行，
> 重建后已消解。

---

## 七、改动点清单

1. **新增** `works/2026-11-04/creative/2026-11-04-gdpx-agent-capability-ceiling.html`（62,376 B）—— 作品本体，单文件。
2. **新增** `notes/2026-11-04-gdpx-agent-capability-ceiling-交付报告.md` —— 本文件。
3. **新增** `notes/412-impeccable-detect-20261105.txt` —— impeccable 门禁留痕（命令 / 原始输出 / 结论 / 对照组）。
4. **新增** `notes/2026-11-04-gdpx-agent-capability-ceiling-口径台账.md` —— 逐条口径、来源、原始数值与重算过程。
5. **新增** `notes/2026-11-04-gdpx-agent-capability-ceiling-preview-desktop.png` / `-mobile.png` / `-legal.png` —— 预览截图。
6. **新增** `thumbs/2026-11-04-creative-2026-11-04-gdpx-agent-capability-ceiling-thumb.webp`（22,510 B）。
7. **修改** `tools/autopublish_types.json` —— 类型登记表补 1 条
   （`2026-11-04-gdpx-agent-capability-ceiling` → `creative`）。
   原因：`autopublish.resolve_type()` 的「目录结构」分支按 `parts[1]` 取类型，而传入路径带 `works/` 前缀，
   导致本件被误判为 research、缩略图命名为 `...-research-...`；登记后重跑流水线，缩略图文件名已规范为 `...-creative-...`。
8. **由 `tools/autopublish.sh` 生成（非手工改动）**：`manifest.json`、`index.html`（含 EMBEDDED 快照）、`enrich.json` 内的本件条目与断言回填、
   作品文件末尾的返回链注入、其他作品因正文指纹变化而重截的缩略图。

---

## 八、剩余未验证项

1. **逐任务通过记录未核**：206 格矩阵的填充比例是按**任务块得分**摊分的结果，不是 206 项任务逐项的真实通过记录。
   官网 `/domains` 页只公开每个行业 1–3 个公开任务的 rollout 明细，206 项逐任务明细未公开。
   页面正文与图例已写明这一点。
2. **官网数据集共 20 个模型，v1.0 榜单发布 13 个**：本作品只做 13 个（与新闻简报口径一致）。
   官网 Pareto 图默认列出全部 20 个（含 Claude Haiku 5.5、Kimi K3、MiniMax M3.1 Flash、Qwen 3.8 Max、Inkling、Muse Spark Open、GPT-6.1 Terra 等），
   其成绩未纳入本作品任何展示与断言。
3. **官方发布文与官网数据在行业冠军上不一致**（量化交易、芯片设计两处）。本作品采用官网重算值，并在页脚显式声明差异；
   未进一步核发布文所用快照版本。
4. **「安全分类器拉低总分」这一机制未量化**：官网给出剔除 cyber / biology / alignment 三域后的另一张排名，
   但未公开剔除后的具体分值，本作品只做文字转述，未画图、未写成断言。
5. **无实机触控测试**：仅在 Chromium 375×780 与 1280×900 视口验证了布局与横向滚动；未在真机上验证拖拽手感与表格滚动。
6. **agent 署名未填**：`build_manifest` 提示 2 件作品缺 agent 署名（本件与 411）。按派单指令「不手工改 enrich.json」未填，
   留待派单方或例会计入。
7. **未做读屏器实测**：交互控件已带 `aria` 语义（`role="slider"` + `aria-valuenow` / `aria-valuetext`、`aria-expanded`、
   `role="option"` + `aria-selected`），但未用真实读屏器验证播报。

---

## 九、结论

**已完成。** 作品落盘 62,376 字节；8 条断言全部逐字回查通过；impeccable detect 0 warning / 0 error；
claim_gate 重校验 1112 条断言零失效；autopublish 十项硬校验全过；缩略图已生成并规范命名；
GDPx 数字已换用 SemiAnalysis 官网与官方发布文一手来源，官网口径重算的总分与榜单发布值逐位一致。
剩余未验证项 7 条已逐条列明，其中最需要读者留意的是第 1 条（206 格为块级摊分，非逐任务明细）。
