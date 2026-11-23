#!/usr/bin/env python3
"""Convierte capturas crudas de run8 (384x240, códigos de color Atari) a PNG."""
import sys, os
sys.path.insert(0,'/home/claude/zak/gfx')
from PIL import Image
from pal import atari_rgb
P=[atari_rgb(i) for i in range(256)]
for f in sys.argv[1:]:
    d=open(f,'rb').read()
    im=Image.new('RGB',(384,240))
    im.putdata([P[b] for b in d])
    im=im.crop((32,0,352,240)).resize((640,480),Image.NEAREST)
    im.save(f.rsplit('.',1)[0]+'.png')
