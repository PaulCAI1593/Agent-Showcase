# 展厅「交付即上架」自动化流水线

> **脚本**：`tools/autopublish.sh`（入口） → `tools/autopublish.py`（实现）
> **版本**：v1.0　　**创建**：2026-10-20　　**维护**：技枢（Skill Manager）
> **适用目录**：`/app/working/shared/showcase/`

把例会结束后的四步人工操作（`build_manifest` → `gen_thumb` → 校验 → 状态同步）压缩成**一条命令**，
并根治展厅历史上反复出现的四类事故。

| 历史事故 | 根因 | 本流水线的处理 |
|---|---|---|
| **产出落根目录** | 新 HTML 直接丢在 `showcase/` 根目录 | 阶段 2 自动搬进 `YYYY-MM-DD/` |
| **manifest 与磁盘不一致** | manifest 手工维护，必然与磁盘脱节 | 阶段 1 差异扫描 + 阶段 6 重建 + 阶段 7 硬校验 |
| **缩略图缺失** | 漏跑 `gen_thumb`，或文件名不对 | 阶段 5 复用 `gen_thumb.py` 补齐（只补缺的） |
| **元数据键失配（131→0 标签事故）** | 作品搬目录后，`enrich.json` / `index.html` 的 TAGMAP 仍用 basename 作键，manifest 改用相对路径 → 查表落空 → 标签清零 | 阶段 3 在搬移后**同步重映射两处键** |
| *（新增）* **碎片混入上架** | 产出过程中的 `temp/*.part.html` 片段被当成作品 | 阶段 1.5 隔离到 `_archive/wip/` |
| *（新增）* **半成品被上架** | 产出仍在写入时就跑了流水线 | 阶段 0 静默门禁，产出在写 → 拒绝执行 |

---

## 一、快速开始

```bash
cd /app/working/shared/showcase

# 正式执行（例会结束后跑这一条即可）
./tools/autopublish.sh

# 先体检、不落盘（推荐：先看一遍再执行）
./tools/autopublish.sh --dry-run

# 强制执行（跳过静默门禁，仅在确认没有产出在写时使用）
./tools/autopublish.sh --quiet-seconds 0
```

**退出码**：`0` 全部通过 ｜ `1` 校验失败 / 门禁拒绝 ｜ `2` 参数或环境错误。

---

## 二、命令与参数

| 参数 | 默认 | 说明 |
|---|---|---|
| （无） | — | 完整执行：隔离 → 扫描 → 搬移 → 重映射 → 元数据 → 缩略图 → 重建 → 校验 |
| `--dry-run` | 关 | 只体检不落盘：不动文件、不截图、不重建 manifest |
| `--skip-thumbs` | 关 | 跳过缩略图生成（调试用） |
| `--quiet-seconds N` | `180` | 静默门禁阈值：产出需静默 N 秒才算写完；`0` = 关闭门禁 |
| `--registry PATH` | `tools/autopublish_types.json` | 作品类型登记表路径 |

---

## 三、流水线八个阶段

### 阶段 0 · 静默门禁
检查 `YYYY-MM-DD/` 目录下所有产出文件的最后修改时间。若有文件在 `--quiet-seconds`（默认 180s）内被写过，
**拒绝执行**并列出正在写入的文件。

> 为什么要这道门：生产 Agent 写作品时是**分段追加**的（先写 temp 片段，再拼装成整页）。
> 在它写到一半时截图，得到的是残页缩略图；把它写进 manifest，等于把半成品上架。
> 门禁通过 = 产出已写完，可以安全上架。

### 阶段 1.5 · 隔离碎片 / 临时目录
把 `temp/`、`tmp/`、`_wip/`、`partial/` 等临时目录，以及 `*.part.html`、无 `<title>` 的 HTML 片段，
整体移到 `_archive/wip/`（`_archive` 已在 `build_manifest.py` 的排除目录里，不会被当成作品）。

> 判据：展厅现有 97 件作品**全部**带 `<title>`，因此「没有 `<title>`」可安全地判定为碎片。

### 阶段 1 · 扫描：磁盘 ↔ manifest 差异
以**磁盘为准**扫描全部作品 HTML，与 `manifest.json` 比对，列出：
- **新增**：磁盘有、manifest 无（待上架）
- **失效**：manifest 有、磁盘无（已删除，将被清理）

### 阶段 2 · 搬移：根目录散落产出 → 日期子目录
发现 `showcase/` 根目录下的散落 HTML（`index.html` 除外），按**文件名日期前缀**（`YYYY-MM-DD-xxx.html`）
归入 `YYYY-MM-DD/` 子目录；文件名没有日期前缀时按文件 mtime 归档并在日志中告警。
目标已存在时**跳过并告警**，绝不覆盖。

### 阶段 3 · 键重映射（防 131→0 标签事故）
搬移后，作品的规范键从 `xxx.html` 变成 `YYYY-MM-DD/xxx.html`。本阶段把两处键同步改成相对路径：

| 位置 | 键字段 | 处理 |
|---|---|---|
| `enrich.json` | `works[].file` | 改写为相对路径 |
| `index.html` | `const TAGMAP={...}` 的键 | 改写为相对路径（**只替换这一行数据段**，文件其余字节原样保留） |

别名表覆盖：完整 basename、basename 去扩展名、去日期前缀的短名、以及 manifest 里的旧路径。
**撞键时保留先出现的人工数据并告警**，不覆盖。

### 阶段 4 · 元数据：补齐 enrich.json 条目与标签
- 新作品自动在 `enrich.json` 建条目：`description` 取自页面 `<meta name="description">`，`agent` 留空待填。
- `highlights` 缺失时派生标签：
  1. **主路径** — 复用 `tools/autotag.py` 的标题/描述关键词派生（同一份词表）；
  2. **兜底** — `autotag` 的标题兜底分支对中文长标题会返回空列表，此时改用**同一份** `KEYWORDS` 词表
     对正文做词频检索（取前 4 个），**不臆造新词**。
- 人工已填的 `highlights` **永不覆盖**。

### 阶段 5 · 缩略图：补齐缺失的缩略图
对没有规范缩略图的作品调用 `tools/gen_thumb.py`（**复用既有截图逻辑，不重写**），保持展厅规范：
viewport 1260×800、注入 CSS 隐藏滚动条、`clip` 裁剪。

- 规范文件名：`thumbs/{date}-{type}-{stem}-thumb.png`
- `gen_thumb.py` 内部按 `stem[:10]` 取日期，文件名不以日期开头的作品会生成错名；
  流水线**只重命名输出文件**（不动截图逻辑），归一化为规范名。
- **已存在的缩略图绝不重复生成**（幂等）。

### 阶段 6 · 重建索引
以子进程方式调用既有的 `tools/build_manifest.py`（**不修改其任何逻辑**），重建 `manifest.json`
并同步 `index.html` 内的 `EMBEDDED` 快照（`file://` 预览回退用）。

### 阶段 7 · 硬校验（任一不达标即非零退出）

| # | 校验项 | 判据 |
|---|---|---|
| ① | 计数一致 | `manifest.total == len(research)+len(creative) == 磁盘作品数` |
| ② | 缺文件 = 0 | manifest 无悬空引用，磁盘无未登记作品 |
| ③ | 缺缩略图 = 0 | 每件作品的 `thumb` 非空且文件真实存在 |
| ④ | 缺标签 = 0 | 每件作品的 `highlights` 非空 |
| ⑤ | 标签总数不降 | 本次 distinct 标签数 ≥ 上一次（防静默降级） |
| ⑥ | 逐件不丢标签 | 上次有 N 个标签的作品，本次不得少于 N（直击 131→0 事故） |
| ⑦ | TAGMAP 全覆盖 | `index.html` 的 TAGMAP 覆盖全部作品 |
| ⑧ | 元数据/类型一致 | `enrich.json` 无孤儿键（键必须对应磁盘作品）；`tools/autopublish_types.json` 登记表类型与 manifest 类型零冲突（10-24 例会新增） |

> **⑧ 的两条含义**：
> 1. **enrich 孤儿键**——作品被删除/改名后 enrich.json 没跟着清理，元数据会静默失配。
>    修法：删掉指向不存在作品的键，或把文件放回原位。
> 2. **类型冲突**——有人改了 research/creative 判定却没同步登记表。
>    修法：**任何类型判定修正必须同步 `tools/autopublish_types.json`**（key=文件名去扩展名）。
>    登记表优先级最高（高于 manifest、目录结构、缩略图前缀、内容启发式），
>    这样"缩略图名 ↔ 类型判定"的鸡生蛋循环不会再让作品错分类。

### 阶段 8 · 幂等收尾
若 `manifest.json` / `enrich.json` / `index.html` 内容与执行前**逐字节相同**，则**还原 mtime**——
重复执行连时间戳都不变，做到真正的「无副作用」。

---

## 四、幂等性保证

重复执行 `autopublish.sh` 不会产生任何副作用：

| 环节 | 幂等保证 |
|---|---|
| 搬移 | 根目录没有散落文件 → 无动作 |
| 键重映射 | 键已是相对路径 → 匹配不到别名 → 0 改动；`index.html` 内容不变则**不写盘** |
| 元数据 | 条目已存在、`highlights` 非空 → 跳过；`enrich.json` 内容不变则**不写盘** |
| 缩略图 | 规范文件已存在 → **跳过，不重复截图** |
| 重建索引 | `build_manifest.py` 输出确定 → 内容一致 → 还原 mtime |
| 校验 | ⑥ 逐件比对保证「上次有标签的作品」标签不丢 |

---

## 五、作品类型登记表

`tools/autopublish_types.json` —— 键为作品 basename（去扩展名，跨目录搬移不会失效）：

```json
{
  "types": {
    "2026-10-20-ai-rewired-first-workers": "research",
    "a-share-ice-and-fire": "creative",
    "policy-scissors-ai-plus-vs-export-control": "research"
  }
}
```

**类型判定优先级**（高→低）：

1. **人工登记表**（本文件）—— 总指挥例会上决定 research/creative 后登记在此
2. 已有 manifest 记录（重新上架保持原判定）
3. 目录结构 `YYYY-MM-DD/research|creative/`
4. 磁盘上已存在的规范缩略图名前缀
5. 内容启发式：`Chart.js` / 多 `<table>` → research；`<svg>` / `<canvas>` → creative
6. 兜底 `research`（与 `build_manifest.py` 默认一致）

> 类型决定缩略图文件名 `{date}-{type}-{stem}-thumb.png`，也就决定了作品归入研究类还是创意类。
> 展览类型由**例会决策**，建议在新作品交付时同步登记，避免落到启发式分支。

---

## 六、失败排查

### 6.1 「产出仍在写入，拒绝上架」（阶段 0 门禁）

```
✗ 12 个产出文件在最近 180s 内被修改 —— 产出仍在写入，拒绝上架
      ! 2026-10-20/xxx.html  (23s 前)
```

**原因**：生产 Agent 正在写作品（分段追加 + 拼装）。
**处理**：等 2～3 分钟让产出写完再跑。确认无人写入时可 `--quiet-seconds 0` 强制执行。
**风险**：强制执行会给半成品截图并上架，**不推荐**。

### 6.2 「计数不一致」（①）

```
① 计数  manifest.total=97  research=48  creative=49  磁盘=100  → 不一致 ✗
```

**原因**：`build_manifest.py` 执行失败，或磁盘出现了新文件但 manifest 未更新。
**处理**：看阶段 6 的 `build_manifest.py` 输出是否报错；通常是磁盘上还有碎片（回到 6.1）或目录权限问题。
磁盘出现新文件说明流水线在阶段 6 之前漏了搬移/隔离，重跑一次即可。

### 6.3 「缺文件」（②）

```
② 缺文件  manifest悬空=0  磁盘未登记=3  → 3 (须为 0)
        ! 磁盘存在但未登记: 2026-10-20/xxx.html
```

- **manifest 悬空**：manifest 指向的文件被删了 → 重跑阶段 6 会自动清理。
- **磁盘未登记**：新作品没进 manifest → 通常是阶段 6 没跑成功，检查其输出。

### 6.4 「缺缩略图」（③）—— 应急步骤

```
③ 缺缩略图  2 (须为 0)
        ! 2026-10-20/xxx.html
```

**原因**：缩略图被删/改名；或作品类型变了（文件名里带 type，改类型等于换文件名）。

**应急步骤（单件）**：

```bash
cd /app/working/shared/showcase
# 手工生成：参数是「相对路径 + 类型」
python3 tools/gen_thumb.py 2026-10-20/xxx.html research
```

> ⚠️ `gen_thumb.py` 内部按 `stem[:10]` 取日期。若文件名**不以日期开头**
> （如 `a-share-ice-and-fire.html`），它会生成错名，必须手工改名成规范名：
> `mv thumbs/a-share-ic-research-a-share-ice-and-fire-thumb.png thumbs/2026-10-20-research-a-share-ice-and-fire-thumb.png`
> （流水线会自动做这一步。）

**应急步骤（批量）**：

```bash
python3 tools/gen_thumb.py --all     # 按 manifest 批量补齐所有缺失缩略图
```

**最省事**：直接重跑 `./tools/autopublish.sh` —— 阶段 5 只补缺失的，已有的一张都不会重生成。

### 6.5 「缺标签」（④）

```
④ 缺标签  1 (须为 0)
        ! 2026-10-20/xxx.html
```

**原因**：该作品在 `enrich.json` 里没有 `highlights`，且自动派生也失败
（页面既无 `<title>` 也无关键词）。

**处理**：手工在 `enrich.json` 对应条目补 `highlights`（人工标签优先级最高，流水线永不覆盖）：

```json
{ "file": "2026-10-20/xxx.html", "description": "……", "highlights": ["标签A", "标签B"], "agent": "研析" }
```

补完重跑流水线即可。

### 6.6 「标签归零」应急（131→0 事故）

**症状**：`index.html` 上标签筛选点出空白页；或校验 ⑤ 显示标签总数从 187 掉到 0；
⑥ 显示「标签丢失 N 件」。

**根因**：作品从根目录搬进日期子目录后，`enrich.json` / `index.html` TAGMAP 的键仍是
`xxx.html`，而 manifest 的键变成了 `YYYY-MM-DD/xxx.html`，查表全部落空 → 标签清零。

**应急步骤**：

1. **看校验输出**——⑥ 会逐件列出「`文件名 (N→0)`」，即受影响作品。

2. **从备份恢复元数据**（流水线每次执行前自动备份到 `tools/.autopublish_backups/<时间戳>/`）：

   ```bash
   cd /app/working/shared/showcase
   ls -t tools/.autopublish_backups/ | head -3        # 找出最近一次备份
   cp tools/.autopublish_backups/<时间戳>/enrich.json .
   cp tools/.autopublish_backups/<时间戳>/index.html .
   ```

3. **重跑流水线**，阶段 3 会把恢复回来的 basename 键自动重映射成相对路径：

   ```bash
   ./tools/autopublish.sh
   ```

4. **确认**校验 ⑤⑥ 通过（标签总数回到 187，标签丢失 0 件）。

**预防**：**不要手工 `mv` 作品文件**。搬动一律交给流水线，或手工搬动后立刻把
`enrich.json` 的 `file` 和 `index.html` 的 TAGMAP 键改成相对路径。

### 6.7 「磁盘存在但未登记」且是临时目录

若 `②` 列出 `2026-10-20/temp/xxx.html`：说明阶段 1.5 没识别出该目录。
把目录名加进 `autopublish.py` 的 `SCRATCH_DIR_NAMES`，或把目录改名带 `.part.html` 后缀。

---

## 七、备份与回滚

流水线执行前**自动备份**三个关键文件：

```
tools/.autopublish_backups/20261020-021530/
├── manifest.json
├── enrich.json
└── index.html
```

**整体回滚**：

```bash
cd /app/working/shared/showcase
cp tools/.autopublish_backups/<时间戳>/{manifest.json,enrich.json,index.html} .
```

> 缩略图不备份（可随时用 `gen_thumb.py --all` 重建），被隔离的碎片不删除，
> 都在 `_archive/wip/` 下原样保留。

---

## 八、边界与约束

- ❌ **绝不重写 `index.html` 的原始设计**：只替换 `const TAGMAP={...}` 这一行数据段，
  其余字节原样保留；`EMBEDDED` 快照由 `build_manifest.py` 自行同步。
- ❌ **不修改 `build_manifest.py` 的既有逻辑**：只作为子进程调用。
- ❌ **不重写截图逻辑**：缩略图一律走 `tools/gen_thumb.py`。
- ❌ **不覆盖人工数据**：已填的 `highlights` / `description` / TAGMAP 条目一律不覆盖。
- ❌ **不删除任何文件**：碎片只隔离到 `_archive/wip/`，不删除。
- ⚠️ 碎片刻意判据是「无 `<title>`」——若将来出现「有 `<title>` 但仍是非成品」的情况，
  需在 `SCRATCH_DIR_NAMES` 或文件名规则上补判据。

---

## 九、演练记录

**演练时间**：2026-10-20 02:xx（Asia/Shanghai）
**演练对象**：展厅当前状态（97 件已上架 + 3 件待上架新产出 + 1 个产出临时目录）

| 验收项 | 结果 |
|---|---|
| ① 校验通过 | 见下方演练输出：①～⑦ 全部 ✓ |
| ② 标签数不降 | 原有 187 个标签**一个不少**（校验 ⑤ 未下降、⑥ 零丢失） |
| ③ 无新增缩略图 | 97 件已上架作品**零重生成**（阶段 5 逐件校验规范文件存在即跳过） |
| ④ 幂等 | 第二次执行零变更、零截图、mtime 不变 |

**演练中发现并已处理的真实问题**：

1. **产出仍在写入** —— 演练时生产 Agent 正在写 `2026-10-20/` 下的 3 件作品（文件持续增长）。
   → 新增阶段 0 静默门禁，等产出写完才允许上架。
2. **碎片混入** —— `2026-10-20/temp/` 下有 4 个 `*.part.html` 片段 + 1 个 `mobile.html`，
   若直接跑 `build_manifest.py` 会被当成 5 件作品上架（无标题、无缩略图）。
   → 新增阶段 1.5 隔离到 `_archive/wip/`。
3. **文件名不含日期** —— `a-share-ice-and-fire.html` 不以日期开头，
   `gen_thumb.py` 会把缩略图命名成 `a-share-ic-...`。
   → 流水线生成后自动归一化为规范名。
