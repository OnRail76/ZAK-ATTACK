#!/usr/bin/env python3
"""hoja de diseño de un jefe: bossheet.py módulo fase pf0 pf1 pf2 salida título"""
import sys, io, contextlib, importlib
sys.path.insert(0, '/home/claude/zak/gfx'); sys.path.insert(0, '/home/claude/zak/tools')
from PIL import Image, ImageDraw, ImageFont
from pal import atari_rgb as A
import world
mod = importlib.import_module(sys.argv[1]); fase = int(sys.argv[2])
pf = [int(v, 16) for v in sys.argv[3:6]]; out = sys.argv[6]; title = sys.argv[7]; notes = sys.argv[8].split('|')
cols = {'.': A(0), '1': A(pf[0]), '2': A(pf[1]), '3': A(pf[2]), '4': A(0x0E)}
def render(c, S):
    im = Image.new('RGB', (c.w * 2 * S, c.h * S), A(0)); d = ImageDraw.Draw(im)
    for y in range(c.h):
        for x in range(c.w):
            d.rectangle((x * 2 * S, y * S, x * 2 * S + 2 * S - 1, y * S + S - 1), fill=cols[c.p[y][x]])
    return im
_argv = sys.argv; sys.argv = ['atlas', '/tmp/claude-0/-home-claude/48632d28-6815-583d-b6bb-3ab1adc0ebad/scratchpad/_atlas.png']
with contextlib.redirect_stdout(io.StringIO()):
    import atlas as AT
sys.argv = _argv
def cells(c):
    return [tuple(''.join(c.p[cy * 8 + y][cx * 4:cx * 4 + 4]) for y in range(8)) for cy in range(9) for cx in range(10)]
c0 = cells(mod.frame(0)); oth = [cells(mod.frame(n)) for n in range(1, 4)]
anim = [i for i in range(90) if any(o[i] != c0[i] for o in oth)]
bad = [i for i, cl in enumerate(c0) if any('4' in r for r in cl) and any('3' in r for r in cl)]
W, H = 1800, 1500
pg = Image.new('RGB', (W, H), (14, 12, 26)); d = ImageDraw.Draw(pg)
fb = ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf', 44)
fm = ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf', 24)
fr = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 22)
d.text((40, 30), title, font=fb, fill=(255, 196, 64))
d.text((40, 92), '10 × 9 caracteres ANTIC 4 (40 × 72 píxeles), paleta de la fase %d · 4 cuadros de animación' % fase, font=fr, fill=(170, 170, 190))
for i in range(4):
    im = render(mod.frame(i), 5); x = 40 + i * (im.width + 30)
    pg.paste(im, (x, 150)); d.text((x, 150 + im.height + 8), 'cuadro %d' % (i + 1), font=fm, fill=(220, 220, 230))
L = getattr(world, 'fase%d' % fase)(); L.canvas(L.arena + 29, world.GROUND - 9, mod.frame(0), 'bg')
scr = AT.screen(L, L.arena, [('zak', 40, 136, ('diag', False))]); scr = scr.resize((scr.width * 3, scr.height * 3), Image.NEAREST)
pg.paste(scr, (40, 600)); d.text((40, 600 + scr.height + 8), 'En la arena: Zak plantado apuntando en diagonal', font=fm, fill=(220, 220, 230))
notes.append('%d caracteres del jefe, %d celdas animadas.' % (len(set(c0)), len(anim)))
y = 600
for n in notes:
    first = True
    for part in n.split('\\n'):
        d.text((1040, y), ('•  ' if first else '    ') + part, font=fr, fill=(220, 220, 230)); y += 36; first = False
pg.save(out)
fr_ = [render(mod.frame(n), 8) for n in range(4)]
fr_[0].save(out.replace('.png', '.gif'), save_all=True, append_images=fr_[1:], duration=200, loop=0)
print('celdas con rojo y blanco a la vez (no permitido):', bad)
