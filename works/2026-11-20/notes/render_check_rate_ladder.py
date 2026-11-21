#!/usr/bin/env python3
"""render_check_rate_ladder.py — #457 单件真实渲染取证（绘界实跑）。
覆盖：远程请求拦截、console/pageerror、两段声明、375px 溢出、
reduced-motion、焦点可见、触达目标、逐元素实测对比度（截图像素取色）、
backlink 返回链实测、桌面/手机整页截图。
"""
import json, os, re, sys, collections
from playwright.sync_api import sync_playwright

HTML = "/app/working/shared/showcase/works/2026-11-20/creative/2026-11-20-rate-ladder-december.html"
NOTES = "/app/working/shared/showcase/works/2026-11-20/notes"
URL = "file://" + HTML
BEATS13 = {"地缘与能源","厂商与算力权力","开源 vs 闭源之争","估值与资本","宏观利率与股市",
           "算力·能耗·环境","就业与劳动","机器人与具身","安全与治理","工具链与产业主权",
           "应用落地","成本与普惠","待归类"}

R = {"pass": [], "fail": [], "warn": [], "evidence": {}}
def ok(k, v): R["pass"].append(f"{k}: {v}")
def bad(k, v): R["fail"].append(f"{k}: {v}")
def wrn(k, v): R["warn"].append(f"{k}: {v}")

raw = open(HTML, encoding="utf-8").read()

# ---------- A. 静态：零远程依赖 ----------
remote = re.findall(r'(?:src|href)\s*=\s*["\'](?:https?:)?//[^"\']+|url\(\s*["\']?(?:https?:)?//[^)"\']+|@import\s+["\']?(?:https?:)?//', raw, re.I)
if remote: bad("静态远程依赖", remote)
else: ok("静态远程依赖", "0 条（src/href/url()/@import 无 http(s):// 或 //）")

# ---------- B. 渲染取证 ----------
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/chromium",
                           args=["--no-sandbox", "--allow-file-access-from-files"])
    ctx = br.new_context(viewport={"width": 1260, "height": 800})
    page = ctx.new_page()
    reqs, cons, errs, blocked = [], [], [], []
    page.on("request", lambda r: reqs.append(r.url))
    page.on("requestfailed", lambda r: blocked.append(r.url + " :: " + (r.failure or "")))
    page.on("console", lambda m: cons.append(f"{m.type}: {m.text}") if m.type in ("error","warning") else None)
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.route("**/*", lambda route: route.abort() if not route.request.url.startswith("file://") else route.continue_())
    page.goto(URL, wait_until="load", timeout=60000)
    page.wait_for_timeout(1800)

    # B1 运行期远程请求
    nonfile = [u for u in reqs if not u.startswith("file://")]
    if nonfile: bad("运行期远程请求", nonfile)
    else: ok("运行期远程请求", f"0 条（共 {len(reqs)} 个请求全为 file://）")
    if errs: bad("pageerror", errs)
    else: ok("pageerror", "0")
    if cons: wrn("console error/warning", cons)
    else: ok("console error/warning", "0")

    # B2 标题 / lang / viewport / beat
    title = page.title()
    html_lang = page.evaluate("document.documentElement.lang")
    vp = page.evaluate("!!document.querySelector('meta[name=viewport]')")
    beat = page.evaluate("(document.querySelector('meta[name=showcase-beat]')||{}).content")
    R["evidence"]["title"] = title
    if html_lang == "zh-CN": ok("lang", "zh-CN")
    else: bad("lang", html_lang)
    if vp: ok("viewport meta", "存在")
    else: bad("viewport meta", "缺失")
    if beat in BEATS13: ok("showcase-beat", f"“{beat}” 在 13 条封闭集内")
    else: bad("showcase-beat", beat)

    # B3 claims 两段
    claims_json = page.evaluate("(document.getElementById('claims')||{}).textContent")
    if not claims_json: bad("claims 块", "缺失")
    else:
        try:
            claims = json.loads(claims_json)
            body_txt = page.evaluate("document.body.innerText")
            norm = lambda s: re.sub(r"\s+", "", s)
            nbody = norm(body_txt)
            hits = [c for c in claims if norm(c.get("quote","")) in nbody]
            raw_hits = [c for c in claims if c.get("quote","") in raw]
            R["evidence"]["claims"] = [{"value":c.get("value"),"label":c.get("label"),"quote":c.get("quote"),
                                        "in_body": c in hits, "in_file": c in raw_hits} for c in claims]
            if len(hits) == len(claims) and 3 <= len(claims) <= 8:
                ok("claims", f"{len(claims)} 条 · quote 正文逐字命中 {len(hits)}/{len(claims)}")
            else:
                bad("claims", f"{len(claims)} 条 · 命中 {len(hits)}/{len(claims)}")
        except Exception as e:
            bad("claims 解析", str(e))

    # B4 375px 横向溢出
    page.set_viewport_size({"width": 375, "height": 812})
    page.wait_for_timeout(600)
    ov = page.evaluate("""() => {
      const d = document.documentElement;
      const sw = d.scrollWidth, cw = d.clientWidth;
      const off = [];
      document.querySelectorAll('body *').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width && (r.right > cw + 1 || r.left < -1) && getComputedStyle(el).position !== 'fixed')
          off.push(el.tagName.toLowerCase()+'.'+(el.className&&el.className.baseVal===undefined?String(el.className).split(' ')[0]:'')+' r='+Math.round(r.right));
      });
      return {sw, cw, off: off.slice(0,12)};
    }""")
    if ov["sw"] <= ov["cw"] + 1 and not ov["off"]:
        ok("375px 无横向滚动", f"scrollWidth={ov['sw']} <= clientWidth={ov['cw']}")
    else:
        bad("375px 横向溢出", ov)

    # B5 触达目标 @375
    small = page.evaluate("""() => {
      const out = [];
      document.querySelectorAll('a,button,input,label,[role=button]').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return;
        if (r.width < 24 || r.height < 24)
          out.push({sel: el.tagName.toLowerCase()+'#'+(el.id||'')+'.'+String(el.className||'').split(' ')[0],
                    w: Math.round(r.width), h: Math.round(r.height), t: (el.innerText||el.value||'').slice(0,16)});
      });
      return out;
    }""")
    R["evidence"]["small_targets_375"] = small
    if small: wrn("触达目标 <24px @375", small)
    else: ok("触达目标 @375", "全部 >=24px")

    # B6 reduced-motion
    page.emulate_media(reduced_motion="reduce")
    page.wait_for_timeout(400)
    rm = page.evaluate("""() => {
      const rev = document.querySelector('.reveal');
      const cs = rev ? getComputedStyle(rev) : null;
      const h1up = document.querySelector('h1 .up');
      const after = h1up ? getComputedStyle(h1up, '::after') : null;
      return {scroll: getComputedStyle(document.documentElement).scrollBehavior,
              revealOpacity: cs && cs.opacity, revealTransition: cs && cs.transitionDuration,
              swipeAnim: after && after.animationDuration};
    }""")
    R["evidence"]["reduced_motion"] = rm
    if rm["scroll"] == "auto" and rm["revealOpacity"] == "1":
        ok("prefers-reduced-motion", json.dumps(rm, ensure_ascii=False))
    else:
        bad("prefers-reduced-motion", rm)
    page.emulate_media(reduced_motion="no-preference")

    # B7 焦点可见（键盘 Tab）
    page.set_viewport_size({"width": 1260, "height": 800})
    page.evaluate("document.body.focus()")
    page.keyboard.press("Tab")
    page.wait_for_timeout(200)
    focus = page.evaluate("""() => {
      const el = document.activeElement; if(!el) return null;
      const cs = getComputedStyle(el);
      return {tag: el.tagName, id: el.id, cls: String(el.className).slice(0,40),
              outline: cs.outlineStyle + ' ' + cs.outlineWidth + ' ' + cs.outlineColor};
    }""")
    R["evidence"]["first_tab_focus"] = focus
    if focus and focus["outline"].startswith("solid") and focus["outline"].split()[1] not in ("0px","medium"):
        ok("Tab 首焦点可见", json.dumps(focus, ensure_ascii=False))
    else:
        wrn("Tab 首焦点", focus)

    # B8 heading 层级 / 图片 alt
    sem = page.evaluate("""() => {
      const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h=>+h.tagName[1]);
      const imgs = [...document.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'), alt:i.alt}));
      let skip = null, prev = 0;
      hs.forEach(l => { if (prev && l > prev + 1 && !skip) skip = prev+'→'+l; prev = l; });
      return {heads: hs, h1count: hs.filter(x=>x===1).length, skip, imgs,
              btnNoName: [...document.querySelectorAll('button')].filter(b=>!b.innerText.trim()&&!b.getAttribute('aria-label')).length};
    }""")
    R["evidence"]["semantics"] = sem
    if sem["h1count"] == 1 and not sem["skip"]: ok("标题层级", f"h1×1, 无跳级, 共 {len(sem['heads'])} 个标题")
    else: bad("标题层级", sem)
    noalt = [i for i in sem["imgs"] if not i["alt"]]
    if noalt: wrn("img alt 缺失", noalt)
    else: ok("img alt", f"{len(sem['imgs'])} 张图全有 alt（或无图）")

    # ---------- C. 逐元素实测对比度（截图像素取色） ----------
    def contrast(a, b):
        def lum(c):
            f = lambda x: (x/255)/12.92 if x/255 <= 0.03928 else (((x/255)+0.055)/1.055)**2.4
            return 0.2126*f(c[0]) + 0.7152*f(c[1]) + 0.0722*f(c[2])
        la, lb = lum(a), lum(b)
        hi, lo = max(la, lb), min(la, lb)
        return (hi+0.05)/(lo+0.05)

    # 采样器：对一组 selector，截其盒子像素，取众数=底色，最远聚类=字色
    def sample(sels, note):
        out = []
        for sel in sels:
            el = page.query_selector(sel)
            if not el: out.append({"sel": sel, "err": "not found"}); continue
            box = el.bounding_box()
            if not box or box["width"] < 2 or box["height"] < 2:
                out.append({"sel": sel, "err": "tiny box"}); continue
            if box["y"] < 0 or box["y"]+box["height"] > 800 or box["x"]+box["width"] > 1260:
                page.evaluate("s=>document.querySelector(s).scrollIntoView({block:'center'})", sel)
                page.wait_for_timeout(250)
                box = el.bounding_box()
            clip = {"x": max(0,box["x"]), "y": max(0,box["y"]),
                    "width": min(box["width"], 1260-max(0,box["x"])),
                    "height": min(box["height"], 800-max(0,box["y"]))}
            if clip["width"] < 2 or clip["height"] < 2:
                out.append({"sel": sel, "err": "clip empty"}); continue
            shot = page.screenshot(clip=clip)
            # PNG 解码：用 chromium 自带? 简化——用 playwright 的 image? 直接内置解码太重；
            # 改走 page.evaluate 在 canvas 上合成? 不行，跨 file:// 截图数据可用 zlib 手解。
            out.append({"sel": sel, "_png": shot, "_box": clip})
        return out

    # 用 canvas + 页内 JS 取色更稳：直接在页面里把元素盒子画进 canvas 不可行（跨元素渲染）。
    # 采用 PNG 纯 Python 解码（zlib + unfilter）。
    import zlib, struct
    def decode_png(data):
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        pos, idat, w, h, bd, ct = 8, b"", 0, 0, 0, 0
        while pos < len(data):
            ln = struct.unpack(">I", data[pos:pos+4])[0]; typ = data[pos+4:pos+8]
            chunk = data[pos+8:pos+8+ln]; pos += 12+ln
            if typ == b"IHDR": w, h, bd, ct = struct.unpack(">IIBB", chunk[:10])
            elif typ == b"IDAT": idat += chunk
            elif typ == b"IEND": break
        raw_ = zlib.decompress(idat)
        ch = {0:1, 2:3, 3:1, 4:2, 6:4}[ct]
        assert bd == 8 and ct in (2,6), f"bd={bd} ct={ct}"
        stride = w*ch
        out, prev = [], bytearray(stride)
        i = 0
        for y in range(h):
            f = raw_[i]; i += 1
            line = bytearray(raw_[i:i+stride]); i += stride
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
            out.append(bytes(line)); prev = line
        return w, h, ch, out

    def measure(sel, note, minpx=30):
        el = page.query_selector(sel)
        if not el: return {"sel": sel, "note": note, "err": "not found"}
        el.scroll_into_view_if_needed(); page.wait_for_timeout(200)
        box = el.bounding_box()
        if not box or box["width"] < 3 or box["height"] < 3:
            return {"sel": sel, "note": note, "err": "box too small"}
        vw, vh = 1260, 800
        x = max(0, min(box["x"], vw-4)); y = max(0, min(box["y"], vh-4))
        w = min(box["width"], vw-x); h = min(box["height"], vh-y)
        if w < 3 or h < 3: return {"sel": sel, "note": note, "err": "offscreen"}
        shot = page.screenshot(clip={"x": x, "y": y, "width": w, "height": h})
        W, H, C, rows = decode_png(shot)
        cnt = collections.Counter()
        for r in rows:
            for i in range(0, len(r), C):
                cnt[(r[i], r[i+1], r[i+2])] += 1
        total = sum(cnt.values())
        if total < minpx: return {"sel": sel, "note": note, "err": "too few px"}
        mode, nmode = cnt.mother if False else cnt.most_common(1)[0]
        # 字色：与底色亮度差最大、且占比>=0.4% 的聚类
        def L(c):
            f = lambda x: (x/255)/12.92 if x/255 <= 0.03928 else (((x/255)+0.055)/1.055)**2.4
            return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])
        cand = [(abs(L(c)-L(mode)), c, n) for c, n in cnt.items() if n >= max(3, total*0.004)]
        if not cand: return {"sel": sel, "note": note, "err": "no glyph cluster", "bg": mode}
        cand.sort(reverse=True)
        _, fg, nfg = cand[0]
        cr = (max(L(fg), L(mode))+0.05)/(min(L(fg), L(mode))+0.05)
        # 字号
        fs = page.evaluate("s=>getComputedStyle(document.querySelector(s)).fontSize", sel)
        big = float(fs.replace("px","")) >= 24
        need = 3.0 if big else 4.5
        return {"sel": sel, "note": note, "fg": "#%02x%02x%02x" % fg, "bg": "#%02x%02x%02x" % mode,
                "cr": round(cr, 2), "need": need, "fs": fs,
                "pass": cr >= need, "px": total}

    page.set_viewport_size({"width": 1260, "height": 800}); page.wait_for_timeout(400)
    targets = [
        ("body p", "正文"),
        (".sec-note", "小节说明"),
        (".deck", "导语"),
        (".cap", "图注"),
        (".cap .src", "图注来源"),
        (".tally-cap", "大数字图注"),
        ("footer", "页脚"),
        ("footer li", "页脚列表"),
        (".hero-foot", "英雄区脚注"),
        (".hero-foot .cue", "英雄区提示"),
        (".board .sub", "面板副标"),
        (".row .lab", "行标签"),
        (".lever label", "档位标签"),
        (".lever label span", "档位副标"),
        (".flap-cap", "翻牌图注"),
        (".market .mnote", "市场注"),
        (".card .facts", "卡片事实"),
        (".card .name", "卡片名"),
        (".path .seq", "路径序列"),
        (".legend", "图例"),
        ("#showcase-bar .sb-brand", "顶栏品牌"),
        ("#showcase-bar .sb-back", "顶栏返回"),
        ("#showcase-backlink", "返回链胶囊"),
        ("#showcase-backlink span", "返回链文字"),
        (".blk .face", "阶梯块面"),
        (".blk.lit .face", "高亮块面"),
        (".quote-block .attr", "引文署名"),
        (".quote-block .say", "引文释义"),
        (".verdict", "结论"),
        ("h1", "主标题"),
        ("h2", "大标题"),
        (".path .pct", "概率大字"),
    ]
    meas = [measure(s, n) for s, n in targets]
    R["evidence"]["contrast_measured"] = meas
    fails = [m for m in meas if m.get("pass") is False]
    if fails: bad("实测对比度 < 需求", fails)
    else: ok("实测对比度", f"{len([m for m in meas if 'cr' in m])} 个取样点全部达标")

    # backlink 专项：胶囊外页面底色
    bl = page.query_selector("#showcase-backlink")
    if bl:
        bb = bl.bounding_box()
        st = page.evaluate("""() => {const a=document.getElementById('showcase-backlink');
            const cs=getComputedStyle(a);
            return {color:cs.color, bg:cs.backgroundColor, opacity:cs.opacity, cls:a.className,
                    font:cs.fontSize+' '+cs.fontWeight};}""")
        # 胶囊外 6px 处页面底色
        shot = page.screenshot(clip={"x": max(0,bb["x"]-14), "y": max(0,bb["y"]-6),
                                     "width": min(300, 1260), "height": min(120, 800)})
        W, H, C, rows = decode_png(shot)
        cnt = collections.Counter()
        for r in rows:
            for i in range(0, len(r), C): cnt[(r[i], r[i+1], r[i+2])] += 1
        R["evidence"]["backlink"] = {"computed": st, "box": bb,
                                     "nearby_colors": ["#%02x%02x%02x(%d)" % (c[0],c[1],c[2],n) for c,n in cnt.most_common(6)]}

    # ---------- D. 截图（桌面 + 手机整页） ----------
    page.set_viewport_size({"width": 1260, "height": 800}); page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0,0)"); page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(NOTES, "457-rate-ladder-desktop.png"), full_page=True)
    page.set_viewport_size({"width": 375, "height": 812}); page.wait_for_timeout(500)
    page.evaluate("window.scrollTo(0,0)"); page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(NOTES, "457-rate-ladder-mobile.png"), full_page=True)

    br.close()

R["summary"] = {"pass": len(R["pass"]), "fail": len(R["fail"]), "warn": len(R["warn"])}
print(json.dumps(R, ensure_ascii=False, indent=1))
