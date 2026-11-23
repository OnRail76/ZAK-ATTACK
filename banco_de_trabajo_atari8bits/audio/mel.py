import numpy as np, sys
from ana import load
from tr import salience, nn
def mel(nm,start,step,count,lo=55,hi=90,n=4096,bass=False):
    sr,x=load(nm); res=[]
    for i in range(count):
        t=start+i*step+step/2
        if t>len(x)/sr-0.1: break
        s=salience(x,sr,t,n,lo,hi,nh=5); ks=sorted(s,key=s.get,reverse=True)
        m=ks[0]; conf=s[ks[0]]/(np.mean(list(s.values()))+1e-9)
        if bass:
            sb=salience(x,sr,t,16384,28,52,nh=3); b=max(sb,key=sb.get)
        else: b=None
        res.append((t,m,conf,b))
    return res
if __name__=='__main__':
    nm=sys.argv[1]; start=float(sys.argv[2]); step=float(sys.argv[3]); cnt=int(sys.argv[4]); per=int(sys.argv[5])
    r=mel(nm,start,step,cnt,bass=True)
    for i in range(0,len(r),per):
        print('%6.2f '%r[i][0]+' '.join('%-4s%s'%(nn(m),'!' if c>4 else ('.' if c>3 else ' ')) for _,m,c,_ in r[i:i+per]) + '   bajo: '+' '.join(nn(b) for *_,b in r[i:i+per:4]))
