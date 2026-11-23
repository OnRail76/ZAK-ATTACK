#!/usr/bin/env python3
"""guion de bot para run8: título -> fase; corre a la derecha disparando y salta a menudo.
uso: bot.py total cada_shot prefijo [pausa_derecha]"""
import sys
total, every, pre = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
L = ["in 0 %d 0 0 0" % total, "in 200 205 0 1 0", "in 420 425 0 1 0"]
f = 500
while f < total:
    # 30 cuadros a la derecha con fuego, salto a mitad
    L.append("in %d %d 9 1 0" % (f, f + 3))
    L.append("in %d %d 8 1 0" % (f + 4, f + 26))
    L.append("in %d %d 8 0 0" % (f + 27, f + 29))
    L.append("in %d %d 8 1 0" % (f + 30, f + 50))
    L.append("in %d %d %d 1 0" % (f + 51, f + 56, 4 if (f // 60) % 2 == 1 else 0))
    L.append("in %d %d 0 0 0" % (f + 57, f + 59))
    f += 60
for g in range(500, total, every):
    L.append("shot %d %s%05d.raw" % (g, pre, g))
L.append("end %d" % total)
print("\n".join(L))
