#!/usr/bin/env python3
"""选题454 交付前 audit（等价落地）：Playwright 实测两视口。

检查项：远程依赖 / 运行时错误 / 横向溢出 / 文本与 SVG 文本对比度 /
语义结构 / reduced-motion 分支。只读，不改作品文件。
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = "/app/working/shared/showcase"
HTML = os.path.join(ROOT, "works/2026-11-19/research/2026-11-19-shenzhen-summit-eve.html")
URL = "file://" + HTML
SHOTS = os.path.join(ROOT, "works/2026-11-19/notes")

JS_CONTRAST = r"""
() => {
  function parse(c){
    const m = c.match(/rgba?\(([^)]+)\)/);
    if(!m) return null;
    const p = m[1].split(',').map(s=>parseFloat(s));
    return {r:p[0], g:p[1], b:p[2], a:p.length>3?p[3]:1};
  }
  function over(fg, bg){
    const a = fg.a + bg.a*(1-fg.a);
    if(a===0) return {r:255,g:255,b:255,a:0};
    return {
      r:(fg.r*fg.a + bg.r*bg.a*(1-fg.a))/a,
      g:(fg.g*fg.a + bg.g*bg.a*(1-fg.a))/a,
      b:(fg.b*fg.a + bg.b*bg.a*(1-fg.a))/a,
      a:a};
  }
  function lum(c){
    function f(v){v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4);}
    return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b);
  }
  function ratio(a,b){
    const l1=lum(a), l2=lum(b);
    const hi=Math.max(l1,l2), lo=Math.min(l1,l2);
    return (hi+0.05)/(lo+0.05);
  }
  function bgOf(el){
    let acc = {r:255,g:255,b:255,a:0};
    const stack = [];
    let n = el;
    while(n && n.nodeType===1){
      const c = parse(getComputedStyle(n).backgroundColor);
      if(c && c.a>0){ stack.push(c); if(c.a===1) break; }
      n = n.parentElement;
    }
    let base = {r:255,g:255,b:255,a:1};
    for(let i=stack.length-1;i>=0;i--){ base = over(stack[i], base); }
    return base;
  }
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while(walker.nextNode()){
    const tn = walker.currentNode;
    const text = (tn.nodeValue||'').trim();
    if(!text) continue;
    const el = tn.parentElement;
    if(!el || seen.has(el)) continue;
    seen.add(el);
    const cs = getComputedStyle(el);
    if(cs.visibility==='hidden' || cs.display==='none' || parseFloat(cs.opacity)===0) continue;
    const fg = parse(cs.color); if(!fg) continue;
    const bg = bgOf(el);
    const eff = over(fg, bg);
    const r = ratio(eff, bg);
    const size = parseFloat(cs.fontSize);
    const weight = parseInt(cs.fontWeight)||400;
    const large = size>=24 || (size>=18.66 && weight>=700);
    const need = large?3:4.5;
    out.push({kind:'html', tag:el.tagName.toLowerCase(), cls:el.className&&el.className.toString().slice(0,40),
              size:size, weight:weight, ratio:Math.round(r*100)/100, need:need,
              text:text.slice(0,32)});
  }
  // SVG 文本
  document.querySelectorAll('svg text').forEach(t=>{
    const fill = getComputedStyle(t).fill;
    const fg = parse(fill); if(!fg) return;
    const svg = t.ownerSVGElement;
    let rect = svg ? svg.querySelector('rect') : null;
    const bgc = rect ? parse(rect.getAttribute('fill')) : {r:255,g:255,b:255,a:1};
    const bg = bgc && bgc.a>0 ? bgc : {r:255,g:255,b:255,a:1};
    const r = ratio(fg, bg);
    const size = parseFloat(getComputedStyle(t).fontSize);
    const weight = parseInt(getComputedStyle(t).fontWeight)||400;
    const large = size>=24 || (size>=18.66 && weight>=700);
    out.push({kind:'svg', tag:'text', cls:'', size:size, weight:weight,
              ratio:Math.round(r*100)/100, need: large?3:4.5, text:(t.textContent||'').slice(0,32)});
  });
  return out;
}
"""

def run(pw, w, h, name, full=True):
    browser = pw.chromium.launch(executable_path="/usr/bin/chromium",
                                 args=["--no-sandbox", "--disable-dev-shm-usage"])
    ctx = browser.new_context(viewport={"width": w, "height": h},
                              device_scale_factor=1, reduced_motion="no-preference")
    page = ctx.new_page()
    errors, failed = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(r.url))
    page.goto(URL, wait_until="load")
    page.wait_for_timeout(1200)

    info = page.evaluate("""() => ({
        scrollW: document.scrollingElement.scrollWidth,
        clientW: document.scrollingElement.clientWidth,
        title: document.title,
        h1: document.querySelectorAll('h1').length,
        h2: document.querySelectorAll('h2').length,
        claims: !!document.getElementById('claims'),
        metrics: document.querySelectorAll('.metric').length,
        remote: performance.getEntriesByType('resource').map(r=>r.name)
                  .filter(n=>n.startsWith('http')),
        imgs: document.querySelectorAll('img').length,
        figs: document.querySelectorAll('figure svg').length
    })""")
    contrast = page.evaluate(JS_CONTRAST)
    bad = [c for c in contrast if c["ratio"] < c["need"]]
    shot = os.path.join(SHOTS, f"454-{name}.png")
    page.screenshot(path=shot, full_page=full)
    out = {"viewport": f"{w}x{h}", "info": info, "console_errors": errors,
           "requestfailed": failed, "contrast_nodes": len(contrast),
           "contrast_below_threshold": bad, "screenshot": shot}
    browser.close()
    return out


def main():
    results = []
    with sync_playwright() as pw:
        results.append(run(pw, 1440, 900, "desktop"))
        results.append(run(pw, 390, 844, "mobile"))
    print(json.dumps(results, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
