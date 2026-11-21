
import json
from playwright.sync_api import sync_playwright
REL="/app/working/shared/showcase/works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html"
NOTES="/app/working/shared/showcase/works/2026-11-19/notes"
url="file://"+REL
out={}
def route(route):
    u=route.request.url
    route.continue_() if u.startswith(("file://","data:","about:")) else route.abort()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox","--hide-scrollbars"])
    pg=b.new_page(viewport={"width":1260,"height":800})
    pg.route("**/*",route)
    errs=[]
    pg.on("console",lambda m: errs.append(m.type+": "+m.text) if m.type=="error" else None)
    pg.on("pageerror",lambda e: errs.append("pageerror: "+str(e)))
    pg.goto(url,wait_until="load"); pg.wait_for_timeout(1500)
    out["console_errors"]=errs
    out["scrollW"]=pg.evaluate("document.documentElement.scrollWidth")
    out["innerW"]=pg.evaluate("window.innerWidth")
    out["h2"]=pg.eval_on_selector_all("h2","els=>els.map(e=>e.textContent.trim().replace(/\s+/g,''))")
    out["claims_n"]=pg.evaluate("JSON.parse(document.getElementById('claims').textContent).length")
    out["metric_labels"]=pg.eval_on_selector_all(".metric-label","e=>e.map(x=>x.textContent.trim())")
    pg.click("#tabInfer"); out["infer_visible"]=pg.is_visible("#pInfer"); out["train_hidden"]=pg.is_hidden("#pTrain")
    pg.click("#tabTrain")
    pg.click('.door[data-a="asc"]'); out["quiz_ok"]=pg.inner_text("#quizVerdict")
    pg.click('#tabWorld'); out["world_view"]=pg.is_visible("#vWorld"); out["act_hidden"]=pg.is_hidden("#vAct")
    pg.click('#tabAct')
    pg.eval_on_selector("#seamRange","el=>{el.value=78;el.dispatchEvent(new Event('input'))}")
    out["rail_after_seam"]=pg.inner_text("#railV")
    pg.eval_on_selector("#depRange","el=>{el.value=100;el.dispatchEvent(new Event('input'))}")
    out["dep_at_100"]=pg.inner_text("#depQuote")[:50]
    pg.eval_on_selector("#depRange","el=>{el.value=0;el.dispatchEvent(new Event('input'))}")
    out["dep_at_0"]=pg.inner_text("#depQuote")[:50]
    pg.hover("#hBase"); out["arch_hover"]=pg.inner_text("#archK")
    pg.hover(".nnode:nth-of-type(1)"); 
    pg.eval_on_selector_all(".nnode","els=>els[1].dispatchEvent(new MouseEvent('mouseenter'))")
    out["net_hover"]=pg.inner_text("#netK")+" / "+pg.inner_text("#netT")
    out["focus_ring"]=pg.evaluate("()=>{const b=document.getElementById('seamRange');b.focus();return getComputedStyle(b).outlineStyle}")
    pg.screenshot(path=NOTES+"/preview-desktop.png",full_page=True)
    m=b.new_page(viewport={"width":375,"height":812},device_scale_factor=2)
    m.route("**/*",route)
    merr=[]
    m.on("pageerror",lambda e:merr.append(str(e)))
    m.goto(url,wait_until="load"); m.wait_for_timeout(1200)
    out["mobile_scrollW"]=m.evaluate("document.documentElement.scrollWidth")
    out["mobile_innerW"]=m.evaluate("window.innerWidth")
    out["mobile_errors"]=merr
    m.screenshot(path=NOTES+"/preview-mobile.png",full_page=True)
    rm=b.new_page(viewport={"width":1260,"height":800},reduced_motion="reduce")
    rm.route("**/*",route)
    rm.goto(url,wait_until="load"); rm.wait_for_timeout(900)
    out["rm_canvas_pixels"]=rm.evaluate("""()=>{const c=document.getElementById('world');const x=c.getContext('2d');
      const d=x.getImageData(0,0,Math.min(c.width,400),Math.min(c.height,300)).data;let n=0;
      for(let i=3;i<d.length;i+=4){if(d[i]>0)n++;}return n;}""")
    out["rm_hero_visible"]=rm.is_visible("h1")
    b.close()
print(json.dumps(out,ensure_ascii=False,indent=1))
