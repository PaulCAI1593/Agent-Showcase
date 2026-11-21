
import json, os, sys
from playwright.sync_api import sync_playwright

HTML = "/app/working/shared/showcase/works/2026-11-21/creative/2026-11-21-tic-holders-ledger.html"
NOTES = "/app/working/shared/showcase/works/2026-11-21/notes"
URL = "file://" + HTML
res = {"overflow": {}, "interactions": {}, "console": [], "screens": []}

def run(pw, width, height, tag, full=True):
    b = pw.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
    pg.on("console", lambda m: res["console"].append(f"{tag}:{m.type}:{m.text}") if m.type in ("error","warning") else None)
    pg.on("pageerror", lambda e: res["console"].append(f"{tag}:pageerror:{e}"))
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(700)
    res["overflow"][tag] = pg.evaluate("() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth, bw: document.body.scrollWidth})")
    if not full:
        # interactions only on desktop pass
        def txt(sel): return pg.inner_text(sel)
        before = txt("#readout")
        pg.click('.seg-btn[data-cal="stock"]'); pg.wait_for_timeout(150)
        res["interactions"]["caliber_stock"] = (before != txt("#readout")) and "期末余额" in txt("#readout")
        pg.click('.seg-btn[data-cal="flow"]'); pg.wait_for_timeout(150)
        res["interactions"]["caliber_flow"] = "净额" in txt("#readout")
        pg.click('.seg-btn[data-cal="both"]'); pg.wait_for_timeout(150)
        pg.click('.leg[data-seg="2"]'); pg.wait_for_timeout(200)
        res["interactions"]["waterfall_seg2"] = "1563" in txt("#wfCap")
        pg.click('.leg[data-seg="1"]'); pg.click('.leg[data-seg="3"]'); pg.wait_for_timeout(300)
        res["interactions"]["stamp"] = pg.evaluate("() => document.getElementById('wfStamp').classList.contains('on')")
        res["interactions"]["progress"] = txt("#wfProgTxt")
        pg.click("#segRest"); pg.wait_for_timeout(150)
        res["interactions"]["bar_rest"] = "未确认" in txt("#barCallout")
        pg.click("#segCn"); pg.wait_for_timeout(100)
        res["interactions"]["bar_cn"] = "6.1%" in txt("#barCallout")
        pg.click('.m[data-m="7"]'); pg.wait_for_timeout(150)
        res["interactions"]["month7"] = "未给出" in txt("#tlDetail")
        pg.click('.m[data-m="9"]'); pg.wait_for_timeout(100)
        pg.click('.chip[data-v="rate"]'); pg.wait_for_timeout(150)
        res["interactions"]["chip_rate"] = "收益率" in txt("#valPanel")
        # keyboard focus visible check
        res["interactions"]["focus_ring"] = pg.evaluate("""() => {
            const b = document.querySelector('.seg-btn'); b.focus();
            const s = getComputedStyle(b, ':focus-visible'); return !!s;
        }""")
        # touch target sizes
        res["interactions"]["small_targets"] = pg.evaluate("""() => {
            const out = [];
            document.querySelectorAll('button').forEach(b => {
                const r = b.getBoundingClientRect();
                if (r.height > 0 && r.height < 24) out.push(b.className + ':' + Math.round(r.height));
            });
            return out;
        }""")
    path = os.path.join(NOTES, f"2026-11-21-tic-preview-{tag}.png")
    pg.screenshot(path=path, full_page=full)
    res["screens"].append(path)
    b.close()

with sync_playwright() as pw:
    run(pw, 1280, 900, "desktop", full=True)
    run(pw, 375, 812, "mobile", full=True)
    run(pw, 1280, 900, "interact", full=False)

print(json.dumps(res, ensure_ascii=False, indent=1))
