# -*- coding: utf-8 -*-
path = '/app/working/shared/showcase/2026-09-01-a-share-tech-crash-analysis.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_section = """
<div class="divider"></div>
<div class="section">
<div class="section-label">Deep Dive</div>
<h2>深度专题：北向资金与市场情绪</h2>
<p class="lead">北向资金被视为A股的"聪明钱"，其流向变化往往预示着市场拐点。</p>

<h3 style="margin-top:40px;margin-bottom:20px">📉 北向资金流向分析</h3>
<table class="data-table">
<thead><tr><th>时间段</th><th>北向资金动向</th><th>核心驱动因素</th><th>市场影响</th></tr></thead>
<tbody>
<tr><td>2026年6月</td><td class="green">连续5日净流入150亿+</td><td>外资从低配转向增配，60%流向AI算力</td><td>科技股持续走强</td></tr>
<tr><td>2026年7月</td><td class="red">单月净流出830亿+（五年新高）</td><td>人民币汇率承压（美元兑离岸人民币7.2949）、宏观数据不及预期</td><td>科技股暴跌的推手之一</td></tr>
<tr><td>2026年8月初</td><td>单日买卖量骤增（买入815亿、卖出898亿）</td><td>北向资金或正在进行大幅调仓</td><td>调仓信号而非系统性撤退</td></tr>
</tbody>
</table>

<div class="insight-box">
<h3>💡 北向资金流出的真相</h3>
<p><strong>北向资金流出≠看空中国。</strong>光大证券研报指出，人民币汇率与短期宏观数据承压是核心原因。瑞银亚洲经济研究主管汪涛认为，北向资金流出是因为经济复苏及政策出台不及预期，属于短期行为。值得注意的是，北向资金在今年7月24日后产生了一项重大变化——"假外资"只可卖出不可继续买入A股，这也在一定程度上放大了净流出数据。</p>
<p><strong>长期看，外资对A股的定位正在从"战术性交易"转向"战略性配置"。</strong>2026年QFII持仓总市值从1846.6亿元增至2212亿元，增幅近20%。贝莱德明确表示：国内科创成长企业估值更具性价比，AI板块不存在显著泡沫。</p>
</div>

<h3 style="margin-top:40px;margin-bottom:20px">📊 市场情绪指标</h3>
<div class="metric-row">
<div class="metric">
<div class="metric-value">~2.03万亿</div>
<div class="metric-label">暴跌日成交额</div>
</div>
<div class="metric">
<div class="metric-value">2,769</div>
<div class="metric-label">下跌个股数</div>
</div>
<div class="metric">
<div class="metric-value">170只</div>
<div class="metric-label">跌幅≥9%个股</div>
</div>
<div class="metric">
<div class="metric-value">265.54万</div>
<div class="metric-label">7月新开户数</div>
</div>
</div>
<p style="font-size:14px;color:#86868b;line-height:1.8;margin-top:16px">7月A股新开户265.54万户，环比下降7.3%。新开户数的下降反映散户风险偏好有所收缩，但并未出现2015年式的恐慌性销户潮。两融个人投资者达753.93万名，7月以来新增5.94万名，市场参与度仍在扩大。成交额维持在2万亿级别，说明市场流动性充裕，暴跌中并非无量空跌。</p>
</div>

<div class="divider"></div>
<div class="section">
<div class="section-label">Sector Rotation</div>
<h2>板块轮动：资金从"极致分化"到"再平衡"</h2>
<p class="lead">暴跌的本质是资金从过度拥挤的科技赛道向低估值防御板块的阶段性转移。</p>

<h3 style="margin-top:40px;margin-bottom:20px">🔄 资金轮动路径</h3>
<div class="card-grid">
<div class="card">
<div class="card-icon" style="color:#ff3b30">📉</div>
<h3>流出方向：高估值科技硬件</h3>
<p>• 通信板块单日暴跌10.88%（新易盛、中际旭创跌停）<br>• 电子板块跌7.02%（源杰科技跌16.77%）<br>• 半导体概念跌7%+（联讯仪器暴跌14%）<br>• CPO概念全线崩塌（长光华芯、长飞光纤跌停）<br>• 融资净买入居前的科技股遭集中止盈</p>
</div>
<div class="card">
<div class="card-icon" style="color:#30d158">📈</div>
<h3>流入方向：防御+价值板块</h3>
<p>• 食品饮料板块逆势上涨2.14%<br>• 商贸零售板块涨1.53%<br>• 银行板块涨1.51%<br>• 大消费方向（白酒、乳业、旅游）全面走强<br>• 贵州茅台股价涨逾2%至1320元，回升至A股第二</p>
</div>
</div>

<div class="quote">
"市场正高度关注美联储议息会议，以及即将密集发布的科技巨头财报。只有当这些财报能够证实AI资本开支确实转化为实际的营收和现金流，市场的恐慌情绪才有望得到实质性缓解。AI产业链正处于从'极致分化'向'结构性再平衡'过渡的关键窗口期。" ——谭智汨
</div>

<div class="insight-box">
<h3>💡 对散户投资者的启示</h3>
<p><strong>1. 不要追涨杀跌。</strong>暴跌当天卖出科技股的散户，在8月4日反弹中错失了5.64%的创业板涨幅。市场短期是投票机，长期是称重机。</p>
<p><strong>2. 关注业绩而非概念。</strong>半年报业绩验证期过后，有业绩支撑的真科技龙头（如中际旭创、新易盛）率先反弹，纯概念股持续低迷。选股的核心逻辑从"赛道信仰"转向"业绩兑现"。</p>
<p><strong>3. 分散配置，不要all in单一赛道。</strong>本次暴跌再次证明——即使是AI这样的超级主线，也会有剧烈的阶段性调整。杠铃策略（科技成长+高股息防御）是更稳健的选择。</p>
<p><strong>4. 用长期视角看待波动。</strong>科创50自2024年9月24日以来涨超166%，期间多次出现10%+的回调。每一次回调都是加仓机会，而非恐慌信号。</p>
</div>
</div>
"""

# Insert before the Data Sources section
marker = '<div class="section-label">Data Sources</div>'
content = content.replace(marker, new_section + '\n<div class="section-label">Data Sources</div>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

import re
cn = len(re.findall(r'[\u4e00-\u9fff]', content))
print(f'Updated: {len(content)} bytes, {cn} Chinese chars')
