#!/usr/bin/env python3
"""
auto_maintain.py — 展厅零 token 维护守护进程

为什么需要它
------------
实测（2026-10-25 ~ 11-01）：6 个 cron 任务**全部 429 报错**
（Token Plan 额度耗尽），自动化从 10-30 起停了 3 天，没人发现。

而根因是：每次 agent 调用要先吞 **72,784 字符 ≈ 45,489 token** 的常驻
上下文，3113 次调用 × 45K = 1.4 亿 token 全是上下文开销（真正的回答
只占 287 万）。

关键洞察：**展厅的机械维护根本不需要 LLM** ——
跑 autopublish、跑巡检、查 cron 死活，全是纯脚本。
让它们依赖 agent cron，等于让"额度"决定"展厅还更不更新"。

所以把它们移出 agent 循环，走这个守护进程：
  · 额度耗尽时，展厅仍然自动收敛
  · cron 挂掉会被立刻发现（写进 HEARTBEAT_STATUS.md 的 🩺 区块）

用法
----
  python3 tools/auto_maintain.py --once      跑一轮就退出（测试/手动用）
  python3 tools/auto_maintain.py            守护循环（默认 30 分钟一轮）
  python3 tools/auto_maintain.py --interval 15

它做什么
--------
1. 展厅收敛：跑 autopublish.sh（静默门禁防抖动，幂等）
2. cron 健康：逐个查 state —— 失败或超期未跑 → 记 🔴
3. 把结果写进 HEARTBEAT_STATUS.md 的「🩺 心跳检查TODO」区块
4. 写一份机器可读的状态快照 state/auto_maintain.json（agent 读它很便宜）
5. 日志轮转
"""

import argparse
import datetime
import fcntl
import json
import os
import re
import subprocess
import sys
import time

# 本文件在 shared/showcase/tools/ 下 → ROOT 就是展厅目录
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOWCASE = ROOT

WORKSPACE = os.path.normpath(os.path.join(ROOT, '..', '..', 'workspaces', 'default'))
STATE_DIR = os.path.join(WORKSPACE, 'state')
# 解释器选择：容器里 `sys.executable` 可能为空串（11-14 实测），且系统
# python3 无 playwright —— 派生子进程一律优先 venv 解释器，避免
# PermissionError('') 与 ModuleNotFoundError 两类环境崩溃。
PY = (sys.executable
      or next((c for c in ('/app/venv/bin/python3', '/usr/bin/python3')
               if os.path.exists(c)), 'python3'))
STATE_FILE = os.path.join(STATE_DIR, 'auto_maintain.json')
HEARTBEAT_STATUS = os.path.join(WORKSPACE, 'HEARTBEAT_STATUS.md')
LOG_DIR = os.path.join(ROOT, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'auto_maintain.log')
# 单实例锁：auto_maintain 与它的看门狗（auto_maintain_watchdog.sh /
# auto_maintain_keepalive.sh）都可能拉起守护进程，两个实例同时写
# HEARTBEAT_STATUS.md 会互相覆盖行。fcntl.flock 随进程退出自动释放，
# 不会留下陈旧锁（陈旧锁会让守护再也起不来）。
LOCK_FILE = os.path.join(LOG_DIR, 'auto_maintain.lock')
# 锁的持有者 pid 另存一份给看门狗脚本判断「是不是已经有实例在跑」
PID_FILE = os.path.join(LOG_DIR, 'auto_maintain.pid')
# 视为「当前健康」的 cron 状态
HEALTHY_STATUS = ('success', 'ok', 'running', '未首次运行')
# 心跳 TODO 区块只保留最近这么多行 —— 否则守护每 30 分钟加一批，会无限膨胀
MAX_TODO_ROWS = 24
# 已处置行保留条数（未处置行不再受此上限约束，见 write_heartbeat）
MAX_SETTLED_ROWS = 12
# 「已自愈」说明行单独保留条数 —— 它是「某 cron 已恢复」的持久证据，
# 不能被上面的已处置行上限挤掉（11-16 实测：说明行 04:50 写入，
# 05:21 那一轮就被挤没了，证据等于没留）。
MAX_HEALED_ROWS = 6

# cron 间隔的粗略映射（分钟）—— 用于判断「该跑了却没跑」
CRON_INTERVAL_HINT = {
    '0 8 * * *': 1440,
    '0 21 * * *': 1440,
    '0 9 * * *': 1440,
    '0 14 * * mon-fri': 1440,
    '0 2 * * tue,thu,sat': 4320,
    '0 0 1 * *': 43200,
    # 周度发布（每周日 02:00）——2026-11-10 补：缺此键时回落 1440，
    # 2.5×24h=60h 后把健康的周度 cron 误报成「已 60 小时未跑（应每 24 小时）」
    '0 2 * * sun': 10080,
}


def bj_now():
    """北京时间（Asia/Shanghai）。容器本地时区是 UTC，直接用 now() 会让
    日志与 HEARTBEAT_STATUS.md 的时间戳比北京时间晚 8 小时，与心跳协议口径不一致。"""
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))


def log(msg):
    ts = bj_now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'{ts} {msg}'
    print(line, flush=True)
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        # 日志轮转：超过 1MB 就换名
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 1024 * 1024:
            os.replace(LOG_FILE, LOG_FILE + '.1')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except OSError:
        pass


def run(cmd, cwd=None, timeout=900):
    """返回 (rc, stdout, stderr)。

    ⚠️ stdout 与 stderr 必须**分开**：qwenpaw CLI 的 INFO 日志走 stderr，
    拼在一起会让 json.loads 失败（守护进程第一次跑时 cron 状态全是 '?'）。
    """
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or ''), (r.stderr or '')
    except subprocess.TimeoutExpired:
        return 124, '', f'超时 {timeout}s'
    except Exception as e:
        return 1, '', str(e)


def load_json(path, default=None):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}


def parse_json(text):
    """从可能夹杂日志的输出里抠出 JSON（对象 {} 或数组 [] 都认）。

    qwenpaw CLI 会往 stderr 打 INFO 日志；cron list 返回的是**数组**，
    cron state 返回的是**对象** —— 两种都要支持。
    """
    t = (text or '').strip()
    if not t:
        return None
    try:
        return json.loads(t)          # 干净输出直接用
    except Exception:
        pass
    for op, cl in (('{', '}'), ('[', ']')):
        i, j = t.find(op), t.rfind(cl)
        if i < 0 or j <= i:
            continue
        try:
            return json.loads(t[i:j + 1])
        except Exception:
            continue
    return None


# ── ⓪ 单实例锁 ────────────────────────────────────────────
def _lock_holder():
    """读锁文件里的持有者信息 → (pid, started_at, argv)。读不到返回 (None,'','')。

    锁文件格式：第 1 行 pid，第 2 行 JSON 详情（便于 shell 脚本 head -1 读 pid）。
    """
    try:
        with open(LOCK_FILE, encoding='utf-8') as f:
            raw = f.read()
    except OSError:
        return (None, '', '')
    lines = raw.split('\n')
    pid = None
    if lines and lines[0].strip().isdigit():
        pid = int(lines[0].strip())
    info = {}
    if len(lines) > 1 and lines[1].strip():
        try:
            info = json.loads(lines[1])
        except Exception:
            info = {}
    return (pid, info.get('started_at', ''), info.get('argv', ''))


def acquire_instance_lock():
    """拿单实例排他锁。

    返回 (fd, pid)：成功时 fd 必须**一直持有**（进程退出时内核自动释放）。
    返回 (None, holder_pid, holder_info)：拿不到（已有实例在跑）。

    用 fcntl.flock(LOCK_EX|LOCK_NB) 而非 O_EXCL 锁文件：flock 由内核管理，
    进程被 kill -9 也会自动释放，不会留下「陈旧锁」把守护锁死。
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    fd = os.open(LOCK_FILE, os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        pid, started_at, argv = _lock_holder()
        os.close(fd)
        return (None, None, {'pid': pid, 'started_at': started_at, 'argv': argv})
    payload = json.dumps({
        'pid': os.getpid(),
        'started_at': bj_now().isoformat(timespec='seconds'),
        'argv': ' '.join(sys.argv),
    }, ensure_ascii=False)
    os.ftruncate(fd, 0)
    os.write(fd, f'{os.getpid()}\n{payload}\n'.encode('utf-8'))
    os.fsync(fd)
    # pidfile 给看门狗脚本用（它读它判断守护是否活着）
    try:
        with open(PID_FILE, 'w', encoding='utf-8') as f:
            f.write(f'{os.getpid()}\n')
    except OSError:
        pass
    return (fd, os.getpid(), {})


def release_instance_lock(fd):
    """释放锁并清掉 pidfile（只删自己写的那个）。"""
    try:
        if os.path.exists(PID_FILE):
            with open(PID_FILE, encoding='utf-8') as f:
                if f.read().strip() == str(os.getpid()):
                    os.remove(PID_FILE)
    except OSError:
        pass
    try:
        if fd is not None:
            os.ftruncate(fd, 0)
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
    except OSError:
        pass


# ── ① 展厅收敛 ────────────────────────────────────────────
def converge_showcase():
    # 不再传 --quiet-seconds 0：强制绕过门禁会把**作者正在写的初稿**直接
    # 索引上架并截图（11-12 实测 #426/#431 落盘数分钟即入馆）。守护改为
    # 尊重默认 180s 静默窗——本轮有写入就跳过，下一轮再收敛；
    # 「交付即上架」与「不上半成品」不再只能二选一。
    rc, out, err = run(['bash', os.path.join(SHOWCASE, 'tools', 'autopublish.sh')],
                       cwd=SHOWCASE, timeout=1800)
    ok = (rc == 0)
    detail = ''
    if not ok:
        m = re.findall(r'✗[^\n]*', out)
        detail = '；'.join(m[:2]) if m else out.strip().splitlines()[-1][:120] if out.strip() else ''
    log(f'展厅收敛: {"✓ 通过" if ok else "✗ 退出码" + str(rc)} {detail}')
    return ok, detail


# ── ② cron 健康 ───────────────────────────────────────────
def last_history_entry(jid):
    """从 jobs_history/<id>.json 取最近一次运行记录（跨 qwenpaw 重启持久）。

    返回 {'run_at':..., 'status':..., 'error':...} 或 None。
    """
    runs = last_history_entries(jid, 1)
    return runs[-1] if runs else None


def last_history_entries(jid, n=2):
    """取最近 n 次运行记录，按 run_at 升序返回（最旧在前）。"""
    p = os.path.join(WORKSPACE, 'jobs_history', jid + '.json')
    if not os.path.exists(p):
        return []
    try:
        with open(p, encoding='utf-8') as f:
            hist = json.load(f)
    except Exception:
        return []
    runs = [e for e in hist if isinstance(e, dict) and e.get('run_at')]
    runs.sort(key=lambda e: str(e.get('run_at')))
    return runs[-n:] if n else runs


def _parse_ts(s):
    """把 ISO 时间串转成 datetime（比较新旧用）。解析不了返回 None。"""
    if not s:
        return None
    try:
        return datetime.datetime.fromisoformat(str(s).replace('Z', '+00:00'))
    except Exception:
        return None


def resolve_status(state_status, state_run, hist_status, hist_run):
    """双源判定 cron 当前状态：取「运行时间较新」的那条证据。

    为什么必须双源（只看一个都会错）：
      · `cron state` 是**运行内存**里的字段，qwenpaw 一重启就全变 null
        （11-04 实测：6 个 cron 的 last_status 同时变 null，而 jobs_history
        里明明记着当天 success）—— 只看 state 会把健康 cron 误判成失败。
      · `jobs_history/<id>.json` 是磁盘上的持久记录，但只由 cron 自己追加，
        进程刚重启还没跑到时它比内存旧 —— 只看 history 会漏掉最新一轮结果。
    所以两条都读，按 run_at 取新的那条；时间都缺时优先 state（内存更新鲜）。

    返回 (status, run_at)。
    """
    ts, th = _parse_ts(state_run), _parse_ts(hist_run)
    if ts and th:
        if th > ts:
            return hist_status, hist_run
        return state_status, state_run
    if ts:
        return state_status, state_run
    if th:
        return hist_status, hist_run
    return (state_status or hist_status), (state_run or hist_run)


def check_crons():
    """逐个查 cron 的运行状态。返回 [{name, status, age_min, ok, note}]"""
    rc, out, err = run(['qwenpaw', 'cron', 'list', '--agent-id', 'default'], timeout=120)
    if rc != 0:
        return [{'name': '(读取失败)', 'status': 'unknown', 'ok': False,
                 'note': out.strip()[:100]}]
    try:
        jobs = parse_json(out)
        if not isinstance(jobs, list) or not jobs:
            raise ValueError('空列表')
    except Exception as e:
        return [{'name': '(解析失败)', 'status': 'unknown', 'ok': False,
                 'note': f'{e}｜输出前120字: {out[:120]}'}]

    now = datetime.datetime.now(datetime.timezone.utc)
    results = []
    for j in jobs:
        jid = j.get('id')
        name = j.get('name', '?')
        cron = (j.get('schedule') or {}).get('cron', '')
        # 已禁用的 cron 不参与健康判定 —— 否则它会永远顶着一句「上次状态 error」
        # 的 🔴（例：11-12 例会禁用月度备份后，11-01 那条 429 记录会永久误报）。
        if not j.get('enabled', True):
            results.append({'name': name, 'status': '已禁用', 'age_min': None,
                            'ok': True, 'note': '已禁用（职责已移交，不再判定）'})
            continue
        rc2, out2, err2 = run(['qwenpaw', 'cron', 'state', jid, '--agent-id', 'default'], timeout=60)
        st = parse_json(out2) or {}
        # ── 双源证据：内存 state + 磁盘 jobs_history ──
        state_status = (st.get('last_status') or '').strip() or None
        if state_status in ('None', 'null', 'undefined'):
            state_status = None
        state_run = st.get('last_run_at')
        hist = last_history_entries(jid, 2)
        h_last = hist[-1] if hist else {}
        h_prev = hist[-2] if len(hist) > 1 else {}
        hist_status = (h_last.get('status') or '').strip() or None
        if hist_status in ('None', 'null', 'undefined'):
            hist_status = None
        hist_run = h_last.get('run_at')
        prev_status = (h_prev.get('status') or '').strip() or None
        # 取较新的一条证据作为「当前状态」
        status, last = resolve_status(state_status, state_run, hist_status, hist_run)
        if not status:
            # 既无内存态也无历史 → 这个 cron 从未跑过（如新建的周度发布 job）。
            # 「还没到点」不是故障，判为正常，等它第一次触发。
            status = '未首次运行'
        age_min = None
        if last:
            try:
                dt = datetime.datetime.fromisoformat(last.replace('Z', '+00:00'))
                age_min = (now - dt).total_seconds() / 60
            except Exception:
                pass
        err = (st.get('last_error') or '')
        mm = re.search(r"'message':\s*'([^']+)'", err)
        err = mm.group(1) if mm else err[:110]
        # 判定：失败，或超过 2.5 倍间隔还没跑
        interval = CRON_INTERVAL_HINT.get(cron, 1440)
        late = age_min is not None and age_min > interval * 2.5
        # running = 此刻正在执行。它会被**自己**判成 🔴 —— 例会跑起来时
        # 守护同时在记「例会 cron 异常」，每 30 分钟污染一次 TODO 表。
        ok = (status in HEALTHY_STATUS) and not late
        # 自愈信号：上一轮是失败、这一轮是成功 → 该 cron 已经好了，
        # 它此前留在 TODO 表里的待处理行是陈旧残留，必须清掉。
        self_healed = ok and prev_status not in (None, 'success', 'ok')
        note = ''
        if status not in HEALTHY_STATUS:
            note = err or f'上次状态 {status}'
        elif late:
            note = f'已 {age_min/60:.0f} 小时未跑（应每 {interval/60:.0f} 小时）'
        results.append({'name': name, 'status': status, 'age_min': age_min,
                        'ok': ok, 'note': note,
                        'state_status': state_status, 'state_run_at': state_run,
                        'hist_status': hist_status, 'hist_run_at': hist_run,
                        'prev_status': prev_status, 'self_healed': self_healed,
                        'run_at': last})
    return results


# ── ③ 写回 HEARTBEAT_STATUS.md ────────────────────────────
def check_claim_layer():
    """断言层巡检（从例会 Step 5 迁来 —— 例会 429 期间这段就没人跑了）。

    查三件事：
      ① 有没有断言引用失效（源文件被改 / 断言陈旧）
      ② 断言总数相对基线是否跌幅 >20%（抽取回归）
      ③ 覆盖率是否低于 60%（新作品没用模板）
    """
    rc, out, err = run([PY, os.path.join(SHOWCASE, 'tools', 'claim_gate.py'),
                        '--verify'], cwd=SHOWCASE, timeout=600)
    ok = (rc == 0)
    note = ''
    if not ok:
        bad = [l.strip() for l in out.splitlines() if '失效' in l]
        note = bad[0][:110] if bad else (out.strip().splitlines()[-1][:110] if out.strip() else '校验失败')
    # 基线对比
    try:
        mf = os.path.join(SHOWCASE, 'manifest.json')
        m = json.load(open(mf, encoding='utf-8'))
        # claim_stats 在 manifest **顶层**（不在 stats 里）—— 读错位置会得到 0
        cs = m.get('claim_stats') or (m.get('stats') or {}).get('claim_stats') or {}
        base = load_json(os.path.join(SHOWCASE, 'tools', '.claim_state.json'), {})
        total = cs.get('total', 0)
        prev = base.get('total')
        if prev and total < prev * 0.8 and ok:
            ok = False
            note = f'断言总数 {total} 较基线 {prev} 跌超 20%（抽取回归）'
        cov = cs.get('coverage', 100)
        if cov < 60:
            note = (note + '；' if note else '') + f'断言覆盖率仅 {cov}%（新作品可能没用模板）'
    except Exception as e:
        note = (note + '；' if note else '') + f'读基线失败 {e}'
    log(f'断言层: {"✓" if ok else "✗"} {note}')
    return ok, note


def check_monthly_backup():
    """月度频道聊天记录备份（纯脚本，从 agent cron 迁来）。

    为什么迁：11-01 该任务在 agent cron 里以 429 RateLimitError 失败 ——
    它的正文只是「跑一个 python 脚本」，根本不需要 LLM，却让额度决定
    备份做不做。同 auto_maintain 的设计初衷：机械维护移出 agent 循环。

    判据：看本月备份目录里有没有当月的备份文件；没有就说明本月没做，
    补跑一次。备份脚本自带幂等（同一份数据重复备份也安全）。
    """
    script = os.path.join(WORKSPACE, 'scripts', 'backup-and-clear-channels.py')
    if not os.path.exists(script):
        return True, '备份脚本不存在，跳过'
    root = os.path.normpath(os.path.join(SHOWCASE, '..', 'backups', 'channel-history'))
    ym = datetime.datetime.now().strftime('%Y-%m')
    month_dir = os.path.join(root, ym)
    try:
        existing = [f for f in os.listdir(month_dir) if f.endswith('.json')]
    except OSError:
        existing = []
    if existing:
        note = f'本月（{ym}）已备份 {len(existing)} 个频道文件'
        log(f'月度备份: ✓ {note}')
        return True, note
    rc, out, err = run(['python3', script], timeout=900)
    ok = (rc == 0)
    n = sum(1 for l in out.splitlines() if '✅' in l)
    note = (f'已补跑，{n} 个频道完成' if ok
            else (out.strip().splitlines()[-1][:110] if out.strip() else '补跑失败'))
    log(f'月度备份: {"✓" if ok else "✗"} {note}')
    return ok, note


def check_runtime(pages=None):
    """作品页运行时巡检（从例会 Step 4.9 迁来）。

    全量 108 件约 4 分钟；守护里每 N 轮跑一次全量太重 → 默认抽样。
    """
    cmd = [PY, os.path.join(SHOWCASE, 'tools', 'audit_pages.py')]
    if pages:
        cmd += ['--sample', str(pages)]
    rc, out, err = run(cmd, cwd=SHOWCASE, timeout=1800)
    ok = (rc == 0)
    m = re.search(r'巡检完成：(\d+) 件，(\d+) 件有问题', out)
    if m:
        n, bad = m.group(1), m.group(2)
        note = f'{n} 件真实加载，{bad} 件有问题'
        ok = (bad == '0')
        log(f'运行时巡检: {"✓" if ok else "✗"} {note}')
        return ok, note
    note = (out.strip().splitlines()[-1][:110] if out.strip() else '巡检未产出结果')
    log(f'运行时巡检: ✗ {note}')
    return False, note


def check_design(full=False):
    """设计质量棘轮：impeccable detect 的规则分布只许降不许升。

    为什么要有：规则14 要求交付前跑 detect+polish，但没有任何机器闸门强制，
    于是全馆积压 4907 条 findings（111/116 件有）。一次性清完不现实
    （每件都是独立视觉世界，批量改色会毁掉作者的世界）——
    所以走棘轮：全量扫描后与基线比，任何规则条数**上升**即判回归。

    full=False 只扫近 30 天改动的作品（快，用于日常巡检，不比棘轮）。
    """
    scope = 'all' if full else 'recent:30'
    cmd = [PY, os.path.join(SHOWCASE, 'tools', 'design_scan.py'),
           '--scope', scope]
    rc, out, err = run(cmd, cwd=SHOWCASE, timeout=3600)
    if rc == 2:
        note = (out.strip().splitlines()[-1][:110] if out.strip() else 'detect 不可用')
        log(f'设计扫描: ✗ {note}')
        return False, note
    m = re.search(r'findings (\d+) 条 .*?涉及 (\d+) 件', out)
    if not m:
        note = (out.strip().splitlines()[-1][:110] if out.strip() else '未产出结果')
        log(f'设计扫描: ✗ {note}')
        return False, note
    total, files = m.group(1), m.group(2)
    if not full:
        note = f'近 30 天改动作品：findings {total} 条 / {files} 件'
        log(f'设计扫描: ✓ {note}')
        return True, note
    ok = (rc == 0)
    note = (f'全量 {files} 件 · findings {total} 条 · '
            + ('棘轮通过（无一规则上升）' if ok else '棘轮被打破：有规则上升'))
    log(f'设计扫描: {"✓" if ok else "✗"} {note}')
    return ok, note


BRIEF_DIRS = [
    '/app/working/shared/tasks/每日AI技术动态简报',
    '/app/working/shared/tasks/每日热点新闻简报',
    '/app/working/shared/tasks/每日股市简报',
]
BRIEF_STALE_HOURS = 36


def check_briefs():
    """素材侧健康：三份每日简报有没有停更。

    实测 2026-11-01：三份简报最后一篇都是 **10-29** —— 素材链已停 3 天。
    素材一停，选题识别就没有输入，整条链（素材→选题→作品→上展）断在源头。
    守护要能看到这件事，否则它安静地停掉，没人知道。
    """
    import glob as _g
    now = time.time()
    rows = []
    stale = []
    for d in BRIEF_DIRS:
        name = os.path.basename(d)
        try:
            files = [f for f in _g.glob(os.path.join(d, '*.md'))]
            if not files:
                stale.append(f'{name}：无任何简报')
                continue
            newest = max(files, key=os.path.getmtime)
            age_h = (now - os.path.getmtime(newest)) / 3600
            day = os.path.basename(newest).replace('.md', '')
            rows.append(f'{name} 最新 {day}（{age_h:.0f} 小时前）')
            if age_h > BRIEF_STALE_HOURS:
                stale.append(f'{name} 已停更 {age_h:.0f} 小时（最新 {day}）')
        except Exception as e:
            stale.append(f'{name}：读取失败 {e}')
    ok = not stale
    log(f'素材侧: {"✓" if ok else "✗"} ' + ('；'.join(stale) if stale else '；'.join(rows)))
    return ok, ('；'.join(stale) if stale else '；'.join(rows))


def write_heartbeat(crons, showcase_ok, showcase_detail, extra=None):
    if not os.path.exists(HEARTBEAT_STATUS):
        return
    try:
        s = open(HEARTBEAT_STATUS, encoding='utf-8').read()
    except OSError:
        return
    ts = bj_now().strftime('%Y-%m-%d %H:%M')
    bad = [c for c in crons if not c['ok']]
    lines = []
    if not showcase_ok:
        lines.append(f'| {ts} | 🔴 | 展厅收敛失败 | {showcase_detail or "见 autopublish 日志"} | ✅已处置 |')
    for label, ok_, detail in (extra or []):
        lines.append(f'| {ts} | {"🟢" if ok_ else "🔴"} | {label} | {detail} | '
                     f'{"✅已处置" if ok_ else "待处理"} |')
    for c in bad:
        lines.append(f'| {ts} | 🔴 | cron「{c["name"]}」异常 | '
                     f'{c["note"] or ("状态 " + c["status"])} | 待处理 |')
    if not lines:
        lines.append(f'| {ts} | 🟢 | 自动维护守护正常 | 展厅收敛✓ · '
                     f'{len(crons)} 个 cron 全部成功 | ✅已处置 |')
    row = '\n'.join(lines)
    m = re.search(r'(## 🩺 心跳检查TODO\s*\n)(\|.*\n)(\|.*\n)(\|[^\n]*\n)*', s)
    if not m:
        return
    block = m.group(0)
    blines = [l for l in block.rstrip('\n').split('\n')]
    # 前两行是表头与分隔行（分隔行格式未必是 |---|...|，别写死）
    head = blines[:2] if len(blines) >= 2 else blines
    rows_txt = [l for l in blines[len(head):] if l.strip()]
    # 截尾按「状态」而非行数：未处置项（待处理 / 🚄处理中）必须全部保留，
    # 否则写在中段的持久条目会被后续巡检轮次挤掉（2026-11-12 实测 31 行→末 24 行）。
    pending = [l for l in rows_txt if not l.rstrip().endswith('✅已处置 |')]
    settled = [l for l in rows_txt if l.rstrip().endswith('✅已处置 |')]

    # ── 陈旧失败不重登 ──────────────────────────────────────
    # 某 cron 当前 status=success（依据 = cron state + jobs_history 双源）时，
    # 它此前留在 TODO 表里的「cron「X」异常」待处理行就是**陈旧残留**：
    # 故障已自愈，行还挂着 → 已自愈的 cron 长期占着待处理区，真故障被淹没。
    # 实证（11-16）：cron「每日AI技术动态简报」11-15 21:09 已 success，
    #   11-15 20:40 那行 feishu 报错仍标待处理；cron「展厅守护保活」当前 success，
    #   11-14 22:21 那行报错仍标待处理。
    # 处置：删掉陈旧行 + 留一条标注「已自愈」的说明（状态 ✅已处置）。
    healthy = {c['name']: c for c in crons if c['ok']}
    cron_row_re = re.compile(r'^cron「(.+?)」(异常|已自愈)$')

    def _prob_cell(l):
        parts = [x.strip() for x in l.split('|')]
        return parts[3] if len(parts) > 3 else l.strip()

    def _cron_of(l):
        m = cron_row_re.match(_prob_cell(l))
        return m.group(1) if m else None

    def _cron_state(l):
        m = cron_row_re.match(_prob_cell(l))
        return m.group(2) if m else None

    # 已有「已自愈」说明行的 cron —— 已有就不再重复写
    noted = set()
    for l in rows_txt:
        if _cron_state(l) == '已自愈':
            nm = _cron_of(l)
            if nm:
                noted.add(nm)

    kept_pending = []
    healed_rows = []
    healed_seen = set()
    for l in pending:
        nm = _cron_of(l)
        if nm and nm in healthy and _cron_state(l) == '异常':
            # 陈旧行 → 本轮要删（下面统一处理）
            healed_seen.add(nm)
            continue
        kept_pending.append(l)
    # 对每个「本轮已健康、且有待处理残留或历史上刚自愈」的 cron：
    #   ① 删掉它的待处理行；② 补一条「已自愈」说明行（已有则不重复写）
    for nm in list(healed_seen) + [c['name'] for c in crons
                                  if c.get('self_healed') and c['ok'] and c['name'] not in healed_seen]:
        if nm not in healthy or nm in noted:
            continue
        c = healthy[nm]
        when = str(c.get('run_at') or c.get('hist_run_at') or '')
        when = when.replace('T', ' ')[:16]
        why = '陈旧待处理行已清除' if nm in healed_seen else '上一轮失败已恢复'
        healed_rows.append(
            f'| {ts} | 🟢 | cron「{nm}」已自愈 | '
            f'最近一次运行 {c.get("status")}'
            + (f'（{when}）' if when else '')
            + f' —— {why} | ✅已处置 |')
        noted.add(nm)
    # 陈旧待处理行真正删除：凡属已健康 cron 的「cron「X」异常」行一律剔除
    kept_pending = [l for l in kept_pending
                    if not (_cron_of(l) in healthy and _cron_state(l) == '异常')]
    pending = kept_pending
    if healed_rows:
        log(f'清理陈旧失败行 {len(healed_rows)} 条：' +
            '、'.join(_cron_of(l) or '?' for l in healed_rows))

    # 去重：同一「问题」的重复登记只留最后一条 —— 守护每 30min 会把同一个
    # cron 失败按**当前时间**重写成新行（2026-11-13 22:20→23:28 刷了 15 行，
    # 撑破 100 行上限且淹没真异常）。按「问题列」归并即可。
    # 把本轮新行与旧行放在一起按「问题列」归并，**只留最新一条**：
    # 这样同一 cron 失败不会每 30min 刷一行，把真异常淹没、撑破 100 行上限。
    new_rows = [l for l in lines if l.strip()] + healed_rows
    order, latest = [], {}
    for l in pending + new_rows:
        k = _prob_cell(l)
        if k not in latest:
            order.append(k)
        latest[k] = l
    merged = [latest[k] for k in order]
    # 「已自愈」说明行单独留一份（不被已处置行上限挤掉）——
    # 它是「某个 cron 已恢复」的持久证据，被挤掉就等于没留痕。
    healed_notes = [l for l in settled if _cron_state(l) == '已自愈']
    settled_other = [l for l in settled if _cron_state(l) != '已自愈']
    keep = (merged
            + healed_notes[-MAX_HEALED_ROWS:]
            + settled_other[-MAX_SETTLED_ROWS:])
    new = '\n'.join(head + keep) + '\n'   # 本轮新行已并入 merged，不重复追加
    s = s.replace(block, new, 1)
    try:
        with open(HEARTBEAT_STATUS, 'w', encoding='utf-8') as f:
            f.write(s)
    except OSError:
        return
    log(f'已写入 HEARTBEAT_STATUS.md：{len(lines)} 条')


# ── ④ 状态快照（给 agent 便宜地读）─────────────────────────
def write_state(crons, showcase_ok, showcase_detail):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'updated_at': bj_now().isoformat(timespec='seconds'),
                'showcase_ok': showcase_ok,
                'showcase_detail': showcase_detail,
                'crons': crons,
                'cron_bad': [c['name'] for c in crons if not c['ok']],
                'cron_healed': [c['name'] for c in crons if c.get('self_healed')],
            }, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def tick(do_audit=False):
    ok, detail = converge_showcase()
    crons = check_crons()
    extra = []
    brief_ok, brief_note = check_briefs()
    extra.append(('素材侧（每日简报）', brief_ok, brief_note))
    claim_ok, claim_note = check_claim_layer()
    extra.append(('断言层巡检', claim_ok, claim_note or '引用全部有效'))
    backup_ok, backup_note = check_monthly_backup()
    extra.append(('月度频道备份', backup_ok, backup_note))
    if do_audit:
        audit_ok, audit_note = check_runtime()
        extra.append(('作品页运行时巡检', audit_ok, audit_note))
    write_heartbeat(crons, ok, detail, extra)
    write_state(crons, ok, detail)
    bad = [c for c in crons if not c['ok']]
    if bad:
        log(f'cron 异常 {len(bad)} 个: ' + '、'.join(c['name'] for c in bad))
    else:
        log(f'cron 全部正常（{len(crons)} 个）')
    return ok, crons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--once', action='store_true', help='跑一轮就退出')
    ap.add_argument('--interval', type=int, default=30, help='轮询间隔（分钟）')
    ap.add_argument('--pages', type=int, default=0, help='运行时巡检抽样件数（0=全量）')
    ap.add_argument('--no-showcase', action='store_true', help='跳过展厅收敛（只查 cron）')
    ap.add_argument('--audit', action='store_true', help='本轮跑全量运行时巡检')
    ap.add_argument('--design', action='store_true', help='本轮跑全量设计棘轮（detect 规则分布）')
    args = ap.parse_args()

    # ── 单实例闸门 ──────────────────────────────────────────
    # auto_maintain 与它的看门狗脚本（auto_maintain_watchdog.sh /
    # auto_maintain_keepalive.sh / restart_automaintain.sh）都可能拉起守护。
    # 两个实例同时写 HEARTBEAT_STATUS.md 会互相覆盖行（谁后写谁赢），
    # 也可能出现「A 正在改、B 正在读」的半截文件。
    # 这里用 fcntl.flock 排他锁把关：拿不到锁 → 打日志直接退出，**不做任何写入**。
    lock_fd, lock_pid, holder = acquire_instance_lock()
    if lock_fd is None:
        holder = holder if isinstance(holder, dict) else {}
        started = holder.get('started_at') or ''
        argv = holder.get('argv') or ''
        log(f'单实例锁：已有实例在运行（pid={holder.get("pid") or "?"}'
            + (f'，启动于 {started}' if started else '')
            + (f'，命令 {argv}' if argv else '')
            + '）→ 本次退出（未做任何写入）')
        return 3
    log(f'已取得单实例锁（pid={lock_pid}，锁文件 {LOCK_FILE}）')
    try:
        return _run(args)
    finally:
        release_instance_lock(lock_fd)
        log('已释放单实例锁')


def _run(args):
    if args.once:
        ok, detail = (True, '') if args.no_showcase else converge_showcase()
        crons = check_crons()
        extra = []
        brief_ok, brief_note = check_briefs()
        extra.append(('素材侧（每日简报）', brief_ok, brief_note))
        claim_ok, claim_note = check_claim_layer()
        extra.append(('断言层巡检', claim_ok, claim_note or '引用全部有效'))
        backup_ok, backup_note = check_monthly_backup()
        extra.append(('月度频道备份', backup_ok, backup_note))
        if args.audit:
            audit_ok, audit_note = check_runtime(args.pages)
            extra.append(('作品页运行时巡检', audit_ok, audit_note))
        if args.design:
            design_ok, design_note = check_design(full=True)
            extra.append(('设计质量棘轮（全量 detect）', design_ok, design_note))
        write_heartbeat(crons, ok, detail, extra)
        write_state(crons, ok, detail)
        bad = [c for c in crons if not c['ok']]
        log(f'一轮完成：展厅 {"✓" if ok else "✗"} · 断言层 {"✓" if claim_ok else "✗"} · '
            f'cron 异常 {len(bad)}/{len(crons)}')
        return 0 if (ok and not bad and claim_ok) else 1

    log(f'守护启动，间隔 {args.interval} 分钟（Ctrl-C 停止）')
    n = 0
    while True:
        try:
            # 每 6 轮（约 3 小时）跑一次全量运行时巡检 —— 从例会迁来，
            # 因为例会正 429，这段检查不能只住在那里。
            do_audit = (n % 6 == 0)
            # 设计棘轮每 12 轮（约 6 小时）跑一次全量比对 —— 扫描本身约 7 分钟
            do_design = (n % 12 == 0)
            ok, detail = converge_showcase()
            crons = check_crons()
            extra = []
            claim_ok, claim_note = check_claim_layer()
            extra.append(('断言层巡检', claim_ok, claim_note or '引用全部有效'))
            backup_ok, backup_note = check_monthly_backup()
            extra.append(('月度频道备份', backup_ok, backup_note))
            if do_audit:
                audit_ok, audit_note = check_runtime()
                extra.append(('作品页运行时巡检（每3小时全量）', audit_ok, audit_note))
            if do_design:
                design_ok, design_note = check_design(full=True)
                extra.append(('设计质量棘轮（每6小时全量）', design_ok, design_note))
            write_heartbeat(crons, ok, detail, extra)
            write_state(crons, ok, detail)
            n += 1
        except Exception as e:
            log(f'轮次异常: {e}')
        try:
            time.sleep(max(1, args.interval) * 60)
        except KeyboardInterrupt:
            log('守护停止')
            return 0


if __name__ == '__main__':
    sys.exit(main())
