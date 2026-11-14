#!/usr/bin/env python3
"""对比度复测：解析 linear-gradient 色标（取最差色标做保守判定）。

用法： python3 2026-11-09-model-codenamedecryption-contrast.py
输出： JSON，列出全部 <4.5:1（大字 <3:1）的可见文本节点与最差色标比值。
"""
import json
import os
import re

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
URL = "file://" + os.path.join(
    ROOT, "works/2026-11-09/creative/2026-11-09-model-codenamedecryption.html")

JS = r"""
() => {
  const hex = h => { h=h.replace('#',''); if(h.length===3) h=h.split('').map(c=>c+c).join('');
    return {r:parseInt(h.slice(0,2),16), g:parseInt(h.slice(2,4),16), b:parseInt(h.slice(4,6),16), a:1}; };
  const parse = c => { const m=String(c).match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
    return m ? {r:+m[1], g:+m[2], b:+m[3], a: m[4]===undefined?1:parseFloat(m[4])} : null; };
  const vars = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const resolve = s => s.replace(/var\((--[\w-]+)(?:,[^)]*)?\)/g, (m,n)=>vars(n)||m);
  const lum = c => { const f=v=>{v/=255; return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);};
    return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); };
  const ratio=(a,b)=>{const l1=lum(a),l2=lum(b),hi=Math.max(l1,l2),lo=Math.min(l1,l2);return (hi+0.05)/(lo+0.05);};
  const over=(fg,bg)=>({r:fg.r*fg.a+bg.r*(1-fg.a), g:fg.g*fg.a+bg.g*(1-fg.a), b:fg.b*fg.a+bg.b*(1-fg.a), a:1});

  // 收集某元素上绘制的候选背景色（background-color + gradient 全部色标）
  function paints(el){
    const st = getComputedStyle(el), out = [];
    const bg = parse(st.backgroundColor);
    if (bg && bg.a > 0) out.push(bg);
    const bi = resolve(st.backgroundImage || '');
    if (bi && bi !== 'none'){
      const re = /(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))/g; let m;
      while ((m = re.exec(bi))){ const c = parse(m[1]) || (m[1][0]==='#' ? hex(m[1]) : null); if (c) out.push(c); }
    }
    return out;
  }
  // 从元素向上求背景候选：把链上所有色标都当候选（保守取最差），遇到不透明层停止
  function bgCandidates(el){
    let cur = el, out = [];
    while (cur){
      const ps = paints(cur);
      out = out.concat(ps);
      if (ps.some(c => c.a === 1)) break;
      cur = cur.parentElement;
    }
    return out.length ? out : [{r:255,g:255,b:255,a:1}];
  }

  const rows = [];
  document.querySelectorAll('body *').forEach(el => {
    if (el.closest('[aria-hidden="true"]')) return;
    const st = getComputedStyle(el);
    if (st.display==='none' || st.visibility==='hidden' || parseFloat(st.opacity)===0) return;
    const r = el.getBoundingClientRect();
    if (r.width<2 || r.height<2) return;
    const txt = Array.from(el.childNodes).filter(n=>n.nodeType===3)
                  .map(n=>n.textContent.trim()).join('');
    if (!txt) return;
    const fgRaw = parse(st.color); if (!fgRaw) return;
    const cands = bgCandidates(el);
    let fg = fgRaw.a<1 ? fgRaw : fgRaw;
    const size = parseFloat(st.fontSize);
    const bold = parseInt(st.fontWeight,10) >= 700;
    const large = size>=24 || (size>=18.66 && bold);
    const need = large ? 3 : 4.5;
    let worst = 99, worstBg = null;
    cands.forEach(c => {
      // 半透明前景先合成到该候选背景上，再算比值
      const fgOn = fgRaw.a < 1 ? over(fgRaw, c) : fgRaw;
      const cr = ratio(fgOn, c);
      if (cr < worst){ worst = cr; worstBg = c; }
    });
    rows.push({text: txt.slice(0,36), size, color: st.color,
               bg: worstBg ? `rgb(${Math.round(worstBg.r)},${Math.round(worstBg.g)},${Math.round(worstBg.b)})` : '?',
               ratio: +worst.toFixed(2), need, pass: worst >= need});
  });
  const fails = rows.filter(r => !r.pass);
  const uniq = [];
  const seen = new Set();
  fails.forEach(f => { const k = f.color+'|'+f.bg+'|'+f.size;
    if (!seen.has(k)){ seen.add(k); uniq.push(f); } });
  return {total_text_nodes: rows.length, fail_count: fails.length,
          unique_failures: uniq,
          min_ratio_all: +Math.min(...rows.map(r=>r.ratio)).toFixed(2)};
}
"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/chromium",
                              args=["--no-sandbox", "--hide-scrollbars"])
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(1800)
        base = pg.evaluate(JS)
        # 翻卡后（背面深色）再测一次
        pg.click("#panel-codes .card")
        pg.wait_for_timeout(500)
        flipped = pg.evaluate(JS)
        # 触发比对（match 状态）再测
        pg.click("#scanbtn")
        pg.wait_for_timeout(1600)
        matched = pg.evaluate(JS)
        b.close()
    print(json.dumps({"initial": base, "after_flip": flipped, "after_match": matched},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
