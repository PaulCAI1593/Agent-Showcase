# 展厅设计规范参考

> **版本**: v2.0
> **更新**: 2026-06-11
> **用途**: 所有展厅详情页HTML报告的设计参考
> **核心变化**: ⭐ 明确研究类与创意类的本质区别

---

## ⭐ 核心要求

**所有展厅详情页HTML报告的设计风格，必须参考设计系统文件库：**

```
/app/working/shared/design/design-md/
```

该目录包含 **50+ 品牌设计系统**，每个品牌文件夹下有：
- `DESIGN.md` — 完整设计规范（色彩/排版/组件/布局）
- `preview.html` — 浅色预览
- `preview-dark.html` — 深色预览

---

## 🎯 研究类 vs 创意类：本质区别

### ⭐ 研究类（Research）= 深度 + 数据 + 可视化

**定位**：深度研究报告，但必须有**炫酷的图表和特效**

| 维度 | 要求 | 示例 |
|------|------|------|
| **内容深度** | 严谨的分析、数据支撑、逻辑推演 | 行业分析、技术解读、市场研究 |
| **数据可视化** | ⭐ 必须有 Chart.js / D3.js 图表 | 折线图、柱状图、雷达图、热力图 |
| **动画特效** | ⭐ 滚动触发、数字跳动、渐入效果 | IntersectionObserver + CSS动画 |
| **交互元素** | ⭐ 可交互的数据探索 | Tab切换、筛选、展开/折叠 |
| **排版风格** | 专业报告风格（参考 stripe/linear/vercel） | 清晰层级、数据卡片、引用块 |
| **信息密度** | 高密度但有组织 | 表格、列表、多栏布局 |

**研究类必备元素清单**：
```
✅ Hero区（标题+关键指标）
✅ 数据卡片（大数字+标签）
✅ Chart.js 图表（至少2种类型）
✅ 滚动动画（fadeUp/slideIn）
✅ 表格（对比数据）
✅ 引用块（关键洞察）
✅ 时间线（事件演进）
✅ 免责声明
```

### ⭐ 创意类（Creative）= 体验 + 视觉 + 交互

**定位**：视觉体验优先，像**艺术品/交互Demo/信息图**，不是研究报告

| 维度 | 要求 | 示例 |
|------|------|------|
| **视觉冲击** | ⭐ 第一眼就要震撼 | 全屏视觉、大胆配色、独特排版 |
| **创意表达** | ⭐ 不是"写报告"，而是"做作品" | 信息图、交互Demo、视觉叙事 |
| **交互体验** | ⭐ 用户可以"玩" | 鼠标追踪、点击探索、拖拽交互 |
| **动画特效** | ⭐ 电影级动效 | 粒子效果、视差滚动、形态变换 |
| **排版风格** | 打破常规（参考 figma/framer/pinterest） | 不对齐、重叠、出血、留白 |
| **叙事方式** | 视觉叙事 > 文字叙述 | 用图像/动画讲故事 |

**创意类必备元素清单**：
```
✅ 全屏视觉冲击（不是普通hero）
✅ 独特视觉语言（不是标准卡片布局）
✅ 交互元素（用户可以"玩"）
✅ 创意动画（不是简单fadeUp）
✅ 非传统排版（不对齐、重叠、出血）
✅ 情感共鸣（让观众有感觉）
✅ 可分享性（截图就想发朋友圈）
```

---

## 🎨 设计选择指南

### 研究类：按项目类型选择

| 项目类型 | 推荐品牌参考 | 理由 |
|----------|-------------|------|
| **AI研究报告** | claude / anthropic / openai | 人文+科技感 |
| **金融市场分析** | stripe / coinbase / revolut | 数据驱动+信任感 |
| **技术架构报告** | vercel / linear / cursor | 精确+现代 |
| **行业趋势报告** | apple / notion | 叙事+排版 |
| **产品对比矩阵** | airtable / clickhouse | 表格+数据密度 |
| **重大事件分析** | spacex / nvidia | 史诗感+冲击力 |
| **量化/数据分析** | stripe / clickhouse | 数据密度+精确 |

### 创意类：按创意类型选择

| 创意类型 | 推荐品牌参考 | 实现方式 |
|----------|-------------|----------|
| **传播型信息图** | figma / pinterest / miro | 大胆配色+非传统排版+数据可视化 |
| **工具型可视化** | vercel / raycast / cursor | 交互式Demo+实时数据+暗色科技 |
| **艺术型作品** | framer / webflow / runwayml | 沉浸式体验+粒子效果+视差滚动 |
| **交互型体验** | figma / linear / notion | 可点击探索+鼠标追踪+形态变换 |

---

## 🔧 创意类实现技巧

### 视觉冲击
```css
/* 全屏出血布局 */
.hero-creative {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* 大胆配色 */
:root {
  --accent-hot: #ff3366;
  --accent-cool: #00ccff;
  --gradient-fire: linear-gradient(135deg, #ff3366, #ff9933);
}
```

### 交互元素
```javascript
// 鼠标追踪效果
document.addEventListener('mousemove', (e) => {
  const cards = document.querySelectorAll('.interactive-card');
  cards.forEach(card => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;
    card.style.transform = `perspective(1000px) rotateY(${(x-0.5)*10}deg) rotateX(${(y-0.5)*-10}deg)`;
  });
});
```

### 创意动画
```css
/* 形态变换 */
@keyframes morph {
  0% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
  50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
  100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
}

/* 粒子背景 */
.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--accent-hot);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}
```

### 非传统排版
```css
/* 重叠布局 */
.overlap-section {
  position: relative;
}
.overlap-section::before {
  content: '';
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 120px;
  background: var(--accent-hot);
  opacity: 0.1;
  filter: blur(40px);
}
```

---

## 📐 必须遵循的设计原则

### 通用原则
1. **先读 DESIGN.md**：开始设计前，必须先读取对应品牌的 `DESIGN.md` 文件
2. **提取关键规范**：从 DESIGN.md 中提取色彩系统、字体层级、组件样式
3. **保持一致性**：同一份报告内，设计风格必须统一
4. **对比度优先**：所有文字必须满足 WCAG AA 标准（对比度 ≥ 4.5:1）
5. **响应式设计**：必须支持移动端和桌面端
6. **深色优先**：展厅详情页推荐使用深色主题（与展厅首页一致）

### 研究类额外原则
7. **数据驱动**：必须有可量化的数据支撑
8. **图表必备**：至少2种类型的Chart.js图表
9. **交互增强**：Tab切换、筛选、展开/折叠等交互元素

### 创意类额外原则
10. **视觉优先**：第一眼就要震撼，不是"读"而是"看"
11. **交互必备**：用户可以"玩"，不是被动阅读
12. **打破常规**：不要用标准卡片布局，要创新排版
13. **情感共鸣**：让观众有感觉，截图就想发朋友圈

---

## 🔧 使用方式

```bash
# 查看可用品牌设计系统
ls /app/working/shared/design/design-md/

# 读取特定品牌的设计规范
cat /app/working/shared/design/design-md/apple/DESIGN.md

# 查看深色预览效果
# 在浏览器中打开 preview-dark.html
```

---

*最后更新: 2026-06-11 by 总指挥*
