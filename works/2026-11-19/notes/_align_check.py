
import json, base64
from playwright.sync_api import sync_playwright
URL="file:///app/working/shared/showcase/works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html"
def route(r):
    r.continue_() if r.request.url.startswith(("file://","data:","about:")) else r.abort()
ANALYZE="""async (b64)=>{
  const img=new Image(); img.src='data:image/png;base64,'+b64; await img.decode();
  const c=document.createElement('canvas'); c.width=img.width; c.height=img.height;
  const x=c.getContext('2d'); x.drawImage(img,0,0);
  const d=x.getImageData(0,0,c.width,c.height).data;
  const cols=[];
  for(let px=0;px<c.width;px++){let n=0;
    for(let py=0;py<c.height;py++){const i=(py*c.width+px)*4;
      if(d[i+3]>200&&d[i]>150&&d[i+1]>150&&d[i+2]>150) n++;}
    cols.push(n);}
  let best=0,bestN=0; cols.forEach((n,i)=>{if(n>bestN){bestN=n;best=i;}});
  return {w:c.width,best,bestN};
}"""
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox","--hide-scrollbars"])
    pg=b.new_page(viewport={"width":1260,"height":860}); pg.route("**/*",route)
    pg.goto(URL,wait_until="load"); pg.wait_for_timeout(1000)
    out["layout"]=pg.evaluate("""()=>{const g=s=>{const r=document.querySelector(s).getBoundingClientRect();
      return {t:Math.round(r.top),b:Math.round(r.bottom),l:Math.round(r.left),r:Math.round(r.right)};};
      return {hero:g('.hero'),canvas:g('#world'),seam:g('.seam'),input:g('#seamRange'),hint:g('.seam__hint'),
              heroOverflow:getComputedStyle(document.querySelector('.hero')).overflow,
              heroScrollH:document.querySelector('.hero').scrollHeight};}""")
    # 隔离画布：隐藏所有文字层
    pg.evaluate("()=>{document.querySelectorAll('.hero__in,.seam__lbl,.seam__hint,.seam__line,.rail,input#seamRange,#showcase-bar,#showcase-backlink').forEach(e=>e.style.visibility='hidden');}")
    rect=pg.evaluate("()=>{const r=document.getElementById('seamRange').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}}")
    cv=pg.evaluate("()=>{const r=document.getElementById('world').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}}")
    iclip={"x":rect["x"],"y":rect["y"],"width":rect["w"],"height":rect["h"]}
    cclip={"x":0,"y":cv["y"],"width":cv["w"],"height":cv["h"]}
    out["align"]={}
    for v in ("10","50","90"):
        pg.eval_on_selector("#seamRange", f"el=>{{el.value={v};el.dispatchEvent(new Event('input'))}}")
        pg.wait_for_timeout(150)
        t=pg.evaluate(ANALYZE, base64.b64encode(pg.screenshot(clip=iclip)).decode())
        c=pg.evaluate(ANALYZE, base64.b64encode(pg.screenshot(clip=cclip)).decode())
        tc=rect["x"]+t["best"]; cc=c["best"]
        out["align"][v]={"thumb":round(tc),"seam":round(cc),"delta":round(cc-tc),"votes":c["bestN"]}
    b.close()
print(json.dumps(out,ensure_ascii=False,indent=1))
