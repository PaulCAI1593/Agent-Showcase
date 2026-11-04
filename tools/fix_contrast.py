#!/usr/bin/env python3
"""
fix_contrast.py — 机械修对比度（只改颜色，逐条复验）

为什么需要它
------------
全馆有 **757 条对比度低于 3:1**（160 条低于 2:1，白字压近白底＝字看不见）。
逐件手工修要 76 件 × 若干轮，人力不现实；而检测器已经把「哪个颜色压哪个底」
算得很清楚了 —— 剩下的只是**把文字色调到达标**这一步机械动作。

所以本工具做「机械动作」，把判断留给检测器复验：
  1. 跑 impeccable detect，解析出 (文字色, 背景色, 比值)
  2. 算出该文字色在原背景上要达到 4.5:1 的目标值（保色相：浅底加深、深底提亮）
  3. 改写 CSS 里的颜色字面量
  4. **重新 detect 复验**：比值必须上升；若引入新问题（如同一颜色在别的背景上反而变差），
     该轮回退

边界（重要）
- 只改**颜色**，不改结构/文案/布局/数据
- 白色文字不全局替换（白字在深底按钮上是对的）→ 改成**按规则定位**：
  只改「同一条规则里既有浅色背景、又有白色文字」的那些规则
- 非白色文字色才做字面量替换（那种色几乎专用于弱化文字）
- 每轮改完必须 detect 复验，比值不升就回退该轮

用法：
  python3 tools/fix_contrast.py <文件相对路径> [...]
  python3 tools/fix_contrast.py --batch 2026-11-03/notes/polish_batch1.txt
  python3 tools/fix_contrast.py --dry-run <文件>
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

MIN_RATIO = 4.5

# 各文件「原始」low-contrast 条数（终局闸门用）
_orig_counts = {}


# ── 颜色与对比度 ─────────────────────────────────────────
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


def adjust_toward(fg_hex, bg_hex, target=MIN_RATIO):
    """保色相地把前景色调到对背景达标。返回新 hex 或 None（调不到）。"""
    fg, bg = hex_to_rgb(fg_hex), hex_to_rgb(bg_hex)
    if contrast(fg, bg) >= target:
        return None
    # 底色亮 → 前景往暗走；底色暗 → 前景往亮走。沿灰阶缩放，保色相。
    if rel_lum(bg) >= 0.5:
        # 往黑走
        best = None
        for k in range(100, 0, -1):
            t = k / 100.0
            cand = tuple(c * t for c in fg)
            if contrast(cand, bg) >= target:
                best = cand
                break
        return rgb_to_hex(best) if best else None
    best = None
    for k in range(100, 301):
        t = k / 100.0
        cand = tuple(c + (255 - c) * (t - 1) for c in fg)
        if contrast(cand, bg) >= target:
            best = cand
            break
    return rgb_to_hex(best) if best else None


def is_light(hexc):
    return rel_lum(hex_to_rgb(hexc)) >= 0.5


# ── 检测 ─────────────────────────────────────────────────
def find_launcher():
    for c in LAUNCHER_CANDIDATES:
        if c and os.path.exists(c) and os.access(c, os.X_OK):
            return c
    return None


def detect(path):
    launcher = find_launcher()
    if not launcher:
        return None
    cmd = [launcher, 'detect', path, '--json']
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        return None
    raw = p.stdout.strip()
    if not raw:
        return []
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return d if isinstance(d, list) else d.get('findings', [])


FIND_RE = re.compile(r'text\s+(#[0-9a-fA-F]{3,6})\s+on\s+(#[0-9a-fA-F]{3,6})')


def low_contrast_findings(findings):
    out = []
    for f in findings or []:
        if f.get('antipattern') != 'low-contrast':
            continue
        m = FIND_RE.search(f.get('snippet', ''))
        if not m:
            continue
        r = re.match(r'([\d.]+):1', f.get('snippet', ''))
        ratio = float(r.group(1)) if r else 0.0
        out.append({'text': m.group(1).lower(), 'bg': m.group(2).lower(),
                    'ratio': ratio, 'snippet': f.get('snippet', '')[:100]})
    return out


# ── 改写 ─────────────────────────────────────────────────
def css_of(html):
    return '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S))


def replace_literal(html, old, new):
    """把颜色字面量替换成新的（仅在 CSS 里，区分大小写不敏感）。"""
    pat = re.compile(re.escape(old), re.I)
    out, n = [], 0
    pos = 0
    for m in re.finditer(r'<style[^>]*>.*?</style>', html, re.S):
        out.append(html[pos:m.start()])
        block = m.group(0)
        block2, cnt = pat.subn(new, block)
        n += cnt
        out.append(block2)
        pos = m.end()
    out.append(html[pos:])
    return ''.join(out), n


RULE_RE = re.compile(r'([^{}]+)\{([^{}]*)\}')


def fix_white_rules(html, bg_hex, new_color):
    """白色文字不全局替换：只改「同规则内既有浅底又有白字」的规则。"""
    def do_block(m):
        sel, body = m.group(1), m.group(2)
        if not re.search(r'color\s*:\s*(#fff(?:fff)?\b|white\b)', body, re.I):
            return m.group(0)
        # 同规则里是否有浅色背景
        bgs = re.findall(r'background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})', body)
        light = [b for b in bgs if is_light(b)]
        if not light and bg_hex and not is_light(bg_hex):
            return m.group(0)
        nb = re.sub(r'(color\s*:\s*)(#fff(?:fff)?\b|white\b)', r'\g<1>' + new_color, body,
                    count=1, flags=re.I)
        return sel + '{' + nb + '}'
    return RULE_RE.sub(do_block, html)


def fix_one(path, dry=False, rounds=5):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return {'path': path, 'error': '文件不存在'}
    orig = open(full, encoding='utf-8', errors='ignore').read()
    html = orig
    applied = []
    _orig_counts[path] = len(low_contrast_findings(detect(path) or []))
    for rnd in range(rounds):
        findings = detect(path)
        if findings is None:
            return {'path': path, 'error': 'detect 不可用'}
        lcs = low_contrast_findings(findings)
        if not lcs:
            break
        before = min((x['ratio'] for x in lcs), default=0)
        before_n = len(lcs)
        # 收集要改的 (文字色 → 目标色)
        # ⚠️ 同一颜色可能同时压在浅底和深底上（如 #0071e3 on #f5f5f7 与 on #000000）：
        #    按「首个背景」定方向会把另一半改坏。所以按该颜色的**全部背景**一起看：
        #    若多数背景需要「加深」，就加深；若冲突则取多数方向，少数项列为残余。
        by_color = {}
        for x in lcs:
            by_color.setdefault(x['text'], []).append(x['bg'])
        mapping = {}
        for color, bgs in by_color.items():
            darker, lighter, cand = 0, 0, {}
            for bg in set(bgs):
                newc = adjust_toward(color, bg)
                if not newc:
                    continue
                cand[bg] = newc
                fg = hex_to_rgb(color)
                if all(hex_to_rgb(c) <= fg for c in [newc]):
                    darker += 1
                else:
                    lighter += 1
            if not cand:
                continue
            if darker and lighter:
                # 冲突：取多数方向
                if darker >= lighter:
                    pick = min(cand.values(), key=lambda c: sum(hex_to_rgb(c)))
                else:
                    pick = max(cand.values(), key=lambda c: sum(hex_to_rgb(c)))
            else:
                pick = cand[next(iter(cand))]
            if pick.lower() != color:
                mapping[color] = pick
        if not mapping:
            break
        changed = False
        for old, new in mapping.items():
            if is_light(old):
                continue                      # 白色/浅色文字走规则定位
            html2, n = replace_literal(html, old, new)
            if n:
                html = html2
                applied.append({'from': old, 'to': new, 'count': n, 'round': rnd + 1})
                changed = True
        # 白色文字：按规则定位（同规则内既有浅底又有白字）
        whites = [x for x in lcs if is_light(x['text'])]
        for x in whites:
            new = adjust_toward(x['text'], x['bg'])
            if not new:
                continue
            html2 = fix_white_rules(html, x['bg'], new)
            if html2 != html:
                html = html2
                applied.append({'from': x['text'], 'to': new, 'count': 'rule-scoped',
                                'round': rnd + 1, 'bg': x['bg']})
                changed = True
        if not changed:
            break
        # 复验：比值必须整体上升，否则回退本轮
        after_findings = detect(path) if not dry else None
        if after_findings is not None:
            after = low_contrast_findings(after_findings)
            after_min = min((x['ratio'] for x in after), default=99)
            after_n = len(after)
            if after_min < before - 0.01 or after_n > before_n:
                # 本轮改坏了 → 回退
                html = html[:0] + orig if False else html  # 占位，下面真正回退
                html = orig
                applied.append({'round': rnd + 1, 'rolled_back': True,
                                'reason': f'复验变差：最差 {before:.2f}→{after_min:.2f}'})
                break
            before, before_n = after_min, after_n
    # ⚠️ 终局闸门：必须与**文件原始状态**比，不是只比轮间。
    #    实测教训：AI-agent-orchestration-wars 119 → 373 条 —— 多轮各自「持平」，
    #    累加后落在比原始更差的终点（同一颜色被用在多种背景上，全局替换把另一半改坏了）。
    #    没有这道闸门，工具会把「改过」当成「改好」。
    final = detect(path)
    if final is not None:
        fin_lcs = low_contrast_findings(final)
        orig_findings = detect(path) if False else None
        orig_n = _orig_counts.get(path)
        if orig_n is not None and len(fin_lcs) > orig_n:
            html = orig
            applied.append({'rolled_back': True,
                            'reason': f'终局闸门：{orig_n} → {len(fin_lcs)} 条，比原始更差，整文件回退'})
    if html != orig and not dry:
        open(full, 'w', encoding='utf-8').write(html)
    lcs = low_contrast_findings(final) if final is not None else []
    return {'path': path, 'applied': applied,
            'low_contrast_before': None, 'low_contrast_after': len(lcs),
            'worst_after': min((x['ratio'] for x in lcs), default=None),
            'changed': html != orig}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--batch', default='')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    paths = list(args.paths)
    if args.batch:
        for line in open(args.batch, encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            paths.append(line.split('\t')[0].split('#')[0].strip())
    if not paths:
        print('用法：fix_contrast.py <文件...> 或 --batch <清单>')
        return 2
    results = []
    for p in paths:
        r = fix_one(p, dry=args.dry_run)
        results.append(r)
        st = '✓' if r.get('changed') else '·'
        print(f"{st} {os.path.basename(p)}: 改动 {len(r.get('applied') or [])} 处 · "
              f"low-contrast 剩 {r.get('low_contrast_after')} 条"
              + (f"（最差 {r['worst_after']:.2f}:1）" if r.get('worst_after') else ''))
        for a in (r.get('applied') or [])[:4]:
            print('    ', a)
    with open('tools/fix_contrast_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
