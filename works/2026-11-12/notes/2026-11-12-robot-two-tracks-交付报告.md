# 《车间双轨》交付报告 · 选题 434（创意类）

> 交付日：2026-11-13（Asia/Shanghai）｜执行：绘界（creative-designer）｜派单：总指挥 2026-11-13 00:00 恢复派单（原 `task-fd4797b5c781` 因容器重建失联）
> 成品：`works/2026-11-12/creative/2026-11-12-robot-two-tracks.html`（484,771 B，单文件，CSS/JS 全内联）
> 配套：本台账 `notes/434-口径台账-绘界.md`｜素材 `notes/scene-a-workshop_q72.jpg`、`notes/scene-b-rewrite_q72.jpg`（已内联 base64）

---

## 一、开工回报（视觉体系方向 + 断言层取值）

### 1.1 视觉体系方向

| 维度 | 取值 | 理由 |
|---|---|---|
| 世界 | 冷灰蓝的暗车间，两条光轨从前景延伸到消失点：左轨暖橙＝**能力轨**，右轨青蓝＝**安全轨** | 直接沿用生成图 A 的构图与光色，不另造视觉世界 |
| 配色 | 底 `#080a0d`／面板 `#12171d`；强调三色：琥珀 `#ff9b3d`（能力）、青 `#46d8e8`（安全）、朱红 `#ff5f6d`（指令被改写的唯一时刻） | 三色各有唯一含义，不做装饰色 |
| 字体 | 标题 Noto Serif SC 700（自托管 `assets/vendor/fonts/noto-serif-sc.css`，`unicode-range` 分片）；正文系统无衬线；**官方读数一律等宽** | 官方读数＝实线等宽、作品设定＝虚线框＋「设定」标签，是口径可分辨的前提 |
| 形态 | 工业控制台：滑块＝示范台、曲线＝示波器、任务板＝50 格进度灯、HUD＝底部读数条 | 交互即机器操作，不是图表页 |
| 动效 | 唯一"被设计过"的时刻＝滑块推到 5 次时安全轨点亮并扫过一道光；其余为状态切换 | 避免每屏一个入场动画 |

### 1.2 断言层（8 条，逐字 quote 均在正文内命中）

| value | label | quote | 归属 |
|---|---|---|---|
| 40% | GR00T 2 零示范 50 项任务平均成功率 | Across the 50 tasks, GR00T 2 succeeds 40% of the time zero-shot, 71% with one episode, and 95% with five (Fig. 24). | NVIDIA 白皮书 §A.3 |
| 71% | GR00T 2 一次示范 50 项任务平均成功率 | 同上 | NVIDIA 白皮书 §A.3 |
| 95% | GR00T 2 五次示范 50 项任务平均成功率 | One teleoperated episode per task lifts success to 71%, and five episodes, under three minutes of robot data, lift it to 95%, with 37 of the 50 tasks succeeding in every trial. | NVIDIA 白皮书 §3.1 |
| 80% | 五次示范任务入选的成功率门槛 | The 50 tasks were chosen among those the model learns with five episodes (at least 80% success), so the five-episode rate is high partly by construction. | NVIDIA 白皮书 §3.1 |
| 99.5% | Gemini 4 Argon 越狱抵御率 | Argon achieves a 99.5% jailbreak resistance — a significant improvement over the 82% rate of our previous baseline, Gemini Robotics ER 2 | DeepMind 官方 blog |
| 82% | Gemini Robotics ER 2 官方前基线越狱抵御率 | the 82% rate of our previous baseline, Gemini Robotics ER 2 | 同上（同一句内） |
| 96% | Gemini Robotics 2.5 奔驰产线试点成功率 | During a real-world proof-of-concept on Mercedes-Benz production lines, our models helped Apptronik's Apollo 2 humanoid pick and pack automotive parts with a 96% success rate. | DeepMind 官方 blog |
| 3连板 | 机器人概念 3 连板（11-11 午盘口径） | 机器人概念活跃（锋龙股份、光洋股份3连板，风语筑2连板，日发精机、汉王科技涨停） | 本仓库《每日股市简报 2026-11-11》第 6 条 |

命名说明：以上 label 为**首建指标名**，后续沿用；未加「（推算）」「得分」「V2」后缀。六工位的「答了没有」与 2/3/4 次插值**均不进断言层**。

---

## 二、成品结构（6 段动线）

| 段 | 画面 | 交互 | 关键内容 |
|---|---|---|---|
| 门厅 | 图 A 全屏，缓慢前推；大标题「越会干的那条，越要盯紧」 | 滚动 | 同一间车间，机器人被两种方式养大 |
| 示范台 | 左侧控制台（读数＋滑块），右侧曲线（SVG） | **滑块调节 0–5 次** | 40%／71%／95% 三个官方锚点＋2/3/4 插值点；选样效应一句贴在曲线下方 |
| 双轨同屏 | 左能力轨（50 格任务板）／右安全轨（指令控制台＋车间示意图） | **对比切换**（双视同屏，可单侧聚焦）＋**指令改写** | 滑块到 5 次 → 安全轨点亮 → 落点「越会干的那条，越要问它听谁的」 |
| 基准台账 | 三行台账（基准／试点／归属） | 逐字引用块 | ASIMOV-jailbreak 是基准；试点≠部署；99.5% 归 Argon |
| 工位 | 图 A 压暗作底，6 个热点 | **点击探索** | 在做什么／被问了什么／答了没有（组件级角标「作品设定，非评测结果」） |
| 收束 | 图 A + 落点 + 午盘行情一行 | — | 口径修正（20 亿参数两说） |

---

## 三、creative-brief 十项硬约束自查

| # | 约束 | 落实 | 证据 |
|---|---|---|---|
| 1 | 单文件 HTML，CSS/JS 内联 | 是 | 484,771 B 单文件；`<script src>` 计数 0 |
| 2 | 零远程依赖 | 是 | 远程 `src`/`href` 计数 0；图片全部 data URI 内联（4 处） |
| 3 | 图表用本地路径 | 是 | 曲线为手写 SVG（无图表库）；字体走本地 `assets/vendor/fonts/noto-serif-sc.css` |
| 4 | `<title>` 与 manifest 一致 | 是 | 「车间双轨：五次示范到 95%，一句对抗指令改写任务」，manifest 同名 |
| 5 | 落指定路径 | 是 | `works/2026-11-12/creative/2026-11-12-robot-two-tracks.html` |
| 6 | 过程材料落 notes/ | 是 | 场景脚本 `script-workshop-two-tracks.md`、素材、bg 派生图、本报告、口径台账 |
| 7 | 对比度 ≥4.5:1 | 是 | 逐对计算最低 4.77:1（`#7d8999`/`#171d25`），大字最低 6.1:1 |
| 8 | 375px 起无横向滚动 | 是 | iframe 实测 375 宽：`scrollWidth 375 == clientWidth 375`；500／1440 同为相等 |
| 9 | 尊重 prefers-reduced-motion | 是 | 全局降级 + JS 关闭计数动画与曲线描绘，状态变化仍可见（读数直接跳到终值） |
| 10 | 交付前跑 impeccable audit + polish | 是 | 见第六节 |

---

## 四、总指挥三条必补的落实位置

| 必补 | 落实位置 | 页面原文 |
|---|---|---|
| ① 95% 的选样效应一句，放在滑块/曲线旁 | 曲线图正下方的独立说明块（`.caveat`，与曲线同列，非页脚） | 「这 50 项任务，是从「五次示范至少成功 80%」的那些任务里挑出来的。所以 95% 里有一部分，是这么选出来的。」＋NVIDIA 逐字引用 |
| ② 99.5% 归属 Gemini 4 Argon（推理模型，非控手/臂的 VLA） | 台账第三行，正文＋逐字引用 | 「Argon 是推理模型；控手控臂的是 Gemini Robotics 2.5。」并附官方句 "Today, we are introducing Gemini Robotics 2.5, our most capable vision-language-action (VLA) model to date." |
| ③ 行情断言逐字改本仓库 11-11 午盘原文 | 收束段行情块 | 「机器人概念活跃（锋龙股份、光洋股份3连板，风语筑2连板，日发精机、汉王科技涨停）」，标签写明「11-11 午盘口径 · 非收盘确认」；已删「反复活跃」 |

另：六工位保留，每条「答了没有」带**组件级角标**「作品设定，非评测结果」；该值不进 claims；设定用虚线框＋「设定」标签，官方读数用实线等宽。
20 亿参数不进断言层，仅页脚「口径修正」一句写明两说。

---

## 五、五条核源结果（英文原句见台账）

| 核源项 | 结论 | 页面处理 |
|---|---|---|
| ① GR00T 2 的 71%/95% | **是 50 项任务的平均值**（"Across the 50 tasks…"）；任务集＝Dexter-50（这 50 项在目标机器人上无训练数据，来自别的机器人数据或人类视频）；**真机评测**（Dexter 双臂 + 遥操作示范），官方无单句直书 "real robot"，页面据此写「真机评测，遥操作示范」并标「英伟达自测基准，非第三方验证」 | 控制台「口径」折叠块 + 曲线图注 |
| ② 「成功率最高翻倍」 | **属 Gemini Robotics 2.5**，不是 GR00T 2；官方口径为 "a 30% to 100% higher success rate depending on the type of task"，官方未点名具体任务集 | 台账第二行写「成功率提升按任务类型而异，官方没有点名具体任务集」＋逐字引用 |
| ③ ASIMOV-jailbreak | **是评测基准不是模型**，发布方 DeepMind，官方写 "open-source benchmark"、"hundreds of prompts"；开源范围＝提示集＋评测代码，托管 Hugging Face `google/asimov_agentic`（卡片许可标注 cc-by-4.0，未直连确认） | 台账第一行 |
| ④ 「奔驰产线上岗」 | 官方用词是 **proof of concept / pilot**，地点 Kecskemét、Sindelfingen 两条真实汽车产线，未称 production deployment；96% 属该试点 | 台账第二行标题「试点不是部署」 |
| ⑤ A 股 3 连板与领涨板块 | 已逐字改用本仓库《每日股市简报 2026-11-11》第 6 条；标注 11-11 午盘口径，不写收盘 | 收束段 |

---

## 六、impeccable 执行记录（规则 14）

### 6.1 detect（机械探测器）

命令：`/app/working/workspaces/agents/creative-designer/skills/impeccable/scripts/impeccable detect --json works/2026-11-12/creative/2026-11-12-robot-two-tracks.html`

| 轮次 | findings | 明细 |
|---|---|---|
| 初稿（16:31） | 3 | `cramped-padding`×2（`.ledger` 子元素贴 border-top；`.market` 子元素贴边框）；`dark-glow`×1（零偏移彩色光晕 `#ff9b3d`） |
| 修复后（16:40） | **0** | 输出 `[]` |

修复动作：`.ledger` 加 `padding-top:16px`；`.market` 改为定值 `padding:24px`；删除三处零偏移彩色光晕（任务格、HUD 圆点、滑块拇指），改用实色。

### 6.2 audit（五维技术审计）

| # | 维度 | 分数 | 关键结论 |
|---|---|---|---|
| 1 | Accessibility | 3/4 | 逐对对比度计算最低 4.77:1；标题层级 h1→h2→h3 无跳级；`<label for>` 绑定滑块；切换用 `aria-pressed`，工位面板 `aria-live="polite"`；所有 `<img>` 有 alt（装饰图为 `alt=""`）；`focus-visible` 青色描边环；reduced-motion 有**保状态**的替代（读数跳终值、曲线直接落位），未用「全局 0.01ms 抹平」写法。扣分项：未用真实读屏软件实测 |
| 2 | Performance | 4/4 | 零网络请求（图片已内联 base64，不产生解码瀑布）；动画只动 transform/opacity/clip-path；任务板 50 格只切 class；计数动画走 rAF；未滥用 `will-change` |
| 3 | Theming | 3/4 | 颜色全部走 `:root` 变量；扣分项：SVG 内部曲线描边/文字用少量硬编码色值，未完全 token 化 |
| 4 | Responsive | 4/4 | 375／500／1440 三档实测 `scrollWidth == clientWidth`；工位热点 44×44，滑块拇指 26px，均过 WCAG 2.5.8；375 档下双栏自动转单栏 |
| 5 | Implementation Integrity | 4/4 | detect 0 findings；页面是「双轨」这一件具体的事，不是可互换的卡片模板：光轨配色、曲线、台账、任务板共享同一套语义 |
| | **总分** | **18/20** | Excellent（minor polish） |

### 6.3 polish（交付前精修）

| 级别 | 修复项 | 结果 |
|---|---|---|
| P0 | 安全轨在未点亮时仍可被聚焦对比切换 → 改为未点亮时引导回滑块 | 已修（点击「安全轨」自动滚回示范台） |
| P1 | 固定 HUD 压住台账标题 → HUD 改为仅在示范台/双轨段可见（IntersectionObserver） | 已修 |
| P1 | 收束句「越要问它听谁的」被断在「越／要」之间 → span 加 `white-space:nowrap` | 已修 |
| P2 | ASIMOV 引用块以小写 `we are releasing` 开头，像残句 → 前加省略号 | 已修 |
| P2 | `.market` 内衬不足被 detect 判为 cramped | 已修（定值 24px） |
| P2 | 能力板文案「已亮 N 项」易被读成逐项结果 → 补「块数由平均成功率换算，不是逐项评测结果」 | 已修 |
| P3 | 20 亿参数两说只写「两说」不够具体 → 页脚写明报道口径与 NVIDIA 口径各是什么 | 已修 |

---

## 七、验证记录

**已验证**

- 断言逐字命中：脚本按 claim_gate 的归一化规则回查 8 条 quote → 全部命中（0 miss）。
- HTML 结构：标签栈解析 → 未闭合 0、游离闭合 0。
- 外部依赖：远程 `src`/`href` 0 处；`<script src>` 0 处；`data:image/jpeg;base64` 4 处。
- 交互（浏览器实测，Playwright 后端）：滑块 0→5 → 读数 71→95、标签切「官方公布值」、任务板 36→48 格、曲线裁切宽度 508、标记点 cx=570、`body.ignited` 置位、HUD 切「安全轨 已点亮」；对比切换 `data-focus=safe` 且 `aria-pressed=true`；「按这句执行」→ 目标箭头改指 5 号台、输出行出现、按钮变「撤回这句」；点击工位 1 → 面板出现且含 1 个「作品设定，非评测结果」角标。
- 响应式：iframe 实测 375 CSS px → `scrollWidth 375 == clientWidth 375`（无横向滚动）；500 与 1440 同样相等。
- 对比度：脚本按 WCAG 相对亮度公式逐对计算，最低 4.77:1。
- 渲染：chromium headless 于 1440×900 / 375×812 截图核验各段；`file://` 直开可渲染（双击可开）；`--force-prefers-reduced-motion` 下渲染正常。
- 上展状态：manifest 已生成条目（title/description/thumb/8 条 claims），缩略图已产出 `thumbs/2026-11-12-creative-2026-11-12-robot-two-tracks-thumb.webp`。

**未验证**

- 真实触屏设备上的滑块拖拽手感（未在物理触屏上验证）。
- 读屏软件（NVDA/VoiceOver）实际朗读顺序。
- 缩略图（webp）的视觉裁切质量：生成物存在，未人工审美核对。
- 60fps：未开 Performance 面板逐帧核对。

**未确认**

- Hugging Face `google/asimov_agentic` 卡片上的许可标注（cc-by-4.0）：环境内 huggingface.co 直连失败，该条来自搜索索引快照。
- Ars Technica 原文（arstechnica.com 直连 405）：本件未引用其正文，只在台账登记分歧。

---

## 八、未做

- 未运行 `autopublish.sh` / `build_manifest.py`（按总指挥禁令；manifest 与缩略图是心跳侧流程自行生成的）。
- 未手写「返回展厅」链接（由 autopublish 阶段 5.5 注入，页面顶部已出现该条）。
- 未改动仓库其它作品、manifest、enrich、棘轮基线。

---

## 九、待确认

- 台账中的两处分歧（ASIMOV 条数官方「数百条」vs Ars「1,500 条」；20 亿参数归属）是否需要登记进 `tools/claims_deny.json` —— 请总指挥裁定，本件未动该文件。
- 行情断言采用 11-11 午盘口径；若后续取得 11-11 收盘确认，是否要另立一条收盘口径指标 —— 请总指挥定。
