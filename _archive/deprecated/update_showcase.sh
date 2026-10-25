#!/bin/bash
# 智囊团展厅增量更新脚本
# 用法: ./update_showcase.sh [research|creative] "标题" "描述" "负责人"
# 功能：按日期创建文件夹，存储HTML报告，更新manifest.json
#
# ⭐ 设计规范要求：
#   详情页HTML报告的设计风格必须参考以下设计系统文件：
#   /app/working/shared/design/design-md/
#   包含 Apple、Stripe、Linear、Vercel、Figma 等 50+ 品牌设计系统
#   参考方式：读取对应品牌的 DESIGN.md，提取色彩/排版/组件规范应用到报告中

AGENT_DIR="/app/working/shared/showcase"
MANIFEST="$AGENT_DIR/manifest.json"

# 检查参数
if [ $# -lt 4 ]; then
    echo "用法: $0 [research|creative] '标题' '描述' '负责人'"
    echo "示例: $0 research 'SpaceX IPO分析' '1.75万亿估值深度报告' 量研"
    exit 1
fi

TYPE="$1"
TITLE="$2"
DESC="$3"
AGENT="$4"

# 验证类型
if [ "$TYPE" != "research" ] && [ "$TYPE" != "creative" ]; then
    echo "错误: 类型必须是 research 或 creative"
    exit 1
fi

# 生成ID和日期
ID="item-$(date +%Y%m%d%H%M%S)"
DATE=$(date +%Y-%m-%d)
SUBDIR="$AGENT_DIR/$DATE"
HTML_FILE="$SUBDIR/${TYPE}-${ID}.html"

# 按日期创建文件夹
mkdir -p "$SUBDIR"

# 生成HTML文件
cat > "$HTML_FILE" << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>$TITLE | 智囊团展厅</title>
  <style>
    :root {
      --light-gray: #f5f5f7;
      --text-primary: #1a1a1a;
      --text-secondary: #4a4a4a;
      --text-muted: #6b6b6b;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
      font-size: 17px;
      line-height: 1.47;
      color: var(--text-primary);
      background: var(--light-gray);
      min-height: 100vh;
    }
    .container { max-width: 800px; margin: 0 auto; padding: 60px 20px; }
    .header {
      background: #000;
      color: #fff;
      padding: 80px 20px;
      text-align: center;
    }
    .header h1 { font-size: 40px; font-weight: 600; margin-bottom: 12px; }
    .header .meta { color: #86868b; font-size: 14px; }
    .content { background: #fff; border-radius: 18px; padding: 48px; margin-top: 40px; }
    .back-link {
      display: inline-block;
      margin-bottom: 24px;
      color: #0071e3;
      text-decoration: none;
      font-size: 14px;
    }
    .back-link:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="header">
    <h1>$TITLE</h1>
    <div class="meta">$AGENT · $DATE · $TYPE</div>
  </div>
  <div class="container">
    <a href="../index.html" class="back-link">← 返回展厅</a>
    <div class="content">
      <h2>项目概述</h2>
      <p>$DESC</p>
      <hr style="margin: 32px 0; border: none; border-top: 1px solid #e5e5e7;">
      <h3>项目详情</h3>
      <ul>
        <li><strong>类型</strong>: $TYPE</li>
        <li><strong>负责人</strong>: $AGENT</li>
        <li><strong>日期</strong>: $DATE</li>
        <li><strong>ID</strong>: $ID</li>
      </ul>
      <p style="margin-top: 32px; color: #86868b; font-size: 14px;">
        注：此处应替换为完整的HTML报告内容
      </p>
    </div>
  </div>
</body>
</html>
EOF

# 相对路径（用于manifest）
RELATIVE_PATH="${DATE}/${TYPE}-${ID}.html"

# 更新manifest.json
python3 -c "
import json

try:
    with open('$MANIFEST', 'r') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {}

# 兼容空对象/缺字段
data.setdefault('version', '1.0')
data.setdefault('research', [])
data.setdefault('creative', [])
data.setdefault('updates', [])

new_item = {
    'id': '$ID',
    'title': '$TITLE',
    'description': '$DESC',
    'agent': '$AGENT',
    'date': '$DATE',
    'type': '$TYPE',
    'file': '$RELATIVE_PATH'
}

if '$TYPE' == 'research':
    data['research'].insert(0, new_item)
    data['researchCount'] = len(data['research'])
else:
    data['creative'].insert(0, new_item)
    data['creativeCount'] = len(data['creative'])

data['total'] = len(data['research']) + len(data['creative'])
data['latestDate'] = '$DATE'

with open('$MANIFEST', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('✅ 已添加作品')
print('   标题:', '$TITLE')
print('   类型:', '$TYPE')
print('   负责人:', '$AGENT')
print('   日期:', '$DATE')
print('   文件:', '$RELATIVE_PATH')
"

echo ""
echo "📊 展厅统计:"
python3 -c "import json; d=json.load(open('$MANIFEST')); print('   总作品:', d.get('total', 0)); print('   研究类:', d.get('researchCount', 0)); print('   创意类:', d.get('creativeCount', 0))"
echo ""
echo "🌐 访问地址: file://$AGENT_DIR/index.html"