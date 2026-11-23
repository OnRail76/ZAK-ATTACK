#!/usr/bin/env python3
"""ZAK ATTACK · generador: dibujos en texto -> src/data.s (charsets, niveles, eventos, sprites, música)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gfx'))
import world, sprites
from music import SONGS

OUT = []
def emit(s=''): OUT.append(s)
def bytes_line(label, data, per=16):
    if label: emit(label + ':')
    for i in range(0, len(data), per):
        emit('        .byte ' + ','.join('$%02X' % b for b in data[i:i + per]))

PIX = {'.': 0, '0': 0, '1': 1, '2': 2, '3': 3, '4': 3}
CLS_ORDER = ['bg', 'haz', 'plat', 'solid']
def CI(c): return CLS_ORDER.index(c.split('#')[0])
EVK = {'soldier': 1, 'drone': 2, 'dog': 3, 'jumper': 4, 'bug': 5, 'fish': 6, 'can': 7, 'turret': 8}

def cell_bytes(cell):
    out = []
    for row in cell:
        b = 0
        for ch in row: b = (b << 2) | PIX[ch]
        out.append(b)
    return bytes(out)

def build_phase(idx, L):
    # recoge celdas usadas (bitmap, clase); inverso si contiene '4'
    used = {}
    blank = (bytes(8), 'bg')
    used[blank] = None
    def key(c):
        cell, cls = c
        return (cell_bytes(cell), cls), any('4' in r for r in cell)
    for r in range(world.ROWS):
        for c in range(L.period):
            assert L.bg[r][c] is None or L.bg[r][c][1] == 'bg', 'fase %d: fondo sólido en fila %d col %d' % (idx + 1, r, c)
    allcells = [L.fg[r][c] for r in range(world.ROWS) for c in range(L.n)] + \
               [L.bg[r][c] for r in range(world.ROWS) for c in range(L.period)]
    for blk in L.blocks.values():               # incluye bloques sin colocar (escombros, torreta rota)
        pass
    extra = ['rubble', 'turretx', 'warn'] + list(getattr(L, 'extra_blocks', []))
    for name in extra:
        for cx, cy, cell, cls in L._cells(name): allcells.append((cell, cls))
    for c in allcells:
        if c is None: continue
        k, inv = key(c)
        used.setdefault(k, None)
    keys = sorted(used.keys(), key=lambda k: (CI(k[1]), k != blank))
    # el mismo bitmap en dos clases cuenta dos veces
    assert len(keys) <= 128, 'fase %d: %d caracteres (máx 128)' % (idx + 1, len(keys))
    code = {k: i for i, k in enumerate(keys)}
    thr = []
    for cl in CLS_ORDER[1:]:
        thr.append(min([code[k] for k in keys if CI(k[1]) >= CLS_ORDER.index(cl)] + [128]))
    charset = bytearray(1024)
    for k, i in code.items(): charset[i * 8:i * 8 + 8] = k[0]
    def cc(c):
        if c is None: return None
        k, inv = key(c)
        return code[k] | (0x80 if inv else 0)
    def blockcodes(name):
        px, cls = L.blocks[name]; w = len(px[0]) // 4; h = len(px) // 8
        g = [[0] * w for _ in range(h)]
        for cx, cy, cell, cl in L._cells(name): g[cy][cx] = cc((cell, cl))
        return g
    # fondo periódico
    bgcols = []
    for c in range(L.period):
        bgcols += [cc(L.bg[r][c]) or 0 for r in range(world.ROWS)]
    # columnas de primer plano: tramos [fila, n, códigos...] FF
    dic = {}; seq = []
    for c in range(L.n):
        col = [cc(L.fg[r][c]) for r in range(world.ROWS)]
        enc = []; r = 0
        while r < world.ROWS:
            if col[r] is None: r += 1; continue
            r0 = r
            while r < world.ROWS and col[r] is not None: r += 1
            enc += [r0, r - r0] + col[r0:r]
        enc.append(0xFF)
        enc = tuple(enc)
        if enc not in dic: dic[enc] = len(dic)
        seq.append(dic[enc])
    seq += [seq[-1]] * 8
    assert len(dic) <= 255, 'fase %d: %d columnas distintas' % (idx + 1, len(dic))
    p = 'f%d_' % (idx + 1)
    emit('; ---- fase %d: %s  (%d caracteres, %d columnas distintas)' % (idx + 1, L.name, len(keys), len(dic)))
    print('fase %d %-16s chars=%3d cols=%3d umbrales=%s' % (idx + 1, L.name, len(keys), len(dic), thr))
    return dict(charset=charset, thr=thr, bgcols=bgcols, dic=dic, seq=seq, p=p, L=L, blockcodes=blockcodes, code=code, cc=cc)

def main():
    phases = [getattr(world, 'fase%d' % i) for i in range(1, 6) if hasattr(world, 'fase%d' % i)]
    built = []
    for i, f in enumerate(phases):
        try:
            L = f()
        except AttributeError:
            continue
        built.append(build_phase(i, L))
    NP = len(built)
    emit('NPHASES = %d' % NP)
    # charsets (alineados a 1 KB)
    emit('        .align 1024')
    for b in built:
        bytes_line(b['p'] + 'chars', b['charset'])
    for b in built:
        L = b['L']; p = b['p']
        bytes_line(p + 'bg', b['bgcols'])
        cols = sorted(b['dic'].items(), key=lambda kv: kv[1])
        emit(p + 'coldata:')
        offs = []; o = 0
        for enc, i in cols:
            offs.append(o); o += len(enc)
            emit('        .byte ' + ','.join('$%02X' % v for v in enc))
        emit(p + 'collo:'); emit('        .byte ' + ','.join('<(%scoldata+%d)' % (p, x) for x in offs))
        emit(p + 'colhi:'); emit('        .byte ' + ','.join('>(%scoldata+%d)' % (p, x) for x in offs))
        bytes_line(p + 'seq', b['seq'])
        ev = sorted(L.events)
        emit(p + 'events:')
        for col, kind, row, param in ev:
            emit('        .byte $%02X,$%02X,%d,%d,%d' % (col & 255, col >> 8, EVK[kind], row, param))
        emit('        .byte $FF,$FF,0,0,0')
        # jefe
        B = L.boss
        emit(p + 'boss:')
        emit('        .byte %d,$%02X,$%02X,%d,%d,%d,%d   ; tipo, col, fila, ancho, alto, npartes' % (
            B['kind'], B['col'] & 255, B['col'] >> 8, B['row'], B['w'], B['h'], len(B['parts'])))
        for (pc, pr, pw, ph, hp) in B['parts']:
            emit('        .byte %d,%d,%d,%d,%d' % (pc, pr, pw, ph, hp))
        for _ in range(4 - len(B['parts'])): emit('        .byte 0,0,0,0,0')
        bytes_line(p + 'rubble', [v for r in b['blockcodes']('rubble') for v in r])
        bytes_line(p + 'turretx', [v for r in b['blockcodes']('turretx') for v in r])
        emit(p + 'warn = $%02X' % (b['blockcodes']('warn')[0][0] | 0x80))
        # caracteres animados: (código, 8 bytes x nframes)
        emit(p + 'anim:')
        for (name, frames, speed) in L.anim:
            cx_, cy_, cell0, cls0 = next(iter(L._cells(frames[0])))
            k = b['cc']((cell0, cls0))
            data = []
            for fr in frames:
                data += list(world_cell_bytes(L, fr))
            emit('        .byte %d,%d,%d   ; %s' % (k & 0x7F, len(frames), speed, name))
            bytes_line(None, data)
        # celdas animadas del jefe (ojos que brillan, bobinas, luces...)
        for (cell0, cls0, frames, speed) in getattr(L, 'banim', []):
            k = b['cc']((cell0, cls0))
            data = []
            for fr in frames: data += list(cell_bytes(tuple(r.replace('4', '3') for r in fr)))
            emit('        .byte %d,%d,%d   ; jefe' % (k & 0x7F, len(frames), speed))
            bytes_line(None, data)
        emit('        .byte $FF')
    # tablas por fase
    def tab(name, f):
        emit(name + ':'); emit('        .byte ' + ','.join(f(b) for b in built))
    def tabw(name, f):
        emit(name + 'lo:'); emit('        .byte ' + ','.join('<(%s)' % f(b) for b in built))
        emit(name + 'hi:'); emit('        .byte ' + ','.join('>(%s)' % f(b) for b in built))
    tab('ph_charhi', lambda b: '>%schars' % b['p'])
    tabw('ph_bg', lambda b: b['p'] + 'bg')
    tabw('ph_collo', lambda b: b['p'] + 'collo')
    tabw('ph_colhi', lambda b: b['p'] + 'colhi')
    tabw('ph_seq', lambda b: b['p'] + 'seq')
    tabw('ph_events', lambda b: b['p'] + 'events')
    tabw('ph_boss', lambda b: b['p'] + 'boss')
    tabw('ph_rubble', lambda b: b['p'] + 'rubble')
    tabw('ph_turretx', lambda b: b['p'] + 'turretx')
    tabw('ph_anim', lambda b: b['p'] + 'anim')
    tab('ph_warnch', lambda b: b['p'] + 'warn')
    tab('ph_period', lambda b: '%d' % b['L'].period)
    tab('ph_lenlo', lambda b: '<%d' % b['L'].n)
    tab('ph_lenhi', lambda b: '>%d' % b['L'].n)
    tab('ph_arenalo', lambda b: '<%d' % b['L'].arena)
    tab('ph_arenahi', lambda b: '>%d' % b['L'].arena)
    for i, k in enumerate(['haz', 'plat', 'solid']):
        tab('ph_' + k, lambda b, i=i: '%d' % b['thr'][i])
    for k in ['bk', 'pf0', 'pf1', 'pf2', 'pf3']:
        tab('ph_' + k, lambda b, k=k: '$%02X' % b['L'].colors[k])
    tab('ph_en1', lambda b: '%d' % getattr(b['L'], 'encol', (0x08, 0x36))[0])
    tab('ph_en2', lambda b: '%d' % getattr(b['L'], 'encol', (0x08, 0x36))[1])
    # nombres
    for b in built:
        emit(b['p'] + 'name: .byte "%s",0' % b['L'].name)
    tabw('ph_name', lambda b: b['p'] + 'name')
    sprite_data()
    music_data()
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'data.s'), 'w').write('\n'.join(OUT) + '\n')

def world_cell_bytes(L, name):
    px, cls = L.blocks[name]
    return cell_bytes(tuple(px[y][0:4] for y in range(8)))

def rev8(b): return int('{:08b}'.format(b)[::-1], 2)

def sprite_rows(txt, chars):
    r = [l for l in txt.strip('\n').split('\n')]
    out = []
    for l in r:
        l = l.ljust(8, '.')[:8]
        v = 0
        for ch in l: v = (v << 1) | (1 if ch in chars else 0)
        out.append(v)
    return out

ZAKF = ['stand', 'run1', 'run2', 'run3', 'jump', 'crouch', 'up', 'dead', 'diag']
ENF = ['soldier1', 'soldier2', 'drone1', 'drone2', 'dog1', 'dog2', 'jumper1', 'jumper2',
       'bug1', 'bug2', 'boom1', 'boom2', 'fish', 'can', 'shock', 'rock', 'fire', 'arm', 'blank']

def sprite_data():
    emit('; ---- sprites')
    emit('ZAKH = 20')
    for d in (0, 1):     # 0 = derecha, 1 = izquierda
        for layer, ch in (('a', 'F'), ('b', 'R')):
            data = []
            for f in ZAKF:
                rows = sprite_rows(sprites.ZAK[f], ch)
                assert len(rows) == 20, f
                data += [rev8(v) if d else v for v in rows]
            bytes_line('zak_%s%d' % (layer, d), data)
    emit('ENH = 16')
    for d in (0, 1):     # 0 = izquierda (dibujo), 1 = derecha
        data = []
        for f in ENF:
            rows = sprite_rows(sprites.EN[f], 'X')
            rows = (rows + [0] * 16)[:16]
            data += [rev8(v) if d else v for v in rows]
        bytes_line('en_gfx%d' % d, data)
    for i, f in enumerate(ENF): emit('EF_%s = %d' % (f.upper(), i))
    # QUIMERA-9: 2 cuadros x 24 líneas, mitades P2 (izq) y P3 (der); _l mira a la izquierda
    for half, ch in ((0, 'A'), (1, 'B')):
        for d in (0, 1):
            data = []
            for f in ('stand', 'leap'):
                rows = [l.ljust(16, '.') for l in sprites.QUIMERA[f].strip('\n').split('\n')]
                for l in rows:
                    if d == 0:   # izquierda: tal cual
                        seg = l[half * 8:half * 8 + 8]
                        v = int(''.join('1' if c != '.' else '0' for c in seg), 2)
                    else:        # derecha: espejo completo, mitad cambiada
                        m = l[::-1]; seg = m[half * 8:half * 8 + 8]
                        v = int(''.join('1' if c != '.' else '0' for c in seg), 2)
                    data.append(v)
            bytes_line('quim_%d%s' % (half, 'lr'[d]), data)
    # logotipo
    import logo
    c = logo.logo(); cells = {bytes(8): 0}; scr = []
    for cy in range(3):
        for cx in range(40):
            cell = tuple(''.join(c.p[cy * 8 + y][cx * 4:cx * 4 + 4]) for y in range(8))
            b = cell_bytes(cell)
            if b not in cells: cells[b] = len(cells)
            scr.append(cells[b])
    cs = bytearray(1024)
    for b, i in cells.items(): cs[i * 8:i * 8 + 8] = b
    emit('        .align 1024')
    bytes_line('logo_chars', cs)
    bytes_line('logo_map', scr)
    bytes_line('logo_grad', logo.GRAD)

def music_data():
    import music
    emit('; ---- música')
    bytes_line('mel_tab', music.MELTAB)
    bytes_line('bas_lo', [v & 255 for v in music.BASTAB])
    bytes_line('bas_hi', [v >> 8 for v in music.BASTAB])
    for name, (tempo, mel, bass, drums) in SONGS.items():
        for ch, seq in (('m', mel), ('b', bass), ('d', drums)):
            data = []
            for note, dur in seq: data += [note, dur * tempo]
            data += [0xFF, 0]
            bytes_line('song_%s_%s' % (name, ch), data)

if __name__ == '__main__':
    main()
