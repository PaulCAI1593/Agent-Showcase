#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""选题420 渲染复核：真实浏览器加载 + 控制台错误 / 资源 404 / 横向滚动 / 图表是否画出。
输出：同目录 preview PNG ×4 + render_check_420.json
"""
import json, os, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
REL = "../research/2026-11-08-ai-valuation-meets-hikes.html"
URL = (HERE / REL).resolve().as_uri()
STEM = "2026-11-08-ai-valuation-meets-hikes"
VIEWPORTS = [
    ("desktop", 1440, 1000),
    ("desktop-mid", 1024, 900),
    ("desktop-low", 800, 900),
    ("mobile", 390, 844),
]

report = {"url": URL, "viewports": [], "console_errors": [], "page_errors": [], "failed_requests": []}

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for name, w, h in VIEWPORTS:
        ctx = browser.new_context(viewport={"width": w, "height": h},
                                  device_scale_factor=2 if name == "mobile" else 1)
        page = ctx.new_page()
        page.on("console", lambda m: report["console_errors"].append({"type": m.type, "text": m.text})
                if m.type == "error" else None)
        page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
        page.on("requestfailed", lambda r: report["failed_requests"].append(r.url))
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(1200)

        m = page.evaluate("""() => ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            canvases: [...document.querySelectorAll('canvas')].map(c => ({
                id: c.id, w: c.width, h: c.height,
                blank: (c.getContext('2d').getImageData(0,0,c.width,c.height).data
                        .every((v,i)=> i%4===3 ? true : v===0))
            })),
            h1: document.querySelectorAll('h1').length,
            sections: document.querySelectorAll('main section').length,
            claims: JSON.parse(document.getElementById('claims').textContent).length,
            beat: document.querySelector('meta[name=showcase-beat]').content
        })""")
        m["viewport"] = name
        m["overflow_x"] = m["scrollWidth"] > m["clientWidth"]
        report["viewports"].append(m)

        page.screenshot(path=str(HERE / f"{STEM}-preview-{name}.png"), full_page=True)
        ctx.close()
    browser.close()

out = HERE / "render_check_420.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
print("written:", out)
