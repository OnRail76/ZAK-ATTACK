import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, sys
def load(nm):
    sr,x=w.read(nm+'.wav'); return sr,x.astype(float)/32768
def onset_env(x,sr,hop=256,n=1024):
    f,t,Z=sg.stft(x,sr,nperseg=n,noverlap=n-hop); M=np.log1p(100*np.abs(Z))
    flux=np.maximum(0,np.diff(M,axis=1)).sum(0); return flux, sr/hop
def tempo(flux,fr):
    q=flux-flux.mean(); ac=np.correlate(q,q,'full')[len(q)-1:]
    lags=np.arange(len(ac))/fr; bpm=60/np.maximum(lags,1e-9)
    m=(bpm>60)&(bpm<200); k=np.argmax(ac*m); return 60/lags[k], ac, lags
if __name__=='__main__':
    for nm in sys.argv[1:]:
        sr,x=load(nm); fl,fr=onset_env(x,sr); bpm,ac,lags=tempo(fl,fr)
        # top candidates
        m=(lags>0.25)&(lags<2.0); idx=sg.find_peaks(ac*m)[0]; idx=sorted(idx,key=lambda i:-ac[i])[:6]
        print(nm,'BPM %.1f'%bpm, 'candidatos', [round(60/lags[i],1) for i in idx])
