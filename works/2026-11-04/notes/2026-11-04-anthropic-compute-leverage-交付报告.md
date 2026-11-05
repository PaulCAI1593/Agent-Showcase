# 交付报告 · 选题411「1.72 美元与 8,954 亿美元——Anthropic 招股书的算力杠杆率拐点」

> 作品：`works/2026-11-04/research/2026-11-04-anthropic-compute-leverage-ratio.html`（53,979 字节）
> 主责：研析　｜　核查协作：察言（intelligence-officer，任务号 `task-dde04998a1f2`）
> 交付日期：2026-11-05（补派于 11-04 期）　｜　追踪线：估值与资本　｜　已验证断言：8 条

---

## 一、改动点

| 文件 | 性质 | 说明 |
|---|---|---|
| `works/2026-11-04/research/2026-11-04-anthropic-compute-leverage-ratio.html` | 新建 | 作品本体，从 `templates/work.html` 起步，全部 `{{ }}` 占位已替换（复检 `grep -c "{{"` = 0） |
| `works/2026-11-04/notes/calc_anthropic_leverage.py` | 新建 | 测算底稿：A 级输入逐项抄自 S-1/A 并标注原文行号，输出全部派生量 |
| `works/2026-11-04/notes/calc_anthropic_leverage_result.json` | 新建 | 底稿运行结果（yield 序列、拐点、承诺拼装、表外对照、Anthropic Direct） |
| `works/2026-11-04/notes/2026-11-04-anthropic-compute-leverage-口径台账.md` | 新建 | 口径台账：来源层级、逐条溯源、口径分歧处置、察言核查结果、未核清单 |
| `works/2026-11-04/notes/2026-11-04-anthropic-compute-leverage-preview-*.png` | 新建 | 4 张预览截图（desktop / desktop-mid / desktop-low / mobile 375） |
| `thumbs/2026-11-04-research-2026-11-04-anthropic-compute-leverage-ratio-thumb.webp` | 新建 | 缩略图（720×457，19,252 字节），由 `tools/gen_thumb.py` + `tools/make_thumbs_webp.py` 生成 |
| `manifest.json` / `index.html` / `enrich.json` | 工具生成 | 由 `./tools/autopublish.sh` 生成，**未手工编辑** |

## 二、核心结论与口径核验（本篇对派单待核项的处理）

| 派单待核项 | 结论 | 依据 |
|---|---|---|
| 「Q3 净亏损 233 亿美元」 | **成立**，且可写入 | S-1/A 季度合并损益表：2026 年三季度净亏损 232.91 亿美元（$23,291M）。任务书判断的「不相容」源于把净亏损与经营口径混读——差额 227.24 亿美元来自可转换票据/衍生负债/SAFE 的**非现金公允价值变动 219.36 亿美元**。同期经营亏损 5.67 亿美元、调整后经营利润 24.63 亿美元。已在正文写明三者分别回答三个问题，并写明净亏损环比是从二季度 663.09 亿美元**收窄** |
| 「1.72 / 2.08 美元」 | **成立，但属推导值** | 由 S-1/A 季度表精确复算：16,956 ÷ 9,863 = 1.7192；11,555 ÷ 5,558 = 2.0790；环比 -17.31%。正文标注为「团队测算」，输入为 A 级原文数字。已补出完整五季序列（0.68 → 0.69 → 1.40 → 2.08 → 1.72） |
| 「Q3 净亏损与营收/调整后营业利润不相容」 | **已解除** | 见上；并额外核出 9M 口径：营收 332.42 亿、净亏损 1,040.39 亿，防止把 233 亿误作累计 |
| 与 Meta 的可比性 | **同概念、不同颗粒度，正文明写** | 构成、可终止性披露、表外额外项三处实质差异；Anthropic 侧 `表外承诺与股东权益之比` 记为「不适用」（股东权益为 -1,498.73 亿美元赤字） |
| RSI 措辞 | **按一手稿精确化** | 「dramatically accelerated progress attributable to AI」在风险因素（全文 1 次）；「recursive self-improvement」在 MD&A 业务章节（全文 1 次）；文件未用「RSI」缩写。正文新增一段写明这一区分 |
| Anthropic Direct | **改写为文件原义** | 文件描述为第三方建设并持有、按公司规格租用并运营的专用数据中心设施；「自建」表述已从正文移除 |
| 日本发行 5,529 亿日元 | **改挂出处** | 该金额不在 S-1/A 内，原始文件为 2026-11-02 向日本关东财务局提交的「有価証券届出書」（路透/彭博/日经转述） |

## 三、验收命令原始输出

### ① 设计门禁

```
$ cd /app/working/shared/showcase && /app/working/workspaces/default/skills/impeccable/scripts/impeccable detect --json works/2026-11-04/research/2026-11-04-anthropic-compute-leverage-ratio.html
[]
exit=0
```

**impeccable 已执行：命令 `impeccable detect --json <作品路径>`；结论 0 warning / 0 error（findings 数组为空，退出码 0）。**
执行顺序：开工前 `impeccable context`（本机启动器仅提供 `detect`，按 AGENTS.md 规则14「audit+polish（或 detect）」以 detect 为准）；交付前跑 detect 一次。渲染复核：4 张预览截图，控制台错误 0，375px 视口无横向滚动（scrollWidth 375 = clientWidth 375）。

### ② 断言闸门

```
$ cd /app/working/shared/showcase && python3 tools/claim_gate.py --backfill
作品 116 · L0 1124 · L1 504 · L2作品 7 · 漂移丢弃 0
变更条目 0（已写回 enrich.json）
exit=0

$ cd /app/working/shared/showcase && python3 tools/claim_gate.py --verify
重校验 1104 条断言
✓ 全部通过
exit=0
```

### ③ 清单校验

```
$ cd /app/working/shared/showcase && python3 tools/build_manifest.py --check
扫描作品      : 116
research      : 59
creative      : 57
total         : 116
latestDate    : 2026-11-04
可用标签      : 250

[check] manifest 与磁盘 一致
  提示: 1 件作品缺 agent 署名（可在 enrich.json 补，依据见 archive/选题库-派单日.md 的"推荐Agent"）
     - works/2026-11-04/research/2026-11-04-anthropic-compute-leverage-ratio.html
  护栏: index.html 194KB / 预算 400KB · EMBEDDED 131KB · 7 个月份
  断言: 1104 条 · 覆盖 108/116 件 (93%) · 待处理 504 · 无结构 7 · 重校验 1104/1104 通过
exit=0
```

### ④ 上架流水线（十项硬校验全过）

```
$ cd /app/working/shared/showcase && ./tools/autopublish.sh
  ① 计数      manifest.total=116  research=59  creative=57  磁盘=116  → 一致 ✓
  ② 缺文件    manifest悬空=0 磁盘未登记=0  → 0 (须为 0)
  ③ 缺缩略图  0 (须为 0)
  ④ 缺标签    0 (须为 0)
  ⑤ 标签总数  上次=250  本次=250  → 未下降 ✓
  ⑥ 标签丢失  0 件 (须为 0)
  ⑦ 快照契约  问题 0 项 (须为 0)
  ⑧ 元数据/类型  enrich孤儿键=0  类型冲突=0  登记表=3条 (须为 0)
  ⑨ 返回链    缺失 0 (须为 0)
  ⑩ 断言层    1104 条 · 引用失效 0 (须为 0)
  ✓ 校验全部通过
  ✓ 流水线完成：116 件作品，250 个标签
```

### ⑤ 缩略图

```
$ python3 tools/gen_thumb.py works/2026-11-04/research/2026-11-04-anthropic-compute-leverage-ratio.html research
  ✅ 2026-11-04-research-2026-11-04-anthropic-compute-leverage-ratio-thumb.png  (119614B)
$ python3 tools/make_thumbs_webp.py
生成 1 张，跳过 173 张（已是最新）
thumbs/ 当前共 2.58 MB

$ ls -la thumbs/2026-11-04-research-2026-11-04-anthropic-compute-leverage-ratio-thumb.webp
-rw-r--r-- 1 root root 19252 Nov  4 23:25 thumbs/2026-11-04-research-2026-11-04-anthropic-compute-leverage-ratio-thumb.webp
（尺寸 720×457，WebP）
```

## 四、契约逐条自检

| 契约项 | 状态 | 证据 |
|---|---|---|
| 从 `templates/work.html` 起步，替换全部 `{{ }}` | 已验证 | `grep -c "{{"` = 0 |
| 封闭语义词汇表（.metrics>.metric>(.metric-value/.metric-label/.metric-source)、.verdict、.timeline>.timeline-item、.evidence>.evidence-item） | 已验证 | 全部按模板结构落地；另用 `.compare` / `.note` / `.scope` 做局部样式（模板允许的额外 class，与 #357 同款） |
| `<script type="application/json" id="claims">`，3~8 条，每条 value/label/quote | 已验证 | 8 条，逐条过 G1/G2/G4；`filter_declared` 返回 8/8 |
| quote 在正文逐字存在 | 已验证 | claim_gate G1 全部命中（`--verify` 重校验 1104 条，失效 0） |
| 解释性判断不写成断言 | 已验证 | 拐点机制、Meta 不可比、RSI 措辞区分等均留在正文 |
| `<meta name="showcase-beat" content="估值与资本">` | 已验证 | manifest 读取：`beat: 估值与资本 · beat_declared: True` |
| 持续跟踪指标标签逐字复用 | 已验证 | 见第五节标签表，未加任何后缀 |
| Anthropic 与 Meta 同概念、不同颗粒度 | 已验证 | 「与 Meta 并排」整节 + 对照表 + 三处实质差异说明，未声称严格可比 |
| 「Q3 净亏损 233 亿美元」口径核验前禁止出现 | 已验证 | 已核（S-1/A 季度表 $23,291M），核后才写入，且附驱动因素与期间标签 |
| 零远程依赖 | 已验证 | 仅自托管字体（`../../../assets/vendor/`）+ 内联 CSS/JS；无 CDN 外链 |
| 过程材料落 `notes/` | 已验证 | 见第一节文件清单 |
| 交付后不手工改 manifest / index.html / enrich.json | 已验证 | 全部由 `./tools/autopublish.sh` 生成 |

## 五、持续跟踪指标标签复用核对（派单硬性要求 4）

| 既往标签 | 既往出处 | 本篇取值 | 是否逐字复用 |
|---|---|---|---|
| `表外承诺合计上限` | #357 Meta（2026-10-27） | 8,954 亿美元（断言） | 是 |
| `表外承诺与股东权益之比` | #357 Meta（2026-10-27） | 不适用（股东权益 -1,498.73 亿美元赤字） | 是（值不可计算，原因写明） |
| `公司总营收` | 既往多件 | 169.56 亿美元（断言） | 是 |
| `研发支出` | 既往多件 | 192.40 亿美元（断言，前九个月） | 是 |
| `API毛利率` | 既往多件 | 85.5%（前九个月整体毛利率，来源行注明「公司整体口径，公司未披露 API 分部毛利率」） | 是 |
| `Anthropic 企业 LLM API 支出占比` | 2026-10-01（ai-agent-three-kingdoms） | 40%（Menlo Ventures 2025，来源行注明「沿用既往口径 · S-1/A 未更新」） | 是 |
| `费城半导体指数` | #364 算力王座（2026-11-03）、#410 | 10,328.3 点（2026-11-02 收盘） | 是 |
| `单位算力收入产出率` | 本篇新建（选题库明示首次引入） | 1.72 美元（Q3）与 2.08 美元（Q2），同标签两值构成序列起点 | 是（新标签，未加后缀） |

## 六、剩余未验证项 / 未做

1. **未对 S-1/A 全文逐条复核**：只复核了季度合并损益表、季度非 GAAP 表、补充经营费用表、合并资产负债表数据、流动性与合同义务章节、两处能力门槛表述及现金流量表相关行；税务、诉讼、股权激励细节等章节未读。页脚已写明。
2. **未取得日本关东财务局（EDINET）有価証券届出書原件**：5,529 亿日元的上限、事务幹事/幹事分工、申购取扱券商名单均来自路透/彭博/日文媒体转述；正文与台账已标注该出处不在 S-1/A。
3. **2026-11-04 的费城半导体指数未采用**：同源数据自相矛盾（Yahoo 历史表 10,202.43 vs 报价头 10,268.65 / -3.13%），Nasdaq API 查询窗口未返回该日。
4. **未评估这些承诺的回报**：本篇只算规模、节奏与覆盖，不判断投资价值。
5. **未做公司中文译本对照**：英文引文的中文表述均为团队翻译。
6. **未写 `enrich.json` 的 `agent` 人工字段**：派单契约禁止手工改 enrich.json。build_manifest 提示本件「缺 agent 署名」，首页「谁在主责」矩阵会显示未署名。建议由智囊在 enrich.json 补 `agent: "研析+察言"`（与 #357 的 `量研+策士` 同为人工字段惯例）。
7. **未运行 `tools/design_scan.py` 全库棘轮比对**：该脚本覆盖全库 116 件，本篇只跑了本件的 detect；设计棘轮的全局结论由例会流水线负责。

## 七、待确认

- `enrich.json` 中本件的 `agent` 字段由谁补（建议值 `研析+察言`）——请智囊决定。

---

**结论：已完成。** 作品落盘 53,979 字节；8 条断言全部逐字回查通过；impeccable detect 0 warning / 0 error；claim_gate 重校验 1104 条断言零失效；build_manifest --check 一致；缩略图已生成；十项硬校验全过。
