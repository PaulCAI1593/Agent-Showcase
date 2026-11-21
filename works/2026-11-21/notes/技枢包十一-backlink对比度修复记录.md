# 技枢包十一 · backlink 对比度修复记录

- 日期：2026-11-21（BJ）
- 状态：已完成
- 范围：修复记录 + 作者本地补丁冲突清单 + 全量棘轮复验。本单不改任何 `works/**/*.html`，不改 `tools/add_backlink.py`。
- 背景：上一单 `task-38c2c2eaf136` 报 3600s 超时失败。模板修复已落盘，总指挥 10:53 实跑验收通过，本单不重做修复。

## 1. 旧行为成因

- 旧基础规则只有 `opacity:.86`，不声明 `color`。
- 文字色来自继承：页面规则 `a{color:var(--brass)}`。全库主 brass 值 `#7d5a1c`（32 件引用）。
- detect 不执行 JS → 拿不到 `on-dark-page`/`on-light-page` 变体类 → 按静态继承计算对比度。
- 反算（本单独立复算，WCAG 2.x 相对亮度，opacity 0.86）：`#7d5a1c@0.86` 叠 `#eaedea` = **4.01:1**；叠全库 18 种纸面 = 3.61–4.47:1。全部低于 4.5:1。
- 后果：11-19 两次因 `low-contrast` 打回。

## 2. 改动位置与前后代码

- 文件：`tools/add_backlink.py`；mtime 2026-11-21 03:09:46 BJ（UTC 2026-11-20 19:09:46）；17,362 字节。本单 `stat` 核对。
- 改动区：`:232-245`（diff 行号 `232c232,245`）。
- 旧版备份：`works/2026-11-21/notes/add_backlink.py.备份-V1-20261121-改1`。本单用 `diff` 对比备份与现版，得到下文原文。

改前（旧版 `:232`，原文）：

```python
        f'opacity:.86}}'
```

改后（现版 `:232-245`，原文）：

```python
        # ⚠️ 基础规则必须自带 color + background（包十一 2026-11-21）。
        # 旧行为：基础规则只有 opacity:.86，color 靠继承页面 a{color:var(--brass)}。
        #   detect 不执行 JS → 拿不到 on-dark/on-light 变体类 → 按静态继承算：
        #   brass@0.86 叠纸色 #eaedea = 4.0-4.2:1，低于 4.5:1（11-19 两次打回）。
        # 为什么 color 与 background 必须一起补：
        #   单一 color 在数学上无法同时达标 —— 浅纸面要暗字、深纸面要亮字。
        #   实测（含 opacity:.86 反算）只补 color：
        #     #654614 → 浅 5.21:1 / 深 1.92:1；#fafafa → 浅 1.11:1 / 深 13.39:1。
        #   自带底后文字压在自己的底上，与页面底色解耦：
        #     color:#fafafa + background:rgba(20,19,15,.92) → 浅 7.10-7.62:1 / 深 13.28-13.64:1。
        #   变体类 .on-dark-page/.on-light-page 特异性更高（id+class），运行时仍覆盖基础规则。
        f'opacity:.86;color:#fafafa;background:rgba(20,19,15,.92);'
        f'border:1px solid rgba(255,255,255,.16);'
        f'backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}}'
```

- 改动要点：基础规则同时声明 `color` + `background`。注释保留旧行为说明与反算数据。变体类在运行时仍以更高特异性（id+class）覆盖基础规则。

## 3. 反算依据（浅/深纸面各 ≥4.5:1）

- 口径：WCAG 2.x 相对亮度；元素 `opacity:.86`；文字压在药丸自有底上，与页面纸色解耦。
- 注释原文数据（只补 color 不可行）：`#654614` → 浅 5.21:1 / 深 1.92:1；`#fafafa` → 浅 1.11:1 / 深 13.39:1。
- 注释原文数据（自带底后）：浅 7.10–7.62:1 / 深 13.28–13.64:1。
- 本单独立复算。方法：`text = blend(#fafafa, 0.86, bg)`，`bg = blend(#14130f, 0.92×0.86, paper)`。
  - 浅纸面：全库 18 种实测 `--paper` → 7.46–8.15:1（`#eaedea` = 7.82:1）。
  - 深色底：全库实测高频深底 `#0b0c12`（163 处）、`#1d1d1f`（23 处）、`#14130f`、`#2a2a2c`、`#0a0a0a`、`#241F17` → 12.77–13.42:1。
  - 结论：浅/深纸面均 ≥4.5:1。复算与注释数值的口径略有差异，结论一致。
- 运行时证据（来源：总指挥 10:53 实跑；本单按「勿重做」约束未复核，标未验证）：抽样三件 detect findings 0 — `2026-11-19-ant-opening-bell`、`2026-11-20-anthropic-listing-ledger`、`2026-11-21-anthropic-coopetition-web`，`low-contrast` 不复现。

## 4. 全量棘轮复验（任务 3）

- 命令：`cd /app/working/shared/showcase && python3 tools/design_scan.py --scope all`
- 日志：`/tmp/design_scan_full_20261121.log`
- 扫描件数：**164**
- findings 总数：**1665**（涉及 107 件；warning 1285 / advisory 380）
- `low-contrast` 现值：**1004**。基线：**1004**（`tools/design_baseline.json`，ts 2026-11-04 14:27:48 UTC）。持平，未上升。
- 棘轮结果：**✓ 棘轮通过：无一规则上升（基线 1665 → 当前 1665）**
- 对比度分档：3–4.5:1 正文不达标 650 / 2–3:1 大字号不达标 241 / <2:1 几乎不可读 110。
- 规则 Top：`low-contrast` 1004、`skipped-heading` 117、`dark-glow` 85、`em-dash-overuse` 69、`kicker-above-heading` 65。
- 未使用 `--update-baseline`。基线文件 mtime 保持 2026-11-04 14:27:48 UTC，本单未改动。核对方法：`stat` + 读 `tools/design_scan.py:170`（仅在 `--update-baseline` 或基线缺失时写入基线）。
- 附注：正常扫描会覆写 `tools/design_snapshot.json`（工具设计行为）。本次 mtime 2026-11-21 04:55:29 UTC（12:55:29 BJ）。
- 本单未执行：`--update-baseline`、autopublish、build_manifest、服务重启、git push。

## 5. 作者本地补丁冲突清单（任务 2，只列不改）

- 全库命令 `grep -rn '#showcase-backlink{' works/ --include='*.html' | grep -v '.bak'` 命中 168 处。本单按基础规则全文归并为 7 种形态，逐条判定。
- 形态分布：
  - 旧模板注入（`...opacity:.86}`，无 color）：158 处。模板旧版产物，非本地补丁。
  - 新模板注入（`opacity:.86;color:#fafafa;background:rgba(20,19,15,.92)`）：3 处。`gpu-collateral-bonds.html:357`、`a-share-morning-divergence.html:303`、`anthropic-coopetition-web.html:185`。
  - **本地 color 补丁：7 处**（模板外来源）。明细如下表。
- 共同条件：
  1. 本单不动任何作品文件。清单交总指挥裁定。
  2. 删除顺序：除第 7 项外，各件注入仍为旧模板。必须先随心跳收敛换成新模板，再删补丁。直接先删会退回继承 brass（3.61–4.47:1），缺陷回归。
  3. 单色补丁无法双面达标。本单反算（5 种浅纸面 / 3 种深底）：`#654614` 浅 4.69–5.79、深 1.76–1.97；`#644816` 浅 4.62–5.70、深 1.78–2.00；`#5f4d1e` 浅 4.47–5.52、深 1.84–2.06；`#171a18` 浅 9.15–11.26、深 1.04–1.09；`#14130f` 浅 9.90–12.21、深 1.00–1.09。每色必有一面不达标。

| # | 文件:行号 | 补丁内容 | 现状 | 建议 |
|---|---|---|---|---|
| 1 | `works/2026-11-19/research/2026-11-19-nvidia-post-huang-receipt.html:304` | 独立规则 `#showcase-backlink{color:#654614}`（注入样式在 `:313`，旧模板无 color） | 补丁生效中 | 删除（随收敛） |
| 2 | `works/2026-11-19/research/2026-11-19-shenzhen-summit-eve.html:346` | 注入样式基础规则内嵌 `opacity:.86;color:#5f4d1e}`，无 background | 单色不达标：深纸面 1.84–2.06:1 | 删除（重注入自动消除） |
| 3 | `works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html:75` | 独立规则 `#showcase-backlink{color:#171a18}`（注入 `:294`，旧模板） | 补丁生效中 | 删除（随收敛） |
| 4 | `works/2026-11-16/research/2026-11-16-nvidia-three-test-week.html:62` | 独立规则 `#showcase-backlink{color:#644816}`（注入 `:260`，旧模板） | 补丁生效中 | 删除（随收敛） |
| 5 | `works/2026-11-17/research/2026-11-17-monday-divergence.html:59` | 独立规则 `#showcase-backlink{color:#644816}`（注入 `:319`，旧模板） | 补丁生效中 | 删除（随收敛） |
| 6 | `works/2026-11-17/research/2026-11-17-europe-open-model-procurement.html:310` | 注入样式基础规则内嵌 `text-decoration:none;color:#14130f;transition:...` | 单色不达标：深纸面 1.00–1.09:1 | 删除（重注入） |
| 7 | `works/2026-11-21/research/2026-11-21-a-share-morning-divergence.html:60` | 独立规则 `#showcase-backlink{color:#644816}`（注入 `:303` 已是新模板） | 死代码：新模板 `color:#fafafa` 同特异性、声明在后，覆盖补丁 | 删除（可直接删） |

- 相对总指挥点名的 2 件（第 1、2 项），另有 5 处同类补丁：第 3–7 项。
- 复核方法：168 处命中按基础规则全文归并为 7 形态，逐形态判定来源；再用 `opacity:.86;color:` 变体检索交叉验证，无遗漏。

