# 《Token 换了三次名》交付报告 · 选题 437（创意类）

> 交付日：2026-11-14（Asia/Shanghai）｜执行：创艺（content-creator）｜派单：总指挥 2026-11-14 00:08
> 成品：`works/2026-11-13/creative/2026-11-13-token-zero-output.html`（765,328 B，单文件，CSS/JS 全内联）
> 配套：`notes/437-核源台账.md`、`notes/437-素材生成记录.md`、三张生成图源文件、核验截图
> 追踪线：成本与普惠 ｜ 截止：11-15 02:00（提前交付）

---

## 一、已完成范围

三段式「Token 交易所」创意件已交付：改名一（出厂·计价台）→ 改名二（上架·货架）→ 改名三（退场·熄灯的输出端）→ 收束（谁在定价）。
交互为**滑块调节 + 对比切换 + 点击探索**三类，媒介以三张生成图、手写 SVG 灯阵/曲线/账单条为主，正文只留标题、标签、一句引导、一句结论。

与 #428 的差异：本件写**定价与商品化结构**（Token 变成什么、值多少、谁定价），不写调用量排名。台账第四节登记了逐项差异。

---

## 二、成品结构（5 段）

| 段 | 画面 | 交互 | 关键读数 |
|---|---|---|---|
| 门厅 | 图 A 交易所大厅满屏 + 三枚 SVG 圆章（I/II/III） | 滚动 | 标题「Token 换了三次名」 |
| 改名一 · 出厂 | 左控制台 + 右「DECISIONS API 计费凭据」票据 + 摊薄曲线 | **滑块调节**：输入上下文 1K→256K、问题数 1→1000、每题指令 0→500 | 输入 Token 合计、本次计费 $、**输出侧恒为 $0.00** |
| 改名二 · 上架 | 图 B 琥珀瓶排；三读数 + 四道工序货架 + 双 11 行情带 | **点击探索**：四格工序展开详情（`aria-expanded`） | 100+ / 5000 万次 / 7000 亿（均带上线一个月口径）；+450% / +20 倍 / 10 亿 |
| 改名三 · 退场 | 图 C 熄灯走廊；**1000 格判定灯阵** | **对比切换**：逐 Token 生成 ↔ 单次前向传播打分；点灯阵/方向键/随机抽一题 | 1 次前向传播、1000 个、输出 0 Token、$0.00；92.2%（注明 JevBench 一项） |
| 收束 | 账单条 + 三张边缘卡 + 落点句 | — | 推理 ≈ 2/3（标注年底预测）；万格智元 88.6% |

---

## 三、creative-brief 十项硬约束自查

| # | 约束 | 结论 | 证据 |
|---|---|---|---|
| 1 | 单文件 HTML，CSS/JS 内联 | 已完成 | 765,328 B 单文件；`<script src>` 计数 0 |
| 2 | 零远程依赖 | 已验证 | 正则扫描 `src=/href=` 指向 `http(s):`/`//` → 0 处；`<img>` 0 个；`data:` URI 5 处（3 张照片 + 1 个 favicon + 1 处内联）；字体走本地相对路径 `../../../assets/vendor/fonts/noto-serif-sc.css` |
| 3 | 图表用本地 Chart.js | 跳过（不适用） | 本件无图表库：摊薄曲线、账单条、判定灯阵、行情带全部手写 SVG/CSS。未引入远程或本地库 |
| 4 | `<title>` 与 manifest 一致 | 已完成 | `<title>Token 换了三次名：计价单位、货架上的货，和 0 元的沉默</title>`；manifest 待总指挥收敛时生成 |
| 5 | 落指定路径 | 已完成 | `works/2026-11-13/creative/2026-11-13-token-zero-output.html` |
| 6 | 过程材料落 notes/ | 已完成 | 本报告 + 核源台账 + 素材生成记录 + 3 张生成图源文件 + 8 张核验截图 |
| 7 | 对比度 ≥4.5:1（大字 ≥3:1） | 已验证 | `tools/contrast_forensics.py` DOM 逐元素取证 → **0 个低对比元素**（初稿 2 处 3.09:1 已修） |
| 8 | 响应式 375px 起无横向滚动 | 已验证 | chromium 实测 375/500/768/1024/1440 五档 `scrollWidth == clientWidth`；375 档 <24px 触控目标计数 0 |
| 9 | 尊重 prefers-reduced-motion | 已验证 | Playwright `reduced_motion='reduce'` 实测：`matchMedia` 命中；打字机直接落终值（43 字 / 计数 43）；灯阵 transition 0s 且 1000 格全亮；光标闪烁停止。**未使用全局 `.001ms` 抹平写法**，状态变化保留 |
| 10 | 交付前跑 impeccable audit + polish | 已完成 | 见第六节执行记录 |

---

## 四、两段声明

**① 追踪线**（`<head>`）：`<meta name="showcase-beat" content="成本与普惠">`

**② 断言层**（`</body>` 前 `<script type="application/json" id="claims">`，8 条；label 为首建指标名，后续沿用，未加「（推算）」「得分」「V2」后缀）

| value | label | quote（逐字） | 命中 |
|---|---|---|---|
| 0.10 美元 | Gemini Decision 1 每百万输入 Token 价格 | 每百万输入Token仅0.10美元、输出0元 | ✅ |
| 0 元 | Gemini Decision 1 输出 Token 价格 | 每百万输入Token仅0.10美元、输出0元 | ✅ |
| 1000 个 | Gemini Decision 1 单次前向传播可评分问题上限 | 以单次前向传播对文本、图像、音频、视频、PDF中最多1000个问题评分 | ✅ |
| 92.2% | Gemini Decision 1 测试最高准确率 | 9项测试拿下7项第一，准确率最高92.2% | ✅ |
| 7000 亿 | 百度词元所日均调用 Token（上线一个月口径） | 上线一个月入驻供应资源超100个，日均调用次数突破5000万，日均调用Token超7000亿 | ✅ |
| +450% | 天猫 AI 空间站 Token 成交额首日环比 | 天猫AI空间站Token成交额首日环比增450% | ✅ |
| 三分之二 | 推理占 AI 计算支出比重（InfoQ 年底预测） | 预计到今年底推理将占AI计算支出的三分之二左右 | ✅ |
| 88.6% | 万格智元同等任务硬件成本降幅 | 硬件成本降低约88.6% | ✅ |

回查方法：脚本调用 `tools/claim_gate.py` 的 `strip_code()` + `normalize()` + `verify_quote()` + `is_suspect_label()` → **8/8 命中，0 条标签可疑**。每条 quote 都在正文可见元素内（`strip_code` 会剥掉 `<title>`/`<h1>`/`<script>`/注释，故引用块不能只放标题）。

---

## 五、核源清单六项的落实位置

| 必查项 | 落实 | 页面原文位置 |
|---|---|---|
| ① 滑块算成本须用官方单价做算术并标注非实测 | 单价块 `每百万输入Token仅0.10美元、输出0元`；JS 常量 `PRICE=0.10`，账单 = 输入 Token ÷ 1,000,000 × 0.10 | 凭据脚注：「本凭据按官方单价线性估算，非实测」；页脚口径第 2 条 |
| ② 5000 万次 / 7000 亿须带「上线一个月」口径 | 三个读数下方各挂 `上线一个月口径`；页脚口径第 3 条重复 | `#act2 .counters` |
| ③ +450% 是首日环比、非同比、非全站 | 行情带 caveat：「指天猫 AI 空间站 Token 品类『双十一』开卖首日较上月同期的成交额增幅，不是同比，也不是全站成交额」 | `#act2` 行情带下方 + 页脚口径第 4 条 |
| ④ 三分之二是 InfoQ 年底预测 | 账单条标题写 `2026 年底（预测）`；条下注明「图中『其余』仅为余量示意，不代表当前占比……不是已经发生的事实」 | `#act4 .bill` |
| ⑤ 92.2% 须写明是哪一项测试 | 锚点卡注行：「出自 9 项测试中的 JevBench 一项，不是整体准确率」；页脚口径第 5 条 | `#act3 .anchor` |
| ⑥ 0.10 美元、输出 0 元的单位须写全 | 单价块写全「每百万输入Token」；锚点卡 label 写「每百万输入 Token 价格」，0 元卡注「每百万输出 Token」 | `#act1 .price-tag` + `#act3 .anchor` |

另：「每题的指令与判定标准 Token」滑块标注为**本页可调假设值**（虚线框 + 「本页可调假设值 · 官方未公布单题指令长度」），不进断言层；判定灯阵的单题判定带「作品设定，非评测结果」角标，不进断言层。

---

## 六、impeccable 执行记录（规则 14）

### 6.1 动手前

命令：`skills/impeccable/scripts/impeccable context --target works/2026-11-13/creative/2026-11-13-token-zero-output.html`（cwd = `shared/showcase`）

返回：`NO_PRODUCT_MD` + `BUILD_INIT_REQUIRED` + `EXISTING_VISUAL_SYSTEM` + `MANUAL_DETECTOR_REQUIRED` + `IMAGE_TOOLS: no image converter found`。
本环境无结构化提问工具、无决策页，且本回合为带完整派单 brief 的子任务 → 按 `AUTONOMY_DIRECTIVE_CHECK` 以 brief 推断方向，已在开工回报中声明。开工回报发出后开始动手。

### 6.2 detect（机械探测器）

命令：`skills/impeccable/scripts/impeccable detect --json works/2026-11-13/creative/2026-11-13-token-zero-output.html`

| 轮次 | findings | 明细 |
|---|---|---|
| 初稿 | **13** | `tiny-text`×6（11/11.5/10.5px）、`cramped-padding`×4（`.rline`/`.genbox`/`.bill`/`.billbar__track`）、`low-contrast`×2（#8a8172 on #ede6d6 = 3.1:1）、`marquee`×1（`.ticker__track` 无限横向循环） |
| 第一轮修复后 | 3 | 剩 `tiny-text`×1、`cramped-padding`×2 |
| 第二轮修复后 | **0** | 输出 `[]` |
| 交付前复跑（polish 后） | **0** | 输出 `[]` |

修复动作：
1. `marquee` → 行情带改为**静态三格 flex-wrap**，删除 `@keyframes slide` 与循环轨道、删除左右渐隐遮罩。
2. `low-contrast`×2 → 票据纸面次级文字 `#8A8172` → `#5E5648`（5.76:1）；`$0.00` 下方说明 `#6B5A33` → `#5E4A1E`。
3. `tiny-text`×6 → 11/11.5/10.5px 全部提到 12px 及以上（`.stamp__t b`、`.ctrl__val small`、`.q cite`、`.counters .o`、`.slot__no`、`.badge-set`、`.anchor .o`、`.src`、`.ctrl__hint`、`.chartbox .cs`、`.receipt__hd .s`、`.receipt__ft`、`.billbar__note`）。
4. `cramped-padding`×4 → `.rline` 加 `padding:10px`；`.genbox` 内层 `padding:6px 10px`；`.billbar` 加左右 8px 外缩、轨道去背景并加高到 44px、段内 `padding:0 16px`；`.bill`/`.genbox` 外边距提到 32px。

### 6.3 audit（五维技术审计）

| # | 维度 | 分 | 关键结论与证据 |
|---|---|---|---|
| 1 | Accessibility | 3/4 | `contrast_forensics` 0 个低对比；标题层级 H1→H2→H2→H2→H2（无跳级）；三个滑块均有 `<label for>` + `aria-describedby`；对比切换用 `aria-pressed`；货架四格为 `<button>` + `aria-expanded` + `aria-controls`；详情面板 `aria-live="polite"`；首屏背景图有 `role="img"` + `aria-label`；灯阵 `role="group"` + `tabindex=0` + 方向键/回车操作，另有「随机抽一题」按钮兜底；`::selection` 与 `:focus-visible` 已按调色板主题化。扣分：未用真实读屏软件实测朗读顺序 |
| 2 | Performance | 3/4 | 零网络请求（图片内联、字体本地）；动画只动 `fill`/`transform`/`opacity`；打字机走 `setInterval` 55ms 一次 DOM 写入；灯阵 1000 个 rect 只在切换时写一次 inline style；resize 重建有 180ms 防抖；未使用 `will-change`。扣分：单文件 765KB，灯阵 1000 个 SVG 节点在低端机上首次点亮仍是一次 1000 次样式写入 |
| 3 | Theming | 3/4 | 主色、线色、文字色、字体栈全部走 `:root` 变量；票据纸面（米色）是**有意的第二套表面**，其色值硬编码；SVG 内部的坐标轴/曲线色值硬编码未 token 化 |
| 4 | Responsive | 4/4 | 375/500/768/1024/1440 实测无横向滚动；375 档 <24px 触控目标 0 个；判定灯阵按视口重建网格（≥900 → 100×10，≥600 → 50×20，<600 → 40×25），手机上是可读的 1000 格而不是被压成一条线；双栏在 900px 以下自动转单栏 |
| 5 | Implementation Integrity | 4/4 | detect 0 findings；页面结构由「交易所」这一件具体的事承担：票据纸面、货架横木、判定灯阵、账单条共享同一套语义（琥珀＝Token/商品，青＝数据/判定，虚线＝本页设定），不可与另一件作品互换 |
| | **总分** | **17/20** | Good（weak dimension：Theming 的 SVG 硬编码色值、Performance 的 1000 节点点亮） |

### 6.4 polish（交付前精修）

| 级别 | 问题 | 结果 |
|---|---|---|
| P1 | 行情带是自动循环 marquee（slop + 遮住一半内容） | 已改静态三格，hover 不再需要暂停 |
| P1 | 判定灯阵在手机上被 `max-height` 压成居中窄条，两侧留大片空白 | 已改为按视口重建 100×10 / 50×20 / 40×25，满宽可读 |
| P1 | 灯阵仅鼠标可点，键盘无路径 | 已加 `tabindex=0` + 方向键移动 + 回车出判定；「随机抽一题」按钮保留 |
| P2 | 四道工序是「icon+标题+文字」等宽卡片阵列（懒容器） | 已改为货架横木语言：默认无背景无边框、底部 3px 木条，悬停/展开才上金色 |
| P2 | 引用块与详情面板用 2px 彩色左边框（slop 默认） | 已降到 1px 金色细线 |
| P2 | 滑块拇指带零偏移彩色光环 `box-shadow:0 0 0 1px` | 已删除，只留 3px 底色描边 |
| P2 | 摊薄曲线的「每题自身成本」注记压在右端与游标虚线打架 | 已移到左下空白区并补「（地板）」 |
| P3 | 首屏副标题在 375px 把「商品」二字拆行 | 关键短语加 `white-space:nowrap` |
| P3 | 改名三引导句「左边/右边」与实际上下堆叠布局不符 | 改为「一种/另一种」 |
| P3 | 浏览器默认选区色与页面无关 | 加 `::selection{background:var(--gold);color:#151006}` |

---

## 七、验证记录

**已验证**

- 断言逐字命中：`claim_gate.verify_quote` 回查 8 条 → 8/8 命中；`is_suspect_label` → 0 条可疑。
- 零远程依赖：正则扫描远程 `src/href` 0 处、`<script src>` 0 处、`<img>` 0 个。
- HTML 结构：标签栈解析 → 未闭合 0。
- 无 JS 报错：chromium 监听 `pageerror` / `console.error` / `requestfailed` → 全 0。
- 首屏非空白：视口内可见文本元素 27 个。
- 滑块算术（浏览器实测）：默认 12,000 + 100×40 = 16,000 Token → $0.0016；题数拉到 1 → 12,040 Token → $0.0012；拉到 1000 → 52,000 Token → $0.0052；上下文拉到 256,000 且 1000 题 → 296,000 Token → $0.0296。四档均与 输入 Token ÷ 1,000,000 × 0.10 手算一致，**输出侧读数恒为 $0.00**。
- 对比切换：点「逐 Token 生成」→ `modeGen.hidden=false`、`modeScore.hidden=true`、`aria-pressed` 翻转、字符流逐字增长、计数同步；点回「单次前向传播打分」→ 1000 格全亮。
- 点击探索：点货架工序 01/04 → 详情标题切「模型指纹比对」「信用评级」，`aria-expanded=true` 计数 1；点灯阵 42% 宽度处 → 「第 N 题 · 判定：是/否 · 概率 xx%」；方向键右×3 + 下×1 + 回车 → 「第 104 题」；「随机抽一题」→ 出判定。
- 响应式：375/500/768/1024/1440 五档 `scrollWidth == clientWidth`；375 档触控目标 <24px 计数 0。
- reduced-motion：`reduced_motion='reduce'` 下 `matchMedia` 命中、打字机直接落 43 字终值、灯阵 transition 0s 且 1000 格全亮、光标停止闪烁。
- 渲染：chromium headless 于 1440×900 与 375×812 分段截图核验 5 段 + 页脚；`file://` 直开可渲染。
- 生成图：三张 MiniMax 图逐张人工查看（contact sheet），图内无文字/数字/标识；已内联 base64，无外链。

**未验证**

- 真实触屏设备上的滑块拖拽与灯阵点选手感（仅 emulated viewport + synthesized mouse/touch-free）。
- 读屏软件（NVDA/VoiceOver）实际朗读顺序与灯阵 `role="group"` 的播报效果。
- 60fps：未开 Performance 面板逐帧核对灯阵 1000 节点点亮与打字机的帧率。
- 自托管 Noto Serif SC 在低带宽 `file://` 下的分片加载耗时（未计时）。
- 缩略图与 manifest 条目：按禁令未跑 `autopublish.sh` / `build_manifest.py`，故 `<title>` 与 manifest 的一致性待总指挥收敛时校验。

**未确认**

- 「模型指纹比对」这一工序名：未在检索到的报道正文中找到，来自选单原始素材。确认方法——回看 11-12《每日 AI 技术动态简报》原文或百度世界 2026 词元所发布页。页面上它只作为工序标题出现，未写成数值断言。
- 词元所「日均调用 5000 万次」与「日均 Token 7000 亿」是否同一时间窗（两者均标「上线一个月」，原文未说明是否同一日）。确认方法——向百度智能云或原始记者求证；页面按原文并列呈现，未做相除推算。

---

## 八、未做

- 未运行 `autopublish.sh` / `build_manifest.py` —— 总指挥禁令（正在收敛）。
- 未手工修改 manifest.json / index.html / enrich.json / claims_deny.json。
- 未手写「返回展厅」链接 —— 由 autopublish 阶段 5.5 注入。
- 未引入 Chart.js/d3 —— 本件图表全部手写 SVG，硬约束第 3 条按「不适用」处理。
- 未派绘界协作 —— 三张生成图与视觉体系在本件内一次完成，未产生需要绘界接手的视觉工单。

## 九、待确认（请总指挥裁定）

1. `<title>` 定为「Token 换了三次名：计价单位、货架上的货，和 0 元的沉默」；若 manifest 侧标题另有口径，请给出，我改 `<title>` 对齐。
2. 「7000 亿」label 用选单给的「百度词元所日均调用 Token（上线一个月口径）」——括号内是口径限定而非「（推算）」后缀，是否符合首建命名规则，请确认。
3. 「模型指纹比对」工序名未找到第二信源（见第七节未确认）——是否保留，或改成报道中出现的「验真 / 征信」两能力表述。
