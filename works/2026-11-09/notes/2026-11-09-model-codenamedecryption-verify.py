#!/usr/bin/env python3
"""选题425 门禁补做：model-codenamedecryption 交付前 Playwright 实测。

用法： python3 2026-11-09-model-codenamedecryption-verify.py
输出： 控制台错误数、三档视口横向溢出、文本对比度、reduced-motion 替代行为。
约束： 只发 file:// 与 data: 请求，外部请求一律 abort（作品契约：零远程依赖）。
"""
import json
import os

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))   # showcase/
REL = "works/2026-11-09/creative/2026-11-09-model-codenamedecryption.html"
URL = "file://" + os.path.join(ROOT, REL)

VIEWPORTS = [(375, 812), (768, 1024), (1440, 900)]

CONTRAST_JS = r"""
() => {
  function parse(c){
    const m = String(c).match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
    if (!m) return null;
    return {r:+m[1], g:+m[2], b:+m[3], a: m[4]===undefined?1:parseFloat(m[4])};
  }
  function over(fg, bg){ // alpha-composite fg over bg
    const a = fg.a;
    return {r: fg.r*a + bg.r*(1-a), g: fg.g*a + bg.g*(1-a), b: fg.b*a + bg.b*(1-a), a:1};
  }
  function lum(c){
    const f = v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
    return 0.2126*f(c.r) + 0.7152*f(c.g) + 0.0722*f(c.b);
  }
  function ratio(a, b){ const l1=lum(a), l2=lum(b); const hi=Math.max(l1,l2), lo=Math.min(l1,l2); return (hi+0.05)/(lo+0.05); }
  function effBg(el){
    let cur = el, stack = [];
    while (cur){
      const c = parse(getComputedStyle(cur).backgroundColor);
      if (c && c.a > 0){ stack.push(c); if (c.a === 1) break; }
      cur = cur.parentElement;
    }
    let bg = stack.length ? stack.pop() : {r:255,g:255,b:255,a:1};
    while (stack.length){ bg = over(stack.pop(), bg); }
    return bg;
  }
  const out = [];
  const seen = new Set();
  document.querySelectorAll('body *').forEach(el => {
    if (el.closest('[aria-hidden="true"]')) return;
    const st = getComputedStyle(el);
    if (st.display === 'none' || st.visibility === 'hidden' || parseFloat(st.opacity) === 0) return;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    // only elements with their own direct text
    const txt = Array.from(el.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join('');
    if (!txt) return;
    const fgRaw = parse(st.color); if (!fgRaw) return;
    const bg = effBg(el);
    const fg = fgRaw.a < 1 ? over(fgRaw, bg) : fgRaw;
    const size = parseFloat(st.fontSize);
    const bold = parseInt(st.fontWeight, 10) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold);
    const need = large ? 3 : 4.5;
    const cr = ratio(fg, bg);
    const key = st.color + '|' + getComputedStyle(el.parentElement||el).backgroundColor + '|' + size;
    if (cr < need && !seen.has(key)){
      seen.add(key);
      out.push({ratio: +cr.toFixed(2), need, size, color: st.color, bg: `rgb(${Math.round(bg.r)}, ${Math.round(bg.g)}, ${Math.round(bg.b)})`, text: txt.slice(0,40)});
    }
  });
  return out;
}
"""


def route(route):
    u = route.request.url
    route.continue_() if u.startswith(("file://", "data:", "about:")) else route.abort()


def main():
    report = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/chromium",
                              args=["--no-sandbox", "--hide-scrollbars",
                                    "--force-device-scale-factor=1"])
        # 1) 控制台错误（含 pageerror / 请求失败）
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.route("**/*", route)
        errs, reqfail = [], []
        pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
        pg.on("requestfailed", lambda r: reqfail.append(r.url))
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(2200)
        # 交互冒烟：翻一张卡、切一次 tab、跑一次比对
        pg.click("#panel-codes .card")
        pg.wait_for_timeout(400)
        pg.click("#tab-open")
        pg.wait_for_timeout(300)
        pg.click("#tab-codes")
        pg.click("#scanbtn")
        pg.wait_for_timeout(1500)
        pg.click("#gobtn")
        pg.wait_for_timeout(800)
        report["console_errors"] = errs
        report["failed_requests"] = reqfail
        report["smoke_interactions"] = "card/tab/scan/gobtn 已点击，无异常"
        ctx.close()

        # 2) 三档视口横向溢出
        overflow = []
        for w, h in VIEWPORTS:
            c = b.new_context(viewport={"width": w, "height": h})
            q = c.new_page()
            q.route("**/*", route)
            q.goto(URL, wait_until="load")
            q.wait_for_timeout(1600)
            m = q.evaluate("""() => ({
                sw: document.documentElement.scrollWidth,
                cw: document.documentElement.clientWidth,
                bw: document.body.scrollWidth,
                offenders: Array.from(document.querySelectorAll('body *'))
                  .filter(el => { const r = el.getBoundingClientRect();
                                  return r.right > document.documentElement.clientWidth + 1 || r.left < -1; })
                  .slice(0, 8)
                  .map(el => (el.tagName + '.' + (el.className && el.className.baseVal===undefined ? String(el.className).split(' ')[0] : '') +
                              ' right=' + Math.round(el.getBoundingClientRect().right)))
            })""")
            overflow.append({"viewport": f"{w}x{h}", "scrollWidth": m["sw"],
                             "clientWidth": m["cw"], "overflow_px": m["sw"] - m["cw"],
                             "offenders": m["offenders"]})
            # 对比度只在桌面档测一次即可（同一配色）
            if w == 1440:
                report["contrast_failures"] = q.evaluate(CONTRAST_JS)
                report["contrast_total_text_nodes"] = q.evaluate(
                    "() => Array.from(document.querySelectorAll('body *')).filter(el => Array.from(el.childNodes).some(n=>n.nodeType===3 && n.textContent.trim()) && el.getBoundingClientRect().width>2 && getComputedStyle(el).display!=='none').length")
            c.close()
        report["overflow"] = overflow

        # 3) reduced-motion 替代行为
        c = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        q = c.new_page()
        q.route("**/*", route)
        q.goto(URL, wait_until="load")
        q.wait_for_timeout(1200)
        before = q.evaluate("""() => {
            const n = document.querySelector('.codename');
            const cs = getComputedStyle(n);
            return {codename_text: n.textContent.trim(), opacity: cs.opacity,
                    match_stamp_opacity: getComputedStyle(document.querySelector('.match-stamp')).opacity};
        }""")
        q.click("#scanbtn")
        q.wait_for_timeout(300)
        after = q.evaluate("""() => ({
            match: document.getElementById('device').classList.contains('match'),
            stamp_opacity: getComputedStyle(document.querySelector('.match-stamp')).opacity,
            btn: document.getElementById('scanbtn').textContent.trim(),
            scroll_behavior: getComputedStyle(document.documentElement).scrollBehavior,
            transition_dur: getComputedStyle(document.querySelector('.tease')).transitionDuration
        })""")
        q.click("#panel-codes .card")
        q.wait_for_timeout(250)
        flipped = q.evaluate("""() => ({
            pressed: document.querySelector('#panel-codes .card').getAttribute('aria-pressed'),
            tease_opacity: getComputedStyle(document.querySelector('#panel-codes .card .tease')).opacity,
            pread: document.getElementById('pread').textContent
        })""")
        report["reduced_motion"] = {"before": before, "after_scan_click": after, "after_card_click": flipped}
        c.close()
        b.close()

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
