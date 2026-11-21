
import json, sys
from playwright.sync_api import sync_playwright

HTML = "/app/working/shared/showcase/works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html"
JS = r"""
() => {
  function parse(c){ const m = c.match(/rgba?\(([^)]+)\)/); if(!m) return null;
    const p = m[1].split(',').map(Number); return {r:p[0], g:p[1], b:p[2], a: p.length>3?p[3]:1}; }
  function lum(c){ function f(v){ v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); }
    return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); }
  function ratio(a,b){ const l1=lum(a), l2=lum(b); const hi=Math.max(l1,l2), lo=Math.min(l1,l2);
    return (hi+0.05)/(lo+0.05); }
  function effBg(el){ let n = el;
    while(n){ const c = parse(getComputedStyle(n).backgroundColor);
      if(c && c.a > 0.5) return c; n = n.parentElement; }
    return {r:255,g:255,b:255,a:1}; }
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    if(!el.childNodes.length) return;
    let txt = '';
    el.childNodes.forEach(n => { if(n.nodeType===3) txt += n.textContent; });
    txt = txt.trim();
    if(!txt) return;
    const st = getComputedStyle(el);
    if(st.visibility==='hidden' || st.display==='none' || parseFloat(st.opacity)<0.5) return;
    const fg = parse(st.color); if(!fg) return;
    const bg = effBg(el);
    const fs = parseFloat(st.fontSize), fw = parseInt(st.fontWeight)||400;
    const large = fs>=24 || (fs>=18.66 && fw>=700);
    const need = large?3:4.5;
    const r = ratio(fg,bg);
    if(r < need) out.push({sel: el.tagName.toLowerCase()+'.'+(el.className||'').toString().split(' ')[0],
      txt: txt.slice(0,26), fg: st.color, bg: 'rgb('+bg.r+','+bg.g+','+bg.b+')',
      ratio: +r.toFixed(2), need, fs, fw});
  });
  return out;
}
"""
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    pg = br.new_page(viewport={"width":1280,"height":900})
    pg.goto("file://"+HTML, wait_until="load")
    pg.wait_for_timeout(900)
    fails = pg.evaluate(JS)
    # also exercise every interactive state, then re-check
    for sel in ['.seg-btn[data-cal="stock"]','.leg[data-seg="2"]','#segRest','.m[data-m="7"]','.chip[data-v="rate"]']:
        pg.click(sel); pg.wait_for_timeout(120)
    fails2 = pg.evaluate(JS)
    br.close()

report = {"initial_fail_count": len(fails), "after_interaction_fail_count": len(fails2),
          "initial": fails, "after": fails2}
print(json.dumps(report, ensure_ascii=False, indent=1))
open("/app/working/shared/showcase/works/2026-11-21/notes/2026-11-21-tic-contrast-check.json","w",encoding="utf-8").write(
    json.dumps(report, ensure_ascii=False, indent=1))
