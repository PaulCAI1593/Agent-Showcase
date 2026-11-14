#!/usr/bin/env python3
"""选题423 过程材料：作品预览截图（桌面整页 / 分节 / 移动端）。

用法： python3 2026-11-09-ai-investment-ledger-shoot.py
输出： works/2026-11-09/notes/2026-11-09-ai-investment-ledger-preview-*.png
约束： 只发 file:// 与 data: 请求，外部请求一律 abort（作品契约：零远程依赖）。
"""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # showcase/
REL = "works/2026-11-09/research/2026-11-09-ai-investment-ledger.html"
OUT = os.path.join(ROOT, "works", "2026-11-09", "notes")
PREFIX = "2026-11-09-ai-investment-ledger-preview"


def route(route):
    u = route.request.url
    if u.startswith(("file://", "data:", "about:")):
        route.continue_()
    else:
        route.abort()


def main():
    os.makedirs(OUT, exist_ok=True)
    url = "file://" + os.path.join(ROOT, REL)
    with sync_playwright() as p:
        b = p.chromium.launch(
            executable_path="/usr/bin/chromium",
            args=["--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=1"],
        )
        pg = b.new_page(viewport={"width": 1260, "height": 900})
        pg.route("**/*", route)
        pg.goto(url, wait_until="load")
        pg.wait_for_timeout(1500)
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(900)
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(500)

        pg.screenshot(path=os.path.join(OUT, PREFIX + "-desktop-full.png"), full_page=True)

        # 分节截图（按 h2 定位）
        heads = pg.query_selector_all("section h2")
        names = ["01-verdict", "02-metrics", "03-ledger", "04-intent",
                 "05-action", "06-support", "07-reconcile", "08-timeline", "09-evidence"]
        for i, h in enumerate(heads[:len(names)]):
            sec = h.evaluate_handle("el => el.closest('section')")
            sec.as_element().screenshot(
                path=os.path.join(OUT, PREFIX + "-" + names[i] + ".png"))

        # 移动端
        m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        m.route("**/*", route)
        m.goto(url, wait_until="load")
        m.wait_for_timeout(1500)
        m.screenshot(path=os.path.join(OUT, PREFIX + "-mobile.png"), full_page=True)

        # 控制台错误检查
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.reload(wait_until="load")
        pg.wait_for_timeout(800)
        print("pageerror:", errs or "none")
        b.close()
    print("done ->", OUT)


if __name__ == "__main__":
    main()
