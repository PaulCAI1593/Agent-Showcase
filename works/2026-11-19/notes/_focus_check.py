
import json
from playwright.sync_api import sync_playwright
url="file:///app/working/shared/showcase/works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html"
def route(r):
    r.continue_() if r.request.url.startswith(("file://","data:","about:")) else r.abort()
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":1260,"height":800}); pg.route("**/*",route)
    pg.goto(url,wait_until="load"); pg.wait_for_timeout(600)
    seq=[]
    for i in range(14):
        pg.keyboard.press("Tab")
        seq.append(pg.evaluate("""()=>{const a=document.activeElement;if(!a)return 'none';
          const s=getComputedStyle(a);return (a.id||a.className||a.tagName)+'|'+s.outlineStyle+'|'+s.outlineWidth+'|'+s.outlineColor;}"""))
    out["tab_sequence"]=seq
    # 原生 range 键盘操作
    pg.evaluate("document.getElementById('seamRange').focus()")
    pg.keyboard.press("ArrowRight"); pg.keyboard.press("ArrowRight")
    out["seam_after_arrows"]=pg.inner_text("#railV")
    b.close()
print(json.dumps(out,ensure_ascii=False,indent=1))
