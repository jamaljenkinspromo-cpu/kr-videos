from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FS,RADIUS,PADX,PADY,MAXPCT=56,16,26,14,0.88
Y=0.78
cues=[["This is what a knee replacement","is supposed to look like."],["This is what it looks like","if you're still in pain."],["Let me show you","what your X-ray missed."]]
for i,lines in enumerate(cues):
    fs=FS
    while fs>20:
        f=ImageFont.truetype(FONT,fs); d=ImageDraw.Draw(Image.new('RGBA',(1,1)))
        if max(d.textbbox((0,0),l,font=f)[2] for l in lines)+2*PADX<=W*MAXPCT: break
        fs-=2
    f=ImageFont.truetype(FONT,fs)
    img=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
    asc,desc=f.getmetrics(); lh=int((asc+desc)*1.12)
    tw=max(d.textbbox((0,0),l,font=f)[2] for l in lines)
    bw=int(tw+2*PADX); bh=int(len(lines)*lh+2*PADY)
    x0=(W-bw)//2; y0=int(H*Y)
    d.rounded_rectangle([x0,y0,x0+bw,y0+bh],radius=RADIUS,fill=(255,255,255,255))
    for j,l in enumerate(lines):
        lw=d.textbbox((0,0),l,font=f)[2]; d.text(((W-lw)//2,y0+PADY+j*lh),l,font=f,fill=(0,0,0,255))
    img.save(f"c{i}.png")
