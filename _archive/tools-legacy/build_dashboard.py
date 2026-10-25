#!/usr/bin/env python3
"""Build the Capital Migration Dashboard HTML file."""
import os

OUTPUT = "/app/working/shared/showcase/2026-08-11-capital-migration.html"

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>全球资本大迁徙 — 黄金$4400+ 美元跌破100</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=DM+Serif+Display&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --gold:#D4A843;--gold-bright:#FFD700;--gold-glow:rgba(255,215,0,.25);
  --green:#00E676;--green-dim:rgba(0,230,118,.15);
  --red:#FF4757;--red-dim:rgba(255,71,87,.15);
  --bg:#08080E;--bg2:#0E0E16;--card:#13131D;--card2:#1A1A28;
  --t1:#F0F0F5;--t2:#9999AA;--t3:#555568;
  --radius:12px;
}
html{scroll-behavior:smooth;background:var(--bg)}
body{font-family:'Noto Sans SC',system-ui,sans-serif;color:var(--t1);overflow-x:hidden;line-height:1.65}
h1,h2,h3{font-family:'DM Serif Display','Noto Sans SC',serif}
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--gold);border-radius:3px}

/* ══ NAV ══ */
.nav{position:fixed;top:0;left:0;right:0;z-index:999;display:flex;justify-content:space-between;align-items:center;padding:0 40px;height:56px;backdrop-filter:blur(24px);background:rgba(8,8,14,.72);border-bottom:1px solid rgba(212,168,67,.08)}
.nav-brand{font-family:'DM Serif Display',serif;font-size:17px;color:var(--gold);letter-spacing:.5px}
.nav-links{display:flex;gap:20px}
.nav-links a{color:var(--t3);text-decoration:none;font-size:12px;font-weight:500;letter-spacing:1px;text-transform:uppercase;transition:color .3s}
.nav-links a:hover,.nav-links a.active{color:var(--gold)}

/* ══ HERO ══ */
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:100px 24px 60px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 50% at 50% 40%,rgba(212,168,67,.07),transparent 70%)}
.hero-tag{font-size:11px;letter-spacing:5px;text-transform:uppercase;color:var(--gold);margin-bottom:20px;font-weight:600}
.hero h1{font-size:clamp(32px,5.5vw,68px);line-height:1.08;margin-bottom:20px}
.hero h1 .g{color:var(--gold-bright);text-shadow:0 0 48px var(--gold-glow)}
.hero h1 .r{color:var(--red);text-shadow:0 0 30px var(--red-dim)}
.hero-sub{font-size:clamp(15px,1.8vw,20px);color:var(--t2);max-width:620px;margin:0 auto 48px;font-weight:300}
.hero-kpi{display:flex;gap:48px;flex-wrap:wrap;justify-content:center}
.kpi{text-align:center}
.kpi-val{font-family:'DM Serif Display',serif;font-size:clamp(28px,3.5vw,48px);font-weight:700}
.kpi-val.up{color:var(--gold-bright)}
.kpi-val.dn{color:var(--red)}
.kpi-val.bl{color:#4FC3F7}
.kpi-lbl{font-size:11px;color:var(--t3);letter-spacing:2px;text-transform:uppercase;margin-top:2px}

/* ══ SECTION ══ */
.sec{padding:100px 24px;position:relative;z-index:1}
.sec-inner{max-width:1060px;margin:0 auto}
.sec-label{font-size:11px;letter-spacing:4px;text-transform:uppercase;color:var(--gold);margin-bottom:10px;font-weight:600}
.sec-title{font-size:clamp(26px,3.8vw,44px);margin-bottom:14px;line-height:1.12}
.sec-desc{font-size:16px;color:var(--t2);max-width:640px;line-height:1.75;margin-bottom:40px}

/* ══ CARDS ══ */
.card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.card{background:var(--card);border:1px solid rgba(255,255,255,.04);border-radius:var(--radius);padding:24px;transition:all .35s;cursor:default;position:relative;overflow:hidden}
.card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--gold),var(--gold-bright));transform:scaleX(0);transition:transform .35s;transform-origin:left}
.card:hover{transform:translateY(-3px);border-color:rgba(212,168,67,.18);background:var(--card2)}
.card:hover::after{transform:scaleX(1)}
.card-icon{font-size:28px;margin-bottom:12px}
.card-title{font-size:13px;font-weight:600;margin-bottom:6px}
.card-val{font-family:'DM Serif Display',serif;font-size:26px;font-weight:700;color:var(--gold-bright)}
.card-chg{font-size:12px;margin-top:4px}
.card-chg.pos{color:var(--green)}
.card-chg.neg{color:var(--red)}

/* ══ TIMELINE ══ */
.tl{position:relative;max-width:900px;margin:0 auto}
.tl::before{content:'';position:absolute;left:50%;top:0;bottom:0;width:2px;background:linear-gradient(to bottom,transparent 0%,var(--gold) 15%,var(--gold) 85%,transparent 100%);transform:translateX(-50%)}
.tl-row{display:flex;align-items:flex-start;margin-bottom:48px;position:relative}
.tl-row:nth-child(odd){flex-direction:row-reverse}
.tl-row:nth-child(odd) .tl-body{text-align:right;padding-right:56px;padding-left:0}
.tl-body{flex:1;padding-left:56px}
.tl-dot{width:14px;height:14px;border-radius:50%;background:var(--gold);position:absolute;left:50%;top:8px;transform:translateX(-50%);z-index:2;box-shadow:0 0 16px var(--gold-glow);border:3px solid var(--bg)}
.tl-date{font-size:12px;color:var(--gold);font-weight:600;letter-spacing:1px;margin-bottom:2px}
.tl-price{font-family:'DM Serif Display',serif;font-size:26px;color:var(--gold-bright)}
.tl-note{font-size:13px;color:var(--t2);margin-top:4px}

/* ══ CHART ══ */
.chart-box{background:var(--card);border:1px solid rgba(255,255,255,.04);border-radius:var(--radius);padding:28px;position:relative}
.chart-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px}
.chart-title{font-size:16px;font-weight:700}
.chart-tabs{display:flex;gap:6px}
.tab-btn{padding:5px 14px;border-radius:16px;font-size:12px;border:1px solid rgba(255,255,255,.1);background:transparent;color:var(--t3);cursor:pointer;transition:all .3s;font-family:inherit}
.tab-btn.on{background:var(--gold);color:var(--bg);border-color:var(--gold);font-weight:600}
.tab-btn:hover:not(.on){border-color:var(--gold);color:var(--gold)}

/* ══ CENTRAL BANK ══ */
.bank-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.bank{background:var(--card);border:1px solid rgba(255,255,255,.04);border-radius:var(--radius);padding:20px;text-align:center;transition:all .35s}
.bank:hover{border-color:rgba(212,168,67,.25);transform:translateY(-2px)}
.bank-flag{font-size:36px;margin-bottom:10px}
.bank-name{font-size:13px;font-weight:600;margin-bottom:4px}
.bank-val{font-family:'DM Serif Display',serif;font-size:20px;color:var(--gold-bright)}
.bank-delta{font-size:11px;color:var(--green);margin-top:3px}
.bank-bar{height:3px;background:rgba(255,255,255,.05);border-radius:2px;margin-top:10px;overflow:hidden}
.bank-bar-fill{height:100%;background:linear-gradient(90deg,var(--gold),var(--gold-bright));border-radius:2px;transition:width 1.8s cubic-bezier(.25,.46,.45,.94)}

/* ══ RATE BARS ══ */
.rate-rows{max-width:700px;margin:0 auto}
.rate-row{display:flex;align-items:center;gap:14px;margin-bottom:18px}
.rate-flag{font-size:26px;width:36px;text-align:center;flex-shrink:0}
.rate-info{flex:1}
.rate-top{display:flex;justify-content:space-between;font-size:13px;margin-bottom:3px}
.rate-top span:last-child{color:var(--gold-bright);font-family:'DM Serif Display',serif;font-weight:700}
.rate-bg{height:7px;background:rgba(255,255,255,.05);border-radius:4px;overflow:hidden}
.rate-fill{height:100%;border-radius:4px;transition:width 2s cubic-bezier(.25,.46,.45,.94)}

/* ══ A/B COMPARE ══ */
.ab{display:grid;grid-template-columns:1fr 1fr;gap:2px;border-radius:var(--radius);overflow:hidden;margin:40px 0}
.ab-side{background:var(--card);padding:32px}
.ab-side:hover{background:var(--card2)}
.ab-hawk{border-right:1px solid rgba(255,255,255,.03)}
.ab-lbl{font-size:10px;letter-spacing:3px;text-transform:uppercase;font-weight:700;margin-bottom:14px}
.ab-lbl.h{color:var(--red)}
.ab-lbl.d{color:var(--green)}
.ab-row{display:flex;justify-content:space-between;padding:11px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:13px}
.ab-row:last-child{border-bottom:none}
.ab-row .lbl{color:var(--t2)}
.ab-row .val{font-weight:700}
.ab-row .val.up{color:var(--green)}
.ab-row .val.dn{color:var(--red)}

/* ══ FLOW ══ */
.flow-wrap{position:relative;min-height:480px;margin:40px 0}
.flow-node{position:absolute;background:var(--card);border:1px solid rgba(212,168,67,.15);border-radius:var(--radius);padding:16px 20px;text-align:center;transition:all .35s;cursor:pointer;z-index:2}
.flow-node:hover{border-color:var(--gold);box-shadow:0 0 24px var(--gold-glow);transform:scale(1.06)}
.flow-node-t{font-size:13px;font-weight:600;margin-bottom:3px}
.flow-node-v{font-family:'DM Serif Display',serif;font-size:18px;color:var(--gold-bright)}
.flow-svg{position:absolute;inset:0;z-index:1;pointer-events:none}

/* ══ INSIGHT ══ */
.insight{background:linear-gradient(135deg,rgba(212,168,67,.06),rgba(0,230,118,.04));border:1px solid rgba(212,168,67,.12);border-radius:var(--radius);padding:40px 48px;margin:40px 0;position:relative;overflow:hidden}
.insight::before{content:'';position:absolute;top:-40%;right:-15%;width:260px;height:260px;background:radial-gradient(circle,rgba(212,168,67,.08),transparent 70%);border-radius:50%}
.insight-q{font-size:clamp(18px,2.5vw,28px);font-weight:700;line-height:1.4;position:relative;z-index:1}
.insight-src{font-size:12px;color:var(--t3);margin-top:12px;position:relative;z-index:1}

/* ══ FOOTER ══ */
.footer{padding:48px 24px;text-align:center;border-top:1px solid rgba(255,255,255,.03)}
.footer p{font-size:12px;color:var(--t3);line-height:1.8}

/* ══ REVEAL ══ */
.rv{opacity:0;transform:translateY(36px);transition:opacity .8s cubic-bezier(.16,1,.3,1),transform .8s cubic-bezier(.16,1,.3,1)}
.rv.vis{opacity:1;transform:translateY(0)}
.rv-d1{transition-delay:.1s}.rv-d2{transition-delay:.2s}.rv-d3{transition-delay:.3s}.rv-d4{transition-delay:.4s}

/* ══ RESPONSIVE ══ */
@media(max-width:768px){
  .nav{padding:0 16px}.nav-links{display:none}
  .sec{padding:72px 16px}
  .tl::before{left:16px}
  .tl-row,.tl-row:nth-child(odd){flex-direction:column}
  .tl-row:nth-child(odd) .tl-body,.tl-body{padding-left:40px;padding-right:0;text-align:left}
  .tl-dot{left:16px}
  .ab{grid-template-columns:1fr}
  .ab-hawk{border-right:none;border-bottom:1px solid rgba(255,255,255,.03)}
  .bank-grid{grid-template-columns:repeat(2,1fr)}
  .hero-kpi{gap:24px}
}

/* ══ LOADING ══ */
.loader{position:fixed;inset:0;background:var(--bg);z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;transition:opacity .7s,visibility .7s}
.loader.out{opacity:0;visibility:hidden}
.loader-bar{width:180px;height:2px;background:rgba(255,255,255,.08);border-radius:1px;margin-top:16px;overflow:hidden}
.loader-fill{height:100%;background:var(--gold);width:0;transition:width .3s}
.loader-t{font-size:11px;color:var(--t3);letter-spacing:3px;margin-top:10px}
</style>
</head>
<body>

<!-- LOADER -->
<div class="loader" id="loader">
  <div style="font-family:'DM Serif Display',serif;font-size:28px;font-weight:700">
    <span style="color:var(--gold)">CAPITAL</span>&nbsp;<span style="color:var(--t3)">MIGRATION</span>
  </div>
  <div class="loader-bar"><div class="loader-fill" id="loaderFill"></div></div>
  <div class="loader-t">LOADING DATA FEEDS...</div>
</div>

<!-- NAV -->
<nav class="nav">
  <div class="nav-brand">⚡ CAPITAL MIGRATION</div>
  <div class="nav-links">
    <a href="#hero" class="active">总览</a>
    <a href="#sec-gold">黄金</a>
    <a href="#sec-dollar">美元</a>
    <a href="#sec-bank">央行</a>
    <a href="#sec-rate">利率</a>
    <a href="#sec-flow">流向</a>
    <a href="#sec-end">结论</a>
  </div>
</nav>

<!-- ══════════ HERO ══════════ -->
<section class="hero" id="hero">
  <div class="hero-tag">2026年8月 · 全球资本市场实时追踪</div>
  <h1>当<span class="g">$4,432</span>的黄金<br>遇上<span class="r">&lt;100</span>的美元</h1>
  <p class="hero-sub">全球资本正在经历一场史无前例的大迁徙。这不仅是市场波动，更是全球货币体系重构的信号。</p>
  <div class="hero-kpi">
    <div class="kpi"><div class="kpi-val up" data-count="4432" data-prefix="$" data-suffix="">$0</div><div class="kpi-lbl">COMEX黄金峰值</div></div>
    <div class="kpi"><div class="kpi-val dn" data-count="99.54" data-prefix="" data-suffix="" data-decimal="2">0</div><div class="kpi-lbl">美元指数 DXY</div></div>
    <div class="kpi"><div class="kpi-val" style="color:var(--gold)" data-count="289" data-prefix="" data-suffix="吨">0</div><div class="kpi-lbl">Q2央行净购金</div></div>
    <div class="kpi"><div class="kpi-val bl" data-count="7608" data-prefix="" data-suffix="万盎司">0</div><div class="kpi-lbl">中国黄金储备</div></div>
  </div>
</section>

<!-- ══════════ SECTION 1: GOLD TIMELINE ══════════ -->
<section class="sec" id="sec-gold" style="background:var(--bg)">
  <div class="sec-inner">
    <div class="sec-label rv">第一章 · 黄金觉醒</div>
    <h2 class="sec-title rv">从$2,000到$4,432<br>一场史诗级的黄金牛市</h2>
    <p class="sec-desc rv">2024年初至今，黄金价格翻倍有余。每一次突破都伴随着地缘冲突、央行购金和美元信用的动摇。</p>

    <div class="tl" id="goldTimeline">
      <div class="tl-row rv"><div class="tl-dot"></div><div class="tl-body"><div class="tl-date">2024年1月</div><div class="tl-price">$2,050</div><div class="tl-note">金价在$2,000上方蓄势，央行购金潮初现</div></div></div>
      <div class="tl-row rv"><div class="tl-dot"></div><div class="tl-body"><div class="tl-date">2024年4月</div><div class="tl-price">$2,400</div><div class="tl-note">中东局势升级，避险需求激增，首次站上$2,400</div></div></div>
      <div class="tl-row rv"><div class="tl-dot"></div><div class="tl-body"><div class="tl-date">2024年9月</div><div class="tl-price">$2,650</div><div class="tl-note">美联储开启降息周期，实际利率下行推动金价</div></div></div>
      <div class="tl-row rv"><div class="tl-dot"></div><div class="tl-body"><div class="tl-date">2025年3月</div><div class="tl-price">$3,100</div><div class="tl-note">贸易战升温，全球央行加速去美元化，黄金突破$3,000</div></div></div>
      <div class="tl-row rv"><div class="tl-dot"></div><div class="tl-body"><div class="tl-date">2025年12月</div><div class="tl-price">$3,500</div><div class="tl-note">美联储年内第三次降息至3.5%-3.75%，金价持续走高</div></div></div>
      <div class="tl-row rv"><div class="tl-dot"></div><div class="tl-body"><div class="tl-date">2026年6月</div><div class="tl-price">$4,050</div><div class="tl-note">黄金ETF管理规模达$2,330亿，机构资金蜂拥入场</div></div></div>
      <div class="tl-row rv"><div class="tl-dot"></div><div class="tl-body"><div class="tl-date">2026年8月7日</div><div class="tl-price">$4,432</div><div class="tl-note">COMEX黄金盘中突破$4,400，非农爆冷触发单周暴涨7%</div></div></div>
    </div>

    <!-- Gold Price Chart -->
    <div class="chart-box rv" style="margin-top:48px">
      <div class="chart-head">
        <div class="chart-title">黄金价格走势 (2024-2026)</div>
        <div class="chart-tabs">
          <button class="tab-btn on" data-range="all">全部</button>
          <button class="tab-btn" data-range="2026">2026</button>
          <button class="tab-btn" data-range="2025">2025</button>
        </div>
      </div>
      <canvas id="goldChart" height="300"></canvas>
    </div>

    <div class="card-grid rv" style="margin-top:32px">
      <div class="card">
        <div class="card-icon">📈</div>
        <div class="card-title">年初至今涨幅</div>
        <div class="card-val">+58%</div>
        <div class="card-chg pos">↑ 从$2,800到$4,432</div>
      </div>
      <div class="card">
        <div class="card-icon">🔥</div>
        <div class="card-title">8月7日单日涨幅</div>
        <div class="card-val">+3.09%</div>
        <div class="card-chg pos">↑ 盘中触及$4,432</div>
      </div>
      <div class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">周涨幅</div>
        <div class="card-val">+7.2%</div>
        <div class="card-chg pos">↑ 六个月最大单周涨幅</div>
      </div>
      <div class="card">
        <div class="card-icon">💰</div>
        <div class="card-title">国内金价</div>
        <div class="card-val">¥940/g</div>
        <div class="card-chg pos">↑ 周大福首饰价¥1,310/g</div>
      </div>
    </div>
  </div>
</section>

<!-- ══════════ SECTION 2: DXY COLLAPSE ══════════ -->
<section class="sec" id="sec-dollar" style="background:var(--bg2)">
  <div class="sec-inner">
    <div class="sec-label rv">第二章 · 美元陷落</div>
    <h2 class="sec-title rv">DXY跌破100<br>一个时代的分水岭</h2>
    <p class="sec-desc rv">美元指数从2022年的114高点跌至99.5，三年间蒸发近15%。100关口的失守，标志着全球对美元信心的结构性转折。</p>

    <div class="chart-box rv">
      <div class="chart-head">
        <div class="chart-title">美元指数 DXY 走势</div>
        <div class="chart-tabs">
          <button class="tab-btn on" data-dxy="all">2024-2026</button>
          <button class="tab-btn" data-dxy="2026">2026</button>
        </div>
      </div>
      <canvas id="dxyChart" height="280"></canvas>
    </div>

    <div class="card-grid rv" style="margin-top:32px">
      <div class="card">
        <div class="card-icon">💵</div>
        <div class="card-title">8月7日收盘</div>
        <div class="card-val" style="color:var(--red)">99.54</div>
        <div class="card-chg neg">↓ 日内跌0.39%</div>
      </div>
      <div class="card">
        <div class="card-icon">📉</div>
        <div class="card-title">7月30日首次破百</div>
        <div class="card-val" style="color:var(--red)">99.97</div>
        <div class="card-chg neg">↓ 跌0.85%失守100关口</div>
      </div>
      <div class="card">
        <div class="card-icon">🏛️</div>
        <div class="card-title">较2022年高点</div>
        <div class="card-val" style="color:var(--red)">-13%</div>
        <div class="card-chg neg">↓ 从114跌至99.5</div>
      </div>
      <div class="card">
        <div class="card-icon">⚠️</div>
        <div class="card-title">美元储备占比</div>
        <div class="card-val" style="color:var(--red)">22%</div>
        <div class="card-chg neg">↓ 已被黄金(27%)超越</div>
      </div>
    </div>

    <div class="insight rv">
      <div class="insight-q">"黄金在全球官方储备资产中的占比升至27%，超越美国国债的22%，成为全球官方储备第一大资产。"</div>
      <div class="insight-src">— 欧洲中央银行 2026年6月报告</div>
    </div>
  </div>
</section>

<!-- ══════════ SECTION 3: CENTRAL BANK ══════════ -->
<section class="sec" id="sec-bank" style="background:var(--bg)">
  <div class="sec-inner">
    <div class="sec-label rv">第三章 · 央行购金潮</div>
    <h2 class="sec-title rv">全球央行疯狂买金<br>连续21个月增持</h2>
    <p class="sec-desc rv">Q2全球央行净购金289吨，同比增长62%。89%的央行储备管理者预计未来12个月将继续增持黄金。</p>

    <div class="bank-grid rv" id="bankGrid">
      <div class="bank" data-pct="100">
        <div class="bank-flag">🇨🇳</div>
        <div class="bank-name">中国</div>
        <div class="bank-val">7,608万盎司</div>
        <div class="bank-delta">↑ 连续21个月增持</div>
        <div class="bank-bar"><div class="bank-bar-fill" style="width:0" data-w="100%"></div></div>
      </div>
      <div class="bank" data-pct="72">
        <div class="bank-flag">🇺🇸</div>
        <div class="bank-name">美国</div>
        <div class="bank-val">8,133吨</div>
        <div class="bank-delta">全球最大储备国</div>
        <div class="bank-bar"><div class="bank-bar-fill" style="width:0" data-w="72%"></div></div>
      </div>
      <div class="bank" data-pct="58">
        <div class="bank-flag">🇩🇪</div>
        <div class="bank-name">德国</div>
        <div class="bank-val">3,352吨</div>
        <div class="bank-delta">欧洲最大黄金储备</div>
        <div class="bank-bar"><div class="bank-bar-fill" style="width:0" data-w="58%"></div></div>
      </div>
      <div class="bank" data-pct="45">
        <div class="bank-flag">🇮🇹</div>
        <div class="bank-name">意大利</div>
        <div class="bank-val">2,452吨</div>
        <div class="bank-delta">占储备65%+</div>
        <div class="bank-bar"><div class="bank-bar-fill" style="width:0" data-w="45%"></div></div>
      </div>
      <div class="bank" data-pct="38">
        <div class="bank-flag">🇷🇺</div>
        <div class="bank-name">俄罗斯</div>
        <div class="bank-val">2,332吨</div>
        <div class="bank-delta">去美元化先锋</div>
        <div class="bank-bar"><div class="bank-bar-fill" style="width:0" data-w="38%"></div></div>
      </div>
      <div class="bank" data-pct="30">
        <div class="bank-flag">🇮🇳</div>
        <div class="bank-name">印度</div>
        <div class="bank-val">$1,152亿</div>
        <div class="bank-delta">↑ 持续增持中</div>
        <div class="bank-bar"><div class="bank-bar-fill" style="width:0" data-w="30%"></div></div>
      </div>
    </div>

    <div class="chart-box rv" style="margin-top:32px">
      <div class="chart-head">
        <div class="chart-title">中国央行黄金储备月度变化 (万盎司)</div>
      </div>
      <canvas id="cbChart" height="260"></canvas>
    </div>

    <div class="insight rv">
      <div class="insight-q">"89%的央行储备管理者预计，未来12个月内全球央行黄金储备将继续增加。"</div>
      <div class="insight-src">— 世界黄金协会 2026年调研</div>
    </div>
  </div>
</section>

<!-- ══════════ SECTION 4: RATE DIVERGENCE ══════════ -->
<section class="sec" id="sec-rate" style="background:var(--bg2)">
  <div class="sec-inner">
    <div class="sec-label rv">第四章 · 利率大分化</div>
    <h2 class="sec-title rv">全球央行利率分歧<br>降息潮中的逆行者</h2>
    <p class="sec-desc rv">美联储降息至3.75%，欧洲央行降至2.40%，而日本央行加息至1.0%。利率分歧正在重塑全球资本流向。</p>

    <div class="rate-rows rv" id="rateBars">
      <div class="rate-row">
        <div class="rate-flag">🇺🇸</div>
        <div class="rate-info">
          <div class="rate-top"><span>美联储 Fed</span><span>3.75%</span></div>
          <div class="rate-bg"><div class="rate-fill" style="width:0;background:linear-gradient(90deg,#FF4757,#FF6B81)" data-w="75%"></div></div>
        </div>
      </div>
      <div class="rate-row">
        <div class="rate-flag">🇬🇧</div>
        <div class="rate-info">
          <div class="rate-top"><span>英国央行 BOE</span><span>3.75%</span></div>
          <div class="rate-bg"><div class="rate-fill" style="width:0;background:linear-gradient(90deg,#FF4757,#FF6B81)" data-w="75%"></div></div>
        </div>
      </div>
      <div class="rate-row">
        <div class="rate-flag">🇦🇺</div>
        <div class="rate-info">
          <div class="rate-top"><span>澳洲联储 RBA</span><span>3.85%</span></div>
          <div class="rate-bg"><div class="rate-fill" style="width:0;background:linear-gradient(90deg,#FF6B81,#FFA502)" data-w="77%"></div></div>
        </div>
      </div>
      <div class="rate-row">
        <div class="rate-flag">🇨🇳</div>
        <div class="rate-info">
          <div class="rate-top"><span>中国央行 PBOC</span><span>1.50%</span></div>
          <div class="rate-bg">