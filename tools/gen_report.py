#!/usr/bin/env python3
"""Generate the Tencent AI Bet HTML report."""
import os

OUT = '/app/working/shared/showcase/2026-08-15-tencent-ai-bet.html'

parts = []

parts.append(r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>腾讯528亿AI赌注</title>
<style>
:root{--black:#000;--light-gray:#f5f5f7;--near-black:#1d1d1f;--apple-blue:#0071e3;--white:#fff;--green:#34c759;--red:#ff3b30;--orange:#ff9500}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;color:var(--near-black);background:var(--white);line-height:1.47;-webkit-font-smoothing:antialiased}
.hero{background:var(--black);color:var(--white);padding:120px 24px 100px;text-align:center}
.hero h1{font-size:56px;font-weight:600;line-height:1.07;max-width:980px;margin:0 auto 24px}
.hero .subtitle{font-size:21px;color:#86868b;max-width:700px;margin:0 auto 40px;line-height:1.38}
.hero .meta{font-size:14px;color:#86868b}.hero .meta span{margin:0 12px}
.container{max-width:980px;margin:0 auto;padding:0 24px}
.section-light{background:var(--white);padding:100px 24px}
.section-dark{background:var(--light-gray);padding:100px 24px}
.section-black{background:var(--black);color:var(--white);padding:100px 24px}
.section-title{font-size:40px;font-weight:600;line-height:1.1;margin-bottom:12px}
.section-subtitle{font-size:21px;color:#86868b;margin-bottom:56px;line-height:1.38}
h3{font-size:28px;font-weight:600;line-height:1.14;margin-bottom:16px;margin-top:56px}
p{font-size:17px;line-height:1.47;margin-bottom:20px;color:#1d1d1f}
.section-black p{color:#d2d2d7}
.highlight-num{font-size:72px;font-weight:700;line-height:1.05;letter-spacing:-0.04em}
.highlight-label{font-size:17px;color:#86868b;margin-top:4px}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;margin-bottom:48px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-bottom:48px}
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:32px;margin-bottom:48px}
.card{background:rgba(255,255,255,0.08);border-radius:20px;padding:32px}
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
.verdict-box h3{color:white}.verdict-box p{color:#d2d2d7}
@media(max-width:768px){.hero h1{font-size:36px}.section-title{font-size:28px}.grid-3,.grid-4{grid-template-columns:1fr}.highlight-num{font-size:48px}}
</style>
</head>
<body>
''')

# HERO
parts.append('''
<div class="hero">
<div class="meta"><span>\U0001F4CA 深度研究报告</span><span>|</span><span>2026年8月15日</span><span>|</span><span>\U0001F4B0经济 \U0001F916技术 \U0001F3ED产业</span></div>
<br><br>
<h1>腾讯528亿"赌注"</h1>
<p class="subtitle">AI投入从战略叙事到财报兑现的拐点<br>Q2财报深度解读与全球科技巨头AI军备竞赛全景分析</p>
</div>
''')

# EXECUTIVE SUMMARY
parts.append('''
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
<p><strong>核心判断：</strong>腾讯2026年Q2财报标志着其AI战略从"叙事期"进入"投入兑现期"的关键拐点。单季528亿元资本开支（YoY +176%）不仅超过2019-2023年任一整年，更令上半年累计847亿元超越2025全年（767.6亿）。AI已非成本中心——广告业务22%增速中AI贡献过半，云服务受AI需求拉动增速超20%，游戏AI用户累计1.67亿。但自由现金流转负、净利润增速仅0.7%表明：<strong>腾讯正在用今天的利润，买下一轮十年的增长。</strong></p>
<p><strong>风险提示：</strong>2026-2028年年均CapEx预计超2000亿元（高盛预测），折旧将持续压制利润表。模型迭代若慢于硬件折旧周期（2.5-3年），巨额算力投资面临贬值风险。</p>
</div>
</div>
</div>
''')

# SECTION 1: Q2 FINANCIAL
parts.append('''
<div class="section-light">
<div class="container">
<h2 class="section-title">一、Q2财报全景透视</h2>
<p class="section-subtitle">从营收结构看AI如何渗透腾讯每一寸业务</p>

<h3>1.1 核心财务数据总览</h3>
<table>
<thead><tr><th>指标</th><th>Q2 2026</th><th>Q2 2025</th><th>同比变化</th></tr></thead>
<tbody>
<tr><td><strong>总营收</strong></td><td>2,047.9亿元</td><td>1,845亿元</td><td class="badge-green">+11%</td></tr>
<tr><td><strong>增值服务（VAS）</strong></td><td>984亿元</td><td>914亿元</td><td class="badge-green">+8%</td></tr>
<tr><td>&nbsp;&nbsp;国内游戏</td><td>473亿元</td><td>404亿元</td><td class="badge-green">+17%</td></tr>
<tr><td>&nbsp;&nbsp;国际游戏</td><td>186亿元</td><td>187亿元</td><td class="badge-orange">-1%（固定汇率+4%）</td></tr>
<tr><td><strong>营销服务（广告）</strong></td><td>435.7亿元</td><td>357亿元</td><td class="badge-green">+22%</td></tr>
<tr><td><strong>金融科技及企业服务</strong></td><td>602.9亿元</td><td>555亿元</td><td class="badge-green">+9%</td></tr>
<tr><td><strong>毛利</strong></td><td>1,184亿元</td><td>1,048亿元</td><td class="badge-green">+13%</td></tr>
<tr><td><strong>毛利率</strong></td><td>58%</td><td>57%</td><td class="badge-green">+1pp</td></tr>
<tr><td><strong>Non-IFRS经营利润</strong></td><td>756.4亿元</td><td>694亿元</td><td class="badge-green">+9%</td></tr>
<tr><td>剔除新AI产品后</td><td>861亿元</td><td>724亿元</td><td class="badge-green">+19%</td></tr>
<tr><td><strong>Non-IFRS净利润</strong></td><td>684亿元</td><td>631亿元</td><td class="badge-green">+9%</td></tr>
<tr><td><strong>净利润（归母）</strong></td><td>560亿元</td><td>556亿元</td><td class="badge-orange">+0.7%</td></tr>
<tr><td><strong>研发支出</strong></td><td>272.8亿元</td><td>202亿元</td><td class="badge-green">+35%</td></tr>
<tr><td><strong>资本开支</strong></td><td>527.8亿元</td><td>191亿元</td><td class="badge-green">+176%</td></tr>
<tr><td><strong>自由现金流</strong></td><td>-138亿元</td><td>正数</td><td class="badge-red">转负</td></tr>
<tr><td><strong>净现金</strong></td><td>582亿元</td><td>746亿元</td><td class="badge-red">-22%</td></tr>
<tr><td>微信/WeChat月活</td><td>14.39亿</td><td>14.11亿</td><td class="badge-green">+2%</td></tr>
</tbody>
</table>
<p style="font-size:13px;color:#86868b;">数据来源：腾讯控股2026年第二季度业绩公告（2026年8月12日发布）</p>

<h3>1.2 AI投入全景：528亿花在哪里？</h3>
<p>Q2腾讯资本开支527.8亿元中，绝大部分流向AI基础设施建设。上半年累计资本开支847亿元，已超越2025全年（767.6亿元）和2024全年（791.98亿元）。这是腾讯历史上最激进的一轮投资周期。</p>

<table>
<thead><tr><th>投入方向</th><th>规模/指标</th><th>说明</th></tr></thead>
<tbody>
<tr><td><strong>GPU算力采购</strong></td><td>占CapEx主体</td><td>优先自用。刘炽平称预付算力订单转手可获>30%溢价，但腾讯放弃短期套利，选择自用优先路线</td></tr>
<tr><td><strong>AI数据中心</strong></td><td>集中扩建</td><td>自建IDC，液冷散热、高密度服务器部署。GPU商用黄金周期约2.5-3年</td></tr>
<tr><td><strong>混元大模型</strong></td><td>第一优先级</td><td>Hy3正式版（2950亿MoE参数）已上线，OpenRouter Token消耗全球前三；Hy4近期发布</td></tr>
<tr><td><strong>WorkBuddy</strong></td><td>第二优先级</td><td>6月PC端访问量2097万次（国内同类第一），MAU达2000万级，接入Hy3后任务解决率72%→90%</td></tr>
<tr><td><strong>CodeBuddy</strong></td><td>AI编程工具</td><td>企业级AI编程助手，稳居国内领先水平</td></tr>
<tr><td><strong>微信AI（小微）</strong></td><td>灰度测试</td><td>WeLM驱动，已扩展至朋友圈（AI帮写/AI点评）。管理层称投入规模低于元宝，成本可控</td></tr>
</tbody>
</table>

<div class="insight-box">
<p><strong>\U0001F4A1 算力分配优先级（管理层原话）：</strong>"先自研模型训练 → 再自有AI应用推理 → 最后剩余算力对外出租"。这代表腾讯选择了一条<strong>自用优先、出租兜底</strong>的战略路径。刘炽平明确表示："如果今天把商业模式直接改成单纯出租算力，那不仅不会亏损，反而是盈利的。"</p>
</div>

<h3>1.3 三大引擎：广告、游戏、云</h3>
<div class="grid-3">
<div class="card" style="background:#f5f5f7;">
<div class="card-title">\U0001F680 广告：AI最强变现引擎</div>
<div class="highlight-num" style="font-size:48px;color:var(--apple-blue)">22%</div>
<p>营销服务收入436亿元，<strong>连续15个季度双位数增长</strong>。AI驱动广告点击率提升15%-22%；"腾讯营销AIM+"客户覆盖率超80%；素材生产效率提升近80%。视频号/小程序/微信搜索广告收入分别同比增长50%/50%/60%。</p>
</div>
<div class="card" style="background:#f5f5f7;">
<div class="card-title">\U0001F3AE 游戏：AI赋能重回双位数</div>
<div class="highlight-num" style="font-size:48px;color:var(--green)">17%</div>
<p>国内游戏收入473亿元。AI渗透研发→运营→体验全链路：<strong>《三角洲行动》</strong>用Hy3D降低场景成本；<strong>《和平精英》AINPC</strong>累计用户<strong>1.67亿</strong>，最高日活1770万。</p>
</div>
<div class="card" style="background:#f5f5f7;">
<div class="card-title">\u2601\uFE0F 云服务：AI需求直推增长</div>
<div class="highlight-num" style="font-size:48px;color:var(--orange)">&gt;20%</div>
<p>金融科技及企业服务收入603亿元（+9%），其中<strong>云服务增速超20%</strong>。AI相关服务占云收入25%-30%。TokenHub日Token使用量达25万亿，两月增长5倍。云毛利率提升至35%以上。</p>
</div>
</div>
</div>
</div>
''')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(''.join(parts))
print(f"Part 1 written: {os.path.getsize(OUT)} bytes")
