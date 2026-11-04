"""任务#354 选题391 口径修订后复验 — 总指挥亲自验证 (2026-10-24)."""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

HTML = pathlib.Path("/app/working/shared/showcase/2026-10-24/creative/2026-10-24-meta-privacy-price-slider.html")
URL = HTML.as_uri()
NOTES = HTML.parent.parent / "notes"

results, errors = [], []
def chk(name, cond, detail=""):
    results.append((name, bool(cond), detail))

def setprice(pg, v):
    pg.evaluate("""(v) => {const s=document.querySelector('#priceRange');
        s.value=v; s.dispatchEvent(new Event('input',{bubbles:true}));}""", v)
    pg.wait_for_timeout(650)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/chromium",
                          args=["--no-sandbox", "--disable-dev-shm-usage",
                                "--force-device-scale-factor=1"])
    pg = b.new_page(viewport={"width": 1366, "height": 900})
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(3400)

    src = HTML.read_text(encoding="utf-8")
    # --- 口径修订内容 ---
    chk("口径说明改为三条", "请先读这三条纠错" in src)
    chk("新增③ 180亿≠隐私和解金", "180 亿 ≠ 隐私和解金" in src)
    chk("③含隐私轨道4.59亿", "约 4.59 亿" in src)
    chk("③含171/170亿口径对照", "171" in src and "170" in src)
    chk("对比面板A标注合计口径", "180亿美元（合计口径）" in src)
    chk("9.42亿来源拆分", "8 月 6 日法官追加 5.67" in src)
    chk("时间轴口径同步", "其中隐私轨道仅约 4.59 亿" in src)
    chk("旧两行表述已清除", "请先读这两条纠错" not in src)
    chk("红线②非AI监管仍在", "与 AI 监管无关" in src)
    chk("金额未改动($18,000,000,000)", "$18,000,000,000" in src)

    # --- 交互复验 ---
    chk("滑块存在", pg.locator("#priceRange").count() == 1)
    chk("滑块默认值569", pg.locator("#priceRange").get_attribute("value") == "569")
    tot = pg.locator("#totalOdo").inner_text()
    chk("默认总额≈249.8亿", "24,979,100,000" in tot, tot)
    chk("五刻度渲染", pg.locator("#tickLayer .stem").count() == 5,
        str(pg.locator("#tickLayer .stem").count()))
    lit0 = pg.locator("#tickLayer .stem.lit").count()
    chk("默认已亮起刻度≥4", lit0 >= 4, str(lit0))

    setprice(pg, 5000)
    tot2 = pg.locator("#totalOdo").inner_text()
    chk("拖到$5000=2195亿", "219,500,000,000" in tot2, tot2)
    chk("上限时5刻度全亮", pg.locator("#tickLayer .stem.lit").count() == 5,
        str(pg.locator("#tickLayer .stem.lit").count()))
    chk("上限百分比100", "100" in pg.locator("#pctVal").inner_text(),
        pg.locator("#pctVal").inner_text())

    setprice(pg, 0)
    chk("归零", "0" in pg.locator("#totalOdo").inner_text().replace(",", ""),
        pg.locator("#totalOdo").inner_text())
    chk("归零0刻度", pg.locator("#tickLayer .stem.lit").count() == 0,
        str(pg.locator("#tickLayer .stem.lit").count()))

    setprice(pg, 569)
    chk("chip缓动跳回569", "24,979,100,000" in pg.locator("#totalOdo").inner_text())

    # 时间轴
    chk("时间轴7节点", pg.locator(".tl-card").count() == 7, str(pg.locator(".tl-card").count()))
    pg.evaluate("""() => {const r=document.querySelector('#tlRange');
        r.value=6; r.dispatchEvent(new Event('input',{bubbles:true}));}""")
    pg.wait_for_timeout(400)
    chk("时间轴可滑到2026.10", pg.evaluate(
        "() => document.querySelector('#tlRange').value") == "6")

    # 对比切换
    pg.locator("#cmpB").click(); pg.wait_for_timeout(450)
    chk("B面板激活", "on" in (pg.locator("#panelB").get_attribute("class") or ""))
    chk("A面板互斥关闭", "on" not in (pg.locator("#panelA").get_attribute("class") or ""))
    pg.locator("#cmpA").click(); pg.wait_for_timeout(450)
    chk("A面板可切回", "on" in (pg.locator("#panelA").get_attribute("class") or ""))

    over = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    chk("无横向溢出", over <= 1, f"overflow={over}px")

    # 重拍受影响预览
    pg.locator("#cmpA").scroll_into_view_if_needed(); pg.wait_for_timeout(600)
    pg.locator(".cmp-panelA").screenshot(path=str(NOTES / "preview-compare.png"))
    corr = pg.locator(".corrections")
    corr.scroll_into_view_if_needed(); pg.wait_for_timeout(600)
    corr.screenshot(path=str(NOTES / "preview-corrections.png"))
    pg.set_viewport_size({"width": 1366, "height": 4200})
    pg.wait_for_timeout(900)
    pg.screenshot(path=str(NOTES / "preview-full.png"), full_page=True)
    b.close()

ok = all(r[1] for r in results) and not errors
print(json.dumps({"console_errors": errors, "pass": ok,
                  "passed": sum(1 for r in results if r[1]), "total": len(results),
                  "checks": [{"name": n, "ok": o, "detail": d} for n, o, d in results]},
                 ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
