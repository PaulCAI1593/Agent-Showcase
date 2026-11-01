#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测算底稿 · 选题404「拉斯塔努拉之后，中东风险溢价为何不涨反跌」
数析 · 2026-10-30 · V1

口径来源见同目录 `2026-10-29-ras-tanura-risk-premium-口径与来源.md`。
本脚本只做算术，不做判断。所有输入值都在 INPUTS 里标注出处。

运行：python3 calc_ras_tanura_premium.py
输出：calc_ras_tanura_premium_result.json
"""

import json
import os

# ── 输入（每项标注出处） ───────────────────────────────────────────────
INPUTS = {
    # 炼厂加工产能（Reuters / CNBC / houseofsaud 引 MEED）
    "refinery_capacity_bpd": 550_000,
    # 全球石油供应，2026-09（IEA Oil Market Report 2026-10，转引自搜索摘要）
    "global_supply_sep26_mbd": 102.3,
    # 全球石油供应，下半年均值（IEA 同上）
    "global_supply_h2_26_mbd": 101.4,
    # EIA 预计 4Q26 中东停产产量均值（STEO 2026-10-06，一手 HTTP 200）
    "shut_in_4q26_mbd": 4.5,
    # EIA 估算东西输油管战前经延布外运量（STEO 2026-10-06，一手 HTTP 200）
    "east_west_pipeline_bpd": 5_000_000,
    # 结算价（CommoPlast 结算表 / CNBC / TradingNews，转引）
    "brent_1027": 113.88,
    "wti_1027": 99.90,
    "brent_1028": 115.30,
    "wti_1028": 101.79,
    # 日变动额（CommoPlast 结算表 / TradingNews，转引）
    "brent_1027_change_usd": -1.93,
    "wti_1027_change_usd": -1.86,
    "brent_1028_change_usd": 1.42,
    "wti_1028_change_usd": 1.89,
    # EIA 9/15 布伦特现货盘中最高（STEO 2026-10-06，一手 HTTP 200）
    "brent_sep15_spot_high": 131.0,
    # EIA 4Q26 布伦特现货均价预测（STEO 2026-10-06，一手 HTTP 200）
    "eia_brent_4q26_avg": 105.0,
    # 2019 Abqaiq（EIA 一手 + CRS，转引）
    "abqaiq_outage_mbd": 5.7,
    "abqaiq_brent_0913": 60.22,
    "abqaiq_brent_0916": 69.02,
}


def pct(numer, denom):
    """百分比，保留两位小数。"""
    return round(numer / denom * 100, 2)


def r(x, n=2):
    return round(x, n)


def main():
    i = INPUTS
    cap = i["refinery_capacity_bpd"]
    out = {}

    # ── 1. 口径②：55 万桶/日在全球供应中的占比 ────────────────────────
    out["capacity_share_of_global_supply"] = {
        "vs_sep26_global_supply_102_3_mbd": pct(cap, i["global_supply_sep26_mbd"] * 1e6),
        "vs_h2_26_global_supply_101_4_mbd": pct(cap, i["global_supply_h2_26_mbd"] * 1e6),
        "note": "55 万桶/日 是炼厂加工产能，占比口径，不是全球占比宣称",
    }

    # ── 2. 口径②：与已发生的更大中断对比 ────────────────────────────
    out["capacity_vs_bigger_disruptions"] = {
        "share_of_eia_4q26_shut_in_4_5_mbd": pct(cap, i["shut_in_4q26_mbd"] * 1e6),
        "share_of_east_west_pipeline_5_0_mbd": pct(cap, i["east_west_pipeline_bpd"]),
        "note": "该炼厂规模小于东西输油管绕行能力（500 万桶/日）与其一",
    }

    # ── 3. 价格序列：10-27 下跌 → 10-28 反弹 ────────────────────────
    brent_1026_settle = r(i["brent_1027"] - i["brent_1027_change_usd"])
    out["price_path"] = {
        "brent_1026_settle_derived": brent_1026_settle,
        "brent_1027_change_usd": i["brent_1027_change_usd"],
        "brent_1027_change_pct": pct(i["brent_1027_change_usd"], brent_1026_settle),
        "wti_1027_change_usd": i["wti_1027_change_usd"],
        "wti_1027_change_pct": pct(i["wti_1027_change_usd"],
                                   r(i["wti_1027"] - i["wti_1027_change_usd"])),
        "brent_1028_change_usd": i["brent_1028_change_usd"],
        "brent_1028_change_pct": pct(i["brent_1028_change_usd"], i["brent_1027"]),
        "wti_1028_change_usd": i["wti_1028_change_usd"],
        "wti_1028_change_pct": pct(i["wti_1028_change_usd"], i["wti_1027"]),
        "brent_1028_intraday_high": 115.90,
        "brent_1028_intraday_high_pct": pct(115.90 - i["brent_1027"], i["brent_1027"]),
        "note": "10-27 前结算由结算价与变动额反推；10-28 盘中高点 115.90（+1.8%）",
    }

    # ── 4. 跨大西洋价差：10-27 → 10-28 ──────────────────────────────
    s27 = r(i["brent_1027"] - i["wti_1027"])
    s28 = r(i["brent_1028"] - i["wti_1028"])
    out["transatlantic_spread"] = {
        "brent_minus_wti_1027": s27,
        "brent_minus_wti_1028": s28,
        "narrowing_usd": r(s27 - s28),
        "cross_check": "CommoPlast 结算表给出 13.98；TradingNews 给出 13.51",
    }

    # ── 5. 风险溢价回落幅度：9/15 现货盘中高点 → 10/27 结算 ─────────
    out["premium_giveback"] = {
        "brent_sep15_spot_high": i["brent_sep15_spot_high"],
        "brent_1027_settle": i["brent_1027"],
        "giveback_usd": r(i["brent_sep15_spot_high"] - i["brent_1027"]),
        "giveback_pct": pct(i["brent_sep15_spot_high"] - i["brent_1027"], i["brent_sep15_spot_high"]),
        "eia_4q26_forecast_avg": i["eia_brent_4q26_avg"],
        "note": "EIA 10/06 预测 4Q26 均价 105 美元，并称油价将总体从 10 月初均价回落",
    }

    # ── 6. 口径③：2019 Abqaiq 历史类比 ──────────────────────────────
    out["abqaiq_2019_historical_analogy"] = {
        "outage_mbd": i["abqaiq_outage_mbd"],
        "brent_0913_to_0916_pct": pct(
            i["abqaiq_brent_0916"] - i["abqaiq_brent_0913"], i["abqaiq_brent_0913"]),
        "brent_0913": i["abqaiq_brent_0913"],
        "brent_0916": i["abqaiq_brent_0916"],
        "ratio_2019_outage_to_2026_capacity": r(
            i["abqaiq_outage_mbd"] * 1e6 / cap, 1),
        "note": "历史类比，非本次参照基准；2019 的定价前提是产量真的停了",
    }

    result = {
        "topic": "拉斯塔努拉之后，中东风险溢价为何不涨反跌",
        "issue": "404",
        "author": "数析",
        "as_of": "2026-10-30 05:00 Asia/Shanghai",
        "inputs": INPUTS,
        "results": out,
    }

    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "calc_ras_tanura_premium_result.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("\n写入:", path)


if __name__ == "__main__":
    main()
