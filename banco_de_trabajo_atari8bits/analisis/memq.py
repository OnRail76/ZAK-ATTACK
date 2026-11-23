import sys,re
lbl={}
for l in open('/home/claude/vortice5/build/game.lbl'):
    p=l.split()
    if len(p)>=3: lbl[p[2].lstrip('.')]=int(p[1],16)
m=open(sys.argv[1],'rb').read()
def g(name,n=1,off=0): a=lbl[name]+off; return list(m[a:a+n])
