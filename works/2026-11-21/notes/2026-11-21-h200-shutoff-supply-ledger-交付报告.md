# 交付报告 · 断供与身份化：H200 停售、五国许可、担保收紧下的中国算力账本

- 交付单：#458（换执行者重派 · 研究类）
- 交付日期：2026-11-21（检索时点 02:13 Asia/Shanghai，早于 14:00 截止）
- 执行者：研析
- 追踪线：厂商与算力权力（`<meta name="showcase-beat" content="厂商与算力权力">`，取自 13 条封闭集）

## 1. 交付物

| 项 | 值 |
|---|---|
| 交付路径 | `shared/showcase/works/2026-11-21/research/2026-11-21-h200-shutoff-supply-ledger.html` |
| 文件字节数 | **42,738 字节**（UTF-8；>10KB 要求满足，单文件成品，未用分片） |
| 断言条数 | **7 条**（`<script type="application/json" id="claims">`） |
| 结构区块 | 9 个 `<section>`：核心判断 / 关键数据 / 三本账 / 两道闸门 / 口径澄清 / 进程 / 图一 / 证据 / 未确认与局限 |
| 本报告路径 | `shared/showcase/works/2026-11-21/notes/2026-11-21-h200-shutoff-supply-ledger-交付报告.md` |

## 2. impeccable 执行记录（AGENTS.md 规则 14）

**impeccable 已执行。**

```
# 1) 上下文加载
$ skills/impeccable/scripts/impeccable context
  → RESOLVED_CONTEXT: projectRoot=.../research-analyst, designPath=DESIGN.md
  → MANUAL_DETECTOR_REQUIRED: 本会话无自动 hook，收尾须手动跑 detect

# 2) 方向定稿后读质量底线
$ 读 skills/impeccable/reference/craft-floor.md

# 3) 机械检测器（首轮）
$ skills/impeccable/scripts/impeccable detect --json <交付文件>
  → 2 项：
    - cream-palette (warning) 页面底色 rgb(242,239,233) 属暖米色默认
    - skipped-heading (warning) <h2> 后直接 <h4>，缺 h3

# 4) 修复（craft-floor 同批复核，一次性 28 处替换）
  - 删除 kicker/eyebrow（craft-floor 明令禁项），编号 458 移入边注元信息
  - 删除 8 处区块序号 01–08（craft-floor 禁项）
  - .note 左侧 3px 彩色粗条 → 1px 边框（禁 >1px 彩色 border-left）
  - 表格单元格 4px 彩色左边框 → 表头色块 + 中性斑马（禁项同上）
  - 条形图 repeating-linear-gradient 斜纹 → 实色（禁项）
  - 文字高亮 linear-gradient → 实色底（禁 gradient text）
  - 圆角 2–3px → 0（账簿直角，elevation 只由边框承担）
  - 底色 cream → 冷调档案纸 #e8ebe9，全 token 化（含 6 个派生 tint token）
  - ledger <h4> → <h3>，消除标题跳级
  - 补浏览器表面：::selection / :focus-visible / 滚动条（webkit + scrollbar-color）
  - 补唯一动效：区块发丝线自左绘出（IntersectionObserver，respect reduced-motion）
  - 正文行宽 .timeline-detail 64ch → 68ch（对齐 65–75ch）
  - 修字体路径 `../../assets` → `../../../assets`（原路径 404，控制台 2 条 ERR_FILE_NOT_FOUND）

# 5) 复检
$ skills/impeccable/scripts/impeccable detect --json <交付文件>
  → []（0 findings）
```

**audit（按 reference/audit.md 五维自评，证据见 §4）**

| # | 维度 | 分 | 关键发现 |
|---|---|---|---|
| 1 | Accessibility | 4 | 三视口计算对比度 0 处不达标；标题层级 H1→H2→H3 无跳级；有 focus-visible 与 reduced-motion 分支；静态文章无交互控件 |
| 2 | Performance | 4 | 无图片、无布局抖动；唯一动效只动 transform；`will-change` 仅挂在 1 个伪元素；字体自托管 + font-display:swap |
| 3 | Theming | 3 | 全部走 `:root` token；本轮已把 6 处硬编码 tint 提为 token；**无深色模式**（纸面卷宗单主题，登记为有意例外） |
| 4 | Responsive | 4 | 1440 / 1024 / 375 三档 `scrollWidth == clientWidth`，无横向溢出；断点 940 / 680；无交互控件故无触控目标问题；**200% 文本缩放未测** |
| 5 | Implementation Integrity | 4 | `impeccable detect` 复检 0 findings；封闭语义词汇表全部就位 |
| | **合计** | **19/20** | Excellent（minor polish） |

**polish（按 reference/polish.md）**：先修功能性（字体 404、标题跳级、断言命中），再修体系漂移（token 化、色板脱离 cream），最后清代码（无调试输出、无死样式、无孤儿 class）。收尾以 detect 清零 + 三视口渲染 QA 收口。

## 3. 断言与标签

### 3.1 断言（7 条，全部过闸）

用 `claim_gate.py` 的 `declared_claims()` + `verify_quote()` + `is_suspect_label()` 逐条实跑：

```
PASS × 7 —— quote 命中=True，语义可疑=[]
gate_work(): L0=3（自动抽取也过闸），L1=3（quote未命中，属时间线邻近误配对，不进任何视图）
```

| # | value | label |
|---|---|---|
| 1 | 24 亿美元 | 英伟达上季度对华 Hopper 数据中心产品销售额（11-17 财报会口径） |
| 2 | 五国 | 纳入先进半导体出口许可范围的国家数（马来西亚、新加坡、印尼、泰国、巴西） |
| 3 | 1200 万 TPP | BIS 逐案许可算力门槛（1200 万 TPP 聚合算力） |
| 4 | 90 天 | BIS 存量业务补办期限（90 天） |
| 5 | 87.9 万块 | 美国对华 AI 芯片许可批准量（截至 2026-05，11-19 众议院外委会披露） |
| 6 | 532 亿块 | 10 月集成电路产量（11-19 国家统计局口径） |
| 7 | 56 万颗 | 平头哥自研AI芯片累计出货量（11-13报道口径） |

### 3.2 实际使用标签清单（动笔前已 grep 近 7 天作品 `.metric-label`）

**复用原文（一字未改，含原日期口径）4 条：**

1. `BIS 逐案许可算力门槛（1200 万 TPP 聚合算力）`
2. `BIS 存量业务补办期限（90 天）`
3. `纳入先进半导体出口许可范围的国家数（马来西亚、新加坡、印尼、泰国、巴西）`
4. `平头哥自研AI芯片累计出货量（11-13报道口径）`

**本篇新建（一次性、自解释，写法＝指标名（来源与日期口径））3 条：**

5. `英伟达上季度对华 Hopper 数据中心产品销售额（11-17 财报会口径）`
6. `美国对华 AI 芯片许可批准量（截至 2026-05，11-19 众议院外委会披露）`
7. `10 月集成电路产量（11-19 国家统计局口径）`

> 检索确认：近 7 天作品中不存在「集成电路产量」「许可批准」同义族，故按新建规则命名；`24 亿美元` 无既有同族标签（grep `中国相关收入`/`24 亿美元` 零命中），故新建。

## 4. 验证证据

**已验证（方法 + 范围 + 结果）**

- 渲染 QA：Playwright + `/usr/bin/chromium`，视口 1440×900 / 1024×800 / 375×812 — 三档均 `scrollWidth == clientWidth`、越界元素 0、控制台错误 0、对比度不达标 0、标题序列 `H1,H2×2,H3×3,H2×6`（无跳级）、9 个 section、Noto Serif SC 与 Newsreader 均已解析。
- 断言闸门：`claim_gate.declared_claims/verify_quote/is_suspect_label` 实跑 — 7/7 PASS。
- 机械检测器：`impeccable detect --json` 复检 — `[]`。
- 边界自检（脚本计数）：`六国` 出现 2 次、`五国＋` 出现 1 次，**均为禁止性表述本身**（「不得合并为「六国」或「五国＋」」「两组数字相加得到的「六国」在规则上没有对应物」），无任何一处把它当作事实口径；`2026-11-18-datacenter-power-ledger` 引用 0 次（旧作品只读参考，未改动、未链接）。
- 字体资源：`../../../assets/vendor/fonts/` 实际存在，控制台 404 已消除（修复前后各跑一次 QA 对比）。

**未验证**

- 预览截图 — 未执行，按禁令由 `gen_thumb.py` 统一持有（本报告不含手工截图）。
- 200% 文本缩放与深色模式 — 未执行，本篇为单主题纸面卷宗，登记为有意例外。
- 11-21 当日后续进展 — 未执行到工作时段（检索时点 02:13），正文已写「未确认」并给出补检方法。

## 5. 核源与边界（逐条对照派单）

| 派单要求 | 落实情况 |
|---|---|
| ① 不改动 11-18 旧作品 | ✅ 只读参考，零写入（`grep` 旧文件仅作标签比对） |
| ② H200 停售口径分清 | ✅ 独立小节「口径澄清：停售是谁的决定」+ 对照表：**英伟达公司决定**（11-17 财报会，克雷斯），非美国官方新禁令；并分列 744.24 官方规则 |
| ③ 744.24 两类触发分列 | ✅ 专节「两道闸门」表格，触发一＝742.6 五国目的地许可，触发二＝744.24 数据中心最终用途许可；正文两处显式禁止合并为「六国／五国＋」，并给出「为什么不能合并」的判定例 |
| ④ 1200 万 TPP 适用范围 | ✅ 限定为「向 D:5 或澳门总部实体提供算力访问的数据中心」，非全部数据中心；表格「适用对象」「阈值」两行逐字写明 |
| ⑤ 11-20/11-21 后续 | ✅ 11-20 有来源（路透、Fortune、阿里真武 V900、众议院外委会 11-19 披露）已另立日期标签；11-21 无来源 → 写「未确认」+ 确认方法 |
| 六项共同项 | 断言 ✅ / 追踪线 ✅ / 路径 ✅ / 材料落 notes ✅ / impeccable 同回合落盘 ✅ / 20 分钟内 >10KB 初稿 ✅（见下） |

**20 分钟初稿取证**：会话起点 `02:13:24`（`get_current_time`）；交付目录 `works/2026-11-21` 创建于 `2026-11-20 18:25:36 UTC = 02:25:36 CST`（`mkdir -p …/notes …/research`）；首版 >10KB 单文件在紧随其后的下一次调用落盘，约 02:26 CST，即开场约 13 分钟，早于 02:33 的 20 分钟线。首版 27,813 字符（write_file 返回值），最终 42,738 字节。文件 mtime 已被后续精修覆盖，故以目录创建时间戳为下界证据。

**生成物未手工改动**：`manifest.json` / `index.html` / `enrich.json` / `tools/claim_changelog.jsonl` 的写入均来自后台 `tools/auto_maintain.py`（PID 582，自 11-20 07:00 运行）与 autopublish 阶段 5.5 自动重建，本会话只写入两个文件：交付 HTML 与本报告。`works/2026-11-18/research/*.html` mtime 仍为 11-18，未被触碰。

**关于 `.bak`（重要，需协调台知悉）**：`works/2026-11-21/research/` 内现有 2 个备份文件，**均由 `tools/auto_maintain.py` 自动生成，不是本会话产物**：

| 文件 | 生成时刻（UTC / CST） | 归属 |
|---|---|---|
| `2026-11-21-h200-shutoff-supply-ledger.html.bak.20261120-184420`（39,200 B，内容为本篇精修中途态） | 18:44:20 / 02:44:20 | 本篇（工具生成） |
| `2026-11-21-tencent-ai-capex-ledger.html.bak.20261120-184420`（34,360 B） | 18:44:20 / 02:44:20 | 另一单 tencent-ai-capex（非本单） |

两个备份在同一秒生成，属 auto_maintain 的批量快照行为。本会话尝试把本篇那份按规则 4 移入 `notes/`（改名为 `.bak-20261120-184420`），**被运行时审批拒绝（`mv` 命令超时未获批，拒绝为终局）**，故文件仍在原处；未对另一单的备份做任何处置（超出本单范围）。如需清点合规，建议由持有 auto_maintain 的一方统一改其备份落点，而非逐个搬运。

## 6. 资料来源

- 每日AI技术动态简报 2026-11-19（第 10、36 行与国家统计局概览）— 逐字引用
- 英伟达 2027 财年 Q3 财报会（11-17 美东）：财新、美国之音中文网转引路透（11-18）
- BIS 11-16 临时最终规则（RIN 0694-AK50）：Pillsbury、Kharon、Lexology、NeoTeo、Complex Discovery、THE D*AI*LY BRIEF、CNBC（11-16 至 11-19）
- 众议院外交事务委员会新闻稿（11-19）+ CNBC / Yahoo Finance 转述（11-19 至 11-20）
- Fortune（11-20，腾讯阿里转国产芯片）、Reuters（11-20，中概科技股承压）
- 通信世界 / 搜狐（11-18，25% 关税安排口径，二手）
- 来源分级：A（BIS 规则原文摘要、国家统计局、国会新闻稿）／C（媒体转述）／D（社交换算口径，已标注）

## 7. 待确认

- D:5 国家组完整名单、744.24 许可审查政策 — 需读规则原文。
- 批准量 87.9 万块对应的实际到货量 — 披露文件未说明。
- 中方拒收 H200 的主管部门口径 — 仅二手转述。
- 1200 万 TPP ≈ 760 块 H100 — 第三方换算，非官方。
