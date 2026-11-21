
import json, base64
from playwright.sync_api import sync_playwright
URL="file:///app/working/shared/showcase/works/2026-11-19/creative/2026-11-19-ascend-embodied-world-model.html"
def route(r):
    r.continue_() if r.request.url.startswith(("file://","data:","about:")) else r.abort()

def scan(pg, b64):
    return pg.evaluate("""async (b64)=>{
      const img=new Image(); img.src='data:image/png;base64,'+b64;
      await img.decode();
      const c=document.createElement('canvas'); c.width=img.width; c.height=img.height;
      const x=c.getContext('2d'); x.drawImage(img,0,0);
      const d=x.getImageData(0,0,c.width,c.height).data;
      const teal=[79,224,200], vio=[199,155,246];
      const near=(i,t)=>Math.abs(d[i]-t[0])<46&&Math.abs(d[i+1]-t[1])<46&&Math.abs(d[i+2]-t[2])<46;
      const cols=[];
      for(let px=0;px<c.width;px++){
        let n=0;
        for(let py=0;py<c.height;py++){
          const i=(py*c.width+px)*4;
          if(d[i+3]>200 && (near(i,teal)||near(i,vio))) n++;
        }
        cols.push(n);
      }
      const hits=[]; let run=null;
      cols.forEach((n,i)=>{ if(n>=4){ if(!run) run=[i,i]; else run[1]=i; } else { if(run){hits.push(run);run=null;} } });
      if(run) hits.push(run);
      return {w:c.width,h:c.height,hits:hits.filter(r=>r[1]-r[0]>=6)};
    }""", b64)

out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium",args=["--no-sandbox","--hide-scrollbars"])
    pg=b.new_page(viewport={"width":1260,"height":860}); pg.route("**/*",route)
    pg.goto(URL,wait_until="load"); pg.wait_for_timeout(900)
    rect=pg.evaluate("()=>{const r=document.getElementById('seamRange').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}}")
    out["rect"]={k:round(v) for k,v in rect.items()}
    clip={"x":rect["x"],"y":rect["y"],"width":rect["w"],"height":rect["h"]}
    res={}
    for v in ("10","50","90"):
        pg.eval_on_selector("#seamRange", f"el=>{{el.value={v};el.dispatchEvent(new Event('input'))}}")
        pg.wait_for_timeout(120)
        png=pg.screenshot(clip=clip)
        res[v]=scan(pg, base64.b64encode(png).decode())
    out["thumb_scan"]=res
    # 画布分界线 x
    out["canvas_seam_frac"]=pg.evaluate("()=>document.getElementById('railV').textContent")
    b.close()
print(json.dumps(out,ensure_ascii=False,indent=1))
