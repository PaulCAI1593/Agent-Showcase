#!/usr/bin/env python3
"""
fix_heading_levels.py — 修标题层级跳跃（skipped-heading）｜⚠️ 默认不启用

⚠️ 状态：**已实测出视觉回归，暂不启用**（2026-11-04）
   试验：把 <h4> 改成 <h3> 并用计算样式回填外观，理论上保视觉；
   实测 3 件里 2 件样式仍不等（h4 21px → h3 28px 等），
   且引入真实回归：low-contrast +17、flat-type-hierarchy +2。
   根因：同特异性规则（.content h3 与 h3[data-hfix] 同为 0,1,1）靠文档顺序决胜，
   回填样式在部分结构里压不住；且改标题层级会改变类型台阶本身。
   处置：整体回退。skipped-heading（117 条）是可访问性提示，
   代价（视觉回归）大于收益 —— 留待逐件人工处理。
   保留本脚本作为取证与修法参考，默认不运行。

问题
----
检测器报的 skipped-heading 形态高度统一：`<h2>` 后面直接跟 `<h4>`（缺 h3）。
这既是可访问性问题（屏幕阅读器按标题层级导航），也是 craft-floor 说的
「标题层级要有明显台阶」。

难点
----
直接把 `<h4>` 改成 `<h3>`，**视觉会变** —— 作品的 CSS 多按标签写样式
（`h3{font-size:20px;color:...}` / `.card h4{font-size:13px}`），
换标签后原来那套样式不再命中，标题会突然变大、变色、换间距。

做法（保视觉）
--------------
1. 页内取证：按文档顺序走标题，记录每级的层级；发现跳跃就记下
   「这个元素要从 h4 变成 h3」，并**抓取它当前的计算样式**
   （font-size / color / font-weight / letter-spacing / margin / line-height）
2. 改源码：换标签 + 加 `data-hfix` 标记
3. 追加 CSS：`h3[data-hfix]{<抓到的样式>}` —— 外观与原来逐项一致
4. 检测器复验 + audit_pages 真跑

终局判据：检测器（与棘轮同源）。
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PROPS = ['font-size', 'color', 'font-weight', 'font-family', 'letter-spacing',
         'margin-top', 'margin-bottom', 'line-height', 'text-transform']

HEADINGS_JS = r"""
() => {
  const out = [];
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')];
  let prev = 0;
  for (const h of hs) {
    const lvl = +h.tagName[1];
    if (prev && lvl > prev + 1) {
      const cs = getComputedStyle(h);
      const style = {};
      for (const p of ['font-size','color','font-weight','letter-spacing',
                        'margin-top','margin-bottom','line-height','text-transform'])
        style[p] = cs.getPropertyValue(p);
      const idx = [...h.parentElement.children].indexOf(h);
      out.push({tag: h.tagName, to: 'H' + (prev + 1), style,
                text: (h.innerText || '').trim().slice(0, 40),
                parent: h.parentElement.tagName.toLowerCase(),
                index: idx, total: h.parentElement.children.length});
    }
    prev = lvl;
  }
  return out;
}
"""


def detect_many(files, timeout=2400):
    launcher = (os.environ.get('IMPECCABLE_BIN', '')
                or '/app/working/workspaces/default/skills/impeccable/scripts/impeccable')
    if not os.path.exists(launcher) or not files:
        return {}
    try:
        p = subprocess.run([launcher, 'detect'] + list(files) + ['--json'],
                           cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {}
    raw = p.stdout.strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if isinstance(data, dict):
        data = data.get('findings', [])
    out = {}
    for f in data:
        rel = f.get('file', '')
        if rel.startswith('file://'):
            rel = rel[len('file://'):]
        rel = rel.replace(ROOT + '/', '').replace(ROOT, '')
        out.setdefault(rel, []).append(f)
    return out


def skipped_count(findings):
    return len([f for f in findings or [] if f.get('antipattern') == 'skipped-heading'])


def inspect(paths):
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path='/usr/bin/chromium',
                               args=['--no-sandbox', '--allow-file-access-from-files'])
        for rel in paths:
            full = os.path.join(ROOT, rel)
            if not os.path.exists(full):
                continue
            pg = br.new_page(viewport={'width': 1260, 'height': 800})
            try:
                pg.goto('file://' + full, wait_until='load')
                pg.wait_for_timeout(500)
                out[rel] = pg.evaluate(HEADINGS_JS)
            except Exception as exc:                       # noqa: BLE001
                out[rel] = []
                print(f'  ! {os.path.basename(rel)} 取证失败: {str(exc)[:70]}')
            finally:
                pg.close()
        br.close()
    return out


def apply_fix(html, items):
    """把指定层级的标题换标签 + 加 data-hfix，并追加保视觉 CSS。"""
    # 按「父容器内的序号」定位（DOM 取证给的 index）
    rules = []
    changed = [0]
    for it in items:
        # ⚠️ 必须加 !important：原文件里 `.content h3{...}` 这类规则与
        #    `h3[data-hfix]` 特异性相同(0,1,1)，谁在文档里靠后谁赢 ——
        #    实测不加 !important 时 h4(21px) 变成 h3(28px)，视觉被改掉了。
        # ⚠️ 每条声明后必须有分号：`font-size:21px !important color:red !important`
        #    会被解析成一条无效声明 → 整条规则被丢弃 → 样式完全没生效（实测踩过）。
        style = ''.join(f'{k}:{v} !important; ' for k, v in it['style'].items() if v)
        if style:
            rules.append(f'h3[data-hfix]{{{style}}}')
            break
    out = html
    for it in items:
        # 定位第 index 个子元素里标签为 <tag> 的那个
        pat = re.compile(r'<' + it['tag'].lower() + r'(\b[^>]*)>(.*?)</' + it['tag'].lower() + r'>',
                         re.S)
        count = {'n': 0}
        # 逐个匹配，按出现顺序与 DOM 序号对齐（同级同标签时可能偏移 → 用文本辅助）
        target_text = it['text'][:24]

        def repl(m):
            count['n'] += 1
            inner = m.group(2)
            # 只改与取证文本相符的那个
            if target_text and target_text not in re.sub(r'<[^>]+>', '', inner):
                return m.group(0)
            attrs = m.group(1)
            if 'data-hfix' in attrs:
                return m.group(0)
            changed[0] += 1
            return f'<{it["to"].lower()}{attrs} data-hfix="1">{inner}</{it["to"].lower()}>'
        out = pat.sub(repl, out)
    if rules and changed[0]:
        css = ('\n/* 标题层级修复（保视觉：由原计算样式回填） */\n'
               + '\n'.join(rules) + '\n')
        if '</style>' in out:
            i = out.rfind('</style>')
            out = out[:i] + css + out[i:]
        else:
            out += css
    return out, changed[0]


def works():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if not d.startswith('.') and d not in ('tools', 'templates', '_archive',
                                                            '_private', 'thumbs', 'assets', 'notes')]
        for fn in filenames:
            if fn.endswith('.html') and not fn.startswith('.') and '.bak' not in fn:
                out.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--files', nargs='*', default=[])
    ap.add_argument('--scope', default='')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    paths = list(args.files) or (works() if args.scope == 'all' else [])
    if not paths:
        print('没有目标文件')
        return 2

    print(f'第 0 遍 detect（权威基线）：{len(paths)} 件 …', flush=True)
    det_before = detect_many(paths)
    print(f'第 1 遍取证（标题层级）：{len(paths)} 件 …', flush=True)
    before = inspect(paths)
    n_items = sum(len(v) for v in before.values())
    print(f'取证到 {n_items} 处层级跳跃', flush=True)

    changed = {}
    for rel, items in before.items():
        if not items:
            continue
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            continue
        orig = open(full, encoding='utf-8', errors='ignore').read()
        html, n = apply_fix(orig, items)
        if n:
            changed[rel] = (orig, html, n)
    print(f'可改 {len(changed)} 件', flush=True)
    if not args.dry_run:
        for rel, (orig, html, n) in changed.items():
            open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(html)

    print(f'第 2 遍 detect：复验 {len(changed)} 件 …', flush=True)
    det_after = detect_many(list(changed.keys()))
    improved, reverted, unver = [], [], []
    for rel, (orig, html, n) in changed.items():
        if rel not in det_before:
            unver.append(rel)
            continue
        nb, na = skipped_count(det_before.get(rel, [])), skipped_count(det_after.get(rel, []))
        if na > nb:
            reverted.append((rel, nb, na))
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(orig)
        else:
            improved.append((rel, nb, na))
    print(f'\n✓ 变好或持平: {len(improved)} 件')
    for rel, b, a in sorted(improved, key=lambda x: x[1] - x[2])[:12]:
        print(f'    skipped-heading {b} → {a}  {os.path.basename(rel)}')
    if reverted:
        print(f'↩ 回退（变差）: {len(reverted)} 件')
        for rel, b, a in reverted[:8]:
            print(f'    {b} → {a}  {os.path.basename(rel)}')
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(changed[rel][0])
    if unver:
        print(f'⚠ 没验到（保持原样）: {len(unver)} 件')
        for rel in unver[:6]:
            print(f'    {os.path.basename(rel)}')
            if not args.dry_run:
                open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(changed[rel][0])

    with open('tools/fix_heading_levels_report.json', 'w', encoding='utf-8') as f:
        json.dump({'improved': improved, 'reverted': reverted, 'unverifiable': unver,
                   'items': n_items}, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
