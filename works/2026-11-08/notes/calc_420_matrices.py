#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""选题420 核算：费率 / 点位 / 概率矩阵
输出：同目录 420-matrices.json（过程材料，不上展）
数据来源：shared/tasks/每日热点新闻简报/2026-11-07.md、
          每日AI技术动态简报/2026-11-07.md、每日股市简报/2026-11-06.md
"""
import json, os

R = {}

# ── 1. 一级市场：估值 / 融资 ──────────────────────────────
openai_round = 110.0            # 亿美元，热点新闻11-07 科技动态2
openai_round_cap = 200.0        # 亿美元，整轮最高或扩至
openai_val = 1.25               # 万亿美元
openai_want = 1.4               # 万亿美元，AI News「$1.4T it wanted」+ 彭博通稿（核源）
openai_want_alt = 1.5           # 万亿美元，彭博10-23 / 路透早期口径（核源，搜索摘要转引）
openai_amount_want = 300.0      # 亿美元，最初目标 ≥300 亿（彭博通稿，核源）
anthropic_ipo = 1.1             # 万亿美元，AI简报11-07 焦点7
anthropic_target = 2.0          # 万亿美元，原目标

R["valuation"] = {
    "anthropic_cut_pct": round((anthropic_target - anthropic_ipo) / anthropic_target * 100, 1),
    "openai_discount_pct_1p4": round((openai_want - openai_val) / openai_want * 100, 1),
    "openai_discount_pct_1p5": round((openai_want_alt - openai_val) / openai_want_alt * 100, 1),
    "openai_round_headroom_pct": round((openai_round_cap - openai_round) / openai_round * 100, 1),
    "openai_amount_vs_initial_pct": round((openai_amount_want - openai_round) / openai_amount_want * 100, 1),
    "anthropic_vs_openai_gap_pct": round((openai_val - anthropic_ipo) / openai_val * 100, 1),
    "note": "1.4万亿为主口径（AI News 页面直取 + 彭博通稿转引），1.5万亿并列不合并",
}

# ── 2. 宏观：非农 surprise ───────────────────────────────
nfp_actual = 16.5    # 万人
nfp_exp = 7.0        # 万人
R["nonfarm"] = {
    "beat_wan": round(nfp_actual - nfp_exp, 1),
    "beat_pct": round((nfp_actual - nfp_exp) / nfp_exp * 100, 1),
    "multiple": round(nfp_actual / nfp_exp, 2),
    "unemp": 4.1,
    "unemp_prev": 4.2,
    "revisions_wan": round(5.3 + 3.1, 1),   # 8月上修5.3万、9月上修3.1万（核源）
    "expectation_sources": {"彭博调查中位数": 7.0, "第一财经": 6.5, "LSEG": 6.5,
                            "FactSet": 6.5, "路透": 5.9},
    "release": "美东 2026-11-06 08:30 = 北京时间 11-06 21:30",
}

# ── 3. 概率矩阵：CME 序列 + LSEG 读数 ─────────────────────
cme_dec = [("11-02", 72.0, None), ("11-03", 74.9, None), ("11-04", 78.9, 21.1),
           ("11-05", 67.0, None), ("11-06早间", 68.7, 31.3), ("非农后", 74.8, 25.2)]
R["fedwatch"] = {
    "same_event": "2026-12-08/09 FOMC，+25bp（证券时报网逐字，核源）",
    "cme_dec": cme_dec,
    "lseg_post": 78.0,
    "lseg_pre_stated": 70.0,          # 「此前约70%」，未标时点，图上不落点
    "cme_first_caijing_post": 77.0,   # 财联社 11-06 22:48（核源，搜索摘要转引）
    "yicai_post": 80.0,               # 第一财经，报告前约75%（核源）
    "vendor_gap_pp": round(78.0 - 74.8, 1),      # 非农后 LSEG 与 CME 差
    "cme_swing_pp": round(78.9 - 67.0, 1),       # CME 11-04 → 11-05 摆动
    "mutual_exclusive_sums": [round(78.9 + 21.1, 1), round(68.7 + 31.3, 1),
                              round(74.8 + 25.2, 1)],
    "jan_meeting_82pct": "口径未确认（核不到原稿）",
    "jan_2027_cum": {"25bp": 63.6, "50bp": 9.5, "hold": 27.0},
}

# ── 4. 点位矩阵：两日 × 四指数（交叉核验） ────────────────
# 素材：股市简报11-06 美股段（11-05 收盘） + 热点新闻11-07 金融动态1（11-06 收盘）
idx = {
    "道指":     {"d1105_pct": -3.44, "d1105_close": 51523.06, "d1106_pct": -0.46, "d1106_close": 51285.73},
    "标普500":  {"d1105_pct": -4.36, "d1105_close": 7353.73,  "d1106_pct": 0.31,  "d1106_close": 7376.86},
    "纳指":     {"d1105_pct": -5.52, "d1105_close": 24315.0,  "d1106_pct": 1.09,  "d1106_close": 24579.42},
}
for k, v in idx.items():
    v["implied_d1106_pct"] = round((v["d1106_close"] / v["d1105_close"] - 1) * 100, 2)
    v["residual_pp"] = round(v["implied_d1106_pct"] - v["d1106_pct"], 2)
R["equities"] = {
    "cross_check": idx,
    "sox": {"d1105_pct": -12.25, "d1106_pct": 4.21, "close_levels": "素材未给收盘点位，不写"},
    "vix": {"d1105_pct": 69.48, "d1105_close": 28.15,
            "implied_prior": round(28.15 / (1 + 0.6948), 2)},
    "weekly": {"纳指": -3.4, "标普500": -2.7, "道指": -0.9},
    "sox_round_trip": round(4.21 - (-12.25), 2),   # 两日合计（未复权、仅代数和，标注为非累计口径）
}

# ── 5. 利率水平 ──────────────────────────────────────────
R["rates"] = {
    "2y": 4.51, "10y": 4.86,
    "slope_bp": round((4.86 - 4.51) * 100, 0),
    "policy_now": "3.75%-4.00%（10月FOMC，10:2维持）",
    "policy_after_25bp": "4.00%-4.25%（本页核算）",
    "10y_prior_1029": 5.021,   # #412 断言
    "10y_prior_1104": 4.89,    # #418 断言
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "420-matrices.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)
print(json.dumps(R, ensure_ascii=False, indent=2))
print("\nwritten:", out)
