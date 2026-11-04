#!/usr/bin/env python3
"""
fix_contrast_dom.py — 用**页内 DOM 取证**修对比度（按元素精修，可规模化）

为什么必须走到 DOM 这一层
------------------------
impeccable detect 对 low-contrast **不给 selector**（2961 条里带 selector 的 0 条），
只给「前景色 + 背景色 + 比值」。机械改法只能猜：
同一颜色常同时压在浅底正文与深底强调上，改色会互相伤害 —— 实测多件因此变差
（119 → 373 条）。

但**浏览器里能算出确切答案**：逐元素取 computed color，再沿祖先链找到真正生效的
背景色，算出比值。这样就知道「哪个元素、什么色、压什么底」，可以：

  ① 颜色只压这一种底 → 就地改该颜色字面量（精确）
  ② 同一颜色压多种底 → 在 <style> 末尾追加**覆盖规则**，只针对这组元素

流程（每件）：
  载入 → DOM 取证 → 分组算新色 → 改写 → **重新载入取证复验** → 变差就整件回退
复验用同一套页内取证（不依赖 detect），所以能验证「实际渲染」而非静态推断。

用法：
  python3 tools/fix_contrast_dom.py --files a.html b.html
  python3 tools/fix_contrast_dom.py --list 2026-11-03/notes/contrast_worst_12.txt --skip 4
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
  const parse = (s) => { const m = s.match(/[\d.]+/g); return m ? m.map(Number) : null; };
  const bgOf = (el) => { let n = el;
    while (n && n !== document.documentElement) {
      const c = getComputedStyle(n).backgroundColor; const p = parse(c);
      if (p && (p[3] === undefined || p[3] > 0.9)) return c; n = n.parentElement; }
    return 'rgb(255,255,255)'; };
  const path = (el) => {
    const parts = [];
    let n = el;
    for (let i = 0; i < 3 && n && n.nodeType === 1 && n !== document.body; i++) {
      const cls = (n.className && n.className.toString ? n.className.toString() : '').trim().split(/\s+/)[0];
      parts.unshift(n.tagName.toLowerCase() + (cls ? '.' + cls : ''));
      n = n.parentElement;
    }
    return parts.join(' > ');
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
    const big = fs >= 24 || (fs >= 18.66 && +cs.fontWeight >= 700);
    const need = big ? 3 : 4.5;
    if (cr < need) out.push({sel: path(el), fg, bg, cr: +cr.toFixed(2), need,
                             fs: cs.fontSize, txt: txt.slice(0,24)});
  });
  return out;
}
"""


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


def adjust_toward(fg_hex, bg_hex, target):
    fg, bg = hex_to_rgb(fg_hex), hex_to_rgb(bg_hex)
    if not fg or not bg:
        return None
    if contrast(fg, bg) >= target:
        return None
    if rel_lum(bg) >= 0.5:
        for k in range(100, 0, -1):
            cand = tuple(c * (k / 100.0) for c in fg)
            if contrast(cand, bg) >= target:
                return rgb_to_hex(cand)
        return None
    for k in range(100, 301):
        t = k / 100.0
        cand = tuple(c + (255 - c) * (t - 1) for c in fg)
        if contrast(cand, bg) >= target:
            return rgb_to_hex(cand)
    return None


def inspect_files(paths):
    """载入每件并做页内取证 → {相对路径: [问题元素]}"""
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
            except Exception as exc:                     # noqa: BLE001
                out[rel] = []
                print(f'  ! {os.path.basename(rel)} 取证失败: {str(exc)[:80]}')
            finally:
                pg.close()
        br.close()
    return out


def plan(items):
    """按 (前景色, 背景色) 分组 → {组: 新色} 与要加的覆盖规则。"""
    groups = {}
    for it in items:
        fgh = rgb_str_to_hex(it['fg'])
        bgh = rgb_str_to_hex(it['bg'])
        if not fgh or not bgh:
            continue
        groups.setdefault((fgh, bgh, it['need']), []).append(it)
    plan_out = []
    for (fgh, bgh, need), els in groups.items():
        new = adjust_toward(fgh, bgh, need)
        if not new:
            continue
        sels = sorted({e['sel'] for e in els})
        plan_out.append({'from': fgh, 'bg': bgh, 'to': new, 'need': need,
                         'count': len(els), 'selectors': sels[:8]})
    return plan_out


def apply_plan(html, plan_out):
    """优先就地改颜色字面量；同一颜色压多种底时追加覆盖规则。"""
    notes = []
    by_from = {}
    for p in plan_out:
        by_from.setdefault(p['from'], []).append(p)
    for fgh, ps in by_from.items():
        bgs = {p['bg'] for p in ps}
        if len(bgs) == 1:
            new = ps[0]['to']
            html2 = re.sub(re.escape(fgh), new, html, flags=re.I)
            if html2 != html:
                html = html2
                notes.append({'from': fgh, 'to': new, 'mode': 'literal'})
        else:
            rules = []
            for p in ps:
                for s in p['selectors']:
                    rules.append(f'{s}{{color:{p["to"]} !important}}')
            css = '\n/* 对比度修复（页内取证生成） */\n' + '\n'.join(rules) + '\n'
            if '</style>' in html:
                i = html.rfind('</style>')
                html = html[:i] + css + html[i:]
            else:
                html += css
            notes.append({'from': fgh, 'to': [p['to'] for p in ps], 'mode': 'override'})
    return html, notes



def detect_many(files, timeout=2400):
    """一次扫描多件 → {相对路径: findings}。检测器是权威判据。"""
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--files', nargs='*', default=[])
    ap.add_argument('--list', default='')
    ap.add_argument('--skip', type=int, default=0, help='跳过清单前 N 件（别人在做）')
    ap.add_argument('--take', type=int, default=0)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    paths = list(args.files)
    if args.list:
        for line in open(args.list, encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            paths.append(line.split('\t')[0].split('#')[0].strip())
    paths = paths[args.skip:]
    if args.take:
        paths = paths[:args.take]
    if not paths:
        print('没有目标文件')
        return 2

    # 检测器「前」基线必须先测（改动前的权威状态），否则闸门无参照
    print(f'第 0 遍 detect（权威基线）：{len(paths)} 件 …', flush=True)
    det_before = detect_many(paths)
    print(f'第 1 遍取证：{len(paths)} 件 …', flush=True)
    before = inspect_files(paths)
    todo = {r: items for r, items in before.items() if items}
    print(f'取证到 {sum(len(v) for v in todo.values())} 个低对比元素，'
          f'涉及 {len(todo)} 件', flush=True)

    changed = {}
    for rel, items in todo.items():
        full = os.path.join(ROOT, rel)
        orig = open(full, encoding='utf-8', errors='ignore').read()
        p = plan(items)
        if not p:
            continue
        html, notes = apply_plan(orig, p)
        if html != orig:
            changed[rel] = (orig, html, notes)
    print(f'可改 {len(changed)} 件', flush=True)
    if not args.dry_run:
        for rel, (orig, html, notes) in changed.items():
            open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(html)

    # ⚠️ 终局判据必须是**检测器**，不是页内取证。
    #    实测教训：页内取证说「变好」、检测器说「变坏」（棘轮抓到 low-contrast +161）——
    #    页内取证只看叶元素的 computed style，检测器还看伪元素/渐变文字/背景图，
    #    两者口径不同。棘轮用检测器，工具就必须用同一个判据，否则闸门形同虚设。
    print(f'第 2 遍 detect（权威判据）：复验 {len(changed)} 件 …', flush=True)
    det_after = detect_many(list(changed.keys()))
    improved, reverted, unver = [], [], []
    for rel, (orig, html, notes) in changed.items():
        nb = len(lc_count(det_before.get(rel, [])))
        na = len(lc_count(det_after.get(rel, [])))
        if rel not in det_before:          # 前基线缺失 → 没参照，不动
            unver.append(rel)
            continue
        if na > nb:
            reverted.append((rel, nb, na))
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(orig)
        else:
            improved.append((rel, nb, na))
    print(f'\n✓ 变好或持平: {len(improved)} 件')
    for rel, b, a in sorted(improved, key=lambda x: x[1] - x[2])[:12]:
        print(f'    低对比元素 {b} → {a}  {os.path.basename(rel)}')
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

    with open('tools/fix_contrast_dom_report.json', 'w', encoding='utf-8') as f:
        json.dump({'improved': improved, 'reverted': reverted,
                   'unverifiable': unver,
                   'notes': {r: v[2] for r, v in changed.items()}},
                  f, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
