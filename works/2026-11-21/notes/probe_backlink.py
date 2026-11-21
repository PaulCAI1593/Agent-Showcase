#!/usr/bin/env python3
"""探针：实测 #showcase-backlink 的运行时 computed 样式与真实渲染对比度。

用法： python3 probe_backlink.py <html> [<html> ...]
输出： 每件作品一行 JSON —— class / color / background / opacity / 对比度
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

JS = r"""
() => {
  const a = document.getElementById('showcase-backlink');
  if (!a) return {err: 'no element'};
  const cs = getComputedStyle(a);
  const rgb = (s) => (s.match(/[\d.]+/g) || []).map(Number);
  const lin = (v) => { v/=255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
  const L = (c) => 0.2126*lin(c[0]) + 0.7152*lin(c[1]) + 0.0722*lin(c[2]);
  const cr = (x, y) => { const a=L(x), b=L(y); const hi=Math.max(a,b), lo=Math.min(a,b);
                         return (hi+0.05)/(lo+0.05); };
  const bgOf = (el) => { let n = el;
    while (n && n !== document.documentElement) {
      const c = rgb(getComputedStyle(n).backgroundColor);
      if (c.length >= 3 && (c.length < 4 || c[3] > 0.9)) return c.slice(0,3);
      n = n.parentElement; }
    return [255,255,255]; };
  const fg = rgb(cs.color).slice(0,3);
  const own = rgb(cs.backgroundColor);
  const op = parseFloat(cs.opacity);
  const pageBg = bgOf(a.parentElement || document.body);
  // 药丸自带不透明底 → 文字压药丸底；否则压页面底
  const hasOwn = own.length >= 3 && (own.length < 4 || own[3] > 0.9);
  // 半透明底：先与页面底合成
  let pillBg;
  if (own.length >= 3) {
    const al = own.length >= 4 ? own[3] : 1;
    pillBg = [0,1,2].map(i => al*own[i] + (1-al)*pageBg[i]);
  } else pillBg = pageBg;
  // opacity:.86 作用于整个药丸 → 文字与药丸底都与页面底混合
  const effFg = [0,1,2].map(i => op*fg[i] + (1-op)*pillBg[i]);
  const effBg = [0,1,2].map(i => op*pillBg[i] + (1-op)*pageBg[i]);
  const direct = cr(fg, pillBg);          // 不考虑 opacity（CSS 解析器视角）
  const rendered = cr(effFg, effBg);      // 真实渲染（含 opacity 混合）
  return {cls: a.className, color: cs.color, bg: cs.backgroundColor,
          opacity: op, pageBg: 'rgb(' + pageBg.join(',') + ')',
          hasOwnBg: hasOwn,
          pillBg: 'rgb(' + pillBg.map(Math.round).join(',') + ')',
          direct: +direct.toFixed(2), rendered: +rendered.toFixed(2),
          need: 4.5, pass_direct: direct >= 4.5, pass_rendered: rendered >= 4.5};
}
"""


def main():
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path='/usr/bin/chromium',
                               args=['--no-sandbox', '--allow-file-access-from-files'])
        for rel in sys.argv[1:]:
            full = rel if os.path.isabs(rel) else os.path.join(ROOT, rel)
            pg = br.new_page(viewport={'width': 1260, 'height': 800})
            try:
                pg.goto('file://' + full, wait_until='load', timeout=60000)
                pg.wait_for_timeout(1200)
                out[rel] = pg.evaluate(JS)
            except Exception as exc:                                  # noqa: BLE001
                out[rel] = {'err': str(exc)[:160]}
            finally:
                pg.close()
        br.close()
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
