#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calc_anthropic_leverage.py — 选题411「Anthropic 算力杠杆率拐点」测算底稿

输入层级
  A 级（一手，原文逐项抄录）
    Anthropic PBC 修订 Form S-1/A（Amendment No.1），2026-11-02 提交 SEC
    https://www.sec.gov/Archives/edgar/data/2130357/000162828026068676/anthropicpbc-sx1ax1.htm
    直取记录：HTTP 200，14,311,205 字节
    文本化副本：/tmp/anthropic_s1a.txt（行号见下方 SRC 注释）
  B 级（团队推导）
    本脚本全部计算结果
  C 级（机构/媒体估算）
    本脚本未采用；正文中的 C 级数据单独标注

单位：金额一律先以「百万美元」录入，输出时给出「亿美元」。

运行：python3 calc_anthropic_leverage.py
输出：calc_anthropic_leverage_result.json（与本脚本同目录）
"""

import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "calc_anthropic_leverage_result.json")

# ─────────────────────────────────────────────────────────────
# A 级输入 1：季度合并损益表（未审计）
# SRC: S-1/A 文本行 8657-8745「Quarterly Consolidated Statements of Operations」
#      列序：Q1'25 / Q2'25 / Q3'25 / Q4'25 / Q1'26 / Q2'26 / Q3'26
# 单位：百万美元
# ─────────────────────────────────────────────────────────────
QUARTERS = ["2025Q1", "2025Q2", "2025Q3", "2025Q4",
            "2026Q1", "2026Q2", "2026Q3"]

REVENUE = [376, 787, 1382, 2040, 4731, 11555, 16956]        # SRC 行 8670-8680
COMPUTE = [944, 1390, 2047, 2945, 3387, 5558, 9863]          # SRC 行 8682-8692
PERSONNEL = [218, 320, 489, 812, 1295, 1857, 1711]           # SRC 行 8694-8700
SALES_MKT = [24, 96, 202, 246, 1033, 2135, 2361]             # SRC 行 8704-8710
OTHER_OPEX = [125, 181, 233, 873, 683, 1031, 3588]           # SRC 行 8712-8718
TOTAL_OPEX = [1311, 1987, 4471, 4876, 6398, 10581, 17523]     # SRC 行 8720-8726
OPERATING_PL = [-935, -1200, -3089, -2836, -1667, 974, -567]  # SRC 行 8728-8734
NET_LOSS = [-6592, -6377, -12138, -16858, -14439, -66309, -23291]  # SRC 行 8760-8766
FV_CHANGE = [-5701, -5241, -9165, -14201, -12791, -59597, -21936]  # SRC 行 8740-8746

# 调整后经营（公司自披露 non-GAAP）SRC 行 9066-9130
ADJ_OP_INCOME = [-830, -1019, -1284, -1721, -617, 2235, 2463]
ADJ_OP_MARGIN = [-221, -129, -93, -84, -13, 19, 15]   # 百分比
SBC = [105, 181, 305, 574, 924, 1261, 1070]          # SRC 行 9100-9106
NONCASH_CHARITY = [0, 0, 0, 541, 126, 0, 1960]       # SRC 行 9108-9114

# ─────────────────────────────────────────────────────────────
# A 级输入 2：前九个月（截至 2026-09-30，未审计）
# SRC: S-1/A 文本行 21200-21245「Supplemental Operating Expense Information」
#      行 21246-21270「Consolidated Statements of Operations」（九个月）
# ─────────────────────────────────────────────────────────────
NINE_MONTH_2026 = {
    "revenue": 33242,          # SRC 行 7686 / 18013（九个月合计），CNBC 转述 33.24B
    "cost_of_revenue": 4812,   # SRC 行 21228
    "research_development": 19240,  # SRC 行 21231
    "sales_marketing": 6619,   # SRC 行 21232
    "general_administrative": 3831,   # SRC 行 21234
    "total_operating_expenses": 34502,  # SRC 行 21235
}
NINE_MONTH_2025 = {
    "revenue": 2545,           # SRC 行 19866（九个月合计）；= 376+787+1,382
    "cost_of_revenue": 1796,
    "research_development": 3594,
    "sales_marketing": 530,
    "general_administrative": 349,
    "total_operating_expenses": 7769,
}

# ─────────────────────────────────────────────────────────────
# A 级输入 3：合并资产负债表数据（截至 2026-09-30）
# SRC: S-1/A 文本行 1558-1570「Consolidated Balance Sheet Data（实际列）」
# 单位：百万美元
# ─────────────────────────────────────────────────────────────
BALANCE_20260930 = {
    "cash_and_st_investments": 131845,   # SRC 行 1562
    "working_capital": 129349,           # SRC 行 1565
    "total_assets": 154320,              # SRC 行 1567
    "total_liabilities": 146683,         # SRC 行 1568
    "redeemable_convertible_preferred": 157510,   # SRC 行 1569
    "additional_paid_in_capital": 6481,  # SRC 行 1570
    "accumulated_deficit": -156193,      # SRC 行 1571
    "total_stockholders_deficit": -149873,       # SRC 行 1572
}

# ─────────────────────────────────────────────────────────────
# A 级输入 4：承诺与流动性
# SRC: S-1/A 文本行 7192-7200（MD&A）、9890-9995（Contractual Obligations）
# 单位：百万美元
# ─────────────────────────────────────────────────────────────
COMMITMENTS = {
    "aggregate_committed_spend": 895400,        # SRC 行 7194 / 9891
    "purchase_commitments": 313819,             # SRC 行 9904 表
    "operating_leases": 4224,                   # SRC 行 9898 表
    "finance_leases": 1950,                    # SRC 行 9900 表
    "contractual_obligations_total": 319993,    # SRC 行 9907 表
    "leases_not_yet_commenced": 451200,        # SRC 行 9972
    "short_term_cancelable_1y": 17400,         # SRC 行 9968
    "post_9_30_commitments": 100200,           # SRC 行 9974
    "post_9_30_short_term_minimum": 6600,      # SRC 行 9976
    "due_within_12_months": 69800,             # SRC 行 9987
    "due_before_2030_12_31": 447500,           # SRC 行 7196
    "remaining_2031_to_2045": 895400 - 447500, # 派生
    "subject_to_termination_or_contingency": 213800,   # SRC 行 9897
    "excluded_no_fixed_dollar_low": 150000,    # SRC 行 9979
    "excluded_no_fixed_dollar_high": 175000,   # SRC 行 9979
    "arrangement_microsoft": 44900,            # SRC 行 9996
    "arrangement_google": 121300,              # SRC 行 9998
}
LIQUIDITY_20260930 = {
    "total_liquidity": 146600,   # SRC 行 7202
    "cash_and_equivalents": 95600,   # SRC 行 7202-7203
    "short_term_investments": 36300,   # SRC 行 7202-7203
    "a_and_r_credit_facility": 14800,  # SRC 行 7202-7203
    "npa_financing_capacity": 77000,   # SRC 行 7204
    "equity_commitments": 5000,        # SRC 行 7204
}

# 现金流量表（前九个月，截至 2026-09-30）SRC 行 19020-19035 / 9820-9826
CASH_FLOW_9M_2026 = {
    "operating": 6569,       # SRC 行 19012 / 9824
    "investing": -36546,     # SRC 行 9820-9822
    "financing": 110735,     # SRC 行 9826
    "purchases_of_ppe": -925,        # SRC 行 19026
    "prepayments_leased_assets": -1955,   # SRC 行 19028
}

# 参照项：Meta 表外承诺（#357，2026-10-27，10-Q 附注 10）
META_20261027 = {
    "off_balance_sheet_total": 824970,   # 3,557.3 + 4,545.2 + 147.2
    "leases_not_commenced": 355730,
    "non_cancelable_contracts": 454520,
    "contingent_cloud_purchase": 14720,
    "stockholders_equity": 272400,       # 3.03 倍反推口径见 #357 底稿
}


def usd100m(x_million):
    """百万美元 → 亿美元（保留 2 位）"""
    return round(x_million / 100.0, 2)


def main():
    r = {}

    # ── 1. 单位算力收入产出率序列 ────────────────────────────
    series = []
    for i, q in enumerate(QUARTERS):
        series.append({
            "quarter": q,
            "revenue_usd100m": usd100m(REVENUE[i]),
            "compute_usd100m": usd100m(COMPUTE[i]),
            "yield_usd": round(REVENUE[i] / COMPUTE[i], 4),
            "yield_rounded_2dp": round(REVENUE[i] / COMPUTE[i], 2),
            "operating_pl_usd100m": usd100m(OPERATING_PL[i]),
            "net_loss_usd100m": usd100m(NET_LOSS[i]),
            "adj_op_income_usd100m": usd100m(ADJ_OP_INCOME[i]),
            "adj_op_margin_pct": ADJ_OP_MARGIN[i],
        })
    r["yield_series"] = series

    # ── 2. Q3 vs Q2 拐点 ────────────────────────────────────
    q2, q3 = QUARTERS.index("2026Q2"), QUARTERS.index("2026Q3")
    rev_g = REVENUE[q3] / REVENUE[q2] - 1
    cmp_g = COMPUTE[q3] / COMPUTE[q2] - 1
    # 若算力按营收增速增长，Q3 算力应为多少
    cmp_at_rev_growth = COMPUTE[q2] * (REVENUE[q3] / REVENUE[q2])
    r["turning_point"] = {
        "revenue_qoq_pct": round(rev_g * 100, 2),
        "compute_qoq_pct": round(cmp_g * 100, 2),
        "yield_q2": round(REVENUE[q2] / COMPUTE[q2], 4),
        "yield_q3": round(REVENUE[q3] / COMPUTE[q3], 4),
        "yield_change_pct": round((REVENUE[q3] / COMPUTE[q3]) /
                                  (REVENUE[q2] / COMPUTE[q2]) * 100 - 100, 2),
        "compute_if_grew_with_revenue_usd100m": usd100m(cmp_at_rev_growth),
        "excess_compute_vs_rev_growth_usd100m": usd100m(COMPUTE[q3] - cmp_at_rev_growth),
        "short_term_compute_q3_usd100m": 5000,        # SRC 行 7165-7167
        "noncash_donation_q3_usd100m": 2000,          # SRC 行 7165-7167
        "sbc_q3_usd100m": usd100m(SBC[q3]),
        "noncash_charity_q3_usd100m": usd100m(NONCASH_CHARITY[q3]),
        "adj_op_margin_q2_pct": ADJ_OP_MARGIN[q2],
        "adj_op_margin_q3_pct": ADJ_OP_MARGIN[q3],
    }

    # ── 3. 前九个月口径 ──────────────────────────────────────
    nm = NINE_MONTH_2026
    r["nine_month_2026"] = {
        "revenue_usd100m": usd100m(nm["revenue"]),
        "cost_of_revenue_usd100m": usd100m(nm["cost_of_revenue"]),
        "research_development_usd100m": usd100m(nm["research_development"]),
        "total_operating_expenses_usd100m": usd100m(nm["total_operating_expenses"]),
        "operating_loss_usd100m": usd100m(nm["revenue"] - nm["total_operating_expenses"]),
        "gross_margin_pct": round((nm["revenue"] - nm["cost_of_revenue"]) /
                                  nm["revenue"] * 100, 2),
        "compute_sum_from_quarters_usd100m": usd100m(sum(COMPUTE[4:7])),
        "compute_yoy_increase_usd100m": usd100m(sum(COMPUTE[4:7]) - sum(COMPUTE[0:3])),
        "compute_yoy_pct": round((sum(COMPUTE[4:7]) / sum(COMPUTE[0:3]) - 1) * 100, 1),
        "rd_share_of_revenue_pct": round(nm["research_development"] / nm["revenue"] * 100, 2),
        "cost_of_revenue_share_pct": round(nm["cost_of_revenue"] / nm["revenue"] * 100, 2),
    }

    # ── 4. 承诺口径拼装（表内合计 → 8,954 亿美元）────────────
    parts = {
        "contractual_obligations_table": COMMITMENTS["contractual_obligations_total"],
        "leases_not_yet_commenced": COMMITMENTS["leases_not_yet_commenced"],
        "short_term_cancelable_1y": COMMITMENTS["short_term_cancelable_1y"],
        "post_9_30_commitments": COMMITMENTS["post_9_30_commitments"],
        "post_9_30_short_term_minimum": COMMITMENTS["post_9_30_short_term_minimum"],
    }
    total = sum(parts.values())
    r["commitment_reconciliation"] = {
        "parts_usd100m": {k: usd100m(v) for k, v in parts.items()},
        "sum_usd100m": usd100m(total),
        "filing_aggregate_usd100m": usd100m(COMMITMENTS["aggregate_committed_spend"]),
        "difference_usd100m": usd100m(total - COMMITMENTS["aggregate_committed_spend"]),
        "purchase_commitments_share_pct": round(
            COMMITMENTS["purchase_commitments"] / COMMITMENTS["aggregate_committed_spend"] * 100, 2),
        "leases_not_commenced_share_pct": round(
            COMMITMENTS["leases_not_yet_commenced"] / COMMITMENTS["aggregate_committed_spend"] * 100, 2),
        "due_12m_share_pct": round(
            COMMITMENTS["due_within_12_months"] / COMMITMENTS["aggregate_committed_spend"] * 100, 2),
        "due_before_2030_share_pct": round(
            COMMITMENTS["due_before_2030_12_31"] / COMMITMENTS["aggregate_committed_spend"] * 100, 2),
        "terminable_share_pct": round(
            COMMITMENTS["subject_to_termination_or_contingency"] /
            COMMITMENTS["aggregate_committed_spend"] * 100, 2),
        "excluded_range_usd100m": [usd100m(COMMITMENTS["excluded_no_fixed_dollar_low"]),
                                   usd100m(COMMITMENTS["excluded_no_fixed_dollar_high"])],
        "payment_horizon_years": 2045 - 2026,
    }

    # ── 5. 承诺 vs 表内资源 ──────────────────────────────────
    b = BALANCE_20260930
    r["off_balance_sheet_context"] = {
        "total_stockholders_equity_usd100m": usd100m(b["total_stockholders_deficit"]),
        "table_offbs_to_equity_ratio": None,   # 分母为负，比率不可计算
        "ratio_status": "股东权益为赤字（-1,498.73 亿美元），比值不可计算",
        "table_offbs_to_total_assets_ratio": round(
            COMMITMENTS["aggregate_committed_spend"] / b["total_assets"], 2),
        "table_offbs_to_redeemable_preferred_ratio": round(
            COMMITMENTS["aggregate_committed_spend"] / b["redeemable_convertible_preferred"], 2),
        "table_offbs_to_liquidity_ratio": round(
            COMMITMENTS["aggregate_committed_spend"] / LIQUIDITY_20260930["total_liquidity"], 2),
        "due_12m_to_9m_operating_cash_ratio": round(
            COMMITMENTS["due_within_12_months"] / CASH_FLOW_9M_2026["operating"], 2),
        "table_offbs_to_q3_revenue_multiple": round(
            COMMITMENTS["aggregate_committed_spend"] / REVENUE[q3], 2),
        "table_offbs_to_9m_revenue_multiple": round(
            COMMITMENTS["aggregate_committed_spend"] / nm["revenue"], 2),
        "q3_net_loss_usd100m": usd100m(NET_LOSS[q3]),
        "q3_operating_loss_usd100m": usd100m(OPERATING_PL[q3]),
        "q3_fair_value_change_usd100m": usd100m(FV_CHANGE[q3]),
        "q3_net_loss_minus_operating_loss_usd100m": usd100m(NET_LOSS[q3] - OPERATING_PL[q3]),
    }

    # ── 6. 与 Meta #357 的口径对照 ──────────────────────────
    anth = COMMITMENTS["aggregate_committed_spend"]
    meta = META_20261027["off_balance_sheet_total"]
    r["meta_comparison"] = {
        "anthropic_usd100m": usd100m(anth),
        "meta_usd100m": usd100m(meta),
        "difference_usd100m": usd100m(anth - meta),
        "ratio": round(anth / meta, 4),
        "meta_stockholders_equity_ratio": 3.03,
        "anthropic_equity_ratio": None,
        "comparability": "同概念（表外承诺合计上限）、不同披露颗粒度，非严格可比",
    }

    # ── 7. Anthropic Direct 现金流形状 ──────────────────────
    r["anthropic_direct"] = {
        "capex_9m_ppe_usd100m": usd100m(CASH_FLOW_9M_2026["purchases_of_ppe"]),
        "prepayments_leased_assets_9m_usd100m": usd100m(CASH_FLOW_9M_2026["prepayments_leased_assets"]),
        "operating_cf_9m_usd100m": usd100m(CASH_FLOW_9M_2026["operating"]),
        "investing_cf_9m_usd100m": usd100m(CASH_FLOW_9M_2026["investing"]),
        "financing_cf_9m_usd100m": usd100m(CASH_FLOW_9M_2026["financing"]),
        "liquidity_usd100m": usd100m(LIQUIDITY_20260930["total_liquidity"]),
        "npa_capacity_usd100m": usd100m(LIQUIDITY_20260930["npa_financing_capacity"]),
        "microsoft_commitment_usd100m": usd100m(COMMITMENTS["arrangement_microsoft"]),
        "google_commitment_usd100m": usd100m(COMMITMENTS["arrangement_google"]),
        "top2_arrangements_share_pct": round(
            (COMMITMENTS["arrangement_microsoft"] + COMMITMENTS["arrangement_google"]) /
            COMMITMENTS["aggregate_committed_spend"] * 100, 2),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\n写出：%s" % OUT)


if __name__ == "__main__":
    main()
