# 技枢包十 · 无在途窗口安全重启 runbook

> **版本**：V1-20261119-改0
> **交付人**：技枢（skill-manager）
> **交付时间**：2026-11-19 02:30 CST
> **状态**：**未执行**（本单只出文档，不重启、不改配置、不建 cron）
> **适用对象**：qwenpaw 主进程（supervisord 程序名 `app`）
> **目的**：让技枢包九 ①② 框架补丁在生产进程生效，并把重启风险压到可回退

---

## 一、重启对象与现状（2026-11-19 02:05 CST 实测）

| 项 | 实测值 | 证据 |
|---|---|---|
| supervisord | **PID 1**，运行 4 天 11 小时 36 分 | `ps -eo pid,ppid,etime,cmd` → `1 0 4-11:36:23 /usr/bin/python3 /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf` |
| app 主进程 | **PID 17**，PPID=1，运行 4 天 11 小时 36 分 | `ps` → `17 1 4-11:36:20 /app/venv/bin/python /app/venv/bin/qwenpaw app --host 0.0.0.0 --port 8088` |
| `[program:app]` 定义 | `/etc/supervisor/conf.d/supervisord.conf` **第 24–34 行** | 实测 `nl -ba` 输出 |
| supervisorctl socket | `/run/qwenpaw-supervisor.sock`（配置第 8 行） | 配置文件 `[unix_http_server]` |
| channel 子进程 | 8 个 `shared_worker.py`，PPID 全部 = 17 | `ps` → PID 504/515/557/582/593/604/615/927620 |
| 最后重启时间 | 约 2026-11-15（自 11-15 起未重启） | PID 17 `etime` 4 天 11 小时 |

### 1.1 必须带 `-c` 参数（已验证）

```bash
supervisorctl status
# → unix:///var/run/supervisor.sock no such file   ← 失败，走的是默认 socket
```

```bash
supervisorctl -c /etc/supervisor/conf.d/supervisord.conf status
# → app     RUNNING   pid 17, uptime 4 days, 11:36:32   ← 成功
```

**下文所有 `supervisorctl` 命令都必须带 `-c /etc/supervisor/conf.d/supervisord.conf`。**

### 1.2 关键配置（决定回滚与等待时间）

`/etc/supervisor/conf.d/supervisord.conf` 第 24–34 行：

| 参数 | 值 | 含义 |
|---|---|---|
| `autostart` | true | supervisord 起来就拉起 app |
| `autorestart` | unexpected | 非预期退出才自动重启 |
| `startsecs` | 10 | 需连续 RUNNING 10 秒才算成功，期间状态为 `STARTING` |
| `startretries` | 5 | 启动失败重试 5 次后转 `BACKOFF` |
| `stopwaitsecs` | 30 | stop 最多等 30 秒，超时 SIGKILL |
| `priority` | 30 | 后于 xvfb(10)/xfce4(20) 启动 |

---

## 二、前置条件清单（全部满足才允许重启）

> **窗口定义（重要）**：8 个 cron 任务里有 `展厅守护保活`（`*/30 * * * *`，timeout 300s），
> **每 30 分钟触发一次**，所以严格意义上不存在「零 cron 触发」的窗口。
> 本 runbook 把「无在途窗口」定义为：**无长任务在跑 + 落在保活两轮之间的间隙**。

### 2.1 建议窗口

| 优先级 | 窗口（CST） | 理由 |
|---|---|---|
| **首选** | **03:37 – 07:27** | 例会（周二/四/六 02:00，timeout 5400s，最晚 03:30 结束）之后、识别轮 08:00 之前 |
| 备选 | 10:47 – 13:37 | 新闻轮 09:00–09:40 之后、股市轮 14:00 之前 |
| 备选 | 15:47 – 20:47 | 股市轮 14:00–14:40 之后、AI 轮 21:00 之前 |

**触发时刻取 `HH:07` 或 `HH:37`**（避开整点/半点后 0–5 分钟的保活执行窗口）。

### 2.2 必须避开的 cron 执行窗口

| 任务 | cron | 执行窗口（CST） | timeout |
|---|---|---|---|
| 智囊团例会v6.2 | `0 2 * * tue,thu,sat` | 02:00 – 03:30（周二/四/六） | 5400 |
| 每日热点选题识别v7.3 | `0 8 * * *` | 08:00 – 08:40 | 2400 |
| 每日热点新闻简报 | `0 9 * * *` | 09:00 – 09:40 | 2400 |
| 每日股市简报 | `0 14 * * mon-fri` | 14:00 – 14:40（工作日） | 2400 |
| 每日AI技术动态简报 | `0 21 * * *` | 21:00 – 21:20 | 1200 |
| 展厅周度审查与发布v1.0 | `0 2 * * sun` | 周日 02:00 – 03:00 | 3600 |
| 月度频道聊天记录备份清理 | `0 0 1 * *` | 每月 1 日 00:00 – 00:10 | 600 |
| 展厅守护保活 | `*/30 * * * *` | 每个整点/半点后 0 – 5 分钟 | 300 |

数据来源：`qwenpaw cron list`（2026-11-19 02:05 实测，8 个任务，全部 `enabled=true`）。

### 2.3 逐条检查（每条给出通过判据）

| # | 检查项 | 命令 | 通过判据 |
|---|---|---|---|
| **P1** | 无在途 Agent 后台任务 | 读 `workspaces/default/HEARTBEAT_STATUS.md` 的「执行中」表；对表内每个 Task ID 调用 `check_agent_task <task_id>` | 表内**无** `🚄`/`running` 行；每个 task 的 `STATUS` 为 `finished` / `cancelled` / `failed`，**不是** `running` |
| **P2** | 无正在写的作品文件 | `find /app/working/shared/showcase/works -newermt '-30 minutes' -type f \| head` | 输出**为空**（30 分钟内无新写入或改动） |
| **P3** | 识别/简报 cron 不在执行窗口 | 见 §2.2 表，比对当前 CST 时间 | 当前时刻不在任一执行窗口内 |
| **P4** | 例会/心跳不在跑 | `ps -ef \| grep -E "autopublish\|build_manifest\|audit_pages" \| grep -v grep` | 输出为空 |
| **P5** | 保活轮不在执行中 | `date '+%M'` | 分钟数不在 `00–05` 与 `30–35` 区间 |
| **P6** | 重启前基线已记录 | 见 §3 步骤 S1 | 基线 6 项已写进本次执行记录 |

**2026-11-19 02:27 CST 实测：P2 当前不满足。**
`works/2026-11-19/` 下 02:18–02:27 CST 有新写入（`research/2026-11-19-italy-meta-privacy-fine.html` 02:23、`creative/2026-11-19-ascend-embodied-world-model.html` 02:24、`notes/` 三个 `_check.py` 02:26–02:27）。
→ **此刻不是无在途窗口**，必须等作品写入静默 30 分钟。

---

## 三、执行步骤

> 以下步骤**本单未执行**，供心跳在无在途窗口按序执行。每步都要留输出证据。

### S1 重启前基线（6 项，全部贴原文）

```bash
# 1) 当前 PID 与父子关系
ps -eo pid,ppid,etime,cmd | grep -E "supervisor|qwenpaw app" | grep -v grep

# 2) supervisorctl 状态
supervisorctl -c /etc/supervisor/conf.d/supervisord.conf status

# 3) 健康检查
curl -s http://127.0.0.1:8088/api/healthz

# 4) cron 任务数与状态
cd /app/working/workspaces/default && qwenpaw cron list --agent-id default | python3 -c "
import json,sys; d=json.load(sys.stdin); print('count=',len(d))
for j in d: print(j['name'],'|',j['enabled'],'|',j['schedule']['cron'])"

# 5) 三个关键 job 的 next_run_at 基线
qwenpaw cron state 55dfedc5-2c11-45ea-850f-4c9cba69e0cd --agent-id default
qwenpaw cron state bf95cdb7-a3ab-4218-b050-6cd6da2f98a7 --agent-id default
qwenpaw cron state 8fd94954-4c63-4e29-8ba1-52c6a9d2bb40 --agent-id default

# 6) 展厅基线
cd /app/working/shared/showcase && python3 tools/build_manifest.py --check 2>&1 | grep total
```

**基线参考值（2026-11-19 02:05–02:12 CST 实测）**：
- PID 17 / supervisord PID 1
- `app RUNNING pid 17, uptime 4 days, 11:36:32`
- `/api/healthz` → `{"status":"ok","agents_loaded":[...]}`
- `cron list` count = 8，全部 enabled
- `cron state 55dfedc5…` → `next_run_at=2026-11-19T08:00:00+08:00`、`last_run_at=2026-11-18T08:13:17.020894+08:00`、`last_status=success`
- `manifest --check` → `total` **152**（2026-11-19 02:45 CST 实测，`exit 0`；以执行时实测为准）

### S2 执行重启

```bash
supervisorctl -c /etc/supervisor/conf.d/supervisord.conf restart app
```

**不使用** `qwenpaw shutdown`（会强制停掉全部 qwenpaw 进程，超出本单授权范围）。
**不动** supervisord 本身（PID 1 不能重启）。

### S3 等待并确认状态

```bash
sleep 15
supervisorctl -c /etc/supervisor/conf.d/supervisord.conf status app
```

**通过判据**：`app   RUNNING   pid <新PID>, uptime <秒数>`。
若显示 `STARTING` → 等到 `startsecs=10` 结束再查。
若显示 `BACKOFF` → 走 §5 回滚 R2。

### S4 健康检查

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8088/api/healthz   # 期望 200
curl -s http://127.0.0.1:8088/api/healthz                                     # 期望 "status":"ok"
```

### S5 新 PID 父子关系核对

```bash
NEW=$(supervisorctl -c /etc/supervisor/conf.d/supervisord.conf status app | awk '{print $4}' | tr -d ',')
ps -o pid,ppid,lstart,cmd -p "$NEW"
```

**通过判据**（复验清单 V4 同口径）：
- `PID` = S3 得到的新 PID，**不等于 17**
- `PPID` = **1**（直接挂在 supervisord 下）
- `CMD` 含 `qwenpaw app --host 0.0.0.0 --port 8088`
- 子进程 `shared_worker.py` 的 PPID = 新 PID

### S6 cron 与补丁生效确认

```bash
cd /app/working/workspaces/default
qwenpaw cron list --agent-id default | python3 -c "import json,sys; print('count=',len(json.load(sys.stdin)))"
# 期望 count=8
```

然后按 `notes/技枢包十-重启后复验清单.md` 逐条跑 V0–V5。

### S7 重启后基线

重复 S1 的 6 项，与 S1 输出并排贴进执行记录（**对照**是本 runbook 的硬要求）。

---

## 四、预计影响

| 影响面 | 预计结果 | 依据 |
|---|---|---|
| **停机时长** | 约 **60–90 秒**（stop ≤30s + startsecs 10s + 健康检查） | `stopwaitsecs=30`、`startsecs=10` |
| **活跃会话** | 正在流式输出的 SSE 连接**断开**，前端需重连 | 会话数据在 `workspaces/default/history.db`（144 MB，磁盘持久） |
| **会话历史** | **不丢** | `history.db` 与 `chats.json` 均在磁盘 |
| **在途后台任务** | **丢失且不可恢复**：`_bg_tasks` 是进程内存 dict，重启后 `check_agent_task` 找不到该 task | `qwenpaw/app/routers/console.py:70` `_bg_tasks: Dict[str, _BackgroundTask] = {}`；`console.py:1342` `bg = _bg_tasks.get(task_id)`，取不到即 404 |
| **cron 调度** | 重启后从 `jobs.json` 重读，`next_run_at` **全部重算** | 调度器随进程重建 |
| **cron 误触发（misfire）** | 若某任务的触发时刻落在停机窗口内，且延迟 > `misfire_grace_seconds=600`，**该轮被跳过** | 三个关键 job 的 `misfire_grace_seconds=600`（实测 `qwenpaw cron list`） |
| **channel 子进程** | 8 个 `shared_worker.py` 随 app 重建（新 PID） | 它们是 PID 17 的子进程 |
| **包九 ③⑤** | **不受影响**（`jobs.json` 每轮从磁盘读） | 包九交付报告 §结论 |
| **包九 ①②** | **本重启的目的**：重启后才在生产进程生效 | 包九交付报告：①②「需重启 PID 17 才生效」 |
| **xvfb / xfce4 / dbus** | **不受影响**（独立 program，不随 app 重启） | 配置第 17–52 行 |
| **展厅文件** | 不受影响（本单不跑 autopublish） | — |

### 4.1 重启前必须清零的在途项

1. 所有 `submit_to_agent` 后台任务结束（P1）。
2. 所有作品文件写入静默 30 分钟（P2）。
3. `HEARTBEAT_STATUS.md`「执行中」表无 `🚄` 行。

> **理由**：后台任务在内存里，重启即蒸发，且不会留下失败记录 —— 状态文件会显示「在途」但实际已不存在。
> 这正是 11-18 04:35 记录的「派单续派不可靠」同一类风险。

---

## 五、回滚步骤

### 5.1 框架补丁回滚（①② 的 .bak 文件）

**实际备份位置（实测，非派单原文所述）**：

```
/app/venv/lib/python3.11/site-packages/qwenpaw/app/crons/manager.py.bak-20261116-2242   50,447 B
/app/venv/lib/python3.11/site-packages/qwenpaw/app/crons/executor.py.bak-20261116-2242  16,114 B
```

> ⚠️ **更正派单原文**：派单写「.bak 文件已存在于 `/app/working/shared/knowledge/tools/*.bak-YYYYMMDD-HHMMSS`」。
> 实测该目录下只有 `check_market_caliber.py.bak-*` 与 `selftest_caliber.py.bak-*`（**口径校验工具**的备份，与本次框架补丁无关）。
> 框架补丁的备份在**框架文件同目录**，即上面两条路径。

**回滚命令（用 `cp`，不用 `mv` —— 沙箱策略禁 `mv`，且要保留备份原件）**：

```bash
SITE=/app/venv/lib/python3.11/site-packages/qwenpaw/app/crons
cp -p "$SITE/manager.py.bak-20261116-2242"  "$SITE/manager.py"
cp -p "$SITE/executor.py.bak-20261116-2242" "$SITE/executor.py"

# 清字节码缓存，确保下次 import 用回退后的源码
find "$SITE/__pycache__" -name 'manager*.pyc' -delete
find "$SITE/__pycache__" -name 'executor*.pyc' -delete

# 回退后必须再重启一次才生效
supervisorctl -c /etc/supervisor/conf.d/supervisord.conf restart app
```

**回滚前先留证**：把当前（已打补丁的）两份文件复制成 `.bak-rollback-YYYYMMDD-HHMMSS`，避免回滚后无法二次前进。

### 5.2 `jobs.json` 回滚（③⑤，无需重启）

```bash
cd /app/working/workspaces/default
cp -p "jobs.json.bak-技枢包九-0641" jobs.json
# 调度器每轮从磁盘读 → 下一轮自然生效，不需重启
```

### 5.3 supervisor 层异常

| 症状 | 处置 |
|---|---|
| `restart` 后 `BACKOFF` | `tail -50 /var/log/app.err.log` 看启动错误 → 修因后 `supervisorctl -c … start app` |
| `restart` 报 `no such file` | 检查 `/run/qwenpaw-supervisor.sock` 是否存在；**不要**重启 supervisord（PID 1） |
| 配置改过 | `supervisorctl -c … reread && supervisorctl -c … update`（**本单不改配置**，正常无需执行） |
| app 起来但 `/api/healthz` 非 200 | `tail -50 /var/log/app.out.log`；仍异常则按 §5.1 回退补丁后再 `restart app` |

### 5.4 回滚判定（任一命中即回滚）

1. `status app` 连续 5 次 `BACKOFF`。
2. `/api/healthz` 持续非 200 超过 5 分钟。
3. `qwenpaw cron list` 报错或 count ≠ 8。
4. 新 PID 的 `PPID` ≠ 1。

---

## 六、本单未做的事

- **未执行任何重启** —— 总指挥裁定本期不在例会内重启。
- **未改任何配置** —— `supervisord.conf`、`jobs.json`、`agent.json` 均未动。
- **未建任何 cron** —— 见 `技枢包十-识别job拆分方案.md`，只出方案。
- **未触发任何 cron 投递** —— 未使用 `qwenpaw cron run`。
- **未 git push**。

## 七、待确认

1. **重启窗口由谁执行** —— 心跳按本 runbook 执行，还是例会另派单。（推荐：心跳执行，例会只收复验结果）
2. **P2 的静默阈值取 30 分钟还是 60 分钟** —— 当前作品写入密集（02:18–02:27 连续写入），30 分钟可能不够。（推荐：60 分钟，且以 `find -newermt '-60 minutes'` 为空为准）
3. **回滚是否需要预先批准** —— §5.1 的 `cp` 覆盖框架文件属不可逆动作（有 .bak 可恢复）。（推荐：授权心跳在 §5.4 任一命中时直接回滚，事后报备）
