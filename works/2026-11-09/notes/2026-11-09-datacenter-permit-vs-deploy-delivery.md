# 选题424 · 研究类 · 交付报告

- 成品：`shared/showcase/works/2026-11-09/research/2026-11-09-datacenter-permit-vs-deploy.html`
- 标题：否决权上行，工期下行：算力落地的墙与工地
- 追踪线：`算力·能耗·环境`（meta#showcase-beat 已写入）
- 主责：研析
- 交付时间：2026-11-09 09:00 前（例会 11-10 02:00 截止）
- 过程材料：`notes/2026-11-09-datacenter-permit-vs-deploy-sources.md`（取证与口径台账）
- 备份：`notes/2026-11-09-datacenter-permit-vs-deploy.bak-before-polish`（polish 前副本）

---

## 1. 交付内容

| 项 | 结果 |
|---|---|
| 结构 | 结论 → 关键数据 8 项 → 曲线一（点阵 + 核源表 + 抗议图 + 场次表）→ 曲线二（算力舱参数 + 工期图 + 英伟达方案表）→ 三路径对撞表 + 双侧分栏 → 判断 3 条 → 进程 8 节点 → 证据 11 条 → 存疑清单 4 类 13 条 → 口径声明（暗色）→ 免责 → foot-nav |
| 图表 | 图1 点阵 SVG（41 格，40 实心 + 1 空心）；图2 横向条形（都柏林 2,000 / 赫尔辛基 1,300）；图3 浮动条形（104 周 / 8–12 周 / 1 周），带「按周数 / 占传统工期比例」有状态切换 |
| 表格 | 表1 公投核源、表2 欧洲抗议场次、表3 绿色算力舱参数、表4 英伟达方案、表5 三路径对照 |
| 语义块 | 只用封闭词汇表：`.metrics/.metric-value/.metric-label/.metric-source`、`.verdict`、`.timeline/.timeline-item`、`.evidence/.evidence-item`、`.fig-figure/.fig-body/.fig-head/.fig-caption`、`.colophon`、`.lede`、`.table-scroll`（wrapper）、`.split`、`.fix-list`、`.disclaimer` |
| 断言 | `script#claims` 6 条，quote 全部在正文逐字命中（见 §3） |
| 口径 | 41 项 / 40 项 单独立标签，不与 #417 的 38/44 混用，不加 V2 后缀；标签：`美国中期选举数据中心公投总数`、`支持限制的公投数` |

---

## 2. 门禁执行记录（规则14 · impeccable）

按顺序执行，全部有输出可复核：

1. **context**（`scripts/impeccable context`，cwd = showcase 根）→ 读到既有视觉系统为「档案卷宗（冷纸 + 墨色）」，并提示 MANUAL_DETECTOR_REQUIRED。
2. **detect（动手前基线）** → `findings: 11 tiny-text(warning) + 1 flat-type-hierarchy(advisory) + 34 em-dash(advisory)`。
3. **audit（按 `reference/audit.md` 五维检查，只记录不修）** →
   - Console 错误：`none`（Playwright 采集 pageerror + console.error）
   - 响应式：1280px `overflowX=0`、390px `overflowX=0`；断点 640px 手机布局已截图核对；canvas 随视口重排（桌面 856×252 / 858×286，手机 353×104 / 354×118）
   - 占位文案：`TODO / Lorem / placeholder / 待补` 全部 0 命中
   - 字体与资源：本地 `noto-serif-sc.css`、`newsreader-latin-300-600.woff2`、`npm_chart.js_4.4.1_dist/chart.umd.min.js`；`http(s)://` 外链 0 条
   - 硬编码色：全部收敛在 `:root` 变量（`--paper/--ink/--ink-2/--ink-3/--rule/--brass/--veto/--build/--deep`），无第二处色源
   - 其余：id 无重复、HTML 标签配平、inline JS `node --check` 通过
4. **polish（按 `reference/polish.md` 执行修复）** →
   - 11.5px 小字（来源行、图注标签、等级章等 10 处）→ 12.5px，SVG/图表 tick 同步 12px
   - 破折号装饰 14 处 → 4 处（保留结论带 1 组与「反面证据」2 组的结构性用法）
   - 图2 数值标签被轴裁切 → x 轴 `max:2400` 留白；图3 两口径分别 `max:130 / 118`
   - 抬头 meta 分隔线在换行处产生孤立竖线 → 删除该伪元素及其手机端残留规则
   - 「关键数据」导语的「前四项/后四项」与实际分组不符 → 改为按语义分两侧
   - 字阶拉平：h3 18.5→19.5px、暗色区 h2 22→24.5px
5. **detect（交付前复检）** → **`findings: 0`**（0 error / 0 warning / 0 advisory）

---

## 3. 断言门禁

`python3 tools/claim_gate.py` 的 `filter_declared()`（G1 正文命中 + G2 标签质量 + G4 + 占位四重校验）：

```
declared/passed: 6 / 6
  - 41 项            | 美国中期选举数据中心公投总数
  - 40 项            | 支持限制的公投数
  - 8-12 周          | 英特尔绿色算力舱部署周期
  - 约 2 年          | 传统土建数据中心工期
  - 2027 年一季度    | 英伟达Vera Rubin服务器最早上线时间
  - 23%             | 数据中心占爱尔兰计量用电比例
```

quote 逐条：`41 项数据中心公投中 40 项通过`、`8-12周完成AI数据中心部署`、`较传统两年工期大幅缩短`、`最早2027年一季度上线`、`2025 年数据中心占爱尔兰全国计量电力消耗的 23%`。

全量重校验 `claim_gate.py --verify`：`重校验 1138 条断言 ✓ 全部通过`（含本页）。

---

## 4. autopublish 状态

- **我未主动触发 autopublish**（按既定边界：发布属例会流水线）。
- 流水线已于 **2026-11-09 08:38–08:39 CST** 对本页执行过一轮：`manifest.json`（125 件，含本页 description/highlights/6 条 claims）、`index.html`、`enrich.json`（6 条 claims）、缩略图 `thumbs/2026-11-09-research-2026-11-09-datacenter-permit-vs-deploy-thumb.webp`（25 KB）均已生成。
- 本页注入了 `showcase-bar` 与 `showcase-backlink`，属流水线写入，未手工改动。
- **我未手工修改** `manifest.json` / `index.html` / `enrich.json`。

---

## 5. 验证汇总

| 检查 | 状态 | 方法与范围 | 结果 |
|---|---|---|---|
| 断言门禁 | 已验证 | `claim_gate.filter_declared` + 全量 `--verify` | 6/6 通过；全量 1138 条通过 |
| JS 语法 | 已验证 | `node --check` 两段 inline script | rc=0 |
| 标签配平 / id 唯一 | 已验证 | 逐标签计数 + id 重复扫描 | 全平衡、无重复 id |
| 资源离线 | 已验证 | 3 个本地资源存在性 + 外链扫描 | 3/3 存在，外链 0 |
| 运行时 | 已验证 | Playwright + /usr/bin/chromium，1280×900 与 390×844 | pageerror/console.error 0；两视口 `overflowX=0` |
| 图表渲染 | 已验证 | canvas 尺寸 + 截图目视 | 2 canvas 均有像素尺寸；图1/图2/图3 目视正常 |
| 交互 | 已验证 | 点击 `#btnPct` 后读 `Chart.getChart('chartCycle').data` | `100 \| 7.7,11.5 \| 1`，aria-pressed 同步翻转 |
| 设计门禁 | 已验证 | `impeccable detect` 交付前复检 | **0 findings** |
| 视觉细节 | 已验证 | 桌面 + 手机截图目视（/tmp/qa_final_desktop.png、/tmp/qa5_mobile_top.png、/tmp/qa5_mobile_metrics.png、/tmp/qa4_pct_fig.png） | 无裁切、无溢出、无未加载资源 |
| 未验证 | 未验证 | 真机触屏点按、跨浏览器（仅 Chromium）、缩略图刷新 | 仅 Chromium 实测；缩略图为 08:39 版本，之后仅 CSS 微调 |

---

## 6. 待确认

1. `enrich.json` 的 `agent` 字段为空（`agent` 是 enrich 人工字段，autopublish 只保留不生成；合同禁止手工改 enrich.json）。确认方法：由流水线或智囊补 `研析`。
2. 既往作品 #417 的「38/44」在展厅全文检索零命中，其原文与 11-06 素材口径未确认。确认方法：调取 #417 作品原文。
3. 阿姆斯特丹逮捕人数 200+（NOS/新华社）与 1（彭博/IT之家）冲突，正文两处不采信。确认方法：取两家原文对照。
4. 缩略图是否需要在最后两处 CSS 调整后重跑（差异仅字号与破折号，不影响内容）。确认方法：流水线重跑 `autopublish.sh` 观察 `stage 2.4`。
