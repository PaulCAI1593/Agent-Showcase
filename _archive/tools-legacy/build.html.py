#!/usr/bin/env python3
"""Build AI Compute Explosion interactive HTML experience."""

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI算力消耗的指数级爆发：从1000亿到500万亿Token的3年迁徙</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --blue:#00d4ff;--green:#00ff88;--dark:#0a0a0f;--darker:#050508;
  --card:#111118;--card-border:rgba(0,212,255,0.15);
  --text:#e0e0e8;--text-dim:#8888aa;--text-bright:#ffffff;
}
@font-face{font-family:'Inter';src:local('Inter'),local('Helvetica Neue'),local('Arial');font-display:swap}
body{
  font-family:'Inter','SF Pro Display',-apple-system,BlinkMacSystemFont,sans-serif;
  background:var(--dark);color:var(--text);overflow-x:hidden;
  line-height:1.6;-webkit-font-smoothing:antialiased;
}
::selection{background:rgba(0,212,255,0.3);color:#fff}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--darker)}
::-webkit-scrollbar-thumb{background:rgba(0,212,255,0.3);border-radius:3px}

/* ============ HERO SECTION ============ */
.hero{
  min-height:100vh;display:flex;flex-direction:column;
  justify-content:center;align-items:center;
  position:relative;overflow:hidden;
  background:radial-gradient(ellipse at 50% 50%,#0d0d1a 0%,#050508 70%);
}
#particles-canvas{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0}
.hero-content{position:relative;z-index:1;text-align:center;max-width:1000px;padding:0 24px}
.hero-label{
  font-size:13px;letter-spacing:4px;text-transform:uppercase;
  color:var(--blue);margin-bottom:24px;opacity:0;
  animation:fadeUp .8s ease forwards .3s;
}
.hero h1{
  font-size:clamp(32px,6vw,72px);font-weight:700;
  line-height:1.05;letter-spacing:-2px;color:var(--text-bright);
  margin-bottom:24px;opacity:0;animation:fadeUp .8s ease forwards .6s;
}
.hero h1 .accent{color:var(--blue)}
.hero h1 .green-accent{color:var(--green)}
.hero-sub{
  font-size:clamp(16px,2vw,22px);color:var(--text-dim);
  max-width:700px;margin:0 auto 40px;opacity:0;
  animation:fadeUp .8s ease forwards .9s;
}
.hero-stats{
  display:flex;gap:48px;justify-content:center;flex-wrap:wrap;
  opacity:0;animation:fadeUp .8s ease forwards 1.2s;
}
.hero-stat{text-align:center}
.hero-stat .number{
  font-size:clamp(28px,4vw,48px);font-weight:700;
  font-variant-numeric:tabular-nums;
  background:linear-gradient(135deg,var(--blue),var(--green));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}
.hero-stat .label{font-size:13px;color:var(--text-dim);margin-top:4px;letter-spacing:1px}
.scroll-hint{
  position:absolute;bottom:40px;left:50%;transform:translateX(-50%);
  display:flex;flex-direction:column;align-items:center;gap:8px;
  opacity:0;animation:fadeUp .8s ease forwards 1.5s;
}
.scroll-hint span{font-size:12px;color:var(--text-dim);letter-spacing:2px;text-transform:uppercase}
.scroll-arrow{
  width:24px;height:24px;border-right:2px solid var(--blue);
  border-bottom:2px solid var(--blue);transform:rotate(45deg);
  animation:bounce 2s infinite;
}
@keyframes bounce{0%,20%,50%,80%,100%{transform:rotate(45deg) translateY(0)}40%{transform:rotate(45deg) translateY(8px)}60%{transform:rotate(45deg) translateY(4px)}}
@keyframes fadeUp{to{opacity:1;transform:translateY(0)}from{opacity:0;transform:translateY(20px)}}

/* ============ SECTIONS ============ */
.section{padding:100px 24px;position:relative}
.section-dark{background:var(--darker)}
.section-light{background:var(--dark)}
.section-header{text-align:center;max-width:800px;margin:0 auto 60px}
.section-label{
  font-size:12px;letter-spacing:4px;text-transform:uppercase;
  color:var(--blue);margin-bottom:16px;
}
.section-title{
  font-size:clamp(24px,4vw,44px);font-weight:700;
  letter-spacing:-1px;color:var(--text-bright);margin-bottom:16px;
}
.section-desc{font-size:17px;color:var(--text-dim);max-width:600px;margin:0 auto}
.container{max-width:1100px;margin:0 auto}

/* ============ TIMELINE ============ */
.timeline-wrap{position:relative;padding:40px 0}
.timeline-line{
  position:absolute;left:50%;top:0;bottom:0;width:2px;
  background:linear-gradient(to bottom,transparent,var(--blue),var(--green),transparent);
  transform:translateX(-50%);
}
.timeline-node{
  display:flex;align-items:flex-start;margin-bottom:80px;
  position:relative;cursor:pointer;
  transition:transform .3s ease;
}
.timeline-node:hover{transform:scale(1.02)}
.timeline-node:nth-child(even){flex-direction:row-reverse}
.timeline-dot{
  position:absolute;left:50%;top:20px;transform:translateX(-50%);
  width:20px;height:20px;border-radius:50%;
  background:var(--blue);border:3px solid var(--dark);
  z-index:2;transition:all .3s ease;
  box-shadow:0 0 20px rgba(0,212,255,0.4);
}
.timeline-node.active .timeline-dot{
  background:var(--green);box-shadow:0 0 30px rgba(0,255,136,0.5);
  transform:translateX(-50%) scale(1.3);
}
.timeline-card{
  width:calc(50% - 40px);background:var(--card);
  border-radius:16px;padding:32px;
  border:1px solid var(--card-border);
  transition:all .4s ease;
  opacity:0;transform:translateY(20px);
}
.timeline-card.visible{opacity:1;transform:translateY(0)}
.timeline-node:nth-child(odd) .timeline-card{margin-right:auto}
.timeline-node:nth-child(even) .timeline-card{margin-left:auto}
.timeline-node.active .timeline-card{
  border-color:rgba(0,255,136,0.3);
  box-shadow:0 8px 40px rgba(0,255,136,0.1);
}
.timeline-year{
  font-size:14px;font-weight:700;color:var(--blue);
  letter-spacing:2px;margin-bottom:8px;
}
.timeline-title{
  font-size:22px;font-weight:700;color:var(--text-bright);
  margin-bottom:12px;line-height:1.3;
}
.timeline-metric{
  display:flex;gap:16px;flex-wrap:wrap;margin-top:16px;
}
.metric-badge{
  background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.2);
  border-radius:8px;padding:8px 14px;
}
.metric-badge .val{font-size:18px;font-weight:700;color:var(--blue)}
.metric-badge .lbl{font-size:11px;color:var(--text-dim);margin-top:2px}
.detail-panel{
  max-height:0;overflow:hidden;transition:max-height .5s ease;
}
.timeline-node.active .detail-panel{max-height:500px}
.detail-content{
  padding-top:16px;border-top:1px solid rgba(255,255,255,0.06);
  margin-top:16px;font-size:14px;color:var(--text-dim);line-height:1.7;
}

/* ============ CHART SECTION ============ */
.chart-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.chart-card{
  background:var(--card);border:1px solid var(--card-border);
  border-radius:16px;padding:32px;position:relative;overflow:hidden;
}
.chart-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--blue),var(--green));
}
.chart-title{font-size:18px;font-weight:600;color:var(--text-bright);margin-bottom:4px}
.chart-subtitle{font-size:13px;color:var(--text-dim);margin-bottom:24px}
.bar-chart{display:flex;flex-direction:column;gap:12px}
.bar-row{display:flex;align-items:center;gap:12px}
.bar-label{width:60px;font-size:13px;color:var(--text-dim);text-align:right;flex-shrink:0}
.bar-track{flex:1;height:32px;background:rgba(255,255,255,0.04);border-radius:6px;overflow:hidden;position:relative}
.bar-fill{
  height:100%;border-radius:6px;display:flex;align-items:center;
  padding-left:12px;font-size:12px;font-weight:600;color:#fff;
  transition:width 1.5s cubic-bezier(.22,1,.36,1);
  width:0;
  position:relative;
}
.bar-fill.blue{background:linear-gradient(90deg,rgba(0,212,255,0.8),rgba(0,212,255,0.4))}
.bar-fill.green{background:linear-gradient(90deg,rgba(0,255,136,0.8),rgba(0,255,136,0.4))}
.bar-fill.orange{background:linear-gradient(90deg,rgba(255,165,0,0.8),rgba(255,165,0,0.4))}
.bar-fill.red{background:linear-gradient(90deg,rgba(255,80,80,0.8),rgba(255,80,80,0.4))}
.bar-value{
  position:absolute;right:12px;font-size:12px;
  color:var(--text-dim);font-weight:500;
}

/* ============ COMPARISON SECTION ============ */
.compare-container{
  display:grid;grid-template-columns:1fr 60px 1fr;
  gap:0;align-items:stretch;
}
.compare-side{
  background:var(--card);border-radius:16px;padding:32px;
  border:1px solid var(--card-border);transition:all .4s ease;
  cursor:pointer;position:relative;overflow:hidden;
}
.compare-side:hover{
  border-color:rgba(0,212,255,0.3);
  box-shadow:0 8px 40px rgba(0,212,255,0.08);
}
.compare-side.active-compare{
  border-color:rgba(0,255,136,0.4);
  box-shadow:0 8px 40px rgba(0,255,136,0.12);
}
.compare-vs{
  display:flex;align-items:center;justify-content:center;
  font-size:20px;font-weight:700;color:var(--text-dim);
}
.compare-tag{
  display:inline-block;padding:4px 12px;border-radius:20px;
  font-size:12px;font-weight:600;margin-bottom:16px;
}
.tag-train{background:rgba(0,212,255,0.15);color:var(--blue)}
.tag-infer{background:rgba(0,255,136,0.15);color:var(--green)}
.compare-title{font-size:24px;font-weight:700;color:var(--text-bright);margin-bottom:8px}
.compare-desc{font-size:14px;color:var(--text-dim);margin-bottom:20px}
.compare-stats{display:flex;flex-direction:column;gap:12px}
.compare-stat{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04)}
.compare-stat .stat-label{font-size:13px;color:var(--text-dim)}
.compare-stat .stat-val{font-size:15px;font-weight:600;color:var(--text-bright)}

/* ============ DONUT CHART ============ */
.donut-section{
  display:flex;gap:40px;align-items:center;justify-content:center;
  flex-wrap:wrap;margin-top:40px;
}
.donut-wrap{position:relative;width:220px;height:220px}
.donut-wrap svg{transform:rotate(-90deg)}
.donut-center{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  text-align:center;
}
.donut-center .pct{font-size:28px;font-weight:700;color:var(--text-bright)}
.donut-center .lbl{font-size:11px;color:var(--text-dim)}
.donut-legend{display:flex;flex-direction:column;gap:12px}
.legend-item{display:flex;align-items:center;gap:10px;font-size:14px}
.legend-dot{width:12px;height:12px;border-radius:3px;flex-shrink:0}

/* ============ ENERGY SECTION ============ */
.energy-grid{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  gap:16px;margin-top:40px;
}
.energy-card{
  background:var(--card);border:1px solid var(--card-border);
  border-radius:12px;padding:24px;text-align:center;
  transition:all .3s ease;
}
.energy-card:hover{transform:translateY(-4px);border-color:rgba(0,255,136,0.3)}
.energy-icon{font-size:32px;margin-bottom:12px}
.energy-val{
  font-size:28px;font-weight:700;margin-bottom:4px;
  background:linear-gradient(135deg,var(--green),var(--blue));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}
.energy-lbl{font-size:12px;color:var(--text-dim);letter-spacing:1px}

/* ============ IMPACT COUNTER ============ */
.counter-strip{
  display:flex;justify-content:center;gap:48px;flex-wrap:wrap;
  padding:60px 24px;
  background:linear-gradient(135deg,rgba(0,212,255,0.05),rgba(0,255,136,0.05));
  border-top:1px solid var(--card-border);border-bottom:1px solid var(--card-border);
}
.counter-item{text-align:center}
.counter-num{
  font-size:clamp(32px,5vw,56px);font-weight:700;
  font-variant-numeric:tabular-nums;
  color:var(--text-bright);
}
.counter-num .unit{font-size:0.5em;color:var(--blue);font-weight:400}
.counter-label{font-size:12px;color:var(--text-dim);margin-top:4px;letter-spacing:1px;text-transform:uppercase}

/* ============ FOOTER ============ */
.footer{
  text-align:center;padding:80px 24px;
  background:var(--darker);border-top:1px solid var(--card-border);
}
.footer-quote{
  font-size:clamp(20px,3vw,36px);font-weight:600;
  color:var(--text-bright);max-width:800px;margin:0 auto 24px;
  line-height:1.3;
}
.footer-note{font-size:14px;color:var(--text-dim);max-width:600px;margin:0 auto}
.footer-sources{
  margin-top:40px;padding-top:40px;border-top:1px solid rgba(255,255,255,0.06);
  font-size:11px;color:var(--text-dim);max-width:800px;margin-left:auto;margin-right:auto;
  text-align:left;line-height:1.8;
}
.footer-sources a{color:var(--blue);text-decoration:none}

/* ============ NAV DOTS ============ */
.nav-dots{
  position:fixed;right:24px;top:50%;transform:translateY(-50%);
  display:flex;flex-direction:column;gap:12px;z-index:100;
}
.nav-dot{
  width:10px;height:10px;border-radius:50%;
  background:rgba(255,255,255,0.15);cursor:pointer;
  transition:all .3s ease;border:none;
}
.nav-dot.active{background:var(--blue);box-shadow:0 0 12px rgba(0,212,255,0.5)}
.nav-dot:hover{background:rgba(0,212,255,0.5)}

/* ============ ANIMATIONS ============ */
.reveal{opacity:0;transform:translateY(30px);transition:all .8s cubic-bezier(.22,1,.36,1)}
.reveal.visible{opacity:1;transform:translateY(0)}

/* ============ RESPONSIVE ============ */
@media(max-width:768px){
  .timeline-line{left:20px}
  .timeline-node,.timeline-node:nth-child(even){flex-direction:column;padding-left:50px}
  .timeline-dot{left:20px!important}
  .timeline-card{width:100%!important}
  .compare-container{grid-template-columns:1fr;gap:16px}
  .compare-vs{padding:8px 0}
  .hero-stats{gap:24px}
  .counter-strip{gap:24px}
  .nav-dots{display:none}
}
</style>
</head>
<body>

<!-- NAV DOTS -->
<nav class="nav-dots" id="navDots">
  <button class="nav-dot active" data-section="hero" title="开场"></button>
  <button class="nav-dot" data-section="story" title="故事"></button>
  <button class="nav-dot" data-section="timeline" title="时间线"></button>
  <button class="nav-dot" data-section="charts" title="数据"></button>
  <button class="nav-dot" data-section="compare" title="对比"></button>
  <button class="nav-dot" data-section="energy" title="能源"></button>
  <button class="nav-dot" data-section="footer" title="终章"></button>
</nav>

<!-- HERO -->
<section class="hero section" id="hero">
  <canvas id="particles-canvas"></canvas>
  <div class="hero-content">
    <div class="hero-label">AI Compute Explosion · 2023—2026</div>
    <h1>
      2023年，全球AI消耗<br>
      <span class="accent">1,000亿</span> Token<br>
      2026年，这个数字是<br>
      <span class="green-accent">500万亿</span>
    </h1>
    <p class="hero-sub">三年，5000倍的指数级爆发。一场关于算力、能源与未来的深刻变革正在发生。</p>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="number" data-count="5000">0</div>
        <div class="label">倍增长</div>
      </div>
      <div class="hero-stat">
        <div class="number" data-count="565">0</div>
        <div class="label">TWh 数据中心能耗</div>
      </div>
      <div class="hero-stat">
        <div class="number" data-count="10">0</div>
        <div class="label">百万 GPU 年出货</div>
      </div>
    </div>
  </div>
  <div class="scroll-hint">
    <span>向下探索</span>
    <div class="scroll-arrow"></div>
  </div>
</section>

<!-- STORY: OPENING NARRATIVE -->
<section class="section section-light" id="story">
  <div class="container">
    <div class="section-header reveal">
      <div class="section-label">Chapter I · 觉醒</div>
      <h2 class="section-title">Token，AI时代的「新石油」</h2>
      <p class="section-desc">当国家数据局将Token正式定名为「词元」，一个信号已经发出：智能经济的价值锚点正在从「流量」转向「Token」。</p>
    </div>
    <div class="counter-strip reveal">
      <div class="counter-item">
        <div class="counter-num" data-target="140" data-suffix="万亿"><span class="counter-val">0</span><span class="unit"> 万亿</span></div>
        <div class="counter-label">2026年3月 日均消耗</div>
      </div>
      <div class="counter-item">
        <div class="counter-num" data-target="289" data-suffix="%"><span class="counter-val">0</span><span class="unit">%</span></div>
        <div class="counter-label">年增长率</div>
      </div>
      <div class="counter-item">
        <div class="counter-num" data-target="78" data-suffix="%"><span class="counter-val">0</span><span class="unit">%</span></div>
        <div class="counter-label">推理场景占比</div>
      </div>
    </div>
    <div style="max-width:700px;margin:40px auto 0;text-align:center" class="reveal">
      <p style="font-size:17px;color:var(--text-dim);line-height:1.8">
        2024年初，中国日均Token调用量约<strong style="color:var(--blue)">1,000亿</strong>；
        到2025年底跃升至<strong style="color:var(--blue)">100万亿</strong>；
        2026年3月突破<strong style="color:var(--green)">140万亿</strong>，
        预计年底达到<strong style="color:var(--green)">300-500万亿</strong>。
        <br><br>
        两年增长超过<strong style="color:var(--text-bright)">1000倍</strong>。
        这不是线性增长——这是典型的指数级加速。
      </p>
    </div>
  </div>
</section>

<!-- INTERACTIVE TIMELINE -->
<section class="section section-dark" id="timeline">
  <div class="container">
    <div class="section-header reveal">
      <div class="section-label">Chapter II · 迁徙</div>
      <h2 class="section-title">算力爆发时间线</h2>
      <p class="section-desc">点击每个节点，探索AI算力消耗的三年指数级迁徙</p>
    </div>
    <div class="timeline-wrap">
      <div class="timeline-line"></div>

      <!-- 2023 -->
      <div class="timeline-node" data-year="2023">
        <div class="timeline-dot"></div>
        <div class="timeline-card">
          <div class="timeline-year">2023 · 起点</div>
          <div class="timeline-title">大模型时代的黎明</div>
          <p style="font-size:14px;color:var(--text-dim)">ChatGPT引爆全球AI浪潮，算力需求开始指数级攀升</p>
          <div class="timeline-metric">
            <div class="metric-badge"><div class="val">~1000亿</div><div class="lbl">全球日均Token</div></div>
            <div class="metric-badge"><div class="val">376万</div><div class="lbl">GPU出货量</div></div>
            <div class="metric-badge"><div class="val">400W</div><div class="lbl">A100单卡功耗</div></div>
          </div>
          <div class="detail-panel"><div class="detail-content">
            <p><strong>GPT-4训练</strong>消耗约50 GWh电力，相当于5,000个美国家庭一年的用电量。全球AI数据中心能耗约85-134 TWh，占全球电力的1.5%。训练是绝对主力——一次训练运行可能持续数周到数月，功耗达25-50 MW。</p>
            <p style="margin-top:8px">英伟达A100是这一时期的主力芯片，单卡功耗400W（SXM版），全球数据中心GPU出货约376万块。微软承诺到年底部署100万块AI芯片。</p>
          </div></div>
        </div>
      </div>

      <!-- 2024 -->
      <div class="timeline-node" data-year="2024">
        <div class="timeline-dot"></div>
        <div class="timeline-card">
          <div class="timeline-year">2024 · 加速</div>
          <div class="timeline-title">推理超越训练，GPU功耗翻倍</div>
          <p style="font-size:14px;color:var(--text-dim)">H100全面铺开，推理算力需求首次超过训练</p>
          <div class="timeline-metric">
            <div class="metric-badge"><div class="val">~10万亿</div><div class="lbl">全球日均Token</div></div>
            <div class="metric-badge"><div class="val">52%</div><div class="lbl">推理算力占比</div></div>
            <div class="metric-badge"><div class="val">700W</div><div class="lbl">H100单卡功耗</div></div>
          </div>
          <div class="detail-panel"><div class="detail-content">
            <p><strong>H100 SXM</strong>单卡功耗跃升至700W，较A100提升75%。全球AI数据中心能耗达<strong>415 TWh</strong>，占全球电力1.5%——相当于整个英国的年用电量。推理算力占比首次超过训练，达到52%。</p>
            <p style="margin-top:8px">谷歌Token月消耗从4月的9.7万亿飙升至年底的数十万亿。中国日均Token从1,000亿级快速攀升。火山引擎日均Token从刚推出时的基数增长了417倍。HBM（高带宽内存）开始成为核心瓶颈。</p>
          </div></div>
        </div>
      </div>

      <!-- 2025 -->
      <div class="timeline-node" data-year="2025">
        <div class="timeline-dot"></div>
        <div class="timeline-card">
          <div class="timeline-year">2025 · 爆发</div>
          <div class="timeline-title">Token经济元年，算力供不应求</div>
          <p style="font-size:14px;color:var(--text-dim)">AI智能体引爆新一轮消耗，云厂商集体涨价</p>
          <div class="timeline-metric">
            <div class="metric-badge"><div class="val">100万亿</div><div class="lbl">中国日均Token</div></div>
            <div class="metric-badge"><div class="val">700万</div><div class="lbl">GPU年出货</div></div>
            <div class="metric-badge"><div class="val">447 TWh</div><div class="lbl">全球DC能耗</div></div>
          </div>
          <div class="detail-panel"><div class="detail-content">
            <p><strong>全球AI Token年消耗量</strong>突破4.8×10¹⁵个，同比增长212%。亚太地区以43%的全球消耗量首次超越北美。NVIDIA出货约700万块AI GPU，其中Blackwell(B200/B300)超过520万块。</p>
            <p style="margin-top:8px">豆包大模型日均Token突破<strong>50万亿</strong>，较上年同期增长超10倍。谷歌月处理Token达<strong>1,300万亿</strong>。全球AI芯片总部署数超4,500万块。单位Token推理成本降至$0.00012，较去年下降64%。智谱打响涨价第一枪——上调Coding Plan套餐30%。</p>
          </div></div>
        </div>
      </div>

      <!-- 2026 -->
      <div class="timeline-node" data-year="2026">
        <div class="timeline-dot"></div>
        <div class="timeline-card">
          <div class="timeline-year">2026 · 临界</div>
          <div class="timeline-title">电力成为终极瓶颈</div>
          <p style="font-size:14px;color:var(--text-dim)">从芯片短缺到电力短缺，算力基建撞上能源天花板</p>
          <div class="timeline-metric">
            <div class="metric-badge"><div class="val">500万亿</div><div class="lbl">预计年底日均</div></div>
            <div class="metric-badge"><div class="val">565 TWh</div><div class="lbl">全球DC能耗</div></div>
            <div class="metric-badge"><div class="val">1000W+</div><div class="lbl">B200单卡功耗</div></div>
          </div>
          <div class="detail-panel"><div class="detail-content">
            <p><strong>全球数据中心能耗</strong>预计跃升至565 TWh，一年净增118 TWh——接近瑞典全国全年用电量。AI服务器用电从95 TWh暴涨至175 TWh，同比增速84%。到2027年，AI服务器用电将首次超过传统服务器。</p>
            <p style="margin-top:8px">B200单卡功耗突破1,000W，GB200系统达到2,700W。50%的美国拟建数据中心遭遇电网接入延期。马斯克2024年的预言正在成真：「一年后是变压器短缺，两年后会出现全面的电力短缺。」预计年底全球Token日均消耗将达300-500万亿。</p>
          </div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- DATA CHARTS -->
<section class="section section-light" id="charts">
  <div class="container">
    <div class="section-header reveal">
      <div class="section-label">Chapter III · 量级</div>
      <h2 class="section-title">数据背后的震撼</h2>
      <p class="section-desc">数字不说谎——每一组数据背后都是指数级增长的曲线</p>
    </div>
    <div class="chart-grid">

      <!-- Token消耗增长 -->
      <div class="chart-card reveal">
        <div class="chart-title">Token日均消耗量</div>
        <div class="chart-subtitle">中国 日均Token消耗 · 2024-2026</div>
        <div class="bar-chart" data-chart="token">
          <div class="bar-row">
            <div class="bar-label">2024 Q1</div>
            <div class="bar-track"><div class="bar-fill blue" data-width="2" style="width:0%"><span class="bar-value">1,000亿</span></div></div>
          </div>
          <div class="bar-row">
            <div class="bar-label">2024 Q4</div>
            <div class="bar-track"><div class="bar-fill blue" data-width="8" style="width:0%"><span class="bar-value">10万亿</span></div></div>
          </div>
          <div class="bar-row">
            <div class="bar-label">2025 H1</div>
            <div class="bar-track"><div class="bar-fill blue" data-width="22" style="width:0%"><span class="bar-value">30万亿</span></div></div>
          </div>
          <div class="bar-row">
            <div class="bar-label">2025 Q4</div>
            <div class="bar-track"><div class="bar-fill green" data-width="50" style="width:0%"><span class="bar-value">100万亿</span></div></div>
          </div>
          <div class="bar-row">
            <div class="bar-label">2026.03</div>
            <div class="bar-track"><div class="bar-fill green" data-width="70" style="width:0%"><span class="bar-value">140万亿</span></div></div>
          </div>
          <div class="bar-row">
            <div class="bar-label">2026 EoY</div>
            <div class="bar-track"><div class="bar-fill green" data-width="100" style="width:0%"><span class="bar-value">300-500万亿</span></div></div>
          </div>
        </div>
      </div>

      <!-- GPU出货量 -->
      <div class="chart-card reveal">
        <div class="chart-title">AI GPU年出货量</div>
        <div class="chart-subtitle">NVIDIA AI GPU出货量（百万块）</div>
        <div class="bar-chart" data-chart="gpu">
          <div class="bar-row">
            <div class="bar-label">2