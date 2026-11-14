#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""独立复核 量研《429-口径核对》全部 blockquote：逐字回源简报全文检索定位。"""
import os, re, glob

BASE = "/app/working/shared/tasks"
DIRS = [os.path.join(BASE, "每日AI技术动态简报"),
        os.path.join(BASE, "每日热点新闻简报"),
        os.path.join(BASE, "每日股市简报")]
FILES = []
for d in DIRS:
    for f in sorted(glob.glob(os.path.join(d, "2026-11-*.md"))):
        FILES.append(f)

def lines_of(p):
    with open(p, encoding="utf-8") as f:
        return f.read().split("\n")

src = "/app/working/shared/showcase/works/2026-11-11/notes/429-口径核对-量研.md"
quotes = []
for i, ln in enumerate(lines_of(src), 1):
    s = ln.strip()
    if s.startswith("> "):
        q = s[2:].strip().replace("**", "")
        if q and not q.startswith("【") and len(q) > 6:
            quotes.append((i, q))

print(f"量研台账 blockquote 总数：{len(quotes)}\n")
notfound = []
for i, q in quotes:
    hits = []
    for f in FILES:
        for j, l in enumerate(lines_of(f), 1):
            s = l.strip()
            s = re.sub(r"^\d+[\.、]\s*", "", s).replace("**", "")
            if q in s:
                hits.append(f"{os.path.basename(os.path.dirname(f))}/{os.path.basename(f)}:L{j}")
                break
        if hits:
            break
    if hits:
        print(f"[OK ] 台账L{i:<4} → {hits[0]:<46} | {q[:60]}")
    else:
        notfound.append((i, q))
        print(f"[MISS] 台账L{i:<4} 全库未命中 | {q[:80]}")

print(f"\n小计：命中 {len(quotes)-len(notfound)} / 未命中 {len(notfound)}")
if notfound:
    print("未命中明细（可能是子句片段或需人工确认）：")
    for i, q in notfound:
        print(f"  台账L{i}: {q}")
