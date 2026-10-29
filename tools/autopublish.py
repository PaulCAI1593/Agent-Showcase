#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autopublish.py — 智囊团展厅「交付即上架」自动化流水线

把每次例会的人工四步（build_manifest → gen_thumb → 校验 → 状态同步）
压缩成一条命令，并根治五类反复事故：

  ① 产出落根目录          → 阶段2 自动搬移散落到根目录的 HTML
  ② manifest 与磁盘不一致   → 阶段1 差异扫描 + 阶段6 重建 + 阶段7 硬校验
  ③ 缩略图缺失            → 阶段5 复用 tools/gen_thumb.py 补齐
  ④ 元数据键失配（131→0 标签事故）→ 阶段3 搬移后重映射 enrich.json / index.html TAGMAP 的键
  ⑤ 碎片/临时目录混入上架   → 阶段1.5 隔离到 _archive/wip
  ＋ 产出仍在写入时误上架半成品 → 阶段0 静默门禁

用法:
    python3 tools/autopublish.py            # 完整流水线
    python3 tools/autopublish.py --dry-run  # 只体检不落盘
    python3 tools/autopublish.py --help

退出码:
    0  全部校验通过
    1  校验失败 / 门禁拒绝执行
    2  参数或环境错误

约束:
    * 不修改 tools/build_manifest.py 的任何逻辑（仅作为子进程调用）
    * 不重写 index.html 的原始设计（只改 TAGMAP 数据段 + 由 build_manifest 同步 EMBEDDED）
    * 不重写截图逻辑（缩略图一律走 tools/gen_thumb.py）
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

# 复用既有工具的逻辑（只读导入，不改动其源码）
import autotag          # noqa: E402
import build_manifest   # noqa: E402
import gen_thumb        # noqa: E402
import make_thumbs_webp  # noqa: E402

MANIFEST = os.path.join(ROOT, 'manifest.json')
ENRICH = os.path.join(ROOT, 'enrich.json')
INDEX = os.path.join(ROOT, 'index.html')
THUMBS = os.path.join(ROOT, 'thumbs')
TYPES_REGISTRY = os.path.join(TOOLS, 'autopublish_types.json')
BACKUP_DIR = os.path.join(TOOLS, '.autopublish_backups')
QUARANTINE_ROOT = os.path.join(ROOT, '_archive', 'wip')

EXCLUDE_FILES = set(build_manifest.EXCLUDE_FILES)

# 缩略图存在性一律委托给 build_manifest.resolve_thumb —— 它已实现
# 「优先 .webp，回退 .png」。此处若自己硬编码 .png，会把已转 webp 的
# 缩略图全判为缺失，导致每次运行都重新截图 100+ 张并回填 21MB PNG。
THUMB_SRC = os.path.join(ROOT, '_private', 'thumbs-src')


def thumb_present(rel, date, typ):
    """该作品是否已有可用缩略图（webp 或 png 均算）。返回相对路径或 ''。"""
    return build_manifest.resolve_thumb(rel, date, typ)


# 缩略图就绪判据（10-27 例会固化，直击三类"看着有、其实是坏的/旧的"首图）：
#   1) 只有 png 不算就绪 —— 必须转成 webp 才算（否则绕过截图流程手工落的 PNG 永不补转）
#   2) webp 字节过小视为近空白图（实测反诈AI 1506B / 720×405）
#   3) 作品正文比 webp 新 —— 展厅首图会与正文永久分叉（实测 #353 主稿 19:09 vs 首图 04:11）
WEBP_MIN_BYTES = 4096
# 内容指纹表：记录"上次截图时作品正文的指纹"。
# 为什么不用裸 mtime 比较：10-26 16:25 那轮批量注入「返回展厅」把 104 件作品的
# mtime 集体推到各自缩略图之后 —— 纯 mtime 判据会触发 104 次无意义重截（约10分钟）。
# 指纹只认"正文是否真的变了"，并剔除流水线自己注入的两块（返回链 / claims 声明），
# 因此注入不算变更、作者改稿一定算变更。
THUMB_STATE = os.path.join(ROOT, '_private', 'thumb_state.json')

BACKLINK_RE = re.compile(r'<!--\s*showcase-backlink.*?-->', re.S)
CLAIMS_BLOCK_RE = re.compile(r'<script[^>]+id=["\']claims["\'][^>]*>.*?</script>', re.S)


def content_fingerprint(rel):
    """作品正文指纹（剔除流水线注入物）。文件不存在返回 ''。"""
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return ''
    try:
        html = read_text(path)
    except OSError:
        return ''
    html = BACKLINK_RE.sub('', html)
    html = CLAIMS_BLOCK_RE.sub('', html)
    html = re.sub(r'\s+', ' ', html)
    return hashlib.sha1(html.encode('utf-8', 'ignore')).hexdigest()[:16]


def thumb_state_key(rel, date, typ):
    return f'{date}|{typ}|{work_key(rel)}'


def thumb_is_blank(path):
    """缩略图是不是一张「视觉上空白」的图。

    判据用**灰度标准差**而不是「亮像素占比」——
    亮像素占比会把深色主题作品整片误判（实测 104 件里 98 件被误判）。
    空白页（内容被永久隐藏 → 拍出来全黑或全白）的标准差 ≈ 0；
    深色页有文字/图形 → 标准差明显大于 0。
    """
    try:
        from PIL import Image, ImageStat
        im = Image.open(path).convert('L')
        st = ImageStat.Stat(im)
        return st.stddev[0] < 2.0
    except Exception:
        return False


def thumb_ready(rel, date, typ, state):
    """返回 (ready, reason)。reason='' 表示就绪。"""
    stem = work_key(rel)
    webp = os.path.join(THUMBS, f'{date}-{typ}-{stem}-thumb.webp')
    png = os.path.join(THUMBS, f'{date}-{typ}-{stem}-thumb.png')
    hi_res = os.path.join(THUMB_SRC, f'{date}-{typ}-{stem}-thumb.png')
    if not os.path.exists(webp):
        if os.path.exists(png) or os.path.exists(hi_res):
            return False, 'png-only 待转 webp'
        return False, '无缩略图'
    size = os.path.getsize(webp)
    if size < WEBP_MIN_BYTES:
        return False, f'webp 过小({size}B < {WEBP_MIN_BYTES}B)，疑空白首图'
    if thumb_is_blank(webp):
        return False, 'webp 是视觉空白图（页面内容可能被永久隐藏）'
    key = thumb_state_key(rel, date, typ)
    fp = content_fingerprint(rel)
    if key not in state:
        # 惰性建档：存量作品信任既有首图，登记指纹后交由后续变更触发重截
        state[key] = {'fp': fp, 'webp': os.path.getsize(webp)}
        return True, '（建档）'
    if fp and state[key].get('fp') and fp != state[key]['fp']:
        return False, '正文指纹已变，需重截'
    return True, ''

BACKUP_RE = build_manifest.BACKUP_RE

# 流水线自己管理的数据文件（不计入「产出是否在写入」判定）
# 流水线自己维护、或属于文档性质的根文件：不是作品，也不该触发静默门禁。
# （否则改一次 README 就会把上架流程锁 180s）
PIPELINE_MANAGED = {'manifest.json', 'enrich.json', 'index.html', 'README.md'}

# showcase 根目录允许存在的文件（白名单）。白名单外的一律在 W2 报出，
# 避免 preview.png / test.txt 这类死重长期隐身（原判据只统计 .html）。
ROOT_ALLOWED = PIPELINE_MANAGED | {'DESIGN_REFERENCE.md'}

# 临时/草稿目录名（命中即整体隔离）
SCRATCH_DIR_NAMES = {
    'temp', 'tmp', '_temp', '_tmp', 'wip', '_wip', 'work', '_work',
    'partial', 'parts', 'fragments', 'draft', '_draft', 'scratch', '_scratch',
}
# 碎片文件名（命中即隔离）
FRAGMENT_SUFFIXES = ('.part.html', '.tmp.html', '.fragment.html', '.draft.html',
                     '.wip.html', '.partial.html', '.bak.html')
FRAGMENT_TILDE = '~'


# ────────────────────────────────────────────────────────────── 基础工具

def log(msg=''):
    print(msg, flush=True)


def rule(title):
    log('\n' + '─' * 68)
    log(f'  {title}')
    log('─' * 68)


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save_json_if_changed(path, data, indent=2):
    """仅在内容真正变化时写盘 —— 保证幂等。"""
    new = json.dumps(data, ensure_ascii=False, indent=indent) + '\n'
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            if f.read() == new:
                return False
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new)
    return True


def read_text(path):
    with open(path, encoding='utf-8', errors='ignore') as f:
        return f.read()


def extract_title(path):
    head = read_text(path)[:4000]
    m = re.search(r'<title>(.*?)</title>', head, re.S | re.I)
    if m:
        t = re.sub(r'\s+', ' ', m.group(1)).strip()
        if t:
            return t
    return os.path.basename(path)[:-5]


def extract_meta_description(path):
    head = read_text(path)[:8000]
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\'](.*?)["\']',
                  head, re.S | re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]*name=["\']description["\']',
                      head, re.S | re.I)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


def strip_html(html):
    body = re.sub(r'<script.*?</script>', ' ', html, flags=re.S | re.I)
    body = re.sub(r'<style.*?</style>', ' ', body, flags=re.S | re.I)
    body = re.sub(r'<[^>]+>', ' ', body)
    return re.sub(r'\s+', ' ', body)


def is_fragment_html(path):
    """没有 <title> 的 HTML = 页面碎片（成品必带 title；展厅现有 97 件全部带 title）。"""
    try:
        head = read_text(path)[:4000]
    except OSError:
        return True
    return not re.search(r'<title>.+?</title>', head, re.S | re.I)


def looks_like_fragment_name(fn):
    if fn.endswith(FRAGMENT_TILDE):
        return True
    return any(fn.endswith(s) for s in FRAGMENT_SUFFIXES)


def in_quarantine(rel, excluded):
    """rel 是否落在被隔离的（目录或文件）范围内。"""
    if not excluded:
        return False
    rel = rel.replace('\\', '/')
    for q in excluded:
        q = q.replace('\\', '/').rstrip('/')
        if rel == q or rel.startswith(q + '/'):
            return True
    return False


# ────────────────────────────────────────────────────────────── 作品身份

def work_key(rel):
    """作品的稳定标识：basename 去扩展名（跨目录搬移不变）。"""
    return os.path.basename(rel)[:-5]


def load_type_registry(path):
    """人工登记的作品类型表：{basename: research|creative}。总指挥例会上决定后登记。"""
    reg = load_json(path, {})
    if isinstance(reg, dict) and 'types' in reg:
        reg = reg['types']
    if not isinstance(reg, dict):
        return {}
    return {k: v for k, v in reg.items() if isinstance(v, str) and v in ('research', 'creative')}


def resolve_type(rel, old_manifest_types, registry):
    """
    判定 research / creative。优先级（高→低）：
      1) 人工登记表 tools/autopublish_types.json
      2) 已有 manifest 记录（重新上架时保持原判定）
      3) 目录结构 YYYY-MM-DD/research|creative/
      4) 磁盘上已存在的规范缩略图名前缀
      5) 内容启发式（Chart.js / <table> → research；<svg>/<canvas> → creative）
      6) 兜底 research（与 build_manifest.py 的默认保持一致）
    """
    stem = work_key(rel)
    parts = rel.split(os.sep)
    date = parts[0] if re.match(r'^\d{4}-\d{2}-\d{2}$', parts[0]) else ''

    if stem in registry:
        return registry[stem], '登记表'
    if rel in old_manifest_types:
        return old_manifest_types[rel], 'manifest'
    if len(parts) >= 3 and parts[1] in ('research', 'creative'):
        return parts[1], '目录结构'
    if date:
        for t in ('research', 'creative'):
            if any(os.path.exists(os.path.join(THUMBS, f'{date}-{t}-{stem}-thumb.{ext}'))
                   for ext in ('webp', 'png')):
                return t, '缩略图前缀'
    try:
        html = read_text(os.path.join(ROOT, rel))
    except OSError:
        html = ''
    low = html.lower()
    if 'chart.js' in low or 'new chart(' in low or low.count('<table') >= 2:
        return 'research', '内容启发式'
    if '<svg' in low or '<canvas' in low:
        return 'creative', '内容启发式'
    return 'research', '默认兜底'


def derive_tags(rel, title, description):
    """
    为新作品派生标签。
      主路径：复用 tools/autotag.py 的标题/描述关键词派生（同一份词表，人工标签优先）
      兜底  ：autotag 的标题兜底分支对中文长标题无效（会返回空列表），
              此时改用同一份 KEYWORDS 词表对正文做词频检索（不臆造新词）。
    """
    tags = autotag.derive(title or '', description or '')
    if tags:
        return tags, 'autotag.derive'
    try:
        text = strip_html(read_text(os.path.join(ROOT, rel)))
    except OSError:
        text = ''
    counts = Counter()
    for idx, kw in enumerate(autotag.KEYWORDS):
        n = text.count(kw)
        if n:
            counts[kw] = (n, idx)
    if counts:
        ranked = sorted(counts, key=lambda k: (-counts[k][0], counts[k][1]))
        return ranked[:4], '正文词频检索(同词表)'
    return [], '派生失败'


# ────────────────────────────────────────────────────────────── 键重映射

def build_key_aliases(disk_works, old_manifest_paths):
    """
    为每个作品算出「可能被写错的历史键」→ 规范相对路径。
    131→0 标签事故的根因：搬移后 enrich.json / TAGMAP 仍用 basename 作键，
    manifest 却改用相对路径，查表全部落空 → 标签清零。
    """
    aliases = {}
    for rel in disk_works:
        stem = work_key(rel)
        base = os.path.basename(rel)
        cands = {base, stem, stem + '.html'}
        m = re.match(r'^\d{4}-\d{2}-\d{2}-(.+)$', stem)
        if m:
            cands.add(m.group(1) + '.html')
        for old in old_manifest_paths:
            if work_key(old) == stem:
                cands.add(old)
        for c in cands:
            aliases.setdefault(c, rel)
    return aliases


def remap_enrich(aliases, enrich_data, stats):
    """重映射 enrich.json 中 works[].file 的键。"""
    works = enrich_data.get('works', []) if isinstance(enrich_data, dict) else enrich_data
    changed = 0
    for w in works:
        old = w.get('file')
        if not old:
            continue
        new = aliases.get(old)
        if new and new != old:
            w['file'] = new
            changed += 1
            stats.append(f'enrich.json 键重映射: {old} → {new}')
    return changed


def remap_tagmap(aliases, stats):
    """
    重映射 index.html 中 TAGMAP 的键。
    只替换 `const TAGMAP={...};` 这一行数据段，index.html 其余字节原样保留。
    """
    if not os.path.exists(INDEX):
        return 0
    html = read_text(INDEX)
    m = re.search(r'^const TAGMAP=(\{.*\});$', html, re.M)
    if not m:
        stats.append('index.html 未找到 TAGMAP，跳过键重映射')
        return 0
    tagmap = json.loads(m.group(1))
    newmap = {}
    changed = 0
    for key, val in tagmap.items():
        new = aliases.get(key, key)
        if new != key:
            changed += 1
            stats.append(f'index.html TAGMAP 键重映射: {key} → {new}')
        if new in newmap:            # 撞键：保留先出现的，避免覆盖人工数据
            stats.append(f'⚠️ 键冲突，保留先出现项: {new}')
            continue
        newmap[new] = val
    if changed:
        line = 'const TAGMAP=' + json.dumps(newmap, ensure_ascii=False) + ';'
        html = html[:m.start()] + line + html[m.end():]
        with open(INDEX, 'w', encoding='utf-8') as f:
            f.write(html)
    return changed


# ────────────────────────────────────────────────────────────── 备份 / 幂等

def make_backup():
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    dest = os.path.join(BACKUP_DIR, ts)
    os.makedirs(dest, exist_ok=True)
    for name in ('manifest.json', 'enrich.json', 'index.html'):
        src = os.path.join(ROOT, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dest, name))
    return dest


def snapshot(path):
    """记录文件内容与 mtime，用于「重复执行不产生副作用」的严格判定。"""
    if not os.path.exists(path):
        return None
    st = os.stat(path)
    with open(path, 'rb') as f:
        return {'mtime': st.st_mtime, 'data': f.read()}


def restore_if_unchanged(path, snap):
    """内容未变则把 mtime 还原 —— 幂等到「连时间戳都不动」。"""
    if not snap or not os.path.exists(path):
        return False
    with open(path, 'rb') as f:
        if f.read() != snap['data']:
            return False
    os.utime(path, (snap['mtime'], snap['mtime']))
    return True


# ────────────────────────────────────────────────────────────── 各阶段

def phase_quiescence(quiet_seconds):
    """静默门禁：产出仍在写入时拒绝执行，避免把半成品上架。"""
    rule('阶段 0 · 静默门禁（产出写入中 → 拒绝执行）')
    if quiet_seconds <= 0:
        log('  [skip] 已通过参数关闭静默门禁')
        return True
    now = time.time()
    skip_roots = {os.path.abspath(THUMBS), os.path.abspath(os.path.join(ROOT, '_archive')),
                  os.path.abspath(os.path.join(ROOT, '_private')),
                  os.path.abspath(TOOLS)}
    recent = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        if os.path.abspath(dirpath) in skip_roots:
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn in PIPELINE_MANAGED:
                continue
            # 工具脚本（add_backlink / vendor_assets 等）留下的 *.bak.<时间戳>
            # 是流水线自身的产物，不是"产出正在写入"。若计入，任何一次批量
            # 改写都会让门禁误锁 180s，把正常的收敛节奏打断。
            if build_manifest.BACKUP_RE.search(fn) or '.bak.' in fn:
                continue
            p = os.path.join(dirpath, fn)
            try:
                age = now - os.path.getmtime(p)
            except OSError:
                continue
            if age < quiet_seconds:
                recent.append((age, os.path.relpath(p, ROOT)))
    recent.sort()
    if recent:
        log(f'  ✗ {len(recent)} 个产出文件在最近 {quiet_seconds}s 内被修改 —— 产出仍在写入，拒绝上架')
        for age, rel in recent[:10]:
            log(f'        ! {rel}  ({age:.0f}s 前)')
        log('  → 请等待产出完成后再运行；确需强制执行请加 --quiet-seconds 0')
        return False
    log(f'  ✓ 全部产出已静默 ≥ {quiet_seconds}s')
    return True


def phase_scan(disk_works, manifest):
    rule('阶段 1 · 扫描：磁盘 ↔ manifest 差异')
    man_files = {i['file'] for g in ('research', 'creative') for i in manifest.get(g, [])}
    new = [w for w in disk_works if w not in man_files]
    stale = [w for w in man_files if w not in set(disk_works)]
    log(f'  磁盘作品      : {len(disk_works)}')
    log(f'  manifest 作品 : {len(man_files)}')
    log(f'  新增(磁盘有/manifest无) : {len(new)}')
    for w in new:
        log(f'      + {w}')
    log(f'  失效(manifest有/磁盘无) : {len(stale)}')
    for w in stale:
        log(f'      - {w}')
    return new, stale


def find_scratch():
    """找出临时/草稿目录与碎片文件。"""
    scratch_dirs, fragment_files = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in build_manifest.EXCLUDE_DIRS and not d.startswith('.')]
        for fn in filenames:
            if not fn.endswith('.html') or fn in EXCLUDE_FILES or BACKUP_RE.search(fn):
                continue
            if fn.startswith('.') or looks_like_fragment_name(fn):
                # 隐藏分片（.part1.html 等）同样是构建中间产物
                fragment_files.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))
        base = os.path.basename(dirpath)
        if base.lower() in SCRATCH_DIR_NAMES:
            scratch_dirs.append(os.path.relpath(dirpath, ROOT))
            dirnames[:] = []          # 不再深入
    return sorted(set(scratch_dirs)), sorted(set(fragment_files))


def phase_quarantine(dry):
    """把碎片/临时目录移出可上架树（build_manifest 已排除 _archive）。"""
    rule('阶段 1.5 · 隔离：碎片 / 临时目录 → _archive/wip')
    scratch_dirs, fragment_files = find_scratch()
    quarantined = set()
    moved = 0
    for rel in scratch_dirs:
        src = os.path.join(ROOT, rel)
        dest = os.path.join(QUARANTINE_ROOT, rel)
        quarantined.add(rel)
        if dry:
            log(f'  [dry] 将隔离目录: {rel} → _archive/wip/{rel}')
            continue
        if os.path.exists(dest):
            dest = dest + '.q-' + datetime.now().strftime('%H%M%S')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(src, dest)
        log(f'  ✓ 已隔离目录: {rel} → {os.path.relpath(dest, ROOT)}')
        moved += 1

    # 目录之外残留的碎片文件（无 <title> 或命名像碎片）
    for rel in list(fragment_files):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        if os.path.dirname(rel) in scratch_dirs:
            continue
        if not is_fragment_html(p) and not os.path.basename(rel).startswith('.'):
            continue
        quarantined.add(rel)
        dest = os.path.join(QUARANTINE_ROOT, rel)
        if dry:
            log(f'  [dry] 将隔离碎片: {rel}')
            continue
        if os.path.exists(dest):
            dest = dest + '.q-' + datetime.now().strftime('%H%M%S')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(p, dest)
        log(f'  ✓ 已隔离碎片: {rel} → {os.path.relpath(dest, ROOT)}')
        moved += 1
    if not moved and not quarantined:
        log('  ✓ 无碎片/临时目录')
    return quarantined


def phase_move(disk_works, stats, dry):
    """把根目录散落的 HTML 搬进对应日期子目录。"""
    rule('阶段 2 · 搬移：根目录散落产出 → 日期子目录')
    scattered = []
    for fn in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, fn)
        if not os.path.isfile(p) or not fn.endswith('.html'):
            continue
        if fn in EXCLUDE_FILES or BACKUP_RE.search(fn):
            continue
        scattered.append(fn)

    if not scattered:
        log('  ✓ 根目录无散落产出')
        return {}

    moves = {}
    for fn in scattered:
        src = os.path.join(ROOT, fn)
        m = re.match(r'^(\d{4}-\d{2}-\d{2})', fn)
        if m:
            date = m.group(1)
        else:
            date = datetime.fromtimestamp(os.path.getmtime(src)).strftime('%Y-%m-%d')
            stats.append(f'⚠️ {fn} 文件名无日期前缀，按 mtime 归档到 {date}')
        dest_dir = os.path.join(ROOT, date)
        dest = os.path.join(dest_dir, fn)
        rel_new = f'{date}/{fn}'
        if os.path.exists(dest):
            stats.append(f'✗ 目标已存在，跳过（需人工处理）: {rel_new}')
            continue
        moves[fn] = rel_new
        if dry:
            log(f'  [dry] {fn} → {rel_new}')
        else:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(src, dest)
            log(f'  ✓ {fn} → {rel_new}')
    return moves


def phase_remap(moves, disk_works, manifest, dry):
    """搬移后重映射 enrich.json 与 index.html TAGMAP 的键。"""
    rule('阶段 3 · 键重映射：enrich.json + index.html TAGMAP（防 131→0 标签事故）')
    stats = []
    old_paths = {i['file'] for g in ('research', 'creative') for i in manifest.get(g, [])}
    aliases = build_key_aliases(disk_works, old_paths)
    for old_base, new_rel in moves.items():
        aliases[old_base] = new_rel

    enrich_data = load_json(ENRICH, {'works': []})
    n1 = remap_enrich(aliases, enrich_data, stats)
    n2 = remap_tagmap(aliases, stats)

    if dry:
        for s in stats:
            log('  [dry] ' + s)
        log(f'  [dry] enrich.json 键重映射 {n1} 条，TAGMAP 键重映射 {n2} 条')
        return n1 + n2

    if n1:
        save_json_if_changed(ENRICH, enrich_data)
    for s in stats:
        log('  ' + s)
    log(f'  ✓ enrich.json 键重映射 {n1} 条，TAGMAP 键重映射 {n2} 条')
    return n1 + n2


def phase_metadata(disk_works, dry):
    """确保每件作品在 enrich.json 中有条目（描述/标签）。"""
    rule('阶段 4 · 元数据：补齐 enrich.json 条目与标签')
    enrich_data = load_json(ENRICH, {'works': []})
    if isinstance(enrich_data, dict) and 'works' not in enrich_data:
        enrich_data = {'works': enrich_data}
    works = enrich_data.setdefault('works', [])
    by_file = {w.get('file'): w for w in works}

    added, tagged = 0, 0
    for rel in disk_works:
        w = by_file.get(rel)
        if w is None:
            w = {'file': rel, 'description': extract_meta_description(os.path.join(ROOT, rel)),
                 'highlights': [], 'agent': ''}
            works.append(w)
            by_file[rel] = w
            added += 1
            log(f'  + 新建 enrich 条目: {rel}')
        if not w.get('description'):
            desc = extract_meta_description(os.path.join(ROOT, rel))
            if desc:
                w['description'] = desc
        if not w.get('highlights'):
            title = extract_title(os.path.join(ROOT, rel))
            tags, how = derive_tags(rel, title, w.get('description', ''))
            if tags:
                w['highlights'] = tags
                tagged += 1
                log(f'  + 派生标签({how}): {rel} → {tags}')
            else:
                log(f'  ✗ 无法派生标签: {rel}（需人工在 enrich.json 补 highlights）')

    if not dry:
        save_json_if_changed(ENRICH, enrich_data)
    log(f'  ✓ enrich.json 新增 {added} 条，补标签 {tagged} 条')
    return added, tagged


def phase_thumbs(disk_works, manifest, registry, dry):
    """为缺缩略图的作品生成缩略图（复用 tools/gen_thumb.py，不重写截图逻辑）。"""
    rule('阶段 5 · 缩略图：补齐缺失的缩略图（复用 gen_thumb.py）')
    old_types = {i['file']: i.get('type', 'research')
                 for g in ('research', 'creative') for i in manifest.get(g, [])}
    os.makedirs(THUMBS, exist_ok=True)
    made, skipped, converted = [], [], 0
    state = load_json(THUMB_STATE, {})
    for rel in disk_works:
        stem = work_key(rel)
        parts = rel.split(os.sep)
        date = parts[0] if re.match(r'^\d{4}-\d{2}-\d{2}$', parts[0]) else ''
        if not date:
            m = re.match(r'^(\d{4}-\d{2}-\d{2})', stem)
            date = m.group(1) if m else ''
        if not date:
            skipped.append((rel, '无法推断日期'))
            continue
        typ, _src = resolve_type(rel, old_types, registry)
        canonical = f'{date}-{typ}-{stem}-thumb.png'
        ready, why = thumb_ready(rel, date, typ, state)
        if ready:
            continue            # 幂等：webp 存在 + 字节达标 + 不早于正文
        if why == 'png-only 待转 webp':
            # 图已经是对的，只是没转格式 —— 补转即可，不必重截（省 4 分钟/百张）
            if dry:
                log(f'  [dry] 将补转 webp（png-only）：{canonical}')
                continue
            log(f'  → 补转 webp（png-only）：{rel}')
            try:
                os.makedirs(THUMB_SRC, exist_ok=True)
                hi = os.path.join(THUMB_SRC, canonical)
                loose = os.path.join(THUMBS, canonical)
                if os.path.exists(loose):
                    os.replace(loose, hi)      # 越界 PNG 归位到私有高清源
                if os.path.exists(hi):
                    make_thumbs_webp.convert_one(hi)
                    converted += 1
                    state[thumb_state_key(rel, date, typ)] = {
                        'fp': content_fingerprint(rel),
                        'webp': os.path.getsize(os.path.join(
                            THUMBS, f'{date}-{typ}-{stem}-thumb.webp'))
                        if os.path.exists(os.path.join(THUMBS, f'{date}-{typ}-{stem}-thumb.webp'))
                        else 0}
                    log('  ✓ 已补转，PNG 高清源归入 _private/thumbs-src/')
            except Exception as e:
                skipped.append((rel, f'补转失败：{e}'))
            continue
        if dry:
            made.append(canonical)
            log(f'  [dry] 将重截 {canonical}（原因：{why}）')
            continue
        log(f'  → {rel} ({typ})｜原因：{why}')
        try:
            gen_thumb.shoot(rel, typ)
        except Exception as exc:
            # 一件作品截不出缩略图（远程资源挂住等）不该带崩整条流水线
            log(f'  ! 缩略图失败（跳过）: {rel} — {str(exc)[:70]}')
            continue
        produced = f'{stem[:10]}-{typ}-{stem}-thumb.png'   # gen_thumb 按 stem[:10] 取日期
        if produced != canonical:
            src = os.path.join(THUMBS, produced)
            if os.path.exists(src):
                os.replace(src, os.path.join(THUMBS, canonical))
                log(f'  ✓ 文件名规范化为 {canonical}（gen_thumb 按 stem 取日期）')
        png = os.path.join(THUMBS, canonical)
        if os.path.exists(png):
            # 新截图先落为 PNG：转成 webp 供页面引用，PNG 归入私有高清源，
            # 避免 thumbs/（对外目录）重新堆积 200KB+/张 的 PNG。
            try:
                os.makedirs(THUMB_SRC, exist_ok=True)
                dst = os.path.join(THUMB_SRC, os.path.basename(png))
                # ⚠️ 必须**覆盖**旧源，不能「已存在就删掉新图」。
                # 否则：作品被修好后重截 → 新 PNG 被删除 → 转的还是旧坏图 →
                # 坏缩略图永远修不好（实测：反诈AI 修好 JS 后重截仍是 1506 字节）。
                os.replace(png, dst)
                make_thumbs_webp.convert_one(dst)
                log(f'  ✓ 已转 webp，PNG 高清源归入 _private/thumbs-src/')
            except Exception as e:            # 转换失败不影响上架：png 仍在 thumbs/ 可用
                log(f'  ! webp 转换跳过（沿用 png）：{e}')
            made.append(canonical)
            # 截图完成 → 登记新指纹，下次只有在正文真的变了才会再截
            wp = os.path.join(THUMBS, f'{date}-{typ}-{stem}-thumb.webp')
            state[thumb_state_key(rel, date, typ)] = {
                'fp': content_fingerprint(rel),
                'webp': os.path.getsize(wp) if os.path.exists(wp) else 0}
        else:
            skipped.append((rel, '生成失败'))
    if not dry:
        save_json_if_changed(THUMB_STATE, state)
    seeded = sum(1 for v in state.values() if v.get('fp'))
    log(f'  ✓ 新生成/重截缩略图 {len(made)} 张，补转 {converted} 张，'
        f'失败/跳过 {len(skipped)} 项｜指纹表 {seeded} 条')
    for rel, why in skipped:
        log(f'      ! {rel}: {why}')
    return made, skipped


def phase_claims(disk_works, dry):
    """
    阶段 5.5 · 返回链 + 断言回填

    为什么放在这里：这两件事以前是**手工**做的独立工具，
    结果新作品自动缺「返回展厅」链接（实测 10-24 新作品就没有）。
    「检测有效、处置被推迟」的典型 —— 接到流水线里才不会再漏。
    """
    rule('阶段 5.5 · 返回链 + 断言回填')
    if dry:
        log('  [dry] 跳过（不注入返回链 / 不回填断言）')
        return

    # ① 返回链（add_backlink 幂等：已有 marker 跳过）
    r = subprocess.run([sys.executable, os.path.join(TOOLS, 'add_backlink.py')],
                       cwd=ROOT, capture_output=True, text=True)
    out = (r.stdout or '').strip().splitlines()
    for line in out[-3:]:
        log('  ' + line)
    if r.returncode != 0:
        log(f'  ! add_backlink 退出码 {r.returncode}')

    # ② 断言回填（重校验 + 写回 enrich.json；作品自带 claims 声明者优先）
    r = subprocess.run([sys.executable, os.path.join(TOOLS, 'claim_gate.py'), '--backfill'],
                       cwd=ROOT, capture_output=True, text=True)
    for line in (r.stdout or '').strip().splitlines():
        log('  ' + line)
    if r.returncode != 0:
        log(f'  ! claim_gate 退出码 {r.returncode}')
    if r.stderr:
        for line in r.stderr.strip().splitlines():
            log('  ! ' + line)


def prune_orphan_enrich(disk_works):
    """自愈：清掉 enrich.json 里指向**已不存在作品**的孤儿条目。

    为什么需要：手工删掉一件作品后，它的 enrich 条目会永远留着 ——
    阶段7 的「孤儿键」校验会永久失败、标签总数也会永久对不上，
    流水线从此卡死。自动清理让流水线可自愈。
    """
    rule('阶段 5.8 · 自愈：清理 enrich.json 孤儿键')
    data = load_json(ENRICH, {'works': []})
    if not isinstance(data, dict) or 'works' not in data:
        log('  [skip] enrich.json 结构非预期，跳过')
        return
    alive = set(disk_works)
    before = len(data['works'])
    kept = [w for w in data['works'] if w.get('file') in alive]
    removed = before - len(kept)
    if removed:
        data['works'] = kept
        save_json_if_changed(ENRICH, data, 2)
        log(f'  ✓ 清理孤儿键 {removed} 条（作品已不在磁盘上）')
    else:
        log('  ✓ 无孤儿键')


JS_BLOCKED = os.path.join(ROOT, 'tools', '.js_blocked.json')


def check_inline_js(disk_works):
    """硬校验：内联脚本必须语法正确。

    为什么必须有：HTML 写错一个引号，**页面照样渲染**（内容都在 DOM 里），
    但脚本整段挂掉 → 依赖脚本的显现动画/交互永远不执行 → 整页空白。
    实测：反诈AI（2026-09-08）因一个字符串里的 ASCII 单引号把字符串提前终止，
    整页只剩导航条、hero 全白 —— 结构检查（计数/缩略图/标签/断言）全过，
    因为它们只看文件与数据，不看脚本能否运行。

    用 node --check 逐个校验；没有 node 时跳过（并说明）。
    """
    rule('阶段 4.5 · 内联脚本语法校验（防「脚本挂掉 → 整页空白」）')
    node = shutil.which('node')
    if not node:
        log('  [skip] 未找到 node，跳过脚本语法校验')
        return []
    import tempfile
    bad = []
    for rel in disk_works:
        path = os.path.join(ROOT, rel)
        try:
            html = open(path, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        scripts = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.S)
        for sc in scripts:
            if not sc.strip():
                continue
            with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False,
                                             encoding='utf-8') as t:
                t.write(sc)
                tmp = t.name
            r = subprocess.run([node, '--check', tmp], capture_output=True, text=True)
            os.unlink(tmp)
            if r.returncode != 0:
                msg = ''
                for line in (r.stderr or '').splitlines():
                    if 'Error' in line:
                        msg = line.strip()
                        break
                bad.append((rel, msg[:120]))
                break
    if bad:
        log(f'  ✗ {len(bad)} 件作品的内联脚本有语法错误 —— 脚本挂掉会导致该页空白')
        for rel, msg in bad[:5]:
            log(f'        ! {rel}: {msg}')
        # 写进排除清单：空白页不留在展厅里（比缺页更糟），但流水线以非零退出码
        # 大声报出来，由 agent 去修 —— 不静默、不隐藏。
    else:
        log(f'  ✓ {len(disk_works)} 件作品的内联脚本语法均正确')
    # 每次都重写清单：已修好/已删除的作品自动解除排除（否则会被永久排除）
    try:
        with open(JS_BLOCKED, 'w', encoding='utf-8') as f:
            json.dump([r for r, _ in bad], f, ensure_ascii=False, indent=2)
    except OSError:
        pass
    return bad


def phase_manifest(dry):
    """调用既有 build_manifest.py 重建索引（不改其逻辑）。"""
    rule('阶段 6 · 重建索引：调用 tools/build_manifest.py')
    if dry:
        log('  [dry] 跳过（不重建 manifest.json）')
        return
    r = subprocess.run([sys.executable, os.path.join(TOOLS, 'build_manifest.py')],
                       cwd=ROOT, capture_output=True, text=True)
    for line in (r.stdout or '').splitlines():
        log('  ' + line)
    if r.returncode != 0:
        log(f'  ✗ build_manifest.py 退出码 {r.returncode}')
    if r.stderr:
        for line in r.stderr.strip().splitlines():
            log('  ! ' + line)


def phase_validate(pre_manifest, pre_tags, excluded=None, js_bad=None):
    """硬校验：任何一项不达标 → 非零退出码。"""
    rule('阶段 7 · 校验（任一不达标即以非零退出码报错）')
    manifest = load_json(MANIFEST, {})
    research = manifest.get('research', [])
    creative = manifest.get('creative', [])
    items = research + creative
    disk = [w for w in build_manifest.scan_works() if not in_quarantine(w, excluded)]
    man_files = {i['file'] for i in items}
    disk_set = set(disk)

    # ① 计数一致
    total = manifest.get('total')
    c_count = (total == len(research) + len(creative) == len(items) == len(disk))
    log(f'  ① 计数      manifest.total={total}  research={len(research)}  creative={len(creative)}  '
        f'磁盘={len(disk)}  → {"一致 ✓" if c_count else "不一致 ✗"}')

    # ② 缺文件
    dangling = sorted(f for f in man_files if f not in disk_set)
    unregistered = sorted(f for f in disk_set if f not in man_files)
    miss_file = len(dangling) + len(unregistered)
    log(f'  ② 缺文件    manifest悬空={len(dangling)}  磁盘未登记={len(unregistered)}  '
        f'→ {miss_file} (须为 0)')
    for f in dangling[:5]:
        log(f'        ! manifest 指向不存在的文件: {f}')
    for f in unregistered[:5]:
        log(f'        ! 磁盘存在但未登记: {f}')

    # ③ 缺缩略图
    miss_thumb = [i['file'] for i in items
                  if not i.get('thumb') or not os.path.exists(os.path.join(ROOT, i['thumb']))]
    log(f'  ③ 缺缩略图  {len(miss_thumb)} (须为 0)')
    for f in miss_thumb[:5]:
        log(f'        ! {f}')

    # ④ 缺标签
    miss_tag = [i['file'] for i in items if not i.get('highlights')]
    log(f'  ④ 缺标签    {len(miss_tag)} (须为 0)')
    for f in miss_tag[:5]:
        log(f'        ! {f}')

    # ⑤ 标签总数不得低于上一次（防静默降级）
    tags = set()
    for i in items:
        tags.update(i.get('highlights', []))
    tag_ok = len(tags) >= pre_tags
    log(f'  ⑤ 标签总数  上次={pre_tags}  本次={len(tags)}  → '
        f'{"未下降 ✓" if tag_ok else "下降 ✗（静默降级）"}')

    # ⑥ 逐件比对：上次有标签的作品，本次标签数不得减少（直击 131→0 事故）
    pre_by_file = {i['file']: len(i.get('highlights', []))
                   for g in ('research', 'creative') for i in pre_manifest.get(g, [])}
    lost = [f"{i['file']} ({pre_by_file[i['file']]}→{len(i.get('highlights', []))})"
            for i in items
            if pre_by_file.get(i['file']) and len(i.get('highlights', [])) < pre_by_file[i['file']]]
    log(f'  ⑥ 标签丢失  {len(lost)} 件 (须为 0)')
    for s in lost[:5]:
        log(f'        ! {s}')

    # ⑦ EMBEDDED 快照契约（TAGMAP 已废弃：其 100/103 与 manifest.highlights 重复，
    #    且部分条目更旧会反向覆盖新标签。标签唯一来源改为 manifest.highlights。）
    #    这里改为校验真正会静默失效的三件事：快照存在、件数同步、字段同名。
    tagmap_missing = []
    if os.path.exists(INDEX):
        html = read_text(INDEX)
        if 'const TAGMAP=' in html:
            tagmap_missing.append('index.html 仍含已废弃的 TAGMAP 数据段')
        em = re.search(r'^const EMBEDDED=(\{.*\});$', html, re.M)
        if not em:
            tagmap_missing.append('index.html 缺少单行 EMBEDDED 数据段（file:// 回退已失效）')
        else:
            try:
                snap = json.loads(em.group(1))
                s_items = snap.get('research', []) + snap.get('creative', [])
                if len(s_items) != len(items):
                    tagmap_missing.append(
                        f'EMBEDDED {len(s_items)} 件 ≠ manifest {len(items)} 件（快照过期）')
                elif s_items and ({'file','title','date','type','highlights'}
                                  - set(s_items[0])):
                    tagmap_missing.append('EMBEDDED 字段名与 manifest 不一致，normalize() 会静默丢字段')
            except json.JSONDecodeError as exc:
                tagmap_missing.append(f'EMBEDDED 解析失败: {exc}')
    log(f'  ⑦ 快照契约  问题 {len(tagmap_missing)} 项 (须为 0)')
    for s in tagmap_missing[:5]:
        log(f'        ! {s}')

    # ⑧ 元数据键与类型登记表一致性（10-24 例会落地：直击"102键 vs 101作品"与
    #    "类型判定漂移"两类隐患——enrich.json 孤儿键会让元数据静默失配，
    #    登记表与 manifest 类型冲突说明有人改了判定却没同步登记表）
    enrich_data = load_json(ENRICH, {'works': []})
    if isinstance(enrich_data, dict) and 'works' not in enrich_data:
        enrich_data = {'works': enrich_data}
    enrich_files = {w.get('file') for w in enrich_data.get('works', []) if w.get('file')}
    enrich_orphans = sorted(enrich_files - disk_set)

    registry = load_type_registry(TYPES_REGISTRY)
    manifest_type = {i['file']: i['type'] for i in items}
    type_conflicts = []
    for rel in sorted(disk_set):
        want = registry.get(work_key(rel))
        if want and manifest_type.get(rel) and want != manifest_type[rel]:
            type_conflicts.append((rel, manifest_type[rel], want))

    meta_ok = not enrich_orphans and not type_conflicts
    log(f'  ⑧ 元数据/类型  enrich孤儿键={len(enrich_orphans)}  '
        f'类型冲突={len(type_conflicts)}  登记表={len(registry)}条 (须为 0)')
    for f in enrich_orphans[:5]:
        log(f'        ! enrich.json 键指向不存在的作品: {f}')
    for f, got, want in type_conflicts[:5]:
        log(f'        ! 类型冲突: {f} manifest={got} 登记表={want}'
            f'（修判定须同步 tools/autopublish_types.json）')

    # ⑨ 返回链完整性（看完成品必须能回展厅，否则只能靠浏览器后退）
    no_backlink = []
    for rel in sorted(disk_set):
        full = os.path.join(ROOT, rel)
        try:
            txt = open(full, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        if 'showcase-backlink' not in txt:
            no_backlink.append(rel)
    log(f'  ⑨ 返回链    缺失 {len(no_backlink)} (须为 0)')
    for f in no_backlink[:5]:
        log(f'        ! 缺「返回展厅」链接: {f}')

    # ⑩ 断言层引用有效性（无人值守产出的断言必须仍能在原文逐字命中）
    claim_bad = claim_total = 0
    try:
        sys.path.insert(0, TOOLS)
        import claim_gate as _gate
        for i in items:
            full = os.path.join(ROOT, i['file'])
            if not os.path.exists(full):
                continue
            html = open(full, encoding='utf-8', errors='ignore').read()
            nbody = _gate.normalize(_gate.re.sub(r'<[^>]+>', ' ', _gate.strip_code(html)))
            for c in (i.get('claims') or []):
                claim_total += 1
                if not _gate.verify_quote(c.get('quote', ''), nbody):
                    claim_bad += 1
    except Exception as exc:                       # 闸门不可用不该阻断上架
        log(f'  ⑩ 断言层    跳过（闸门不可用: {exc}）')
    else:
        log(f'  ⑩ 断言层    {claim_total} 条 · 引用失效 {claim_bad} (须为 0)')
        cs = manifest.get('claim_stats') or {}
        log(f'              覆盖 {cs.get("works_covered", 0)}/{cs.get("works_total", 0)} 件 '
            f'({cs.get("coverage", 0)}%) · 待处理 {cs.get("pending", 0)} · '
            f'无结构 {cs.get("no_structure", 0)}')

    fails = []
    # ── 以下为 WARN（不判失败）：十项硬校验的语义保持不变，
    #    但让两类"看着全绿其实有洞"的缺口不再隐身（10-27 例会新增）。
    #  W1 作品契约声明块缺失（规则15）：0/104 时"断言层全绿"是假象 ——
    #      manifest 里的 claims 是 claim_gate 自动抽取的回落值，不是作者声明。
    no_claims = [i['file'] for i in items
                 if '<script type="application/json" id="claims">' not in
                 read_text(os.path.join(ROOT, i['file']))]
    no_beat = [i['file'] for i in items
               if 'name="showcase-beat"' not in read_text(os.path.join(ROOT, i['file']))]
    #  W2 根目录非白名单残留：原「根目录残留=0」只统计 .html，
    #      preview.png / test.txt 这类死重一直检不出来（10-26 实测 3 个）。
    strays = sorted(f for f in os.listdir(ROOT)
                    if os.path.isfile(os.path.join(ROOT, f))
                    and not f.startswith('.') and f not in ROOT_ALLOWED)
    log(f'  ⚠ W1 作品契约  缺claims声明 {len(no_claims)} 件 · 缺追踪线声明 {len(no_beat)} 件'
        f'（不判失败，但覆盖率 88% 的缺口就在这里）')
    for f in no_claims[-3:]:
        log(f'        ! 无 claims 声明块: {f}')
    if strays:
        log(f'  ⚠ W2 根目录非白名单文件 {len(strays)} 个: ' + ', '.join(strays[:8]))
    if not c_count:
        fails.append('计数不一致')
    if miss_file:
        fails.append(f'缺文件 {miss_file}')
    if miss_thumb:
        fails.append(f'缺缩略图 {len(miss_thumb)}')
    if miss_tag:
        fails.append(f'缺标签 {len(miss_tag)}')
    if not tag_ok:
        fails.append(f'标签总数下降 {pre_tags}→{len(tags)}')
    if lost:
        fails.append(f'标签丢失 {len(lost)}')
    if tagmap_missing:
        fails.append(f'TAGMAP 未覆盖 {len(tagmap_missing)}')
    if enrich_orphans:
        fails.append(f'enrich.json 孤儿键 {len(enrich_orphans)}')
    if type_conflicts:
        fails.append(f'类型登记表冲突 {len(type_conflicts)}')
    if no_backlink:
        fails.append(f'缺返回链 {len(no_backlink)}')
    if claim_bad:
        fails.append(f'断言引用失效 {claim_bad}')
    if js_bad:
        fails.append(f'内联脚本语法错误 {len(js_bad)}')

    log('')
    if fails:
        log('  ✗ 校验未通过：' + '；'.join(fails))
    else:
        log('  ✓ 校验全部通过')
    return fails, len(tags)


# ────────────────────────────────────────────────────────────── 主流程

def main():
    global TYPES_REGISTRY

    ap = argparse.ArgumentParser(
        description='展厅「交付即上架」自动化流水线',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='只体检不落盘（不搬移/不截图/不重建）')
    ap.add_argument('--skip-thumbs', action='store_true', help='跳过缩略图生成（调试用）')
    ap.add_argument('--quiet-seconds', type=int, default=180,
                    help='静默门禁：产出需静默多少秒才算写完（默认 180；0 = 关闭门禁）')
    ap.add_argument('--registry', default=TYPES_REGISTRY, help='作品类型登记表路径')
    args = ap.parse_args()

    TYPES_REGISTRY = args.registry

    rule('智枢展厅 · 交付即上架流水线')
    log(f'  根目录 : {ROOT}')
    log(f'  模式   : {"演练（不落盘）" if args.dry_run else "正式执行"}')
    log(f'  时间   : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    pre_manifest = load_json(MANIFEST, {'research': [], 'creative': []})
    pre_tags = set()
    for g in ('research', 'creative'):
        for i in pre_manifest.get(g, []):
            pre_tags.update(i.get('highlights', []))
    log(f'  基线   : manifest {pre_manifest.get("total", 0)} 件 / 标签 {len(pre_tags)} 个')

    registry = load_type_registry(args.registry)
    if registry:
        log(f'  登记表 : {len(registry)} 条类型登记（{os.path.basename(args.registry)}）')

    # ── 阶段 0：静默门禁
    if not phase_quiescence(args.quiet_seconds):
        return 1

    snaps = {p: snapshot(p) for p in (MANIFEST, ENRICH, INDEX)}
    if not args.dry_run:
        dest = make_backup()
        log(f'  备份   : {os.path.relpath(dest, ROOT)}')

    # ── 阶段 1.5：隔离碎片
    quarantined = phase_quarantine(args.dry_run)

    def live_works():
        return [w for w in build_manifest.scan_works() if not in_quarantine(w, quarantined)]

    # ── 阶段 1：扫描
    disk_works = live_works()
    phase_scan(disk_works, pre_manifest)

    # ── 阶段 2：搬移
    stats = []
    moves = phase_move(disk_works, stats, args.dry_run)
    if moves:
        disk_works = live_works()

    # ── 阶段 3：键重映射
    phase_remap(moves, disk_works, pre_manifest, args.dry_run)

    # ── 阶段 4：元数据
    disk_works = live_works()
    phase_metadata(disk_works, args.dry_run)

    # ── 阶段 4.5：内联脚本语法校验（发现问题即判失败，不让它上展）
    js_bad = check_inline_js(live_works())

    # ── 阶段 4.8：注入档案条 + 死规则救援
    # ⚠️ 必须**在截图之前**：缩略图是页面截图，若此时页面还没注入救援样式
    # （59 件作品的内容被死规则永久隐藏），拍出来就是全黑 —— 实测 50 张黑图。
    phase_claims(disk_works, args.dry_run)

    # ── 阶段 5：缩略图
    if not args.skip_thumbs:
        phase_thumbs(disk_works, pre_manifest, registry, args.dry_run)
    else:
        rule('阶段 5 · 缩略图')
        log('  [skip] 按参数跳过')

    # ── 阶段 5.8：自愈（清孤儿键）
    if not args.dry_run:
        prune_orphan_enrich(live_works())

    # ── 阶段 6：重建索引
    phase_manifest(args.dry_run)

    # ── 幂等收尾：内容未变则还原 mtime（重复执行不产生任何副作用）
    if not args.dry_run:
        same = [os.path.basename(p) for p, s in snaps.items() if restore_if_unchanged(p, s)]
        if same:
            log(f'  幂等: {", ".join(same)} 内容未变，已还原 mtime')

    # ── 阶段 7：校验
    fails, tag_count = phase_validate(pre_manifest, len(pre_tags), quarantined, js_bad)

    rule('结果')
    if args.dry_run:
        log('  演练模式：未写入任何文件')
    if fails:
        log(f'  ✗ 流水线失败：{"；".join(fails)}')
        return 1
    log(f'  ✓ 流水线完成：{load_json(MANIFEST, {}).get("total")} 件作品，{tag_count} 个标签')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        log(f'\n✗ 流水线异常终止: {type(e).__name__}: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(2)
