
import json
from playwright.sync_api import sync_playwright
NOTES="/app/working/shared/showcase/works/2026-11-19/notes"
URL="file:///app/working/shared/showcase/works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html"
def route(r):
    r.continue_() if r.request.url.startswith(("file://","data:","about:")) else r.abort()
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox","--hide-scrollbars"])
    for vp in ({"width":1260,"height":860},{"width":375,"height":812}):
        pg=b.new_page(viewport=vp); pg.route("**/*",route)
        pg.goto(URL,wait_until="load"); pg.wait_for_timeout(900)
        key=str(vp["width"])
        out[key]=pg.evaluate("""()=>{const q=s=>document.querySelector(s);
          const R=e=>{const r=e.getBoundingClientRect();return {t:Math.round(r.top),b:Math.round(r.bottom),h:Math.round(r.height)};};
          const hero=q('.hero'), hint=q('.seam__hint'), inp=q('#seamRange'), seam=q('.seam'), cw=q('#world');
          const hs=getComputedStyle(hero);
          return {hero:R(hero),canvas:R(cw),seam:R(seam),input:R(inp),hint:R(hint),
            overflow:hs.overflow, minH:hs.minHeight, scrollH:hero.scrollHeight,
            hint_clipped_by_hero: R(hint).b > R(hero).b,
            input_clipped: R(inp).b > R(hero).b,
            bodyH:document.body.scrollHeight};}""")
        # 截取 hero 区域看是否含提示文字
        pg.screenshot(path=f"{NOTES}/_vp{vp['width']}_hero.png", clip={"x":0,"y":0,"width":vp["width"],"height":min(vp["height"],900)})
        pg.close()
    b.close()
print(json.dumps(out,ensure_ascii=False,indent=1))
