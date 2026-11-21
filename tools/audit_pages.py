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

巡检范围：只扫**成品页** —— works/<日期>/{research,creative}/*.html，
与 build_manifest.py 的 scan_works() 同口径（当前 147 件）。
works/<日期>/notes/ 下是作者的飞草稿分片，不是作品页，不扫
（旧口径把分片当作品，分片首屏内容不全 → 每轮稳定误报）。

2026-11-17 口径修正（两处真缺陷）
--------------------------------
① **跨页串号**：旧版所有作品共用一个 page，上一页未落定的远程请求会在
   下一次 goto 时被中止（ERR_ABORTED），该事件落在**下一页**的监听窗口里
   → 研究件替创意件背了 world-atlas 的锅。现在每件作品用**独立 page**，
   且只统计本页 goto 之后的事件。
② **失败定性**：requestfailed 把「资源真的缺失」和「导航中止 / 浏览器策略
   拦截」混在一起。现在先分类，再判页面是否**确实依赖**该资源，
   两关都过才计入问题。

用法：
  python3 tools/audit_pages.py            # 全量巡检
  python3 tools/audit_pages.py --sample 20 # 抽样
  python3 tools/audit_pages.py --fix        # 巡检并把能自动修的（缺返回链等）修掉
"""
import argparse
import glob
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

from playwright.sync_api import sync_playwright

VIEWPORT = {"width": 1260, "height": 800}

# ── requestfailed 定性口径（2026-11-17 修正缺陷 ②）────────────────
# requestfailed ≠「资源真的缺失」。Chromium 把三类事件放在同一个事件里：
#   ① 导航切换 / 页面关闭中止了未完成的请求 → net::ERR_ABORTED
#   ② 浏览器策略拦截（扩展 / 企业策略 / 安全浏览）→ net::ERR_BLOCKED_BY_CLIENT 等
#   ③ 资源真的加载失败（DNS / 连接 / 超时 / 本地文件缺失）→ 其余错误码
# 只有 ③ 才算「资源加载失败」。
#
# 「算问题」还要再过两关：
#   · 页面**确实依赖**该资源（远程资源需源码里有引用证据；本地文件天然依赖）
#   · 不是 favicon 之类噪声
POLICY_BLOCKED_CODES = {
    "ERR_BLOCKED_BY_CLIENT", "ERR_BLOCKED_BY_RESPONSE",
    "ERR_BLOCKED_BY_ADMINISTRATOR", "ERR_BLOCKED_BY_ORB",
    "ERR_SAFEBROWSING_BLOCK", "ERR_UNKNOWN_URL_SCHEME",
    "ERR_CSP_BLOCKED",
}
# 导航中止：不是资源缺失，不算问题
BENIGN_FAILURE_CODES = {"ERR_ABORTED"}
# 未落定的远程请求要等它落定（秒）：
# 慢的远程依赖若不落定，下次 goto 会把它中止 → 变成 ERR_ABORTED，
# 失败就记不到本页头上（这正是 2026-11-17 串号缺陷的成因）。
NET_SETTLE_WAIT = 10.0

# ── 作品集口径 = 成品页 ──
# 作品页只在 works/<日期>/{research,creative}/ 下（与 build_manifest.py 的
# scan_works() 同源）。works/<日期>/notes/ 下是作者的**飞草稿分片**
# （如 2026-11-17-model-triage-board.part1.html），不是作品页。
#
# 旧口径 works/20*/*/*.html 把 notes/ 分片一并扫进来 —— 分片不是完整页面，
# 首屏内容自然不全，于是每轮巡检稳定误报「首屏几乎没有可见内容」，
# 真异常被淹没（2026-11-17 实测：151 件里 5 件分片，4 件误报）。
WORK_SUBDIRS = ("research", "creative")


def works():
    """返回成品页清单（相对仓库根目录，已排序）。

    排除：
      - notes/ 下的飞草稿分片、_436_parts/ 等中间产物（路径不含这两类目录）
      - .bak 备份（含 .bak.YYYYMMDD-HHMMSS 形式）
      - 隐藏文件、impeccable 探针文件（__ 开头）
    """
    out = []
    for sub in WORK_SUBDIRS:
        for f in glob.glob(f"works/*/{sub}/*.html"):
            name = os.path.basename(f)
            if name.startswith(".") or name.startswith("__"):
                continue
            if ".bak" in name:
                continue
            out.append(f)
    return sorted(out)


def manifest_total():
    """读 manifest.json 的 total（只读）。文件缺失或损坏 → None。"""
    try:
        with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as f:
            return json.load(f).get("total")
    except Exception:
        return None


def failure_code(err_text):
    """从 Playwright 的 failure 文本里取出 Chromium 错误码。"""
    t = (err_text or "").strip()
    if not t:
        return ""
    if "net::" in t:
        tail = t.split("net::")[-1].strip()
        return tail.split()[0] if tail else ""
    return t.split()[0] if t.split() else ""


def classify_failure(err_text):
    """把一次 requestfailed 分类。

    返回 (kind, code)：
      policy  —— 浏览器策略拦截，不是资源缺失
      abort   —— 导航/关闭中止了请求，不是资源缺失
      genuine —— 资源真的没加载出来
    """
    code = failure_code(err_text)
    if code in POLICY_BLOCKED_CODES:
        return "policy", code
    if code in BENIGN_FAILURE_CODES:
        return "abort", code
    return "genuine", code


def source_refs_url(src, url):
    """源码里是否引用了该资源（判「本页确实依赖它」）。

    远程资源：整串 / 路径 / 主机 / 文件名 任一命中即算引用。
    主机命中覆盖「字体 woff 来自 gstatic，源码里只有 preconnect」这类间接依赖。
    """
    if not src:
        return False
    u = url.split("#")[0].split("?")[0]
    if not u:
        return False
    if u in src:
        return True
    m = re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://([^/]+)(/.*)?$", u)
    if m:
        host, path = m.group(1), (m.group(2) or "").lstrip("/")
        if path and path in src:
            return True
        if host and host in src:
            return True
    elif u.startswith("file://"):
        p = u[len("file://"):]
        parts = p.split("/")
        for i in range(1, len(parts)):
            tail = "/".join(parts[i:])
            if tail and tail in src:
                return True
    base = u.rstrip("/").rsplit("/", 1)[-1]
    return bool(base) and base in src


def audit_one(pg, rel):
    """返回该页的问题列表。

    口径（2026-11-17 修正，两条缺陷）：
      ① **事件归属**：只收本页 goto 之后的事件。调用方给每件作品单独开 page，
         上一页未落定的请求不会再把失败记到本页头上。
      ② **失败定性**：requestfailed 先分类（策略拦截 / 导航中止 / 真失败），
         再判页面是否**确实依赖**该资源，两关都过才计入问题。
    """
    problems = []
    errors, failed, console_err = [], [], []
    pending = {}          # (method, url) -> 未落定的远程请求数
    armed = {"v": False}  # goto 之后才收事件
    ignored = {"policy": 0, "abort": 0, "unrelated": 0}

    def on_pageerror(e):
        if not armed["v"]:
            return
        errors.append(str(e)[:220])

    def on_console(m):
        if not armed["v"] or m.type != "error":
            return
        console_err.append(m.text[:220])

    def on_request(r):
        if r.url.startswith("file://"):
            return
        k = (r.method, r.url)
        pending[k] = pending.get(k, 0) + 1

    def on_settled(r):
        k = (r.method, r.url)
        if k in pending:
            pending[k] -= 1
            if pending[k] <= 0:
                pending.pop(k, None)

    def on_failed(r):
        on_settled(r)
        if not armed["v"]:
            return
        failed.append((r.url, r.failure))

    pg.on("pageerror", on_pageerror)
    pg.on("console", on_console)
    pg.on("request", on_request)
    pg.on("requestfinished", on_settled)
    pg.on("requestfailed", on_failed)

    # 页面源码：判「本页是否依赖该资源」的证据
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore") as f:
            src = f.read()
    except Exception:
        src = ""

    armed["v"] = True
    try:
        pg.goto("file://" + os.path.abspath(rel), wait_until="load", timeout=30000)
    except Exception as e:
        return ([f"加载失败: {str(e)[:120]}"],
                {"errors": 0, "console": 0, "failed": 0, "failed_all": 0,
                 "vis": -1, "ignored": ignored,
                 "pending_remote": sum(pending.values())})

    pg.wait_for_timeout(2200)

    # 等未落定的远程请求（上限 NET_SETTLE_WAIT 秒）：
    # 远程请求若在页面切换时被中止 → ERR_ABORTED → 不是资源缺失；
    # 等它落定，真实失败（DNS / 连接 / 超时）才算在**本页**头上。
    deadline = time.monotonic() + NET_SETTLE_WAIT
    while pending and time.monotonic() < deadline:
        pg.wait_for_timeout(200)

    # 真实可见内容 —— ⚠️ 不能用 innerText：它把 opacity:0 的文字也算进去。
    # 实测 2026-06-20 等作品整页被 .fade-in 这类**死规则**永久隐藏，
    # innerText 有 15524 字、视觉上却全黑 —— 巡检因此漏掉了它们。
    #
    # 判定要点：
    #  ① 合成可见性（父元素 opacity:0 会合成生效，子元素 computed opacity 仍是 1）
    #     → 用 Element.checkVisibility（浏览器原生）
    #  ② 只看**首屏内**（截图只拍首屏，屏外的不可见不算问题）
    try:
        # 口径（2026-11-13 修正）：判「首屏有没有可见内容」不能只看**叶子节点**——
        # 标题常被内层 span 包裹（hero__title 内是 span），叶子口径会把「标题可见」
        # 误判成「首屏空白」。改为：视口内**有可见文本的元素**都算（自身直接文本非空
        # 或含可见后代），并排除 fixed 定位（HUD 等演示区控件本就不该出现在首屏）。
        vis = pg.evaluate("""() => {
            const vh = window.innerHeight;
            const text = e => (e.textContent || '').trim();
            const cands = [...document.querySelectorAll('body *')].filter(e => {
                if (!text(e)) return false;
                const hasTextChild = [...e.childNodes].some(
                    n => n.nodeType === 3 && (n.textContent || '').trim().length);
                const hasVisibleChild = [...e.children].some(c => text(c));
                if (!hasTextChild && !hasVisibleChild) return false;
                const r = e.getBoundingClientRect();
                if (r.height <= 2 || r.width <= 2) return false;
                if (r.bottom <= 0 || r.top >= vh) return false;
                if (getComputedStyle(e).position === 'fixed') return false;
                let op = 1, el = e;
                while (el && el !== document.body) {
                    const cs = getComputedStyle(el);
                    op *= parseFloat(cs.opacity);
                    if (cs.visibility === 'hidden' || cs.display === 'none') { op = 0; break; }
                    el = el.parentElement;
                }
                return op > 0.05;
            });
            return {len: cands.length, leaves: cands.length,
                    sample: (cands[0] ? cands[0].textContent : '').trim().slice(0, 40)};
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
    # requestfailed 定性 + 依赖判定（2026-11-17 修正）
    real = []
    for url, err in failed:
        kind, code = classify_failure(err)
        if kind == "policy":          # 浏览器策略拦截 → 不算资源缺失
            ignored["policy"] += 1
            continue
        if kind == "abort":           # 导航中止 → 不算资源缺失
            ignored["abort"] += 1
            continue
        if "favicon" in url.lower():  # favicon 之类噪声
            continue
        # 本地文件：浏览器只会请求页面引用过的文件 → 天然依赖
        # 远程资源：必须在源码里有引用证据（整串 / 路径 / 主机 / 文件名）
        depends = True if url.startswith("file://") else source_refs_url(src, url)
        if not depends:
            ignored["unrelated"] += 1
            continue
        real.append((url, code))
    if real:
        u0, c0 = real[0]
        problems.append(f"资源加载失败 ×{len(real)}: {u0[-90:]}（{c0 or '未知错误'}）")
    if 0 <= vis["len"] < 4:   # 2026-11-13：阈值 8→4（极简首屏也会被判空白）
        problems.append(f"首屏几乎没有可见内容（可见叶子 {vis['len']} / 总叶子 {vis.get('leaves','?')}）"
                        f" —— 典型的「死规则把内容永久隐藏」")
    if hidden > 0:
        problems.append(f"{hidden} 个主容器被隐藏（opacity/visibility 为 0）")

    armed["v"] = False
    return problems, {"errors": len(errors), "console": len(console_err),
                       "failed": len(real), "failed_all": len(failed),
                       "vis": vis["len"], "ignored": ignored,
                       "pending_remote": sum(pending.values())}


def main():
    # argparse：原手解析会把 --help 吞掉（只过滤 '-' 开头的参数）→ 直接跑全量
    # 巡检（分钟级），而不是打印帮助；--sample 漏传值还会 IndexError。
    # 调用方 auto_maintain.py:270 传 ['--sample', str(n)]，语义不变。
    ap = argparse.ArgumentParser(
        prog='audit_pages.py', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--sample', type=int, default=None, metavar='N',
                    help='只抽查 N 件（不带则全量）')
    ap.add_argument('files', nargs='*',
                    help='只查这几件（相对仓库根目录）；不带则全量')
    a = ap.parse_args()
    sample = a.sample
    only = a.files
    all_works = works()
    ws = all_works
    # 件数对账：巡检口径与 manifest 必须同口径（146 = 146）。
    # 对不上就当场报出来，不靠人眼比对两处数字。
    mtot = manifest_total()
    if mtot is not None and mtot != len(all_works):
        print(f"  ⚠ 件数与 manifest.json 不一致：成品页 {len(all_works)} vs "
              f"manifest {mtot}（先跑 build_manifest.py 重建）")
    if only:
        ws = [f for f in only if os.path.exists(f)]
        outside = [f for f in ws if f not in set(all_works)]
        if outside:
            print("  ⚠ 以下文件不在成品页集合内，结论仅供参考："
                  + "、".join(outside))
    elif sample:
        # 抽样只从收紧后的成品页里抽，不会抽到 notes/ 分片
        step = max(1, len(ws) // sample)
        ws = ws[::step][:sample]

    print(f"巡检 {len(ws)} 件作品（真实加载 + 抓运行时错误）\n")
    bad = []
    agg = {"policy": 0, "abort": 0, "unrelated": 0, "pending_pages": 0}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/usr/bin/chromium",
                                 args=["--no-sandbox"])
        for i, rel in enumerate(ws, 1):
            # 每件作品一个**独立 page**（2026-11-17 修正缺陷 ①）：
            # 共用一个 page 时，上一页未落定的远程请求会在下一页的监听窗口里
            # 触发 requestfailed → 失败被记到**下一页**头上（跨页串号）。
            # 独立 page 同时避免监听器跨作品累积。
            pg = br.new_page(viewport=VIEWPORT)
            try:
                probs, stat = audit_one(pg, rel)
            finally:
                try:
                    pg.close()
                except Exception:
                    pass
            ig = stat.get("ignored", {})
            for k in ("policy", "abort", "unrelated"):
                agg[k] += ig.get(k, 0)
            if stat.get("pending_remote"):
                agg["pending_pages"] += 1
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
    print(f"requestfailed 口径：策略拦截 {agg['policy']} 次 / 导航中止 {agg['abort']} 次 / "
          f"与本页无关 {agg['unrelated']} 次（均不计为问题）；"
          f"远程依赖未落定 {agg['pending_pages']} 件")
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
