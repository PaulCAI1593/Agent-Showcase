#!/usr/bin/env python3
"""Part 3: JavaScript - Particles, Charts, Animations"""
OUT = '/app/working/shared/showcase/2026-08-11-capital-migration.html'

JS = r"""
<script>
// ═══════════════════════════════════════════
// PARTICLE BACKGROUND
// ═══════════════════════════════════════════
(function(){
const c=document.getElementById('bg'),x=c.getContext('2d');
let W,H,pts=[];
function resize(){W=c.width=innerWidth;H=c.height=innerHeight}
resize();window.addEventListener('resize',resize);
class P{
  constructor(){this.reset()}
  reset(){this.x=Math.random()*W;this.y=Math.random()*H;this.vx=(Math.random()-.5)*.3;this.vy=(Math.random()-.5)*.3;this.r=Math.random()*1.5+.5;this.a=Math.random()*.5+.1;this.gold=Math.random()>.6}
  update(){this.x+=this.vx;this.y+=this.vy;if(this.x<0||this.x>W)this.vx*=-1;if(this.y<0||this.y>H)this.vy*=-1}
  draw(){x.beginPath();x.arc(this.x,this.y,this.r,0,Math.PI*2);x.fillStyle=this.gold?`rgba(212,168,67,${this.a})`:`rgba(255,255,255,${this.a*.3})`;x.fill()}
}
for(let i=0;i<80;i++)pts.push(new P);
function loop(){x.clearRect(0,0,W,H);pts.forEach(p=>{p.update();p.draw()});
// connections
for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){
  const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);
  if(d<120){x.beginPath();x.moveTo(pts[i].x,pts[i].y);x.lineTo(pts[j].x,pts[j].y);x.strokeStyle=`rgba(212,168,67,${.08*(1-d/120)})`;x.stroke()}}
requestAnimationFrame(loop)}
loop();
})();

// ═══════════════════════════════════════════
// LOADING
// ═══════════════════════════════════════════
(function(){
let p=0;const bar=document.getElementById('ldBar');
const iv=setInterval(()=>{p+=Math.random()*15+5;if(p>100)p=100;bar.style.width=p+'%';if(p>=100){clearInterval(iv);setTimeout(()=>{document.getElementById('ld').classList.add('hide')},400)}},150);
})();

// ═══════════════════════════════════════════
// SCROLL REVEAL
// ═══════════════════════════════════════════
const obs=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('vis');
// Animate bars
e.target.querySelectorAll('.bk-bf[data-w]').forEach(b=>{setTimeout(()=>{b.style.width=b.dataset.w+'%'},200)});
e.target.querySelectorAll('.rbf[data-w]').forEach(b=>{setTimeout(()=>{b.style.width=b.dataset.w+'%'},200)});
}})},{threshold:.15});
document.querySelectorAll('.rv,.ti').forEach(el=>obs.observe(el));

// ═══════════════════════════════════════════
// NAV ACTIVE STATE
// ═══════════════════════════════════════════
const sections=['hero','gold','dxy','bank','rate','flow','end'];
const navLinks=document.querySelectorAll('.nav-links a');
window.addEventListener('scroll',()=>{
  const y=window.scrollY+100;
  sections.forEach((id,i)=>{
    const el=document.getElementById(id);
    if(el&&y>=el.offsetTop&&y<el.offsetTop+el.offsetHeight){
      navLinks.forEach(l=>l.classList.remove('on'));
      navLinks[i]&&navLinks[i].classList.add('on');
    }
  });
});

// ═══════════════════════════════════════════
// GOLD TIMELINE
// ═══════════════════════════════════════════
(function(){
const data=[
  {d:'2024年1月',p:'$2,050',n:'年初低位，市场观望'},
  {d:'2024年4月',p:'$2,400',n:'突破历史高位，央行购金推动'},
  {d:'2024年8月',p:'$2,500',n:'降息预期升温'},
  {d:'2025年3月',p:'$3,000',n:'突破$3,000里程碑'},
  {d:'2025年9月',p:'$3,500',n:'美联储重启降息'},
  {d:'2026年1月',p:'$3,800',n:'年初攻势凌厉'},
  {d:'2026年3月',p:'$4,000',n:'突破$4,000心理关口'},
  {d:'2026年7月',p:'$4,021',n:'短暂回撤，恐慌蔓延'},
  {d:'2026年8月7日',p:'$4,432',n:'COMEX突破$4,400！'},
];
const el=document.getElementById('goldTimeline');
data.forEach((d,i)=>{
  el.innerHTML+=`<div class="ti" style="transition-delay:${i*0.1}s"><div class="td"></div><div class="tc"><div class="t-date">${d.d}</div><div class="t-price">${d.p}</div><div class="t-note">${d.n}</div></div><div style="flex:1"></div></div>`;
});
})();

// ═══════════════════════════════════════════
// DXY CHART (Canvas-based)
// ═══════════════════════════════════════════
(function(){
const canvas=document.getElementById('dxyChart');
const ctx=canvas.getContext('2d');
const fullData=[
  {d:'2024-01',v:103.5},{d:'2024-03',v:104.5},{d:'2024-06',v:105.8},
  {d:'2024-09',v:106.5},{d:'2024-12',v:108.0},{d:'2025-03',v:104.5},
  {d:'2025-06',v:103.0},{d:'2025-09',v:101.5},{d:'2025-12',v:102.0},
  {d:'2026-01',v:101.5},{d:'2026-03',v:101.0},{d:'2026-06',v:100.8},
  {d:'2026-07',v:100.4},{d:'2026-07-30',v:99.97},{d:'2026-08-05',v:99.68},
  {d:'2026-08-07',v:99.54}
];

function draw(data){
  const dpr=window.devicePixelRatio||1;
  const rect=canvas.getBoundingClientRect();
  canvas.width=rect.width*dpr;canvas.height=300*dpr;
  ctx.scale(dpr,dpr);
  const W=rect.width,H=300,pad={t:30,r:30,b:40,l:50};
  const cW=W-pad.l-pad.r,cH=H-pad.t-pad.b;
  
  const vals=data.map(d=>d.v);
  const minV=Math.min(...vals)-1,maxV=Math.max(...vals)+1;
  const scaleX=i=>(i/(data.length-1))*cW+pad.l;
  const scaleY=v=>pad.t+cH-(v-minV)/(maxV-minV)*cH;
  
  // Grid
  ctx.strokeStyle='rgba(255,255,255,0.04)';ctx.lineWidth=1;
  for(let v=Math.ceil(minV);v<=maxV;v+=1){
    const y=scaleY(v);
    ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();
    ctx.fillStyle='rgba(255,255,255,0.3)';ctx.font='11px sans-serif';ctx.textAlign='right';
    ctx.fillText(v.toFixed(0),pad.l-8,y+4);
  }
  
  // 100 line
  const y100=scaleY(100);
  ctx.strokeStyle='rgba(255,71,87,0.5)';ctx.lineWidth=1.5;ctx.setLineDash([6,4]);
  ctx.beginPath();ctx.moveTo(pad.l,y100);ctx.lineTo(W-pad.r,y100);ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='rgba(255,71,87,0.7)';ctx.font='bold 11px sans-serif';ctx.textAlign='left';
  ctx.fillText('100 心理关口',W-pad.r-90,y100-6);
  
  // Area
  ctx.beginPath();ctx.moveTo(scaleX(0),scaleY(vals[0]));
  for(let i=1;i<data.length;i++){
    const cx=(scaleX(i-1)+scaleX(i))/2;
    ctx.bezierCurveTo(cx,scaleY(vals[i-1]),cx,scaleY(vals[i]),scaleX(i),scaleY(vals[i]));
  }
  ctx.lineTo(scaleX(data.length-1),pad.t+cH);ctx.lineTo(scaleX(0),pad.t+cH);ctx.closePath();
  const grad=ctx.createLinearGradient(0,pad.t,0,pad.t+cH);
  grad.addColorStop(0,'rgba(255,71,87,0.15)');grad.addColorStop(1,'rgba(255,71,87,0)');
  ctx.fillStyle=grad;ctx.fill();
  
  // Line
  ctx.beginPath();ctx.moveTo(scaleX(0),scaleY(vals[0]));
  for(let i=1;i<data.length;i++){
    const cx=(scaleX(i-1)+scaleX(i))/2;
    ctx.bezierCurveTo(cx,scaleY(vals[i-1]),cx,scaleY(vals[i]),scaleX(i),scaleY(vals[i]));
  }
  ctx.strokeStyle='var(--red)';ctx.lineWidth=2.5;ctx.stroke();
  
  // End dot
  const ex=scaleX(data.length-1),ey=scaleY(vals[data.length-1]);
  ctx.beginPath();ctx.arc(ex,ey,6,0,Math.PI*2);ctx.fillStyle='#FF4757';ctx.fill();
  ctx.beginPath();ctx.arc(ex,ey,12,0,Math.PI*2);ctx.fillStyle='rgba(255,71,87,0.2)';ctx.fill();
  ctx.fillStyle='#FF4757';ctx.font='bold 13px Georgia,serif';ctx.textAlign='right';
  ctx.fillText('99.54',ex-16,ey-10);
  
  // X labels
  ctx.fillStyle='rgba(255,255,255,0.35)';ctx.font='10px sans-serif';ctx.textAlign='center';
  const step=Math.max(1,Math.floor(data.length/6));
  for(let i=0;i<data.length;i+=step){
    ctx.fillText(data[i].d.replace('20',''),scaleX(i),H-pad.b+18);
  }
}

draw(fullData);
window.showDxy=function(range){
  document.querySelectorAll('.ch-tabs .ct').forEach(b=>b.classList.remove('on'));
  event.target.classList.add('on');
  let d=fullData;
  if(range==='1y')d=fullData.slice(5);
  else if(range==='6m')d=fullData.slice(9);
  draw(d);
};
window.addEventListener('resize',()=>draw(fullData));
})();

// ═══════════════════════════════════════════
// FLOW SVG ARROWS
// ═══════════════════════════════════════════
(function(){
const svg=document.getElementById('flowSvg');
const map=document.getElementById('flowMap');
if(!svg||!map)return;

function drawArrows(){
  svg.innerHTML='';
  const rect=map.getBoundingClientRect();
  svg.setAttribute('viewBox',`0 0 ${rect.width} ${rect.height}`);
  
  const sources=map.querySelectorAll('.fn');
  const froms=[0,1,2],tos=[3,4,5,6];
  
  froms.forEach(fi=>{
    const f=sources[fi];
    const fr=f.getBoundingClientRect();
    const fx=fr.left-rect.left+fr.width;
    const fy=fr.top-rect.top+fr.height/2;
    
    tos.forEach(ti=>{
      const t=sources[ti];
      const tr=t.getBoundingClientRect();
      const tx=tr.left-rect.left;
      const ty=tr.top-rect.top+tr.height/2;
      
      const mx=(fx+tx)/2;
      const path=document.createElementNS('http://www.w3.org/2000/svg','path');
      path.setAttribute('d',`M${fx},${fy} C${mx},${fy} ${mx},${ty} ${tx},${ty}`);
      path.setAttribute('fill','none');
      path.setAttribute('stroke',ti===3?'rgba(212,168,67,0.25)':'rgba(255,255,255,0.08)');
      path.setAttribute('stroke-width',ti===3?'2.5':'1.5');
      path.setAttribute('stroke-dasharray',ti===3?'none':'6,4');
      
      // Animated dash
      if(ti===3){
        const len=path.getTotalLength?200:200;
        path.setAttribute('stroke-dasharray',`${len}`);
        path.setAttribute('stroke-dashoffset',`${len}`);
        path.style.animation=`dashDraw 2s ${fi*0.3}s forwards`;
      }
      svg.appendChild(path);
      
      // Arrow head
      if(ti===3){
        const arrow=document.createElementNS('http://www.w3.org/2000/svg','circle');
        arrow.setAttribute('cx',tx);arrow.setAttribute('cy',ty);arrow.setAttribute('r','3');
        arrow.setAttribute('fill','rgba(212,168,67,0.5)');
        svg.appendChild(arrow);
      }
    });
  });
}

// Add animation style
const style=document.createElement('style');
style.textContent='@keyframes dashDraw{to{stroke-dashoffset:0}}';
document.head.appendChild(style);

setTimeout(drawArrows,500);
window.addEventListener('resize',()=>setTimeout(drawArrows,100));
})();

// ═══════════════════════════════════════════
// TOOLTIP
// ═══════════════════════════════════════════
(function(){
let tip=null;
document.addEventListener('mousemove',e=>{
  if(tip){tip.style.left=e.clientX+12+'px';tip.style.top=e.clientY-10+'px'}
});
document.querySelectorAll('[data-tip]').forEach(el=>{
  el.addEventListener('mouseenter',e=>{
    tip=document.createElement('div');
    tip.style.cssText='position:fixed;background:rgba(18,18,26,.95);border:1px solid rgba(212,168,67,.3);border-radius:8px;padding:10px 14px;font-size:12px;color:#F0F0F5;pointer-events:none;z-index:1000;max-width:260px;box-shadow:0 8px 32px rgba(0,0,0,.4);backdrop-filter:blur(10px);line-height:1.5';
    tip.textContent=el.dataset.tip;
    document.body.appendChild(tip);
    tip.style.left=e.clientX+12+'px';tip.style.top=e.clientY-10+'px';
  });
  el.addEventListener('mouseleave',()=>{if(tip){tip.remove();tip=null}});
});
})();
</script>
</body>
</html>
"""

with open(OUT, 'a', encoding='utf-8') as f:
    f.write(JS)
print("JavaScript written OK")
print("Dashboard complete!")
