#!/usr/bin/env python3
"""
contrast_forensics.py — 页内 DOM 取证：定位每一处低对比元素的
「哪个元素 / 什么前景色 / 压什么底 / 需要多少」。

为什么需要它
------------
impeccable detect 对 low-contrast 只给「前景色 + 背景色 + 比值」，
**不给 selector**（2961 条里带 selector 的 0 条）。
同一颜色常同时压在浅底与深底两种背景上，按颜色猜着改会互相伤害。

所以：把页面在浏览器里打开，逐元素取 computed color，
沿祖先链找到真正生效的背景，算出比值与唯一 selector。

比 detect 多做的事
------------------
1. 解析 **渐变背景**（detect 报 "gradient on div.xxx"，DOM 取证能拿到渐变色标）
2. 给每个问题元素一条**唯一可定位**的 CSS selector
3. 输出 (前景色, 背景色) 分组，直接对应「改哪一组」

用法：
  python3 tools/contrast_forensics.py <html> [<html> ...]
  python3 tools/contrast_forensics.py --json <html> ...
  python3 tools/contrast_forensics.py --out evidence.json <html> ...
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 页内取证 JS（题目给定脚本 + 渐变背景 + 唯一 selector + 祖先链）
INSPECT_JS = r"""
() => {
  const lum = (c) => { const s = c.map(v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); });
    return 0.2126*s[0] + 0.7152*s[1] + 0.0722*s[2]; };
  const parse = (s) => { const m = s.match(/[\d.]+/g); return m ? m.map(Number) : null; };
  const bgOf = (el) => { let n = el;
    while (n && n !== document.documentElement) { const c = getComputedStyle(n).backgroundColor;
      const p = parse(c); if (p && (p[3] === undefined || p[3] > 0.9)) return c; n = n.parentElement; }
    return 'rgb(255,255,255)'; };
  const bgOwner = (el) => { let n = el;
    while (n && n !== document.documentElement) { const c = getComputedStyle(n).backgroundColor;
      const p = parse(c); if (p && (p[3] === undefined || p[3] > 0.9)) return n; n = n.parentElement; }
    return document.body; };
  const own = (n) => { const c = (n.className && n.className.toString ? n.className.toString() : '').trim();
    const f = c.split(/\s+/).filter(Boolean);
    return n.tagName.toLowerCase() + (f.length ? '.' + f.join('.') : ''); };
  const cls = (n) => { const c = (n.className && n.className.toString ? n.className.toString() : '').trim();
    return c.split(/\s+/).filter(Boolean)[0] || ''; };
  const uniq = (el) => {
    // 生成一条尽量唯一的 selector：优先 id，其次逐级祖先 class 组合
    const chain = [];
    let n = el, depth = 0;
    while (n && n.nodeType === 1 && depth < 5) {
      let s = n.tagName.toLowerCase();
      if (n.id) { chain.unshift(s + '#' + n.id); break; }
      const c = cls(n);
      if (c) s += '.' + c;
      chain.unshift(s);
      n = n.parentElement; depth++;
    }
    const cand = chain.join(' > ');
    try { const m = document.querySelectorAll(cand); if (m.length === 1) return cand; } catch (e) {}
    // 回退：加 :nth-of-type
    let sel = el.tagName.toLowerCase();
    const c = cls(el); if (c) sel += '.' + c;
    try { const m = document.querySelectorAll(sel);
      if (m.length > 1) { const i = [...m].indexOf(el); sel += ':nth-of-type(' + (i+1) + ')'; }
    } catch (e) {}
    return sel;
  };
  const gradOf = (el) => {
    // 沿祖先链找最近的渐变背景，返回 {stops:[hex], owner:selector}
    let n = el;
    while (n && n.nodeType === 1) {
      const bi = getComputedStyle(n).backgroundImage;
      if (bi && bi !== 'none' && bi.indexOf('gradient') >= 0) {
        const cols = (bi.match(/rgba?\([^)]*\)/g) || []).map(s => {
          const m = s.match(/[\d.]+/g).map(Number);
          return '#' + m.slice(0,3).map(v => ('0'+Math.round(v).toString(16)).slice(-2)).join('');
        });
        return {stops: cols, owner: uniq(n)};
      }
      n = n.parentElement;
    }
    return null;
  };
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    if (el.children.length) return;
    const txt = (el.innerText || '').trim();
    if (!txt) return;
    const cs = getComputedStyle(el);
    const fg = cs.color, bg = bgOf(el);
    const f = parse(fg), b = parse(bg);
    if (!f || !b) return;
    const L1 = lum(f.slice(0,3)), L2 = lum(b.slice(0,3));
    const cr = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    const fs = parseFloat(cs.fontSize);
    const fw = +cs.fontWeight;
    const big = fs >= 24 || (fs >= 18.66 && fw >= 700);
    const need = big ? 3 : 4.5;
    const grad = gradOf(el);
    if (cr >= need && !grad) return;
    const owner = bgOwner(el);
    out.push({sel: uniq(el), tag: el.tagName.toLowerCase(),
              cls: cls(el), own: own(el),
              ctx: own(owner), ctxTag: owner.tagName.toLowerCase(),
              fg, bg, cr: +cr.toFixed(2), need,
              fs: cs.fontSize, fw: fw, big: big,
              grad: grad ? grad.stops : null, gradOwner: grad ? grad.owner : null,
              txt: txt.slice(0,26)});
  });
  return out;
}
"""

HEX_RE = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')


def hex_to_rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) < 6:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v)))) for v in rgb)


def rel_lum(rgb):
    def f(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def rgb_str_to_hex(s):
    m = re.findall(r'[\d.]+', s)
    if not m or len(m) < 3:
        return None
    try:
        r, g, b = (int(float(x)) for x in m[:3])
    except ValueError:
        return None
    return '#%02x%02x%02x' % (r, g, b)


def inspect(paths):
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path='/usr/bin/chromium',
                               args=['--no-sandbox', '--allow-file-access-from-files'])
        for full in paths:
            pg = br.new_page(viewport={'width': 1260, 'height': 800})
            try:
                pg.goto('file://' + full, wait_until='load', timeout=60000)
                pg.wait_for_timeout(1500)
                out[full] = pg.evaluate(INSPECT_JS)
            except Exception as exc:                                  # noqa: BLE001
                out[full] = []
                print(f'  ! {os.path.basename(full)} 取证失败: {str(exc)[:100]}')
            finally:
                pg.close()
        br.close()
    return out


def main():
    args = sys.argv[1:]
    as_json = '--json' in args
    outf = None
    if '--out' in args:
        i = args.index('--out')
        outf = args[i + 1]
        del args[i:i + 2]
    files = args
    if not files:
        print(__doc__)
        return 2
    paths = [f if os.path.isabs(f) else os.path.join(ROOT, f) for f in files]
    res = inspect(paths)
    if outf:
        with open(outf, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0

    for full, items in res.items():
        print(f'\n{"="*70}\n{os.path.relpath(full, ROOT)}  —— {len(items)} 个低对比元素')
        groups = {}
        for it in items:
            key = (it['fg'], it['bg'], it['need'])
            groups.setdefault(key, []).append(it)
        for (fg, bg, need), els in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            grad = [e for e in els if e.get('grad')]
            print(f'\n  ▸ fg={fg}  bg={bg}  need={need}  ×{len(els)}')
            if grad:
                stops = sorted({s for e in grad for s in e['grad']})
                print(f'      渐变底: {stops}  容器: {grad[0]["gradOwner"]}')
            seen = set()
            for e in els:
                if e['sel'] in seen:
                    continue
                seen.add(e['sel'])
                print(f'      {e["cr"]:>5}:1  {e["sel"]}   «{e["txt"]}»')
                if len(seen) >= 8:
                    break
    return 0


if __name__ == '__main__':
    sys.exit(main())
