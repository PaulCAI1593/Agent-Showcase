# 交付报告 · 法国主权信用重定价（选题 394 / 重派 #363）

- 作品：`/app/working/shared/showcase/2026-11-03/research/2026-11-03-france-sovereign-repricing.html`
- 字节数：36,643 B（md5 `cc2f9783e6b81e503d4fd5e79b0c318c`）
- 追踪线：`宏观利率与股市`（封闭集内）
- 主责：策士（主责）· 量研（协作）
- 交付时间：2026-11-03 17:00 之后（Asia/Shanghai）
- 契约：`shared/showcase/_private/dispatch-contract-2026-10-29.md`

---

## 一、交付摘要

本篇按派单核定口径写成：核心结论锚点从「穆迪下调法国主权信用」改写为「**穆迪未下调，法国仍被重定价；驱动力是供给不是评级**」。正文含四段分析（口径纠偏 / 供给与需求机制 / 三道门槛 / 触发器与判定线）、8 格关键数据、8 条时间线、8 条逐字引用证据、8 条声明断言。

---

## 二、口径纠偏记录（派单四条预设 → 核定结论）

| 派单预设 | 核定结论 | 本篇处理 |
|---|---|---|
| 「穆迪已下调」 | **不成立**。2026-10-23 穆迪完成**定期审查**，维持 Aa3、维持负面展望，未下调；市场预期下调至 A1 不成立 | 正文首段与结论锚点均据此改写；证据区留穆迪声明原文 |
| 「旧利息占财政收入 2.2%」 | **口径错误**。2.2% 是**利息支出占 GDP**（2025 年） | 全文按 GDP 口径书写，并给出口径纠正条目（2025 年 2.2% → 2027 年 2.9%） |
| 「债务/GDP 119.3%」 | **时点需限定**。119.3% 是 **2026 年预测**（RESF 2027 草案），2027 年为 121.7% | 断言写明年份；不出现裸「119%」；指标标签带年份限定 |
| 「新发行 3400 亿」 | 成立，但需限定年份与口径：2027 年**中长期净发行** 3400 亿欧元（AFT 2026-09-29，净回购后），2026 年为 3100 亿 | 指标标签写明「2027 年中长期净发行」，出处行标「净回购后口径」 |

核查来源：`2026-11-03/notes/01-事实核查与来源台账.md`（02:06 起落盘，12,877 B）。按派单要求**未重做核查**，直接采用其核定结论。

---

## 三、来源纪律

- **S1 页面直取（1 条）**：欧洲央行 2026-10-29 货币政策声明与拉加德记者会全文（唯一一手稿）。
- **S2 转引自搜索摘要、页面未直取（其余全部）**：穆迪公告（经 Euronext / Reuters 转引）、AFT 2026-09-29 公告、OFI 引 RESF 2027 草案、Fitch 研究与评级行动、Oxford Economics、OMFIF、ABN AMRO、TwentyFour AM、法国央行金融稳定报告、Le Monde、Reuters、新闻社行情转引。
- **S3 口径未证实**：S&P 下次审查日 2026-11-27；10 年期 OAT 拍卖日 2026-11-05（投资日历口径）。两者均按「口径未证实」写入，不作断言。
- **S4 本篇不写**：欧洲央行存款便利利率水平（未取到一手，正文不出现该数字）。
- 页面每格指标出处均标注「转引自搜索摘要，页面未直取」；证据区逐条标注来源层级。
- **两源不一致、未合并**：2027 年节省规模 430 亿（OFI/欧盟）vs 540 亿（Reuters）；2027 年债务 121.7%（RESF）vs 120.2%（欧委会）；2027 年利息支出占 GDP 2.9%（OFI/RESF）vs 2.8%（欧委会秋季预测）；同期行情多报价并存（10-22 的 5.0601% / 5.1% / 5.14%；10-23 的 176bp 对 10-30 的 175bp）。

---

## 四、断言层与标签策略

- 声明断言 **8 条**，全部落在 `关键数据` 区块的 `.metric-value` + `.metric-label` 连续片段上，`quote` 均在正文逐字存在，8/8 过闸门（G1 逐字命中 + G2 标签非句子）。
- **持续跟踪指标标签**：全库检索 77 个既有标签，**无任何法国主权口径的既有标签**（本篇是该指标线的首件）。因此本篇采用**可复用、无后缀**的规范写法，未来同指标可直接沿用形成序列：
  - `穆迪法国主权评级`
  - `10 年期 OAT 收益率`
  - `OAT-Bund 利差`
  - `法国 5 年期 CDS 利差`
  - `法国公共债务占 GDP（2027 年预测）`（年份为口径限定，不同年份为不同口径，单独成标签）
  - `利息支出占 GDP（2027 年预测）`
  - `2027 年中长期净发行`
  - `2027 年国家债务还本付息`
  - 标签未加「（推算）」「得分」「V2」等后缀。
- 解释性、因果性判断（供给冲击、三道门槛、判定线）只存在于正文，不进断言层。

---

## 五、验证（命令原始输出）

### 5.1 设计门禁 · impeccable（契约共同五项第 5 条）

**impeccable 已执行：命令 + 结论**

```
$ /app/working/workspaces/default/skills/impeccable/scripts/impeccable context
NO_PRODUCT_MD: This project has no PRODUCT.md yet, but it does have an incumbent visual implementation. …
EXISTING_VISUAL_SYSTEM: For refinement or extension, code and assets are incumbent design authority …
MANUAL_DETECTOR_REQUIRED: … run the mechanical detector over it: …

$ /app/working/workspaces/default/skills/impeccable/scripts/impeccable detect --json 2026-11-03/research/2026-11-03-france-sovereign-repricing.html
[]
detect_exit=0
```

结论：**0 warning / 0 error / 0 advisory**（JSON 为空数组）。
过程：首轮 detect 报 1 条 advisory（`em-dash-overuse`，30 个破折号，AI 腔调特征）。按 craft-floor 建议改写 13 处破折号为冒号、分号、句号与「至」字区间，仅保留 2 条来源引文中的原样破折号，复跑 detect 得 `[]`。

### 5.2 manifest 校验（build_manifest.py --check）

```
$ python3 tools/build_manifest.py --check
扫描作品      : 115
research      : 58
creative      : 57
total         : 115
latestDate    : 2026-11-03
可用标签      : 250

提示 1 条：
   - 2026-11-03/creative/2026-11-03-ai-accelerator-crown-shift.html: 无缩略图（页面将显示无图卡片）

[check] manifest 与磁盘 一致
  提示: 1 件作品缺 agent 署名（可在 enrich.json 补，依据见 archive/选题库-派单日.md 的"推荐Agent"）
     - 2026-11-03/creative/2026-11-03-ai-accelerator-crown-shift.html
  护栏: index.html 200KB / 预算 400KB · EMBEDDED 137KB · 7 个月份
  断言: 1176 条 · 覆盖 103/115 件 (90%) · 待处理 439 · 无结构 9 · 重校验 1176/1176 通过
check_exit=0
```

结论：**退出码 0**，manifest 与磁盘一致，护栏无问题。
说明：提示的 1 条缺缩略图与 1 条缺 agent 署名均属同日**另一件创意作品**（`2026-11-03-ai-accelerator-crown-shift.html`，非本篇），不在本篇范围，未代改。

### 5.3 断言闸门（claim_gate.py）

```
$ python3 tools/claim_gate.py --backfill
作品 115 · L0 1168 · L1 439 · L2作品 9 · 漂移丢弃 0
变更条目 0（已写回 enrich.json）
backfill_exit=0

$ python3 tools/claim_gate.py --verify
重校验 1176 条断言
✓ 全部通过
verify_exit=0
```

结论：**引用失效 0**（全库 1176 条逐条重校验通过；本篇 8 条声明断言全部命中原文）。

### 5.4 缩略图

```
$ python3 tools/gen_thumb.py 2026-11-03/research/2026-11-03-france-sovereign-repricing.html research
  ✅ 2026-11-03-research-2026-11-03-france-sovereign-repricing-thumb.png  (111259B)
$ python3 tools/make_thumbs_webp.py
生成 1 张，跳过 116 张（已是最新）
thumbs/ 当前共 1.76 MB
```

产物：`thumbs/2026-11-03-research-2026-11-03-france-sovereign-repricing-thumb.webp`（17,470 B）。PNG 源图按仓库惯例存于 `_private/thumbs-src/`，公开目录 `thumbs/` 只留 webp。

### 5.5 其他自查

- 模板占位符：`grep -c "{{"` → **0**（全部 `{{ }}` 已替换）。
- 远程依赖：`grep "https\?://"` → **无命中**；页面仅引用本地相对路径字体（`../../assets/vendor/fonts/`）。
- 封闭语义词汇表：只使用 `.metrics .metric .metric-value .metric-label .metric-source .verdict .timeline .timeline-item .timeline-date .timeline-title .timeline-detail .evidence .evidence-item .evidence-quote .evidence-source`，未自创统计块 class。
- 响应式：375px 视口 `document.documentElement.scrollWidth = 375`，无横向滚动。
- 预览截图（过程材料）：`notes/preview-desktop-top.png`、`notes/preview-desktop-mid.png`、`notes/preview-mobile-top.png`。

---

## 六、未做

- 未运行 `tools/autopublish.sh`：契约注明「返回展厅」链接与档案条由 autopublish 阶段 5.5 自动注入，手写会重复；本篇验收项不含 autopublish。
- 未重做事实核查：按派单要求直接采用已核定台账。
- 未代改同日另一件创意作品的缩略图与 agent 署名。

## 七、待确认

- 11 月 3 日国民议会 2027 年预算税收部分表决结果 —— 截至截稿未见已核定来源，正文标为待确认，判定线②以其为准。
- S&P 下次审查日 2026-11-27 —— 口径未独立证实。
- 10 年期 OAT 拍卖日 2026-11-05 —— 投资日历口径，未独立证实。
- 2027 年节省规模 430 亿 vs 540 亿欧元 —— 两源不一致，已分别标注、未合并。
- 欧委会 2027 年债务 120.2% vs RESF 121.7% —— 不同预测批次，未合并。
- ECB 存款便利利率水平 —— 未取到一手，本文不写该数字。
