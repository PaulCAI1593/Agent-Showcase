#!/usr/bin/env python3
"""Generate the Capital Migration Interactive Dashboard HTML"""

import os

OUTPUT = '/app/working/shared/showcase/2026-08-11-capital-migration.html'

html_parts = []

def P(s):
    html_parts.append(s)

# ── HEAD + CSS ──
P('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全球资本大迁徙 — 黄金$4400+ & 美元跌破100 | 交互仪表盘</title>
<meta name="description" content="2026年8月，全球资本正在经历史无前例的大迁徙：黄金突破$4400，美元指数跌破100。深度交互体验，看清钱的流向。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=DM+Serif+Display&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --gold:#D4A843;--gold-bright:#FFD700;--gold-dim:#8B7335;
  --green:#00E676;--green-dim:#00A152;
  --red:#FF4757;--blue:#4FC3F7;
  --bg:#06060C;--bg2:#0D0D15;--bg3:#13131F;--bg4:#1A1A28;
  --t1:#F0F0F8;--t2:#9999B0;--t3:#555570;--t4:#333345;
  --glass:rgba(13,13,21,0.75);
  --radius:12px;--radius-lg:20px;
}
html{scroll-behavior:smooth;overflow-x:hidden}
body{background:var(--bg);color:var(--t1);font-family:'Noto Sans SC',system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased}
.serif{font-family:'DM Serif Display','Noto Sans SC',serif}
.mono{font-family:'JetBrains Mono',monospace}

::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--gold-dim);border-radius:3px}

a{color:var(--gold);text-decoration:none}

/* ── NAV ── */
.topnav{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:14px 32px;background:rgba(6,6,12,0.8);backdrop-filter:blur(24px) saturate(1.4);border-bottom:1px solid rgba(212,168,67,0.08);transition:transform .3s}
.topnav.hidden{transform:translateY(-100%)}
.nav-brand{font-family:'DM Serif Display',serif;font-size:18px;color:var(--gold);letter-spacing:1px}
.nav-brand span{color:var(--t3);font-size:12px;font-family:'JetBrains Mono',monospace;margin-left:8px}
.nav-pills{display:flex;gap:4px}
.nav-pill{padding:6px 14px;border-radius:20px;font-size:12px;font-weight:500;color:var(--t2);background:transparent;border:none;cursor:pointer;transition:all .25s;letter-spacing:.3px}
.nav-pill:hover{color:var(--gold);background:rgba(212,168,67,0.08)}
.nav-pill.on{color:var(--bg);background:var(--gold);font-weight:700}

/* ── HERO ── */
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:100px 32px 60px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 50% at 50% 20%,rgba(212,168,67,0.07),transparent 70%),radial-gradient(ellipse 60% 40% at 80% 70%,rgba(0,230,118,0.04),transparent 60%)}
.hero-tag{font-size:12px;letter-spacing:5px;text-transform:uppercase;color:var(--gold);margin-bottom:20px;font-weight:500;position:relative}
.hero-tag::before,.hero-tag::after{content:'';position:absolute;top:50%;width:40px;height:1px;background:var(--gold-dim)}
.hero-tag::before{right:calc(100% + 12px)}
.hero-tag::after{left:calc(100% + 12px)}
.hero-h1{font-family:'DM Serif Display',serif;font-size:clamp(40px,7vw,80px);line-height:1.05;margin-bottom:24px;position:relative}
.hero-h1 .g{color:var(--gold-bright);text-shadow:0 0 60px rgba(255,215,0,0.25)}
.hero-h1 .r{color:var(--red);text-shadow:0 0 40px rgba(255,71,87,0.2)}
.hero-sub{font-size:clamp(15px,1.8vw,20px);color:var(--t2);max-width:640px;margin:0 auto 48px;font-weight:300;position:relative}
.hero-kpi-row{display:flex;gap:32px;flex-wrap:wrap;justify-content:center;position:relative}
.hero-kpi{text-align:center;min-width:140px}
.hero-kpi-val{font-family:'DM Serif Display',serif;font-size:clamp(30px,4vw,52px);font-weight:900;line-height:1}
.hero-kpi-val.up{color:var(--gold-bright)}
.hero-kpi-val.dn{color:var(--red)}
.hero-kpi-val.nt{color:var(--blue)}
.hero-kpi-lbl{font-size:11px;color:var(--t3);letter-spacing:2px;text-transform:uppercase;margin-top:8px}
.hero-scroll{position:absolute;bottom:32px;display:flex;flex-direction:column;align-items:center;gap:6px;opacity:.5}
.hero-scroll span{font-size:10px;letter-spacing:3px;color:var(--t4)}
.hero-scroll i{display:block;width:1px;height:32px;background:linear-gradient(to bottom,var(--gold-dim),transparent);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:.3}50%{opacity:1}}

/* ── SECTIONS ── */
.sec{padding:100px 32px;position:relative;z-index:1}
.sec-inner{max-width:1080px;margin:0 auto}
.sec-tag{display:inline-flex;align-items:center;gap:6px;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--gold);margin-bottom:12px;font-weight:600}
.sec-tag::before{content:'';display:block;width:20px;height:2px;background:var(--gold)}
.sec-h2{font-family:'DM Serif Display',serif;font-size:clamp(28px,4.5vw,52px);line-height:1.1;margin-bottom:12px}
.sec-desc{font-size:16px;color:var(--t2);max-width:620px;margin-bottom:40px}
.divider{width:60px;height:2px;background:linear-gradient(90deg,var(--gold),transparent);margin:40px 0}

/* ── CARDS ── */
.card{background:var(--bg3);border:1px solid rgba(255,255,255,0.04);border-radius:var(--radius);padding:28px;transition:all .35s}
.card:hover{border-color:rgba(212,168,67,0.15);transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,0,0,0.3)}
.card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.card-icon{font-size:28px;margin-bottom:12px}
.card-title{font-size:14px;font-weight:600;margin-bottom:6px}
.card-val{font-family:'DM Serif Display',serif;font-size:28px;font-weight:900;color:var(--gold-bright)}
.card-chg{font-size:12px;margin-top:4px}
.card-chg.up{color:var(--green)}
.card-chg.dn{color:var(--red)}

/* ── TIMELINE ── */
.tl{position:relative;padding:20px 0}
.tl::before{content:'';position:absolute;left:50%;top:0;bottom:0;width:2px;background:linear-gradient(to bottom,transparent 5%,var(--gold-dim) 20%,var(--gold) 50%,var(--gold-dim) 80%,transparent 95%);transform:translateX(-50%)}
.tl-node{display:flex;align-items:center;margin-bottom:48px;position:relative}
.tl-node:nth-child(even){flex-direction:row-reverse}
.tl-content{flex:1;padding:0 48px}
.tl-node:nth-child(even) .tl-content{text-align:right}
.tl-dot{width:14px;height:14px;background:var(--gold);border:3px solid var(--bg);border-radius:50%;position:absolute;left:50%;transform:translateX(-50%);z-index:2;box-shadow:0 0 16px rgba(212,168,67,0.5)}
.tl-date{font-size:12px;color:var(--gold);letter-spacing:1px;font-weight:600;margin-bottom:2px}
.tl-price{font-family:'DM Serif Display',serif;font-size:26px;font-weight:900;color:var(--gold-bright)}
.tl-note{font-size:13px;color:var(--t2);margin-top:4px}
@media(max-width:768px){
  .tl::before{left:20px}
  .tl-node,.tl-node:nth-child(even){flex-direction:column;align-items:flex-start}
  .tl-content,.tl-node:nth-child(even) .tl-content{padding:0 0 0 44px;text-align:left}
  .tl-dot{left:20px}
}

/* ── CHART BOX ── */
.chartbox{background:var(--bg3);border:1px solid rgba(255,255,255,0.04);border-radius:var(--radius-lg);padding:32px;margin:32px 0;position:relative;overflow:hidden}
.chartbox canvas{width:100%!important;max-height:380px}
.chart-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px}
.chart-title{font-size:16px;font-weight:700}
.tabs{display:flex;gap:6px}
.tab{padding:5px 14px;border-radius:20px;font-size:12px;border:1px solid var(--t4);background:transparent;color:var(--t2);cursor:pointer;transition:all .2s}
.tab.on{background:var(--gold);color:var(--bg);border-color:var(--gold);font-weight:700}
.tab:hover:not(.on){border-color:var(--gold);color:var(--gold)}

/* ── BANK GRID ── */
.bank-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:32px 0}
.bank-card{background:var(--bg3);border:1px solid rgba(255,255,255,0.04);border-radius:var(--radius);padding:22px;text-align:center;transition:all .35s;cursor:pointer}
.bank-card:hover{border-color:rgba(212,168,67,0.25);transform:translateY(-3px)}
.bank-flag{font-size:36px;margin-bottom:8px}
.bank-name{font-size:13px;font-weight:600;margin-bottom:4px}
.bank-val{font-family:'DM Serif Display',serif;font-size:20px;font-weight:900;color:var(--gold-bright)}
.bank-chg{font-size:11px;color:var(--green);margin-top:4px}
.bank-bar{height:3px;background:var(--t4);border-radius:2px;margin-top:10px;overflow:hidden}
.bank-bar i{display:block;height:100%;background:linear-gradient(90deg,var(--gold-dim),var(--gold-bright));border-radius:2px;width:0;transition:width 1.5s cubic-bezier(.22,1,.36,1)}

/* ── RATE BARS ── */
.rate-row{display:flex;align-items:center;gap:14px;margin-bottom:18px}
.rate-flag{font-size:26px;width:36px;text-align:center;flex-shrink:0}
.rate-info{flex:1}
.rate-name{font-size:13px;display:flex;justify-content:space-between;margin-bottom:3px}
.rate-name b{color:var(--gold-bright);font-family:'JetBrains Mono',monospace;font-weight:700}
.rate-bg{height:6px;background:var(--t4);border-radius:3px;overflow:hidden}
.rate-fill{height:100%;border-radius:3px;width:0;transition:width 2s cubic-bezier(.22,1,.36,1)}

/* ── FLOW VIZ ── */
.flow-wrap{position:relative;min-height:460px;margin:32px 0}
.flow-node{position:absolute;background:var(--bg3);border:1px solid rgba(212,168,67,0.15);border-radius:var(--radius);padding:18px 22px;text-align:center;transition:all .35s;cursor:pointer;z-index:2}
.flow-node:hover{border-color:var(--gold);box-shadow:0 0 24px rgba(212,168,67,0.12);transform:scale(1.06)}
.flow-node h4{font-size:13px;font-weight:600;margin-bottom:2px}
.flow-node .fv{font-family:'DM Serif Display',serif;font-size:20px;font-weight:900;color:var(--gold-bright)}
.flow-svg{position:absolute;inset:0;z-index:1;pointer-events:none}

/* ── A/B COMPARE ── */
.ab{display:grid;grid-template-columns:1fr 1fr;gap:0;border-radius:var(--radius-lg);overflow:hidden;margin:32px 0;border:1px solid rgba(255,255,255,0.04)}
.ab-side{padding:36px;cursor:pointer;transition:background .3s}
.ab-side:hover{background:var(--bg4)}
.ab-side.a{border-right:1px solid rgba(255,255,255,0.04)}
.ab-lbl{font-size:10px;letter-spacing:3px;text-transform:uppercase;font-weight:700;margin-bottom:16px}
.ab-lbl.hawk{color:var(--red)}
.ab-lbl.dove{color:var(--green)}
.ab-row{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.03)}
.ab-row:last-child{border-bottom:none}
.ab-row .k{font-size:13px;color:var(--t2)}
.ab-row .v{font-size:14px;font-weight:700}
.ab-row .v.up{color:var(--green)}
.ab-row .v.dn{color:var(--red)}
@media(max-width:768px){.ab{grid-template-columns:1fr}.ab-side.a{border-right:none;border-bottom:1px solid rgba(255,255,255,0.04)}}

/* ── QUOTE ── */
.quote-box{background:linear-gradient(135deg,rgba(212,168,67,0.06),rgba(0,230,118,0.03));border:1px solid rgba(212,168,67,0.12);border-radius:var(--radius-lg);padding:48px;margin:40px 0;position:relative;overflow:hidden}
.quote-box::before{content:'';position:absolute;top:-40%;right:-15%;width:280px;height:280px;background:radial-gradient(circle,rgba(212,168,67,0.08),transparent 70%);border-radius:50%}
.quote-txt{font-family:'DM Serif Display',serif;font-size:clamp(20px,3vw,30px);line-height:1.35;margin-bottom:12px;position:relative}
.quote-src{font-size:12px;color:var(--t3);position:relative}

/* ── FOOTER ── */
.foot{padding:48px 32px;text-align:center;border-top:1px solid rgba(255,255,255,0.03)}
.foot p{font-size:12px;color:var(--t4);line-height:1.8}
.foot .g{color:var(--gold)}

/* ── REVEAL ANIM ── */
.rv{opacity:0;transform:translateY(36px);transition:opacity .8s cubic-bezier(.16,1,.3,1),transform .8s cubic-bezier(.16,1,.3,1)}
.rv.vis{opacity:1;transform:none}
.rv.d1{transition-delay:.1s}.rv.d2{transition-delay:.2s}.rv.d3{transition-delay:.3s}.rv.d4{transition-delay:.4s}

/* ── LOADING ── */
.loader{position:fixed;inset:0;background:var(--bg);z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;transition:opacity .6s,visibility .6s}
.loader.off{opacity:0;visibility:hidden}
.loader-bar{width:180px;height:2px;background:var(--t4);border-radius:1px;overflow:hidden;margin-top:18px}
.loader-bar i{display:block;height:100%;background:var(--gold);width:0;transition:width .3s}
.loader-t{font-size:10px;color:var(--t4);letter-spacing:3px;margin-top:10px}
</style>
</head>
<body>

<div class="loader" id="loader">
  <div style="font-family:'DM Serif Display',serif;font-size:28px"><span style="color:var(--gold)">CAPITAL</span> <span style="color:var(--t3)">MIGRATION</span></div>
  <div class="loader-bar"><i id="lb"></i></div>
  <div class="loader-t">LOADING DATA FEEDS...</div>
</div>

<nav class="topnav" id="topnav">
  <div class="nav-brand">CAPITAL MIGRATION <span>2026.08</span></div>
  <div class="nav-pills" id="navPills">
    <button class="nav-pill on" data-t="hero">总览</button>
    <button class="nav-pill" data-t="sec-gold">黄金</button>
    <button class="nav-pill" data-t="sec-dollar">美元</button>
    <button class="nav-pill" data-t="sec-bank">央行</button>
    <button class="nav-pill" data-t="sec-rate">利率</button>
    <button class="nav-pill" data-t="sec-flow">流向</button>
    <button class="nav-pill" data-t="sec-end">结论</button>
  </div>
</nav>

<!-- ═══════ HERO ═══════ -->
<section class="hero" id="hero">
  <div class="hero-tag">2026年8月 · 全球资本市场实时观测</div>
  <h1 class="hero-h1">当<span class="g">$4,400</span>的黄金<br>遇上<span class="r">&lt;100</span>的美元</h1>
  <p class="hero-sub">全球资本正在经历一场史无前例的大迁徙。这不是市场噪音，而是全球货币体系重构的信号。</p>
  <div class="hero-kpi-row">
    <div class="hero-kpi"><div class="hero-kpi-val up" data-count="4432" data-prefix="$" data-suffix="">$0</div><div class="hero-kpi-lbl">COMEX黄金峰值</div></div>
    <div class="hero-kpi"><div class="hero-kpi-val dn" data-count="99.54" data-prefix="" data-suffix="" data-dec="2">0</div><div class="hero-kpi-lbl">美元指数 DXY</div></div>
    <div class="hero-kpi"><div class="hero-kpi-val up" style="color:var(--gold)" data-count="289" data-prefix="" data-suffix="吨">0</div><div class="hero-kpi-lbl">Q2央行净购金</div></div>
    <div class="hero-kpi"><div class="hero-kpi-val nt" data-count="7608" data-prefix="" data-suffix="万盎司">0</div><div class="hero-kpi-lbl">中国黄金储备</div></div>
  </div>
  <div class="hero-scroll"><span>SCROLL</span><i></i></div>
</section>
''')

# ── SECTION: GOLD TIMELINE ──
P('''
<!-- ═══════ GOLD TIMELINE ═══════ -->
<section class="sec" id="sec-gold">
  <div class="sec-inner">
    <div class="sec-tag rv">第一章</div>
    <h2 class="sec-h2 rv">黄金的史诗级<span style="color:var(--gold-bright)">狂飙</span></h2>
    <p class="sec-desc rv">从2024年初的$2,000到2026年8月的$4,432——黄金用两年半时间完成了120%的涨幅，创下人类历史最长牛市纪录。</p>
    <div class="tl rv">
      <div class="tl-node"><div class="tl-content"><div class="tl-date">2024年1月</div><div class="tl-price">$2,050</div><div class="tl-note">起点：美联储暂停加息，市场等待方向</div></div><div class="tl-dot"></div></div>
      <div class="tl-node"><div class="tl-content"><div class="tl-date">2024年6月</div><div class="tl-price">$2,380</div><div class="tl-note">央行购金潮启动，中国连续18个月增持</div></div><div class="tl-dot"></div></div>
      <div class="tl-node"><div class="tl-content"><div class="tl-date">2024年10月</div><div class="tl-price">$2,790</div><div class="tl-note">美联储首次降息50bp，全球降息潮开启</div></div><div class="tl-dot"></div></div>
      <div class="tl-node"><div class="tl-content"><div class="tl-date">2025年4月</div><div class="tl-price">$3,400</div><div class="tl-note">特朗普"对等关税"引发全球贸易战恐慌</div></div><div class="tl-dot"></div></div>
      <div class="tl-node"><div class="tl-content"><div class="tl-date">2025年12月</div><div class="tl-price">$3,750</div><div class="tl-note">美联储年内第三次降息至3.5%-3.75%</div></div><div class="tl-dot"></div></div>
      <div class="tl-node"><div class="tl-content"><div class="tl-date">2026年6月</div><div class="tl-price">$4,030</div><div class="tl-note">黄金占全球储备27%，超越美债22%</div></div><div class="tl-dot"></div></div>
      <div class="tl-node"><div class="tl-content"><div class="tl-date">2026年8月7日</div><div class="tl-price">$4,432</div><div class="tl-note">COMEX突破$4400，非农爆冷引发恐慌性买盘</div></div><div class="tl-dot"></div></div>
      <div class="tl-node"><div class="tl-content"><div class="tl-date">2026年8月8日</div><div class="tl-price">$4,342</div><div class="tl-note">现货黄金周涨幅超7%，六个月最大单周涨幅</div></div><div class="tl-dot"></div></div>
    </div>

    <div class="chartbox rv">
      <div class="chart-top">
        <div class="chart-title">黄金价格走势 (2024-2026)</div>
        <div class="tabs">
          <button class="tab on" data-range="all">全部</button>
          <button class="tab" data-range="2026">2026</button>
          <button class="tab" data-range="6m">近6月</button>
        </div>
      </div>
      <canvas id="goldChart" height="360"></canvas>
    </div>

    <div class="card-grid rv">
      <div class="card"><div class="card-icon">📈</div><div class="card-title">COMEX黄金期货</div><div class="card-val">$4,401</div><div class="card-chg up">▲ +2.37% 周涨幅 +7%</div></div>
      <div class="card"><div class="card-icon">💎</div><div class="card-title">现货黄金 XAU</div><div class="card-val">$4,342</div><div class="card-chg up">▲ +2.40% 创6月来新高</div></div>
      <div class="card"><div class="card-icon">🏦</div><div class="card-title">国内AU9999</div><div class="card-val">¥940/克</div><div class="card-chg up">▲ 周大福足金 ¥1,310/克</div></div>
      <div class="card"><div class="card-icon">📊</div><div class="card-title">GLD ETF价格</div><div class="card-val">$376.3</div><div class="card-chg up">▲ 管理规模 $2,330亿</div></div>
    </div>
  </div>
</section>
''')

# ── SECTION: DXY COLLAPSE ──
P('''
<!-- ═══════ DXY COLLAPSE ═══════ -->
<section class="sec" id="sec-dollar" style="background:var(--bg2)">
  <div class="sec-inner">
    <div class="sec-tag rv">第二章</div>
    <h2 class="sec-h2 rv">美元指数<span style="color:var(--red)">跌破100</span></h2>
    <p class="sec-desc rv">100——这不是一个普通的数字。它是美元霸权的心理防线。2026年7月30日，DXY盘中跌破100大关，8月7日收于99.54，创2023年7月以来新低。</p>

    <div class="chartbox rv">
      <div class="chart-top">
        <div class="chart-title">美元指数 DXY 走势</div>
        <div class="tabs">
          <button class="tab on">2026</button>
          <button class="tab">2025-2026</button>
        </div>
      </div>
      <canvas id="dxyChart" height="320"></canvas>
    </div>

    <div class="card-grid rv">
      <div class="card"><div class="card-icon">📉</div><div class="card-title">DXY 收盘价</div><div class="card-val" style="color:var(--red)">99.54</div><div class="card-chg dn">▼ -0.39% 8月7日</div></div>
      <div class="card"><div class="card-icon">🔑</div><div class="card-title">关键心理关口</div><div class="card-val" style="color:var(--red)">100</div><div class="card-chg dn">▼ 7月30日首次跌破</div></div>
      <div class="card"><div class="card-icon">📉</div><div class="card-title">月内累计跌幅</div><div class="card-val" style="color:var(--red)">-2.5%</div><div class="card-chg dn">▼ 连续下行走弱</div></div>
      <div class="card"><div class="card-icon">🌐</div><div class="card-title">影响</div><div class="card-val" style="color:var(--green)">资本外流</div><div class="card-chg up">新兴市场获益</div></div>
    </div>

    <div class="quote-box rv">
      <div class="quote-txt">"美元指数跌破100——这不是数字游戏，而是全球资本流向的转折点。"</div>
      <div class="quote-src">—— 2026年7月30日，多家财经媒体头版标题</div>
    </div>
  </div>
</section>
''')

# ── SECTION: CENTRAL BANK ──
P('''
<!-- ═══════ CENTRAL BANK ═══════ -->
<section class="sec" id="sec-bank">
  <div class="sec-inner">
    <div class="sec-tag rv">第三章</div>
    <h2 class="sec-h2 rv">全球央行的<span style="color:var(--gold-bright)">购金狂潮</span></h2>
    <p class="sec-desc rv">黄金在全球官方储备中的占比已达27%，超越美国国债的22%。89%的央行储备管理者预计，未来12个月黄金储备将继续增加。</p>

    <div class="bank-grid rv">
      <div class="bank-card"><div class="bank-flag">🇨🇳</div><div class="bank-name">中国</div><div class="bank-val">7,608万盎司</div><div class="bank-chg">连续21个月增持 ▲</div><div class="bank-bar"><i data-w="95%"></i></div></div>
      <div class="bank-card"><div class="bank-flag">🇮🇳</div><div class="bank-name">印度</div><div class="bank-val">$1,152亿</div><div class="bank-chg">储备价值持续攀升 ▲</div><div class="bank-bar"><i data-w="65%"></i></div></div>
      <div class="bank-card"><div class="bank-flag">🇷🇺</div><div class="bank-name">俄罗斯</div><div class="bank-val">2,330吨</div><div class="bank-chg">全球第三大持有国 ▲</div><div class="bank-bar"><i data-w="80%"></i></div></div>
      <div class="bank-card"><div class="bank-flag">🇵🇱</div><div class="bank-name">波兰</div><div class="bank-val">420吨</div><div class="bank-chg">欧洲最大买家 ▲</div><div class="bank-bar"><i data-w="55%"></i></div></div>
      <div class="bank-card"><div class="bank-flag">🇹🇷</div><div class="bank-name">土耳其</div><div class="bank-val">540吨</div><div class="bank-chg">连续增持中 ▲</div><div class="bank-bar"><i data-w="60%"></i></div></div>
      <div class="bank-card"><div class="bank-flag">🌍</div><div class="bank-name">全球合计</div><div class="bank-val">289吨/季</div><div class="bank-chg" style="color:var(--green)">Q2同比增长62% ▲▲</div><div class="bank-bar"><i data-w="100%"></i></div></div>
    </div>

    <div class="chartbox rv">
      <div class="chart-top">
        <div class="chart-title">黄金 vs 美债 — 全球储备资产占比</div>
        <div class="tabs">
          <button class="tab on">2026 Q2</button>
          <button class="tab">2020</button>
        </div>
      </div>
      <canvas id="reserveChart" height="300"></canvas>
    </div>

    <div class="quote-box rv">
      <div class="quote-txt">"黄金在全球官方储备资产中的占比升至27%，首次超越美国国债的22%，成为全球储备第一大资产。"</div>
      <div class="quote-src">—— 欧洲中央银行 2026年6月报告</div>
    </div>
  </div>
</section>
''')

# ── SECTION: RATE DIVERGENCE ──
P('''
<!-- ═══════ RATE DIVERGENCE ═══════ -->
<section class="sec" id="sec-rate" style="background:var(--bg2)">
  <div class="sec-inner">
    <div class="sec-tag rv">第四章