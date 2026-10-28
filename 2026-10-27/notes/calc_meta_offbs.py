#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#357 / 选题393 —— Meta 表外承诺（8250 亿美元）测算底稿
单位：亿美元（除非另注）

数据来源层级见 同目录 来源核验_meta-offbs-V1-20261028.md：
  A = Meta 10-Q / Q3 财报披露数（转引自搜索摘要，页面未直取）
  B = 由 A 推导（团队测算）
  C = 机构估算（非公司口径，不作事实断言）
"""
import json

# ── A 级输入 ───────────────────────────────────────────────
LEASE_UNSTARTED   = 3557.0   # 未计入资产负债表的经营+融资租赁承诺
CONTRACTS         = 4545.0   # 截至 9/30 不可撤销短期与长期合同
CLOUD_CAP         = 147.0    # 未来五年云容量采购上限
DUE_2026          = 458.5    # 合同中 2026 年内到期
DUE_2027          = 1214.1   # 合同中 2027 年到期
RESTRICTED_CASH   = 108.0    # 由货币市场基金转入受限现金等价物
CASH_AND_SEC      = 824.49   # 期末现金、现金等价物及有价证券
TOTAL_ASSETS      = 4788.36
TOTAL_LIAB        = 2064.50
EQUITY            = 2723.86  # 归属母公司股东权益
LT_DEBT_NONCURR   = 809.22   # 非流动长期债务
LT_DEBT_FACE      = 840.00   # 长期债务面值总额
OP_LEASE_CUR      = 25.22    # 表内经营租赁负债·流动
OP_LEASE_NONCURR  = 286.51   # 表内经营租赁负债·非流动
Q3_OCF            = 327.86
Q3_CAPEX          = 349.06
Q3_FCF            = -21.20
M9_OCF            = 968.73
CAPEX_LOW, CAPEX_HIGH = 1350.0, 1450.0
Q4_REV_MID        = 745.0    # Q4 营收指引中值
REV_GROWTH_Q4     = 0.24     # Q4 营收指引同比增速（中值口径）
MKT_CAP           = 16400.0  # 市值（StockAnalysis，10-23，1.64 万亿美元）
CDS_BP            = 119.3    # 五年期 CDS（ICE Data Services，10-22 盘中）
JUL_COMMITMENT    = 7000.0   # 7 月口径同类承诺

# ── C 级输入（机构估算，不得作事实断言）────────────────────
CAPEX_2027_EST    = 2050.0   # 美银对 2027 资本开支的预测

R = {}

# ── 1 承诺总额的三种拆法 ───────────────────────────────────
R['承诺合计上限']            = LEASE_UNSTARTED + CONTRACTS + CLOUD_CAP
R['租赁+合同']               = LEASE_UNSTARTED + CONTRACTS
R['三月增量']                = R['承诺合计上限'] - JUL_COMMITMENT
R['三月增量_百分比']         = R['三月增量'] / JUL_COMMITMENT

# ── 2 杠杆比：表外 vs 表内 ─────────────────────────────────
R['承诺_长期债务_倍']        = R['承诺合计上限'] / LT_DEBT_NONCURR
R['承诺_股东权益_倍']        = R['承诺合计上限'] / EQUITY
R['承诺_现金_倍']            = R['承诺合计上限'] / CASH_AND_SEC
R['承诺_市值_百分比']        = R['承诺合计上限'] / MKT_CAP
R['未起租租赁_表内经营租赁_倍'] = LEASE_UNSTARTED / (OP_LEASE_CUR + OP_LEASE_NONCURR)
R['表内经营租赁负债合计']     = OP_LEASE_CUR + OP_LEASE_NONCURR
R['租赁总敞口_含未起租']      = LEASE_UNSTARTED + OP_LEASE_CUR + OP_LEASE_NONCURR
R['租赁总敞口_股东权益_倍']   = R['租赁总敞口_含未起租'] / EQUITY

# ── 3 上限情景：未起租租赁全部上表（名义额、不折现）────────
R['现_负债资产比']           = TOTAL_LIAB / TOTAL_ASSETS
R['现_债务资产比']           = LT_DEBT_NONCURR / TOTAL_ASSETS
R['现_债务权益比']           = LT_DEBT_NONCURR / EQUITY
R['上限_负债']               = TOTAL_LIAB + LEASE_UNSTARTED
R['上限_资产']               = TOTAL_ASSETS + LEASE_UNSTARTED
R['上限_负债资产比']         = R['上限_负债'] / R['上限_资产']
R['上限_债务资产比']         = (LT_DEBT_NONCURR + LEASE_UNSTARTED) / R['上限_资产']
R['上限_债务权益比']         = (LT_DEBT_NONCURR + LEASE_UNSTARTED) / EQUITY

# ── 4 到期阶梯与现金覆盖 ───────────────────────────────────
FREE_CASH = CASH_AND_SEC - RESTRICTED_CASH          # 可自由支配现金（近似口径）
R['可自由支配现金']         = FREE_CASH
R['2026到期_现金覆盖']      = DUE_2026 / CASH_AND_SEC
R['2026到期_自由现金覆盖']  = DUE_2026 / FREE_CASH
R['两年到期合计']           = DUE_2026 + DUE_2027
R['两年到期_现金覆盖']      = R['两年到期合计'] / CASH_AND_SEC
R['两年到期_缺口_对现金']   = R['两年到期合计'] - CASH_AND_SEC
R['两年到期_自由现金覆盖']  = R['两年到期合计'] / FREE_CASH
R['两年到期_缺口_对自由现金'] = R['两年到期合计'] - FREE_CASH
R['受限现金_两年到期占比']  = RESTRICTED_CASH / R['两年到期合计']
R['2026到期_占全年capex中值'] = DUE_2026 / ((CAPEX_LOW + CAPEX_HIGH) / 2)
R['两年到期_占全年capex中值'] = R['两年到期合计'] / ((CAPEX_LOW + CAPEX_HIGH) / 2)

# ── 5 2026 全年自由现金流转负的临界值 ─────────────────────
CAPEX_MID = (CAPEX_LOW + CAPEX_HIGH) / 2
R['Q4需OCF_capex中值']      = CAPEX_MID - M9_OCF
R['Q4需OCF_capex上限']      = CAPEX_HIGH - M9_OCF
R['Q4需OCF中值_较Q3增幅']   = R['Q4需OCF_capex中值'] / Q3_OCF - 1
R['Q4需OCF上限_较Q3增幅']   = R['Q4需OCF_capex上限'] / Q3_OCF - 1
OCF_2026_FLAT = M9_OCF + Q3_OCF                        # Q4 与 Q3 持平
R['全年OCF_Q4持平']         = OCF_2026_FLAT
R['全年FCF_Q4持平_capex中值'] = OCF_2026_FLAT - CAPEX_MID
R['全年FCF_Q4持平_capex上限'] = OCF_2026_FLAT - CAPEX_HIGH

# ── 6 2027 撞墙测算（C 级 capex 估算）─────────────────────
OCF_2027 = OCF_2026_FLAT * (1 + REV_GROWTH_Q4)
R['2027外推OCF']            = OCF_2027
R['2027现金需求_capex+合同到期'] = CAPEX_2027_EST + DUE_2027
R['2027融资缺口']            = R['2027现金需求_capex+合同到期'] - OCF_2027
R['缺口_对在手现金_倍']     = R['2027融资缺口'] / CASH_AND_SEC
R['缺口_对在手现金_倍_扣全年FCF赤字'] = R['2027融资缺口'] / (CASH_AND_SEC + R['全年FCF_Q4持平_capex中值'])
R['2027合同到期_占外推OCF'] = DUE_2027 / OCF_2027
R['发债笔数_按250亿']       = R['2027融资缺口'] / 250.0
R['CDS年化成本_840亿']       = LT_DEBT_FACE * CDS_BP / 10000
R['CDS年化成本_若2000亿']   = 2000.0 * CDS_BP / 10000

def fmt(x):
    return f"{x:,.2f}"

print("=" * 78)
print("#357 Meta 表外承诺测算底稿（单位：亿美元）")
print("=" * 78)
for k, v in R.items():
    print(f"{k:36s} {fmt(v) if isinstance(v, float) else v}")
print("=" * 78)
out = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in R.items()}
with open("calc_meta_offbs_result.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("已写出 calc_meta_offbs_result.json")
