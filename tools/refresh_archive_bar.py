#!/usr/bin/env python3
"""档案条同步器 —— 只修「档案条」里的陈旧数字与色值，不动作品正文

为什么需要它
------------
档案条（#showcase-bar）是 tools/add_backlink.py 在**首次注入**时写进作品页的，
里面有四个会随全馆变化而漂移的量：

  1. 「N 件 / YYYY-MM」   —— 该月作品件数
  2. 「N 条已验证断言」   —— 本件作品的断言条数
  3. 「2026-10-22」      —— 本件日期
  4. `.sb-cnt` 色值      —— 档案条计数器前景色

add_backlink.py 的契约是「已有 marker 就跳过」，所以这四个量**注入后再也不刷新**。
实测后果（2026-11-03）：
  · 92 件作品的档案条仍写「24 条已验证断言」，而 manifest 里只剩 23 条
    （那 1 条是被 G4 规则清掉的「页面自身计数」伪断言）—— 页面在说假话。
  · 29 件作品的「N 件 / YYYY-MM」与实际月度件数不符。
  · `.sb-cnt` 前景色 rgba(255,255,255,.44) 在 #0b0c12 底上只有 4.36:1，
    低于团队 DESIGN.md 的 WCAG AA 4.5:1 底线（impeccable detect 对全馆报同源 advisory）。

为什么不是「去掉再重注」
----------------------
add_backlink.py --remove 会把注入物连同 rescue CSS 一起剥掉再重注，
diff 覆盖 <body> 起始处的结构，115 件全量重写风险偏高。
本工具只做**定向字符串替换**：档案条里那三段文本 + 那一条色值。
稳态下（数字没变）一个字节都不写 —— 这就是它可以挂在 autopublish 流水线里的原因。

为什么自己扫盘、不读 manifest
-----------------------------
断言条数取**作品自身的声明块**（权威来源，与原文同文件，不可能漂移），
件/月件数从**磁盘实际作品列表**算 —— 两者都不依赖 manifest.json 的重建时机，
因此挂在流水线的任意阶段都成立（manifest 在阶段 6 才重建，
若从 manifest 读条数，阶段 5.5 同步到的还是上一轮的旧数）。

用法
----
  python3 tools/refresh_archive_bar.py --dry-run    # 只报差异，不写
  python3 tools/refresh_archive_bar.py             # 写盘（备份到 _archive/backups/）

退出码：0 = 正常（含「无差异」）；2 = 参数或环境错误。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_ROOT = os.path.join(ROOT, '_archive', 'backups')

# 档案条三段文本 + 计数器色值。全部带上下文锚点，避免误伤正文。
RE_CNT_MONTH = re.compile(r'(<span class="sb-cnt">)(\d+)( 件 / )(\d{4}-\d{2})(</span>)')
RE_CNT_CLAIM = re.compile(r'(<span class="sb-cnt sb-claims">)(\d+)( 条已验证断言</span>)')
RE_DATE = re.compile(r'(<span class="sb-date">)(\d{4}-\d{2})(</span>)')
RE_COLOR = re.compile(r'(#showcase-bar \.sb-cnt\{color:rgba\(255,255,255,)(\.\d+)(\)\})')

# 4.5:1 底线：.44 = 4.36:1 不达标；.48 = 5.01:1 达标。
TARGET_ALPHA = '.48'

# 与 build_manifest 一致的作品扫描口径（排除工具/归档/缩略图/过程材料）。
EXCLUDE_DIRS = {'_archive', 'thumbs', '.git', '__pycache__', 'notes', 'templates', 'tools', 'assets'}
RE_CLAIMS_BLOCK = re.compile(
    r'<script[^>]*id=["\']claims["\'][^>]*>(.*?)</script>', re.S)


def scan_works():
    """扫盘列出作品页相对路径（与 build_manifest.scan_works 同口径）。"""
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for fn in filenames:
            if not fn.endswith('.html') or fn.startswith('.'):
                continue
            if fn == 'index.html':
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
            if rel.endswith('.html.bak') or '.bak.' in rel:
                continue
            out.append(rel)
    return sorted(out)


def declared_claim_count(html: str) -> int | None:
    """作品自身声明的断言条数。取不到返回 None（调用方回落 enrich.json）。"""
    m = RE_CLAIMS_BLOCK.search(html)
    if not m:
        return None
    try:
        arr = json.loads(m.group(1))
    except Exception:
        return None
    return len(arr) if isinstance(arr, list) else None


def enrich_claim_counts():
    """enrich.json 里的断言条数（作品没有自带声明块时的回落来源）。"""
    p = os.path.join(ROOT, 'enrich.json')
    if not os.path.exists(p):
        return {}
    try:
        with open(p, encoding='utf-8') as f:
            e = json.load(f)
    except Exception:
        return {}
    out = {}
    for it in (e.get('works') or []):
        rel = it.get('file')
        if rel:
            out[rel] = len(it.get('claims') or [])
    return out


def collect():
    """返回 {相对路径: {date, month, month_count, claim_count}}。"""
    rels = scan_works()
    dates = {}
    for rel in rels:
        parts = rel.split(os.sep)
        d = parts[0] if re.match(r'^\d{4}-\d{2}-\d{2}$', parts[0]) else ''
        if not d:
            m = re.match(r'^(\d{4}-\d{2}-\d{2})', os.path.basename(rel))
            d = m.group(1) if m else ''
        dates[rel] = d
    months = {}
    for d in dates.values():
        if d:
            k = d[:7]
            months[k] = months.get(k, 0) + 1

    enrich = enrich_claim_counts()
    out = {}
    for rel in rels:
        d = dates[rel]
        path = os.path.join(ROOT, rel)
        try:
            html = open(path, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        n = declared_claim_count(html)
        if n is None:
            n = enrich.get(rel, 0)
        out[rel] = {
            'date': d,
            'month': d[:7],
            'month_count': months.get(d[:7], 0),
            'claim_count': n,
        }
    return out


def refresh_html(html: str, meta: dict) -> tuple[str, list[str]]:
    """返回 (新内容, 变更说明)。无变更时新内容 == 原内容。"""
    changes = []

    def fix_month(m):
        if int(m.group(2)) != meta['month_count'] or m.group(4) != meta['month']:
            changes.append('件/月 %s %s → %s %s'
                           % (m.group(2), m.group(4), meta['month_count'], meta['month']))
            return m.group(1) + str(meta['month_count']) + m.group(3) + meta['month'] + m.group(5)
        return m.group(0)

    def fix_claim(m):
        if int(m.group(2)) != meta['claim_count']:
            changes.append('断言数 %s → %s' % (m.group(2), meta['claim_count']))
            return m.group(1) + str(meta['claim_count']) + m.group(3)
        return m.group(0)

    def fix_date(m):
        if m.group(2) != meta['date']:
            changes.append('日期 %s → %s' % (m.group(2), meta['date']))
            return m.group(1) + meta['date'] + m.group(3)
        return m.group(0)

    def fix_color(m):
        cur = m.group(2)
        # 只在低于底线时上调；已经达标（如 .52）不改，避免无意义 diff。
        if float(cur) < float(TARGET_ALPHA):
            changes.append('计数器色值 %s → %s' % (cur, TARGET_ALPHA))
            return m.group(1) + TARGET_ALPHA + m.group(3)
        return m.group(0)

    new = RE_CNT_MONTH.sub(fix_month, html)
    new = RE_CNT_CLAIM.sub(fix_claim, new)
    new = RE_DATE.sub(fix_date, new)
    new = RE_COLOR.sub(fix_color, new)
    return new, changes


def main() -> int:
    ap = argparse.ArgumentParser(description='同步作品页档案条里的陈旧数字与色值')
    ap.add_argument('--dry-run', action='store_true', help='只报差异，不写盘')
    args = ap.parse_args()

    metas = collect()
    if not metas:
        print('扫不到作品页（ROOT=%s）' % ROOT, file=sys.stderr)
        return 2

    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    changed = skipped = missing = 0
    for rel, meta in sorted(metas.items()):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            missing += 1
            continue
        html = open(p, encoding='utf-8', errors='ignore').read()
        new, changes = refresh_html(html, meta)
        if not changes:
            skipped += 1
            continue
        changed += 1
        print('  %s | %s' % (rel, '；'.join(changes)))
        if args.dry_run:
            continue
        bak_dir = os.path.join(BACKUP_ROOT, 'archive-bar-' + stamp)
        os.makedirs(bak_dir, exist_ok=True)
        dst = os.path.join(bak_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(p, dst)
        open(p, 'w', encoding='utf-8').write(new)

    verb = '将改' if args.dry_run else '已改'
    print('%s %d 件；无差异 %d 件；文件缺失 %d 件' % (verb, changed, skipped, missing))
    if not args.dry_run and changed:
        print('备份目录：%s' % os.path.join(BACKUP_ROOT, 'archive-bar-' + stamp))
    return 0


if __name__ == '__main__':
    sys.exit(main())
