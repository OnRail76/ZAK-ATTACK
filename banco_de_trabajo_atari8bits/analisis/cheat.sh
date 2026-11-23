#!/bin/sh
# versión de prueba invulnerable (solo para testear el recorrido completo)
cd "$(dirname "$0")/.."
C=/home/claude/tools/cc65/bin
$C/ca65 -g -D CHEAT=1 -D PROF=1 -I src -o build/cheat.o src/game.s && \
$C/ld65 -C src/vortice5.cfg -Ln build/cheat.lbl -o build/dummy build/cheat.o && \
python3 tools/mkxex.py build/cheat.xex
