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

import json, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'manifest.json')
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
    dry = '--dry-run' in sys.argv
    remove = '--remove' in sys.argv
    works = load_works()
    changed = skipped = already = 0

    for rel in works:
        p = os.path.join(ROOT, rel)
        txt = open(p, encoding='utf-8', errors='ignore').read()

        if remove:
            if MARKER not in txt:
                skipped += 1
                continue
            new = re.sub(re.escape(MARKER) + r'[\s\S]*?</a>\n?', '', txt, count=1)
            new = re.sub(r'<style>#' + STYLE_ID + r'\{[\s\S]*?</style>\n?', '', new, count=1)
            new = re.sub(r'<script id="showcase-backlink-js">[\s\S]*?</script>\n?',
                         '', new, count=1)
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
        new = txt[:mb.end()] + '\n' + snippet(index_rel_for(rel)) + txt[mb.end():]
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
