#!/usr/bin/env python3
"""Generate the humanoid robot startup boom interactive HTML."""
import os

OUTPUT = "/app/working/shared/showcase/2026-08-27-humanoid-robot-startup-boom.html"

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>11.6万户 · 人形机器人创业潮背后的冷思考</title>
<style>
/* ========== RESET & BASE ========== */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#000;--bg2:#0a0a0f;--bg3:#111118;
  --text:#fff;--text2:#86868b;--text3:#555;
  --blue:#0071e3;--blue2:#0090ff;--orange:#ff9500;--orange2:#ff6b35;
  --red:#ff3b30;--green:#30d158;--cyan:#64d2ff;
  --card:#161618;--card2:#1c1c1e;
  --glass:rgba(255,255,255,.06);
  --glow-blue:0 0 30px rgba(0,113,227,.3);
  --glow-orange:0 0 30px rgba(255,149,0,.3);
}
html{scroll-behavior:smooth;font-size:16px}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue","PingFang SC",sans-serif;line-height:1.5;overflow-x:hidden;-webkit-font-smoothing:antialiased}
a{color:var(--blue);text-decoration:none}
::selection{background:var(--blue);color:#fff}

/* ========== NAV ========== */
.nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:12px 40px;display:flex;align-items:center;justify-content:space-between;background:rgba(0,0,0,.72);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.06);transition:transform .3s}
.nav-logo{font-size:14px;font-weight:600;letter-spacing:-.01em;color:var(--text2)}
.nav-logo span{color:var(--orange)}
.nav-links{display:flex;gap:24px}
.nav-links a{font-size:13px;color:var(--text2);transition:color .2s}
.nav-links a:hover{color:var(--text)}

/* ========== HERO ========== */
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 40px 80px;overflow:hidden}
.hero-canvas{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0}
.hero-content{position:relative;z-index:2;max-width:900px}
.hero-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 16px;border-radius:100px;background:rgba(255,149,0,.12);border:1px solid rgba(255,149,0,.25);font-size:13px;color:var(--orange);margin-bottom:32px;letter-spacing:.02em}
.hero-badge::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--orange);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.hero h1{font-size:clamp(36px,6vw,72px);font-weight:700;letter-spacing:-.03em;line-height:1.05;margin-bottom:24px}
.hero h1 .num{background:linear-gradient(135deg,var(--orange),var(--orange2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero h1 .sub{color:var(--text2);font-weight:400}
.hero-sub{font-size:clamp(16px,2vw,22px);color:var(--text2);max-width:680px;margin:0 auto 48px;line-height:1.6}
.hero-stats{display:flex;gap:48px;justify-content:center;flex-wrap:wrap}
.hero-stat{text-align:center}
.hero-stat .val{font-size:48px;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.hero-stat .val.blue{color:var(--blue2)}
.hero-stat .val.orange{color:var(--orange)}
.hero-stat .val.red{color:var(--red)}
.hero-stat .label{font-size:13px;color:var(--text2);margin-top:4px}
.scroll-hint{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);z-index:2;display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--text3);font-size:12px;animation:float 3s ease-in-out infinite}
.scroll-hint .arrow{width:20px;height:20px;border-right:1.5px solid var(--text3);border-bottom:1.5px solid var(--text3);transform:rotate(45deg)}
@keyframes float{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(8px)}}

/* ========== SECTIONS ========== */
section{padding:100px 40px;max-width:1200px;margin:0 auto}
.section-header{text-align:center;margin-bottom:64px}
.section-header h2{font-size:clamp(28px,4vw,48px);font-weight:700;letter-spacing:-.02em;margin-bottom:16px}
.section-header p{font-size:17px;color:var(--text2);max-width:600px;margin:0 auto}

/* ========== KPI STRIP ========== */
.kpi-strip{background:var(--bg2);border-top:1px solid rgba(255,255,255,.06);border-bottom:1px solid rgba(255,255,255,.06);padding:48px 40px}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;max-width:1200px;margin:0 auto}
.kpi-card{background:var(--card);border-radius:12px;padding:28px 24px;position:relative;overflow:hidden;transition:transform .3s,box-shadow .3s}
.kpi-card:hover{transform:translateY(-2px);box-shadow:var(--glow-blue)}
.kpi-card::before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--blue),transparent)}
.kpi-card .icon{font-size:24px;margin-bottom:12px}
.kpi-card .number{font-size:36px;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.kpi-card .number.c-blue{color:var(--blue2)}
.kpi-card .number.c-orange{color:var(--orange)}
.kpi-card .number.c-green{color:var(--green)}
.kpi-card .number.c-red{color:var(--red)}
.kpi-card .desc{font-size:14px;color:var(--text2);margin-top:6px}
.kpi-card .trend{display:inline-flex;align-items:center;gap:4px;font-size:12px;margin-top:8px;padding:3px 8px;border-radius:6px;font-weight:500}
.kpi-card .trend.up{background:rgba(48,209,88,.12);color:var(--green)}
.kpi-card .trend.down{background:rgba(255,59,48,.12);color:var(--red)}

/* ========== STORY TIMELINE ========== */
.story-section{background:var(--bg);position:relative}
.story-grid{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
.story-text h3{font-size:28px;font-weight:600;letter-spacing:-.01em;margin-bottom:16px;line-height:1.3}
.story-text p{font-size:16px;color:var(--text2);line-height:1.7;margin-bottom:16px}
.story-visual{position:relative;background:var(--card);border-radius:16px;padding:32px;min-height:400px}
.story-quote{font-size:20px;font-style:italic;line-height:1.6;color:var(--text);border-left:3px solid var(--orange);padding-left:20px;margin:24px 0}
.story-source{font-size:12px;color:var(--text3);margin-top:12px}

/* ========== MAP SECTION ========== */
.map-section{background:var(--bg2);border-top:1px solid rgba(255,255,255,.06);border-bottom:1px solid rgba(255,255,255,.06)}
.map-container{position:relative;max-width:1000px;margin:0 auto}
.map-svg{width:100%;height:auto}
.city-dot{cursor:pointer;transition:all .3s}
.city-dot:hover{filter:drop-shadow(0 0 12px var(--blue))}
.city-dot circle{transition:all .3s}
.city-tooltip{position:absolute;background:var(--card2);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:20px;min-width:260px;pointer-events:none;opacity:0;transform:translateY(8px);transition:all .3s;z-index:10;box-shadow:0 8px 32px rgba(0,0,0,.5)}
.city-tooltip.active{opacity:1;transform:translateY(0)}
.city-tooltip h4{font-size:18px;font-weight:600;margin-bottom:8px}
.city-tooltip .city-stat{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.06);font-size:14px}
.city-tooltip .city-stat:last-child{border:none}
.city-tooltip .city-stat span:last-child{color:var(--blue2);font-weight:600}
.city-legend{display:flex;gap:24px;justify-content:center;margin-top:24px;flex-wrap:wrap}
.city-legend-item{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text2)}
.city-legend-item .dot{width:10px;height:10px;border-radius:50%}
.city-legend-item .dot.tier1{background:var(--blue)}
.city-legend-item .dot.tier2{background:var(--cyan)}
.city-legend-item .dot.tier3{background:var(--orange)}

/* ========== TOGGLE ========== */
.toggle-section{background:var(--bg)}
.toggle-container{max-width:900px;margin:0 auto}
.toggle-bar{display:flex;justify-content:center;margin-bottom:48px;position:relative}
.toggle-bar::before{content:"";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:1px;height:28px;background:rgba(255,255,255,.1)}
.toggle-btn{padding:12px 32px;border:none;background:transparent;color:var(--text2);font-size:15px;font-weight:500;cursor:pointer;transition:all .3s;border-radius:100px;letter-spacing:.01em}
.toggle-btn.active{color:#fff}
.toggle-btn.active.hype{background:rgba(0,113,227,.15);border:1px solid rgba(0,113,227,.3)}
.toggle-btn.active.reality{background:rgba(255,149,0,.15);border:1px solid rgba(255,149,0,.3)}
.toggle-content{position:relative;min-height:500px}
.toggle-panel{position:absolute;top:0;left:0;right:0;opacity:0;transform:translateY(20px);transition:all .5s;pointer-events:none}
.toggle-panel.active{opacity:1;transform:translateY(0);pointer-events:auto}
.data-row{display:flex;align-items:center;gap:24px;padding:20px 0;border-bottom:1px solid rgba(255,255,255,.06)}
.data-row .metric-name{font-size:15px;color:var(--text2);min-width:140px}
.data-bar-wrap{flex:1;position:relative;height:36px;background:rgba(255,255,255,.04);border-radius:8px;overflow:hidden}
.data-bar{height:100%;border-radius:8px;display:flex;align-items:center;padding:0 16px;font-size:14px;font-weight:600;transition:width 1.2s cubic-bezier(.22,1,.36,1);width:0}
.data-bar.hype{background:linear-gradient(90deg,var(--blue),var(--blue2))}
.data-bar.reality{background:linear-gradient(90deg,var(--orange),var(--orange2))}
.data-row .val-text{font-size:15px;font-weight:600;min-width:80px;text-align:right}
.insight-box{margin-top:32px;padding:24px;border-radius:12px;font-size:15px;line-height:1.7;color:var(--text2)}
.insight-box.hype-insight{background:rgba(0,113,227,.08);border:1px solid rgba(0,113,227,.2)}
.insight-box.reality-insight{background:rgba(255,149,0,.08);border:1px solid rgba(255,149,0,.2)}
.insight-box strong{color:var(--text)}

/* ========== CHART SECTION ========== */
.chart-section{background:var(--bg2);border-top:1px solid rgba(255,255,255,.06)}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:32px}
.chart-card{background:var(--card);border-radius:16px;padding:28px;position:relative;overflow:hidden}
.chart-card::before{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--blue),transparent)}
.chart-card h4{font-size:17px;font-weight:600;margin-bottom:20px}
.chart-card canvas{width:100%;height:260px}
.chart-card.full{grid-column:1/-1}
.chart-card.full canvas{height:300px}

/* ========== COMPANY GRID ========== */
.company-section{background:var(--bg)}
.company-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.company-card{background:var(--card);border-radius:12px;padding:24px;transition:transform .3s,box-shadow .3s;cursor:default}
.company-card:hover{transform:translateY(-3px);box-shadow:var(--glow-blue)}
.company-card .cc-header{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.company-card .cc-icon{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px}
.company-card .cc-name{font-size:16px;font-weight:600}
.company-card .cc-tag{font-size:11px;color:var(--text3);margin-top:2px}
.company-card .cc-stats{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}
.company-card .cc-stat{font-size:13px;color:var(--text2)}
.company-card .cc-stat span{color:var(--text);font-weight:600}

/* ========== REFLECTION ========== */
.reflection{background:linear-gradient(180deg,var(--bg) 0%,#050510 100%);text-align:center;padding:120px 40px}
.reflection h2{font-size:clamp(28px,4vw,48px);font-weight:700;letter-spacing:-.02em;margin-bottom:24px;line-height:1.2}
.reflection p{font-size:18px;color:var(--text2);max-width:700px;margin:0 auto 16px;line-height:1.7}
.reflection .big-q{font-size:clamp(36px,5vw,64px);font-weight:700;background:linear-gradient(135deg,var(--orange),var(--blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:40px 0}
.reflection .closing{font-size:15px;color:var(--text3);margin-top:48px}

/* ========== FOOTER ========== */
.footer{background:var(--bg);border-top:1px solid rgba(255,255,255,.06);padding:40px;text-align:center}
.footer p{font-size:12px;color:var(--text3);line-height:1.8}

/* ========== ANIMATIONS ========== */
.reveal{opacity:0;transform:translateY(40px);transition:opacity .8s,transform .8s}
.reveal.visible{opacity:1;transform:translateY(0)}
.reveal-delay-1{transition-delay:.1s}
.reveal-delay-2{transition-delay:.2s}
.reveal-delay-3{transition-delay:.3s}
.reveal-delay-4{transition-delay:.4s}

/* ========== RESPONSIVE ========== */
@media(max-width:768px){
  section{padding:60px 20px}
  .kpi-grid{grid-template-columns:1fr 1fr}
  .story-grid{grid-template-columns:1fr}
  .chart-grid{grid-template-columns:1fr}
  .company-grid{grid-template-columns:1fr}
  .hero-stats{gap:24px}
  .nav-links{display:none}
}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <div class="nav-logo">🤖 人形机器人 <span>创业潮</span></div>
  <div class="nav-links">
    <a href="#data">数据全景</a>
    <a href="#story">故事线</a>
    <a href="#map">城市地图</a>
    <a href="#toggle">冷思考</a>
    <a href="#charts">趋势图</a>
    <a href="#players">核心玩家</a>
  </div>
</nav>

<!-- HERO -->
<section class="hero" id="hero">
  <canvas class="hero-canvas" id="particleCanvas"></canvas>
  <div class="hero-content">
    <div class="hero-badge">2026年 · 国家市场监管总局数据</div>
    <h1>
      <span class="num">11.6万户</span><br>
      <span class="sub">人形机器人创业潮背后的冷思考</span>
    </h1>
    <p class="hero-sub">2026年上半年，中国新设人形机器人领域企业11.6万户，同比增长9.5%。平均每天超过640家新公司涌入这个赛道。热潮之下，是机遇还是泡沫？</p>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="val orange" data-target="11.6" data-suffix="万">0</div>
        <div class="label">新设企业（户）</div>
      </div>
      <div class="hero-stat">
        <div class="val blue" data-target="935" data-suffix="亿">0</div>
        <div class="label">H1融资总额</div>
      </div>
      <div class="hero-stat">
        <div class="val green" data-target="10" data-suffix="万+">0</div>
        <div class="label">全年预计产量</div>
      </div>
      <div class="hero-stat">
        <div class="val red" data-target="97" data-suffix="%">0</div>
        <div class="label">中国全球占比</div>
      </div>
    </div>
  </div>
  <div class="scroll-hint">
    <span>向下滚动探索</span>
    <div class="arrow"></div>
  </div>
</section>

<!-- KPI STRIP -->
<div class="kpi-strip" id="data">
  <div class="kpi-grid">
    <div class="kpi-card reveal">
      <div class="icon">🏭</div>
      <div class="number c-blue" data-target="116000" data-format="comma">0</div>
      <div class="desc">2026H1 新设企业数</div>
      <div class="trend up">↑ 9.5% YoY</div>
    </div>
    <div class="kpi-card reveal reveal-delay-1">
      <div class="icon">💰</div>
      <div class="number c-orange" data-target="935" data-suffix="亿">0</div>
      <div class="desc">H1 具身智能融资总额</div>
      <div class="trend up">↑ 5× YoY</div>
    </div>
    <div class="kpi-card reveal reveal-delay-2">
      <div class="icon">🤖</div>
      <div class="number c-green" data-target="400" data-suffix="+">0</div>
      <div class="desc">整机产品型号</div>
      <div class="trend up">超全球半数</div>
    </div>
    <div class="kpi-card reveal reveal-delay-3">
      <div class="icon">📉</div>
      <div class="number c-red" data-target="65" data-suffix="%">0</div>
      <div class="desc">注册资本<500万企业占比</div>
      <div class="trend down">⚠ 微小企业为主</div>
    </div>
  </div>
</div>

<!-- STORY SECTION -->
<section class="story-section" id="story">
  <div class="section-header reveal">
    <h2>从热潮到冷思考</h2>
    <p>当资本、政策与技术三股力量交汇，一场前所未有的创业浪潮正在重塑中国机器人产业</p>
  </div>

  <div class="story-grid reveal">
    <div class="story-text">
      <h3>🔥 热度：造梦元年</h3>
      <p>2026年春节，四家国产机器人在央视春晚同台亮相，宇树科技标价70万元的人形机器人单日斩获数百笔订单，"机器熊猫"上线即告售罄。</p>
      <p>资本市场闻风而动：银河通用完成25亿元融资，估值飙至200亿元；宇树科技科创板IPO，市值约420亿元。一级市场给故事，二级市场给估值，应用场景的想象空间从工厂延伸到家庭。</p>
      <div class="story-quote">
        "三类玩家凑齐了——大厂有钱有渠道，创业公司有技术有故事，地方政府有地有政策补贴。热闹得像2016年的共享单车。"
        <div class="story-source">—— 产业观察人士</div>
      </div>
    </div>
    <div class="story-visual">
      <h3 style="font-size:22px;font-weight:600;margin-bottom:16px">⚡ 三股浪潮叠加</h3>
      <div style="display:flex;flex-direction:column;gap:16px">
        <div style="background:rgba(0,113,227,.1);border:1px solid rgba(0,113,227,.2);border-radius:12px;padding:20px">
          <div style="font-size:14px;font-weight:600;color:var(--blue2);margin-bottom:6px">🏢 跨界巨头</div>
          <div style="font-size:14px;color:var(--text2);line-height:1.6">比亚迪发布"小迪"，理想、小鹏、小米集体布局。车企带着供应链和制造能力杀入赛道。</div>
        </div>
        <div style="background:rgba(48,209,88,.1);border:1px solid rgba(48,209,88,.2);border-radius:12px;padding:20px">
          <div style="font-size:14px;font-weight:600;color:var(--green);margin-bottom:6px">🚀 创业公司</div>
          <div style="font-size:14px;color:var(--text2);line-height:1.6">宇树科技IPO排队认购，优必选已上市，众擎、帕西尼等密集融资。创业公司正从"烧钱"走向"量产"。</div>
        </div>
        <div style="background:rgba(255,149,0,.1);border:1px solid rgba(255,149,0,.2);border-radius:12px;padding:20px">
          <div style="font-size:14px;font-weight:600;color:var(--orange);margin-bottom:6px">🏛️ 政策驱动</div>
          <div style="font-size:14px;color:var(--text2);line-height:1.6">地方政府把机器人当"下一个新能源汽车"布局。重庆、深圳、杭州纷纷设立专项孵化器，提供共享试验场地和公共算力平台。</div>
        </div>
      </div>
    </div>
  </div>

  <div class="story-grid reveal" style="margin-top:64px">
    <div class="story-visual" style="background:rgba(255,149,0,.05);border:1px solid rgba(255,149,0,.15)">
      <h3 style="font-size:22px;font-weight:600;margin-bottom:16px;color:var(--orange)">🧊 冷思考：数字经不起细看</h3>
      <div class="story-quote" style="border-color:var(--red)">
        "全球研究机构预测2026年人形机器人出货量约5万台，国内乐观估计占一半也就两三万台。现在光是今年新注册的企业就有11.6万家——平均每家分不到一台。"
      </div>
      <p style="font-size:15px;color:var(--text2);line-height:1.7;margin-top:16px">产业链账本也越算越像PPT。上游减速器、灵巧手、传感器，能稳定出货的供应商不超过十家；下游应用场景大多还在试点。一轮轮融资下来，机构早就把回报落袋为安了。</p>
      <p style="font-size:15px;color:var(--text2);line-height:1.7;margin-top:12px">约<strong style="color:var(--orange)">四成企业尚无明确量产时间表</strong>。市场监管总局已表示将加强产业引导和标准供给，防止低水平重复建设。</p>
    </div>
    <div class="story-visual">
      <h3 style="font-size:22px;font-weight:600;margin-bottom:16px">📊 关键对比</h3>
      <div style="display:flex;flex-direction:column;gap:20px">
        <div>
          <div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px"><span>新设企业数</span><span style="color:var(--orange);font-weight:600">11.6万户</span></div>
          <div style="height:8px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden"><div style="height:100%;width:95%;background:linear-gradient(90deg,var(--orange),var(--orange2));border-radius:4px"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px"><span>预计出货量</span><span style="color:var(--blue2);font-weight:600">~3.8万台</span></div>
          <div style="height:8px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden"><div style="height:100%;width:3.3%;background:linear-gradient(90deg,var(--blue),var(--blue2));border-radius:4px;min-width:12px"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px"><span>2025全球出货量</span><span style="color:var(--cyan);font-weight:600">~1.8万台</span></div>
          <div style="height:8px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden"><div style="height:100%;width:1.5%;background:var(--cyan);border-radius:4px;min-width:12px"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px"><span>H1融资总额</span><span style="color:var(--green);font-weight:600">935亿元</span></div>
          <div style="height:8px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden"><div style="height:100%;width:80%;background:linear-gradient(90deg,var(--green),#4ade80);border-radius:4px"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px"><span>稳定出货供应商</span><span style="color:var(--red);font-weight:600">< 10家</span></div>
          <div style="height:8px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden"><div style="height:100%;width:0.8%;background:var(--red);border-radius:4px;min-width:12px"></div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- MAP SECTION -->
<section class="map-section" id="map">
  <div class="section-header reveal">
    <h2>中国机器人创业生态地图</h2>
    <p>长三角、珠三角、京津冀三大区域合计占比超七成，点击城市探索详情</p>
  </div>
  <div class="map-container reveal">
    <svg class="map-svg" viewBox="0 0 800 600" id="chinaMap">
      <!-- Simplified China outline -->
      <path d="M350 50 L450 30 L550 60 L650 80 L700 130 L720 200 L710 280 L680 330 L650 370 L620 400 L580 430 L540 450 L500 470 L460 480 L420 490 L380 500 L340 490 L300 470 L260 440 L230 400 L210 350 L200 300 L210 250 L230 200 L260 150 L300 100 Z" fill="rgba(255,255,255,.03)" stroke="rgba(255,255,255,.1)" stroke-width="1.5"/>
      
      <!-- Grid lines -->
      <g opacity="0.06" stroke="#fff" stroke-width="0.5">
        <line x1="0" y1="150" x2="800" y2="150"/>
        <line x1="0" y1="300" x2="800" y2="300"/>
        <line x1="0" y1="450" x2="800" y2="450"/>
        <line x1="200" y1="0" x2="200" y2="600"/>
        <line x1="400" y1="0" x2="400" y2="600"/>
        <line x1="600" y1="0" x2="600" y2="600"/>
      </g>
      
      <!-- City dots with data -->
      <g id="cityDots">
        <!-- Beijing -->
        <g class="city-dot" data-city="beijing" onclick="showCity('beijing', event)">
          <circle cx="490" cy="155" r="22" fill="rgba(0,113,227,.15)" stroke="rgba(0,113,227,.4)" stroke-width="1">
            <animate attributeName="r" values="22;26;22" dur="3s" repeatCount="indefinite"/>
          </circle>
          <circle cx="490" cy="155" r="8" fill="#0071e3"/>
          <text x="490" y="145" text-anchor="middle" fill="#fff" font-size="11" font-weight="600">北京</text>
        </g>
        
        <!-- Shenzhen -->
        <g class="city-dot" data-city="shenzhen" onclick="showCity('shenzhen', event)">
          