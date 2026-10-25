#!/usr/bin/env python3
"""Generate the NVIDIA-HuggingFace Power Map interactive HTML."""

import os

OUTPUT = "/app/working/shared/showcase/2026-09-01-nvidia-huggingface-power-map.html"

# ─── CSS ────────────────────────────────────────────────────────────────
CSS = r"""
:root {
  --nvidia-green: #76B900;
  --nvidia-green-dim: rgba(118,185,0,0.15);
  --tech-blue: #00BFFF;
  --tech-blue-dim: rgba(0,191,255,0.12);
  --bg-dark: #0a0a0f;
  --bg-card: #12121a;
  --bg-card-hover: #1a1a28;
  --text-primary: #f0f0f5;
  --text-secondary: #8888aa;
  --accent-red: #ff4444;
  --accent-gold: #FFD700;
  --border: rgba(255,255,255,0.06);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif;background:var(--bg-dark);color:var(--text-primary);overflow-x:hidden;line-height:1.6}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(118,185,0,0.3);border-radius:3px}

/* ─── HERO ────────────────────────────────────────────────────────── */
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;overflow:hidden;background:radial-gradient(ellipse at 50% 30%,rgba(118,185,0,0.08) 0%,transparent 60%),var(--bg-dark)}
.hero-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(118,185,0,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(118,185,0,0.03) 1px,transparent 1px);background-size:60px 60px;animation:gridPulse 8s ease-in-out infinite}
@keyframes gridPulse{0%,100%{opacity:0.3}50%{opacity:0.7}}
.hero-particles{position:absolute;inset:0;overflow:hidden}
.particle{position:absolute;border-radius:50%;background:var(--nvidia-green);opacity:0;animation:particleFloat linear infinite}
@keyframes particleFloat{0%{opacity:0;transform:translateY(100vh) scale(0)}10%{opacity:0.6}90%{opacity:0.6}100%{opacity:0;transform:translateY(-10vh) scale(1)}}
.hero-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 20px;border-radius:999px;background:rgba(118,185,0,0.1);border:1px solid rgba(118,185,0,0.25);font-size:13px;color:var(--nvidia-green);letter-spacing:0.5px;margin-bottom:32px;opacity:0;animation:fadeUp 0.8s 0.3s forwards}
.hero-badge::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--nvidia-green);animation:dotPulse 2s infinite}
@keyframes dotPulse{0%,100%{opacity:1}50%{opacity:0.3}}
.hero h1{font-size:clamp(36px,6vw,72px);font-weight:700;letter-spacing:-1.5px;line-height:1.05;max-width:900px;opacity:0;animation:fadeUp 1s 0.5s forwards}
.hero h1 .green{color:var(--nvidia-green)}
.hero h1 .blue{color:var(--tech-blue)}
.hero-sub{font-size:clamp(16px,2vw,22px);color:var(--text-secondary);max-width:700px;margin-top:24px;opacity:0;animation:fadeUp 1s 0.8s forwards}
.hero-stats{display:flex;gap:48px;margin-top:48px;opacity:0;animation:fadeUp 1s 1.1s forwards}
.hero-stat{text-align:center}
.hero-stat-val{font-size:clamp(28px,4vw,48px);font-weight:700;color:var(--nvidia-green);font-variant-numeric:tabular-nums}
.hero-stat-label{font-size:13px;color:var(--text-secondary);margin-top:4px}
.scroll-hint{position:absolute;bottom:40px;display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--text-secondary);font-size:12px;opacity:0;animation:fadeUp 1s 1.5s forwards}
.scroll-arrow{width:24px;height:24px;border-right:2px solid var(--nvidia-green);border-bottom:2px solid var(--nvidia-green);transform:rotate(45deg);animation:scrollBounce 2s infinite}
@keyframes scrollBounce{0%,100%{transform:rotate(45deg) translateY(0)}50%{transform:rotate(45deg) translateY(8px)}}
@keyframes fadeUp{to{opacity:1;transform:translateY(0)}from{opacity:0;transform:translateY(30px)}}

/* ─── SECTIONS ──────────────────────────────────────────────────── */
section{padding:100px 24px;max-width:1200px;margin:0 auto}
.section-label{display:inline-flex;align-items:center;gap:8px;font-size:12px;color:var(--nvidia-green);text-transform:uppercase;letter-spacing:2px;margin-bottom:16px;font-weight:600}
.section-title{font-size:clamp(28px,4vw,48px);font-weight:700;letter-spacing:-1px;margin-bottom:16px}
.section-desc{font-size:17px;color:var(--text-secondary);max-width:700px;margin-bottom:48px}

/* ─── TOGGLE SWITCH ──────────────────────────────────────────────── */
.toggle-container{display:flex;justify-content:center;margin-bottom:48px}
.toggle-bar{display:flex;background:var(--bg-card);border-radius:999px;padding:4px;border:1px solid var(--border)}
.toggle-btn{padding:12px 32px;border-radius:999px;border:none;background:transparent;color:var(--text-secondary);font-size:15px;font-weight:600;cursor:pointer;transition:all 0.4s;position:relative;z-index:1}
.toggle-btn.active{color:#000}
.toggle-btn.active::after{content:'';position:absolute;inset:0;border-radius:999px;background:var(--nvidia-green);z-index:-1}
.toggle-btn:not(.active):hover{color:var(--text-primary)}

/* ─── WORLD MAP ──────────────────────────────────────────────────── */
.map-container{position:relative;width:100%;aspect-ratio:2/1;background:var(--bg-card);border-radius:16px;overflow:hidden;border:1px solid var(--border);margin-bottom:48px}
.map-container svg{width:100%;height:100%}
.map-tooltip{position:fixed;padding:16px 20px;background:rgba(18,18,26,0.95);backdrop-filter:blur(20px);border:1px solid var(--border);border-radius:12px;font-size:13px;pointer-events:none;opacity:0;transition:opacity 0.2s;z-index:100;max-width:320px;box-shadow:0 20px 60px rgba(0,0,0,0.5)}
.map-tooltip h4{color:var(--nvidia-green);font-size:15px;margin-bottom:6px}
.map-tooltip .tt-row{display:flex;justify-content:space-between;gap:16px;padding:3px 0;color:var(--text-secondary)}
.map-tooltip .tt-row span:last-child{color:var(--text-primary);font-weight:600;font-variant-numeric:tabular-nums}
.company-dot{cursor:pointer;transition:all 0.3s}
.company-dot:hover{filter:drop-shadow(0 0 12px var(--nvidia-green))}

/* ─── INFLUENCE RINGS ──────────────────────────────────────────── */
@keyframes ringPulse{0%{r:0;opacity:0.6}100%{r:30;opacity:0}}
.ring-pulse{animation:ringPulse 3s infinite}

/* ─── DATA CARDS GRID ──────────────────────────────────────────── */
.cards-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-bottom:48px}
.data-card{background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:28px;transition:all 0.3s;position:relative;overflow:hidden}
.data-card:hover{background:var(--bg-card-hover);border-color:rgba(118,185,0,0.2);transform:translateY(-2px)}
.data-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--nvidia-green),var(--tech-blue));opacity:0;transition:opacity 0.3s}
.data-card:hover::before{opacity:1}
.data-card .icon{font-size:28px;margin-bottom:12px}
.data-card h3{font-size:18px;font-weight:600;margin-bottom:6px}
.data-card p{font-size:14px;color:var(--text-secondary);line-height:1.5}
.data-card .big-num{font-size:36px;font-weight:700;color:var(--nvidia-green);font-variant-numeric:tabular-nums}
.data-card .tag{display:inline-block;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600;margin-top:8px}
.tag-green{background:rgba(118,185,0,0.15);color:var(--nvidia-green)}
.tag-blue{background:rgba(0,191,255,0.15);color:var(--tech-blue)}
.tag-red{background:rgba(255,68,68,0.15);color:var(--accent-red)}
.tag-gold{background:rgba(255,215,0,0.15);color:var(--accent-gold)}

/* ─── TIMELINE ────────────────────────────────────────────────── */
.timeline{position:relative;padding-left:40px}
.timeline::before{content:'';position:absolute;left:15px;top:0;bottom:0;width:2px;background:linear-gradient(180deg,var(--nvidia-green),var(--tech-blue),transparent)}
.timeline-item{position:relative;margin-bottom:48px;opacity:0;transform:translateX(-20px);transition:all 0.6s}
.timeline-item.visible{opacity:1;transform:translateX(0)}
.timeline-dot{position:absolute;left:-33px;top:6px;width:12px;height:12px;border-radius:50%;background:var(--nvidia-green);box-shadow:0 0 20px rgba(118,185,0,0.4)}
.timeline-year{font-size:13px;color:var(--nvidia-green);font-weight:600;margin-bottom:4px}
.timeline-title{font-size:18px;font-weight:600;margin-bottom:4px}
.timeline-desc{font-size:14px;color:var(--text-secondary);line-height:1.5}

/* ─── CHART SECTIONS ──────────────────────────────────────────── */
.chart-row{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:48px}
@media(max-width:768px){.chart-row{grid-template-columns:1fr}}
.chart-box{background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:28px;min-height:360px;position:relative}
.chart-box h3{font-size:16px;font-weight:600;margin-bottom:4px}
.chart-box .chart-sub{font-size:13px;color:var(--text-secondary);margin-bottom:20px}
.chart-box canvas{width:100%!important}

/* ─── POWER STRIPS ──────────────────────────────────────────────── */
.power-strips{display:flex;flex-direction:column;gap:12px;margin-bottom:48px}
.power-strip{display:flex;align-items:center;gap:16px;padding:16px 20px;background:var(--bg-card);border-radius:12px;border:1px solid var(--border);transition:all 0.3s}
.power-strip:hover{border-color:rgba(118,185,0,0.2)}
.power-strip .ps-name{width:160px;font-weight:600;font-size:14px;flex-shrink:0}
.power-strip .ps-bar-wrap{flex:1;height:28px;background:rgba(255,255,255,0.04);border-radius:6px;overflow:hidden;position:relative}
.power-strip .ps-bar{height:100%;border-radius:6px;transition:width 1.5s cubic-bezier(0.16,1,0.3,1);display:flex;align-items:center;justify-content:flex-end;padding-right:10px;font-size:12px;font-weight:700;color:#000;min-width:40px}
.power-strip .ps-val{width:80px;text-align:right;font-size:14px;font-weight:700;font-variant-numeric:tabular-nums;flex-shrink:0}

/* ─── BATTLE CARD ──────────────────────────────────────────────── */
.battle-grid{display:grid;grid-template-columns:1fr 60px 1fr;gap:0;margin-bottom:48px;align-items:stretch}
.battle-side{padding:32px;border-radius:12px}
.battle-left{background:linear-gradient(135deg,rgba(255,68,68,0.08),rgba(255,68,68,0.02));border:1px solid rgba(255,68,68,0.15);text-align:right}
.battle-right{background:linear-gradient(135deg,rgba(118,185,0,0.08),rgba(118,185,0,0.02));border:1px solid rgba(118,185,0,0.15)}
.battle-vs{display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;color:var(--text-secondary)}
.battle-side h3{font-size:22px;font-weight:700;margin-bottom:16px}
.battle-left h3{color:var(--accent-red)}
.battle-right h3{color:var(--nvidia-green)}
.battle-item{padding:8px 0;font-size:14px;color:var(--text-secondary);border-bottom:1px solid rgba(255,255,255,0.04)}
.battle-item:last-child{border:none}

/* ─── NARRATIVE QUOTE ──────────────────────────────────────────── */
.quote-block{position:relative;padding:48px;background:linear-gradient(135deg,rgba(118,185,0,0.06),rgba(0,191,255,0.04));border-radius:16px;border-left:4px solid var(--nvidia-green);margin-bottom:48px}
.quote-block::before{content:'\"';position:absolute;top:16px;left:24px;font-size:64px;color:rgba(118,185,0,0.2);font-family:Georgia,serif;line-height:1}
.quote-text{font-size:clamp(18px,2.5vw,24px);font-weight:500;line-height:1.5;position:relative;z-index:1}
.quote-author{margin-top:16px;font-size:14px;color:var(--text-secondary)}
.quote-author strong{color:var(--nvidia-green)}

/* ─── FOOTER ──────────────────────────────────────────────────── */
footer{text-align:center;padding:80px 24px;border-top:1px solid var(--border)}
footer p{font-size:13px;color:var(--text-secondary)}
footer .ft-brand{font-size:15px;font-weight:600;color:var(--nvidia-green);margin-bottom:8px}

/* ─── RESPONSIVE ──────────────────────────────────────────────── */
@media(max-width:640px){
  .hero-stats{flex-direction:column;gap:24px}
  .battle-grid{grid-template-columns:1fr;gap:16px}
  .battle-vs{display:none}
  .battle-side{text-align:left!important}
  section{padding:60px 16px}
}

/* ─── SCROLL REVEAL ──────────────────────────────────────────── */
.reveal{opacity:0;transform:translateY(40px);transition:all 0.8s cubic-bezier(0.16,1,0.3,1)}
.reveal.visible{opacity:1;transform:none}

/* ─── FLOW ARROWS ──────────────────────────────────────────────── */
.flow-container{display:flex;align-items:center;justify-content:center;gap:0;flex-wrap:wrap;margin-bottom:48px}
.flow-node{padding:20px 24px;background:var(--bg-card);border:1px solid var(--border);border-radius:12px;text-align:center;min-width:140px;transition:all 0.3s}
.flow-node:hover{border-color:rgba(118,185,0,0.3);background:var(--bg-card-hover)}
.flow-node .fn-icon{font-size:24px;margin-bottom:6px}
.flow-node .fn-title{font-size:13px;font-weight:600}
.flow-node .fn-sub{font-size:11px;color:var(--text-secondary)}
.flow-arrow{font-size:24px;color:var(--nvidia-green);padding:0 8px}

/* ─── METRICS ROW ──────────────────────────────────────────── */
.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:48px}
@media(max-width:768px){.metrics-row{grid-template-columns:repeat(2,1fr)}}
.metric-card{text-align:center;padding:24px 16px;background:var(--bg-card);border-radius:12px;border:1px solid var(--border)}
.metric-card .mc-val{font-size:clamp(24px,3vw,36px);font-weight:700;font-variant-numeric:tabular-nums}
.metric-card .mc-label{font-size:12px;color:var(--text-secondary);margin-top:4px}
.mc-green{color:var(--nvidia-green)}
.mc-blue{color:var(--tech-blue)}
.mc-gold{color:var(--accent-gold)}
.mc-red{color:var(--accent-red)}

/* ─── ANIMATED LINE ──────────────────────────────────────────── */
@keyframes dashMove{to{stroke-dashoffset:-20}}
.flow-line{stroke-dasharray:10 10;animation:dashMove 1s linear infinite}
"""

# ─── HTML BODY ──────────────────────────────────────────────────────
HTML_BODY = r"""
<!-- ═══════════════ HERO ═══════════════ -->
<section class="hero" id="hero">
  <div class="hero-grid"></div>
  <div class="hero-particles" id="particles"></div>
  <div class="hero-badge">⚡ P0 创意交互体验 · 2026-09-01</div>
  <h1>当 <span class="green">129亿</span> 美元<br>改写AI权力版图</h1>
  <p class="hero-sub">英伟达收购Hugging Face —— 从芯片霸主到生态帝国<br>一场正在重绘全球AI地理的世纪交易</p>
  <div class="hero-stats">
    <div class="hero-stat"><div class="hero-stat-val" data-count="129" data-suffix="亿">$129亿</div><div class="hero-stat-label">交易金额</div></div>
    <div class="hero-stat"><div class="hero-stat-val" data-count="300" data-suffix="万+">300万+</div><div class="hero-stat-label">托管模型</div></div>
    <div class="hero-stat"><div class="hero-stat-val" data-count="1300" data-suffix="万+">1300万+</div><div class="hero-stat-label">全球开发者</div></div>
    <div class="hero-stat"><div class="hero-stat-val" data-count="86" data-suffix="x">86x</div><div class="hero-stat-label">收入倍数</div></div>
  </div>
  <div class="scroll-hint"><span>向下探索</span><div class="scroll-arrow"></div></div>
</section>

<!-- ═══════════════ CHAPTER 1: THE DEAL ═══════════════ -->
<section id="chapter1" class="reveal">
  <div class="section-label">📖 CHAPTER 01</div>
  <h2 class="section-title">天价交易：867亿人民币的"核弹"</h2>
  <p class="section-desc">2026年8月26日，英伟达以129亿美元收购Hugging Face——AI开源生态版图被彻底改写</p>

  <div class="quote-block">
    <p class="quote-text">"当英伟达以129亿美元收购Hugging Face，AI开源生态的版图被彻底改写。这不仅是一家芯片公司史上最大的收购之一，更标志着AI产业从'卖铲子'到'掌控金矿'的战略跃迁。"</p>
    <p class="quote-author">—— <strong>华尔街见闻</strong> · 2026.08.27</p>
  </div>

  <div class="cards-grid">
    <div class="data-card">
      <div class="icon">🏢</div>
      <h3>Hugging Face 是谁？</h3>
      <p>AI界的GitHub。成立于2016年，托管300万+公开模型、100万+数据集，服务1300万开发者。月活访客超1800万，2000+企业付费使用Enterprise Hub。</p>
      <span class="tag tag-green">全球最大的开源AI平台</span>
    </div>
    <div class="data-card">
      <div class="big-num">$129亿</div>
      <h3>收购价格</h3>
      <p>较2023年D轮45亿美元估值增长187%。按年化收入1.5亿美元计算，收购价约为收入的86倍——天价中的天价。</p>
      <span class="tag tag-gold">英伟达史上最大收购之一</span>
    </div>
    <div class="data-card">
      <div class="icon">📊</div>
      <h3>财务背景</h3>
      <p>英伟达Q2营收962亿美元，现金储备超600亿美元。129亿仅占其现金的五分之一——对黄仁勋来说，这是轻而易举的战略投资。</p>
      <span class="tag tag-blue">现金流充裕</span>
    </div>
    <div class="data-card">
      <div class="icon">🔥</div>
      <h3>收购前9个月</h3>
      <p>英伟达曾以5亿美元注资方案被拒——Hugging Face担心损害平台中立性。从"拒绝参股"到"整体卖身"，只隔了一个夏天。</p>
      <span class="tag tag-red">戏剧性转折</span>
    </div>
  </div>

  <!-- Strategy Flow -->
  <h3 style="font-size:20px;font-weight:600;margin-bottom:24px">🎯 三重战略逻辑</h3>
  <div class="flow-container">
    <div class="flow-node"><div class="fn-icon">🛡️</div><div class="fn-title">防御性进攻</div><div class="fn-sub">对冲闭源芯片威胁</div></div>
    <div class="flow-arrow">→</div>
    <div class="flow-node"><div class="fn-icon">🔗</div><div class="fn-title">掌控中间层</div><div class="fn-sub">控制AI分发管道</div></div>
    <div class="flow-arrow">→</div>
    <div class="flow-node"><div class="fn-icon">☁️</div><div class="fn-title">重返云计算</div><div class="fn-sub">DGX Cloud捷径</div></div>
    <div class="flow-arrow">→</div>
    <div class="flow-node"><div class="fn-icon">👑</div><div class="fn-title">全栈AI帝国</div><div class="fn-sub">芯片→模型→生态</div></div>
  </div>
</section>

<!-- ═══════════════ CHAPTER 2: GLOBAL MAP ═══════════════ -->
<section id="chapter2" class="reveal">
  <div class="section-label">🌍 CHAPTER 02</div>
  <h2 class="section-title">AI权力地理图：谁在控制版图？</h2>
  <p class="section-desc">探索全球AI企业的分布与影响力——从硅谷到北京，从巴黎到东京，权力正在重新划分</p>

  <div class="toggle-container">
    <div class="toggle-bar">
      <button class="toggle-btn active" onclick="toggleMap('before')">收购前</button>
      <button class="toggle-btn" onclick="toggleMap('after')">收购后</button>
    </div>
  </div>

  <div class="map-container" id="worldMap"></div>
  <div class="map-tooltip" id="mapTooltip"></div>

  <h3 style="font-size:20px;font-weight:600;margin-bottom:16px">🏆 AI企业估值金字塔（2026年7月）</h3>
  <div class="power-strips" id="valuationStrips"></div>
</section>

<!-- ═══════════════ CHAPTER 3: BEFORE vs AFTER ═══════════════ -->
<section id="chapter3" class="reveal">
  <div class="section-label">⚔️ CHAPTER 03</div>
  <h2 class="section-title">收购前 vs 收购后：生态大变局</h2>
  <p class="section-desc">一笔交易如何重塑AI产业的竞争格局</p>

  <div class="battle-grid">
    <div class="battle-side battle-left">
      <h3>🔴 收购前</h3>
      <div class="battle-item">Hugging Face 中立平台，支持所有芯片</div>
      <div class="battle-item">AMD/Intel/华为均可平等接入</div>
      <div class="battle-item">开发者信任品牌独立性</div>
      <div class="battle-item">OpenAI、微软均有接触机会</div>
      <div class="battle-item">开源生态分散竞争</div>
    </div>
    <div class="battle-vs">VS</div>
    <div class="battle-side battle-right">
      <h3>🟢 收购后</h3>
      <div class="battle-item">英伟达掌控开源AI分发枢纽</div>
      <div class="battle-item">竞争对手GPU面临生态挤压</div>
      <div class="battle-item">平台中立性面临根本性考验</div>
      <div class="battle-item">Nemotron自有模型+平台流量</div>
      <div class="battle-item">从芯片到生态的全栈帝国</div>
    </div>
  </div>

  <div class="quote-block">
    <p class="quote-text">"黄仁勋买的不是一家SaaS公司的收入，是一个生态的入口。模型再厉害，开发者找不到、用不上，等于零。Hugging Face掌握的，就是开源模型从实验室到开发者手里的那最后一公里。"</p>
    <p class="quote-author">—— <strong>钛媒体</strong> · 2026.08.31</p>
  </div>
</section>

<!-- ═══════════════ CHAPTER 4: DATA DEEP DIVE ═══════════════ -->
<section id="chapter4" class="reveal">
  <div class="section-label">📊 CHAPTER 04</div>
  <h2 class="section-title">数据透视：权力的量化</h2>
  <p class="section-desc">用数据丈量AI权力的规模、速度与方向</p>

  <div class="metrics-row">
    <div class="metric-card"><div class="mc-val mc-green">$5.14T</div><div class="mc-label">英伟达市值（全球第一）</div></div>
    <div class="metric-card"><div class="mc-val mc-blue">$216B</div><div class="mc-label">FY2026年营收（+65%）</div></div>
    <div class="metric-card"><div class="mc-val mc-gold">90%+</div><div class="mc-label">AI训练GPU市场份额</div></div>
    <div class="metric-card"><div class="mc-val mc-red">$1T</div><div class="mc-label">芯片需求积压订单</div></div>
  </div>

  <div class="chart-row">
    <div class="chart-box">
      <h3>🏢 全球AI企业估值排行</h3>
      <p class="chart-sub">2026年7月 · 单位：十亿美元</p>
      <canvas id="chartValuation"></canvas>
    </div>
    <div class="chart-box">
      <h3>💰 Hugging Face 估值演变</h3>
      <p class="chart-sub">从创立到被收购的估值跃迁</p>
      <canvas id="chartHFEvolution"></canvas>
    </div>
  </div>

  <div class="chart-row">
    <div class="chart-box">
      <h3>⚡ 全球AI GPU市场份额（2026）</h3>
      <p class="chart-sub">训练侧 · 数据中心GPU收入占比</p>
      <canvas id="chartGPUMarket"></canvas>
    </div>
    <div class="chart-box">
      <h3>🇨🇳 中国AI加速卡市场格局</h3>
      <p class="chart-sub">2026年Q1 · 出口管制后的格局巨变</p>
      <canvas id="chartChinaMarket"></canvas>
    </div>
  </div>

  <div class="chart-box" style="margin-bottom:48px">
    <h3>📈 全球AI投资浪潮（2020-2026）</h3>
    <p class="chart-sub">千亿美元级资本狂潮 · 单位：十亿美元</p>
    <canvas id="chartAIFunding" style="height:300px"></canvas>
  </div>
</section>

<!-- ═══════════════ CHAPTER 5: POWER ARCHITECTURE ═══════════════ -->
<section id="chapter5" class="reveal">
  <div class="section-label">🏗️ CHAPTER 05</div>
  <h2 class="section-title">AI权力架构：四层金字塔</h2>
  <p class="section-desc">从芯片到应用，AI产业的权力如何层层传导</p>

  <div class="flow-container" style="flex-direction:column;gap:20px;align-items:stretch;max-width:800px;margin:0 auto 48px">
    <div style="display:flex;justify-content:center">
      <div class="flow-node" style="min-width:300px;border-color:rgba(255,215,0,0.3);background:linear-gradient(135deg,rgba(255,215,0,0.08),var(--bg-card))"><div class="fn-icon">👑</div><div class="fn-title" style="font-size:16px">智能层 · Foundation Models</div><div class="fn-sub" style="font-size:13px">Anthropic $965B · OpenAI $852B · DeepSeek $82B<br>Meta Llama · Mistral · 智谱 · 月之暗面</div></div>
    </div>
    <div style="text-align:center;font-size:24px;color:var(--nvidia-green)">↕</div>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap">
      <div class="flow-node" style="border-color:rgba(0,191,255,0.3);background:linear-gradient(135deg,rgba(0,191,255,0.08),var(--bg-card))"><div class="fn-icon">🔗</div><div class="fn-title">分发层 · Distribution</div><div class="fn-sub">Hugging Face ★被英伟达收购★<br>OpenRouter · 各大云平台</div></div>
      <div class="flow-node" style="border-color:rgba(0,191,255,0.3);background:linear-gradient(135deg,rgba(0,191,255,0.08),var(--bg-card))"><div class="fn-icon">☁️</div><div class="fn-title">平台层 · Hyperscalers</div><div class="fn-sub">Microsoft Azure · AWS · Google Cloud<br>CoreWeave · Nscale</div></div>
    </div>
    <div style="text-align:center;font-size:24px;color:var(--nvidia-green)">↕</div>
    <div style="display:flex;justify-content:center">
      