
import json
def lum(h):
    h=h.lstrip("#"); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[(v/12.92) if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def ratio(a,b):
    la,lb=lum(a),lum(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
BG="#0B0A14"; BG2="#100E1D"; PANEL="#161331"; PANEL2="#1D1940"
pairs=[("ink","#F3F0FC",BG),("ink/panel","#F3F0FC",PANEL),("dim","#C3BADF",BG),("dim/bg2","#C3BADF",BG2),
("dim2","#AAA0CC",BG),("dim2/panel","#AAA0CC",PANEL),("dim2/bg2","#AAA0CC",BG2),
("sea","#4FE0C8",BG),("asc","#C79BF6",BG),("asc/panel","#C79BF6",PANEL),
("gold","#F5B942",BG),("gold/bg2","#F5B942",BG2),("red","#FF6E5C",BG),
("on-sea-btn","#08110F","#4FE0C8"),("on-asc-btn","#140B24","#C79BF6"),
("ink/panel2","#F3F0FC",PANEL2),("dim/panel2","#C3BADF",PANEL2),("dim2/panel2","#AAA0CC",PANEL2),
("rail-ink","#F3F0FC",BG2),("chip-dim2","#AAA0CC",PANEL2),("gold/panel","#F5B942",PANEL)]
res=[]
for n,a,b in pairs:
    r=ratio(a,b); res.append((n,round(r,2),"PASS" if r>=4.5 else ("LARGE-ONLY" if r>=3 else "FAIL")))
res.sort(key=lambda x:x[1])
for x in res: print(x)
print("min:",min(x[1] for x in res))
