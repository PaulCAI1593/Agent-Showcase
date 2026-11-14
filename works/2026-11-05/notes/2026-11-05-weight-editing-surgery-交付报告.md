# 交付报告 · 选题416「让模型改自己的权重——MIT 权重编辑」首屏可见性修复

> 作品：`works/2026-11-05/creative/2026-11-05-weight-editing-surgery.html`（30,003 字节，修复前 28,580 字节）
> 主责：**创艺（content-creator）**　｜　任务：心跳重派修复（原派单 `task-f96a5fda04bb` 已超时失败）
> 追踪线：安全与治理　｜　修复日期：2026-11-10　｜　截止：2026-11-11 02:00

---

## 一、排查结论（先给原因）

**原因：首屏不是被「死规则」隐藏，而是首屏文本节点过少——可见叶子 6 个，低于巡检阈值 8。**

**现象**：`tools/audit_pages.py` 报 `首屏几乎没有可见内容（可见叶子 6 / 总叶子 53）`，心跳判定为「进场动画初始 opacity:0 把内容永久隐藏」。

**证据**（修复前用 Playwright 探针逐元素取 computed style，viewport 1260×800，无滚动）：

- 首屏 6 个可见叶子全部 `checkVisibility(...) === true`、`opacity = 1`、`visibility = visible`，**没有一条 opacity:0 / visibility:hidden 的死规则**；`.mirror .lit{opacity:0}` 等初始隐藏规则都在首屏之外（第 4 节），且已有 `#showcase-rescue` 救援样式。
- 首屏截图不是全黑：只有大标题 `能力，<em>住在哪？</em>` + 一行 cue，其余 47 个叶子全在折叠线以下。对照同馆近作首屏可见叶子 18～66（`2026-11-02-agent-access-layer` 25、`2026-10-22-ai-credit-contagion-chain` 19、`2026-09-29-global-rates-nuclear-bomb` 34），本件 6 明显偏空。
- 页面 JS 零报错、零 console.error、零资源失败 —— 不是脚本挂掉导致的空白。

**结论**：修法是**给首屏补真实信息层**（眉题 / 导语 / 关键数字），不是拆隐藏规则；视觉风格沿用本页 mono 标签 + 绿色强调，不推翻设计。

## 二、改动点

| 位置 | 性质 | 说明 |
|---|---|---|
| `works/2026-11-05/creative/2026-11-05-weight-editing-surgery.html:34` | 改 | `.open` 增加纵向 `padding:clamp(56px,8vh,92px) 0`，首屏内容变多后仍留呼吸位，避免小视口裁切 |
| 同文件 `:46-63` | 增 | 新增 `.eyebrow` / `.lede` / `.facts` 三段样式，取本页既有 token（`--mono` `--muted` `--green` `--line`） |
| 同文件 `:268-277` | 增 | `.open-copy` 内补 3 类真实内容：眉题（日期 · 创意件 416 · 追踪线）、导语（MIT 权重空间编程一句话）、4 枚关键数字胶囊 |
| `works/2026-11-05/notes/416-首屏-desktop-修复后.png` | 新建 | 修复后首屏截图（1260×800） |
| `works/2026-11-05/notes/416-首屏-mobile-390-修复后.png` | 新建 | 修复后首屏截图（390×844） |

新增文案全部来自本页既有来源段与断言，未引入新事实：`0.016%`、`1/6250`、`约 6 倍`、`不训练 / 不算梯度` 均可在正文「来源与口径」与 `<script id="claims">` 中逐字找到。

## 三、验收命令原始输出

### ① 首屏巡检（必检）

```
$ cd /app/working/shared/showcase && python3 tools/audit_pages.py works/2026-11-05/creative/2026-11-05-weight-editing-surgery.html
巡检 1 件作品（真实加载 + 抓运行时错误）

========================================================
巡检完成：1 件，0 件有问题
✓ 全部作品页运行时健康
AUDIT_EXIT=0
```

修复前同命令输出：`✗ 首屏几乎没有可见内容（可见叶子 6 / 总叶子 53）`，`EXIT=1`。
修复后实测：可见叶子 **6 → 12**（总叶子 53 → 59），desktop 与 mobile 390 均为 12。

### ② 设计门禁（AGENTS.md 规则14）

```
$ cd /app/working/shared/showcase && /app/working/workspaces/default/skills/impeccable/scripts/impeccable detect works/2026-11-05/creative/2026-11-05-weight-editing-surgery.html --json
[]
exit=0
```

**impeccable 已执行：命令 `impeccable detect <作品路径> --json`；结论 findings = 0（0 warning / 0 error，退出码 0）。**
补充：本机启动器 v4.7.1 只有 `detect`，`impeccable polish` / `impeccable audit` 均返回 `Unknown command`；按 `_private/dispatch-contract-2026-10-29.md` 第 5 条「本机启动器仅提供 detect，按规则14『audit+polish（或 detect）』以 detect 为准」，本次以 detect 为门禁，0 findings 故无 polish 动作。

### ③ 断言闸门（未改动断言，跑复验）

```
$ cd /app/working/shared/showcase && python3 tools/claim_gate.py --verify
重校验 1174 条断言
✓ 全部通过
```

### ④ 清单校验

```
$ cd /app/working/shared/showcase && python3 tools/build_manifest.py --check
扫描作品      : 128
research      : 66
creative      : 62
total         : 128
latestDate    : 2026-11-09
可用标签      : 258

[check] manifest 与磁盘 一致
  提示: 3 件作品缺 agent 署名（可在 enrich.json 补，…）
     - works/2026-11-06/research/2026-11-06-midterm-ai-repricing.html
     - works/2026-11-05/research/2026-11-05-wartime-compute-governance.html
     - works/2026-11-05/creative/2026-11-05-weight-editing-surgery.html
  护栏: index.html 207KB / 预算 400KB · EMBEDDED 144KB · 7 个月份
  断言: 1174 条 · 覆盖 122/128 件 (95%) · 待处理 535 · 无结构 8 · 重校验 1174/1174 通过
CHECK_EXIT=0
```

退出码 0 → 按任务要求**未跑** `./tools/autopublish.sh`（该脚本未执行，无输出可引）。

### ⑤ 无 JS / 无滚动兜底

```
Playwright（java_script_enabled=False，viewport 1260×800，未滚动）is_visible()：
  .eyebrow            True
  h1                  True
  .cue                True
  .lede               True
  .facts span ×4      True（4/4）
  .scroll-hint        True
```

### ⑥ 响应式与对比度

```
375×720: {"sw":375,"cw":375,"overflow":false}   → 无横向滚动
对比度（WCAG 公式）：#A8B8B2/#0B0F0E = 9.33 · #46E08B/#0B0F0E = 11.29
                      #EAF2EE/#0B0F0E = 16.93 · #FFB454/#0B0F0E = 10.94
```

全部 ≥ 4.5:1（新增文字用 `--muted` 与 `--green`，均在既有取值内）。

## 四、硬约束自检

| 约束 | 状态 | 证据 |
|---|---|---|
| 不改 `<script id="claims">` 中的 quote 原文 | 已验证 | `grep -n "id=\"claims\""` → `:397`；本件未触碰该块；`claim_gate --verify` 1174/1174 通过 |
| 不手工编辑 `manifest.json` | 已验证 | 本会话仅执行 `build_manifest.py --check`（只读）；`manifest.json` mtime `2026-11-10 00:23:34`（早于本次改动 03:36），修改态 ` M manifest.json` 为 11-10 00:23 既有流水线产物，非本次写入 |
| 不 git push | 已验证 | 本会话未执行任何 git 写命令；`works/2026-11-05/` 整目录仍为未跟踪 `??` |
| 零远程依赖 | 已验证 | `grep -c "http"` = 0（无 CDN 外链）；新增内容仅内联 CSS 与静态文本 |
| 过程材料落 `notes/` | 已验证 | 2 张修复后截图 + 本报告均在 `works/2026-11-05/notes/` |
| 占位符 | 已验证 | `grep -c "{{"` = 0 |
| 保持既有视觉风格 | 已验证 | 只在 `.open-copy` 追加信息层，标题/画布/滚动提示/翻卡/手术台全部未动；新增样式沿用既有 token |

## 五、未做 / 未验证

- 未改动 `.mirror .lit`、`.perm input` 等首屏外的初始隐藏规则（它们属于交互动效，且已有 `#showcase-rescue` 兜底）——它们不是本缺陷原因。
- 未跑全库 `tools/design_scan.py` 棘轮比对（覆盖 128 件，属例会流水线职责）。
- 未跑 `./tools/autopublish.sh`（`--check` 已 exit 0，按任务条件不需要）。
- 未更新 `416-首屏-desktop.png` 等修复前截图（保留作对照证据）。

## 六、待确认

- `build_manifest.py --check` 提示本件在 `enrich.json` 缺 `agent` 署名（与另外 2 件同批提示，属既有状态）。补 `enrich.json` 不在本次授权范围（任务只授权「署名进交付报告」，且 `enrich.json` 由流水线管理）——请智囊决定是否由流水线补 `agent: "创艺"`。

---

**结论：已完成。** 首屏可见叶子 6 → 12；`audit_pages.py` 0 问题 exit 0；impeccable detect 0 findings exit 0；`claim_gate --verify` 1174/1174 通过；`build_manifest.py --check` exit 0；无 JS 无滚动首屏全部可见；375px 无横向滚动；对比度 ≥9.33。

**签名：创艺（content-creator）　2026-11-10**
