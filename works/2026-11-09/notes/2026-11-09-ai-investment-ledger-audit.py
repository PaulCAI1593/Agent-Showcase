#!/usr/bin/env python3
"""选题423 过程材料：交付前技术审计（impeccable audit 的可执行部分）。

检查项：横向溢出、文字对比度、reduced-motion、焦点可见性、控制台错误、图表尺寸。
用法： python3 2026-11-09-ai-investment-ledger-audit.py
"""
import os, sys, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REL = "works/2026-11-09/research/2026-11-09-ai-investment-ledger.html"

JS_CONTRAST = """
() => {
  function lum(c){
    const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);};
    return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2]);
  }
  function parse(s){const m=s.match(/rgba?\\(([^)]+)\\)/);if(!m)return null;
    const p=m[1].split(',').map(Number);return p.length>3&&p[3]===0?null:p.slice(0,3);}
  function bgOf(el){
    let n=el;
    while(n&&n!==document.documentElement){
      const c=parse(getComputedStyle(n).backgroundColor);
      if(c)return c;
      n=n.parentElement;
    }
    return [255,255,255];
  }
  const out=[];
  document.querySelectorAll('p,span,div,li,td,th,cite,figcaption,h1,h2,dd,dt').forEach(el=>{
    const txt=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join('');
    if(txt.length<4)return;
    const cs=getComputedStyle(el);
    if(cs.visibility==='hidden'||cs.display==='none')return;
    const fg=parse(cs.color); if(!fg)return;
    const bg=bgOf(el);
    const L1=lum(fg),L2=lum(bg);
    const ratio=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    const size=parseFloat(cs.fontSize), weight=parseInt(cs.fontWeight)||400;
    const large = size>=24 || (size>=18.66 && weight>=700);
    const need = large?3:4.5;
    if(ratio < need){
      out.push({sel:el.tagName+'.'+(el.className||''), text:txt.slice(0,28),
                ratio:+ratio.toFixed(2), need, size, color:cs.color});
    }
  });
  return out;
}
"""

JS_LAYOUT = """
() => ({
  docW: document.documentElement.scrollWidth,
  winW: window.innerWidth,
  overflow: [...document.querySelectorAll('body *')]
    .filter(el=>el.getBoundingClientRect().right > window.innerWidth + 1)
    .slice(0,8).map(el=>el.tagName+'.'+(el.className||'')+':'+Math.round(el.getBoundingClientRect().right)),
  canvases: [...document.querySelectorAll('canvas')].map(c=>c.id+':'+Math.round(c.getBoundingClientRect().height)),
  headings: [...document.querySelectorAll('h1,h2,h3')].map(h=>h.tagName).join(','),
  reduced: matchMedia('(prefers-reduced-motion: reduce)').matches
})
"""


def main():
    url = "file://" + os.path.join(ROOT, REL)
    report = {"contrast": {}, "layout": {}, "console": [], "focus": None}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/chromium",
                              args=["--no-sandbox", "--hide-scrollbars"])
        for w, h, tag in ((1280, 900, "desktop"), (768, 1024, "tablet"), (390, 844, "mobile")):
            pg = b.new_page(viewport={"width": w, "height": h})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console:"+m.type+":"+m.text) if m.type == "error" else None)
            def route(route):
                u = route.request.url
                route.continue_() if u.startswith(("file://", "data:", "about:")) else route.abort()
            pg.route("**/*", route)
            pg.goto(url, wait_until="load")
            pg.wait_for_timeout(1200)
            report["layout"][tag] = pg.evaluate(JS_LAYOUT)
            report["console"] += [tag+" "+e for e in errs]
            if tag == "desktop":
                report["contrast"]["failures"] = pg.evaluate(JS_CONTRAST)
                pg.keyboard.press("Tab")
                report["focus"] = pg.evaluate("""()=>{
                  const el=document.activeElement;
                  const cs=getComputedStyle(el);
                  return {tag:el.tagName, text:(el.textContent||'').slice(0,30),
                          outline:cs.outlineStyle+' '+cs.outlineWidth+' '+cs.outlineColor};
                }""")
            if tag == "mobile":
                pg.screenshot(path=os.path.join(ROOT, "works/2026-11-09", "notes",
                              "2026-11-09-ai-investment-ledger-preview-mobile-viewport.png"))
            pg.close()
        b.close()
    print(json.dumps(report, ensure_ascii=False, indent=1))
    fails = report["contrast"]["failures"]
    bad = [t for t in report["layout"].values() if t["docW"] > t["winW"] + 1]
    print("\nSUMMARY: contrast_failures=%d  horizontal_overflow=%s  console_errors=%d"
          % (len(fails), [t for t in report["layout"] if report["layout"][t]["docW"] > report["layout"][t]["winW"]+1] or "none",
             len(report["console"])))
    return 0 if not fails and not bad and not report["console"] else 1


if __name__ == "__main__":
    sys.exit(main())
