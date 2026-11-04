# 贡献指南

## 加一篇作品

```bash
# 1) 放到规范路径（类型由目录表达，文件名带日期前缀）
#    works/2026-11-05/research/2026-11-05-my-topic.html
#    works/2026-11-05/creative/2026-11-05-my-topic.html

# 2) 过程材料（口径台账 / 交付报告 / 预览图）一律进当天的 notes/
#    works/2026-11-05/notes/

# 3) 一条命令上架（含十项硬校验）
./tools/autopublish.sh
```

## 硬性要求

| 要求 | 说明 |
|---|---|
| **路径** | `works/YYYY-MM-DD/{research\|creative}/YYYY-MM-DD-<slug>.html` |
| **断言声明** | 页面底部 `<script type="application/json" id="claims">`，每条含 `value` / `label` / `quote`；`quote` 必须能在正文里逐字找到；3~8 条为宜 |
| **追踪线声明** | `<head>` 内 `<meta name="showcase-beat" content="追踪线名">`，取自 13 条封闭集，不新增 |
| **研究类** | 从 `templates/work.html` 起步，只用封闭语义词汇表：`.metrics>.metric>(.metric-value/.metric-label/.metric-source)`、`.verdict`、`.timeline>.timeline-item`、`.evidence>.evidence-item` |
| **创意类** | 不用研究类模板；视觉自由，但同样要有两段声明；须满足 `templates/creative-brief.md` 的十项硬约束（单文件 / 零远程依赖 / 对比度 ≥4.5:1 / 响应式 / 尊重 prefers-reduced-motion） |
| **描述与标签** | 在 `enrich.json` 写 `description` 与 `highlights`（生成器只补空、不覆盖人工内容） |
| **署名** | `enrich.json` 的 `agent` 字段填负责 Agent（缺失会让首页「谁在主责」矩阵出现未署名行） |

## 交付前自检

```bash
python3 tools/claim_gate.py --scan       # 断言层体检
python3 tools/audit_pages.py <文件>      # 真实加载 + 抓运行时错误
python3 tools/build_manifest.py --check  # manifest 与磁盘一致
./tools/autopublish.sh                   # 十项硬校验
python3 tools/design_scan.py --scope all # 设计棘轮：任何规则条数上升即回归
```

最后一条尤其重要：`design_scan.py` 是**棘轮**——它记录了当前每条设计规则的 findings 数，
任何一条上升都会判失败。只许降不许升，修一批紧一档。

## 常见坑（都是已发生过的）

- 断言的 `quote` 必须是**整段连续原文**，改了标点或中间插字就失效（G1）
- 标签不能是句子，也不能带另一个金额（「B轮融资 $450M · 估值」会把两个值混成一条）
- 「N 条已验证断言」这类**页面自己的计数行**不是命题，会被 G4 拒收
- 作品页里的相对引用深度随目录变化（`works/YYYY-MM-DD/<type>/` 下恒为 3 层：`../../../`）
- 不要手工改 `manifest.json` / `index.html` / `enrich.json` —— 它们是生成物

细则见 [docs/OPERATIONS.md](docs/OPERATIONS.md)。
