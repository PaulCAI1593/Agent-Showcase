#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""选题420 分段截图（用于目视检查排版，交付后保留在 notes/）"""
import pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
URL = (HERE / "../research/2026-11-08-ai-valuation-meets-hikes.html").resolve().as_uri()
STEM = "2026-11-08-ai-valuation-meets-hikes"

SECTIONS = [
    ("01-masthead", "header.masthead"),
    ("02-verdict", "section.verdict-band"),
    ("03-metrics", "main > section:nth-of-type(2)"),
    ("04-frame", "main > section:nth-of-type(3)"),
    ("05-primary", "main > section:nth-of-type(4)"),
    ("06-macro", "main > section:nth-of-type(5)"),
    ("07-equity", "main > section:nth-of-type(6)"),
    ("08-mech", "main > section:nth-of-type(7)"),
    ("09-timeline", "main > section:nth-of-type(8)"),
    ("10-gates", "main > section:nth-of-type(9)"),
    ("11-evidence", "main > section:nth-of-type(10)"),
    ("12-colophon", "footer.colophon"),
]

with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    ctx = br.new_context(viewport={"width": 1440, "height": 1000})
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1500)
    for name, sel in SECTIONS:
        loc = page.locator(sel).first
        try:
            loc.scroll_into_view_if_needed()
            page.wait_for_timeout(1100)
            loc.screenshot(path=str(HERE / f"{STEM}-preview-{name}.png"))
            print("ok", name)
        except Exception as e:
            print("fail", name, e)
    br.close()
