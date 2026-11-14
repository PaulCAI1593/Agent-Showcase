# 交付报告 · 选题415《战时算力治理五个可验证拐点》设计质量棘轮修复

> 作品：`works/2026-11-05/research/2026-11-05-wartime-compute-governance.html`（修复后 54,602 字节；修复前 54,651 字节，mtime 11-10 03:08）
> 主责：**研析（research-analyst）**　｜　任务：心跳重派修复（原派单 `task-100bab3e3d12` 已超时失败）
> 追踪线：算力·能耗·环境　｜　修复日期：2026-11-10　｜　截止：2026-11-11 02:00

---

## 一、排查结论（先给原因）

**原因：单件作品引入 7 条新 findings，根因是三处，全部落在本件，不涉及其它 127 件。**

**现象**：`tools/design_scan.py` 全量 1665 → 1672（+7），by_file 增量全部来自本件（0 → 7）。修复前单件复扫确认 7 条：`side-tab` 3、`skipped-heading` 3、`em-dash-overuse` 1。

**证据**（修复前 `impeccable detect <本件> --json` 逐条）：

- `side-tab` ×3 —— `border-left: 3px + border-radius: 4px`。根因：`.scope` 盒子用 3px 彩色左侧强调条 + 4px 圆角；页面有 3 个 `.scope` 盒子，各记 1 条。
- `skipped-heading` ×3 —— `<h2> "数据图" followed by <h4> "图 1 …" (missing h3)`、`<h2> "口径与验证" … <h4>`、`<h2> "来源分级" … <h4>`。根因：全文 9 个 `<h4>` 分属这 3 组，`h2` 之后直接跳到 `h4`，缺 `h3` 层，每组记 1 条。
- `em-dash-overuse` ×1 —— `41 em-dashes in body text`。规则口径（引擎 0.1.17 内置文案）：正文 ≥8 个破折号且密度接近「每 500 字 1 个」才触发。本件 41 个 `—` 字符、正文 10,493 字（去空白），密度 **1/256 字**，远超阈值。

**结论**：修法是「去侧边强调条、补齐标题层级、把破折号降为冒号/逗号/分号」，不改断言、不改事实、不推翻视觉体系。

## 二、改动点

| 位置 | 改动 |
|---|---|
| 作品 `:167` | `.scope` 的 `border-left:3px solid var(--brass)` → `1px`（保留 1px 铜色左边与 `.scope.warn` 红色左边，去掉粗侧条） |
| 作品 `:171` `:175` | `.scope h4` → `.scope h3`，`.scope.warn h4` → `.scope.warn h3`；`margin-bottom:10px` → `margin:0 0 10px`（压掉基础 `h3{margin:44px 0 12px}`） |
| 作品 `:187` | `.chart-frame h4` → `.chart-frame h3`；`margin-bottom:4px` → `margin:0 0 4px` |
| 作品 `:199` | `.src-group h4` → `.src-group h3`；`margin-bottom:10px` → `margin:0 0 10px` |
| 作品 `:549 :558 :567 :616 :622 :632 :651 :658 :671` | 9 处 `<h4>…</h4>` → `<h3>…</h3>`（标题文字一字未改） |
| 作品正文 21 行 | em-dash 41 → 4：16 行成对破折号（32 字符）改为冒号/逗号/分号；5 行日期区间 `10—11` → `10 至 11`（`11月10—11日` → `11月10至11日`）。保留的 4 个 `—` 是 `<title>` 与 `<h1>` 各 1 处中文破折号（标题须与 manifest 一致） |
| `enrich.json:7308` | `agent: ""` → `agent: "研析"`（补署名） |
| `manifest.json` | 由 `python3 tools/build_manifest.py` 重新生成并同步 `index.html` EMBEDDED；**未手工编辑** |
| `works/2026-11-05/notes/` | 新增 5 张修复后截图：`415-修复后-首屏-desktop.png`、`415-修复后-首屏-mobile-375.png`、`415-修复后-数据图-h3.png`、`415-修复后-口径与验证-h3.png`、`415-修复后-来源分级-h3.png` |

修改方式：一次性 Python 脚本按「(old, new, 期望出现次数)」精确替换，任一替换计数不符即中止且不落盘；落盘前逐条断言 8 条 claim quote + meta description + `<title>` 仍在原文中。
改后与改前备份 diff 复核（`diff -u /tmp/415.backup.html <作品>`）：共 38 行改动 = 正文 21 行（em-dash）+ 标签 9 行（h4→h3）+ CSS 8 行（选择器、外边距、侧边条）。

## 三、验收命令原始输出

### ① 门禁目标命令（AGENTS.md 规则14）

```
$ cd /app/working/shared/showcase && python3 tools/design_scan.py --scope file:works/2026-11-05/research/2026-11-05-wartime-compute-governance.html
扫描 1 件作品 · findings 0 条 · 涉及 0 件
严重度分布: {}
规则 Top:

（非全量扫描：只报告，不比棘轮）
FILE_SCAN_EXIT=0
```

**已验证：门禁命令 findings = 0（修复前 7 条），退出码 0。**

引擎直跑同一件：

```
$ cd /app/working/shared/showcase && /app/working/workspaces/default/skills/impeccable/scripts/impeccable detect works/2026-11-05/research/2026-11-05-wartime-compute-governance.html --json
[]
DETECT_EXIT=0
```

**已验证：`impeccable detect` 返回 `[]`，退出码 0（修复前 7 条）。**
0 findings → 无待修对象，本次未执行 polish 动作。

### ② 全库棘轮（确认 +7 已归零、且未误伤他件）

```
$ cd /app/working/shared/showcase && python3 tools/design_scan.py --scope all --top 6
扫描 130 件作品 · findings 1665 条 · 涉及 107 件
严重度分布: {'warning': 1285, 'advisory': 380}
规则 Top:
    1004  low-contrast
     117  skipped-heading
      85  dark-glow
      69  em-dash-overuse
      65  kicker-above-heading
      52  gray-on-color

✓ 棘轮通过：无一规则上升（基线 1665 → 当前 1665）
FULL_EXIT=0
```

**已验证：`skipped-heading` 120 → 117、`em-dash-overuse` 70 → 69、`side-tab` 回落基线；总 1665 = 基线 1665，无一规则上升，退出码 0。** `tools/design_snapshot.json` 已恢复为 `scope=all / total=1665`（全量口径，供心跳比对）。

### ③ 清单校验

```
$ cd /app/working/shared/showcase && python3 tools/build_manifest.py --check
[check] manifest 与磁盘 一致
  提示: 2 件作品缺 agent 署名（可在 enrich.json 补，…）
     - works/2026-11-06/research/2026-11-06-midterm-ai-repricing.html
     - works/2026-11-05/creative/2026-11-05-weight-editing-surgery.html
  护栏: index.html 207KB / 预算 400KB · EMBEDDED 144KB · 7 个月份
  断言: 1174 条 · 覆盖 122/128 件 (95%) · 待处理 535 · 无结构 8 · 重校验 1174/1174 通过
CHECK_EXIT=0
```

**已验证：退出码 0；断言层 1174/1174 复验通过（改正文未击穿 quote 断言）。**
退出码 0 → 按任务条件**未跑** `./tools/autopublish.sh`（该脚本未执行，无输出可引）。本件已不再出现在缺署名清单（清单由 3 件降为 2 件）。

### ④ 断言闸门单独复验

```
$ cd /app/working/shared/showcase && python3 tools/claim_gate.py --verify
重校验 1174 条断言
✓ 全部通过
CLAIM_EXIT=0
```

### ⑤ 运行时健康巡检

```
$ cd /app/working/shared/showcase && python3 tools/audit_pages.py works/2026-11-05/research/2026-11-05-wartime-compute-governance.html
巡检 1 件作品（真实加载 + 抓运行时错误）
========================================================
巡检完成：1 件，0 件有问题
✓ 全部作品页运行时健康
AUDIT_EXIT=0
```

### ⑥ 浏览器实测（Playwright，`/usr/bin/chromium`，file:// 直载）

```
desktop 1260×800：pageerror = 0，console.error = 0
  改造后的 9 个标题计算样式：
    .chart-frame h3（图 1/图 2/图 3）  font-size 16px  margin-top 0px
    .scope h3（口径警示/时间锚/验证记录） font-size 15px  margin-top 0px
    .src-group h3（A / B·C / 团队简报）   font-size 13px  margin-top 0px
  原有 5 个 .shell 内 h3（拐点 1-5）仍为 21px / margin-top 44px（首条 8px），未被波及
  .scope ×3：border-left 宽度 1px、border-radius 4px；warn 盒左边 rgb(160,58,42)（红），其余 rgb(125,90,28)（铜）
  横向溢出：scrollWidth 1260 = clientWidth 1260 → false
mobile 375×812：
  {"sw":375,"cw":375,"overflow":false}，9 个改造标题 checkVisibility 全部 true
```

**已验证：无运行时错误、标题层级改造未引起字号/间距漂移、无横向滚动。**
截图：`works/2026-11-05/notes/415-修复后-*.png`（5 张，已目视复核 `415-修复后-口径与验证-h3.png`：标题 15px 铜/红、左边 1px、正文标点正常）。

## 四、硬约束自检

| 约束 | 状态 | 证据 |
|---|---|---|
| 不改断言 quote 原文 | 已验证 | 替换脚本内置 8 条 quote + meta description + `<title>` 逐字在文断言，全部命中；`claim_gate --verify` 1174/1174 通过；`build_manifest --check` 重校验 1174/1174 通过 |
| 不手工编辑 `manifest.json` | 已验证 | 本会话对 manifest 只有 `python3 tools/build_manifest.py`（生成器）与 `--check`（只读）；署名改在 `enrich.json:7308` |
| 不 git push | 已验证 | 本会话未执行任何 git 写命令；`git status` 显示作品文件为未跟踪（`works/2026-11-05/…html` 不在 git 索引内），改动仅落在工作区文件 |
| em-dash 不新增 | 已验证 | 全文 `—` 计数 41 → 4（仅 `<title>`/`<h1>` 各 1 处成对破折号）；未引入任何新的 `—` |
| 拆小步执行 | 已验证 | 排查 → 单件修复 → 单件扫描 → 清单校验 → 署名 → 全量棘轮 → 巡检 → 截图 → 报告，各步独立完成，单步最长 < 2 分钟 |

## 五、未做 / 未验证

- 未跑 `./tools/autopublish.sh` —— `build_manifest.py --check` 退出码为 0，按任务条件不需要。
- 未执行 `impeccable polish` —— 本件 detect 0 findings，无待修对象。
- 未改动全库存量 1665 条 findings（107 件）—— 属棘轮存量批次治理，不在本次派单范围。
- 未改动另外 2 件缺署名作品（`2026-11-06-midterm-ai-repricing`、`2026-11-05-weight-editing-surgery`）—— 不在本次授权范围。
- 未做多断点（平板 768px）截图 —— 已测 1260px 与 375px 两端，中间断点未截图。

## 六、待确认

- 全库仍有 1665 条存量 findings、107 件带 findings —— 是否按批次安排 polish，请智囊排期。
- 剩余 2 件缺 `agent` 署名是否由流水线统一补 `enrich.json`，请智囊决定。

---

**结论：已完成并已验证。** 单件 findings 7 → 0（`design_scan --scope file` 退出码 0）；全库棘轮 1665 = 基线 1665、无一规则上升（退出码 0）；`build_manifest.py --check` 退出码 0、断言重校验 1174/1174 通过；`claim_gate --verify` 通过；`audit_pages` 0 问题；浏览器实测无 JS 错误、1260/375 两端无横向溢出；断言 quote 一字未改；未跑 git push、未手工编辑 manifest.json。

**签名：研析（research-analyst）　2026-11-10**
