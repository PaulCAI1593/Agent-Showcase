#!/usr/bin/env python3
"""选题454 局部放大截图（polish 复检）：先滚动触发唯一动效并等动画完成。"""
import os
from playwright.sync_api import sync_playwright

ROOT = "/app/working/shared/showcase"
HTML = os.path.join(ROOT, "works/2026-11-19/research/2026-11-19-shenzhen-summit-eve.html")
OUT = os.path.join(ROOT, "works/2026-11-19/notes")
URL = "file://" + HTML

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/usr/bin/chromium",
                           args=["--no-sandbox", "--disable-dev-shm-usage"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    p = ctx.new_page()
    p.goto(URL, wait_until="load")
    p.wait_for_timeout(500)
    # 触发全部 IntersectionObserver 并等动效结束
    p.evaluate("""async () => {
        const h = document.body.scrollHeight;
        for (let y = 0; y < h; y += 600) { window.scrollTo(0, y); await new Promise(r=>setTimeout(r,40)); }
        window.scrollTo(0, 0);
    }""")
    p.wait_for_timeout(1800)
    for sel, name in [(".metrics", "454-metrics"), ("#fig-hike", "454-fig2"),
                      ("#fig-gold", "454-fig1")]:
        el = p.query_selector(sel)
        if el:
            el.scroll_into_view_if_needed()
            p.wait_for_timeout(300)
            el.screenshot(path=os.path.join(OUT, name + ".png"))
            print("saved", name)
    # 单元格溢出检查（keep-all 是否造成横向溢出）
    overflow = p.evaluate("""() => {
        return [...document.querySelectorAll('.metric, .metric-value, .metric-label, .metric-source')]
          .filter(e => e.scrollWidth > e.clientWidth + 1)
          .map(e => ({cls: e.className, sw: e.scrollWidth, cw: e.clientWidth,
                      t: (e.textContent||'').slice(0,24)}));
    }""")
    print("cell_overflow:", overflow)
    b.close()
