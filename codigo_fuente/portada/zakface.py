#!/usr/bin/env python3
"""Retrato de Zak en pixel art (dibujado a mano con código, inspirado en la foto real).
Lienzo de 120x120 píxeles; cabeza ligeramente inclinada como en la foto."""
import math
from PIL import Image, ImageDraw

N = 120
OUTL = (26, 20, 30)
FUR = (138, 124, 114)      # gris pardo
FUR_L = (178, 166, 154)    # luces
FUR_D = (102, 90, 86)      # sombra
STRIPE = (64, 54, 54)      # rayas atigradas
WHITE = (242, 240, 234)
WHITE_S = (204, 202, 206)
EAR_P = (214, 150, 150)
EAR_PD = (172, 108, 116)
NOSE = (236, 150, 154)
NOSE_D = (176, 94, 104)
IRIS = (204, 194, 40)
IRIS_L = (232, 226, 96)
IRIS_D = (140, 142, 22)
PUPIL = (16, 14, 14)
RED, RED_L, RED_D = (226, 34, 46), (255, 118, 98), (124, 10, 26)

TILT = math.radians(-11)
CX, CY = 60, 64
def T(x, y):
    dx, dy = x - CX, y - CY
    return (CX + dx * math.cos(TILT) - dy * math.sin(TILT), CY + dx * math.sin(TILT) + dy * math.cos(TILT))
def TP(pts): return [T(x, y) for x, y in pts]
def ell(cx, cy, rx, ry, n=40, a0=0, a1=360):
    return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
            for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]

def face(with_band=True):
    img = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # ---- orejas (detrás de la cabeza)
    d.polygon(TP([(16, 52), (12, 6), (52, 32)]), fill=FUR)
    d.polygon(TP([(68, 30), (106, 2), (104, 52)]), fill=FUR)
    d.polygon(TP([(21, 44), (17, 14), (44, 33)]), fill=EAR_P)
    d.polygon(TP([(75, 32), (101, 11), (99, 45)]), fill=EAR_P)
    d.polygon(TP([(24, 42), (21, 22), (36, 34)]), fill=EAR_PD)
    d.polygon(TP([(82, 34), (98, 20), (97, 40)]), fill=EAR_PD)
    for a, b in (((22, 40), (30, 32)), ((25, 44), (34, 38)), ((90, 40), (84, 34)), ((94, 44), (88, 39))):
        d.line(TP([a, b]), fill=FUR_L)                       # pelos del interior
    # ---- cabeza: óvalo ancho con mechones en las mejillas
    head = ell(60, 66, 46, 37)
    d.polygon(TP(head), fill=FUR)
    tufts = [(13, 62), (6, 72), (15, 74), (8, 84), (19, 84), (14, 94), (26, 92)]
    d.polygon(TP(tufts + [(30, 70)]), fill=FUR)
    tufts_r = [(107, 60), (115, 70), (106, 72), (113, 82), (102, 82), (108, 92), (95, 90)]
    d.polygon(TP(tufts_r + [(92, 68)]), fill=FUR_D)
    # sombra lateral derecha y luz en la frente izquierda
    d.polygon(TP(ell(76, 74, 30, 26, a0=-70, a1=80) + [(76, 74)]), fill=FUR_D)
    d.polygon(TP(ell(44, 44, 20, 12)), fill=FUR_L)
    # ---- blanco: franja entre los ojos, hocico, mejilla izquierda y barbilla
    d.polygon(TP([(57, 48), (64, 47), (68, 62), (74, 78), (48, 80), (54, 62)]), fill=WHITE)
    d.polygon(TP(ell(53, 88, 12, 9)), fill=WHITE)
    d.polygon(TP(ell(73, 87, 12, 9)), fill=WHITE)
    d.polygon(TP(ell(63, 96, 8, 4)), fill=WHITE_S)
    d.polygon(TP([(12, 76), (22, 72), (34, 82), (38, 98), (24, 100), (14, 90)]), fill=WHITE)
    for wx, wy in ((50, 87), (54, 90), (48, 91), (76, 86), (80, 89), (74, 90)):
        d.point(T(wx, wy), fill=WHITE_S)
    # ---- rayas atigradas: la "M" de la frente y las mejillas
    d.polygon(TP([(46, 32), (74, 32), (66, 50), (54, 50)]), fill=FUR_D)
    for pts in ([(47, 33), (51, 49)], [(53, 31), (56, 47)], [(60, 30), (60, 45)], [(67, 31), (64, 47)], [(73, 33), (69, 49)],
                [(38, 38), (44, 51)], [(33, 42), (37, 52)], [(82, 38), (76, 51)], [(87, 42), (83, 52)]):
        d.line(TP(pts), fill=STRIPE, width=2)
    for pts in ([(28, 58), (14, 55)], [(29, 66), (13, 65)], [(30, 72), (18, 75)], [(92, 56), (106, 52)], [(93, 63), (108, 61)], [(91, 70), (104, 73)]):
        d.line(TP(pts), fill=STRIPE, width=2)
    d.line(TP([(30, 56), (34, 52), (40, 52)]), fill=STRIPE, width=1)
    d.line(TP([(82, 50), (88, 50), (92, 54)]), fill=STRIPE, width=1)
    # ---- ojos almendrados, párpado algo caído: mirada decidida
    for ex, ey, side in ((42, 62, -1), (79, 60, 1)):
        d.polygon(TP(ell(ex, ey, 11, 8)), fill=OUTL)
        d.polygon(TP(ell(ex, ey, 9.5, 6.6)), fill=IRIS)
        d.polygon(TP(ell(ex, ey + 2, 8.5, 4.2, a0=0, a1=180)), fill=IRIS_L)
        d.polygon(TP(ell(ex, ey, 2.2, 5.6)), fill=PUPIL)
        # párpado superior en diagonal (ceño de comando)
        hi, lo = (ey - 9, ey - 3) if side < 0 else (ey - 3, ey - 9)
        d.polygon(TP([(ex - 12, hi - 3), (ex + 12, lo - 3), (ex + 12, lo), (ex - 12, hi)]), fill=FUR)
        d.line(TP([(ex - 11, hi), (ex + 11, lo)]), fill=OUTL, width=2)
        d.point(T(ex + 3, ey + 1), fill=(255, 255, 240)); d.point(T(ex + 4, ey + 1), fill=(255, 255, 240))
        d.point(T(ex + 3, ey + 2), fill=(255, 255, 240))
    # ---- nariz y boca
    d.polygon(TP([(56, 76), (72, 75), (70, 79), (64, 84), (58, 80)]), fill=NOSE)
    d.line(TP([(57, 76), (71, 75)]), fill=(250, 190, 190))
    d.line(TP([(60, 81), (64, 84), (68, 80)]), fill=NOSE_D)
    d.line(TP([(65, 83), (65, 87)]), fill=OUTL)
    d.line(TP([(65, 87), (61, 89), (58, 88)]), fill=OUTL)
    d.line(TP([(65, 87), (69, 89), (72, 87)]), fill=OUTL)
    # ---- bandana
    if with_band:
        band = [(14, 40), (60, 33), (108, 37), (108, 46), (60, 42), (14, 50)]
        d.polygon(TP(band), fill=RED)
        d.line(TP([(14, 40), (60, 33), (108, 37)]), fill=RED_L, width=1)
        d.line(TP([(14, 50), (60, 42), (108, 46)]), fill=RED_D, width=1)
        d.line(TP([(16, 44), (60, 37), (106, 41)]), fill=(240, 70, 70), width=1)
    # ---- contorno negro alrededor de todo
    a = img.split()[3]
    out = Image.new('RGBA', (N, N), (0, 0, 0, 0)); od = out.load(); ap = a.load(); ip = img.load()
    for y in range(N):
        for x in range(N):
            if ap[x, y] == 0 and any(0 <= x + dx < N and 0 <= y + dy < N and ap[x + dx, y + dy] > 0
                                     for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                od[x, y] = OUTL + (255,)
    out.alpha_composite(img)
    # bigotes por encima (fuera del contorno)
    wd = ImageDraw.Draw(out)
    for x0, y0, x1, y1 in ((40, 84, 2, 76), (40, 88, 2, 88), (84, 83, 119, 73), (86, 87, 119, 85), (84, 91, 116, 97)):
        wd.line(TP([(x0, y0), (x1, y1)]), fill=(236, 234, 228, 255), width=1)
    return out

def knot_tails(scale):
    """colas de la bandana a la izquierda, en la misma rejilla"""
    img = Image.new('RGBA', (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    k = T(14, 45)
    d.polygon([(k[0], k[1] - 2), (k[0] - 10, k[1] - 9), (k[0] - 16, k[1] - 6), (k[0] - 22, k[1] - 12), (k[0] - 20, k[1] - 4), (k[0] - 8, k[1] + 1)], fill=RED)
    d.polygon([(k[0], k[1] + 1), (k[0] - 8, k[1] + 9), (k[0] - 12, k[1] + 16), (k[0] - 7, k[1] + 17), (k[0] - 3, k[1] + 9)], fill=RED_D)
    d.ellipse((k[0] - 3, k[1] - 3, k[0] + 3, k[1] + 3), fill=RED)
    return img

if __name__ == '__main__':
    f = face()
    t = knot_tails(1)
    t.alpha_composite(f)
    bg = Image.new('RGBA', (N, N), (60, 30, 80, 255)); bg.alpha_composite(t)
    bg.resize((N * 8, N * 8), Image.NEAREST).save('/home/claude/zak/portada/zakface_prev.png')
