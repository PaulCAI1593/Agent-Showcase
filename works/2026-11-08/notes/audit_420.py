#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""选题420 · impeccable audit 五维诊断（规则14 门禁补做）

对应 skills/impeccable/reference/audit.md 的 5 个维度：
  1 A11y  2 Performance  3 Theming  4 Responsive  5 Implementation Integrity
输出：同目录 420-audit-five-dim-20261110.json
"""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
REL = "../research/2026-11-08-ai-valuation-meets-hikes.html"
URL = (HERE / REL).resolve().as_uri()
HTML = (HERE / REL).read_text(encoding="utf-8")
OUT = HERE / "420-audit-five-dim-20261110.json"

VIEWPORTS = [("desktop-1440", 1440, 1000), ("tablet-1024", 1024, 900), ("mobile-390", 390, 844)]

CONTRAST_JS = r"""
() => {
  const lum = (c) => { const s = c.map(v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); });
    return 0.2126*s[0] + 0.7152*s[1] + 0.0722*s[2]; };
  const parse = (s) => { const m = s.match(/[\d.]+/g); return m ? m.map(Number) : null; };
  const hexParse = (h) => { h = h.replace('#',''); if (h.length===3) h = h.split('').map(x=>x+x).join('');
    return [parseInt(h.slice(0,2),16), parseInt(h.slice(2,4),16), parseInt(h.slice(4,6),16)]; };
  const bgOf = (el) => { let n = el;
    while (n && n !== document.documentElement) { const c = getComputedStyle(n).backgroundColor;
      const p = parse(c); if (p && (p[3] === undefined || p[3] > 0.9)) return p.slice(0,3); n = n.parentElement; }
    return [255,255,255]; };
  const own = (n) => { const c = (n.className && n.className.toString ? n.className.toString() : '').trim();
    const f = c.split(/\s+/).filter(Boolean);
    return n.tagName.toLowerCase() + (f.length ? '.' + f.join('.') : ''); };
  const out = [];
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  const seen = new Set();
  while (walk.nextNode()) {
    const el = walk.currentNode;
    const txt = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
    if (!txt) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.05) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    let fg = parse(cs.color); if (!fg) continue; fg = fg.slice(0,3);
    const bg = bgOf(el);
    const l1 = lum(fg), l2 = lum(bg);
    const ratio = (Math.max(l1,l2)+0.05) / (Math.min(l1,l2)+0.05);
    const size = parseFloat(cs.fontSize);
    const weight = parseInt(cs.fontWeight) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const sel = own(el);
    const key = sel + '|' + fg.join(',') + '|' + bg.join(',') + '|' + (large?'L':'N');
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({selector: sel, text: txt.slice(0,28), fg: 'rgb('+fg.join(',')+')', bg: 'rgb('+bg.join(',')+')',
              ratio: Math.round(ratio*100)/100, fontPx: size, weight: weight, large: large,
              need: large ? 3 : 4.5, pass45: ratio >= 4.5, passNeed: ratio >= (large?3:4.5)});
  }
  return out;
}
"""

AUDIT_JS = r"""
() => {
  const els = [...document.querySelectorAll('*')];
  const willChange = els.filter(e => { const w = getComputedStyle(e).willChange; return w && w !== 'auto'; }).length;
  const anims = els.filter(e => { const a = getComputedStyle(e).animationName; return a && a !== 'none'; }).length;
  const transitions = els.filter(e => { const t = getComputedStyle(e).transitionProperty; return t && t !== 'none'; }).length;
  const imgs = [...document.images];
  const links = [...document.querySelectorAll('a, button, [role=button], input, select, textarea')];
  const small = links.map(e => { const r = e.getBoundingClientRect();
      return {sel: e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).trim().split(/\s+/)[0] : ''),
              w: Math.round(r.width), h: Math.round(r.height), text: (e.textContent||'').trim().slice(0,18)}; })
    .filter(o => o.w > 0 && o.h > 0 && (o.w < 24 || o.h < 24));
  const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1]);
  let skips = [];
  for (let i = 1; i < headings.length; i++) if (headings[i] - headings[i-1] > 1)
    skips.push('h'+headings[i-1]+'→h'+headings[i]);
  const customProps = (() => { let n = 0;
    for (const sh of document.styleSheets) { try { for (const r of sh.cssRules) {
      if (r.style) for (const p of r.style) if (p.startsWith('--')) n++; } } catch(e){} }
    return n; })();
  const r = document.documentElement;
  return {
    scrollWidth: r.scrollWidth, clientWidth: r.clientWidth,
    overflowX: r.scrollWidth > r.clientWidth,
    imgTotal: imgs.length, imgNoLazy: imgs.filter(i => i.loading !== 'lazy').length,
    imgNoAlt: imgs.filter(i => !i.hasAttribute('alt')).length,
    willChangeEls: willChange, animationEls: anims, transitionEls: transitions,
    touchTargetsSmall: small, headingCount: headings.length, headingSkips: skips,
    h1Count: headings.filter(h => h === 1).length,
    landmarks: {main: document.querySelectorAll('main').length, nav: document.querySelectorAll('nav').length,
                header: document.querySelectorAll('header').length, footer: document.querySelectorAll('footer').length},
    cssCustomProps: customProps,
    reducedMotionRule: [...document.styleSheets].some(sh => { try {
        return [...sh.cssRules].some(r => r.media && r.media.mediaText.includes('prefers-reduced-motion')); } catch(e){ return false; } }),
    ariaRough: [...document.querySelectorAll('[onclick]')].filter(e => !e.hasAttribute('role') && e.tagName !== 'BUTTON' && e.tagName !== 'A').length
  };
}
"""

report = {"target": URL, "viewports": {}, "contrast": {}, "static": {}}

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for name, w, h in VIEWPORTS:
        ctx = browser.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        errs = {"console": [], "pageerror": [], "failed": []}
        page.on("console", lambda m, e=errs: e["console"].append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda ex, e=errs: e["pageerror"].append(str(ex)))
        page.on("requestfailed", lambda rq, e=errs: e["failed"].append(rq.url))
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1200)
        metrics = page.evaluate(AUDIT_JS)
        metrics["consoleErrors"] = errs["console"]
        metrics["pageErrors"] = errs["pageerror"]
        metrics["failedRequests"] = errs["failed"]
        report["viewports"][name] = metrics
        if name == "desktop-1440":
            rows = page.evaluate(CONTRAST_JS)
            report["contrast"] = {
                "elementsMeasured": len(rows),
                "minRatio": min(r["ratio"] for r in rows),
                "below45": [r for r in rows if not r["pass45"]],
                "belowNeed": [r for r in rows if not r["passNeed"]],
                "worst10": sorted(rows, key=lambda r: r["ratio"])[:10],
            }
        ctx.close()
    browser.close()

# 静态检查（Performance / Theming）
report["static"] = {
    "hasReducedMotion": "prefers-reduced-motion" in HTML,
    "scriptBytes": len(HTML),
    "inlineScriptCount": HTML.count("<script"),
    "remoteRequests": len(re.findall(r'https?://', HTML)),
    "hardcodedHexOutsideRoot": len(re.findall(r'#[0-9a-fA-F]{6}\b', HTML.split(":root", 1)[-1])),
    "cssVarDefs": len(re.findall(r'--[a-z0-9-]+\s*:', HTML)),
}

OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
print("written:", OUT)
