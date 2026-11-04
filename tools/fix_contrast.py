#!/usr/bin/env python3
"""
fix_contrast.py — 批量化修对比度（两遍 detect，逐件终局闸门）

为什么是批处理
--------------
逐件调 detect = 每件启一次浏览器。大文件（40KB+ 内联 CSS/JS）单件就要几分钟，
还会超时（实测 3 件 detect 超时）。改成：
    第 1 遍 detect（一次扫描整批） → 逐件算改色方案 → 逐件改写
    第 2 遍 detect（一次扫描整批） → 逐件比对：变差就整件回退
两遍扫描，不是 2N 遍。

安全边界（都是被棘轮抓出来的教训）
-----------------------------------
1. **终局 vs 原始**：逐件与第 1 遍的结果比，变差 → 整件回退。
   教训：多轮各自「持平」，累加后落在比原始更差的终点（119 → 373 条）。
2. **改写策略**：先规则级（只改「同规则内既有该文字色、又有匹配背景」的规则），
   定位不到再退回全局替换 —— 此时有终局闸门兜底，最坏是不改。
   教训：全局替换会把「同色异底」的另一半改坏。
3. **第 2 遍拿不到结果 → 该件不改**（「没验过」不等于「通过」）。
   教训：复验超时时闸门被跳过，坏状态直接落盘（棘轮抓到 +23）。

用法：
  python3 tools/fix_contrast.py --scope all
  python3 tools/fix_contrast.py --files a.html b.html
  python3 tools/fix_contrast.py --scope all --min-ratio 3      # 只修 <3:1 的
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

LAUNCHER_CANDIDATES = [
    os.environ.get('IMPECCABLE_BIN', ''),
    '/app/working/workspaces/default/skills/impeccable/scripts/impeccable',
    os.path.join(ROOT, '.agents/skills/impeccable/scripts/impeccable'),
]

RULE_RE = re.compile(r'([^{}]+)\{([^{}]*)\}')
FIND_RE = re.compile(r'text\s+(#[0-9a-fA-F]{3,6})\s+on\s+(#[0-9a-fA-F]{3,6})')
RATIO_RE = re.compile(r'([\d.]+):1')


# ── 颜色 ─────────────────────────────────────────────────
def hex_to_rgb(h):
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v)))) for v in rgb)


def rel_lum(rgb):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def is_light(hexc):
    return rel_lum(hex_to_rgb(hexc)) >= 0.5


def _near(a, b):
    try:
        ca, cb = hex_to_rgb(a), hex_to_rgb(b)
    except Exception:
        return False
    return sum(abs(x - y) for x, y in zip(ca, cb)) < 45


def adjust_toward(fg_hex, bg_hex, target):
    """保色相地把前景色调到对背景达标；调不到返回 None。"""
    fg, bg = hex_to_rgb(fg_hex), hex_to_rgb(bg_hex)
    if contrast(fg, bg) >= target:
        return None
    if rel_lum(bg) >= 0.5:                      # 浅底 → 前景加深
        for k in range(100, 0, -1):
            cand = tuple(c * (k / 100.0) for c in fg)
            if contrast(cand, bg) >= target:
                return rgb_to_hex(cand)
        return None
    for k in range(100, 301):                   # 深底 → 前景提亮
        t = k / 100.0
        cand = tuple(c + (255 - c) * (t - 1) for c in fg)
        if contrast(cand, bg) >= target:
            return rgb_to_hex(cand)
    return None


# ── 检测 ─────────────────────────────────────────────────
def find_launcher():
    for c in LAUNCHER_CANDIDATES:
        if c and os.path.exists(c) and os.access(c, os.X_OK):
            return c
    return None


def detect_many(files, timeout=2400):
    """一次扫描多件 → {相对路径: findings}。"""
    launcher = find_launcher()
    if not launcher or not files:
        return {}
    cmd = [launcher, 'detect'] + list(files) + ['--json']
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
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


def lc_of(findings):
    out = []
    for f in findings or []:
        if f.get('antipattern') != 'low-contrast':
            continue
        sn = f.get('snippet', '')
        m = FIND_RE.search(sn)
        r = RATIO_RE.match(sn)
        if not m:
            continue
        out.append({'text': m.group(1).lower(), 'bg': m.group(2).lower(),
                    'ratio': float(r.group(1)) if r else 0.0})
    return out


# ── 改写 ─────────────────────────────────────────────────
def fix_rules_for_color(html, color, bg, new_color):
    def do_block(m):
        sel, body = m.group(1), m.group(2)
        if not re.search(r'color\s*:\s*' + re.escape(color) + r'\b', body, re.I):
            return m.group(0)
        bgs = re.findall(r'background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})', body)
        if not bgs or not any(_near(b, bg) for b in bgs):
            return m.group(0)
        nb = re.sub(r'(color\s*:\s*)' + re.escape(color),
                    r'\g<1>' + new_color, body, count=1, flags=re.I)
        return sel + '{' + nb + '}'

    def do_style(m):
        head = m.group(0)[:m.group(0).index('>') + 1]
        return head + RULE_RE.sub(do_block, m.group(1)) + '</style>'

    return re.sub(r'<style[^>]*>(.*?)</style>', do_style, html, flags=re.S)


def replace_literal(html, old, new):
    pat = re.compile(re.escape(old), re.I)
    out, n, pos = [], 0, 0
    for m in re.finditer(r'<style[^>]*>.*?</style>', html, re.S):
        out.append(html[pos:m.start()])
        block, cnt = pat.subn(new, m.group(0))
        n += cnt
        out.append(block)
        pos = m.end()
    out.append(html[pos:])
    return ''.join(out), n


def plan_for(lcs, target):
    """为一件作品算 (颜色 → 新色) 映射：按该颜色的**全部背景**取多数方向。"""
    by_color = {}
    for x in lcs:
        by_color.setdefault(x['text'], []).append(x['bg'])
    mapping = {}
    for color, bgs in by_color.items():
        cand, darker, lighter = {}, 0, 0
        fg = hex_to_rgb(color)
        for bg in set(bgs):
            newc = adjust_toward(color, bg, target)
            if not newc:
                continue
            cand[bg] = newc
            if all(hex_to_rgb(newc)[i] <= fg[i] for i in range(3)):
                darker += 1
            else:
                lighter += 1
        if not cand:
            continue
        if darker and lighter:
            pick = (min(cand.values(), key=lambda c: sum(hex_to_rgb(c))) if darker >= lighter
                    else max(cand.values(), key=lambda c: sum(hex_to_rgb(c))))
        else:
            pick = cand[next(iter(cand))]
        if pick.lower() != color:
            mapping[color] = pick
    return mapping


def apply_mapping(html, mapping, lcs):
    applied = []
    for color, new in mapping.items():
        hit = False
        for bg in {x['bg'] for x in lcs if x['text'] == color}:
            h2 = fix_rules_for_color(html, color, bg, new)
            if h2 != html:
                html = h2
                hit = True
        if hit:
            applied.append({'from': color, 'to': new, 'mode': 'rule-scoped'})
            continue
        h2, n = replace_literal(html, color, new)
        if n:
            html = h2
            applied.append({'from': color, 'to': new, 'mode': 'global', 'count': n})
    return html, applied


# ── 主流程 ───────────────────────────────────────────────
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
    ap.add_argument('--target', type=float, default=4.5)
    ap.add_argument('--min-ratio', type=float, default=0.0,
                    help='只修低于此比值的（0=全修）')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    files = list(args.files)
    if args.scope == 'all':
        files = works()
    if args.limit:
        files = files[:args.limit]
    if not files:
        print('没有目标文件')
        return 2

    print(f'第 1 遍 detect：{len(files)} 件 …', flush=True)
    before = detect_many(files)
    if not before:
        print('✗ detect 不可用或超时，本轮不改任何文件')
        return 2

    targets, backups, plans = {}, {}, {}
    for rel, finds in before.items():
        lcs = lc_of(finds)
        if args.min_ratio:
            lcs = [x for x in lcs if x['ratio'] < args.min_ratio]
        if not lcs:
            continue
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            continue
        orig = open(full, encoding='utf-8', errors='ignore').read()
        mapping = plan_for(lcs, args.target)
        if not mapping:
            continue
        html, applied = apply_mapping(orig, mapping, lcs)
        if html == orig:
            continue
        backups[rel] = orig
        plans[rel] = applied
        targets[rel] = html
    print(f'第 1 遍：{len(before)} 件有记录，可改 {len(targets)} 件', flush=True)

    if not args.dry_run:
        for rel, html in targets.items():
            open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(html)

    print(f'第 2 遍 detect：复验 {len(targets)} 件 …', flush=True)
    after = detect_many(list(targets.keys()))

    improved, reverted, unverifiable = 0, [], []
    for rel, html in targets.items():
        n_before = len(lc_of(before.get(rel, [])))
        if rel not in after:
            unverifiable.append(rel)      # 没验过 → 不算数
            continue
        n_after = len(lc_of(after.get(rel, [])))
        if n_after > n_before:
            reverted.append((rel, n_before, n_after))
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(backups[rel])
        else:
            improved += 1

    print(f'\n✓ 变好或持平: {improved} 件')
    if reverted:
        print(f'↩ 回退（变差）: {len(reverted)} 件')
        for rel, b, a in reverted[:12]:
            print(f'    {b} → {a}  {os.path.basename(rel)}')
    if unverifiable:
        print(f'⚠ 第 2 遍没验到（保持原样）: {len(unverifiable)} 件')
        for rel in unverifiable[:8]:
            print(f'    {os.path.basename(rel)}')
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(backups[rel])

    with open('tools/fix_contrast_report.json', 'w', encoding='utf-8') as f:
        json.dump({'plans': plans, 'reverted': reverted, 'unverifiable': unverifiable,
                   'improved': improved}, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
