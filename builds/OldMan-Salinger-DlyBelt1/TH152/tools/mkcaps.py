import re, sys, os, json
from PIL import Image, ImageDraw, ImageFont
SRT, OUTDIR, SCHEDF = sys.argv[1], sys.argv[2], sys.argv[3]
W,H = 1080,1920
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FS,RADIUS,PADX,PADY,MAXPCT = 56,16,26,14,0.88
SCHED=json.load(open(SCHEDF))   # list of [a,b,y]; default in 'default'
DEFAULT=SCHED['default']
def ypct(t):
    for a,b,y in SCHED['ranges']:
        if a<=t<b: return y
    return DEFAULT
os.makedirs(OUTDIR,exist_ok=True)
def t2s(t):
    h,m,rest=t.split(':'); s,ms=rest.split(',')
    return int(h)*3600+int(m)*60+int(s)+int(ms)/1000
cues=[]
for b in re.split(r'\n\s*\n', open(SRT,encoding='utf-8-sig').read().strip()):
    L=[l for l in b.strip().splitlines() if l.strip()]
    tl=next((l for l in L if '-->' in l),None)
    if not tl: continue
    a,bb=[p.strip() for p in tl.split('-->')]
    cues.append((t2s(a),t2s(bb),L[L.index(tl)+1:]))
maxw=W*MAXPCT
boxes=[]
for i,(st,en,lines) in enumerate(cues):
    fs=FS
    while fs>20:
        f=ImageFont.truetype(FONT,fs)
        d=ImageDraw.Draw(Image.new('RGBA',(1,1)))
        if max(d.textbbox((0,0),l,font=f)[2] for l in lines)+2*PADX<=maxw: break
        fs-=2
    f=ImageFont.truetype(FONT,fs)
    img=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
    asc,desc=f.getmetrics(); lh=int((asc+desc)*1.12)
    tw=max(d.textbbox((0,0),l,font=f)[2] for l in lines)
    bw=int(tw+2*PADX); bh=int(len(lines)*lh+2*PADY)
    x0=(W-bw)//2; y0=int(H*ypct((st+en)/2))
    y0=min(y0, H-bh-40)
    d.rounded_rectangle([x0,y0,x0+bw,y0+bh],radius=RADIUS,fill=(255,255,255,255))
    for j,l in enumerate(lines):
        lw=d.textbbox((0,0),l,font=f)[2]
        d.text(((W-lw)//2, y0+PADY+j*lh), l, font=f, fill=(0,0,0,255))
    img.save(f"{OUTDIR}/c{i:04d}.png", compress_level=1)
    boxes.append([st,en,y0,y0+bh])
Image.new('RGBA',(W,H),(0,0,0,0)).save(f"{OUTDIR}/blank.png")
json.dump([[st,en] for st,en,_ in cues], open(f"{OUTDIR}/times.json","w"))
json.dump(boxes, open(f"{OUTDIR}/boxes.json","w"))
print('cues',len(cues))
