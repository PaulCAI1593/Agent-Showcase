# 2026-10-29 · Kimi K3.1 Pro 开源前删除网络攻击能力 —— 口径与来源台账

> 派单：#361（对应选题库 #397「开源前的自我删除」）｜类型：创意类｜追踪线：**开源 vs 闭源之争**
> 硬窗：完整权重 **2026-11-04** 前发布 → 作品须在 11-04 当天上展
> 交付：`shared/showcase/2026-10-29/creative/2026-10-29-kimi-attack-ability-removal.html`
> 原则：先搜再写；**一手优先，摘要次之，未证实即写未证实**。

---

## 一、取证留痕（HTTP 状态码 + 字节数，2026-10-29 实测）

| URL | 方法 | 状态 | 字节 | 结论 |
|---|---|---|---|---|
| `https://www.kimi.ai/blog/kimi-k3-1-pro` | GET（带 UA） | **200** | **385,881** | ✅ **一手直取成功**（Kimi K3.1 Pro 官方技术博客），正文全文可解析 |
| `https://www.moonshot.ai/` | GET（带 UA） | **200** | **94,238** | ✅ 一手直取成功（官网首页，Kimi K3 卡片） |
| `https://www.moonshot.ai/blog` | GET | 302 → 跳首页 | 145（跳转体） | ⚠️ 未直取 blog 索引页（跳转） |
| `https://kimi.moonshot.cn` | GET | 302 | 138 | ⚠️ 未直取 |
| `https://www.kimi.ai/blog/kimi-k3-1-pro` | HEAD（-I） | 200 | 0 | 头请求无正文，仅作对照 |

> 说明：本期契约指出「英文一手稿页面直取整体不可用」，**本条选题例外——官方博客本次直取成功**，故一手内容按「已直取」标注，HTTP 状态码与字节数如实记录。
> 其余来源均为 `web_search` **摘要级**，页面未直取，一律标注「**转引自搜索摘要，页面未直取**」。

## 二、已直取（官方博客原文口径，可直接引用）

来源：`https://www.kimi.ai/blog/kimi-k3-1-pro`（HTTP 200 / 385,881 字节）

| 条目 | 数值 / 原文要点 |
|---|---|
| 定位 | K3.1 系列第一款，"our most capable 3T-class open-weight model to date"，**1-million-token context window** |
| Terminal-Bench 4.0 | **K3.1 Pro 得分 65.7%**，ahead of **GPT-6 Astra (58.2%)**，narrowly behind **Claude Opus 5.5 (66.4%)** |
| 脚注口径 | 官方默认 reasoning effort = `max`，temperature = 1.0，top-p = 0.95 |
| 3D / CAD | BenchCAD **92.7% with tools**，approaching Claude Opus 5.5 (96.2%)、GPT-6 Astra (95.9%) |
| 内部编码基准 | Kimi Code Bench 3.0 Long-horizon **61.2%**（K3 为 **55.95%**） |
| 金融 | OfficeQA Pro v2 **64.4**，state-of-the-art |
| 事实幻觉 | Kimi Hallu Bench Hard（内部基准）：claim 级幻觉率 **23.4% → 8.3%**；含至少一处事实错误的回答比例为前代的 **42.4%** |
| 删除动作（两阶段） | ① mid-training 语料内嵌 cyber 相关内容 → 识别并移除；② RL environment mix 中存在 cyber 相关任务 → 过滤。**保留通用编码任务** |
| 原始引语 | "cyber-related content was embedded within the general mid-training corpus, and cyber-related tasks were present in the RL environment mix — a natural byproduct of training on broad data" |
| 原始引语 | "we identified and removed cyber-related data from both training stages, while retaining the general-purpose coding tasks needed for model usefulness" |
| 原始引语 | "We will continue to apply appropriate controls at every training stage, of which cyber-related data identification and restriction is one example" |
| 基准定义 | xdev-bench-hard = **in-house benchmark**，expert-curated，source-code-based vulnerability discovery and exploitation；任务复现 Linux kernel / Node.js / JavaScriptCore / Exim / VirGL 的近期披露漏洞；pass@3，无硬超时、无输出上限 |
| 关键数字 | **未过滤检查点 90.5%**（pass@3）→ **发布版 81.0%**（pass@3） |
| 原始引语 | "the checkpoint without these risk-reduction measures — no cyber-related data removal at mid-training and no cyber-related RL environment filtering — solves 90.5% of problems at pass@3; the final K3.1 Pro reaches 81.0%" |
| 能力定性 | "data removal meaningfully reduces cyber capability relative to what the same training pipeline would otherwise produce"；同时 "stronger general coding and long-horizon debugging capabilities generalize to cyber tasks even after targeted data removal" |
| 自评定位 | "K3.1 Pro's cyber capability remains behind that of frontier proprietary models that have been publicly available for at least three months" |
| 开权原则 | ① "we aim not to release open weights that would extend the absolute frontier of cyber capability… offensive cyber capability is, by design, below what our pipeline can produce"；② "we intend to progressively raise the cyber capability available in open weights"，理由是让防御方能审计自己维护的代码（含长期无人做安全评审的 legacy 系统） |
| 交付 | "The full model weights will be released by Nov 4, 2026."；另有 Highspeed 版，速度 2–3× |

来源：`https://www.moonshot.ai/`（HTTP 200 / 94,238 字节）

| 条目 | 数值 |
|---|---|
| Kimi K3 卡片 | "2.8T parameters, natively multimodal, 1M-token context" |

> ⚠️ K3.1 Pro 是 K3 的后训练版本（博客："post-trained version of Kimi K3"），因此 **2.8 万亿参数属 K3 基座口径**；作品正文按此口径写。

## 三、转引自搜索摘要（页面未直取）

| 条目 | 数值 | 摘要来源 | 备注 |
|---|---|---|---|
| Artificial Analysis 独立智力指数 | **55**，全球第四；Opus 5.5 58 / Sonnet 5.5 56 / Muse Wonder Full 56；较 Kimi K3 的 44 涨 11 分 | 搜狐 10-24 / 知乎专栏 / 腾讯新闻 10-26 | 第三方口径，未直取 |
| AA 同基准复测 TB4.0 | 约 **67%**（与自报 65.7% 并存） | 知乎专栏 | 说明 harness 口径漂移 |
| SWE-Marathon v1.1 | **51.7%**，Opus 5.5 46.3%，该榜第一 | 腾讯新闻 10-26 | 摘要引用 |
| Terminal-Bench Science | **38.1%**（比 Opus 低约 25 点） | 腾讯新闻 10-26 | 摘要引用 |
| 长上下文推理 | **88.7% → 86.3%** | 腾讯新闻 10-26 | 摘要引用 |
| API 定价 | 输入 **$2** / 输出 **$10** / cache-hit $0.20（每百万 token），较 K3 约降 **33%** | 知乎专栏 / 搜狐 | 摘要引用 |
| 激活参数 | **1040 亿激活**（104B） | 知乎专栏 + 内部简报 10-24（激活104B） | 摘要引用 |
| 出口管制 | 中国上周提议把恶意软件相关 AI 技术与漏洞发现工具纳入出口管制 | 内部简报 10-24 技术趋势4（来源 Mint/BidSense） | 摘要级 |
| 舆论分叉 | "负责任对齐，还是降低审核成本" | 内部简报 10-26（知乎热榜/虎嗅） | 摘要级 |
| 商业摩擦 | 额度消耗过快，"栽在额度上" | 腾讯新闻 10-26 | 摘要级 |
| BYOBot 评语 | "第四很好，但不是第一，而定价说的正是这件事" | 内部简报 10-25 | 摘要级 |

## 四、口径拆分（同物异名 vs 两条轨道）—— 避免造出"不存在的分差"

1. **参数规模**：2.8 万亿（官网 "2.8T"）＝中文媒体"3 万亿级" —— **同一轨道，媒体取整**，不构成矛盾。
2. **Terminal-Bench 4.0 的三个数字是三条不同轨道，禁止相减**：
   - 轨道 A：官方自报 **65.7%**（博客脚注口径：reasoning effort=max / temp=1.0 / top-p=0.95）
   - 轨道 B：第三方同基准复测 **约 67%**（摘要级）→ 说明**分数随 harness 漂移**
   - 轨道 C：Artificial Analysis **综合智力指数 55** —— **不是同一把尺子**
   → 因此作品正文与台账都写明：**55 与 65.7 不可直接相减说"被打回 10.7 分"**；"65.7 vs 55"只能作为「两种口径并置」。
3. **90.5 / 81.0**：同一自设基准 xdev-bench-hard 的同口径 pass@3 对照，唯一差异是"是否做两阶段删除"，差值 **9.5 个百分点**。这是本次"自我删除"**唯一可量化的刻度**，且**只有发布方自己测过**。
4. **"开源"与"开放权重"**：官方博客用词为 open-weight release；作品统一写"开放权重"，不混用"开源=公开全部权重"的表述。

## 五、未证实 / 禁止表述清单（作品正文已遵守）

| 禁止写法 | 原因 | 作品中的替代写法 |
|---|---|---|
| 「安全已验证」「删除了攻击能力」 | 无独立第三方复现，官方仅自证 | 「官方自述 / 自设基准测得」「只有发布方自己测过」 |
| 「权重中的攻击能力已被抹除」 | 官方只说"相较同一条流水线本可产出的能力"降低，未提供权重层能力的外部审计证据 | 原样引用官方措辞并标注其自评性质 |
| 「55 分 vs 65.7 分，掉 10.7 分」 | 两条不同轨道 | 并置两把尺子，并写明不可相减 |
| 「xdev-bench-hard 第三方认证通过」 | in-house 基准 | 每次出现都写「自设基准（in-house）」 |
| 「已被证实更安全」 | 官方自评："remains behind frontier proprietary models available for at least three months" | 如实转述官方自评，并标注"自评" |

## 六、作品断言清单（claims，8 条，逐字存在于作品文件内）

| # | value | label | quote（逐字片段） | 口径 |
|---|---|---|---|---|
| 1 | 65.7% | Terminal-Bench 4.0 官方自报得分 | `Terminal-Bench 4.0 得分 65.7%` | 公司自报，博客脚注口径 |
| 2 | 58.2% | 同基准 GPT-6 Astra 得分 | `GPT-6 Astra 的 58.2%` | 官方博客转引 |
| 3 | 66.4% | 同基准 Claude Opus 5.5 得分 | `Claude Opus 5.5 的 66.4%` | 官方博客转引 |
| 4 | 55 | Artificial Analysis 独立智力指数（全球第四） | `Artificial Analysis 独立智力指数 55` | 第三方，摘要级转引 |
| 5 | 90.5% | 未过滤检查点在 xdev-bench-hard 的 pass@3 | `未过滤检查点 pass@3 为 90.5%` | 自设基准，pass@3 |
| 6 | 81.0% | 发布版在同一自设基准的 pass@3 | `发布版 pass@3 为 81.0%` | 自设基准，pass@3 |
| 7 | 2.8 万亿 | Kimi K3 基座总参数（K3.1 Pro 为其后训练版本） | `2.8 万亿参数` | 官网一手，HTTP 200 / 94,238 字节 |
| 8 | 104B | 每 token 激活参数 | `激活 104B` | 摘要级转引（知乎专栏 + 内部简报） |

## 七、留痕

- 一手正文落盘：官方博客抓取副本 `/tmp/kimi_blog.html`（385,881 字节）+ 解析文本 `/tmp/kimi_blog.txt`（23,125 字符），本会话有效，可复核。
- 作品文件：`shared/showcase/2026-10-29/creative/2026-10-29-kimi-attack-ability-removal.html`
- 交付报告：`shared/showcase/2026-10-29/notes/2026-10-29-kimi-attack-ability-removal-交付报告.md`
