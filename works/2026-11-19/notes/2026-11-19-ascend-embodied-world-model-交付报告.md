# 交付报告 · 配额之外的那一半（选题448 · 创意类）

- **交付物**：`shared/showcase/works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html`
- **状态**：已完成。初稿 2026-11-19 02:16（UTC 18:16）落盘，距开工 11 分钟，早于 14:00 截止。
- **追踪线**：机器人与具身
- **类型**：创意类（无研究类模板，视觉/叙事/交互自定）

---

## 1. 文件

| 项 | 实测值 |
|---|---|
| 字节数 | **57297 bytes**（UTF-8） |
| 形态 | 单文件 HTML，CSS/JS 全内联 |
| 远程依赖 | 0（grep 无 `src="http…"` / `href="http…"`；`audit_pages.py` 远程依赖未落定 0 件） |
| 字体 | 本地 `../../../assets/vendor/fonts/noto-serif-sc.css` |

## 2. 两段声明

- **追踪线声明**：`<head>` 内 `<meta name="showcase-beat" content="机器人与具身">` — 13 条封闭集内。
- **断言声明**：`</body>` 前 `<script type="application/json" id="claims">`，**6 条**（要求 3~8）。每条 quote 在本作品正文中逐字命中（`claim_gate.normalize(strip_code(html))` 子串校验 6/6 通过；标签 G2 可疑检查 6/6 通过）。

| value | label | quote（正文逐字） |
|---|---|---|
| 第一（2 个基准） | CloudRobo-WM1.2 基准排名（RoboTwin 2.0 / LiberoPro 2.0） | `在 RoboTwin 2.0、LiberoPro 2.0 两个基准均列第一` |
| 16500+ | CloudRobo 平台开发者数 | `CloudRobo 平台已超 16500 名开发者` |
| 5 家（点名） | CloudRobo 生态伙伴厂商数 | `生态伙伴含亿嘉和、拓斯达、福龙马、节卡、千寻等` |
| 昇腾 | CloudRobo-WM1.2 训练算力平台 | `基于国产昇腾算力训练` |
| 共享世界模型骨干 + DualAct | CloudRobo-WM1.2 架构组成 | `采用共享世界模型骨干与原生 DualAct 架构` |
| Gemini Robotics 2.5 / GR00T 2 | 依赖英伟达生态的对照模型 | `此前海外具身大脑模型（Gemini Robotics 2.5、GR00T 2）高度依赖英伟达生态` |

## 3. 拟用指标标签（4 条，逐字照抄，全部实际使用）

| 标签 | 位置 | 页面值 |
|---|---|---|
| `CloudRobo-WM1.2 训练算力平台` | 02 节指标条 `.metric-label` + 断言 label | 昇腾 |
| `CloudRobo-WM1.2 基准排名（RoboTwin 2.0 / LiberoPro 2.0）` | 同上 | 第一 ×2 |
| `CloudRobo 平台开发者数` | 同上 | 16500+ |
| `CloudRobo 生态伙伴厂商数` | 同上 | 5 家（点名） |

4/4 命中，无改写、无增删。

## 4. 交互形式清单（7 种，要求 ≥2）

1. **算力配比分界线**（hero，可拖 range + 键盘方向键）：拖动即重绘画布世界，右半（昇腾侧）地形随配比起伏；顶栏读数同步 `昇腾 N% · 英伟达生态 100−N%`。
2. **动作 / 世界 视角切换**（tablist）：同场景两种读法，图与结论同步切换。
3. **架构悬停揭示**：共享世界模型骨干 / 原生 DualAct 架构 / 动作分支 A·B / 昇腾训练算力底座，`mouseenter`+`focus`+`click`+`Enter` 四种触发，非聚焦部件降透明度。
4. **训练侧 vs 推理侧切换 + 双基准成绩对照**：训练侧卡显示 RoboTwin 2.0、LiberoPro 2.0 均「第 1」；推理侧卡是依赖对照（Gemini Robotics 2.5 / GR00T 2），并显式声明「这一卡是对照，不是成绩」。
5. **配额盲测**（游戏）：答题 → 判定 → 出证据（正确/错误两种反馈色与文案）。
6. **生态伙伴网络图谱**：中心 CloudRobo + 5 家点名厂商 + 外圈 165 点（1 点 ≈ 100 人，已标注示意），悬停/聚焦更新侧栏文案与节点尺寸。
7. **硬件依赖度滑块**（昇腾 ↔ 英伟达）：0 与 100 两端各挂一条有出处的引文，中间态显式标注「概念示意，两端之外没有被公开披露的比例」。

对齐实测：分界线与滑块拇指在 10 / 50 / 90 三点的水平偏差 ≤1px（像素扫描取证，见 `notes/_align_check.py`）。

## 5. 断言纪律

- 「基于国产昇腾算力可以训练出世界领先的具身世界模型」只以**厂商自述**出现：06 节引文框带 `厂商自述 · 未独立验证` 标签 + `华为云称` + 来源；**未写成团队已验证的结论，也未进 claims**。
- 基准卡标注「分数未公开 · 只公开名次」，不做跨模型排名推断。
- 滑块配比、网络点数、轨迹/状态场图形均标注为示意。

## 6. impeccable 执行记录

**impeccable 已执行（命令 + 结论）**

| 命令（cwd = `/app/working/shared/showcase`） | 结论 |
|---|---|
| `scripts/impeccable context --target works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html` | 已加载；返回 `MANUAL_DETECTOR_REQUIRED`，指示成稿后跑 detect |
| `scripts/impeccable detect --json <同上>` 第 1 轮 | **27 findings**：cramped-padding 17、numbered-section-labels 6、side-tab 2、repeating-stripes-gradient 1、em-dash-overuse 1 |
| `scripts/impeccable detect --json <同上>` 第 2 轮 | **2 findings**：wide-tracking 1、cramped-padding 1 |
| `scripts/impeccable detect --json <同上>` 最终 | **0 findings**（`notes/impeccable-detect-final.json`） |
| `reference/craft-floor.md` 逐条自查 | 见下方修复清单 |

修复清单（audit → polish 一轮完成）：

- 删除 6 处编号章节眉题 `01·开场 … 06·收尾`（`numbered-section-labels` + craft-floor「眉题在标题之上」禁令）。
- 删除 hero 眉题与 hero 指标条（hero-metric 模板），日期/开源状态改为标题下方副署。
- 删除 `.bcard::after` 3px 底部色条、`.bcard__bar i` 重复渐变条纹（side-tab / repeating-stripes）。
- `.arch__cap`、`.dep__quote` 的 3px 彩色 `border-left` 改全框；`.prose` 降为 1px。
- 正文破折号 `—` 由 12 降到 **0**。
- `.hero__by` 字距 0.09em → 0.05em（wide-tracking）。
- **padding 里的 `clamp()` 全部改 token**：用 `/tmp/impeccable-probe2.html` 复现证明检测器把 `clamp()` padding 判为 0（`var()` 正常），故引入 `--pad / --gutter / --sec-y / --hero-y / --seam-y` 五档 token + 900px / 560px 断点，cramped-padding 17 → 0。

## 7. 验证

- 已验证 · `python3 tools/audit_pages.py <本文件>` → 「巡检 1 件，0 件有问题」，运行时健康、远程依赖 0。
- 已验证 · `python3 tools/claim_gate.py --verify`（全库）→ 1338 条断言全部通过；本作 6 条 declared quote 6/6 命中正文。
- 已验证 · Playwright 1260×860 / 375×812：`console_errors=[]`、`scrollWidth == innerWidth`（1260 / 375，无横向滚动）、`mobile_errors=[]`。
- 已验证 · 键盘：Tab 遍历 14 个交互元素，全部 `outline: solid 2px rgb(245,185,66)`；range 方向键 50 → 52。
- 已验证 · `prefers-reduced-motion: reduce`：画布仍绘制 417 个静态像素（不跑 rAF），h1 可见。
- 已验证 · 对比度：21 组前景/背景比对，最低 **6.8:1**（要求 ≥4.5:1），见 `notes/_contrast_check.py`。
- 已验证 · 断言/标签/追踪线/路径硬约束脚本复查：6 claims、4 标签逐字、`机器人与具身`、零远程引用。
- 未验证 · `./tools/autopublish.sh` 未运行：它会重建 `manifest.json` / `index.html` / `enrich.json`，属流水线阶段 5.5，本次不代跑、也未手工改动这三个文件。
- 未验证 · 真机触屏拖拽：仅 Chromium 桌面 + 375 视口模拟（`audit_pages` 口径下无运行时问题）。

## 8. 过程材料（均在本目录）

预览：`preview-s1.png` … `preview-s6.png`、`preview-m-hero.png`、`preview-m-s3.png`、`preview-desktop.png`、`preview-mobile.png`
检测：`impeccable-detect-01/02/03/final.json`
脚本：`_render_check.py`、`_contrast_check.py`、`_focus_check.py`、`_align_check.py`、`_thumb_scan.py`、`_layout_probe.py`、`_shots2.py`
