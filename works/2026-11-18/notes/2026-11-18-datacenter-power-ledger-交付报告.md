# 2026-11-18 · 675 座与 400 座 —— AI 的两张用电账本 · 交付报告

**已完成：选题 452 研究类作品单文件成品落盘并通过全部交付校验。**

**改动**

- 新建 `shared/showcase/works/2026-11-18/research/2026-11-18-datacenter-power-ledger.html`（69,175 字节，单文件，无外部依赖）
- 过程材料落 `shared/showcase/works/2026-11-18/notes/`：口径台账 1 份、预览图与分区截图 15 张
- 未改素材、未联网检索、未手改 `manifest.json` / `index.html` / `enrich.json` / `agent.json`

**作品结构**

- 9 个区块、3 张自绘 SVG 图、3 张数据表、8 格关键数据账册、7 条进程、6 条证据、8 条未确认清单
- `<meta name="showcase-beat" content="算力·能耗·环境">` 已在 `<head>` 声明
- `script#claims` 声明 8 条断言，quote 全部在本文件内逐字存在
- 「返回展厅」链路由 `autopublish` 阶段 5.5 注入，未手写

**验证**

- 已验证：`claim_gate.filter_declared` 逐条校验 — declared 8 / passed 8（G1 逐字引用 + G2 标签质量全部通过）。
- 已验证：`./tools/autopublish.sh` 正式执行 — 148 件作品 / 287 个标签 / 断言 1322 条 · 引用失效 0 · 重校验 1322/1322 通过；十项硬校验 **全部通过**（计数一致 / 无悬空文件 / 缩略图齐全 / 标签齐全 / 标签总数未下降 / 标签未丢失 / 快照契约 / 元数据与类型一致 / 返回链齐全 / 断言引用零失效）。
- 已验证：`impeccable detect <file>` — `[]`，**0 条 findings**。
- 已验证：`python3 tools/design_scan.py --scope file:<file>` — **0 条 findings**，设计棘轮无上升。
- 已验证：证据节 6 条逐字比对原文 — 5 条命中 2026-11-17 简报，1 条命中 2026-11-10 简报；9009 亿那条命中 `works/2026-11-12/notes/432-核源台账-研析.md:166` 所记 S-1 原文。
- 已验证：无障碍与响应式实测（Chromium，375 / 768 / 1280 三档）— 文字对比度 **0 条低于 4.5:1**；页面级横向溢出 **0**；触控目标 <24×24px **0 个**；标题层级 H1→H2→H3 无跳级；3 张 SVG 均带 `role="img"` + `<title>` + `<desc>`。
- 已验证：渲染截图人工核对 — 双栏账本、三张图、三张表、账册、时间轴、证据、缺口清单在 1280 与 375 两档均正常排版；控制台错误 0。
- 未验证：`prefers-reduced-motion` 分支仅做了代码级确认（CSS 存在 + `js-motion` 类切换逻辑），未在真机开启该偏好跑一遍 — 确认方法：用 Chromium 强制 `prefers-reduced-motion: reduce` 后截图比对。
- 未验证：BIS 条文原文 — 素材只给概括表述，本轮不联网，未取 Federal Register 正式文本。

**判定与证据边界（正文已写明）**

- 判定一：**电力先改成本结构，许可先改可获得性。**
- 判定二：**被两条账同时夹住的是受限主体的代训订单。**
- 判定三：**「被解释」会变成算力的固定成本项。**
- 三条判定的成立条件与推翻条件逐条列在表三；卡点强度（云厂商中 / 模型公司中高 / 数据中心运营商高 / 受限主体的代训订单最高）明确标注为本文判断，素材不给受影响主体的数量或比例。
- 素材缺口已显式写入正文与台账 8 条，其中第一条为任务点名的 **未确认：缺 BIS 条文原文**。

**待确认**

1. 未确认：`enrich.json` 中本篇 `agent` 字段为空，`autopublish` 输出提示「1 件作品缺 agent 署名」— 本轮约束「不改 enrich.json」，未手工补。确认方法：在 `enrich.json` 该条目把 `"agent": ""` 改为 `"agent": "研析"`。
2. 未确认：`add_backlink.py` 在 `works/2026-11-18/research/` 下生成了备份 `2026-11-18-datacenter-power-ledger.html.bak.20261118-002701`，与作品同目录。本轮移动该文件的 shell 命令被审批拒绝，未执行。确认方法：由总指挥执行 `mv works/2026-11-18/research/*.bak.* works/2026-11-18/notes/`（该文件不参与扫描，`build_manifest` 与 `design_scan` 均按 `.bak` 排除）。
3. 未确认：`autopublish` 同时重截了 6 张既有缩略图（2026-11-02 / 11-03 等，原因：正文指纹已变或 webp 过小疑空白首图）。这是流水线内置行为，非本篇范围。确认方法：`git status --porcelain` 查看 `thumbs/` 变更。

**设计工程技能：impeccable 已执行**

- `impeccable context` → 沿用展厅既有「档案卷宗」视觉世界（EXISTS_VISUAL_SYSTEM），按 MANUAL_DETECTOR_REQUIRED 要求手工跑检测器
- **audit 结果**：五维实测，无障碍 / 响应式 / 性能 / 主题化 / 实现完整性 — 对比度 0 违规、溢出 0、小触控目标 0、检测器 0 findings
- **polish 结果**：渲染实测后修正 5 项（图搬出窄列全宽、表一重复单元格、卡点条行内元素高度、动效选择器、容器内缩与移动端提示），修正后 detect 0 findings
- 终检：`impeccable detect` = `[]`；`design_scan --scope file` = 0 条

### Modern Web Guidance

- `responsive-table`（`npx -y modern-web-guidance@latest retrieve "responsive-table"`）— 表格改用语义 `thead/th[scope]` + `.table-wrapper` 滚动容器带 `tabindex="0"` `role="region"` `aria-labelledby`，窄屏用 `@container` 查询而非 `@media`，`<thead>` 隐藏后由 `td::before{content:attr(data-l)}` 注入列标签。本篇三张表全部按此实现，375px 下自动转堆叠且列名不丢。
- `accessibility` / `html`（`search` 返回的 guide）— 强化语义 landmark、焦点可见、SVG 的 `role`/`title`/`desc` 与装饰图标 `aria-hidden`。
- 未使用渐变、玻璃拟态、手搓弹窗、`feTurbulence` 颗粒等训练数据里的过时写法；图表全部为自绘几何 SVG，动画仅 1 处且尊重 `prefers-reduced-motion`。
