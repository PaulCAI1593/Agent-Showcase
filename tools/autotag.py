#!/usr/bin/env python3
"""为 enrich.json 中缺失 highlights 的作品，从标题自动派生标签。

只补 highlights 为空的条目；已有标签一律不动（人工标签优先）。
关键词表为智囊团 AI/产业领域常用词，按出现顺序取前 4 个。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENRICH = os.path.join(ROOT, "enrich.json")

KEYWORDS = [
    "AI Agent", "智能体", "人形机器人", "机器人", "自动驾驶", "具身智能",
    "开源模型", "闭源", "大模型", "多模态", "推理模型", "小模型", "模型",
    "AI芯片", "算力", "GPU", "HBM", "存储", "内存", "半导体", "晶圆",
    "AI普惠化", "价格战", "Token", "推理成本", "订阅", "付费",
    "新质生产力", "就业", "职场", "组织", "治理", "监管", "合规", "伦理",
    "安全", "对齐", "越权", "沙箱", "逃逸", "红队", "漏洞",
    "OpenAI", "Anthropic", "英伟达", "NVIDIA", "谷歌", "Google", "苹果", "Apple",
    "微软", "Meta", "特斯拉", "三星", "华为", "字节", "腾讯", "阿里", "百度",
    "DeepSeek", "开源", "闭源", "商业化", "融资", "IPO", "估值", "上市",
    "美联储", "降息", "加息", "CPI", "通胀", "股市", "债市", "汇率", "关税",
    "石油", "能源", "锂电", "光伏", "新能源", "碳排放", "电网", "稀土",
    "中东", "伊朗", "以色列", "胡塞", "沙特", "霍尔木兹", "俄乌", "制裁", "地缘",
    "台海", "南海", "贸易", "供应链", "产业链", "制造业", "出口管制",
    "教育", "医疗", "金融", "零售", "电商", "游戏", "内容", "影视", "社交",
    "医疗AI", "AI医疗", "AI教育", "AI金融", "AI搜索", "AI编程", "编程助手",
    "数字人", "AI陪伴", "AI硬件", "AI眼镜", "AI手机", "AI PC", "端侧AI", "推理",
    "生成式", "AIGC", "漫剧", "短剧", "营销", "增长", "获客",
    "云", "数据中心", "电力", "核能", "核电", "水利", "基建",
]


def derive(title, desc):
    text = f"{title} {desc}"
    hits = []
    for kw in KEYWORDS:
        if kw in text and kw not in hits:
            hits.append(kw)
        if len(hits) >= 4:
            break
    if not hits:
        # 兜底：取标题前两个词组
        parts = re.split(r"[·：:，,、—-]", title)
        hits = [p.strip() for p in parts if 2 <= len(p.strip()) <= 8][:2]
    return hits


def main():
    with open(ENRICH, encoding="utf-8") as f:
        data = json.load(f)
    works = data["works"] if "works" in data else data

    filled = 0
    for w in works:
        if w.get("highlights"):
            continue
        fp = os.path.join(ROOT, w["file"])
        title = w.get("title") or ""
        if not title and os.path.exists(fp):
            with open(fp, encoding="utf-8", errors="ignore") as f:
                head = f.read(4000)
            m = re.search(r"<title>(.*?)</title>", head, re.S | re.I)
            title = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        w["highlights"] = derive(title, w.get("description", ""))
        filled += 1

    with open(ENRICH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"补齐 highlights: {filled} 件，共 {len(works)} 件")


if __name__ == "__main__":
    main()
