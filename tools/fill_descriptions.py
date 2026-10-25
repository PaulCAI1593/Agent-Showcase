#!/usr/bin/env python3
"""
fill_descriptions.py — 从作品正文提取 description，补进 enrich.json

为什么：
  首页卡片副标题来自 enrich.json 的 description。53/102 条为空，
  卡片只能显示"查看详情 →"占位，首页观感差一半。
  本脚本从作品自身正文提取，**只填空、不覆盖已有人工描述**。

提取优先级（越前越可信）：
  1. <meta name="description">
  2. 摘要类元素（class/id 含 summary/lede/abstract/摘要/执行摘要/核心结论）
  3. <h1> 之后第一段实质正文
  4. 全文第一段实质正文

用法：
  python3 tools/fill_descriptions.py --dry-run   # 只看提取结果，不写文件
  python3 tools/fill_descriptions.py             # 写入 enrich.json
  python3 tools/fill_descriptions.py --min 40    # 过滤过短的噪声（默认 24）
"""

import json, os, re, sys, html as htmlmod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, 'manifest.json')
ENRICH = os.path.join(ROOT, 'enrich.json')

SUMMARY_HINT = re.compile(
    r'(summary|lede|abstract|tldr|executive|核心|摘要|结论|概览|导读|要点)', re.I)

# 明显不是正文的噪声
NOISE = re.compile(r'(function|var |const |=>|\{\{|\}\}|px;|rgba?\(|#[0-9a-f]{3,6}\b)')


def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = htmlmod.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    # 修掉设计稿里字间距造成的 "市 场 风 格" 这类逐字空格
    s = re.sub(r'(?<=[\u4e00-\u9fff]) (?=[\u4e00-\u9fff])', '', s)
    return s


# 通用小节名：拿它们补描述只会产出"…｜执行摘要"这种噪声，必须跳过
GENERIC_HEADING = re.compile(
    r'^(执行摘要|摘要|核心发现|核心结论|概览|导读|要点|目录|背景|结论|总结|'
    r'overview|summary|introduction|conclusion|table of contents)\s*[:：]?\s*$'
    r'|^[一二三四五六七八九十]+[、\.]\s*(执行摘要|摘要|核心发现|概览|结论)\s*$', re.I)


def first_heading(txt):
    """取第一个**有信息量**的 h2/h3 小节标题，用于补强过短的副标题。"""
    for tag in ('h2', 'h3'):
        for hm in re.finditer(rf'<{tag}[^>]*>(.{{4,80}}?)</{tag}>', txt, re.S | re.I):
            h = clean(hm.group(1))
            if not h or NOISE.search(h):
                continue
            if re.fullmatch(r'[\d\.\-—、\s]+', h):
                continue
            if GENERIC_HEADING.search(h):
                continue          # 跳过"执行摘要"这类空泛小节名
            # 去掉 "一、" "1." "01 " 这类序号前缀，卡片上更干净
            h = re.sub(r'^(?:[一二三四五六七八九十]+|[0-9]{1,2})\s*[、\.．:：]\s*', '', h).strip()
            if len(h) < 4 or GENERIC_HEADING.search(h):
                continue
            return h
    return ''


def candidates(txt):
    """按可信度返回若干候选描述。"""
    out = []

    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', txt, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', txt, re.I)
    if m:
        out.append(('meta', clean(m.group(1))))

    # 摘要类容器
    for mm in re.finditer(
            r'<(section|div|p|article)[^>]*(?:class|id)=["\']([^"\']*)["\'][^>]*>(.{0,900}?)</\1>',
            txt, re.S | re.I):
        if SUMMARY_HINT.search(mm.group(2)):
            body = clean(mm.group(3))
            if len(body) > 12:
                out.append((f'summary:{mm.group(2)[:24]}', body))

    # h1 之后的段落
    i = txt.lower().find('<h1')
    seg = txt[i:i + 30000] if i >= 0 else txt
    for pm in re.finditer(r'<p[^>]*>(.{6,600}?)</p>', seg, re.S | re.I):
        out.append(('after-h1', clean(pm.group(1))))
        break

    for pm in re.finditer(r'<p[^>]*>(.{6,600}?)</p>', txt, re.S | re.I):
        out.append(('any-p', clean(pm.group(1))))
        break

    # 最后兜底：纯仪表盘/信息图几乎没有正文段落，用 h1 + 小节标题组合，
    # 至少卡片上是一句能读懂的话，而不是"查看详情 →"占位。
    hm = re.search(r'<h1[^>]*>(.{2,80}?)</h1>', txt, re.S | re.I)
    if hm:
        h1 = clean(hm.group(1))
        sub = first_heading(txt)
        out.append(('h1+heading', f'{h1}｜{sub}' if sub and sub != h1 else h1))

    return out


def pick(cands, min_len, heading=''):
    for src, body in cands:
        if not body or len(body) < min_len:
            continue
        if NOISE.search(body):
            continue
        if body.startswith(('<', '{', '@', '/*')):
            continue
        # 副标题过短时，用第一个小节标题补强，避免卡片只有一句空泛的话
        if heading and len(body) < 40 and heading not in body:
            body = f'{body}｜{heading}'
        b = body if len(body) <= 110 else body[:108].rstrip('，。、；：,. ;') + '…'
        return b, src
    return None, None


def repair_tails(e, dry):
    """
    清洗早期版本产出的"…｜执行摘要"这类噪声尾巴：
    去掉尾部的空泛小节名；若去掉后仍短，则用新的 first_heading 重新补强。
    """
    fixed = []
    for w in e.get('works', []):
        d = (w.get('description') or '').strip()
        if '｜' not in d:
            continue
        head, _, tail = d.rpartition('｜')
        if not head or GENERIC_HEADING.search(tail.strip()):
            new = head.strip().rstrip('：: —-')
            p = os.path.join(ROOT, w['file'])
            if len(new) < 40 and os.path.exists(p):
                txt = open(p, encoding='utf-8', errors='ignore').read()
                h = first_heading(txt)
                if h and h not in new:
                    new = f'{new}｜{h}'
            w['description'] = new
            fixed.append((w['file'], d, new))
    print(f'尾部噪声修复: {len(fixed)} 条')
    for f, a, b in fixed:
        print(f'   {os.path.basename(f)[:40]:42}')
        print(f'      旧: {a[:70]}')
        print(f'      新: {b[:70]}')
    if fixed and not dry:
        with open(ENRICH, 'w', encoding='utf-8') as fh:
            json.dump(e, fh, ensure_ascii=False, indent=2)
        print('已写回 enrich.json')
    elif fixed:
        print('[dry-run] 未写回')
    return len(fixed)


def main():
    dry = '--dry-run' in sys.argv
    if '--repair-tails' in sys.argv:
        e = json.load(open(ENRICH, encoding='utf-8')) if os.path.exists(ENRICH) else {'works': []}
        repair_tails(e, dry)
        return 0
    min_len = int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 8

    m = json.load(open(MANIFEST, encoding='utf-8'))
    items = m['research'] + m['creative']
    e = json.load(open(ENRICH, encoding='utf-8')) if os.path.exists(ENRICH) else {'works': []}
    by_file = {w['file']: w for w in e.get('works', [])}

    todo = [i for i in items if not (i.get('description') or '').strip()]
    print(f'缺描述: {len(todo)} 条\n')

    filled = 0
    failed = []
    for it in todo:
        p = os.path.join(ROOT, it['file'])
        if not os.path.exists(p):
            failed.append((it['file'], '文件不存在')); continue
        txt = open(p, encoding='utf-8', errors='ignore').read()
        desc, src = pick(candidates(txt), min_len, first_heading(txt))
        if not desc:
            failed.append((it['file'], '无可信正文段落')); continue

        w = by_file.setdefault(it['file'], {'file': it['file']})
        w['description'] = desc
        w.setdefault('highlights', it.get('highlights') or [])
        w.setdefault('agent', it.get('agent') or '')
        by_file[it['file']] = w
        filled += 1
        print(f'  [{src:22}] {os.path.basename(it["file"])[:40]:42} {desc[:64]}')

    print(f'\n可填 {filled} 条；提取失败 {len(failed)} 条')
    for f, why in failed:
        print(f'   ! {os.path.basename(f)[:50]:52} {why}')

    if dry:
        print('\n[dry-run] 未写入 enrich.json')
        return 0

    e['works'] = sorted(by_file.values(), key=lambda w: w['file'])
    with open(ENRICH, 'w', encoding='utf-8') as f:
        json.dump(e, f, ensure_ascii=False, indent=2)
    print(f'\n已写入 {ENRICH}（共 {len(e["works"])} 条）')
    print('下一步：python3 tools/build_manifest.py && ./tools/autopublish.sh')
    return 0


if __name__ == '__main__':
    sys.exit(main())
