# 选题422 · 开放权重 600B 浪潮 · 核源与口径台账

- 日期：2026-11-08（Asia/Shanghai）
- 主责：研析；训练成本与参数口径核算：量研（quant-researcher，session `research-analyst:to:quant-researcher:1794097440553:babd4c8d`）
- 素材：`shared/tasks/每日AI技术动态简报/2026-11-07.md`（焦点3/4/5、技术趋势2）、`shared/tasks/每日热点新闻简报/2026-11-07.md`（科技动态3）
- 交付：`shared/showcase/works/2026-11-08/research/2026-11-08-open-weights-600b-wave.html`

---

## 一、候选断言核源结果

| # | 候选断言 | 核源结论 | 采用 |
|---|---|---|---|
| 1 | 594B ← Inkling 2 Small 参数量（简报汇总口径） | **已核到一手官方公告**：thinkingmachines.ai/news/inkling-2-small/（2026-11-05，页面直取）。原文：`It is a Mixture-of-Experts model with 594B total parameters, 17B active, and supports image inputs and variable effort.` | 采用，来源等级由「汇总口径」升为**官方公告** |
| 2 | 68 小时 ← Inkling 2 训练时长（12T token） | **数字核实，口径错位**。官方：68 小时只对应 **H1 阶段 8.4T token**（`It ran for 68 hours on NVIDIA GB300 NVL72 racks`）。全预训练各阶段相加 = 8.4 + 3.8 + 0.32 + 0.034 ≈ **12.55T token**，但分四阶段、时长只披露 H1；另有主 RL run **9 天**、2048 GPU、>4×10²³ FLOPs、3T+ token。简报「12T token 仅用 68 小时训完」把两个口径合并了。 | 采用，但标签改为「Inkling 2 Small 预训练 H1 时长」，并在正文写明修正 |
| 3 | 5600 亿 ← Ling-3.2-flash 总参数 | **已核到官方文档**：developer.ant-ling.com/zh-CN/docs/models/ling/（页面直取，`Last updated on November 5, 2026`）。原文：`拥有 560B 总参数、25B 激活参数`。5600 亿 = 560B，简报口径与官方一致。 | 采用，来源等级升为**官方文档** |
| 4 | 100 万 token ← Ling-3.2-flash 上下文长度 | **已核到官方文档**：`模型上下文窗口为 1M，原生支持多模态理解`；简报写「100 万 token 上下文」。两口径等价。 | 采用，quote 取简报原文，官方 1M 同页列出 |
| 5 | GPT-6 Cyber「Critical」评级 + IP 白名单（原为单一来源 BYOBot AI Daily） | **已核到 OpenAI 官方系统卡**：deploymentsafety.openai.com/gpt-6-cyber（页面直取）。原文两句：`we give GPT-6 Cyber the same capability designations as GPT-6 Astra: Critical in Cybersecurity` 与 `To make stolen credentials harder to use, we require IP allowlisting for Daybreak Red API access by default.` | 采用，来源等级由「单一来源」升为**官方系统卡**，两条入 claims |

补充核源（候选表之外，同样进页面）：

| 项 | 核源结论 |
|---|---|
| 混元 Hy4 正式版 770B | 中国经济网转官方发布稿（页面直取，2026-11-04 18:29）：`Hy3 系列参数不到 300B，Hy4 系列达到 770B`。激活 49B / 上下文 1M 为 **Hy4 preview（2026-08-28）口径**，正式版官方稿未重复该两项 → 页面标注为 preview 口径。 |
| Hy4 开放状态 | 官方稿：`Hy4 将于近期开源模型权重，发布模型系统卡片` → 归「承诺近期开源」，非「已开源」。 |
| ERNIE-5.5-Flash-Base | Hugging Face 页面 **未能直取**（本机 curl 到 huggingface.co 返回 000，网络受限），参数与 33.5T token 取自简报汇总 + 多家媒体一致转述（TSNMedia、Pandaily、llms.blog、Lab Index）→ 标注**汇总口径 + 媒体交叉一致**，未标官方直取。 |
| Kimi K3.1 Pro | Hugging Face 同样未能直取；2.8T / 104B / 1M / 近 MIT 自定义许可取自简报与 21 世纪经济报道、虎嗅、澎湃新闻交叉一致 → **媒体交叉，未直取官方仓库**。 |
| Ling-3.2-flash 开放状态 | 官方文档**未写** 3.2-flash 权重开放；Ling 系列整体定位为「自主研发并开源的通用大语言模型系列」，但文档明确写已开源的是 Ling-3.0-flash-VL（`目前模型已在 Hugging Face 及 ModelScope 平台开源`）。多家媒体核到「本轮未见 HF 开源权重」→ 页面把 3.2-flash 归**仅 API**，并在核源节写明这是对简报「开源阵营」表述的降级。 |
| GPT-6 Cyber ExploitGym | 官方系统卡：GPT-6 Cyber 48.45%，GPT-6 Astra 42.43%（system card）。简报引用的 Times of AI「48.5% vs 32.1% GPT-5.6 Cyber」是另一对比对象 → 页面用官方系统卡口径，不并列混用。 |

## 二、量研核算（训练成本与参数口径）

来源：量研 2026-11-08 回复（session 见上）。页面中标注为**团队推算 · 未验证**。

- 理论 FLOPs（总参口径）：6 × N × D = 6 × 594×10⁹ × 8.4×10¹² ≈ **3.0×10²⁵ FLOPs**
- 理论 FLOPs（激活参口径）：6 × 17×10⁹ × 8.4×10¹² ≈ **8.6×10²³ FLOPs**
- 两口径相差 **35 倍**（594 ÷ 17），与 MoE 只激活 17B 的事实一致；按总参口径算成本会系统性高估。
- 68 小时 = 2.448×10⁵ 秒 → 隐含算力：总参口径 ≈ **1.2×10²⁰ FLOP/s（122 EFLOP/s）**；激活参口径 ≈ **3.5×10¹⁸ FLOP/s（3.5 EFLOP/s）**
- 机架换算（假设 GB300 NVL72 单机架 FP8 训练峰值 ≈ 1.1 EFLOP/s，厂商公开口径，未独立验证）：总参口径 ≈ 111 机架；激活参口径 ≈ 3.2 机架（MFU 100%）/ ≈ 8 机架（MFU 40%）→ 约 **216~576 张 GB300**。
- 成本（假设 $2~6 / GPU·小时，含整机折价，不含电费、存储、失败重跑）：8 机架 × 68 小时 × 72 卡 = 39,168 卡时 → **约 7.8 万~23.5 万美元**；若按总参口径 111 机架则为 **约 109 万~326 万美元**。
- 量研原始估算给出「72 卡 × 68 小时 = 4,896 卡时、1.0 万~2.9 万美元」，这是**单机架**下限；页面采用按隐含算力反推的机架区间，并同时列出两个口径，避免把单机架成本当成全量成本。
- 量研 B 节把 Inkling 2 Small 上下文写成 256K，与官方 `1M context` 冲突 → **以官方公告为准**，已在页面修正。

## 三、未核与局限

1. ERNIE-5.5-Flash-Base 与 Kimi K3.1 Pro 的 Hugging Face 仓库未直取（网络受限），参数为媒体交叉转述。
2. GB300 NVL72 单机架算力与租赁单价均为公开区间假设，未做硬件基准测试；成本区间只用于说明量级。
3. 混元 Hy4 正式版的激活参数、上下文长度沿用 preview 口径，正式版官方稿未重复披露。
4. Inkling 2 Small 权重落盘时间以官方「下周（next week）」为准，未见具体日期；条件为外部安全测试与红队测试完成。
5. 未跑真实模型推理或复现任何基准分数；页面所有分数均为厂商自报或榜单转述。

---

## 四、门禁执行记录（规则14 · impeccable）

补做日期：2026-11-10（Asia/Shanghai）。补做原因：例会 Step 3 核查发现本 notes 无门禁记录（grep `impeccable|门禁|detect|audit` = 0 命中），按规则14打回。

**作品文件未改动**：`works/2026-11-08/research/2026-11-08-open-weights-600b-wave.html`，46,416 字节，`md5 a4fed3409a1a5c204081cca0f7e51909`，与例会登记一致。本轮只做只读检查与记录，正文数据与断言零改动（`claim_gate.py --verify` 复核见下）。

### 1. 执行顺序与命令

**impeccable 已执行（命令+结论）**，逐条如下：

① `context` — 开工前加载上下文

```
$ cd /app/working/shared/showcase && /app/working/workspaces/agents/research-analyst/skills/impeccable/scripts/impeccable context --target works/2026-11-08/research/2026-11-08-open-weights-600b-wave.html
```
结论（exit 0）：`SCOPED_EXISTING_ALLOWED`（窄幅打磨可用既有实现作权威，不被缺失 PRODUCT.md 阻塞）、`EXISTING_VISUAL_SYSTEM`（代码即视觉权威）、`SURFACE_CONTEXT_AVAILABLE / surfaceBriefReason: not-found`（`.impeccable/surfaces/` 下仅有 hormuz 作品的 brief，本目标无对应 brief，未误用）、`MANUAL_DETECTOR_REQUIRED`（本会话无自动 hook，须手工跑 detect）。

② `detect` — 动手前基线

```
$ cd /app/working/shared/showcase && <skill>/scripts/impeccable detect --json works/2026-11-08/research/2026-11-08-open-weights-600b-wave.html
[]
```
结论：**0 findings**（exit 0），无 error / warning / advisory。

③ `audit` — 按 `reference/audit.md` 五维只记录不修

见下节「五维评分」与「Playwright 实测」。结论：**18/20（Excellent）**，可测项全部通过，3 条 P3 观察项均判定不修（理由见「P3 处置」）。

④ `polish` — 按 `reference/polish.md` 做 triage

结论：**0 项必修**。audit 未产出 P0/P1/P2；3 条 P3 全部「不修」，理由：无渲染影响、且修改会改变已上展文件的字节（例会已登记 46,416B）。因此未对作品文件产生任何写入。

⑤ `detect` — 交付前复检

```
$ cd /app/working/shared/showcase && <skill>/scripts/impeccable detect --json works/2026-11-08/research/2026-11-08-open-weights-600b-wave.html
[]
```
结论：**最终 findings = 0**（exit 0），与基线一致。

### 2. 五维评分（audit）

| # | 维度 | 分 | 关键发现 |
|---|---|---|---|
| 1 | Accessibility | 3/4 | 对比度全达标（见下）；标题层级 1→2→3 无跳级；`lang="zh-Hans"`；未禁用默认焦点环。缺口：无自定义 `:focus-visible` 样式（依赖 UA 默认） |
| 2 | Performance | 4/4 | 全页 1 次请求（`file://` 自身），外部请求 0、失败 0；无 `<img>`/`<script src>`/`<link>`；动效只动 `transform`；`IntersectionObserver` 一次性触发 |
| 3 | Theming | 3/4 | 页面色全部走 `:root` 11 个 token（`--paper/--ink/--ink-soft/--ink-3/--rule/--warn-red/--warn-green/--near-black/--serif/--mono/--paper-raised`）。缺口：SVG 内 6 处 hex 直写、`.metric-label` 引用未定义 `--ink-2`；无暗色主题（浅色档案设计，属有意为之） |
| 4 | Responsive | 4/4 | 1440/768/375 三档无页面级横向溢出；表格走 `.matrix-wrap` 原生横滑，触摸实测可滑；640px 断点折叠时间线；唯一 <24px 触点靠间距例外通过 |
| 5 | Implementation Integrity | 4/4 | `detect` 两次均 0 findings；占位文案 0 命中；id 重复 0；inline JS 2 块 `node --check` 全过；`#claims` JSON 与正文一致 |
| | **合计** | **18/20** | **Excellent（18-20：minor polish）** |

### 3. Playwright 实测

环境：`/app/venv/bin/python3` + Playwright，浏览器 `/usr/bin/chromium --no-sandbox`，脚本 `/tmp/audit_422.py`、`/tmp/svg_contrast_422.py`。目标以 `file://` 打开。

| 检查项 | 方法 | 结果 |
|---|---|---|
| **控制台错误** | 三档视口分别监听 `console`(error/warning) + `pageerror` | **0**（1440×900、768×1024、375×812 各 0 条） |
| **三档视口无溢出** | 比较 `documentElement.scrollWidth` vs `clientWidth`，并扫描越界元素（排除横滑容器内部） | **无溢出**：1440/1440、768/768、375/375，越界元素 0 个 |
| **对比度 ≥4.5:1（HTML）** | 逐元素取 `color` 与合成背景（沿祖先混合 alpha）算 WCAG 比值，274 个含文本元素 | **0 不达标**，最低 **4.63:1**（`.metric-source` 12.5px） |
| **对比度 ≥4.5:1（SVG）** | 逐 `<text>` 取 `fill`，并判定其落在哪个 `<rect>` 上再算比值，34 段 | **0 不达标**，最低 **4.64:1**（「承诺下周 · 1 款」`#1d1d1f` on `#8a867d`） |
| 网络请求 | 监听 `request` / `requestfailed` | 总请求 1（自身），外部 `http(s)://` 0，失败 0 |
| 触摸横滑 | CDP `Input.dispatchTouchEvent` 在 `.matrix-wrap` 上左滑 | `scrollLeft` 0 → **393**（原生横滑可用） |
| 页面竖滑未被吞 | 同上，页面区域竖滑 | `scrollY` 4365 → **4872**（横滑容器未抢走纵向手势） |
| 触摸目标 | 扫描 `a/button` 包围盒 | 唯一小于 24px 者 `↑ 回到顶部` 65×19；最近其它可点目标距离 ≥8430px，24px 圆不相交 → 满足 WCAG 2.5.8 间距例外 |
| 语义与命名 | DOM 扫描 | `h1`×1、`main`×1、标题无跳级、id 重复 0、`img` 缺 alt 0、`svg` 4 个（3 个 `role=img`+`aria-label`，第 4 个为 `aria-hidden` 装饰图标且位于带 `aria-label` 的链接内）、无名链接 0（`<a id="top">` 是 `#top` 锚点目标，不入焦点序列） |
| 降级动效 | 读 CSS | `@media (prefers-reduced-motion:reduce)` 生效，且用 `transform:scaleX(1)` 保住区块分隔线状态，非「一刀切杀掉反馈」 |
| inline JS 语法 | 抽出 2 个 `<script>` 块跑 `node --check` | exit 0 ×2 |
| 占位文案 | grep `TODO\|Lorem\|placeholder\|待补\|XXX` | 0 命中 |
| 断言层未动 | `python3 tools/claim_gate.py --verify` | **重校验 1155 条断言，✓ 全部通过**（exit 0） |

截图（只读留档）：`/tmp/qa422_1440.png`、`/tmp/qa422_768.png`、`/tmp/qa422_375.png`、`/tmp/qa422_375_matrix.png`、`/tmp/qa422_375_timeline.png`、`/tmp/qa422_375_fig2.png`、`/tmp/qa422_1440_fig2.png`、`/tmp/qa422_1440_split.png`。目视：抬头、结论暗带、四档色条、矩阵表、时间线均无裁切、无重叠、无未加载资源。

### 4. P3 处置（polish triage：全部不修）

| # | 项 | 为什么不修 |
|---|---|---|
| P3-1 | `.metric-label` 写 `var(--ink-2,#4f5551)`，`--ink-2` 未在 `:root` 定义 | fallback `#4f5551` 与 `--ink-soft` 同值，渲染零差异；改字节会动到已上展文件。建议下次改版改写为 `var(--ink-soft)` |
| P3-2 | SVG 内 6 处 hex 直写（`#1d1d1f/#66635c/#c9c4b8` 及四档色），未走 token | SVG `fill` 属性不能直接吃 `var()`；渲染与对比度已实测达标。迁移需新增 CSS 类，属改版事项 |
| P3-3 | 图2 副标签 `font-size="11.5"`（对比度 5.08:1 达标）低于他作 12.5px 下限 | `detect` 未判罚（该规则扫 CSS 声明，不扫 SVG 属性）；改字节会影响已上展登记。列为下次改版项 |

### 5. 验证状态

- **已验证**：`impeccable context`、`detect`（基线 + 交付前复检，均 0 findings）、`audit` 五维可测项、`polish` triage、Playwright 全部检查项、`claim_gate.py --verify` — 结果见上表。
- **未验证**：真机触屏（触摸结论来自 Chromium CDP 合成触摸）、跨浏览器（仅 Chromium）、屏幕阅读器实读、200% 文本缩放 — 本轮未执行。
- **未确认**：本机 `impeccable` 启动器只暴露 `context/detect` 等子命令，`audit`/`polish` 无独立 CLI，故二者按 `reference/audit.md`、`reference/polish.md` 的检查表人工执行 — 确认方法：读 `skills/impeccable/scripts/command-metadata.json`。
- **既有问题（与本轮无关）**：`python3 tools/build_manifest.py --check` 报 6 条 README.md / index.html 计数陈旧（作品 125 vs 126、断言 1155 vs 1159），是 #422 等新作品入册后未重新生成所致；本轮只对 notes 追加本节，manifest 不索引 notes，且只跑了 `--check` 只读模式，未写任何生成物。确认方法：重跑 `tools/build_manifest.py`（写模式）后复检。
