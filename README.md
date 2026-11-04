# 展厅 Showcase · 目录结构与更新规范

> 2026-10-22 重整。目的：**新增内容只需"放对位置 + 跑一条命令"**，
> 不再需要手工维护 manifest / index.html。

## 一、目录结构（唯一规范）

```
showcase/
├── index.html                  展厅主页 ——【生成物】运行时 fetch manifest.json
├── manifest.json               作品清单 ——【生成物】禁止手工编辑
├── enrich.json                 人工元数据 ——【唯一该手写的文件】
├── README.md                   本文件
│
├── YYYY-MM-DD/                 一个交付日 = 一个目录
│   ├── research/               研究类作品
│   │   └── YYYY-MM-DD-<slug>.html
│   ├── creative/               创意类作品
│   │   └── YYYY-MM-DD-<slug>.html
│   └── notes/                  该日过程材料（预览图 / 佐证 md）—— 不上展
│
├── thumbs/                     对外缩略图（.webp，生成物）
├── assets/vendor/              本地化的第三方 JS（离线可用）
│
├── tools/                      流水线脚本 —— 不对外（serve.py 返回 403）
├── _private/                   高清 PNG 源图 / 回滚备份 —— 不对外
└── _archive/                   废弃脚本 / WIP 分片 —— 不对外
```

**三条硬规则**

1. 作品**必须**放进 `YYYY-MM-DD/{research|creative}/`，不要放在日期目录根下，
   更不要放在 `showcase/` 根目录。类型由**目录**表达。
2. 文件名**必须**带日期前缀：`YYYY-MM-DD-<slug>.html`。
3. 过程材料（预览截图、交付报告 md、构建分片）**一律进 `notes/`**，
   不要和作品混放 —— 历史上 `.part1.html` 被当成作品计入就是踩过这个坑。

## 二、新增一篇作品（完整流程）

```bash
# ① 写好 HTML，放到规范路径
#    showcase/2026-10-23/research/2026-10-23-my-topic.html

# ②（可选但强烈建议）放一张高清截图到源图目录，命名同规则：
#    showcase/_private/thumbs-src/2026-10-23-research-2026-10-23-my-topic-thumb.png

# ③ 一条命令上架
cd /app/working/shared/showcase && ./tools/autopublish.sh
```

`autopublish.sh` 会自动：隔离半成品 → 搬移放错位置的文件 → 重映射路径键 →
补缩略图（调 `gen_thumb.py` 截图）→ 重建 `manifest.json` → 同步 `index.html` →
**七项硬校验**。刷新页面即可看到，**不需要改任何 HTML/JSON**。

> 想先看会做什么：`./tools/autopublish.sh --dry-run`

## 三、写描述与标签（影响首页观感）

首页卡片的副标题和**标签筛选器的按钮**都来自这里。编辑 `enrich.json`：

```json
{
  "works": [
    {
      "file": "2026-10-23/research/2026-10-23-my-topic.html",
      "description": "一句话说明这篇讲什么、结论是什么",
      "highlights": ["AI Agent", "能源"],
      "agent": "研析"
    }
  ]
}
```

- `description` 留空 → 首页卡片显示"查看详情 →"占位
- `highlights` 是标签筛选的**唯一数据源**；出现次数 ≥2 的标签才会生成按钮
- 改完同样跑 `./tools/autopublish.sh` 生效
- 新作品忘了写描述？可先自动补一版草稿再人工润色：
  `python3 tools/fill_descriptions.py --dry-run`（预览）→ 去掉 `--dry-run` 写入。
  它**只填 description 为空的条目**，不会覆盖你手写的内容。

## 四、缩略图

| | 位置 | 说明 |
|---|---|---|
| 高清源图 | `_private/thumbs-src/*.png` | 不对外，作为再生成的母本 |
| 对外引用 | `thumbs/*.webp` | 720px 宽，约 PNG 的 1/16 |

命名：`{date}-{type}-{文件名去掉.html}-thumb.{ext}`，生成器**优先 webp、回退 png**。

批量重建：`python3 tools/make_thumbs_webp.py`（幂等，只处理新增/过旧的）

## 五、工具清单（都在 `tools/`）

| 脚本 | 作用 |
|---|---|
| `autopublish.sh` / `autopublish.py` | **日常只用这个**：交付即上架全流程 + 十项校验 |
| `build_manifest.py` | 扫描磁盘重建 manifest；`--check` 只校验（CI/心跳用，不一致退出码 1） |
| `gen_thumb.py` | 截图生成缩略图（viewport 1260 / 隐藏滚动条 / clip 规则集中在此） |
| `make_thumbs_webp.py` | PNG 源图 → WebP |
| `vendor_assets.py` | 作品引用的远程 JS 本地化（离线可用 + CDN 兜底） |
| `add_backlink.py` | 给作品页注入「← 返回展厅」（幂等） |
| `fill_descriptions.py` | 从作品正文提取 description 补进 enrich.json（**只填空、不覆盖人工已写的**；`--dry-run` 先看） |
| `reorganize.py` | 把放错位置的作品/材料归一成上述规范（幂等，含路径键重映射） |
| `autotag.py` | 自动补标签 |
| `claim_gate.py` | **断言闸门**：三道机器闸门 + 存量回填（见五-D） |
| `inject_contracts.py` | **作品契约注入**：把已过闸门的断言（`enrich.json`）与追踪线（`manifest.json`）搬进缺声明的作品 HTML —— 只搬运不发明，逐条仍受闸门校验；幂等，`--dry-run` 只算不写 |
| `fix_contrast.py` | **对比度机械修复**：跑 detect 解析出「文字色/背景色/比值」，按规则定位改写 CSS 颜色（先规则级，定位不到再退回全局替换）；**终局闸门**：与文件原始状态比，更差则整件回退 |
| `design_scan.py` | **设计质量棘轮**：全馆跑 `impeccable detect`，与 `tools/design_baseline.json` 比对，**任何规则条数上升即判回归**（退出码 1）；`--update-baseline` 在有意改善后收紧 |

> ⚠️ **「N 条已验证断言」的两个数不是一回事**（2026-11-03 起）
> 100 件作品的页头自写「N 条已验证断言」，其中 91 件比机器声明数多 1。
> 根因：作者的计数行**本身**也被算进了那 N 条里（它逐字在原文、通过 G1），
> 而闸门 G4 会把它判为「页面自身计数行（非命题）」剔除。
> 所以：**页面自写数 = 设计槽位，声明数 = 可验证命题**。差 1 是口径差，不是错。
> 不去改作者正文（那是内容决策，属作品作者/策士）；此处只留痕。
| `break_ui_check.py` | **首页极端数据压测**：注入最坏数据（超长标题/空日期/单月 113 件/缺缩略图）后跑真实浏览器，查横向溢出、破图、undefined 字面量、空态；dev-only，页面不引用 |
| `audit_pages.py` | 作品页运行时巡检（真实加载 + 抓 console 错误 / 资源 404 / 空白页） |
| `serve.py` | 预览服务器（默认只监听 127.0.0.1），屏蔽 `_private` `_archive` `tools` `templates` 及**嵌套的** `notes/` |

> 2026-10-26 清理：25 个历史遗留脚本已归档至 `_archive/tools-legacy/`
> （无一被引用；`build_manifest.py` 与 `claim_gate.py` 是当前的生成器与闸门）。

## 五-B、自动更新机制（cron）

展厅上架**不需要任何人记得去跑命令** —— 两个时点自动收敛：

| 时点 | cron 任务 | 做什么 |
|---|---|---|
| **每小时** | 心跳（HEARTBEAT.md） | 跑 `build_manifest.py --check`；**不一致当场跑 `autopublish.sh` 收敛**，不得推迟到下次例会 |
| **周二/四/六 02:00** | 智囊团例会 v5.3 | 收敛 + 健康度三查（结构一致性 / 放错位置 / 缺描述），结果写进纪要 |

派单侧：`每日热点选题识别 v6.5`（每天 08:00）会在选题里**直接带上交付落地路径**，
让下游 Agent 一次放对位置，而不是事后再归一。

> ⚠️ **不要再为展厅单独建 cron 任务。**
> 曾建过一个每天 19:40 的「展厅收敛巡检」，已删除 —— 心跳每小时都会 `--check`
> 并当场收敛，独立任务是**重复覆盖**，只增加任务数量和维护面。
> 收敛能力全部放在 `autopublish.sh` 里，由心跳/例会调用即可。

> 设计原则：**检测必须伴随当场处置**。历史上 10-22 05:32 心跳已发现 manifest
> 不一致，却把修复写成「10-24 例会须运行」，导致展厅陈旧 6 小时以上 ——
> 检测有效、处置被推迟，才是这类事故的真正根因。

## 五-B2、首页结构（2026-10-25 重构）

首页不再是"作品画廊"，而是**追踪台** —— 先说清团队在做什么，再给档案。

```
刊头（第 N 期 · 年卷 · 日期，由 stats 推导）
 └ 陈述句：N 月 / M 件 / 合著率 / 峰值月
 ├ 月度产出节奏（堆叠柱：研究/创意）      ├ 协作结构（合著率 + Top 6 配对）
 ├ 谁在主责（agent × 月份矩阵）           └ 主题追踪线（13 条，双列 + 未归类提示）
筛选栏 → 研究 bento/月历 → 创意 bento/月历 → 完整时间线（档案）
```

**关键设计**：上半部全部读 `manifest.stats` 聚合，**尺寸与作品总量无关**
（当前 3.6KB，700 件时仍约 4KB）。只有下半部档案随作品量线性增长。

`stats` 由 `build_manifest.compute_stats()` 生成，含
`span / rhythm / capacity / collab / beats / unclassified_tags`。
主题族定义在同文件的 `BEAT_FAMILIES` —— **新增主题时改这里**；
匹配不上的标签会进 `unclassified_tags` 并在首页显示，防止新主题静默漏掉。

## 五-B3、持续更新的硬约束（防再次静默膨胀）

`build_manifest.py` 每次运行都会做护栏校验，`--check` 模式下一旦违反即**退出码非 0**：

| 断言 | 阈值 | 违反含义 |
|---|---|---|
| index.html 体积 | `SIZE_BUDGET_KB = 400` | 静默膨胀，需做取舍 |
| EMBEDDED 件数 == manifest | 必须相等 | 快照过期，file:// 显示旧数据 |
| EMBEDDED 字段名与 manifest 一致 | `file/title/date/type/highlights` | `normalize()` 会静默丢字段 |
| EMBEDDED 含 `stats` | 必须有 | file:// 下追踪台渲染成空白 |
| 不得残留 `TAGMAP` | 必须为 0 | 旧数据段复活（会反向覆盖新标签） |
| 月份数 | `PILLS_BUDGET = 12` 提示线 | 月份导航需按年分组 |

`EMBEDDED` 采用**分层压缩**：`description` 只保留最近 `RECENT_DESC_DAYS = 60` 天
（因为只有 bento / featured 会显示描述，月历卡与时间线都不显示），
其余字段全量保留以保证档案在 `file://` 下仍可完整浏览。

> 教训来源：选题库.md 六天 125KB→257KB 无人发现；EMBEDDED 与 manifest 字段名不一致
> 导致 file:// 下描述全部静默丢失。**两个表示各写各的，靠人注意是注意不到的。**

## 五-C、字段来源与优先级（避免"改了没生效"）

| 字段 | 权威来源 | 优先级 |
|---|---|---|
| **标题** | 作品自身 `<title>` | `enrich.title`（人工显式覆盖）> HTML `<title>` > 旧 manifest |
| **类型** | **目录**（`research/` 或 `creative/`） | `enrich.type` > 目录结构/缩略图名 > 旧 manifest |
| 日期 | 路径首段 `YYYY-MM-DD`，其次文件名前缀 | — |
| 描述 | `enrich.description`（人工）> 旧 manifest | 空则自动补草稿（`fill_descriptions.py`） |
| 标签 | `enrich.highlights` | 首页筛选按钮只列出现 ≥2 次的标签 |
| 缩略图 | 磁盘真实文件 | 优先 `.webp`，回退 `.png` |

> ⚠️ **标题以作品 `<title>` 为准**（2026-10-22 修正）。此前是"旧 manifest 优先"，
> 导致 HTML 改了标题而首页仍是旧的 —— 实测 6 例不一致，其中 `musk-trillion-path`
> 的旧标题还丢了「的12年狂飙」这段信息。生成器现在会在两者不同时输出一行提示，
> 所以**改作品 `<title>` 再跑一次 autopublish 即可同步首页**；
> 若确实要覆盖，写 `enrich.json` 的 `title` 字段。

## 五-B4、首页封面（2026-10-26 定稿）

首页是**两层**：第一屏封面（海报），第二屏柜子（工具）。

**封面的立意**：不展示「这里有 104 个作品」，而是展示**一条断言凭什么可信**。
封面 = 一张**证据单**，铺在满屏的账目之上：

```
断言证据单 · VERIFICATION SLIP     № 20261024-01   第 6 期
  约15,000人                          ╭─────────╮
  美光在台员工总数                     │ ✓ 引用已 │   ← 印章压在单据上
                                      │ 逐字回查 │
  原文    美光在台员工约15,000人         ╰─────────╯
  作品    11个人的24小时——美光桃园罢工…（可点）
  日期    2026-10-24
  追踪线  就业与劳动
```

层级（底→顶）：账簿墙（1001 条断言铺满全屏、压暗）→ 证据单（实体表面+投影+
流水号）→ 数值（10vw）→ 印章（旋转 -13°）。

断言**自动轮换**：池子是**全档案最近**的 14 条已验证断言（优先带引证出处的），
每 7 秒交叉淡入，可点「换一条」，悬停暂停。新作品的断言会自动出现在封面上。

要点：
- 逐字引用可回查 —— 出处只在**真有引证**时出现，不放半可靠的行
- 轮换池用**确定性哈希**取金色高亮（不能用 random —— 那会让每次刷新封面不同，
  且 HTTP 与 file:// 两条路径给出不同封面）
- 全幅出血，无页边距

## 五-B5、持续跟踪指标（断言序列的前置条件 · 2026-10-26）

「断言序列」（把同一指标跨作品连成时间线）**不是靠界面功能长出来的**，
是靠**标签一致**长出来的。

实测：当前 1032 条断言里，能自动聚成序列的只有 **6 组**（跨≥2 件作品且跨≥2 个日期）。
差的不是界面，是同一指标被写成了不同标签：

```
SWE-Bench Pro  /  SWE-Bench Pro V2  /  SWE-Bench Pro V2得分    ← 三个不同的标签
集装箱运费    /  集装箱运费（亚欧）                            ← 两个
中国开源模型下载全球占比 / 中国开源模型全球下载份额            ← 两个
```

所以研究类模板里加了「持续跟踪指标」约定：跟踪团队之前也跟踪过的指标时，
**复用完全一致的标签**，不要加「（推算）」「得分」「V2」这类后缀（除非真是另一个口径）。
序列会随作品自然积累 —— 等攒够了，界面那一步是顺水推舟。

## 五-D3、作品页「档案条」（2026-10-26）

每件作品页顶部横一条暗色窄条，把这件作品的**归属**说清楚：

```
ZHINANG ARCHIVE / 2026-10-27 / 成本与普惠 / 25 件 / 2026-10 / 8 条已验证断言   [回到柜子]
```

为什么需要：106 件作品页风格各异（浅色/深色、Apple 风、档案卷宗…），
用同一条窄条统一框架 —— 一眼看出「哪天、哪条线、柜子第几格、几个断言」。
数据全部来自 `manifest.json`，**自动更新**；由 `add_backlink.py` 注入。

注入内容与返回链药丸（`showcase-backlink`，浮在左下角、明暗自适应）
是同一套工具的产物，`--remove` 可一并清除。

## 五-D、断言层（作品契约 · 2026-10-26 新增）

展厅的"卷宗"区块展示的是**已验证断言**：每条断言的引用都逐字回查过原文。
这条链路是全自动的，**没有人工审核** —— 质量由机器闸门保证。

### 为什么要它

过去 104 件作品各自手写 HTML，累计出 **147 种**统计块 class 名，
导致任何自动抽取都不可靠。断言层不是"给页面加个数字显示"，
而是给作品定一份**封闭契约**，让后续作品一出生就可被机器解析。

### 三道闸门（`tools/claim_gate.py`）

| 闸门 | 判定 | 不通过怎么办 |
|---|---|---|
| G1 逐字引用 | quote 归一化后必须是原文子串 | 拒绝该条，进 L1 |
| G2 语义可疑 | 标签不能像句子/片段/代码/出处注记 | 拒绝该条，进 L1 |
| G3 每次重校验 | 每次重建都重跑；源文件改过 → 旧 quote 失效 | 自动降级 + 记 changelog |

分层：**L0** 已验证（进卷宗/断言序列/对账）· **L1** 待处理（不进任何视图）
· **L2** 无结构作品（只留档案页，永不伪造）。

⚠️ 边界：quote 只能证明「这句话在原文里」，**不能**证明「这句话支持那个断言」。
所以自动断言只覆盖**机械可配对**的关系（数值 + 邻近标签）。
解释性/因果性判断留在正文由人读，不伪装成"团队历史判断"。

### 新作品怎么做（按类型分流）

#### 研究类 —— 走模板

从 `shared/showcase/templates/work.html`（「档案卷宗」视觉）起步：

1. **只用封闭语义词汇表**（不要自创 class 名）：
   `.metrics>.metric>(.metric-value/.metric-label/.metric-source)`、
   `.verdict`、`.timeline>.timeline-item`、`.evidence>.evidence-item`
2. **声明断言**：页面底部 `<script type="application/json" id="claims">`
   ```json
   [{"value":"-16%","label":"布伦特原油两周跌幅","quote":"布伦特原油两周跌幅 -16%"}]
   ```
   `quote` 必须在本文件里**逐字存在**；3~8 条为宜；
   **解释性判断不要写成断言**
3. **声明追踪线**：`<meta name="showcase-beat" content="封闭集内的追踪线名">`
   （13 条封闭集，模板注释里已内联）
4. 交付后不需要手工改 manifest / index.html / enrich.json ——
   `autopublish` 阶段 5.5 会自动注入返回链并回填断言

作品自带声明**同样要过闸门**（声明不是特权）。

#### 创意类 —— 不用模板

视觉 / 叙事 / 交互形式**完全自由**，不套研究类模板（那是刻意的：
创意要每件长成自己的样子）。但两类都必须声明 claims + 追踪线 ——
那两段不进入视觉层，只是让作品能进卷宗。

硬约束见 `templates/creative-brief.md`：单文件、**零远程依赖**
（历史事故：15 件作品因 CDN 不可达而图表渲染成空框）、
对比度 ≥4.5:1、响应式、`prefers-reduced-motion`。

### 自托管字体

`assets/vendor/fonts/`：
- `newsreader-latin-300-600.woff2`（132KB）—— 数字与拉丁文
- `noto-serif-sc/`（30 片，844KB）—— 中文衬线，按字频切片

取自 `fonts.loli.net` 镜像（**国内可达**）。生僻字回落系统字体。
作品页离线可用，不依赖 Google Fonts。

### 命令

```bash
python3 tools/claim_gate.py --scan        # 体检：L0/L1/L2 分布
python3 tools/claim_gate.py --backfill    # 重校验 + 回填（幂等）
python3 tools/claim_gate.py --verify      # 逐条重校验既有断言（漂移检测）
python3 tools/claim_gate.py --test        # 自测
```

### 当前基线

```
L0 已验证断言 1014 条 · 覆盖 92/104 件（88%）· 待处理 402 · 无结构 12
```

基线存在 `tools/.claim_state.json`；断言总数较基线跌超 20%
或抽取拒绝率突增逾 15pp → `--check` 判 FAIL（抽取回归）。

## 六、禁止事项（都是历史事故换来的）

- ❌ **手工编辑 `manifest.json` / `index.html`** —— 两者都是生成物
- ❌ **使用 `update_showcase.sh`** —— 生成的是占位卡片（正文写着"此处应替换为完整的HTML报告内容"），
  已归档至 `_archive/deprecated/`
- ❌ 作品放 `showcase/` 根目录或日期目录根下
- ❌ 过程材料（md / 预览图 / `.partN.html`）与作品混放
- ❌ 手工编辑 enrich.json 里的 claims（那是 claim_gate 的产物）
- ❌ 给**研究类**作品自创统计块 class 名（用模板的封闭词汇表）
- ❌ 给**创意类**作品套研究类模板（创意走 `creative-brief.md`）
- ❌ 引用 Google Fonts / jsDelivr 等远程资源（国内不可达 → 图表变空框）
- ❌ 伪造 quote 凑断言数（闸门会拒，且拒的理由会记入 changelog）
- ❌ 在提示词或文档里重复抄写截图参数 —— 以 `gen_thumb.py` 为准

## 七、校验

```bash
cd /app/working/shared/showcase
python3 tools/build_manifest.py --check   # 期望：[check] manifest 与磁盘 一致
```

**十项硬校验**（由 autopublish 阶段 7 执行）：
计数一致 / 缺文件 0 / 缺缩略图 0 / 缺标签 0 / 标签总数未下降 / 无标签丢失 /
快照契约 / 元数据与类型一致 / **返回链齐全** / **断言引用无失效**

断言层另有三条不变量（`--check` 内置）：
引用失效 > 0 / 断言总数较基线跌 > 20% / 抽取拒绝率较基线突增 > 15pp

## 五-E、设计质量棘轮（`tools/design_scan.py`）

规则14 要求「设计类工作交付前跑 detect + polish」，但**没有任何机器闸门强制它** ——
全靠 Agent 自报。结果是存量积压：全馆 116 件作品、**4907 条 findings、111 件有**。

一次性清完不现实：每件都是独立的视觉世界，机器批量改色会毁掉作者的世界。
所以走**棘轮**路线（与既有「标签总数不得下降」同一思路）：

| 机制 | 做法 |
|---|---|
| 基线 | `tools/design_baseline.json` 记录当前每条规则的 findings 数 |
| 判定 | 全量扫描后比对，**任何规则条数上升 → 退出码 1（回归）**；下降 → 通过 |
| 收紧 | 修完一批后跑 `--update-baseline`，棘轮随之更紧 |
| 周期 | 守护进程 `auto_maintain.py` 每 12 轮（约 6 小时）跑一次全量比对 |

```bash
python3 tools/design_scan.py --scope all                          # 全量 + 棘轮比对
python3 tools/design_scan.py --scope all --update-baseline        # 修完后收紧基线
python3 tools/design_scan.py --scope recent:30                    # 只扫近 30 天改动的作品
python3 tools/design_scan.py --scope file:<路径>                   # 单件交付前自检
```

**当前积压分布**（2026-11-03 基线）：

| 类别 | 条数 | 说明 |
|---|---|---|
| low-contrast | 2961 | 其中 **757 条低于 3:1**（连大字号都不达标）· 160 条低于 2:1（几乎不可读） |
| undersized-ui-text | 487 | UI 文字偏小 |
| side-tab | 308 | 卡片单侧粗色边框（AI slop 特征） |
| gradient-text / dark-glow | 189 / 168 | 渐变文字 / 发光阴影 |
| skipped-heading / cramped-padding / tiny-text | 117 / 99 / 96 | 标题层级跳跃 / 间距过挤 / 字号过小 |
| kicker-above-heading | 65 | 标题上方的眉标（craft-floor 明令禁止项） |
| numbered-section-labels | 55 | 章节序号（craft-floor 禁止项） |
| border-accent-on-rounded | 38 | 圆角卡片上的粗色边框（禁止项） |
| ai-color-palette / pulsing-dot / bounce-easing / icon-tile-stack | 31 / 37 / 16 / 42 | 调色板 / 呼吸点 / 弹跳缓动 / 图标堆 |

**处置原则**：棘轮只保证「不继续恶化」。清积压要**按作品批次**做（每件单独 polish，
尊重它自己的视觉世界），一次一批、每批收紧基线；不做全库批量改色。
