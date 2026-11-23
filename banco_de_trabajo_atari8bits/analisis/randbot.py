#!/usr/bin/env python3
"""bot aleatorio: random.seed(semilla); vuelca página cero y BSS cada 50 cuadros"""
import sys, random
seed, total = int(sys.argv[1]), int(sys.argv[2]); pre = sys.argv[3]
dif = int(sys.argv[4]) if len(sys.argv) > 4 else 1
random.seed(seed)
L = ["in 0 %d 0 0 0" % total]
if dif != 1: L.append("in 260 263 %d 0 0" % (4 if dif == 0 else 8))
L += ["in 320 325 0 1 0", "in 540 545 0 1 0"]
f = 600
while f < total:
    d = random.randint(3, 40)
    L.append("in %d %d %d %d 0" % (f, f + d, random.choice([0, 1, 2, 4, 8, 8, 8, 9, 5, 10, 6]), random.choice([0, 1, 1])))
    f += d + 1
for g in range(500, total, 50):
    L.append("mem %d 0080 128 %sz%d.bin" % (g, pre, g)); L.append("mem %d 0700 256 %sb%d.bin" % (g, pre, g))
L.append("end %d" % total)
print("\n".join(L))
