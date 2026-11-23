# RATTUS PRIME · jefe final (propuesta). Cabeza de rata gigante del ejército R.A.T.A.:
# casco metálico con remaches, ojos encendidos (puntos débiles), boca con incisivos (núcleo).
# 40 x 72 píxeles ANTIC 4 = 10 x 9 caracteres. 1 PF0 (pelo), 2 PF1 (ámbar), 3 PF2 (rojo), 4 PF3 (blanco, inverso)
import math
from canvas import C

W, H = 40, 72

def ellipse(c, cx, cy, rx, ry, col):
    for y in range(c.h):
        for x in range(c.w):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: c.set(x, y, col)

def head():
    c = C(W, H)
    # orejas grandes y redondas (pelo con interior rojo)
    ellipse(c, 6, 11, 6.5, 11, '1'); ellipse(c, 6.5, 12, 3.8, 7.5, '3')
    ellipse(c, 34, 11, 6.5, 11, '1'); ellipse(c, 33.5, 12, 3.8, 7.5, '3')
    # cráneo
    ellipse(c, 20, 25, 15, 19, '1')
    # hocico largo que acaba en punta
    for y in range(30, 62):
        half = 15 - (y - 30) * 0.42
        if half < 1.5: half = 1.5
        c.rect(int(20 - half), y, int(19 + half), y, '1')
    # casco metálico con remaches y cresta
    for y in range(6, 15):
        half = int(11 + (y - 6) * 0.45)
        c.rect(20 - half, y, 19 + half, y, '2')
    c.rect(8, 15, 31, 16, '3')
    for x in (10, 15, 24, 29): c.rect(x, 9, x, 10, '1')
    c.rect(18, 3, 21, 7, '2'); c.rect(19, 1, 20, 3, '3')
    # cejas fruncidas
    c.line(7, 19, 15, 23, '.'); c.line(7, 20, 15, 24, '.')
    c.line(32, 19, 24, 23, '.'); c.line(32, 20, 24, 24, '.')
    # cuencas
    for cx in (11, 28): ellipse(c, cx + .5, 28, 4.6, 4.6, '.')
    # nariz en la punta del hocico
    ellipse(c, 20, 52, 3.2, 2.6, '3')
    return c

def eyes(c, f):
    """ojos encendidos: iris ámbar con pupila roja que late (4 cuadros)"""
    for cx in (11, 28):
        r = (3.2, 3.6, 4.0, 3.6)[f % 4]
        if f % 4 == 3:                       # apagados: solo un rescoldo rojo
            ellipse(c, cx + .5, 28, 1.4, 2.4, '3')
            continue
        ellipse(c, cx + .5, 28, r, r, '2')
        ellipse(c, cx + .5, 28, 1.4, 2.4, '3')
        if f % 2 == 0: c.set(cx + 1, 26, '2')

def mouth(c, f):
    """bajo la nariz: boca negra con dos incisivos blancos (celdas inversas); masca"""
    op = (0, 1, 2, 1)[f % 4]
    c.rect(15, 56, 24, 58 + op, '.')
    c.rect(16, 57, 19, 64 + op, '4'); c.rect(20, 57, 23, 64 + op, '4')
    c.rect(19, 57, 20, 64 + op, '.')
    c.rect(15, 65 + op, 24, 66 + op, '1')

def whiskers(c, f):
    d = (0, 1, 0, -1)[f % 4]
    for y0, y1 in ((46, 42 + d), (49, 49 + d), (52, 56 + d)):
        c.line(12, y0, 0, y1, '2'); c.line(27, y0, 39, y1, '2')

def frame(n):
    c = head()
    eyes(c, n); mouth(c, n); whiskers(c, n)
    return c

# puntos débiles (columna, fila, ancho, alto, vida) en caracteres, relativos al bloque
PARTS = [(3, 7, 4, 2, 44),     # boca (núcleo): se expone al romper los dos ojos
         (2, 2, 2, 2, 16),     # ojo izquierdo
         (6, 2, 2, 2, 16)]     # ojo derecho
