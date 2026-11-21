#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import sys
H = "/app/working/shared/showcase/works/2026-11-20/creative/2026-11-20-rate-ladder-december.html"
N = "/app/working/shared/showcase/works/2026-11-20/notes"
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    pg = br.new_context(viewport={"width":1260,"height":800}).new_page()
    pg.goto("file://"+H, wait_until="load"); pg.wait_for_timeout(1500)
    # 滚到底再回顶，让所有 reveal 就位
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(1600)
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(600)
    pg.screenshot(path=N+"/457-rate-ladder-desktop-after.png", full_page=True)
    # lever 特写
    el = pg.query_selector(".lever"); el.scroll_into_view_if_needed(); pg.wait_for_timeout(900)
    box = el.bounding_box()
    pg.screenshot(path=N+"/457-rate-ladder-lever-after.png",
                  clip={"x":box["x"]-14,"y":box["y"]-40,"width":box["width"]+28,"height":box["height"]+80})
    br.close()
print("shots done")
