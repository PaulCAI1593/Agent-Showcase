#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渲染实测 · 选题419「三个季度涨近 4 倍——AI 吃掉的存储，最后写进你的 iPhone 价签」
创艺 · 2026-11-08 · V1

做六件事：
  1. 真跑一遍页面，抓 console 报错、pageerror、资源 404
  2. 核对 showcase-beat 与断言层（6 条 quote 在渲染后正文逐字命中）
  3. 核对交互：仪表盘切换 / 传导链点击 / 滑块推演 / 爆炸图 / 账单打印
  4. 核对硬约束：零远程依赖、375px 无横向溢出、prefers-reduced-motion 可用
  5. 核对边界：不出现 10-15 既有标签数值（2025Q4 合约价涨幅、34% 物料占比）
  6. 出预览截图（落 notes/）

用法：python3 render_check_memory_price.py
"""

import json
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))          # showcase/
REL = "2026-11-06/creative/2026-11-06-memory-price-apple-pass-through.html"
PAGE = os.path.join(ROOT, REL)
SHOTS = HERE
CHROME = "/usr/bin/chromium"

CLAIMS = [
    ("近 4 倍", "存储芯片价格三个季度涨幅", "AI需求在三个季度内使存储芯片价格翻了近四倍"),
    ("至少五款", "苹果计划新 iPhone 款数", "推出至少五款新iPhone并准备1000万台折叠屏机"),
    ("1000 万台", "折叠屏 iPhone 备货量", "推出至少五款新iPhone并准备1000万台折叠屏机"),
    ("-8.13%", "希捷单日跌幅（11-04）", "存储股希捷跌8.13%"),
    ("-7.00%", "美光单日跌幅（11-04）", "美光跌7.00%"),
    ("600 美元", "iPhone 18 Pro 256GB→1TB 终端加价（美版）",
     "升级至1TB版本时,物料成本增量约为192美元,终端售价加价600美元"),
]

BANNED = ["2025Q4", "34%", "物料成本中的占比", "涨超 40%", "+40%"]

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + (" — " + str(detail) if detail else ""))


def run():
    errors, pageerrors, failed = [], [], []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: pageerrors.append(str(e)))
        page.on("requestfailed", lambda r: failed.append(r.url))
        page.goto("file://" + PAGE, wait_until="load")
        page.wait_for_timeout(1600)

        # 1. 基本
        title = page.title()
        check("<title> 含作品名", "iPhone 价签" in title, title)
        beat = page.get_attribute('meta[name="showcase-beat"]', "content")
        check("showcase-beat = 成本与普惠", beat == "成本与普惠", beat)
        check("无 console error", not errors, errors[:3])
        check("无 pageerror", not pageerrors, pageerrors[:3])
        check("无资源加载失败", not failed, failed[:3])

        # 2. 远程依赖
        remote = page.eval_on_selector_all(
            "script[src],link[href],img[src],iframe[src]",
            "els => els.map(e => e.getAttribute('src') || e.getAttribute('href'))"
            ".filter(u => /^https?:/i.test(u))")
        check("零远程依赖", not remote, remote)

        # 3. 断言层
        claims = json.loads(page.eval_on_selector("#claims", "e => e.textContent"))
        check("claims 条数 3~8", 3 <= len(claims) <= 8, len(claims))
        body_text = page.inner_text("body")
        file_text = open(PAGE, encoding="utf-8").read()
        for v, l, q in CLAIMS:
            hit_dom = q in body_text.replace("\n", "")
            hit_file = q in file_text
            check("quote 命中（正文+文件）: " + q[:24], hit_dom and hit_file,
                  {"dom": hit_dom, "file": hit_file})
        got = [(c["value"], c["label"], c["quote"]) for c in claims]
        check("claims 与交付清单一致", got == CLAIMS, got[:2])

        # 4. 图表
        check("价格图 SVG 已绘制", page.eval_on_selector_all("#chart svg path", "e => e.length") >= 2)
        check("三季柱已生成", page.eval_on_selector_all("#gbars .fill", "e => e.length") == 3)

        # 5. 交互 A：仪表盘切换
        page.click("#tab-drop")
        page.wait_for_timeout(500)
        vis = page.is_visible("#p-drop") and page.is_hidden("#p-x")
        widths = page.eval_on_selector_all("#p-drop .fill", "els => els.map(e => e.getBoundingClientRect().width)")
        check("仪表盘切换到五股跌幅", vis and all(w > 20 for w in widths), [round(w) for w in widths])
        page.click("#tab-stock")
        page.wait_for_timeout(1800)
        lit = page.eval_on_selector_all("#dots i.on", "e => e.length")
        check("备货点阵动画点亮 100 点", lit == 100, lit)
        page.click("#tab-x")

        # 6. 交互 B：传导链
        page.click('.node[data-n="5"]')
        page.wait_for_timeout(250)
        d5 = page.is_visible('.node-detail[data-d="5"]')
        d1 = page.is_hidden('.node-detail[data-d="1"]')
        check("传导链节点 5 展开、节点 1 收起", d5 and d1, {"d5": d5, "d1": d1})

        # 7. 交互 C：滑块推演
        before = page.inner_text("#simPrice")
        page.eval_on_selector("#squeeze", "el => { el.value = 80; el.dispatchEvent(new Event('input')) }")
        page.wait_for_timeout(150)
        after = page.inner_text("#simPrice")
        fine = page.inner_text("#simFine")
        check("滑块推演联动且标注非断言", before != after and "非断言" in fine, {"before": before, "after": after})

        # 8. 交互 D：爆炸图
        page.click("#blastToggle")
        page.wait_for_timeout(400)
        opened = page.eval_on_selector("#blast", "e => e.classList.contains('open')")
        page.click('.layer[data-k="board"]')
        page.wait_for_timeout(400)
        det = page.inner_text("#layerDetail")
        check("爆炸图合上/点选图层切换详情", (not opened) and "主板" in det, det.split("\n")[0])

        # 9. 交互 E：账单打印
        page.click("#printBtn")
        page.wait_for_timeout(3200)
        shown = page.eval_on_selector_all(".rline.show", "e => e.length")
        total = page.eval_on_selector_all(".rline", "e => e.length")
        stamped = page.eval_on_selector("#stamp", "e => e.classList.contains('on')")
        check("账单逐行打印 + 盖章", shown == total and stamped, {"shown": shown, "total": total, "stamped": stamped})

        # 10. 边界：不引用 10-15 既有标签
        for b in BANNED:
            check("边界未引用: " + b, b not in file_text)

        # 11. 截图
        shots = [
            ("419-preview-01-hero.png", "#hero"),
            ("419-preview-02-growth.png", "#act-growth"),
            ("419-preview-04-climax.png", "#act-climax"),
            ("419-preview-05-close.png", "#act-close"),
            ("419-preview-06-evidence.png", "#evidence"),
        ]
        for name, sel in shots:
            loc = page.locator(sel)
            loc.scroll_into_view_if_needed()
            page.wait_for_timeout(1100)
            loc.screenshot(path=os.path.join(SHOTS, name))
        page.evaluate("document.querySelector('#journey').scrollIntoView()")
        page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(SHOTS, "419-preview-03-journey.png"))
        # 仪表盘另两张
        page.evaluate("document.querySelector('#act-growth').scrollIntoView()")
        page.click("#tab-drop"); page.wait_for_timeout(900)
        page.locator("#act-growth .dash").screenshot(path=os.path.join(SHOTS, "419-preview-02b-dash-drops.png"))
        page.click("#tab-stock"); page.wait_for_timeout(2000)
        page.locator("#act-growth .dash").screenshot(path=os.path.join(SHOTS, "419-preview-02c-dash-stock.png"))
        page.click("#tab-x")
        page.locator("#act-growth .figure").screenshot(path=os.path.join(SHOTS, "419-preview-02d-price-chart.png"))

        # 12. 375px 窄屏
        page.set_viewport_size({"width": 375, "height": 780})
        page.wait_for_timeout(600)
        sw = page.evaluate("document.documentElement.scrollWidth")
        check("375px 无横向溢出", sw <= 376, sw)
        page.screenshot(path=os.path.join(SHOTS, "419-preview-07-mobile-375.png"), full_page=False)
        page.locator("#hero").screenshot(path=os.path.join(SHOTS, "419-preview-07b-mobile-hero.png"))

        # 13. prefers-reduced-motion
        ctx2 = browser.new_context(viewport={"width": 1280, "height": 900},
                                   reduced_motion="reduce")
        p2 = ctx2.new_page()
        rm_err = []
        p2.on("pageerror", lambda e: rm_err.append(str(e)))
        p2.goto("file://" + PAGE, wait_until="load")
        p2.wait_for_timeout(900)
        hero_visible = p2.is_visible("h1")
        receipt_text = p2.inner_text("#receipt")
        check("reduced-motion 下页面可用", hero_visible and not rm_err and "换机的你" in receipt_text, rm_err[:2])
        ctx2.close()
        browser.close()

    fails = [r for r in results if not r[1]]
    out = {"total": len(results), "pass": len(results) - len(fails), "fail": len(fails),
           "results": [{"name": n, "ok": ok, "detail": str(d)} for n, ok, d in results]}
    with open(os.path.join(SHOTS, "419-render-check-20261108.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\n== %d/%d PASS ==" % (out["pass"], out["total"]))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(run())
