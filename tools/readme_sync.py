#!/usr/bin/env python3
"""
readme_sync.py — README「现在时」计数的唯一写入器

为什么需要（2026-11-16 实测事故）：
  README 的作品数 / 断言数 / 日期目录数过去只靠人手改，没有自动写入器。
  每周日 02:00 的周度 cron 提交后，README 写「70 个日期目录」，
  而该提交的 works/ 实际只有 69 个目录（提交前归档了空目录）——
  差 1 → CI「① 结构一致性」失败（run 43916920136，verify-archive 红）。

原则：
  - 只改数字，不改叙述：历史叙述（「过去 104 件」等）不在替换范围。
  - 每个模式只替换**第一处**，与 build_manifest.guardrails 的校验口径一致
    （那里用 re.search，只看第一处）。两处口径必须一致，否则校验失配。
  - 内容未变则不写盘：重复执行不产生副作用，也不改 mtime。
"""

import os
import re

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
README_PATH = os.path.join(ROOT, 'README.md')


def date_dirs_with_works():
    """日期目录真值：只数「真的有作品」的目录。

    判据 = `works/<date>/{research,creative}/` 下至少有一个 .html。

    为什么不能直接数 os.listdir：git **不跟踪空目录**。派单时预建的空脚手架
    （如 `works/2026-11-14/{creative,notes}`）在本地存在，在 CI checkout 后消失，
    于是本地按磁盘写进 README 的计数比 CI 的校验真值多 1 —— 2026-11-22 CI
    run 44935646865 就是这么红的（README 76 vs CI 75）。
    口径必须与 build_manifest.guardrails() 完全一致，两边都调本函数。
    """
    works_root = os.path.join(ROOT, 'works')
    if not os.path.isdir(works_root):
        return []
    out = []
    for d in sorted(os.listdir(works_root)):
        full = os.path.join(works_root, d)
        if not os.path.isdir(full):
            continue
        if any(os.path.isfile(os.path.join(full, sub, fn)) and fn.endswith('.html')
               for sub in ('research', 'creative')
               for fn in (os.listdir(os.path.join(full, sub))
                          if os.path.isdir(os.path.join(full, sub)) else [])):
            out.append(d)
    return out


def sync_readme_counts(manifest):
    """按 manifest + 磁盘真值改写 README 计数。返回改写说明列表。"""
    if not os.path.exists(README_PATH):
        return ['README.md 不存在，跳过']
    try:
        with open(README_PATH, encoding='utf-8') as f:
            text = f.read()
    except OSError as exc:
        return [f'README.md 读取失败：{exc}']

    works_dirs = date_dirs_with_works()

    research = manifest.get('research') or []
    creative = manifest.get('creative') or []
    vals = {
        'total': int(manifest.get('total') or 0),
        'research': len(research),
        'creative': len(creative),
        'claims': sum(len(i.get('claims') or []) for i in research + creative),
        'beats': len((manifest.get('stats') or {}).get('beats') or []),
        'months': len({d[:7] for d in works_dirs}),
        'dirs': len(works_dirs),
        'tags': len({t for i in research + creative for t in (i.get('highlights') or [])}),
    }

    rules = [
        (r'(\d+)(\s*Chinese-language works across\s*)(\d+)(\s*months)',
         lambda m, v: f"{v['total']}{m.group(2)}{v['months']}{m.group(4)}", '英文副标题'),
        (r'(\d+)(\s*件作品按月份归档)',
         lambda m, v: f"{v['total']}{m.group(2)}", '首段件数'),
        (r'(\d+)(\s*件（研究类\s*)(\d+)(\s*·\s*创意类\s*)(\d+)(）)',
         lambda m, v: (f"{v['total']}{m.group(2)}{v['research']}"
                       f"{m.group(4)}{v['creative']}{m.group(6)}"), '作品表行'),
        (r'(已验证断言\*\*\s*\|\s*)(\d+)(\s*条)',
         lambda m, v: f"{m.group(1)}{v['claims']}{m.group(3)}", '断言表行'),
        (r'(\d+)(\s*条主题线)',
         lambda m, v: f"{v['beats']}{m.group(2)}", '追踪线表行'),
        (r'(\d+)(\s*个日期目录)',
         lambda m, v: f"{v['dirs']}{m.group(2)}", '目录树件数'),
        (r'(\|\s*\*\*标签\*\*\s*\|\s*)(\d+)(\s*个)',
         lambda m, v: f"{m.group(1)}{v['tags']}{m.group(3)}", '标签表行'),
    ]

    out = text
    notes = []
    for pat, fn, name in rules:
        m = re.search(pat, out)
        if not m:
            notes.append(f'未命中「{name}」，跳过')
            continue
        new = fn(m, vals)
        if new != m.group(0):
            out = out[:m.start()] + new + out[m.end():]
            notes.append(f'{name} 已改写')
    if out != text:
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(out)
        notes.append('README.md 已写入')
    return notes
