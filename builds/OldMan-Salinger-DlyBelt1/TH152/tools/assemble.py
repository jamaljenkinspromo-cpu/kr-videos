# concat parts -> normal-speed video (ts copy) + PCM wav; global word list; retime factor
import json, subprocess, os
os.chdir('/root/work/final')
ORDER=['S1','RICK','S2','KRISTEN','S3']
SPK={'S1':'sal','RICK':'rick','S2':'sal','KRISTEN':'kristen','S3':'sal'}
def pk(f):
    o=subprocess.check_output(['ffprobe','-v','error','-count_packets','-select_streams','v:0','-show_entries','stream=nb_read_packets','-of','csv=p=0',f]).decode().strip()
    return int(o.split(',')[0])
off=0.0; W=[]; segs=[]; frames=0
for p in ORDER:
    src=f'/root/work/raw/{p}.mp4'
    n=pk(src); dur=n/25.0
    pw=json.load(open(f'/root/work/raw/{p}.json'))
    for w in pw: W.append({'w':w['w'],'s':round(w['s']+off,3),'e':round(min(w['e'],dur)+off,3),'spk':SPK[p]})
    segs.append({'part':p,'start':off,'end':off+dur,'frames':n,'spk':SPK[p]})
    if not os.path.exists(f'{p}.ts'):
        subprocess.check_call(['ffmpeg','-v','error','-y','-i',src,'-map','0:v:0','-c','copy','-bsf:v','h264_mp4toannexb','-f','mpegts',f'{p}.ts'])
    # audio: exactly dur seconds of PCM (pad/trim) so A/V stay locked per part
    subprocess.check_call(['ffmpeg','-v','error','-y','-i',src,'-map','0:a:0','-af',f'apad,atrim=end_sample={int(round(dur*48000))}','-ar','48000','-ac','2','-c:a','pcm_s16le',f'{p}.wav'])
    off+=dur; frames+=n
subprocess.check_call(['ffmpeg','-v','error','-y','-i','concat:'+'|'.join(f'{p}.ts' for p in ORDER),'-map','0:v:0','-c','copy','-fflags','+genpts','-r','25','master_v.mp4'])
open('alist.txt','w').write(''.join(f"file '{p}.wav'\n" for p in ORDER))
subprocess.check_call(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','alist.txt','-c','copy','master_a.wav'])
script=open('/root/work/in/SCRIPT.txt').read().split()
assert [w['w'] for w in W]==script, 'word list != script'
target=len(script)/3.0; total=frames/25.0; speed=total/target
Wf=[{'w':w['w'],'s':round(w['s']/speed,3),'e':round(w['e']/speed,3),'spk':w['spk']} for w in W]
json.dump(W,open('words_normal.json','w')); json.dump(Wf,open('words_fast.json','w'))
for s in segs: s['fs']=s['start']/speed; s['fe']=s['end']/speed
json.dump({'segs':segs,'frames':frames,'total':total,'target':target,'speed':speed,'fps_new':25*speed},open('timeline.json','w'),indent=1)
print('frames',frames,'normal',round(total,3),'target',round(target,3),'speed',round(speed,6),'packets master',pk('master_v.mp4'))
