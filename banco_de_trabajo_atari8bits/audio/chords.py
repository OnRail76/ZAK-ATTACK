import numpy as np, sys
from ana import load
from tr import salience, nn, NAMES
def chroma(x,sr,t0,t1,n=8192):
    c=np.zeros(12); cnt=0
    for t in np.arange(t0,t1,0.05):
        i=int(t*sr); seg=x[i:i+n]
        if len(seg)<n: break
        S=np.abs(np.fft.rfft(seg*np.hanning(n))); f=np.fft.rfftfreq(n,1/sr)
        m=(f>80)&(f<2000); fm=f[m]; Sm=S[m]
        pc=np.round(12*np.log2(fm/440)+69).astype(int)%12
        np.add.at(c,pc,Sm**2); cnt+=1
    return c/ (c.max()+1e-9)
TEMPL={}
for r in range(12):
    for q,iv in (('',(0,4,7)),('m',(0,3,7))):
        v=np.zeros(12); v[[ (r+i)%12 for i in iv]]=1; TEMPL[NAMES[r]+q]=v
def chord(c):
    return max(TEMPL,key=lambda k: np.dot(TEMPL[k],c)/np.linalg.norm(TEMPL[k]))
def run(nm,bpm,off,nbars,per=2):
    sr,x=load(nm); beat=60/bpm; out=[]
    for b in range(nbars):
        row=[]
        for h in range(4//per):
            t0=off+(b*4+h*per)*beat; t1=t0+per*beat
            if t1>len(x)/sr: break
            c=chroma(x,sr,t0,t1); ch=chord(c)
            sb=salience(x,sr,(t0+t1)/2,16384,28,52,nh=3); bm=max(sb,key=sb.get)
            row.append('%-4s(%s)'%(ch,nn(bm)))
        out.append(row); print('c%02d %5.1fs '%(b,off+b*4*beat)+'  '.join(row))
    return out
if __name__=='__main__':
    run(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4]))
