#!/usr/bin/env python3
"""Generate the safe-haven asset dual-rise interactive HTML."""
import textwrap

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>避险资产双升：比特币+黄金背后的故事 | 2026</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0a0a;--bg2:#111;--bg3:#1a1a1a;--t1:#fff;--t2:#888;--t3:#555;--gold:#D4AF37;--goldL:#F0D060;--btc:#F7931A;--btcL:#FFB84D;--blue:#0071e3;--border:#222}
html{scroll-behavior:smooth;background:var(--bg);color:var(--t1);font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text','Helvetica Neue',Arial,sans-serif}
body{overflow-x:hidden;line-height:1.6}
::selection{background:var(--gold);color:#000}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--t3);border-radius:3px}

/* NAV DOTS */
.nav-dots{position:fixed;right:24px;top:50%;transform:translateY(-50%);z-index:1000;display:flex;flex-direction:column;gap:12px}
.nav-dots a{width:10px;height:10px;border-radius:50%;background:var(--t3);transition:all .3s;display:block}
.nav-dots a.active{background:var(--gold);transform:scale(1.4)}
.nav-dots a:hover{background:var(--goldL)}

/* SECTIONS */
section{min-height:100vh;position:relative;display:flex;align-items:center;justify-content:center;padding:80px 40px}
.container{max-width:1100px;width:100%;margin:0 auto}

/* HERO */
#hero{background:radial-gradient(ellipse at 50% 30%,#1a1510 0%,var(--bg) 70%);flex-direction:column;text-align:center}
#hero h1{font-size:clamp(28px,5vw,56px);font-weight:700;letter-spacing:-1px;line-height:1.15;margin-bottom:24px;background:linear-gradient(135deg,var(--goldL),var(--btcL));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
#hero .subtitle{font-size:clamp(14px,2vw,20px);color:var(--t2);margin-bottom:12px;letter-spacing:2px}
#hero .year-badge{display:inline-block;padding:6px 20px;border:1px solid var(--gold);border-radius:20px;font-size:13px;color:var(--gold);letter-spacing:3px;margin-bottom:40px}
.scroll-hint{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);animation:bounce 2s infinite}
.scroll-hint span{display:block;width:24px;height:24px;border-right:2px solid var(--gold);border-bottom:2px solid var(--gold);transform:rotate(45deg);opacity:.6}
@keyframes bounce{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(12px)}}

/* PARTICLES */
#particles{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none}

/* SECTION COMMON */
.section-title{font-size:clamp(24px,4vw,42px);font-weight:700;margin-bottom:8px;letter-spacing:-0.5px}
.section-sub{font-size:clamp(13px,1.5vw,16px);color:var(--t2);margin-bottom:48px}
.gold-text{color:var(--gold)}
.btc-text{color:var(--btc)}

/* COUNTER SECTION */
.counters{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:40px}
.counter-card{background:var(--bg2);border-radius:16px;padding:40px 32px;position:relative;overflow:hidden}
.counter-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.counter-card.gold-card::before{background:linear-gradient(90deg,var(--gold),var(--goldL))}
.counter-card.btc-card::before{background:linear-gradient(90deg,var(--btc),var(--btcL))}
.counter-label{font-size:13px;color:var(--t3);text-transform:uppercase;letter-spacing:2px;margin-bottom:8px}
.counter-big{font-size:clamp(36px,5vw,56px);font-weight:700;letter-spacing:-2px;margin-bottom:4px}
.counter-sub{font-size:14px;color:var(--t2);margin-bottom:20px}
.stat-row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border);font-size:14px}
.stat-row:last-child{border:none}
.stat-label{color:var(--t2)}
.stat-val{font-weight:600}
.stat-val.green{color:#4ade80}
.stat-val.red{color:#f87171}
.sparkline{margin-top:20px;height:60px}

/* AB TOGGLE */
.ab-section{background:var(--bg2)}
.ab-toggle{display:flex;justify-content:center;gap:0;margin-bottom:40px}
.ab-btn{padding:14px 40px;font-size:15px;font-weight:600;border:2px solid var(--border);background:transparent;color:var(--t2);cursor:pointer;transition:all .4s;letter-spacing:1px}
.ab-btn:first-child{border-radius:8px 0 0 8px}
.ab-btn:last-child{border-radius:0 8px 8px 0}
.ab-btn.active-gold{background:var(--gold);color:#000;border-color:var(--gold)}
.ab-btn.active-btc{background:var(--btc);color:#000;border-color:var(--btc)}
.ab-content{position:relative;min-height:400px}
.ab-panel{opacity:0;transform:translateY(20px);transition:all .5s ease;position:absolute;top:0;left:0;right:0;pointer-events:none}
.ab-panel.visible{opacity:1;transform:translateY(0);pointer-events:auto;position:relative}
.ab-grid{display:grid;grid-template-columns:1fr 1fr;gap:32px}
.ab-stat{background:var(--bg3);border-radius:12px;padding:24px}
.ab-stat h4{font-size:13px;color:var(--t3);text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}
.ab-stat .big-num{font-size:32px;font-weight:700}
.vol-gauge{width:100%;height:120px;margin-top:8px}

/* TIMELINE */
#timeline{flex-direction:column;align-items:flex-start}
.timeline-wrap{position:relative;padding-left:40px}
.timeline-line{position:absolute;left:15px;top:0;bottom:0;width:2px;background:linear-gradient(180deg,var(--gold),var(--btc))}
.tl-item{position:relative;margin-bottom:48px;cursor:pointer}
.tl-dot{position:absolute;left:-33px;top:4px;width:16px;height:16px;border-radius:50%;border:2px solid var(--gold);background:var(--bg);transition:all .3s;z-index:2}
.tl-item:nth-child(even) .tl-dot{border-color:var(--btc)}
.tl-item:hover .tl-dot,.tl-item.open .tl-dot{background:var(--gold);transform:scale(1.3)}
.tl-item:nth-child(even):hover .tl-dot,.tl-item:nth-child(even).open .tl-dot{background:var(--btc)}
.tl-date{font-size:12px;color:var(--t3);letter-spacing:1px;text-transform:uppercase;margin-bottom:4px}
.tl-title{font-size:18px;font-weight:600;transition:color .3s}
.tl-item:hover .tl-title{color:var(--gold)}
.tl-item:nth-child(even):hover .tl-title{color:var(--btc)}
.tl-detail{max-height:0;overflow:hidden;transition:max-height .5s ease,opacity .3s;opacity:0}
.tl-item.open .tl-detail{max-height:300px;opacity:1}
.tl-detail-inner{margin-top:12px;padding:20px;background:var(--bg3);border-radius:10px;font-size:14px;color:var(--t2);line-height:1.7;border-left:3px solid var(--gold)}
.tl-item:nth-child(even) .tl-detail-inner{border-left-color:var(--btc)}

/* THREE CARDS */
.cards-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:40px}
.flip-card{height:320px;perspective:1000px;cursor:pointer}
.flip-inner{position:relative;width:100%;height:100%;transition:transform .6s;transform-style:preserve-3d}
.flip-card:hover .flip-inner{transform:rotateY(180deg)}
.flip-front,.flip-back{position:absolute;width:100%;height:100%;backface-visibility:hidden;border-radius:16px;padding:32px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.flip-front{background:linear-gradient(145deg,var(--bg2),var(--bg3));border:1px solid var(--border)}
.flip-back{background:linear-gradient(145deg,#1a1815,#15120f);transform:rotateY(180deg);border:1px solid rgba(212,175,55,.2)}
.flip-icon{font-size:48px;margin-bottom:16px}
.flip-title{font-size:20px;font-weight:700;margin-bottom:8px}
.flip-desc{font-size:13px;color:var(--t2);line-height:1.6}

/* DEBATE SPLIT */
.debate-split{display:grid;grid-template-columns:1fr 60px 1fr;gap:0;align-items:stretch;margin-top:40px}
.debate-side{padding:40px 32px;border-radius:16px}
.debate-left{background:linear-gradient(145deg,#1a1810,#14120c);border:1px solid rgba(212,175,55,.15)}
.debate-right{background:linear-gradient(145deg,#1a1510,#151008);border:1px solid rgba(247,147,26,.15)}
.debate-center{display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:900;color:var(--t3)}
.debate-side h3{font-size:22px;font-weight:700;margin-bottom:20px}
.debate-side ul{list-style:none;padding:0}
.debate-side li{padding:8px 0;font-size:14px;color:var(--t2);border-bottom:1px solid rgba(255,255,255,.05);display:flex;align-items:flex-start;gap:8px}
.debate-side li::before{content:'→';color:var(--gold);flex-shrink:0}
.debate-right li::before{color:var(--btc)}
.compare-bars{margin-top:32px}
.bar-row{margin-bottom:16px}
.bar-label{font-size:12px;color:var(--t3);margin-bottom:4px;text-transform:uppercase;letter-spacing:1px}
.bar-track{height:8px;background:var(--bg);border-radius:4px;overflow:hidden;position:relative}
.bar-fill{height:100%;border-radius:4px;transition:width 1.5s ease;width:0}
.bar-fill.gold-bar{background:linear-gradient(90deg,var(--gold),var(--goldL))}
.bar-fill.btc-bar{background:linear-gradient(90deg,var(--btc),var(--btcL))}

/* DASHBOARD */
.dash-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;margin-top:40px}
.dash-card{background:var(--bg2);border-radius:16px;padding:28px}
.dash-card h4{font-size:13px;color:var(--t3);text-transform:uppercase;letter-spacing:1px;margin-bottom:16px}
.dash-big{font-size:36px;font-weight:700;margin-bottom:4px}
.dash-sub{font-size:13px;color:var(--t2);margin-bottom:16px}
.chart-area{height:120px;position:relative}
.chart-area svg{width:100%;height:100%}

/* CLOSING */
#closing{text-align:center;background:radial-gradient(ellipse at 50% 60%,#16120c 0%,var(--bg) 70%)}
.big-quote{font-size:clamp(22px,3.5vw,38px);font-weight:600;line-height:1.4;max-width:800px;margin:0 auto 32px;letter-spacing:-0.5px}
.closing-sub{font-size:clamp(14px,1.8vw,18px);color:var(--t2);max-width:600px;margin:0 auto 40px;line-height:1.7}
.insight-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:40px}
.insight-card{background:var(--bg2);border-radius:12px;padding:24px;text-align:left;border-top:2px solid var(--gold)}
.insight-card:nth-child(2){border-top-color:var(--btc)}
.insight-card:nth-child(3){border-top-color:var(--blue)}
.insight-card h4{font-size:15px;font-weight:600;margin-bottom:8px}
.insight-card p{font-size:13px;color:var(--t2);line-height:1.6}

/* FOOTER */
.footer{text-align:center;padding:40px;font-size:12px;color:var(--t3);border-top:1px solid var(--border)}

/* RESPONSIVE */
@media(max-width:768px){
  section{padding:60px 20px}
  .counters,.ab-grid,.cards-grid,.dash-grid,.insight-cards{grid-template-columns:1fr}
  .debate-split{grid-template-columns:1fr;gap:16px}
  .debate-center{display:none}
  .nav-dots{display:none}
  .ab-content{min-height:auto}
}

/* ANIMATIONS */
.reveal{opacity:0;transform:translateY(40px);transition:all .8s cubic-bezier(.16,1,.3,1)}
.reveal.active{opacity:1;transform:translateY(0)}
.reveal-delay-1{transition-delay:.1s}
.reveal-delay-2{transition-delay:.2s}
.reveal-delay-3{transition-delay:.3s}
</style>
</head>
<body>

<!-- NAV DOTS -->
<nav class="nav-dots" id="navDots"></nav>

<!-- SECTION 1: HERO -->
<section id="hero">
  <canvas id="particles"></canvas>
  <div class="subtitle">SAFE-HAVEN ASSETS · DUAL RISE</div>
  <div class="year-badge">— 2026 —</div>
  <h1>当传统避险资产黄金<br>和数字黄金比特币<br>同时飙升</h1>
  <p style="font-size:clamp(14px,1.8vw,18px);color:var(--t2);max-width:600px;margin:0 auto 0">意味着什么？</p>
  <div class="scroll-hint"><span></span></div>
</section>

<!-- SECTION 2: THE NUMBERS -->
<section id="numbers">
  <div class="container">
    <div class="reveal">
      <div class="section-title">这一年发生了什么</div>
      <div class="section-sub">从历史高点到深度回调，再到强势反弹——两种避险资产走出了截然不同却又殊途同归的路径</div>
    </div>
    <div class="counters">
      <div class="counter-card gold-card reveal reveal-delay-1">
        <div class="counter-label">黄金 GOLD (XAU/USD)</div>
        <div class="counter-big gold-text" id="goldPrice">$4,860</div>
        <div class="counter-sub">2026年8月价格 · 年内波动 ±37%</div>
        <div class="stat-row"><span class="stat-label">历史最高</span><span class="stat-val gold-text">$5,626.80</span></div>
        <div class="stat-row"><span class="stat-label">年内最低</span><span class="stat-val red">$3,942</span></div>
        <div class="stat-row"><span class="stat-label">央行Q1购金</span><span class="stat-val green">$370亿创纪录</span></div>
        <div class="stat-row"><span class="stat-label">ETF总规模</span><span class="stat-val">$6,690亿</span></div>
        <svg class="sparkline" viewBox="0 0 300 60" preserveAspectRatio="none">
          <polyline fill="none" stroke="var(--gold)" stroke-width="2" points="0,5 30,2 60,4 90,1 120,8 150,20 180,35 210,42 240,38 270,28 300,22"/>
          <linearGradient id="goldGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--gold)" stop-opacity=".3"/><stop offset="100%" stop-color="var(--gold)" stop-opacity="0"/></linearGradient>
          <polygon fill="url(#goldGrad)" points="0,5 30,2 60,4 90,1 120,8 150,20 180,35 210,42 240,38 270,28 300,22 300,60 0,60"/>
        </svg>
      </div>
      <div class="counter-card btc-card reveal reveal-delay-2">
        <div class="counter-label">比特币 BITCOIN (BTC/USD)</div>
        <div class="counter-big btc-text" id="btcPrice">$79,455</div>
        <div class="counter-sub">2026年8月21日 · 3天暴涨24%</div>
        <div class="stat-row"><span class="stat-label">历史最高</span><span class="stat-val btc-text">$126,000</span></div>
        <div class="stat-row"><span class="stat-label">年内最低</span><span class="stat-val red">$58,000</span></div>
        <div class="stat-row"><span class="stat-label">空单爆仓</span><span class="stat-val red">$31亿(24h)</span></div>
        <div class="stat-row"><span class="stat-label">ETF累计流入</span><span class="stat-val green">$530亿+</span></div>
        <svg class="sparkline" viewBox="0 0 300 60" preserveAspectRatio="none">
          <polyline fill="none" stroke="var(--btc)" stroke-width="2" points="0,8 30,12 60,18 90,22 120,28 150,35 180,40 210,42 240,30 270,15 300,8"/>
          <linearGradient id="btcGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--btc)" stop-opacity=".3"/><stop offset="100%" stop-color="var(--btc)" stop-opacity="0"/></linearGradient>
          <polygon fill="url(#btcGrad)" points="0,8 30,12 60,18 90,22 120,28 150,35 180,40 210,42 240,30 270,15 300,8 300,60 0,60"/>
        </svg>
      </div>
    </div>
  </div>
</section>

<!-- SECTION 3: A/B COMPARISON -->
<section id="compare" class="ab-section">
  <div class="container">
    <div class="reveal">
      <div class="section-title" style="text-align:center">对比探索</div>
      <div class="section-sub" style="text-align:center">切换视角，发现两种避险资产的异同</div>
    </div>
    <div class="ab-toggle reveal">
      <button class="ab-btn active-gold" onclick="switchAB('gold')">🥇 黄金 GOLD</button>
      <button class="ab-btn" onclick="switchAB('btc')">₿ 比特币 BITCOIN</button>
    </div>
    <div class="ab-content">
      <!-- GOLD PANEL -->
      <div class="ab-panel visible" id="panel-gold">
        <div class="ab-grid">
          <div class="ab-stat">
            <h4>2026年价格走势</h4>
            <svg viewBox="0 0 400 180" style="width:100%">
              <defs><linearGradient id="gFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--gold)" stop-opacity=".4"/><stop offset="100%" stop-color="var(--gold)" stop-opacity="0"/></linearGradient></defs>
              <line x1="0" y1="30" x2="400" y2="30" stroke="#222" stroke-dasharray="4"/>
              <text x="4" y="26" fill="#555" font-size="10">$5,626</text>
              <line x1="0" y1="120" x2="400" y2="120" stroke="#222" stroke-dasharray="4"/>
              <text x="4" y="116" fill="#555" font-size="10">$3,942</text>
              <polyline fill="url(#gFill)" stroke="var(--gold)" stroke-width="2.5" stroke-linejoin="round"
                points="0,30 40,28 80,35 120,50 160,80 200,100 240,115 280,120 320,105 360,75 400,65"/>
              <circle cx="80" cy="35" r="5" fill="var(--gold)" class="pulse-dot"/>
              <text x="60" y="22" fill="var(--gold)" font-size="11" font-weight="600">ATH $5,627</text>
              <circle cx="280" cy="120" r="5" fill="#f87171" class="pulse-dot"/>
              <text x="240" y="140" fill="#f87171" font-size="11" font-weight="600">低点 $3,942</text>
              <circle cx="400" cy="65" r="5" fill="var(--gold)" class="pulse-dot"/>
              <text x="345" y="58" fill="var(--gold)" font-size="11" font-weight="600">$4,860</text>
            </svg>
          </div>
          <div class="ab-stat">
            <h4>核心属性</h4>
            <div style="margin-top:8px">
              <div class="stat-row"><span class="stat-label">共识历史</span><span class="stat-val" style="color:var(--gold)">5,000+ 年</span></div>
              <div class="stat-row"><span class="stat-label">年供给增长</span><span class="stat-val">~2% (矿业开采)</span></div>
              <div class="stat-row"><span class="stat-label">波动率 (30d)</span><span class="stat-val">15-20%</span></div>
              <div class="stat-row"><span class="stat-label">央行储备占比</span><span class="stat-val green">首次超过美国国债(1996年以来)</span></div>
              <div class="stat-row"><span class="stat-label">对手方风险</span><span class="stat-val green">零</span></div>
              <div class="stat-row"><span class="stat-label">便携性</span><span class="stat-val red">低 (物理限制)</span></div>
              <div class="stat-row"><span class="stat-label">2025年回报率</span><span class="stat-val green">+60%+</span></div>
            </div>
          </div>
          <div class="ab-stat" style="grid-column:1/-1">
            <h4>避险测试：2026年伊朗冲突</h4>
            <p style="color:var(--t2);font-size:14px;line-height:1.7">2月27日冲突爆发后48小时内，<strong style="color:var(--gold)">黄金飙升5.2%</strong>，迅速稳定在$4,700附近。央行在Q1购入535吨黄金，较2025年同期近乎翻倍。黄金展现了其作为<strong>终极避险资产</strong>的千年信用——但当通胀预期上升时，实际利率的上升反而压制了金价，导致Q2暴跌24%。</p>
          </div>
        </div>
      </div>
      <!-- BTC PANEL -->
      <div class="ab-panel" id="panel-btc">
        <div class="ab-grid">
          <div class="ab-stat">
            <h4>2026年价格走势</h4>
            <svg viewBox="0 0 400 180" style="width:100%">
              <defs><linearGradient id="bFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--btc)" stop-opacity=".4"/><stop offset="100%" stop-color="var(--btc)" stop-opacity="0"/></linearGradient></defs>
              <line x1="0" y1="10" x2="400" y2="10" stroke="#222" stroke-dasharray="4"/>
              <text x="4" y="22" fill="#555" font-size="10">$126K (2025.10 ATH)</text>
              <polyline fill="url(#bFill)" stroke="var(--btc)" stroke-width="2.5" stroke-linejoin="round"
                points="0,10 40,30 80,60 120,90 160,110 200,125 240,130 280,135 320,100 360,65 400,55"/>
              <circle cx="0" cy="10" r="5" fill="var(--btc)" class="pulse-dot"/>
              <text x="10" y="8" fill="var(--btc)" font-size="11" font-weight="600">$126K ATH</text>
              <circle cx="280" cy="135" r="5" fill="#f87171" class="pulse-dot"/>
              <text x="240" y="155" fill="#f87171" font-size="11" font-weight="600">低点 ~$58K</text>
              <circle cx="400" cy="55" r="5" fill="var(--btc)" class="pulse-dot"/>
              <text x="340" y="48" fill="var(--btc)" font-size="11" font-weight="600">$79,455</text>
            </svg>
          </div>
          <div class="ab-stat">
            <h4>核心属性</h4>
            <div style="margin-top:8px">
              <div class="stat-row"><span class="stat-label">供给上限</span><span class="stat-val" style="color:var(--btc)">2,100万 (绝对稀缺)</span></div>
              <div class="stat-row"><span class="stat-label">年供给增长</span><span class="stat-val green">~0% (算法锁定)</span></div>
              <div class="stat-row"><span class="stat-label">波动率 (30d)</span><span class="stat-val red">20-39%</span></div>
              <div class="stat-row"><span class="stat-label">S&P 500相关性</span><span class="stat-val red">0.74 (像风险资产)</span></div>
              <div class="stat-row"><span class="stat-label">对手方风险</span><span class="stat-val green">零 (去中心化)</span></div>
              <div class="stat-row"><span class="stat-label">便携性</span><span class="stat-val green">极高 (12个助记词=全部财富)</span></div>
              <div class="stat-row"><span class="stat-label">ETF累计流入</span><span class="stat-val green">$530亿+</span></div>
            </div>
          </div>
          <div class="ab-stat" style="grid-column:1/-1">
            <h4>避险测试：2026年伊朗冲突</h4>
            <p style="color:var(--t2);font-size:14px;line-height:1.7">冲突爆发后48小时，<strong style="color:var(--btc)">比特币暴跌12%</strong>，一度跌至$72,000。但战争暴露了BTC的独特优势：<strong>便携性</strong>。迪拜黄金物流中断，而伊朗最大交易所Nobitex流出量暴增700%——人们用12个助记词带着全部财富穿越边境。BTC不是传统避险资产，而是<strong>战时流动性工具</strong>。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- SECTION 4: TIMELINE -->
<section id="timeline">
  <div class="container">
    <div class="reveal">
      <div class="section-title">关键时间线</div>
      <div class="section-sub">点击事件节点，展开深度解读</div>
    </div>
    <div class="timeline-wrap reveal">
      <div class="timeline-line"></div>

      <div class="tl-item" onclick="toggleTimeline(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年1月29日</div>
        <div class="tl-title gold-text">黄金创历史新高 $5,626.80</div>
        <div class="tl-detail"><div class="tl-detail-inner">
          <strong>伊朗冲突引爆避险潮。</strong>黄金触及COMEX期货历史高点$5,626.80/盎司。ETF单月流入$190亿创纪录，总规模达$6,690亿。央行Q1购金244吨，支出$370亿创单季纪录。这一水平在两年前几乎无法想象。
        </div></div>
      </div>

      <div class="tl-item" onclick="toggleTimeline(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年2月27日</div>
        <div class="tl-title">美伊战争爆发 — 避险资产的实时压力测试</div>
        <div class="tl-detail"><div class="tl-detail-inner">
          <strong>黄金+5.2% vs BTC-12%。</strong>冲突爆发后48小时内出现戏剧性分化：黄金飙升5.2%后稳定在$4,700；比特币暴跌12%，一路下探至$72,000。1年滚动相关性降至-0.17。BTC与纳斯达克100同步下跌——数字黄金的安全港叙事遭遇最严峻的实证挑战。
        </div></div>
      </div>

      <div class="tl-item" onclick="toggleTimeline(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年3月-4月</div>
        <div class="tl-title btc-text">BTC与S&P 500相关性飙至0.74</div>
        <div class="tl-detail"><div class="tl-detail-inner">
          <strong>数字黄金的身份危机。</strong>比特币30天价格走势与标普500高度同步。Strategy(MicroStrategy)仍在战争中购入$12亿BTC，但短期流动性压力主导价格。CoinDesk评论："BTC不是避险资产，也不是纯风险资产，它已成为一个全天候流动性池。"
        </div></div>
      </div>

      <div class="tl-item" onclick="toggleTimeline(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年6月30日</div>
        <div class="tl-title gold-text">黄金跌至年内低点 $3,942</div>
        <div class="tl-detail"><div class="tl-detail-inner">
          <strong>加息恐惧压制避险逻辑。</strong>战争推高油价→通胀预期上升→市场预期美联储鹰派→实际利率上升→无息资产黄金承压。Q2暴跌22-24%，创2