#!/usr/bin/env python3
"""Build AI Compute Explosion interactive HTML experience."""
import os

OUTPUT = "/app/working/shared/showcase/2026-09-03-ai-compute-explosion.html"

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI算力消耗的指数级爆发：从1000亿到500万亿Token的3年迁徙</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
--blue:#0071e3;--green:#00c853;--cyan:#00e5ff;
--bg-dark:#0a0a0f;--bg-card:#111118;--bg-card2:#16161f;
--text:#e8e8ed;--text-dim:#86868b;--text-bright:#f5f5f7;
}
html{scroll-behavior:smooth}
body{
font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue",Arial,sans-serif;
background:var(--bg-dark);color:var(--text);overflow-x:hidden;line-height:1.6;
}
::selection{background:var(--blue);color:#fff}

/* ═══ Particle Canvas ═══ */
#particles{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none}

/* ═══ Navigation ═══ */
nav{
position:fixed;top:0;left:0;right:0;z-index:100;
background:rgba(10,10,15,0.72);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
border-bottom:1px solid rgba(255,255,255,0.06);
padding:14px 32px;display:flex;justify-content:space-between;align-items:center;
transition:transform .3s;
}
nav.hidden{transform:translateY(-100%)}
nav .logo{font-size:15px;font-weight:600;color:var(--text-bright);letter-spacing:.5px}
nav .logo span{color:var(--blue)}
nav .nav-links{display:flex;gap:24px}
nav .nav-links a{color:var(--text-dim);text-decoration:none;font-size:13px;font-weight:500;transition:color .2s}
nav .nav-links a:hover{color:var(--blue)}

/* ═══ Sections ═══ */
section{position:relative;z-index:1;min-height:100vh;display:flex;align-items:center;justify-content:center}
.container{max-width:980px;margin:0 auto;padding:0 24px;width:100%}

/* ═══ Hero ═══ */
#hero{min-height:100vh;text-align:center;flex-direction:column}
#hero .tag{
display:inline-block;padding:6px 16px;border-radius:20px;
background:rgba(0,113,227,0.12);color:var(--blue);font-size:13px;font-weight:600;
margin-bottom:24px;letter-spacing:.5px;
}
#hero h1{
font-size:clamp(36px,7vw,72px);font-weight:700;line-height:1.05;
letter-spacing:-1.5px;color:var(--text-bright);margin-bottom:20px;
}
#hero h1 .highlight{
background:linear-gradient(135deg,var(--blue),var(--cyan));
-webkit-background-clip:text;-webkit-text-fill-color:transparent;
background-clip:text;
}
#hero .subtitle{
font-size:clamp(16px,2.5vw,22px);color:var(--text-dim);max-width:680px;
margin:0 auto 40px;font-weight:400;line-height:1.5;
}
#hero .scroll-hint{
position:absolute;bottom:40px;left:50%;transform:translateX(-50%);
display:flex;flex-direction:column;align-items:center;gap:8px;
color:var(--text-dim);font-size:12px;animation:bounce 2s infinite;
}
@keyframes bounce{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(-10px)}}
#hero .scroll-hint .arrow{width:20px;height:20px;border-right:2px solid var(--text-dim);border-bottom:2px solid var(--text-dim);transform:rotate(45deg)}

/* ═══ Big Number Counter ═══ */
.big-number{
font-size:clamp(48px,10vw,120px);font-weight:800;
background:linear-gradient(135deg,var(--blue),var(--green));
-webkit-background-clip:text;-webkit-text-fill-color:transparent;
background-clip:text;line-height:1;margin:20px 0;
font-variant-numeric:tabular-nums;
}
.unit{font-size:clamp(18px,3vw,32px);font-weight:400;-webkit-text-fill-color:var(--text-dim)}

/* ═══ Section Headers ═══ */
.section-header{text-align:center;margin-bottom:60px}
.section-header .label{
font-size:13px;font-weight:600;color:var(--blue);text-transform:uppercase;
letter-spacing:2px;margin-bottom:12px;
}
.section-header h2{
font-size:clamp(28px,5vw,48px);font-weight:700;color:var(--text-bright);
letter-spacing:-.8px;line-height:1.1;margin-bottom:16px;
}
.section-header p{font-size:17px;color:var(--text-dim);max-width:600px;margin:0 auto}

/* ═══ Timeline ═══ */
#timeline{background:linear-gradient(180deg,var(--bg-dark) 0%,#0d0d14 100%);padding:120px 0}
.timeline-track{position:relative;padding:40px 0}
.timeline-line{
position:absolute;left:50%;top:0;bottom:0;width:2px;
background:linear-gradient(180deg,transparent,var(--blue),var(--green),transparent);
transform:translateX(-50%);
}
.timeline-nodes{display:flex;flex-direction:column;gap:80px;position:relative}
.timeline-node{
display:flex;align-items:flex-start;gap:40px;position:relative;
cursor:pointer;transition:transform .3s;
}
.timeline-node:hover{transform:translateX(8px)}
.timeline-node:nth-child(even){flex-direction:row-reverse;text-align:right}
.timeline-node:nth-child(even):hover{transform:translateX(-8px)}
.timeline-dot{
width:24px;height:24px;border-radius:50%;flex-shrink:0;
background:var(--bg-dark);border:3px solid var(--blue);
position:relative;z-index:2;margin-top:8px;
transition:all .3s;
}
.timeline-node:hover .timeline-dot,.timeline-node.active .timeline-dot{
background:var(--blue);box-shadow:0 0 20px rgba(0,113,227,0.5);
}
.timeline-content{flex:1;max-width:calc(50% - 60px)}
.timeline-year{
font-size:14px;font-weight:700;color:var(--blue);letter-spacing:1px;margin-bottom:8px;
}
.timeline-title{
font-size:clamp(20px,3vw,28px);font-weight:700;color:var(--text-bright);margin-bottom:8px;
}
.timeline-desc{font-size:15px;color:var(--text-dim);line-height:1.6}
.timeline-data{
margin-top:16px;padding:16px 20px;border-radius:12px;
background:var(--bg-card);border:1px solid rgba(255,255,255,0.06);
display:none;
}
.timeline-node.active .timeline-data{display:block;animation:fadeSlideUp .4s ease}
@keyframes fadeSlideUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.timeline-data .data-item{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04)}
.timeline-data .data-item:last-child{border-bottom:none}
.timeline-data .data-label{color:var(--text-dim);font-size:14px}
.timeline-data .data-value{color:var(--text-bright);font-weight:600;font-size:14px;font-variant-numeric:tabular-nums}

/* ═══ Data Cards ═══ */
#data-explosion{background:var(--bg-dark);padding:120px 0}
.data-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:40px}
.data-card{
background:var(--bg-card);border-radius:16px;padding:32px;
border:1px solid rgba(255,255,255,0.06);
transition:transform .3s,border-color .3s;position:relative;overflow:hidden;
}
.data-card:hover{transform:translateY(-4px);border-color:rgba(0,113,227,0.3)}
.data-card::before{
content:'';position:absolute;top:0;left:0;right:0;height:3px;
background:linear-gradient(90deg,var(--blue),var(--green));
opacity:0;transition:opacity .3s;
}
.data-card:hover::before{opacity:1}
.data-card .card-icon{font-size:28px;margin-bottom:16px}
.data-card .card-value{
font-size:36px;font-weight:800;color:var(--text-bright);
margin-bottom:4px;font-variant-numeric:tabular-nums;
}
.data-card .card-label{font-size:14px;color:var(--text-dim);margin-bottom:12px}
.data-card .card-change{
display:inline-block;padding:4px 10px;border-radius:8px;
font-size:12px;font-weight:600;
background:rgba(0,200,83,0.12);color:var(--green);
}

/* ═══ Charts ═══ */
#charts{background:linear-gradient(180deg,#0d0d14,var(--bg-dark));padding:120px 0}
.chart-container{
background:var(--bg-card);border-radius:16px;padding:32px;margin-bottom:32px;
border:1px solid rgba(255,255,255,0.06);
}
.chart-title{font-size:18px;font-weight:600;color:var(--text-bright);margin-bottom:8px}
.chart-subtitle{font-size:13px;color:var(--text-dim);margin-bottom:24px}
.bar-chart{display:flex;align-items:flex-end;gap:12px;height:260px;padding-top:20px}
.bar-group{flex:1;display:flex;flex-direction:column;align-items:center;gap:8px;height:100%;justify-content:flex-end}
.bar{
width:100%;border-radius:6px 6px 0 0;min-width:32px;
transition:height 1.2s cubic-bezier(.22,1,.36,1);
position:relative;cursor:pointer;
}
.bar:hover{filter:brightness(1.2)}
.bar .bar-value{
position:absolute;top:-28px;left:50%;transform:translateX(-50%);
font-size:11px;font-weight:700;color:var(--text-bright);white-space:nowrap;
font-variant-numeric:tabular-nums;
}
.bar .bar-label{
font-size:11px;color:var(--text-dim);text-align:center;margin-top:8px;
position:absolute;bottom:-24px;left:50%;transform:translateX(-50%);white-space:nowrap;
}
.bar-group{position:relative;padding-bottom:28px}

/* ═══ VS Compare ═══ */
#compare{background:var(--bg-dark);padding:120px 0}
.compare-container{
background:var(--bg-card);border-radius:16px;overflow:hidden;
border:1px solid rgba(255,255,255,0.06);
}
.compare-tabs{display:flex;border-bottom:1px solid rgba(255,255,255,0.06)}
.compare-tab{
flex:1;padding:16px;text-align:center;font-size:15px;font-weight:600;
color:var(--text-dim);cursor:pointer;transition:all .3s;position:relative;
}
.compare-tab.active{color:var(--text-bright)}
.compare-tab.active::after{
content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
background:var(--blue);
}
.compare-panels{padding:32px}
.compare-panel{display:none;animation:fadeSlideUp .4s ease}
.compare-panel.active{display:block}
.compare-row{display:flex;gap:24px;margin-bottom:20px;flex-wrap:wrap}
.compare-col{flex:1;min-width:200px}
.compare-col h4{font-size:14px;font-weight:600;color:var(--blue);margin-bottom:12px}
.compare-stat{
padding:16px;border-radius:12px;background:var(--bg-card2);
margin-bottom:12px;
}
.compare-stat .stat-label{font-size:12px;color:var(--text-dim);margin-bottom:4px}
.compare-stat .stat-value{font-size:22px;font-weight:700;color:var(--text-bright);font-variant-numeric:tabular-nums}
.compare-stat .stat-bar{height:4px;border-radius:2px;background:rgba(255,255,255,0.06);margin-top:8px;overflow:hidden}
.compare-stat .stat-fill{height:100%;border-radius:2px;transition:width 1s ease}

/* ═══ Energy ═══ */
#energy{background:linear-gradient(180deg,#0d0d14,#080810);padding:120px 0}
.energy-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin-top:40px}
.energy-card{
background:var(--bg-card);border-radius:16px;padding:28px;text-align:center;
border:1px solid rgba(255,255,255,0.06);transition:transform .3s;
}
.energy-card:hover{transform:translateY(-4px)}
.energy-card .energy-icon{font-size:36px;margin-bottom:12px}
.energy-card .energy-value{
font-size:32px;font-weight:800;margin-bottom:4px;
font-variant-numeric:tabular-nums;
}
.energy-card .energy-label{font-size:13px;color:var(--text-dim);margin-bottom:8px}
.energy-card .energy-compare{font-size:12px;color:var(--text-dim);line-height:1.4}
.energy-card .energy-compare strong{color:var(--green)}

/* ═══ GPU Evolution ═══ */
.gpu-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-top:40px}
.gpu-card{
background:var(--bg-card);border-radius:14px;padding:24px;text-align:center;
border:1px solid rgba(255,255,255,0.06);transition:all .4s;
}
.gpu-card:hover{border-color:var(--blue);transform:translateY(-4px)}
.gpu-card .gpu-year{font-size:12px;color:var(--blue);font-weight:600;margin-bottom:4px}
.gpu-card .gpu-name{font-size:18px;font-weight:700;color:var(--text-bright);margin-bottom:8px}
.gpu-card .gpu-watt{
font-size:36px;font-weight:800;
background:linear-gradient(135deg,#ff6b35,#ff3d00);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;
background-clip:text;
}
.gpu-card .gpu-unit{font-size:12px;color:var(--text-dim)}

/* ═══ Insight Cards ═══ */
.insight-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:40px}
.insight-card{
background:var(--bg-card);border-radius:16px;padding:28px;
border:1px solid rgba(255,255,255,0.06);position:relative;overflow:hidden;
}
.insight-card::before{
content:'';position:absolute;top:0;left:0;width:4px;height:100%;
}
.insight-card.tech::before{background:var(--blue)}
.insight-card.econ::before{background:#f59e0b}
.insight-card.env::before{background:var(--green)}
.insight-card.industry::before{background:#a855f7}
.insight-card .insight-tag{
font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;
}
.insight-card.tech .insight-tag{color:var(--blue)}
.insight-card.econ .insight-tag{color:#f59e0b}
.insight-card.env .insight-tag{color:var(--green)}
.insight-card.industry .insight-tag{color:#a855f7}
.insight-card h3{font-size:18px;font-weight:700;color:var(--text-bright);margin-bottom:10px}
.insight-card p{font-size:14px;color:var(--text-dim);line-height:1.6}

/* ═══ Closing ═══ */
#closing{
background:linear-gradient(180deg,#080810,var(--bg-dark));
padding:120px 0;text-align:center;
}
#closing h2{
font-size:clamp(24px,4vw,44px);font-weight:700;color:var(--text-bright);
max-width:700px;margin:0 auto 24px;letter-spacing:-.5px;line-height:1.2;
}
#closing p{font-size:17px;color:var(--text-dim);max-width:560px;margin:0 auto 40px}
.cta-btn{
display:inline-block;padding:14px 32px;border-radius:12px;
background:var(--blue);color:#fff;font-size:15px;font-weight:600;
text-decoration:none;transition:all .3s;
}
.cta-btn:hover{background:#0066cc;transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,113,227,0.3)}

/* ═══ Footer ═══ */
footer{
padding:40px 24px;text-align:center;color:var(--text-dim);font-size:12px;
border-top:1px solid rgba(255,255,255,0.04);
}
footer a{color:var(--blue);text-decoration:none}

/* ═══ Scroll Animations ═══ */
.reveal{opacity:0;transform:translateY(40px);transition:opacity .8s,transform .8s}
.reveal.visible{opacity:1;transform:translateY(0)}
.reveal-delay-1{transition-delay:.1s}
.reveal-delay-2{transition-delay:.2s}
.reveal-delay-3{transition-delay:.3s}
.reveal-delay-4{transition-delay:.4s}

/* ═══ Glow Ring ═══ */
.glow-ring{
position:absolute;border-radius:50%;
background:radial-gradient(circle,rgba(0,113,227,0.15),transparent 70%);
pointer-events:none;
}

/* ═══ Responsive ═══ */
@media(max-width:768px){
  nav .nav-links{display:none}
  .timeline-line{left:20px}
  .timeline-node,.timeline-node:nth-child(even){flex-direction:column;gap:12px;text-align:left}
  .timeline-content{max-width:100%}
  .compare-row{flex-direction:column}
  .bar-chart{height:200px}
}
</style>
</head>
<body>

<canvas id="particles"></canvas>

<nav id="navbar">
  <div class="logo">Token<span>Explosion</span></div>
  <div class="nav-links">
    <a href="#hero">开场</a>
    <a href="#timeline">时间线</a>
    <a href="#data-explosion">数据爆发</a>
    <a href="#charts">图表</a>
    <a href="#compare">对比</a>
    <a href="#energy">能源</a>
  </div>
</nav>

<!-- ═══════ HERO ═══════ -->
<section id="hero">
  <div class="tag">⚡ 2023 — 2026 · AI算力迁徙</div>
  <h1>
    <span class="highlight">1000亿</span> 到 <span class="highlight">500万亿</span><br>
    Token的3年迁徙
  </h1>
  <p class="subtitle">
    2023年，全球AI模型消耗1000亿Token；2026年，这个数字是500万亿。<br>
    一场指数级的算力爆发，正在重塑技术、经济与地球。
  </p>
  <div class="big-number" id="hero-counter">0</div>
  <div class="unit">Token / 日均消耗（2026年）</div>
  <div class="scroll-hint">
    <span>向下滚动探索</span>
    <div class="arrow"></div>
  </div>
</section>

<!-- ═══════ TIMELINE ═══════ -->
<section id="timeline">
  <div class="container">
    <div class="section-header reveal">
      <div class="label">探索式交互</div>
      <h2>三年迁徙时间线</h2>
      <p>点击不同年份，揭示算力消耗的关键转折</p>
    </div>
    <div class="timeline-track">
      <div class="timeline-line"></div>
      <div class="timeline-nodes">

        <div class="timeline-node reveal" data-year="2023" onclick="toggleTimeline(this)">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-year">2023 · 起点</div>
            <div class="timeline-title">大模型元年，算力初燃</div>
            <div class="timeline-desc">ChatGPT引爆全球AI热潮，GPT-4发布，大模型参数规模突破万亿级。算力需求刚刚开始它的指数曲线。</div>
            <div class="timeline-data">
              <div class="data-item"><span class="data-label">全球日均Token消耗</span><span class="data-value">~100亿</span></div>
              <div class="data-item"><span class="data-label">GPU出货量（NVIDIA数据中心）</span><span class="data-value">~376万块</span></div>
              <div class="data-item"><span class="data-label">H100单卡功耗</span><span class="data-value">700W</span></div>
              <div class="data-item"><span class="data-label">全球数据中心能耗</span><span class="data-value">~176 TWh</span></div>
              <div class="data-item"><span class="data-label">训练vs推理 算力占比</span><span class="data-value">60% : 40%</span></div>
              <div class="data-item"><span class="data-label">标志性事件</span><span class="data-value">ChatGPT / GPT-4 / Llama 2</span></div>
            </div>
          </div>
        </div>

        <div class="timeline-node reveal" data-year="2024" onclick="toggleTimeline(this)">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-year">2024 · 加速</div>
            <div class="timeline-title">推理崛起，Token通胀初现</div>
            <div class="timeline-desc">推理需求超越训练，中国日均Token从1000亿飙升。云厂商开始涨价，算力成为稀缺资源。</div>
            <div class="timeline-data">
              <div class="data-item"><span class="data-label">中国日均Token消耗（年初）</span><span class="data-value">~1,000亿</span></div>
              <div class="data-item"><span class="data-label">全球数据中心能耗</span><span class="data-value">415 TWh</span></div>
              <div class="data-item"><span class="data-label">AI数据中心IT能耗</span><span class="data-value">55.1 TWh</span></div>
              <div class="data-item"><span class="data-label">全球AI GPU出货量</span><span class="data-value">~3,500万块 H100等效</span></div>
              <div class="data-item"><span class="data-label">每百万Token均价</span><span class="data-value">$0.03</span></div>
              <div class="data-item"><span class="data-label">标志性事件</span><span class="data-value">Sora / Claude 3 / Gemini 1.5</span></div>
            </div>
          </div>
        </div>

        <div class="timeline-node reveal" data-year="2025" onclick="toggleTimeline(this)">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-year">2025 · 爆发</div>
            <div class="timeline-title">智能体引爆，千倍增长</div>
            <div class="timeline-desc">AI Agent规模化落地，单次任务消耗Token达数十万级。全球Token年消耗突破4.8千万亿，增长212%。</div>
            <div class="timeline-data">
              <div class="data-item"><span class="data-label">中国日均Token消耗（年底）</span><span class="data-value">100万亿</span></div>
              <div class="data-item"><span class="data-label">全球Token年消耗</span><span class="data-value">4.8×10¹⁵ (4.8千万亿)</span></div>
              <div class="data-item"><span class="data-label">GPU出货量</span><span class="data-value">~700万块</span></div>
              <div class="data-item"><span class="data-label">推理Token占比</span><span class="data-value">72% — 78%</span></div>
              <div class="data-item"><span class="data-label">每百万Token均价</span><span class="data-value">$0.018（↓40%）</span></div>
              <div class="data-item"><span class="data-label">豆包日均Token（年底）</span><span class="data-value">突破50万亿</span></div>
            </div>
          </div>
        </div>

        <div class="timeline-node reveal" data-year="2026" onclick="toggleTimeline(this)">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-year">2026 · 现在</div>
            <div class="timeline-title">500万亿时代，Token即货币</div>
            <div class="timeline-desc">Token被正式定名为"词元"，成为AI时代的计量单位。日均消耗从千亿到百万亿，增长超千倍。</div>
            <div class="timeline-data">
              <div class="data-item"><span class="data-label">中国日均Token消耗（3月）</span><span class="data-value">140万亿</span></div>
              <div class="data-item"><span class="data-label">预计年底日均</span><span class="data-value">300—500万亿</span></div>
              <div class="data-item"><span class="data-label">全球数据中心能耗（预计）</span><span class="data-value">565 TWh</span></div>
              <div class="data-item"><span class="data-label">AI服务器用电量</span><span class="data-value">175 TWh（↑84%）</span></div>
              <div class="data-item"><span class="data-label">GPU出货量（预计）</span><span class="data-value">850—1000万块</span></div>
              <div class="data-item"><span class="data-label">标志性事件</span><span class="data-value">Token定名"词元" / 涨价潮</span></div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</section>

<!-- ═══════ DATA EXPLOSION ═══════ -->
<section id="data-explosion">
  <div class="container">
    <div class="section-header reveal">
      <div class="label">数据式交互</div>
      <h2>数字背后的故事</h2>
      <p>每一个跳动的数字，都是指数增长的注脚</p>
    </div>
    <div class="data-grid">
      <div class="data-card reveal">
        <div class="card-icon">🔤</div>
        <div class="card-value" data-target="5000000" data-suffix="亿">0</div>
        <div class="card-label">2026年预计日均Token消耗</div>
        <div class="card-change">↑ 50,000x vs 2023</div>
      </div>
      <div class="data-card reveal reveal-delay-1">
        <div class="card-icon">⚡</div>
        <div class="card-value" data-target="565" data-suffix=" TWh">0</div>
        <div class="card-label">2026年全球数据中心能耗</div>
        <div class="card-change">↑ 36% vs 2024</div>
      </div>
      <div class="data-card reveal reveal-delay-2">
        <div class="card-icon">🔧</div>
        <div class="card-value" data-target="1000" data-suffix="万+">0</div>
        <div class="card-label">2026年GPU出货量（预计）</div>
        <div class="card-change">↑ 166% vs 2023</div>
      </div>
      <div class="data-card reveal reveal-delay-3">
        <div class="card-icon">💰</div>
        <div class="card-value" data-target="40" data-suffix="%" data-prefix="↓">0</div>
        <div class="card-label">Token单价年降幅（2024→2025）</div>
        <div class="card-change">$0.03 → $0.018 /百万Token</div>
      </div>
      <div class="data-card reveal reveal-delay-4">
        <div class="card-icon">🤖</div>
        <div class="card-value" data-target="78" data-suffix="%">0</div>
        <div class="card-label">推理Token占比（2025）</div>
        <div class="card-change">训练仅占22%</div>
      </div>
      <div class="data-card reveal reveal-delay-4">
        <div class="card-icon">🌍</div>
        <div class="card-value" data-target="43" data-suffix="%">0</div>
        <div class="card-label">亚太地区全球Token消耗占比</div>
        <div class="card-change">首次超越北美</div>
      </div>
    </div>
  </div>
</section>

<!-- ═══════ CHARTS ═══════ -->
<section id="charts">
  <div class="container">
    <div class="section-header reveal">
      <div class="label">动态图表</div>
      <h2>增长的曲线</h2>
      <p>从线性到指数，算力需求的陡峭曲线</p>
    </div>

    <!-- Token Chart -->
    <div class="chart-container reveal">
      <div class="chart-title">中国日均Token消耗量（万亿）</div>
      <div class="chart-subtitle">数据来源：国家数据局、OpenRouter、各平台公开数据</div>
      <div class="bar-chart" id="token-chart">
        <div class="bar-group"><div class="bar" style="height:0;background:linear-gradient(180deg,var(--blue),#0044aa)" data-height="1"><span class="bar-value">0.1</span><span class="bar-label">2023</span></div></div>
        <div class="bar-group"><div class="bar" style="height:0;background:linear-gradient(180deg,var(--blue),#0044aa)" data-height="3"><span class="bar-value">0.1</span><span class="bar-label">2024初</span></div></div>
        <div class="bar-group"><div class="bar" style="height:0;background:linear-gradient(180deg,var(--cyan),var(--blue))" data-height="15"><span class="bar-value">30</span><span class="bar-label">2025中</span></div></div>
        <div class="bar-group"><div class="bar" style="height:0;background:linear-gradient(180deg,var(--green),#00994d)" data-height="55"><span class="bar-value">100</span><span class="bar-label">2025底</span></div></div>
        <div class="bar-group"><div class="bar" style="height:0;background:linear-gradient(180deg,var(--green),#00994d)" data-height="72"><span class="bar-value">140</span><span class="bar-label">2026.3</span></div></div>
        <div class="bar-group"><div class="bar" style="height:0;background:linear-gradient(180deg,#00ff88,var(--green))" data-height="100"><span class="bar-value">500</span><span class="bar-label">2026底(预)</span></div></div>
      </div>
    </div>

    <!-- GPU Chart -->
    <div class="chart-container reveal">
      <div class="chart-title">全球AI GPU出货量（百万块）</div>
      