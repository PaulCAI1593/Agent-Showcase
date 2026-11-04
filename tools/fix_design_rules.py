#!/usr/bin/env python3
"""
fix_design_rules.py — 机械修 impeccable 的可机械修规则（批量、逐件终局闸门）

为什么能修这些
--------------
low-contrast 修不动（检测器不给 selector，只能按颜色猜），但积压里有一批
规则的触发点**在源码里是确定性的**：

| 规则 | 触发形态 | 修法 | 风险 |
|---|---|---|---|
| tiny-text | `font-size: 11.5px`（<12px） | 提到 12px | 低（小幅） |
| undersized-ui-text | `font-size: 12px`（<14px） | 提到 14px | 中（版面会动） |
| bounce-easing | `cubic-bezier(...)` 带回弹（y>1） | 换成标准 ease-out | 低 |
| pulsing-dot | `animation: ... pulse ...` | 去掉该动画 | 低 |
| gradient-text | `background-clip: text` + `color: transparent` | 改成实色 | 低 |
| side-tab | 卡片上 `border-left/right: ≥2px solid <色>` | 降到 1px | 中（视觉身份） |
| border-accent-on-rounded | 同规则里既有粗边框又有 border-radius | 边框降到 1px | 中 |

**不做**的：dark-glow（阴影形态多，改动易失真）、ai-color-palette（配色判断）、
kicker-above-heading / numbered-section-labels（要动文案结构，是内容决策）。

安全边界（与 fix_contrast.py 同一套教训）
----------------------------------------
1. **终局 vs 原始**：逐件逐规则比对，变差 → 整件回退。
2. **第 2 遍没验到 → 不写盘**（「没验过」不等于「通过」）。
3. 改完只碰颜色/字号/动画属性，**不碰文案、数字、结构、数据**。
4. 版面可能被动（字号变大）→ 交付前必须跑 audit_pages。

用法：
  python3 tools/fix_design_rules.py --scope all
  python3 tools/fix_design_rules.py --files a.html b.html
  python3 tools/fix_design_rules.py --scope all --rules tiny-text undersized-ui-text
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

SIZE_RE = re.compile(r'([\d.]+)\s*px')
MIN_SIZE = {'tiny-text': 12.0, 'undersized-ui-text': 14.0}
EASE_OUT = 'cubic-bezier(.16,1,.3,1)'


def find_launcher():
    for c in LAUNCHER_CANDIDATES:
        if c and os.path.exists(c) and os.access(c, os.X_OK):
            return c
    return None


def detect_many(files, timeout=2400):
    launcher = find_launcher()
    if not launcher or not files:
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


def counts(findings):
    c = {}
    for f in findings or []:
        r = f.get('antipattern', '?')
        c[r] = c.get(r, 0) + 1
    return c


def style_blocks(html):
    return re.findall(r'<style[^>]*>.*?</style>', html, re.S)


def edit_styles(html, fn):
    """对 <style> 块**与内联 style 属性**都应用 fn。

    只改 <style> 会漏掉内联样式里的缓动/阴影 —— 实测 bounce-easing 残余 16 条
    就在内联 style 里。
    """
    def do(m):
        blk = m.group(0)
        head = blk[:blk.index('>') + 1]
        return head + fn(blk[blk.index('>') + 1:-len('</style>')]) + '</style>'
    html = re.sub(r'<style[^>]*>.*?</style>', do, html, flags=re.S)

    def do_attr(m):
        return 'style="' + fn(m.group(1)) + '"'
    html = re.sub(r'style="([^"]*)"', do_attr, html)
    return html


# ── 各规则的修法 ─────────────────────────────────────────
def fix_sizes(html, findings, rule):
    """把被点名的过小字号提到该规则的门槛。"""
    threshold = MIN_SIZE[rule]
    sizes = set()
    for f in findings:
        for m in SIZE_RE.finditer(f.get('snippet', '')):
            try:
                v = float(m.group(1))
            except ValueError:
                continue
            if v < threshold:
                sizes.add(m.group(0))
    if not sizes:
        return html, []
    changed = []

    def fn(block):
        out = block
        for s in sizes:
            num = float(SIZE_RE.match(s).group(1))
            new = f'{threshold:g}px'
            pat = re.compile(r'(font-size\s*:\s*)' + re.escape(s), re.I)
            out, n = pat.subn(r'\g<1>' + new, out)
            if n:
                changed.append({'from': s, 'to': new, 'count': n})
            # font: 12px/1.4 ... 简写里的字号
            pat2 = re.compile(r'(font\s*:\s*(?:[^;{}]*?))' + re.escape(s))
            out, n2 = pat2.subn(r'\g<1>' + new, out)
            if n2:
                changed.append({'from': s, 'to': new, 'count': n2, 'via': 'font 简写'})
        return out
    return edit_styles(html, fn), changed


def fix_bounce(html, findings, rule):
    """回弹缓动（cubic-bezier 的 y 超出 [0,1]）→ 标准 ease-out。"""
    def fn(block):
        out = block

        def repl(m):
            args = [x.strip() for x in m.group(1).split(',')]
            try:
                ys = [float(a) for a in args if re.fullmatch(r'-?[\d.]+', a)]
            except ValueError:
                return m.group(0)
            if not ys or max(ys) <= 1.0:
                return m.group(0)
            return 'cubic-bezier(' + EASE_OUT + ')'
        out = re.sub(r'cubic-bezier\(([^)]*)\)', repl, out)
        return out
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'bounce-easing', 'to': EASE_OUT}])


def fix_pulse(html, findings, rule):
    """呼吸点：去掉 pulse 动画（装饰性动画模拟「活着的」状态）。"""
    def fn(block):
        out = block
        out = re.sub(r'animation\s*:\s*[^;{}]*\b(pulse|pulsing|blink|blip)\w*[^;{}]*;?',
                     'animation:none;', out, flags=re.I)
        return out
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'pulsing-dot', 'to': 'animation:none'}])


def fix_gradient_text(html, findings, rule):
    """渐变文字 → 实色（渐变文字是装饰而非信息）。"""
    def fn(block):
        out = block
        # 找出 background-clip:text 的规则，把 color:transparent 换成渐变里的第一个色
        def do_rule(m):
            sel, body = m.group(1), m.group(2)
            if not re.search(r'background-clip\s*:\s*text', body, re.I):
                return m.group(0)
            grad = re.search(r'linear-gradient\(([^)]*)\)', body, re.I)
            color = None
            if grad:
                for c in re.findall(r'#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)', grad.group(1)):
                    color = c
                    break
            if not color:
                color = 'currentColor'
            nb = re.sub(r'color\s*:\s*transparent', 'color:' + color, body, flags=re.I)
            nb = re.sub(r'-webkit-text-fill-color\s*:\s*transparent',
                        '-webkit-text-fill-color:' + color, nb, flags=re.I)
            nb = re.sub(r'background\s*:\s*linear-gradient\([^;]*\)', 'background:none', nb,
                        flags=re.I)
            return sel + '{' + nb + '}'
        out = re.sub(r'([^{}]+)\{([^{}]*)\}', do_rule, out)
        return out
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'gradient-text', 'to': '实色'}])


def fix_side_tab(html, findings, rule):
    """单侧粗色边框 → 1px（AI 生成 UI 最容易认出的特征）。"""
    def fn(block):
        return re.sub(r'border-(left|right)\s*:\s*([2-9]|\d{2,})px\s+(solid|double)',
                      r'border-\1:1px \3', block, flags=re.I)
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'side-tab', 'to': '1px'}])


def _desat(color_hex):
    """把彩色转为同亮度的中性灰（保留 alpha）。

    ⚠️ 阴影多数写作 rgba(...) 而不是 hex —— 只认 hex 会让整类修法静默失效
    （实测 dark-glow 166 条一条没动就是这个原因）。
    """
    if color_hex.lower().startswith('rgba'):
        nums = re.findall(r'[\d.]+', color_hex)
        if len(nums) < 3:
            return None
        r, g, b = (int(float(x)) for x in nums[:3])
        a = nums[3] if len(nums) > 3 else '1'
        if max(r, g, b) - min(r, g, b) < 30:
            return None
        y = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
        return f'rgba({y},{y},{y},{a})'
    h = color_hex.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) < 6:
        return None
    try:
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None
    if max(r, g, b) - min(r, g, b) < 30:          # 本来就是中性色
        return None
    y = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
    return f'#{y:02x}{y:02x}{y:02x}'


def fix_dark_glow(html, findings, rule):
    """零偏移彩色光晕 → 中性阴影 + 一个真实偏移（craft-floor：发光阴影是 AI 味）。"""
    def fn(block):
        out = block

        def repl_shadow(m):
            prop, body = m.group(1), m.group(2)
            # 只处理「0 偏移」的阴影（0 0 blur color）
            if not re.match(r'\s*0(?:px)?\s+0(?:px)?\s+', body):
                return m.group(0)
            # ⚠️ 73/90 处零偏移阴影的颜色是 var(--xxx) 间接引用 —— 静态脱不了色。
            #    但「零偏移彩色光晕」这条规则的**核心是零偏移**：
            #    给一个真实偏移（0 2px）就解掉了，保留原有色彩与设计意图。
            def col(mc):
                d = _desat(mc.group(1))
                return mc.group(0) if not d else d
            nb = re.sub(r'(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))', col, body, flags=re.I)
            nb = re.sub(r'^(\s*)0(?:px)?\s+0(?:px)?\s+', r'\g<1>0 2px ', nb)
            if nb == body:
                return m.group(0)
            return f'{prop}: {nb}'

        out = re.sub(r'((?:box|text)-shadow)\s*:\s*([^;{}]+)', repl_shadow, out, flags=re.I)
        return out
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'dark-glow', 'to': '中性化 + 偏移'}])



def fix_border_accent_rounded(html, findings, rule):
    """圆角元素上的粗边框 → 降到 1px（craft-floor：圆角与粗色边框相撞）。"""
    def fn(block):
        out = block

        def do_rule(m):
            sel, body = m.group(1), m.group(2)
            if not re.search(r'border-radius\s*:\s*(\d+px|9999px|50%|\d+rem)', body, re.I):
                return m.group(0)
            nb = re.sub(r'border-(top|left|right|bottom)\s*:\s*([2-9]|\d{2,})px\s+(solid|dashed|double)',
                         r'border-\1:1px \3', body, flags=re.I)
            if nb == body:
                return m.group(0)
            return sel + '{' + nb + '}'

        return re.sub(r'([^{}]+)\{([^{}]*)\}', do_rule, out)
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'border-accent-on-rounded', 'to': '1px'}])


def fix_side_tab_pseudo(html, findings, rule):
    """伪元素画的单侧粗条纹 → 降到 1px（AI 生成 UI 最易认的特征）。"""
    def fn(block):
        out = block

        def do_rule(m):
            sel, body = m.group(1), m.group(2)
            if '::before' not in sel and '::after' not in sel:
                return m.group(0)
            if 'position' not in body or 'absolute' not in body:
                return m.group(0)
            nb = re.sub(r'(width|height)\s*:\s*([2-9]|\d{2,})px', r'\1:1px', body)
            if nb == body:
                return m.group(0)
            return sel + '{' + nb + '}'

        return re.sub(r'([^{}]+)\{([^{}]*)\}', do_rule, out)
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'side-tab', 'to': '1px'}])



def fix_cramped_padding(html, findings, rule):
    """内容紧贴边框/背景（无内缩）→ 给点 padding。

    检测器直接点名了 class（片段形如 `\"table-wrap\": children flush against border`），
    按 class 精确加内缩即可，不猜。
    """
    classes = set()
    for f in findings:
        for m in re.finditer(r'"([a-zA-Z][\w-]*)"\s*:', f.get('snippet', '')):
            classes.add(m.group(1))
    if not classes:
        return html, []
    if not classes:
        return html, []
    # ⚠️ 必须**追加到样式表末尾**：插在规则体开头的 padding 会被同规则后面的
    #    padding 声明覆盖（同规则内后者胜）—— 实测这样改 33 件一条没降。
    rules = '\n'.join(f'.{c}{{padding:10px !important}}' for c in sorted(classes))
    css = '/* cramped-padding 修复 */\n' + rules + '\n'
    if '</style>' in html:
        i = html.rfind('</style>')
        out = html[:i] + css + html[i:]
    else:
        out = html + css
    return out, [{'rule': 'cramped-padding', 'to': 'padding:10px !important',
                  'classes': sorted(classes)}]


def fix_codex_grid(html, findings, rule):
    """两轴网格线渐变背景 → 去掉（craft-floor：网格底纹需要有真实的画布/蓝图做底）。"""
    # 两轴网格 = 同一条声明里出现两次 repeating-linear-gradient
    classes = set()
    for m in re.finditer(r'([.#][\w-]+)\s*\{[^}]*repeating-linear-gradient[^}]*repeating-linear-gradient',
                         html, re.S):
        classes.add(m.group(1))
    if not classes:
        return html, []
    rules = '\n'.join(f'{c}{{background-image:none !important}}' for c in sorted(classes))
    css = '/* codex-grid-background 修复 */\n' + rules + '\n'
    i = html.rfind('</style>')
    out = (html[:i] + css + html[i:]) if i > 0 else html + css
    return out, [{'rule': 'codex-grid-background', 'to': '去除网格底纹',
                  'classes': sorted(classes)}]


def fix_bounce_keyframes(html, findings, rule):
    """@keyframes bounce 的过冲（scale>1 / translateY 幅度大）→ 收敛成平缓位移。

    检测器片段形如 `animation: bounce` —— 指的是用了 bounce 关键帧动画。
    不删动画（会改变作者的设计），而是把过冲压掉。
    """
    def fn(block):
        out = block
        def soften(m):
            kf = m.group(0)
            kf = re.sub(r'scale\(\s*(1\.\d+)\s*\)', 'scale(1)', kf)
            kf = re.sub(r'translateY\(\s*(-?[\d.]+)px\s*\)',
                        lambda mm: 'translateY(%spx)' % (float(mm.group(1)) * 0.4), kf)
            return kf
        # 关键帧名有多种变体：bounce / bounceDown / shield-bounce / bounce-arrow / cue-bounce
        out = re.sub(r'@keyframes\s+[\w-]*bounce[\w-]*\s*\{.*?\n\}', soften, out, flags=re.S)
        out = re.sub(r'@keyframes\s+[\w-]*bounce[\w-]*\s*\{[^{}]*\{[^{}]*\}[^{}]*\}',
                     soften, out, flags=re.S)
        return out
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'bounce-easing', 'to': '收敛 bounce 过冲'}])


def _px_of(val, unit):
    try:
        v = float(val)
    except ValueError:
        return None
    if unit == 'px':
        return v
    if unit in ('rem', 'em'):
        return v * 16.0          # 根字号近似 16px（em 相对父级，取近似）
    if unit == 'pt':
        return v * 1.3333
    return None


def fix_undersized_ui(html, findings, rule):
    """过小字号 → 提到 11px 下限。

    检测器报的是**计算后**的字号（如 9.6px / 10.4px）—— 源码里往往写成
    0.6rem / 0.65em 这类相对单位，字面量匹配不到 → 必须按计算值反推。
    """
    floor = 11.0
    def fn(block):
        out = block
        def repl(m):
            val, unit = m.group(1), m.group(2)
            px = _px_of(val, unit)
            if px is None or px >= floor:
                return m.group(0)
            if unit in ('rem',):
                newv = '%.4frem' % (floor / 16.0)
            elif unit == 'em':
                newv = '%.4fem' % (floor / 16.0)
            else:
                newv = '%gpx' % floor
            return f'font-size:{newv}'
        out = re.sub(r'font-size\s*:\s*([\d.]+)(px|rem|em|pt)\b', repl, out, flags=re.I)
        return out
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'undersized-ui-text', 'to': '提到 11px'}])


def fix_gradient_text_v2(html, findings, rule):
    """渐变文字（background-clip:text）→ 改实色。

    上一版要求「同一规则体内同时有 color:transparent」，实际作品常把 color 写在
    另一条规则里 → 整类漏掉（实测 30 条一条没清）。
    现在：命中 background-clip:text 的规则，直接给它补一个实色 color。
    """
    def fn(block):
        out = block
        def do_rule(m):
            sel, body = m.group(1), m.group(2)
            if not re.search(r'(-webkit-)?background-clip\s*:\s*text', body, re.I):
                return m.group(0)
            if re.search(r'color\s*:\s*transparent', body, re.I):
                return m.group(0)
            g = re.search(r'linear-gradient\(([^)]*)\)', body, re.I)
            color = None
            if g:
                c = re.findall(r'#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)', g.group(1))
                if c:
                    color = c[0]
            if not color:
                return m.group(0)
            return sel + '{' + body.rstrip().rstrip(';') + ';color:' + color + ' !important;}'
        return re.sub(r'([^{}]+)\{([^{}]*)\}', do_rule, out)
    new = edit_styles(html, fn)
    return new, ([] if new == html else [{'rule': 'gradient-text', 'to': '改实色'}])


def _hex_to_hsl(rgb):
    import colorsys
    r, g, b = [c / 255.0 for c in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l


def _hsl_to_hex(h, s, l):
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h, l, max(0.0, min(1.0, s)))
    return '#%02x%02x%02x' % (int(r * 255 + .5), int(g * 255 + .5), int(b * 255 + .5))


def _rel_lum(rgb):
    def f(c):
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast(a, b):
    la, lb = _rel_lum(a), _rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def fix_gray_on_color(html, findings, rule):
    """彩色底上的灰字 → 染上底色相（craft-floor：「never gray」）。

    检测器直接给出配对：`text #b0b8c4 on bg #16213e` —— 实测 43 条全是同一对，
    一次字面量替换即可全部解决。做法：把前景色的**色相**换成背景色的色相，
    再微调亮度直到对比度达标（保持原有明暗关系）。
    """
    pairs = []
    for f in findings:
        m = re.search(r'text\s+(#[0-9a-fA-F]{3,6})\s+on\s+(#[0-9a-fA-F]{3,6})',
                      f.get('snippet', ''))
        if m:
            pairs.append((m.group(1).lower(), m.group(2).lower()))
    if not pairs:
        return html, []
    notes = []
    for fg_hex, bg_hex in set(pairs):
        fg = _hex_rgb(fg_hex)
        bg = _hex_rgb(bg_hex)
        if not fg or not bg:
            continue
        fh, fs, fl = _hex_to_hsl(fg)
        bh, bs, bl = _hex_to_hsl(bg)
        new_sat = max(fs, min(bs, 0.45))
        best = None
        for dl in [i / 100.0 for i in range(-100, 101)]:
            cand_l = fl + dl * 0.9
            if not (0.02 <= cand_l <= 0.98):
                continue
            cand = _hsl_to_hex(bh, new_sat, cand_l)
            c = _hex_rgb(cand)
            if c and _contrast(c, bg) >= 4.5:
                best = cand
                break
        if not best:
            continue
        html2 = re.sub(re.escape(fg_hex), best, html, flags=re.I)
        if html2 != html:
            html = html2
            notes.append({'from': fg_hex, 'to': best, 'bg': bg_hex})
    return html, ([{'rule': 'gray-on-color', 'to': '染底色相'}] if notes else [])


def _hex_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def fix_codex_grid_v2(html, findings, rule):
    """两轴网格底纹 → 去掉（selector 未必是 class，元素选择器也算）。"""
    classes = set()
    for m in re.finditer(r'([^{}]{1,80}?)\s*\{[^}]*repeating-linear-gradient[^}]*repeating-linear-gradient',
                         html, re.S):
        sel = m.group(1).strip()
        if sel and not sel.startswith('@'):
            classes.add(sel.split(',')[0].strip())
    if not classes:
        return html, []
    rules = '\n'.join(f'{c}{{background-image:none !important}}' for c in sorted(classes))
    css = '/* codex-grid-background 修复 */\n' + rules + '\n'
    i = html.rfind('</style>')
    out = (html[:i] + css + html[i:]) if i > 0 else html + css
    return out, [{'rule': 'codex-grid-background', 'to': '去除网格底纹',
                  'selectors': sorted(classes)}]

FIXERS = {
    'tiny-text': lambda h, f, r: fix_sizes(h, f, r),
    'undersized-ui-text': lambda h, f, r: fix_sizes(h, f, r),
    'bounce-easing': fix_bounce,
    'pulsing-dot': fix_pulse,
    'gradient-text': fix_gradient_text,
    'side-tab': fix_side_tab,
    'dark-glow': fix_dark_glow,
    'border-accent-on-rounded': fix_border_accent_rounded,
    'side-tab': fix_side_tab_pseudo,
    'cramped-padding': fix_cramped_padding,
    'codex-grid-background': fix_codex_grid,
    'bounce-easing': fix_bounce_keyframes,
    'undersized-ui-text': fix_undersized_ui,
    'gradient-text': fix_gradient_text_v2,
    'gray-on-color': fix_gray_on_color,
    'codex-grid-background': fix_codex_grid_v2,
}


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
    ap.add_argument('--rules', nargs='*', default=list(FIXERS.keys()))
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    files = list(args.files) or (works() if args.scope == 'all' else [])
    if not files:
        print('没有目标文件')
        return 2

    print(f'第 1 遍 detect：{len(files)} 件 …', flush=True)
    before = detect_many(files)
    if not before:
        print('✗ detect 不可用/超时，本轮不改任何文件')
        return 2

    targets, backups, applied_all = {}, {}, {}
    for rel, finds in before.items():
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            continue
        orig = open(full, encoding='utf-8', errors='ignore').read()
        html = orig
        applied = []
        for rule in args.rules:
            fs = [f for f in finds if f.get('antipattern') == rule]
            if not fs:
                continue
            html2, ch = FIXERS[rule](html, fs, rule)
            if html2 != html:
                html = html2
                applied.append({'rule': rule, 'changes': ch[:6]})
        if html != orig:
            backups[rel] = orig
            applied_all[rel] = applied
            targets[rel] = html
    print(f'第 1 遍：{len(before)} 件有记录，可改 {len(targets)} 件', flush=True)
    if not args.dry_run:
        for rel, html in targets.items():
            open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(html)

    print(f'第 2 遍 detect：复验 {len(targets)} 件 …', flush=True)
    after = detect_many(list(targets.keys()))
    improved, reverted, unver = [], [], []
    for rel, html in targets.items():
        if rel not in after:
            unver.append(rel)
            continue
        cb, ca = counts(before.get(rel, [])), counts(after.get(rel, []))
        worse = any(ca.get(r, 0) > cb.get(r, 0) for r in set(cb) | set(ca))
        if worse:
            reverted.append((rel, sum(cb.values()), sum(ca.values())))
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(backups[rel])
        else:
            improved.append((rel, sum(cb.values()), sum(ca.values())))
    print(f'\n✓ 变好或持平: {len(improved)} 件')
    for rel, b, a in sorted(improved, key=lambda x: x[1] - x[2])[:10]:
        print(f'    {b} → {a}  {os.path.basename(rel)}')
    if reverted:
        print(f'↩ 回退（变差）: {len(reverted)} 件')
        for rel, b, a in reverted[:10]:
            print(f'    {b} → {a}  {os.path.basename(rel)}')
    if unver:
        print(f'⚠ 没验到（保持原样）: {len(unver)} 件')
        for rel in unver[:8]:
            print(f'    {os.path.basename(rel)}')
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(backups[rel])

    with open('tools/fix_design_rules_report.json', 'w', encoding='utf-8') as f:
        json.dump({'applied': applied_all, 'improved': improved,
                   'reverted': reverted, 'unverifiable': unver},
                  f, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
