#!/usr/bin/env python3
"""Generate the Humanoid Robot Startup Boom interactive HTML experience."""

import os

OUTPUT = "/app/working/shared/showcase/2026-08-27-humanoid-robot-startup-boom.html"

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>人形机器人创业潮：11.6万户背后的冷思考</title>
<style>
/* ═══════════════ RESET & VARIABLES ═══════════════ */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#000;--bg2:#0a0a0f;--bg3:#111118;
  --blue:#0071e3;--blue-glow:rgba(0,113,227,.35);
  --orange:#ff9500;--orange-glow:rgba(255,149,0,.3);
  --red:#ff3b30;--green:#30d158;
  --text:#fff;--text2:#86868b;--text3:#555;
  --card:rgba(255,255,255,.04);
  --card-border:rgba(255,255,255,.08);
  --max-w:1100px;
  --font:-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text','Helvetica Neue','PingFang SC',sans-serif;
}
html{scroll-behavior:smooth;background:var(--bg);color:var(--text);font-family:var(--font)}
body{overflow-x:hidden;-webkit-font-smoothing:antialiased}
a{color:var(--blue);text-decoration:none}
::selection{background:var(--blue);color:#fff}

/* ═══════════════ UTILITY ═══════════════ */
.container{max-width:var(--max-w);margin:0 auto;padding:0 24px}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}

/* ═══════════════ HERO ═══════════════ */
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;overflow:hidden;background:var(--bg)}
.hero canvas{position:absolute;inset:0;z-index:0}
.hero-content{position:relative;z-index:2;max-width:900px;padding:0 24px}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(255,149,0,.12);border:1px solid rgba(255,149,0,.25);border-radius:100px;padding:6px 18px;font-size:13px;color:var(--orange);letter-spacing:.5px;margin-bottom:32px;font-weight:500}
.hero-badge .dot{width:6px;height:6px;border-radius:50%;background:var(--orange);animation:pulse 2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.hero h1{font-size:clamp(36px,7vw,72px);font-weight:700;line-height:1.05;letter-spacing:-.03em;margin-bottom:20px;background:linear-gradient(135deg,#fff 0%,#fff 40%,var(--orange) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero h1 .num{font-size:clamp(48px,9vw,96px);-webkit-text-fill-color:var(--orange);font-weight:800}
.hero-sub{font-size:clamp(16px,2.2vw,22px);color:var(--text2);line-height:1.6;max-width:680px;margin:0 auto 48px}
.hero-stats{display:flex;gap:40px;justify-content:center;flex-wrap:wrap;margin-bottom:48px}
.hero-stat{text-align:center}
.hero-stat .val{font-size:clamp(28px,4vw,48px);font-weight:700;color:var(--text);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.hero-stat .val .unit{font-size:.5em;color:var(--text2);font-weight:400;margin-left:4px}
.hero-stat .label{font-size:13px;color:var(--text3);margin-top:4px;letter-spacing:.5px;text-transform:uppercase}
.scroll-hint{position:absolute;bottom:32px;left:50%;transform:translateX(-50%);z-index:2;display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--text3);font-size:12px;letter-spacing:1px;animation:bob 2s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(8px)}}
.scroll-hint svg{width:20px;height:20px;stroke:var(--text3);fill:none;stroke-width:2}

/* ═══════════════ SECTION COMMON ═══════════════ */
section{padding:120px 0;position:relative}
.section-dark{background:var(--bg)}
.section-mid{background:var(--bg2)}
.section-light{background:var(--bg3)}
.section-tag{display:inline-flex;align-items:center;gap:6px;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:var(--blue);margin-bottom:16px;font-weight:600}
.section-title{font-size:clamp(28px,4.5vw,48px);font-weight:600;letter-spacing:-.02em;line-height:1.1;margin-bottom:16px}
.section-desc{font-size:clamp(15px,1.8vw,18px);color:var(--text2);line-height:1.7;max-width:680px}

/* ═══════════════ NARRATIVE BLOCKS ═══════════════ */
.narrative{padding:80px 0}
.narrative-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;margin-top:48px}
.narr-card{background:var(--card);border:1px solid var(--card-border);border-radius:16px;padding:32px;transition:all .3s ease;position:relative;overflow:hidden}
.narr-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--blue),var(--orange));opacity:0;transition:opacity .3s}
.narr-card:hover{border-color:rgba(255,255,255,.15);transform:translateY(-4px)}
.narr-card:hover::before{opacity:1}
.narr-card .icon{font-size:32px;margin-bottom:16px}
.narr-card h3{font-size:20px;font-weight:600;margin-bottom:8px;letter-spacing:-.01em}
.narr-card p{font-size:15px;color:var(--text2);line-height:1.6}
.narr-card .highlight{color:var(--orange);font-weight:600}

/* ═══════════════ A/B TOGGLE ═══════════════ */
.ab-section{padding:120px 0}
.ab-header{text-align:center;margin-bottom:64px}
.ab-toggle-wrap{display:flex;justify-content:center;margin-top:32px}
.ab-toggle{display:flex;background:rgba(255,255,255,.06);border-radius:100px;padding:4px;border:1px solid var(--card-border);position:relative}
.ab-btn{padding:12px 32px;border-radius:100px;font-size:15px;font-weight:500;color:var(--text2);cursor:pointer;transition:all .3s;border:none;background:transparent;position:relative;z-index:1;font-family:var(--font)}
.ab-btn.active{color:#fff}
.ab-slider{position:absolute;top:4px;height:calc(100% - 8px);background:var(--blue);border-radius:100px;transition:all .4s cubic-bezier(.4,0,.2,1)}
.ab-btn:nth-child(1).active~.ab-slider{left:4px;width:calc(50% - 4px)}
.ab-btn:nth-child(2).active~.ab-slider{left:calc(50%);width:calc(50% - 4px)}
.ab-panels{position:relative;min-height:500px}
.ab-panel{position:absolute;inset:0;opacity:0;transform:translateY(20px);transition:all .5s cubic-bezier(.4,0,.2,1);pointer-events:none}
.ab-panel.active{opacity:1;transform:translateY(0);pointer-events:auto}
.ab-card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}
.ab-card{background:var(--card);border:1px solid var(--card-border);border-radius:12px;padding:24px;text-align:center}
.ab-card .big-num{font-size:42px;font-weight:700;letter-spacing:-.02em;margin-bottom:4px;font-variant-numeric:tabular-nums}
.ab-card .big-num.hot{color:var(--orange)}
.ab-card .big-num.cool{color:var(--blue)}
.ab-card .card-label{font-size:13px;color:var(--text3);text-transform:uppercase;letter-spacing:.5px}
.ab-card .card-note{font-size:13px;color:var(--text2);margin-top:8px;line-height:1.5}
.ab-quote{margin-top:48px;padding:32px;border-left:3px solid var(--orange);background:rgba(255,149,0,.05);border-radius:0 12px 12px 0;font-size:17px;line-height:1.8;color:var(--text2)}
.ab-quote em{color:var(--text);font-style:normal;font-weight:600}

/* ═══════════════ CITY MAP ═══════════════ */
.map-section{padding:120px 0;background:var(--bg)}
.map-wrap{position:relative;margin-top:48px;display:flex;gap:32px;align-items:flex-start;flex-wrap:wrap}
.map-canvas{flex:1;min-width:320px;position:relative}
.map-canvas svg{width:100%;height:auto}
.map-sidebar{flex:0 0 360px;min-width:300px}
.city-card{background:var(--card);border:1px solid var(--card-border);border-radius:16px;padding:28px;transition:all .3s;cursor:pointer}
.city-card.selected{border-color:var(--blue);box-shadow:0 0 30px var(--blue-glow)}
.city-card h3{font-size:22px;font-weight:600;margin-bottom:4px}
.city-card .city-rank{font-size:12px;color:var(--orange);letter-spacing:.5px;text-transform:uppercase;margin-bottom:16px}
.city-metrics{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.city-metric{text-align:center;padding:12px 8px;background:rgba(255,255,255,.03);border-radius:8px}
.city-metric .cm-val{font-size:24px;font-weight:700;color:var(--text);font-variant-numeric:tabular-nums}
.city-metric .cm-label{font-size:11px;color:var(--text3);margin-top:2px;text-transform:uppercase;letter-spacing:.5px}
.city-detail{margin-top:16px;padding-top:16px;border-top:1px solid var(--card-border)}
.city-detail p{font-size:14px;color:var(--text2);line-height:1.6}
.city-detail .tag{display:inline-block;padding:3px 10px;background:rgba(0,113,227,.15);border-radius:100px;font-size:12px;color:var(--blue);margin:2px}

/* ═══════════════ CHARTS ═══════════════ */
.charts-section{padding:120px 0}
.chart-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:32px;margin-top:48px}
.chart-box{background:var(--card);border:1px solid var(--card-border);border-radius:16px;padding:28px;position:relative;overflow:hidden}
.chart-box h4{font-size:16px;font-weight:600;margin-bottom:4px}
.chart-box .chart-sub{font-size:13px;color:var(--text3);margin-bottom:20px}
.chart-box canvas{width:100%!important;height:220px!important}

/* ═══════════════ TIMELINE ═══════════════ */
.timeline-section{padding:120px 0;background:var(--bg2)}
.timeline{position:relative;margin-top:48px;padding-left:40px}
.timeline::before{content:'';position:absolute;left:15px;top:0;bottom:0;width:2px;background:linear-gradient(to bottom,var(--blue),var(--orange),var(--red))}
.tl-item{position:relative;margin-bottom:48px;opacity:0;transform:translateX(-20px);transition:all .6s ease}
.tl-item.visible{opacity:1;transform:translateX(0)}
.tl-dot{position:absolute;left:-33px;top:4px;width:12px;height:12px;border-radius:50%;background:var(--blue);border:2px solid var(--bg2);z-index:1}
.tl-item:nth-child(even) .tl-dot{background:var(--orange)}
.tl-date{font-size:13px;color:var(--blue);font-weight:600;letter-spacing:.5px;margin-bottom:4px}
.tl-item:nth-child(even) .tl-date{color:var(--orange)}
.tl-title{font-size:18px;font-weight:600;margin-bottom:4px}
.tl-desc{font-size:14px;color:var(--text2);line-height:1.6;max-width:600px}

/* ═══════════════ INSIGHT BLOCKS ═══════════════ */
.insight-section{padding:120px 0}
.insight-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px;margin-top:48px}
.insight-card{background:linear-gradient(135deg,rgba(0,113,227,.08),rgba(255,149,0,.05));border:1px solid var(--card-border);border-radius:16px;padding:32px}
.insight-card .ic-icon{font-size:28px;margin-bottom:12px}
.insight-card h4{font-size:18px;font-weight:600;margin-bottom:8px}
.insight-card p{font-size:14px;color:var(--text2);line-height:1.7}
.insight-card .ic-tag{display:inline-block;margin-top:12px;padding:4px 12px;border-radius:100px;font-size:12px;font-weight:500}
.ic-tag.tech{background:rgba(0,113,227,.15);color:var(--blue)}
.ic-tag.society{background:rgba(48,209,88,.15);color:var(--green)}
.ic-tag.economy{background:rgba(255,149,0,.15);color:var(--orange)}
.ic-tag.manufacture{background:rgba(255,59,48,.15);color:var(--red)}

/* ═══════════════ CLOSING ═══════════════ */
.closing{padding:160px 0;text-align:center;background:var(--bg);position:relative;overflow:hidden}
.closing::before{content:'';position:absolute;top:50%;left:50%;width:600px;height:600px;background:radial-gradient(circle,rgba(0,113,227,.1),transparent 70%);transform:translate(-50%,-50%);pointer-events:none}
.closing h2{font-size:clamp(28px,5vw,56px);font-weight:700;letter-spacing:-.03em;line-height:1.15;margin-bottom:24px}
.closing h2 .w{color:var(--text)}
.closing h2 .b{color:var(--blue)}
.closing .close-sub{font-size:clamp(16px,2vw,20px);color:var(--text2);line-height:1.7;max-width:640px;margin:0 auto 48px}
.closing-cta{display:inline-flex;align-items:center;gap:8px;padding:14px 32px;background:var(--blue);border-radius:100px;color:#fff;font-size:15px;font-weight:600;transition:all .3s;cursor:pointer;border:none;font-family:var(--font)}
.closing-cta:hover{background:#0077ed;transform:scale(1.03)}

/* ═══════════════ FOOTER ═══════════════ */
.footer{padding:40px 0;text-align:center;border-top:1px solid var(--card-border);background:var(--bg)}
.footer p{font-size:12px;color:var(--text3);line-height:1.8}

/* ═══════════════ RESPONSIVE ═══════════════ */
@media(max-width:768px){
  .hero-stats{gap:20px}
  .map-wrap{flex-direction:column}
  .map-sidebar{flex:1;min-width:unset}
  .chart-grid{grid-template-columns:1fr}
  .ab-card-grid{grid-template-columns:1fr 1fr}
  .hero h1{font-size:36px}
  .hero h1 .num{font-size:48px}
}
@media(max-width:480px){
  .ab-card-grid{grid-template-columns:1fr}
  .hero-stats{flex-direction:column;gap:16px}
}

/* ═══════════════ ANIMATIONS ═══════════════ */
.reveal{opacity:0;transform:translateY(40px);transition:all .8s cubic-bezier(.4,0,.2,1)}
.reveal.visible{opacity:1;transform:translateY(0)}
.reveal-delay-1{transition-delay:.1s}
.reveal-delay-2{transition-delay:.2s}
.reveal-delay-3{transition-delay:.3s}
.reveal-delay-4{transition-delay:.4s}

/* ═══════════════ NUMBER COUNTER ═══════════════ */
.count-up{font-variant-numeric:tabular-nums}

/* ═══════════════ BAR CHART CSS ═══════════════ */
.bar-chart{display:flex;align-items:flex-end;gap:8px;height:200px;padding-top:20px}
.bar-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px}
.bar{width:100%;border-radius:6px 6px 0 0;transition:height 1.2s cubic-bezier(.4,0,.2,1);position:relative;min-height:4px}
.bar:hover{filter:brightness(1.2)}
.bar-label{font-size:11px;color:var(--text3);text-align:center;white-space:nowrap}
.bar-value{font-size:12px;font-weight:600;color:var(--text);text-align:center;opacity:0;transition:opacity .3s}
.bar-col:hover .bar-value{opacity:1}

/* ═══════════════ DONUT CHART ═══════════════ */
.donut-wrap{display:flex;align-items:center;gap:32px;flex-wrap:wrap;justify-content:center}
.donut-canvas{width:180px;height:180px}
.donut-legend{display:flex;flex-direction:column;gap:10px}
.legend-item{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text2)}
.legend-dot{width:10px;height:10px;border-radius:3px;flex-shrink:0}

/* ═══════════════ PROGRESS BARS ═══════════════ */
.progress-list{display:flex;flex-direction:column;gap:16px}
.progress-item{display:flex;flex-direction:column;gap:6px}
.progress-header{display:flex;justify-content:space-between;font-size:13px}
.progress-header .ph-name{color:var(--text2)}
.progress-header .ph-val{color:var(--text);font-weight:600}
.progress-track{height:8px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden}
.progress-fill{height:100%;border-radius:4px;transition:width 1.5s cubic-bezier(.4,0,.2,1);width:0}
</style>
</head>
<body>

<!-- ═══════════════ HERO ═══════════════ -->
<section class="hero" id="hero">
  <canvas id="particle-canvas"></canvas>
  <div class="hero-content">
    <div class="hero-badge"><span class="dot"></span>数据截至 2026年8月 · 市场监管总局</div>
    <h1>2026上半年<br>新设人形机器人企业<br><span class="num count-up" data-target="11.6">0</span><span class="num" style="font-size:.5em">万户</span></h1>
    <p class="hero-sub">平均每天诞生 <strong style="color:var(--orange)">644家</strong> 新公司。<br>比生成式AI的新设企业数量还多一倍。<br>这是创业潮，还是泡沫的前夜？</p>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="val"><span class="count-up" data-target="9.5" data-decimal="1">0</span><span class="unit">%</span></div>
        <div class="label">同比增长</div>
      </div>
      <div class="hero-stat">
        <div class="val"><span class="count-up" data-target="935">0</span><span class="unit">亿</span></div>
        <div class="label">上半年融资总额</div>
      </div>
      <div class="hero-stat">
        <div class="val"><span class="count-up" data-target="97">0</span><span class="unit">%</span></div>
        <div class="label">中国全球出货占比</div>
      </div>
      <div class="hero-stat">
        <div class="val"><span class="count-up" data-target="10">0</span><span class="unit">万台</span></div>
        <div class="label">全年预计产量</div>
      </div>
    </div>
  </div>
  <div class="scroll-hint">
    <span>向下滑动</span>
    <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
  </div>
</section>

<!-- ═══════════════ NARRATIVE: WHO IS ENTERING ═══════════════ -->
<section class="narrative section-mid" id="narrative">
  <div class="container">
    <div class="reveal">
      <div class="section-tag">🔥 谁在进场</div>
      <h2 class="section-title">三股力量，同时涌入</h2>
      <p class="section-desc">大厂带供应链，创业者带故事，地方政府带政策。像极了2016年的共享单车。</p>
    </div>
    <div class="narrative-grid">
      <div class="narr-card reveal reveal-delay-1">
        <div class="icon">🏭</div>
        <h3>跨界巨头</h3>
        <p>比亚迪发布"小迪"，小鹏IRON年底量产，小米、理想集体布局。车企带着<span class="highlight">供应链和制造能力</span>直接杀入。不需要融资，用订单说话。</p>
      </div>
      <div class="narr-card reveal reveal-delay-2">
        <div class="icon">🚀</div>
        <h3>创业公司</h3>
        <p>宇树科技IPO估值<span class="highlight">420亿</span>，智平方12轮融资估值破百亿，逐际动力半年吸金4亿美元。从"烧钱"走向"量产"的生死赛跑。</p>
      </div>
      <div class="narr-card reveal reveal-delay-3">
        <div class="icon">🏛️</div>
        <h3>政策驱动</h3>
        <p>地方政府把机器人当作下一个"新能源汽车"来布局。专项孵化器、共享试验场地、公共算力平台，<span class="highlight">降低早期投入压力</span>。</p>
      </div>
    </div>
  </div>
</section>

<!-- ═══════════════ A/B TOGGLE: HYPE vs REALITY ═══════════════ -->
<section class="ab-section section-dark" id="ab-toggle">
  <div class="container">
    <div class="ab-header reveal">
      <div class="section-tag">⚖️ 双面叙事</div>
      <h2 class="section-title">热潮数据 vs 冷思考现实</h2>
      <p class="section-desc">同一组数据，两种解读。点击切换，感受创业潮的温度与深度。</p>
      <div class="ab-toggle-wrap">
        <div class="ab-toggle">
          <button class="ab-btn active" data-panel="hot" onclick="switchAB('hot',this)">🔥 热潮数据</button>
          <button class="ab-btn" data-panel="cool" onclick="switchAB('cool',this)">🧊 冷思考</button>
          <div class="ab-slider"></div>
        </div>
      </div>
    </div>

    <div class="ab-panels">
      <!-- HOT PANEL -->
      <div class="ab-panel active" id="panel-hot">
        <div class="ab-card-grid">
          <div class="ab-card">
            <div class="big-num hot">11.6<span style="font-size:.5em">万户</span></div>
            <div class="card-label">新设企业</div>
            <div class="card-note">上半年新注册企业数，超过生成式AI的两倍</div>
          </div>
          <div class="ab-card">
            <div class="big-num hot">935<span style="font-size:.5em">亿元</span></div>
            <div class="card-label">融资总额</div>
            <div class="card-note">同比增长5倍，322笔融资事件</div>
          </div>
          <div class="ab-card">
            <div class="big-num hot">400+</div>
            <div class="card-label">整机产品</div>
            <div class="card-note">超过全球半数，技术路线百花齐放</div>
          </div>
          <div class="ab-card">
            <div class="big-num hot">20</div>
            <div class="card-label">百亿估值企业</div>
            <div class="card-note">"百亿俱乐部"持续扩容</div>
          </div>
        </div>
        <div class="ab-quote">
          "人形机器人正从'概念'走进日常，从'展品'变为'商品'。以前是人找活干，现在是<strong>活找机器人</strong>。" —— 深圳众擎机器人
        </div>
      </div>

      <!-- COOL PANEL -->
      <div class="ab-panel" id="panel-cool">
        <div class="ab-card-grid">
          <div class="ab-card">
            <div class="big-num cool">~5<span style="font-size:.5em">万台</span></div>
            <div class="card-label">全球预计出货</div>
            <div class="card-note">11.6万家企业，平均每家分不到一台</div>
          </div>
          <div class="ab-card">
            <div class="big-num cool">65%</div>
            <div class="card-label">小微企业占比</div>
            <div class="card-note">注册资本低于500万元</div>
          </div>
          <div class="ab-card">
            <div class="big-num cool">~40%</div>
            <div class="card-label">无量产时间表</div>
            <div class="card-note">约四成企业尚无明确量产计划</div>
          </div>
          <div class="ab-card">
            <div class="big-num cool">&lt;10</div>
            <div class="card-label">稳定供应商</div>
            <div class="card-note">减速器、灵巧手、传感器供应商</div>
          </div>
        </div>
        <div class="ab-quote" style="border-color:var(--blue)">
          "说到底，'人形机器人元年'更准确的叫法应该是<strong>'造梦元年'</strong>。能笑到最后的，不是讲故事最动听的那家，而是真正拿到订单、账上有钱、熬得过两三轮技术迭代的那几家。" —— 行业分析
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ═══════════════ INTERACTIVE CITY MAP ═══════════════ -->
<section class="map-section section-mid" id="city-map">
  <div class="container">
    <div class="reveal">
      <div class="section-tag">🗺️ 交互式地图</div>
      <h2 class="section-title">探索城市机器人创业生态</h2>
      <p class="section-desc">长三角、珠三角、京津冀三大区域合计占比超七成。点击城市节点，探索不同地区的创业图景。</p>
    </div>
    <div class="map-wrap reveal">
      <div class="map-canvas">
        <svg viewBox="0 0 800 600" id="china-map" xmlns="http://www.w3.org/2000/svg">
          <!-- Simplified China outline -->
          <defs>
            <radialGradient id="glow-blue" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="rgba(0,113,227,0.4)"/>
              <stop offset="100%" stop-color="rgba(0,113,227,0)"/>
            </radialGradient>
            <radialGradient id="glow-orange" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="rgba(255,149,0,0.4)"/>
              <stop offset="100%" stop-color="rgba(255,149,0,0)"/>
            </radialGradient>
            <filter id="blur-glow">
              <feGaussianBlur stdDeviation="3"/>
            </filter>
          </defs>
          <!-- Grid lines -->
          <g opacity="0.05" stroke="#fff">
            <line x1="0" y1="100" x2="800" y2="100"/><line x1="0" y1="200" x2="800" y2="200"/>
            <line x1="0" y1="300" x2="800" y2="300"/><line x1="0" y1="400" x2="800" y2="400"/>
            <line x1="0" y1="500" x2="800" y2="500"/>
            <line x1="100" y1="0" x2="100" y2="600"/><line x1="200" y1="0" x2="200" y2="600"/>
            <line x1="300" y1="0" x2="300" y2="600"/><line x1="400" y1="0" x2="400" y2="600"/>
            <line x1="500" y1="0" x2="500" y2="600"/><line x1="600" y1="0" x2="600" y2="600"/>
            <line x1="700" y1="0" x2="700" y2="600"/>
          </g>
          <!-- City nodes -->
          <g id="city-nodes">
            <!-- Beijing -->
            <circle class="city-dot" data-city="beijing" cx="520" cy="180" r="28" fill="url(#glow-blue)" opacity="0.6"/>
            <circle class="city-dot-inner" data-city="beijing" cx="520" cy="180" r="8" fill="var(--blue)" style="cursor:pointer"/>
            <text x="520" y="160" text-anchor="middle" fill="var(--text)" font-size="13" font-weight="600" style="pointer-events:none">北京</text>
            <text x="520" y="208" text-anchor="middle" fill="var(--orange)" font-size="10" style="pointer-events:none">银河通用·星海图</text>

            <!-- Shanghai -->
            <circle class="city-dot" data-city="shanghai" cx="620" cy="330" r="24" fill="url(#glow-blue)" opacity="0.6"/>
            <circle class="city-dot-inner" data-city="shanghai" cx="620" cy="330" r="7" fill="var(--blue)" style="cursor:pointer"/>
            