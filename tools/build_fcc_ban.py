#!/usr/bin/env python3
"""Build FCC China Robot Ban interactive HTML experience."""

import os

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "2026-08-18-fcc-china-robot-ban.html")

# ─── CSS ───
CSS = r"""
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#000;--bg2:#08080c;--bg3:#111118;--bg4:#1a1a24;
  --blue:#0071e3;--blue-g:rgba(0,113,227,.25);
  --red:#ff3b30;--red-g:rgba(255,59,48,.2);
  --green:#30d158;--amber:#ff9f0a;
  --t1:#f5f5f7;--t2:#86868b;--t3:#48484a;
}
html{scroll-behavior:smooth}
body{font-family:-apple-system,'SF Pro Text','Helvetica Neue',sans-serif;background:var(--bg);color:var(--t1);line-height:1.47;-webkit-font-smoothing:antialiased;overflow-x:hidden}
::selection{background:var(--blue);color:#fff}

/* grid */
.grid{position:fixed;inset:0;z-index:0;pointer-events:none;\n  background-image:linear-gradient(rgba(0,113,227,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(0,113,227,.025) 1px,transparent 1px);\n  background-size:60px 60px}

/* hero */
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:80px 24px;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;\n  background:radial-gradient(ellipse at 50% 40%,rgba(255,59,48,.07) 0%,transparent 60%),radial-gradient(ellipse at 30% 70%,rgba(0,113,227,.05) 0%,transparent 50%);z-index:1}
.hero-date{font-family:'SF Mono',monospace;font-size:13px;letter-spacing:.15em;color:var(--red);text-transform:uppercase;margin-bottom:24px;z-index:2;opacity:0;transform:translateY(20px)}
.hero h1{font-weight:700;font-size:clamp(36px,6vw,72px);line-height:1.05;letter-spacing:-.03em;max-width:900px;z-index:2;opacity:0;transform:translateY(40px)}
.hero h1 .r{color:var(--red)}.hero h1 .b{color:var(--blue)}
.hero-sub{font-size:clamp(16px,2.2vw,22px);color:var(--t2);max-width:640px;margin-top:28px;z-index:2;opacity:0;transform:translateY(30px)}
.hero-stat{display:flex;gap:40px;margin-top:48px;z-index:2;opacity:0;transform:translateY(20px)}
.hero-stat-item{text-align:center}
.hero-stat-num{font-size:clamp(28px,4vw,48px);font-weight:700;letter-spacing:-.02em}
.hero-stat-label{font-size:12px;color:var(--t2);letter-spacing:.1em;margin-top:4px}
.scroll-hint{position:absolute;bottom:40px;z-index:2;display:flex;flex-direction:column;align-items:center;gap:8px;opacity:0;animation:fadeUp 1s 2.5s forwards}
.scroll-hint span{font-size:11px;color:var(--t3);letter-spacing:.25em}
.scroll-hint .arr{width:20px;height:20px;border-right:1.5px solid var(--t3);border-bottom:1.5px solid var(--t3);transform:rotate(45deg);animation:bounce 2s infinite}
@keyframes bounce{0%,100%{transform:rotate(45deg) translateY(0)}50%{transform:rotate(45deg) translateY(8px)}}
@keyframes fadeUp{to{opacity:1;transform:translateY(0)}}

/* sections */
.sec{position:relative;z-index:1;padding:100px 24px}
.sec-in{max-width:1080px;margin:0 auto}
.sec-label{font-family:'SF Mono',monospace;font-size:12px;letter-spacing:.2em;color:var(--blue);text-transform:uppercase;margin-bottom:12px}
.sec-title{font-weight:700;font-size:clamp(28px,4vw,44px);line-height:1.1;letter-spacing:-.02em;margin-bottom:20px}
.sec-desc{color:var(--t2);font-size:17px;max-width:640px}

/* chapters */
.ch{padding:120px 24px;position:relative;z-index:1}
.ch-in{max-width:980px;margin:0 auto}
.ch-num{font-family:'SF Mono',monospace;font-size:11px;color:var(--t3);letter-spacing:.3em;margin-bottom:16px}
.ch h2{font-weight:700;font-size:clamp(24px,3.5vw,40px);line-height:1.12;letter-spacing:-.02em;margin-bottom:24px}
.ch-body{color:var(--t2);font-size:17px;line-height:1.65;max-width:680px}
.ch-body p+p{margin-top:16px}
.ch-quote{border-left:3px solid var(--red);padding:20px 24px;margin:28px 0;background:rgba(255,59,48,.04);border-radius:0 8px 8px 0}
.ch-quote p{font-size:16px;color:var(--t1);font-style:italic;line-height:1.6}
.ch-quote cite{display:block;margin-top:8px;font-size:13px;color:var(--t2);font-style:normal}

/* timeline */
.tl-box{position:relative;padding:100px 24px 120px;z-index:1;overflow:hidden}
.tl-track{position:relative;margin-top:60px;padding-left:48px}
.tl-track::before{content:'';position:absolute;left:18px;top:0;bottom:0;width:2px;background:linear-gradient(to bottom,var(--blue),var(--red))}
.tl-node{position:relative;margin-bottom:48px;padding:28px 32px;background:var(--bg3);border-radius:14px;cursor:pointer;transition:all .4s cubic-bezier(.16,1,.3,1);border:1px solid rgba(255,255,255,.04);opacity:0;transform:translateX(-30px)}
.tl-node::before{content:'';position:absolute;left:-38px;top:32px;width:14px;height:14px;border-radius:50%;background:var(--blue);border:3px solid var(--bg);transition:all .3s}
.tl-node.hl::before{background:var(--red);box-shadow:0 0 16px var(--red-g)}
.tl-node:hover{transform:translateX(6px);background:var(--bg4);border-color:rgba(0,113,227,.15)}
.tl-year{font-family:'SF Mono',monospace;font-size:13px;color:var(--blue);letter-spacing:.1em;margin-bottom:6px}
.tl-node.hl .tl-year{color:var(--red)}
.tl-title{font-weight:600;font-size:19px;margin-bottom:8px;line-height:1.3}
.tl-detail{color:var(--t2);font-size:15px;line-height:1.55;max-height:0;overflow:hidden;transition:max-height .5s cubic-bezier(.16,1,.3,1),opacity .4s;opacity:0}
.tl-node.expanded .tl-detail{max-height:400px;opacity:1;margin-top:14px}
.tl-tag{display:inline-block;font-size:11px;padding:3px 10px;border-radius:20px;font-family:'SF Mono',monospace;letter-spacing:.05em;margin-right:6px;margin-top:8px}
.tag-chip{background:rgba(0,113,227,.12);color:var(--blue)}
.tag-5g{background:rgba(48,209,88,.12);color:var(--green)}
.tag-robot{background:rgba(255,59,48,.12);color:var(--red)}
.tag-ai{background:rgba(255,159,10,.12);color:var(--amber)}

/* compare */
.cmp-wrap{max-width:920px;margin:60px auto 0;position:relative;border-radius:16px;overflow:hidden;aspect-ratio:16/10;background:var(--bg3)}
.cmp-side{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:48px;overflow:hidden}
.cmp-before{clip-path:inset(0 50% 0 0);z-index:2;background:linear-gradient(135deg,#0a1a0a,#0d120d)}
.cmp-after{z-index:1;background:linear-gradient(135deg,#1a0a0a,#120d0d)}
.cmp-label{position:absolute;top:20px;padding:6px 16px;border-radius:20px;font-family:'SF Mono',monospace;font-size:12px;letter-spacing:.1em;z-index:3}
.cmp-before .cmp-label{left:20px;background:var(--green);color:#000}
.cmp-after .cmp-label{right:20px;background:var(--red);color:#fff}
.cmp-side h3{font-size:22px;font-weight:600;margin-bottom:20px}
.cmp-item{display:flex;align-items:center;gap:12px;margin-bottom:14px;font-size:15px;color:var(--t2)}
.cmp-item .d{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.d-g{background:var(--green)}.d-r{background:var(--red)}.d-a{background:var(--amber)}
.cmp-slider{position:absolute;top:0;bottom:0;width:4px;background:#fff;z-index:10;cursor:ew-resize;left:50%;transform:translateX(-50%);box-shadow:0 0 20px rgba(255,255,255,.2)}
.cmp-slider::after{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:36px;height:36px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center}
.cmp-slider .handle{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:40px;height:40px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;color:#000;box-shadow:0 2px 12px rgba(0,0,0,.3)}

/* dashboard */
.dash-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin-top:48px}
.dash-card{background:var(--bg3);border-radius:12px;padding:28px 24px;border:1px solid rgba(255,255,255,.04);transition:all .3s cubic-bezier(.16,1,.3,1);opacity:0;transform:translateY(30px)}
.dash-card:hover{border-color:rgba(0,113,227,.2);transform:translateY(-2px)}
.dash-num{font-weight:700;font-size:clamp(32px,4vw,48px);line-height:1;letter-spacing:-.02em;margin-bottom:8px}
.dash-num.r{color:var(--red)}.dash-num.b{color:var(--blue)}.dash-num.g{color:var(--green)}.dash-num.a{color:var(--amber)}
.dash-label{font-size:14px;color:var(--t2);margin-bottom:4px}
.dash-delta{font-family:'SF Mono',monospace;font-size:12px}
.dash-delta.up{color:var(--red)}.dash-delta.dn{color:var(--green)}

/* bar chart */
.bar-chart{margin-top:56px;max-width:800px;margin-left:auto;margin-right:auto}
.bar-title{font-size:15px;color:var(--t2);margin-bottom:28px}
.bar-row{display:flex;align-items:center;gap:16px;margin-bottom:16px}
.bar-label{width:80px;font-size:14px;color:var(--t2);text-align:right;flex-shrink:0}
.bar-track{flex:1;height:36px;background:rgba(255,255,255,.03);border-radius:8px;position:relative;overflow:hidden}
.bar-fill{height:100%;border-radius:8px;display:flex;align-items:center;padding-left:14px;font-family:'SF Mono',monospace;font-size:13px;font-weight:600;color:#fff;transition:width 1.8s cubic-bezier(.16,1,.3,1);width:0}
.bar-fill.us{background:linear-gradient(90deg,rgba(0,113,227,.6),var(--blue))}
.bar-fill.cn{background:linear-gradient(90deg,rgba(255,59,48,.6),var(--red))}

/* line chart */
.line-chart{margin-top:56px;max-width:800px;margin-left:auto;margin-right:auto}
.line-chart svg{width:100%;height:auto}

/* impact */
.imp-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;margin-top:48px}
.imp-card{background:var(--bg3);border-radius:12px;padding:32px 28px;border:1px solid rgba(255,255,255,.04);transition:all .3s;opacity:0;transform:translateY(30px)}
.imp-card:hover{border-color:rgba(255,59,48,.2);transform:translateY(-2px)}
.imp-icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:16px}
.imp-card h4{font-size:18px;font-weight:600;margin-bottom:10px}
.imp-card p{font-size:14px;color:var(--t2);line-height:1.65}

/* escalation panel */
.esc-panel{margin-top:56px;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}
.esc-card{background:var(--bg3);border-radius:12px;padding:24px;text-align:center;border:1px solid rgba(255,255,255,.04);opacity:0;transform:translateY(20px);transition:all .3s}
.esc-card:hover{border-color:rgba(0,113,227,.2)}
.esc-step{font-family:'SF Mono',monospace;font-size:11px;color:var(--blue);letter-spacing:.15em;margin-bottom:12px}
.esc-card h5{font-size:16px;font-weight:600;margin-bottom:8px}
.esc-card p{font-size:13px;color:var(--t2);line-height:1.5}

/* closing */
.closing{padding:160px 24px;text-align:center;position:relative;z-index:1;background:linear-gradient(to bottom,var(--bg),#050510)}
.closing h2{font-weight:700;font-size:clamp(28px,4vw,48px);line-height:1.15;max-width:700px;margin:0 auto 28px;letter-spacing:-.02em}
.closing p{color:var(--t2);font-size:17px;max-width:560px;margin:0 auto}
.closing-line{width:60px;height:2px;background:var(--red);margin:40px auto 0}
.footer{padding:40px 24px;text-align:center;border-top:1px solid rgba(255,255,255,.04)}
.footer p{font-size:12px;color:var(--t3)}

/* particles canvas */
#particles{position:fixed;inset:0;z-index:0;pointer-events:none}

/* tooltip */
.tooltip{position:fixed;z-index:100;padding:10px 16px;background:var(--bg4);border:1px solid rgba(255,255,255,.1);border-radius:8px;font-size:13px;color:var(--t1);pointer-events:none;opacity:0;transition:opacity .2s;max-width:280px;box-shadow:0 8px 32px rgba(0,0,0,.4)}

/* nav dots */
.nav-dots{position:fixed;right:24px;top:50%;transform:translateY(-50%);z-index:50;display:flex;flex-direction:column;gap:12px}
.nav-dot{width:10px;height:10px;border-radius:50%;background:var(--t3);cursor:pointer;transition:all .3s;border:none;padding:0}
.nav-dot.active{background:var(--blue);box-shadow:0 0 8px var(--blue-g)}
.nav-dot:hover{background:var(--t2)}

@media(max-width:640px){
  .cmp-side{padding:24px}.cmp-side h3{font-size:18px}
  .tl-track{padding-left:36px}
  .dash-grid{grid-template-columns:1fr 1fr}
  .hero-stat{flex-wrap:wrap;gap:24px}
  .nav-dots{display:none}
}
"""

# ─── HTML Body ───
BODY = r"""
<div class="grid"></div>
<canvas id="particles"></canvas>

<!-- HERO -->
<section class="hero" data-sec="0">
  <div class="hero-date" id="heroDate">2026年7月28日 · FCC 受管制清单更新</div>
  <h1 id="heroTitle">技术脱钩<br>从<span class="b">芯片禁令</span>蔓延到<br><span class="r">实体设备</span></h1>
  <p class="hero-sub" id="heroSub">当美国联邦通信委员会将中国人形机器人列入受管制清单，一场始于半导体的科技冷战，正式蔓延到物理世界。</p>
  <div class="hero-stat" id="heroStat">
    <div class="hero-stat-item"><div class="hero-stat-num" style="color:var(--red)">7年</div><div class="hero-stat-label">脱钩持续时间</div></div>
    <div class="hero-stat-item"><div class="hero-stat-num" style="color:var(--blue)">4大领域</div><div class="hero-stat-label">被禁技术方向</div></div>
    <div class="hero-stat-item"><div class="hero-stat-num" style="color:var(--amber)">80亿$</div><div class="hero-stat-label">2026机器人市场</div></div>
  </div>
  <div class="scroll-hint"><span>SCROLL TO EXPLORE</span><div class="arr"></div></div>
</section>

<!-- CHAPTER 1 -->
<section class="ch" data-sec="1">
  <div class="ch-in">
    <div class="ch-num">01 — 导火索</div>
    <h2>FCC 封杀令：<span style="color:var(--red)">「先进机器人设备」</span>进入受管制清单</h2>
    <div class="ch-body">
      <p>2026年7月28日，美国联邦通信委员会（FCC）更新其《受管制清单》（Covered List），新增两类设备：<strong>「先进机器人设备」</strong>——明确定义为人形机器人和四足机器人——以及外国生产的联网电力逆变器。</p>
      <p>宇树科技被直接点名。路透社、BBC 在标题中直写：「美国禁止进口中国人形机器人」。这不是一次普通的贸易限制——它复刻了2018年芯片战初期针对中兴、华为的策略路径。</p>
      <p>FCC 设立了<strong>1年审查期</strong>：期满未通过安全审查的设备，将自动列入永久禁令。商务部同步筹划反补贴关税、高端算力芯片出口许可、仿真软件封锁、外资审查阻断投融资的「立体封锁网」。</p>
    </div>
    <div class="ch-quote">
      <p>「它没写中国名字。但所有人都清楚，谁是这个品类最大的供应方。」</p>
      <cite>—— 路透社报道，2026年7月28日</cite>
    </div>
  </div>
</section>

<!-- TIMELINE -->
<section class="tl-box sec" data-sec="2" id="timeline">
  <div class="sec-in">
    <div class="sec-label">INTERACTIVE TIMELINE</div>
    <div class="sec-title">脱钩演变史</div>
    <div class="sec-desc">从芯片到5G，从机器人到AI——点击节点探索每个阶段的详细信息</div>
    <div class="tl-track" id="tlTrack">
      <div class="tl-node" data-year="2018">
        <div class="tl-year">2018年4月</div>
        <div class="tl-title">中兴通讯遭全面制裁</div>
        <div class="tl-detail">美国商务部以中兴违反制裁规定为由，禁止美国企业向中兴出售零部件，中兴一度面临停产危机。这是中美科技脱钩的第一枪——芯片禁令从「精准打击」开始。</div>
        <span class="tl-tag tag-chip">芯片</span>
      </div>
      <div class="tl-node" data-year="2019">
        <div class="tl-year">2019年5月</div>
        <div class="tl-title">华为被列入实体清单</div>
        <div class="tl-detail">华为及68家关联公司被列入商务部实体清单。谷歌暂停华为 Android 授权，芯片供应链断裂。华为被迫启动「备胎计划」，海思芯片转正。全球5G建设遭遇地缘政治干扰。</div>
        <span class="tl-tag tag-chip">芯片</span><span class="tl-tag tag-5g">5G</span>
      </div>
      <div class="tl-node" data-year="2020">
        <div class="tl-year">2020年8月</div>
        <div class="tl-title">5G 设备全面禁令</div>
        <div class="tl-detail">FCC 禁止美国运营商使用联邦补贴资金采购华为、中兴5G设备。随后发布「拆除与替换」计划，拨款19亿美元拆除已部署的中国5G设备。技术脱钩从芯片蔓延到通信基础设施。</div>
        <span class="tl-tag tag-5g">5G</span>
      </div>
      <div class="tl-node" data-year="2022">
        <div class="tl-year">2022年10月</div>
        <div class="tl-title">芯片出口管制全面升级</div>
        <div class="tl-detail">美国商务部发布全面芯片出口管制规则，限制向中国出口先进制程芯片（14nm以下）及制造设备。荷兰ASML、日本东京电子等盟国企业被要求同步限制出口。芯片战从双边升级为多边围堵。</div>
        <span class="tl-tag tag-chip">芯片</span><span class="tl-tag tag-ai">AI</span>
      </div>
      <div class="tl-node" data-year="2023">
        <div class="tl-year">2023年1月</div>
        <div class="tl-title">CHIPS 法案正式实施</div>
        <div class="tl-detail">《芯片与科学法案》生效，拨款527亿美元扶持美国本土半导体制造。法案附带「护栏条款」：接受补贴的企业10年内不得在中国扩大先进芯片产能。全球芯片供应链加速「去中国化」。</div>
        <span class="tl-tag tag-chip">芯片</span>
      </div>
      <div class="tl-node" data-year="2025">
        <div class="tl-year">2025年5月</div>
        <div class="tl-title">比尔·盖茨：禁令适得其反</div>
        <div class="tl-detail">微软联合创始人比尔·盖茨在 CNN 采访中直言：「美国的科技禁令迫使中国在芯片制造等领域全力冲刺。我们清楚告诉他们需要自己造芯片，他们正在取得巨大进展。」中国IC出口2024年前11个月达1.03万亿元，同比增长20.3%。</div>
        <span class="tl-tag tag-chip">芯片</span><span class="tl-tag tag-ai">AI</span>
      </div>
      <div class="tl-node hl" data-year="2026">
        <div class="tl-year">2026年7月28日</div>
        <div class="tl-title">FCC 封杀中国人形机器人</div>
        <div class="tl-detail">FCC 更新受管制清单，将人形机器人、四足机器人、联网电力逆变器纳入管控。宇树科技被直接点名。商务部同步筹划反补贴关税 + 算力芯片出口许可 + 仿真软件封锁 + 外资审查的「立体封锁网」。技术脱钩正式从数字世界蔓延到「实体设备」。</div>
        <span class="tl-tag tag-robot">机器人</span><span class="tl-tag tag-ai">AI</span>
      </div>
    </div>
  </div>
</section>

<!-- A/B COMPARISON -->
<section class="sec" data-sec="3" id="compare">
  <div class="sec-in">
    <div class="sec-label">A / B COMPARISON</div>
    <div class="sec-title">脱钩前 vs 脱钩后</div>
    <div class="sec-desc">拖动滑块，对比产业链的剧变</div>
    <div class="cmp-wrap" id="cmpWrap">
      <div class="cmp-side cmp-before">
        <div class="cmp-label">脱钩前</div>
        <h3>全球协作时代</h3>
        <div class="cmp-item"><span class="d d-g"></span>芯片：台积电代工，全球分工体系</div>
        <div class="cmp-item"><span class="d d-g"></span>5G：华为设备覆盖170+国家</div>
        <div class="cmp-item"><span class="d d-g"></span>机器人：中国占全球产能70%+</div>
        <div class="cmp-item"><span class="d d-g"></span>AI：开源模型全球共享</div>
        <div class="cmp-item"><span class="d d-g"></span>供应链：中美双向深度绑定</div>
      </div>
      <div class="cmp-side cmp-after">
        <div class="cmp-label">脱钩后</div>
        <h3>区域割裂时代</h3>
        <div class="cmp-item"><span class="d d-r"></span>芯片：美国本土制造回流</div>
        <div class="cmp-item"><span class="d d-r"></span>5G：华为设备被盟国拆除</div>
        <div class="cmp-item"><span class="d d-r"></span>机器人：中国产品被禁止进口</div>
        <div class="cmp-item"><span class="d d-a"></span>AI：开源共享受出口管制约束</div>
        <div class="cmp-item"><span class="d d-r"></span>供应链：「友岸外包」重构</div>
      </div>
      <div class="cmp-slider" id="cmpSlider"><div class="handle">◀▶</div></div>
    </div>
  </div>
</section>

<!-- DATA DASHBOARD -->
<section class="sec" data-sec="4" id="dashboard">
  <div class="sec-in">
    <div class="sec-label">DATA DASHBOARD</div>
    <div class="sec-title">脱钩数据全景</div>
    <div class="dash-grid" id="dashGrid">
      <div class="dash-card"><div class="dash-num r" data-target="80" data-suffix="亿$">0</div><div class="dash-label">2026全球人形机器人市场</div><div class="dash-delta up">FCC禁令致中国出海受阻</div></div>
      <div class="dash-card"><div class="dash-num b" data-target="527" data-suffix="亿$">0</div><div class="dash-label">CHIPS法案拨款总额</div><div class="dash-delta up">美国本土半导体制造补贴</div></div>
      <div class="dash-card"><div class="dash-num g" data-target="1.03" data-suffix="万亿¥" data-decimal="1">0</div><div class="dash-label">2024年中国IC出口额</div><div class="dash-delta dn">同比增长20.3%，逆势增长</div></div>
      <div class="dash-card"><div class="dash-num a" data-target="19" data-suffix="亿$">0</div><div class="dash-label">拆除替换中国5G设备</div><div class="dash-delta up">覆盖全美运营商已部署设备</div></div>
      <div class="dash-card"><div class="dash-num r" data-target="1" data-suffix="年">0</div><div class="dash-label">FCC审查期</div><div class="dash-delta up">期满未通过即自动列入禁令</div></div>
      <div class="dash-card"><div class="dash-num b" data-target="6840" data-suffix="件">0</div><div class="dash-label">中国机器人专利申请(2024)</div><div class="dash-delta dn">全球第一，超美国2倍+</div></div>
    </div>
    <div class="bar-chart" id="barChart">
      <div class="bar-title">全球机器人专利申请量对比（2024年）</div>
      <div class="bar-row"><div class="bar-label">中国</div><div class="bar-track"><div class="bar-fill cn" data-width="82">6,840件</div></div></div>
      <div class="bar-row"><div class="bar-label">美国</div><div class="bar-track"><div class="bar-fill us" data-width="45">3,210件</div></div></div>
      <div class="bar-row"><div class="bar-label">日本</div><div class="bar-track"><div class="bar-fill us" data-width="28">2,050件</div></div></div>
      <div class="bar-row"><div class="bar-label">韩国</div><div class="bar-track"><div class="bar-fill us" data-width="15">1,120件</div></div></div>
      <div class="bar-row"><div class="bar-label">欧洲</div><div class="bar-track"><div class="bar-fill us" data-width="12">890件</div></div></div>
    </div>
    <!-- escalation path -->
    <div style="margin-top:64px">
      <div class="bar-title">技术脱钩升级路径：从芯片到实体设备</div>
      <div class="esc-panel" id="escPanel">
        <div class="esc-card"><div class="esc-step">STEP 01</div><h5>芯片禁令</h5><p>2018·中兴 → 华为<br>精准打击核心元器件</p></div>
        <div class="esc-card"><div class="esc-step">STEP 02</div><h5>5G封锁</h5><p>2020·设备禁令<br>通信基础设施脱钩</p></div>
        <div class="esc-card"><div class="esc-step">STEP 03</div><h5>多边围堵</h5><p>2022·ASML/日本<br>盟友联合管制</p></div>
        <div class="esc-card"><div class="esc-step">STEP 04</div><h5>实体设备</h5><p>2026·机器人禁令<br>蔓延到物理世界</p></div>
      </div>
    </div>
  </div>
</section>

<!-- CHAPTER 2 -->
<section class="ch" data-sec="5">
  <div class="ch-in">
    <div class="ch-num">02 — 多维冲击</div>
    <h2>当技术脱钩蔓延到<span style="color:var(--red)">「实体世界」</span></h2>
    <div class="ch-body">
      <p>芯片禁令影响的是计算能力，5G禁令影响的是通信网络——而机器人禁令，影响的是<strong>「物理世界的操作能力」</strong>。人形机器人集成了AI大脑、传感器感知、精密执行器和云端互联，是数字技术与物理世界的终极融合体。</p>
      <p>封杀机器人，意味着美国试图在「物理空间的智能化」这个赛道上，提前切断中国的竞争路径。但这真的是一个可以被「封杀」的目标吗？</p>
    </div>
  </div>
</section>

<!-- IMPACT -->
<section class="sec" data-sec="6" id="impact">
  <div class="sec-in">
    <div class="sec-label">IMPACT DIMENSIONS</div>
    <div class="sec-title">四维冲击</div>
    <div class="sec-desc">技术脱钩的涟漪效应，远不止贸易本身