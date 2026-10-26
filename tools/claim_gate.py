#!/usr/bin/env python3
"""
claim_gate.py — 断言闸门（无人值守质量防线）

为什么需要它
------------
展厅要"全自动更新"，就没有人工审核这道闸了。但 AI 抽取断言会出错，
且错得很有说服力（一串数字配一个像模像样的标签）。所以闸门必须
**机器可判定**，不能靠人眼。

三道闸门（缺一不可）
--------------------
  G1 逐字引用可验证
      每条断言带 quote（原文逐字片段）。校验时归一化后做子串匹配：
      quote 不在原文 → 拒绝。这是可确定性判定的，不需要人。
      实测：968 候选 → 拦掉 223（23%）。

  G2 语义可疑自动隔离
      quote 命中 ≠ 标签配对正确（值可能来自隔壁指标）。
      廉价启发式识别「像句子的标签」（含句末标点 / 虚词开头）→ 降级。
      实测：745 条中 32 条（4.3%）可被此规则自动识别。

  G3 每次重建都重校验
      人会疲劳，机器每次都会重跑。源文件被改动后旧 quote 失效 →
      自动降级 + 记 changelog。这是人工审核永远做不到的事。

分层（决定"能进哪个视图"）
--------------------------
  L0 已验证 —— quote 命中 且 标签不属可疑 → 进卷宗 / 断言序列 / 对账
  L1 待处理 —— 候选但未过闸 → 不进任何视图，只进待办队列
  L2 无结构 —— 作品本身没有统计块 → 只留档案页，永不伪造

边界（重要）
------------
quote 只能证明「这句话在原文里」，**不能证明「这句话支持那个断言」**。
因此自动断言只覆盖**机械可配对**的关系（同容器内或文本距离极近的
「数值 + 标签」）。解释性/因果性判断一律不进断言层 —— 那些留在
作品正文里由人读，不伪装成"团队历史判断"。

用法
----
  python3 claim_gate.py --scan              # 体检报告（只读，不写）
  python3 claim_gate.py --backfill          # 存量回填 → enrich.json
  python3 claim_gate.py --verify            # 重校验既有断言（漂移检测）
  python3 claim_gate.py --test              # 自测
"""

import json
import os
import re
import sys
import datetime
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENRICH = os.path.join(ROOT, 'enrich.json')
CHANGELOG = os.path.join(ROOT, 'tools', 'claim_changelog.jsonl')

EXCLUDE_DIRS = {'_archive', 'thumbs', '.git', '__pycache__', 'notes',
                'templates', 'tools', 'assets'}
EXCLUDE_FILES = {'index.html', 'enrich.json', 'manifest.json'}

# ── G2 语义可疑启发式 ──
# 注意：长度**不**作为拒绝条件。实测中「-25% CoreWeave 周跌（10/16 收盘）」
# 这类长标签大多是**正确**的（带时间状语），按长度拒绝会误伤 10%。
SENT_PUNCT = re.compile(r'[。；;！？!?]')
CONNECTIVE_START = re.compile(r'^(与|的|和|但|而|则|为|是|在|到|从|向|由|对|或|及)')
# 中文助词/连词结尾 = 语法不完整的片段（如「自回归模型的」）。
# 实测来源：<span class="spec-value">自回归模型的4倍</span> —— 真值是「4倍」，
# 但残留的「自回归模型的」不是指标名。中文指标名不会以这些字结尾。
PARTICLE_END = re.compile(r'(的|了|是|在|和|与|或|而|但|则|为|被|把|将|其|此)$')
# 出处注记不是指标名。实测：「14% *数据来源：各国能源部门及国际能源署（IEA）2026年」
# —— 数值是真的，但标签是脚注。卷宗里显示这个会误导读者。
SOURCE_NOTE = re.compile(r'(数据来源|资料来源|来源[：:]|出处[：:]|注[：:]|^\s*[*※#]|^\s*来源)')
# 标签不得含结构/代码符号。实测真垃圾是 <b>NO=79%</b> 这种 —— 标签抽成
# "NO="，是代码片段。但不能因此误伤 "Claude Code"、"128K"、"SWE-Bench Pro"、
# "vLLM / TGI / SGLang"、"CRWV 2031 年 9.75% 债到期收益率" 这类合法名。
# ⚠️ 符号集要**紧**：`%` `+` `&` 都不能进（"9.75%"、"C++"、"R&D" 都合法）。
# 早期用"必须含中文或纯缩写"规则误伤 111 条；用 `%+&` 符号集又误伤
# "9.75% 债到期收益率" 这类 —— 都是过度过滤。
SYMBOL_CHARS = re.compile(r'[=<>~$*|@#\\]')
HTML_ENTITY = re.compile(r'&(?:[a-z]{2,6}|#\d{2,5});?', re.I)
# 模板占位符守卫。模板的 claims 块里 {{ 数值 }} 这类占位是**合法 JSON**
# （占位在引号内），所以"只填了 quote 忘了填 value"时垃圾值能过 G1。
TEMPLATE_PLACEHOLDER = re.compile(r'\{\{|\}\}')
HAS_CJK = re.compile(r'[一-鿿]')

# ── 数值 + 单位 ──
UNITS = [
    '亿美元', '万桶/日', '亿桶', '亿美元', '万亿Token', '元/百万Token',
    '万桶', '美元', '万亿', '海里', '公里', '%', '亿', '倍', 'GW', 'TB', 'GB',
    '天', '年', '艘', '人', '户', '家', '条', '个', '元', '次', '座', '台',
]
_VALUE_RE = re.compile(
    r'^[\-+~≈<>]?[\d][\d,\.]*\s*(?:' + '|'.join(re.escape(u) for u in UNITS) + r')$'
)
_HAS_UNIT = re.compile('(?:' + '|'.join(re.escape(u) for u in UNITS) + r')')
_TOKEN_RE = re.compile(r'<(\w+)([^>]*)>([^<>]{1,80})')
_INLINE_NUM = re.compile(r'[\-+~≈<>]?[\d][\d,\.]*\s*(?:' +
                         '|'.join(re.escape(u) for u in UNITS) + r')')
_YEAR_ONLY = re.compile(r'^\d{4}\s*年$')      # 2026年 是年份，不是指标

_PUNCT_STRIP = '，。、；：""''（）()·—…!！?？「」《》'


# ── 归一化 ──────────────────────────────────────────────
def normalize(s):
    """归一化：去标签、压空白、去中英文标点。用于逐字引用比对。"""
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\s+', '', s)
    for c in _PUNCT_STRIP:
        s = s.replace(c, '')
    return s


def strip_code(html):
    """
    剥掉注释 / script / style —— 里面的文本不是作品正文。

    ⚠️ **顺序必须是 注释 → script/style**，不能反。
    反了会出事：HTML 注释里若出现字面量 `<script id="claims">`（模板的用法说明
    里就写了），则 `<script.*?</script>` 会从注释里那个 `<script>` 一直吃到文件
    底部真正的 `</script>` —— **整篇正文被当注释/script 删掉**。
    症状极隐蔽：文件渲染完全正常，只是抽取不出任何断言。
    （2026-10-26 端到端验证时发现：模板稿只抽出 6 个 token。）
    """
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)      # 先剥注释
    html = re.sub(r'<script\b.*?</script>', '', html, flags=re.S | re.I)
    html = re.sub(r'<style\b.*?</style>', '', html, flags=re.S | re.I)
    return html


def is_suspect_label(label):
    """G2：标签是否「像一句被截断的话」——这类多半是错配。

    返回可疑原因列表，空列表 = 通过。
    """
    reasons = []
    if SENT_PUNCT.search(label):
        reasons.append('含句末标点(像句子)')
    if CONNECTIVE_START.match(label):
        reasons.append('以虚词/连接词开头')
    if PARTICLE_END.search(label):
        reasons.append('以助词结尾(片段不完整)')
    if SOURCE_NOTE.search(label):
        reasons.append('是出处注记而非指标名')
    if SYMBOL_CHARS.search(label):
        reasons.append('含结构符号(疑似代码片段)')
    if HTML_ENTITY.search(label):
        reasons.append('含HTML实体泄漏')
    return reasons


# ── 候选抽取 ────────────────────────────────────────────
def _mk(value, label, quote):
    return {'value': value, 'label': label, 'quote': quote}


_WORD = re.compile(r'[A-Za-z一-鿿]')
_SENT_INTERNAL = re.compile(r'[，、；：。]')
_MARKER_PREFIX = re.compile(r'^[\s•·▲▼🔴🟠🟡🟢➡️↑↓*\u2022]{0,6}$')
_TRAIL_PUNCT = re.compile(r'^[\s.,;:!?%)\]}》」』…·•\-—–]*$')


def _clean_label(s):
    """剥掉标签首尾的装饰性标点，返回核心串。"""
    return s.strip(' 　,，。;；:：()（）[]【】·|/-—–')


def _extract_inline(text):
    """
    同一元素内的「数值 + 标签」内联配对（如 <p>-16% 布伦特原油两周跌幅</p>）。

    内联抽取天然绕过 G1（quote 就是整个文本节点，必然连续存在），
    所以质量必须由这里的规则守住。四条：

      A 数值在句首      —— 数值夹在句子中间 → 残留必是句子碎片，直接放弃
      B 残留不以数字收尾/开头 —— 否则说明残留里还挂着另一个数值（配对不干净）
      C 残留核心含 ≥2 个词字 —— 否则只是"(6月)"这类括号片段
      D 残留无句内标点   —— 有逗号/句号 → 是句子不是标签

    另有全局约束：同一文本节点内**有且仅有 1 个带单位数值**才配对。
    多个数值时无法判断哪个配哪个 → 直接放弃（宁缺毋滥），
    这正是早期全局正则产出「欧洲12其他10」式垃圾的根因。
    """
    t = re.sub(r'\s+', ' ', text).strip()
    if not t:
        return None
    hits = list(_INLINE_NUM.finditer(t))
    if len(hits) != 1:
        return None
    m = hits[0]
    value = m.group(0).strip()
    if _YEAR_ONLY.match(value.replace(' ', '')):
        return None

    # A 数值必须在句首或句尾 —— 夹在句子中间 → 残留必是句子碎片，直接放弃
    prefix = t[:m.start()]
    suffix = t[m.end():]
    if _MARKER_PREFIX.match(prefix):
        rest = suffix                      # 值在句首 → 标签是后半段
    elif _TRAIL_PUNCT.match(suffix):
        rest = prefix                      # 值在句尾 → 标签是前半段
    else:
        return None

    core = _clean_label(rest)
    if len(core) < 3 or not _WORD.search(core):
        return None
    # B 残留首尾不能是数字（说明还挂着另一个数值）
    if core[0].isdigit() or core[-1].isdigit():
        return None
    # C 至少 2 个词字
    if len(_WORD.findall(core)) < 2:
        return None
    # D 无句内标点（是句子不是标签）
    if _SENT_INTERNAL.search(core):
        return None
    return _mk(value, core[:28], t)


def extract_candidates(html):
    """
    抽取「数值 + 标签」配对，两种来源：

      A. 跨元素：数值元素 + 邻近标签元素（1~3 个文本节点内）
         quote 由两段拼成 → **可能不在原文中连续出现** → G1 会拦掉
      B. 同元素内联：文本节点内「数值 + 其余文字」
         quote = 整个文本节点 → 必然连续存在 → 由「单数值规则」保证质量

    刻意不做语义理解 —— 语义交给 G2 隔离。
    """
    body = strip_code(html)
    tokens = _TOKEN_RE.findall(body)
    out = []
    seen = set()

    # ── B. 同元素内联 ──
    for _tag, _attrs, raw in tokens:
        if not raw or not _INLINE_NUM.search(raw):
            continue
        c = _extract_inline(raw)
        if not c:
            continue
        key = (c['value'], c['label'])
        if key in seen:
            continue
        seen.add(key)
        out.append(c)

    # ── A. 跨元素 ──
    for i, (_tag, _attrs, raw) in enumerate(tokens):
        value = raw.strip()
        if not (2 <= len(value) <= 16):
            continue
        if not _VALUE_RE.match(value) or not _HAS_UNIT.search(value):
            continue
        if _YEAR_ONLY.match(value.replace(' ', '')):
            continue
        label = ''
        for j in range(i + 1, min(i + 4, len(tokens))):
            cand = re.sub(r'\s+', ' ', tokens[j][2]).strip()
            if len(cand) < 3:
                continue
            if not re.search(r'[\w一-鿿]', cand):
                continue
            if _VALUE_RE.match(cand):
                continue
            label = cand[:28]
            break
        if not label:
            continue
        key = (value, label)
        if key in seen:
            continue
        seen.add(key)
        out.append(_mk(value, label, f'{value} {label}'))
    return out


# ── G1 逐字引用校验 ─────────────────────────────────────
def verify_quote(quote, normalized_body):
    """引用必须在原文中逐字命中。命中=真命题存在；不命中=拒绝。"""
    return normalize(quote) in normalized_body


# ── 闸门主流程 ──────────────────────────────────────────
def gate_work(html):
    """对单篇作品跑完整闸门。返回 {l0, l1, l2_reason}。

    l0 每条: {value, label, quote}
    l1 每条: {value, label, quote, reason}
    """
    body = strip_code(html)
    nbody = normalize(re.sub(r'<[^>]+>', ' ', body))
    cands = extract_candidates(html)

    l0, l1 = [], []
    for c in cands:
        if not verify_quote(c['quote'], nbody):
            l1.append({**c, 'reason': 'quote未命中'})
            continue
        reasons = is_suspect_label(c['label'])
        if reasons:
            l1.append({**c, 'reason': '; '.join(reasons)})
            continue
        l0.append(c)

    l2_reason = ''
    if not cands:
        l2_reason = '作品无统计块（无可抽取的数值+标签配对）'
    return {'l0': l0, 'l1': l1, 'l2_reason': l2_reason}


def scan_works(root=ROOT):
    """扫描磁盘上所有作品。返回 {relpath: gate_result}。"""
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for fn in filenames:
            if not fn.endswith('.html') or fn.startswith('.'):
                continue
            if fn in EXCLUDE_FILES:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            try:
                html = open(full, encoding='utf-8', errors='ignore').read()
            except OSError:
                continue
            out[rel] = gate_work(html)
    return out


def filter_declared(html, declared):
    """
    校验作品**自己声明**的断言。声明不是特权 —— 同样要过 G1/G2。

    没有这一步，作品只要在 <script id="claims"> 里写什么都直接入库，
    闸门形同虚设（这正是"新作品可信度更高"这个前提的兑现点）。
    """
    if not declared:
        return []
    body = strip_code(html)
    nbody = normalize(re.sub(r'<[^>]+>', ' ', body))
    out = []
    for c in declared:
        if not isinstance(c, dict):
            continue
        value = str(c.get('value', '')).strip()
        label = str(c.get('label', '')).strip()
        quote = str(c.get('quote', '')).strip()
        if not (value and label and quote):
            continue
        # 占位符未替换 → 拒绝（否则"只填 quote 忘填 value"会把 {{ 数值 }} 当值入库）
        if (TEMPLATE_PLACEHOLDER.search(value) or TEMPLATE_PLACEHOLDER.search(label)
                or TEMPLATE_PLACEHOLDER.search(quote)):
            continue
        if not verify_quote(quote, nbody):
            continue                       # G1：引用不在原文 → 拒绝
        if is_suspect_label(label):
            continue                       # G2：标签像句子 → 拒绝
        out.append({'value': value, 'label': label, 'quote': quote})
    return out


def declared_claims(html):
    """读取作品自身声明的断言（<script id="claims">）。

    ⚠️ 必须先剥注释再找 script —— 注释里若出现字面量 `<script id="claims">`，
    直接正则匹配会命中注释里那个，捕获到垃圾内容导致 JSON 解析失败
    （症状：声明被静默忽略，退回自动抽取）。
    """
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    m = re.search(r'<script\b[^>]*id=["\']claims["\'][^>]*>(.*?)</script>', html, re.S | re.I)
    if not m:
        return None
    try:
        data = json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, list) else None


# ── enrich.json 读写 ────────────────────────────────────
def load_enrich():
    if not os.path.exists(ENRICH):
        return {'works': []}
    with open(ENRICH, encoding='utf-8') as f:
        return json.load(f)


def save_enrich(data):
    with open(ENRICH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def log_changelog(event, work, detail):
    """changelog：机器每次自动决策都留痕，供追溯。"""
    rec = {'ts': datetime.datetime.now().isoformat(timespec='seconds'),
           'event': event, 'work': work, 'detail': detail}
    with open(CHANGELOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')


# ── 回填 ────────────────────────────────────────────────
def backfill(dry_run=False):
    """把通过闸门的断言写回 enrich.json。幂等：重跑不产生差异。"""
    enrich = load_enrich()
    works = enrich.get('works', [])
    by_file = {w['file']: w for w in works}
    results = scan_works()

    stats = Counter()
    changed = []
    for rel, g in results.items():
        target = by_file.get(rel)
        if target is None:
            # 作品在磁盘但 enrich 无条目 → 建一个（不覆盖已有 description 等）
            target = {'file': rel}
            works.append(target)
            by_file[rel] = target
            stats['new_entry'] += 1
        old_claims = target.get('claims') or []
        # 作品自带声明优先（更权威），但同样要过闸门
        full = os.path.join(ROOT, rel)
        raw = open(full, encoding='utf-8', errors='ignore').read()
        declared = declared_claims(raw)
        if declared is not None:
            new_claims = filter_declared(raw, declared)
            if len(new_claims) != len(declared):
                stats['declared_rejected'] += len(declared) - len(new_claims)
        else:
            new_claims = g['l0']
        # G3 漂移检测：旧断言的 quote 若已不在原文 → 记录并丢弃
        stale = []
        if old_claims:
            body = strip_code(raw)
            nbody = normalize(re.sub(r'<[^>]+>', ' ', body))
            for oc in old_claims:
                if not verify_quote(oc.get('quote', ''), nbody):
                    stale.append(oc)
        if stale:
            log_changelog('claim_stale', rel, {'count': len(stale),
                                               'quotes': [s.get('quote', '')[:40] for s in stale]})
            stats['stale_dropped'] += len(stale)
        if old_claims != new_claims:
            target['claims'] = new_claims
            changed.append(rel)
        stats['works'] += 1
        stats['l0'] += len(g['l0'])
        stats['l1'] += len(g['l1'])
        if g['l2_reason']:
            stats['l2_works'] += 1

    if not dry_run:
        enrich['works'] = works
        save_enrich(enrich)
    return stats, changed


# ── 重校验（漂移检测）────────────────────────────────────
def verify_existing():
    """重校验 enrich.json 里既有的断言。返回问题列表。"""
    enrich = load_enrich()
    problems = []
    checked = 0
    for w in enrich.get('works', []):
        claims = w.get('claims') or []
        if not claims:
            continue
        full = os.path.join(ROOT, w['file'])
        if not os.path.exists(full):
            problems.append(f"{w['file']}: 作品不存在（断言悬空）")
            continue
        body = strip_code(open(full, encoding='utf-8', errors='ignore').read())
        nbody = normalize(re.sub(r'<[^>]+>', ' ', body))
        for c in claims:
            checked += 1
            if not verify_quote(c.get('quote', ''), nbody):
                problems.append(f"{w['file']}: quote失效 → {c.get('quote','')[:40]}")
    return problems, checked


# ── 报告 ────────────────────────────────────────────────
def report(results):
    items = list(results.values())
    l0 = sum(len(g['l0']) for g in items)
    l1 = sum(len(g['l1']) for g in items)
    l2 = sum(1 for g in items if g['l2_reason'])
    covered = sum(1 for g in items if g['l0'])
    print(f'作品            : {len(items)}')
    print(f'L0 已验证断言    : {l0}')
    print(f'L1 待处理        : {l1}')
    print(f'L2 无结构作品    : {l2}')
    print(f'有 L0 的作品     : {covered} / {len(items)}  ({covered/max(len(items),1)*100:.0f}%)')
    if l0:
        print(f'平均每件         : {l0/max(covered,1):.1f} 条')
    print()
    # L1 原因分布
    reasons = Counter()
    for g in items:
        for c in g['l1']:
            reasons[c['reason']] += 1
    if reasons:
        print('L1 拦截原因：')
        for r, n in reasons.most_common():
            print(f'   {n:4}  {r}')
        print()
    # 覆盖分布
    buckets = Counter()
    for g in items:
        n = len(g['l0'])
        b = '0' if n == 0 else ('1-4' if n < 5 else ('5-14' if n < 15 else '15+'))
        buckets[b] += 1
    print('每件 L0 数量分布：', dict(buckets))


# ── 自测 ────────────────────────────────────────────────
def selftest():
    ok = fail = 0

    def check(name, got, want):
        nonlocal ok, fail
        if got == want:
            ok += 1
            print(f'   ✓ {name}')
        else:
            fail += 1
            print(f'   ✗ {name}  期望={want} 实得={got}')

    print('【G1 逐字引用】')
    body = '霍尔木兹海峡免费开放60天 布伦特原油两周跌幅 全球海运石油占比'
    check('真引用命中', verify_quote('布伦特原油两周跌幅', normalize(body)), True)
    check('编造引用拒绝', verify_quote('布伦特原油上涨至138美元', normalize(body)), False)
    check('跨标点命中', verify_quote('从封锁恐慌到开放博弈', normalize('从封锁恐慌，到开放博弈')), True)

    print('【G2 语义可疑】')
    check('含句末标点 → 可疑', bool(is_suspect_label('与"程序员坍塌"叙事方向相反。')), True)
    check('虚词开头 → 可疑', bool(is_suspect_label('的净流入创历史新高')), True)
    check('正常标签 → 通过', is_suspect_label('CoreWeave 周跌（10/16 收盘）'), [])
    check('长标签不误伤', is_suspect_label('CRWV 2031 年 9.75% 债到期收益率'), [])
    check('助词结尾 → 可疑', bool(is_suspect_label('自回归模型的')), True)
    check('正常指标名不误伤', is_suspect_label('推理速度'), [])
    check('同比不误伤', is_suspect_label('同比'), [])
    check('代码片段 → 可疑', bool(is_suspect_label('NO=')), True)
    check('拉丁技术名不误伤', is_suspect_label('Claude Code'), [])
    check('含%的指标名不误伤', is_suspect_label('CRWV 2031 年 9.75% 债到期收益率'), [])
    check('C++不误伤', is_suspect_label('C++ 编译速度'), [])
    check('R&D不误伤', is_suspect_label('R&D 投入占比'), [])
    check('HTML实体泄漏 → 可疑', bool(is_suspect_label('&lt')), True)
    check('出处注记 → 可疑', bool(is_suspect_label('*数据来源：各国能源部门')), True)

    print('【抽取】')
    html = '<div><span class="kpi-value">-25%</span><span class="kpi-label">CoreWeave 周跌</span></div>'
    cands = extract_candidates(html)
    check('抽到 1 条', len(cands), 1)
    check('值正确', cands[0]['value'] if cands else None, '-25%')
    check('标签正确', cands[0]['label'] if cands else None, 'CoreWeave 周跌')
    check('无单位不算', len(extract_candidates('<span>2026年</span><span>某个标签</span>')), 0)
    check('年份不算指标', len(extract_candidates('<p>2026年 是转折点</p>')), 0)
    check('内联可抽', len(extract_candidates('<p>-16% 布伦特原油两周跌幅</p>')), 1)
    check('内联多数值放弃', len(extract_candidates('<p>-16% 跌 200 天 涨 30%</p>')), 0)
    check('内联值正确', extract_candidates('<p>-16% 布伦特原油两周跌幅</p>')[0]['value'], '-16%')
    check('内联标签正确', extract_candidates('<p>-16% 布伦特原油两周跌幅</p>')[0]['label'], '布伦特原油两周跌幅')

    print('【剥注释顺序（隐蔽 bug 回归）】')
    # 注释里出现字面量 <script id="claims"> 时，剥注释顺序错了会吃掉整篇正文
    tricky = ('<!-- 用法说明：底部写 <script id="claims"> 声明断言 -->'
              '<p>布伦特原油两周跌幅 -16%</p>'
              '<script type="application/json" id="claims">'
              '[{"value":"-16%","label":"布伦特原油两周跌幅","quote":"布伦特原油两周跌幅 -16%"}]'
              '</script>')
    check('注释含 script 字面量仍能抽到', len(extract_candidates(tricky)) >= 1, True)
    check('注释含 script 字面量时正文未被吞', '布伦特原油' in strip_code(tricky), True)
    dec = declared_claims(tricky)
    check('声明块能正确解析', len(dec) if dec else 0, 1)

    print('【占位符守卫】')
    ph = ('<p>布伦特原油两周跌幅 -16%</p>'
          '<script type="application/json" id="claims">'
          '[{"value":"{{ 数值 }}","label":"布伦特原油两周跌幅","quote":"布伦特原油两周跌幅 -16%"}]'
          '</script>')
    check('未替换的占位值被拒', len(filter_declared(ph, declared_claims(ph) or [])), 0)

    print('【创意类：自由结构（无语义 class 名）】')
    # 创意类不用模板 —— class 名任意，只能靠声明把断言送进卷宗
    free = ('<div class="whatever-x"><span>$0.10 / 1M</span>'
            '<span>Token 价格战下沿单价</span></div>'
            '<script type="application/json" id="claims">'
            '[{"value":"$0.10 / 1M","label":"Token 价格战下沿单价","quote":"$0.10 / 1M"}]'
            '</script>')
    check('自由结构能读出声明', len(declared_claims(free) or []), 1)
    check('自由结构的声明能过闸', len(filter_declared(free, declared_claims(free) or [])), 1)
    check('自由结构自动抽取为 0（所以必须声明）', len(extract_candidates(free)), 0)

    print('【闸门端到端】')
    g = gate_work('<p>布伦特原油两周跌幅 -16%</p><p>存储芯片在 iPhone 18 Pro 物料成本 34%</p>')
    check('L0 有 2 条', len(g['l0']), 2)
    check('L1 为 0', len(g['l1']), 0)

    print(f'\n自测结果: {ok} 通过 / {fail} 失败')
    return 0 if fail == 0 else 1


# ── CLI ─────────────────────────────────────────────────
def main():
    if '--test' in sys.argv:
        return selftest()
    if '--verify' in sys.argv:
        problems, checked = verify_existing()
        print(f'重校验 {checked} 条断言')
        if problems:
            print(f'✗ {len(problems)} 条失效：')
            for p in problems[:20]:
                print('   -', p)
            return 1
        print('✓ 全部通过')
        return 0
    if '--backfill' in sys.argv:
        dry = '--dry-run' in sys.argv
        stats, changed = backfill(dry_run=dry)
        print(f"作品 {stats['works']} · L0 {stats['l0']} · L1 {stats['l1']} · "
              f"L2作品 {stats['l2_works']} · 漂移丢弃 {stats['stale_dropped']}")
        print(f"变更条目 {len(changed)}" + ('（dry-run，未写盘）' if dry else '（已写回 enrich.json）'))
        return 0
    # 默认：体检报告
    results = scan_works()
    report(results)
    return 0


if __name__ == '__main__':
    sys.exit(main())
