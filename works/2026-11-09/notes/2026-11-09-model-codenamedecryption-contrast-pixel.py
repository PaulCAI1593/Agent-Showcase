#!/usr/bin/env python3
"""对比度实测（像素法）：先把全文本设为透明重渲染，取每个文本节点框内的
众数颜色作为真实背景，再与该节点的 computed color 算 WCAG 比值。

覆盖两种状态：初始态、翻卡+比对完成态（reveal 类文本仅在交互后可见）。

用法： python3 2026-11-09-model-codenamedecryption-contrast-pixel.py
输出： JSON（fail 列表 + 最小比值），并落盘纯背景过程截图。
"""
import io
import json
import os

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
URL = "file://" + os.path.join(
    ROOT, "works", "2026-11-09", "creative", "2026-11-09-model-codenamedecryption.html")

TEXT_META = r"""
() => Array.from(document.querySelectorAll('body *')).map((el) => {
  if (el.closest('[aria-hidden="true"]')) return null;
  const st = getComputedStyle(el);
  if (st.display === 'none' || st.visibility === 'hidden') return null;
  if (parseFloat(st.opacity) === 0) return null;
  const txt = Array.from(el.childNodes).filter(n => n.nodeType === 3)
                .map(n => n.textContent.trim()).join('');
  if (!txt) return null;
  const r = el.getBoundingClientRect();
  if (r.width < 3 || r.height < 3) return null;
  return {text: txt.slice(0, 40), color: st.color, tag: el.tagName,
          cls: (typeof el.className === 'string' ? el.className : ''),
          flipped: !!el.closest('.flipped'),
          inback: !!el.closest('.back'),
          x: r.left, y: r.top + window.scrollY, w: r.width, h: r.height,
          size: parseFloat(st.fontSize), weight: parseInt(st.fontWeight, 10) || 400};
}).filter(Boolean)
"""


def lum(c):
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def ratio(a, b):
    l1, l2 = lum(a), lum(b)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def parse_rgb(s):
    parts = s[s.find('(') + 1:s.find(')')].split(',')
    return (int(float(parts[0])), int(float(parts[1])), int(float(parts[2])),
            float(parts[3]) if len(parts) > 3 else 1.0)


def mode_color(px, stride, iw, ih, x, y, w, h):
    counts = {}
    xa, ya = max(0, int(x)), max(0, int(y))
    xb, yb = min(iw, int(x + w)), min(ih, int(y + h))
    for yy in range(ya, yb):
        base = yy * stride
        for xx in range(xa, xb):
            p = base + xx * 3
            k = (px[p], px[p + 1], px[p + 2])
            counts[k] = counts.get(k, 0) + 1
    if not counts:
        return None
    return max(counts.items(), key=lambda kv: kv[1])[0]


def collect(pg, shot_path, tag, only_cls=None, only_tags=None, only_flipped=False,
            exclude_back=False):
    """返回 (rows, fails)；截图前必须已把字形设为透明。
    only_cls：只统计 class 含其中任一子串的元素。
    only_flipped：只统计位于 .flipped 卡片内的元素（翻卡态只测背面文本）。
    exclude_back：排除 .back 内文本（未翻卡时背面背对读者，不可见）。"""
    meta = pg.evaluate(TEXT_META)
    if only_cls or only_tags:
        meta = [m for m in meta
                if (only_cls and any(s in m["cls"] for s in only_cls))
                or (only_tags and m["tag"] in only_tags)]
    if only_flipped:
        meta = [m for m in meta if m["flipped"]]
    if exclude_back:
        meta = [m for m in meta if not m["inback"]]
    shot = pg.screenshot(full_page=True, path=shot_path)
    img = Image.open(io.BytesIO(shot)).convert("RGB")
    iw, ih = img.size
    px = img.tobytes()
    stride = iw * 3
    rows, fails = [], []
    for m in meta:
        bg = mode_color(px, stride, iw, ih, m["x"], m["y"], m["w"], m["h"])
        if bg is None:
            continue
        fg = parse_rgb(m["color"])
        fg_on = fg[:3]
        if fg[3] < 1:
            fg_on = tuple(round(fg[i] * fg[3] + bg[i] * (1 - fg[3])) for i in range(3))
        large = m["size"] >= 24 or (m["size"] >= 18.66 and m["weight"] >= 700)
        need = 3.0 if large else 4.5
        cr = ratio(fg_on, bg)
        row = {"state": tag, "cls": m["cls"], "text": m["text"], "size": m["size"],
               "color": m["color"], "bg": "rgb(%d,%d,%d)" % bg,
               "ratio": round(cr, 2), "need": need, "pass": cr >= need}
        rows.append(row)
        if not row["pass"]:
            fails.append(row)
    return rows, fails


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/chromium",
                              args=["--no-sandbox", "--hide-scrollbars",
                                    "--force-device-scale-factor=1"])
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(2200)

        # 让文字字形不可见（保留 computed color），重渲染，截整页 → 纯背景像素
        pg.add_style_tag(content="*{-webkit-text-fill-color:transparent !important;"
                                 "text-shadow:none !important;"
                                 "text-decoration-color:transparent !important}")
        pg.wait_for_timeout(400)

        all_rows, all_fails = [], []
        r1, f1 = collect(pg, os.path.join(HERE, "_contrast_bg_initial.png"),
                         "initial", exclude_back=True)
        all_rows += r1; all_fails += f1

        # 交互态：reveal 类文本（.tease 默认 opacity:0、.match-stamp 默认 opacity:0）
        # 强制显形 + 跑完比对；不翻卡，避免 3D 背面遮挡造成误判。
        pg.add_style_tag(content=".tease{opacity:1!important;transform:none!important}")
        pg.click("#scanbtn")
        pg.wait_for_timeout(1600)
        r2, f2 = collect(pg, os.path.join(HERE, "_contrast_bg_interactive.png"),
                         "reveal+matched", only_cls=("tease", "match-stamp"))
        all_rows += r2; all_fails += f2

        # 卡片背面态：逐张翻卡，只测 .flipped 卡片内的背面文本（正面背对不可见）
        def flip_pass(cards, prefix):
            for i, c in enumerate(cards):
                c.click()
                pg.wait_for_timeout(450)
                r, f = collect(pg, os.path.join(HERE, "_contrast_bg_flipped.png"),
                               f"{prefix}-{i}",
                               only_cls=("who", "clue", "src", "stamp"),
                               only_tags=("Q",), only_flipped=True)
                all_rows.extend(r)
                all_fails.extend(f)

        flip_pass(pg.query_selector_all("#panel-codes .card"), "card-back")
        pg.click("#tab-open")
        pg.wait_for_timeout(300)
        flip_pass(pg.query_selector_all("#panel-open .card"), "card-back-open")
        b.close()

    uniq, seen = [], set()
    for f in all_fails:
        k = (f["color"], f["bg"], f["size"])
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    out = {"total_text_nodes": len(all_rows), "fail_count": len(all_fails),
           "unique_failures": uniq,
           "min_ratio": round(min((r["ratio"] for r in all_rows), default=0), 2),
           "viewport": "1440x900",
           "method": "文本透明重渲染 + 框内众数背景色 + computed color（WCAG 2.1）"}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
