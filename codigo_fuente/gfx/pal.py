import os
_d=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pal.bin'),'rb').read()
PAL=[tuple(_d[i*3:i*3+3]) for i in range(256)]
def atari_rgb(code): return PAL[code&0xFE]
