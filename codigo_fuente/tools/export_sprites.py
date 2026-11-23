#!/usr/bin/env python3
"""Exporta los sprites del juego como PNG transparentes (píxel 2:1 como en el Atari) para el atlas y el folleto."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gfx'))
from PIL import Image
from pal import atari_rgb as A
import sprites, logo
OUT = sys.argv[1]
S = 6
def grid(t, w=8): return [l.ljust(w, '.') for l in t.strip('\n').split('\n')]
def save(g, colf, name, pw=2):
    h = len(g); w = len(g[0])
    im = Image.new('RGBA', (w * pw * S, h * S), (0, 0, 0, 0)); p = im.load()
    for y, row in enumerate(g):
        for x, ch in enumerate(row):
            c = colf(ch)
            if c is None: continue
            for yy in range(S):
                for xx in range(pw * S): p[x * pw * S + xx, y * S + yy] = c + (255,)
    im.save(os.path.join(OUT, name + '.png'))
for fr in sprites.ZAK:
    save(grid(sprites.ZAK[fr]), lambda ch: None if ch == '.' else A(0x0C if ch == 'F' else 0x44), 'zak_' + fr)
cols = dict(soldier=0x08, drone=0x46, dog=0x96, jumper=0xC6, bug=0xDA, boom=0x1E, fish=0x0E, can=0x1C)
for fr in sprites.EN:
    base = fr.rstrip('0123456789')
    c = cols.get(base, 0x0E)
    save(grid(sprites.EN[fr]), lambda ch, c=c: A(c) if ch == 'X' else None, 'en_' + fr)
for fr in sprites.QUIMERA:
    save(grid(sprites.QUIMERA[fr], 16), lambda ch: None if ch == '.' else A(0xC6 if ch == 'A' else 0x0C), 'quimera_' + fr, pw=4)
# explosiones de jefe (los 4 cuadros y la paleta de boss.s)
art = ["........\n........\n...XX...\n..XXXX..\n..XXXX..\n...XX...\n........\n........",
       "..X..X..\n...XX...\n.XXXXXX.\nXXXXXXXX\nXXXXXXXX\n.XXXXXX.\n...XX...\n..X..X..",
       "X.XXXX.X\n.XX..XX.\nXX....XX\nX......X\nX......X\nXX....XX\n.XX..XX.\nX.XXXX.X",
       ".X....X.\nX..XX..X\n..X..X..\n.X....X.\n.X....X.\n..X..X..\nX..XX..X\n.X....X."]
pal = [0x0E, 0x2E, 0x3A, 0x44]
for i, a in enumerate(art):
    g = [r for r in a.split('\n') for _ in (0, 1)]
    save(g, lambda ch, c=pal[i]: A(c) if ch == 'X' else None, 'boom_%d' % i)
# logotipo del juego
c = logo.logo(); im = Image.new('RGBA', (320 * 3, 24 * 3), (0, 0, 0, 0)); p = im.load()
for y in range(24):
    for x in range(160):
        k = c.p[y][x]
        if k == '.': continue
        rgb = A(logo.GRAD[y]) if k == '3' else A(0x0E) if k == '2' else A(0x42)
        for yy in range(3):
            for xx in range(6): p[x * 6 + xx, y * 3 + yy] = rgb + (255,)
im.save(os.path.join(OUT, 'logo_atari.png'))
print(len(os.listdir(OUT)), 'sprites')
