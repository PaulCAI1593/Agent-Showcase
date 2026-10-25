#!/usr/bin/env python3
"""Wait until the showcase output tree is quiescent, then report."""
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUIET = int(sys.argv[1]) if len(sys.argv) > 1 else 180
TIMEOUT = int(sys.argv[2]) if len(sys.argv) > 2 else 1800

SKIP = {os.path.abspath(os.path.join(ROOT, 'thumbs')),
        os.path.abspath(os.path.join(ROOT, '_archive')),
        os.path.abspath(os.path.join(ROOT, 'tools'))}
MANAGED = {'manifest.json', 'enrich.json', 'index.html'}


def newest():
    best = (0.0, '')
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        if os.path.abspath(dirpath) in SKIP:
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn in MANAGED:
                continue
            p = os.path.join(dirpath, fn)
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            if m > best[0]:
                best = (m, os.path.relpath(p, ROOT))
    return best


start = time.time()
last = None
while time.time() - start < TIMEOUT:
    ts, rel = newest()
    age = time.time() - ts
    if last != rel:
        print(f'[{time.strftime("%H:%M:%S")}] newest: {rel}  ({age:.0f}s ago)', flush=True)
        last = rel
    if age >= QUIET:
        print(f'QUIESCENT: {rel} 已静默 {age:.0f}s (阈值 {QUIET}s)', flush=True)
        sys.exit(0)
    time.sleep(15)
print(f'TIMEOUT: 等待 {TIMEOUT}s 内未达到静默阈值 {QUIET}s', flush=True)
sys.exit(1)
