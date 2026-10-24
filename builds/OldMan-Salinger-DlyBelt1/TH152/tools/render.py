import json, subprocess, os, sys
os.chdir('/root/work/final')
T=json.load(open('timeline.json')); S=json.load(open('spots.json'))
speed=T['speed']; frames=T['frames']; dur=T['target']
FPS=f"{frames*3}/2044"
caps=json.load(open('strip/times.json')); boxes=json.load(open('strip/boxes.json'))
# caption concat list, clamped from 0.0, sums to dur
lines=[]; prev=0.0
for i,(s,e) in enumerate(caps):
    s=max(s,prev); e=max(e,s+0.04)
    if i+1<len(caps): e=min(e,max(caps[i+1][0],s+0.04))
    if s>prev+1e-4: lines.append(("strip/blank.png",s-prev))
    lines.append((f"strip/c{i:04d}.png",e-s)); prev=e
if prev<dur: lines.append(("strip/blank.png",dur-prev))
tot=sum(d for _,d in lines); assert abs(tot-dur)<0.01,(tot,dur)
with open('caps.txt','w') as f:
    for p,d in lines: f.write(f"file '{p}'\nduration {d:.4f}\n")
    f.write(f"file '{lines[-1][0]}'\n")
# strip crop
top=min(b[2] for b in boxes); bot=max(b[3] for b in boxes)
top-=top%2; h=bot-top+ (bot-top)%2
inputs=['-itsscale',f'{1/speed:.9f}','-i','master_v.mp4','-f','concat','-safe','0','-i','caps.txt']
fc=[f"[1:v]fps={FPS},format=rgba,crop=1080:{h}:0:{top}[cap]"]
cur='[0:v]'; k=2; n=0
for f,a,b in S['popups']:
    inputs+=['-loop','1','-t',f'{b-a:.3f}','-itsoffset',f'{a:.3f}','-i',f]
    fc.append(f"[{k}:v]scale=720:720:force_original_aspect_ratio=decrease,setsar=1,fps={FPS},format=yuva420p[p{n}]")
    fc.append(f"{cur}[p{n}]overlay=(W-w)/2:1160:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[v{n}]"); cur=f'[v{n}]'; k+=1; n+=1
for a,b in S['product']:
    inputs+=['-itsoffset',f'{a:.3f}','-t',f'{b-a:.3f}','-i','/root/work/dl/product.mp4']
    fc.append(f"[{k}:v]crop=666:720:216:1134,setsar=1,fps={FPS}[p{n}]")
    fc.append(f"{cur}[p{n}]overlay=(W-w)/2:1160:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[v{n}]"); cur=f'[v{n}]'; k+=1; n+=1
fc.append(f"{cur}[cap]overlay=0:{top}:format=auto[vout]")
fc.append(f"[{k}:a]atempo={speed:.7f}[aout]")
inputs+=['-i','master_a.wav']
kb=min(5000,max(600,int(760000/dur)-110))
cmd=['ffmpeg','-y','-v','warning','-stats']+inputs+['-filter_complex',';'.join(fc),'-map','[vout]','-map','[aout]',
 '-r',FPS,'-frames:v',str(frames),'-c:v','libx264','-preset','veryfast','-b:v',f'{kb}k','-maxrate',f'{kb*115//100}k','-bufsize',f'{kb*2}k','-pix_fmt','yuv420p','-bf','0',
 '-c:a','aac','-b:a','96k','-ar','48000','-movflags','+faststart',sys.argv[1]]
open('render_cmd.txt','w').write(' '.join(cmd))
print('strip',top,h,'kbps',kb,'fps',FPS, 'blur in graph:', any(x in ';'.join(fc) for x in ['blur','pixel','mosaic']))
subprocess.check_call(cmd)
