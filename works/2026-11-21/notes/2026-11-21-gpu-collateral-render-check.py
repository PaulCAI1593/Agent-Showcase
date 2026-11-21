#!/usr/bin/env python3
"""渲染 QA · 2026-11-21-gpu-collateral-bonds.html
三视口（1440/1024/375）：横向溢出、越界元素、控制台错误、对比度、标题序列、字体。
"""
import sys, json, re
from playwright.sync_api import sync_playwright

URL = "file:///app/working/shared/showcase/works/2026-11-21/research/2026-11-21-gpu-collateral-bonds.html"
VIEWPORTS = [(1440, 900), (1024, 800), (375, 812)]

JS_AUDIT = r"""
() => {
  const out = {overflowX: null, offenders: [], headings: [], contrast: [], fonts: {}, sections: 0, claims: null};
  out.overflowX = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  const vw = document.documentElement.clientWidth;
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && (r.right > vw + 1 || r.left < -1)) {
      const cs = getComputedStyle(el);
      if (cs.position === 'fixed') return;
      // 位于可横向滚动容器（.tbl-wrap 等 overflow-x:auto）内部 = 受控滚动，不算页面溢出
      let n = el.parentElement, contained = false;
      while (n && n !== document.body) {
        const o = getComputedStyle(n).overflowX;
        if (o === 'auto' || o === 'scroll') { contained = true; break; }
        n = n.parentElement;
      }
      if (contained) return;
      out.offenders.push({tag: el.tagName, cls: el.className && String(el.className).slice(0,60),
                          left: Math.round(r.left), right: Math.round(r.right)});
    }
  });
  out.headings = [...document.querySelectorAll('h1,h2,h3,h4,h5')].map(h => h.tagName);
  out.sections = document.querySelectorAll('section').length;
  const cl = document.getElementById('claims');
  out.claims = cl ? JSON.parse(cl.textContent).length : 0;
  out.fonts.serif = document.fonts.check('16px "Noto Serif SC"');
  out.fonts.num = document.fonts.check('16px "Newsreader"');

  const lum = c => {
    const [r,g,b] = c.match(/\d+(\.\d+)?/g).slice(0,3).map(Number).map(v => {
      v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4);
    });
    return 0.2126*r + 0.7152*g + 0.0722*b;
  };
  const bgOf = el => {
    let n = el;
    while (n && n !== document.documentElement) {
      const bg = getComputedStyle(n).backgroundColor;
      if (bg && !/rgba\(0, 0, 0, 0\)|transparent/.test(bg)) return bg;
      n = n.parentElement;
    }
    return 'rgb(255,255,255)';
  };
  document.querySelectorAll('p,span,div,td,th,li,dd,dt,h1,h2,h3,cite,figcaption').forEach(el => {
    if (!el.textContent.trim()) return;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    // 只取直接文本节点
    const direct = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!direct) return;
    const cs = getComputedStyle(el);
    const fg = cs.color, bg = bgOf(el);
    const L1 = lum(fg), L2 = lum(bg);
    const ratio = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    const size = parseFloat(cs.fontSize);
    const bold = parseInt(cs.fontWeight,10) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold);
    const need = large ? 3 : 4.5;
    if (ratio < need) {
      out.contrast.push({text: el.textContent.trim().slice(0,28), fg, bg,
                         ratio: +ratio.toFixed(2), need, size});
    }
  });
  return out;
}
"""

results = {}
with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path="/usr/bin/chromium",
                                 args=["--no-sandbox", "--font-render-hinting=none"])
    for w, h in VIEWPORTS:
        page = browser.new_page(viewport={"width": w, "height": h})
        errors = []
        page.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type in ("error","warning") else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(700)
        data = page.evaluate(JS_AUDIT)
        data["console"] = errors
        results[f"{w}x{h}"] = data
        page.close()
    browser.close()

fail = 0
for vp, d in results.items():
    print(f"\n== {vp} ==")
    print(" overflowX(px):", d["overflowX"])
    print(" offenders:", len(d["offenders"]), d["offenders"][:6])
    print(" console:", d["console"][:6])
    print(" contrast fail:", len(d["contrast"]), d["contrast"][:8])
    print(" headings:", "".join(d["headings"]), "| sections:", d["sections"], "| claims:", d["claims"])
    print(" fonts:", d["fonts"])
    if d["overflowX"] > 0 or d["offenders"] or d["console"] or d["contrast"]:
        fail += 1

seq = results["1440x900"]["headings"]
print("\nheading sequence:", seq)
hs = "".join(seq)
assert hs.startswith("H1"), "must start with H1"
assert "H4" not in hs and "H5" not in hs, "no heading skip to H4/H5"
for i in range(1, len(seq)):
    if seq[i] == "H4" and seq[i-1] == "H2":
        raise SystemExit("FAIL: H2 -> H4 skip")
print("QA:", "PASS" if fail == 0 else f"{fail} viewport(s) with findings")
sys.exit(1 if fail else 0)
