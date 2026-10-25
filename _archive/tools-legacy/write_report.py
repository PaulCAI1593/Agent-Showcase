#!/usr/bin/env python3
import os
os.makedirs('/app/working/shared/showcase', exist_ok=True)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tencent 528B AI Bet Report</title>
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
h3{font-size:28px;font-weight:600;line-height:1.14;letter-spacing:-0.01em;margin-bottom:16px;margin-top:48px}
p{font-size:17px;line-height:1.47;letter-spacing:-0.374px;margin-bottom:20px;color:#1d1d1f}
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
.verdict-box h3{color:white}
.verdict-box p{color:#d2d2d7}
@media(max-width:768px){.hero h1{font-size:36px}.section-title{font-size:28px}.grid-3,.grid-4{grid-template-columns:1fr}.grid-2{grid-template-columns:1fr}.highlight-num{font-size:48px}}
</style>
</head>
<body>
<div class="hero">
<div class="meta"><span>&#x1F4CA; 深度研究报告</span><span>|</span><span>2026年8月15日</span><span>|</span><span>&#x1F4B0;经济 &#x1F916;技术 &#x1F3ED;产业</span></div>
<br><br>
<h1>腾讯528亿"赌注"</h1>
<p class="subtitle">AI投入从战略叙事到财报兑现的拐点——Q2财报深度解读与全球科技巨头AI军备竞赛全景分析</p>
</div>

<div class="section-dark">
<div class="container">
<h2 class="section-title">执行摘要</h2>
<p class="section-subtitle">一份数据驱动的战略判断</p>
<div class="grid-4">
<div><div class="highlight-num" style="color:var(--apple-blue)">528<span style="font-size:36px">亿</span></div><div class="highlight-label">Q2资本开支 <span class="comparison-arrow arrow-up">+176%</span></div></div>
<div><div class="highlight-num" style="color:var(--green)">2048<span style="font-size:36px">亿</span></div><div class="highlight-label">Q2总营收 <span class="comparison-arrow arrow-up">+11%</span></div></div>
<div><div class="highlight-num" style="color:var(--orange)">273<span style="font-size:36px">亿</span></div><div class="highlight-label">Q2研发支出 <span class="comparison-arrow arrow-up">+35%</span></div></div>
<div><div class="highlight-num" style="color:var(--red)">-138<span style="font-size:36px">亿</span></div><div class="highlight-label">自由现金流</div></div>
</div>
<div class="insight-box">
<p><strong>核心判断：</strong>腾讯2026年Q2财报标志着其AI战略从"叙事期"进入"投入兑现期"的关键拐点。单季528亿元资本开支（YoY +176%）不仅超过2019-2023年任一整年，更令上半年累计847亿元超越2025全年。AI已非成本中心——广告业务22%增速中AI贡献过半，云服务受AI需求拉动增速超20%，游戏AI用户累计1.67亿。但自由现金流转负、净利润增速仅0.7%表明：腾讯正在用今天的利润，买下一轮十年的增长。</p>
<p><strong>风险提示：</strong>2026-2028年年均CapEx预计超2000亿元，折旧将持续压制利润表。模型迭代若慢于硬件折旧周期，巨额算力投资面临贬值风险。</p>
</div>
</div>
</div>
"""

with open('/app/working/shared/showcase/2026-08-15-tencent-ai-bet.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Part 1 written")
