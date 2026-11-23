# Banco de trabajo · juegos para Atari 8 bits

Lo que se usó para hacer **Vórtice 5** y sirve para el próximo título: herramientas,
el flujo de trabajo de principio a fin y las lecciones aprendidas por el camino.

## 1. Montar las herramientas (Linux, una vez)

| Herramienta | Para qué | Cómo |
|---|---|---|
| cc65 2.19 (ca65 + ld65) | Ensamblar y enlazar | `git clone https://github.com/cc65/cc65 && make -C cc65` → binarios en `cc65/bin` |
| atari800 (libatari800) | Emulador sin pantalla para pruebas automáticas | `git clone https://github.com/atari800/atari800 && cd atari800 && ./autogen.sh && ./configure --target=libatari800 --disable-netsio && make` |
| `run8` | El arnés de pruebas (este banco) | `gcc -O2 -I atari800/src/libatari800 -o run8 arnes/run8.c atari800/src/libatari800.a -lm` |
| Python 3 + Pillow + numpy | Gráficos, generadores, análisis | `pip install pillow numpy scipy` |
| Playwright + Chromium | Documentación HTML → PDF | `pip install playwright && playwright install chromium` |
| ffmpeg | Grabar la banda sonora a MP3 | paquete del sistema |

Para jugar de verdad: Altirra (Windows) o atari800 con pantalla.

## 2. El flujo de trabajo

```
gfx/*.py  ──►  tools/gen.py  ──►  src/data.s  ──►  ca65/ld65  ──►  main.bin
(dibujos en texto)  (charsets, mapas,   (generado)                     │
                     oleadas, jefes,                      mkxex.py ───┼──► .xex
                     música, textos)                      mkpack.py ──┴──► .atr + .car
```

1. **Dibujar en texto.** Sprites, tiles, escenarios y jefes son cuadrículas de caracteres
   en Python (`graficos/canvas.py` da rectángulos, elipses, trazos y espejo; `graficos/pal.py`
   convierte códigos de color $HL a RGB NTSC). La misma fuente sirve al juego y a los documentos.
2. **Generar los datos.** Un script convierte los dibujos en charsets de 1 KB, metatiles,
   mapas, tablas de enemigos, jefes partidos en dos juegos de caracteres y música en tablas.
   Comprueba los límites (128 caracteres por juego, sprites por franja…) y avisa si algo no cabe.
3. **Ensamblar.** `build.sh` regenera, ensambla, enlaza y empaqueta los tres formatos.
4. **Probar sin manos** con `run8` (sección 3).
5. **Medir** velocidad, sprites ocultos y duplicados (sección 4).
6. **Documentar** con los generadores de `documentacion/` (sección 5).

## 3. El arnés `run8`

Ejecuta un .xex/.atr/.car en atari800 sin pantalla siguiendo un guion de texto:

```
in  F0 F1 joy trig start   # entre los cuadros F0 y F1: joy (1 arriba, 2 abajo, 4 izq., 8 der.; se suman), fuego 0/1, START 0/1
shot F nombre.raw          # captura de pantalla en el cuadro F (384×240, códigos de color)
mem  F 0080 128 z.bin      # volcado de memoria (dirección en hex, longitud en decimal)
end  F                     # último cuadro
```

- `WAV=salida.raw run8 juego.xex guion` graba el sonido (PCM 16 bits, 44.100 Hz, mono).
- `shot.py` convierte capturas a PNG; `memq.py` lee variables por nombre con el fichero de etiquetas.
- Con una versión invulnerable (`-D CHEAT=1`) un bot recorre el juego entero en un minuto de reloj.

## 4. Medir

| Script | Qué da |
|---|---|
| `fullrun.py` | Guion de partida completa: elige dificultad, juega en zigzag con fuego y vuelca memoria cada N cuadros |
| `allstats.sh` + `stats.py` | Por tramo (fase/jefe y sector): velocidad (vueltas de lógica por cuadro), balas, balas/disparos/sprites que se quedan sin dibujar, duplicados |
| `nodprof.sh` + `prof.py` | Coste en ciclos de cada rutina, con sondas `PROF n` (VCOUNT + cuadro) y DMA apagado |

Una vuelta de lógica que pasa de un cuadro tarda dos: el juego va al 50 % en ese momento.
Lo que importa es que casi todas las vueltas quepan en un cuadro, no la media.

## 5. Documentar

- `render_assets.py`: sprites, tiles, cráteres y jefes desde los mismos `gfx/*.py`, más recortes de capturas reales.
- `build_atlas.py` (A4 apaisado) y `build_manual.py` (A5) escriben HTML; `make_pdf.py` lo pasa a PDF.
- `common.py` reúne los textos compartidos (créditos, historia, lema, datos de sectores).

## 6. Lecciones aprendidas (Vórtice 5)

**Pantalla y DLI**
- Tablas DLI de más de 256 bytes con índice Y dan la vuelta: una tabla por campo (32 bytes), rutinas A/B con direccionamiento absoluto.
- Con VSCROL = 7 la primera línea mide un scanline y su DLI llega dentro de la anterior: deja una línea en blanco tras el marcador y carga la línea 0 en la VBI.
- Pon el bit de DLI solo en la línea anterior a una línea que cambia algo, con una máscara de cambios por línea. Un barrido desenrollado de la máscara vale más que ordenar listas.
- Doble búfer: dos display lists y dos juegos de tablas; la lógica prepara el cuadro siguiente y la VBI solo cambia punteros.
- La PMG de resolución de una línea deja libre $B000–$B2FF: buen sitio para tablas de trabajo.

**Sprites**
- Multiplexar P2/P3 por franjas y los 4 misiles como un solo recurso compartido entre disparos y balas.
- **Turnos**: lo que no cupo en un cuadro va primero en el siguiente. Así nada queda invisible dos cuadros seguidos; como mucho parpadea.
- Un sprite que no cambió (posición, gráfico, player) no se borra ni se repinta. Que cada objeto conserve su player.
- Recorre los objetos en el orden en que suelen estar ya (el reparto de huecos lo marca): la ordenación por inserción sale casi gratis.

**Rendimiento**
- VBI inmediata propia en juego (copiar sombras a mano) en vez de pasar por el SO.
- No toques los LMS si el scroll no se movió; cachea lo que solo cambia con el scroll.
- Colisiones contra listas compactas de lo que está vivo y en pantalla.
- Si un tramo sigue lento, a veces la solución es de diseño: espaciar las oleadas.

**Sonido**
- Lo que corre en la VBI necesita sus propios temporales de página cero.
- Nunca cortes en seco: bucles que cierran en el acorde que lleva al principio y fundido en cada cambio de pista.
- AUDCTL $78 (dos voces de 16 bits) para pantallas; $28 en juego (bajo de 16 bits, melodía de 8, efectos en su canal).

**Juego justo**
- Ninguna bala nace dentro de una zona alrededor de la nave; tope de balas según la dificultad.
- Una bala nueva no nace encima de otra igual; un enemigo que devuelve disparos, con enfriamiento.

**Formatos**
- ATR autoarrancable sin DOS: tope de 255 sectores (~32 KB); vigílalo.
- Cartucho AtariMax 128 KB: el banco 0 copia los demás a RAM y desconecta el cartucho.
- Desconecta el BASIC de los XL/XE (PORTB) si usas $A000–$BFFF.

## 7. Lista para el próximo título

1. Copia `plantilla/` (build.sh, vortice5.cfg, cart.s) y los empaquetadores.
2. Define paleta y reglas del hardware antes de dibujar (cuántos colores, sprites por franja, tamaño de jefes).
3. Dibuja en `gfx/` con `canvas.py`; haz que el generador compruebe los límites.
4. Haz una versión con `CHEAT` y `PROF` desde el primer día; mide en cada cambio grande.
5. Prueba los tres formatos al final de cada ronda.

## 8. Lecciones aprendidas (Zak Attack, run and gun con scroll horizontal)

**Pantalla**
- ANTIC 4 + HSCROL sobre un anillo de 64 columnas por fila (128 bytes, cada columna escrita dos veces): la ventana de 48 bytes nunca da la vuelta y basta tocar el byte bajo de 22 LMS en la VBI.
- HSCROL = 3 − (camx & 3); HPOS del píxel 0 del campo = 45 con este montaje.
- Fondo repetido cada 16 columnas + primer plano en tramos [fila, n, códigos]: 5 fases en ~8 KB.
- El generador comprueba que el fondo no use caracteres sólidos (en el tren, las colinas eran "suelo" invisible).
- Una DLI bajo el marcador cambia juego de caracteres y colores; otra en la última fila devuelve el borde a negro.
- Logotipo con juego de caracteres propio (41 celdas) y degradado por DLI línea a línea en el título.

**Errores que costaron**
- Otra vez el temporal compartido entre VBI y programa principal: la VBI usa SOLO sus variables (`vbt`). El síntoma fue fondo corrupto en la segunda vuelta.
- Una rutina de sonido que pisa X/Y dentro de un bucle de colisiones produjo puntuaciones BCD imposibles ("063<00"). `play_sfx` conserva X e Y.
- `cld` al principio de la VBI: puede llegar en medio de una suma BCD.
- Jefes: comprobar con números que el punto débil queda a la altura de los disparos (pies − 12 de pie, − 5 agachado, ~−60 saltando).

**Pruebas**
- `bot.py` + `runbot.sh`: corre, salta, se para a disparar y a veces se gira; con `-D CHEAT=1` los fosos lo devuelven arriba y no pierde vidas. Recorre las 5 fases en ~23 000 cuadros.
- `zp.py`: lee variables de página cero por nombre desde un volcado de `run8`.
- Contador `lagcnt` de cuadros perdidos: < 1 %, casi todo en cambios de fase.
- `atlas.py`: atlas gráfico desde los mismos datos del juego (pantallas simuladas), antes de programar nada.

**Segunda ronda (pruebas de Tony en atari800 de verdad)**
- Calibra la posición de los sprites contra el decorado desde el primer día: captura cruda, busca el color del sprite y el de un tile conocido y compara con las coordenadas del mundo. Aquí el sprite iba 9 color clocks a la derecha (Zak "se metía" en las cajas) y el campo visible empieza en camx + 12.
- Ninguna rutina devuelve intacto un puntero de página cero que no sea suyo: `aim_bullet` usaba `ptr3` y el bucle de torretas guardaba ahí su índice. Con el índice basura escribía fuera de las tablas: colores rotos (cielo rosa) y cuelgue.
- Aritmética con signo: `lsr` sobre un valor negativo lo convierte en uno enorme (el pescado aparecía abajo del todo). Usa `cmp #$80 / ror`.
- Recogibles: si no hay hueco de sprite, el evento espera; los enemigos se pierden, el pescado no.
- Enemigos de tierra con prueba de pared (`move_xw`): el soldado se para, el perro salta.
- Bot aleatorio (`randbot.py`) para buscar cuelgues: cuidado con los falsos positivos en pantallas de texto y GAME OVER.
- Música de marcha: batería en el canal de efectos (bombo con barrido de tono, caja y charles de ruido); un golpe de batería tapa el sonido del disparo, nunca una explosión o un golpe a Zak.

**Tercera ronda (puntería, dificultad, avisos)**
- Joystick de un botón y apuntar: "plantarse con FIRE" (FIRE desde quieto fija a Zak y la palanca apunta) conserva correr-saltar-disparar y añade diagonales en el suelo.
- Otra vez registros pisados: una rutina auxiliar (`scale_hp`) cambiaba Y en medio de un bucle que leía datos con (ptr),Y → todas las piezas del jefe mal colocadas. Toda rutina auxiliar guarda lo que toca.
- Los flancos de la palanca en una variable propia: `put_line` reutilizaba `tmp+2` y el menú cambiaba de dificultad solo.
- Inicializa explícitamente lo que vive en BSS (la dificultad salía con basura del cargador).
- Aviso de jefe genérico: la pieza que va a atacar invierte sus caracteres (bit 7) cada 4 cuadros y se restaura al terminar; proyectiles "en espera" (contador en el hueco del enemigo) para escombros y barridos.

**Cuarta ronda (más enemigos, metro)**
- 4 enemigos con 2 players: franjas. Huecos 0-1 arriba (drones), 2-3 abajo (tierra); una DLI en la fila 9 recoloca HPOSP2/P3 y cambia COLPM2/3. Cada tipo tiene su color. En los jefes, una sola franja.
- Los eventos que no encuentran hueco esperan (hasta 1,5 s los enemigos; los recogibles siempre).
- Otra rutina guardaba su índice en `tmp+3`, que `putchar` usa: escombros en una fila entera al romper piezas de jefe. Cada rutina, su variable.
- Enemigos de tierra: prueba de pared Y de borde (`move_xg`); la saltadora mira si hay suelo donde caer.
- Torretas de caracteres fuera: se hacían eternas; mejor más enemigos de los que ya hay.

**Quinta ronda (comportamiento de enemigos)**
- No orientes a los enemigos hacia el jugador en cada cuadro: al alcanzarlo tiemblan encima y no se van. Dirección al aparecer; media vuelta solo en paredes y bordes.
- Comprobar el suelo de destino ANTES de despegar (o compensar el píxel): si no, nunca hay suelo y el enemigo salta en el sitio.
- Con franjas de sprites, limita el salto de los de abajo para que no crucen la línea (impulso según la altura).
- Pinta los sprites al principio del cuadro (justo tras la VBI) y escribe HPOS directamente: así no hay sprites partidos por el haz.
- Lava/electricidad matan enemigos; ningún enemigo de tierra aparece sobre un foso; tope de vida en pantalla.

**Sexta ronda (balas invisibles)**
- El modo quinto player pinta los misiles con la prioridad de PF3: quedan DETRÁS de los píxeles PF0-PF2. Las balas desaparecían dentro de los jefes y detrás de edificios y azulejos. Mejor sin quinto player: cada misil con el color de su player y por delante del fondo (GPRIOR $01).
- Balas enemigas más visibles: M2/M3 a doble anchura (SIZEM $50) y 4 líneas de alto.
- Las balas del jefe salen de su borde, no de su centro.

**Séptima ronda (jefes nuevos animados)**
- Jefes de caracteres animados sin sprites: se dibujan 4 cuadros; el generador compara celda a celda, da un carácter propio a las que cambian y emite sus 4 bitmaps; el juego los reescribe cada 8 cuadros (ojos que se encienden, bobinas que giran, luces en ola).
- En una celda inversa todos los píxeles de color 3 salen en PF3: no mezcles el blanco (PF3) con el color 3 en la misma celda, ni cambies el blanco entre cuadros.
- Copia de caracteres animados: puntero de destino = destino − Y, así origen y destino comparten índice (lda (p1),y / sta (p2),y).
- Hojas de diseño (`bossheet.py`) para aprobar un jefe antes de meterlo en el juego.
- Regla de diseño con estas limitaciones: los jefes solo disparan; los proyectiles con sprite se pierden o confunden.

**Octava ronda (explosiones de jefe y repaso de niveles)**
- Para saber qué plataformas sobran, simula la física del juego cuadro a cuadro (búsqueda exhaustiva de estados x, y, vy, subpíxel) y marca las celdas que Zak llega a pisar. Salió que el salto sube 39 píxeles y las plataformas a 40 eran inalcanzables: 7 tramos fuera.
- Muchos sprites a la vez sin parpadeo: durante la muerte del jefe se activan DLI extra en las filas 9, 11 y 13 (la VBI pone o quita el bit $80 de esas líneas de la display list según una copia del indicador, para que DL y cadena de DLI siempre coincidan). Cada DLI recoloca P2 y P3 y les da color: 4 franjas × 2 = 8 explosiones.
- Cada explosión: 4 cuadros de 8 × 8 con las líneas dobladas, y una paleta que avanza con la edad (blanco, amarillo, naranja, rojo).
- Las explosiones antiguas usaban los huecos de enemigo de la franja de arriba con la y del jefe (franja de abajo): no se veían nunca. Un sprite solo existe dentro de su franja.
- Nombres de dificultad de Tony: la difícil se llama siempre HARDCORE.
- Cartucho que se desactiva (AtariMax, copia a RAM): con el OS XL real, la VBI compara TRIG3 con GINTLK ($03FA) y, si el cartucho «desaparece», se cuelga a propósito (pantalla negra). Tras `sta $D510` hay que copiar TRIG3 ($D013) a GINTLK. El arnés usa AltirraOS, que no lo hace, así que el fallo no salía en las pruebas: probar los .car también con las ROM reales cuando se pueda.

**Novena ronda (cierre del proyecto)**
- Banda sonora: una opción de compilación (`JUKE=n`) hace que el título toque el tema n; el arnés graba el POKEY con `WAV=`. Se recorta desde la primera muestra con sonido, dos vueltas del bucle y un fundido, y se pasa a MP3 con etiquetas.
- Capturas para la documentación: una sola pasada del bot con volcado de memoria y capturas cada 10 cuadros; el emulador no siempre repite igual entre pasadas, así que se elige de la misma pasada.
- Para pillar el GAME OVER hace falta un bot que avance sin disparar (quieto no aparece ningún enemigo).
- Atlas y folleto en HTML con páginas de tamaño fijo y Chromium a PDF; sprites exportados desde los mismos datos del juego.
