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
import argparse, json
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
        # 掐断外部请求：作品按契约**零远程依赖**，任何外链要么是坏的、
        # 要么会把 load 挂住（曾有一件作品拖 45 秒并带崩整条流水线）。
        # 掐断后 load 不会挂，且能暴露"这件其实依赖外链"。
        def _route(route):
            u = route.request.url
            if u.startswith('file://') or u.startswith('data:') or u.startswith('about:'):
                route.continue_()
            else:
                route.abort()
        try:
            pg.route('**/*', _route)
        except Exception:
            pass
        # ⚠️ 必须等 load（样式与图片就绪），否则截到半张白纸 ——
        # 曾用 domcontentloaded 绕开超时，结果 51 张缩略图全黑。
        # 超时则降级到 domcontentloaded 再截，宁可截到未完全渲染也不能不截。
        try:
            pg.goto(url, wait_until="load", timeout=20000)
        except Exception:
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=10000)
            except Exception:
                pass
        pg.add_style_tag(content=CSS)
        pg.wait_for_timeout(3500)
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
    # argparse：原 `sys.argv[1] == "--all"` 会把 --help 当成 html 路径，
    # 不带参数则 IndexError。
    # 注意：本模块被 autopublish.py:739 `import gen_thumb` 复用，
    # 所以解析必须留在 main() 里，不能提到模块级（否则 import 就解析调用方 argv）。
    ap = argparse.ArgumentParser(
        prog='gen_thumb.py', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--all', action='store_true',
                    help='扫描 manifest 中所有缺缩略图的作品')
    ap.add_argument('rel', nargs='?', help='html 文件相对路径')
    ap.add_argument('typ', nargs='?', help='research|creative（可省，自动推断）')
    a = ap.parse_args()

    if a.all:
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
        if not a.rel:
            ap.error('需要 html 文件相对路径，或用 --all')
        rel = a.rel
        typ = a.typ or infer_type(os.path.splitext(rel)[0])
        if not typ:
            print("无法推断类型，请显式传入 research|creative")
            sys.exit(1)
        shoot(rel, typ)


if __name__ == "__main__":
    main()
