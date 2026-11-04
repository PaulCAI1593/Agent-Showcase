#!/usr/bin/env python3
"""
audit_pages.py — 作品页健康巡检（运行时错误 / 空白页 / 资源缺失）

为什么需要它
------------
十项硬校验只看**文件与数据**（计数/缩略图/标签/断言/返回链），
不看**脚本能不能跑**。2026-09-08 反诈AI 就是这样漏过去的：一行字符串里
多一个单引号 → 整脚本挂掉 → 页面只剩导航条，而所有校验全绿。

同一类问题还有别的形态，静态检查都发现不了：
- **运行时错误**（语法对但执行时炸）→ 某个交互/图表永久失效
- **资源 404**（本地化脚本路径错）→ 图表空白
- **内容为空**（渲染出来是空的）
- **控制台报错**（可能不影响首屏但埋雷）

所以必须**逐页真跑一遍**。这是唯一可靠的办法。

用法：
  python3 tools/audit_pages.py            # 全量巡检
  python3 tools/audit_pages.py --sample 20 # 抽样
  python3 tools/audit_pages.py --fix        # 巡检并把能自动修的（缺返回链等）修掉
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

from playwright.sync_api import sync_playwright

VIEWPORT = {"width": 1260, "height": 800}


def works():
    out = []
    for f in sorted(glob.glob("works/20*/*/*.html")):
        if ".bak" in f or f.startswith("."):
            continue
        out.append(f)
    return out


def audit_one(pg, rel):
    """返回该页的问题列表。"""
    problems = []
    errors, failed, console_err = [], [], []

    def on_pageerror(e):
        errors.append(str(e)[:220])

    def on_console(m):
        if m.type in ("error",):
            console_err.append(m.text[:220])

    def on_failed(r):
        failed.append(r.url[-90:])

    pg.on("pageerror", on_pageerror)
    pg.on("console", on_console)
    pg.on("requestfailed", on_failed)

    try:
        pg.goto("file://" + os.path.abspath(rel), wait_until="load", timeout=30000)
    except Exception as e:
        return [f"加载失败: {str(e)[:120]}"], {"errors": 0, "console": 0, "failed": 0}

    pg.wait_for_timeout(2200)

    # 真实可见内容 —— ⚠️ 不能用 innerText：它把 opacity:0 的文字也算进去。
    # 实测 2026-06-20 等作品整页被 .fade-in 这类**死规则**永久隐藏，
    # innerText 有 15524 字、视觉上却全黑 —— 巡检因此漏掉了它们。
    #
    # 判定要点：
    #  ① 合成可见性（父元素 opacity:0 会合成生效，子元素 computed opacity 仍是 1）
    #     → 用 Element.checkVisibility（浏览器原生）
    #  ② 只看**首屏内**（截图只拍首屏，屏外的不可见不算问题）
    try:
        vis = pg.evaluate("""() => {
            const vh = window.innerHeight;
            const leaves = [...document.querySelectorAll('body *')].filter(
                e => e.children.length === 0 && (e.textContent || '').trim().length);
            const shown = leaves.filter(e => {
                const r = e.getBoundingClientRect();
                if (r.height <= 2 || r.width <= 2) return false;
                if (r.bottom <= 0 || r.top >= vh) return false;
                if (typeof e.checkVisibility === 'function') {
                    return e.checkVisibility({opacityProperty: true, visibilityProperty: true});
                }
                let op = 1, el = e;
                while (el && el !== document.body) {
                    const cs = getComputedStyle(el);
                    op *= parseFloat(cs.opacity);
                    if (cs.visibility === 'hidden' || cs.display === 'none') { op = 0; break; }
                    el = el.parentElement;
                }
                return op > 0.05;
            });
            return {len: shown.length, leaves: leaves.length,
                    sample: (shown[0] ? shown[0].textContent : '').trim().slice(0, 40)};
        }""")
    except Exception:
        vis = {"len": -1, "leaves": -1, "sample": ""}

    # 高度为 0 的主容器 → 内容被隐藏（fade-up 没触发那类）
    try:
        # 只判**视口内**被隐藏的容器 —— 视口外的 .fade-up 本就该是 opacity:0
        # （滚动才显现），否则会把正常的滚动显现动画全判成问题。
        hidden = pg.evaluate("""() => {
            const vh = window.innerHeight;
            const els = [...document.querySelectorAll('section, .hero, main, .wrap')];
            let n = 0;
            els.forEach(e => {
                const cs = getComputedStyle(e);
                const r = e.getBoundingClientRect();
                const inView = r.top < vh * 0.9 && r.bottom > 0;
                if (r.height > 40 && inView &&
                    (cs.opacity === '0' || cs.visibility === 'hidden')) n++;
            });
            return n;
        }""")
    except Exception:
        hidden = -1

    if errors:
        problems.append(f"JS 运行时错误 ×{len(errors)}: {errors[0]}")
    if console_err:
        problems.append(f"console.error ×{len(console_err)}: {console_err[0]}")
    if failed:
        # 忽略 favicon 之类
        real = [u for u in failed if "favicon" not in u]
        if real:
            problems.append(f"资源加载失败 ×{len(real)}: {real[0]}")
    if 0 <= vis["len"] < 8:
        problems.append(f"首屏几乎没有可见内容（可见叶子 {vis['len']} / 总叶子 {vis.get('leaves','?')}）"
                        f" —— 典型的「死规则把内容永久隐藏」")
    if hidden > 0:
        problems.append(f"{hidden} 个主容器被隐藏（opacity/visibility 为 0）")

    return problems, {"errors": len(errors), "console": len(console_err),
                       "failed": len(failed), "vis": vis["len"]}


def main():
    args = sys.argv[1:]
    sample = None
    if "--sample" in args:
        sample = int(args[args.index("--sample") + 1])
    # 位置参数 = 只查这几件（相对仓库根目录）；不带参数则全量
    only = [a for a in args if not a.startswith("-") and not a.isdigit()]
    ws = works()
    if only:
        ws = [f for f in only if os.path.exists(f)]
    elif sample:
        step = max(1, len(ws) // sample)
        ws = ws[::step][:sample]

    print(f"巡检 {len(ws)} 件作品（真实加载 + 抓运行时错误）\n")
    bad = []
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/usr/bin/chromium",
                                 args=["--no-sandbox"])
        pg = br.new_page(viewport=VIEWPORT)
        for i, rel in enumerate(ws, 1):
            probs, stat = audit_one(pg, rel)
            if probs:
                bad.append((rel, probs))
                print(f"  ✗ {rel}")
                for x in probs:
                    print(f"      {x}")
            if i % 20 == 0:
                print(f"  … 已查 {i}/{len(ws)}")
        br.close()

    print(f"\n{'='*56}")
    print(f"巡检完成：{len(ws)} 件，{len(bad)} 件有问题")
    if bad:
        print("\n问题分布：")
        kinds = {}
        for rel, probs in bad:
            for x in probs:
                k = x.split("（")[0].split(":")[0]
                kinds[k] = kinds.get(k, 0) + 1
        for k, n in sorted(kinds.items(), key=lambda x: -x[1]):
            print(f"  {n:>3} × {k}")
        print("\n有问题作品：")
        for rel, _ in bad:
            print(f"  {rel}")
    else:
        print("✓ 全部作品页运行时健康")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
