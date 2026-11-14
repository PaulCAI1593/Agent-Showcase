# 《卖算力的人在招股书上掏钱》交付报告 · 选题 432（研究类）

> 成品：`works/2026-11-12/research/2026-11-12-anthropic-ipo-capital-loop.html`（102,884 B，单文件）
> sha256：`3f5da5912a50c8b7d30813e6e7ff0ab12bb336d67b0708c217b57e5a8920a725`
> mtime：2026-11-12 16:31:48 UTC（= 2026-11-13 00:31:48 Asia/Shanghai）
> 追踪线 beat：`估值与资本`（`<meta name="showcase-beat">` 与抬头 `<dt>追踪线</dt>` 一致）
> 报告补写：2026-11-13 05:57—07:0x（Asia/Shanghai），执行：研析；派单：总指挥 2026-11-13 04:08（第二次派发，原 `task-1a595f3c841c` 被 MiniMax 配额 2056 挡住）
> 本次**只补交付报告，未改作品 HTML**：补写前后 sha256 一致（见文末「未做」）。
> 配套台账（同目录）：`432-口径裁定-总指挥.md`、`432-核源台账-研析.md`、`432-口径核算-数析.md`、`432-图表数据-数析.json`

---

## 一、impeccable 已执行（规则 14 留痕）

工具：`/app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable`，版本 `4.7.1`（`--version` 退出码 0）。

该发行版的 CLI 只有 8 个动词：`detect` / `ignores` / `help` / `install` / `link` / `update` / `check` / `telemetry`。
**`audit` 与 `polish` 不在 CLI 里**，二者是 skill 的 agent 侧作业手册（`reference/audit.md`、`reference/polish.md`）。故下表分开记：CLI 能跑的命令记命令与退出码；agent 侧作业记执行方式与结论。

### 1.1 context（上下文装载）

```bash
cd /app/working/shared/showcase
/app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable \
  context --target works/2026-11-12/research/2026-11-12-anthropic-ipo-capital-loop.html
```

退出码 **0**。输出为指令块 + `RESOLVED_CONTEXT`：

| 字段 | 值 |
|---|---|
| targetPath | `works/2026-11-12/research/2026-11-12-anthropic-ipo-capital-loop.html` |
| targetExists | true |
| projectRoot / repoRoot | `/app/working/shared/showcase` |
| hasVisualImplementation | true |
| productPath / designPath | null（本仓库无 PRODUCT.md、无 DESIGN.md） |
| surfaceBriefPath | null（surfaceBriefReason: not-found；候选 brief 指向另两件作品，与本件无关） |

指令块要点：`NO_PRODUCT_MD` / `BUILD_INIT_REQUIRED` / `SCOPED_EXISTING_ALLOWED` / `EXISTING_VISUAL_SYSTEM` —— 本件属「窄口径精修」，可用既有实现为权威，**不得新造视觉世界**；`init` 只作为后续选项，不阻塞交付。

### 1.2 detect --json（首轮与终轮）

**首轮（口径修订前，研究目录内原件）** —— 原始会话的工具输出原样记录（历史会话 tool 结果）：

```
0 anti-patterns found.

── Advisory (not counted as failures) ──

/app/working/shared/showcase/works/2026-11-12/research/2026-11-12-anthropic-ipo-capital-loop.html
  [low-contrast] 4.2:1 (need 4.5:1) — text #646b67 on #dfe4e0   （×2）
  [em-dash-overuse] 50 em-dashes in body text

3 advisory notes. Suppress with --no-advisory.
EXIT:0
```

- 退出码 **0**；findings（失败项）**0 条**；advisory **3 条**（2 条对比度建议 + 1 条破折号密度建议，均不计入失败）。
- 补测：`notes/2026-11-12-anthropic-ipo-capital-loop.html.bak.20261112-081806`（首稿快照，61,299 B）上重跑 → 退出码 0、1 条 advisory（`em-dash-overuse` 50 处）。该路径下探测器降级为 regex-only（需解析页面的 `low-contrast` 等规则未跑），故对比度项不能由该快照复现。

**终轮（现行件）** —— 本轮实测：

```bash
cd /app/working/shared/showcase
/app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable \
  detect --json works/2026-11-12/research/2026-11-12-anthropic-ipo-capital-loop.html
```

- 退出码 **0**，stdout 为 `[]`（findings 0、advisory 0）。
- 同件 text 模式退出码 **0**，输出 0 字节（该版本对完全干净的文件不打印任何内容）。

| 轮次 | 退出码 | findings | advisory | 说明 |
|---|---|---|---|---|
| 首轮（口径修订前） | 0 | 0 | 3 | 2× low-contrast 4.2:1（#646b67 / #dfe4e0）、1× em-dash-overuse 50 |
| 终轮（现行件） | 0 | 0 | 0 | `detect --json` → `[]`；text 模式无输出 |

**两条 advisory 为何消失（已实测）**：现行件渲染实测，全部 `--ink-3`（#646b67）文本的有效底色是 `#eaedea`（--paper）、`#f4f6f4`（--paper-raised）、`#eaece7`（.loop-col-mid）三种，**没有一条落在 `#dfe4e0`（--rule-soft）上** —— `--rule-soft` 在本件只作为卡片间隙与描边露出（`.metrics` / `.loop` 的 grid 容器底色），不承载文本，4.2:1 的配对已不存在。破折号由 50 处降到 34 处，密度 0.31 处/500 字符，低于探测器约 1 处/500 字符的触发线。

### 1.3 audit（agent 侧技术审计，五维）

CLI 不可用，已实测确认：

```bash
/app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable \
  audit works/2026-11-12/research/2026-11-12-anthropic-ipo-capital-loop.html
# → stderr: Unknown command: "audit"   退出码 1
```

退出码 **1**（= 命令错误，非缺陷）。审计按 `reference/audit.md` 的五维清单执行，证据来自 Chromium 实加载（`/usr/bin/chromium`，Playwright，viewport 1260×800）与源码核对：

| # | 维度 | 分数 | 关键结论与证据 |
|---|---|---|---|
| 1 | Accessibility | 3/4 | 运行时逐个文本节点计算对比度（遍历 `document.body` 文本节点 → 取有效底色 → WCAG 相对亮度公式）→ **不达标 0 处**；正文阈值 4.5:1、大字 3:1。标题层级 h1×1 → h2×11 → h3×4，**无跳级**；`:focus-visible{outline:2px solid var(--brass);outline-offset:3px}` 存在；`<html lang="zh-CN">`、viewport meta 齐备；4 张 canvas 均带 `role="img"` + `aria-label`；10 张表全部有 `<caption>`；reduced-motion 有**保状态**的替代（`html{scroll-behavior:auto}` + `.rule-draw{transform:none!important;transition:none!important}`），且 reduced-motion 下 4 张 canvas 的绘制像素数与常规完全相同（图表静态绘制，不依赖动画）；页面自身 0 个 `<img>`、0 个表单、0 个交互控件。扣分项：未用真实读屏软件（NVDA / VoiceOver）实测朗读顺序 |
| 2 | Performance | 4/4 | 102,884 B 单文件；外部依赖仅 1 个本地 vendor 脚本 `assets/vendor/npm_chart.js_4.4.1_dist/chart.umd.min.js`；远程 `src`/`href` 0 处；图片 0 张；动画只动 `transform`（`.rule-draw`，`will-change:transform` 精确落到该类 1 处，未滥用）；4 张 canvas 由 Chart.js 一次性绘制，非逐帧重绘 |
| 3 | Theming | 3/4 | `:root` 16 个语义 token；作品自身 CSS 里另有 8 个硬编码 hex（深色面板 `#f2e6cd`/`#2b322d`/`#eaece7`/`#c9d0ca`/`#f0e7d6`、滚动条 `#c2c9c4`/`#a9b2ac`、`.verdict-note b`）。扣分项：canvas 绘图 JS 在脚本内自带 6 个硬编码色（`var BRASS='#7d5a1c', WASH='#ecdfc0', BLUE='#1f5f8b', RULE='#dfe4e0', INK='#4f5551', GREY='#c9d0ca'`，第 1485 行）复刻 token 色，未从 CSS 变量读取；另 5 个硬编码 hex（`#0b0c12`/`#f0c27f`/`#a78bfa`/`#f5e6c8`/`#14130f`）属发布管线注入的 showcase-bar / backlink，非本作品代码 |
| 4 | Responsive | 4/4 | 实测 375 / 768 / 1440 三档，`documentElement.scrollWidth == clientWidth`（375/375、768/768、1440/1440），**无横向滚动**；断点 1000px（`.loop` 转单栏）+ 640px；`@media (prefers-reduced-motion:reduce)` 单独成块。页面自身无交互控件，触控目标项 N/A（仅 2 个发布管线注入的链接） |
| 5 | Implementation Integrity | 4/4 | detect 终轮 0 findings、运行时 0 pageerror / 0 console.error；8 条断言全过闸门（见第五节）；beat 名与抬头一致；页面是本选题特有的结构（12 个 section、11 段 h2：结论 / 关键数据 / 资金闭环 / 配售名单 / 四口径估值 / 904 亿自洽校验 / 1205 亿单子 / 英伟达市值 / 定价时间轴 / 五个风险点 / 一手证据），不是可互换的模板 |
| | **总分** | **18/20** | **Excellent（minor polish）** |

### 1.4 polish（agent 侧交付前精修）

CLI 不可用，已实测确认：

```bash
/app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable \
  polish works/2026-11-12/research/2026-11-12-anthropic-ipo-capital-loop.html
# → stderr: Unknown command: "polish"   退出码 1
```

退出码 **1**（= 命令错误，非缺陷）。按 `reference/polish.md` 的「系统 → 证据 → 分级 → 整条路径」四步做只读精修检查（本次不得改 HTML，故只判定、不落笔）：

| 级别 | 检查项 | 判定 |
|---|---|---|
| P0 | 任务是否阻断、状态是否误导、路径是否不可达 | 无。页面为单页长文，无任务流；口径限定语与「推算 / 未确认」标注均在正文显式写出（页尾自述「标注『推算』的数值由本页算式给出，不作事实陈述；标注『未确认』的项写明了确认方法」） |
| P1 | 加载 / 空 / 错误 / 成功态 | 不适用（静态单页，无异步态） |
| P2 | 响应式与设计系统漂移 | 无。3 档视口无横向滚动；`.evidence` / `.evidence-item` / `.evidence-quote` / `.evidence-source` 为封闭词汇表类名，自创类只作视觉外壳 |
| P3 | 视觉与动效一致性 | 无。唯一动效是 `.rule-draw` 的 scaleX 描绘，reduced-motion 下有保状态替代 |
| P3 | 代码与资产清理 | 1 处可优化项：canvas 绘图色值硬编码（见 1.3 第 3 维）。**本轮不修** —— 改它会动作品 HTML，违反本轮禁令且破坏棘轮与断言序列；登记为待确认项 |

精修结论：**未发现需要在本轮改动的项**；唯一 P3 项（canvas 调色板未 token 化）因禁令未处理，已列入「待确认」。

---

## 二、`design_scan.py --scope file:` 结论

```bash
cd /app/working/shared/showcase
python3 tools/design_scan.py --scope file:works/2026-11-12/research/2026-11-12-anthropic-ipo-capital-loop.html
```

退出码 **0**，输出：

```
扫描 1 件作品 · findings 0 条 · 涉及 0 件
严重度分布: {}
规则 Top:

（非全量扫描：只报告，不比棘轮）
```

结论：本件 **0 findings**，严重度分布为空。

**附（全库棘轮复核）**：该命令会把 `tools/design_snapshot.json` 覆写为本次单件快照（工具自身的副作用，见「未做」第 3 条）。为把该文件恢复成全量语义，另跑了一次：

```bash
cd /app/working/shared/showcase && python3 tools/design_scan.py --scope all
```

退出码 **0**：`扫描 136 件作品 · findings 1665 条 · 涉及 107 件`，严重度分布 `{'warning': 1285, 'advisory': 380}`，规则 Top 首项 `low-contrast 1004`，末行 **`✓ 棘轮通过：无一规则上升（基线 1665 → 当前 1665）`**。

---

## 三、`audit_pages.py` 结论

```bash
cd /app/working/shared/showcase
python3 tools/audit_pages.py works/2026-11-12/research/2026-11-12-anthropic-ipo-capital-loop.html
```

退出码 **0**，输出：

```
巡检 1 件作品（真实加载 + 抓运行时错误）

========================================================
巡检完成：1 件，0 件有问题
✓ 全部作品页运行时健康
```

结论：Chromium 真加载 + 抓 pageerror / console.error / 资源 404 / 首屏可见叶子数 / 主容器隐藏数，**5 类检查全部未命中**，0 件有问题。

补充实测（本次另做，与巡检同法）：`pageerror` 0 条、`console.error` 0 条、首屏可见叶子数正常、4 张 canvas 均有非零绘制像素。

---

## 四、`build_manifest.py --check` 结论

```bash
cd /app/working/shared/showcase && python3 tools/build_manifest.py --check
```

退出码 **0**，输出：

```
扫描作品      : 134
research      : 69
creative      : 65
total         : 134
latestDate    : 2026-11-12
可用标签      : 262

[check] manifest 与磁盘 一致
  护栏: index.html 215KB / 预算 400KB · EMBEDDED 152KB · 7 个月份
  断言: 1221 条 · 覆盖 128/134 件 (96%) · 待处理 584 · 无结构 8 · 重校验 1221/1221 通过
```

结论：**退出码 0**；manifest 与磁盘一致；134 件（research 69 / creative 65）；断言 **1221 条，重校验 1221/1221 全过**；本件 8 条声明断言未被闸门拦截（见第五节）。

> 说明：`--check` 分支在 `build_manifest.py:968`（`if check_only:`）进入，`:979` 处 `return 0 if (same and not probs) else 1`，早于 `:981` 的 `open(MANIFEST,'w')` 写盘 —— 本次执行**未写 manifest.json / index.html**（源码已核）。

---

## 五、断言层自检（8 条）

### 5.1 声明块与闸门

| 项 | 值 |
|---|---|
| 声明块 | `<script type="application/json" id="claims">`，文件第 **1430—1473 行** |
| 条数 | **8** |
| 闸门结果 | `claim_gate.filter_declared()` → 通过 **8/8**（G1 引用命中、G2 标签非句式、G4 非页面自身计数行，均过） |
| 屏蔽清单 | `deny_filter()` 丢弃 **0** 条，入库 **8** 条 |
| manifest 落库 | `manifest.json` 中本件 claims 数组 = 8 条，`beat_declared: true`，`beat: 估值与资本` |

### 5.2 逐条列出

| # | value | label | quote | quote 落点（现行件行号） |
|---|---|---|---|---|
| 1 | 70 至 78 美元/股 | Anthropic IPO 定价区间（11-11） | `Anthropic IPO 定价区间出炉：每股 70 至 78 美元，目标完全摊薄估值 1.4 万亿美元` | 1395 · `.evidence-quote` |
| 2 | 260 亿美元 | Anthropic IPO 私募配售规模（11-11） | `另有260亿美元私募配售` | 1391 · `.evidence-quote` |
| 3 | 1.4 万亿美元 | Anthropic IPO 目标完全摊薄估值（11-11） | `完全稀释约1.4万亿美元` | 1391 · `.evidence-quote`（与第 2 条同一引用块内） |
| 4 | 1205 亿美元 | Anthropic—SpaceXAI 算力服务协议金额上限 | `we agreed to spend an aggregate of up to $120.5 billion over terms extending into 2029` | 1290 · `.evidence-quote`（S-1/A 一手逐字） |
| 5 | 168.89 美元 | 英伟达 11-10 收盘价 | `英伟达跌5.53%收168.89美元创近半年新低` | 1399 · `.evidence-quote` |
| 6 | 9998.33 点 | 费城半导体指数收盘点位（11-10） | `费城半导体指数跌0.35%报9998.33点` | 1205 · `.timeline-detail` |
| 7 | 4.99% | 10年期美债收益率（11-10收盘口径） | `10年期收益率盘中一度触及5%，收于4.99%` | 1403 · `.evidence-quote` |
| 8 | 1.1万亿 | Anthropic IPO传闻估值 | `Anthropic IPO 传闻估值降至 1.1 万亿` | 886 · 口径登记段正文 |

**标签逐字合规**：第 6、7 条沿用 #429 的 canonical 标签（`费城半导体指数收盘点位（11-10）`、`10年期美债收益率（11-10收盘口径）`）；第 8 条 `Anthropic IPO传闻估值` 仍挂 1.1 万亿，**1.4 万亿未写进该旧标签**，另立新标签 `Anthropic IPO 目标完全摊薄估值（11-11）`（第 3 条）—— 与裁定单要求一致。

### 5.3 quote 逐字命中方式

命中判定用的是仓库自己的闸门实现 `tools/claim_gate.py`，与 `build_manifest.py` 入库路径同一条：

1. 正文侧：`strip_code(html)` —— ① 先剥 HTML 注释；② 再剥 `<script>` / `<style>`（**顺序不可反**，否则注释里出现的字面 `<script id="claims">` 会把正文整段吃掉）；③ 清空 `<title>` 与 `<h1>`；④ 剥页面架构元素（chrome）。
2. 归一化：`normalize()` —— 去标签 → 压掉全部空白 → 去掉 `_PUNCT_STRIP` 里的中英文标点（`，。、；：""''（）()·—…!！?？「」《》`）。
3. 引用侧：对 quote 做同一套 `normalize()`。
4. 判定：`normalize(quote) in nbody` —— 即**去空白、去标点后的逐字命中**；命中即 G1 通过（原文存在该命题）。
5. 追加两道：`is_suspect_label()`（G2，标签不得像句子）+ `META_LABEL`（G4，标签不得是页面自身计数行）；再过 `deny_filter()`（人工屏蔽清单）。
6. 复核（本次另做，与第 4 步互补）：在**原始 HTML 文本**上做「空白不敏感」的整行定位，得到上表行号，确认每条 quote 都落在正文的真实元素里（`.evidence-quote` / `.timeline-detail` / 正文段），不是落在 `script#claims` 块内自证。

实测：**8/8 条 G1 命中、8/8 条 G2 通过、0 条被 deny 丢弃**。上表 8 条 quote 的落点行号均可复核。

---

## 六、三处口径更新说明（相对 #429）

#429（11-11 已交付《Anthropic IPO 定价窗口》）是同日同题材的前作。本件是定价结果与资金结构，不与之重叠。以下三处是本件相对 #429 的口径推进。

### 6.1 904 亿 = 含老股的交易总额；公司到手约 885.05 亿

- 页面位置：「904 亿怎么凑出来的：一次自洽校验」段（表四 募资口径自洽校验、表五 8.25 亿股的内部结构、表六 十倍缺口：分母要分「交易总额」与「公司实收」两个）。
- 算式：8.25 亿股 × 78 美元 = 643.5 亿（与原文「总价值约为 643.5 亿美元」逐字一致），+ 私募配售 260 亿 = **903.5 亿**，四舍五入即原文「合计融资最高约 904 亿美元」（差额 0.5 亿，0.0553%）。改用下沿 70 美元则差 66.5 亿（7.36%），量级完全不同，可证「最高」指上沿。
- 股数拆分（11-10 修订稿一手）：新发 8.01351354 亿股 ≈ 625.05 亿（归公司）＋ 现有股东出售 2364.8646 万股 ≈ 18.45 亿（老股东，公司不获此款）＋ 私募配售 260 亿（公司收全额，承销商不收折扣）→ **公司实收约 885.05 亿**（推算：625.05 + 260，未扣承销费与发行费）。
- 两个必答问题的页面答案：① 配售算不算在 904 亿里 —— **算**（「另有 260 亿」的「另有」是增量，若配售股已含在 8.25 亿股内则合计应为 643.5，904 不成立）；② 新股里含不含老股 —— **含**（8.25 亿股是本次公开发行的总股数，其中 2364.8646 万股由部分现有股东出售）。
- 页面明示相对 #429 的更新关系：「这是相对 #429 的口径更新：11-11 那篇当时只能写『原文未说明是否含老股』」。缺口倍数因此分两个分母：9009 ÷ 904 = **9.97 倍**（交易总额口径），9009 ÷ 885.05 = **10.18 倍**（公司实收口径）。
- 页面同时禁止的读法：不写「Anthropic 融到 904 亿」；904 亿是交易总额，不是公司到手金额。

### 6.2 1205 亿 = SpaceX.AI 算力服务协议的**金额上限**（付款方 Anthropic / 收款方 SpaceX.AI，英伟达非该协议收款方）

- 页面位置：「1205 亿这笔单子：签约方、性质与期限」段（表七 供应商承诺：11-10 修订稿的一手口径；表八 1205 亿的相对规模）。
- 简报原话是「与 SpaceX 签订 1200 亿美元英伟达 GPU 采购协议」，是取整转述。回到 11-10 修订稿原文：金额**上限 1205 亿美元**，签约方是 Anthropic 与 SpaceX 旗下 **SpaceX.AI**。
- 方向写死：**付款方 Anthropic，收款方 SpaceX.AI**；英伟达只是这块算力的**芯片供应商**，不是这笔协议的收款方。页面在配售名单表内也同步改写英伟达那一行（「其 GPU 是 SpaceXAI 算力服务的硬件来源；那笔协议的收款方是 SpaceX.AI，不是英伟达」）。
- 性质：算力**服务**协议，不是买断硬件；期限延续至 2029 年；2026 年 5—10 月间签订并修订多项协议；初始不可取消期结束后双方均可提前 90 天书面通知取消。
- 断言层标签：`Anthropic—SpaceXAI 算力服务协议金额上限`（值 1205 亿美元），quote 用 S-1/A 逐字句 `we agreed to spend an aggregate of up to $120.5 billion over terms extending into 2029`。
- 页面另外钉住两个读法边界：这 1205 亿不是本次募资款的去向，两份合同在 2026 年 4—10 月就签好了；Anthropic 与 SpaceX.AI 在这 1205 亿之间的分摊比例原文未披露（标「未确认」）。

### 6.3 估值改四口径：+1.5 万亿「承销团队考虑、未落地」带 11-12 时点，不覆盖 11-11 那条

- 页面位置：「四口径估值：1.02、1.4、1.5 与 2 万亿」段（表二 四口径估值的定义差、股数反推与相对 2 万亿的缺口；图三；表三 隐含倍数）。
- 四根柱子：① 基本市值 **约 1.02 万亿美元**（发行后基本总股本 × 78 美元，非摊薄）；② 完全摊薄估值 **最高约 1.4 万亿美元**（含员工期权、限制性股票、慈善捐赠配对预留股份）；③ **最低 1.5 万亿美元**（承销团队正在考虑的目标区间下沿，**11-12 时点，未落地**）；④ 此前市场讨论上限 **2 万亿美元**（机构施压前的讨论口径，不是披露值）。相对 2 万亿的低幅依次为 49.0% / 30.0% / 25.0%。
- 关键约束（页面原文）：「本篇把它单列为一个口径并带上 11-12 时点，**不覆盖 11-11 的 1.4 万亿，也不改动 11-11 那条标签**。」
- 标签层落实：断言层仍只有 `Anthropic IPO 目标完全摊薄估值（11-11）`（值 1.4 万亿美元），1.5 万亿**未进断言层**；页面上 1.5 万亿用独立标签 `Anthropic IPO 目标完全摊薄估值（11-12 承销团队考虑上调口径，未落地）`，带 11-12 时点与「未落地」限定。
- 三者关系页面写明：`Anthropic IPO传闻估值`（1.1 万亿，一级市场传闻口径，出处为 11-08 作品《AI 估值第一次撞上加息定价》）、`Anthropic IPO 目标完全摊薄估值（11-11）`（1.4 万亿，定价结果）、1.5 万亿（承销团队考虑中的目标）—— **不是同一指标，数值不可互换，也不可写成同一序列里的两期**。
- 股数列全部标「推算」（简报与招股文件报道均未披露股数与摊薄工具规模）；1.5 万亿相对 1.4 万亿高 7.14%（推算）。

---

## 七、未确认项

| # | 项 | 状态 | 本篇处理 | 确认方法 |
|---|---|---|---|---|
| 1 | **博通 1612 亿的出处未登记** | 未确认 | 该数在页内出现 4 处（第 620 / 731 / 1029 / 1376 行，五年期设备租赁租金总额、不含利息、用于 TPU 算力），**不入断言层**（断言层 0 条）。核源台账里它出自每经（2026-10-26 引首版招股书）的转述句；页面表七把整表归到「11-10 修订稿一手直取」，但 11-10 修订稿中承载 1612 亿的那一句原文未单独定位并登记 | 查 Anthropic, PBC S-1/A（2026-11-10）设备租赁条款原句，逐字定位 1612 亿所在句并登记进 `432-核源台账-研析.md` |
| 2 | **「募资是否含老股转让」在媒体原文里的自述** | 未确认 | 本篇用 11-10 修订稿的一手股数拆分（8.25 亿股 = 新发 8.01351354 亿 + 老股 2364.8646 万；「We will not receive any proceeds」）推定 904 亿含老股，属**推算式解答**，不是媒体原句的逐字确认 | 查路透/读创原文全文与 S-1/A「Use of proceeds」章节 |
| 3 | **外部原文未二次核验** | 未确认 | 本轮（补交付报告）未重新访问任何外部 URL。全部外部事实依据为 11-11 至 11-12 已抓取的 `432-核源台账-研析.md` 原文摘录与 S-1/A 一手直取文件（`https://www.sec.gov/Archives/edgar/data/2130357/.../anthropicpbc-sx1ax2.htm`，HTTP 200，14,798,492 字节） | 重新 curl 各原文 URL（财联社/东方财富、每经、央广网、腾讯新闻、FT、读创、香港经济日报），与台账逐字对照 |
| 4 | IPO Boutique「较预期低近 20%」的分母与基准 | 未确认（页内已登记） | 页面明写「这句话对应的分母与基准未确认，本篇不把它与任何比值并列计算，也不写入断言层」 | 查格隆汇 11-11 08:44 原文全文 |
| 5 | Anthropic 与 SpaceX.AI 在 1205 亿之间的分摊比例 | 未确认（页内已登记） | 页面标「未确认」，不据此推算 | 查 S-1/A 的 SpaceXAI Arrangements 分摊披露 |
| 6 | 摊薄增量约 48.72 亿股（1.4 ÷ 1.02） | 未确认（页内已登记） | 页面标为无法从公开报道验证，需查 S-1 的 Capitalization 与 Dilution 两节 | 查 S-1/A 该两节 |
| 7 | canvas 绘图色值未 token 化 | 已定位，未处理 | 本轮禁令要求不改作品 HTML，未动 | 改 canvas 取色为 `getComputedStyle` 读 CSS 变量；需另开一轮并重跑棘轮 |

---

## 八、未做（禁令遵守）

1. **未改作品 HTML**。补写报告前后 sha256 均为 `3f5da5912a50c8b7d30813e6e7ff0ab12bb336d67b0708c217b57e5a8920a725`，102,884 B，mtime 仍为 2026-11-12 16:31:48 UTC。
2. **未跑 `autopublish.sh`**，**未跑 `build_manifest.py` 的写盘分支**（只跑 `--check`；该分支 `build_manifest.py:968` 进入、`:979` 返回，不写盘）。manifest、index.html、缩略图均未由本次改动。
3. **副作用（已修复）**：`design_scan.py` 每次运行都会覆写 `tools/design_snapshot.json`。跑 `--scope file:` 会把该文件从全量快照（6,133 B）改成单件快照（249 B）；随后跑 `--scope all` 把它恢复为全量语义（`scope: all`、`scanned: 136`、`total: 1665`，文件回到 **6,133 B**）。`tools/design_baseline.json`（棘轮基线）**未被写入**（只有带 `--update-baseline` 才写），棘轮判定不受影响。除该快照文件外，未改任何其他文件。
4. 未动 `tools/claims_deny.json`、`tools/claim_changelog.jsonl`、其它作品、棘轮基线。

---

## 九、待确认

- 断言层是否需要为 1.5 万亿另立一条带「未落地」限定的指标条目（当前按裁定单不入断言层，只在页面与表格内呈现）—— 请总指挥定。
- 博通 1612 亿的出处是否补登记后进入断言层（当前按「出处未确认」排除）—— 请总指挥定。
- canvas 调色板 token 化是否另开一轮（会改作品 HTML，须重跑棘轮与断言序列）—— 请总指挥定。
