# 交付报告 · 2026-11-21-tencent-ai-capex-ledger（研究类 #460）

**状态：已完成（作品与本报告同回合落盘）。**

## 一、交付事实

| 项 | 值 |
|---|---|
| 交付路径 | `shared/showcase/works/2026-11-21/research/2026-11-21-tencent-ai-capex-ledger.html` |
| 字节数 | 37,663 bytes（UTF-8，`stat` 实测） |
| claims 条数 | 7 条（script#claims，value/label/quote 齐全） |
| 追踪线 | 估值与资本（`<meta name="showcase-beat" content="估值与资本">`） |
| 过程材料目录 | `shared/showcase/works/2026-11-21/notes/` |
| 备份 | `notes/2026-11-21-tencent-ai-capex-ledger.html.bak-20261120-184438`，与交付文件逐字节一致；时间戳为容器 UTC 时区（= 本地 2026-11-21 02:44:38）。将 `mv` 改为本地日期的重命名操作被审批拦截，故保留原名，特此标注 |

## 二、实际使用标签（7 个，全部新建）

动笔前已执行标签自查：`grep -ho 'class="metric-label"...' works/2026-11-1[4-9]/*.html works/2026-11-20/*.html … | sort -u` → 近 7 天共 **96** 个唯一标签，**无腾讯同义族**（`grep 腾讯` 零命中），故按本单给定命名一次性新建：

1. `腾讯 Q3 营收（11-19 财报口径）`
2. `腾讯云收入增速（21%→35%）`
3. `腾讯 Q3 自由现金流（含算力采购预付款）`
4. `腾讯 Q3 自由现金流（剔除算力采购预付款）`
5. `腾讯 WorkBuddy 日活（11-19 财报口径）`
6. `腾讯 WorkBuddy 日均 Token 调用量（11-19 财报口径）`
7. `腾讯 WorkBuddy 最近七天年化收入（美元）`

## 三、impeccable 执行记录（命令 + 结论）

| 步骤 | 命令 | 结论 |
|---|---|---|
| 上下文加载 | `impeccable context` | 已执行。无 PRODUCT.md，按 scoped 流程继续；加载 DESIGN.md（策士 v3.0） |
| 规范阅读 | 读 `reference/craft-floor.md`、`reference/new-work.md`、`reference/polish.md` | 已执行。方向按 brief-pinned：继承 work.html「档案卷宗」世界，版式按账本主题重排（新口径图、核源表、双栏账本） |
| audit（自动） | `impeccable detect research/2026-11-21-tencent-ai-capex-ledger.html` | 初扫：0 anti-patterns + 1 advisory（em-dash 10 处）→ 修订后复扫：**exit 0、零发现** |
| 阳性对照 | `impeccable detect /tmp/detect_probe.html` | 2 anti-patterns + 1 advisory（exit 2），证明扫描器有效、零发现可信 |
| polish（人工轮） | 按 `reference/polish.md` 清单逐项 | 见下 |
| 渲染验证 | playwright 双视口（1440×900 / 390×844） | 见「五、验证」 |

**polish 人工轮做了什么：**

- 修正 3 处正文 em-dash（「证据——那属于」「）——任何」「万——与」→ 分号/句号/逗号），em-dash 10→4，低于 detect 阈值 8；标题分隔符 `——` 保留（标题合法用法）
- 补 browser surfaces 主题化：`::selection`（brass-wash 底 + ink 字）、`:focus-visible`（brass 描边）
- 对比度核对：正文 `--ink-2/#4f5551` 与 `--ink-3/#646b67` 对纸底 6.9:1 / 5.1:1；条内白字 `#f4f6f4` 对 brass `#7d5a1c` ≈5.3:1、对 `#4f5551` ≈7:1；深色带 `#b3bbb6` 对 `#121513` 高对比 —— 均 ≥4.5:1
- 响应式核对：900px 断点（图表/双栏单列化）、640px 断点（时间线/指标单列），SVG 全部 viewBox 自适应 `width:100%`
- 唯一动效（发丝线绘制）+ `prefers-reduced-motion` 关闭，无散布特效
- 内容一致性：断言读法列表与 claims quote 逐字一致（脚本自检 7/7 命中）；无 `{{ }}` 占位残留

## 四、六项共同要求 + 研究类三项落实

1. **断言声明** ✅ 7 条，quote 逐字自检 7/7 命中（python 脚本比对 `quote in html`）
2. **追踪线声明** ✅ `估值与资本`（13 条封闭集内）
3. **交付路径** ✅ 文件名按本单正文路径逐字符核对后写入
4. **过程材料落 notes/** ✅ 交付报告（本文件）、备份均在 `notes/`；未在作品目录留任何分片/备份；未手工截图（预览截图由 gen_thumb.py 统一持有）
5. **设计门禁** ✅ 见第三节（detect 命令 + 结论齐全，本报告与作品同回合落盘）
6. **执行纪律** ✅ 初稿 >10KB 于开场 20 分钟内落盘（write_file 25,787 字符首版）；本回合无后台子任务挂起
7. **模板** ✅ 从 `shared/showcase/templates/work.html` 起步，重排版式（新增口径图 3 幅、核源表、双栏账本、断言读法块），未照搬占位文案
8. **封闭语义词汇表** ✅ 只用 `.metrics/.metric(.metric-value/.metric-label/.metric-source)`、`.verdict`、`.timeline>.timeline-item`、`.evidence>.evidence-item`；局部 class（`.readback/.charts/.caliber-table/.split-ledger` 等）仅作局部样式
9. **标签纪律** ✅ 见第二节（先 grep 后定名）

## 五、验证

- **已验证**：claims/beat/语义 class 脚本自检 — 7 quotes 全命中、beat 正确、metric 7 组齐全。
- **已验证**：`impeccable detect` 复扫 — exit 0 零发现；阳性对照证明扫描器有效。
- **已验证**：playwright 渲染 — 双视口无横向溢出、console 零错误、Noto Serif SC 加载成功、3 幅 SVG 与 7 条 claims 渲染在位、页面高 6,947px（桌面）。
- **已验证**：源文回查 — 2026-11-19.md 第 11/23 行、2026-11-20.md 第 21 行逐字比对；100 万亿 Token 主体经 36氪、BigGo、第一财经转载三源核对归于 WorkBuddy（资料核对，非运行验证）。
- **未验证**：Q2 -138 亿元、分部收入 983.26/430.49/636.55 亿元等第三方数据未回查财报原文 —— 已按转载口径标注且未列入断言层。
- **失败/阻塞记录**：`mv` 备份重命名被审批拦截（300s 超时），按指令未重试同类操作，保留 UTC 文件名并在此披露。
- **披露**：`research/` 下存在一个非本人创建的 `2026-11-21-tencent-ai-capex-ledger.html.bak.20261120-184420`（34,360 bytes，与并行任务 `h200-shutoff` 的同名格式备份同一秒生成，疑似自动化 hook 所致）。本人未在作品目录创建任何分片或备份；该文件的迁移需审批，留待处理。

## 六、核源清单 6 项处理（已在作品内成表）

① -691/169 写明同指标两口径、禁「由负转正」；② 5 亿美元全程带「最近七天年化」；③ 100 万亿主体核到 WorkBuddy（三源一致）；④ 1000 万（WorkBuddy）与 3000 万（小微）分列不相加；⑤ 元宝自陈进 evidence、投入产出比判断只留正文；⑥ 币种不换算、日期标「Q3（11-19 发布）」。
