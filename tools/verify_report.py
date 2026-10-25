import re
html = open('2026-10-15-memory-price-tsunami.html', encoding='utf-8').read()
body = re.sub(r'<style.*?</style>', '', html, flags=re.S)
text = re.sub(r'<[^>]+>', ' ', body)
cjk = len(re.findall(r'[\u4e00-\u9fff]', text))
print('CJK_chars:', cjk)
print('tables:', html.count('<table>'))
print('closed_html:', html.strip().endswith('</html>'))
print('apple_vars:', all(x in html for x in ['#0071e3', '#f5f5f7', '#1d1d1f', '980px']))
