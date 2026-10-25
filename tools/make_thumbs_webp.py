#!/usr/bin/env python3
"""
make_thumbs_webp.py — 从 PNG 源图生成卡片用 WebP 缩略图

背景：
  展厅缩略图原本是 1190×660 左右的 PNG，平均 211KB，102 张共 21MB，
  而卡片实际显示宽度只有约 370px —— 3~4 倍冗余，且截图用 PNG 是错格式。
  转成 720px 宽 WebP 后 21MB → 1.34MB（约 1/16），肉眼无可见质量损失。

目录约定：
  _private/thumbs-src/*.png   高清源图（serve.py 已屏蔽，不对外提供）
  thumbs/*.webp               对外实际引用的缩略图

用法：
  python3 tools/make_thumbs_webp.py            # 增量：只生成缺失/过旧的 webp
  python3 tools/make_thumbs_webp.py --force    # 全部重新生成
"""

import os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_private', 'thumbs-src')
OUT = os.path.join(ROOT, 'thumbs')
MAX_W = 720          # 卡片显示约 370px，2x 足够覆盖常见高分屏
QUALITY = 78


def convert_one(src_path, quality=QUALITY):
    """
    把单张 PNG 源图转成 thumbs/ 下的同名 .webp。
    供 autopublish 在新截图落地后即时调用，避免对外目录堆积大 PNG。
    返回生成的 webp 路径。
    """
    from PIL import Image
    dst = os.path.join(OUT, os.path.basename(src_path)[:-4] + '.webp')
    os.makedirs(OUT, exist_ok=True)
    im = Image.open(src_path).convert('RGB')
    if im.width > MAX_W:
        im.thumbnail((MAX_W, MAX_W * 3), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=quality, method=6)
    return dst


def main():
    force = '--force' in sys.argv
    try:
        from PIL import Image
    except ImportError:
        print('需要 Pillow：pip install Pillow')
        return 1

    srcs = sorted(glob.glob(os.path.join(SRC, '*.png')))
    if not srcs:
        print(f'未找到源图目录内容：{SRC}')
        return 1
    os.makedirs(OUT, exist_ok=True)

    made = skipped = 0
    for s in srcs:
        dst = os.path.join(OUT, os.path.basename(s)[:-4] + '.webp')
        if not force and os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(s):
            skipped += 1
            continue
        im = Image.open(s).convert('RGB')
        if im.width > MAX_W:
            im.thumbnail((MAX_W, MAX_W * 3), Image.LANCZOS)
        im.save(dst, 'WEBP', quality=QUALITY, method=6)
        made += 1

    total = sum(os.path.getsize(os.path.join(OUT, f))
                for f in os.listdir(OUT) if f.endswith('.webp'))
    print(f'生成 {made} 张，跳过 {skipped} 张（已是最新）')
    print(f'thumbs/ 当前共 {total/1048576:.2f} MB')
    print('下一步：python3 tools/build_manifest.py   # 让 manifest 指向 webp')
    return 0


if __name__ == '__main__':
    sys.exit(main())
