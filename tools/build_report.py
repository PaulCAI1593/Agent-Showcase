#!/usr/bin/env python3
"""Build the complete Tencent AI report HTML file."""

parts = []

# Part 1: HTML head, CSS, Hero, Executive Summary
parts.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>腾讯528亿AI赌注 | 从战略叙事到财报兑现的拐点</title>
<style>
:root{--black:#000;--light-gray:#f5f5f7;--near-black:#1d1d1f;--apple-blue:#0071e3;--link-blue:#0066cc;--white:#fff;--green:#34c759;--red:#ff3b30;--orange:#ff9500}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','PingFang SC',sans-serif;color:var(--near-black);background:var(--white);line-height:1.47;-webkit-font-smoothing:antialiased;letter-spacing:-0.374px}
.hero{background:var(--black);color:var(--white);padding:120px 24px 100px;text-align:center}
.hero h1{font-size:56px;font-weight:600;line-height:1.07;letter-spacing:-0.28px;max-width:980px;margin:0 auto 24px}
.hero .subtitle{font-size:21px;font-weight:400;color:#86868b;max-width:700px;margin:0 auto 40px;line-height:1.38}
.hero .meta{font-size:14px;color:#86868b}
.hero .meta span{margin:0 12px}
.container{max-width:980px;margin:0 auto;padding:0 24px}
.section-light{background:var(--white);padding:100px 24px}
.section-dark{background:var(--light-gray);padding:100px 24px}
.section-black{background:var(--black);color:var(--white);padding:100px 24px}
.section-title{font-size:40px;font-weight:600;line-height:1.1;letter-spacing:-0.015em;margin-bottom:12px}
.section-subtitle{font-size:21px;color:#86868b;margin-bottom:56px;line-height:1.38}
h3{font-size:28px;font-weight:600;line-height:1.14;letter-spacing:-0.01em;margin-bottom:16px;margin-top:56px}
h4{font-size:21px;font-weight:600;margin-bottom:12px;margin-top:32px}
p{font-size:17px;line-height:1.47;letter-spacing:-0.374px;margin-bottom:20px;color:#1d1d1f}
.section-black p,.section-dark p.light-text{color:#d2d2d7}
.highlight-num{font-size:72px;font-weight:700;line-height:1.05;letter-spacing:-0.04em}
.highlight-label{font-size:17px;color:#86868b;margin-top:4px}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;margin-bottom:48px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-bottom:48px}
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:32px;margin-bottom:48px}
.card{background:var(--light-gray);border-radius:20px;padding:32px}
.card-dark{background:rgba(255,255,255,0.06);border-radius:20px;padding:32px}
.card-title{font-size:14px;text-transform:uppercase;letter-spacing:0.04em;color:#86868b;margin-bottom:12px;font-weight:600}
table{width:100%;border-collapse:collapse;margin:32px 0;font-size:15px}
th{text-align:left;padding:12px 16px;font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:0.04em;color:#86868b;border-bottom:1px solid #d2d2d7}
td{padding:14px 16px;border-bottom:1px solid #e5e7eb;vertical-align:top}
tr:hover td{background:rgba(0,0,0,0.02)}
.section-black table th{border-bottom-color:#424245}
.section-black table td{border-bottom-color:#424245;color:#d2d2d7}
.section-black table tr:hover td{background:rgba(255,255,255,0.05)}
.badge-green{color:var(--green);font-weight:600}
.badge-red{color:var(--red);font-weight:600}
.badge-orange{color:var(--orange);font-weight:600}
.badge-blue{color:var(--apple-blue);font-weight:600}
.insight-box{background:#f5f5f7;border-left:4px solid var(--apple-blue);padding:24px 32px;margin:32px 0;border-radius:0 12px 12px 0}
.insight-box p{margin-bottom:8px;font-size:15px}
.insight-box strong{color:var(--near-black)}
.section-black .insight-box{background:rgba(255,255,255,0.05);border-left-color:#0071e3}
.section-black .insight-box p{color:#d2d2d7}
.tag{display:inline-block;padding:4px 12px;border-radius:980px;font-size:13px;font-weight:500;margin-right:8px;margin-bottom:8px}
.tag-blue{background:rgba(0,113,227,0.12);color:var(--apple-blue)}
.tag-green{background:rgba(52,199,89,0.12);color:var(--green)}
.tag-red{background:rgba(255,59,48,0.12);color:var(--red)}
.tag-orange{background:rgba(255,149,0,0.12);color:var(--orange)}
.footnote{font-size:13px;color:#86868b;line-height:1.6;margin-top:48px;padding-top:24px;border-top:1px solid #d2d2d7}
.section-black .footnote{border-top-color:#424245}
.comparison-arrow{display:inline-block;font-size:14px;padding:2px 8px;border-radius:6px;font-weight:600}
.arrow-up{background:rgba(52,199,89,0.12);color:var(--green)}
.arrow-down{background:rgba(255,59,48,0.12);color:var(--red)}
.verdict-box{background:linear-gradient(135deg,#1d1d1f 0%,#2d2d30 100%);border-radius:20px;padding:48px;color:white;margin:32px 0}
.verdict-box h3{color:white}
.verdict-box p{color:#d2d2d7}
ul{margin:16px 0 24px 24px;font-size:17px;line-height:1.6}
li{margin-bottom:8px}
.section-black ul{color:#d2d2d7}
.section-dark ul{color:#1d1d1f}
.bar-container{display:flex;align-items:center;gap:12px;margin:8px 0}
.bar-track{flex:1;height:10px;background:#e5e7eb;border-radius:5px;overflow:hidden}
.bar-fill{height:100%;border-radius:5px}
.bar-label{font-size:14px;font-weight:600;min-width:60px;text-align:right}
.toc{display:flex;flex-wrap:wrap;gap:12px;margin:32px 0}
.toc a{display:inline-block;padding:8px 20px;background:rgba(255,255,255,0.08);border-radius:980px;color:#d2d2d7;text-decoration:none;font-size:15px;transition:background 0.2s}
.toc a:hover{background:rgba(255,255,255,0.15)}
@media(max-width:768px){.hero h1{font-size:36px}.section-title{font-size:28px}.grid-3,.grid-4{grid-template-columns:1fr}.grid-2{grid-template-columns:1fr}.highlight-num{font-size:48px}}
</style>
</head>
<body>

<!-- HERO -->
<div class="hero">
<div class="meta"><span>📊 深度研究报告</span><span>|</span><span>2026年8月15日</span><span>|</span><span>💰经济 · 🤖技术 · 🏭产业</span></div>
<br><br>
<h1>腾讯528亿"赌注"</h1>
<p class="subtitle">AI投入从战略叙事到财报兑现的拐点——Q2财报深度解读与全球科技巨头AI军备竞赛全景分析</p>
<div class="toc">
<a href="#s1">Q2财报全景</a>
<a href="#s2">AI投入深度拆解</a>
<a href="#s3">国内巨头对比</a>
<a href="#s4">全球军备竞赛</a>
<a href="#s5">商业化拐点</a>
<a href="#s6">AI投入产出比</a>
<a href="#s7">战略价值评估</a>
</div>
</div>
""")

# Part 2: Executive Summary
parts.append("""
<div class="section-dark">
<div class="container">
<h2 class="section-title">执行摘要</h2>
<p class="section-subtitle">一份数据驱动的战略判断</p>
<div class="grid-4">
<div><div class="highlight-num" style="color:var(--apple-blue)">528<span style="font-size:36px">亿</span></div><div class="highlight-label">Q2资本开支 <span class="comparison-arrow arrow-up">+176%</span></div></div>
<div><div class="highlight-num" style="color:var(--green)">2048<span style="font-size:36px">亿</span></div><div class="highlight-label">Q2总营收 <span class="comparison-arrow arrow-up">+11%</span></div></div>
<div><div class="highlight-num" style="color:var(--orange)">273<span style="font-size:36px">亿</span></div><div class="highlight-label">Q2研发支出 <span class="comparison-arrow arrow-up">+35%</span></div></div>
<div><div class="highlight-num" style="color:var(--red)">-138<span style="font-size:36px">亿</span></div><div class="highlight-label">自由现金流（剔除预付后+376亿）</div></div>
</div>
<div class="insight-box">
<p><strong>核心判断：</strong>腾讯2026年Q2财报标志着其AI战略从"叙事期"进入"投入兑现期"的关键拐点。单季528亿元资本开支（YoY +176%）不仅超过2019-2023年任一整年，更令上半年累计847亿元超越2025全年。AI已非成本中心——广告业务22%增速中AI贡献过半，云服务受AI需求拉动增速超20%，游戏AI用户累计1.67亿。但自由现金流转负（-138亿元）、净利润增速仅0.7%表明：腾讯正在用今天的利润，买下一轮十年的增长。</p>
<p><strong>⚠️ 风险提示：</strong>2026-2028年年均CapEx预计超2000亿元，折旧将持续压制利润表。模型迭代若慢于硬件折旧周期（约2.5-3年），巨额算力投资面临贬值风险。</p>
</div>
</div>
</div>
""")

# Part 3: Section 1 - Q2 Financial Deep Dive
parts.append("""
<div class="section-light" id="s1">
<div class="container">
<h2 class="section-title">一、Q2财报全景透视</h2>
<p class="section-subtitle">从营收结构看AI如何渗透腾讯每一寸业务</p>

<h3>1.1 核心财务数据总览</h3>
<table>
<thead><tr><th>指标</th><th>Q2 2026</th><th>Q2 2025</th><th>同比变化</th></tr></thead>
<tbody>
<tr><td><strong>总营收</strong></td><td>2,047.9亿元</td><td>~1,845亿元</td><td class="badge-green">+11%</td></tr>
<tr><td><strong>增值服务（VAS）</strong></td><td>984亿元</td><td>~910亿元</td><td class="badge-green">+8%</td></tr>
<tr><td>&nbsp;&nbsp;国内游戏</td><td>473亿元</td><td>~404亿元</td><td class="badge-green">+17%</td></tr>
<tr><td>&nbsp;&nbsp;国际游戏</td><td>186亿元</td><td>~187亿元</td><td class="badge-orange">-1%（恒定汇率+4%）</td></tr>
<tr><td><strong>营销服务（广告）</strong></td><td>435.7亿元</td><td>~357亿元</td><td class="badge-green">+22%</td></tr>
<tr><td><strong>金融科技及企业服务</strong></td><td>602.9亿元</td><td>~553亿元</td><td class="badge-green">+9%</td></tr>
<tr><td><strong>毛利率</strong></td><td>58%</td><td>57%</td><td class="badge-green">+1pp</td></tr>
<tr><td><strong>Non-IFRS经营利润</strong></td><td>756.4亿元</td><td>~694亿元</td><td class="badge-green">+9%</td></tr>
<tr><td>剔除新AI产品后Non-IFRS OP</td><td>861亿元</td><td>~724亿元</td><td class="badge-green">+19%</td></tr>
<tr><td><strong>归母净利润</strong></td><td>560亿元</td><td>~556亿元</td><td class="badge-orange">+0.7%</td></tr>
<tr><td><strong>研发支出</strong></td><td>272.8亿元</td><td>~202亿元</td><td class="badge-green">+35%</td></tr>
<tr><td><strong>资本开支</strong></td><td>527.8亿元</td><td>191亿元</td><td class="badge-green">+176%</td></tr>
<tr><td><strong>自由现金流</strong></td><td>-138亿元</td><td>正值</td><td class="badge-red">转负</td></tr>
<tr><td>剔除AI算力预付款后FCF</td><td>+376亿元</td><td>—</td><td>—</td></tr>
<tr><td><strong>净现金</strong></td><td>582亿元</td><td>746亿元</td><td class="badge-red">-22%</td></tr>
</tbody>
</table>
<p style="font-size:13px;color:#86868b;">数据来源：腾讯控股2026年Q2业绩公告（2026年8月12日发布）；2025年Q2数据为估算值。</p>

<h3>1.2 三大业务引擎解析</h3>

<div class="grid-3">
<div class="card">
<div class="card-title">🚀 广告：AI最强变现引擎</div>
<div class="highlight-num" style="font-size:48px;color:var(--apple-blue)">22%</div>
<p>营销服务收入436亿元，<strong>连续15个季度双位数增长</strong>。AI驱动广告点击率提升15%-22%；"腾讯营销AIM+"覆盖微信小店、短剧等场景，客户覆盖率超80%；素材生产效率提升近80%，制作周期从3天缩短至12小时。视频号广告收入同比增长50%。</p>
</div>
<div class="card">
<div class="card-title">🎮 游戏：AI赋能重回双位数</div>
<div class="highlight-num" style="font-size:48px;color:var(--green)">17%</div>
<p>国内游戏收入473亿元。AI渗透研发→运营→体验全链路。<strong>《和平精英》AINPC</strong>累计体验用户1.67亿，最高日活1770万。《三角洲行动》用Hy3D模型大幅降低场景制作成本。</p>
</div>
<div class="card">
<div class="card-title">☁️ 云服务：AI需求直推增长</div>
<div class="highlight-num" style="font-size:48px;color:var(--orange)">20%+</div>
<p>金融科技及企业服务收入603亿元（+9%），其中<strong>云服务增速超20%</strong>。AI相关服务占云收入25%-30%。MaaS平台TokenHub日Token使用量达25万亿，两月增5倍。</p>
</div>
</div>

<h3>1.3 CapEx解读：528亿花在哪里？</h3>
<p>Q2资本开支527.8亿元，同比增长176%，环比增长65%，远超市场预期的321亿元。上半年累计847.2亿元，已超过2025年全年（767.6亿元）和2024年全年（792亿元）。这是一个信号性数字。</p>

<table>
<thead><tr><th>投入方向</th><th>优先级</th><th>说明</th></tr></thead>
<tbody>
<tr><td><strong>GPU算力采购</strong></td><td>核心</td><td>预付大额订单锁定算力，刘炽平称转手可获>30%溢价</td></tr>
<tr><td><strong>AI数据中心</strong></td><td>核心</td><td>自建IDC，液冷散热、高密度服务器部署</td></tr>
<tr><td><strong>混元大模型</strong></td><td>P0</td><td>Hy3正式版已上线（2950亿MoE参数），Hy4近期发布</td></tr>
<tr><td><strong>WorkBuddy推理</strong></td><td>P1</td><td>PC端月访问量2097万次，国内同类第一</td></tr>
<tr><td><strong>CodeBuddy</strong></td><td>P2</td><td>企业级AI编程工具，国内领先</td></tr>
<tr><td><strong>微信AI（小微）</strong></td><td>P2</td><td>WeLM驱动，灰度测试中，成本可控</td></tr>
</tbody>
</table>

<div class="insight-box">
<p><strong>💡 算力分配优先级（管理层原话）：</strong>"先自研模型训练 → 再自有AI应用推理 → 最后剩余算力对外出租"。刘炽平表示，预付算力订单目前转手可获超30%利润，但腾讯选择不走短期套利路径，而是将算力用于模型训练和应用推理的长期目标。</p>
<p><strong>关键数据：</strong>自由现金流-138亿元中，AI算力采购预付款是主因。剔除预付款后FCF为+376亿元，说明主营业务造血能力依然强劲。</p>
</div>

</div>
</div>
""")

# Part 4: Section 2 - AI Investment Breakdown
parts.append("""
<div class="section-dark" id="s2">
<div class="container">
<h2 class="section-title">二、AI投入深度拆解</h2>
<p class="section-subtitle">从"战略叙事"到"财报兑现"的三条变现路径</p>

<h3>2.1 AI变现路径一：广告增效（已兑现）</h3>
<p>广告是腾讯AI变现最确定、见效最快的赛道。核心逻辑：<strong>13亿微信日活 × AI提升点击率 = 指数级广告增量</strong>。</p>

<table>
<thead><tr><th>AI广告能力</th><th>具体数据</th><th>来源</th></tr></thead>
<tbody>
<tr><td>AI推荐模型优化</td><td>广告点击率提升15%-22%</td><td>管理层Q2电话会</td></tr>
<tr><td>AIM+智能投放</td><td>客户覆盖率超80%</td><td>财报披露</td></tr>
<tr><td>AI创意生成</td><td>素材生产效率提升近80%</td><td>财报披露</td></tr>
<tr><td>制作周期</td><td>从3天缩短至12小时</td><td>财报披露</td></tr>
<tr><td>视频号广告</td><td>收入同比增长50%</td><td>Q2财报</td></tr>
<tr><td>小程序小店广告</td><td>收入同比增长50%</td><td>Q2财报</td></tr>
<tr><td>微信搜索广告</td><td>收入同比增长60%</td><td>Q2财报</td></tr>
<tr><td>连续季度增长</td><td>连续15个季度双位数增长</td><td>历史数据</td></tr>
</tbody>
</table>

<div class="insight-box">
<p><strong>💡 广告是腾讯AI的"印钞机"：</strong>正如36氪分析所述，"元宝产品好不好不重要，腾讯根本没有在订阅上下注的动力。13亿微信日活，每提升一个点击率百分点，就是几十亿广告增量。订阅跟这个比，是蚂蚱和大象。"管理层马化腾明确表示："AI技术在广告定向方面的应用持续深化，推动了整体业绩提升。"</p>
</div>

<h3>2.2 AI变现路径二：云服务（正在兑现）</h3>
<p>腾讯云是AI投入中最接近规模化收入兑现的板块。</p>
<ul>
<li>Q1企业服务收入同比增20%，其中<strong>云收入同比增40%</strong>（远高于集团整体增速）</li>
<li>AI相关服务占云收入<strong>25%-30%</strong>，云毛利率提升至<strong>35%以上</strong></li>
<li>MaaS平台TokenHub日Token使用量达<strong>25万亿</strong>，两个月增长5倍</li>
<li>WorkBuddy付费用户毛利率<strong>已接近腾讯云整体水平</strong></li>
<li>管理层James Mitchell表示："国内Token生产成本远低于外界认知，Token业务在当前低价下也能保持正毛利"</li>
</ul>

<h3>2.3 AI变现路径三：游戏AI（已渗透，增长中）</h3>
<p>AI已深度渗透腾讯游戏研发、运营、玩家体验全链路，是AI技术落地变现的核心场景之一。</p>
<table>
<thead><tr><th>维度</th><th>案例</th><th>效果</th></tr></thead>
<tbody>
<tr><td><strong>研发端</strong></td><td>《三角洲行动》Hy3D模型</td><td>端手一体化生产管线，大幅降低场景制作成本</td></tr>
<tr><td><strong>运营端</strong></td><td>智能体Agent</td><td>提升版本迭代与活动运营效率</td></tr>
<tr><td><strong>体验端</strong></td><td>《和平精英》AINPC</td><td>累计体验用户1.67亿，最高日活1770万</td></tr>
<tr><td><strong>增长</strong></td><td>国内游戏收入</td><td>473亿元，同比+17%，重回双位数</td></tr>
</tbody>
</table>

<h3>2.4 模型能力：混元Hy系列进展</h3>
<table>
<thead><tr><th>模型</th><th>参数规模</th><th>关键指标</th><th>状态</th></tr></thead>
<tbody>
<tr><td><strong>Hy3正式版</strong></td><td>2950亿（MoE）</td><td>OpenRouter Token消耗量全球前三</td><td>已上线</td></tr>
<tr><td><strong>Hy3 vs 海外旗舰</strong></td><td>2950亿</td><td>比肩2-5倍参数规模旗舰模型</td><td>持续优化</td></tr>
<tr><td><strong>Hy3正式版调用量</strong></td><td>—</td><td>日均Token用量为preview版的7倍</td><td>已验证</td></tr>
<tr><td><strong>Hy4</strong></td><td>更大规模</td><td>多模态能力升级</td><td>近期上线</td></tr>
</tbody>
</table>

</div>
</div>
""")

# Part 5: Section 3 - Domestic Comparison
parts.append("""
<div class="section-light" id="s3">
<div class="container">
<h2 class="section-title">三、国内科技巨头AI投入对比</h2>
<p class="section-subtitle">腾讯 vs 阿里 vs 字节跳动 vs 百度——四种路径，一个共识</p>

<h3>3.1 四大巨头2026年资本开支对比</h3>
<table>
<thead><tr><th>公司</th><th>2026年CapEx指引</th><th>YoY变化</th><th>核心投向</th><th>战略路径</th></tr></thead>
<tbody>
<tr><td><strong>字节跳动</strong></td><td>~2000亿元</td><td>+25%（原1600亿上调）</td><td>GPU集群、豆包大模型、AI芯片</td><td>内部消化+对外MaaS并重</td></tr>
<tr><td><strong>腾讯</strong></td><td>~2100亿元（高盛预测）</td><td>+174%</td><td>GPU算力、Hy模型、WorkBuddy、微信AI</td><td>自用优先，出租兜底</td></tr>
<tr><td><strong>阿里巴巴</strong></td><td>3800亿（三年规划，2025-2027）</td><td>年均~1267亿</td><td>云基础设施、AI芯片（70%国产）</td><td>云即底盘，算力对外出租</td></tr>
<tr><td><strong>百度</strong></td><td>~400亿元</td><td>持续增长</td><td>昆仑芯、智能云AI基础设施</td><td>自研芯片+云服务</td></tr>
</tbody>
</table>

<h3>3.2 路径分化：三种模式</h3>
<div class="grid-3">
<div class="card">
<div class="card-title">路径A：云即底盘</div>
<h4 style="margin-top:0">阿里 & 百度</h4>
<p>云是核心业务，算力对外租赁是原生主营。阿里云AI相关产品收入占比已突破30%。百度自研昆仑芯降低对GPU依赖。</p>
<span class="tag tag-blue">算力即商品</span>
</div>
<div class="card">
<div class="card-title">路径B：自用优先</div>
<h4 style="margin-top:0">腾讯</h4>
<p>云非第一优先级，新增算力优先保障混元、WorkBuddy、微信AI。剩余算力才考虑出租。管理层明确"模型优先，出租是退路"。</p>
<span class="tag tag-green">算力即壁垒</span>
</div>
<div class="card">
<div class="card-title">路径C：混合模式</div>
<h4 style="margin-top:0">字节跳动</h4>
<p>内部业务算力混部，对外MaaS与算力租赁并重。豆包月活3.45亿（2026年3月），但已开始探索订阅付费。</p>
<span class="tag tag-orange">算力即生态</span>
</div>
</div>

<h3>3.3 AI用户规模对比</h3>
<table>
<thead><tr><th>产品</th><th>月活用户（MAU）</th><th>数据时间</th></tr></thead>
<tbody>
<tr><td><strong>字节豆包</strong></td><td>3.45亿</td><td>2026年3月（QuestMobile）</td></tr>
<tr><td><strong>阿里千问</strong></td><td>1.66亿</td><td>2026年3月</td></tr>
<tr><td><strong>DeepSeek</strong></td><td>1.27亿（后增至1.45亿）</td><td>2026年3月/Q3</td></tr>
<tr><td><strong>腾讯元宝</strong></td><td>3286万-1.14亿（春节峰值）</td><td>2025年Q3/2026年春节</td></tr>
<tr><td><strong>腾讯WorkBuddy</strong></td><td>~2000万</td><td>2026年6月</td></tr>
</tbody>
</table>

<div class="insight-box">
<p><strong>💡 腾讯的"慢"与"快"：</strong>元宝月活不及豆包的零头，但腾讯的AI变现逻辑与其他三家截然不同——<strong>它不靠C端AI应用订阅赚钱</strong>。腾讯真正的"AI印钞机"是广告（22%增速）和游戏（17%增速），AI助手只是能力载体。WorkBuddy月访问量2097万次已领跑国内PC端办公AI赛道，但管理层已明确将资源向WorkBuddy倾斜，降低元宝等产品的优先级。</p>
</div>

</div>
</div>
""")

# Part 6: Section 4 - Global AI Arms Race
parts.append("""
<div class="section-black" id="s4">
<div class="container">
<h2 class="section-title" style="color:white">四、全球AI军备竞赛</h2>
<p class="section-subtitle">2026年九大CSP合计CapEx 8300亿美元，腾讯在全球坐标系中的位置</p>

<h3 style="color:white">4.1 全球九大CSP资本支出总览（2026年）</h3>
<table>
<thead><tr><th>公司</th><th>2026 CapEx指引</th><th>YoY变化</th><th>核心投向</th></tr></thead>
<tbody>
<tr><td><strong>Amazon/AWS</strong></td><td>~$2,200亿</td><td>+50%+</td><td>Trainium/Inferentia自研芯片、边缘AI</td></tr>
<tr><td><strong>Microsoft</strong></td><td>~$1,900亿</td><td>+130%</td><td>Azure AI数据中心（>60%用于AI）</td></tr>
<tr><td><strong>Alphabet/Google</strong></td><td>$1,950-2,050亿</td><td>+100%+</td><td>TPU v6、Gemini训练、Google Cloud</td></tr>
<tr><td><strong>Meta</strong></td><td>$1,250-1,450亿</td><td>+85%</td><td>Llama系列训练、AI推荐引擎</td></tr>
<tr><td><strong>Oracle</strong></td><td>显著增长</td><td>—</td><td>OCI AI基础设施</td></tr>
<tr><td><strong>字节跳动</strong></td><td>~2000亿元（$275亿）</td><td>+25%</td><td>GPU集群、豆包大模型</td></tr>
<tr><td><strong>腾讯</strong></td><td>~2100亿元（$290亿）</td><td>+174%</td><td>GPU、Hy模型、AI应用</td></tr>
<tr><td><strong>阿里巴巴</strong></td><td>~1267亿元（$175亿）</td><td>三年3800亿</td><td>云基础设施、AI芯片</td></tr>
<tr><td><strong>百度</strong></td><td>~400亿元（$55亿）</td><td>持续增长</td><td>昆仑芯、智能云</td></tr>
</tbody>
</table>
<p style="font-size:13px;color:#86868b;">数据来源：TrendForce集邦咨询2026年5月报告、各公司财报/指引。九大CSP合计CapEx预估~8,300亿美元，YoY +79%。</p>

<h3 style="color:white">4.2 美国四巨头的"回报叙事"</h3>
<p>2026年Q2是全球科技巨头首次集体正面回应"AI CapEx回报"质疑的财报季：</p>

<div class="grid-2">
<div class="card-dark">
<div class="card-title">📈 Microsoft：AI回报的标杆</div>
<ul>
<li>Q2营收$119.8B（+24%）</li>
<li>Azure AI已达<strong>$25B+年化收入</strong>，三位数增长</li>
<li>Copilot和Azure已在<strong>今天</strong>产生现金回报</li>
<li>管理层称CapEx将在2027年前保持舒适正现金流</li>
<li>市场奖励：竞争对手股价跌时，微软逆势上涨</li>
</ul>
</div>
<div class="card-dark">
<div class="card-title">📈 Amazon/AWS：利润率逆势扩张