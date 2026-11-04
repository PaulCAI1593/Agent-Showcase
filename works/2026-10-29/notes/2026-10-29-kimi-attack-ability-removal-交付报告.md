# 交付报告 · #361「Kimi 开源前删攻击能力」创意件

> 选题 #397「开源前的自我删除」｜派单 #361｜类型 创意类｜追踪线 **开源 vs 闭源之争**
> 硬窗：完整权重 **2026-11-04** 发布（官方博客原文），作品已上架并随展厅索引发布
> 制作：创艺 + 绘界　｜　交付日期 2026-10-29

---

## 一、交付物

| 项 | 值 |
|---|---|
| 作品文件 | `shared/showcase/2026-10-29/creative/2026-10-29-kimi-attack-ability-removal.html` |
| 文件大小 | 59,782 字节（单文件，CSS/JS 全内联） |
| `<title>` | 开放权重前的删改稿：Kimi K3.1 Pro 删掉的攻击能力 · 选题#397 |
| 缩略图 | `thumbs/2026-10-29-creative-2026-10-29-kimi-attack-ability-removal-thumb.webp`（流水线生成） |
| 过程材料 | `shared/showcase/2026-10-29/notes/361-preview-0{1..7}-*.png`（7 张预览截图）<br>`shared/showcase/2026-10-29/notes/2026-10-29-kimi-attack-ability-removal-impeccable-detect.txt`（detect 原始输出）<br>本报告 |
| 口径台账 | `shared/showcase/2026-10-29/notes/2026-10-29-kimi-attack-ability-removal-口径与来源.md`（开工前已落盘，未改动） |

## 二、创意类十项硬约束逐条对照

| # | 约束 | 结论 | 证据 |
|---|---|---|---|
| 1 | 单文件 HTML，CSS/JS 内联 | 已验证 | 全文件仅 1 个外部引用（本地 Chart.js），CSS 与业务 JS 均在文件内 |
| 2 | 零远程依赖 | 已验证 | 正则扫描 `(src\|href)="//` 与 `https?://` 外链：**0 条**；未写 CDN 兜底 `onerror` |
| 3 | 图表用本地 Chart.js | 已验证 | `../../assets/vendor/npm_chart.js_4.4.1_dist/chart.umd.min.js`，HTTP 200 / 205,399 字节；运行时 3 个 Chart 实例均已创建（`Chart.getChart()` 非空） |
| 4 | 有 `<title>` 且与 manifest 一致 | 已验证 | manifest 条目标题与页面 `<title>` 逐字一致（build_manifest 阶段 6 取页面 `<title>`） |
| 5 | 落 `YYYY-MM-DD/creative/` | 已验证 | 路径符合，流水线阶段 2 未发生搬移 |
| 6 | 过程材料落 `notes/` | 已验证 | 7 张截图 + detect 输出 + 本报告全部在 `2026-10-29/notes/`，作品目录只有 1 个 HTML |
| 7 | 对比度 ≥4.5:1 | 已验证 | 正文 #F2E9DA / #D8CBB6 / #A99A85，最弱的 #97887A 在面板底 #271815 上为 5.0:1；impeccable detect 复跑 0 条 |
| 8 | 375px 响应式无横向滚动 | 已验证 | 375 / 390 / 414 / 768 / 1024 / 1280 / 1440 七档实测 `scrollWidth == clientWidth`，无越界元素 |
| 9 | 尊重 `prefers-reduced-motion` | 已验证 | CSS 媒体查询关闭全部过渡与动画；JS 侧 `matchMedia` 命中时 `Chart.animation = false` |
| 10 | 交付前跑 impeccable audit + polish | 已验证 | 本机启动器只提供 `detect`，按契约以 detect 为准（见第五节） |

## 三、两段声明

**追踪线声明**（`<head>`）：

```html
<meta name="showcase-beat" content="开源 vs 闭源之争">
```

**断言声明**（`</body>` 前，`<script type="application/json" id="claims">`）：8 条，在契约要求的 3~8 条区间上限。

| value | label | quote | 口径 |
|---|---|---|---|
| 65.7% | Terminal-Bench 4.0 官方自报得分 | Terminal-Bench 4.0 得分 65.7% | 公司自报，博客脚注口径 |
| 58.2% | 同基准 GPT-6 Astra 得分 | GPT-6 Astra 的 58.2% | 官方博客转引 |
| 66.4% | 同基准 Claude Opus 5.5 得分 | Claude Opus 5.5 的 66.4% | 官方博客转引 |
| 55 | Artificial Analysis 独立智力指数（全球第四） | Artificial Analysis 独立智力指数 55 | 第三方，摘要级转引 |
| 90.5% | 未过滤检查点漏洞利用通过率 | 未过滤检查点 pass@3 为 90.5% | 自设基准，pass@3 |
| 81.0% | 发布版漏洞利用通过率 | 发布版 pass@3 为 81.0% | 自设基准，pass@3 |
| 2.8 万亿 | Kimi K3 基座总参数 | 2.8 万亿参数 | 官网一手，HTTP 200 / 94,238 字节 |
| 104B | 每 token 激活参数 | 激活 104B | 摘要级转引 |

**闸门校验**：`claim_gate.filter_declared()` 对本文件运行，声明 8 条、**通过 8 条**，全部 quote 在正文逐字命中，`is_suspect_label()` 无可疑标签。流水线阶段 7 第 ⑩ 项：断言层 1,131 条，**引用失效 0**。

## 四、质疑面与惊叹面同篇幅（实测）

派单要求「质疑面 65.7 vs 55 须与惊叹面同篇幅」。落地方式有三层，均为结构强制，不是口头承诺：

1. **并置台（第 1 幕）左右两面用同一套版式**：面板标题、口径行、图表、数据行、判读段五段一一对应，字号行高一致。
   - 判读段字数：**惊叹面 127 字 / 质疑面 133 字，差 6 字（4.7%）**
2. **双面档案（第 4 幕）6 组事实逐行对读**，同一 CSS grid 行内左右各一块，行高自动取最大值，天然等高；可点任一行点亮对应行。
   - 6 对字数：93/88、104/113、83/86、85/80、93/85、93/94
   - 合计：**惊叹 551 字 / 质疑 546 字，差 5 字（0.9%）**；单对最大差 9 字
3. **追问式交互把 65.7 与 55 摆到同一根对齐线上**（第 1 幕底部滑块）：一条红色虚线同时落在两张图上，实时显示这根线在两把尺子各自命中什么。拉到 65.7 时，左尺命中 Kimi K3.1 Pro，右尺最近点是 Opus 5.5 的 58，差 7.7，页面直接写「不可相减」。

## 五、impeccable detect（命令 + 结论）

```
命令：/app/working/workspaces/agents/content-creator/skills/impeccable/scripts/impeccable detect --json \
        2026-10-29/creative/2026-10-29-kimi-attack-ability-removal.html
```

**impeccable 已执行：命令 + 结论。**

| 轮次 | 输出 |
|---|---|
| 首轮 | 4 类：`low-contrast`(2, advisory)、`cramped-padding`(9, warning)、`flat-type-hierarchy`(1, advisory)、`skipped-heading`(2, warning) |
| 修法 | ① `--dim2` 由 `#8C7F6D` 提亮为 `#97887A`（4.4:1 → 5.0:1）；② 边框从容器移到内容行、`.act` 顶部留白、`.cal` 改列间距 26px 并给每格留内边距；③ 正文 15px / h3 22px / h2 26px+，拉开层级；④ 14 处 `<h4>` 全部改为 `<h3>` |
| 复跑（流水线注入返回链后再次复跑） | **`[]`**（0 条，含 advisory） |

原始输出已存 `notes/2026-10-29-kimi-attack-ability-removal-impeccable-detect.txt`。

## 六、运行时验证（Playwright / Chromium，1260×800 与多档视口）

| 检查 | 结果 |
|---|---|
| 页面 JS 运行时错误 | 0 |
| console.error | 0（file:// 加载时无外部请求） |
| 资源加载失败 / 4xx / 5xx | 0 / 0 / 0 |
| 首屏可见内容 | 14 个可见叶子（audit_pages 判空阈值为 8） |
| 被 opacity/visibility 隐藏的主容器 | 0 |
| 图表是否真的画出来 | 3 张 canvas 均有非零绘制像素，Chart 实例存在 |
| 横向滚动 | 七档视口均无，1280 档无越界元素 |
| 375px 触控目标 < 24px | 0 个 |

**交互实测（脚本驱动）**：

- 对齐线拉到 55.0 → 左尺无此位置，最近 GPT-6 Astra 58.2 差 3.2；右尺命中 Kimi K3.1 Pro
- 对齐线拉到 65.7 → 左尺命中 Kimi K3.1 Pro（自报）；右尺无此位置，最近 Opus 5.5 的 58 差 7.7
- 关掉第一阶段删除 → 开关状态、示意滑块（50）、读数（85.8）与「单阶段时官方没有公布任何数字」提示同步
- 两阶段均开 → 读数 81.0、差值 9.5 个百分点，与官方端点一致

## 七、流水线校验（`tools/autopublish.py`）

十项硬校验**全部通过**：① 计数 109=109 ✓ ② 缺文件 0 ✓ ③ 缺缩略图 0 ✓ ④ 缺标签 0 ✓ ⑤ 标签总数 238→243 未下降 ✓ ⑥ 标签丢失 0 ✓ ⑦ 快照契约 0 问题 ✓ ⑧ enrich 孤儿键 0、类型冲突 0 ✓ ⑨ 返回链缺失 0 ✓ ⑩ 断言引用失效 0 ✓。

- manifest 已重建：creative 55 件，total 109，latestDate 2026-10-29
- enrich 条目已补：agent = 创艺+绘界，highlights = 开放权重 / 删改稿 / 90.5→81.0 / 65.7 vs 55 / 不可相减 / xdev-bench-hard
- 返回展厅链路由 autopublish 阶段 5.5 自动注入（未手写），注入后复跑 detect 仍为 `[]`

## 八、作品结构（7 幕）

1. 报头与三行读数（90.5→81.0 / 65.7 / 55）
2. **并置台**：两把尺子左右并排 + 对齐线交互（65.7 与 55）
3. **减法台**：两阶段删除开关 + 示意滑块 + 90.5 / 81.0 柱状图（0 基线，右侧标出 9.5 差值括号）
4. 删改稿：三段官方原话逐字引用 + 红笔删改标记
5. **双面档案**：惊叹面与质疑面 6 组逐行对读
6. 不能这么写：5 条禁用表述与替代表述对照
7. 口径台账：5 类来源的取法、状态码、字节数与用途
8. 硬窗日历：10-29 → 11-01 → 11-04 → 11-04 之后（官方称将逐步抬高开放权重的 cyber 能力）

## 九、口径纪律（沿用开工前台账）

- 一手直取：`https://www.kimi.ai/blog/kimi-k3-1-pro`（HTTP 200 / 385,881 字节）、`https://www.moonshot.ai/`（HTTP 200 / 94,238 字节）
- 其余全部标注「摘要级转引，页面未直取」，包括 AA 指数 55、同基准复测约 67%、SWE-Marathon 51.7%、激活 104B、降价 33%、出口管制传闻
- 作品未出现「删除了攻击能力」「权重中的攻击能力已被抹除」「55 分对 65.7 分掉 10.7 分」「已被证实更安全」等禁用表述；这些禁用写法本身作为对照表出现在第 6 幕
- 滑块中段为示意插值，页面明写「官方只公布了两个端点」
- **未确认**：官方未公布任何第三方复核机制或复现安排，11-04 之后无人替发布方验证那 9.5 个百分点
