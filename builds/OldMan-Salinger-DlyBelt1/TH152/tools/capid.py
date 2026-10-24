import json, subprocess, numpy as np, io
from PIL import Image
T=json.load(open('strip/times.json')); B=json.load(open('strip/boxes.json'))
n=len(T); idx=sorted(set(list(range(0,n,12))+[n-1]+[i for i in range(n) if any(abs(T[i][0]-t)<4 for t in [385.36,418.81,424.65,517.35])]))
refs={}
def dark(i):
    if i not in refs:
        a=np.array(Image.open(f'strip/c{i:04d}.png')); refs[i]=((a[:,:,0]<100)&(a[:,:,3]>200), a[:,:,3]>200)
    return refs[i]
fails=0; scores=[]
for i in idx:
    s,e=T[i]; t=min(s+0.45,(s+e)/2)
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i','OUT.mp4','-frames:v','1','-f','rawvideo','-pix_fmt','gray','-'])
    v=np.frombuffer(raw,np.uint8).reshape(1920,1080)
    def iou(j):
        d,op=dark(j); dv=(v<100)&op
        return (d&dv).sum()/max((d|dv).sum(),1)
    own=iou(i); rivals=[iou(j) for j in (i-1,i+1) if 0<=j<n]
    ok=own>max(rivals) ; fails+= not ok; scores.append(own)
    if not ok: print('FAIL',i,t,own,rivals)
print('checked',len(idx),'fails',fails,'own min',round(min(scores),3),'median',round(float(np.median(scores)),3))
