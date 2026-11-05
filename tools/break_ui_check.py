#!/usr/bin/env python3
"""
break_ui_check.py — 首页极端数据压测（break-ui 技能）

为什么需要它
------------
十项硬校验只保证「数据与文件一致」，不保证「极端数据下页面不崩」。
归档会持续长大：标题长度、断言条数、标签数、单月件数都没有上限。
真实档案里已经出现过 60 字标题、246 个标签；再长一点、某个月再来 100 件，
首页就必须还站得住。

与 audit_pages.py 的分工
------------------------
audit_pages.py：真作品、真数据，看有没有运行时错误。
本脚本：**最坏数据**，看版面会不会塌。

dev-only：页面本身不引用本脚本，也不含任何开关；数据从测试侧注入。

用法：
  python3 tools/break_ui_check.py            # 跑全部场景
  python3 tools/break_ui_check.py --shots    # 额外保存截图到 tools/break_ui_shots/
"""
import argparse, json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

from playwright.sync_api import sync_playwright

VIEWPORTS = [("desktop", 1280, 800), ("narrow", 320, 720), ("wide", 1920, 1080)]
INDEX = "file://" + os.path.join(ROOT, "index.html")


def fixture_worst():
    """每个破坏签名一行，混合分布（break-ui 硬规则3：一份数据打中所有签名）。"""
    def it(f, title, date, typ, thumb="", claims=None, beat="", tags=None, desc=""):
        return {"file": f, "thumb": thumb, "title": title, "date": date, "type": typ,
                "highlights": tags or [], "beat": beat, "claims": claims or [],
                "description": desc}

    def C(v, l, s=""):
        return {"value": v, "label": l, "source": s}

    LONG = "国务院金融监督管理总局办公厅关于印发商业银行互联网贷款管理暂行办法的通知及实施细则的通知"
    w = [
        # 签名①：超长标题 + 缩略图 404 + 超长断言 + 超长标签
        it("works/2026-11-01/research/a.html", LONG * 2, "2026-11-01", "research",
           thumb="thumbs/DOES-NOT-EXIST.webp", claims=[C(LONG, LONG, LONG)],
           beat="估值与资本", tags=["a" * 80], desc=LONG * 3),
        # 签名②：无断言 / 无标签 / 无追踪线
        it("works/2026-11-01/creative/b.html", "短", "2026-11-01", "creative"),
        # 签名③：空标题 + 空日期
        it("works/2026-11-01/research/c.html", "", "", "research"),
        # 签名④：标题含 HTML 片段与引号
        it("works/2026-11-01/research/d.html", '标题含"引号"与 <script> 与 & 符号',
           "2026-11-01", "research", claims=[C("", ""), C("0", "")],
           beat="估值与资本", tags=["<b>x</b>"]),
        # 签名⑤：Emoji 开头
        it("works/2026-11-01/creative/e.html", "🚀 Emoji 开头的标题", "2026-11-01", "creative"),
        # 签名⑥：400 字标题 + 300 字断言
        it("works/2026-11-01/research/f.html", "f" * 400, "2026-11-01", "research",
           claims=[C("1" * 300, "x" * 300)]),
    ]
    # 签名⑦：单月 113 件（一个抽屉塞爆）
    for k in range(113):
        w.append(it(f"works/2026-10-01/research/bulk{k}.html", f"批量作品 {k}",
                    "2026-10-01", "research", claims=[C(f"{k}%", f"指标 {k}")]))
    stats = {"generated": "2026-11-03", "span": {"a": 1}, "rhythm": [], "capacity": {},
             "collab": {}, "beats": ["估值与资本"], "unclassified_tags": [],
             "claims": {"total": 999999}}
    return {"research": [x for x in w if x["type"] == "research"],
            "creative": [x for x in w if x["type"] == "creative"],
            "stats": stats}


def fixture_empty():
    return {"research": [], "creative": [],
            "stats": {"generated": "2026-11-03", "span": {}, "rhythm": [], "capacity": {},
                      "collab": {}, "beats": [], "unclassified_tags": [],
                      "claims": {"total": 0}}}


def fixture_one():
    w = fixture_worst()
    return {"research": [w["research"][0]], "creative": [], "stats": w["stats"]}


MEASURE = """() => {
  // ⚠️ window.clientWidth 不存在（恒为 undefined → NaN），`NaN > 0` 恒假，这条检查等于没跑
  const out = {hOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
               brokenImgs: 0, overflowEls: [], emptyDrawers: 0, undefinedText: 0,
               notes: []};
  out.brokenImgs = [...document.images].filter(i => i.complete && i.naturalWidth === 0).length;
  // 元素级横向溢出（排除刻意裁剪的装饰层）
  //  · .cover-field —— 拼贴装饰层（pointer-events:none; z-index:0），图片刻意出血、由自身 overflow:hidden 裁切
  //  · text-overflow:ellipsis —— 元素自己声明单行截断，scrollWidth > clientWidth 是省略号的正常表现
  //  排除只认这两条显式声明；像 .cover-focus 那种未声明的图片溢出照报不误
  const skip = el => el.closest('.ledger-wall,.lw-row,.cover-title,.cover-field');
  for (const el of document.querySelectorAll('body *')) {
    if (skip(el)) continue;
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
    if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0) {
      const cs = getComputedStyle(el);
      if (cs.overflowX !== 'visible' && cs.overflowX !== 'hidden') continue;
      if (cs.textOverflow === 'ellipsis') continue;
      out.overflowEls.push({tag: el.tagName, cls: el.className.toString().slice(0, 60),
                            sw: el.scrollWidth, cw: el.clientWidth});
    }
  }
  // 溢出条目不截断：计数必须真实，回归时能看出是一处还是几十处
  // 渲染出 undefined / NaN / [object Object] 字面量
  // ⚠️ 两个坑：① 方括号必须转义，否则 /[object Object]/ 是字符类，匹配任意字母
  //            ② 只看叶子节点的 innerText，父节点的 innerText 会把子节点重复计入
  const bads = ['undefined', 'NaN', '[object Object]'];
  for (const el of document.querySelectorAll('body *')) {
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
    if (el.children.length) continue;
    const t = (el.innerText || '').trim();
    if (!t || t.length > 400) continue;
    for (const b of bads) {
      const i = t.indexOf(b);
      if (i >= 0) {
        out.undefinedText++;
        if (out.notes.length < 6) out.notes.push(b + ' @' + el.tagName + '.' +
          (el.className || '').toString().slice(0, 30) + ' «' + t.slice(Math.max(0, i - 25), i + 30) + '»');
      }
    }
  }
  // 卡片元信息出现 undefined（空日期切片）
  const metaBad = [...document.querySelectorAll('.card-meta')]
      .filter(e => /undefined|NaN/.test(e.textContent)).length;
  out.undefinedText += metaBad;
  if (metaBad) out.notes.push('card-meta undefined×' + metaBad);
  return out;
}"""


def run(pg, data, label, shots=False):
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
    pg.on("console", lambda m: errs.append("console:" + m.text[:120]) if m.type == "error" else None)
    pg.goto(INDEX, wait_until="load")
    pg.wait_for_timeout(400)
    # file:// 下 fetch(manifest.json) 必然失败 → 降级提示必须出现（showStale 修复的验收点）
    stale = pg.locator("#stale-notice").count()
    stale_text = pg.locator("#stale-notice").inner_text()[:60] if stale else ""
    # 注入最坏数据（数据边界，不是改组件）
    if data is not None:
        pg.evaluate("(d)=>{ if(window.boot) boot(d); }", data)
        pg.wait_for_timeout(500)
    rows = []
    for name, w, h in VIEWPORTS:
        pg.set_viewport_size({"width": w, "height": h})
        pg.wait_for_timeout(350)
        m = pg.evaluate(MEASURE)
        m["viewport"] = name
        m["w"] = w
        rows.append(m)
        if shots:
            os.makedirs("tools/break_ui_shots", exist_ok=True)
            pg.screenshot(path=f"tools/break_ui_shots/{label}-{name}.png", full_page=False)
    body = pg.locator('#drawers').inner_text()[:120]
    empt = pg.evaluate("()=>{const d=document.getElementById('drawers');"
                       "return {drawers:document.querySelectorAll('.drawer').length,"
                       "txt:(d?d.innerText:'').trim().slice(0,80)};}")
    return {"label": label, "stale_notice": stale, "stale_text": stale_text,
            "errors": errs[:6], "rows": rows, "empty": empt}


def main():
    # argparse：原 `in sys.argv` 判定会把 --help 当成「没传 --shots」→
    # 不打印帮助，直接跑一轮分钟级的全量 UI 巡检。
    ap = argparse.ArgumentParser(
        prog='break_ui_check.py', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--shots', action='store_true',
                    help='额外保存截图到 tools/break_ui_shots/')
    shots = ap.parse_args().shots
    results = []
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/usr/bin/chromium",
                               args=["--allow-file-access-from-files", "--no-sandbox"])
        pg = br.new_page(viewport={"width": 1280, "height": 800})
        for label, fx in [("real", None), ("worst", fixture_worst()),
                          ("empty", fixture_empty()), ("one", fixture_one())]:
            try:
                if fx is None:          # 真实数据基线：不注入任何东西
                    results.append(run(pg, None, label, shots))
                else:
                    results.append(run(pg, fx, label, shots))
            except Exception as exc:  # noqa: BLE001
                results.append({"label": label, "error": str(exc)[:200]})
        br.close()
    print(json.dumps(results, ensure_ascii=False, indent=1))
    # 汇总成可判读的结论
    print("\n===== 结论 =====")
    # 退出码语义（原实现两头都错：夹具的注入错误让它恒 1，页面自身的破口又从不计入）：
    #   real / empty —— 页面与空态必须干净，任何一项计数或 console 错误 → 退出 1
    #   worst / one  —— 负样本，故意注入破图与溢出。它们的 404 是预期，不算失败；
    #                  反过来，若一行都没检出，说明检查器失去灵敏度 → 退出 1
    bad = 0
    INTENTIONAL = {"worst", "one"}
    for r in results:
        if "error" in r:
            print(f"[FAIL] {r['label']}: {r['error']}")
            bad += 1
            continue
        label = r["label"]
        print(f"[{label}] 降级提示={r['stale_notice']} ({r['stale_text'][:30]})")
        if r["errors"]:
            if label in INTENTIONAL:
                print(f"   console 错误 {len(r['errors'])}（夹具注入破图，预期）")
            else:
                print(f"   运行时错误 {len(r['errors'])}: {r['errors'][:2]}")
                bad += 1
        flagged_rows = 0
        for row in r["rows"]:
            flags = []
            if row["hOverflow"] > 0:
                flags.append(f'页面横向溢出 {row["hOverflow"]}px')
            if row["brokenImgs"]:
                flags.append(f'破图 {row["brokenImgs"]} 张')
            if row["overflowEls"]:
                flags.append(f'元素溢出 {len(row["overflowEls"])} 处')
            if row["undefinedText"]:
                flags.append(f'undefined/NaN 字面量 {row["undefinedText"]} 处')
            if flags:
                flagged_rows += 1
            print(f'   {row["viewport"]:8s} {row["w"]}px  ' + ("；".join(flags) if flags else "✓ 无破口"))
        if label in INTENTIONAL:
            if not flagged_rows:
                print("   [FAIL] 负样本一行都未检出 → 检查器灵敏度丢失")
                bad += 1
        elif flagged_rows:
            print(f"   [FAIL] {label} 有 {flagged_rows} 个视口报出破口")
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
