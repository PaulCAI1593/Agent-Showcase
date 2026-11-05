#!/usr/bin/env python3
"""
add_backlink.py — 给作品页注入「返回展厅」悬浮链接

背景：
  展厅是「中心页 → 作品页」的单向结构：102 个作品页里**没有任何一个**
  能回到 index.html，看完只能按浏览器后退。
  （讽刺的是已归档禁用的 update_showcase.sh 反而带 "← 返回展厅" 链接。）

做法：
  在 <body> 之后插入一个固定定位的小胶囊链接，指向 index.html
  （相对路径按作品所在目录深度计算）。注入是**幂等**的：
  已存在 marker 的文件会跳过，可安全重复运行。

用法：
  python3 tools/add_backlink.py --dry-run    # 预览
  python3 tools/add_backlink.py              # 注入
  python3 tools/add_backlink.py --remove     # 撤掉注入的链接
"""

import argparse, json, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'manifest.json')
def esc(x):
    return (str(x).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


MARKER = '<!-- showcase-backlink -->'

STYLE_ID = 'showcase-backlink'


# JS 写成普通字符串再插值 —— f-string 里满是大括号，转义极易出错。
_js = (
    # ⚠️ 必须在 DOMContentLoaded 之后探测：脚本内联在 body 里，
    # 解析期页面尚未排版，getBoundingClientRect / elementsFromPoint
    # 拿到的都是错位数据（实测深色研究页被判成浅色）。
    '(function(){'
    'function detect(){'
    'var a=document.getElementById("__ID__");if(!a)return;'
    'function lum(s){var m=String(s).match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)(?:,\\s*([\\d.]+))?\\)/);'
    'if(!m)return null;'
    'if(m[4]!==undefined&&parseFloat(m[4])===0)return null;'
    'return 0.299*m[1]+0.587*m[2]+0.114*m[3];}'
    # 判据：药丸**视觉上压着**的那个元素的底色。
    # body 常无有效底色（多行 body{} 规则读不到、深色页靠 .hero 满屏），
    # 读 body 会误判。elementsFromPoint 返回整叠，跳过药丸自身。
    'var r=a.getBoundingClientRect();'
    'var st=document.elementsFromPoint?document.elementsFromPoint(r.left+6,r.top+r.height/2):[];'
    'var L=null;'
    'for(var i=0;i<st.length;i++){var u=st[i];'
    'if(u===a||(a.contains&&a.contains(u)))continue;'
    'L=lum(getComputedStyle(u).backgroundColor);if(L!==null)break;}'
    'if(L===null){u=document.body;'
    'while(u){L=lum(getComputedStyle(u).backgroundColor);if(L!==null)break;u=u.parentElement;}}'
    'if(L===null)L=255;'
    'a.classList.add(L<128?"on-dark-page":"on-light-page");}'
    'if(document.readyState==="loading")'
    'document.addEventListener("DOMContentLoaded",detect);else detect();'
    '})();'
)

# ── 档案条 ──────────────────────────────────────────────────
# 每件作品顶部横一条暗色窄条：日期 · 追踪线 · 该月件数 · 回到柜子。
# 目的：106 件作品页各自为政（浅色/深色/Apple/档案卷宗四种风格），
# 用同一条窄条把它们的"归属"说清楚 —— 这件是哪天的、哪条线的、
# 柜子第几格。数据全部来自 manifest，自动更新。
BAR_ID = 'showcase-bar'


def bar_html(rel, meta):
    m = meta or {}
    bits = []
    if m.get('date'):
        bits.append('<span class="sb-date">%s</span>' % esc(m['date']))
    if m.get('beat'):
        bits.append('<span class="sb-beat">%s</span>' % esc(m['beat']))
    if m.get('month_count'):
        bits.append('<span class="sb-cnt">%s 件 / %s</span>'
                    % (m['month_count'], esc(m.get('month') or '')))
    if m.get('claim_count'):
        bits.append('<span class="sb-cnt sb-claims">%s 条已验证断言</span>'
                    % m['claim_count'])
    sep = '<span class="sb-sep">/</span>'
    body = sep.join(bits)
    B = BAR_ID
    css = (
        f'#{B}{{position:relative;z-index:5;display:flex;align-items:center;gap:14px;'
        f'flex-wrap:wrap;padding:9px 20px;background:#0b0c12;color:rgba(255,255,255,.62);'
        f'border-bottom:1px solid rgba(255,255,255,.09);'
        f'font:12px/1.4 -apple-system,BlinkMacSystemFont,"SF Pro Text","Noto Sans SC",sans-serif;'
        f'letter-spacing:.02em}}'
        f'#{B} .sb-brand{{font-family:Georgia,"Songti SC",serif;color:#f0c27f;'
        f'letter-spacing:.16em;text-transform:uppercase;font-size:11px}}'
        f'#{B} .sb-sep{{color:rgba(255,255,255,.2)}}'
        f'#{B} .sb-beat{{color:#a78bfa}}'
        f'#{B} .sb-cnt{{color:rgba(255,255,255,.48)}}'  # 4.36:1(.44) 不达 WCAG AA 4.5:1 → .48 = 5.01:1
        f'#{B} .sb-back{{margin-left:auto;color:#f5e6c8;text-decoration:none;'
        f'border:1px solid rgba(245,230,200,.28);border-radius:980px;padding:4px 12px;'
        f'font-size:11.5px;transition:background .2s,border-color .2s}}'
        f'#{B} .sb-back:hover{{background:rgba(245,230,200,.14);border-color:rgba(245,230,200,.5)}}'
        f'@media(max-width:640px){{#{B}{{gap:9px;padding:8px 14px;font-size:11px}}'
        f'#{B} .sb-back{{margin-left:0;order:9}}}}'
    )
    return (
        f'{MARKER}\n<style>{css}</style>\n'
        f'<div id="{B}"><span class="sb-brand">Zhinang Archive</span>'
        + (sep if body else '') + body
        + f'<a class="sb-back" href="{esc(index_rel_for(rel))}">回到柜子</a></div>\n'
    )


# ── 死规则救援 ────────────────────────────────────────────────
# 有一批作品写了「滚动显现」的样式（.fade-in / .reveal / .rv … 设 opacity:0），
# 但**没有任何规则或 JS 让它变可见** —— 内容永久隐藏，整页视觉全黑。
# 实测 59 件作品有 281 处这种死规则（缩略图全黑、首页卡片是黑块）。
#
# 这里不改动作者写的 CSS（保留原意），而是**追加一条覆盖规则**把内容放出来：
#   <被隐藏类>{opacity:1!important;visibility:visible!important;transform:none!important}
# 关键是只对「设了 opacity:0 且全篇没有可见对应物」的选择器生效。

RULE_RE = re.compile(r'([^{}]+)\{([^{}]*)\}', re.S)
_KEYFRAME_STEP = re.compile(r'^(from|to|\d+%)$')


def dead_rules(html):
    """找出「永久隐藏内容」的选择器。"""
    css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S))
    if not css:
        return []
    rules = RULE_RE.findall(css)
    # 收集所有选择器 → 是否有可见对应物
    visible = set()
    for sel, body in rules:
        sel_c = ' '.join(sel.split())
        if _KEYFRAME_STEP.match(sel_c.strip()):
            continue
        if re.search(r'opacity\s*:\s*(1|0\.[1-9])', body) or 'animation' in body:
            visible.add(sel_c)
    dead = []
    for sel, body in rules:
        sel_c = ' '.join(sel.split())
        if _KEYFRAME_STEP.match(sel_c.strip()):
            continue
        if '::' in sel_c or ',' in sel_c:
            continue                       # 伪元素 / 组合选择器：不动
        if not re.search(r'opacity\s*:\s*0(?![.\d])', body):
            continue
        if sel_c in visible:
            continue                       # 有对应物（正常显现）
        # 「前缀式」对应物也算活着：.hero-title 的对应物常写成 .hero-title.visible
        # / .hero-title.in-view —— 精确匹配会漏判，把正常作品误判成死规则。
        alive = False
        pat = re.compile(r'(^|[\s,])' + re.escape(sel_c) + r'(?![\w-])')
        for o, b in rules:
            if o.strip() == sel_c:
                continue
            if pat.search(' '.join(o.split())) and (
                    re.search(r'opacity\s*:\s*(1|0\.[1-9])', b) or 'animation' in b):
                alive = True
                break
        if alive:
            continue
        if sel_c not in [d[0] for d in dead]:
            dead.append((sel_c, 'transform' in body))
    return dead


def rescue_css(html):
    dead = dead_rules(html)
    sels = []
    for sel, has_tf in dead:
        decl = 'opacity:1!important;visibility:visible!important'
        if has_tf:
            decl += ';transform:none!important'
        sels.append(f'{sel}{{{decl}}}')
    # 预加载遮罩没被关掉 → 整页被盖住（黑屏）。JS 失败时就会这样。
    if re.search(r'id=["\']preloader["\']', html, re.I):
        sels.append('#preloader{display:none!important;opacity:0!important;pointer-events:none!important}')
    if not sels:
        return ''
    return ('<style id="showcase-rescue">/* 死规则救援：把被永久隐藏的内容放出来 */'
            + ''.join(sels) + '</style>\n')

_ARTIFACTS = [
    r'<!--\s*showcase-backlink\s*-->\s*',
    r'<style>\s*#showcase-bar\{.*?</style>\s*',
    r'<style>\s*#showcase-backlink\{.*?</style>\s*',
    r'<style\s+id="showcase-rescue">.*?</style>\s*',
    r'<div\s+id="showcase-bar">.*?</div>\s*',
    r'<a\s+id="showcase-backlink"[^>]*>.*?</a>\s*',
    r'<script\s+id="showcase-backlink-js">.*?</script>\s*',
    r'</div>\s*',
    r'回到柜子</a>\s*',
]


def strip_injected(html):
    """从 body 开头反复剥离所有注入物与历史残渣，直到稳定。

    为什么不能只用一条正则：注入物里有嵌套（档案条内部还有一个 <a>），
    而早期的移除正则 `MARKER…</a>` 会撞上档案条内部的链接 —— 把档案条
    整段吃掉并留下孤立的 </div>，108 件作品全被注入了畸形 HTML。
    改成「从 body 开头逐段剥离」，每一步都可验证、不靠猜。
    """
    m = re.search(r'<body[^>]*>', html, re.I)
    if not m:
        return html
    head, rest = html[:m.end()], html[m.end():]
    changed = True
    while changed:
        changed = False
        t = rest.lstrip('\n\r\t ')
        for pat in _ARTIFACTS:
            mm = re.match(pat, t, re.S | re.I)
            if mm:
                rest = t[mm.end():]
                changed = True
                break
    return head + '\n' + rest


def snippet(index_rel: str) -> str:
    return (
        f'{MARKER}\n'
        f'<style>#{STYLE_ID}{{position:fixed;left:16px;bottom:16px;z-index:99999;'
        f'display:inline-flex;align-items:center;gap:7px;padding:9px 15px;'
        f'border-radius:980px;font:500 13px/1 -apple-system,BlinkMacSystemFont,"SF Pro Text","Noto Sans SC",sans-serif;'
        f'text-decoration:none;transition:opacity .2s,transform .2s,background .2s,color .2s,border-color .2s;'
        f'opacity:.86}}'
        f'#{STYLE_ID}:hover{{opacity:1;transform:translateY(-1px)}}'
        # 底色自适应：作品页有浅色（档案卷宗）与深色（早期作品）两种，
        # 固定深色药丸贴在浅纸上会很跳。用页面底色亮度决定药丸明暗。
        # 类名语义消歧义：on-dark-page = 页面是深色 → 药丸用**浅色**（浅底深字）
        # on-light-page = 页面是浅色 → 药丸用**深色**（深底浅字）
        # ⚠️ 之前把「页面深色」与「药丸深色」混为一谈，导致深色页贴深色药丸。
        f'#{STYLE_ID}.on-dark-page{{color:#14130f;background:rgba(252,252,250,.92);'
        f'border:1px solid rgba(0,0,0,.10);backdrop-filter:blur(10px);'
        f'-webkit-backdrop-filter:blur(10px)}}'
        f'#{STYLE_ID}.on-light-page{{color:#fafafa;background:rgba(20,19,15,.82);'
        f'border:1px solid rgba(255,255,255,.16);backdrop-filter:blur(10px);'
        f'-webkit-backdrop-filter:blur(10px)}}'
        f'#{STYLE_ID} svg{{width:14px;height:14px;fill:none;stroke:currentColor;'
        f'stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}}</style>\n'
        f'<a id="{STYLE_ID}" href="{index_rel}" aria-label="返回档案柜">'
        f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h13M13 7l5 5-5 5"/>'
        f'<path d="M4 5.5h16M4 18.5h16"/></svg>'
        f'<span>回到档案柜</span></a>\n'
        f'<script id="showcase-backlink-js">{_js.replace("__ID__", STYLE_ID)}</script>\n'
    )


def index_rel_for(work_rel: str) -> str:
    work_dir = os.path.dirname(os.path.join(ROOT, work_rel))
    return os.path.relpath(os.path.join(ROOT, 'index.html'), work_dir).replace(os.sep, '/')


def manifest_meta():
    """从 manifest.json 取每件作品的档案条元数据。

    档案条要说的就是「这件属于哪里」：日期、追踪线、该月有多少件、
    有多少条已验证断言 —— 全部自动更新，不需要人工维护。
    """
    try:
        m = json.load(open(MANIFEST, encoding='utf-8'))
    except Exception:
        return {}
    items = list(m.get('research', [])) + list(m.get('creative', []))
    months = {}
    for it in items:
        k = (it.get('date') or '')[:7]
        months[k] = months.get(k, 0) + 1
    out = {}
    for it in items:
        out[it['file']] = {
            'date': it.get('date') or '',
            'beat': it.get('beat') or '',
            'month': (it.get('date') or '')[:7],
            'month_count': months.get((it.get('date') or '')[:7], 0),
            'claim_count': len(it.get('claims') or []),
        }
    return out


def load_works():
    """
    列出要注入返回链的作品页。

    ⚠️ 必须**扫磁盘**，不能读 manifest。
    原因：autopublish 的阶段 5.5 在阶段 6（重建 manifest）**之前**执行，
    此刻 manifest 还是旧的 —— 新交付的作品根本不在里面，于是拿不到返回链。
    （2026-10-26 端到端验证实测：新作品返回链缺失，校验⑨报 2 条。）
    磁盘才是"哪些是作品"的真相源。
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import build_manifest
        return build_manifest.scan_works()
    except Exception:
        # 兜底：万一 build_manifest 不可用，至少别让整个流水线挂掉
        m = json.load(open(MANIFEST, encoding='utf-8'))
        return [i['file'] for i in m['research'] + m['creative']]


def main():
    # argparse：原 `in sys.argv` 判定会把 --help 等未知参数静默当正常执行，
    # 而本脚本会写作品 HTML —— 诊断命令直接落盘。写盘工具必须先过 argparse。
    ap = argparse.ArgumentParser(
        prog='add_backlink.py', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='只预览，不写作品 HTML')
    ap.add_argument('--remove', action='store_true', help='移除已注入的返回链与档案条')
    a = ap.parse_args()
    dry, remove = a.dry_run, a.remove
    works = load_works()
    changed = skipped = already = 0

    for rel in works:
        p = os.path.join(ROOT, rel)
        txt = open(p, encoding='utf-8', errors='ignore').read()

        if remove:
            new = strip_injected(txt)
            if not dry:
                open(p, 'w', encoding='utf-8').write(new)
            changed += 1
            continue

        if MARKER in txt:
            already += 1
            continue
        mb = re.search(r'<body[^>]*>', txt, re.I)
        if not mb:
            skipped += 1
            continue
        meta_all = manifest_meta()
        new = (txt[:mb.end()]
               + '\n' + bar_html(rel, meta_all.get(rel))
               + rescue_css(txt)
               + snippet(index_rel_for(rel))
               + txt[mb.end():])
        if dry:
            changed += 1
            continue
        bak = p + f'.bak.{time.strftime("%Y%m%d-%H%M%S")}'
        if not os.path.exists(bak):
            open(bak, 'w', encoding='utf-8').write(txt)
        open(p, 'w', encoding='utf-8').write(new)
        changed += 1

    verb = '移除' if remove else ('将注入' if dry else '已注入')
    print(f'{verb} {changed} 个作品页；已有链接跳过 {already}；无 <body> 跳过 {skipped}')
    if dry:
        print('[dry-run] 未写入任何文件')
    elif not remove:
        print('原文件备份为 *.bak.<时间戳>（生成器已自动排除）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
