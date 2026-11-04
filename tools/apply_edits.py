#!/usr/bin/env python3
"""apply_edits.py — 对 HTML 做精确的文本替换（带出现次数断言）。

用法：python3 tools/apply_edits.py <file> <json-edits-file>
edits 格式：[{"old": "...", "new": "...", "count": 1}, ...]
"""
import json
import sys


def main():
    path, edits_path = sys.argv[1], sys.argv[2]
    edits = json.load(open(edits_path, encoding='utf-8'))
    s = open(path, encoding='utf-8').read()
    for i, e in enumerate(edits):
        old, new, cnt = e['old'], e['new'], e.get('count', 1)
        found = s.count(old)
        if found != cnt:
            print(f'✗ 第{i+1}处未命中：期望 {cnt} 处，实际 {found} 处\n  old={old[:90]!r}')
            sys.exit(1)
        s = s.replace(old, new)
        print(f'✓ 第{i+1}处：{found} 处已替换  «{old[:60]}»')
    open(path, 'w', encoding='utf-8').write(s)
    print('已写入', path)


if __name__ == '__main__':
    main()
