# 420 · impeccable audit（五维）执行记录 · 2026-11-10

- 作品：`works/2026-11-08/research/2026-11-08-ai-valuation-meets-hikes.html`
- 依据：`skills/impeccable/reference/audit.md`（Diagnostic Scan 五维 + 0–4 打分）
- 数据：`notes/420-audit-five-dim-20261110.json`（本机 Chromium 实跑）、`notes/420-canvas-check-20261110.json`、`notes/420-overflow-320-1920-20261110.json`
- 命令记录：`notes/420-impeccable-detect-20261110.txt`
- 说明：本环境 `impeccable audit` 子命令不存在（返回 `Unknown command: "audit"`），故按 reference/audit.md 的清单逐维实测。

## 一、健康分

| # | 维度 | 分 | 关键发现 |
|---|------|----|----------|
| 1 | Accessibility | **3** | 65 处正文元素对比度全部 ≥4.5:1（最低 4.63）；标题无跳级；缺 `<nav>` 地标（页面仅有两条返回链接） |
| 2 | Performance | **4** | 0 远程请求、0 图片、0 `will-change`、0 关键帧动画；transition 仅 transform/opacity/background/color/border-color |
| 3 | Theming | **3** | `:root` 20 个自定义属性、97 处 `var()`；`:root` 外 21 处硬编码色，其中 4 处属 autopublish 注入的 `#showcase-bar` 样式块 |
| 4 | Responsive Design | **4** | 1440/1024/390/320/1920 五档均无页面级横向溢出；可点目标全部 ≥24px；4 条媒体查询 |
| 5 | Implementation Integrity | **4** | `impeccable detect` 三轮均 `[]`（0 findings）；对照组同命令 73 findings；8/8 断言 quote 命中 |
| | **合计** | **18/20** | **Excellent（18–20：仅需小修）** |

## 二、逐维证据

### 1. Accessibility（3/4）

- **对比度**：DOM 逐元素取 computed color + 祖先链真实背景，量 65 个有文字节点的唯一元素。
  - 最低 **4.63:1**（`th` / `caption` / `p.note` / `span.src` 等，`--ink-3 #646b67` 压 `--paper #eaedea`）
  - `<4.5:1` 的元素 **0 个**；`<3:1` 的元素 **0 个**（阈值按 `need = large ? 3 : 4.5`，与 audit.md 一致）
- **标题层级**：16 个标题，`h1` ×1，**无跳级**（skips = []）
- **地标**：`header` ×1、`main` ×1、`footer` ×1；**`nav` ×0**
- **键盘**：全局 `:focus-visible{outline:2px solid var(--brass);outline-offset:3px}`（`research/…hikes.html:63`）
- **动效**：存在 `@media (prefers-reduced-motion:reduce)` 规则
- **触控目标**：3 视口下 `a/button/[role=button]/input` 中尺寸 `<24px` 的 **0 个**
- **ARIA**：`aria-label` ×4、`aria-hidden` ×3；`[onclick]` 无角色的元素 **0 个**
- **图片**：`<img>` **0 个**（图表为 Canvas，故 alt/lazy 两项不适用）

扣分点：返回链接（`#showcase-bar .sb-back`、`#showcase-backlink`）未包在 `<nav>` 内，页面也无 skip link。这是单页长文的次要缺口，不构成 WCAG A/AA 失败，故 3 分而非 4 分。

### 2. Performance（4/4）

- 远程请求 `http(s)://` **0 处**，字体与 Chart.js 全部本地
- `will-change` 元素 **0**；关键帧动画元素 **0**
- transition 只有 3 条声明：`transform .9s cubic-bezier(.16,1,.3,1)`、`opacity/transform/background/color/border-color .2s`、`#showcase-bar .sb-back` 的 `background/border-color` —— **无 width/height/top/left 等布局属性动画**
- 页面 62,322 B，内联 `<script>` 4 个
- 3 视口 canvas 均已绘制（见 `420-canvas-check-20261110.json`，非零像素 23,401–271,446）

### 3. Theming（3/4）

- `:root` 定义 20 个自定义属性（`--paper/--ink/--brass/--rule/--down/--up/--series-b/--series-c/--shell` 等），正文中 `var(--…)` 使用 97 次
- `:root` 内硬编码色 16 个（即调色板本身）；`:root` 外 21 个，其中：
  - 4 个属 autopublish 注入的 `#showcase-bar` 样式块（`#0b0c12` `#f0c27f` `#a78bfa` `#f5e6c8`，`research/…hikes.html:295`）——注入块不归本件管
  - 其余为图表与焦点环用色（`#fafafa` `#ffffff` `#14130f` 等）
- 无暗色主题切换需求（展厅为单主题档案页，深色区段用同一套 token）

扣分点：注入条与图表色未走 token，故 3 分。

### 4. Responsive Design（4/4）

| 视口 | scrollWidth | clientWidth | 横向溢出 | console 错误 |
|------|-------------|-------------|----------|--------------|
| 1440×1000 | 1440 | 1440 | 否 | 0 |
| 1024×900 | 1024 | 1024 | 否 | 0 |
| 390×844 | 390 | 390 | 否 | 0 |
| 320×720 | 320 | 320 | 否 | 0 |
| 1920×1080 | 1920 | 1920 | 否 | 0 |

- 320px 下 `table.ledger` 右边界到 366px，但父级 `.table-wrap{overflow-x:auto}`（`research/…hikes.html:153`）自行横向滚动，**页面本身不溢出**
- 媒体查询 4 条：`max-width:900px`、`max-width:640px` ×2、`prefers-reduced-motion:reduce`
- Canvas 在 390px 下宽 324px，随容器收缩

### 5. Implementation Integrity（4/4）

- `impeccable detect --json` → **`[]`**（首轮、终轮各一次；人读形式一次无输出）
- `tools/design_scan.py --scope file:…` → **findings 0 条**
- **对照组**：同命令对 `works/2026-10-03/research/2026-10-03-ai-data-famine.html` 返回 **73 findings**，证明检测器非空转
- 断言层：`script#claims` 8 条，quote 逐字命中正文 **8/8**
- 追踪线：`<meta name="showcase-beat" content="估值与资本">`，13 条封闭集内，`manifest.json` 中已登记
- 控制台：3 视口 error / pageerror / failedRequests 全 0

## 三、polish 复评结论

按 `reference/polish.md` 的 triage 顺序走了一遍（功能缺陷 → 状态缺失 → 层级/响应式/设计系统漂移 → 视觉与动效 → 代码清理）：

1. **功能缺陷**：无。3 视口下 3 张图表全部绘制，无控制台错误、无 404。
2. **状态缺失**：不适用（静态长文，无异步加载与空态）。
3. **层级/响应式/设计系统漂移**：detect 0 条；五维审计仅两条 advisory（无 `nav` 地标、注入条硬编码色）。
4. **视觉与动效**：对比度最低 4.63:1，标题无跳级，触控目标全部 ≥24px。
5. **代码清理**：无冗余。

**结论：polish 无需要修复的 findings，未对作品正文做任何写入。**
作品 md5 补做前后一致：`bc982ea12c2fcfeadaf10ad21503beb2`。

两条 advisory 留待下一次全馆 polish 批次处理，不在本次 P0 补做范围内（会改动作品结构，且非 detect findings）。
