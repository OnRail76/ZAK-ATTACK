#!/bin/sh
# recorrido completo (versión de prueba invulnerable) en las tres dificultades + estadísticas
cd "$(dirname "$0")/.."
sh tools/cheat.sh >/dev/null || exit 1
BSS=$(grep "__BSS_RUN__" build/cheat.lbl | awk '{print $2}')
SZ=$(grep "__BSS_SIZE__" build/cheat.lbl | awk '{print $2}')
for d in 0 1 2; do
  rm -rf test/run$d; mkdir -p test/run$d
  python3 tools/fullrun.py $d ${FRAMES:-52000} 2 $BSS 1400 > test/run$d/g.txt
  (cd test/run$d && ../../tools/run8 ../../build/cheat.xex g.txt >/dev/null 2>&1) &
done
wait
for d in 0 1 2; do echo "== dificultad $d"; python3 tools/stats.py test/run$d build/cheat.lbl 2; done
