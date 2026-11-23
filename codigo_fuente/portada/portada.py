#!/usr/bin/env python3
"""ZAK ATTACK · portada. La cara de Zak (foto real) pasada a píxeles anchos con paleta Atari,
bandana de comando, ciudad de neón, logotipo y créditos."""
import sys, math, random
sys.path.insert(0, '/home/claude/zak/gfx')
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from pal import PAL
import logo as LG
import sprites as SP

random.seed(5)
A = lambda c: PAL[c & 0xFE]
W, H = 1500, 2000
OUT = sys.argv[1] if len(sys.argv) > 1 else 'zak_attack_portada.png'
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
FBI = '/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf'
FM = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
def F(p, s):
    try: return ImageFont.truetype(p, s)
    except OSError: return ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf', s)

# ------------------------------------------------------------------ fondo
cv = Image.new('RGB', (W, H))
d = ImageDraw.Draw(cv)
top, mid, bot = A(0x50), A(0x42), A(0x22)
for y in range(H):
    t = y / H
    if t < 0.55:
        k = t / 0.55; c = tuple(int(top[i] * (1 - k) + mid[i] * k) for i in range(3))
    else:
        k = (t - 0.55) / 0.45; c = tuple(int(mid[i] * (1 - k) + (8, 4, 12)[i] * k) for i in range(3))
    d.line((0, y, W, y), fill=c)
# bandas de barrido (como líneas de DLI)
for y in range(0, H, 6): d.line((0, y, W, y), fill=(0, 0, 0), width=1)
cv = Image.blend(cv, Image.new('RGB', (W, H), (0, 0, 0)), 0.15)
d = ImageDraw.Draw(cv)
# luna-explosión detrás de la cabeza
glow = Image.new('L', (W, H), 0); g = ImageDraw.Draw(glow)
g.ellipse((260, 360, 1240, 1340), fill=255)
glow = glow.filter(ImageFilter.GaussianBlur(120))
cv = Image.composite(Image.new('RGB', (W, H), A(0x2C)), cv, glow.point(lambda v: int(v * 0.75)))
d = ImageDraw.Draw(cv)
# estrellas
for _ in range(160):
    x, y = random.randrange(W), random.randrange(0, 900)
    s = random.choice((4, 4, 8))
    d.rectangle((x, y, x + s * 2 - 1, y + s - 1), fill=A(random.choice((0x1C, 0x0E, 0x9C))))
# ciudad en píxeles anchos (cada píxel Atari = 12 x 6)
PX, PY = 12, 6
def block(x, y, w, h, c): d.rectangle((x * PX, y * PY, (x + w) * PX - 1, (y + h) * PY - 1), fill=c)
x = 0
base = H // PY
while x < W // PX:
    bw = random.randint(6, 14); bh = random.randint(60, 150)
    far = A(0x52) if random.random() < 0.5 else A(0x62)
    block(x, base - bh - 40, bw, bh + 40, far)
    for wy in range(base - bh - 36, base - 40, 4):
        for wx in range(x + 1, x + bw - 1, 2):
            if random.random() < 0.55: block(wx, wy, 1, 2, A(random.choice((0x1A, 0x2A, 0x2C, 0x0E))))
    x += bw + random.randint(0, 2)
# calle
block(0, base - 40, W // PX, 3, A(0x08))
block(0, base - 37, W // PX, 37, A(0x42))
for yy in range(base - 34, base, 4):
    for xx in range(0, W // PX, 6): block(xx + (yy // 4) % 2 * 3, yy, 2, 1, A(0x32))

# ------------------------------------------------------------------ cara de Zak (pixel art dibujado)
import zakface
fc = zakface.knot_tails(1); fc.alpha_composite(zakface.face())
SC = 9
big = fc.resize((zakface.N * SC, zakface.N * SC), Image.NEAREST)
# sombra suave detrás
sh = Image.new('RGBA', big.size, (0, 0, 0, 0)); sh.paste((10, 0, 20, 170), (0, 0), big.split()[3])
sh = sh.filter(ImageFilter.GaussianBlur(14))
FX, FY = (W - big.width) // 2 + 40, 470
cv.paste(sh, (FX + 24, FY + 30), sh)
cv.paste(big, (FX, FY), big)
d = ImageDraw.Draw(cv)

# ------------------------------------------------------------------ logotipo (el mismo del juego, grande)
c = LG.logo()
S = 9
stops = [(255, 252, 200), (255, 224, 70), (255, 150, 30), (236, 60, 30), (150, 14, 50)]
FIRE = []
for y in range(24):
    t = y / 23 * (len(stops) - 1); i = min(int(t), len(stops) - 2); k = t - i
    FIRE.append(tuple(int(stops[i][j] * (1 - k) + stops[i + 1][j] * k) for j in range(3)))
lx, ly = (W - 160 * S) // 2, 80
for y in range(24):
    for x in range(160):
        k = c.p[y][x]
        if k == '.': continue
        col = FIRE[y] if k == '3' else (255, 255, 236) if k == '2' else (52, 0, 26)
        d.rectangle((lx + x * S + 10, ly + y * 16 + 12, lx + x * S + S - 1 + 10, ly + y * 16 + 27), fill=(10, 0, 12))
        d.rectangle((lx + x * S, ly + y * 16, lx + x * S + S - 1, ly + y * 16 + 15), fill=col)
# lema
f = F(FBI, 64)
txt = 'GATO.  COMANDO.  CAOS.'
tw = d.textlength(txt, font=f)
d.text(((W - tw) / 2 + 4, 488 + 4), txt, font=f, fill=(0, 0, 0))
d.text(((W - tw) / 2, 488), txt, font=f, fill=A(0x1E))

# ------------------------------------------------------------------ Zak de juego y ratas (sprites reales)
def sprite(rows, x, y, cols, s=10):
    for gy, r in enumerate(rows.strip('\n').split('\n')):
        for gx, ch in enumerate(r):
            if ch in cols:
                d.rectangle((x + gx * 2 * s, y + gy * s, x + gx * 2 * s + 2 * s - 1, y + gy * s + s - 1), fill=cols[ch])
gy0 = H - 40 * PY - 20 * 10
sprite(SP.ZAK['run1'], 110, gy0, {'F': A(0x0C), 'R': A(0x44)})
for i in range(6):
    d.rectangle((300 + i * 70, gy0 + 85, 330 + i * 70, gy0 + 95), fill=A(0x0E))
sprite(SP.EN['soldier1'], 1120, H - 40 * PY - 16 * 10, {'X': A(0x08)})
sprite(SP.EN['drone1'], 1180, gy0 - 260, {'X': A(0x46)})
sprite(SP.EN['boom2'], 980, H - 40 * PY - 16 * 10 - 20, {'X': A(0x1E)})

# ------------------------------------------------------------------ franjas y créditos
d.rectangle((0, H - 150, W, H), fill=(8, 6, 14))
d.rectangle((0, H - 156, W, H - 150), fill=A(0x2A))
f1 = F(FB, 54); f2 = F(FM, 34)
t1 = 'ATARI 400 · 800 · XL · XE'
d.text((60, H - 128), t1, font=f1, fill=(240, 240, 245))
d.text((60, H - 62), '48 KB  ·  disco · cartucho · XEX', font=f2, fill=A(0x1C))
t3 = 'Por Tony y Claude A.I.'
d.text((W - 60 - d.textlength(t3, font=f2), H - 62), t3, font=f2, fill=(220, 220, 230))
t4 = '1 jugador · 5 fases'
d.text((W - 60 - d.textlength(t4, font=f2), H - 118), t4, font=f2, fill=(220, 220, 230))
# sello de esquina
d.polygon([(W - 330, 1180), (W, 1180), (W, 1280), (W - 360, 1280)], fill=(224, 32, 44))
f5 = F(FBI, 40)
d.text((W - 320, 1192), '8 BITS DE PURA', font=F(FM, 26), fill=(255, 230, 200))
d.text((W - 320, 1222), 'ACCIÓN FELINA', font=f5, fill=(255, 255, 255))
cv.save(OUT)
print(OUT, cv.size)
