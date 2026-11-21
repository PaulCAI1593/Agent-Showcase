#!/usr/bin/env python3
"""render_check2_rate_ladder.py — 对比度与版式复测 v3（滚动→等揭示→computed color + 截图众数底色 + 透明度链）。"""
import json, os, re, collections, zlib, struct
from playwright.sync_api import sync_playwright

HTML = "/app/working/shared/showcase/works/2026-11-20/creative/2026-11-20-rate-ladder-december.html"
URL = "file://" + HTML

def lum(c):
    f = lambda x: (x/255)/12.92 if x/255 <= 0.03928 else (((x/255)+0.055)/1.055)**2.4
    return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])
def contrast(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb)
    return (hi+0.05)/(lo+0.05)

def decode_png(data):
    pos, idat, w, h, bd, ct = 8, b"", 0, 0, 0, 0
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos+4])[0]; typ = data[pos+4:pos+8]
        chunk = data[pos+8:pos+8+ln]; pos += 12+ln
        if typ == b"IHDR": w, h, bd, ct = struct.unpack(">IIBB", chunk[:10])
        elif typ == b"IDAT": idat += chunk
        elif typ == b"IEND": break
    raw = zlib.decompress(idat); ch = {0:1,2:3,3:1,4:2,6:4}[ct]
    assert bd == 8 and ct in (2,6), (bd, ct)
    stride = w*ch; rows = []; prev = bytearray(stride); i = 0
    for y in range(h):
        f = raw[i]; i += 1
        line = bytearray(raw[i:i+stride]); i += stride
        if f == 1:
            for x in range(ch, stride): line[x] = (line[x]+line[x-ch]) & 255
        elif f == 2:
            for x in range(stride): line[x] = (line[x]+prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x-ch] if x >= ch else 0
                line[x] = (line[x]+((a+prev[x])>>1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x-ch] if x >= ch else 0
                b = prev[x]; c = prev[x-ch] if x >= ch else 0
                pp = a+b-c; pa, pb, pc = abs(pp-a), abs(pp-b), abs(pp-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x]+pr) & 255
        rows.append(bytes(line)); prev = line
    return w, h, ch, rows

def clusters(rows, ch):
    cnt = collections.Counter()
    for r in rows:
        for i in range(0, len(r), ch): cnt[(r[i], r[i+1], r[i+2])] += 1
    return cnt

TARGETS = [
    ("body p", "正文 deck 段"), (".sec-note", "小节说明"), (".deck", "导语"),
    (".cap", "图注"), (".cap .src", "图注来源"), (".tally-cap", "票数图注"),
    ("footer", "页脚"), ("footer li", "页脚列表"), (".hero-foot span", "英雄脚注"),
    (".hero-foot .cue", "英雄提示"), (".board .sub", "面板副标"),
    (".row .lab", "行标签"), (".row .val", "行数值"),
    (".lever label", "档位标签(选中)"), (".lever label:nth-of-type(2)", "档位标签(未选)"),
    (".flap-cap", "翻牌图注"), (".market .mnote", "市场注"), (".market .mlab", "市场标签"),
    (".card .name", "卡片名"), (".card .facts", "卡片事实"), (".card .delta", "涨跌标"),
    (".path .seq", "路径序列"), (".legend", "图例"), (".legend span", "图例项"),
    (".blk .face", "阶梯块面"), (".blk.lit .face", "高亮块面"),
    (".quote-block .attr", "引文署名"), (".quote-block .say", "引文释义"),
    (".verdict", "结论句"), ("h1", "主标题"), ("h1 .up", "主标题强调行"),
    ("h2", "大标题"), (".path .pct", "概率大字"), (".market .mval", "市场大数"),
    ("#showcase-bar .sb-brand", "顶栏品牌"), ("#showcase-bar .sb-back", "顶栏返回"),
    ("#showcase-backlink span", "返回链文字"),
]
ST_JS = """s=>{const el=document.querySelector(s);const cs=getComputedStyle(el);
  let op=1,u=el;while(u){op*=parseFloat(getComputedStyle(u).opacity);u=u.parentElement;}
  const m=(cs.color.match(/[0-9.]+/g)||[]).map(Number);
  return {color:m.slice(0,3),alpha:m.length>3?m[3]:1,op,fs:parseFloat(cs.fontSize),fw:+cs.fontWeight,
          txt:(el.innerText||'').trim().slice(0,24)};}"""

R = {}
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    page = br.new_context(viewport={"width":1260,"height":800}).new_page()
    page.goto(URL, wait_until="load", timeout=60000); page.wait_for_timeout(1500)

    out = []
    for sel, note in TARGETS:
        el = page.query_selector(sel)
        if not el: out.append({"sel":sel,"note":note,"err":"not found"}); continue
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(950)   # 等 IntersectionObserver 揭示 + 0.7s 过渡
        st = page.evaluate(ST_JS, sel)
        box = el.bounding_box()
        vw, vh = 1260, 800
        x = max(0,min(box["x"],vw-4)); y = max(0,min(box["y"],vh-4))
        w = min(box["width"],vw-x); h = min(box["height"],vh-y)
        if w<4 or h<4: out.append({"sel":sel,"note":note,"err":"box too small"}); continue
        W,H,C,rows = decode_png(page.screenshot(clip={"x":x,"y":y,"width":w,"height":h}))
        cnt = clusters(rows,C); total = sum(cnt.values())
        common = cnt.most_common(6)
        bg = common[0][0]
        if sum(abs(a-b) for a,b in zip(bg,st["color"])) < 24 and len(common)>1:
            cands = sorted((lum(c), c) for c, n in common if n >= max(3, total*0.01))
            bg = cands[0][1]
        op = st["op"]
        eff = tuple(op*(st["alpha"]*st["color"][i] + (1-st["alpha"])*bg[i]) + (1-op)*bg[i] for i in range(3))
        cr = contrast(eff, bg)
        big = st["fs"] >= 24 or (st["fs"] >= 18.66 and st["fw"] >= 700)
        need = 3.0 if big else 4.5
        out.append({"sel":sel,"note":note,"fg":"#%02x%02x%02x"%tuple(int(round(v)) for v in eff),
                    "bg":"#%02x%02x%02x"%bg,"cr":round(cr,2),"need":need,"fs":st["fs"],
                    "op":round(op,3),"pass":cr>=need,"txt":st["txt"],
                    "top":["#%02x%02x%02x(%d)"%(c[0],c[1],c[2],n) for c,n in common[:3]]})
    R["contrast"] = out

    el = page.query_selector("#showcase-backlink")
    el.scroll_into_view_if_needed(); page.wait_for_timeout(300)
    st = page.evaluate("""()=>{const a=document.getElementById('showcase-backlink');const cs=getComputedStyle(a);
      return {color:cs.color,bg:cs.backgroundColor,opacity:cs.opacity,cls:a.className,fs:cs.fontSize,fw:cs.fontWeight};}""")
    box = el.bounding_box()
    W,H,C,rows = decode_png(page.screenshot(clip={"x":box["x"],"y":box["y"],"width":box["width"],"height":box["height"]}))
    cnt = clusters(rows,C); common = cnt.most_common(8)
    R["backlink"] = {"computed":st,"box":box,
                     "clusters":["#%02x%02x%02x(%d)"%(c[0],c[1],c[2],n) for c,n in common],
                     "text_vs_pill_cr": round(contrast(common[1][0], common[0][0]),2),
                     "text_cluster":"#%02x%02x%02x"%common[1][0], "pill_cluster":"#%02x%02x%02x"%common[0][0]}

    page.emulate_media(reduced_motion="reduce"); page.wait_for_timeout(500)
    R["rm_final"] = page.evaluate("""()=>{
      const arw=document.querySelector('.pip.hot .arw');
      const up=document.querySelector('h1 .up');
      const fill=document.querySelector('.fill');
      return {arwOpacity: arw&&getComputedStyle(arw).opacity,
              underlineTransform: up&&getComputedStyle(up,'::after').transform,
              fillWidth: fill&&getComputedStyle(fill).width,
              revealIn: document.querySelectorAll('.reveal.in').length,
              revealTotal: document.querySelectorAll('.reveal').length};}""")
    page.emulate_media(reduced_motion="no-preference"); page.wait_for_timeout(300)

    R["geom"] = page.evaluate("""()=>{
      const ls=[...document.querySelectorAll('.lever label')].map(l=>({t:l.innerText.split('\\n')[0],y:Math.round(l.getBoundingClientRect().y),x:Math.round(l.getBoundingClientRect().x),w:Math.round(l.getBoundingClientRect().width),h:Math.round(l.getBoundingClientRect().height)}));
      const ys=[...new Set([...document.querySelectorAll('.ch')].map(c=>Math.round(c.getBoundingClientRect().y)))];
      const kb=document.querySelector('.lever .knob').getBoundingClientRect();
      const h4s=[...document.querySelectorAll('footer h3,footer h4')].map(h=>h.tagName);
      return {labels:ls, flapRows:ys.length, knobRect:{x:Math.round(kb.x),y:Math.round(kb.y),w:Math.round(kb.width),h:Math.round(kb.height)}, footerHeads:h4s,
              heads:[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h=>+h.tagName[1])};}""")

    page.evaluate("document.body.focus()")
    walk = []
    for i in range(8):
        page.keyboard.press("Tab")
        walk.append(page.evaluate("""()=>{const e=document.activeElement;if(!e)return null;
          return e.tagName+(e.id?'#'+e.id:'')+'.'+String(e.className||'').split(' ')[0]+'|'+(e.innerText||e.getAttribute('aria-label')||'').slice(0,14);}"""))
    R["tab_walk"] = walk

    flap_rows = {}
    for v in ("0","25","50"):
        page.click(f'label[for="d{v}"]'); page.wait_for_timeout(700)
        flap_rows[v] = page.evaluate("()=>{const ys=[...new Set([...document.querySelectorAll('.ch')].map(c=>Math.round(c.getBoundingClientRect().y)))];return ys.length;}")
    R["flap_rows_by_state"] = flap_rows
    br.close()

print(json.dumps(R, ensure_ascii=False, indent=1))
