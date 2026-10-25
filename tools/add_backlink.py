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


def snippet(index_rel: str) -> str:
    return (
        f'{MARKER}\n'
        f'<style>#{STYLE_ID}{{position:fixed;left:16px;bottom:16px;z-index:99999;'
        f'display:inline-flex;align-items:center;gap:6px;padding:8px 14px;'
        f'border-radius:980px;font:500 13px/1 -apple-system,BlinkMacSystemFont,"SF Pro Text","Noto Sans SC",sans-serif;'
        f'color:#fff;text-decoration:none;background:rgba(0,0,0,.62);'
        f'border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(10px);'
        f'-webkit-backdrop-filter:blur(10px);opacity:.82;transition:opacity .2s,transform .2s}}'
        f'#{STYLE_ID}:hover{{opacity:1;transform:translateY(-1px)}}</style>\n'
        f'<a id="{STYLE_ID}" href="{index_rel}">← 返回展厅</a>\n'
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
            new = re.sub(re.escape(MARKER) + r'[\s\S]*?<a id="' + STYLE_ID + r'"[^>]*>[^<]*</a>\n?',
                         '', txt, count=1)
            new = re.sub(r'<style>#' + STYLE_ID + r'\{[\s\S]*?</style>\n?', '', new, count=1)
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
