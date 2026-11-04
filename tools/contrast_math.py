#!/usr/bin/env python3
"""contrast_math.py — 对比度配色计算工具（保色相加深/提亮）。"""
import re
import sys

sys.path.insert(0, '/app/working/shared/showcase/tools')
from contrast_forensics import hex_to_rgb, rgb_to_hex, rel_lum, contrast  # noqa: E402


def scale(rgb, k):
    return tuple(c * k for c in rgb)


def scale_up(rgb, k):
    return tuple(c + (255 - c) * (k - 1) for c in rgb)


def darken_to(fg_hex, bg_hex, target, margin=0.0):
    """保色相加深 fg，直到对 bg 的对比度 ≥ target（bg 浅时用）。"""
    fg, bg = hex_to_rgb(fg_hex), hex_to_hex(bg_hex)
    if contrast(fg, bg) >= target + margin:
        return None
    for i in range(1000, 0, -1):
        k = i / 1000.0
        if contrast(scale(fg, k), bg) >= target + margin:
            return rgb_to_hex(scale(fg, k))
    return None


def lighten_to(fg_hex, bg_hex, target, margin=0.0):
    """保色相提亮 fg，直到对 bg 的对比度 ≥ target（bg 深时用）。"""
    fg, bg = hex_to_hex(fg_hex), hex_to_rgb(bg_hex)
    for i in range(1000, 3001):
        k = i / 1000.0
        if contrast(scale_up(fg, k), bg) >= target + margin:
            return rgb_to_hex(scale_up(fg, k))
    return None


def deepen_bg_for_white(bg_hex, target, alpha=1.0):
    """保色相加深 bg，使（白色按 alpha 叠加后的合成色）对 bg 的对比度 ≥ target。"""
    bg = hex_to_rgb(bg_hex)
    for i in range(1000, 0, -1):
        k = i / 1000.0
        cand = scale(bg, k)
        if alpha >= 1.0:
            comp = (255, 255, 255)
        else:
            comp = tuple(alpha * 255 + (1 - alpha) * c for c in cand)
        if contrast(comp, cand) >= target:
            return rgb_to_hex(cand)
    return None


def report(label, fg_hex, bg_hex, target):
    f, b = hex_to_rgb(fg_hex), hex_to_rgb(bg_hex)
    cr = contrast(f, b)
    ok = 'OK ' if cr >= target else 'FAIL'
    print(f'  {ok} {label:34s} {fg_hex} on {bg_hex} = {cr:.2f}:1  (need {target})')


if __name__ == '__main__':
    print('--- 中灰候选 ---')
    for c in ['#86868b', '#76767b', '#6e6e73', '#6b6b70', '#68686d', '#63636a']:
        report(f'{c} on #ffffff', c, '#ffffff', 4.5)
        report(f'{c} on #f5f5f7', c, '#f5f5f7', 4.5)
        report(f'{c} on #fafafa', c, '#fafafa', 4.5)
        report(f'{c} on #000000 (深底须保留)', c, '#000000', 4.5)

    print('\n--- 蓝候选（浅底） ---')
    for c in ['#0071e3', '#0066cc', '#0062c4', '#005ec2']:
        report(f'{c} on #ffffff', c, '#ffffff', 4.5)
        report(f'{c} on #fafafa', c, '#fafafa', 4.5)
        report(f'{c} on #f5f5f7', c, '#f5f5f7', 4.5)
        report(f'{c} on #e6f1fc', c, '#e6f1fc', 4.5)

    print('\n--- 蓝候选（深底 #000） ---')
    for c in ['#0071e3', '#0a7cff', '#1d7fff', '#2997ff', '#4da3ff']:
        report(f'{c} on #000000', c, '#000000', 4.5)

    print('\n--- 琥珀候选（浅底） ---')
    for c in ['#ff9500', '#d17f00', '#c27400', '#b36900', '#a86200']:
        report(f'{c} on #ffffff', c, '#ffffff', 4.5)
        report(f'{c} on #fafafa', c, '#fafafa', 4.5)
        report(f'{c} on #ffefd9', c, '#ffefd9', 4.5)

    print('\n--- 绿候选 ---')
    for c in ['#2e7d32', '#266b2a', '#1f6124', '#276f2b']:
        report(f'{c} on #eaf2eb', c, '#eaf2eb', 4.5)
        report(f'{c} on #ffffff', c, '#ffffff', 4.5)

    print('\n--- 扇区渐变：白色文字所需的最浅底 ---')
    for bg in ['#d70015', '#ff3b30', '#ff9500', '#ffb340', '#5d5d6f', '#86868b',
               '#0071e3', '#4a9eff', '#2e7d32', '#66bb6a']:
        n85 = deepen_bg_for_white(bg, 4.5, alpha=0.85)
        n100 = deepen_bg_for_white(bg, 4.5, alpha=1.0)
        r85 = report(f'{bg} 白字(不透明)', '#ffffff', bg, 4.5)
        print(f'      → note(0.85 合成) 需最深 {n85} ; 白字需最深 {n100}')
