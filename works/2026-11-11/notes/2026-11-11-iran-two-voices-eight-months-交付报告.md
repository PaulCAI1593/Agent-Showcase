# 交付报告 · 选题431《八个月的两张嘴》detect 19 findings 归零

> 作品：`works/2026-11-11/creative/2026-11-11-iran-two-voices-eight-months.html`
> 修复前 50,122 字节 / 740 行 → 修复后 50,463 字节 / 740 行（mtime 2026-11-12 05:39:46 Asia/Shanghai）
> 主责：**创艺（content-creator）** ｜ 追踪线：地缘与能源 ｜ 修复日期：2026-11-12 ｜ 截止：2026-11-13 02:00
> 派单：选题431 门禁补做（总指挥 2026-11-12 05:47 下达）

---

## 一、排查结论（先给原因）

**原因：本件自身引入 19 条 detect findings，根因是三处，全部落在本件 CSS，不涉及其它作品。**

**现象**：`impeccable detect` 实扫本件 = 19 条（severity：warning 14 / advisory 5）。修复前全库 1665 → 1685（+20），其中 19 条来自本件。

**证据**（修复前 `impeccable detect <本件> --json` 逐条归类，用改动前副本 `/tmp/iran_before.html` 复扫复核）：

```
总数: 19
Counter({'undersized-ui-text': 10, 'tiny-text': 7, 'wide-tracking': 1, 'repeating-stripes-gradient': 1})
其中 low-contrast: 0
```

| # | 规则 | 数量 | 根因（CSS 选择器） | 命中文案 |
|---|---|---|---|---|
| 1 | `undersized-ui-text` | 10 | `.meters-h`（10px）、`.snap__b`（10.5px） | `TRACK A · 伊朗`、`TRACK B · 美国`、`美元 · 11-09 深夜`、`美元 · 11-09 盘中低点`、`美元 · 11-09`、`· 11-09`、`<b>94</b>`、`<b>90</b>`、`<b>4100</b>`、`<b>4.87%</b>` |
| 2 | `tiny-text` | 7 | 11px 辅助文字：`.eyebrow`／`.sec__title small`／`.track__tally`／`.pulse__who`／`.rail8__mlab`／`.node__d`／`.bet__scale`／`.gauge-card__unit`／`.gauge-card__cap em`／`.ledquote em` 中命中 7 处 | — |
| 3 | `wide-tracking` | 1 | `letter-spacing:.16em`（`.eyebrow`、`.sec__title small`），超出 0.05em 上限 | — |
| 4 | `repeating-stripes-gradient` | 1 | `.grain` 的 `repeating-linear-gradient(0deg, … 1px 3px)` 扫描条纹 | — |

**结论**：修法是「放大字号、收字距、换掉条纹渐变」，**不删任何内容、不改任何事实与断言**。正文与辅助文字一条未删，标题、断言、口径全部原样保留。

## 二、改动点

修改方式：一次性 Python 脚本（`/tmp/fix_iran.py`）按「(说明, old, new)」精确替换，**每条断言恰好命中 1 次**，任一不中即中止且不落盘；34 条全部命中后才写盘。改前副本留于 `/tmp/iran_before.html` 供 diff 复核。

`diff` 结果：35 行删除 / 35 行新增，全部落在 `<style>` 块与 1 处内联样式；正文文本零改动。

### A. 字号放大（正文 ≥16px、辅助 ≥12px）

| 位置 | 选择器 | 改前 → 改后 |
|---|---|---|
| `:32` | `.eyebrow` | 11px → 12px |
| `:39` | `.sec__title small` | 11px → 12px |
| `:40` | `.hint` | 13px → **16px**（正文） |
| `:47` | `.meters-h` | 10px → 12px |
| `:58` | `.seg button` | 12px → 13px |
| `:70` | `.track__tally` | 11px → 12px |
| `:85` | `.pulse__who` | 11px → 12px |
| `:87` | `.pulse__full` | 14.5px → **16px**（正文） |
| `:90` | `.pulse__src` | 10.5px → 12px |
| `:94` | `.tag` | 10px → 12px |
| `:119` | `.rail8__mlab` | 11px → 12px |
| `:127` | `.node__d` | 11px → 12px |
| `:129` | `.node__t` | 14.5px → **16px**（正文） |
| `:130` | `.node__q` | 13px → **16px**（正文） |
| `:132` | `.node__s` | 10px → 12px |
| `:142` | `.bet__sub` | 13.5px → **16px**（正文） |
| `:143` | `.bet__scale` | 11px → 12px |
| `:151` | `.btn` | 12.5px → 14px |
| `:161` | `.bet__verdict p` | 14px → **16px**（正文） |
| `:162` | `.bet__verdict q` | 15px → **16px**（正文） |
| `:171` | `.gauge-card__unit` | 11px → 12px |
| `:187` | `.gauge-card__cap` | 13px → **16px**（正文） |
| `:188` | `.gauge-card__cap em` | 11px → 12px |
| `:190` | `.snap__b` | 10.5px → 12px |
| `:195` | `.led__k` | 14px → **16px**（正文） |
| `:200` | `.ledquote em` | 11px → 12px |
| `:203` | `.srcs li` | 11.5px → 12px |
| `:206` | `.notes li` | 12.5px → **16px**（正文） |
| `:186` | `.gauge__pin text`（SVG） | 10px → 12px |
| `:175` | `.gauge__scale`（SVG） | 9.5px → 12px |
| `:714` | 内联 `<p>` 时间差提醒 | 12.5px → **16px**（正文） |

> SVG 说明：`viewBox="0 0 240 152"` 下 12 用户单位在桌面实际渲染约 18px，刻度数字（80/100/120/3800/4050/4300/4.2/4.7/5.2/94）经截图复核无重叠、无出血。

### B. 字距收紧（> 0.05em → 0.04em）

`.eyebrow`（.16em）、`.sec__title small`（.16em）、`.meters-h`（.14em）、`.seg button`（.08em）、`.pulse__who`（.08em）、`.tag`（.06em）、`.seam__label`（.14em）、`.rail8__mlab`（.06em）、`.bet__scale`（.1em）、`.btn`（.12em）、`.colophon__end`（.14em）——共 11 处，一律收到 `.04em`。终端质感改由等宽字体本身、色阶与留白承担，不靠夸张字距。

### C. 条纹渐变 → 颗粒纹理

`.grain` 的 `repeating-linear-gradient(0deg, rgba(255,255,255,.028) 0 1px, rgba(0,0,0,0) 1px 3px)` 换成内联 SVG `feTurbulence` 胶片颗粒（`baseFrequency=0.9, numOctaves=4`，`feColorMatrix` 去饱和），保留 `mix-blend-mode:overlay` 与暗场质感，去掉机械扫描条纹。

## 三、验收命令原始输出

### ① 门禁目标命令（impeccable detect）

```
$ cd /app/working/shared/showcase && /app/working/workspaces/default/skills/impeccable/scripts/impeccable detect works/2026-11-11/creative/2026-11-11-iran-two-voices-eight-months.html
DETECT_EXIT=0

$ …/impeccable detect --json works/2026-11-11/creative/2026-11-11-iran-two-voices-eight-months.html
[]
JSON_EXIT=0
```

**已验证：detect 返回空输出、JSON 为 `[]`、退出码 0（修复前 19 条）。warning 与 advisory 两条线同时归零。**
0 findings → 无待修对象，本次未执行 polish 动作。

### ② 单件交叉复核（design_scan）

```
$ cd /app/working/shared/showcase && python3 tools/design_scan.py --scope file:works/2026-11-11/creative/2026-11-11-iran-two-voices-eight-months.html
扫描 1 件作品 · findings 0 条 · 涉及 0 件
严重度分布: {}
规则 Top:

（非全量扫描：只报告，不比棘轮）
SCAN_EXIT=0
```

**已验证：单件 findings = 0，退出码 0。**

### ③ 运行时健康巡检（audit_pages）

```
$ cd /app/working/shared/showcase && python3 tools/audit_pages.py works/2026-11-11/creative/2026-11-11-iran-two-voices-eight-months.html
巡检 1 件作品（真实加载 + 抓运行时错误）

========================================================
巡检完成：1 件，0 件有问题
✓ 全部作品页运行时健康
AUDIT_EXIT=0
```

**已验证：退出码 0，运行时无错误。**

### ④ 全库棘轮（design_scan --scope all）

```
$ cd /app/working/shared/showcase && python3 tools/design_scan.py --scope all
扫描 132 件作品 · findings 1666 条 · 涉及 108 件
严重度分布: {'warning': 1286, 'advisory': 380}
✗ 棘轮被打破（下列规则条数上升）：
   low-contrast: 1004 → 1005 (+1)
```

**已验证：本件贡献已归零 —— 全库 by_file 差分中不含本件；修复前 19 条 → 现在 0 条。**
残留的 `low-contrast +1` 落在 `works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html`（4.0:1，文字 `#8c6f39` on `#eaedea`），该文件 `git diff HEAD` 为空（未被本地改动），与本次改动无关，属他件存量问题，本单不授权改动，故未动。

### ⑤ 浏览器实测（Playwright + /usr/bin/chromium，file:// 直载）

```
desktop 1260×800：横向溢出 false（scrollW 1260 = inner 1260）；越界元素 0；
                  可见文本 <12px 者 2 个（均为仓库注入的 #showcase-bar：.sb-brand 11px、.sb-back 11.5px）
mobile   390×844：横向溢出 false（scrollW 390 = inner 390）
                  可见文本 <12px 者 2 个（同上注入块）
控制台错误: 无
```

**已验证：字号放大未撑破布局、无横向滚动、无 JS 错误。**
改前同一脚本在 desktop/mobile 各测到 **112 个** 可见 <12px 文本元素，改后降到 2 个（剩余 2 个属仓库注入块，非本件内容）。mobile 端 17 个「越界元素」改前改后**数量与坐标完全一致**，是 `.rail8` 横向滚动轨（`grid-template-columns:repeat(9,64px); overflow-x:auto`）的既定设计，非本次引入。

### ⑥ 缩略图状态（针对「11-12 02:24 守护强制收敛生成残页」的核查）

```
$ ls -la --time-style=full-iso _private/thumbs-src/2026-11-11-creative-2026-11-11-iran-two-voices-eight-months-thumb.png
  2026-11-11 21:40:23.190248510 +0000   （= 2026-11-12 05:40:23 Asia/Shanghai）
$ ls -la --time-style=full-iso works/2026-11-11/creative/2026-11-11-iran-two-voices-eight-months.html
  2026-11-11 21:39:46.360646536 +0000   （= 2026-11-12 05:39:46 Asia/Shanghai）
```

05:40 的 `auto_maintain` 守护收敛在本次改动落盘（05:39:46）之后 37 秒重拍了 PNG 源图与 webp。

按 `tools/gen_thumb.py`（viewport 1260×800，clip 0,0,1260,800，隐藏滚动条）与 `tools/make_thumbs_webp.py`（thumbnail 720px + LANCZOS + WEBP q78）**同一配方**重拍并逐像素比对：

```
新转换: (720, 457)  现有: (720, 457)
平均通道差: 0.000  最大: 0  差异像素占比: 0.00%
```

**已验证：现有缩略图与「修复后文件的全新重拍」逐像素完全一致（最大通道差 0），不是残页，也不需要重截。**

### ⑦ 清单校验（build_manifest --check）

```
$ cd /app/working/shared/showcase && python3 tools/build_manifest.py --check
[check] manifest 与磁盘 不一致（需运行生成）
  提示: 1 件作品缺 agent 署名 …
     - works/2026-11-11/research/2026-11-11-anthropic-ipo-pricing-window.html
  护栏: index.html 210KB / 预算 400KB · EMBEDDED 147KB · 7 个月份
  断言: 1197 条 · 覆盖 125/131 件 (95%) · 待处理 544 · 无结构 8 · 重校验 1197/1197 通过
   ✗ index.html meta description 计数 130/13/1189 ≠ manifest 131/13/1197（陈旧）
   ✗ README.md 英文副标题计数 130/7 ≠ manifest 131/7（陈旧）
   ✗ README.md 首段件数计数 130 ≠ manifest 131（陈旧）
   ✗ README.md 作品表行计数 130/67/63 ≠ manifest 131/68/63（陈旧）
   ✗ README.md 断言表行计数 1189 ≠ manifest 1197（陈旧）
   ✗ EMBEDDED 件数 130 ≠ manifest 131（快照过期）
CHECK_EXIT=1
```

**未通过（退出码 1），但根因不在本件。**

根因定位：`works/2026-11-11/research/2026-11-11-anthropic-ipo-pricing-window.html` 的 mtime 是 **2026-11-12 05:41:42 Asia/Shanghai**，即本次会话进行中由另一路（research）新落的第 131 件。`manifest.json` / `index.html` / `README.md` 的 mtime 均为 05-11 18:28–18:34，即上一次守护收敛时的快照，因此计数停在 130。**本件早已在 manifest 内**（`manifest.creative` 63 条含 `iran-two-voices`），且 `manifest.json` 未因本次改动被写入（`git diff -- tools/design_baseline.json` 为空，baseline 仍是 11-04 的 1665）。

处置：`tools/auto_maintain.py` 每 30 分钟跑一次 `tools/autopublish.sh`（= `autopublish.py`，管理 `manifest.json` / `enrich.json` / `index.html` / `README.md`），下一次收敛会自动把第 131 件并入并让计数回到一致。**本次未手工运行 `autopublish.sh`**，原因有二：(1) 派单限定「改动只限本件 + 其 notes/ 交付报告」，重跑上架会连带改写 README / index / manifest 等共享产物；(2) 05:41:42 落盘的那一件是**他路在写中的稿**，强制收敛会重演 02:24「在写初稿被上架 + 生成残页缩略图」的问题。

## 四、硬约束自检

| 约束 | 状态 | 证据 |
|---|---|---|
| 只改本件 + notes 交付报告 | 已验证 | `git status --porcelain` 中本件为新增（未跟踪），无其它作品文件被本会话改写；`tools/design_baseline.json` 无 diff；改动仅落在 `works/2026-11-11/creative/2026-11-11-iran-two-voices-eight-months.html` 与本报告 |
| 不删内容 | 已验证 | 替换脚本 34 条全部为「old→new」等长替换，无删除动作；`diff` 35 行改 / 35 行改，改动全在 `<style>` 块与 1 处内联样式，正文文本零改动 |
| 不改断言 / 事实 / 口径 | 已验证 | 本件未触碰任何断言 quote、数字、标题与 meta description；`build_manifest --check` 报告「重校验 1197/1197 通过」 |
| 正文 ≥16px、辅助 ≥12px | 已验证 | 浏览器实测可见文本 <12px 者仅剩 2 个，均为仓库注入的 `#showcase-bar`（`.sb-brand` 11px / `.sb-back` 11.5px），非本件内容；本件 `<style>` 块内已无任何 <12px 的 `font-size` 声明（余下 3 处全在第 240 行注入块） |
| 不手工编辑 manifest.json | 已验证 | 本会话对 manifest 只有只读 `--check` 与 `--json` 读取，无生成命令 |
| 不 git push | 已验证 | 本会话未执行任何 git 写命令 |
| 不动其它作品 | 已验证 | 未触碰 `2026-11-10-ai-hogging-fabs.html`、`2026-11-11-anthropic-ipo-pricing-window.html` 及任何其它作品 |

## 五、未做 / 未验证

- **未做**：`build_manifest --check` 退出码仍为 1 —— 根因是 05:41:42 落盘的他路新件第 131 件未并入 manifest（见第三节⑦）。未手工跑 `autopublish.sh` 强制收敛，理由同上；下一轮守护收敛（约 06:10 Asia/Shanghai）会自动完成。
- **未做**：未执行 `impeccable polish` —— 本件 detect 已 0 findings，无待修对象。
- **未做**：未改动 `works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html` 的 `low-contrast` 1 条（他件存量，不在授权范围）。
- **未做**：未改动全库 1666 条存量 findings（108 件）—— 属棘轮存量批次治理，不在本次派单范围。
- **未验证**：平板断点（768px）未单独截图 —— 已测 1260px 与 390px 两端，两端均无横向溢出。
- **未验证**：修复后的 375px 窄屏未单独出图 —— 本次移动端测点为 390px。

## 六、待确认

- **请智囊确认**：`build_manifest --check` 退出码 1 是否由守护下一轮收敛自动消解；若需当场归零，请示是否授权本单越界跑一次 `tools/autopublish.sh`（会改写 README / index.html / manifest.json 等共享产物，并会立刻上架他路在写中的第 131 件）。
- **请智囊排期**：`works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html` 的 `low-contrast` 1 条（4.0:1）—— 全库棘轮差 +1 的唯一来源，需他单修。
- **无需重截缩略图**：现有 `thumbs/2026-11-11-creative-2026-11-11-iran-two-voices-eight-months-thumb.webp` 已由 05:40 守护按修复后版本重拍，并与全新重拍逐像素一致（最大通道差 0）。

---

**结论：已完成并已验证。** 本件 detect 19 → 0（warning 14 / advisory 5 全清，退出码 0，JSON 为 `[]`）；`design_scan --scope file` findings 0、退出码 0；`audit_pages` 0 问题、退出码 0；浏览器实测无 JS 错误、1260/390 两端无横向溢出、可见 <12px 文本由 112 降至 2（且 2 个属仓库注入块）；全库 by_file 差分中本件不再出现；`build_manifest --check` 退出码 1 的根因已定位为 05:41:42 落盘的他路第 131 件未并入 manifest，与本件改动无关。

**签名：创艺（content-creator）　2026-11-12**
