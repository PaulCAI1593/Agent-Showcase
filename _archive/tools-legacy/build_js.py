#!/usr/bin/env python3
"""Generate the remaining JavaScript for the HTML file."""

js_content = r"""
// ========== ECOSYSTEM MAP ==========
(function(){
  var canvas = document.getElementById("ecoCanvas");
  if(!canvas) return;
  var ctx = canvas.getContext("2d");
  var w, h, nodes = [], hoveredNode = null;
  function resize(){
    w = canvas.width = canvas.offsetWidth * 2;
    h = canvas.height = canvas.offsetHeight * 2;
  }
  resize();
  window.addEventListener("resize", function(){ resize(); initNodes(); });
  
  var models = [
    {name:"Qwen3-235B", org:"Alibaba", size:60, color:"#e63946", x:0.25, y:0.3, downloads:"Flagship MoE", desc:"235B params, 22B active, #1 open source globally"},
    {name:"Qwen3.6-Plus", org:"Alibaba", size:50, color:"#e63946", x:0.18, y:0.45, downloads:"Coding King", desc:"#2 coding ability globally, 1.4T tokens/day"},
    {name:"Qwen3-32B", org:"Alibaba", size:35, color:"#e63946", x:0.32, y:0.2, downloads:"32B Dense", desc:"Lightweight high-perf, edge deployment"},
    {name:"Qwen3-8B", org:"Alibaba", size:28, color:"#e63946", x:0.15, y:0.25, downloads:"8B Dense", desc:"Edge device optimized"},
    {name:"DeepSeek-V4", org:"DeepSeek", size:55, color:"#4361ee", x:0.55, y:0.25, downloads:"1M Context", desc:"1M context window, leading Agent capability"},
    {name:"DS-V4-Flash", org:"DeepSeek", size:48, color:"#4361ee", x:0.65, y:0.4, downloads:"8.83T/wk", desc:"Weekly +570% WoW, fastest inference"},
    {name:"DeepSeek-R1", org:"DeepSeek", size:42, color:"#4361ee", x:0.5, y:0.45, downloads:"Reasoning", desc:"Ultra-low training cost, shocked the world"},
    {name:"DS-Prover-V2", org:"DeepSeek", size:30, color:"#4361ee", x:0.7, y:0.2, downloads:"Math Proofs", desc:"671B params, formal theorem proving"},
    {name:"GLM-4", org:"Zhipu AI", size:40, color:"#00d4ff", x:0.4, y:0.6, downloads:"1.5B+ DL", desc:"Chinese dialogue + tool calling, enterprise"},
    {name:"GLM-4V", org:"Zhipu AI", size:30, color:"#00d4ff", x:0.3, y:0.7, downloads:"Multimodal", desc:"Vision + Chinese generation"},
    {name:"MiMo-V2-Pro", org:"Xiaomi", size:38, color:"#ffd60a", x:0.75, y:0.55, downloads:"3.08T/wk", desc:"First model to hit 3T tokens/week"},
    {name:"MiniMax", org:"MiniMax", size:32, color:"#ffd60a", x:0.82, y:0.35, downloads:"Long Context", desc:"Long context + low-cost inference"},
    {name:"Kimi", org:"Moonshot", size:30, color:"#ffd60a", x:0.85, y:0.65, downloads:"Ultra-Long", desc:"Ultra-long document processing"},
    {name:"Yi", org:"01.AI", size:28, color:"#ffd60a", x:0.2, y:0.6, downloads:"Yi Series", desc:"Multilingual + multimodal"},
    {name:"Llama", org:"Meta", size:45, color:"#888888", x:0.8, y:0.15, downloads:"Overtaken", desc:"Former #1, now surpassed by Qwen"},
    {name:"Gemma", org:"Google", size:32, color:"#888888", x:0.9, y:0.25, downloads:"418M", desc:"Google open source series"},
    {name:"Mistral", org:"France", size:28, color:"#888888", x:0.88, y:0.45, downloads:"EU Strongest", desc:"European open source AI representative"}
  ];
  var connections = [[0,2],[0,3],[1,0],[4,5],[4,6],[4,7],[8,9],[10,11],[10,12],[0,14],[4,14],[6,14]];
  
  function initNodes(){
    nodes = models.map(function(m,i){
      return {name:m.name,org:m.org,size:m.size,color:m.color,downloads:m.downloads,desc:m.desc,
        px:m.x*w, py:m.y*h, index:i};
    });
  }
  initNodes();
  
  canvas.addEventListener("mousemove", function(e){
    var rect = canvas.getBoundingClientRect();
    var mx = (e.clientX - rect.left) * 2;
    var my = (e.clientY - rect.top) * 2;
    hoveredNode = null;
    for(var i=0;i<nodes.length;i++){
      var dx = mx - nodes[i].px, dy = my - nodes[i].py;
      if(Math.sqrt(dx*dx+dy*dy) < nodes[i].size + 10){ hoveredNode = nodes[i]; break; }
    }
    canvas.style.cursor = hoveredNode ? "pointer" : "default";
  });
  
  canvas.addEventListener("click", function(){
    if(hoveredNode){
      var tip = document.getElementById("ecoTooltip");
      if(tip){
        tip.innerHTML = '<strong style="font-size:16px">' + hoveredNode.name + '</strong><br>' +
          '<span style="color:' + hoveredNode.color + '">' + hoveredNode.org + '</span><br>' +
          '<span style="font-size:12px;color:#aaa">' + hoveredNode.downloads + '</span><br>' +
          '<span style="font-size:13px;margin-top:4px;display:block">' + hoveredNode.desc + '</span>';
        tip.style.display = "block";
        tip.style.left = Math.min(hoveredNode.px/2, w/2 - 150) + "px";
        tip.style.top = (hoveredNode.py/2 - 80) + "px";
        setTimeout(function(){ tip.style.display = "none"; }, 3000);
      }
    }
  });
  
  function drawMap(){
    ctx.clearRect(0,0,w,h);
    ctx.strokeStyle = "rgba(255,255,255,0.03)";
    ctx.lineWidth = 1;
    for(var x=0;x<w;x+=60){ ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke(); }
    for(var y=0;y<h;y+=60){ ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke(); }
    
    connections.forEach(function(pair){
      var na = nodes[pair[0]], nb = nodes[pair[1]];
      ctx.beginPath();
      ctx.moveTo(na.px, na.py);
      var cpx = (na.px+nb.px)/2, cpy = (na.py+nb.py)/2 - 30;
      ctx.quadraticCurveTo(cpx, cpy, nb.px, nb.py);
      var isH = hoveredNode && (hoveredNode.index===pair[0] || hoveredNode.index===pair[1]);
      ctx.strokeStyle = isH ? "rgba(255,255,255,0.2)" : "rgba(255,255,255,0.06)";
      ctx.lineWidth = isH ? 2 : 1;
      ctx.stroke();
      if(isH){
        var t = (Date.now()%2000)/2000;
        var px = na.px+(nb.px-na.px)*t, py = na.py+(nb.py-na.py)*t-30*Math.sin(t*Math.PI);
        ctx.beginPath();ctx.arc(px,py,3,0,Math.PI*2);ctx.fillStyle=na.color;ctx.fill();
      }
    });
    
    var time = Date.now()*0.001;
    nodes.forEach(function(n){
      n.px += Math.sin(time+n.index)*0.15;
      n.py += Math.cos(time*0.7+n.index)*0.1;
      var isH = hoveredNode === n;
      var r = isH ? n.size*1.2 : n.size;
      if(isH){
        var glow = ctx.createRadialGradient(n.px,n.py,0,n.px,n.py,r*2);
        glow.addColorStop(0,n.color+"40");glow.addColorStop(1,n.color+"00");
        ctx.beginPath();ctx.arc(n.px,n.py,r*2,0,Math.PI*2);ctx.fillStyle=glow;ctx.fill();
      }
      ctx.beginPath();ctx.arc(n.px,n.py,r,0,Math.PI*2);
      ctx.fillStyle = n.color+(isH?"dd":"88");ctx.fill();
      ctx.strokeStyle = isH?"#fff":n.color;ctx.lineWidth=isH?2:1;ctx.stroke();
      ctx.fillStyle="#fff";
      ctx.font=(isH?"bold ":"")+(isH?14:11)+"px -apple-system,sans-serif";
      ctx.textAlign="center";ctx.fillText(n.name,n.px,n.py+r+16);
      if(isH){ctx.font="10px -apple-system,sans-serif";ctx.fillStyle="#aaa";ctx.fillText(n.org,n.px,n.py+r+30);}
    });
    requestAnimationFrame(drawMap);
  }
  drawMap();
})();

// Tooltip element
var tipEl = document.createElement("div");
tipEl.id = "ecoTooltip";
tipEl.style.cssText = "display:none;position:fixed;z-index:100;background:rgba(20,20,40,0.95);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:16px 20px;color:#e8e8f0;font-size:14px;pointer-events:none;backdrop-filter:blur(10px);max-width:300px;line-height:1.5;box-shadow:0 8px 32px rgba(0,0,0,0.5)";
document.body.appendChild(tipEl);

// ========== SCROLL ANIMATIONS ==========
var observer = new IntersectionObserver(function(entries){
  entries.forEach(function(e){
    if(e.isIntersecting){
      e.target.classList.add("visible");
      e.target.querySelectorAll(".bar-fill").forEach(function(bar){
        setTimeout(function(){ bar.style.width = bar.dataset.width + "%"; }, 200);
      });
      e.target.querySelectorAll(".compare-bar-inner").forEach(function(bar){
        setTimeout(function(){ bar.style.width = bar.dataset.width + "%"; }, 200);
      });
      e.target.querySelectorAll("[data-target]").forEach(function(num){
        animateNumber(num);
      });
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll(".reveal, .tl-item").forEach(function(el){ observer.observe(el); });

// ========== NUMBER ANIMATION ==========
function animateNumber(el){
  if(el.dataset.animated) return;
  el.dataset.animated = "true";
  var target = parseFloat(el.dataset.target);
  var suffix = el.dataset.suffix || "";
  var isDecimal = el.dataset.decimal === "true";
  var duration = 2000;
  var start = performance.now();
  function update(now){
    var progress = Math.min((now - start) / duration, 1);
    var eased = 1 - Math.pow(1 - progress, 3);
    var current = eased * target;
    el.textContent = (isDecimal ? current.toFixed(1) : Math.floor(current)) + suffix;
    if(progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// ========== NAV HIDE ON SCROLL ==========
var lastScroll = 0;
window.addEventListener("scroll", function(){
  var nav = document.getElementById("nav");
  var st = window.scrollY;
  if(st > lastScroll && st > 100) nav.classList.add("hidden");
  else nav.classList.remove("hidden");
  lastScroll = st;
});

// ========== COMPARISON VIEW SWITCH ==========
function switchView(region){
  document.querySelectorAll(".toggle-btn").forEach(function(b){ b.classList.remove("active"); });
  event.target.classList.add("active");
  document.querySelectorAll(".compare-col").forEach(function(col){
    if(region === "all"){
      col.style.display = "";
      col.classList.toggle("highlight", col.dataset.region === "china");
    } else {
      if(col.dataset.region === region){
        col.style.display = "";
        col.classList.add("highlight");
      } else {
        col.style.display = "none";
        col.classList.remove("highlight");
      }
    }
  });
}

// ========== SMOOTH ANCHOR SCROLL ==========
document.querySelectorAll("a[href^='#']").forEach(function(a){
  a.addEventListener("click", function(e){
    e.preventDefault();
    var target = document.querySelector(a.getAttribute("href"));
    if(target) target.scrollIntoView({ behavior: "smooth" });
  });
});
</script>
</body>
</html>
"""

with open("/app/working/shared/showcase/2026-08-20-china-open-source-ai-ecosystem.html", "a") as f:
    f.write(js_content)

print("JavaScript appended successfully")
