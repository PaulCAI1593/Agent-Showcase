#!/usr/bin/env python3
"""
design_scan.py — 全馆设计质量棘轮（impeccable detect 的积压治理）

为什么需要它
------------
规则14 要求「设计类工作交付前必须跑 detect + polish」，但**没有任何机器闸门
强制它** —— 全靠 Agent 自报。结果：115 件作品里 111 件有 findings，
累计 4907 条（平均每件 44 条），其中 757 条对比度低于 3:1（连大字号都不达标）。

一次性清完 4907 条不现实（每件都是独立的视觉世界，机器批量改色会毁掉作者的世界）。
所以本工具走**棘轮**路线 —— 与仓库既有的「标签总数不得下降」同一思路：

  基线 = 当前 findings 分布
  之后任何一次全量扫描，若某条规则的条数**上升** → 退出码 1（回归）
  条数下降 → 通过（并在 --update-baseline 时刷新基线）

这样：
- 新作品交付若引入新的 AI slop → 立刻被拦
- 存量作品可以按批次慢慢 polish，每批都让棘轮更紧
- 不需要有人记得「记得去 polish」

用法：
  python3 tools/design_scan.py --scope all               # 全量扫描 + 棘轮比对
  python3 tools/design_scan.py --scope all --update-baseline   # 刷新基线（有意改善后）
  python3 tools/design_scan.py --scope recent:30         # 只扫近 30 天改动的作品（报告，不比棘轮）
  python3 tools/design_scan.py --scope file:<路径>        # 单件（交付前自检用）
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BASELINE = os.path.join(ROOT, 'tools', 'design_baseline.json')
SNAPSHOT = os.path.join(ROOT, 'tools', 'design_snapshot.json')

LAUNCHER_CANDIDATES = [
    os.environ.get('IMPECCABLE_BIN', ''),
    '/app/working/workspaces/default/skills/impeccable/scripts/impeccable',
    os.path.join(ROOT, '.agents/skills/impeccable/scripts/impeccable'),
    os.path.expanduser('~/.agents/skills/impeccable/scripts/impeccable'),
]


def find_launcher():
    for c in LAUNCHER_CANDIDATES:
        if c and os.path.exists(c) and os.access(c, os.X_OK):
            return c
    return None


def works():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if not d.startswith('.') and d not in ('tools', 'templates', '_archive',
                                                            '_private', 'thumbs', 'assets', 'notes')]
        for fn in filenames:
            if not fn.endswith('.html') or fn.startswith('.'):
                continue
            if '.bak' in fn:
                continue
            full = os.path.join(dirpath, fn)
            out.append(os.path.relpath(full, ROOT))
    return sorted(out)


def pick(scope, days=30):
    if scope.startswith('file:'):
        return [scope[5:]]
    if scope == 'all':
        return works()
    if scope.startswith('recent:'):
        n = int(scope.split(':', 1)[1])
        cutoff = time.time() - n * 86400
        return [f for f in works() if os.path.getmtime(os.path.join(ROOT, f)) >= cutoff]
    return works()


def run_detect(files):
    launcher = find_launcher()
    if not launcher:
        return None, '找不到 impeccable 启动脚本（设 IMPECCABLE_BIN 或装技能）'
    if not files:
        return [], ''
    cmd = [launcher, 'detect'] + files + ['--json']
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=3600)
    except subprocess.TimeoutExpired:
        return None, 'detect 超时'
    raw = p.stdout.strip()
    if not raw:
        return None, f'detect 无输出（stderr: {p.stderr.strip()[:200]}）'
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return None, f'detect 输出解析失败: {e}'
    if isinstance(data, dict):
        data = data.get('findings', [])
    return data, ''


def summarize(findings):
    by_rule = collections.Counter(f.get('antipattern', '?') for f in findings)
    by_sev = collections.Counter(f.get('severity', '?') for f in findings)
    by_file = collections.Counter(os.path.basename(f.get('file', '')) for f in findings)
    # 对比度按严重度分档：<3:1 连大字号都不达标
    contrast_bands = collections.Counter()
    for f in findings:
        if f.get('antipattern') != 'low-contrast':
            continue
        m = re.match(r'([\d.]+):1', f.get('snippet', ''))
        if not m:
            continue
        r = float(m.group(1))
        contrast_bands['<2:1 几乎不可读' if r < 2 else
                       ('2-3:1 大字号不达标' if r < 3 else '3-4.5:1 正文不达标')] += 1
    return {'by_rule': dict(by_rule), 'by_severity': dict(by_sev),
            'by_file': dict(by_file), 'contrast_bands': dict(contrast_bands),
            'total': len(findings),
            'files_with_findings': len(by_file)}


def load(path):
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scope', default='all')
    ap.add_argument('--update-baseline', action='store_true')
    ap.add_argument('--top', type=int, default=10)
    args = ap.parse_args()

    files = pick(args.scope)
    findings, err = run_detect(files)
    if findings is None:
        print(f'✗ {err}')
        return 2
    summary = summarize(findings)
    print(f'扫描 {len(files)} 件作品 · findings {summary["total"]} 条 · '
          f'涉及 {summary["files_with_findings"]} 件')
    print(f'严重度分布: {summary["by_severity"]}')
    if summary['contrast_bands']:
        print(f'对比度分档: {summary["contrast_bands"]}')
    top = collections.Counter(summary['by_rule']).most_common(args.top)
    print('规则 Top:')
    for rule, n in top:
        print(f'   {n:5d}  {rule}')

    with open(SNAPSHOT, 'w', encoding='utf-8') as f:
        json.dump({'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'scope': args.scope,
                   'scanned': len(files), **summary}, f, ensure_ascii=False, indent=1)

    if args.scope != 'all':
        print('\n（非全量扫描：只报告，不比棘轮）')
        return 0

    base = load(BASELINE)
    if args.update_baseline or base is None:
        with open(BASELINE, 'w', encoding='utf-8') as f:
            json.dump({'ts': time.strftime('%Y-%m-%d %H:%M:%S'), **summary},
                      f, ensure_ascii=False, indent=1)
        print(f'\n✓ 基线已写入 {os.path.relpath(BASELINE, ROOT)}'
              f'（总 {summary["total"]} 条 / {summary["files_with_findings"]} 件）')
        return 0

    regressions = []
    for rule, n in summary['by_rule'].items():
        was = base.get('by_rule', {}).get(rule, 0)
        if n > was:
            regressions.append((rule, was, n))
    if regressions:
        print('\n✗ 棘轮被打破（下列规则条数上升）：')
        for rule, was, now in regressions:
            print(f'   {rule}: {was} → {now} (+{now - was})')
        print('   → 新作品引入了新的设计问题，或存量被改坏。先修，再 --update-baseline。')
        return 1
    print(f'\n✓ 棘轮通过：无一规则上升'
          f'（基线 {base.get("total")} → 当前 {summary["total"]}）')
    if summary['total'] < base.get('total', 0):
        print('   有改善 → 可跑 --update-baseline 收紧棘轮')
    return 0


if __name__ == '__main__':
    sys.exit(main())
