#!/usr/bin/env python3
"""
fix_design_dom.py — 用页内计算样式修剩余设计问题（伪元素 / 渐变文字 / 阴影 / 边框）

补齐 fix_contrast_dom.py 的盲点
------------------------------
上一轮结论是「DOM 取证对剩余问题几乎无效」，原因很具体：页内取证只看
**叶元素的 computed color**，而检测器报的 low-contrast 里大量来自：
  ① 伪元素（::before / ::after 里的文字）
  ② 渐变文字（color: transparent + background-clip: text）
  ③ 阴影/背景图相关的元素

本工具把这三类都读出来（getComputedStyle(el, '::before') 能拿到伪元素的
计算样式），再对**具体元素**追加覆盖规则，而不是猜颜色字面量。

覆盖四类：
  low-contrast          —— 含伪元素与渐变文字
  dark-glow             —— 计算后的阴影若为「零偏移 + 彩色」→ 改中性 + 给偏移
  border-accent-on-rounded —— 圆角元素上 border-*-width ≥2px → 1px
  side-tab              —— 伪元素画的绝对定位条纹（width/height ≥2px）→ 1px

终局判据：**检测器**（不是页内取证）—— 上一轮的教训：两套口径不一致时，
工具说「变好」而棘轮说「变坏」（+161 条）。

用法：
  python3 tools/fix_design_dom.py --files a.html b.html
  python3 tools/fix_design_dom.py --scope all
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

INSPECT_JS = r"""
() => {
  const lum = (c) => { const s = c.map(v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); });
    return 0.2126*s[0] + 0.7152*s[1] + 0.0722*s[2]; };
  const parse = (s) => { const m = (s||'').match(/[\d.]+/g); return m ? m.map(Number) : null; };
  const bgOf = (el) => { let n = el;
    while (n && n !== document.documentElement) {
      const c = getComputedStyle(n).backgroundColor; const p = parse(c);
      if (p && (p[3] === undefined || p[3] > 0.9)) return c; n = n.parentElement; }
    return 'rgb(255,255,255)'; };
  const path = (el, pseudo) => {
    const parts = []; let n = el;
    for (let i = 0; i < 3 && n && n.nodeType === 1 && n !== document.body; i++) {
      const cls = (n.className && n.className.toString ? n.className.toString() : '').trim().split(/\s+/)[0];
      parts.unshift(n.tagName.toLowerCase() + (cls ? '.' + cls : ''));
      n = n.parentElement;
    }
    return parts.join(' > ') + (pseudo || '');
  };
  const out = [];
  const check = (el, cs, pseudo, txt) => {
    // 渐变文字：color 透明 + background-clip:text → 用渐变首色当前景
    let fg = cs.color;
    const bi = cs.backgroundImage || '';
    if (/gradient/.test(bi) && /text/.test(cs.webkitBackgroundClip || cs.backgroundClip || '')) {
      const g = bi.match(/linear-gradient\(([^)]*)\)/);
      if (g) { const c = g[1].match(/#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)/);
               if (c) fg = c[0]; }
    }
    const f = parse(fg), bg = bgOf(el);
    const b = parse(bg);
    if (f && b) {
      const L1 = lum(f.slice(0,3)), L2 = lum(b.slice(0,3));
      const cr = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
      const fs = parseFloat(cs.fontSize);
      const big = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700);
      const need = big ? 3 : 4.5;
      if (cr < need) out.push({kind:'contrast', sel:path(el,pseudo), fg, bg, cr:+cr.toFixed(2),
                               need, fs: cs.fontSize, txt:(txt||'').slice(0,22)});
    }
    // 阴影：零偏移 + 彩色 → 发光
    const sh = cs.boxShadow && cs.boxShadow !== 'none' ? cs.boxShadow : '';
    if (sh) {
      const m = sh.match(/rgba?\(([^)]*)\)\s*(-?[\d.]+)px\s*(-?[\d.]+)px/);
      if (m) {
        const rgb = m[1].split(',').map(Number);
        const ox = parseFloat(m[2]), oy = parseFloat(m[3]);
        const chroma = rgb.length >= 3 ? (Math.max(rgb[0],rgb[1],rgb[2]) - Math.min(rgb[0],rgb[1],rgb[2])) : 0;
        if (chroma > 30 && Math.abs(ox) < 0.5 && Math.abs(oy) < 0.5)
          out.push({kind:'glow', sel:path(el,pseudo), color:'rgb('+rgb.slice(0,3).join(',')+')',
                    alpha: rgb[3] === undefined ? 1 : rgb[3]});
      }
    }
    // 圆角元素上的粗边框
    const bw = parseFloat(cs.borderTopWidth);
    const br = parseFloat(cs.borderTopLeftRadius);
    if (bw >= 2 && br >= 8)
      out.push({kind:'accent-border', sel:path(el,pseudo), w: cs.borderTopWidth});
    // 伪元素画的绝对定位条纹
    if (pseudo) {
      const w = parseFloat(cs.width), h = parseFloat(cs.height);
      if ((w >= 2 || h >= 2) && cs.position === 'absolute')
        out.push({kind:'stripe', sel:path(el,pseudo), w: cs.width, h: cs.height});
    }
  };
  document.querySelectorAll('body *').forEach(el => {
    const txt = (el.innerText || '').trim();
    if (!el.children.length && txt) check(el, getComputedStyle(el), null, txt);
    for (const ps of ['::before','::after']) {
      const cs = getComputedStyle(el, ps);
      if (cs && cs.content && cs.content !== 'none' && cs.content !== 'normal') {
        const t = cs.content.replace(/^["']|["']$/g,'');
        if (t && t.trim()) check(el, cs, ps, t);
      }
    }
  });
  return out;
}
"""


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v)))) for v in rgb)


def hex_to_rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


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


def str_to_rgb(s):
    m = re.findall(r'[\d.]+', s or '')
    if len(m) < 3:
        return None
    try:
        return tuple(int(float(x)) for x in m[:3])
    except ValueError:
        return None


def adjust_toward(fg, bg, target):
    if contrast(fg, bg) >= target:
        return None
    if rel_lum(bg) >= 0.5:
        for k in range(100, 0, -1):
            cand = tuple(c * (k / 100.0) for c in fg)
            if contrast(cand, bg) >= target:
                return cand
        return None
    for k in range(100, 301):
        t = k / 100.0
        cand = tuple(c + (255 - c) * (t - 1) for c in fg)
        if contrast(cand, bg) >= target:
            return cand
    return None


def inspect_files(paths):
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path='/usr/bin/chromium',
                               args=['--no-sandbox', '--allow-file-access-from-files'])
        for rel in paths:
            full = os.path.join(ROOT, rel)
            if not os.path.exists(full):
                continue
            pg = br.new_page(viewport={'width': 1260, 'height': 800})
            try:
                pg.goto('file://' + full, wait_until='load')
                pg.wait_for_timeout(600)
                out[rel] = pg.evaluate(INSPECT_JS)
            except Exception as exc:                       # noqa: BLE001
                out[rel] = []
                print(f'  ! {os.path.basename(rel)} 取证失败: {str(exc)[:70]}')
            finally:
                pg.close()
        br.close()
    return out


def detect_many(files, timeout=2400):
    launcher = (os.environ.get('IMPECCABLE_BIN', '')
                or '/app/working/workspaces/default/skills/impeccable/scripts/impeccable')
    if not os.path.exists(launcher) or not files:
        return {}
    try:
        p = subprocess.run([launcher, 'detect'] + list(files) + ['--json'],
                           cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {}
    raw = p.stdout.strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if isinstance(data, dict):
        data = data.get('findings', [])
    out = {}
    for f in data:
        rel = f.get('file', '')
        if rel.startswith('file://'):
            rel = rel[len('file://'):]
        rel = rel.replace(ROOT + '/', '').replace(ROOT, '')
        out.setdefault(rel, []).append(f)
    return out


def lc_count(findings):
    return [f for f in findings or [] if f.get('antipattern') == 'low-contrast']


def build_rules(items):
    """把取证结果变成 CSS 覆盖规则（按元素选择器，精确不误伤）。"""
    rules = {}
    for it in items:
        if it['kind'] == 'contrast':
            fg = str_to_rgb(it['fg'])
            bg = str_to_rgb(it['bg'])
            if not fg or not bg:
                continue
            new = adjust_toward(fg, bg, it['need'])
            if not new:
                continue
            key = (it['sel'], 'color')
            val = rgb_to_hex(new)
            rules.setdefault(key, val)
        elif it['kind'] == 'glow':
            c = str_to_rgb(it['color'])
            if not c:
                continue
            y = round(rel_lum(c))
            a = it.get('alpha', 1)
            rules.setdefault((it['sel'], 'box-shadow'),
                             f'0 2px 10px rgba({y},{y},{y},{a})')
        elif it['kind'] == 'accent-border':
            rules.setdefault((it['sel'], 'border-top-width'), '1px')
        elif it['kind'] == 'stripe':
            rules.setdefault((it['sel'], 'width'), '1px')
    return rules


def apply_rules(html, rules):
    if not rules:
        return html
    lines = []
    for (sel, prop), val in rules.items():
        lines.append(f'{sel}{{{prop}:{val} !important}}')
    css = ('\n/* 设计修复（页内计算样式取证生成） */\n' + '\n'.join(lines) + '\n')
    if '</style>' in html:
        i = html.rfind('</style>')
        return html[:i] + css + html[i:]
    return html + css


def works():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if not d.startswith('.') and d not in ('tools', 'templates', '_archive',
                                                            '_private', 'thumbs', 'assets', 'notes')]
        for fn in filenames:
            if fn.endswith('.html') and not fn.startswith('.') and '.bak' not in fn:
                out.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--files', nargs='*', default=[])
    ap.add_argument('--scope', default='')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    paths = list(args.files) or (works() if args.scope == 'all' else [])
    if not paths:
        print('没有目标文件')
        return 2

    print(f'第 0 遍 detect（权威基线）：{len(paths)} 件 …', flush=True)
    det_before = detect_many(paths)
    print(f'第 1 遍取证：{len(paths)} 件 …', flush=True)
    before = inspect_files(paths)
    n_items = sum(len(v) for v in before.values())
    kinds = {}
    for v in before.values():
        for it in v:
            kinds[it['kind']] = kinds.get(it['kind'], 0) + 1
    print(f'取证到 {n_items} 个问题：{kinds}', flush=True)

    changed = {}
    for rel, items in before.items():
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            continue
        orig = open(full, encoding='utf-8', errors='ignore').read()
        rules = build_rules(items)
        html = apply_rules(orig, rules)
        if html != orig:
            changed[rel] = (orig, html, len(rules))
    print(f'可改 {len(changed)} 件', flush=True)
    if not args.dry_run:
        for rel, (orig, html, n) in changed.items():
            open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(html)

    print(f'第 2 遍 detect（权威判据）：复验 {len(changed)} 件 …', flush=True)
    det_after = detect_many(list(changed.keys()))
    improved, reverted, unver = [], [], []
    for rel, (orig, html, n) in changed.items():
        if rel not in det_before:
            unver.append(rel)
            continue
        nb, na = len(lc_count(det_before.get(rel, []))), len(lc_count(det_after.get(rel, [])))
        worse = False
        # ⚠️ gray-on-color 也要盯：为过对比度而加深的灰度，落在彩色面上
        #    会被另一条规则捕获（实测 +20）。闸门漏盯 = 工具自伤。
        for rule in ('low-contrast', 'dark-glow', 'border-accent-on-rounded',
                     'side-tab', 'gray-on-color'):
            b = len([f for f in det_before.get(rel, []) if f.get('antipattern') == rule])
            a = len([f for f in det_after.get(rel, []) if f.get('antipattern') == rule])
            if a > b:
                worse = True
        if worse:
            reverted.append((rel, nb, na))
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(orig)
        else:
            improved.append((rel, nb, na))
    print(f'\n✓ 变好或持平: {len(improved)} 件')
    for rel, b, a in sorted(improved, key=lambda x: x[1] - x[2])[:10]:
        print(f'    low-contrast {b} → {a}  {os.path.basename(rel)}')
    if reverted:
        print(f'↩ 回退（变差）: {len(reverted)} 件')
        for rel, b, a in reverted[:10]:
            print(f'    {b} → {a}  {os.path.basename(rel)}')
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(changed[rel][0])
    if unver:
        print(f'⚠ 没验到（保持原样）: {len(unver)} 件')
        for rel in unver[:8]:
            print(f'    {os.path.basename(rel)}')
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(changed[rel][0])

    with open('tools/fix_design_dom_report.json', 'w', encoding='utf-8') as f:
        json.dump({'improved': improved, 'reverted': reverted, 'unverifiable': unver,
                   'kinds': kinds, 'items': n_items}, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
