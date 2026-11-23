# ZAK ATTACK · escenarios y jefes dibujados en texto (ANTIC 4: 4x8 por carácter)
# Píxeles: . = fondo (COLBK), 1 = PF0, 2 = PF1, 3 = PF2, 4 = PF3 (carácter inverso)
# Cada fase: bloques -> nivel de 22 filas x N columnas, fondo periódico, eventos y jefe.
from canvas import C

ROWS = 22
GROUND = 17          # fila de la superficie del suelo normal

def T(txt):
    """bloque de texto -> lista de filas (ancho múltiplo de 4, alto múltiplo de 8)"""
    r = [l.strip() for l in txt.strip('\n').split('\n')]
    w = max(map(len, r)); r = [l.ljust(w, '.') for l in r]
    assert w % 4 == 0 and len(r) % 8 == 0, (w, len(r), r[0])
    return r

class Level:
    def __init__(s, name, ncols, period):
        s.name = name; s.n = ncols; s.period = period
        s.fg = [[None] * ncols for _ in range(ROWS)]          # (pixels, clase)
        s.bg = [[None] * period for _ in range(ROWS)]
        s.events = []
        s.blocks = {}
    def block(s, name, txt, cls='bg'):
        s.blocks[name] = (T(txt), cls)
    def _cells(s, name):
        px, cls = s.blocks[name]
        h = len(px) // 8; w = len(px[0]) // 4
        for cy in range(h):
            for cx in range(w):
                cell = tuple(px[cy * 8 + y][cx * 4:cx * 4 + 4] for y in range(8))
                yield cx, cy, cell, cls
    def put(s, col, row, name, layer='fg'):
        g = s.fg if layer == 'fg' else s.bg
        for cx, cy, cell, cls in s._cells(name):
            c = col + cx
            if layer == 'bg': c %= s.period
            if 0 <= row + cy < ROWS and 0 <= c < len(g[0]):
                g[row + cy][c] = (cell, cls)
    def fill(s, c0, c1, r0, r1, name, layer='fg'):
        px, cls = s.blocks[name]; w = len(px[0]) // 4; h = len(px) // 8
        for r in range(r0, r1 + 1, h):
            for c in range(c0, c1 + 1, w): s.put(c, r, name, layer)
    def clear(s, c0, c1, r0, r1):
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1): s.fg[r][c] = None
    def canvas(s, col, row, cv, cls='bg'):
        """pega un lienzo canvas.C (ancho múltiplo de 4, alto de 8) como celdas"""
        rows = [''.join(r) for r in cv.p]
        name = '_cv%d_%d' % (col, row)
        s.blocks[name] = (rows, cls); s.put(col, row, name)
    def boss_anim(s, col, row, frames, speed=7):
        """coloca el cuadro 0 del jefe; las celdas que cambian entre cuadros reciben un
        carácter propio que el juego reescribe (animación sin sprites)"""
        s.canvas(col, row, frames[0], 'bg')
        s.banim = getattr(s, 'banim', [])
        h = frames[0].h // 8; w = frames[0].w // 4
        def cell(cv, cx, cy): return tuple(''.join(cv.p[cy * 8 + y][cx * 4:cx * 4 + 4]) for y in range(8))
        for cy in range(h):
            for cx in range(w):
                cs = [cell(f, cx, cy) for f in frames]
                if len(set(cs)) == 1: continue
                inv = [any('4' in r for r in c) for c in cs]
                assert len(set(inv)) == 1, 'celda animada con y sin blanco (%d,%d)' % (cx, cy)
                tag = 'bg#%d' % len(s.banim)
                s.fg[row + cy][col + cx] = (cs[0], tag)
                s.banim.append((cs[0], tag, cs, speed))
    def ev(s, col, kind, row=0, param=0):
        s.events.append((col, kind, row, param))

# ---------------------------------------------------------------------------
# Piezas comunes
# ---------------------------------------------------------------------------
def common(L, ground_top, ground_fill, crate=True):
    L.block('gtop', ground_top, 'solid')
    L.block('gfill', ground_fill, 'solid')
    L.block('warn', """
3..3
.33.
....
3..3
.33.
....
3..3
.33.
""")
    L.block('rubble', """
....
....
....
.2..
.12.
1211
1121
2111
""")
    if crate:
        L.block('crate', """
22222222
21311312
21131132
21113112
21131132
21311312
23111132
22222222
22222222
23111132
21311312
21131132
21113112
21131132
21311312
22222222
""", 'solid')
    # torreta 2x2 (pasable; se destruye a tiros)
    L.block('turret', """
....3333
...32223
2222.223
....3223
...33333
..311113
..31.113
..311113
.3333333
.3111113
.3121213
.3111113
.3333333
.3.3.3.3
.3333333
.3111113
""")
    L.block('turretx', """
........
........
........
........
........
........
........
........
...2....
...12.2.
..21121.
.2111211
.3333333
.3.3.3.3
.3333333
.3111113
""")

def ground(L, c0, c1, row=GROUND):
    L.fill(c0, c1, row, row, 'gtop')
    L.fill(c0, c1, row + 1, ROWS - 1, 'gfill')

# ---------------------------------------------------------------------------
# FASE 1 · CALLEJÓN NEÓN
# ---------------------------------------------------------------------------
def fase1():
    L = Level('CALLEJON NEON', 300, 16)
    common(L, """
3333
2323
3333
1111
1.11
1111
11.1
1111
""", """
1111
1.11
1111
11.1
1111
.111
1111
111.
""")
    # fondo: rascacielos con ventanas, estrellas
    L.block('star', """
....
....
.2..
....
....
....
....
....
""")
    L.block('wall', """
1111
1221
1111
1111
1111
1..1
1111
1111
""")
    L.block('wall2', """
1111
1..1
1111
1111
1111
1221
1111
1111
""")
    L.block('roof', """
....
..1.
..1.
.111
1111
1111
1221
1111
""")
    L.block('roofb', """
....
....
....
....
1111
1111
1..1
1111
""")
    L.block('neon', """
1111
3333
3..3
3.33
3..3
3333
1111
1111
""")
    L.block('pipe', """
.11.
.11.
.11.
.11.
.11.
.11.
.11.
.11.
""")
    # plataformas: escalera de incendios y toldo
    L.block('fesc', """
33333333
3.3.3.3.
.1....1.
.1....1.
.1....1.
.1....1.
.1....1.
.1....1.
""", 'plat')
    L.block('awn', """
32323232
23232323
.2.2.2.2
........
........
........
........
........
""", 'plat')
    L.block('bin', """
.33.
3333
3113
3113
3113
3113
3113
3333
""", 'solid')
    # skyline periódico (16 columnas)
    heights = [8, 8, 5, 5, 5, 11, 11, 3, 3, 3, 3, 9, 9, 6, 6, 13]
    for c, h in enumerate(heights):
        top = GROUND - h
        L.put(c, top, 'roof' if c % 2 == 0 else 'roofb', 'bg')
        for r in range(top + 1, GROUND):
            L.put(c, r, 'wall' if (r + c) % 3 else 'wall2', 'bg')
        for r in range(0, top):
            if (c * 7 + r * 5) % 11 == 0: L.put(c, r, 'star', 'bg')
    L.put(3, GROUND - 3, 'neon', 'bg'); L.put(4, GROUND - 3, 'neon', 'bg')
    # cartel de neón en honor a nuestro primer juego: VORTICE 5
    FONT = {'V': ['2.2', '2.2', '2.2', '2.2', '.2.'], 'O': ['222', '2.2', '2.2', '2.2', '222'],
            'R': ['22.', '2.2', '22.', '2.2', '2.2'], 'T': ['222', '.2.', '.2.', '.2.', '.2.'],
            'I': ['222', '.2.', '.2.', '.2.', '222'], 'C': ['222', '2..', '2..', '2..', '222'],
            'E': ['222', '2..', '22.', '2..', '222'], '5': ['222', '2..', '222', '..2', '222'], ' ': ['...'] * 5}
    def sign_cell(ch):
        rows = ['3333', '1111'] + [('1' + FONT[ch][y]).replace('.', '1') for y in range(5)] + ['3333']
        return '\n'.join(rows)
    L.block('sgnL', '3333\n3111\n3111\n3111\n3111\n3111\n3111\n3333')
    L.block('sgnR', '3333\n1113\n1113\n1113\n1113\n1113\n1113\n3333')
    L.block('sgnH', '....\n.3..\n.3..\n.3..\n.3..\n.3..\n.3..\n.3..')
    SIGN_COL, SIGN_ROW = 22, 8
    L.put(SIGN_COL, SIGN_ROW, 'sgnL')
    for i, ch in enumerate('VORTICE 5'):
        L.block('sg_%d' % i, sign_cell(ch))
        L.put(SIGN_COL + 1 + i, SIGN_ROW, 'sg_%d' % i)
    L.put(SIGN_COL + 10, SIGN_ROW, 'sgnR')
    L.put(SIGN_COL + 2, SIGN_ROW - 1, 'sgnH'); L.put(SIGN_COL + 8, SIGN_ROW - 1, 'sgnH')
    for r in range(GROUND - 13, GROUND): L.put(14, r, 'pipe', 'bg')
    # ---- recorrido
    ground(L, 0, 299)
    L.clear(58, 62, GROUND, ROWS - 1)          # primer foso
    L.clear(150, 155, GROUND, ROWS - 1)        # calle cortada
    L.clear(214, 218, GROUND, ROWS - 1)
    L.put(30, GROUND - 2, 'crate'); L.put(44, GROUND - 2, 'crate'); L.put(46, GROUND - 2, 'crate')
    L.put(46, GROUND - 4, 'crate')
    L.put(40, GROUND - 1, 'bin'); L.put(96, GROUND - 1, 'bin'); L.put(130, GROUND - 1, 'bin')
    for c in range(104, 116, 2): L.put(c, 13, 'awn')
    for c in range(146, 160, 2): L.put(c, 13, 'fesc')
    L.put(170, GROUND - 2, 'crate'); L.put(172, GROUND - 2, 'crate'); L.put(172, GROUND - 4, 'crate')
    for c in range(186, 198, 2): L.put(c, 12, 'awn')
    for c in range(206, 226, 2): L.put(c, 13, 'fesc')
    L.put(236, GROUND - 2, 'crate'); L.put(238, GROUND - 2, 'crate')
    # oleadas: soldados (abajo) y drones (arriba)
    for c in range(16, 252, 11):
        L.ev(c, 'soldier', GROUND)
    for c in range(40, 252, 17):
        L.ev(c, 'drone', 6)
    L.ev(110, 'fish', GROUND - 1)
    # ---- arena y jefe MEKDOZER 1 (bulldog excavador)
    L.arena = 260
    boss = C(40, 56)
    boss.rect(4, 44, 39, 55, '1')                       # orugas
    for x in range(5, 39, 4): boss.rect(x, 46, x + 1, 53, '2')
    boss.box(4, 44, 39, 55, '3')
    boss.rect(10, 22, 37, 43, '3')                       # cuerpo
    boss.rect(12, 24, 35, 41, '1')
    for x in (14, 20, 26, 32): boss.rect(x, 26, x + 1, 39, '3')
    boss.rect(16, 4, 36, 21, '3')                        # cabeza bulldog
    boss.rect(18, 6, 34, 19, '1')
    boss.rect(16, 0, 19, 5, '3'); boss.rect(33, 0, 36, 5, '3')   # orejas
    boss.rect(20, 8, 23, 11, '2'); boss.rect(29, 8, 32, 11, '2')  # ojos
    boss.rect(20, 14, 32, 17, '3')                       # hocico/rejilla
    for x in range(21, 32, 3): boss.rect(x, 15, x, 16, '1')
    boss.rect(0, 30, 11, 43, '2')                        # pala
    boss.rect(0, 30, 3, 43, '3')
    for y in (33, 37, 41): boss.rect(1, y, 2, y, '1')
    frames = []
    for f in range(4):
        bf = C(40, 56); bf.paste(boss, 0, 0)
        if f == 1:                                          # destello
            bf.rect(21, 9, 22, 10, '3'); bf.rect(30, 9, 31, 10, '3')
        if f == 3:                                          # apagados
            bf.rect(20, 8, 23, 11, '1'); bf.rect(29, 8, 32, 11, '1')
        frames.append(bf)
    L.boss_anim(L.arena + 29, GROUND - 7, frames, 7)
    # partes: (columna, fila relativas al bloque, ancho, alto, vida)
    L.boss = dict(kind=1, col=L.arena + 29, row=GROUND - 7, w=10, h=7,
                  parts=[(4, 0, 6, 3, 30),       # cabeza (punto débil)
                         (0, 3, 3, 3, 14)],      # pala
                  name='MEKDOZER 1')
    L.colors = dict(bk=0x80, pf0=0x52, pf1=0x2A, pf2=0x08, pf3=0x0E)
    L.encol = (0x08, 0x46)
    L.enemies = ('soldier', 'drone')
    L.anim = []
    return L

# ---------------------------------------------------------------------------
# FASE 2 · METRO  (andenes, túnel de azulejos; caer a las vías = muerte)
# ---------------------------------------------------------------------------
def fase2():
    L = Level('METRO', 300, 16)
    common(L, """
2222
2222
3333
3.3.
3333
1111
1111
1111
""", """
1111
1111
1.11
1111
1111
11.1
1111
1111
""")
    L.block('tile', """
1111
1111
1111
....
11.1
11.1
11.1
....
""")
    L.block('tile2', """
1.11
1.11
1.11
....
1111
1111
1111
....
""")
    L.block('band', """
2222
2222
2222
2222
....
....
....
....
""")
    L.block('ceil', """
....
....
....
1111
....
....
....
....
""")
    L.block('lamp', """
1111
.11.
2222
2222
.22.
....
....
....
""")
    L.block('pillar', """
.33.
.33.
.33.
.33.
.33.
.33.
.33.
.33.
""")
    L.block('sign', """
33333333
3.2.2..3
3.2.22.3
3.2.2..3
33333333
........
........
........
""")
    L.block('rail', """
....
....
....
....
3333
1..1
1111
....
""")
    L.block('bench', """
33333333
3......3
3......3
3......3
33333333
.3....3.
.3....3.
.3....3.
""", 'solid')
    L.block('walk', """
33333333
2.2.2.2.
........
........
........
........
........
........
""", 'plat')
    # fondo periódico: techo con cable y focos, azulejos, franja de color, cartel y pilar
    for c in range(16):
        L.put(c, 1, 'ceil', 'bg')
        if c in (3, 11): L.put(c, 2, 'lamp', 'bg')
        for r in range(3, GROUND):
            L.put(c, r, 'band' if r == 8 else ('tile' if (r + c) % 2 else 'tile2'), 'bg')
        if c == 15:
            for r in range(2, GROUND): L.put(c, r, 'pillar', 'bg')
    L.put(6, 5, 'sign', 'bg')
    # andenes y vías
    ground(L, 0, 299)
    pits = ((50, 55), (104, 109), (160, 165), (212, 217))
    for g0, g1 in pits:
        L.clear(g0, g1, GROUND, ROWS - 1)
        for c in range(g0, g1 + 1): L.put(c, ROWS - 1, 'rail')
    for g0, g1 in ((104, 109), (212, 217)):
        for c in range(g0 - 2, g1 + 3, 2): L.put(c, 13, 'walk')       # pasarelas sobre las vías
    for c in (30, 76, 130, 186, 236): L.put(c, GROUND - 1, 'bench')
    for c in range(66, 78, 2): L.put(c, 12, 'walk')
    # enemigos: drones arriba; perros y ratas soldado abajo
    for c in range(24, 252, 16): L.ev(c, 'drone', 5)
    for i, c in enumerate(range(14, 252, 10)): L.ev(c, ('dog', 'soldier')[i % 2], GROUND)
    L.ev(150, 'fish', GROUND - 1)
    # ---- jefe: la cabina de un convoy de metro que entra en la estación
    L.arena = 260
    b = C(40, 72)
    b.rect(2, 0, 37, 71, '3')                                   # carrocería plateada
    b.box(2, 0, 37, 71, '1')
    b.rect(8, 2, 31, 7, '1'); b.rect(10, 3, 29, 6, '2')         # rótulo de destino
    for x in range(12, 28, 4): b.rect(x, 4, x + 1, 5, '1')
    b.rect(5, 10, 34, 33, '1')                                  # parabrisas
    b.rect(14, 15, 25, 33, '3'); b.rect(15, 11, 17, 15, '3'); b.rect(22, 11, 24, 15, '3')   # rata conductora
    b.rect(16, 19, 17, 20, '2'); b.rect(22, 19, 23, 20, '2')
    b.line(6, 12, 10, 12, '3'); b.line(29, 12, 33, 12, '3')     # reflejos
    b.rect(2, 38, 37, 41, '2')                                  # franja amarilla
    b.rect(4, 44, 35, 51, '1')                                  # rejilla
    for x in range(6, 34, 3): b.rect(x, 45, x, 50, '3')
    b.rect(4, 56, 11, 63, '1'); b.rect(5, 57, 10, 62, '2')      # faro izquierdo
    b.rect(28, 56, 35, 63, '1'); b.rect(29, 57, 34, 62, '2')    # faro derecho
    b.rect(0, 64, 39, 71, '1'); b.rect(16, 64, 23, 69, '3')     # parachoques y enganche
    frames = []
    for f in range(4):
        bf = C(40, 72); bf.paste(b, 0, 0)
        if f == 1:
            bf.rect(7, 59, 8, 60, '3'); bf.rect(31, 59, 32, 60, '3')     # destello de faros
        if f == 3:
            bf.rect(16, 19, 17, 20, '3'); bf.rect(22, 19, 23, 20, '3')   # ojos apagados
            bf.rect(5, 57, 10, 62, '1'); bf.rect(29, 57, 34, 62, '1')    # faros apagados
        frames.append(bf)
    L.boss_anim(L.arena + 29, GROUND - 9, frames, 7)
    L.boss = dict(kind=2, col=L.arena + 29, row=GROUND - 9, w=10, h=9,
                  parts=[(3, 1, 4, 3, 30),     # parabrisas con la conductora (núcleo)
                         (1, 7, 2, 1, 12),     # faro izquierdo
                         (7, 7, 2, 1, 12)],    # faro derecho
                  name='METROPLEX III')
    L.colors = dict(bk=0x00, pf0=0x82, pf1=0x1C, pf2=0x0A, pf3=0x0E)
    L.encol = (0x46, 0x96)
    L.enemies = ('drone', 'dog', 'soldier')
    L.anim = []
    return L

# ---------------------------------------------------------------------------
# FASE 3 · FACTORÍA DEL MIEDO  (vigas, cintas, fosos de metal fundido)
# ---------------------------------------------------------------------------
def fase3():
    L = Level('FACTORIA DEL MIEDO', 300, 16)
    common(L, """
3333
1331
3333
1111
1.1.
.1.1
1111
1111
""", """
1111
1.1.
.1.1
1111
1111
1.1.
.1.1
1111
""")
    L.block('girder', """
1111
1..1
.11.
1..1
1111
....
....
....
""")
    L.block('col', """
.11.
.11.
.11.
.11.
.11.
.11.
.11.
.11.
""")
    L.block('pipeh', """
....
....
1111
2222
1111
....
....
....
""")
    L.block('glow', """
....
.2..
....
....
...2
....
....
....
""")
    L.block('lava', """
2.2.
2222
2323
3232
2222
2222
2222
2222
""", 'haz')
    L.block('lava2', """
.2.2
2222
3232
2323
2222
2222
2222
2222
""", 'haz')
    L.block('belt', """
3333
2.2.
3333
1111
....
....
....
....
""", 'plat')
    L.block('belt2', """
3333
.2.2
3333
1111
....
....
....
....
""", 'plat')
    for c in range(16):
        L.put(c, 2, 'girder', 'bg')
        if c in (3, 11):
            for r in range(3, GROUND): L.put(c, r, 'col', 'bg')
        if c not in (3, 11): L.put(c, 8, 'pipeh', 'bg')
        if (c * 5) % 7 == 1: L.put(c, 5, 'glow', 'bg')
    ground(L, 0, 299)
    for g0, g1 in ((40, 45), (90, 96), (140, 145), (190, 197), (230, 235)):
        L.clear(g0, g1, GROUND, ROWS - 1)
        for c in range(g0, g1 + 1):
            L.put(c, ROWS - 2, 'lava'); L.put(c, ROWS - 1, 'gfill')
    for c in range(56, 72): L.put(c, 13, 'belt')
    for c in range(104, 118): L.put(c, 12, 'belt')
    for c in range(150, 166): L.put(c, 13, 'belt')
    L.put(80, GROUND - 2, 'crate'); L.put(124, GROUND - 2, 'crate'); L.put(126, GROUND - 2, 'crate')
    for c in range(18, 252, 13): L.ev(c, 'soldier', GROUND)
    for c in range(30, 252, 19): L.ev(c, 'jumper', GROUND)
    for c in range(44, 252, 23): L.ev(c, 'drone', 5)
    L.ev(170, 'fish', GROUND - 1)
    L.anim = [('lava', ['lava', 'lava2'], 7), ('belt', ['belt', 'belt2'], 3)]
    # CONTROL CENTRAL II: computadora con bobinas por ojos y rejilla de luces por boca
    import boss3
    L.arena = 260
    L.boss_anim(L.arena + 29, GROUND - 9, [boss3.frame(n) for n in range(4)], 7)
    L.boss = dict(kind=3, col=L.arena + 29, row=GROUND - 9, w=10, h=9,
                  parts=boss3.PARTS, name='CONTROL CENTRAL II')
    L.colors = dict(bk=0x00, pf0=0x82, pf1=0x36, pf2=0x1A, pf3=0x0E)
    L.encol = (0x08, 0xC6)
    L.enemies = ('soldier', 'jumper')
    return L

# ---------------------------------------------------------------------------
# FASE 4 · PLANTA QUIMICA  (tubos de cultivo, charcos tóxicos)
# ---------------------------------------------------------------------------
def fase4():
    L = Level('PLANTA QUIMICA', 300, 16)
    common(L, """
3333
3..3
3333
1111
1311
1111
1131
1111
""", """
1111
1311
1111
1131
1111
1311
1111
1131
""")
    L.block('panel', """
1111
1...
1...
1...
1...
1...
1...
1...
""")
    L.block('ptop', """
1111
....
....
....
....
....
....
....
""")
    L.block('tubetop', """
33333333
31111113
.3....3.
.3....3.
.3....3.
.3....3.
.3....3.
.3....3.
""")
    L.block('tube', """
.3....3.
.3.2..3.
.3....3.
.32222.3
.322223.
.32.223.
.322223.
.322223.
""")
    L.block('tube2', """
.3....3.
.3..2.3.
.3....3.
.3222223
.322223.
.3222.3.
.322223.
.322223.
""")
    L.block('tubebot', """
.322223.
.322223.
33333333
31111113
33333333
........
........
........
""")
    L.block('light', """
1111
.33.
.33.
....
....
....
....
....
""")
    L.block('goo', """
....
....
.2..
2222
2.22
2222
2222
2222
""", 'haz')
    L.block('goo2', """
....
....
..2.
2222
22.2
2222
2222
2222
""", 'haz')
    L.block('shelf', """
33333333
1......1
........
........
........
........
........
........
""", 'plat')
    for c in range(16):
        L.put(c, 0, 'light' if c % 4 == 1 else 'ptop', 'bg')
        for r in range(1, GROUND):
            if c % 4 == 0: L.put(c, r, 'panel', 'bg')
            elif r % 4 == 0: L.put(c, r, 'ptop', 'bg')
    for t in (2, 10):
        L.put(t, 7, 'tubetop', 'bg')
        for r in range(8, 15): L.put(t, r, 'tube' if r % 2 else 'tube2', 'bg')
        L.put(t, 15, 'tubebot', 'bg')
    ground(L, 0, 299)
    for g0, g1 in ((48, 52), (120, 125), (176, 180)):
        L.clear(g0, g1, GROUND, ROWS - 1)
    for g0, g1 in ((84, 88), (210, 216)):
        for c in range(g0, g1 + 1): L.put(c, GROUND, 'goo')
    for c in range(60, 74, 2): L.put(c, 13, 'shelf')
    for c in range(76, 84, 2): L.put(c, 9, 'shelf')
    for c in range(196, 212, 2): L.put(c, 13, 'shelf')
    L.put(100, GROUND - 2, 'crate'); L.put(160, GROUND - 2, 'crate'); L.put(162, GROUND - 2, 'crate')
    for c in range(22, 250, 24): L.ev(c, 'jumper', GROUND)
    for c in range(36, 250, 28): L.ev(c, 'bug', GROUND)
    L.ev(140, 'fish', GROUND - 1); L.ev(232, 'can', GROUND - 1)
    L.anim = [('goo', ['goo', 'goo2'], 15), ('tube', ['tube', 'tube2'], 15)]
    L.arena = 260
    L.boss = dict(kind=4, col=L.arena + 30, row=GROUND - 4, w=0, h=0, parts=[(0, 0, 0, 0, 40)],
                  name='QUIMERA-9', sprite=True)
    L.colors = dict(bk=0x90, pf0=0x92, pf1=0xC8, pf2=0x0C, pf3=0x0E)
    L.encol = (0xC6, 0xDA)
    L.enemies = ('jumper', 'bug')
    return L

# ---------------------------------------------------------------------------
# FASE 5 · INDUSTRIAS RATA  (fortaleza, luces de emergencia, núcleo)
# ---------------------------------------------------------------------------
def fase5():
    L = Level('INDUSTRIAS RATA', 300, 16)
    common(L, """
3333
2222
1111
1.11
1111
11.1
1111
1111
""", """
1111
1.11
1111
11.1
1111
1.11
1111
11.1
""")
    L.block('wallp', """
1111
1..1
1.11
1111
1111
11.1
1..1
1111
""")
    L.block('wallq', """
1111
1111
1..1
1..1
1111
1111
1111
1111
""")
    L.block('seam', """
1111
....
....
....
....
....
....
....
""")
    L.block('pillar', """
1..1
1..1
1..1
1..1
1..1
1..1
1..1
1..1
""")
    L.block('alarm', """
.22.
2332
2332
.22.
1111
1111
1111
1111
""")
    L.block('alarm2', """
.22.
2222
2222
.22.
1111
1111
1111
1111
""")
    L.block('core', """
....2222....
..22333322..
.2333..3332.
.233....332.
.233....332.
.2333..3332.
..22333322..
....2222....
""")
    L.block('zap', """
.3..
..3.
.3..
3...
.3..
..3.
.3..
3...
""", 'haz')
    L.block('zap2', """
..3.
.3..
..3.
...3
..3.
.3..
..3.
...3
""", 'haz')
    L.block('ledge', """
33333333
21212121
........
........
........
........
........
........
""", 'plat')
    for c in range(16):
        for r in range(0, GROUND):
            if c % 4 == 0 or r % 3 == 0: L.put(c, r, 'wallq' if (c % 4 == 0 and r % 3 == 1) else 'seam' if c % 4 else 'pillar', 'bg')
    L.put(6, 1, 'alarm', 'bg'); L.put(14, 1, 'alarm', 'bg')
    L.put(9, 5, 'core', 'bg')
    ground(L, 0, 299)
    for g0, g1 in ((52, 56), (112, 117), (186, 190)):
        L.clear(g0, g1, GROUND, ROWS - 1)
    for g0, g1 in ((80, 82), (150, 152), (226, 228)):
        for c in range(g0, g1 + 1):
            for r in range(GROUND - 3, GROUND): L.put(c, r, 'zap')
    for c in range(62, 76, 2): L.put(c, 13, 'ledge')
    for c in range(196, 210, 2): L.put(c, 13, 'ledge')
    L.put(96, GROUND - 2, 'crate')
    for i, c in enumerate(range(14, 252, 9)):
        L.ev(c, ('soldier', 'dog', 'bug', 'soldier', 'dog')[i % 5], GROUND)
    for c in range(24, 252, 15):
        L.ev(c, 'drone', 5)
    L.ev(160, 'fish', GROUND - 1)
    L.anim = [('zap', ['zap', 'zap2'], 3), ('alarm', ['alarm', 'alarm2'], 15)]
    # RATTUS PRIME: cabeza de rata gigante del ejército R.A.T.A.
    import boss5
    L.arena = 260
    L.boss_anim(L.arena + 29, GROUND - 9, [boss5.frame(n) for n in range(4)], 7)
    L.boss = dict(kind=5, col=L.arena + 29, row=GROUND - 9, w=10, h=9,
                  parts=boss5.PARTS, name='RATTUS PRIME')
    L.colors = dict(bk=0x00, pf0=0x54, pf1=0x1C, pf2=0x44, pf3=0x0E)
    L.encol = (0x08, 0x96)
    L.enemies = ('soldier', 'dog', 'drone', 'bug')
    return L
