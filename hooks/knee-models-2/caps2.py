from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FS,RADIUS,PADX,PADY,MAXPCT=56,16,26,14,0.88
Y=0.78
cues=[["This is why my knee replacement","still hurt two years later."],["Turns out, it wasn't just","\u201cgive it time.\u201d"],["Now look."],["A loose, easy knee","every single night."],["And it was all because"],["I figured out","what the X-rays missed."]]
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
