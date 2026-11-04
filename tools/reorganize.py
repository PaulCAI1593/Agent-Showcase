#!/usr/bin/env python3
"""
reorganize.py — 把展厅归一成唯一目录规范，并把「作品」与「过程材料」分开

为什么需要：
  历史上作品落地有三种写法并存（根目录扁平 / 日期目录直放 / 日期+类型子目录），
  且交付过程产生的预览图、报告 md 混在作品目录里 —— 这正是
  「.part1.html 被当成作品」「文件乱放」「缩略图找不到」的土壤。
  本脚本把这些一次性收敛成规范结构，之后新增内容照规范放即可。

目标结构（唯一规范）：
  showcase/YYYY-MM-DD/research/YYYY-MM-DD-<slug>.html     研究类作品
  showcase/YYYY-MM-DD/creative/YYYY-MM-DD-<slug>.html     创意类作品
  showcase/YYYY-MM-DD/notes/                              该日过程材料
                                                          （预览图/佐证 md，不上展）
  showcase/thumbs/YYYY-MM-DD-{type}-YYYY-MM-DD-<slug>-thumb.webp
  showcase/_private/thumbs-src/                           高清 PNG 源图（不对外）
  showcase/_archive/                                      废弃脚本 / WIP 分片（不对外）
  showcase/tools/                                         流水线脚本（不对外）

安全性：
  - 只移动 .html 作品与非 .html 过程材料，不删除任何文件
  - 移动后同步改写 TAGMAP / enrich.json 的路径键，避免标签清零（历史 131→0 事故）
  - 支持 --dry-run 预览

用法：
  python3 tools/reorganize.py --dry-run
  python3 tools/reorganize.py && python3 tools/build_manifest.py && ./tools/autopublish.sh
"""

import json, os, re, shutil, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import build_manifest  # noqa: E402

MANIFEST = os.path.join(ROOT, 'manifest.json')
INDEX = os.path.join(ROOT, 'index.html')
ENRICH = os.path.join(ROOT, 'enrich.json')
TYPES_REGISTRY = os.path.join(TOOLS, 'autopublish_types.json')

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
LEAD_DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-')


def load_json(p, default):
    if not os.path.exists(p):
        return default
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def current_types():
    """file -> research/creative，优先 manifest，其次类型登记表。"""
    m = load_json(MANIFEST, {'research': [], 'creative': []})
    t = {i['file']: i['type'] for g in ('research', 'creative') for i in m.get(g, [])}
    reg = load_json(TYPES_REGISTRY, {})
    for stem, typ in (reg.items() if isinstance(reg, dict) else []):
        if typ in ('research', 'creative'):
            t.setdefault(stem, typ)
            t.setdefault(f'**/{stem}.html', typ)
    return t


def work_date(rel):
    parts = rel.split(os.sep)
    # works/YYYY-MM-DD/... 的日期在第 2 段；兼容旧的根级日期目录
    idx = 1 if parts and parts[0] == 'works' else 0
    if len(parts) > idx and DATE_RE.match(parts[idx]):
        return parts[idx]
    m = LEAD_DATE_RE.match(os.path.basename(rel))
    return m.group(1) if m else None


def slug_of(rel):
    """去掉目录、日期前缀与扩展名。"""
    b = os.path.basename(rel)[:-5]
    return LEAD_DATE_RE.sub('', b) or b


def canonical_path(date, typ, slug):
    # 日期目录统一在 works/ 下（2026-11-04 目录整理）
    return os.path.join('works', date, typ, f'{date}-{slug}.html')


def is_canonical(rel):
    # 结构：works/YYYY-MM-DD/{research|creative}/YYYY-MM-DD-slug.html（4 段）
    parts = rel.split(os.sep)
    if len(parts) != 4 or parts[0] != 'works':
        return False
    date, typ, fn = parts[1], parts[2], parts[3]
    if not DATE_RE.match(date) or typ not in ('research', 'creative'):
        return False
    return fn == f'{date}-{slug_of(fn)}.html'


def main():
    dry = '--dry-run' in sys.argv
    types = current_types()

    # 收集磁盘上全部作品 html（用生成器的同一套排除规则）
    works = build_manifest.scan_works()
    moves = []          # (old_rel, new_rel)
    for rel in works:
        date = work_date(rel)
        if not date:
            print(f'  ! 无法推断日期，跳过：{rel}')
            continue
        typ = types.get(rel) or types.get(os.path.basename(rel)[:-5]) \
            or build_manifest.detect_type(rel, None)
        if typ not in ('research', 'creative'):
            typ = 'research'
        new = canonical_path(date, typ, slug_of(rel))
        if new != rel:
            moves.append((rel, new))

    # 过程材料：日期目录内所有非 .html 文件 → notes/
    notes_moves = []
    for d in sorted(os.listdir(os.path.join(ROOT, 'works'))):
        if not DATE_RE.match(d):
            continue
        for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, 'works', d)):
            for fn in filenames:
                if fn.endswith('.html'):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
                tgt = os.path.join('works', d, 'notes', fn)
                if rel != tgt:
                    notes_moves.append((rel, tgt))

    print(f'作品规范化移动 : {len(moves)}')
    for o, n in moves[:8]:
        print(f'   {o}  →  {n}')
    if len(moves) > 8:
        print(f'   ... 另有 {len(moves)-8} 条')
    print(f'过程材料移入 notes/ : {len(notes_moves)}')
    for o, n in notes_moves[:6]:
        print(f'   {o}  →  {n}')
    if len(notes_moves) > 6:
        print(f'   ... 另有 {len(notes_moves)-6} 条')

    if dry:
        print('\n[dry-run] 未移动任何文件')
        return 0

    path_map = {}
    thumb_renames = []
    for o, n in moves:
        src, dst = os.path.join(ROOT, o), os.path.join(ROOT, n)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        path_map[o] = n
        # 文件名变了（补日期前缀）→ 缩略图必须同步改名，
        # 否则生成器按 {date}-{type}-{stem}-thumb 找不到图，卡片会退化成无图。
        old_stem = os.path.basename(o)[:-5]
        new_stem = os.path.basename(n)[:-5]
        if old_stem != new_stem:
            date = work_date(n)
            typ = n.split(os.sep)[2] if n.split(os.sep)[0] == 'works' else n.split(os.sep)[1]
            for ext in ('webp', 'png'):
                ot = os.path.join('thumbs', f'{date}-{typ}-{old_stem}-thumb.{ext}')
                if os.path.exists(os.path.join(ROOT, ot)):
                    nt = os.path.join('thumbs', f'{date}-{typ}-{new_stem}-thumb.{ext}')
                    shutil.move(os.path.join(ROOT, ot), os.path.join(ROOT, nt))
                    thumb_renames.append((ot, nt))
                    # 高清源图同名，一并改名以保持一致
                    src_png = os.path.join('_private', 'thumbs-src',
                                           f'{date}-{typ}-{old_stem}-thumb.png')
                    if os.path.exists(os.path.join(ROOT, src_png)):
                        shutil.move(os.path.join(ROOT, src_png),
                                    os.path.join(ROOT, src_png.replace(old_stem, new_stem)))
    for o, n in notes_moves:
        src, dst = os.path.join(ROOT, o), os.path.join(ROOT, n)
        if os.path.exists(dst):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)

    # 清掉搬空后的旧目录
    for o, _ in moves:
        d = os.path.dirname(os.path.join(ROOT, o))
        try:
            if not os.listdir(d):
                os.rmdir(d)
        except OSError:
            pass

    remap_json_keys(path_map)
    print(f'\n已移动 作品 {len(moves)} / 材料 {len(notes_moves)} / 缩略图改名 {len(thumb_renames)}；'
          f'路径键同步 {len(path_map)} 条')
    for ot, nt in thumb_renames:
        print(f'   thumb: {os.path.basename(ot)}  →  {os.path.basename(nt)}')
    print('下一步：python3 tools/build_manifest.py && ./tools/autopublish.sh')
    return 0


def remap_json_keys(path_map):
    """把 TAGMAP(index.html) 与 enrich.json 的键改成新路径，防标签清零。"""
    if not path_map:
        return
    # index.html 里的 TAGMAP
    html = open(INDEX, encoding='utf-8').read()
    m = re.search(r'^const TAGMAP=(\{.*\});$', html, re.M)
    if m:
        tagmap = json.loads(m.group(1))
        new_tm = {path_map.get(k, k): v for k, v in tagmap.items()}
        if new_tm != tagmap:
            html = html[:m.start(1)] + json.dumps(new_tm, ensure_ascii=False) + html[m.end(1):]
            open(INDEX, 'w', encoding='utf-8').write(html)
            print(f'   TAGMAP 键已重映射（{len(new_tm)} 条）')
    # enrich.json
    if os.path.exists(ENRICH):
        e = load_json(ENRICH, {})
        if isinstance(e, dict):
            changed = False
            for key in ('works',):
                for item in e.get(key, []):
                    if item.get('file') in path_map:
                        item['file'] = path_map[item['file']]
                        changed = True
            for k in list(e.keys()):
                if k in path_map:
                    e[path_map[k]] = e.pop(k)
                    changed = True
            if changed:
                with open(ENRICH, 'w', encoding='utf-8') as f:
                    json.dump(e, f, ensure_ascii=False, indent=2)
                print('   enrich.json 键已重映射')


if __name__ == '__main__':
    sys.exit(main())
