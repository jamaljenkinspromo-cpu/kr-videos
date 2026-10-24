import json
os_=__import__('os'); os_.chdir('/root/work/final')
L=[l.strip() for l in open('/root/work/in/SCRIPT.txt') if l.strip()]
W=json.load(open('words_fast.json')); T=json.load(open('timeline.json'))
rng=[];i=0
for l in L:
    n=len(l.split()); rng.append((i,i+n-1)); i+=n
assert i==len(W)
def line(prefix):
    k=[j for j,l in enumerate(L) if l.startswith(prefix)]; assert len(k)==1,(prefix,k); return k[0]
def ls(p): return W[rng[line(p)][0]]['s']
def le(p): return W[rng[line(p)][1]]['e']
P='/home/claude/kr-videos/builds/OldMan-Salinger-DlyBelt1/popups/'
spots=[
 ('01-new-knee-parts.png',ls("Let me show you on this knee model."),le("As you can see, a new knee")),
 ('02-living-tissue.png',ls("Now, the part nobody shows you"),le("This tissue has to bend")),
 ('03-calm-knee-room.png',ls("Now there's more swollen tissue sitting"),le("That's what a calm knee looks like.")),
 ('04-swollen-crowding.png',ls("But many of us, through no fault"),le("Instead, the swollen tissue crowds")),
 ('05-calm-vs-squeeze.png',ls("We call that The Squeeze"),le("We call that The Squeeze")),
 ('05-calm-vs-squeeze.png',ls("Your replacement can be perfectly fine"),le("Your replacement can be perfectly fine")),
 ('06-xray-sees-vs-cant.png',ls("But that's only half of the answer"),le("So when they tell you")),
 ('07-inflammation-alarm.png',ls("You see, deep in the tissue around your new knee"),le("That's because a lot of it sits deep")),
 ('08-swollen-to-calm.png',ls("Red and near-infrared light has been studied"),le("You see, when that tissue calms down")),
]
# product clip: one full play (4.296 s at source speed, it is b-roll so it plays at its own speed) at the start of each product line
CL=4.295958
prod=[]
for p in ["Many months and more prototypes","It's called the KenRelief Red Light Therapy Wrap","The secret is two wavelengths"]:
    prod.append(['product',ls(p),ls(p)+CL])
s08=spots[-1][1]
for p in prod:
    if p[2]>s08: p[2]=s08-0.04
out={'popups':[[P+f,round(a,3),round(b,3)] for f,a,b in spots],'product':[[a,round(b,3)] for _,a,b in [(x[0],round(x[1],3),x[2]) for x in prod]]}
# sanity: no overlaps
allsp=sorted([(a,b,f) for f,a,b in out['popups']]+[(a,b,'product') for a,b in out['product']])
for x,y in zip(allsp,allsp[1:]): assert x[1]<=y[0]+1e-6,(x,y)
json.dump(out,open('spots.json','w'),indent=1)
for a,b,f in allsp: print(f"{a:7.2f} {b:7.2f} {b-a:5.2f} {f.split('/')[-1]}")
# check 08 is after problem section i.e. after 'It's called' line
print('08 start',s08,'product reveal',ls("It's called the KenRelief"))
# speaker ranges for caption rows
Y={'sal':0.50,'rick':0.62,'kristen':0.71}
json.dump({'default':0.50,'ranges':[[s['fs'],s['fe'],Y[s['spk']]] for s in T['segs']]},open('sched.json','w'))
