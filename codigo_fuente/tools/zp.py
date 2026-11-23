import sys
lbl={}
for l in open('build/game.lbl'):
    p=l.split()
    if len(p)>=3: lbl[p[2].lstrip('.')]=int(p[1],16)
m=open(sys.argv[1],'rb').read()
for n in sys.argv[2:]:
    a=lbl[n]-0x80
    print(n, ' '.join('%02X'%b for b in m[a:a+3]))
