# -*- coding: utf-8 -*-
path = '/app/working/shared/showcase/2026-09-01-a-share-tech-crash-analysis.html'
chunk = """
<div class="divider"></div>
<div class="section">
<div class="section-label">Historical Comparison</div>
<h2>历史对照：这次不一样吗？</h2>
<p class="lead">将本轮调整放在历史坐标系中审视，寻找参照与规律。</p>
<table class="data-table">
<thead><tr><th>对比维度</th><th>2015年杠杆牛崩盘</th><th>2022年科技股调整</th><th>2026年7月本轮调整</th></tr></thead>
<tbody>
<tr><td>上证指数PE</td><td>~22倍</td><td>~12倍</td><td>~17倍（中位水平）</td></tr>
<tr><td>两融/流通市值</td><td class="red">4.72%</td><td>~2.0%</td><td class="green">~2.23%（远低于峰值）</td></tr>
<tr><td>宏观背景</td><td>去杠杆+股灾</td><td>美联储暴力加息</td><td>LPR稳定，有望降息</td></tr>
<tr><td>产业周期</td><td>移动互联网尾声</td><td>AI概念萌芽期</td><td>AI产业化爆发期</td></tr>
<tr><td>盈利支撑</td><td>弱</td><td>弱</td><td class="green">极强（IC利润增18.5倍）</td></tr>
<tr><td>调整性质</td><td>系统性崩盘</td><td>趋势性熊市</td><td class="green">结构性调整（高切低）</td></tr>
</tbody>
</table>
<div class="quote">
"当前科技股的调整，或许更多是阶段性高切低，而非行情终局。赛道拥挤度消化、结构性再平衡，并不等同于牛市终结。" ——国泰海通证券
</div>
</div>

<div class="divider"></div>
<div class="section">
<div class="section-label">Social &amp; Sentiment</div>
<h2>社会与情绪维度</h2>
<p class="lead">暴跌不仅仅是数字游戏——它影响着数千万投资者的信心和决策。</p>
<div class="card-grid">
<div class="card">
<div class="card-icon">📱</div>
<h3>微博热搜：A股暴跌刷屏</h3>
<p>"A股暴跌"话题冲上微博热搜。2769只个股下跌，从通信板块到半导体到CPO，科技赛道全线崩塌。散户恐慌情绪蔓延，但机构视角截然不同。</p>
</div>
<div class="card">
<div class="card-icon">🏦</div>
<h3>国家队信号：不走熊的基础</h3>
<p>东方财富证券陈果明确表态："当前A股不具备走熊基础"。下半年多家真科技公司登陆A股有望吸引增量资金，提升市场活跃度和风险偏好。</p>
</div>
<div class="card">
<div class="card-icon">👥</div>
<h3>散户 vs 机构：认知差</h3>
<p>散户看到的是-7.35%的恐惧，机构看到的是黄金坑的机遇。7月暴跌后，仅8月4日一天，创业板指就大涨5.64%——恐慌卖出的筹码被聪明资金接走。</p>
</div>
<div class="card">
<div class="card-icon">🌏</div>
<h3>外资态度：分歧中的共识</h3>
<p>短期外资因汇率压力净流出，但贝莱德、摩根士丹利等巨头依然看多中国科技资产。外资坚持"杠铃策略"——一端科技成长，一端高股息防御。</p>
</div>
</div>
</div>
"""
with open(path, 'a', encoding='utf-8') as f:
    f.write(chunk)
print('Part 4 done')
