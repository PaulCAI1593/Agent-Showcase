#!/usr/bin/env python3
"""Append sections 2-5 to the report."""
OUT = '/app/working/shared/showcase/2026-08-15-tencent-ai-bet.html'

parts = []

# SECTION 2: DOMESTIC COMPARISON
parts.append('''
<div class="section-dark">
<div class="container">
<h2 class="section-title">二、国内巨头AI投入对决</h2>
<p class="section-subtitle">腾讯 vs 阿里 vs 字节跳动 vs 百度：四条路径，一个共识</p>

<h3>2.1 2026年资本开支对比</h3>
<table>
<thead><tr><th>公司</th><th>2026年CapEx预期</th><th>同比增速</th><th>AI投入重点</th><th>战略路径</th></tr></thead>
<tbody>
<tr><td><strong>腾讯</strong></td><td>~2,000亿元（高盛/摩根大通）</td><td class="badge-green">+160%</td><td>GPU算力、混元模型、WorkBuddy、微信AI</td><td>自用优先，出租兜底</td></tr>
<tr><td><strong>阿里巴巴</strong></td><td>3年3,800-4,800亿元（2025-2027）</td><td class="badge-green">+50%+</td><td>云基础设施、AI芯片（70%国产）、阿里云智算中心</td><td>云即底盘，算力对外租赁是主业</td></tr>
<tr><td><strong>字节跳动</strong></td><td>2,000亿元（上调自1,600亿）</td><td class="badge-green">+33%</td><td>GPU集群（10万+）、AI芯片850亿、豆包推理</td><td>内外并重，MaaS+算力租赁并行</td></tr>
<tr><td><strong>百度</strong></td><td>~400亿元</td><td class="badge-green">持续增长</td><td>昆仑芯自研、文心大模型、智能云AI基建</td><td>自研芯片+云+模型一体化</td></tr>
</tbody>
</table>

<h3>2.2 C端AI应用竞争格局</h3>
<table>
<thead><tr><th>产品</th><th>月活（MAU）</th><th>所属公司</th><th>关键指标</th></tr></thead>
<tbody>
<tr><td><strong>豆包</strong></td><td>3.45亿（2026年3月）</td><td>字节跳动</td><td>日消耗120万亿token；标准版68元/月起，已启动收费</td></tr>
<tr><td><strong>千问</strong></td><td>1.66亿</td><td>阿里巴巴</td><td>全球下载超30亿次（Qwen3.8开源）</td></tr>
<tr><td><strong>DeepSeek</strong></td><td>1.27亿</td><td>深度求索</td><td>开源模型全球影响力</td></tr>
<tr><td><strong>元宝</strong></td><td>~1.14亿（峰值）</td><td>腾讯</td><td>2025年投流约150亿元，春节10亿红包；日活突破5000万</td></tr>
<tr><td><strong>文心一言</strong></td><td>—</td><td>百度</td><td>较早收费，错失用户增长窗口</td></tr>
</tbody>
</table>

<div class="insight-box">
<p><strong>\U0001F4A1 关键洞察：</strong>国内四巨头的AI投入已形成三条分化路径。<strong>路径A（阿里/百度）</strong>：云是底盘，算力对外租赁是原生主业；<strong>路径B（腾讯）</strong>：云非第一优先级，算力租赁仅作安全垫，优先保障混元、WorkBuddy、微信AI；<strong>路径C（字节）</strong>：内外并重，豆包收费验证商业化，火山引擎承接MaaS。三条路线的根源不在算力价值认知差异，而在集团对云计算业务的战略定位先天不同。</p>
</div>

<h3>2.3 AI商业化进度对比</h3>
<table>
<thead><tr><th>公司</th><th>广告AI</th><th>云AI服务</th><th>C端产品</th><th>商业化阶段</th></tr></thead>
<tbody>
<tr><td><strong>腾讯</strong></td><td class="badge-green">★★★★★</td><td class="badge-blue">★★★☆☆</td><td class="badge-blue">★★★☆☆</td><td>广告已兑现，云起步，C端探索</td></tr>
<tr><td><strong>阿里</strong></td><td class="badge-blue">★★★☆☆</td><td class="badge-green">★★★★★</td><td class="badge-blue">★★★☆☆</td><td>云AI收入占比30%+，通义系列开源生态</td></tr>
<tr><td><strong>字节</strong></td><td class="badge-green">★★★★☆</td><td class="badge-blue">★★★★☆</td><td class="badge-green">★★★★★</td><td>豆包MAU 3.45亿，已启动付费</td></tr>
<tr><td><strong>百度</strong></td><td class="badge-blue">★★★☆☆</td><td class="badge-blue">★★★☆☆</td><td class="badge-orange">★★☆☆☆</td><td>文心变现中但用户增长受限</td></tr>
</tbody>
</table>
</div>
</div>
''')

# SECTION 3: GLOBAL COMPARISON
parts.append('''
<div class="section-black">
<div class="container">
<h2 class="section-title">三、全球AI军备竞赛</h2>
<p class="section-subtitle">当腾讯砸下528亿，大洋彼岸的巨头们在做什么？</p>

<h3>3.1 2026年全球九大CSP资本开支</h3>
<p>据TrendForce最新数据，2026年全球九大云服务商合计资本支出预估上调至<strong>约8,300亿美元</strong>（约合6万亿人民币），年增率从61%提升至<strong>79%</strong>。</p>

<table>
<thead><tr><th>公司</th><th>2026 CapEx指引</th><th>同比增速</th><th>AI收入/进展</th></tr></thead>
<tbody>
<tr><td><strong>AWS（亚马逊）</strong></td><td>~$2,200亿</td><td class="badge-green">+50%</td><td>AI run rate $250亿+，三位数增长；自研Trainium芯片</td></tr>
<tr><td><strong>Microsoft</strong></td><td>~$1,900亿</td><td class="badge-green">+130%</td><td>Azure AI收入三位数增长；Copilot商业化领先</td></tr>
<tr><td><strong>Alphabet（Google）</strong></td><td>$1,950-2,050亿</td><td class="badge-green">+100%+</td><td>Q2收入$1,198亿（+24%）；Google Cloud $248亿（+32%）</td></tr>
<tr><td><strong>Meta</strong></td><td>$1,250-1,450亿</td><td class="badge-green">+85%</td><td>Q2收入$608亿（+28%）；AI推荐驱动广告</td></tr>
<tr><td><strong>Oracle</strong></td><td>大幅增长</td><td class="badge-green">—</td><td>GPU云需求驱动</td></tr>
<tr><td><strong>字节跳动</strong></td><td>2,000亿元</td><td class="badge-green">+33%</td><td>TikTok全球化+豆包+火山引擎</td></tr>
<tr><td><strong>腾讯</strong></td><td>~2,000亿元</td><td class="badge-green">+160%</td><td>混元+WorkBuddy+云+微信AI</td></tr>
<tr><td><strong>阿里巴巴</strong></td><td>3年3,800-4,800亿元</td><td class="badge-green">—</td><td>阿里云AI产品占比30%+</td></tr>
<tr><td><strong>百度</strong></td><td>~400亿元</td><td class="badge-green">—</td><td>10季度累计AI投入超1000亿</td></tr>
</tbody>
</table>

<h3>3.2 美国Big4的"AI收获期"信号</h3>
<p>2026年Q2美国科技巨头财报首次系统性回答了"AI CapEx是否有回报"的问题：</p>

<div class="grid-2">
<div>
<div class="verdict-box">
<h3>AWS：利润率逆势扩张</h3>
<p>AWS在史上最重投资周期中，经营利润率同比扩张520bp至历史高位。AI run rate达$250亿+，三位数增长。AI数据中心CapEx"结构性低回报"的论点正在被证伪。</p>
</div>
</div>
<div>
<div class="verdict-box">
<h3>Microsoft：AI已产生现金回报</h3>
<p>微软CapEx开始趋平，但AI驱动的收入曲线急剧超越。Azure AI和Copilot已在产生现金回报。市场奖励微软——因其竞争对手仍在建设阶段，微软已在收割。</p>
</div>
</div>
</div>

<div class="grid-2">
<div>
<div class="verdict-box">
<h3>Alphabet：首次FCR转负</h3>
<p>Alphabet自IPO以来首次单季自由现金流为负（-$59亿），季度CapEx $449亿。但收入$1,198亿（+24%），Google Cloud $248亿（+32%）。增长强劲与现金消耗并存。</p>
</div>
</div>
<div>
<div class="verdict-box">
<h3>Meta：AI推荐驱动广告</h3>
<p>Q2收入$608亿（+28%），广告几乎独占收入90%+。AI推荐模型驱动，资本开支上调至$1,250-1,450亿。免费现金流降至$7.84亿，但一次性法律和裁员费用影响显著。</p>
</div>
</div>
</div>

<div class="insight-box">
<p><strong>\U0001F4A1 关键类比：腾讯 vs Meta剧本。</strong>2022年Meta将CapEx从$190亿加到$320亿（+68%），股价11个月从$331跌到$91（-73%），市场叙事与今天质疑腾讯一模一样。后续剧本：2023年靠裁员控制成本+广告复苏+AI推荐反哺，股价三年五倍至$600+。如今Meta将2026 CapEx上调至$1,250-1,450亿——市场没有恐慌，反而在Meta宣布对外出租闲置GPU当天给了8.8%的涨幅。</p>
</div>
</div>
</div>
''')

with open(OUT, 'a', encoding='utf-8') as f:
    f.write(''.join(parts))
import os
print(f"Sections 2-3 appended: {os.path.getsize(OUT)} bytes total")
