#!/usr/bin/env python3
"""Genera las imágenes del atlas y del manual desde las mismas fuentes gráficas del juego
(gfx/*.py) y desde capturas del emulador. uso: render_assets.py carpeta_gfx carpeta_capturas salida"""
import sys, os
GFX, SHOTS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, GFX)
from PIL import Image, ImageDraw
from pal import atari_rgb
from sprites import SHIP, SHIP_COLORS, ENEMIES, COMMON
from tiles import T, SECTORS, PF3
from scenery import SETS, build as build_scr, crater_round, crater_over, crystal, flesh
from bosses import BOSS_DEF
from canvas import C
os.makedirs(OUT, exist_ok=True)
SX, SY = 10, 6                       # píxel del Atari ~1,7:1
def rows(s): return [r.strip() for r in s.strip('\n').split('\n')]
def canvas(w, h, bg): return Image.new('RGBA', (w * SX, h * SY), bg)
def dot(d, x, y, col, w=1, h=1): d.rectangle([x * SX, y * SY, (x + w) * SX - 1, (y + h) * SY - 1], fill=col)
def save(im, name): im.save(os.path.join(OUT, name + '.png'))
def slug(s):
    import unicodedata
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return ''.join(c if c.isalnum() else '_' for c in s).strip('_')
TR = (0, 0, 0, 0)
# nave
cols = {'a': atari_rgb(SHIP_COLORS['P0']), 'b': atari_rgb(SHIP_COLORS['P1']), 'c': atari_rgb(SHIP_COLORS['P0'] | SHIP_COLORS['P1'])}
for k, v in SHIP.items():
    r = rows(v); im = canvas(10, len(r) + 2, TR); d = ImageDraw.Draw(im)
    for y, row in enumerate(r):
        for x, ch in enumerate(row):
            if ch in cols: dot(d, x + 1, y + 1, cols[ch])
    save(im, 'ship_' + k)
r = rows(SHIP['centro'])
for name, on, col in (('p0', 'ac', SHIP_COLORS['P0']), ('p1', 'bc', SHIP_COLORS['P1'])):
    im = canvas(10, len(r) + 2, TR); d = ImageDraw.Draw(im)
    for y, row in enumerate(r):
        for x, ch in enumerate(row):
            if ch in on: dot(d, x + 1, y + 1, atari_rgb(col))
    save(im, 'ship_' + name)
# enemigos y comunes (todos los frames)
def enemy(e, f, bg=TR, pad=1):
    n, s, role, col, wd, frames = e
    fr = rows(frames[f % len(frames)]); m = 2 if wd == 'D' else 1
    im = canvas(8 * m + 2 * pad, len(fr) * m + 2 * pad, bg); d = ImageDraw.Draw(im)
    for y, row in enumerate(fr):
        for x, ch in enumerate(row):
            if ch == 'X': dot(d, pad + x * m, pad + y * m, atari_rgb(col), m, m)
    return im
for e in ENEMIES + COMMON:
    for f in range(len(e[5])): save(enemy(e, f), 'en_%s_%d' % (slug(e[0]), f))
# tiles de suelo y cráteres, sobre la paleta de su sector
def pf(c, S, name):
    m = {'.': S['BG'], '1': S['PF0'], '2': S['PF1'], '3': S['PF2']}
    im = canvas(c.w, c.h, (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    for y in range(c.h):
        for x in range(c.w): dot(d, x, y, atari_rgb(m[c.p[y][x]]))
    save(im, name)
GROUND = {1: ['torreta', 'contenedor', 'crater'], 2: ['polipo_cerrado', 'polipo_abierto', 'bolsa_acida', 'crater', 'k'],
          3: ['torreta_cuadrada', 'surtidor', 'surtidor_activo', 'crater'], 4: ['cristal_torreta', 'emisor_laser', 'crater', 'k', 'q'],
          5: ['torreta_parasita', 'bomba_bio', 'crater', 'k', 'q']}
for S in SECTORS:
    n = S['n']
    for k in GROUND[n]:
        c = SETS[n]['meta'][k] if k in ('k', 'q') else C.rows(T[k])
        pf(c, S, 'tile%d_%s' % (n, {'k': 'crater_redondo', 'q': 'crater_suelo'}.get(k, k)))
    pf(build_scr(n), S, 'mapa%d' % n)
# jefes (con y sin impacto)
for i, (name, sub, fn, pal, wp) in enumerate(BOSS_DEF):
    c = fn()
    for tag, p in (('', pal), ('_hit', dict(pal, PF2=0x0E))):
        pf(c, p, 'boss%d%s' % (i + 1, tag))
# capturas del juego: recorte del área de juego (playfield estrecho) o pantalla completa
for f in os.listdir(SHOTS):
    if not f.endswith('.png'): continue
    im = Image.open(os.path.join(SHOTS, f)).convert('RGB')
    full = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    full.save(os.path.join(OUT, 'full_' + f))
    crop = im.crop((56, 0, 584, 480)).resize((528 * 2, 480 * 2), Image.NEAREST)
    crop.save(os.path.join(OUT, 'game_' + f))
print('ok', len(os.listdir(OUT)))
