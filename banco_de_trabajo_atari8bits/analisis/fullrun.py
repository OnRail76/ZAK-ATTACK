#!/usr/bin/env python3
"""Genera un guion de partida completa para run8: elige dificultad, juega (bot) y vuelca memoria.
uso: fullrun.py dificultad(0-2) cuadros paso bss_ini bss_tam > guion"""
import sys
dif, total, step, bss, size = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4], 16), int(sys.argv[5])
L = ["in 0 %d 0 0 0" % total]
f = 100
moves = {0: [4], 1: [], 2: [8]}[dif]          # desde Normal: izquierda=Fácil, derecha=Hardcore
for m in moves: L.append("in %d %d %d 0 0" % (f, f + 5, m)); f += 20
L.append("in %d %d 0 1 0" % (f + 20, f + 25)); f += 120
while f < total:
    L.append("in %d %d %d 1 0" % (f, f + 69, 4 if (f // 70) % 2 == 0 else 8)); f += 70
for g in range(600, total, step):
    L.append("mem %d 0080 128 z%d.bin" % (g, g)); L.append("mem %d %04X %d b%d.bin" % (g, bss, size, g))
L.append("end %d" % total)
print("\n".join(L))
