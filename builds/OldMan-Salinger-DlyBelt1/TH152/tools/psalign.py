# forced alignment of a script chunk against a wav using pocketsphinx 5
import sys, re, json, os
from pocketsphinx import Decoder, get_model_path
MP=get_model_path()
NUM={'2014':'twenty fourteen','1':'one','5':'five','660':'six sixty','850':'eight fifty','20':'twenty','30':'thirty',
 '90-day':'ninety day','90':'ninety','10,000':'ten thousand','24':'twenty four','50%':'fifty percent','240':'two forty',
 '$200':'two hundred dollars','$50,000':'fifty thousand dollars'}
def norm(w):
    k=w.lower().strip('"\'.,!?;:()')
    if k in NUM: return NUM[k].split()
    k=k.replace('-',' ')
    out=[]
    for p in k.split():
        p=re.sub(r"[^a-z']",'',p)
        if p: out.append(p)
    return out or ['uh']
def mkdec():
    d=Decoder(hmm=os.path.join(MP,'en-us/en-us'),dict=DICT,lm=None,loglevel='FATAL')
    return d
DICT=os.path.expanduser('~/work/tools/custom.dict')
if not os.path.exists(DICT):
    base=open(os.path.join(MP,'en-us/cmudict-en-us.dict')).read()
    extra="""kenrelief K EH N R IH L IY F
near-infrared N IH R IH N F R ER EH D
fda EH F D IY EY
kristen K R IH S T AH N
salinger S AE L IH N JH ER
"""
    open(DICT,'w').write(base+extra)
def align_words(wav, words, t0=0.0):
    import wave, numpy as np
    keys=[]; owner=[]
    for i,w in enumerate(words):
        for k in norm(w): keys.append(k); owner.append(i)
    d=mkdec()
    d.set_align_text(' '.join(keys))
    raw=open(wav,'rb').read()[44:]
    d.start_utt(); d.process_raw(raw,full_utt=True); d.end_utt()
    segs=[(s.word,s.start_frame/100+t0,(s.end_frame+1)/100+t0) for s in d.seg() if s.word not in ('<s>','</s>','<sil>','[NOISE]')]
    segs=[(re.sub(r'\(\d+\)','',w),a,b) for w,a,b in segs]
    if len(segs)!=len(keys): raise RuntimeError(f'seg {len(segs)} vs keys {len(keys)}')
    res=[None]*len(words)
    for (w,a,b),o in zip(segs,owner):
        if res[o] is None: res[o]=[a,b]
        else: res[o][1]=b
    return [{'w':words[i],'s':round(res[i][0],3),'e':round(res[i][1],3)} for i in range(len(words))]
if __name__=='__main__':
    wav, txt, out = sys.argv[1:4]
    words=open(txt).read().split()
    r=align_words(wav,words)
    json.dump(r,open(out,'w')); print(len(words),len(r))
