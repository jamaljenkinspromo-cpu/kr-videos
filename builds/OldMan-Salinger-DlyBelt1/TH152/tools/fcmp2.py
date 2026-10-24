import subprocess, numpy as np, sys
F=54945/2044
def frame(f,t):
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{t:.4f}','-i',f,'-vf','crop=1080:880:0:0,scale=270:220','-frames:v','1','-f','rawvideo','-pix_fmt','gray','-'])
    return np.frombuffer(raw,np.uint8).astype(float)
for n in map(int,sys.argv[1:]):
    o=frame('OUT.mp4',(n+0.5)/F); res=[(round(abs(o-frame('master_v.mp4',(m+0.5)/25)).mean(),2),m-n) for m in (n-1,n,n+1)]
    print(n,res,flush=True)
