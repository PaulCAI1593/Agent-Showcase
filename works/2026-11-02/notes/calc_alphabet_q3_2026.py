#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研析测算底稿 · Alphabet 2026 Q3「AI 搜索变现缺口」选题
所有一手数取自 SEC EDGAR：
  EX-99.1 Q3 2026  https://www.sec.gov/Archives/edgar/data/1652044/000165204426000080/googexhibit991q32026.htm
  EX-99.1 Q2 2026  .../000165204426000066/googexhibit991q22026.htm
  EX-99.1 Q1 2026  .../000165204426000043/googexhibit991q12026.htm
  EX-99.1 Q4 2025  .../000165204426000012/googexhibit991q42025.htm
  10-Q  2026 Q3    .../000165204426000084/goog-20260930.htm
单位：百万美元（原始披露口径）。派生量单位在 key 后标注。
"""
import json

M = 1e8  # 百万美元 → 亿美元

# ── 一手：损益（EX-99.1 Q3 2026）──────────────────────────────
rev_q3_26, rev_q3_25 = 127577, 102346
op_q3_26, op_q3_25 = 40576, 31228
ni_common_q3_26, ni_common_q3_25 = 26170, 34979
ni_q3_26 = 26468                      # 现金流量表口径的净利润
eps_q3_26, eps_q3_25 = 2.12, 2.87
search_q3_26, search_q3_25 = 63350, 56567
yt_ads_q3_26, yt_ads_q3_25 = 11207, 10261
ads_q3_26, ads_q3_25 = 82012, 74182
services_q3_26, services_q3_25 = 96302, 87052
cloud_q3_26, cloud_q3_25 = 30709, 15157
cloud_op_q3_26, cloud_op_q3_25 = 11121, 3594
svc_op_q3_26, svc_op_q3_25 = 39157, 33527
alpha_level_q3_26, alpha_level_q3_25 = -7655, -4467
equity_sec_loss_q3_26 = 8664          # 权益证券投资损失（正数=损失）
equity_sec_ni_hit = 6700              # 公司披露：对净利润的影响
equity_sec_eps_hit = 0.55             # 公司披露：对摊薄 EPS 的影响

# ── 一手：现金流（EX-99.1 Q3 2026 · FCF 对账表）────────────────
fcf_q = {                            # 季度: (经营现金流, 资本开支, 自由现金流)
    "Q4 2025": (52402, 27851, 24551),
    "Q1 2026": (45790, 35674, 10116),
    "Q2 2026": (39069, 44924, -5855),
    "Q3 2026": (42290, 51355, -9065),
}
ttm_ocf, ttm_capex, ttm_fcf = 179551, 159804, 19747
ytd_capex_2026 = 131953
ytd_ocf_2026 = 127149
ocf_q3_25, capex_q3_25 = 48414, 23953

# ── 一手：融资（EX-99.1 Q3 2026 · 现金流量表）──────────────────
q3_debt_issued_net, q3_debt_repaid = 28996, 3626
q3_equity_issued_net = 12371
q3_buyback, q3_buyback_py = 0, 11504
ytd_debt_issued_net = 85222
ytd_debt_repaid = 88879
ytd_common_issued_net = 42870
ytd_preferred_issued_net = 19063

# ── 一手：资产负债表（EX-99.1 Q3 2026）─────────────────────────
cash_sec_q3_26, cash_sec_2025 = 265098, 126843
ltd_q3_26, ltd_2025 = 125102, 46547
inv_q3_26, inv_2025 = 13308, 2439
ppe_q3_26, ppe_2025 = 372827, 246597
assets_q3_26, assets_2025 = 1003312, 595281
equity_q3_26, equity_2025 = 677549, 415265

# ── 一手：未来承诺（10-Q + 电话会）────────────────────────────
purchase_commitments_10q = 924400     # 10-Q：$924.4B 重大采购承诺
leases_not_commenced_10q = 130500    # 10-Q：$130.5B 尚未开始履行的租赁付款
purchase_commitments_call = 924000   # 电话会 CFO：$924B
other_obligations_call = 152000      # 电话会 CFO：未开始租赁及其他义务 $152B
rpo_total, rpo_cloud = 567700, 560800
due_within_12m = 213400

# ── 一手：2026 年 6 月股权融资（10-Q 附注）─────────────────────
jun_public_offering_net = 20500      # 公开发行净额
jun_private_placement_net = 10000    # 伯克希尔定向净额
jun_preferred_net = 19063            # 强制可转优先股净额

# ── 一手：分部与季度序列（各季 EX-99.1）───────────────────────
search_series = {"Q4 2025": (54034, 63073), "Q1 2026": (50702, 60399),
                 "Q2 2026": (54190, 63271), "Q3 2026": (56567, 63350)}
cloud_series = {"Q4 2025": (11955, 17664), "Q1 2026": (12260, 20028),
                "Q2 2026": (13624, 24768), "Q3 2026": (15157, 30709)}
cloud_op_series = {"Q4 2025": 5313, "Q1 2026": 6598, "Q2 2026": 8814, "Q3 2026": 11121}

# ── 一手：变现指标（10-Q 变现指标表，三季度同比）──────────────
paid_clicks_q3 = 8                   # %
cpc_q3 = 4                           # %

out = {}
def pct(a, b):
    return round((a / b - 1) * 100, 1)

# 1) 搜索：增速下台阶 + 环比停滞
out["搜索同比增速(%)"] = {k: pct(v[1], v[0]) for k, v in search_series.items()}
out["搜索环比(%)"] = {
    "Q1 2026 vs Q4 2025": pct(search_series["Q1 2026"][1], search_series["Q4 2025"][1]),
    "Q2 2026 vs Q1 2026": pct(search_series["Q2 2026"][1], search_series["Q1 2026"][1]),
    "Q3 2026 vs Q2 2026": pct(search_series["Q3 2026"][1], search_series["Q2 2026"][1]),
}
out["搜索广告占总营收(%)"] = round(search_q3_26 / rev_q3_26 * 100, 1)
out["搜索广告占广告收入(%)"] = round(search_q3_26 / ads_q3_26 * 100, 1)

# 2) 云：加速 + 利润结构
out["云同比增速(%)"] = {k: pct(v[1], v[0]) for k, v in cloud_series.items()}
out["云环比(%)"] = {
    "Q2 2026 vs Q1 2026": pct(cloud_series["Q2 2026"][1], cloud_series["Q1 2026"][1]),
    "Q3 2026 vs Q2 2026": pct(cloud_series["Q3 2026"][1], cloud_series["Q2 2026"][1]),
}
out["云营业利润率(%)"] = {
    "Q3 2025": round(cloud_op_q3_25 / cloud_q3_25 * 100, 1),
    "Q3 2026": round(cloud_op_q3_26 / cloud_q3_26 * 100, 1),
}
out["Google Services 营业利润率(%)"] = {
    "Q3 2025": round(svc_op_q3_25 / services_q3_25 * 100, 1),
    "Q3 2026": round(svc_op_q3_26 / services_q3_26 * 100, 1),
}
out["云营业利润 / 搜索广告收入(%)"] = round(cloud_op_q3_26 / search_q3_26 * 100, 1)
out["Alphabet 层面活动亏损同比(%)"] = pct(alpha_level_q3_26, alpha_level_q3_25)

# 3) 变现缺口代理：查询量 5 年最高 vs 付费点击 +8% vs 收入 +12%
out["搜索变现三角(%)"] = {
    "查询量同比": "5 年来最高（管理层口径，未给数值）",
    "付费点击同比": paid_clicks_q3,
    "单次点击成本同比": cpc_q3,
    "搜索收入同比": pct(search_q3_26, search_q3_25),
}

# 4) 现金流：负值 + Q4 隐含资本开支
out["自由现金流(百万美元)"] = {k: v[2] for k, v in fcf_q.items()}
out["自由现金流 TTM(百万美元)"] = ttm_fcf
out["Q3 FCF 同比变动(百万美元)"] = fcf_q["Q3 2026"][2] - (ocf_q3_25 - capex_q3_25)
out["2026 前三季资本开支(百万美元)"] = ytd_capex_2026
out["2026 前三季自由现金流(百万美元)"] = ytd_ocf_2026 - ytd_capex_2026
out["Q4 隐含资本开支(百万美元)"] = {
    "指引下限 1950 亿美元": 195000 - ytd_capex_2026,
    "指引上限 2050 亿美元": 205000 - ytd_capex_2026,
}
out["Q4 隐含资本开支 / Q3 单季(倍)"] = {
    "下限": round((195000 - ytd_capex_2026) / capex_q3_25 if False else (195000 - ytd_capex_2026) / 51355, 2),
    "上限": round((205000 - ytd_capex_2026) / 51355, 2),
}
out["资本开支占营收(%)"] = {
    "Q3 2025": round(capex_q3_25 / rev_q3_25 * 100, 1),
    "Q3 2026": round(51355 / rev_q3_26 * 100, 1),
}

# 5) 现金与融资
out["现金及有价证券(百万美元)"] = {"2025-12-31": cash_sec_2025, "2026-09-30": cash_sec_q3_26}
out["现金及有价证券净增(百万美元)"] = cash_sec_q3_26 - cash_sec_2025
out["长期债务(百万美元)"] = {"2025-12-31": ltd_2025, "2026-09-30": ltd_q3_26}
out["长期债务净增(百万美元)"] = ltd_q3_26 - ltd_2025
out["长期债务增幅(%)"] = pct(ltd_q3_26, ltd_2025)
out["Q3 外部融资净流入(百万美元)"] = q3_debt_issued_net + q3_equity_issued_net
out["Q3 股票回购(百万美元)"] = {"2026": q3_buyback, "2025": q3_buyback_py}
out["前三季外部融资净流入(百万美元)"] = (
    ytd_debt_issued_net + ytd_common_issued_net + ytd_preferred_issued_net - ytd_debt_repaid)
out["2026 年 6 月股权融资合计净额(百万美元)"] = (
    jun_public_offering_net + jun_private_placement_net + jun_preferred_net)
out["总资产(百万美元)"] = {"2025-12-31": assets_2025, "2026-09-30": assets_q3_26}
out["总资产增幅(%)"] = pct(assets_q3_26, assets_2025)
out["固定资产净额(百万美元)"] = {"2025-12-31": ppe_2025, "2026-09-30": ppe_q3_26}
out["股东权益(百万美元)"] = {"2025-12-31": equity_2025, "2026-09-30": equity_q3_26}
out["库存(百万美元)"] = {"2025-12-31": inv_2025, "2026-09-30": inv_q3_26}
out["库存净增(百万美元)"] = inv_q3_26 - inv_2025

# 6) 未来承诺
out["未来承诺合计(百万美元)"] = {
    "10-Q 口径：采购承诺 + 未开始租赁": purchase_commitments_10q + leases_not_commenced_10q,
    "电话会口径：采购承诺 + 未开始租赁及其他义务": purchase_commitments_call + other_obligations_call,
}
out["12 个月内到期采购承诺(百万美元)"] = due_within_12m
out["云剩余履约义务(百万美元)"] = {"合计": rpo_total, "其中 Google Cloud": rpo_cloud}

# 7) 利润质量：股权投资的拖累
out["剔除权益证券损失后摊薄 EPS(美元)"] = round(eps_q3_26 + equity_sec_eps_hit, 2)
out["权益证券损失对净利润的影响(百万美元)"] = equity_sec_ni_hit
out["净利润同比(%)"] = pct(ni_common_q3_26, ni_common_q3_25)
out["摊薄 EPS 同比(%)"] = pct(eps_q3_26, eps_q3_25)
out["营业利润同比(%)"] = pct(op_q3_26, op_q3_25)
out["营收同比(%)"] = pct(rev_q3_26, rev_q3_25)

# 8) 与预期的缺口（二手共识，见口径台账）
out["与共识缺口(百万美元)"] = {
    "营收": rev_q3_26 - 128220,
    "搜索广告": search_q3_26 - 64960,
    "广告合计": ads_q3_26 - 83570,
    "云": cloud_q3_26 - 29100,
    "自由现金流(共识 -27 亿)": fcf_q["Q3 2026"][2] - (-2700),
    "资本开支(共识 550.9 亿)": 51355 - 55090,
}

for k, v in out.items():
    print(f"{k}: {v}")
print("\n--- 换算为亿美元 ---")
print("营收", round(rev_q3_26 / M, 2), "搜索", round(search_q3_26 / M, 2),
      "云", round(cloud_q3_26 / M, 2), "capex", round(51355 / M, 2),
      "FCF", round(fcf_q["Q3 2026"][2] / M, 2))
print("长期债务", round(ltd_q3_26 / M, 2), "现金及有价证券", round(cash_sec_q3_26 / M, 2),
      "采购承诺", round(purchase_commitments_10q / M, 2), "未开始租赁", round(leases_not_commenced_10q / M, 2))
print("Q3 外部融资净流入", round((q3_debt_issued_net + q3_equity_issued_net) / M, 2),
      "前三季", round(out["前三季外部融资净流入(百万美元)"] / M, 2),
      "6 月股权融资", round(out["2026 年 6 月股权融资合计净额(百万美元)"] / M, 2))

json.dump(out, open("/app/working/shared/showcase/2026-11-02/notes/calc_alphabet_q3_2026_result.json", "w"),
          ensure_ascii=False, indent=2)
print("\n结果已写入 calc_alphabet_q3_2026_result.json")
