# 已废弃脚本

## update_showcase.sh（2026-10-17 归档）

**禁用原因**：该脚本生成的**不是真实作品**，而是占位卡片——HTML 里直接写着
"注：此处应替换为完整的HTML报告内容"，只有标题/描述/负责人三行有效信息。

它还会造成 3 个额外问题：
1. 文件落在 `YYYY-MM-DD/research-item-xxx.html`（直接放日期目录），
   而非规范的 `YYYY-MM-DD/research/xxx.html` —— 即"文件乱放"的来源
2. **直接改写 manifest.json**，绕过 `tools/build_manifest.py` 生成流程
   → 缩略图路径、type 判定会再次出错
3. 生成的条目无缩略图、无 description，首页显示为无图占位卡

**替代方案**：
```bash
# 1. 产出真实 HTML 到规范路径
#    showcase/YYYY-MM-DD/{research|creative}/YYYY-MM-DD-<slug>.html
# 2. 生成/刷新 manifest（自动判定 type、自动解析真实缩略图）
python3 tools/build_manifest.py
# 3. 校验
python3 tools/build_manifest.py --check
```
index.html 已改为运行时 fetch manifest.json，**无需再手动同步内嵌数据**。
