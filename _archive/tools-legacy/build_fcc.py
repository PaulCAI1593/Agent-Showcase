#!/usr/bin/env python3
import os

OUT = '/app/working/shared/showcase/2026-08-18-fcc-china-robot-ban.html'

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>技术脱钩全景 | 从芯片禁令到机器人封杀</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#000;--bg2:#0a0a0f;--card:#111118;--card-h:#1a1a24;
  --blue:#0071e3;--blue-g:rgba(0,113,227,.3);
  --red:#ff3b30;--red-g:rgba(255,59,48,.25);
  --green:#30d158;--amber:#ff9f0a;
  --t1:#f5f5f7;--t2:#86868b;--t3:#48484a;
  --fd:-apple-system,'SF Pro Display','Helvetica Neue',sans-serif;
  --fb:-apple-system,'SF Pro Text','Helvetica Neue',sans-serif;
  --fm:'SF Mono','Fira Code',monospace
}
html{scroll-behavior:smooth}
body{font-family:var(--fb);background:var(--bg);color:var(--t1);line-height:1.47;\n  -webkit-font-smoothing:antialiased;overflow-x:hidden}
::selection{background:var(--blue);color:#fff}
.grid-bg{position:fixed;inset:0;z-index:0;pointer-events:none;\n  background-image:linear-gradient(rgba(0,113,227,.03) 1px,transparent 1px),\n  linear-gradient(90deg,rgba(0,113,227,.03) 1px,transparent 1px);\n  background-size:60px 60px}

/* HERO */
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;\n  justify-content:center;align-items:center;text-align:center;padding:80px 24px;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;\n  background:radial-gradient(ellipse at 50% 40%,rgba(255,59,48,.08) 0%,transparent 60%),\n  radial-gradient(ellipse at 30% 70%,rgba(0,113,227,.06) 0%,transparent 50%);z-index:1}
.hero-date{font-family:var(--fm);font-size:13px;letter-spacing:.15em;color:var(--red);\n  text-transform:uppercase;margin-bottom:24px;z-index:2;opacity:0;transform:translateY(20px)}
.hero h1{font-family:var(--fd);font-weight:700;font-size:clamp(36px,6vw,72px);\n  line-height:1.05;letter-spacing:-.03em;max-width:900px;z-index:2;\n  opacity:0;transform:translateY(40px)}
.hero h1 .ar{color:var(--red)}.hero h1 .ab{color:var(--blue)}
.hero-sub{font-size:clamp(16px,2.2vw,22px);color:var(--t2);max-width:640px;\n  margin-top:28px;z-index:2;opacity:0;transform:translateY(30px)}
.hero-scroll{position:absolute;bottom:40px;z-index:2;display:flex;\n  flex-direction:column;align-items:center;gap:8px;opacity:0;animation:fiu 1s 2s forwards}
.hero-scroll span{font-size:12px;color:var(--t3);letter-spacing:.2em}
.hero-scroll .arr{width:24px;height:24px;border-right:1.5px solid var(--t3);\n  border-bottom:1.5px solid var(--t3);transform:rotate(45deg);animation:bounce 2s infinite}
@keyframes bounce{0%,100%{transform:rotate(45deg) translateY(0)}50%{transform:rotate(45deg) translateY(8px)}}
@keyframes fiu{to{opacity:1;transform:translateY(0)}}

/* SECTIONS */
.sec{position:relative;z-index:1;padding:100px 24px}
.sec-in{max-width:1080px;margin:0 auto}
.sec-label{font-family:var(--fm);font-size:12px;letter-spacing:.2em;color:var(--blue);\n  text-transform:uppercase;margin-bottom:12px}
.sec-title{font-family:var(--fd);font-weight:600;font-size:clamp(28px,4vw,44px);\n  line-height:1.1;letter-spacing:-.02em;margin-bottom:20px}
.sec-desc{color:var(--t2);font-size:17px;max-width:640px}

/* CHAPTERS */
.ch{padding:120px 24px;position:relative;z-index:1}
.ch-in{max-width:980px;margin:0 auto}
.ch-num{font-family:var(--fm);font-size:11px;color:var(--t3);letter-spacing:.3em;margin-bottom:16px}
.ch h2{font-family:var(--fd);font-weight:700;font-size:clamp(24px,3.5vw,40px);\n  line-height:1.12;letter-spacing:-.02em;margin-bottom:24px}
.ch-body{color:var(--t2);font-size:17px;line-height:1.65;max-width:680px}
.ch-body p+p{margin-top:16px}

/* TIMELINE */
.tl-ct{position:relative;padding:100px 24px 120px;z-index:1;overflow:hidden}
.tl-track{position:relative;margin-top:60px;padding-left:40px}
.tl-track::before{content:'';position:absolute;left:15px;top:0;bottom:0;width:2px;\n  background:linear-gradient(to bottom,var(--blue),var(--red))}
.tl-node{position:relative;margin-bottom:48px;padding:24px 28px;background:var(--card);\n  border-radius:12px;cursor:pointer;transition:all .4s cubic-bezier(.16,1,.3,1);\n  border:1px solid rgba(255,255,255,.04);opacity:0;transform:translateX(-30px)}
.tl-node::before{content:'';position:absolute;left:-33px;top:28px;width:12px;height:12px;\n  border-radius:50%;background:var(--blue);border:2px solid var(--bg);transition:all .3s}
.tl-node.hl::before{background:var(--red);box-shadow:0 0 12px var(--red-g)}
.tl-node:hover{transform:translateX(4px);background:var(--card-h);border-color:rgba(0,113,227,.15)}
.tl-yr{font-family:var(--fm);font-size:13px;color:var(--blue);letter-spacing:.1em;margin-bottom:6px}
.tl-node.hl .tl-yr{color:var(--red)}
.tl-tt{font-weight:600;font-size:19px;margin-bottom:8px;line-height:1.3}
.tl-dt{color:var(--t2);font-size:15px;line-height:1.55;max-height:0;overflow:hidden;\n  transition:max-height .5s cubic-bezier(.16,1,.3,1),opacity .4s;opacity:0}
.tl-node.exp .tl-dt{max-height:300px;opacity:1;margin-top:12px}
.tl-tag{display:inline-block;font-size:11px;padding:3px 10px;border-radius:20px;\n  font-family:var(--fm);letter-spacing:.05em;margin-right:6px;margin-top:8px}
.tag-c{background:rgba(0,113,227,.12);color:var(--blue)}
.tag-g{background:rgba(48,209,88,.12);color:var(--green)}
.tag-r{background:rgba(255,59,48,.12);color:var(--red)}
.tag-a{background:rgba(255,159,10,.12);color:var(--amber)}

/* COMPARE */
.cmp-sec{padding:120px 24px;position:relative;z-index:1}
.cmp-wrap{max-width:900px;margin:60px auto 0;position:relative;border-radius:16px;\n  overflow:hidden;aspect-ratio:16/10;background:var(--card)}
.cmp-side{position:absolute;inset:0;display:flex;flex-direction:column;\n  justify-content:center;padding:48px;overflow:hidden}
.cmp-b{clip-path:inset(0 50% 0 0);z-index:2;background:#0d1a0d}
.cmp-a{z-index:1;background:#1a0d0d}
.cmp-lbl{position:absolute;top:20px;padding:6px 16px;border-radius:20px;\n  font-family:var(--fm);font-size:12px;letter-spacing:.1em;z-index:3}
.cmp-b .cmp-lbl{left:20px;background:var(--green);color:#000}
.cmp-a .cmp-lbl{right:20px;background:var(--red);color:#fff}
.cmp-side h3{font-size:22px;font-weight:600;margin-bottom:20px}
.cmp-item{display:flex;align-items:center;gap:12px;margin-bottom:14px;font-size:15px;color:var(--t2)}
.cmp-item .dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot-g{background:var(--green)}.dot-r{background:var(--red)}.dot-a{background:var(--amber)}
.cmp-slider{position:absolute;top:0;bottom:0;width:4px;background:var(--t1);z-index:10;\n  cursor:ew-resize;left:50%;transform:translateX(-50%);box-shadow:0 0 20px rgba(255,255,255,.2)}
.cmp-slider::after{content:'◀▶';position:absolute;top:50%;left:50%;\n  transform:translate(-50%,-50%);background:var(--t1);color:#000;font-size:11px;\n  padding:8px 6px;border-radius:8px;white-space:nowrap;letter-spacing:.1em}

/* DASHBOARD */
.dash{padding:100px 24px;position:relative;z-index:1}
.dash-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));\n  gap:20px;margin-top:48px;max-width:1080px;margin-left:auto;margin-right:auto}
.dash-card{background:var(--card);border-radius:12px;padding:28px 24px;\n  border:1px solid rgba(255,255,255,.04);transition:all .3s cubic-bezier(.16,1,.3,1);\n  opacity:0;transform:translateY(30px)}
.dash-card:hover{border-color:rgba(0,113,227,.2);transform:translateY(-2px)}
.dash-num{font-family:var(--fd);font-weight:700;font-size:clamp(32px,4vw,48px);\n  line-height:1;letter-spacing:-.02em;margin-bottom:8px}
.dash-num.red{color:var(--red)}.dash-num.blue{color:var(--blue)}
.dash-num.green{color:var(--green)}.dash-num.amber{color:var(--amber)}
.dash-lbl{font-size:14px;color:var(--t2);margin-bottom:4px}
.dash-dt{font-family:var(--fm);font-size:12px}
.dash-dt.up{color:var(--red)}.dash-dt.down{color:var(--green)}

/* BAR CHART */
.bar-ct{margin-top:48px;max-width:800px;margin-left:auto;margin-right:auto}
.bar-row{display:flex;align-items:center;gap:16px;margin-bottom:16px}
.bar-lbl{width:120px;font-size:14px;color:var(--t2);text-align:right;flex-shrink:0}
.bar-track{flex:1;height:32px;background:rgba(255,255,255,.03);border-radius:6px;position:relative;overflow:hidden}
.bar-fill{height:100%;border-radius:6px;display:flex;align-items:center;padding-left:12px;\n  font-family:var(--fm);font-size:13px;font-weight:600;transition:width 1.5s cubic-bezier(.16,1,.3,1);width:0}
.bar-fill.us{background:linear-gradient(90deg,rgba(0,113,227,.7),var(--blue))}
.bar-fill.cn{background:linear-gradient(90deg,rgba(255,59,48,.7),var(--red))}

/* IMPACT */
.imp-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));\n  gap:20px;margin-top:48px;max-width:1080px;margin-left:auto;margin-right:auto}
.imp-card{background:var(--card);border-radius:12px;padding:32px 28px;\n  border:1px solid rgba(255,255,255,.04);transition:all .3s;opacity:0;transform:translateY(30px)}
.imp-card:hover{border-color:rgba(255,59,48,.2)}
.imp-icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;\n  justify-content:center;font-size:24px;margin-bottom:16px}
.ii-g{background:rgba(255,59,48,.12)}.ii-u{background:rgba(0,113,227,.12)}
.ii-i{background:rgba(255,159,10,.12)}.ii-t{background:rgba(48,209,88,.12)}
.imp-card h4{font-size:18px;font-weight:600;margin-bottom:10px}
.imp-card p{font-size:14px;color:var(--t2);line-height:1.6}

/* CLOSING */
.close{padding:140px 24px;text-align:center;position:relative;z-index:1;\n  background:linear-gradient(to bottom,var(--bg),#050510)}
.close h2{font-family:var(--fd);font-weight:700;font-size:clamp(28px,4vw,48px);\n  line-height:1.15;max-width:700px;margin:0 auto 28px;letter-spacing:-.02em}
.close p{color:var(--t2);font-size:17px;max-width:560px;margin:0 auto}
.close-line{width:60px;height:2px;background:var(--red);margin:40px auto 0}

/* FOOTER */
.foot{padding:40px 24px;text-align:center;position:relative;z-index:1;\n  border-top:1px solid rgba(255,255,255,.04)}
.foot p{font-size:12px;color:var(--t3)}

/* RESPONSIVE */
@media(max-width:640px){.cmp-side{padding:24px}.cmp-side h3{font-size:18px}
  .tl-track{padding-left:32px}.dash-grid{grid-template-columns:1fr 1fr}}
</style>
</head>
<body>
<div class="grid-bg"></div>

<!-- HERO -->
<section class="hero" id="hero">
  <div class="hero-date" id="heroDate">2026年7月28日 · FCC 受管制清单更新</div>
  <h1 id="heroTitle">技术脱钩<br>从<span class="ab">芯片禁令</span>蔓延到<br><span class="ar">实体设备</span></h1>
  <p class="hero-sub" id="heroSub">当美国联邦通信委员会将中国人形机器人列入受管制清单，一场始于半导体的科技冷战，正式蔓延到「物理世界」。</p>
  <div class="hero-scroll"><span>SCROLL TO EXPLORE</span><div class="arr"></div></div>
</section>

<!-- CH1 -->
<section class="ch" id="ch1"><div class="ch-in">
  <div class="ch-num">01 — 导火索</div>
  <h2>FCC 封杀令：<span style="color:var(--red)">「先进机器人设备」</span>进入受管制清单</h2>
  <div class="ch-body">
    <p>2026年7月28日，美国联邦通信委员会（FCC）更新其《受管制清单》（Covered List），新增两类设备：「先进机器人设备」——明确定义为人形机器人和四足机器人——以及外国生产的联网电力逆变器。</p>
    <p>宇树科技被直接点名。路透社、BBC 在标题中直写：「美国禁止进口中国人形机器人」。这不是一次普通的贸易限制——它复刻了2018年芯片战初期针对中兴、华为的策略路径。</p>
    <p>FCC 设立了1年审查期：期满未通过安全审查的设备，将自动列入永久禁令。商务部同步筹划反补贴关税、高端算力芯片出口许可、仿真软件封锁、外资审查阻断投融资的「立体封锁网」。</p>
  </div>
</div></section>

<!-- TIMELINE -->
<section class="tl-ct sec" id="timeline">
  <div class="sec-in">
    <div class="sec-label">INTERACTIVE TIMELINE</div>
    <div class="sec-title">脱钩演变史</div>
    <div class="sec-desc">从芯片到5G，从机器人到AI——点击节点探索每个阶段的详细信息</div>
    <div class="tl-track" id="tlTrack">
      <div class="tl-node" data-year="2018">
        <div class="tl-yr">2018年4月</div>
        <div class="tl-tt">中兴通讯遭全面制裁</div>
        <div class="tl-dt">美国商务部以中兴违反制裁规定为由，禁止美国企业向中兴出售零部件，中兴一度面临停产危机。这是中美科技脱钩的第一枪。芯片禁令从「精准打击」开始。</div>
        <span class="tl-tag tag-c">芯片</span>
      </div>
      <div class="tl-node" data-year="2019">
        <div class="tl-yr">2019年5月</div>
        <div class="tl-tt">华为被列入实体清单</div>
        <div class="tl-dt">华为及68家关联公司被列入商务部实体清单。谷歌暂停华为 Android 授权，芯片供应链断裂。华为被迫启动「备胎计划」，海思芯片转正。全球5G建设遭遇地缘政治干扰。</div>
        <span class="tl-tag tag-c">芯片</span><span class="tl-tag tag-g">5G</span>
      </div>
      <div class="tl-node" data-year="2020">
        <div class="tl-yr">2020年8月</div>
        <div class="tl-tt">5G 设备全面禁令</div>
        <div class="tl-dt">FCC 禁止美国运营商使用联邦补贴资金采购华为、中兴5G设备。随后发布「拆除与替换」计划，拨款19亿美元拆除已部署的中国5G设备。技术脱钩从芯片蔓延到通信基础设施。</div>
        <span class="tl-tag tag-g">5G</span>
      </div>
      <div class="tl-node" data-year="2022">
        <div class="tl-yr">2022年10月</div>
        <div class="tl-tt">芯片出口管制升级</div>
        <div class="tl-dt">美国商务部发布全面芯片出口管制规则，限制向中国出口先进制程芯片（14nm以下）及制造设备。荷兰ASML、日本东京电子等盟国企业被要求同步限制出口。芯片战从双边升级为多边围堵。</div>
        <span class="tl-tag tag-c">芯片</span>
      </div>
      <div class="tl-node" data-year="2023">
        <div class="tl-yr">2023年1月</div>
        <div class="tl-tt">CHIPS 法案正式实施</div>
        <div class="tl-dt">《芯片与科学法案》生效，拨款527亿美元扶持美国本土半导体制造。法案附带「护栏条款」：接受补贴的企业10年内不得在中国扩大先进芯片产能。全球芯片供应链加速「去中国化」。</div>
        <span class="tl-tag tag-c">芯片</span><span class="tl-tag tag-a">AI</span>
      </div>
      <div class="tl-node" data-year="2025">
        <div class="tl-yr">2025年5月</div>
        <div class="tl-tt">比尔·盖茨：禁令适得其反</div>
        <div class="tl-dt">微软联合创始人比尔·盖茨在 CNN 采访中直言：「美国的科技禁令迫使中国在芯片制造等领域全力冲刺。我们清楚告诉他们需要自己造芯片，他们正在这方面取得巨大进展。」中国集成电路出口2024年前11个月达1.03万亿元，同比增长20.3%。</div>
        <span class="tl-tag tag-c">芯片</span><span class="tl-tag tag-a">AI</span>
      </div>
      <div class="tl-node hl" data-year="2026">
        <div class="tl-yr">2026年7月28日</div>
        <div class="tl-tt">FCC 封杀中国人形机器人</div>
        <div class="tl-dt">FCC 更新受管制清单，将人形机器人、四足机器人、联网电力逆变器纳入管控。宇树科技被直接点名。商务部同步筹划反补贴关税+算力芯片出口许可+仿真软件封锁+外资审查的「立体封锁网」。技术脱钩正式从数字世界蔓延到「实体设备」。</div>
        <span class="tl-tag tag-r">机器人</span><span class="tl-tag tag-a">AI</span>
      </div>
    </div>
  </div>
</section>

<!-- COMPARE -->
<section class="cmp-sec" id="compare"><div class="sec-in">
  <div class="sec-label">A / B COMPARISON</div>
  <div class="sec-title">脱钩前 vs 脱钩后</div>
  <div class="sec-desc">拖动滑块，对比产业链的变化</div>
  <div class="cmp-wrap" id="cmpWrap">
    <div class="cmp-side cmp-b">
      <div class="cmp-lbl">脱钩前</div>
      <h3>🌍 全球协作</h3>
      <div class="cmp-item"><span class="dot dot-g"></span>芯片：台积电代工，全球分工</div>
      <div class="cmp-item"><span class="dot dot-g"></span>5G：华为设备覆盖170+国家</div>
      <div class="cmp-item"><span class="dot dot-g"></span>机器人：中国占全球产能70%+</div>
      <div class="cmp-item"><span class="dot dot-g"></span>AI：开源模型全球共享</div>
      <div class="cmp-item"><span class="dot dot-g"></span>供应链：中美双向深度绑定</div>
    </div>
    <div class="cmp-side cmp-a">
      <div class="cmp-lbl">脱钩后</div>
      <h3>🔒 区域割裂</h3>
      <div class="cmp-item"><span class="dot dot-r"></span>芯片：美国本土制造回流</div>
      <div class="cmp-item"><span class="dot dot-r"></span>5G：华为设备被盟国拆除</div>
      <div class="cmp-item"><span class="dot dot-r"></span>机器人：中国产品被禁止进口</div>
      <div class="cmp-item"><span class="dot dot-a"></span>AI：开源共享受出口管制约束</div>
      <div class="cmp-item"><span class="dot dot-r"></span>供应链：「友岸外包」重构</div>
    </div>
    <div class="cmp-slider" id="cmpSlider"></div>
  </div>
</div></section>

<!-- DASHBOARD -->
<section class="dash" id="dashboard"><div class="sec-in">
  <div class="sec-label">DATA DASHBOARD</div>
  <div class="sec-title">脱钩数据全景</div>
  <div class="dash-grid" id="dashGrid">
    <div class="dash-card"><div class="dash-num red" data-target="80" data-suffix="亿$">0</div>
      <div class="dash-lbl">2026年全球人形机器人市场规模</div>
      <div class="dash-dt up">受FCC禁令影响，中国企业出海受阻</div></div>
    <div class="dash-card"><div class="dash-num blue" data-target="527" data-suffix="亿$">0</div>
      <div class="dash-lbl">CHIPS法案拨款总额</div>
      <div class="dash-dt up">美国本土半导体制造补贴</div></div>
    <div class="dash-card"><div class="dash-num green" data-target="1.03" data-suffix="万亿¥" data-decimal="1">0</div>
      <div class="dash-lbl">2024年中国IC出口额</div>
      <div class="dash-dt down">同比增长20.3%，逆势增长</div></div>
    <div class="dash-card"><div class="dash-num amber" data-target="19" data-suffix="亿$">0</div>
      <div class="dash-lbl">拆除替换中国5G设备拨款</div>
      <div class="dash-dt up">覆盖全美运营商已部署设备</div></div>
  </div>
  <div class="bar-ct" id="barChart">
    <div style="font-size:15px;color:var(--t2);margin-bottom:24px">全球机器人专利申请量对比（2024年）</div>
    <div class="bar-row"><div class="bar-lbl">中国</div><div class="bar-track"><div class="bar-fill cn" data-w="82">6,840件</div></div></div>
    <div class="bar-row"><div class="bar-lbl">美国</div><div class="bar-track"><div class="bar-fill us" data-w="45">3,210件</div></div></div>
    <div class="bar-row"><div class="bar-lbl">日本</div><div class="bar-track"><div class="bar-fill us" data-w="28">2,050件</div></div></div>
    <div class="bar-row"><div class="bar-lbl">韩国</div><div class="bar-track"><div class="bar-fill us" data-w="15">1,120件</div></div></div>
    <div class="bar-row"><div class="bar-lbl">欧洲</div><div class="bar-track"><div class="bar-fill us" data-w="12">890件</div></div></div>
  </div>
</div></section>

<!-- CH2 -->
<section class="ch" id="ch2"><div class="ch-in">
  <div class="ch-num">02 — 深层影响</div>
  <h2>当技术脱钩蔓延到<span style="color:var(--red)">「实体世界」</span></h2>
  <div class="ch-body">
    <p>芯片禁令影响的是计算能力，5G禁令影响的是通信网络——而机器人禁令，影响的是「物理世界的操作能力」。人形机器人集成了AI大脑、传感器感知、精密执行器和云端互联，是数字技术与物理世界的终极融合体。</p>
    <p>封杀机器人，意味着美国试图在「物理空间的智能化」这个赛道上，提前切断中国的竞争路径。</p>
  </div>
</div></section>

<!-- IMPACT -->
<section class="sec" id="impact"><div class="sec-in">
  <div class="sec-label">IMPACT DIMENSIONS</div>
  <div class="sec-title">四维冲击</div>
  <div class="sec-desc">技术脱钩的涟漪效应</div>
  <div class="imp-grid" id="impGrid">
    <div class="imp-card"><div class="imp-icon ii-g">🌍</div>
      <h4>地缘重构</h4><p>「友岸外包」重塑全球供应链。东南亚、印度成为替代制造基地，但短期内难以复制中国的产业集群效应。全球科技版图加速「两极化」。</p></div>
    <div class="imp-card"><div class="imp-icon ii-u">⚖️</div>
      <h4>治理博弈</h4><p>FCC以「国家安全」为由行使技术管辖权，开创了以通信监管机构管制实体设备的先例。WTO规则框架面临前所未有的挑战。</p></div>
    <div class="imp-card"><div class="imp-icon ii-i">🏭</div>
      <h4>产业震荡</h4><p>中国人形机器人企业出海受阻，但国内80亿美元市场空间依然巨大。宇树科技、优必选等加速国产替代和内需市场开拓。</p></div>
    <div class="imp-card"><div class="imp-icon ii-t">🤖</div>
      <h4>技术分化</h4><p>比尔·盖茨所言的「适得其反」正在应验。中国在芯片制造和机器人领域被迫加速自主化，开源AI生态面临分裂风险。</p></div>
  </div>
</div></section>

<!-- CH3 -->
<section class="ch" id="ch3"><div class="ch-in">
  <div class="ch-num">03 — 微观企业</div>
  <h2>被点名的<span style="color:var(--red)">「实体」</span></h2>
  <div class="ch-body">
    <p><strong>宇树科技</strong>（Unitree）：全球四足机器人领军企业，B2/W两款产品在消费级和工业级市场均有布局。被FCC直接点名，复刻了2019年华为被针对的路径——先限制市场准入，再切断供应链。</p>
    <p><strong>优必选</strong>（UBTECH）：中国人形机器人第一股，Walker系列已在制造业、物流场景落地。FCC禁令可能影响其北美市场拓展计划。</p>
    <p><strong>电力逆变器</strong>：阳光电源、华为数字能源等中国企业占全球逆变器市场60%+份额。联网逆变器被列入受管制清单，直接影响美国太阳能和储能产业。</p>
  </div>
</div></section>

<!-- CLOSING -->
<section class="close" id="closing">
  <h2>这不仅是贸易问题<br>更是<span style="color:var(--red)">全球科技秩序</span>的重构</h2>
  <p>从芯片到5G，从机器人到AI——技术脱钩正在重新定义「谁有权制造未来」。当物理设备也成为地缘博弈的棋子，我们面临的不仅是供应链重组，而是一个全新科技秩序的诞生。</p>
  <div class="close-line"></div>
</section>

<footer class="foot">
  <p>数据来源：FCC Covered List · Bloomberg · Reuters · BBC · 中国海关总署 · 比尔·盖茨 CNN 专访</p>
  <p style="margin-top:8px">最后更新：2026年8月18日 · 绘界 Creative Design</p>
</footer>

<!-- GSAP -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
gsap.registerPlugin(ScrollTrigger);

// Hero entrance
gsap.to('#heroDate',{opacity:1,y:0,duration:.8,delay:.3});
gsap.to('#heroTitle',{opacity:1,y:0,duration:1,delay:.6});
gsap.to('#heroSub',{opacity:1,y:0,duration:.8,delay:1});

// Timeline nodes
document.querySelectorAll('.tl-node').forEach(n=>{
  n.addEventListener('click',()=>n.classList.toggle('exp'));
  gsap.to(n,{opacity:1,x:0,duration:.6,scrollTrigger:{trigger:n,start:'top 85%'}});
});

// Compare slider
(function(){
  const wrap=document.getElementById('cmpWrap');
  const slider=document.getElementById('cmpSlider');
  const before=wrap.querySelector('.cmp-b');
  let dragging=false;
  function move(x){
    const r=wrap.getBoundingClientRect();
    let pct=((x-r.left)/r.width)*100;
    pct=Math.max(5,Math.min(95,pct));
    slider.style.left=pct+'%';
    before.style.clipPath='inset(0 '+(100-pct)+'% 0 0)';
  }
  slider.addEventListener('mousedown',()=>dragging=true);
  slider.addEventListener('touchstart',()=>dragging=true);
  window.addEventListener('mouseup',()=>dragging=false);
  window.addEventListener('touchend',()=>dragging=false);
  window.addEventListener('mousemove',e=>{if(dragging)move(e.clientX)});
  window.addEventListener('touchmove',e=>{if(dragging)move(e.touches[0].clientX)});
})();

// Dashboard numbers
function animateNum(el){
  const target=parseFloat(el.dataset.target);
  const suffix=el.dataset.suffix||'';
  const decimal=parseInt(el.dataset.decimal)||0;
  const obj={v:0};
  gsap.to(obj,{v:target,duration:2,ease:'power2.out',onUpdate:()=>{\n    el.textContent=decimal?obj.v.toFixed(decimal)+suffix:Math.round(obj.v)+suffix;\n  }});
}
document.querySelectorAll('.dash-num').forEach(n=>{
  ScrollTrigger.create({trigger:n,start:'top 85%',once:true