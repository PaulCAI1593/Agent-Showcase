#!/usr/bin/env python3
"""
vendor_assets.py — 把作品页引用的远程 JS 依赖本地化

背景：
  展厅作品页有 15 件依赖 cdnjs.cloudflare.com / cdn.jsdelivr.net 加载
  GSAP、ScrollTrigger、D3、topojson、Chart.js。展厅主要在内网自阅，
  一旦外网不可达或 CDN 被墙，这些页面的图表/动画**直接变空白框**
  （实测 d3 地图：有 CDN 时 1 个 SVG，无 CDN 时 0 个）。

做法：
  1. 扫描 manifest 中全部作品，收集 <script src="http..."> 依赖
  2. 下载到 showcase/assets/vendor/（按原文件名，重名时带版本目录）
  3. 把引用改写为**相对路径**（按作品所在目录深度计算）
  4. 同时保留原 CDN 地址作为 onerror 兜底：本地缺失时仍能回源

用法：
  python3 tools/vendor_assets.py --dry-run    # 只列出将要做什么
  python3 tools/vendor_assets.py              # 下载 + 改写
"""

import json, os, re, sys, time, urllib.request, urllib.error, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDOR = os.path.join(ROOT, 'assets', 'vendor')
MANIFEST = os.path.join(ROOT, 'manifest.json')

SCRIPT_RE = re.compile(r'(<script[^>]*?)\bsrc=["\'](https?://[^"\']+)["\']([^>]*?)>', re.I)

# 作品里引用了**已经 404 的** CDN 地址（该依赖其实一直没加载成功）。
# 本地化时改用同库可用版本，并把页面引用一并纠正。
URL_FIXUPS = {
    'https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.3/topojson.min.js':
        'https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.min.js',
}


def load_works():
    m = json.load(open(MANIFEST, encoding='utf-8'))
    return [i['file'] for i in m['research'] + m['creative']]


def local_name(url):
    """返回 (子目录, 文件名) —— 子目录按库名+版本区分，避免同名不同版本互相覆盖。"""
    host, _, path = url.partition('://')
    tail = path.split('/', 1)[1] if '/' in path else path
    fname = os.path.basename(tail)
    parent = tail.rsplit('/', 1)[0] if '/' in tail else host
    sub = re.sub(r'[^A-Za-z0-9._-]+', '_', parent)
    return sub, fname


def rel_from(work_rel, asset_abs):
    """作品页里应写的相对路径（考虑作品可能在日期子目录中）。"""
    work_dir = os.path.dirname(os.path.join(ROOT, work_rel))
    return os.path.relpath(asset_abs, work_dir).replace(os.sep, '/')


def main():
    dry = '--dry-run' in sys.argv
    works = load_works()

    urls = collections.Counter()
    for rel in works:
        txt = open(os.path.join(ROOT, rel), encoding='utf-8', errors='ignore').read()
        for m in SCRIPT_RE.finditer(txt):
            if m.group(2).startswith('http'):
                urls[m.group(2)] += 1

    if not urls:
        print('未发现远程 <script> 依赖，无需处理')
        return 0

    print(f'发现 {len(urls)} 个不同远程依赖，共 {sum(urls.values())} 处引用')
    os.makedirs(VENDOR, exist_ok=True)

    # 下载
    mapping = {}
    for u in sorted(urls):
        sub, fname = local_name(u)
        dst = os.path.join(VENDOR, sub, fname)
        mapping[u] = dst
        if os.path.exists(dst) and os.path.getsize(dst) > 1000:
            print(f'   已存在 {os.path.relpath(dst, ROOT)} ({os.path.getsize(dst)}B)')
            continue
        if dry:
            print(f'   [dry] 将下载 {u}  →  {os.path.relpath(dst, ROOT)}')
            continue
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            fetch_url = URL_FIXUPS.get(u, u)
            with urllib.request.urlopen(fetch_url, timeout=60) as r:
                data = r.read()
            if len(data) < 500:
                print(f'   ! 内容过小，疑似失败：{fetch_url}')
                continue
            with open(dst, 'wb') as f:
                f.write(data)
            note = f'  （原地址已 404，改用 {fetch_url.rsplit("/",1)[-1]}）' if fetch_url != u else ''
            print(f'   ✓ {os.path.relpath(dst, ROOT)} ({len(data)}B){note}')
        except Exception as e:
            print(f'   ✗ 下载失败 {u}: {e}')
            mapping.pop(u, None)

    if dry:
        print(f'\n[dry-run] 将改写 {sum(urls.values())} 处引用；未写入任何文件')
        return 0

    # 改写
    changed_files = changed_refs = 0
    for rel in works:
        p = os.path.join(ROOT, rel)
        txt = open(p, encoding='utf-8').read()
        if 'http' not in txt:
            continue

        def repl(m):
            nonlocal changed_refs
            pre, url, post = m.group(1), m.group(2), m.group(3)
            if url not in mapping:
                return m.group(0)
            local = rel_from(rel, mapping[url])
            # 保留 CDN 兜底：本地文件缺失时回源（用可用地址）
            fb = URL_FIXUPS.get(url, url)
            # 注意：SCRIPT_RE 把标签结尾的 '>' 也消费掉了，重建时必须补回，
            # 否则会产出 `<script src="..." onerror="..."</script>` 这种残缺标签。
            new = f'{pre}src="{local}"{post} onerror="this.onerror=null;this.src=\'{fb}\'">'
            # 避免重复注入（已本地化过的行）
            if 'onerror=' in post:
                return m.group(0)
            changed_refs += 1
            return new

        new_txt = SCRIPT_RE.sub(repl, txt)
        if new_txt != txt:
            # 备份名必须匹配 build_manifest.BACKUP_RE（.bak.YYYYMMDD-HHMMSS），
            # 否则会被当成新作品扫描进 manifest。
            stamp = time.strftime('%Y%m%d-%H%M%S')
            bak = p + f'.bak.{stamp}'
            if not os.path.exists(bak):
                open(bak, 'w', encoding='utf-8').write(txt)
            open(p, 'w', encoding='utf-8').write(new_txt)
            changed_files += 1

    print(f'\n已改写：{changed_refs} 处引用，涉及 {changed_files} 个文件')
    print(f'原文件备份为 *.bak.<时间戳>（生成器已自动排除，可逐个回滚）')
    print('下一步：python3 tools/build_manifest.py --check')
    return 0


if __name__ == '__main__':
    sys.exit(main())
