class C:
    def __init__(s,w,h,f='.'): s.w,s.h=w,h; s.p=[[f]*w for _ in range(h)]
    @staticmethod
    def rows(txt):
        r=[l.strip() for l in txt.strip('\n').split('\n')]
        c=C(max(map(len,r)),len(r))
        for y,l in enumerate(r):
            for x,ch in enumerate(l): c.p[y][x]=ch
        return c
    def set(s,x,y,c):
        if 0<=x<s.w and 0<=y<s.h and c is not None: s.p[y][x]=c
    def get(s,x,y): return s.p[y][x] if 0<=x<s.w and 0<=y<s.h else None
    def rect(s,x0,y0,x1,y1,c):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1): s.set(x,y,c)
    def box(s,x0,y0,x1,y1,c):
        for x in range(x0,x1+1): s.set(x,y0,c); s.set(x,y1,c)
        for y in range(y0,y1+1): s.set(x0,y,c); s.set(x1,y,c)
    def ell(s,cx,cy,rx,ry,c,ring=None):
        # pixel aspect ~1.7 wide: rx in pixels already
        for y in range(s.h):
            for x in range(s.w):
                d=((x+.5-cx)/rx)**2+((y+.5-cy)/ry)**2
                if d<=1:
                    if ring is not None and d>((rx-1)/rx)**2 and d>((ry-1.3)/ry)**2: s.set(x,y,ring)
                    else: s.set(x,y,c)
    def line(s,x0,y0,x1,y1,c):
        n=max(abs(x1-x0),abs(y1-y0),1)
        for i in range(n+1):
            s.set(round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n),c)
    def paste(s,o,ox,oy,transparent=None):
        for y in range(o.h):
            for x in range(o.w):
                ch=o.p[y][x]
                if ch!=transparent: s.set(ox+x,oy+y,ch)
    def mirror(s):  # left half -> right half
        for y in range(s.h):
            for x in range(s.w//2): s.p[y][s.w-1-x]=s.p[y][x]
        return s
    def txt(s): return '\n'.join(''.join(r) for r in s.p)

A=1.7  # aspecto de pixel (ancho/alto)
def disc(c,cx,cy,r,col):
    rx=r/A*1.0+0.5; ry=r
    for y in range(int(cy-ry-1),int(cy+ry+2)):
        for x in range(int(cx-rx-1),int(cx+rx+2)):
            if ((x+.5-cx)/rx)**2+((y+.5-cy)/ry)**2<=1: c.set(x,y,col)
def stroke(c,pts,r,col,out=None):
    seq=[]
    for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
        n=int(max(abs(x1-x0)*A,abs(y1-y0)))+1
        for i in range(n+1): seq.append((x0+(x1-x0)*i/n,y0+(y1-y0)*i/n))
    if out is not None:
        for x,y in seq: disc(c,x,y,r+1.2,out)
    for x,y in seq: disc(c,x,y,r,col)
def bez(p0,p1,p2,n=12):
    return [((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in [i/n for i in range(n+1)]]
