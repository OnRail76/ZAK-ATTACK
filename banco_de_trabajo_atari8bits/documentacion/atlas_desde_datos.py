#!/usr/bin/env python3
"""ZAK ATTACK · atlas gráfico Atari 8 bits, dibujado desde los mismos datos que usa el juego."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gfx'))
from PIL import Image, ImageDraw, ImageFont
from pal import atari_rgb as A
import world, sprites, logo

OUT = sys.argv[1] if len(sys.argv) > 1 else 'atlas.png'
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FR = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
FM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
def F(p, s): return ImageFont.truetype(p, s)

BG = (14, 12, 26); PANEL = (26, 22, 44); EDGE = (92, 70, 160); GOLD = (255, 196, 64); TXT = (225, 225, 235); DIM = (150, 150, 175)
ZCOL = (0x0C, 0x44)
PHASES = [world.fase1(), world.fase2(), world.fase3(), world.fase4(), world.fase5()]
PIXC = {'.': 'bk', '0': 'bk', '1': 'pf0', '2': 'pf1', '3': 'pf2', '4': 'pf3'}

def grid(t): return [l.ljust(8, '.') for l in t.strip('\n').split('\n')]

# ---------------------------------------------------------------- pantalla simulada
def screen(L, c0, actors=(), hud=True, quimera=None):
    """devuelve imagen 320x(8+176) en píxeles hires (1 cc = 2 px)"""
    col = {k: A(v) for k, v in L.colors.items()}
    im = Image.new('RGB', (320, 184), col['bk'])
    px = im.load()
    for r in range(world.ROWS):
        for c in range(40):
            wc = c0 + c
            cell = L.fg[r][wc] if wc < L.n else None
            if cell is None: cell = L.bg[r][wc % L.period]
            if cell is None: continue
            for y in range(8):
                for x in range(4):
                    k = cell[0][y][x]
                    if k in '.0': continue
                    rgb = col[PIXC[k]]
                    X = (c * 4 + x) * 2; Y = 8 + r * 8 + y
                    px[X, Y] = rgb; px[X + 1, Y] = rgb
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 319, 7), fill=A(0x00))
    for kind, x, y, data in actors:          # x en cc de pantalla, y = línea de pies
        if kind == 'zak':
            fr, flip = data
            g = grid(sprites.ZAK[fr])
            for gy, row in enumerate(g):
                for gx, ch in enumerate(row[::-1] if flip else row):
                    if ch == '.': continue
                    rgb = A(ZCOL[0] if ch == 'F' else ZCOL[1])
                    d.rectangle(((x + gx) * 2, 8 + y - 20 + gy, (x + gx) * 2 + 1, 8 + y - 20 + gy), fill=rgb)
        elif kind == 'en':
            fr, colr = data
            g = grid(sprites.EN[fr])
            for gy, row in enumerate(g):
                for gx, ch in enumerate(row):
                    if ch == 'X':
                        d.rectangle(((x + gx) * 2, 8 + y - 16 + gy, (x + gx) * 2 + 1, 8 + y - 16 + gy), fill=A(colr))
        elif kind == 'bul':
            d.rectangle((x * 2, 8 + y, x * 2 + 3, 8 + y + 1), fill=A(0x0E))
    if quimera:
        x, y, fr = quimera
        g = [l.ljust(16, '.') for l in sprites.QUIMERA[fr].strip('\n').split('\n')]
        for gy, row in enumerate(g):
            for gx, ch in enumerate(row):
                if ch == '.': continue
                rgb = A(0xC6 if ch == 'A' else 0x0C)
                d.rectangle(((x + gx * 2) * 2, 8 + y - 24 + gy, (x + gx * 2) * 2 + 3, 8 + y - 24 + gy), fill=rgb)
    return im

def hud_text(im, L, idx, scale):
    d = ImageDraw.Draw(im)
    f = F(MONO, int(6.5 * scale))
    d.text((6 * scale, 0.5 * scale), 'PUNTOS 004200   VIDA ♥♥♥  ZAKx3  FASE %d' % (idx + 1), font=f, fill=A(0x0C))

def up(im, s): return im.resize((im.width * s, im.height * s), Image.NEAREST)

# ---------------------------------------------------------------- logo
def logo_img():
    c = logo.logo()
    im = Image.new('RGB', (320, 24), A(0))
    p = im.load()
    for y in range(24):
        for x in range(160):
            k = c.p[y][x]
            if k == '.': continue
            rgb = A(logo.GRAD[y]) if k == '3' else A(0x0E) if k == '2' else A(0x42)
            p[x * 2, y] = rgb; p[x * 2 + 1, y] = rgb
    return im

# ---------------------------------------------------------------- lienzo del atlas
W, H = 2400, 3200
atlas = Image.new('RGB', (W, H), BG)
D = ImageDraw.Draw(atlas)

def panel(x0, y0, x1, y1, title=None):
    D.rounded_rectangle((x0, y0, x1, y1), 14, fill=PANEL, outline=EDGE, width=3)
    if title:
        D.text((x0 + 22, y0 + 14), title, font=F(FB, 34), fill=GOLD)
    return y0 + 64

def text(x, y, s, size=24, fill=TXT, font=FR):
    D.text((x, y), s, font=F(font, size), fill=fill)

def bullets(x, y, items, size=24, gap=36, width=None):
    for it in items:
        D.ellipse((x, y + size * 0.42, x + 9, y + size * 0.42 + 9), fill=GOLD)
        text(x + 22, y, it, size); y += gap
    return y

# cabecera
D.rectangle((0, 0, W, 300), fill=(8, 6, 16))
atlas.paste(up(logo_img(), 3), (40, 40))
text(40, 130 + 0, 'ATLAS GRÁFICO  ·  VERSIÓN ATARI 8 BITS', 54, GOLD, FB)
text(40, 200, 'Redibujado con los límites reales de la máquina: cada píxel de esta hoja sale de los datos que leerá el juego,', 26, DIM)
text(40, 236, 'con la paleta NTSC del emulador atari800. Por Tony y Claude A.I.', 26, DIM)
text(1720, 40, 'Atari 400/800/XL/XE · 48 KB', 30, TXT, FM)
text(1720, 82, 'ANTIC 4 + PMG + POKEY', 30, TXT, FM)
text(1720, 124, 'NTSC · joystick de 1 botón', 30, TXT, FM)
text(1720, 166, 'XEX · ATR · cartucho', 30, TXT, FM)

# ---------------------------------------------------------------- reglas
y = panel(40, 330, 1180, 820, 'LO QUE CABE (Y LO QUE SE QUEDA FUERA)')
bullets(64, y + 6, [
    'Un solo jugador: Zak ocupa P0+P1 (dos colores superpuestos). Mika sale.',
    'Dos enemigos móviles a la vez (P2 y P3), un color cada uno.',
    'Dos modelos de enemigo por fase (la fase 5 los mezcla de dos en dos).',
    'Torretas, peligros y jefes grandes: hechos con caracteres.',
    'Un solo arma: tiro recto, 2 balas en pantalla. En el aire,',
    '    arriba+fuego dispara en diagonal o en vertical. Sin power-ups de arma.',
    'Recogibles: pescado (recupera la vida) y lata dorada (vida extra).',
    'Balas = misiles en modo quinto player: siempre blancas.',
    'Saltar = arriba (joystick de un botón), agacharse = abajo.',
], 24, 40)

y = panel(1220, 330, 2360, 820, 'TÉCNICA DE PANTALLA')
bullets(1244, y + 6, [
    'Marcador: 1 línea ANTIC 2 (fuente de la ROM).',
    'Juego: 22 filas ANTIC 4 = 160 × 176 píxeles, 4 colores + PF3.',
    'Scroll fino horizontal (HSCROL) sobre un anillo de 64 columnas.',
    'Un juego de caracteres de 1 KB por fase (máx. 128): fondo,',
    '    peligros, plataformas de un sentido, sólidos y jefe.',
    'Fondo repetido cada 16 columnas + primer plano comprimido.',
    'Una DLI cambia caracteres y colores bajo el marcador.',
    'Caracteres animados reescribiendo 8 bytes (lava, cintas, chispas).',
    'Logotipo: juego propio + degradado línea a línea por DLI.',
], 24, 40)

# ---------------------------------------------------------------- Zak
y0 = 860
y = panel(40, y0, 1180, y0 + 420, 'ZAK  ·  P0 (PELO) + P1 (EQUIPO)')
names = ['Quieto', 'Correr 1', 'Correr 2', 'Correr 3', 'Salto', 'Agachado', 'Tiro arriba', 'Caído']
S = 6
for i, fr in enumerate(sprites.ZAK):
    g = grid(sprites.ZAK[fr]); x0 = 70 + i * 136
    for gy, row in enumerate(g):
        for gx, ch in enumerate(row):
            if ch == '.': continue
            D.rectangle((x0 + gx * 2 * S // 1 // 1 * 1, y + 20 + gy * S, x0 + gx * 2 * S + 2 * S - 1, y + 20 + gy * S + S - 1),
                        fill=A(ZCOL[0] if ch == 'F' else ZCOL[1]))
    text(x0, y + 150, names[i], 20, DIM)
text(70, y + 200, '8 × 20 píxeles (anchura normal de player = 8 color clocks). Espejo para mirar a la izquierda.', 21, DIM)
text(70, y + 232, 'Colores: $0C pelo blanco, $44 bandana y equipo. Balas en $0E (quinto player), un punto más brillantes.', 21, DIM)
for i, c in enumerate((0x0C, 0x44, 0x0E)):
    D.rectangle((70 + i * 80, y + 280, 130 + i * 80, y + 320), fill=A(c))
    text(70 + i * 80, y + 325, '$%02X' % c, 18, DIM, FM)

# enemigos
y = panel(1220, y0, 2360, y0 + 420, 'ENEMIGOS  ·  P2 / P3, UN COLOR')
ens = [('soldier1', 'soldier2', 'Rata soldado', 0x08, 'F1 F3 F5'), ('drone1', 'drone2', 'Dron mosquito', 0x46, 'F1 F2 F5'),
       ('dog1', 'dog2', 'Perro guardián', 0x96, 'F2 F5'), ('jumper1', 'jumper2', 'Rata saltadora', 0xC6, 'F3 F4'),
       ('bug1', 'bug2', 'Bicho mutágeno', 0xDA, 'F4 F5'), ('boom1', 'boom2', 'Explosión', 0x1E, 'todas'),
       ('fish', 'can', 'Pescado / lata', 0x0E, 'recogibles')]
S = 4
for i, (a, b, nm, c, ph) in enumerate(ens):
    x0 = 1250 + (i % 4) * 278; yy = y + 10 + (i // 4) * 170
    for k, fr in enumerate((a, b)):
        g = grid(sprites.EN[fr]); cc = c if fr != 'can' else 0x1C
        for gy, row in enumerate(g):
            for gx, ch in enumerate(row):
                if ch == 'X':
                    D.rectangle((x0 + k * 74 + gx * 2 * S, yy + gy * S, x0 + k * 74 + gx * 2 * S + 2 * S - 1, yy + gy * S + S - 1), fill=A(cc))
    text(x0, yy + 72, nm, 21, TXT, FM)
    text(x0, yy + 100, ph, 18, DIM)

# ---------------------------------------------------------------- fases
y0 = 1320
panel(40, y0, 2360, y0 + 1260, 'LAS 5 FASES  ·  PANTALLAS SIMULADAS CON LOS DATOS DEL JUEGO')
scenes = [
    (14, [('zak', 26, 136, ('run1', False)), ('en', 92, 136, ('soldier1', 0x08)), ('en', 132, 64, ('drone1', 0x46)), ('bul', 38, 124, None), ('bul', 90, 70, None)]),
    (28, [('zak', 30, 112, ('jump', False)), ('en', 100, 112, ('dog1', 0x96)), ('en', 120, 48, ('drone2', 0x46)), ('bul', 42, 98, None)]),
    (52, [('zak', 40, 104, ('stand', False)), ('en', 120, 136, ('jumper2', 0xC6)), ('en', 90, 136, ('soldier2', 0x08)), ('bul', 52, 92, None)]),
    (56, [('zak', 24, 136, ('crouch', False)), ('en', 70, 104, ('jumper1', 0xC6)), ('en', 110, 136, ('bug1', 0xDA)), ('bul', 36, 129, None)]),
    (58, [('zak', 30, 104, ('up', False)), ('en', 100, 136, ('dog2', 0x96)), ('en', 140, 136, ('soldier1', 0x08)), ('bul', 36, 70, None)]),
]
desc = [
    ('Ciudad nocturna, escaleras de incendios, toldos y el cartel de neón VORTICE 5.', 'Ratas soldado + drones. Torretas en cornisas.', 'GRUÑÓN-01, bulldog excavador'),
    ('Techo del convoy en marcha; caer entre vagones es perder una vida.', 'Drones + perros guardián.', 'LOCOMORRÓN, frontal con 2 torretas'),
    ('Vigas, tuberías, cintas transportadoras y metal fundido animado.', 'Ratas soldado + saltadoras. Torretas.', 'EL HORNO, 3 respiraderos + reactor'),
    ('Tubos de cultivo burbujeantes, estanterías y charcos tóxicos.', 'Saltadoras + bichos mutágenos.', 'QUIMERA-9, sprite doble (P2+P3)'),
    ('Fortaleza: paneles, alarmas que parpadean, núcleo y arcos eléctricos.', 'Las 4 familias, de dos en dos. Torretas.', 'RATTUS PRIME, exoesqueleto'),
]
for i, L in enumerate(PHASES):
    c0, act = scenes[i]
    im = up(screen(L, c0, act), 2)
    hud_text(im, L, i, 2)
    col = i % 3; row = i // 3
    x0 = 70 + col * 770; yy = y0 + 80 + row * 610
    if i >= 3: x0 = 70 + (i - 3) * 770 + 385
    atlas.paste(im, (x0, yy))
    D.rectangle((x0 - 2, yy - 2, x0 + im.width + 1, yy + im.height + 1), outline=EDGE, width=2)
    text(x0, yy + im.height + 10, 'FASE %d · %s' % (i + 1, L.name), 26, GOLD, FB)
    text(x0, yy + im.height + 46, desc[i][0], 18, TXT)
    text(x0, yy + im.height + 72, desc[i][1] + '  Jefe: ' + desc[i][2] + '.', 18, DIM)
    for k, key in enumerate(['bk', 'pf0', 'pf1', 'pf2']):
        D.rectangle((x0 + 520 + k * 40, yy + im.height + 104, x0 + 552 + k * 40, yy + im.height + 128), fill=A(L.colors[key]), outline=EDGE)
    text(x0, yy + im.height + 104, 'BK/PF0/PF1/PF2: ' + ' '.join('$%02X' % L.colors[k] for k in ['bk', 'pf0', 'pf1', 'pf2']), 17, DIM, FM)

# ---------------------------------------------------------------- jefes
y0 = 2610
panel(40, y0, 2360, y0 + 560, 'JEFES  ·  CUERPO DE CARACTERES, PARTES MÓVILES CON SPRITES')
bossinfo = [
    ('GRUÑÓN-01', 'Pala que embiste a ras de suelo (P2): salta.', 'Escombros que caen (P3). Punto débil: la cabeza.'),
    ('LOCOMORRÓN', 'Dos torretas alternas con aviso.', 'Rotas las dos, se abre el motor.'),
    ('EL HORNO', 'Tres respiraderos lanzan bolas de fuego.', 'Apagados los tres, queda el reactor.'),
    ('QUIMERA-9', 'Salta entre alturas (sprite 32 × 24).', 'Misiles desde su lomo. Todo él es blanco.'),
    ('RATTUS PRIME', 'Barridos de brazo alto/bajo: salta o agáchate.', 'Sin brazos, dispara a la cápsula.'),
]
for i, L in enumerate(PHASES):
    B = L.boss
    c0 = L.arena
    if B.get('sprite'):
        im = screen(L, c0, [('zak', 34, 136, ('stand', False))], quimera=(96, 136, 'stand'))
    else:
        im = screen(L, c0, [('zak', 34, 136 if i != 1 else 112, ('stand', False))])
    im = im.crop((48, 8 + 40, 320, 8 + 176))
    im = up(im, 2).resize((440, int(136 * 440 / 272)), Image.NEAREST)
    x0 = 66 + i * 458; yy = y0 + 80
    atlas.paste(im, (x0, yy))
    D.rectangle((x0 - 2, yy - 2, x0 + im.width + 1, yy + im.height + 1), outline=EDGE, width=2)
    n, a, b = bossinfo[i]
    text(x0, yy + im.height + 12, 'B%d · %s' % (i + 1, n), 24, GOLD, FB)
    text(x0, yy + im.height + 48, a, 17, TXT)
    text(x0, yy + im.height + 72, b, 17, DIM)
    parts = len(B['parts'])
    text(x0, yy + im.height + 100, '%d parte%s con vida propia' % (parts, '' if parts == 1 else 's'), 17, DIM)

atlas.save(OUT)
print('atlas', OUT, atlas.size)
