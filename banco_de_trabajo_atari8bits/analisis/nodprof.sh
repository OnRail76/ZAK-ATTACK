#!/bin/sh
# perfil de CPU sin DMA (Normal, partida completa con la versión invulnerable)
cd "$(dirname "$0")/.."
C=/home/claude/tools/cc65/bin
$C/ca65 -g -D CHEAT=1 -D PROF=1 -D NODMA=1 -I src -o build/nodma.o src/game.s && $C/ld65 -C src/vortice5.cfg -Ln build/nodma.lbl -o build/dummy build/nodma.o && python3 tools/mkxex.py build/nodma.xex >/dev/null || exit 1
BSS=$(grep "__BSS_RUN__" build/nodma.lbl | awk '{print $2}')
rm -rf test/nod && mkdir -p test/nod && python3 tools/fullrun.py ${DIF:-1} 52000 1 $BSS 1400 > test/nod/g.txt && (cd test/nod && ../../tools/run8 ../../build/nodma.xex g.txt >/dev/null 2>&1)
python3 tools/prof.py test/nod build/nodma.lbl
