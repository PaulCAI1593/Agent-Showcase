
import json, os
from playwright.sync_api import sync_playwright

HTML="/app/working/shared/showcase/works/2026-11-21/creative/2026-11-21-anthropic-coopetition-web.html"
NOTES="/app/working/shared/showcase/works/2026-11-21/notes"
URL="file://"+HTML
res={}
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":1280,"height":900})
    errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL,wait_until="load"); pg.wait_for_timeout(1200)

    res["hero_rect"]=pg.evaluate("""() => {
      const h=document.querySelector('h1').getBoundingClientRect();
      const w=document.querySelector('#hero .wrap').getBoundingClientRect();
      const s=document.querySelector('.sec-h').getBoundingClientRect();
      return {h1x:Math.round(h.x), wrapx:Math.round(w.x), wrapw:Math.round(w.width)}; }""")
    pg.screenshot(path=os.path.join(NOTES,"2026-11-21-coopetition-s1-hero.png"))

    # network section
    pg.evaluate("() => document.getElementById('net').scrollIntoView()")
    pg.wait_for_timeout(1400)
    pg.click('[data-id="amd"]'); pg.wait_for_timeout(1100)
    res["net"]=pg.evaluate("""() => {
      const d=document.getElementById('dossier').getBoundingClientRect();
      const c=document.querySelector('.core-bd').getBoundingClientRect();
      return {dossierOpacity:getComputedStyle(document.getElementById('dossier')).opacity,
              dvis: d.width>0 && d.x>700, core:{x:Math.round(c.x),y:Math.round(c.y),w:Math.round(c.width)}
             }; }""")
    pg.screenshot(path=os.path.join(NOTES,"2026-11-21-coopetition-s2-net.png"))

    # climax
    pg.evaluate("() => document.getElementById('climax').scrollIntoView()")
    pg.wait_for_timeout(2200)
    res["climax"]=pg.evaluate("""() => ({
      n1: document.querySelector('[data-count="28"]').textContent,
      n2: document.querySelector('[data-count="2600"]').textContent,
      vis: getComputedStyle(document.querySelector('.fig')).opacity })""")
    pg.screenshot(path=os.path.join(NOTES,"2026-11-21-coopetition-s3-climax.png"))

    # timeline
    pg.evaluate("() => document.getElementById('time').scrollIntoView()")
    pg.wait_for_timeout(5200)
    res["time"]=pg.evaluate("""() => ({
      rdT: document.getElementById('rdT').textContent,
      rdP: document.getElementById('rdP').textContent,
      rdN: document.getElementById('rdN').textContent,
      scrubH: Math.round(document.getElementById('scrub').getBoundingClientRect().height),
      pathOffset: document.getElementById('tpath').style.strokeDashoffset })""")
    pg.screenshot(path=os.path.join(NOTES,"2026-11-21-coopetition-s4-time.png"))

    # real pointer drag on scrub
    box=pg.locator("#scrub").bounding_box()
    cy=box["y"]+box["height"]/2
    x0=box["x"]+box["width"]*0.5
    before=pg.inner_text("#rdP")
    pg.mouse.move(x0,cy); pg.mouse.down()
    pg.mouse.move(box["x"]+box["width"]*0.12,cy,steps=12); pg.mouse.up()
    pg.wait_for_timeout(200)
    res["drag"]={"before":before,"after":pg.inner_text("#rdP"),"note":pg.inner_text("#rdN"),
                 "value":pg.eval_on_selector("#scrub","el=>el.value")}

    # ledger
    pg.evaluate("() => document.getElementById('ledger').scrollIntoView()")
    pg.wait_for_timeout(600)
    pg.screenshot(path=os.path.join(NOTES,"2026-11-21-coopetition-s5-ledger.png"))
    res["pageerrors_desktop"]=errs
    pg.close()

    # mobile
    m=b.new_page(viewport={"width":375,"height":812},is_mobile=True,has_touch=True)
    merrs=[]; m.on("pageerror",lambda e:merrs.append(str(e)))
    m.goto(URL,wait_until="load"); m.wait_for_timeout(1000)
    m.screenshot(path=os.path.join(NOTES,"2026-11-21-coopetition-m1-hero.png"))
    m.evaluate("() => document.getElementById('net').scrollIntoView()"); m.wait_for_timeout(1300)
    m.click('[data-id="google"]'); m.wait_for_timeout(900)
    m.screenshot(path=os.path.join(NOTES,"2026-11-21-coopetition-m2-sheet.png"))
    m.evaluate("() => document.getElementById('climax').scrollIntoView()"); m.wait_for_timeout(2200)
    m.screenshot(path=os.path.join(NOTES,"2026-11-21-coopetition-m3-climax.png"))
    m.evaluate("() => document.getElementById('time').scrollIntoView()"); m.wait_for_timeout(5200)
    m.screenshot(path=os.path.join(NOTES,"2026-11-21-coopetition-m4-time.png"))
    res["mobile"]=m.evaluate("""() => ({
      sw:document.documentElement.scrollWidth, iw:window.innerWidth,
      scrubH:Math.round(document.getElementById('scrub').getBoundingClientRect().height),
      rdP:document.getElementById('rdP').textContent,
      coreVisible: (()=>{const c=document.querySelector('.core-bd').getBoundingClientRect();
        return c.x>0 && c.y>0 && c.width>0;})() })""")
    res["pageerrors_mobile"]=merrs
    m.close(); b.close()

print(json.dumps(res,ensure_ascii=False,indent=1))
open(os.path.join(NOTES,"2026-11-21-coopetition-section-check.json"),"w",encoding="utf-8").write(
    json.dumps(res,ensure_ascii=False,indent=1))
