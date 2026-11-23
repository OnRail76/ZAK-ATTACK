#!/usr/bin/env python3
"""Estadísticas de una partida grabada con run8 (volcados z<f>.bin = $80-$FF y b<f>.bin = BSS).
uso: stats.py carpeta etiquetas.lbl paso"""
import sys, os, collections
d, lblf, step = sys.argv[1], sys.argv[2], int(sys.argv[3])
lbl = {}
for l in open(lblf):
    p = l.split()
    if len(p) >= 3: lbl[p[2].lstrip('.')] = int(p[1], 16)
B0 = lbl['__BSS_RUN__'] if '__BSS_RUN__' in lbl else None
files = sorted(int(f[1:-4]) for f in os.listdir(d) if f.startswith('z'))
S = collections.defaultdict(lambda: collections.defaultdict(list))
prev = None
for f in files:
    z = open(f'{d}/z{f}.bin', 'rb').read(); b = open(f'{d}/b{f}.bin', 'rb').read()
    Z = lambda n: z[lbl[n] - 0x80]
    Bv = lambda n, k=1: list(b[lbl[n] - B0:lbl[n] - B0 + k])
    if Z('mode') != 1: prev = None; continue
    key = (Z('sector') + 1, 'jefe' if Z('bstate') >= 2 else 'fase')
    lc = Bv('loopcnt')[0]
    if prev and prev[0] == key: S[key]['it'].append(((lc - prev[1]) & 255) / step)
    prev = (key, lc)
    if Z('ready') == 1: s = Z('fsel') ^ 1          # cuadro construido, a la espera de la VBI
    elif Z('newfrm') == 1: s = Z('fsel')           # recién mostrado, lógica sin empezar
    else: continue
    bu_y = Bv('bu_y', 8); bu_x = Bv('bu_x', 8); vx = Bv('bu_vxl', 8); vh = Bv('bu_vxh', 8)
    vis = [i for i in range(8) if bu_y[i] and 32 <= bu_y[i] < 222]
    sh = [y for y in Bv('sh_y', 6) if y >= 32]
    n = Bv('md_n', 2)[s]; mm = Bv('md_m', 32)[s * 16:s * 16 + n]
    ds = sum(1 for m in mm if bin(m).count('1') == 1); db = sum(1 for m in mm if bin(m).count('1') == 2)
    ot = Bv('ob_type', 8); oy = Bv('ob_y', 8)
    objs = [i for i in range(8) if ot[i] != 255 and oy[i] < 224 and oy[i] + 8 > 32]
    dw = Bv('dw_n', 2)[s]
    dup = sum(1 for a in range(len(vis)) for c in range(a + 1, len(vis))
              if abs(bu_x[vis[a]] - bu_x[vis[c]]) <= 1 and abs(bu_y[vis[a]] - bu_y[vis[c]]) <= 1
              and vx[vis[a]] == vx[vis[c]] and vh[vis[a]] == vh[vis[c]] and Bv('bu_vyh', 8)[vis[a]] == Bv('bu_vyh', 8)[vis[c]])
    S[key]['hb'].append(len(vis) - db); S[key]['nb'].append(len(vis))
    S[key]['hs'].append(len(sh) - ds); S[key]['ns'].append(len(sh))
    S[key]['ho'].append(len(objs) - dw); S[key]['no'].append(len(objs))
    S[key]['dup'].append(dup)
def pc(v): return 100.0 * sum(1 for x in v if x > 0) / max(1, len(v))
print('%-9s %6s %8s %14s %14s %14s %6s' % ('tramo', 'veloc', 'balas', 'balas ocultas', 'disp. ocultos', 'sprites ocult', 'dupl'))
for k in sorted(S):
    v = S[k]
    it = sum(v['it']) / max(1, len(v['it']))
    print('%-9s %5.0f%% %4.1f/%2d %6.1f%% (máx %d) %6.1f%% (máx %d) %6.1f%% (máx %d) %5.1f%%' % (
        '%d %s' % k, 100 * it, sum(v['nb']) / max(1, len(v['nb'])), max(v['nb'] or [0]),
        pc(v['hb']), max(v['hb'] or [0]), pc(v['hs']), max(v['hs'] or [0]), pc(v['ho']), max(v['ho'] or [0]), pc(v['dup'])))
