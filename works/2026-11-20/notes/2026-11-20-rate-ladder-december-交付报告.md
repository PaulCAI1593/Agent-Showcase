# 2026-11-20-rate-ladder-december 交付报告（#457 设计门禁补做单）

> **已完成**：impeccable audit + polish 真实补做，作品本体修复 2 处缺陷，
> autopublish 收敛通过（退出码 0），design_scan / detect 终态 findings 0。
> 执行人：绘界（creative-designer）
> 执行窗口：2026-11-21 02:13 – 03:05 Asia/Shanghai
> 作品：`works/2026-11-20/creative/2026-11-20-rate-ladder-december.html`（改后 34,803B，改前 34,776B）
> 本报告：`works/2026-11-20/notes/2026-11-20-rate-ladder-december-交付报告.md`

---

## 1. impeccable 实际执行命令与结论

| # | 实际命令（cwd = `/app/working/shared/showcase`） | 结论 |
|---|---|---|
| 1 | `skills/impeccable/scripts/impeccable context` | 输出 `SCOPED_EXISTING_ALLOWED`（窄修命令可直接以现有实现为权威继续）+ `MANUAL_DETECTOR_REQUIRED`（收尾必须跑 detect）。无 PRODUCT.md 不阻塞窄修。 |
| 2 | `impeccable audit --target <file>` | **失败：`Unknown command: "audit"`（exit 1）**。launcher 只暴露 `detect / ignores / help / install / link / update / check / telemetry`。按 SKILL.md 改走：`reference/audit.md` 五维人工审计 + `detect` 机械检测。此为工具面事实，非跳过。 |
| 3 | `impeccable detect --json works/2026-11-20/creative/2026-11-20-rate-ladder-december.html` | **`[]`，exit 0**。改前、改后、autopublish 终态共 3 次，均 `[]`。 |
| 4 | `reference/audit.md` 五维审计（见 §2） | 人工发现 detect 未覆盖的 2 项缺陷（见 §3）。 |
| 5 | `reference/polish.md` 流程：取证 → 分诊 → 修复 → 复验 | 修复 2 项，未处理 3 项（见 §3）。 |
| 6 | UI 编辑前读 `reference/craft-floor.md` | 已读（5,524B）；本件无其列明的 ban（无 kicker 压标题、无渐变文字、无 emoji 图标；`letter-spacing` 最深 -0.035em，未破 -0.04em 地板）。 |

辅助取证工具（真实运行）：

- `python3 tools/design_scan.py --scope file:<file>`（注意：`--scope` 需 `file:` 前缀；直接传路径会回落全量 158 件）
- `python3 tools/contrast_forensics.py --json <file>`（showcase 自带 DOM 取证；其渐变路径按不透明色标取最差值，会高估 rgba 渐变底的严重度，本报告不采用其梯度条目作判定）
- 自建 `notes/render_check_rate_ladder.py`（v1）与 `notes/render_check2_rate_ladder.py`（v3 定稿）：Playwright + `/usr/bin/chromium` 真渲染取证

## 2. audit 五维结论（按 reference/audit.md 评分口径，0–4）

| 维度 | 分 | 依据（实测） |
|---|---|---|
| 1 Accessibility | 3 | 对比度 37/37 达标（§4）；reduced-motion 有真替代而非杀内容（§4）；`role=radiogroup`+`aria-label`、`aria-live=polite`、阶梯块 `role=button`+`tabindex=0`+`aria-label` 齐；Tab 走查顺序：顶栏返回 → 返回链 → 单选组 → 3 个阶梯块 → 回顶，无陷阱，焦点环实测 `solid 3px rgb(255,196,99)`。扣分：`.path` 路径卡仅鼠标可点（§3 未处理 2）。 |
| 2 Performance | 3 | `will-change` 0 处；5 个 keyframes 全部有限次（无 infinite）；单 IIFE 脚本、IntersectionObserver 揭示、无布局抖动循环；`.blk` 用 `height` 过渡触发布局，但仅 4 块、仅用户点击时触发，可接受。 |
| 3 Theming | 3（单品口径） | 单件创意艺术品：`:root` 有完整 token，深色单一主题是设计意图，无主题切换需求；组件内硬编码色属该世界自身调色板。 |
| 4 Responsive | 4 | 375px：`scrollWidth=375 ≤ clientWidth=375`，越界元素 0；断点 440/640/700/760/820/900/940；字号全 `clamp()`；档位 label 实测 88×67px ≥24px（`input` 1×1 为标准视觉隐藏单选模式，焦点与点击均由 label 承担，v1 报的 3 条 `<24px` 为误报）。 |
| 5 Implementation integrity | 3 → 4（修后） | `detect` 三次 `[]`；但人工审计发现 detect 不覆盖的版式缺陷（knob 占格、标题跳级），已修复并复验（§3）。 |

## 3. polish 分诊与处置

### 已修复（改本体，4 处编辑）

**F1（P1，版式缺陷）档位第三项被挤到第二行。**
根因：`.lever` 是 3 列 grid，HTML 里 `<span class="knob">`（JS 会写 transform 的滑块占位）**没有任何 CSS 规则**，占掉首格，`input` 为 absolute 脱流，3 个 label 被排成 4 格 → 第 3 格换行。两份历史备份（`bak.20261120-010914`、`bak.20261120-061122`）grep `knob` 均 4 处、均无 CSS 规则 → **创作期即存在**，非后续改动引入。
证据（`457-render-check2-before.json` vs `after.json`）：

- 改前 labels：`y=2552 / 2552 / 2623`（第三项 +71px 换行），`knobRect 88×67` 占首格 `x=128`
- 改后 labels：`y=2552 / 2552 / 2552`（单行），`knobRect 0×0`
- 整页与特写目检：`457-rate-ladder-desktop-after.png`、`457-rate-ladder-lever-after.png` → 三档单行等分，无回归

修法：作品 CSS 追加 1 行 `.lever .knob{display:none}`（checked label 自带琥珀高亮，滑块本就冗余；JS 的 `if(knob)` 有守卫，行为不受影响）。

**F2（P3，语义层级）footer h4 致 h2→h4 跳级。**
证据：改前 heads `[1,2,3,3,3,2,2,4,4]`；改后 `[1,2,3,3,3,2,2,3,3]`，无跳级。
修法：`<h4>`→`<h3>` ×2 + CSS 选择器 `footer h4`→`footer h3`（`footer h3` 特异性高于全局 `h1,h2,h3`，视觉零变化，已截图核对）。

### 未处理（含原因）

1. **flap 翻牌读数三态均占 2 行**（改前改后同，`flap_rows_by_state = {0:2, 25:2, 50:2}`）。原因：340px 控制台可用宽约 286px，`fs30` 下「3.75% 至 4%」需约 328px、「4.00% 至 4.25%」约 384px，单行容量不足是结构性的；压缩字号会牺牲可读性，且若只让默认态单行会造成状态间行数跳变。`flex-wrap:wrap` 是既定容纳方式，`aria-live=polite` 保证读屏完整。属风格判断，非硬约束。
2. **`.path` 路径卡仅鼠标可点**（点击只钉住边框高亮，34.5%/31.5% 信息始终可见，无信息依赖）。修复需新增 role/tabindex/keydown 一套键盘逻辑，超出本单最小修复范围。
3. **`.knob` 的 HTML span + JS 定位代码在 `display:none` 后成为死代码**。移除属代码清理，超出修复必要范围；已隔离，无行为影响。

明确不动项：`#showcase-backlink` 的 CSS（派单明令不加本地补丁，技枢包十一统一修模板）；`#showcase-rescue` 注入块（系统注入的死规则救援，非作品本体）。

## 4. design_scan findings 前后

| 时点 | 命令 | 结果 |
|---|---|---|
| 前 | `python3 tools/design_scan.py --scope file:works/2026-11-20/creative/2026-11-20-rate-ladder-december.html` | **findings 0**（扫描 1 件 · findings 0 条 · 涉及 0 件，exit 0） |
| 同（另一次） | `impeccable detect --json <file>` | **`[]`**，exit 0 |
| 后 | 同上两条，autopublish 之后各再跑 1 次 | **findings 0** / **`[]`**，exit 0 |

说明：派单所引「单件 findings 0」已由本人实跑复现（前后均 0）。本单自建的更严检查（标题层级、档位行数）不在 design_scan 规则集内，其前后为 FAIL→PASS（§3）。

## 5. 对比度实测

**方法**：Playwright + `/usr/bin/chromium` 真渲染；元素滚动入视口并等 IntersectionObserver 揭示（0.95s）后取 computed color，截其盒子像素取众数为底色，按元素+祖先 opacity 链合成实际显示色，计算 WCAG 比值。脚本 `notes/render_check2_rate_ladder.py`，结果 `notes/457-render-check2-before.json` / `-after.json`。

- **37 个取样点：37/37 达标（改前、改后均 0 fail）**。最低值：`.card .delta` 涨跌标 `#e5635a on #2a1c1a = 4.90:1`（需 4.5）；次低 `.quote-block .attr` 6.25:1。正文类 `.card .name`/`.cap`/`.board .sub` 等 muted-on-ink 均 6.53:1。
- **backlink 返回链专项（本页实测，未加任何补丁）**：
  - computed：`color rgb(20,19,15)`、`background rgba(252,252,250,.92)`、`opacity .86`、class **`on-dark-page`**（注入 JS 按元素后方亮度判定，本页为深色页）
  - 截图像素簇：字色 `#14110d`（204px）/ 胶囊底 `#cbcac7`（2,914px）→ **实测 11.48:1**（含 opacity .86 合成后的真实渲染值）
  - 派单所述「浅纸面 4.0–4.2:1」系统性缺陷**在本页不显现**（深色页两条路径——有 class、无 class 继承 amber——均高于 4.5）。按派单只记录、不修补。
- `contrast_forensics.py` 梯度条目为「不透明色标最差值」口径（把 `rgba(.16)` 当不透明算），对本件 hero 渐变产生高估，仅存证不作判定。

## 6. 创意件十项硬约束逐条判定

依据 `templates/creative-brief.md` 第二节（十项硬约束）：

| # | 约束 | 判定 | 证据 |
|---|---|---|---|
| 1 | 单文件 HTML，CSS/JS 内联 | **通过** | 34,803B；`<style>`/`<script>` 全内联；唯一外部引用为本地相对路径字体 |
| 2 | 零远程依赖 | **通过** | 静态正则（`src\|href`、`url()`、`@import` 的 `http(s)://` 与 `//`）命中 **0 条**；运行期 2 个请求全 `file://`，非 file 请求经 route abort 计 0；字体 `assets/vendor/fonts/newsreader-latin-300-600.woff2` 实存 132,000B |
| 3 | 图表用本地 Chart.js/d3 | **不适用** | 本件无图表库 |
| 4 | `<title>` 与 manifest 一致 | **通过** | 双侧同为「加息阶梯：12 月 FOMC 的三条路径推演」 |
| 5 | 落 `works/YYYY-MM-DD/creative/` | **通过** | 路径正确 |
| 6 | 过程材料落 notes/ | **通过** | 本报告、脚本、JSON、截图、日志全在 `works/2026-11-20/notes/` |
| 7 | 对比度 ≥4.5:1（大字号 ≥3:1） | **通过** | 37/37 实测，最低 4.90:1（§5） |
| 8 | 响应式：375px 起无横向滚动 | **通过** | `scrollWidth=375 ≤ clientWidth=375`，越界元素 0 |
| 9 | 尊重 prefers-reduced-motion | **通过** | reduce 下：`.reveal` 12/12 直接可见、`scroll-behavior:auto`、`h1` 下划线终态 `scaleX(1)`、票柱 `arw opacity=1`、进度条宽度已到位 → **内容零丢失**（全局 `* .001ms` kill 的审计顾虑已实测排除） |
| 10 | 交付前跑 impeccable audit + polish | **通过** | 本报告 §1–§3，真实执行留痕 |

**两段声明（派单特别项）**：

- `name="showcase-beat"` = `宏观利率与股市`，在 13 条封闭集内 — **通过**
- `<script type="application/json" id="claims">` 6 条，quote 正文逐字命中 **6/6**（body innerText 与文件原文双侧核对）— **通过**
- autopublish 阶段⑩ 复验：**1402 条 · 引用失效 0**（全库，含本件 6 条）

## 7. 改动文件与备份

| 项 | 路径 | 说明 |
|---|---|---|
| 改动本体（唯一） | `works/2026-11-20/creative/2026-11-20-rate-ladder-december.html` | 4 处：+`.lever .knob{display:none}`（+27B）；`footer h4`→`footer h3` 选择器；`<h4>`→`<h3>` ×2。34,776B → 34,803B |
| 改前备份（notes/） | `works/2026-11-20/notes/2026-11-20-rate-ladder-december.html.bak.20261120-185926` | 34,776B，改前原文 |
| 历史备份（原有） | `notes/...bak.20261120-010914`（31,290B）、`notes/...bak.20261120-061122`（34,752B） | 用于确认 knob 缺陷自创作期存在 |
| 未手工改动 | `manifest.json` / `index.html` / `enrich.json` | 仅经 autopublish 自动重建；日志载「幂等: 内容未变」 |

## 8. autopublish 收敛（改本体后必跑）

命令：`cd /app/working/shared/showcase && ./tools/autopublish.sh`
**退出码：0**（日志 `notes/457-autopublish.log`）。十项硬校验原文：

```
① 计数      manifest.total=160 research=86 creative=74 磁盘=160 → 一致 ✓
② 缺文件    manifest悬空=0 磁盘未登记=0 → 0 (须为 0)
③ 缺缩略图  0 (须为 0)
④ 缺标签    0 (须为 0)
⑤ 标签总数  上次=288 本次=288 → 未下降 ✓
⑥ 标签丢失  0 件 (须为 0)
⑦ 快照契约  问题 0 项 (须为 0)
⑧ 元数据/类型 enrich孤儿键=0 类型冲突=0 (须为 0)
⑨ 返回链    缺失 0 (须为 0)
⑩ 断言层    1402 条 · 引用失效 0 (须为 0)
✓ 校验全部通过
```

附带：本件缩略图因「正文指纹已变」自动重截（249,532B PNG → webp）；返回链阶段「已注入 0 · 已有链接跳过 160」，未触碰 backlink。

## 9. 证据文件清单（均在 `works/2026-11-20/notes/`）

| 文件 | 内容 |
|---|---|
| `render_check_rate_ladder.py` + `457-render-check.json` | v1 取证（12 pass / 2 fail / 1 warn；其中对比度 4 条为揭示前取样伪影，已由 v3 修正替代，本报告不采用） |
| `render_check2_rate_ladder.py` + `457-render-check2-before/after.json` | v3 定稿取证：37 点对比度、backlink 像素簇、reduced-motion 终态、档位几何、Tab 走查 |
| `457-rate-ladder-desktop.png` / `-mobile.png` | 改前整页（1260 / 375） |
| `457-rate-ladder-desktop-after.png` / `-lever-after.png` | 改后整页 + 档位特写 |
| `457-autopublish.log` | 收敛日志（exit 0） |
| `shot457.py` | 截图脚本 |

## 10. 验证状态汇总

- **已验证**：§4–§8 全部为本机实跑输出（命令与路径可复现）。
- **未验证**：真机手机浏览器触摸实测（仅 chromium 模拟视口 375px）；Safari/Firefox 交叉引擎渲染。
- **未做**：未改 `.path` 键盘通道、未删 `.knob` 死代码（原因见 §3）；未对 backlink 加任何本地 CSS（遵派单）。
