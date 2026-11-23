import numpy as np, scipy.signal as sg, sys
from ana import load, onset_env
NAMES=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def nn(m): return NAMES[m%12]+str(m//12-1)
def salience(x,sr,t,n,lo,hi,nh=5):
    i=int(t*sr); seg=x[max(0,i-n//2):i+n//2]
    if len(seg)<n: seg=np.pad(seg,(0,n-len(seg)))
    S=np.abs(np.fft.rfft(seg*np.hanning(n))); f=np.fft.rfftfreq(n,1/sr)
    sal={}
    for m in range(lo,hi):
        f0=440*2**((m-69)/12); s=0
        for h in range(1,nh+1):
            fh=f0*h
            if fh>sr/2: break
            k=int(round(fh*n/sr)); s+=S[max(0,k-1):k+2].max()/h**0.5
        sal[m]=s
    return sal
def main(nm,bpm,bars,start_bar=0):
    sr,x=load(nm)
    fl,fr=onset_env(x,sr)
    beat=60/bpm
    # fase del pulso
    best=None
    for off in np.arange(0,beat,0.005):
        idx=((off+np.arange(0,len(x)/sr-1,beat))*fr).astype(int)
        s=fl[idx[idx<len(fl)]].sum()
        if best is None or s>best[0]: best=(s,off)
    off=best[1]; print('fase %.3f s'%off)
    step=beat/4
    for b in range(start_bar,start_bar+bars):
        line=[]
        for s16 in range(16):
            t=off+(b*16+s16)*step+step/2
            if t>len(x)/sr-0.2: break
            sb=salience(x,sr,t,8192,28,55,nh=4); bm=max(sb,key=sb.get)
            sm=salience(x,sr,t,4096,55,96,nh=5); mm=sorted(sm,key=sm.get,reverse=True)[:2]
            # onset fuerza en el paso
            k=int((t-step/2)*fr); on=fl[k:k+max(1,int(step*fr))].max()
            line.append('%s/%s%s'%(nn(bm),nn(mm[0]),'*' if on>np.percentile(fl,80) else ' '))
        print('c%02d '%b+' '.join('%-9s'%c for c in line))
if __name__=='__main__':
    main(sys.argv[1],float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]) if len(sys.argv)>4 else 0)
