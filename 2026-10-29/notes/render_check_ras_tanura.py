#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渲染实测 · 选题404「拉斯塔努拉之后，中东风险溢价为何不涨反跌」
数析 · 2026-10-30 · V1

做四件事：
  1. 真跑一遍页面，抓 console 报错、pageerror、资源 404
  2. 核对封闭语义词汇表与断言层的结构
  3. 检查 375px 窄屏是否出现横向滚动
  4. 出预览截图（落 notes/）

用法：python3 render_check_ras_tanura.py
"""

import json
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))          # showcase/
REL = "2026-10-29/research/2026-10-29-ras-tanura-risk-premium.html"
PAGE = os.path.join(ROOT, REL)
SHOTS = HERE
CHROME = "/usr/bin/chromium"

# 封闭语义词汇表（契约第 7 条）
VOCAB = {
    ".metrics": 1, ".metric": 8, ".metric-value": 8, ".metric-label": 8,
    ".metric-source": 8, ".verdict": 1, ".timeline": 1, ".timeline-item": 11,
    ".evidence": 1, ".evidence-item": 7,
}

report = {"file": REL, "checks": [], "shots": []}


def check(name, ok, detail=""):
    report["checks"].append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print(("  PASS  " if ok else "  FAIL  ") + name + ("  " + str(detail) if detail else ""))
    return ok


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--font-render-hinting=none"],
        )
        page = browser.new_page(viewport={"width": 1280, "height": 900},
                                device_scale_factor=2)

        console_errors, page_errors, failed = [], [], []
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.on("requestfailed", lambda r: failed.append(f"{r.url} :: {r.failure}"))
        page.on("response", lambda r: failed.append(f"{r.url} :: HTTP {r.status}")
                if r.status >= 400 else None)

        page.goto("file://" + PAGE, wait_until="load")
        page.wait_for_timeout(1200)

        # ── 1. 运行时错误 ────────────────────────────────────────
        check("无 console error", not console_errors, console_errors[:5])
        check("无 pageerror", not page_errors, page_errors[:5])
        check("无资源加载失败 / 404", not failed, failed[:5])

        # ── 2. 封闭语义词汇表 ────────────────────────────────────
        for sel, want in VOCAB.items():
            got = page.locator(sel).count()
            check(f"词汇表 {sel} = {want}", got == want, f"实际 {got}")

        # ── 3. 声明与追踪线 ──────────────────────────────────────
        beat = page.locator('meta[name="showcase-beat"]').get_attribute("content")
        check("showcase-beat = 地缘与能源", beat == "地缘与能源", beat)
        raw = page.evaluate("""() => {
            const s = document.getElementById('claims');
            return s ? s.textContent : null;
        }""")
        claims = json.loads(raw)
        check("claims 条目数 3~8", 3 <= len(claims) <= 8, len(claims))
        check("claims 每条含 value/label/quote",
              all(all(k in c and c[k] for k in ("value", "label", "quote")) for c in claims))
        body = page.evaluate("() => document.body.innerText")
        punct = "，。、；：""''（）()·—…!！?？「」《》"
        norm = "".join(ch for ch in body if not ch.isspace() and ch not in punct)
        miss = [c["quote"] for c in claims
                if "".join(ch for ch in c["quote"] if not ch.isspace() and ch not in punct) not in norm]
        check("quote 逐字存在于渲染正文", not miss, miss)
        check("占位符已全部替换", "{{" not in body and "}}" not in body)
        check("正文无外链", page.locator("a[href^='http']").count() == 0)

        # ── 4. 字体与渲染 ────────────────────────────────────────
        serif_ok = page.evaluate("""() => {
            const h = document.querySelector('h1');
            return getComputedStyle(h).fontFamily;
        }""")
        check("中文衬线已加载", "Noto Serif SC" in serif_ok or "Songti" in serif_ok
              or "Source Han Serif" in serif_ok, serif_ok[:70])
        fonts_loaded = page.evaluate("() => document.fonts.status")
        check("document.fonts 已就绪", fonts_loaded in ("loaded", "unloaded"), fonts_loaded)

        # ── 5. 三条硬口径是否写进正文 ────────────────────────────
        for key, needle in [
            ("口径① 据彭博引述知情人士", "据彭博引述知情人士"),
            ("口径① 沙方未确认", "沙特当局未确认"),
            ("口径② 炼厂加工产能", "原油加工产能"),
            ("口径② 非全球占比", "不是全球占比"),
            ("口径③ 历史类比", "历史类比"),
        ]:
            check(f"正文含「{key}」", needle in body)

        # ── 6. 窄屏无横向滚动 ────────────────────────────────────
        page.set_viewport_size({"width": 375, "height": 780})
        page.wait_for_timeout(500)
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        check("375px 无横向滚动", overflow <= 1, f"溢出 {overflow}px")
        page.set_viewport_size({"width": 1280, "height": 900})
        page.wait_for_timeout(400)

        # ── 7. 预览截图 ──────────────────────────────────────────
        # section 序号：1 结论带 / 2 关键数据 / 3 口径闸门 / 4 价格路径 /
        #              5 四层机制 / 6 进程 / 7 证据
        plan = [
            ("404-preview-01-hero.png", "header.masthead"),
            ("404-preview-02-verdict.png", "section.verdict-band"),
            ("404-preview-03-metrics.png", "section:nth-of-type(2)"),
            ("404-preview-04-caliber.png", "section:nth-of-type(3)"),
            ("404-preview-05-path.png", "section:nth-of-type(4)"),
            ("404-preview-06-mechanism.png", "section:nth-of-type(5)"),
            ("404-preview-07-timeline.png", "section:nth-of-type(6)"),
            ("404-preview-08-evidence.png", "section:nth-of-type(7)"),
        ]
        for fname, sel in plan:
            loc = page.locator(sel).first
            loc.scroll_into_view_if_needed()
            page.wait_for_timeout(450)
            out = os.path.join(SHOTS, fname)
            loc.screenshot(path=out)
            report["shots"].append(fname)
            print("  SHOT  ", fname, os.path.getsize(out), "bytes")

        browser.close()

    out_json = os.path.join(SHOTS, "404-render-check-20261030.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    failed_n = sum(1 for c in report["checks"] if not c["ok"])
    print(f"\n共 {len(report['checks'])} 项检查，失败 {failed_n} 项。结果写入 {out_json}")
    return 1 if failed_n else 0


if __name__ == "__main__":
    sys.exit(main())
