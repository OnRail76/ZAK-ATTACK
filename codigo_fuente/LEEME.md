# ZAK ATTACK · Atari 400/800/XL/XE

Run'n'Gun Felino en 8 bits para Atari de 8 bits (48 KB). GATO. COMANDO. CAOS.

> Zak vivía entre camas, colchas y cajas de cartón… pero una vez, hace muchos años, ¡salvó al mundo!
> Industrias Rata preparaba su Asedio Global. Ese día, Zak, el gato feliz… COGIÓ SU FUSIL.

- Diseño gráfico, fases, nombres, historia y demás: Tony, 2026
- Diseño V3: Run'n'Gun Felino en 8 bits · GATO, COMANDO, CAOS
- Música: Yo, Claudio
- Programación y versión Atari 8 bits: Claude A.I.
- Gato protagonizado por ZAK, el Gato

## Ficheros
| Fichero | Uso |
|---|---|
| `juego/zakattack.xex` | Ejecutable para emulador o cargador de disco/SD |
| `juego/zakattack.atr` | Disco autoarrancable sin DOS (240 sectores) |
| `juego/zakattack.car` | Cartucho AtariMax 128 KB (tipo 41) |

| `banda_sonora/` | Los 8 temas en MP3, grabados del POKEY |
| `documentacion/ZAK_ATTACK_Atlas_visual.pdf` | Atlas visual completo del proyecto (18 páginas) |
| `documentacion/ZAK_ATTACK_Instrucciones.pdf` | Folleto de instrucciones ilustrado (A5, 12 páginas) |
| `codigo_fuente/` | Fuentes del juego, generadores de gráficos y documentos |
| `banco_de_trabajo_atari8bits/` | Banco de trabajo con arnés, plantillas y la guía de lecciones |

Probado en atari800 (NTSC, XL 64 KB). Pensado para NTSC; en PAL va algo más lento.

## Controles (joystick de un botón)
- Izquierda / derecha: correr. Abajo: agacharse. Arriba: saltar (cada salto, una nueva pulsación).
- FIRE corriendo: disparo recto sin dejar de correr ni de saltar.
- FIRE desde quieto: Zak **se planta** y, mientras mantienes FIRE, la palanca apunta:
  adelante, arriba+lado (diagonal), arriba (vertical) o abajo (agachado). Suelta FIRE para volver a moverte.
- En el aire, 8 direcciones: arriba, diagonal arriba, adelante, diagonal abajo y abajo.
- Tecla P o espacio: pausa.

## Título
- Izquierda / derecha: dificultad. FIRE: empezar.
- Truco: **abajo, abajo, FIRE** (hasta 2 segundos entre pulsaciones) → MODO INVENCIBLE (el marcador pone VIDA INV).

## Dificultad
| | FÁCIL | NORMAL | HARDCORE |
|---|---|---|---|
| Vidas / corazones | 5 / 4 | 3 / 3 | 3 / 2 |
| Balas enemigas a la vez | 1 | 2 | 2, más rápidas |
| Vida de los jefes | −25 % | normal | +25 % |
| Aviso antes de cada ataque de jefe | 1 s | 0,7 s | 0,4 s |

## La partida
El pescado recupera la vida; la lata dorada da una vida extra.
Cinco fases con su jefe: Callejón Neón (MEKDOZER 1), Metro (METROPLEX III),
Factoría del Miedo (CONTROL CENTRAL II), Planta Química (QUIMERA-9) e Industrias Rata (RATTUS PRIME).
Hasta 4 enemigos a la vez: 2 en el aire y 2 en tierra (los sprites P2/P3 se recolocan a media pantalla).
Los enemigos de tierra no se tiran a los fosos.
Los jefes solo disparan (ráfagas de balas naranjas que salen de su borde); la excepción es el escombro de MEKDOZER 1.
Cada ataque se avisa: parpadea la pieza que va a disparar; el escombro tiembla arriba y unas flechas blancas
marcan dónde caerá; QUIMERA-9 cambia de color antes de saltar. Los ojos de los jefes se encienden y se apagan,
las bobinas de CONTROL CENTRAL II giran y su rejilla de luces parpadea; RATTUS PRIME masca y mueve los bigotes.
Los jefes con piezas solo exponen su núcleo cuando caen las piezas (el núcleo parpadea).
Al acabar: GAME OVER o MISIÓN CUMPLIDA con la puntuación y vuelta al título. Nunca entra el modo atracción.

## Compilar
`./build.sh` (necesita cc65 en `/home/claude/tools/cc65/bin` o en `CC65`).
`CA65FLAGS="-D CHEAT=1" ./build.sh` crea la versión invulnerable para el bot de pruebas.
`CA65FLAGS="-D JUKE=n" ./build.sh` hace que el título toque el tema n (0-7): así se graba la banda sonora con `WAV=fichero ./tools/run8`.
`python3 docs/build_docs.py && python3 docs/render.py` rehace el atlas y el folleto (HTML → PDF con Chromium).
