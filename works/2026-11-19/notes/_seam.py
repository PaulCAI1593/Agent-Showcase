
import json
from playwright.sync_api import sync_playwright
url="file:///app/working/shared/showcase/works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html"
def route(r):
    r.continue_() if r.request.url.startswith(("file://","data:","about:")) else r.abort()
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox","--hide-scrollbars"])
    pg=b.new_page(viewport={"width":1260,"height":860}); pg.route("**/*",route)
    pg.goto(url,wait_until="load"); pg.wait_for_timeout(800)
    out["input_rect"]=pg.evaluate("""()=>{const i=document.getElementById('seamRange');
      const r=i.getBoundingClientRect();return {x:Math.round(r.x),w:Math.round(r.width),y:Math.round(r.y),
      val:i.value,min:i.min,max:i.max,dir:getComputedStyle(i).direction,
      trackW:getComputedStyle(i,'::-webkit-slider-runnable-track').width};}""")
    out["row_rect"]=pg.evaluate("()=>{const r=document.querySelector('.seam__row').getBoundingClientRect();return [Math.round(r.x),Math.round(r.width)]}")
    el=pg.query_selector(".seam")
    el.screenshot(path="/app/working/shared/showcase/works/2026-11-19/notes/preview-seam.png")
    b.close()
print(json.dumps(out,ensure_ascii=False,indent=1))
