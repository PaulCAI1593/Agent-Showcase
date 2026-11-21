# 456 补交付报告 · 2026-11-20《Anthropic 挂牌的五本账》

**已完成**：本单 6 项留痕全部写入本文件 —— ① 作品硬事实与版式取舍；② claims 7 条 label/value/quote 逐字列表；③ quote 逐字命中核对命令与输出（7/7）；④ 与 455《ANT 开钟时刻》的口径对账（含 1.405 万亿 / 1.5 万亿同日两值的判定与消歧方案、83 美元出处与 455 第四节未决项闭环）；⑤ 数据来源逐条列表；⑥ impeccable 执行记录与三条门禁命令原文输出（全部 exit 0）。

- 报告时间：2026-11-20 13:57 BJ
- 报告人：研析（research-analyst）
- 派单：【研析·#456 补交付报告·截止 11-20 15:00 BJ】
- **本单只写报告**：作品本体、455 作品与报告、claims 的 label/value/quote 一律未改；未执行 `git push`。
- **时区口径**：本报告文字用 BJ（Asia/Shanghai）。粘贴的命令输出里 `stat`/文件 `mtime` 为容器 OS 时钟（UTC），与 BJ 相差 8 小时（例：OS `Nov 20 01:09:15 +0000` = BJ `09:09:15`）。

---

## 一、作品硬事实与版式取舍

### 1.1 硬事实（脚本实测）

| 项 | 值 | 取证 |
|---|---|---|
| 作品路径 | `works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html` | `stat` |
| 体积 | **57,887 字节** | `stat -c '%s'` → `57887` |
| 文件 mtime | OS `2026-11-20 01:09:15 +0000`（= BJ 09:09:15） | `stat -c '%y'` |
| 改前备份 | 同目录 `…html.bak.20261120-010915`，54,584 字节 | `stat` |
| beat（追踪线） | **估值与资本** | `…html:50` → `<meta name="showcase-beat" content="估值与资本">` |
| 类型 / 日期 / 署名 | research / 2026-11-20 / **研析** | `enrich.json` → `agent: 研析`；作品内 `…html:412` `<dt>主责</dt><dd>研析</dd>`、`…html:506` 表 1 caption「（2026-11-20 · 研析）」 |
| manifest id | `item-2026-11-20-research-2026-11-20-anthropic-listing-ledger` | `manifest.json:10` |
| 缩略图 | `thumbs/2026-11-20-research-2026-11-20-anthropic-listing-ledger-thumb.webp`，21,176 字节 | `stat` |
| claims 条数 | **7 条**（派单建议 6 条 + 补入既有标签 1 条，3~8 区间内） | `…html:861` 起的 `script#claims` |
| 结构 | `<section>` 10 · h1 1 · h2 10 · `<svg>` 4 · `<canvas>` 2 · `<figcaption>` 4 · `<table>` 1 · 指标格 8 · `<button>` 0 · `addEventListener` 1 | `re` 统计 |
| 标签配平 | `div` 108/108 · `section` 10/10 | 构建期自检输出（见 6.1） |
| 远程依赖 | **0**（无 `http(s)://`、无协议相对引用；字体自托管 `@import` 相对路径 `…html:55`、`…html:58`） | `grep -oE '(src\|href)="[^"]*"'` 过滤后为空 |
| 占位符残留 | `{{` 出现 **0** 次 | `grep -c '{{'` → `0` |
| 上展状态 | 157 件之一，`build_manifest.py --check` 收录 | 见第七节 |

### 1.2 研究类「参考模板不套壳」的版式取舍理由

**规范依据**：`docs/OPERATIONS.md:350`（2026-11-05 表达口径：从 `templates/work.html` 起步，版式与信息组织按本篇内容重排，**禁止单纯复制模板版式与占位文案**）；`README.md:25`（研究类＝「参考模板不套壳」）；本次派单原文同口径要求。

**沿用模板的部分（参考）**

| 沿用项 | 说明 |
|---|---|
| 封闭语义词汇表 | 只用 `.metrics > .metric > (.metric-value/.metric-label/.metric-source)`、`.verdict-band > .verdict/.verdict`、`.timeline > .timeline-item`、`.evidence > .evidence-item`，不自创承载语义的 class（`…html:16-31` 契约注释） |
| 卷宗视觉基调 | 冷调档案纸（`--paper:#eaedea`）+ 墨色 + 陈铜（`--brass:#7d5a1c`）+ 衬线，与模板「档案卷宗」同族 |
| 自托管字体 | `@import ../../../assets/vendor/fonts/noto-serif-sc.css`、`Newsreader` woff2，离线可用（`…html:55`、`…html:58`） |

**按内容重排的部分（不套壳）**

| 取舍 | 理由 |
|---|---|
| 段落骨架从 4 段扩到 9 个内容段 | 模板只有 4 个 `<section>`，标题是占位符 `{{ 结论 }}`／`{{ 关键数据 }}`／`{{ 进程 }}`／`{{ 证据 }}`。本篇的骨架是「一笔一笔对账」，所以重排为 `figures`（关键数据 8 格）→ `ledger`（五本账对账表）→ `charts`（图 1–4）→ `sides`（撑住／质疑两边账）→ `macro`（经济金融视角）→ `governance`（安全与治理视角）→ `timeline` → `evidence` → `tbd`（未确认）。套模板壳会把对账表塞进四段通用结构，条理反而变差 |
| 新增模板没有的段 | `ledger` 对账表、`sides` 两边账、`macro`＋`governance` 两重视角（派单要求的「经济金融 + 安全与治理」多元化视角）、`tbd` 未确认清单 —— 这四类信息模板没有对应位置 |
| 图表优先、说明让给图 | 4 `<svg>` + 2 `<canvas>` + 1 张对账表，共 4 条 `<figcaption>` 逐图写口径与直除说明（`…html:577`、`…html:585`、`…html:622`、`…html:630`），符合「可多配图表、数据图、表格」 |
| 不复制占位文案 | `{{` 残留 0 处；全部 h2 为实义标题 |
| 朱砂只做批注色 | `--vermilion:#c44536` 只用于大号数值与示意标注，不做正文色（`…html:11-13` 视觉身份注释） |

---

## 二、claims 7 条 · label / value / quote 逐字列表

权威来源：作品内 `…html:861` 起的 `<script type="application/json" id="claims">`。`enrich.json` 中该作品条目与之**逐字一致**（下表由两处解析后比对，无差异）。

| # | value（数值） | label（指标名） | quote（回源用原文片段） |
|---|---|---|---|
| 1 | `83 美元` | `Anthropic IPO 定价（11-18）` | `83 美元 Anthropic IPO 定价（11-18）` |
| 2 | `70 至 78 美元/股` | `Anthropic IPO 定价区间（11-11）` | `70 至 78 美元/股 Anthropic IPO 定价区间（11-11）` |
| 3 | `1073 亿美元` | `Anthropic 合计募资额（11-18）` | `1073 亿美元 Anthropic 合计募资额（11-18）` |
| 4 | `1.5 万亿美元` | `Anthropic 完全稀释估值（11-18）` | `1.5 万亿美元 Anthropic 完全稀释估值（11-18）` |
| 5 | `332 亿美元` | `Anthropic 前三季度营收（2026）` | `332 亿美元 Anthropic 前三季度营收（2026）` |
| 6 | `约 9000 亿美元` | `Anthropic 算力与基础设施承诺总额` | `约 9000 亿美元 Anthropic 算力与基础设施承诺总额` |
| 7 | `155 美元` | `Melius 目标价（11-19）` | `155 美元 Melius 目标价（11-19）` |

- 标签家族：7 条全部以 `Anthropic ` 起头（第 7 条 `Melius 目标价（11-19）` 除外），第 2、6 条为派单指定**逐字复用的既有标签**，未改名、未加后缀（`…html:849-850` 页脚已声明）。
- 指标格共 **8 格**，第 8 格 `接近 7 倍` / `Anthropic 超额认购倍数（11-18）`（`…html:476-478`）**未入 claims**，见 4.7。

---

## 三、quote 逐字命中核对（命令与输出）

### 3.1 核对原理（复刻 `claim_gate.py` G1，非人眼判断）

G1 判定是确定性的：`quote 不在归一化正文 → 拒绝`。核对脚本复刻了 `tools/claim_gate.py` 的两个函数，**未改动该工具**：

- `normalize(s)`（`tools/claim_gate.py:122`）：去 HTML 标签 → 去全部空白 → 去 `_PUNCT_STRIP` 标点
- `strip_code(html)`（`tools/claim_gate.py:128` 附近）：**先剥注释、再剥 `<script>/<style>`**，得到「作品正文」

判定：`normalize(quote) in normalize(strip_code(全文))`

### 3.2 实际执行的命令与原文输出

```bash
cd /app/working/shared/showcase && python3 /tmp/verify_quotes.py works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html
```

原文输出（exit 0）：

```text
文件: works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html
claims 条数: 7
归一化正文长度: 5092 字符

idx | label | value | normalize(quote) | 命中
----------------------------------------------------------------------------------------------------
  1 | Anthropic IPO 定价（11-18） | 83 美元 | 83美元AnthropicIPO定价11-18 | 命中
  2 | Anthropic IPO 定价区间（11-11） | 70 至 78 美元/股 | 70至78美元/股AnthropicIPO定价区间11-11 | 命中
  3 | Anthropic 合计募资额（11-18） | 1073 亿美元 | 1073亿美元Anthropic合计募资额11-18 | 命中
  4 | Anthropic 完全稀释估值（11-18） | 1.5 万亿美元 | 1.5万亿美元Anthropic完全稀释估值11-18 | 命中
  5 | Anthropic 前三季度营收（2026） | 332 亿美元 | 332亿美元Anthropic前三季度营收2026 | 命中
  6 | Anthropic 算力与基础设施承诺总额 | 约 9000 亿美元 | 约9000亿美元Anthropic算力与基础设施承诺总额 | 命中
  7 | Melius 目标价（11-19） | 155 美元 | 155美元Melius目标价11-19 | 命中
----------------------------------------------------------------------------------------------------
逐字命中: 7/7
[附加] 「接近 7 倍 Anthropic 超额认购倍数（11-18）」归一化后在正文中: True
```

**判定：7/7 逐字命中（与总指挥 11-20 11:25 BJ 实跑的 7/7 一致）。**

核对脚本 `/tmp/verify_quotes.py` 全文（供复跑）：

```python
#!/usr/bin/env python3
import json, re, sys
PUNCT = '，。、；：""''（）()·—…!！?？「」《》'
def normalize(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\s+', '', s)
    for c in PUNCT: s = s.replace(c, '')
    return s
def strip_code(html):
    s = re.sub(r'<!--.*?-->', ' ', html, flags=re.S)
    s = re.sub(r'<(script|style)\b.*?</\1>', ' ', s, flags=re.S | re.I)
    return s
path = sys.argv[1]
raw = open(path, encoding='utf-8').read()
body = normalize(strip_code(raw))
m = re.search(r'<script\b[^>]*id=["\']claims["\'][^>]*>(.*?)</script>', raw, re.S | re.I)
claims = json.loads(m.group(1))
print(f'文件: {path}')
print(f'claims 条数: {len(claims)}')
print(f'归一化正文长度: {len(body)} 字符')
print()
print('idx | label | value | normalize(quote) | 命中')
print('-' * 100)
ok = 0
for i, c in enumerate(claims, 1):
    q = normalize(c['quote'])
    hit = q in body
    ok += 1 if hit else 0
    print(f'{i:>3} | {c["label"]} | {c["value"]} | {q} | {"命中" if hit else "未命中"}')
print('-' * 100)
print(f'逐字命中: {ok}/{len(claims)}')
extra = normalize('接近 7 倍 Anthropic 超额认购倍数（11-18）')
print(f'[附加] 「接近 7 倍 Anthropic 超额认购倍数（11-18）」归一化后在正文中: {extra in body}')
sys.exit(0 if ok == len(claims) else 1)
```

### 3.3 官方工具复核（同一 G1 的仓库内实现）

`python3 tools/claim_gate.py --verify` → 见第七节门禁 1 原文输出：**重校验 1383 条断言，✓ 全部通过**（含本篇 7 条，无漂移）。

---

## 四、⭐ 与 455《ANT 开钟时刻》的口径对账（本单核心）

### 4.1 两条断言的原文登记

| 项 | 455《ANT 开钟时刻》 | 本篇《Anthropic 挂牌的五本账》 |
|---|---|---|
| 作品 | `works/2026-11-19/creative/2026-11-19-ant-opening-bell.html` | `works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html` |
| label | `Anthropic IPO 目标完全摊薄估值（11-18 定价口径）` | `Anthropic 完全稀释估值（11-18）` |
| value | `1.405 万亿美元` | `1.5 万亿美元` |
| quote | `全稀释估值约 1.405 万亿美元` | `1.5 万亿美元 Anthropic 完全稀释估值（11-18）` |
| 作品内位置 | `…ant-opening-bell.html:323`（时间线）；`:345`、`:350`（图注） | `…listing-ledger.html:471-473`（指标格）、`:788`（时间线）、`:445`（结论注） |
| 作品内口径注 | `:350` →「按区间上限计算的全稀释估值 · 11-18 定价口径」 | `:473` →「完全稀释口径 · 11-19 简报」 |

### 4.2 两者各自的口径来源（素材原文）

**1.405 万亿美元 —— 出自定价区间 70–78 的摊薄计算（按区间上限 78 美元）**

- 素材：`每日AI技术动态简报/2026-11-18.md:35`，原句（逐字）：
  > `1. Anthropic 上市定价成为全球 AI 估值新指标：按区间上限计算公开发售约 643.5 亿美元、全稀释估值约 1.405 万亿美元；另有 260 亿美元私募由 AMD、博通、谷歌、美光、微软、英伟达、台积电七家认购，占发行规模约四成，其中谷歌与英伟达各 100 亿美元；公司此前目标估值曾达 2 万亿美元，最终下修逾两成。来源：Yahoo 财经 / 36 氪（11-18）`
- 关键词是**「按区间上限计算」**：输入价 = 78 美元（11-11 定价区间的上限），不是最终定价。
- 旁证：同批简报 `每日AI技术动态简报/2026-11-18.md:10`「区间每股 70 至 78 美元，……定价预计高于区间」。

**1.5 万亿美元 —— 出自 83 美元挂牌价后的摊薄市值**

- 素材：`每日AI技术动态简报/2026-11-19.md:5`，原句（逐字）：
  > `1. Anthropic 挂牌纳斯达克（代码 ANT）：11 月 18 日定价每股 83 美元，高出 70 至 78 美元区间约 6%；发行扩至 9.564 亿股，公开募资约 813 亿美元，叠加七家战略方 260 亿美元私募合计 1073 亿美元，超 SpaceX 纪录；完全稀释估值约 1.5 万亿美元。来源：智通财经 / CNN（11-19）`
- 输入价 = **83 美元**（11-18 实际定价），简报发布于 11-19。
- 本篇指标格出处注（`…listing-ledger.html:473`）：`完全稀释口径 · 11-19 简报`。

### 4.3 判定：**是同一口径的分叉，不是两个互相矛盾的估值**

直除证据（**本报告计算，非来源原文**，已标注）：

| 计算 | 结果 |
|---|---|
| 1.405 万亿 ÷ 78 | ≈ 180.1 亿股（隐含完全摊薄股本） |
| 1.5 万亿 ÷ 83 | ≈ 180.7 亿股（隐含完全摊薄股本） |
| 1.405 × (83 ÷ 78) | = **1.4966 万亿 ≈ 1.5 万亿**（差约 0.3%，落在「约 1.5 万亿」的取整内） |

两条隐含股本相差 0.3%，且按 78 美元口径线性换到 83 美元即得 1.5 万亿。**因此两者是同一个完全摊薄口径 × 两个股价（78 区间上限 vs 83 实际定价），属于同一口径的分叉（价格时点不同），不是同一天测出的两个答案。**

### 4.4 为什么允许它们并存

1. **各自忠实于各自素材的当日原文**：1.405 万亿的原句在 11-18 简报、1.5 万亿的原句在 11-19 简报，两条 quote 都在各自作品正文逐字命中（455 报告第三节 6/6；本篇第三节 7/7）。断言层登记的是「简报原文说了什么」，不是「哪个数更对」。
2. **两值不冲突**：差额完全由输入价 78 → 83 解释（见 4.3 直除），不存在需要二选一的矛盾。
3. **派单契约要求逐字复用标签**：本次派单给定的指标标签原文就是 `Anthropic 完全稀释估值（11-18）`，并明令「不得给既有标签换名字或加后缀」（派单第 5 条），本篇无权自行改写成带价格口径的长标签。

### 4.5 不粉饰：这条对账确实有三处问题

1. **label 层不能自解释**：两条都带 `（11-18）`，只读 `manifest.json`／enrich 序列的人会看到「同一天、同名目、两个值」，页面外无任何提示。
2. **455 的 label 措辞不准**：`11-18 定价口径` 暗示用的是 11-18 的定价，但 1.405 的输入是**区间上限 78 美元**；455 自己的图注（`:350`）写的是「按区间**上限**计算」，是准确的 —— 即 **455 内部 label 与图注口径不一致**。
3. **本篇的口径注不够细**：`:473` 只写「完全稀释口径 · 11-19 简报」，没写「按 83 美元定价」，也没有回指 1.405 万亿美元这条同族数值。

### 4.6 消歧方案（本单不改任何字节，交总指挥裁定）

1. **补口径注（推荐）** —— 把本篇 `…listing-ledger.html:473` 的 `metric-source` 由 `完全稀释口径 · 11-19 简报` 改为 `完全稀释口径 · 按 83 美元定价 · 11-19 简报`。后果：label/value/quote 全部不动，跨作品时间序列不断；读者在页面上即可看到口径差。**本单硬约束禁止改动，需另开单执行。**
2. **改 455 的 label** —— 把 455 那条改为 `Anthropic IPO 目标完全摊薄估值（11-18 · 按区间上限 78 美元）`。后果：口径最清楚，但 label 变更会断开与 451/454 同族序列，需同步 455 作品声明块与 `enrich.json`，风险最高。**同样需另开单，且本单明令不改 455。**
3. **都不动，只在文档层登记** —— 在 `docs/OPERATIONS.md` §五-B5 的「同标签跨日期」清单里登记 `1.405（78 上限）／1.5（83 定价）＝同口径不同价`。后果：零作品改动、零风险；页面上仍无提示。

### 4.7 83 美元的出处，与 455 第四节未决项的闭环

**83 美元出处（简报行号 + 原句）**

| 层级 | 定位 | 原句（逐字） |
|---|---|---|
| 主源 | `每日AI技术动态简报/2026-11-19.md:5` | `1. Anthropic 挂牌纳斯达克（代码 ANT）：11 月 18 日定价每股 83 美元，高出 70 至 78 美元区间约 6%；……完全稀释估值约 1.5 万亿美元。来源：智通财经 / CNN（11-19）` |
| 佐证 | `每日股市简报/2026-11-19.md:32` | `- 驱动：Anthropic IPO 定价 83 美元/股，投资者卖出流动性最好的资产筹措认购资金；美联储官员鹰派表态与会议纪要推高 12 月加息定价（上海有色网转引华尔街见闻，11-19）。` |

作品内四处落地：`…listing-ledger.html:456-458`（指标格，出处注 `智通财经 / CNN · 每股 · 11-19 简报`）、`:809-810`（evidence 原文引用 + 出处）、`:787-788`（时间线）、`:519`（表 1 对账行）。

**是否闭环（对照 455 报告第四节）**

455 报告 `works/2026-11-19/notes/2026-11-19-ant-opening-bell-交付报告.md` 第四节原文：

> `| Anthropic 每股最终定价 | **未确认**（素材只说「高于区间」） | 查招股书或交易所公告；**成品内不得写死每股价** —— 本次扫描成品 6 条 claims 未含每股价，符合约束 |`

| 检查项 | 结论 | 依据 |
|---|---|---|
| 素材层闭环 | **已完成** | 11-19 两份简报给出 83 美元原句（4.7 表），455 当时的 11-19 素材里没有该数（455 派单素材不含定价结果），本篇素材含 |
| 一手层闭环 | **未验证** | 455 给的确认方法是「查招股书或交易所公告」，本篇与本单均未查；83 美元是媒体转述（智通财经 / CNN、华尔街见闻），来源等级 **C（二手）** |
| 455 报告状态更新 | **未做** | 本单硬约束「不改 455 及其它作品」，455 报告第四节该行仍显示「未确认」。确认方法：由总指挥在 455 报告侧加一行指向本报告 |

即：**「每股最终定价＝未确认」这条未决项在素材层已由本篇闭环（83 美元 + 两处行号原句），一手源确认仍待做；455 报告文本本身未改（本单禁改），需要总指挥在 455 侧补注。**

### 4.8 附加观察（非派单要求，如实报告）

1. **同标签两值**：`Anthropic 算力与基础设施承诺总额` 在 11-16／11-17／11-18 四件作品中 value = `9009 亿美元`，本篇 = `约 9000 亿美元`（源词不同：S-1 口径 9009 vs 11-19 简报「约 9000 亿美元」），数值兼容但**同标签跨作品取值不同**。建议按 4.6 选项 3 一并登记。核对方式：解析 `enrich.json` 全库按 label 过滤。
2. **8 格 vs 7 断言**：指标网格 8 格，声明 7 条，第 8 格 `接近 7 倍 / Anthropic 超额认购倍数（11-18）` 未入 claims；其 quote 归一化后**可在正文命中**（3.2 附加行 `True`）。派单建议断言清单未含该条 → **未声明的原因未确认**，确认方法：查本次派单会话的执行记录或由研析自述。

---

## 五、数据来源逐条列表（断言 → 素材文件:行号 → 原句摘录）

作品只用派单指定的本地 11-19 三份简报（派单第 7 条），**未做网络检索**。`每日热点新闻简报/2026-11-19.md` 已查：`grep -c Anthropic` → `0`，该期无 Anthropic 条目（与作品页脚 `…listing-ledger.html:846` 一致）。

| # | 断言（value / label） | 素材文件:行号 | 原句摘录（逐字） | 作品内位置 |
|---|---|---|---|---|
| 1 | `83 美元` / `Anthropic IPO 定价（11-18）` | `每日AI技术动态简报/2026-11-19.md:5`（佐证 `每日股市简报/2026-11-19.md:32`） | `11 月 18 日定价每股 83 美元` ／ 佐证：`Anthropic IPO 定价 83 美元/股` | `:456-458`、`:809-810`、`:519`、`:787` |
| 2 | `70 至 78 美元/股` / `Anthropic IPO 定价区间（11-11）` | `每日AI技术动态简报/2026-11-19.md:5`（回指；旁证 `每日AI技术动态简报/2026-11-18.md:10`、`每日AI技术动态简报/2026-11-11.md:12`） | `高出 70 至 78 美元区间约 6%` ／ 旁证：`区间每股 70 至 78 美元` ／ `Anthropic IPO 定价区间出炉：每股 70 至 78 美元` | `:461-463`（出处注「招股区间 · 11-19 简报回指」）、`:781` |
| 3 | `1073 亿美元` / `Anthropic 合计募资额（11-18）` | `每日AI技术动态简报/2026-11-19.md:5` | `公开募资约 813 亿美元，叠加七家战略方 260 亿美元私募合计 1073 亿美元` | `:466-468`、`:809`、`:526-528`（`813+260=1073，三数自洽`） |
| 4 | `1.5 万亿美元` / `Anthropic 完全稀释估值（11-18）` | `每日AI技术动态简报/2026-11-19.md:5` | `完全稀释估值约 1.5 万亿美元` | `:471-473`、`:788`、`:445` |
| 5 | `332 亿美元` / `Anthropic 前三季度营收（2026）` | `每日AI技术动态简报/2026-11-19.md:35` | `2026 年前三季度营收 332 亿美元（上年同期 25 亿）、约 79% 按用量计费` | `:481-483`、`:813-814` |
| 6 | `约 9000 亿美元` / `Anthropic 算力与基础设施承诺总额` | `每日AI技术动态简报/2026-11-19.md:35` | `但仍有约 9000 亿美元算力与租赁承诺` | `:486-488`、`:813` |
| 7 | `155 美元` / `Melius 目标价（11-19）` | `每日AI技术动态简报/2026-11-19.md:35` | `Melius 于 11 月 19 日给予"买入"评级、目标价 155 美元` | `:491-492`、`:728`、`:813` |

**非断言数字的来源**（作品页脚 `…listing-ledger.html:847` 已声明为「本篇直除」，非简报原文）：13.3 倍、8.4 倍、27 倍、6.4%、87%、约 443 亿美元、约 34 倍；看空账来自 `每日AI技术动态简报/2026-11-19.md` 热门观点 7（钜亨网），安全联署来自同文件行业影响 6（Digg / 新浪科技），两处均以 `.evidence-quote` 逐字登记（`:817-826`）。

**注**：`每日AI技术动态简报/2026-11-18.md` 与 `每日AI技术动态简报/2026-11-11.md` 的行号**仅用于本报告第 4 节与 455 的口径对账**，未进入本篇作品。

---

## 六、impeccable 执行记录（命令原文输出）

### 6.1 构建期（2026-11-20 08:05–09:09 BJ，取自本 agent 会话历史 seq 8727–8782）

**步骤 1 · 上下文**：`impeccable context` 已执行（构建期会话），返回 `SCOPED_EXISTING_ALLOWED` 类指令：本页属既有展厅体系的窄幅产出，以在用版式为准；随后读 `skills/impeccable/reference/craft-floor.md`（质量下限），在动手前执行。

**步骤 2 · 首轮 `detect --json` 原文输出**（3 条 findings）：

```bash
cd /app/working/shared/showcase && /app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable detect --json works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html
```

```text
[
  {
    "antipattern": "cramped-padding",
    "name": "Cramped padding",
    "severity": "warning",
    "category": "quality",
    "file": "/app/working/shared/showcase/works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html",
    "line": 0,
    "snippet": "<div> \"tbl-wrap\": children flush against border+bg on all sides (no inset)"
  },
  {
    "antipattern": "cramped-padding",
    "name": "Cramped padding",
    "severity": "warning",
    "category": "quality",
    "file": "/app/working/shared/showcase/works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html",
    "line": 0,
    "snippet": "<div> \"side\": children flush against border-top/left on left (no inset)"
  },
  {
    "antipattern": "flat-type-hierarchy",
    "name": "Flat type hierarchy",
    "severity": "advisory",
    "category": "slop",
    "file": "/app/working/shared/showcase/works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html",
    "line": 0,
    "snippet": "Role sizes: body 17px, h3 21px, h2 25px (largest adjacent step 1.24:1; target 1.25:1; weight separates headings from body text)",
    "advisory": true
  }
]
```

**步骤 3 · 逐条修复**（4 处 CSS，均为作品内既有修改，不属本单）：表格边框移到 `table.ledger` 本身（消除 `tbl-wrap` 贴边）；双栏分隔线改为 `.two-col::after` 伪元素（消除 `.side` 贴边）；`h3` 21→22px、移动端 `h2` 25→28px（补齐 1.25× 字阶）；移动端 `two-col` 单列时同步去掉分隔线。

**步骤 4 · 复检原文输出**：

```bash
/app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable detect --json works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html; echo "exit=$?"
```

```text
[]
exit=0
```

**步骤 5 · 结构与断言自检原文输出**：

```text
div open/close: 108 108
section open/close: 10 10
claims: 7 passed: 7
[]
```

**步骤 6 · 渲染复核**：Browser SDK 打开 `file://` 作品页，对 `#figures`／`#charts`／`#governance .flow` 等 9 个区块滚动截图并逐张目检，修正 2 处（指标格底注不齐、治理流程图被窄栏挤到换行）。

### 6.2 本单补留痕（2026-11-20 13:40–13:57 BJ 实跑）

**工具可用性**：

```bash
cd /app/working/shared/showcase && /app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable --version
```

```text
4.7.1
```

```bash
cd /app/working/shared/showcase && /app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable audit --help; echo "AUDIT_EXIT=$?"
```

```text
Unknown command: "audit"

To see a list of supported commands, run:
  impeccable --help
AUDIT_EXIT=1
```

> 如实说明：本机 impeccable **v4.7.1 只暴露 `detect`**，`audit`／`polish` 子命令不存在（与 #438 报告同口径）。派单要求的「audit + polish」在本版本无对应命令，故以 `context` → `craft-floor` → `detect` → 人工修复 → `detect` 复检为等效留痕；派单点名的 `design_scan.py`（其底层即 `impeccable detect`）在第七节另留痕。

**上下文（本单复跑，只读）**：

```bash
cd /app/working/shared/showcase && /app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable context --target works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html
```

原文输出要点（exit 0，全文较长，摘首尾）：

```text
NO_PRODUCT_MD: This project has no PRODUCT.md yet, but it does have an incumbent visual implementation. ...
SCOPED_EXISTING_ALLOWED: Narrow refinement commands may use the incumbent implementation as authority without blocking on context setup; they must preserve it and offer init afterward.
EXISTING_VISUAL_SYSTEM: For refinement or extension, code and assets are incumbent design authority and missing DESIGN.md is a documentation gap. ...
SURFACE_CONTEXT_AVAILABLE: Persisted surface briefs exist, but none was selected unambiguously for this invocation. ... Candidates: [...]
RESOLVED_CONTEXT:
{
  "targetPath": "works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html",
  "targetExists": true,
  "projectRoot": "/app/working/shared/showcase",
  "repoRoot": "/app/working/shared/showcase",
```

**交付前 detect（规则 14 留痕主命令）**：

```bash
cd /app/working/shared/showcase && /app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable detect works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html; echo "IMPECCABLE_EXIT=$?"
```

原文输出（**无任何 findings 输出，exit 0**）：

```text
IMPECCABLE_EXIT=0
```

**判定：impeccable `detect` 0 findings（exit 0），与总指挥 11-20 11:25 BJ 的 `design_scan.py --scope file:` findings 0 一致。**

---

## 七、三条门禁命令 · 原文输出

### 门禁 1–3 串联（派单原文命令）

```bash
cd /app/working/shared/showcase && python3 tools/claim_gate.py --verify && python3 tools/design_scan.py --scope file:works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html && python3 tools/build_manifest.py --check
```

**原文输出（整链 exit 0）**：

```text
重校验 1383 条断言
✓ 全部通过
扫描 1 件作品 · findings 0 条 · 涉及 0 件
严重度分布: {}
规则 Top:

（非全量扫描：只报告，不比棘轮）
扫描作品      : 157
research      : 84
creative      : 73
total         : 157
latestDate    : 2026-11-20
可用标签      : 288
claims 闸门   : 存量豁免 138 件 · 本轮拦下 0 件（无 <script id="claims"> 声明块）

[check] manifest 与磁盘 一致
  护栏: index.html 245KB / 预算 400KB · EMBEDDED 182KB · 7 个月份
  断言: 1383 条 · 覆盖 151/157 件 (96%) · 待处理 684 · 无结构 8 · 重校验 1383/1383 通过
CHAIN_EXIT=0
```

**判定**：`--verify` 1383/1383 通过；`design_scan --scope file:` **findings 0**；`--check` **manifest 与磁盘一致**，157 件（research 84／creative 73），与总指挥 11-20 11:25 BJ 复核的 157 件、1383/1383 完全一致。

### 门禁 4：运行时巡检（派单原文命令）

```bash
python3 tools/audit_pages.py works/2026-11-20/research/2026-11-20-anthropic-listing-ledger.html
```

**原文输出（exit 0）**：

```text
巡检 1 件作品（真实加载 + 抓运行时错误）


========================================================
巡检完成：1 件，0 件有问题
requestfailed 口径：策略拦截 0 次 / 导航中止 0 次 / 与本页无关 0 次（均不计为问题）；远程依赖未落定 0 件
✓ 全部作品页运行时健康
G4_EXIT=0
```

---

## 八、改动、验证与待确认

**改动**

- 本单唯一新增文件：`works/2026-11-20/notes/2026-11-20-anthropic-listing-ledger-交付报告.md`（本文件），及为它新建的目录 `works/2026-11-20/notes/`。
- 未改：作品 HTML（一字节未动）、455 作品与 455 报告、任何 claims 的 label/value/quote、`manifest.json`／`index.html`／`enrich.json`（三条门禁均为只读命令）。
- 未执行：`git push`。

**验证**

- 已验证：quote 逐字命中 7/7 — 方法：复刻 `claim_gate.py` G1 的 `/tmp/verify_quotes.py` 对本篇跑通，exit 0（第三节）。
- 已验证：三条门禁 + `audit_pages` 全部 exit 0 — 方法：按派单原文命令实跑，输出见第七节。
- 已验证：`impeccable detect` 0 findings — 方法：v4.7.1 实跑，exit 0（6.2）。
- 已验证：作品硬事实（57,887 字节、beat、署名、缩略图、远程依赖 0、占位符 0）— 方法：`stat`／`grep`／`re` 统计（1.1）。
- 已验证：素材行号与原句 — 方法：`sed -n` 逐行读取三份 11-19 简报与 11-18／11-11 简报（第四、五节）。
- 未验证：83 美元的一手来源（招股书／交易所公告）— 原因：本单与派单均限定只读本地简报，不做网络检索。
- 未验证：作品在真实浏览器中的交互行为逐点点测 — 原因：本篇无 `<button>`、仅 1 处 `addEventListener`，`audit_pages` 运行时健康已覆盖 JS 报错面；控件点测无对象。

**待确认**

1. 4.6 的消歧方案三选一，由总指挥裁定（推荐选项 1「补口径注」，需另开单）。
2. 455 报告第四节「每股最终定价＝未确认」是否由总指挥加注指向本报告（本单禁改 455）。
3. 第 8 格 `Anthropic 超额认购倍数（11-18）` 未入 claims 的原因 — 未确认，确认方法：查派单会话执行记录或研析自述。
4. `Anthropic 算力与基础设施承诺总额` 同标签两值（9009 亿／约 9000 亿）是否登记进 `docs/OPERATIONS.md` §五-B5。
