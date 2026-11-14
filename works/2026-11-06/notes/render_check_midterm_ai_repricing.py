#!/usr/bin/env python3
"""417 mid-term AI repricing — 离线结构与图表数据自检。运行：python3 render_check.py"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "research" / "2026-11-06-midterm-ai-repricing.html"
FAILS, WARNS = [], []
s = TARGET.read_text(encoding="utf-8")

def fail(m): FAILS.append(m)
def warn(m): WARNS.append(m)

# 1. 必备结构
for pat, name in [
    (r'<meta name="showcase-beat" content="[^"]+"', "追踪线 meta"),
    (r'<title>[^<]+</title>', "title"),
    (r'<meta name="description" content="[^"]+"', "description"),
]:
    if not re.search(pat, s): fail(f"缺 {name}")

# 2. claims
m = re.search(r'id="claims">\s*(\[.*?\])\s*</script>', s, re.S)
if not m: fail("缺 claims 块"); claims = []
else:
    claims = json.loads(m.group(1))
    if not (3 <= len(claims) <= 8): fail(f"claims 数量 {len(claims)} 不在 3~8")
    def norm(t): return re.sub(r'[\s\W_]+', '', t)
    ns = norm(s)
    labels = [c.get("label") for c in claims]
    for c in claims:
        if not all(c.get(k) for k in ("value", "label", "quote")):
            fail(f"claims 字段缺失: {c}")
        elif norm(c["quote"]) not in ns:
            fail(f"quote 未在正文逐字命中: {c['label']} -> {c['quote'][:30]}...")
    if len(set(labels)) != len(labels): fail("claims label 重复")
    for lab in labels:
        if re.search(r'（推算）|（V2|得分', lab): fail(f"label 含禁用后缀: {lab}")

# 3. 语义块词汇表（自创数据类名）
allowed = {'metrics','metric','metric-value','metric-label','metric-source','verdict',
           'timeline','timeline-item','evidence','evidence-item'}
html_no_style = re.sub(r'<style.*?</style>', '', s, flags=re.S)
for cls in re.findall(r'class="([^"]+)"', html_no_style):
    for c in cls.split():
        if c in allowed: continue
        # 非语义布局类：结构/排版类允许，但数据承载类必须在词汇表
        if c in {'shell','masthead','mast-grid','mast-meta','standfirst','lede','note',
                 'chart-wrap','chart-box','chart-cap','table-wrap','duo','duo-card',
                 'duo-kicker','tag','gate','gate-item','gate-name','gate-body',
                 'hold','pass','colophon','rule-draw','drawn','is-ahead','is-key',
                 'is-flag','is-down','is-up','metric-num','mu','ledger','caliber-note'}:
            continue
        warn(f"未登记 class: {c}")

# 4. 必需语义块存在
for cls in ['metrics','metric','metric-value','metric-label','metric-source',
            'verdict','timeline','timeline-item','evidence','evidence-item']:
    if f'class="{cls}"' not in s and f'{cls} ' not in s and cls not in \
       [c for block in re.findall(r'class="([^"]+)"', html_no_style) for c in block.split()]:
        fail(f"缺语义块 .{cls}")

# 5. 五组涨跌幅矩阵数据（与简报逐字核对）
matrix = {'道指':3.03,'标普':1.58,'纳指':1.44,'费半':-3.11,'微软':6.68,'亚马逊':6.12,
          '苹果':5.31,'谷歌':3.25,'Meta':1.44,'英伟达':-3.17,'特斯拉':-3.34,
          'CoreWeave':-9.90,'IREN':-11,'Hut 8':-23,'希捷':-8.13,'闪迪':-7.91,
          '美光':-7.00,'西部数据':-6.77,'SK 海力士':-5.12,'Credo':-9.55,'迈威尔':-7.08,'Coherent':-5.93}
mrow = re.search(r'var mLabels=\[(.*?)\];\s*var mData=\[(.*?)\];', s)
if not mrow: fail("缺矩阵数据")
else:
    labels = [x.strip().strip("'") for x in mrow.group(1).split(',')]
    data = [float(x) for x in mrow.group(2).split(',')]
    if len(labels) != len(data): fail("矩阵 labels/data 长度不一致")
    for lab, val in zip(labels, data):
        if lab not in matrix: fail(f"矩阵标签不在白名单: {lab}")
        elif abs(matrix[lab] - val) > 1e-9: fail(f"矩阵数值错: {lab} 图{val} 源{matrix[lab]}")

# 6. 选后两日数据
m2 = re.search(r'data:\{\s*labels:\[.{0,80}?\],\s*datasets:\[\s*\{label:\'11-04 单日\',data:\[(.*?)\].*?\{label:\'11-05 单日\',data:\[(.*?)\]', s, re.S)
if not m2: fail("缺两日数据")
else:
    d4 = [float(x) for x in m2.group(1).split(',')]
    d5 = [float(x) for x in m2.group(2).split(',')]
    if d4 != [3.03,1.58,1.44,-3.11]: fail(f"11-04 数据错: {d4}")
    if d5 != [-3.44,-4.36,-5.52,-12.25]: fail(f"11-05 数据错: {d5}")

# 7. 利率序列
mr = re.search(r"data:\{\s*labels:\['11-02','11-03','11-04','11-09'\],\s*datasets:\[\{\s*label:'CME FedWatch[^']*',\s*data:\[(.*?)\]", s, re.S)
if not mr: fail("缺利率序列")
else:
    r = [float(x) for x in mr.group(1).split(',')]
    if r != [72,74.9,78.9,78]: fail(f"利率序列错: {r}")

# 8. 本地资源不外链
for u in re.findall(r'(?:src|href)="(https?://[^"]+)"', s):
    fail(f"外部资源: {u}")

# 9. 关键断言值在正文出现（防 claims 与正文脱节）
for v in ['1569.40','53356.12','10270.85','48.42','-12.25%','1.25','78%']:
    if v not in s: fail(f"正文缺断言值 {v}")

# 10. 口径日期标注
if '11-09 收盘' not in s: fail("缺行情口径日期标注")
if 'CPI' not in s: fail("缺 CPI 窗口说明")

# 11. HTML 大小
size = TARGET.stat().st_size
if size < 10 * 1024: fail(f"文件过小 {size}B")

print(f"文件: {TARGET.name}  {size:,}B  claims={len(claims)}")
if WARNS:
    print("\n警告:")
    for w in WARNS: print("  ~", w)
if FAILS:
    print("\n失败:")
    for f in FAILS: print("  ✗", f)
    sys.exit(1)
print("\n全部检查通过")
