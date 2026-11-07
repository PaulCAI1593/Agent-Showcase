#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渲染实测 · 选题418「94.62美元与-8.67%——伊朗递出和平方案当天，油价跌破100美元」
研析 · 2026-11-07 · V1

做五件事：
  1. 真跑一遍页面，抓 console 报错、pageerror、资源 404
  2. 核对封闭语义词汇表与断言层结构（7 条 quote 在渲染后正文逐字命中）
  3. 核对硬口径：标签日期无 11-05、盘中 value 带「盘中」、JPM 定性判断在正文
  4. 检查 375px 窄屏横向溢出
  5. 出预览截图（落 notes/）

用法：python3 render_check_oil_risk.py
"""

import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))          # showcase/
REL = "2026-11-06/research/2026-11-06-oil-risk-premium-reset.html"
PAGE = os.path.join(ROOT, REL)
SHOTS = HERE
CHROME = "/usr/bin/chromium"

# 封闭语义词汇表（契约第 7 条）
VOCAB = {
    ".metrics": 1, ".metric": 8, ".metric-value": 8, ".metric-label": 8,
    ".metric-source": 8, ".verdict": 1, ".timeline": 1, ".timeline-item": 6,
    ".evidence": 1, ".evidence-item": 10,
}

# 断言层 7 条（value / label / quote 必须与 script#claims 一致）
CLAIMS = [
    ("94.62 美元/桶", "布伦特 1 月合约结算价（11-04）", "布伦特1月跌8.67%收94.62美元"),
    ("88.12 美元/桶", "WTI 12月合约结算价（11-04）", "WTI 12月跌8.29%收88.12美元/桶"),
    ("4063 美元/盎司", "现货黄金结算价（11-04）", "现货黄金涨超3%至4063美元上方、创8月以来最大单日涨幅"),
    ("盘中 -10%，跌破 100 美元", "布伦特盘中跌幅（11-04）", "盘中布油一度跌10%跌破100美元"),
    ("140 万桶/日", "摩根大通估全球石油过剩量（10月）", "9 月过剩约 110 万桶/日、10 月扩大至约 140 万桶/日"),
    ("4.89%", "10年期美债收益率（11-04）", "10年期美债收益率降约7个基点至4.89%、创两个月低点"),
    ("20.8%", "欧元区 10 月能源 CPI 同比", "10月CPI同比涨4.0%创三年新高，能源价格涨20.8%"),
    ("-8.67%", "布伦特结算跌幅（11-04）", "布伦特1月跌8.67%收94.62美元"),
]

SHOTS_LIST = [
    ("418-preview-01-masthead.png", ".masthead"),
    ("418-preview-02-verdict.png", ".verdict-band"),
    ("418-preview-03-metrics.png", "section:nth-of-type(2)"),
    ("418-preview-04-price.png", "section:nth-of-type(3)"),
    ("418-preview-05-diverge.png", "section:nth-of-type(4)"),
    ("418-preview-06-mech.png", "section:nth-of-type(5)"),
    ("418-preview-07-timeline.png", "section:nth-of-type(6)"),
    ("418-preview-08-frame.png", "section:nth-of-type(7)"),
    ("418-preview-09-gates.png", "section:nth-of-type(8)"),
    ("418-preview-10-evidence.png", "section:nth-of-type(9)"),
]

report = {"file": REL, "checks": [], "shots": []}


def check(name, ok, detail=""):
    report["checks"].append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print(("  PASS  " if ok else "  FAIL  ") + name + ("  " + str(detail) if detail else ""))
    return ok


def norm(s):
    """与 claim_gate.normalize 同口径：去标签、压空白、去中英文标点。"""
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", "", s)
    punct = "，。、；：？！“”‘’（）()《》〈〉【】[]「」『』—…·,.;:?\"'`~@#$%^&*-_+=|\\<>/　"
    for c in punct:
        s = s.replace(c, "")
    return s


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
        page.wait_for_timeout(1800)
        page.evaluate("document.fonts.ready.then(()=>1)")
        page.wait_for_timeout(600)

        print("\n== 1. 运行时 ==")
        check("无 console error", not console_errors, str(console_errors[:3]))
        check("无 pageerror", not page_errors, str(page_errors[:3]))
        check("无资源 404 / 失败请求", not failed, str(failed[:3]))
        check("无 {{ }} 模板占位", "{{" not in page.content(), "")
        check("正文无外链 http(s)", not re.search(r'href="https?://|src="https?://', page.content()), "")

        print("\n== 2. 结构 ==")
        html = open(PAGE, encoding="utf-8").read()
        for cls, want in VOCAB.items():
            n = page.evaluate("(s)=>document.querySelectorAll(s).length", cls)
            # .metric 需排除 metric-value/label/source 的父级之外仍为 7（模板口径：.metric 元素数）
            check(f"词汇 {cls} = {want}", n == want, f"实测 {n}")

        beat = page.evaluate("()=>{const m=document.querySelector('meta[name=showcase-beat]');return m?m.content:'';}")
        check("showcase-beat = 地缘与能源", beat == "地缘与能源", beat)

        title = page.title()
        check("<title> 为派单标题", title == "94.62美元与-8.67%——伊朗递出和平方案当天，油价跌破100美元", title)

        raw_claims = page.evaluate(
            "()=>{const el=document.querySelector('script#claims');return el?JSON.parse(el.textContent):[];}")
        check("claims 条数 = 8", len(raw_claims) == 8, str(len(raw_claims)))
        tri = [(c.get("value"), c.get("label"), c.get("quote")) for c in raw_claims]
        check("claims 三元组与预期一致", tri == CLAIMS, str([t[1] for t in tri]))

        body_text = norm(page.evaluate("()=>document.body.innerText"))
        for v, l, q in CLAIMS:
            check(f"quote 逐字命中：{l}", norm(q) in body_text)

        # 图表：三张 canvas 都要真的画出像素
        drawn = page.evaluate("""()=>{
          return Array.from(document.querySelectorAll('canvas')).map(c=>{
            try{ return c.toDataURL('image/png').length; }catch(e){ return 0; }
          });
        }""")
        check("三张图表均已绘制", len(drawn) == 3 and all(n > 5000 for n in drawn), str(drawn))
        check("Chart.js 已加载", page.evaluate("()=>typeof Chart!=='undefined'"), "")

        print("\n== 3. 硬口径 ==")
        # 标签内不得出现 11-05
        labels = page.evaluate(
            "()=>Array.from(document.querySelectorAll('.metric-label')).map(e=>e.textContent.trim())")
        check("标签日期无 11-05", not any("11-05" in x for x in labels), str(labels))
        check("八个标签中无句末标点", not any(re.search(r"[。！？]$", x) for x in labels), "")
        check("四个持续跟踪标签写法正确",
              all(x in labels for x in [
                  "布伦特 1 月合约结算价（11-04）",
                  "WTI 12月合约结算价（11-04）",
                  "现货黄金结算价（11-04）",
                  "欧元区 10 月能源 CPI 同比"]), str(labels[:4]))
        check("盘中条 value 含「盘中」", any("盘中" in (c.get("value") or "") for c in raw_claims), "")
        check("JPM 定性判断在正文（非断言）",
              norm("摩根大通指全球石油市场在9月和10月已重转供应过剩") in body_text
              and not any("重转供应过剩" in (c.get("label") or "") for c in raw_claims), "")
        check("结算价与盘中价分列措辞存在",
              norm("结算价与盘中价分列") in body_text, "")
        check("未把 11-05 写成交易日（正文无「11-05 结算价」）",
              "11-05结算价" not in body_text, "")
        check("无近似转写的假引文（Samaa 旧写法已清除）",
              "held discussions" not in body_text, "")
        check("标题「当天」口径注存在",
              norm("标题「当天」的口径") in body_text, "")
        check("伊朗方案两说已分列", norm("该提交的时点有两说") in body_text, "")
        check("现货金与期金两口径分开表述",
              norm("4073") in body_text and norm("4063") in body_text, "")

        print("\n== 4. 窄屏 ==")
        page.set_viewport_size({"width": 375, "height": 780})
        page.wait_for_timeout(700)
        over = page.evaluate(
            "()=>Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-375")
        check("375px 横向溢出 = 0", over <= 0, f"{over}px")

        print("\n== 5. 截图 ==")
        page.set_viewport_size({"width": 1280, "height": 900})
        page.wait_for_timeout(500)
        for fname, sel in SHOTS_LIST:
            el = page.query_selector(sel)
            if not el:
                check(f"截图 {fname}", False, f"未找到 {sel}")
                continue
            path = os.path.join(SHOTS, fname)
            el.screenshot(path=path)
            report["shots"].append(fname)
            check(f"截图 {fname}", os.path.exists(path) and os.path.getsize(path) > 10000,
                  f"{os.path.getsize(path) if os.path.exists(path) else 0} bytes")

        browser.close()

    out = os.path.join(HERE, "418-render-check-20261107.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    fails = [c for c in report["checks"] if not c["ok"]]
    print(f"\n合计 {len(report['checks'])} 项检查，失败 {len(fails)} 项。结果已写 {out}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
