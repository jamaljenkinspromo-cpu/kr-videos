import json,re,sys
W=json.load(open(sys.argv[1])); TOTAL=float(sys.argv[2]); OUT=sys.argv[3]
MAXLINE=26; MAXLINES=2; MAXWORDS=7; HOLD=0.22
FUNC=set("a an the and but or so because if when while that which who to of in on at for with from as is are was were it its his her their this these those you your my we our".split())
sents=[];cur=[]
for w in W:
    cur.append(w)
    if re.search(r'[.!?]["\')]?$', w['w']): sents.append(cur); cur=[]
if cur: sents.append(cur)
def wrap(ws):
    lines=[];ln=''
    for w in ws:
        c=w if not ln else ln+' '+w
        if len(c)<=MAXLINE or not ln: ln=c
        else: lines.append(ln); ln=w
    if ln: lines.append(ln)
    return lines
def fits(ws):
    L=wrap([x['w'] for x in ws])
    return len(L)<=MAXLINES and len(ws)<=MAXWORDS and max(len(l) for l in L)<=MAXLINE
def breakcost(s,i):
    prev,nxt=s[i-1],s[i]
    gap=nxt['s']-prev['e']
    c=3.0
    if gap>=0.30: c=0.0
    elif gap>=0.18: c=0.5
    elif gap>=0.10: c=1.2
    if re.search(r'[,;:—–]$',prev['w']): c=min(c,0.35)
    if prev['w'].lower().strip('.,!?;:') in FUNC: c+=2.5
    return c
caps=[]
for s in sents:
    n=len(s); INF=float('inf')
    dp=[INF]*(n+1); bk=[0]*(n+1); dp[0]=0.0
    for i in range(1,n+1):
        for j in range(i-1,-1,-1):
            seg=s[j:i]
            if not fits(seg):
                if i-j>MAXWORDS: break
                continue
            cost=dp[j]
            if j>0: cost+=breakcost(s,j)
            L=len(seg)
            if L==1 and (seg[0]['e']-seg[0]['s'])<0.34: cost+=1.6
            if L==1: cost+=0.5
            if L>5: cost+=0.35*(L-5)
            if cost<dp[i]: dp[i]=cost; bk[i]=j
    idx=[n]
    while idx[-1]>0: idx.append(bk[idx[-1]])
    idx.reverse()
    for a,b in zip(idx,idx[1:]): caps.append((s[a:b], b==n))
def fmt(x):
    x=max(0.0,min(x,TOTAL))
    h=int(x//3600);m=int(x%3600//60);sc=int(x%60);ms=int(round((x-int(x))*1000))
    if ms==1000: sc+=1;ms=0
    return f"{h:02d}:{m:02d}:{sc:02d},{ms:03d}"
rows=[]
for i,(c,endsent) in enumerate(caps):
    st=c[0]['s']
    nxt = caps[i+1][0][0]['s'] if i+1<len(caps) else TOTAL
    en = min(c[-1]['e']+HOLD, nxt-0.04, TOTAL) if endsent else min(nxt,TOTAL)
    if en<=st+0.10: en=min(st+0.32,TOTAL)
    rows.append((st,en,'\n'.join(wrap([x['w'] for x in c]))))
with open(OUT,'w',encoding='utf-8') as f:
    for i,(s0,e0,t) in enumerate(rows,1): f.write(f"{i}\n{fmt(s0)} --> {fmt(e0)}\n{t}\n\n")
from collections import Counter
h=Counter(len(c) for c,_ in caps); print('captions',len(caps),'hist',[h.get(k,0) for k in range(1,8)])
print('words in captions',sum(len(c) for c,_ in caps))
