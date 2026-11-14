#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""独立复核 429 核源台账：逐条 quote 与源文件行号比对 + 负面断言检验。"""
import re, os, sys

BASE = "/app/working/shared/tasks"
AI = os.path.join(BASE, "每日AI技术动态简报")
HOT = os.path.join(BASE, "每日热点新闻简报")
STK = os.path.join(BASE, "每日股市简报")

def load(p):
    with open(p, encoding="utf-8") as f:
        return f.read().split("\n")

def strip_line(line):
    s = line.lstrip()
    s = re.sub(r"^\d+[\.、]\s*", "", s)
    s = s.replace("**", "")
    return s.strip()

# (标签, 文件, 行号, 台账quote片段)
CHECKS = [
    ("①-a AI11-10 L7 估值+募资", AI+"/2026-11-10.md", 7,
     "Anthropic IPO 最快本周二启动路演，拟 11 月 16 日当周定价、纳斯达克挂牌，目标募资 800 亿至 1000 亿美元，共识估值下修至 1.1 万亿至 1.75 万亿美元。来源：东方财富 / 华尔街日报"),
    ("①-b 热点11-09 L6 1.2-1.3万亿", HOT+"/2026-11-09.md", 6,
     "Anthropic推出Claude for Microsoft 365：与Word、Excel、Outlook、Teams深度整合；其IPO潜在估值预期下调至1.2-1.3万亿美元。（虎扑/华尔街见闻 11-09）"),
    ("①-c 热点11-09 L5 OpenAI 1.25万亿", HOT+"/2026-11-09.md", 5,
     "OpenAI与博通180亿美元芯片交易遇融资缺口：双方仍在磋商解决方案；OpenAI新一轮融资缩水，首批110亿美元到账，估值1.25万亿美元，软银、红杉参投，软银出资或降至数亿美元。（虎扑/华尔街见闻 11-09）"),
    ("②-a 股市11-10 L28 布伦特90", STK+"/2026-11-10.md", 28,
     "油价暴跌、金价回升：布伦特原油跌近6%、盘中触及90美元；现货黄金收复4100美元；美元指数几乎回吐上周五全部涨幅；10年期美债收益率仍在4.87%附近。（腾讯新闻 11-10）"),
    ("②-b 热点11-10 L16 布伦特94", HOT+"/2026-11-10.md", 16,
     "国际油价暴跌：布伦特原油跌至每桶94美元；市场对结束伊朗战争前景乐观，特朗普表态缓和，能源成本下降缓解通胀担忧，美债收益率走低。（中国基金报 11-09）"),
    ("②-d 热点11-09 L19 布伦特97.3", HOT+"/2026-11-09.md", 19,
     "今晨国际油价跳水：WTI跌0.42%报90.45美元/桶，布伦特跌逾1%报97.3美元/桶；上周原油跌超10%，创半年多最大周跌。（21世纪经济报道 11-09）"),
    ("③/⑦-a 热点11-10 L19 高盛65%+2960亿", HOT+"/2026-11-10.md", 19,
     "高盛警示\"1998年剧本\"缺陷：1998年危机靠美联储降息兜底，2026年市场却仍定价12月加息约65%概率，且无LTCM式救助；超大规模数据中心运营商今年已发行2960亿美元债券。（金融界 11-08）"),
    ("⑦-b 热点11-10 L17 摩根大通40年", HOT+"/2026-11-10.md", 17,
     "华尔街抄底买盘推动反弹：分析师称科技股抛售后新一轮买盘入场；摩根大通称本轮为\"约40年来最大规模动量多头交易平仓\"，投资者悲观情绪已接近极端。（中国基金报 11-09）"),
    ("⑥-3 AI11-10 L32 1.1万亿新锚点", AI+"/2026-11-10.md", 32,
     "Anthropic 定价 1.1 万亿美元区间将成为一级市场 AI 估值新锚点，影响同类公司 IPO 与融资定价。来源：东方财富"),
    ("⑥-2 AI11-10 L8 涡轮机34亿", AI+"/2026-11-10.md", 8,
     "Anthropic 斥资约 34 亿美元购买天然气涡轮机，加入 AI 公司锁定发电能力的供电竞赛，资产负债表与化石能源周期绑定加深。来源：TechCrunch（TodayAI 日报 11-10）"),
    ("⑥-4 AI11-10 L26 三线推进", AI+"/2026-11-10.md", 26,
     "上市前的密集发布节奏：Anthropic 以新模型 + 降价 + IPO 路演三线推进，行业竞争与融资窗口高度同步。来源：东方财富"),
    ("⑤-a 热点11-10 L20 今晚CPI", HOT+"/2026-11-10.md", 20,
     "今晚关注美国10月CPI：为12月9日FOMC会议前最后的关键通胀数据，定价摇摆变量。（ratespike 11-08）"),
    ("⑤-c 热点11-09 L43 周二公布", HOT+"/2026-11-09.md", 43,
     "Kalshi与Polymarket同步定价12月加息76.5%：10月CPI（周二公布）是12月9日会议前最后的摇摆变量。（ratespike 11-08）"),
    ("混用风险 股市11-10 L11 中国CPI", STK+"/2026-11-10.md", 11,
     "资金面与宏观：央行11月10日开展1900亿元隔夜逆回购，利率1.25%，单日净投放80亿元；统计局9日发布10月CPI同比+0.7%、PPI同比+5.7%；前10个月货物贸易进出口44.81万亿元、同比+20%。（腾讯新闻/新浪财经 11-10）"),
    ("旁证 热点11-10 L15 深夜", HOT+"/2026-11-10.md", 15,
     "隔夜美股（美东11-09）全线大涨：道指涨超700点，标普500涨超1.8%，纳指涨约2%，纳指100涨近3%；费城半导体指数直线暴涨5%；AMD涨超8%、博通涨超7%。（中国基金报 11-09 深夜）"),
]

print("=== A. 逐条 quote 行号比对 ===")
ok = bad = 0
for label, path, ln, quote in CHECKS:
    if not os.path.exists(path):
        print(f"[MISS] {label}: 文件不存在 {path}"); bad += 1; continue
    lines = load(path)
    if ln > len(lines):
        print(f"[MISS] {label}: 行号 {ln} 超出行数 {len(lines)}"); bad += 1; continue
    raw = lines[ln-1]
    s = strip_line(raw)
    hit = (s == quote) or (quote in s) or (s in quote)
    status = "OK " if hit else "MISMATCH"
    if hit: ok += 1
    else: bad += 1
    print(f"[{status}] {label}")
    if not hit:
        print(f"    源行: {s[:160]}")
        print(f"    引用: {quote[:160]}")
print(f"-- A 小计: 匹配 {ok} / 不符 {bad}")

print()
print("=== B. 负面断言检验（台账称'零命中'的项）===")
NEG = [
    ("热点11-09 无「94美元」", HOT+"/2026-11-09.md", ["94美元", "每桶94"]),
    ("热点11-09 无「1.25万亿」以外Anthropic估值语境", HOT+"/2026-11-09.md", ["Anthropic估值", "Anthropic 一级市场"]),
    ("AI11-08 无 Anthropic/1.25万亿估值锚", AI+"/2026-11-08.md", ["1.25万亿", "1.25 万亿"]),
    ("热点11-08 无「高盛」", HOT+"/2026-11-08.md", ["高盛"]),
    ("热点11-08 无「65%」", HOT+"/2026-11-08.md", ["65%"]),
    ("AI11-08 无「65%」", AI+"/2026-11-08.md", ["65%"]),
    ("AI11-08 无「94美元」", AI+"/2026-11-08.md", ["94美元"]),
    ("热点11-08 无「94美元」", HOT+"/2026-11-08.md", ["94美元"]),
]
for label, path, needles in NEG:
    if not os.path.exists(path):
        print(f"[MISS] {label}: 文件不存在"); continue
    txt = "\n".join(load(path))
    found = [n for n in needles if n in txt]
    print(f"[{'CLEAN' if not found else 'HIT'}] {label} -> {found if found else '零命中'}")

print()
print("=== C. 12月加息概率口径并存核对（台账称 5 个不同口径并存）===")
PROB = [("65%", HOT+"/2026-11-10.md"), ("78%", HOT+"/2026-11-10.md"),
        ("84.2%", STK+"/2026-11-10.md"), ("76.5%", HOT+"/2026-11-09.md"),
        ("80%", HOT+"/2026-11-08.md")]
for n, p in PROB:
    txt = "\n".join(load(p)) if os.path.exists(p) else ""
    print(f"  {n:8s} in {os.path.basename(p)}: {'命中' if n in txt else '未命中'}")
