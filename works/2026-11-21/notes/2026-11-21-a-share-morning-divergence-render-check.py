#!/usr/bin/env python3
"""渲染验证：双视口 + 溢出 + console + 语义块计数（#461 交付用）"""
import json, pathlib
from playwright.sync_api import sync_playwright

TARGET = pathlib.Path("/app/working/shared/showcase/works/2026-11-21/research/2026-11-21-a-share-morning-divergence.html")
NOTES = TARGET.parent.parent / "notes"
URL = TARGET.as_uri()

VIEWPORTS = [("desktop", 1440, 900), ("mobile", 390, 844)]
report = {}

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for name, w, h in VIEWPORTS:
        page = browser.new_page(viewport={"width": w, "height": h})
        errors = []
        page.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.goto(URL, wait_until="load")
        page.wait_for_timeout(800)
        data = page.evaluate("""() => {
          const de = document.documentElement;
          const overflow = de.scrollWidth - de.clientWidth;
          const bad = [];
          document.querySelectorAll('*').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.right > de.clientWidth + 1 && el.offsetParent !== null) {
              const cn = (el.className && el.className.baseVal !== undefined) ? el.className.baseVal : (el.className || '');
              bad.push(el.tagName + '.' + cn + ' right=' + Math.round(r.right));
            }
          });
          return {
            overflowX: overflow,
            overflowing: bad.slice(0, 8),
            pageHeight: de.scrollHeight,
            metrics: document.querySelectorAll('.metrics .metric').length,
            metricLabels: [...document.querySelectorAll('.metric-label')].map(e => e.textContent.trim()),
            verdicts: document.querySelectorAll('.verdict').length,
            timeline: document.querySelectorAll('.timeline-item').length,
            evidence: document.querySelectorAll('.evidence-item').length,
            svg: document.querySelectorAll('svg').length,
            tables: document.querySelectorAll('table.tbl').length,
            claims: JSON.parse(document.getElementById('claims').textContent).length,
            beat: document.querySelector('meta[name="showcase-beat"]').content,
            serifLoaded: document.fonts.check("16px 'Noto Serif SC'"),
            placeholders: document.body.innerText.includes('{{')
          };
        }""")
        data["consoleErrors"] = errors
        report[name] = data
        page.screenshot(path=str(NOTES / ("2026-11-21-a-share-morning-divergence-preview-%s.png" % name)), full_page=False)
        page.close()
    browser.close()

print(json.dumps(report, ensure_ascii=False, indent=2))
