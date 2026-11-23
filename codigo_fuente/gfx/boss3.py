# CONTROL CENTRAL II · jefe de la fase 3 (propuesta). Computadora de ciencia ficción:
# dos bobinas de cinta como ojos (giran) y una rejilla de luces como boca (parpadean).
# 40 x 72 píxeles ANTIC 4 = 10 x 9 caracteres. Colores: 1 PF0, 2 PF1, 3 PF2, 4 PF3 (inverso).
import math
from canvas import C

W, H = 40, 72
REELS = ((5, 18), (25, 18))       # esquina sup. izq. de cada ventana de bobina (8 x 16)

def body():
    c = C(W, H)
    # armario: marco claro, paneles oscuros
    c.rect(0, 4, 39, 71, '3'); c.rect(2, 6, 37, 69, '1')
    # remate superior con placa
    c.rect(4, 0, 35, 5, '3'); c.rect(6, 1, 33, 4, '1')
    for x in range(8, 32, 3): c.rect(x, 2, x + 1, 3, '2')
    # franja de rótulo bajo el remate
    c.rect(2, 8, 37, 13, '1'); c.rect(4, 9, 35, 12, '2')
    for x in (7, 11, 15, 19, 23, 27, 31): c.rect(x, 10, x + 1, 11, '1')
    # ventanas de las bobinas
    for x0, y0 in REELS:
        c.rect(x0 - 1, y0 - 1, x0 + 10, y0 + 16, '3')
        c.rect(x0, y0, x0 + 9, y0 + 15, '.')
    # boca: marco de la rejilla de luces (baja, a la altura del disparo de Zak)
    c.rect(4, 44, 35, 63, '3'); c.rect(5, 45, 34, 62, '.')
    # botones y rejilla de ventilación entre ojos y boca, y zócalo
    for y in (37, 39, 41): c.rect(8, y, 31, y, '3')
    c.rect(36, 38, 37, 39, '2'); c.rect(2, 38, 3, 39, '2')
    for y in (66, 68): c.rect(4, y, 35, y, '3')
    return c

def reel(c, x0, y0, frame):
    """bobina de 8 x 16 (2 x 2 caracteres): llanta, cinta, buje y radios que giran"""
    cx, cy = x0 + 4.5, y0 + 8
    for y in range(16):
        for x in range(8):
            dx = (x + 0.5 - 4) * 2.0; dy = y + 0.5 - 8          # píxel 2:1
            r = math.hypot(dx, dy)
            if r <= 7.6:
                c.set(x0 + 1 + x, y0 + y, '2' if r > 5.4 else '.')   # cinta enrollada
            if 6.6 < r <= 7.6: c.set(x0 + 1 + x, y0 + y, '3')         # llanta
    for k in range(3):                                                  # tres radios
        a = math.radians(frame * 40 + k * 120)
        for t in range(1, 6):
            x = cx + math.cos(a) * t / 2.0; y = cy + math.sin(a) * t
            c.set(int(round(x - 0.5)), int(round(y - 0.5)), '3')
    c.rect(x0 + 4, y0 + 7, x0 + 5, y0 + 8, '3' if frame % 2 else '2')  # buje que parpadea

LIGHTS_X = [7, 11, 15, 19, 23, 27, 31]
LIGHTS_Y = [47, 53, 59]
def lights(c, frame):
    """rejilla 7 x 3 de luces de 2 x 3: el color de cada luz recorre la paleta en ola"""
    pal = ['1', '2', '3']
    for j, y in enumerate(LIGHTS_Y):
        for i, x in enumerate(LIGHTS_X):
            k = (i + j * 2 + frame) % 4
            col = '.' if k == 3 else pal[k]
            c.rect(x, y, x + 1, y + 2, col)

def frame(n):
    c = body()
    for x0, y0 in REELS: reel(c, x0, y0, n)
    lights(c, n)
    return c

# puntos débiles (columna, fila, ancho, alto, vida) en caracteres, relativos al bloque
PARTS = [(1, 6, 8, 2, 36),     # boca: núcleo (filas 6-7 = líneas 112-127: tiro normal), se abre cuando caen las bobinas
         (1, 2, 3, 2, 14),     # bobina izquierda
         (6, 2, 3, 2, 14)]     # bobina derecha
