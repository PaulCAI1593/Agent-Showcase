#!/usr/bin/env python3
"""Append sections 4-6 to the report."""
OUT = '/app/working/shared/showcase/2026-08-15-tencent-ai-bet.html'

parts = []

# SECTION 4: AI COMMERCIALIZATION
parts.append('''
<div class="section-light">
<div class="container">
<h2 class="section-title">四、AI商业化路径分析</h2>
<p class="section-subtitle">从"战略叙事"到"财报兑现"的拐点信号</p>

<h3>4.1 拐点信号已现：三条收入兑现线</h3>
<p>腾讯AI投入的回报并非遥不可及——至少三条业务线已在财报中体现AI带来的增量收入：</p>

<table>
<thead><tr><th>兑现线</th><th>Q2证据</th><th>AI贡献度</th><th>置信度</th></tr></thead>
<tbody>
<tr><td><strong>\U0001F3AF 广告（最强线）</strong></td><td>营销服务+22%，连续15季双位数增长。AI推荐模型驱动点击率提升15-22%，AIM+覆盖80%+客户</td><td>过半增速来自AI</td><td class="badge-green">高（已验证）</td></tr>
<tr><td><strong>\u2601\uFE0F 云服务</strong></td><td>云增速超20%。AI占云收入25-30%。TokenHub日Token 25万亿。WorkBuddy付费用户毛利率≈云整体毛利率</td><td>AI贡献增量显著</td><td class="badge-green">高（数据可查）</td></tr>
<tr><td><strong>\U0001F3AE 游戏</strong></td><td>国内游戏+17%。Hy3D降低场景成本。AINPC累计用户1.67亿，日活1770万</td><td>间接贡献（降本+用户留存）</td><td class="badge-blue">中高</td></tr>
<tr><td><strong>\U0001F4AC 微信AI</strong></td><td>小微灰度测试中，已扩至朋友圈。WeLM驱动</td><td>尚未产生直接收入</td><td class="badge-orange">待验证</td></tr>
</tbody>
</table>

<h3>4.2 最先实现盈利的AI业务线</h3>
<p>从商业化成熟度排序：</p>

<div class="grid-3">
<div class="card" style="background:#f5f5f7;">
<div class="card-title">NO.1 广告AI</div>
<div class="highlight-num" style="font-size:48px;color:var(--green)">已盈利</div>
<p>AI广告推荐是腾讯AI最先、最直接的盈利场景。每提升1个百分点的广告点击率，对应几十亿增量收入。AIM+将制作周期从3天压至12小时。管理层直言："AI技术在广告定向方面的应用持续深化，推动了整体业绩提升。"视频号广告收入占比已超35%。</p>
</div>
<div class="card" style="background:#f5f5f7;">
<div class="card-title">NO.2 云AI服务</div>
<div class="highlight-num" style="font-size:48px;color:var(--apple-blue)">接近盈利</div>
<p>WorkBuddy付费用户毛利率已与腾讯云整体毛利率相当。Token业务在当前低价下保持正毛利——"国内Token生产成本远低于外界认知"（James Mitchell原话）。但免费用户补贴拉低了整体毛利率。MaaS/API调用正随规模效应改善。</p>
</div>
<div class="card" style="background:#f5f5f7;">
<div class="card-title">NO.3 WorkBuddy</div>
<div class="highlight-num" style="font-size:48px;color:var(--orange)">接近临界</div>
<p>月访问量2097万次（国内PC端同类第一），MAU达2000万级。企业版198元/席/月起。接入Hy3后任务解决率72%→90%。管理层已将WorkBuddy列为资金投入优先级高于元宝的产品。但免费到付费转化率仍是悬念。</p>
</div>
</div>

<h3>4.3 投入产出比（AI Revenue / AI Investment）估算</h3>

<table>
<thead><tr><th>指标</th><th>估算值</th><th>说明</th></tr></thead>
<tbody>
<tr><td><strong>Q2 AI相关增量收入</strong></td><td>~100-150亿元</td><td>广告AI增量(~60-80亿) + 云AI增量(~30-40亿) + 游戏AI降本(~10-20亿)</td></tr>
<tr><td><strong>Q2 AI相关投入</strong></td><td>~500亿元+</td><td>CapEx 528亿（主体AI）+ R&D AI部分(~150亿)</td></tr>
<tr><td><strong>单季度AI ROI</strong></td><td>~0.2-0.3x</td><td>投入远大于当期回报，属战略投资期</td></tr>
<tr><td><strong>累计AI ROI趋势</strong></td><td>逐步改善</td><td>广告AI已过盈亏平衡线；云AI随规模效应改善中</td></tr>
<tr><td><strong>管理层预期</strong></td><td>12-18个月验证窗口</td><td>"模型训练集中CapEx主要发生在今明两年"——刘炽平</td></tr>
</tbody>
</table>

<div class="insight-box">
<p><strong>\U0001F4A1 关键判断：</strong>当前AI ROI偏低（约0.2-0.3x）是战略投资期的正常表现，不应与运营期比较。参考Meta 2022-2023年的剧本——当时CapEx激增导致FCF腰斩，但AI推荐模型成熟后驱动广告收入创历史新高，股价三年五倍。腾讯的核心逻辑是：<strong>13亿微信日活 × AI广告效率提升 = 数十亿级增量</strong>，这个乘法效应才是528亿投资的底层逻辑。</p>
</div>
</div>
</div>
''')

# SECTION 5: SCENARIO ANALYSIS
parts.append('''
<div class="section-dark">
<div class="container">
<h2 class="section-title">五、情景推演与风险矩阵</h2>
<p class="section-subtitle">腾讯AI战略的三种可能走向</p>

<h3>5.1 三大情景</h3>

<table>
<thead><tr><th>情景</th><th>概率</th><th>描述</th><th>触发条件</th></tr></thead>
<tbody>
<tr>
<td><strong class="badge-green">\u2605 情景一：模型追赶成功</strong></td>
<td>40%</td>
<td>混元12-18个月缩小与海外旗舰差距，在中文场景形成差异化。WorkBuddy完成免费→付费规模化转化，微信AI全量落地。算力内部消化持续，出租始终是备选。</td>
<td>Hy4进入中文SuperCLUE前三 + WorkBuddy付费转化率突破15%</td>
</tr>
<tr>
<td><strong class="badge-blue">\u25CB 情景二：中等水平，混合变现</strong></td>
<td>45%</td>
<td>混元无法完全追平海外旗舰，但在垂类场景具备可用性。自用算力消耗持续，富余算力分批对外出租，形成自用+出租混合模式。</td>
<td>WorkBuddy MAU稳定增长但付费率低于10%；微信AI灰度有限扩量</td>
</tr>
<tr>
<td><strong class="badge-red">\u25CB 情景三：模型滞后，退路启用</strong></td>
<td>15%</td>
<td>模型能力不及预期，内部算力消耗不足。大规模算力转向出租，面临市场饱和+芯片折旧双重约束。年折旧约100-130亿，按50%利用率计算租金收入约60-80亿，存在缺口。</td>
<td>Hy4性能不达预期 + WorkBuddy用户增长停滞</td>
</tr>
</tbody>
</table>

<h3>5.2 风险矩阵</h3>
<table>
<thead><tr><th>风险</th><th>影响程度</th><th>应对措施</th></tr></thead>
<tbody>
<tr><td><strong>硬件折旧周期风险</strong></td><td class="badge-red">高</td><td>GPU商用黄金期2.5-3年。高盛预测2026-2028年CapEx为2100/2450/2470亿元，折旧将持续压制利润表</td></tr>
<tr><td><strong>算力租赁市场下行</strong></td><td class="badge-orange">中高</td><td>2026-2027年全球GPU产能集中释放，行业租金价格大概率下行。单纯"收算力税"的长期盈利能力存疑</td></tr>
<tr><td><strong>组织执行风险</strong></td><td class="badge-orange">中</td><td>混元（TEG）与WeLM微信模型（WXG）分属两套事业群、两套算力池。管理层表态能否穿透组织边界是关键</td></tr>
<tr><td><strong>自由现金流持续承压</strong></td><td class="badge-orange">中</td><td>若年均CapEx维持2000亿+，经营利润增速个位数，千亿回购空间可能收缩</td></tr>
<tr><td><strong>国际地缘风险</strong></td><td class="badge-blue">中低</td><td>腾讯算力采购70%转向国产，降低对英伟达依赖</td></tr>
</tbody>
</table>
</div>
</div>
''')

# SECTION 6: CONCLUSION
parts.append('''
<div class="section-black">
<div class="container">
<h2 class="section-title">六、结论与长期价值评估</h2>
<p class="section-subtitle">腾讯AI战略的终局思考</p>

<h3>6.1 核心结论</h3>

<div class="verdict-box">
<h3>\U0001F4CC 判断一：腾讯AI投入已过"是否投入"阶段，进入"何时兑现"阶段</h3>
<p>广告AI（+22%增速中AI贡献过半）、云AI服务（AI占云收入25-30%）、游戏AI（AINPC 1.67亿用户）三条线已在财报中体现。这不是PPT式的战略叙事，而是真实的财报兑现。</p>
</div>

<div class="verdict-box">
<h3>\U0001F4CC 判断二：528亿不是"赌注"，是"必选题"</h3>
<p>全球九大CSP合计CapEx 8,300亿美元（+79%）。美国Big4 alone $7,250亿。腾讯2,000亿元（~$280亿）在全球排名中并不突出。在AI军备竞赛中，不投入意味着被淘汰。腾讯的"赌注"实际上是参与下一轮竞争的入场券。</p>
</div>

<div class="verdict-box">
<h3>\U0001F4CC 判断三：腾讯的核心优势在"消化能力"而非"投入规模"</h3>
<p>腾讯的独特之处不是砸了多少钱，而是<strong>拥有13亿微信日活的天然消化场景</strong>。广告效率每提升1个百分点=几十亿增量；游戏AI提升留存=直接营收；WorkBuddy/CodeBuddy的推理需求=自用算力消耗。这是阿里和字节都不具备的差异化优势。正如马化腾所说："腾讯正从智能、应用、基础设施三大维度打造AI驱动的全新腾讯。"</p>
</div>

<div class="verdict-box">
<h3>\U0001F4CC 判断四：12-18个月是关键验证窗口</h3>
<p>刘炽平明确表示"模型训练的集中CapEx主要发生在今明两年"。推理算力投入则与业务回报挂钩，"如果回报达不到预期，就会调整投资规模"。这意味着：<strong>2027年底前，市场将有足够数据判断腾讯AI投入的回报率。</strong></p>
</div>

<h3>6.2 长期价值评估矩阵</h3>
<table>
<thead><tr><th>维度</th><th>评分</th><th>说明</th></tr></thead>
<tbody>
<tr><td><strong>战略方向</strong></td><td class="badge-green">\u2605\u2605\u2605\u2605\u2605</td><td>"自用优先+出租兜底"路径合理，算力分配优先级清晰</td></tr>
<tr><td><strong>执行能力</strong></td><td class="badge-green">\u2605\u2605\u2605\u2605\u2606</td><td>Hy3三个月迭代至正式版、WorkBuddy领跑市场。扣分项：TEG/WXG跨事业群协调</td></tr>
<tr><td><strong>商业化进度</strong></td><td class="badge-blue">\u2605\u2605\u2605\u2606\u2606</td><td>广告已兑现、云起步、WorkBuddy接近临界。但C端订阅变现弱于字节</td></tr>
<tr><td><strong>财务承受力</strong></td><td class="badge-blue">\u2605\u2605\u2605\u2606\u2606</td><td>游戏+微信现金流稳健，但FCF转负、净现金-22%。若CapEx年均2000亿+持续三年，压力显著</td></tr>
<tr><td><strong>竞争壁垒</strong></td><td class="badge-green">\u2605\u2605\u2605\u2605\u2606</td><td>微信生态+游戏现金牛+云MaaS形成三角护城河。13亿日活是最强壁垒</td></tr>
</tbody>
</table>

<div class="insight-box">
<p><strong>\U0001F3AF 终极判断：</strong>腾讯正在用528亿/季度的价格，购买AI时代的"船票"。与Meta 2022-2023年的剧本高度相似——短期利润率承压、市场恐慌、但核心业务现金流稳健。如果AI能在12-18个月内持续兑现广告+云+游戏的增量回报，腾讯可能正在用今天的利润，买下一轮十年的增长。反之，若模型迭代滞后于硬件折旧周期，数百亿级CapEx将成为长期折旧包袱。</p>
<p><strong>关注信号：</strong>①Hy4发布后性能是否达到预期 ②WorkBuddy付费转化率 ③微信AI灰度→公测时间节点 ④Q3/Q4 CapEx是否放缓 ⑤自由现金流何时回正</p>
</div>

<div class="footnote">
<p><strong>数据来源</strong></p>
<p>[1] 腾讯控股2026年第二季度业绩公告，2026年8月12日<br>
[2] 高盛/瑞银/摩根大通/杰富瑞腾讯研报，2026年8月13日<br>
[3] TrendForce集邦咨询，"2026年全球九大CSP资本支出预估"，2026年5月<br>
[4] 36氪，"算不平的AI账：字节收网，阿里腾讯百度还在站岗"，2026年8月<br>
[5] 钛媒体，"腾讯528亿算力账：模型优先，出租是退路"，2026年8月13日<br>
[6] 华尔街见闻，"528亿砸下去，腾讯要换估值锚"，2026年8月<br>
[7] 新浪财经，"二季度砸下528亿，腾讯AI何时能挣回来"，2026年8月13日<br>
[8] 易观分析，"2026年Q2中国办公智能体平台市场洞察报告"<br>
[9] QuestMobile，"2025年第三季度中国AI应用市场报告"<br>
[10] UncoverAlpha，"Amazon, Google, Microsoft, Meta Q2 Earnings"，2026年8月<br>
[11] 21世纪经济报道，"腾讯2026年第二季度资本支出超527亿元"，2026年8月13日</p>
<p style="margin-top:24px"><strong>免责声明：</strong>本报告基于公开信息整理分析，不构成任何投资建议。报告中的估值和预测仅为分析参考，实际结果可能与预期存在重大差异。</p>
</div>
</div>
</div>

<div style="background:var(--black);color:#86868b;text-align:center;padding:48px 24px;font-size:14px;">
<p>研析 Research Analyst | 2026年8月15日</p>
<p>AI投入从战略叙事到财报兑现的拐点</p>
</div>

</body>
</html>
''')

with open(OUT, 'a', encoding='utf-8') as f:
    f.write(''.join(parts))
import os
size = os.path.getsize(OUT)
print(f"Report complete: {size} bytes ({size//1024}KB)")
# Count Chinese chars
with open(OUT, 'r', encoding='utf-8') as f:
    text = f.read()
# strip HTML tags for rough word count
import re
clean = re.sub(r'<[^>]+>', '', text)
chinese = len(re.findall(r'[\u4e00-\u9fff]', clean))
print(f"Chinese characters: {chinese}")
