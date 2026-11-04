#!/usr/bin/env python3
"""汇总 impeccable detect 的 low-contrast（按前景/背景色对分组）"""
import collections
import json
import subprocess
import sys

LAUNCH = '/app/working/workspaces/default/skills/impeccable/scripts/impeccable'
ROOT = '/app/working/shared/showcase'


def main():
    files = sys.argv[1:]
    p = subprocess.run([LAUNCH, 'detect'] + files + ['--json'], cwd=ROOT,
                       capture_output=True, text=True, timeout=3600)
    data = json.loads(p.stdout)
    if isinstance(data, dict):
        data = data.get('findings', [])
    by_file = collections.defaultdict(collections.Counter)
    total = 0
    for f in data:
        if f.get('antipattern') != 'low-contrast':
            continue
        total += 1
        by_file[f.get('file', '').split('/')[-1]][f.get('snippet', '')] += 1
    print(f'low-contrast 总计 {total} 条')
    for fn in sorted(by_file, key=lambda k: -sum(by_file[k].values())):
        print(f'\n=== {fn}  ({sum(by_file[fn].values())} 条)')
        for snip, n in by_file[fn].most_common(60):
            print(f'   {n:>3} × {snip}')
    # 全部规则计数
    rules = collections.Counter(f.get('antipattern', '?') for f in data)
    print('\n全部规则计数:')
    for r, n in rules.most_common():
        print(f'   {n:>5d}  {r}')


if __name__ == '__main__':
    main()
