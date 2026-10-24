import subprocess, numpy as np, sys
def frame(f,n):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',f,'-vf',f'select=eq(n\\,{n}),crop=1080:880:0:0,scale=270:220','-frames:v','1','-f','rawvideo','-pix_fmt','gray','-'])
    return np.frombuffer(raw,np.uint8).astype(float)
for n in map(int,sys.argv[1:]):
    o=frame('OUT.mp4',n); res=[(abs(o-frame('master_v.mp4',m)).mean(),m-n) for m in (n-1,n,n+1)]
    print(n,[(round(d,2),k) for d,k in res])
