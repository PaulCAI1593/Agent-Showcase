#!/usr/bin/env python3
"""
inject_contracts.py — 给缺声明的作品补上「作品契约」

为什么需要它
------------
规则15 要求**每一件**作品都在底部声明断言（`<script id="claims">`）、
在 `<head>` 声明追踪线（`<meta name="showcase-beat">`）。这条契约是
「跨作品时间线」的地基：同一指标的断言靠**标签一致**自动连成序列。

现实：113 件里只有 12 件有 claims 块、10 件有追踪线声明。
103 件没有追踪线 → 这些作品的断言接不进任何序列，追踪台上的线全是断头路。

所以要补。但**不能手工补**：
- 手工写断言 = 绕过闸门，等于自己给自己发通行证
- 手写 103 次 = 不可复现，下次新增作品又漏

本工具的立场：**只搬运，不发明**
- 断言全部来自 `enrich.json` —— 那是 `claim_gate.py` 逐条过闸门
  （G1 逐字引用 / G2 标签像句子 / G4 页面自身计数行）之后写回的权威集合
- 追踪线全部来自 `manifest.json` 的 `beat` 字段 —— 由 `group_by_line()` 判定
- 本工具**不新增任何断言**，只把已过闸门的数据搬进 HTML

它不碰作品的视觉：一段 `application/json`（不执行）+ 一个 meta，不产生任何 class。

用法：
  python3 tools/inject_contracts.py --dry-run   # 预览
  python3 tools/inject_contracts.py             # 写入（幂等）
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

DECL_RE = re.compile(r'<script type="application/json" id="claims">')
BEAT_RE = re.compile(r'<meta name="showcase-beat"')
CHARSET_RE = re.compile(r'<meta charset="[^"]*">', re.I)

# ── 人工归线（13 条封闭集）────────────────────────────────
# 关键词推断（group_by_line）判不出归属的 7 件，由总指挥按**断言内容**归线，
# 理由写在这里，便于日后复核与改判。
# 归线的权威位置是作品自己的 <meta name="showcase-beat">（build_manifest 声明优先），
# 所以这里注入声明，manifest 下次构建自动跟随 —— 不手改生成物。
BEAT_OVERRIDES = {
    # 断言全是收入结构/毛利率/资本开支（+176% 2048、+35% -138、+22% 金融科技）→ 财务视角
    'works/2026-08-15/research/2026-08-15-tencent-ai-bet.html': '估值与资本',
    # 断言全是营收/YoY/毛利率/Cloud 增速的横向对比 → 财报视角
    'works/2026-08-13/creative/2026-08-13-ai-earnings-dashboard.html': '估值与资本',
    # 断言是净资产/财富/市值里程碑 → 资本视角
    'works/2026-06-20/creative/2026-06-20-musk-trillion-path.html': '估值与资本',
    # 断言是工具份额/企业渗透/AI 写代码比例/设备覆盖 → AI 编程工具的产业面
    'works/2026-06-20/creative/2026-06-20-spacex-cursor.html': '工具链与产业主权',
    # 断言是 FrontierCode / SWE-Bench Pro / HLE 的模型对战 → 厂商军备竞赛
    'works/2026-06-12/creative/2026-06-12-ai-model-wars-48h.html': '厂商与算力权力',
    # 断言是各 IDE 工具份额与渗透率 → 工具链
    'works/2026-06-11/creative/2026-06-11-ai-coding-tools-matrix.html': '工具链与产业主权',
    # 断言是多模型路由的接入层 → 工具链（与 407「智能体上岗证」同面）
    'works/2026-06-11/creative/2026-06-11-model-routing-layer.html': '工具链与产业主权',
}


def load(name):
    with open(os.path.join(ROOT, name), encoding='utf-8') as f:
        return json.load(f)


def esc_json_for_script(obj):
    """JSON 序列化后，把可能提前闭合 script 的字符转义掉。

    quote 里若含 `</script>`，直接内联会让整页 HTML 提前结束 —— 这是真实事故类型。
    """
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    return s.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')


def claims_block(claims):
    lines = ['<script type="application/json" id="claims">']
    lines.append('[')
    for i, c in enumerate(claims):
        obj = {'value': c.get('value', ''), 'label': c.get('label', ''),
               'quote': c.get('quote', '')}
        lines.append('  ' + json.dumps(obj, ensure_ascii=False)
                     + (',' if i < len(claims) - 1 else ''))
    lines.append(']')
    lines.append('</script>')
    return '\n'.join(lines)


def inject_one(rel, claims, beat, dry=False):
    """返回 (new_html, actions)。actions 是本件实际做了什么。

    ⚠️ dry=True 时**只算不写** —— 早期版本把 dry 只用于打印，
    结果「预览」真的改了 91 个作品文件。这种地雷不能留。
    """
    path = os.path.join(ROOT, rel)
    html = open(path, encoding='utf-8', errors='ignore').read()
    actions = []
    orig = html

    # ── 追踪线 meta ──
    if beat and not BEAT_RE.search(html):
        meta = f'<meta name="showcase-beat" content="{beat}">'
        m = CHARSET_RE.search(html)
        if m:
            html = html[:m.end()] + '\n' + meta + html[m.end():]
        elif '<head>' in html:
            html = html.replace('<head>', '<head>\n' + meta, 1)
        else:
            return None, ['<head> 缺失，未注入追踪线']
        actions.append('beat')

    # ── 断言块 ──
    if claims and not DECL_RE.search(html):
        block = claims_block(claims)
        if '</body>' in html:
            html = html.replace('</body>', block + '\n</body>', 1)
        else:
            html = html + '\n' + block
        actions.append('claims')

    if html != orig and not dry:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    return html, actions


def main():
    # 参数交给 argparse（与 build_manifest.py / claim_gate.py 同法）：
    # 原实现 `dry = '--dry-run' in sys.argv` 意味着**任何**未识别参数
    # （含 --help、拼错的 --dryrun）都会落到 dry=False 分支 —— 诊断命令
    # 会真的把 claims/meta 写进作品 HTML。写盘工具必须先过 argparse。
    ap = argparse.ArgumentParser(
        prog='inject_contracts.py', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='只预览，不写入作品 HTML')
    dry = ap.parse_args().dry_run
    manifest = load('manifest.json')
    enrich = load('enrich.json')
    by_file = {w['file']: w for w in enrich.get('works', [])}

    n_beats = n_claims = n_skip = n_nobeat = n_noclaims = 0
    touched = []
    for grp in ('research', 'creative'):
        for it in manifest[grp]:
            rel = it['file']
            if not os.path.exists(os.path.join(ROOT, rel)):
                continue
            beat = (it.get('beat') or '').strip()
            beat = BEAT_OVERRIDES.get(rel, beat)
            claims = by_file.get(rel, {}).get('claims') or []
            # 只注入闸门放行、且三字段齐全的断言
            claims = [c for c in claims
                      if c.get('value') and c.get('label') and c.get('quote')]
            html, actions = inject_one(rel, claims, beat, dry=dry)
            if html is None:
                n_skip += 1
                continue
            if actions:
                touched.append((rel, actions))
                if 'beat' in actions:
                    n_beats += 1
                if 'claims' in actions:
                    n_claims += 1
                if not dry:
                    pass
            else:
                n_skip += 1
            if not beat:
                n_nobeat += 1
            if not claims:
                n_noclaims += 1

    print(f'{"[dry-run] " if dry else ""}注入追踪线 meta: {n_beats} 件')
    print(f'{"[dry-run] " if dry else ""}注入断言块    : {n_claims} 件')
    print(f'{"[dry-run] " if dry else ""}未改动          : {n_skip} 件')
    print(f'  其中无追踪线可注入（manifest 未判定归属）: {n_nobeat} 件')
    print(f'  其中无断言可注入（0 条已验证断言）      : {n_noclaims} 件')
    for rel, acts in touched[:8]:
        print(f'   · {rel} → {acts}')
    if len(touched) > 8:
        print(f'   · …另有 {len(touched) - 8} 件')
    return 0


if __name__ == '__main__':
    sys.exit(main())
