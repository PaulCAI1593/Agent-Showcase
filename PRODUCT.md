# Product

<!-- impeccable:product-schema 1 -->

> Provenance: written 2026-10-27 for P0 task #358 (选题389). No human interview was possible in this agent-to-agent pipeline; every fact below comes from the task brief or the verification ledger `2026-10-27/notes/2026-10-27-50m-ai-songs-口径与来源.md`, and is marked 简报锚定 (brief-anchored) or 推断 (inferred).

## Platform

web

## Stack

Static single-file HTML, CSS/JS inline, zero remote dependencies (brief-pinned hard constraint; chart libs only via local vendor path — this surface draws its own SVG, so no library).

## Users

中文互联网读者 / 内容消费者，在 QwenPaw 展厅（showcase）里点开一件"当日事件交互作品"。次要读者：关注平台经济与创作者劳动的从业者。（简报锚定：选题来自每日热点，创意类作品目标是让读者"亲身经历"一件事。）

## Positioning

一件可操作的隐喻作品：把"AI曲目挤占版税池"从新闻数字变成可拖动的分配实验——读者亲手把 AI 流占比拉高，看同一笔钱怎么变薄；同时页面强制把"惊叹面"与"质疑面"以同篇幅并置，不做单面宣传。（简报锚定。）

## Operating Context

展厅流水线：`autopublish.sh` 十项硬校验（标题=manifest、claims JSON 引用逐字存在、showcase-beat 在封闭集、无外链、375px 无横向滚动、prefers-reduced-motion、对比度≥4.5:1）。交付截止 2026-10-29 02:00。（简报锚定。）

## Capabilities and Constraints

- 单文件、离线可开（file:// 双击）。
- 数据红线：每个数字标来源与时点；搜索摘要级转引需标"转引自搜索摘要，页面未直取"；核不到的写"口径未证实"；反事实推演必须在视觉上可区分。
- 交互 ≥2 且勿扩项：版税稀释滑块（含三刻度）；人类优先策略 ON/OFF 推荐池 A/B。
- 叙事四段：开场立场句 / 发展(发生了什么、谁做的决定) / 高潮(版税水池) / 收尾("不是下架，是停止付费曝光"——评论措辞需标注为作品概括)。
- claims JSON 3–8 条，quote 逐字在页。
- 未定事实：无（简报已封闭选择空间；视觉/叙事自由为简报明示授权）。

## Brand Commitments

展厅声音：诚实的视觉——该难看的地方（真实稀释、真实分歧）就让它难看；不用图表装饰结论。多面并置由作品结构呈现，不由作者下结论。（简报锚定 + creative-brief.md。）

## Evidence on Hand

16 条搜索摘要级来源（S1–S16，含 NBC/Billboard/Deezer Newsroom/RouteNote/Stability AI/TechTimes/WIPO/Chartlex 等）与 C 级未证实清单，全部记录于 `2026-10-27/notes/2026-10-27-50m-ai-songs-口径与来源.md`。不可虚构：任何未在该台账出现的数字、日期、平台声明。

## Product Principles

1. 可操作的隐喻优于说明文字：分配问题要被"拖出来"。
2. 诚实分层：实测 / 平台自报 / 换算 / 反事实，四种口径在视觉上可分辨。
3. 矛盾并置：惊叹与质疑同篇幅，让张力自己浮现。
4. 快速交付但留痕：数据核验与门禁执行都要有过程材料。

## Accessibility & Inclusion

WCAG 级底线：对比度正文 ≥4.5:1、大字号 ≥3:1；prefers-reduced-motion 完整降级；滑块键盘可达；375px 无横向滚动。（简报硬约束。）
