
import json
from playwright.sync_api import sync_playwright
URL="file:///app/working/shared/showcase/works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html"
NOTES="/app/working/shared/showcase/works/2026-11-19/notes"
def route(r):
    r.continue_() if r.request.url.startswith(("file://","data:","about:")) else r.abort()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox","--hide-scrollbars"])
    pg=b.new_page(viewport={"width":1260,"height":860}); pg.route("**/*",route)
    pg.goto(URL,wait_until="load"); pg.wait_for_timeout(1200)
    for sec in ("s1","s2","s3","s4","s5","s6"):
        pg.evaluate(f"()=>{{window.scrollTo({{top:document.getElementById('{sec}').offsetTop-60,behavior:'instant'}})}}")
        pg.wait_for_timeout(450)
        pg.screenshot(path=f"{NOTES}/preview-{sec}.png")
    # 移动端首屏与第 3 节
    m=b.new_page(viewport={"width":375,"height":812},device_scale_factor=2); m.route("**/*",route)
    m.goto(URL,wait_until="load"); m.wait_for_timeout(1000)
    m.screenshot(path=NOTES+"/preview-m-hero.png")
    m.evaluate("()=>{window.scrollTo({top:document.getElementById('s3').offsetTop-40,behavior:'instant'})}")
    m.wait_for_timeout(500)
    m.screenshot(path=NOTES+"/preview-m-s3.png")
    b.close()
print("shots ok")
