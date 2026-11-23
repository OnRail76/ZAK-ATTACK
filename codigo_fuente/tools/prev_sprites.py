import sys; sys.path.insert(0,'gfx')
from PIL import Image
from pal import atari_rgb
import sprites
S=6
def grid(t): return [l for l in t.strip('\n').split('\n')]
def draw(im,x0,y0,g,cols):
    for y,l in enumerate(g):
        for x,ch in enumerate(l):
            if ch in cols:
                for dy in range(S):
                    for dx in range(2*S): im.putpixel((x0+x*2*S+dx,y0+y*S+dy),cols[ch])
im=Image.new('RGB',(12*8*2*S,2*22*S+4*18*S),atari_rgb(0x90))
for i,(k,g) in enumerate(sprites.ZAK.items()):
    draw(im,i*10*2*S//1+10,10,grid(g),{'F':atari_rgb(0x2C),'R':atari_rgb(0x44)})
ec=[0x08,0x08,0x36,0x36,0x96,0x96,0xC8,0xC8,0xDA,0xDA,0x1E,0x1E,0x0E,0x1C]
for i,(k,g) in enumerate(sprites.EN.items()):
    draw(im,(i%9)*10*2*S+10,24*S+(i//9)*18*S+10,grid(g),{'X':atari_rgb(ec[i])})
im.save('shots/sprites_prev.png')
