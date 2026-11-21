
import json
from playwright.sync_api import sync_playwright
url="file:///app/working/shared/showcase/works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html"
NOTES="/app/working/shared/showcase/works/2026-11-19/notes"
def route(r):
    r.continue_() if r.request.url.startswith(("file://","data:","about:")) else r.abort()
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox","--hide-scrollbars"])
    pg=b.new_page(viewport={"width":1260,"height":860}); pg.route("**/*",route)
    pg.goto(url,wait_until="load"); pg.wait_for_timeout(1500)
    out["title"]=pg.title()
    out["body_bg"]=pg.evaluate("getComputedStyle(document.body).backgroundColor")
    out["h1"]=pg.evaluate("getComputedStyle(document.querySelector('h1')).fontSize")
    out["scrollHeight"]=pg.evaluate("document.body.scrollHeight")
    out["font_loaded"]=pg.evaluate("document.fonts.check('16px \"Noto Serif SC\"')")
    out["canvas"]=pg.evaluate("""()=>{const c=document.getElementById('world');const x=c.getContext('2d');
      const d=x.getImageData(0,0,c.width,Math.min(c.height,400)).data;let n=0;
      for(let i=3;i<d.length;i+=4) if(d[i]>0) n++; return [c.width,c.height,n];}""")
    pg.screenshot(path=NOTES+"/preview-hero.png")            # 视口
    pg.evaluate("document.getElementById('s3').scrollIntoView()"); pg.wait_for_timeout(700)
    pg.screenshot(path=NOTES+"/preview-s3.png")
    pg.evaluate("document.getElementById('s4').scrollIntoView()"); pg.wait_for_timeout(700)
    pg.screenshot(path=NOTES+"/preview-s4.png")
    pg.evaluate("document.getElementById('s6').scrollIntoView()"); pg.wait_for_timeout(700)
    pg.screenshot(path=NOTES+"/preview-s6.png")
    b.close()
print(json.dumps(out,ensure_ascii=False,indent=1))
