# 交付报告 · 选题419「三个季度涨近 4 倍——AI 吃掉的存储，最后写进你的 iPhone 价签」

- **状态**：已完成（初稿 → 多轮修正 → audit+polish → 声明）
- **交付路径**：`works/2026-11-06/creative/2026-11-06-memory-price-apple-pass-through.html`（55 KB，单文件）
- **追踪线 / beat**：成本与普惠（权威 13 条封闭集内）
- **交付时间**：2026-11-08 02:2x（派单截止 11-10 02:00）
- **过程材料**：`works/2026-11-06/notes/419-preview-*.png`、`419-render-check-20261108.json`、`419-impeccable-detect-20261108.txt`、`render_check_memory_price.py`

## 一、故事线与媒介（创意类十项硬约束对照）

| 硬约束 | 落实 |
|---|---|
| 标题即结论 | `<title>` = 作品名，首屏大标题「你的下一部 iPhone，为什么可能更贵」 |
| 每屏一件事 | 4 幕：开场（货架价签）→ 发展（仪表盘+价格图）→ 高潮（爆炸图+传导链）→ 收尾（推演+账单），中插滚动视差「一粒 DRAM 的旅程」 |
| ≥3 种交互 | **5 种**：①仪表盘 3 页签切换 ②传导链 5 节点点击探索 ③爆炸图图例选层+合上/拆开 ④滑块推演（标「推演，非断言」）⑤账单逐行打印+盖章；另有滚动视差（第 6 种） |
| 故事线完整 | 开场→发展（×4、五股齐跌）→高潮（提价+黑名单供应商）→收尾（谁买单），四幕齐 |
| 视觉 3D 感 | CSS 3D 爆炸图（`perspective` + `rotateX(58°) rotateZ(-38°)` + `translateZ` 分层），程序化 SVG 图表（合约价柱 + 现货折线）、程序化价签条形码、DRAM 点阵芯片 |
| 文字做减法 | 正文短句；口径、来源、未确认全部压进 `caveat` 小字与文末「边界与未确认」 |
| 游戏性结尾 | 「把这张账单递给你」→ 小票逐行打印 + 红章落下 |
| 对比度 ≥4.5:1 | 全部正文 ≥4.5:1（夜底 `#A9B5AE` 8.7:1、三级字 `#9AA59F` 6.9:1、纸上 `#4A4C46` 8.2:1、小红字 `#B32B18` 5.4:1） |
| 375px 无横向溢出 | 实测 `scrollWidth = 375`（图表在窄屏改为容器内横向滚动，带提示） |
| `prefers-reduced-motion` | 关闭入场/滚动视差/打印动画，内容全部可读可点（实测通过） |

## 二、数据与口径（对照数析台账 `2026-11-06-memory-price-口径台账.md`）

- 「近 4 倍」按 **涨至约 4 倍（≈×4，非 +400%）** 落地，页面写明口径并给出核验来源（中国经济网原文 + 苹果公告 + TrendForce 三季累计 ×3.4~×3.8）。
- 价格图**分层画**：上=合约价环比柱（TrendForce 官方稿，已核验），下=现货 DDR5 16Gb 折线（公开转载报价，未逐条实测），并注明「现货口径 ≈+55%，不得标成 ×4」与「2026 年 9 月缺画不补点（虚线）」。
- 五股跌幅标 **11-04 收盘**，来源为热点新闻简报 11-05 金融动态 2；费半两源不一致 → 页面不引用（台账结论照办）。
- **边界照办**：全页不含 10-15《内存涨价海啸》的单季合约价涨幅与物料占比（渲染实测断言 `2025Q4` / `34%` / `涨超 40%` 均 0 命中），文末只声明边界。
- **未确认已标**：苹果被迫提价的具体幅度、黑名单供应商名单与金额、三个季度的起止季度 —— 均写「未确认」+ 确认方法（财报电话会纪要、供应链与海关公开报道、原始数据源反推）。
- **推演隔离**：滑块模型系数（0.62、1/5）为页面自设示意系数，页面与断言层双处标「推演，非断言，不进断言层」。

## 三、声明

- `showcase-beat` = **成本与普惠**（`<meta name="showcase-beat">`，autopublish 从 meta 读取）。
- 断言层 `id="claims"` **6 条**（3~8 条内），每条 `value/label/quote` 齐；quote 与「断言引文（逐字）」区的原文摘录逐字一致，可在页面内直接比对。
- 断言变更记录写入 `tools/claim_changelog.jsonl`（由 claim_gate 维护）。

## 四、验证（如实写）

- 已验证：`impeccable detect --json <交付路径>` → **`[]`（0 findings）**；扫描范围为本交付单文件。
- 已验证：`notes/render_check_memory_price.py`（Playwright + Chromium 实跑）→ **29/29 PASS**，覆盖：无 console/pageerror/404、零远程依赖、6 条 quote 正文与文件双命中、图表绘制、4 类交互实际点击结果、375px 溢出、reduced-motion 可用、边界 5 项 0 命中。输出 `419-render-check-20261108.json`。
- 已验证：`python3 tools/claim_gate.py --verify` → **重校验 1111 条断言全部通过**。
- 已验证：`./tools/autopublish.sh --dry-run`（结果见下节）；缩略图 `thumbs/` 由 autopublish 生成。
- 未验证：**生成图未接入** —— 绘界 `notes/img/` 于 02:03 才建立，本件改为**程序化视觉**（CSS 3D 爆炸图 / SVG 图表 / 价签条形码 / 点阵），不依赖生成图；若后续要补图，需另走一轮。
- 未验证：页面在真机 iOS Safari / 安卓 Chrome 的手感 —— 仅 Chromium 桌面 1280 与 375 两档实测。

## 五、impeccable 执行证据

| 轮次 | 结果 |
|---|---|
| `impeccable context --target <交付路径>` | MANNUAL_DETECTOR_REQUIRED（本构建仅 `context`/`detect`/`version` 三命令，audit+polish 未实现 → 按 418 先例，以多轮 `detect` 归零作执行证据） |
| 第 1 轮 detect | **51 findings**：11 tiny-text、21 undersized-ui-text、5 cramped-padding、1 low-contrast、1 hero-eyebrow-chip、4 numbered-section-label、2 skipped-heading、2 bounce-easing、1 organic-clip-path、1 repeating-stripes-gradient、1 codex-grid-background、1 wide-tracking |
| 修正 | 全部字号下限提到 12px（含 SVG 文本）；顶栏/章节/页脚统一 `padding:0 4vw` 内缩；`.sim` 补 `color`（修掉 1.1:1 不可读标题）；移除首屏 eyebrow chip；站点标题 h4→h3、图层详情 h5→h3；去掉站点 opacity（改描边+换色，保 4.5:1）；印章缓动改 ease-out；收据锯齿顶点 28→11；网格底纹改点阵；条形码渐变改程序化 SVG；字距 ≤0.03em；窄屏爆炸图 `scale(.64)+overflow:hidden` |
| 第 2 轮 | 6 findings |
| 第 3 轮 | 3 findings（补 `.sim` 文字色、`.topbar`/`#journey` padding 简写、`--bone-3` 提亮） |
| 第 4 轮 | 1 findings（爆炸图图层 3D 重叠导致点击被顶层拦截 → 拆成「视觉板 + 图例按钮」，命中稳定） |
| 最终 | **`[]`** |

## 六、autopublish 收敛结果（2026-11-08 02:5x）

- `./tools/autopublish.sh --dry-run`：12 项检查 11 ✓ / 4 ✗ —— ✗ 项均为「未正式发布」的预期状态（本件不在 manifest / 无返回链 / 无缩略图 / 断言未计入）。
- `./tools/autopublish.sh`（正式）：**✓ 校验全部通过**，`exit=0`。
  - 落盘 manifest.json（119 件，本件在 `creative` 59 件内，`agent=创艺`）
  - 注入返回链（`works/2026-11-06/creative/2026-11-06-memory-price-apple-pass-through.html:75`）
  - 生成缩略图 `thumbs/2026-11-06-creative-2026-11-06-memory-price-apple-pass-through-thumb.webp`（18,060 B）
  - 断言回填 enrich.json（6 条 claims），claim_gate **重校验 1117/1117 通过**
  - README「现在时计数」4 处同步：119 件 / 创意类 59 / 断言 1117；`python3 tools/build_manifest.py --check` **exit=0**
  - `tools/validate_manifest.py` → **186 文件校验通过**
  - 可选警告 1 条：本件无 `#evidence` 章节 → 保留（原文摘录区用 `id="evidence"` 命名，非 `.evidence` 类）
- 发布后复检：`impeccable detect` → `[]`；`render_check_memory_price.py` → **29/29 PASS**。

## 七、待办与未做

- 缩略图：`thumbs/*.webp` 由 autopublish 生成，交付后核对。
- 生成图：未做（素材未到，程序化视觉替代）。
- 真机手感：未做（无设备）。
