#!/bin/sh
# Vórtice 5 · compilación: genera datos, ensambla, enlaza y empaqueta
set -e
cd "$(dirname "$0")"
CC65=${CC65:-/home/claude/tools/cc65/bin}
python3 tools/gen.py
mkdir -p build
$CC65/ca65 -g -I src -o build/game.o -l build/game.lst src/game.s
$CC65/ld65 -C src/vortice5.cfg -m build/game.map -Ln build/game.lbl -o build/dummy build/game.o
python3 tools/mkxex.py build/vortice5.xex
$CC65/ca65 -I src -o build/cart.o src/cart.s
$CC65/ld65 -C src/cart.cfg -o build/cart0.bin build/cart.o
python3 tools/mkpack.py
