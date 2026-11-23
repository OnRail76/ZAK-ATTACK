# Logotipo ZAK ATTACK: 160 x 24 (ANTIC 4, 3 filas de caracteres, juego de caracteres propio)
# 3 = relleno (degradado por DLI línea a línea), 2 = brillo, 1 = contorno
from canvas import C
G = {
'Z': """
############
############
.......####.
......####..
.....####...
....####....
...####.....
..####......
.####.......
############
############
""",
'A': """
....####....
...######...
..###..###..
..###..###..
.###....###.
.###....###.
.##########.
###......###
###......###
###......###
###......###
""",
'K': """
###.....####
###....####.
###...####..
###..####...
###.####....
#######.....
###.####....
###..####...
###...####..
###....####.
###.....####
""",
'T': """
############
############
....####....
....####....
....####....
....####....
....####....
....####....
....####....
....####....
....####....
""",
'C': """
...#########
.###########
####........
###.........
###.........
###.........
###.........
###.........
####........
.###########
...#########
""",
}
def logo():
    c = C(160, 24)
    x = 4
    for ch in 'ZAK ATTACK':
        if ch == ' ': x += 8; continue
        g = [l for l in G[ch].strip('\n').split('\n')]
        for gy, row in enumerate(g):
            sl = (10 - gy) // 4            # cursiva
            for gx, p in enumerate(row):
                if p == '#':
                    for dy in (0, 1): c.set(x + gx + sl + 1, 1 + gy * 2 + dy, '3')
        x += 16
    # brillo en la primera línea de cada trazo y contorno alrededor
    body = [[c.p[y][x] == '3' for x in range(160)] for y in range(24)]
    for y in range(24):
        for x in range(160):
            if body[y][x] and (y == 0 or not body[y - 1][x]): c.p[y][x] = '2'
            if not body[y][x]:
                if any(0 <= y + dy < 24 and 0 <= x + dx < 160 and body[y + dy][x + dx]
                       for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                    c.p[y][x] = '1'
    return c
# degradado del relleno (PF2) por línea: amarillo -> naranja -> rojo
GRAD = [0x1E, 0x1E, 0x1C, 0x1C, 0x1A, 0x2A, 0x2A, 0x28, 0x28, 0x26, 0x36, 0x36,
        0x34, 0x34, 0x44, 0x44, 0x42, 0x42, 0x44, 0x46, 0x36, 0x28, 0x1A, 0x1C]
COLORS = dict(bk=0x00, pf0=0x40, pf1=0x0E)
