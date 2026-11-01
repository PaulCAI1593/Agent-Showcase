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
STATE_FILE = os.path.join(STATE_DIR, 'auto_maintain.json')
HEARTBEAT_STATUS = os.path.join(WORKSPACE, 'HEARTBEAT_STATUS.md')
LOG_DIR = os.path.join(ROOT, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'auto_maintain.log')
# 心跳 TODO 区块只保留最近这么多行 —— 否则守护每 30 分钟加一批，会无限膨胀
MAX_TODO_ROWS = 24

# cron 间隔的粗略映射（分钟）—— 用于判断「该跑了却没跑」
CRON_INTERVAL_HINT = {
    '0 8 * * *': 1440,
    '0 21 * * *': 1440,
    '0 9 * * *': 1440,
    '0 14 * * mon-fri': 1440,
    '0 2 * * tue,thu,sat': 4320,
    '0 0 1 * *': 43200,
}


def log(msg):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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


# ── ① 展厅收敛 ────────────────────────────────────────────
def converge_showcase():
    rc, out, err = run(['bash', os.path.join(SHOWCASE, 'tools', 'autopublish.sh'),
                       '--quiet-seconds', '0'], cwd=SHOWCASE, timeout=1800)
    ok = (rc == 0)
    detail = ''
    if not ok:
        m = re.findall(r'✗[^\n]*', out)
        detail = '；'.join(m[:2]) if m else out.strip().splitlines()[-1][:120] if out.strip() else ''
    log(f'展厅收敛: {"✓ 通过" if ok else "✗ 退出码" + str(rc)} {detail}')
    return ok, detail


# ── ② cron 健康 ───────────────────────────────────────────
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
        rc2, out2, err2 = run(['qwenpaw', 'cron', 'state', jid, '--agent-id', 'default'], timeout=60)
        st = parse_json(out2) or {}
        status = st.get('last_status', '?')
        last = st.get('last_run_at')
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
        ok = (status in ('success', 'ok')) and not late
        note = ''
        if status not in ('success', 'ok'):
            note = err or f'上次状态 {status}'
        elif late:
            note = f'已 {age_min/60:.0f} 小时未跑（应每 {interval/60:.0f} 小时）'
        results.append({'name': name, 'status': status, 'age_min': age_min,
                        'ok': ok, 'note': note})
    return results


# ── ③ 写回 HEARTBEAT_STATUS.md ────────────────────────────
def write_heartbeat(crons, showcase_ok, showcase_detail):
    if not os.path.exists(HEARTBEAT_STATUS):
        return
    try:
        s = open(HEARTBEAT_STATUS, encoding='utf-8').read()
    except OSError:
        return
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    bad = [c for c in crons if not c['ok']]
    lines = []
    if not showcase_ok:
        lines.append(f'| {ts} | 🔴 | 展厅收敛失败 | {showcase_detail or "见 autopublish 日志"} | ✅已处置 |')
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
    keep = rows_txt[-MAX_TODO_ROWS:]
    new = '\n'.join(head + keep + [row]) + '\n'
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
                'updated_at': datetime.datetime.now().isoformat(timespec='seconds'),
                'showcase_ok': showcase_ok,
                'showcase_detail': showcase_detail,
                'crons': crons,
                'cron_bad': [c['name'] for c in crons if not c['ok']],
            }, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def tick():
    ok, detail = converge_showcase()
    crons = check_crons()
    write_heartbeat(crons, ok, detail)
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
    ap.add_argument('--no-showcase', action='store_true', help='跳过展厅收敛（只查 cron）')
    args = ap.parse_args()

    if args.once:
        if args.no_showcase:
            ok, detail = True, ''
        else:
            ok, detail = converge_showcase()
        crons = check_crons()
        write_heartbeat(crons, ok, detail)
        write_state(crons, ok, detail)
        bad = [c for c in crons if not c['ok']]
        log(f'一轮完成：展厅 {"✓" if ok else "✗"} · cron 异常 {len(bad)}/{len(crons)}')
        return 0 if (ok and not bad) else 1

    log(f'守护启动，间隔 {args.interval} 分钟（Ctrl-C 停止）')
    while True:
        try:
            if not args.no_showcase:
                converge_showcase()
            crons = check_crons()
            # 收敛结果也要拿到，写入用
            write_heartbeat(crons, True, '')
            write_state(crons, True, '')
        except Exception as e:
            log(f'轮次异常: {e}')
        try:
            time.sleep(max(1, args.interval) * 60)
        except KeyboardInterrupt:
            log('守护停止')
            return 0


if __name__ == '__main__':
    sys.exit(main())
