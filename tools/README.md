# tools/ — 流水线脚本清单

全部脚本以 **仓库根目录**为基准工作（`ROOT = dirname(dirname(__file__))`），直接跑即可，无需安装依赖（只用 Python 标准库 + playwright）。

## 核心流水线（日常只用这些）

| 脚本 | 作用 |
|---|---|
| `autopublish.sh` / `autopublish.py` | **交付即上架全流程**：注入返回链 → 回填断言 → 重建生成物 → 十项硬校验 |
| `build_manifest.py` | 扫描磁盘重建 `manifest.json` / `index.html` 离线快照 / `enrich.json`；`--check` 只校验（不一致退出码 1） |
| `claim_gate.py` | **断言闸门**：G1 逐字引用 / G2 标签质量 / G3 漂移 / G4 自身计数；`--scan` 体检、`--backfill` 回填、`--verify` 重校验、`--test` 自测 |
| `inject_contracts.py` | 把已过闸门的断言与追踪线搬进缺声明的作品（只搬运不发明） |
| `reorganize.py` | 归一目录：作品 → `works/YYYY-MM-DD/<type>/`、过程材料 → 当天 `notes/`；含路径键重映射 |
| `add_backlink.py` | 给作品页注入「返回展厅」与档案条（幂等） |
| `fill_descriptions.py` | 从作品正文提取 `description` 补进 `enrich.json`（**只填空、不覆盖人工已写的**） |
| `autotag.py` | 为**缺** `highlights` 的作品从标题派生标签（已有标签一律不动） |
| `audit_pages.py` | 作品页运行时巡检：真实加载 + 抓 console 错误 / 资源 404 / 空白页 |
| `design_scan.py` | **设计质量棘轮**：全量 `impeccable detect` 与基线比对，任何规则条数上升即判回归 |
| `gen_thumb.py` / `make_thumbs_webp.py` | 截图生成缩略图（viewport 1260）/ PNG → WebP |
| `vendor_assets.py` | 作品引用的远程 JS 本地化（离线可用 + CDN 兜底） |
| `serve.py` | 预览服务器（默认只监听 127.0.0.1），屏蔽 `_private` `_archive` `tools` `templates` 与嵌套的 `notes/` |

## 实验性工具（一次性修复脚本，非流水线组成部分）

以下脚本是某次批量修复的产物，**默认不启用**，保留作为取证与修法参考：

| 脚本 | 状态 |
|---|---|
| `fix_contrast.py` | 对比度机械修复（颜色级），带终局闸门 |
| `fix_contrast_dom.py` | 页内 DOM 取证修对比度（伪元素 / 渐变文字 / 阴影） |
| `fix_design_dom.py` | 页内计算样式修四类装饰问题 |
| `fix_design_rules.py` | 静态修字号 / 渐变文字 / 灰字染底色相 / 网格底纹 / bounce 关键帧 |
| `fix_heading_levels.py` | 标题层级跳跃（**保视觉未成立，已标注默认不启用**） |
| `break_ui_check.py` | 首页极端数据压测（最坏数据 + 真实浏览器 + 三档视口） |
| `contrast_forensics.py` | 对比度取证分析 |

这些脚本都遵循同一套安全约定：逐件终局判据 + 变差整件回退 + 复验超时不写盘。

## 依赖

- Python 3.11+（标准库）
- `playwright`（仅 `audit_pages.py` 与实验性脚本需要）：`pip install playwright && playwright install chromium`
- `impeccable` 技能（仅 `design_scan.py` 与实验性脚本需要）：`impeccable detect`
