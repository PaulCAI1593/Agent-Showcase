#!/usr/bin/env python3
"""Generate the Safe Haven Asset Dual Rise interactive HTML experience."""

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
:root{
  --bg:#0a0a0a;--bg2:#111;--bg3:#1a1a1a;
  --txt:#fff;--txt2:#999;--txt3:#555;
  --gold:#D4AF37;--gold2:#F0D060;
  --btc:#F7931A;--btc2:#FFB84D;
  --blue:#0071e3;--border:#222;
}
html{scroll-behavior:smooth;background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue","PingFang SC","Noto Sans CJK SC",sans-serif}
body{overflow-x:hidden}
::selection{background:var(--gold);color:#000}

/* NAV DOTS */
.nav-dots{position:fixed;right:24px;top:50%;transform:translateY(-50%);z-index:1000;display:flex;flex-direction:column;gap:14px}
.nav-dots a{width:10px;height:10px;border-radius:50%;background:var(--txt3);display:block;transition:all .3s;text-decoration:none}
.nav-dots a.active{background:var(--gold);box-shadow:0 0 12px var(--gold);transform:scale(1.4)}

/* SECTIONS */
section{min-height:100vh;position:relative;display:flex;align-items:center;justify-content:center;padding:80px 40px}
.container{max-width:1100px;width:100%;margin:0 auto}
.section-label{font-size:12px;letter-spacing:3px;text-transform:uppercase;color:var(--txt3);margin-bottom:12px}
h2{font-size:clamp(28px,4vw,48px);font-weight:600;line-height:1.15;letter-spacing:-0.5px;margin-bottom:20px}
h3{font-size:24px;font-weight:600;margin-bottom:12px}

/* HERO */
#hero{min-height:100vh;background:radial-gradient(ellipse at 50% 30%,#1a1500 0%,var(--bg) 70%);flex-direction:column;text-align:center;overflow:hidden}
#hero .subtitle{font-size:18px;color:var(--txt2);margin-top:20px;max-width:700px;line-height:1.6}
.hero-date{font-size:14px;color:var(--gold);letter-spacing:4px;margin-top:32px}
.scroll-hint{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--txt3);font-size:12px;animation:bounce 2s infinite}
@keyframes bounce{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(8px)}}
.scroll-hint .arrow{width:20px;height:20px;border-right:2px solid var(--txt3);border-bottom:2px solid var(--txt3);transform:rotate(45deg)}
#hero canvas{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none}

/* SECTION 2: NUMBERS */
#numbers{background:var(--bg);padding:120px 40px}
.numbers-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;margin-top:40px}
.asset-card{background:var(--bg3);border-radius:16px;padding:40px;position:relative;overflow:hidden;border:1px solid var(--border)}
.asset-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.asset-card.gold-card::before{background:linear-gradient(90deg,var(--gold),var(--gold2))}
.asset-card.btc-card::before{background:linear-gradient(90deg,var(--btc),var(--btc2))}
.asset-icon{font-size:36px;margin-bottom:16px}
.asset-name{font-size:14px;letter-spacing:3px;text-transform:uppercase;margin-bottom:20px}
.asset-card.gold-card .asset-name{color:var(--gold)}
.asset-card.btc-card .asset-name{color:var(--btc)}
.price-journey{display:flex;flex-direction:column;gap:16px;margin:24px 0}
.price-point{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:rgba(255,255,255,.03);border-radius:8px}
.price-point .label{font-size:13px;color:var(--txt2)}
.price-point .value{font-size:18px;font-weight:600;font-variant-numeric:tabular-nums}
.price-point .value.up{color:#22c55e}
.price-point .value.down{color:#ef4444}
.mini-chart{height:60px;margin:20px 0;position:relative}
.mini-chart svg{width:100%;height:100%}

/* SECTION 3: TOGGLE */
#compare{background:var(--bg2);flex-direction:column;padding:100px 40px}
.toggle-bar{display:flex;background:var(--bg);border-radius:40px;padding:4px;margin:30px 0;width:fit-content;border:1px solid var(--border)}
.toggle-btn{padding:12px 36px;border-radius:36px;border:none;font-size:14px;font-weight:600;cursor:pointer;transition:all .4s;background:transparent;color:var(--txt2);letter-spacing:1px}
.toggle-btn.active-gold{background:var(--gold);color:#000}
.toggle-btn.active-btc{background:var(--btc);color:#000}
.compare-panel{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:30px;width:100%}
.compare-col{text-align:center}
.compare-col .big-num{font-size:clamp(36px,5vw,56px);font-weight:700;line-height:1;margin:16px 0}
.compare-col .metric{font-size:14px;color:var(--txt2);margin-top:8px}
.volatility-gauge{width:160px;height:90px;margin:20px auto}
.corr-ring{width:120px;height:120px;margin:20px auto;position:relative}
.corr-ring svg{width:100%;height:100%;transform:rotate(-90deg)}
.corr-ring .center-text{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center}
.corr-ring .center-text .num{font-size:24px;font-weight:700}
.corr-ring .center-text .lbl{font-size:10px;color:var(--txt3)}

/* SECTION 4: TIMELINE */
#timeline{background:var(--bg);flex-direction:column;padding:100px 40px;min-height:auto}
.timeline{position:relative;margin-top:40px;padding-left:40px}
.timeline::before{content:'';position:absolute;left:15px;top:0;bottom:0;width:2px;background:linear-gradient(to bottom,var(--gold),var(--btc))}
.tl-item{position:relative;margin-bottom:32px;cursor:pointer}
.tl-dot{position:absolute;left:-33px;top:8px;width:18px;height:18px;border-radius:50%;border:3px solid var(--gold);background:var(--bg);transition:all .3s;z-index:2}
.tl-item:nth-child(n+4) .tl-dot{border-color:var(--btc)}
.tl-item:hover .tl-dot{transform:scale(1.3);box-shadow:0 0 20px var(--gold)}
.tl-item:nth-child(n+4):hover .tl-dot{box-shadow:0 0 20px var(--btc)}
.tl-date{font-size:13px;color:var(--gold);letter-spacing:1px;font-weight:600}
.tl-item:nth-child(n+4) .tl-date{color:var(--btc)}
.tl-title{font-size:18px;font-weight:600;margin:6px 0;transition:color .3s}
.tl-item:hover .tl-title{color:var(--gold2)}
.tl-item:nth-child(n+4):hover .tl-title{color:var(--btc2)}
.tl-detail{max-height:0;overflow:hidden;transition:max-height .5s ease,padding .5s;padding:0 16px;background:var(--bg3);border-radius:12px;margin-top:8px;border:1px solid transparent}
.tl-item.open .tl-detail{max-height:300px;padding:16px;border-color:var(--border)}
.tl-detail p{font-size:14px;color:var(--txt2);line-height:1.7}
.tl-detail .tag{display:inline-block;padding:3px 10px;border-radius:12px;font-size:11px;margin-right:6px;margin-top:8px}
.tag-gold{background:rgba(212,175,55,.15);color:var(--gold)}
.tag-btc{background:rgba(247,147,26,.15);color:var(--btc)}
.tag-red{background:rgba(239,68,68,.15);color:#ef4444}
.tag-green{background:rgba(34,197,94,.15);color:#22c55e}

/* SECTION 5: THREE LENSES */
#lenses{background:var(--bg2);flex-direction:column;padding:100px 40px}
.lenses-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:40px}
.lens-card{perspective:800px;height:280px;cursor:pointer}
.lens-inner{position:relative;width:100%;height:100%;transition:transform .7s cubic-bezier(.4,0,.2,1);transform-style:preserve-3d}
.lens-card.flipped .lens-inner{transform:rotateY(180deg)}
.lens-front,.lens-back{position:absolute;top:0;left:0;width:100%;height:100%;backface-visibility:hidden;border-radius:16px;padding:32px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.lens-front{background:var(--bg3);border:1px solid var(--border)}
.lens-back{background:linear-gradient(135deg,#1a1a1a,#111);border:1px solid var(--border);transform:rotateY(180deg);padding:24px}
.lens-icon{font-size:48px;margin-bottom:16px}
.lens-title{font-size:20px;font-weight:600;margin-bottom:8px}
.lens-front .hint{font-size:12px;color:var(--txt3);margin-top:auto}
.lens-back p{font-size:14px;color:var(--txt2);line-height:1.7}
.lens-back .back-title{font-size:16px;font-weight:600;color:var(--gold);margin-bottom:10px}

/* SECTION 6: THE DEBATE */
#debate{background:var(--bg);padding:100px 40px}
.debate-split{display:grid;grid-template-columns:1fr 80px 1fr;gap:0;margin-top:40px;align-items:start}
.debate-side{padding:32px;border-radius:16px}
.debate-side.left{background:linear-gradient(135deg,rgba(212,175,55,.08),rgba(212,175,55,.02));border:1px solid rgba(212,175,55,.2)}
.debate-side.right{background:linear-gradient(135deg,rgba(247,147,26,.08),rgba(247,147,26,.02));border:1px solid rgba(247,147,26,.2)}
.debate-vs{display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;color:var(--txt3);padding-top:40px}
.debate-side h3{margin-bottom:20px}
.debate-side.left h3{color:var(--gold)}
.debate-side.right h3{color:var(--btc)}
.debate-item{padding:12px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between;align-items:center}
.debate-item:last-child{border:none}
.debate-item .dlabel{font-size:13px;color:var(--txt2)}
.debate-item .dbar{height:6px;border-radius:3px;background:var(--bg);flex:1;margin:0 16px;position:relative;overflow:hidden}
.debate-item .dbar-fill{height:100%;border-radius:3px;transition:width 1.5s ease;width:0}
.left .dbar-fill{background:linear-gradient(90deg,var(--gold),var(--gold2))}
.right .dbar-fill{background:linear-gradient(90deg,var(--btc),var(--btc2))}
.debate-item .dval{font-size:14px;font-weight:600;width:50px;text-align:right}

/* SECTION 7: DASHBOARD */
#dashboard{background:var(--bg2);flex-direction:column;padding:100px 40px}
.dash-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:40px}
.dash-card{background:var(--bg3);border-radius:16px;padding:28px;border:1px solid var(--border)}
.dash-card h4{font-size:14px;color:var(--txt2);margin-bottom:16px;letter-spacing:1px}
.dash-card .big-stat{font-size:clamp(28px,4vw,42px);font-weight:700;margin-bottom:4px}
.dash-card .stat-label{font-size:12px;color:var(--txt3)}
.dash-chart{height:120px;margin-top:16px;position:relative}
.dash-chart svg{width:100%;height:100%}
.bar-chart{display:flex;align-items:flex-end;gap:6px;height:100%;padding-top:10px}
.bar{border-radius:4px 4px 0 0;min-width:20px;flex:1;transition:height 1.5s ease;position:relative}
.bar.gold-bar{background:linear-gradient(to top,var(--gold),var(--gold2))}
.bar.btc-bar{background:linear-gradient(to top,var(--btc),var(--btc2))}
.bar-label{position:absolute;bottom:-20px;left:50%;transform:translateX(-50%);font-size:9px;color:var(--txt3);white-space:nowrap}

/* SECTION 8: CLOSING */
#closing{background:radial-gradient(ellipse at 50% 50%,#1a1500 0%,var(--bg) 70%);flex-direction:column;text-align:center;padding:100px 40px}
.closing-quote{font-size:clamp(20px,3vw,32px);font-weight:500;line-height:1.5;max-width:800px;margin:0 auto 40px;color:var(--gold2)}
.closing-sub{font-size:16px;color:var(--txt2);font-style:italic;max-width:600px;margin:0 auto 48px;line-height:1.7}
.insight-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:20px;max-width:900px}
.insight-card{background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:12px;padding:24px;text-align:left}
.insight-card .ic-icon{font-size:24px;margin-bottom:10px}
.insight-card .ic-title{font-size:15px;font-weight:600;margin-bottom:6px}
.insight-card .ic-text{font-size:13px;color:var(--txt2);line-height:1.6}
.footer-note{margin-top:60px;font-size:11px;color:var(--txt3);line-height:1.6}

/* RESPONSIVE */
@media(max-width:768px){
  .numbers-grid,.compare-panel,.lenses-grid,.debate-split,.dash-grid,.insight-cards{grid-template-columns:1fr}
  section{padding:60px 20px}
  .debate-vs{padding:16px 0}
  .nav-dots{right:12px}
}
</style>
</head>
<body>

<!-- NAV DOTS -->
<nav class="nav-dots" id="navDots"></nav>

<!-- SECTION 1: HERO -->
<section id="hero" data-section="0">
  <canvas id="particleCanvas"></canvas>
  <div class="container" style="position:relative;z-index:2">
    <div class="hero-date">2026 · 全球避险资产报告</div>
    <h1 style="font-size:clamp(32px,5.5vw,64px);font-weight:700;margin-top:24px;line-height:1.1;letter-spacing:-1px">
      当黄金和比特币<br><span style="background:linear-gradient(90deg,var(--gold),var(--btc));-webkit-background-clip:text;-webkit-text-fill-color:transparent">同时飙升</span>
    </h1>
    <p class="subtitle">传统避险之王与数字黄金的历史性同框。这不仅是一场价格的狂欢，更是全球经济信心的晴雨表。</p>
  </div>
  <div class="scroll-hint"><span>向下探索</span><div class="arrow"></div></div>
</section>

<!-- SECTION 2: THE NUMBERS -->
<section id="numbers" data-section="1">
  <div class="container">
    <div class="section-label">01 · 价格全景</div>
    <h2>两种避险资产的<span style="color:var(--gold)">过山车</span>之旅</h2>
    <div class="numbers-grid">
      <!-- Gold Card -->
      <div class="asset-card gold-card reveal">
        <div class="asset-icon">🥇</div>
        <div class="asset-name">黄金 GOLD · XAU/USD</div>
        <div class="price-journey">
          <div class="price-point"><span class="label">📍 1月29日 · 历史新高</span><span class="value up" data-count="5626">$5,626</span></div>
          <div class="price-point"><span class="label">📉 6月30日 · 年内低点</span><span class="value down" data-count="3942">$3,942</span></div>
          <div class="price-point"><span class="label">📈 8月 · 反弹回升</span><span class="value up" data-count="4860">$4,860</span></div>
        </div>
        <div class="mini-chart" id="goldChart"></div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:12px">
          <span style="background:rgba(212,175,55,.12);color:var(--gold);padding:6px 12px;border-radius:20px;font-size:12px">央行Q1购入244吨 $370亿创纪录</span>
          <span style="background:rgba(34,197,94,.12);color:#22c55e;padding:6px 12px;border-radius:20px;font-size:12px">ETF规模 $6,690亿</span>
        </div>
      </div>
      <!-- BTC Card -->
      <div class="asset-card btc-card reveal">
        <div class="asset-icon">₿</div>
        <div class="asset-name">比特币 BITCOIN · BTC/USD</div>
        <div class="price-journey">
          <div class="price-point"><span class="label">📍 2025年10月 · ATH</span><span class="value up">$126,000</span></div>
          <div class="price-point"><span class="label">📉 2026年中 · 低点</span><span class="value down">$62,500</span></div>
          <div class="price-point"><span class="label">🚀 8月21日 · 3天暴涨24%</span><span class="value up">$79,455</span></div>
        </div>
        <div class="mini-chart" id="btcChart"></div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:12px">
          <span style="background:rgba(247,147,26,.12);color:var(--btc);padding:6px 12px;border-radius:20px;font-size:12px">空单爆仓 $31亿 · 17万人</span>
          <span style="background:rgba(139,92,246,.12);color:#8b5cf6;padding:6px 12px;border-radius:20px;font-size:12px">ETF累计流入 $530亿+</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- SECTION 3: TOGGLE COMPARE -->
<section id="compare" data-section="2">
  <div class="container" style="text-align:center">
    <div class="section-label">02 · 对比切换</div>
    <h2>一触切换：<span style="color:var(--gold)">黄金</span> vs <span style="color:var(--btc)">比特币</span></h2>
    <div class="toggle-bar">
      <button class="toggle-btn active-gold" id="togGold" onclick="switchAsset('gold')">🥇 黄金 GOLD</button>
      <button class="toggle-btn" id="togBtc" onclick="switchAsset('btc')">₿ 比特币 BTC</button>
    </div>
    <div class="compare-panel" id="comparePanel">
      <div class="compare-col">
        <div class="section-label">当前价格</div>
        <div class="big-num" id="cpPrice" style="color:var(--gold)">$4,860</div>
        <div class="metric" id="cpUnit">美元/盎司</div>
      </div>
      <div class="compare-col">
        <div class="section-label">年初至今</div>
        <div class="big-num" id="cpYtd" style="color:var(--gold)">+12%</div>
        <div class="metric" id="cpYtdLabel">年化回报</div>
      </div>
      <div class="compare-col">
        <div class="section-label">30日波动率</div>
        <div class="volatility-gauge" id="volGauge"></div>
        <div class="metric" id="cpVol">18%</div>
      </div>
      <div class="compare-col">
        <div class="section-label">与另一资产相关性</div>
        <div class="corr-ring" id="corrRing"></div>
        <div class="metric" id="cpCorr">0.41</div>
      </div>
    </div>
  </div>
</section>

<!-- SECTION 4: TIMELINE -->
<section id="timeline" data-section="3" style="min-height:auto">
  <div class="container">
    <div class="section-label">03 · 关键事件时间线</div>
    <h2>避险双升的<span style="color:var(--btc)">七幕剧</span></h2>
    <p style="color:var(--txt2);font-size:14px;margin-bottom:12px">点击事件节点查看详情 ↓</p>
    <div class="timeline" id="timelineWrap">
      <div class="tl-item reveal" onclick="toggleTl(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年1月29日</div>
        <div class="tl-title">🥇 黄金创下历史最高 $5,626.80</div>
        <div class="tl-detail">
          <p>伊朗冲突前夕，避险情绪达到顶峰。全球黄金ETF单月涌入190亿美元，创历史新高。央行在Q1购入244吨黄金，花费370亿美元——这是有史以来单季度最高纪录。</p>
          <span class="tag tag-gold">避险潮</span><span class="tag tag-green">ETF流入$190亿</span>
        </div>
      </div>
      <div class="tl-item reveal" onclick="toggleTl(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年2月27日</div>
        <div class="tl-title">⚔️ 美伊战争爆发</div>
        <div class="tl-detail">
          <p>48小时内黄金飙升5.2%至~$4,700，而比特币暴跌12%至~$65,000。传统避险资产和数字资产给出完全相反的答案。迪拜黄金物流网络受战争冲击中断，伊朗最大加密交易所Nobitex资金流出暴增700%。</p>
          <span class="tag tag-gold">黄金+5.2%</span><span class="tag tag-btc">BTC-12%</span><span class="tag tag-red">地缘冲击</span>
        </div>
      </div>
      <div class="tl-item reveal" onclick="toggleTl(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年3-4月</div>
        <div class="tl-title">📊 BTC与标普500相关性飙至0.74</div>
        <div class="tl-detail">
          <p>比特币的"数字黄金"身份遭受最严峻考验。30日与S&P 500相关性高达0.74，与黄金相关性降至-0.17。Strategy公司逆势买入$12亿BTC，机构仍在押注长期价值。</p>
          <span class="tag tag-btc">相关性0.74</span><span class="tag tag-green">机构买入$12亿</span>
        </div>
      </div>
      <div class="tl-item reveal" onclick="toggleTl(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年6月30日</div>
        <div class="tl-title">📉 黄金跌至年内低点 $3,942</div>
        <div class="tl-detail">
          <p>从ATH暴跌22-24%，创2013年以来最差季度表现。战争推高油价→通胀预期上升→美联储鹰派→实际利率走高→无息资产承压。但$3,942恰好是2025年11月低点——技术支撑位形成结构底。央行继续买入，中国连续9个月增持。</p>
          <span class="tag tag-gold">-24%</span><span class="tag tag-red">加息恐惧</span><span class="tag tag-green">央行托底</span>
        </div>
      </div>
      <div class="tl-item reveal" onclick="toggleTl(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年8月19日</div>
        <div class="tl-title">🚀 美国财政部翻倍债券回购 → BTC暴涨24%</div>
        <div class="tl-detail">
          <p>财政部宣布将10-30年期国债回购规模从$20亿翻倍至$40亿。30年期收益率从19年高位5.34%骤降至5.19%。美元走弱→风险资产飙升。BTC一天涨8%，触发自2021年11月以来最大规模空头清算——$31亿在24小时内被抹去。</p>
          <span class="tag tag-btc">3天+24%</span><span class="tag tag-red">空单爆仓$31亿</span><span class="tag tag-green">流动性注入</span>
        </div>
      </div>
      <div class="tl-item reveal" onclick="toggleTl(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年8月20日</div>
        <div class="tl-title">🏛️ 白宫加密峰会 · 监管破冰</div>
        <div class="tl-detail">
          <p>特朗普会见加密行业高管，SEC主席与CFTC主席出席。SEC提出"Regulation Crypto Assets"新规，允许早期融资豁免证券注册。总统呼吁国会通过《Clarity Act》明确监管框架。BTC ETF单日流入$6.06亿——三个月最高。</p>
          <span class="tag tag-btc">ETF流入$6亿</span><span class="tag tag-green">监管利好</span>
        </div>
      </div>
      <div class="tl-item reveal" onclick="toggleTl(this)">
        <div class="tl-dot"></div>
        <div class="tl-date">2026年8月</div>
        <div class="tl-title">🔗 BTC/黄金90日相关性达0.41 · 历史最高</div>
        <div class="tl-detail">
          <p>两种避险资产的相关性达到有史以来最高持续水平。去美元化叙事将它们推向同一个方向：央行储备中黄金首次超过美国国债占比（1996年以来首次）。42%的机构投资者预测黄金将达$5,000-$6,000。"数字黄金"与"实体黄金"从对立走向共生。</p>
          <span class="tag tag-gold">黄金>美债</span><span class="tag tag-btc">相关性0.41</span><span class="tag tag-green">去美元化</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- SECTION 5: THREE LENSES -->
<section id="lenses" data-section="4">
  <div class="container" style="text-align:center">
    <div class="section-label">04 · 三重透镜</div>
    <h2>为什么避险资产<span style="color:var(--gold)">双升</span>？</h2>
    <p style="color:var(--txt2);font-size:14px">翻转卡片，点击查看详情 ↓</p>
    <div class="lenses-grid">
      <div class="lens-card reveal" onclick="this.classList.toggle('flipped')">
        <div class="lens-inner">
          <div class="lens-front">
            <div class="lens-icon">🏛️</div>
            <div class="lens-title">宏观经济</div>
            <p style="color:var(--txt2);font-size:14px">去美元化浪潮与主权债务危机</p>
            <div class="hint">点击翻转 →</div>
          </div>
          <div class="lens-back">
            <div class="back-title">🏛️ 宏观经济</div>
            <p>美国国债突破$38万亿，年度赤字持续扩大。2022年冻结俄罗斯$3,000亿储备的教训让全球南方觉醒——美元资产可以被武器化。中国、印度、土耳其、波兰连续三年每年购入超1,000吨黄金。黄金在央行储备中的占比自1996年以来首次超过美国国债。</p>
          </div>
        </div>
      </div>
      <div class="lens-card reveal" onclick="this.classList.toggle('flipped')">
        <div class="lens-inner">
          <div class="lens-front">
            <div class="lens-icon">🌍</div>
            <div class="lens-title">地缘政治</div>
            <p style="color:var(--txt2);font-size:14px">伊朗冲突与全球供应链中断</p>
            <div class="hint">点击翻转 →</div>
          </div>
          <div class="lens-back">
            <div class="back-title">🌍 地缘政治</div>
            <p>2026年2月美伊冲突直接打击能源供应，霍尔木兹海峡通行风险飙升。油价逼近$120/桶推高全球通胀。迪拜黄金物流网络中断，实物黄金跨境运输困难。而比特币——一个人记住12个助记词就能穿越国境带走全部财富。战争暴露了两种资产的互补优势。</p>
          </div>
        </div>
      </div>
      <div class="lens-card reveal" onclick="this.classList.toggle('flipped')">
        <div class="lens-inner">
          <div class="lens-front">
            <div class="lens-icon">💰</div>
            <div class="lens-title">货币政策</div>
            <p style="color:var(--txt2);font-size:14px">降息预期回归与流动性注入</p>
            <div class="hint">点击翻转 →</div>
          </div>
          <div class="lens-back">
            <div class="back-title">💰 货币政策</div>
            <p>8月美国CPI数据低于预期，通胀恐慌消退。市场重新定价降息路径，实际利率预期走低——这对无息资产黄金和比特币都是利好。财政部翻倍债券回购等于隐性注入流动性。美元指数跌至三个月低位。BTC三天暴涨24%，黄金反弹至$4,860。流动性回来了。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
