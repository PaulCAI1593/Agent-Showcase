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
def check_claim_layer():
    """断言层巡检（从例会 Step 5 迁来 —— 例会 429 期间这段就没人跑了）。

    查三件事：
      ① 有没有断言引用失效（源文件被改 / 断言陈旧）
      ② 断言总数相对基线是否跌幅 >20%（抽取回归）
      ③ 覆盖率是否低于 60%（新作品没用模板）
    """
    rc, out, err = run([sys.executable, os.path.join(SHOWCASE, 'tools', 'claim_gate.py'),
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


def check_runtime(pages=None):
    """作品页运行时巡检（从例会 Step 4.9 迁来）。

    全量 108 件约 4 分钟；守护里每 N 轮跑一次全量太重 → 默认抽样。
    """
    cmd = [sys.executable, os.path.join(SHOWCASE, 'tools', 'audit_pages.py')]
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
    cmd = [sys.executable, os.path.join(SHOWCASE, 'tools', 'design_scan.py'),
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
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
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


def tick(do_audit=False):
    ok, detail = converge_showcase()
    crons = check_crons()
    extra = []
    brief_ok, brief_note = check_briefs()
    extra.append(('素材侧（每日简报）', brief_ok, brief_note))
    claim_ok, claim_note = check_claim_layer()
    extra.append(('断言层巡检', claim_ok, claim_note or '引用全部有效'))
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

    if args.once:
        ok, detail = (True, '') if args.no_showcase else converge_showcase()
        crons = check_crons()
        extra = []
        brief_ok, brief_note = check_briefs()
        extra.append(('素材侧（每日简报）', brief_ok, brief_note))
        claim_ok, claim_note = check_claim_layer()
        extra.append(('断言层巡检', claim_ok, claim_note or '引用全部有效'))
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
