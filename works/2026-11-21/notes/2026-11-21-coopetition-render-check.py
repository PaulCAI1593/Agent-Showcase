
import json, os
from playwright.sync_api import sync_playwright

HTML = "/app/working/shared/showcase/works/2026-11-21/creative/2026-11-21-anthropic-coopetition-web.html"
NOTES = "/app/working/shared/showcase/works/2026-11-21/notes"
URL = "file://" + HTML
res = {"overflow": {}, "interactions": {}, "console": [], "screens": [], "targets": {}}

CONTRAST_JS = r"""
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
      txt: txt.slice(0,30), fg: st.color, bg:'rgb('+bg.r+','+bg.g+','+bg.b+')',
      ratio:+r.toFixed(2), need, fs, fw});
  });
  return out;
}
"""

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])

    # --- desktop full page ---
    pg = b.new_page(viewport={"width":1280,"height":900}, device_scale_factor=1)
    pg.on("console", lambda m: res["console"].append(f"desktop:{m.type}:{m.text}") if m.type in ("error","warning") else None)
    pg.on("pageerror", lambda e: res["console"].append(f"desktop:pageerror:{e}"))
    pg.goto(URL, wait_until="load"); pg.wait_for_timeout(900)
    res["overflow"]["desktop"] = pg.evaluate("() => ({sw:document.documentElement.scrollWidth, iw:window.innerWidth})")
    p1 = os.path.join(NOTES, "2026-11-21-coopetition-preview-desktop.png")
    pg.screenshot(path=p1, full_page=True); res["screens"].append(p1)

    # interactions
    def txt(sel): return pg.inner_text(sel)
    pg.click('[data-id="amazon"]'); pg.wait_for_timeout(250)
    res["interactions"]["node_amazon"] = ("亚马逊" in txt("#dbody")) and ("约 28%" in txt("#dbody")) and ("难以完全预判或缓解" in txt("#dbody"))
    p2 = os.path.join(NOTES, "2026-11-21-coopetition-preview-interact.png")
    pg.screenshot(path=p2); res["screens"].append(p2)
    pg.click('.chip[data-role="compete"]'); pg.wait_for_timeout(250)
    res["interactions"]["chip_compete"] = pg.evaluate("""() => ({
      pressed: document.querySelector('.chip[data-role="compete"]').getAttribute('aria-pressed'),
      dimmedNodes: document.querySelectorAll('.node.dim').length,
      hiArcs: document.querySelectorAll('.arc.hi').length })""")
    pg.click('.chip[data-role="supply"]'); pg.wait_for_timeout(200)
    res["interactions"]["chip_supply"] = pg.evaluate("() => document.querySelectorAll('.node.dim').length")
    pg.click('.chip[data-role="supply"]'); pg.wait_for_timeout(150)  # toggle back to all
    res["interactions"]["chip_toggle_back"] = pg.evaluate("() => document.querySelectorAll('.node.dim').length")
    # timeline scrub
    before = txt("#rdP")
    pg.eval_on_selector("#scrub", "el => { el.value = 72; el.dispatchEvent(new Event('input', {bubbles:true})); }")
    pg.wait_for_timeout(150)
    res["interactions"]["scrub_72"] = {"before": before, "after": txt("#rdP"), "note": txt("#rdN"), "time": txt("#rdT")}
    # keyboard: focus a node and press Enter
    pg.eval_on_selector('[data-id="tsmc"]', "el => el.focus()")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    res["interactions"]["kbd_enter_tsmc"] = "台积电" in txt("#dbody")
    # Escape closes
    pg.keyboard.press("Escape"); pg.wait_for_timeout(150)
    res["interactions"]["esc_close"] = "点开网络里的任意一家" in txt("#dbody")
    # touch targets
    res["targets"]["small"] = pg.evaluate("""() => { const out=[];
      document.querySelectorAll('button, input, .node').forEach(el=>{ const r=el.getBoundingClientRect();
        if(r.height>0 && r.height<24) out.push((el.className.baseVal!==undefined?el.className.baseVal:el.className)+':'+Math.round(r.height)); });
      return out; }""")
    # contrast (desktop, after reset)
    res["contrast_desktop"] = pg.evaluate(CONTRAST_JS)
    pg.close()

    # --- mobile ---
    m = b.new_page(viewport={"width":375,"height":812}, device_scale_factor=1, is_mobile=True, has_touch=True)
    m.on("pageerror", lambda e: res["console"].append(f"mobile:pageerror:{e}"))
    m.goto(URL, wait_until="load"); m.wait_for_timeout(900)
    res["overflow"]["mobile"] = m.evaluate("() => ({sw:document.documentElement.scrollWidth, iw:window.innerWidth})")
    p3 = os.path.join(NOTES, "2026-11-21-coopetition-preview-mobile.png")
    m.screenshot(path=p3, full_page=True); res["screens"].append(p3)
    m.click('[data-id="google"]'); m.wait_for_timeout(500)
    res["interactions"]["mobile_sheet_open"] = m.evaluate("""() => {
      const d=document.getElementById('dossier'); const r=d.getBoundingClientRect();
      return {open:d.classList.contains('open'), top:Math.round(r.top), vh:window.innerHeight,
              hasGoogle: document.getElementById('dbody').innerText.indexOf('谷歌')>-1}; }""")
    p4 = os.path.join(NOTES, "2026-11-21-coopetition-preview-mobile-sheet.png")
    m.screenshot(path=p4); res["screens"].append(p4)
    res["contrast_mobile"] = m.evaluate(CONTRAST_JS)
    m.close()
    b.close()

os.makedirs(NOTES, exist_ok=True)
open(os.path.join(NOTES,"2026-11-21-coopetition-render-check.json"),"w",encoding="utf-8").write(
    json.dumps(res, ensure_ascii=False, indent=1))
print(json.dumps(res, ensure_ascii=False, indent=1))
