import json,sys,re
W=json.load(open(sys.argv[1]))
sents=[];cur=[]
for i,w in enumerate(W):
    cur.append(i)
    if re.search(r'[.!?]["\')]?$',w['w']): sents.append(cur);cur=[]
if cur: sents.append(cur)
bad=0
tiny=[w for w in W if w['e']-w['s']<0.05]
print('words',len(W),'tiny(<50ms)',len(tiny),[t['w'] for t in tiny][:20])
for s in sents:
    a,b=W[s[0]]['s'],W[s[-1]]['e']; r=len(s)/max(b-a,0.01)
    t=sum(1 for i in s if W[i]['e']-W[i]['s']<0.05)
    if r>5.0 or t>=2: bad+=1; print('SUSPECT',round(a,2),round(r,2),t,' '.join(W[i]['w'] for i in s)[:90])
gaps=sorted(((W[i+1]['s']-W[i]['e'],W[i]['e'],W[i]['w']) for i in range(len(W)-1)),reverse=True)[:5]
print('largest gaps',[(round(g,2),round(t,2),w) for g,t,w in gaps])
print('suspect sentences',bad,'of',len(sents))
