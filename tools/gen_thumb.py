#!/usr/bin/env python3
"""规范化缩略图生成器（v6.4 展厅规范）

用法:
    python3 tools/gen_thumb.py <html文件相对路径> [类型]
    python3 tools/gen_thumb.py --all      # 扫描 manifest 中所有缺缩略图的作品

规范（强制）:
  * viewport 宽度 = 1260（非 1280）
  * 注入 CSS 隐藏滚动条:
    ::-webkit-scrollbar{display:none}*{scrollbar-width:none}body,html{overflow:hidden!important}
  * clip 裁剪: {"x":0,"y":0,"width":1260,"height":800}
  * 输出文件名: thumbs/{date}-{type}-{stem}-thumb.png
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THUMBS = os.path.join(ROOT, "thumbs")
CSS = (
    "::-webkit-scrollbar{display:none}"
    "*{scrollbar-width:none}"
    "body,html{overflow:hidden!important}"
)


def shoot(html_rel, typ):
    stem = os.path.splitext(os.path.basename(html_rel))[0]
    date = stem[:10]
    out_name = f"{date}-{typ}-{stem}-thumb.png"
    out_path = os.path.join(THUMBS, out_name)
    if not os.path.exists(html_path(html_rel)):
        print(f"  ✗ 源文件不存在: {html_rel}")
        return None
    os.makedirs(THUMBS, exist_ok=True)
    url = "file://" + html_path(html_rel)
    with sync_playwright() as p:
        b = p.chromium.launch(
            executable_path="/usr/bin/chromium",
            args=["--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=1"],
        )
        pg = b.new_page(viewport={"width": 1260, "height": 800})
        pg.goto(url, wait_until="load", timeout=45000)
        pg.add_style_tag(content=CSS)
        pg.wait_for_timeout(2500)
        pg.screenshot(path=out_path, clip={"x": 0, "y": 0, "width": 1260, "height": 800})
        b.close()
    print(f"  ✅ {out_name}  ({os.path.getsize(out_path)}B)")
    return "thumbs/" + out_name


def html_path(rel):
    return os.path.join(ROOT, rel)


def infer_type(stem):
    """类型推断：无前缀命名规范下，按 manifest 优先，其次按标题关键词。"""
    with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as f:
        man = json.load(f)
    for grp in ("research", "creative"):
        for it in man[grp]:
            if it["file"] == stem + ".html":
                return grp
    return None


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as f:
            man = json.load(f)
        todo = [
            (it["file"], grp)
            for grp in ("research", "creative")
            for it in man[grp]
            if not (it.get("thumb") and os.path.exists(html_path(it["thumb"])))
        ]
        print(f"缺缩略图 {len(todo)} 件，开始生成：")
        for rel, grp in todo:
            shoot(rel, grp)
    else:
        rel = sys.argv[1]
        typ = sys.argv[2] if len(sys.argv) > 2 else infer_type(os.path.splitext(rel)[0])
        if not typ:
            print("无法推断类型，请显式传入 research|creative")
            sys.exit(1)
        shoot(rel, typ)


if __name__ == "__main__":
    main()
