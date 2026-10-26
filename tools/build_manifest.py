#!/usr/bin/env python3
"""
build_manifest.py — showcase 单一数据源生成器

解决的问题（根因修复）：
  1. 缩略图路径日期前缀重复（thumb 字段生成逻辑错误）
  2. type（research/creative）手工登记错误
  3. manifest 长期手工维护，必然与磁盘脱节
  4. 标签靠手写死值，与数据词表对不上，导致筛选按钮点出空白页

用法：
  python3 build_manifest.py            # 扫描磁盘，重建 manifest.json
  python3 build_manifest.py --check    # 只校验，不写文件（CI 用）

设计原则：
  - manifest.json 是**生成物**，不是手工文件
  - 以磁盘为准：文件存在才算条目，缩略图以实际 webp/png 文件为准
  - 保留人工字段：description / highlights / agent / title 等在 enrich.json 中维护
"""

import json, os, re, sys, itertools
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import claim_gate as gate
except ImportError:                                    # 闸门缺失时降级但不崩
    gate = None

# ── 追踪线主题族（人工可编辑；关键词子串匹配标签）──
# 跨族标签会重复计入，这是刻意取舍：追踪线要的是"这条主题覆盖了多少作品"，
# 不是互斥分区。unclassified_tags 会暴露未被任何族覆盖的标签，防止新主题静默漏掉。
BEAT_PENDING = "待归类"   # 显式退出标记：作者声明"本篇不属于任何现有线"

BEAT_FAMILIES = {
    "开源 vs 闭源之争":  ["开源", "闭源", "模型疲劳", "AI模型", "大模型"],    "Agent 与编排":      ["Agent", "编排", "智能体", "Harness", "Codex"],
    "厂商与算力权力":    ["OpenAI", "Anthropic", "DeepSeek", "英伟达", "Hugging",
                          "AI权力", "中国AI", "Mistral", "Google", "Meta Muse"],
    "地缘与能源":        ["霍尔木兹", "能源", "伊朗", "中东", "地缘", "油价", "美伊", "军演"],
    "估值与资本":        ["估值", "泡沫", "IPO", "私人信贷", "AI基建", "资本",
                          "黄金", "美元", "避险", "比特币"],
    "宏观利率与股市":    ["美债", "日债", "加息", "利率", "通胀", "A股", "科技股",
                          "股市", "美联储", "非农", "半导体", "韩国"],
    "算力·能耗·环境":    ["算力", "数据中心", "核能", "电力", "能耗", "碳", "绿色AI", "硬件"],
    "就业与劳动":        ["就业", "白领", "职业", "技能", "生产力", "超级个体",
                          "职场", "初级员工", "入门"],
    "机器人与具身":      ["机器人", "具身", "手术", "医疗"],
    "安全与治理":        ["安全", "提示注入", "自我欺骗", "越权", "监管", "信任",
                          "合规", "FDA", "图灵"],
    "工具链与产业主权":  ["阿里", "出口管制", "产业政策", "人工智能+", "工具链",
                          "供应链", "禁令", "FCC", "40项"],
    "应用落地":          ["医疗器械", "漫剧", "微信", "社交", "反诈", "教育",
                          "数据饥荒", "合成数据", "Science", "诺奖", "数学证明",
                          "数字孪生", "日常", "人机共生"],
    "成本与普惠":        ["Token价格", "普惠", "成本", "存储涨价", "三星", "苹果",
                          "HBM", "服务器", "定价", "罢工", "工资"],
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # showcase/（本脚本位于 tools/）
THUMBS = os.path.join(ROOT, 'thumbs')
MANIFEST = os.path.join(ROOT, 'manifest.json')
ENRICH = os.path.join(ROOT, 'enrich.json')

# ── 持续更新的硬约束 ──
RECENT_DESC_DAYS = 60      # EMBEDDED 只为最近 N 天保留 description（仅 bento/featured 会显示）
SIZE_BUDGET_KB = 400       # index.html 体积上限，超出即 FAIL，强制做取舍而不是静默膨胀
PILLS_BUDGET = 12          # 月份 pill 数量上限提示线
# 人工类型登记表（key = 文件名去扩展名，跨目录稳定）。
# 优先级最高：高于 enrich 显式 type、目录结构、缩略图前缀与旧 manifest，
# 以打破「缩略图名 ↔ 类型判定」的循环误分类。
TYPES_REGISTRY = os.path.join(ROOT, 'tools', 'autopublish_types.json')


def load_type_registry():
    reg = load_json(TYPES_REGISTRY, {})
    if isinstance(reg, dict) and 'types' in reg:
        reg = reg['types']
    if not isinstance(reg, dict):
        return {}
    return {k: v for k, v in reg.items() if v in ('research', 'creative')}

EXCLUDE_DIRS = {'_archive', 'thumbs', '.git', '__pycache__', 'templates', 'tools', 'assets', 'notes'}
EXCLUDE_FILES = {'index.html', 'enrich.json', 'manifest.json', 'build_manifest.py'}
BACKUP_RE = re.compile(r'\.bak\.\d{8}-\d{6}$')
# 交付前必须替换的占位符：模板 {{ }} 与旧式【】 两种都算
PLACEHOLDER_RE = re.compile(r'\{\{[^}]*\}\}|【[^】]{2,20}】')


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def scan_works():
    """扫描所有作品 HTML（排除归档/备份/工具脚本）。"""
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for fn in filenames:
            if not fn.endswith('.html'):
                continue
            if fn.startswith('.'):
                # 隐藏分片（.part1.html / .part2.html 等）= 构建中间产物，非作品
                continue
            if fn in EXCLUDE_FILES or BACKUP_RE.search(fn):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            out.append(rel)
    return sorted(out)


def detect_type(rel, old):
    """
    判定 research / creative。
    优先级：目录结构 > 缩略图文件名 > 旧 manifest。
    目录结构最可靠（YYYY-MM-DD/research|creative/...）。
    """
    parts = rel.split(os.sep)
    if len(parts) >= 3 and parts[1] in ('research', 'creative'):
        return parts[1]
    # 缩略图命名带 type 前缀，也是可靠信号
    stem = os.path.basename(rel)[:-5]
    date = parts[0] if re.match(r'^\d{4}-\d{2}-\d{2}$', parts[0]) else ''
    for t in ('research', 'creative'):
        for ext in ('webp', 'png'):
            if date and os.path.exists(os.path.join(THUMBS, f'{date}-{t}-{stem}-thumb.{ext}')):
                return t
    return old or 'research'


def resolve_thumb(rel, date, typ):
    """
    缩略图名规则：{date}-{type}-{stem}-thumb.{ext} —— 只认磁盘上真实存在的。
    优先 .webp（由 tools/make_thumbs_webp.py 生成，体积约为 PNG 的 1/15），
    无 webp 时回退 .png。
    """
    stem = os.path.basename(rel)[:-5]
    for t in (typ, 'research', 'creative'):
        for ext in ('webp', 'png'):
            name = f'{date}-{t}-{stem}-thumb.{ext}'
            if os.path.exists(os.path.join(THUMBS, name)):
                # type 与声明不符时视为无图（避免把别处缩略图错挂到本条目）
                return 'thumbs/' + name if t == typ else ''
    return ''


def detect_date(rel, fallback):
    m = re.match(r'^(\d{4}-\d{2}-\d{2})', os.path.basename(rel))
    if m:
        return m.group(1)
    parts = rel.split(os.sep)
    if parts and re.match(r'^\d{4}-\d{2}-\d{2}$', parts[0]):
        return parts[0]
    return fallback or ''


def extract_title(path, fallback):
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            head = f.read(4000)
        m = re.search(r'<title>(.*?)</title>', head, re.S | re.I)
        if m:
            t = re.sub(r'\s+', ' ', m.group(1)).strip()
            if t:
                return t
    except OSError:
        pass
    return fallback or os.path.basename(path)[:-5]


def sync_embedded(manifest):
    """
    同步 index.html 内的 EMBEDDED 快照。
    index.html 以 fetch('manifest.json') 为主数据源；EMBEDDED 仅用于
    file:// 协议（浏览器禁止 fetch 读取本地 json）时的回退。
    没有这一步，file:// 预览会一直看到旧数据。
    """
    idx = os.path.join(ROOT, 'index.html')
    if not os.path.exists(idx):
        return False
    html = open(idx, encoding='utf-8').read()
    m = re.search(r'^const EMBEDDED=\{.*\};$', html, re.M)
    if not m:
        print('  提示: index.html 中未找到 EMBEDDED 快照，跳过（可能已改为纯 fetch 模式）')
        return False

    # 紧凑快照：file:// 必须内联数据，所以只能压字段、不能压条数（档案要可浏览）。
    # description 只有 bento / featured（最新 3 件）会显示，月历卡与时间线都不显示，
    # 因此仅对最近 RECENT_DESC_DAYS 天保留，其余省略 —— 视觉零损失，省约 27%。
    import datetime
    cutoff = (datetime.date.today() - datetime.timedelta(days=RECENT_DESC_DAYS)).isoformat()
    snap = {g: [] for g in ('research', 'creative')}
    kept = 0
    # 解析追踪线归属：声明优先，否则按关键词推断（与聚合层同一套口径）
    line_of = {}
    for name, hits in group_by_line(manifest['research'] + manifest['creative'])[0].items():
        for it in hits:
            line_of.setdefault(it['file'], name)
    for g in ('research', 'creative'):
        for i in manifest[g]:
            rec = {'file': i['file'], 'thumb': i['thumb'], 'title': i['title'],
                   'date': i['date'], 'type': i['type'], 'highlights': i['highlights']}
            beat = i.get('beat') or line_of.get(i['file']) or ''
            if beat:
                rec['beat'] = beat
            # 断言（压缩为 value/label，供卡片展示与**全文检索**命中）
            # ⚠️ 必须放**全部**：平均每件 10.8 条，只放前 3 条等于七成断言搜不到
            # （实测 997 条里只索引了 250 条）。全量仅增约 31KB，预算内。
            # 卡片只显示 claims[0]（最具代表性的一条，由 order_claims 排在首位）。
            cl = i.get('claims') or []
            if cl:
                rec['claims'] = [{'v': c.get('value', ''), 'l': c.get('label', '')}
                                 for c in cl]
            if i['date'] >= cutoff and i['description']:
                rec['description'] = i['description']
                kept += 1
            snap[g].append(rec)
    # 字段名必须与 manifest 一致，否则 normalize() 读不到（曾因此 file:// 全丢描述）
    # stats 必须一并内联：追踪台是首页主叙事，file:// 下缺了它会渲染成空白区块。
    snap['stats'] = manifest.get('stats', {})
    new_emb = 'const EMBEDDED=' + json.dumps(snap, ensure_ascii=False) + ';'
    html = html[:m.start()] + new_emb + html[m.end():]

    # TAGMAP 已废弃：它 100/103 与 manifest.highlights 重复，且部分条目更旧会反向覆盖。
    # 标签唯一来源现在是 manifest.highlights / EMBEDDED.highlights。
    tm = re.search(r'^const TAGMAP=(\{.*\});$\n?', html, re.M)
    removed_tagmap = bool(tm)
    if tm:
        html = html[:tm.start()] + html[tm.end():]

    open(idx, 'w', encoding='utf-8').write(html)
    print(f'  已同步 index.html EMBEDDED 快照（file:// 回退用，'
          f'{len(snap["research"]) + len(snap["creative"])} 件，其中 {kept} 件含描述）')
    if removed_tagmap:
        print('  已移除废弃的 TAGMAP 数据段（标签改由 manifest.highlights 单一来源）')
    return True


def guardrails(manifest):
    """校验 index.html 的生成物契约与尺寸预算。返回问题列表（空=通过）。"""
    problems = []
    idx_path = os.path.join(ROOT, 'index.html')
    if not os.path.exists(idx_path):
        return problems
    ih = open(idx_path, encoding='utf-8').read()
    size_kb = len(ih.encode()) / 1024

    if 'const TAGMAP=' in ih:
        problems.append('index.html 仍含已废弃的 TAGMAP 数据段')

    em = re.search(r'^const EMBEDDED=(\{.*\});$', ih, re.M)
    if not em:
        problems.append('index.html 缺少单行 EMBEDDED 数据段（生成器契约已断）')
    else:
        try:
            snap = json.loads(em.group(1))
            s_items = snap.get('research', []) + snap.get('creative', [])
            if len(s_items) != manifest['total']:
                problems.append(f'EMBEDDED 件数 {len(s_items)} ≠ manifest {manifest["total"]}（快照过期）')
            if 'stats' not in snap:
                problems.append('EMBEDDED 缺少 stats 聚合（file:// 下追踪台会渲染成空白）')
            elif s_items:
                missing = {'file', 'title', 'date', 'type', 'highlights'} - set(s_items[0])
                if missing:
                    problems.append(f'EMBEDDED 字段与 manifest 不一致，缺 {sorted(missing)}')
        except json.JSONDecodeError as exc:
            problems.append(f'EMBEDDED 解析失败: {exc}')

    # 交付前必须替换的占位符：模板 {{ }} 与旧式【】 两种都算
    # 曾出现模板的【作品标题】占位被原样发布上展 —— 必须在护栏里硬失败
    leftovers = []
    for g in ('research', 'creative'):
        for i in manifest[g]:
            for field, val in (('标题', i.get('title') or ''),
                               ('描述', i.get('description') or '')):
                if PLACEHOLDER_RE.search(val):
                    leftovers.append(f'{i["file"]} 的{field}仍含占位符（{val[:36]}）')
    if leftovers:
        problems.append(f'{len(leftovers)} 件作品仍含未替换的占位符 —— 交付前必须替换')
        for x in leftovers[:5]:
            print('       !', x)

    if size_kb > SIZE_BUDGET_KB:
        problems.append(f'index.html {size_kb:.0f}KB 超出预算 {SIZE_BUDGET_KB}KB')

    # 署名缺失会让首页"谁在主责"矩阵出现"未署名"行，并压低合著率
    unattributed = [i['file'] for g in ('research', 'creative')
                    for i in manifest[g] if not (i.get('agent') or '').strip()]
    if unattributed:
        print(f'  提示: {len(unattributed)} 件作品缺 agent 署名'
              f'（可在 enrich.json 补，依据见 archive/选题库-派单日.md 的"推荐Agent"）')
        for f in unattributed[:3]:
            print('     -', f)

    months = {i['date'][:7] for g in ('research','creative') for i in manifest[g]}
    if len(months) > PILLS_BUDGET:
        print(f'  提示: 已积累 {len(months)} 个月份，超过 {PILLS_BUDGET} 个'
              f'——月份导航需按年分组，否则 pill 会无限增长')
    emb_kb = len(em.group(1).encode())/1024 if em else 0
    print(f'  护栏: index.html {size_kb:.0f}KB / 预算 {SIZE_BUDGET_KB}KB · '
          f'EMBEDDED {emb_kb:.0f}KB · {len(months)} 个月份')
    return problems


def read_declared_beat(path):
    """
    读取作品声明的追踪线：<meta name="showcase-beat" content="...">

    声明式优于猜：过去靠标签关键词猜归属，形态标签（"数据可视化"）
    会被误当主题线。现在由产出方显式声明，封闭集校验。
    """
    try:
        html = open(path, encoding='utf-8', errors='ignore').read()
    except OSError:
        return ''
    m = re.search(r'<meta[^>]*name=["\']showcase-beat["\'][^>]*content=["\']([^"\']+)["\']',
                  html, re.I)
    if not m:
        m = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']showcase-beat["\']',
                      html, re.I)
    return m.group(1).strip() if m else ''


def read_declared_claims(path):
    """
    读取作品自身声明的断言：<script type="application/json" id="claims">[...]</script>

    这是**权威来源** —— 断言与原文同文件，不可能漂移。
    存量作品没有这个块时回落到 enrich.json（由 claim_gate 回填并逐条重校验）。

    实现复用 claim_gate.declared_claims —— 两处各写一份正则必然分叉，
    而分叉的代价是「声明被静默忽略」（曾因剥注释顺序错误导致）。
    """
    if gate is None:
        return None
    try:
        html = open(path, encoding='utf-8', errors='ignore').read()
    except OSError:
        return None
    return gate.declared_claims(html)


def compute_claim_stats(manifest, gate):
    """
    断言层聚合（来自 claim_gate 的 L0 层）。

    只有过了两道机器闸门的断言才计入；L1 待处理与 L2 无结构作品
    **不进任何视图**，只体现在计数里供巡检。
    """
    items = manifest['research'] + manifest['creative']
    results = gate.scan_works()
    total = covered = 0
    by_beat = Counter()
    unverified = 0
    # ⚠️ total 取**已入库的 claims**，不取重新扫描的结果 ——
    # 两者会差 1~2 条（重扫描与回填的分类边界不完全一致），
    # 导致「断言总数 1001」却「重校验 1000/1000 通过」这种自相矛盾。
    for i in items:
        n = len(i.get('claims') or [])
        total += n
        if n:
            covered += 1
        g = results.get(i['file'])
        if g:
            unverified += len(g['l1'])
    # 断言按作品所属追踪线归集（**声明优先**，与卷宗口径一致）
    line_works, _ = group_by_line(items)
    for name, hit in line_works.items():
        for i in hit:
            by_beat[name] += len(i.get('claims') or [])
    l1 = sum(len(g['l1']) for g in results.values())
    l2 = sum(1 for g in results.values() if g['l2_reason'])
    return {
        'total': total,
        'works_covered': covered,
        'works_total': len(items),
        'coverage': round(covered / len(items) * 100) if items else 0,
        'pending': l1,
        'no_structure': l2,
        'by_beat': [{'name': n, 'claims': c} for n, c in by_beat.most_common()],
    }


def claim_guardrails(manifest, gate):
    """
    断言层不变量。返回问题列表（空=通过）。

    为什么要这些：断言层是"无人值守"产出的，最危险的失效模式是
    **静默退化** —— 抽取规则坏掉、源文件被改、某条引用失效，
    但页面照常渲染，没人看得出来。所以把"退化"直接判成 FAIL。

    两种退化要分清：
      ① 引用失效（已入库的断言对不上原文）→ 硬失败，必须重跑回填
      ② 抽取拒绝率突增（候选变多但通过变少）→ 规则坏了，硬失败
    注意：**拒绝率高本身不是失败** —— 闸门本就该拒掉大部分坏候选。
    """
    problems = []
    stats = manifest.get('claim_stats') or {}
    total = stats.get('total', 0)
    pending = stats.get('pending', 0)
    cand = total + pending
    rate = (pending / cand) if cand else 0

    # ① 逐条重校验：source of truth 是作品原文
    bad, checked = 0, 0
    for g in manifest['research'] + manifest['creative']:
        full = os.path.join(ROOT, g['file'])
        if not os.path.exists(full):
            bad += 1
            continue
        html = open(full, encoding='utf-8', errors='ignore').read()
        nbody = gate.normalize(gate.re.sub(r'<[^>]+>', ' ', gate.strip_code(html)))
        for c in (g.get('claims') or []):
            checked += 1
            if not gate.verify_quote(c.get('quote', ''), nbody):
                bad += 1
    if bad:
        problems.append(f'{bad}/{checked} 条断言引用失效'
                        f'（源文件已改或断言陈旧 → 需重跑 claim_gate --backfill）')

    # ② 基线对比：断言总数跌幅 / 抽取拒绝率突增
    state_path = os.path.join(ROOT, 'tools', '.claim_state.json')
    state = load_json(state_path, {})
    prev_total = state.get('total')
    prev_rate = state.get('reject_rate')
    if prev_total and total < prev_total * 0.8:
        problems.append(f'断言总数 {total} 较基线 {prev_total} 下跌超过 20%'
                        f'（抽取回归或源文件被改）')
    if prev_rate is not None and rate > prev_rate + 0.15:
        problems.append(f'抽取拒绝率 {rate*100:.1f}% 较基线 {prev_rate*100:.1f}% '
                        f'突增逾 15pp（抽取规则可能已失效）')

    if state.get('total') != total or state.get('reject_rate') is None:
        try:
            with open(state_path, 'w', encoding='utf-8') as f:
                json.dump({'total': total, 'reject_rate': round(rate, 4),
                           'date': __import__('datetime').date.today().isoformat()},
                          f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    print(f'  断言: {total} 条 · 覆盖 {stats.get("works_covered", 0)}/'
          f'{stats.get("works_total", 0)} 件 ({stats.get("coverage", 0)}%) · '
          f'待处理 {pending} · 无结构 {stats.get("no_structure", 0)} · '
          f'重校验 {checked - bad}/{checked} 通过')
    return problems


_TOKEN_SPLIT = re.compile(r'[一-鿿]|[A-Za-z][A-Za-z0-9]{1,}|\d+(?:\.\d+)?')


def pick_representative(l0, work):
    """
    从一件作品的已验证断言里挑一条**最有代表性**的（卷宗正文用）。

    单纯取第一条会挑到不相干的：实测「Fable 5 全球禁令」这篇的断言里
    第一条带 % 的是 "80.3% SWE-bench Pro 得分" —— 真实，但在地缘线里
    完全不具代表性。

    打分：标签的分词与「标题 + 标签 + 摘要」的重合度，
    再给带 % 的加一点权重（百分比最可比较）。确定性排序，重跑结果一致。
    """
    ctx = ' '.join([work.get('title', ''), work.get('description', ''),
                    ' '.join(work.get('highlights') or [])]).lower()
    ctx_tokens = set(_TOKEN_SPLIT.findall(ctx))
    best, best_score = l0[0], -1.0
    for c in l0:
        label_tokens = set(_TOKEN_SPLIT.findall(c['label'].lower()))
        overlap = len(label_tokens & ctx_tokens)
        score = overlap * 2.0 + (1.0 if '%' in c['value'] else 0.0)
        # 同分时取更短的标签（更像指标名，不像句子）
        score -= len(c['label']) * 0.01
        if score > best_score:
            best, best_score = c, score
    return best['value'], best['label']


def group_by_line(items):
    """
    把作品按追踪线归组。

    **声明优先**：作品自带 `<meta name="showcase-beat">` 声明时以声明为准；
    没有声明才回落到标签关键词匹配（存量作品）。

    为什么必须声明优先：声明式优于猜。靠关键词猜会把形态标签
    （"数据可视化""危机模拟"）混进主题线，也会让一条作品同时落进多条线。
    之前建了声明字段却没在聚合里用 —— 等于有两个真相源，正是本项目
    反复踩的坑（2026-10-26 端到端验证时发现）。
    """
    out = {name: [] for name in BEAT_FAMILIES}
    unclassified = []
    for i in items:
        # ⚠️ 只有**显式声明**才独占一条线；推断归属仍按关键词多归属
        # （BEAT_FAMILIES 的注释已写明「跨族标签会重复计入，是刻意取舍」——
        #  追踪线要的是「这条主题覆盖了多少作品」，不是互斥分区）。
        if i.get('beat_declared'):
            beat = (i.get('beat') or '').strip()
            if beat in out:
                out[beat].append(i)
            else:
                unclassified.append(i)
            continue
        tags = i.get('highlights') or []
        matched = False
        for name, kws in BEAT_FAMILIES.items():
            if any(any(k in t for k in kws) for t in tags):
                out[name].append(i)
                matched = True
        if not matched:
            unclassified.append(i)
    return out, unclassified


def order_claims(claims, work):
    """把最具代表性的断言排到第一位，其余保持原序。

    卡片只展示第一条。若直接用抽取顺序，会出现标题被拆成指标的碎片
    （实测：「11个人的24小时」被抽成 值="11个" / 标签="人的24小时"）。
    这里用与卷宗一致的相关性打分（标题/标签/摘要 × 标签重合度）来排序。
    """
    if len(claims) < 2:
        return claims
    ctx = ' '.join([work.get('title', ''), work.get('description', ''),
                    ' '.join(work.get('highlights') or [])]).lower()
    ctx_tokens = set(_TOKEN_SPLIT.findall(ctx))
    def score(c):
        lt = set(_TOKEN_SPLIT.findall(str(c.get('label', '')).lower()))
        return (len(lt & ctx_tokens) * 2.0
                + (1.0 if '%' in str(c.get('value', '')) else 0.0)
                - len(str(c.get('label', ''))) * 0.01)
    return sorted(claims, key=lambda c: -score(c))


def compute_dossier(manifest, gate):
    """
    卷宗数据：把「追踪线」从一行计数升级为**可读的叙事 + 已验证断言**。

    每条追踪线 = 一章，按时间排序列出该线的作品，每件挂一条**已过闸门**的
    代表断言（值 + 指标名）。断言带 quote，可回链原文核对。

    为什么只挂一条：卷宗要的是"这条线怎么走的"，不是把所有数字倒出来。
    完整断言集在 manifest.items[].claims 里，供查询层用。

    体积：每条线 ≤ 20 章，每章 3 个短字段 —— 与作品总量线性相关但常数很小。
    """
    items = manifest['research'] + manifest['creative']
    results = gate.scan_works() if gate else {}
    by_file = {i['file']: i for i in items}

    # 追踪线 → 作品（**声明优先**，见 group_by_line）
    line_works, _unclassified = group_by_line(items)

    dossier = []
    for name, works in line_works.items():
        if not works:
            continue
        works = sorted(works, key=lambda i: i['date'])
        claims_n = 0
        chapters = []
        for w in works:
            g = results.get(w['file'])
            l0 = g['l0'] if g else []
            claims_n += len(l0)
            ch = {'file': w['file']}
            if l0:
                ch['v'], ch['l'] = pick_representative(l0, w)
            chapters.append(ch)
        dossier.append({
            'beat': name,
            'works': len(works),
            'claims': claims_n,
            'first': works[0]['date'],
            'last': works[-1]['date'],
            'chapters': chapters,
        })
    dossier.sort(key=lambda d: (-d['claims'], -d['works']))

    cs = manifest.get('claim_stats') or {}
    return {
        'total': cs.get('total', 0),
        'works_covered': cs.get('works_covered', 0),
        'works_total': cs.get('works_total', len(items)),
        'coverage': cs.get('coverage', 0),
        'pending': cs.get('pending', 0),
        'no_structure': cs.get('no_structure', 0),
        'dossier': dossier,
    }


def compute_stats(manifest):
    """
    构建期算好的聚合，尺寸与作品总量无关（约 2-4KB，700 件时仍约 2-4KB）。
    首页只读这些聚合，档案页才读全量列表 —— 这样首页体积与内容量解耦。
    """
    import collections, datetime
    items = manifest['research'] + manifest['creative']
    if not items:
        return {}
    months = sorted({i['date'][:7] for i in items})

    # 月度节奏
    rhythm = [{'month': mm,
               'works': sum(1 for i in items if i['date'][:7] == mm),
               'research': sum(1 for i in manifest['research'] if i['date'][:7] == mm),
               'creative': sum(1 for i in manifest['creative'] if i['date'][:7] == mm)}
              for mm in months]

    # 主责 × 月份矩阵（主责 = agent 字段第一个名字）
    lead_of = lambda i: (i.get('agent') or '未署名').split('+')[0].strip() or '未署名'
    mat = collections.defaultdict(collections.Counter)
    for i in items:
        mat[lead_of(i)][i['date'][:7]] += 1
    agents = sorted(mat, key=lambda a: -sum(mat[a].values()))
    capacity = {'months': months,
                'rows': [{'agent': a,
                          'total': sum(mat[a].values()),
                          'by_month': [mat[a].get(mm, 0) for mm in months]}
                         for a in agents]}

    # 协作图谱：节点=agent（恒定 ~11），边=共现配对（受组合数约束，不随作品量线性增长）
    solo = sum(1 for i in items if '+' not in (i.get('agent') or ''))
    edges = collections.Counter()
    for i in items:
        team = [x.strip() for x in (i.get('agent') or '').split('+') if x.strip()]
        for a, b in itertools.combinations(sorted(team), 2):
            edges[(a, b)] += 1
    collab = {'total': len(items), 'solo': solo, 'joint': len(items) - solo,
              'rate': round((len(items) - solo) / len(items) * 100) if items else 0,
              'edges': [{'a': a, 'b': b, 'works': n} for (a, b), n in edges.most_common(12)]}

    # 追踪线：标签族跨月覆盖 + 断更。**声明优先**（group_by_line）。
    # 未归类的显式进 unclassified，让"新主题出现"可见而不是静默漏掉。
    line_works, unclassified_items = group_by_line(items)
    beats = {}
    for name, hit in line_works.items():
        if not hit:
            continue
        ds = sorted(i['date'] for i in hit)
        last = datetime.date(*map(int, ds[-1].split('-')))
        beats[name] = {'works': len(hit),
                       'months': len({d[:7] for d in ds}),
                       'first': ds[0], 'last': ds[-1],
                       'weeks_idle': (datetime.date.today() - last).days // 7}
    unclassified = Counter()
    for i in unclassified_items:
        beat = (i.get('beat') or '').strip()
        if beat:
            unclassified[f'（声明）{beat}'] += 1
        for t in (i.get('highlights') or []):
            unclassified[t] += 1
    beat_list = sorted(beats.items(), key=lambda kv: (-kv[1]['months'], -kv[1]['works']))

    return {
        'generated': datetime.date.today().isoformat(),
        'span': {'first': min(i['date'] for i in items),
                 'last': max(i['date'] for i in items),
                 'months': len(months)},
        'rhythm': rhythm,
        'capacity': capacity,
        'collab': collab,
        'beats': [{'name': n, **v} for n, v in beat_list],
        'unclassified_tags': [{'tag': t, 'works': n} for t, n in unclassified.most_common(15)],
    }


def main():
    check_only = '--check' in sys.argv

    old_items = load_json(MANIFEST, {'research': [], 'creative': []})
    old_by_file = {i['file']: i for g in ('research', 'creative') for i in old_items.get(g, [])}
    enrich = load_json(ENRICH, {})          # file -> {description, highlights, agent}
    enrich_by_file = {e['file']: e for e in enrich.get('works', [])} if 'works' in enrich else enrich
    TYPE_REGISTRY = load_type_registry()    # 人工类型登记表（stem -> research|creative）

    works = scan_works()
    research, creative, issues = [], [], []

    for rel in works:
        old = old_by_file.get(rel, {})
        date = detect_date(rel, old.get('date'))
        if not date:
            issues.append(f'{rel}: 无法推断日期')
            continue

        e = enrich_by_file.get(rel, {})
        # 类型优先级：人工登记表 autopublish_types.json > enrich.json 显式 type
        # > 目录结构/缩略图名启发式 > 旧 manifest。
        # 登记表用文件名（去扩展名）为键，跨目录搬移不变，
        # 修复"缩略图名依赖类型、类型又依赖缩略图名"的鸡生蛋误分类循环。
        typ = TYPE_REGISTRY.get(os.path.basename(rel)[:-5]) or e.get('type') or detect_type(rel, old.get('type'))
        thumb = resolve_thumb(rel, date, typ)
        # 标题优先级：enrich.json 显式人工标题 > 作品自身 <title> > 旧 manifest。
        # 关键改动：让 HTML <title> 压过旧 manifest —— 首页显示 manifest 标题、
        # 打开页面显示 HTML 标题，两边不一致会很割裂；旧实现「manifest 优先」
        # 导致 HTML 改标题后永久漂移（实测 6 例）。
        html_title = extract_title(os.path.join(ROOT, rel), '')
        title = e.get('title') or html_title or old.get('title') or ''
        if (not e.get('title')) and html_title and old.get('title') and html_title != old['title']:
            issues.append(f'标题以作品 <title> 为准（原 manifest: {old["title"][:34]}）: {rel}')
        # 占位符残留 → 直接判 FAIL（曾出现模板的【】占位标题被原样发布上展）
        for field, val in (('标题', title), ('描述', e.get('description') or old.get('description') or '')):
            if PLACEHOLDER_RE.search(val or ''):
                issues.append(f'{rel}: {field}仍含占位符（{val[:40]}）—— 交付前必须替换')

        item = {
            'id': old.get('id') or f'item-{date}-{typ}-{os.path.basename(rel)[:-5]}',
            'title': title,
            'description': e.get('description') or old.get('description') or '',
            'agent': e.get('agent') or old.get('agent') or '',
            'date': date,
            'type': typ,
            'file': rel,
            'highlights': e.get('highlights') or old.get('highlights') or [],
            'thumb': thumb,
        }
        # 断言层：作品自身声明优先，但**同样要过闸门**（声明不是特权）
        declared = read_declared_claims(os.path.join(ROOT, rel))
        if declared is not None and gate is not None:
            raw = open(os.path.join(ROOT, rel), encoding='utf-8', errors='ignore').read()
            passed = gate.filter_declared(raw, declared)
            item['claims'] = passed
            if len(passed) != len(declared):
                issues.append(f'{rel}: {len(declared)-len(passed)} 条声明断言未过闸门'
                              f'（引用不在原文或标签像句子）')
        elif e.get('claims') is not None:
            item['claims'] = e['claims']
        # 断言排序：**最具代表性的一条排第一** —— 卡片只显示第一条，
        # 顺序不当会出现「11个 / 人的24小时」这种标题碎片当指标展示
        if item.get('claims'):
            item['claims'] = order_claims(item['claims'], item)
        # 追踪线：声明优先，否则按关键词推断 —— **解析后的归属一律写入 item**，
        # 否则 manifest 只记「声明过的」，而 EMBEDDED 记「解析后的」，
        # 同一件作品在两处显示不同归属（实测 manifest 说无、EMBEDDED 说有）。
        beat = read_declared_beat(os.path.join(ROOT, rel))
        if beat:
            item['beat_declared'] = True      # 显式声明 = 权威，单归属
        else:
            for _name, _kws in BEAT_FAMILIES.items():
                if any(any(k in t for k in _kws) for t in (e.get('highlights') or [])):
                    beat = _name
                    break
        if beat:
            item['beat'] = beat              # 解析后归属（卡片主标签，单条）
            # 「待归类」是显式退出（作者知道该篇不属于任何现有线），不是错误；
            # 其他不在封闭集里的名字才是真问题（写错了）。
            if beat not in BEAT_FAMILIES and beat != BEAT_PENDING:
                issues.append(f'{rel}: 追踪线「{beat}」不在封闭集内'
                              f'（首页会归入新线索候选；合法值见 templates/work.html）')
        (research if typ == 'research' else creative).append(item)
        if not thumb:
            issues.append(f'{rel}: 无缩略图（页面将显示无图卡片）')

    research.sort(key=lambda i: i['date'], reverse=True)
    creative.sort(key=lambda i: i['date'], reverse=True)

    # 丢弃 manifest 中已不存在的条目
    found = {i['file'] for i in research + creative}
    for rel in old_by_file:
        if rel not in found and not os.path.exists(os.path.join(ROOT, rel)):
            issues.append(f'manifest 引用了不存在的文件（将移除）: {rel}')

    manifest = {
        'version': '3.0',
        'generatedBy': 'build_manifest.py',
        'total': len(research) + len(creative),
        'researchCount': len(research),
        'creativeCount': len(creative),
        'latestDate': max([i['date'] for i in research + creative] or ['']),
        'research': research,
        'creative': creative,
    }
    # 聚合放 manifest 内（单一生成物、单一契约），而非另开 stats.json
    manifest['stats'] = compute_stats(manifest)
    if gate is not None:
        manifest['claim_stats'] = compute_claim_stats(manifest, gate)
        manifest['stats']['claims'] = compute_dossier(manifest, gate)

    print(f'扫描作品      : {len(works)}')
    print(f'research      : {len(research)}')
    print(f'creative      : {len(creative)}')
    print(f'total         : {manifest["total"]}')
    print(f'latestDate    : {manifest["latestDate"]}')
    tags = Counter(t for i in research + creative for t in i['highlights'])
    print(f'可用标签      : {len(tags)}')
    if issues:
        print(f'\n提示 {len(issues)} 条：')
        for s in issues[:20]:
            print('   -', s)
        if len(issues) > 20:
            print(f'   ... 另有 {len(issues)-20} 条')

    if check_only:
        cur = load_json(MANIFEST, {})
        same = (cur.get('total') == manifest['total']
                and {i['file'] for i in cur.get('research', []) + cur.get('creative', [])} == found)
        print('\n[check] manifest 与磁盘', '一致' if same else '不一致（需运行生成）')
        probs = guardrails(manifest)
        if gate is not None:
            probs += claim_guardrails(manifest, gate)
        for g in probs:
            print('   ✗', g)
        return 0 if (same and not probs) else 1

    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f'\n已写入 {MANIFEST}')
    sync_embedded(manifest)
    # 写盘+同步之后再校验，报告才是本次落盘的真实状态
    probs = guardrails(manifest)
    if gate is not None:
        probs += claim_guardrails(manifest, gate)
    for g in probs:
        print('   ✗ 落盘后仍有问题:', g)
    return 0 if not probs else 1


if __name__ == '__main__':
    sys.exit(main())
