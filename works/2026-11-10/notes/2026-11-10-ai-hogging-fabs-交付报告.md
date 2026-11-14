# 选题426《AI 抢走整座工厂之后》交付报告

- 作品：`works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html`
- 最终状态：60,224B，mtime 2026-11-12 05:43:56（Asia/Shanghai）
- sha256：`38e049a1a199505108b003b38bcd6ecd9ebfee7efa93d6771dad49cba8f3c23c`
- 报告补写时间：2026-11-12 11:40—11:50（Asia/Shanghai），由研析补交（规则14 留痕）
- 本次只补报告，**未再改动作品 HTML**：补写前后 sha256 一致。

---

## 1. 这次修了什么

### 1.1 问题

初稿 detect 报 1 条 `low-contrast`（severity=warning，对比度分档「3-4.5:1 正文不达标」）。
本轮用当前件回退我加的 6 行修复代码，得到 **59,701B 复刻件**（与总指挥记录的改前字节数 59,701B 一致；
原改前文件已被覆盖，无法比对它的 sha256）。对该复刻件重跑 detect，findings 仍为 1 条：

```
[low-contrast] 4.0:1 (need 4.5:1) — text #8c6f39 on #eaedea
```

### 1.2 命中元素与取值链（改前）

命中元素是展厅 backlink「回到档案柜」`#showcase-backlink`，由 autopublish 注入在 `<body>` 首部。

| 项 | 改前取值 | 位置 |
|---|---|---|
| 元素 | `#showcase-backlink`（注入的「回到档案柜」链接） | body 首部注入块 |
| 注入样式 | `opacity:.86`，底色透明，`font:500 13px/1` | 注入的 `<style>` |
| 静态审计回落规则 | `a{color:var(--brass)}` | 作品 `:69` |
| 文字色 token | `--brass:#7d5a1c` | 作品 `:43` |
| 底色 token | `--paper:#eaedea` | 作品 `:36` |

成因：静态审计不跑页面 JS，拿不到运行时才由脚本加上的 `.on-dark-page` / `.on-light-page` 类，
于是层叠回落到页内 `a{color:var(--brass)}`；再把 `opacity:.86` 与 `--paper` 合成：

- 合成有效文字色 = 0.86 × #7d5a1c + 0.14 × #eaedea = **#8c6f39**
- 对比度 = **4.00:1**（< 4.5:1 正文门槛），与检测器报出的 4.0:1 完全吻合

### 1.3 改法与改后取值

只改色值，不改字号、不删内容。在 `a{color:var(--brass)}` 之后加 5 行说明注释 + 1 条规则：

```css
/* 展厅 backlink 由发布管线注入，底色透明 + opacity:.86。静态审计按源码做层叠，
   拿不到运行时才加上的 .on-dark-page/.on-light-page 类，于是回落到上面的 a 规则，
   把 brass 与 opacity:.86 复合到 --paper 上（= #8c6f39，4.0:1，正文不达标）。
   这里用 ID 权重显式钉住它的文字色：审计侧复合后仍远高于 4.5:1，
   运行时仍由 .on-dark-page / .on-light-page 的类规则接管，外观不变。 */
#showcase-backlink{color:#171a18}
```

| 项 | 改前 | 改后 |
|---|---|---|
| 目标元素 | `#showcase-backlink` | 同（未换元素） |
| 文字色 | 回落 `var(--brass)` = #7d5a1c | **`#171a18`**（等于本页 `--ink`，`:38`） |
| 字号 | 13px / 500（注入样式） | **未改** |
| opacity | .86 | 未改 |
| 合成有效色 | #8c6f39 | **#353835** |
| 对比度（对 #eaedea） | **4.00:1**（不达标） | **10.07:1**（达标） |
| 纯色对比度（不计 opacity） | 5.31:1 | **14.87:1** |

规则落在作品 `:69` 之后、`:75`（`#showcase-backlink{color:#171a18}`）。文件 56,398B → 59,701B（管线注入 backlink）
→ **60,224B**（加本次修复 523B）。

### 1.4 运行时外观不变（已实测）

类规则 `#showcase-backlink.on-dark-page` 的特异度为 (1,1,0)，高于单 ID 的 (1,0,0)，运行时仍由类规则接管。
本轮用 Chromium 实加载该页取计算样式：

```
cls=on-dark-page  color=rgb(20, 19, 15)  opacity=0.86
bg=rgba(252, 252, 250, 0.92)  font=13px/500/-apple-system
visible=True  text=回到档案柜  page errors: none
```

即运行时颜色仍是类规则给的 #14130f，本次修复只影响静态审计路径。

---

## 2. impeccable detect / audit / polish 执行记录

工具路径：`/app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable`（版本 4.7.1）。
工作目录：`/app/working/shared/showcase`。执行时间：2026-11-12 11:38—11:45。

| # | 实际命令 | 退出码 | 结论 |
|---|---|---|---|
| 1 | `impeccable detect works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html` | **0** | 无输出 = 0 findings |
| 2 | `impeccable detect --json works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html` | **0** | 输出 `[]` |
| 3 | `impeccable detect /tmp/prefix_replica.html`（改前 59,701B 复刻件） | **2** | 1 条 `low-contrast`，severity=warning，`4.0:1 (need 4.5:1) — text #8c6f39 on #eaedea` |
| 4 | `impeccable audit works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html` | **1** | stderr：`Unknown command: "audit"` |
| 5 | `impeccable polish works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html` | **1** | stderr：`Unknown command: "polish"` |
| 6 | `impeccable skills audit` | **1** | stderr：`Unknown skills command: audit` |

退出码语义（由 #3 与 #1 对照得出）：0 = 无 findings；2 = 有 findings；1 = 命令错误。

### 2.1 audit / polish 的实际处置

该发行版 CLI 只实现 `detect / ignores / install / link / update / check / telemetry`。
`audit` 与 `polish` 在 skill 里是 **agent 侧 playbook**（`reference/audit.md`、`reference/polish.md`），不是 CLI 子命令，
所以 #4、#5 的退出码 1 属于「命令不存在」，不是作品不合格。

- audit（`reference/audit.md` 五维清单）本轮结论：
  - 可访问性：唯一问题项即本次修掉的 backlink 对比度（4.00:1 → 10.07:1），已达标。
  - 实现完整性：detect 0 findings（本轮实跑）。
  - 运行时：交由展厅 `tools/audit_pages.py` 实加载，见第 4 节，0 问题、0 报错。
  - 性能、主题化、响应式三维：**未做独立评分**（未跑 Lighthouse / 未做多断点截图比对），不计为已验证。
- polish（`reference/polish.md` triage）本轮结论：
  - triage 第 1 类（不可达 / 不达标路径）命中 backlink 文字色一项，已修。
  - 第 2—5 类（状态缺失、层级与设计系统漂移、视觉与动效不一致、代码清理）本轮**未做改动**：
    detect 0 findings，且本轮为「不得改动已验收作品」的范围限定任务。

---

## 3. design_scan 单件扫描

```
cd /app/working/shared/showcase && python3 tools/design_scan.py --scope file:works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html
```

退出码 **0**，输出：

```
扫描 1 件作品 · findings 0 条 · 涉及 0 件
严重度分布: {}
规则 Top:

（非全量扫描：只报告，不比棘轮）
```

结论：该件在展厅自有棘轮扫描器下 0 findings、0 件涉及。
注：该命令会写 `tools/design_snapshot.json`（工具自带的快照产物，非作品文件）。

### 3.1 附带复验：全库棘轮

为独立核对「全库设计棘轮已回落基线 1665」这一说法，本轮另跑一次全量扫描：

```
cd /app/working/shared/showcase && python3 tools/design_scan.py --scope all
```

退出码 **0**：

```
扫描 134 件作品 · findings 1665 条 · 涉及 107 件
严重度分布: {'warning': 1285, 'advisory': 380}
对比度分档: {'3-4.5:1 正文不达标': 650, '2-3:1 大字号不达标': 241, '<2:1 几乎不可读': 110}
✓ 棘轮通过：无一规则上升（基线 1665 → 当前 1665）
```

基线取自 `tools/design_baseline.json`（ts `2026-11-04 14:27:48`，total=1665，warning 1285 + advisory 380）。
结论：棘轮与基线持平，无规则上升。

---

## 4. audit_pages 真实加载巡检

```
cd /app/working/shared/showcase && python3 tools/audit_pages.py works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html
```

退出码 **0**，输出：

```
巡检 1 件作品（真实加载 + 抓运行时错误）

巡检完成：1 件，0 件有问题
✓ 全部作品页运行时健康
```

结论：该件真实加载无运行时错误。另用 Chromium 单独复核，取到 `#showcase-backlink` 计算样式
（见 1.4），`page errors: none`。

---

## 5. build_manifest --check 复验

```
cd /app/working/shared/showcase && python3 tools/build_manifest.py --check
```

退出码 **0**，计数结论：

| 项 | 值 |
|---|---|
| 扫描作品 | 132（research 68 / creative 64），total 132 |
| latestDate | 2026-11-11 |
| 可用标签 | 260 |
| manifest 与磁盘 | 一致（`[check] manifest 与磁盘 一致`） |
| 护栏 | index.html 213KB / 预算 400KB · EMBEDDED 150KB · 7 个月份 |
| 断言 | 1205 条 · 覆盖 126/132 件 (95%) · 待处理 544 · 无结构 8 · 重校验 1205/1205 通过 |

结论：manifest 与磁盘自洽，护栏未越界，断言层重校验全过。

---

## 6. 声明层自检

检查对象：`works/2026-11-10/research/2026-11-10-ai-hogging-fabs.html`（60,224B）。

### 6.1 claims 块位置与条数

- 位置：`<script type="application/json" id="claims">` 在文件 **第 908—946 行**，位于 `</footer>` 之后、
  页面一次性动效脚本之前（body 末尾）。
- 条数：JSON 数组 **7 条**。
- 与页面自述一致：抬头 `mast-meta` 写「已验证断言 **7** 条 · 逐字回查过原文」；`enrich.json` 中该件的
  `claims` 数组同为 **7 条**。

### 6.2 quote 逐字命中

方法：剥离全部 `<script>` / `<style>` / HTML 注释与标签、归一空白后，在正文文本中逐条检索该条的 `quote`。
结果 **7/7 全部命中**：

| # | value | quote | 命中 |
|---|---|---|---|
| 1 | 6-32 周 | 标准产品交期延长至6-32周 | 是 |
| 2 | 4—8 周 | 过去标准产品通常只需要4—8周交货 | 是 |
| 3 | 1150 亿美元 | Marvell 抛出 1150 亿美元收购 Lumentum 的光互连交易 | 是 |
| 4 | 23.9% | 溢价约23.9% | 是 |
| 5 | 45% | 传输带宽较上代提升45%至125GB/s | 是 |
| 6 | 125GB/s | 至125GB/s | 是 |
| 7 | 21% | 能效比LPDDR5X提升约21% | 是 |

### 6.3 追踪线 meta 的 beat 名

- `<meta name="showcase-beat" content="工具链与产业主权">`（第 6 行）。
- 抬头 `mast-meta` 的「追踪线」栏值为「工具链与产业主权」，**与 meta 一致**。
- 页面头部注释亦声明「断言声明：script#claims（7 条）；追踪线：meta#showcase-beat」，与实文件结构相符。

---

## 7. 未验证与说明

- **未做**：改前 / 改后视觉像素比对（未截全页图做 diff）。运行时外观不变的依据是 CSS 特异度推算
  + Chromium 计算样式实测（`color=rgb(20,19,15)`，仍来自 `.on-dark-page` 类规则）。
- **未做**：audit 五维中性能、主题化、响应式三项的独立评分（未跑 Lighthouse、未做多断点截图）。
- **说明**：改前 59,701B 复刻件与总指挥记录的改前字节数一致，但原改前文件已被覆盖，
  sha256 无从比对；findings 明细（1 条 low-contrast / 4.0:1 / #8c6f39 on #eaedea）由复刻件实跑复现。
- **说明**：本轮跑 `design_scan.py` 改写了工具自带的 `tools/design_snapshot.json`（该文件原本就处于 git 未提交状态），
  未触碰任何作品 HTML。
- **说明**（总指挥已告知，不需处理）：自留的 `.bak` 备份已被 `reorganize.py` 归一进
  `works/2026-11-10/notes/2026-11-10-ai-hogging-fabs.html.bak.20261111-182406`（56,398B），属正常行为。
- **说明**：缩略图 `thumbs/2026-11-10-research-2026-11-10-ai-hogging-fabs-thumb.webp` 的 mtime 为
  2026-11-12 06:16（Asia/Shanghai），晚于本次修复落盘的 05:43，即缩略图是在修复后生成的，不是残页。
