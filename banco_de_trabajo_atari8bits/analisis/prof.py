#!/usr/bin/env python3
"""Tiempos medios por rutina (en ciclos aprox.) a partir de volcados con -D PROF."""
import sys, os, collections
d, lblf = sys.argv[1], sys.argv[2]
lbl = {}
for l in open(lblf):
    p = l.split()
    if len(p) >= 3: lbl[p[2].lstrip('.')] = int(p[1], 16)
B0 = lbl['__BSS_RUN__']
names = {10: 'build: nave+objetos', 11: 'build: lista+orden proyectiles', 12: 'build: reparto proyectiles', 1: 'pm_draw', 2: 'entrada+nave+disparos', 3: 'scroll', 4: 'oleadas+objetos', 5: 'suelo', 6: 'balas', 7: 'colisiones', 8: 'jefe', 9: 'marcador', 13: '(fin lógica)', 14: 'build: CHBASE+resto', 15: 'set_lms'}
order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15]
acc = collections.defaultdict(lambda: collections.defaultdict(list))
files = sorted(int(f[1:-4]) for f in os.listdir(d) if f.startswith('z'))
seen = set()
for f in files:
    z = open(f'{d}/z{f}.bin', 'rb').read(); b = open(f'{d}/b{f}.bin', 'rb').read()
    Z = lambda n: z[lbl[n] - 0x80]
    if Z('mode') != 1: continue
    pv = list(b[lbl['prof_lv'] - B0:lbl['prof_lv'] - B0 + 16]); pf = list(b[lbl['prof_lf'] - B0:lbl['prof_lf'] - B0 + 16])
    sig = tuple(pv + pf)
    if sig in seen: continue
    seen.add(sig)
    key = (Z('sector') + 1, 'jefe' if Z('bstate') >= 2 else 'fase')
    # la VBI incrementa 'frame' hacia la línea 124: lo que va después pertenece al cuadro anterior
    ab = [((pf[i] - (1 if pv[i] >= 124 else 0)) & 255) * 131 + pv[i] for i in order]
    t = [((a - ab[0]) % (256 * 131)) for a in ab]
    if any(x < 0 for x in t) or t[-1] > 1200: continue
    for a, bb, i in zip(t, t[1:], order[1:]):
        acc[key][i].append((bb - a) * 228)
    acc[key]['total'].append(t[-1] * 228)
for k in sorted(acc):
    v = acc[k]
    tot = sum(v['total']) / len(v['total'])
    print('== sector %d %s: %d muestras, vuelta media %.0f ciclos (%.2f cuadros)' % (k[0], k[1], len(v['total']), tot, tot / 29868))
    for i in order[1:]:
        m = sum(v[i]) / len(v[i]); print('   %-24s %6.0f' % (names[i], m))
