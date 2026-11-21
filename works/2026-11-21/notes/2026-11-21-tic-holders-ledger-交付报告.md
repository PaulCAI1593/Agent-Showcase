# 《TIC 持有人账本》交付报告（证据重建补录）

> **本报告为总指挥指派的证据重建补录，非作品作者自述。**
> 报告人：知库（wisdom-keeper），补录时间 2026-11-21（北京）。
> 方法：只依据盘上已有文件（成品 HTML、过程脚本、截图、.bak、素材源）逐条读取与实跑；作者设计意图与主观评价一律列入「未确认」。

**前两次失败记录**

| 单号 | 执行方 | 现象 |
|---|---|---|
| `task-6f5e23834a22` | 创艺 | 3600s 超时，只出作品，缺交付报告 |
| `task-d9543f345e5b` | 绘界 | 2026-11-21 12:56 只落 406B 骨架后无动静 |

**作品**：`works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html`
**署名**：创艺
**补录单**：#459，截止 2026-11-21 20:00 北京时间

## 目录

1. [结构实测](#1-结构实测)
2. [交互形式 ≥2](#2-交互形式-2)
3. [两口径对照](#3-两口径对照)
4. [claims 5 条与 quote 命中核对](#4-claims-5-条与-quote-命中核对)
5. [impeccable 实跑](#5-impeccable-实跑)
6. [contrast-check 实测数字](#6-contrast-check-实测数字)
7. [.bak diff 结论](#7-bak-diff-结论)
8. [标签族对账（规则15 ④）](#8-标签族对账规则15-)
9. [缺陷与未确认清单](#9-缺陷与未确认清单)

## 1. 结构实测

实测命令（在 `/app/working/shared/showcase` 下执行，python3 去标签统计）：

```bash
python3 - <<'EOF'
import re
s=open('works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html',encoding='utf-8').read()
print('bytes:',len(s.encode('utf-8')))
body=re.sub(r'<(script|style)[\s\S]*?</\1>','',s)
text=re.sub(r'<[^>]+>','',re.sub(r'&[a-z]+;',' ',body))
print('visible_no_ws:',len(re.sub(r'\s','',text)))
for pat,name in [(r'<section\b','section'),(r'<button\b','button'),(r'addEventListener','addEventListener'),(r'<input\b','input'),(r'<svg\b','svg')]:
    print(name,len(re.findall(pat,s)))
EOF
```

实测数字（2026-11-21 16:5x 北京，本报告人亲跑）：

| 指标 | 实测值 |
|---|---|
| 文件字节 | 40,264 B（UTF-8）；35,275 字符 |
| 可见文本（去标签、去 script/style、去空白） | 1,843 字（含空白 2,172 字） |
| `<section>` | 5（`reconcile` / `holders` / `streak` / `valuation` / `ledger`，`works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html:289-444`） |
| `<button>` | 14 |
| `addEventListener` | 12 处（其中 1 处在注入的 `showcase-backlink-js` 脚本内；作者交互绑定 11 行） |
| `<input>` | 0 |
| `<svg>` | 2（返回按钮图标 1、瀑布图 1） |

派单称作品 36,736 B，盘上实测 40,264 B，差异列入第 9 节。

## 2. 交互形式 ≥2

以下绑定位置均从成品代码读出（行号指 `works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html`）：

1. **口径切换**：`.seg-btn[data-cal="stock"|"flow"|"both"]`，`click` → `setCal()`，改 `body.dataset.cal`、`aria-pressed`、`#readout` 文本（`:509`）。
2. **瀑布图图例**：`.leg[data-seg="1"|"2"|"3"]`，`click` / `mouseenter` / `focus` → `showSeg()`（`:542-544`），另有段落 `p` 的 `click` → `showSeg()`（`:547`），`.wf` 的 `mouseleave` → `clearHot()`（`:549`）。
3. **持有者条形分段**：`#segCn` / `#segRest`，`click` → `showBar()`（`:562-563`）。
4. **月份切换**：`.m[data-m="7"|"8"|"9"]`，`click` → `showMonth()`（`:578`）。
5. **估值三件事**：`.chip[data-v="fx"|"rate"|"price"]`，`click` / `mouseenter` → `showVal()`（`:600-601`）。

**运行时只读验证**（本报告人亲跑，不写任何文件）：

```bash
python3 - <<'EOF'   # playwright 依次点击并断言读数变化
...（点击 .seg-btn[data-cal="stock"] / .leg[data-seg="2"] / .m[data-m="7"] / .chip[data-v="rate"] / #segCn）
EOF
```

输出：`口径切换 -> True`、`瀑布图例 -> True`、`月份切换 -> True`、`估值chip -> True`、`条形分段 -> True`、`pageerror -> []`。5/5 通过，无运行时错误。

**`preview-interact.png` 是哪个交互态**：`2026-11-21-tic-render-check.py` 的 interact pass（1280×900、`full=False`）在依次执行全部交互后截图，最后一次点击是 `.chip[data-v="rate"]`。本报告人亲眼查看该图：画面为「估值，是哪三件事」区，**利率 chip 选中态**（橙色描边），右侧面板显示「估值因素 · 利率／收益率动，市值跟着动」＋红色「未确认」徽标；底部可见「五条可核对的数据」标题与「回到档案柜」按钮。即 **rate chip 选中后的估值面板状态**。

## 3. 两口径对照

本选题核心：净买入 +808 亿（交易流量口径）与余额 −755 亿（存量口径）同时成立。成品的呈现方式（行号同上，均为读出的原文）：

| 呈现位置 | 成品原文 |
|---|---|
| meta 描述（`:7`） | 「9 月 TIC：海外持有美债余额环比减少 755 亿美元至 9.2412 万亿美元，同月按交易流量仍净买入 808 亿美元。两个口径同时成立，差额来自估值。」 |
| 导语（`:252`） | 「9 月，海外投资者净买入美债 808 亿美元。同一个月，他们的余额少了 755 亿。」 |
| 存量卡（`:267`） | `−755 亿美元`（`data-count="755"`、`data-prefix="−"`） |
| 流量卡（`:280-282`） | `+808 亿美元`；小字「按交易流量计 · 9 月海外仍净买入美债 808 亿美元」 |
| 瀑布图 SVG（`:292-318`） | 三段拆解：`+808`（净买入·交易流量口径）→ `−1563`（估值变动·本件推算）→ `−755`（余额变动·存量口径）；aria-label 写明「三段拆解」 |
| 对账段（`:328`） | 「同一笔 9 月，交易口径记 +808，余额口径记 −755。中间那笔 −1563 是估值：没发生买卖，钱的记法变了。」 |
| 图例行（`:335/:343`） | 「+808 亿美元 · 净买入（交易流量口径，素材原句）」「−755 亿美元 · 余额变动（存量口径，素材原句）」 |
| 印章（`:350`） | 「三笔对上：808 − 1563 = −755」 |
| 口径纪律（`:467`） | 「『余额下降 755 亿』属存量口径（期末余额环比），『净买入 808 亿』属交易流量口径。两条同时成立，不得写成互相矛盾的两条事实。差额来自估值因素；估值的具体构成（汇率、利率、价格）本件素材未给出，标未确认。」 |
| 口径切换读数（`:496-498`） | stock「读法：期末余额的环比变动…」／flow「读法：当月买入减卖出的净额…」／both「读法：两个口径同时成立。差额来自估值，不是矛盾。」 |

派单写「余额 −752/−755 亿」：成品全文 `grep '752'` 无命中，**成品只写 −755**；素材 `2026-11-19.md:44` 也只有 755。−752 的来源列入第 9 节未确认。

## 4. claims 5 条与 quote 命中核对

5 条断言逐字照抄自 `works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html:480-484`（`id="claims"` JSON 块）：

| # | value（逐字） | label（逐字） | quote（逐字） |
|---|---|---|---|
| 1 | `9.2412 万亿美元` | `海外投资者持有美债规模（9 月 TIC）` | `海外投资者持有美债规模环比减少 755 亿美元至 9.2412 万亿美元` |
| 2 | `755 亿美元` | `海外持有美债单月降幅（9 月 TIC）` | `环比减少 755 亿美元` |
| 3 | `5639 亿美元` | `中国持有美债规模（9 月 TIC）` | `中国持仓降至 5639 亿美元` |
| 4 | `808 亿美元` | `9 月海外净买入美债（交易流量口径）` | `9 月海外仍净买入美债 808 亿美元` |
| 5 | `3 个月` | `中国美债持仓低位连续月数（9 月 TIC）` | `连续第三个月刷新 2008 年 8 月以来低位` |

**门工具核对（原文输出）**：

```
$ cd /app/working/shared/showcase && python3 tools/claim_gate.py --verify
重校验 1421 条断言
✓ 全部通过
```

**本件 5 条 quote 对素材逐字命中**（归一化子串匹配，素材 = `shared/tasks/每日热点新闻简报/2026-11-19.md:44`，本报告人亲跑）：

```
HIT  9.2412 万亿美元 | 海外投资者持有美债规模（9 月 TIC）
HIT  755 亿美元 | 海外持有美债单月降幅（9 月 TIC）
HIT  5639 亿美元 | 中国持有美债规模（9 月 TIC）
HIT  808 亿美元 | 9 月海外净买入美债（交易流量口径）
HIT  3 个月 | 中国美债持仓低位连续月数（9 月 TIC）
quote命中 5/5
```

## 5. impeccable 实跑

两条命令均由本报告人于 2026-11-21 亲跑，原文输出如下。

**design_scan**：

```
$ cd /app/working/shared/showcase && python3 tools/design_scan.py --scope file:works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html
扫描 1 件作品 · findings 0 条 · 涉及 0 件
严重度分布: {}
规则 Top:

（非全量扫描：只报告，不比棘轮）
```

**audit_pages**：

```
$ cd /app/working/shared/showcase && python3 tools/audit_pages.py works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html
巡检 1 件作品（真实加载 + 抓运行时错误）


========================================================
巡检完成：1 件，0 件有问题
requestfailed 口径：策略拦截 0 次 / 导航中止 0 次 / 与本页无关 0 次（均不计为问题）；远程依赖未落定 0 件
✓ 全部作品页运行时健康
```

结论：design_scan findings 0 条；audit_pages 0 件有问题、运行时健康。

## 6. contrast-check 实测数字

`2026-11-21-tic-contrast-check.json`（94 B）原文：

```json
{
 "initial_fail_count": 0,
 "after_interaction_fail_count": 0,
 "initial": [],
 "after": []
}
```

**测了什么**（读 `2026-11-21-tic-contrast-check.py`）：Playwright/Chromium 加载作品（1280×900），对 `body *` 中含直接文本、可见的元素取前景色与实际背景色，按 WCAG 相对亮度算对比度；大字（≥24px，或 ≥18.66px 且粗体）需 **≥3:1**，其余需 **≥4.5:1**（脚本 `need = large?3:4.5`），不达标元素记入失败清单。随后依次点击 `.seg-btn[data-cal="stock"]`、`.leg[data-seg="2"]`、`#segRest`、`.m[data-m="7"]`、`.chip[data-v="rate"]` 再复测一次。

**数字结论**：初次 **0 处**不达标，交互后 **0 处**不达标，两份失败清单均为空——即两次检测中所有被测文本均达到其对应阈值（正文 ≥4.5:1）。

**如实说明**：该 json 只记录失败项，**未记录通过项的具体比值**，因此「每处比值多少」在盘上无数据可引。确认方法：改 `contrast-check.py` 让它输出全部元素的 ratio 后重跑（本报告人未改——该文件是创艺过程件，纪律禁止改动）；本次未执行 → 比值数值列第 9 节未确认。

## 7. .bak diff 结论

对象：`works/2026-11-21/notes/2026-11-21-tic-holders-ledger.html.bak-20261121-024420`（36,825 B）→ `works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html`（40,264 B）。

```bash
cd /app/working/shared/showcase && diff works/2026-11-21/notes/2026-11-21-tic-holders-ledger.html.bak-20261121-024420 works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html
```

结果：45 行 diff、31 行变更（`<`/`>` 计）。逐处改动事实：

| # | 位置 | 改动事实 |
|---|---|---|
| 1 | CSS `.wf-lab` | `font-size:13px` → `font-size:15px` |
| 2 | CSS `.wf-val` | `font-size:15px` → `font-size:17px` |
| 3 | `:240-247`（新增 8 行） | 插入 `<!-- showcase-backlink -->` 标记的顶栏（`#showcase-bar`，含「回到柜子」）、固定返回按钮 `#showcase-backlink` 及其明暗检测脚本 `#showcase-backlink-js` |
| 4 | 瀑布 SVG `viewBox` | `0 0 660 348` → `0 0 660 296`（高度减 52） |
| 5 | 瀑布轴标签 y 坐标 | 三组标签 `y=330/348` → `y=248/268`（净买入／估值变动／余额变动 两行标签整体上移） |
| 6 | 数字滚动动画 | `(t - t0) / 900` → `(t - t0) / 450`（时长 900ms → 450ms） |
| 7 | 新增兜底 | 新增 `setTimeout(…, 800)`：800ms 后把计数元素直接置为 `dataset.count` 终值 |

另一份 `bak-20261121-030144`（40,264 B）与现成品 `md5sum` 相同（`fc8b39930406e2292b8a67429e07bbbc`），即终稿快照，与现文件无差异。

**只描述改动事实，不推断意图**：第 1-2、4-7 项均为作者文件内的改动；第 3 项是带 `showcase-backlink` 标记的基础设施块（全馆收敛件特征），**注入者未确认**（第 9 节）。

## 8. 标签族对账（规则15 ④）

**本件 5 条 label 全库逐字检索**（命令：`grep -rF '"label":"<label>"' --include='*.html' works/ | grep -v tic-holders-ledger`，5 条逐一执行）：**0 命中**——5 条 label 在 `works/` 其他文件中均无逐字同名。

**对照族实例**：

| 族 | 检索结果 |
|---|---|
| `恒生指数午盘点位（…）` | `恒生指数午盘点位（11-16）` 6 处、`恒生指数午盘点位（11-20）` 6 处（`grep -rhoE '恒生指数午盘点位（[^）]*）' works/`）——同指标名跨件逐字一致，仅日期后缀变化 |
| `英伟达 11-13 收盘价` | 跨 15 个文件逐字复用（`grep -rlF '英伟达 11-13 收盘价' works/ \| wc -l` → 15） |
| `（…TIC）` 后缀 | `grep -rhoE '"label":"[^"]*TIC）"' works/` 仅返回本件 4 条 → 该后缀全库首次出现 |

**结论**：本件 5 条标签**全部为新建**，不复用既有族；命名格式沿用族约定「指标名（口径/期间）」（4 条以「（9 月 TIC）」、1 条以「（交易流量口径）」结尾），与「恒生指数午盘点位（11-16）」族的构词方式同构。是否把「（9 月 TIC）」登记为新族并归入「美债/TIC」系列 → 交裁定（第 9 节）。

**index 收录状态**（只读核对）：`index.html` 已含本件条目（`"file": "works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html"`，`type: creative`，`beat: 宏观利率与股市`），且含 `"l": "海外投资者持有美债规模（9 月 TIC）"`（命中 1 次）。

## 9. 缺陷与未确认清单

| # | 事项 | 状态 | 确认方法 |
|---|---|---|---|
| 1 | 派单称作品 36,736 B，盘上实测 40,264 B（`ls -l`、python `len(utf-8)` 双测一致） | 未确认（差异原因） | 向总指挥核对 36,736 的数字来源 |
| 2 | 派单写余额「−752/−755 亿」；成品 `grep '752'` 无命中，素材也只有 755 | 未确认（−752 来源） | 向总指挥核对；本报告只按成品写 −755 |
| 3 | diff 第 3 项 `showcase-backlink` 注入块的注入者（作者 or 收敛管道） | 未确认 | 查 autopublish/build_manifest 日志或提交记录（本单禁跑这两命令，未执行） |
| 4 | contrast-check.json 无通过项比值，「每处比值多少」盘上无数据 | 未确认 | 改 `2026-11-21-tic-contrast-check.py` 输出全部 ratio 后重跑（纪律禁改过程件，未执行） |
| 5 | `2026-11-21-tic-render-check.py` 的交互断言结果只 print、未落盘，当时是否全 True | 未确认 | 重跑该脚本；本报告已用等价只读脚本复验 5 类交互全 True（见第 2 节），但不等同于原脚本输出 |
| 6 | `preview-desktop.png` / `preview-mobile.png` 内容 | 未核看（本报告只亲眼看了 interact 一张） | 用 view_image 逐张查看 |
| 7 | 作者设计意图、主观评价（为何放大标签、为何把动画改 450ms 等） | 未确认 | 问创艺本人；diff 只给改动事实（第 7 节） |
| 8 | 派单提到的 `E5-收尾-剩余10条处置记录.md` 盘上未见，实际存在的是 `E7-E4E5收尾处置记录.md` | 未确认（文件名） | 向总指挥核对单号与文件名对应关系 |
| 9 | 派单称「claims 5 条 quote 5/5」与「远程依赖 0」 | 已验证（本报告第 4 节、第 1 节命令：`grep -oE '(src\|href)="https?://…"'` 为空） | — |

## 验收自检

```bash
ls -l --time-style=+%F\ %T works/2026-11-21/notes/2026-11-21-tic-holders-ledger-交付报告.md
wc -l works/2026-11-21/notes/2026-11-21-tic-holders-ledger-交付报告.md
grep -c '未确认' works/2026-11-21/notes/2026-11-21-tic-holders-ledger-交付报告.md
```

（本报告人亲跑输出；文件自 2026-11-21 16:56 起逐节落盘，远大于 406 B 骨架。验收输出随最终保存再跑一次，见交付回复。）

**未做**

- 未改作品、未改 claims、未改 `tools/*.py`、未跑 autopublish / build_manifest — 按纪律。
- 未 git push — 按派单。
- 未重跑 `2026-11-21-tic-render-check.py` / `contrast-check.py` — 两者会覆盖创艺的过程截图/结果文件，属保留证据。

**待确认**

- 第 9 节表中 1-8 项，交总指挥裁定。
