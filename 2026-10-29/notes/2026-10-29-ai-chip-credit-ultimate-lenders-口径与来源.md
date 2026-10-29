# 口径与来源台账 · #360「630 亿银行团与 290 亿担保——AI 芯片信贷的『最终贷款人』结构」

> 研析 · 2026-10-29 · V1
> 作品落盘：`shared/showcase/2026-10-29/research/2026-10-29-ai-chip-credit-ultimate-lenders.html`
> 追踪线：估值与资本
> 本台账遵循本期契约「来源硬约束」：**一手直取**与**二手转引**分栏标注，直取成功者记 HTTP 状态码与字节数，核不到者写「口径未证实」。

---

## 〇、开工前的三处口径预警（先于结论）

派单简报的三条核心事实，核对后有三处需要拆口径，否则会写错：

| # | 派单写法 | 核对结果 | 处理 |
|---|---|---|---|
| 1 | 「630 亿美元融资 + 博通担保最高 290 亿」像是一笔交易的两个数字 | **不是同一笔。** 630 亿是 2026-10-26 美银/黑石/花旗/摩根士丹利宣布的新 SPV；「最高 290 亿」是 **Reuters 引博通备案文件**所述的**前一笔** Apollo/黑石 350 亿交易里的担保上限 | 页面把两笔交易拆成两行、两个口径；290 亿明确标为「前笔交易」，不与 630 亿相加 |
| 2 | 630 亿看起来像「AI 芯片总投资」 | 630 亿是**承诺融资额度**，用途是 SPV 采购博通 XPU 加速器与网络设备并**租赁给 Anthropic**，交付自 2027 年起 | 页面红线：写「承诺融资规模」，并写明「采购融资 + 长期租赁安排」两段 |
| 3 | 「CoreWeave 总债务超 510 亿」 | CoreWeave 10-Q 一手：债务本金 **355.51 亿**；二手「约 520 亿」= 355.51 + 经营租赁 163.19 + 融资租赁 2.21 ≈ **520.9 亿**，是「全部付息义务」口径 | 页面以一手 355.51 亿为准，注明二手口径来源与差额构成 |

---

## 一、一手来源（页面直取成功 · 记 HTTP 状态码与字节数）

| # | 文件 | URL | HTTP | 字节数 | 本页用到的字段 |
|---|---|---|---|---|---|
| A1 | CoreWeave, Inc. 10-Q（2026-06-30 季度） | `https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm` | **200** | **2,197,630** | 债务附注全部 16 笔分层及各自有效利率；未来本金支付表（合计 355.51 亿）；总负债 356 亿口径原句；经营租赁负债 163.19 亿；Q2 利息支出净额 6.40 亿；Q2 营收 25.75 亿 |
| A2 | Anthropic, PBC S-1（2026-10-26 申报） | `https://www.sec.gov/Archives/edgar/data/2130357/000162828026067168/anthropicpbc-sx1.htm` | **200** | **14,169,254** | 未起租未折现租赁义务 3214 亿（2025-12-31 为 502 亿）；非可取消采购承诺 2656 亿（2025-12-31 为 545.59 亿）；RPO 108 亿；表内经营租赁负债 10.79 亿（流动 1.48 + 非流动 9.31）；现金及短期投资 1316.51 亿；H1 净亏 807 亿其中 724 亿为可转债等公允价值变动；H1 收入 163 亿；累计亏损 1329 亿；CSP 渠道收入占比 48% |

**A1 逐字原文（可直接回查）**
> "As of June 30, 2026, our total indebtedness was $35.6 billion and we had $10.0 billion of undrawn availability under our Revolving Credit Facility, DDTL 3.0 Facility, DDTL 4.0 Facility (as defined in the note) and DDTL 5.0 Facility."

> "As of June 30, 2026, the future principal payments for the Company's total debt were as follows (in millions): Remaining portion of 2026 $4,413 / 2027 6,184 / 2028 4,416 / 2029 2,421 / 2030 3,221 / Thereafter 14,896 / Total $35,551"

> 债务附注分层有效利率（节选）：DDTL 1.0 Facility Mar 2028 **15%**；DDTL 2.0 Aug 2030 11%；DDTL 2.1 Mar 2031 9%；DDTL 3.0 Aug 2030 9%；DDTL 5.0 Nov 2031 9%；2030 Notes 10%；2031 9.00% Notes 10%；2031 9.75% Notes 10%；2032 9.625% Notes 10%；2032 EUR Notes 9%；Convertible Senior Notes 2%；OEM and Software License Financing 11%；Magnetar Loan 12%；DDTL 4.0 7%。

**A2 逐字原文（可直接回查）**
> "As of December 31, 2025 and June 30, 2026 (unaudited), the Company had entered into lease agreements primarily related to compute and infrastructure capacity that had not yet commenced, with total estimated future undiscounted lease obligations of approximately $50.2 billion and $321.4 billion, respectively... These lease obligations will commence between 2026 and 2028, with lease terms ranging from less than one year to 20 years. The Company may elect to satisfy a portion of its obligations by issuing convertible promissory notes."

> "As of June 30, 2026 (unaudited), expected future fixed or minimum guaranteed commitments under these agreements were approximately $265.6 billion with terms ranging from one to 20 years."

> "Remaining performance obligations... As of June 30, 2026 (unaudited), remaining performance obligations amounted to $10.8 billion. The Company expects to recognize approximately 75% of this amount as revenue over the next 12 months."

> "As of June 30, 2026, we had cash and cash equivalents of $112.4 billion, $19.3 billion of short-term investments, and $3.2 billion available under the Credit Facility."

> "We have incurred net losses in each year since our founding, including a net loss of $1.5 billion, $8.3 billion, and $42.0 billion for the years ended December 31, 2023, 2024, and 2025, respectively, and $80.7 billion for the six months ended June 30, 2026... These net losses included change in fair value of convertible notes, derivative liabilities, and SAFEs of ... $72.4 billion for the six months ended June 30, 2026."

> "we have entered into purchase commitments and lease agreements, including short-term commitments, as well as leases not yet commenced, with an aggregate committed spend of more than $___ , substantially all of which is related to compute and infrastructure."

⚠️ **A2 的披露缺格**：S-1 HTML 中「aggregate committed spend of more than $ ___」这一句的**金额数字本身在页面 HTML 里是空格占位**（绝对定位的空 font 标签），不是抽取失败而是**原文渲染即无数字**。因此该数字**不可直取**，本页不引用，只用同一份文件里可直取的 3214 亿 / 2656 亿 / 108 亿三项。媒体口径「合计最高 7500 亿」标为**二手转引、口径未证实**。

---

## 二、二手来源（搜索摘要级 · 一律标「转引自搜索摘要，页面未直取」）

| # | 事实 | 来源（媒体） | 日期 | 页面直取 | 口径备注 |
|---|---|---|---|---|---|
| B1 | 美银、黑石、花旗、摩根士丹利宣布 630 亿交易；新设 SPV 采购博通 XPU 加速器与网络方案租赁给 Anthropic；交付 2027 年起；第一留置权由美银/花旗/摩根士丹利安排，黑石独家提供次级留置权承诺部分；博通提供 residual value support | 联合新闻稿（PRNewswire） | 2026-10-26 | 未直取 | 转引自搜索摘要 |
| B2 | 第一留置权约 435 亿，占 630 亿的 69%，系 Reuters 引两位知情人士；公告未披露完整拆分；博通未回应置评请求 | Reuters | 2026-10-26 | 未直取 | **消息人士口径**，非公司披露 |
| B3 | 博通用 residual value support 覆盖金额与第一留置权等额 | Quartz（引联合声明） | 2026-10-27 | 未直取 | 与 B2 同一数字，不同标签 |
| B4 | 博通残值支持覆盖 630 亿的约 72.5%（≈456.75 亿），敞口随租赁付款递减；前笔 350 亿交易覆盖 80%（≈280 亿） | UBS（Investing.com 转述） | 2026-10-27 | 未直取 | **与 B2/B3 差 21.75 亿**，页面并列两口径 |
| B5 | 前笔 Apollo/黑石 350 亿交易：分层为 A1 60 亿（国债+100bp）、A2 240 亿（票息 5.75%）、Class B 45 亿（8.5%）；博通对 A1/A2 提供信用增级与残值担保并对差额 100% 补偿；Atlas SP 出资 8 亿股权；约 150 亿将于 2027 年初向投资者开放 | Private Debt News Weekly #100 / AI Weekly / tradingkey | 2026-10 | 未直取 | 三源互证；分层合计 345 亿 + 股权 8 亿 ≈ 353 亿，与公告口径 350 亿的差额未披露 |
| B6 | 「前笔交易博通担保上限 290 亿」（引博通备案文件）；30 亿担保把 A1/A2 拉近博通自身投资级 | Reuters / tradingkey | 2026-10-26 起 | 未直取 | **290 亿属于前笔 350 亿交易**；本页红线之一 |
| B7 | Fitch 确认博通 A- 评级、展望正面；称博通涉及两笔客户结构、超 700 亿租赁付款的残值支持；称「近期 435 亿美元残值支持协议」；已建 RVS 敏感度水平；计划在 FYE27 调整后债务加 40 亿、FYE28 加 90 亿、FYE29 加约 150 亿；净担保负债 = 未偿担保租赁义务 − 机架公允市值，按加速折旧 2 年底 TPU pod 价值降约三分之二；预计博通 FY26 分红后自由现金流超 300 亿 | Fitch Ratings（研究页 + Yahoo 转述） | 2026-10-27 | 未直取 | 一手机构评级方法说明，转引自搜索摘要 |
| B8 | BofA 压测：平台扩至 20GW 时博通最大残值担保敞口可达 3700 亿、极端损失约 420 亿；首笔交易峰值敞口约 260 亿（约 2027 年 9 月）、最大损失约 29 亿；假设分期提款、5 年摊还、芯片价格年降 20%、违约时额外 25% 价格冲击；Moody's 7 月报告称六家跟踪公司资本开支 2026 年 7850 亿 → 2027 年近 1 万亿；警告短期内多笔交易将推高风险 | BigGo Finance 转述（原始为 BofA/Moody's 报告） | 2026-10 | 未直取 | **二手转述的卖方研究**，可信度标「中」，页面标为估算不作为断言层 |
| B9 | 博通季度收入 296 亿（+86%），AI 半导体收入 167 亿（+221%），FY27 AI 收入指引约 1150 亿；Anthropic 2027 年再部署 5GW TPU，预计成为其最大芯片客户 | Yahoo Finance / Investing.com | 2026-10-26/27 | 未直取 | 用于说明担保能力来源 |
| B10 | Meta：250 亿普通股（自 225 亿上调）+ 125 亿存托股 + 600 亿 ATM，合计约 975 亿；定价 625 美元/股；约 5 倍超额认购；英伟达认购 30 亿、AMD 10 亿，芯片商合计意向上限 50 亿；2026 资本开支 1350–1450 亿 | CNBC / Quartz / Bloomberg / Yahoo | 2026-10-26/27 | 未直取 | 仅作**股权端对照组**；Meta 自身表外承诺阶梯属 #357 题域，本页不展开 |
| B11 | CoreWeave 2032 年到期 12.5 亿美元债券收益率一度触及 15%、收于新高 14.5%（Chamath 图表）；当周最高 15.97%；CNBC 10-14 报道收益率逼近 15%；Q2 利息支出净额 6.40 亿（上年 2.67 亿），Q2 亏损税前 5.64 亿 | Yahoo Finance / CNBC / Wisevoter | 2026-10-14 / 10-20 | 未直取 | **二手收益率口径与一手合同利率并列**，日期口径已拆（10-14 与 10-20，不是 10-17） |
| B12 | 费半：2026-06-22 历史收盘高点 14634.72；2025-12-31 收盘 7083.13；10-16 收 11137.29（-3.83%，八连跌、2008 年以来最长）；10-22 单日 -6.72%；10-19 +1.61%、10-26 +2.82%、10-27 +3.33%（英为财情口径）；北京时间 10-28 收盘费半涨 3.6%、涨近 400 点（≈11483 点），连续两日成分股全线上涨；财联社 03:47 盘中报 11527.32（+4%） | Yahoo 财经历史数据 / 英为财情 investing.com / historyofmarket.com / 新浪转 21 世纪经济报道 / 财联社 | 2026-10 | 部分直取失败，**均为摘要转引** | 同一交易日三个口径，页面以「涨 3.6%、约 11483 点」为主口径并注明差异 |
| B13 | Anthropic S-1 媒体解读：H1 2026 净亏 807.48 亿，其中 723.88 亿来自可转债/衍生负债/SAFE 公允价值变动（占 89.6%）；非可取消采购承诺 2025 年末 546 亿 → 6/30/26 2656 亿；未折现租赁义务 502 亿 → 3214 亿；至少 4750 亿云算力采购承诺、其中至少 3899 亿承诺给亚马逊/字母表/SpaceXAI/微软；含芯片租赁后总承诺最高 7500 亿；RPO 108 亿中 75% 在未来 12 个月确认；与微软协议改为 2026-11 至 2033-05 至少消费 449 亿且除未交付批次或重大违约外不可取消 | CNBC / Yahoo Finance / tradingkey | 2026-10-26 | 未直取 | 7500 亿为媒体口径，**口径未证实**，不进断言层 |

---

## 三、交叉验证与口径判定表

| 争点 | 说法 1 | 说法 2 | 判定 |
|---|---|---|---|
| 630 亿里第一留置权多大 | Reuters：约 435 亿（占 69%），引两位知情人士 | QZ 引联合声明：博通 RVS 金额与第一留置权等额 | **同一笔 435 亿被两个标签描述**（第一留置权规模 / RVS 协议额），不是两个数字 |
| 博通担保覆盖比例 | Fitch：435 亿 RVS 协议 | UBS：72.5%（≈456.75 亿） | **同物异名（口径差 21.75 亿）**，页面并列，不取平均、不合并 |
| 290 亿属于哪笔交易 | 派单简报：与 630 亿并列 | Reuters 引博通备案：属**前笔** Apollo/黑石 350 亿交易 | **派单口径有误**，页面纠正 |
| 前期交易担保上限 | Reuters/博通备案：最高 290 亿 | UBS：占 350 亿的 80%（≈280 亿）；tradingkey：A1+A2 = 300 亿 | **同一笔的三个口径（280/290/300）**，页面写「约 280–300 亿区间」，并标明各归谁 |
| CoreWeave 总债务 | 二手：约 520 亿 | 一手 10-Q：本金 355.51 亿 | **同物异名**（债务 vs 债务+租赁）→ 差额 165.4 亿已拆解 |
| 费半 10-28 涨跌幅 | 英为财情：10-27 收 11452.2（+3.33%） | 新浪转 21 世纪：北京时间 10-28 收涨 3.6%、涨近 400 点（≈11483） | **收盘价序列口径差**，主口径取「涨 3.6%、约 11483 点」，另注英为财情口径 |

---

## 四、与 #351 / #357 的题域边界

- **#351（AI 信贷传染链 · 二级市场）**：讲债务 → 债价 → 股市 → 地缘的传导与地理层级。本页**不重复宏观段**：费半八连跌只作为「担保期权的对手方背景」出现一句，不写传染链叙事、不写韩国/印尼层级、不写长端贴现率。
- **#357（Meta 表外 8250 亿阶梯）**：讲单一厂商的表外承诺阶梯。本页的 Anthropic 侧数据**来自 S-1 一手**，与 Meta 10-Q 承诺表**不重叠**；Anthropic 只写到「表内经营租赁负债 10.79 亿 vs 未起租租赁义务 3214 亿」这一个机制点，**不铺阶梯、不算期限缺口**。Meta 只作为「股权端 vs 债务端」的结构对照出现，不展开其表外结构。
- 本页独占题域：**一级信贷供给结构** —— 谁放贷、怎么分层、谁担保、担保在二级市场怎么定价、残值市场是否存在。

---

## 五、诚实边界（不写进页面的不确定项）

1. 435 亿 / 456.75 亿两个担保口径**未取得博通或 SPV 的原始文件**（未直取），无法判定哪个是合同口径。
2. 630 亿交易的**最终提款规模、定价、SPV 内股权比例**均未披露。
3. 「残值市场不存在」是**机制推断**（定制 TPU pod 的第二买家只有 Anthropic 与 Google），非任何机构原文结论；页面标为研析判断。
4. BofA 的 3700 亿 / 420 亿压测是**二手转述的卖方研究**，非原始报告；页面标为估算、不进断言层。
5. Anthropic S-1 中「aggregate committed spend of more than $___」的金额在原文 HTML 中即为空格占位，**不可直取**；媒体口径「7500 亿」标口径未证实。
6. CoreWeave 二级收益率 14.5% / 15.97% 来自社交媒体图表与聚合站转述，**未取得交易级行情**；一手可验证的是 10-Q 里的合同有效利率（DDTL 1.0 = 15%）。

---

## 六、测算底稿

`calc_ultimate_lenders.py` → `calc_ultimate_lenders_result.json`（39 项，全部可复算）。
