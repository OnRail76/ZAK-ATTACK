# -*- coding: utf-8 -*-
"""Folleto de instrucciones de Vórtice 5 (A5 vertical) -> manual.html (luego make_pdf.py)."""
from common import *

css = '''
@page{size:148mm 210mm;margin:0}
*{box-sizing:border-box}
:root{--paper:#f3eee3;--ink:#17181f;--soft:#5d5f6b;--red:#c63c2b;--amber:#d9921c;--line:#d6cfbf;--night:#0b0d14}
html,body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,sans-serif;font-size:9.6pt;line-height:1.5;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:148mm;height:210mm;padding:13mm 12mm 14mm;position:relative;overflow:hidden;page-break-after:always;display:flex;flex-direction:column;gap:4.5mm}
.page:last-child{page-break-after:auto}
.dark{background:var(--night);color:#e9ebf2}
h1,h2,h3{font-family:"Inter Display",Inter,sans-serif;margin:0}
h2{font-size:19pt;font-weight:800;line-height:1.05;letter-spacing:.01em}
h2 small{display:block;font:600 7pt "DejaVu Sans Mono",monospace;letter-spacing:.18em;color:var(--red);margin-bottom:2mm;text-transform:uppercase}
h3{font-size:10.5pt;font-weight:700;margin:0 0 1mm}
p{margin:0}
.mono{font-family:"DejaVu Sans Mono",monospace}
.soft{color:var(--soft)}
.shot{background:#000;border-radius:1.5mm;overflow:hidden;box-shadow:0 0 0 .4mm #000}
.shot img{display:block;width:100%;image-rendering:pixelated}
img.px{image-rendering:pixelated;display:block}
.foot{position:absolute;left:12mm;right:12mm;bottom:6mm;display:flex;justify-content:space-between;font:6.5pt "DejaVu Sans Mono",monospace;color:#8b8678;letter-spacing:.08em}
table{border-collapse:collapse;width:100%;font-size:8.6pt}
th,td{text-align:left;padding:1.3mm 1.8mm;border-bottom:1px solid var(--line);vertical-align:middle}
th{font:600 6.5pt "DejaVu Sans Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--soft)}
td.n{font-family:"DejaVu Sans Mono",monospace;text-align:right;white-space:nowrap}
.box{border:1.2px solid var(--ink);border-radius:2mm;padding:3mm 3.5mm}
.tip{background:#e7dfcd;border-radius:2mm;padding:2.6mm 3.4mm;font-size:8.8pt}
.tip b{color:var(--red)}
.key{display:inline-block;font:700 7.5pt "DejaVu Sans Mono",monospace;border:1px solid var(--ink);border-radius:1mm;padding:0 1.4mm;background:#fff}
.sp{background:#000;border-radius:1.2mm;display:flex;align-items:center;justify-content:center;gap:2mm;padding:2mm;width:22mm;height:15mm;flex:none}
.row{display:flex;gap:3mm;align-items:center}
ul{margin:0;padding-left:4.5mm} li{margin:.6mm 0}
'''

def foot(n): return f'<div class="foot"><span>VÓRTICE 5 · INSTRUCCIONES</span><span>{n}</span></div>'
pages = []; P = pages.append

# portada
P(f'''<section class="page dark" style="padding:0;background:radial-gradient(120% 70% at 50% 35%,#2b0f18 0%,#0b0d14 65%)">
<div style="padding:14mm 12mm 0;display:flex;flex-direction:column;gap:3mm">
 <span class="mono" style="font-size:7pt;letter-spacing:.18em;color:#f2b84b">MANUAL DE INSTRUCCIONES</span>
 <h1 style="font-size:46pt;font-weight:800;line-height:.9;letter-spacing:.01em">VÓRTICE <span style="color:#f07a6a">5</span></h1>
 <div style="font:600 15pt 'Inter Display',sans-serif;color:#f2b84b">{SUBTITLE}</div>
 <div style="align-self:flex-start;border:1.3px solid #e9ebf2;border-radius:1.5mm;padding:1.2mm 3mm;font:700 8.5pt 'Inter Display',sans-serif">{DESIGN}</div>
</div>
<div class="shot" style="margin:7mm 12mm 0"><img src="img/game_b5_39500.png" style="height:96mm;object-fit:cover;object-position:top"></div>
<div style="position:absolute;left:12mm;right:12mm;bottom:12mm;display:flex;flex-direction:column;gap:2mm">
 <p style="font-size:8.5pt;font-style:italic;color:#cfd3e0">{TAGLINE}</p>
 <p style="font-size:7.5pt;color:#e9ebf2;border-left:2px solid #f2b84b;padding-left:2.5mm">{CREDITS}</p>
 <p class="mono" style="font-size:6.5pt;color:#959cb2;letter-spacing:.06em">{MACHINE.upper()} · JOYSTICK</p>
</div></section>''')

# historia
P(f'''<section class="page dark">
<h2 style="color:#e9ebf2"><small style="color:#f2b84b">La historia</small>El Ordenador Estelar se ha vuelto loco</h2>
<div style="font-size:12pt;line-height:1.6;display:flex;flex-direction:column;gap:4mm;margin-top:2mm">
 {''.join(f'<p>{s}</p>' for s in STORY)}
 <p style="font:800 26pt 'Inter Display',sans-serif;color:#f07a6a">{STORY_PUNCH}</p>
</div>
<div class="shot" style="margin-top:auto"><img src="img/game_s5_35500.png" style="height:52mm;object-fit:cover"></div>
<p style="font-size:8pt;color:#cfd3e0;border-left:2px solid #f2b84b;padding-left:2.5mm">{CREDITS}<br><i>{TAGLINE}</i></p>
<div class="foot" style="color:#6a7187"><span>VÓRTICE 5 · INSTRUCCIONES</span><span>2</span></div></section>''')

# carga y controles
P(f'''<section class="page">
<h2><small>Antes de despegar</small>Carga y controles</h2>
<table><thead><tr><th>Fichero</th><th>Cómo cargarlo</th></tr></thead><tbody>
<tr><td class="mono">vortice5.xex</td><td>Con cualquier cargador de ejecutables o DOS (opción L), SIO2SD, FujiNet, Altirra o atari800.</td></tr>
<tr><td class="mono">vortice5.atr</td><td>Disco autoarrancable: enciende el ordenador con el disco puesto. No necesita DOS.</td></tr>
<tr><td class="mono">vortice5.car</td><td>Cartucho AtariMax de 128 KB (tipo 41 en emuladores).</td></tr>
</tbody></table>
<div class="row" style="gap:4mm;align-items:flex-start">
 <div class="box" style="flex:1"><h3>Necesitas</h3><ul><li>Atari 400, 800, XL o XE con 48 KB.</li><li>Joystick en el puerto 1.</li><li>Sistema NTSC (60 Hz). En PAL funciona, un 17 % más lento.</li><li>El juego desconecta solo el BASIC de los XL/XE.</li></ul></div>
</div>
<h3 style="margin-top:2mm">Controles</h3>
<table><tbody>
<tr><td style="width:34mm"><b>Joystick</b></td><td>Mueve el Vórtice 5 en las ocho direcciones.</td></tr>
<tr><td><b>Botón</b> <span class="key">FIRE</span></td><td>Dispara el Pulso. Si lo mantienes, dispara solo.</td></tr>
<tr><td><span class="key">START</span></td><td>Empieza la partida (igual que FIRE).</td></tr>
<tr><td>Izquierda / derecha, <span class="key">SELECT</span></td><td>En el título, eligen la dificultad.</td></tr>
</tbody></table>
<div class="tip">El Pulso daña tanto a lo que vuela como a lo que hay en el suelo: torretas, contenedores y bombas caen con el mismo disparo, como en los clásicos.</div>
{foot(3)}</section>''')

# título y dificultad
P(f'''<section class="page">
<h2><small>Pantalla de título</small>Elige tu dificultad</h2>
<div class="row" style="gap:3mm"><div class="shot" style="flex:1"><img src="img/full_t_dif0.png"></div><div class="shot" style="flex:1"><img src="img/full_t_dif2.png"></div></div>
<p class="soft" style="font-size:8pt">Mueve el joystick a izquierda o derecha (o pulsa SELECT) para cambiar entre Fácil, Normal y Hardcore. FIRE o START para empezar.</p>
<table><thead><tr><th></th><th style="text-align:right">Fácil</th><th style="text-align:right">Normal</th><th style="text-align:right">Hardcore</th></tr></thead><tbody>
<tr><td>Vidas</td><td class="n">5</td><td class="n">3</td><td class="n">2</td></tr>
<tr><td>Velocidad de las balas</td><td class="n">lenta</td><td class="n">normal</td><td class="n">rápida</td></tr>
<tr><td>Disparan</td><td class="n">menos</td><td class="n">normal</td><td class="n">más</td></tr>
<tr><td>Balas enemigas a la vez</td><td class="n">5</td><td class="n">6</td><td class="n">8</td></tr>
<tr><td>Zona segura alrededor de la nave</td><td class="n">amplia</td><td class="n">media</td><td class="n">justa</td></tr>
</tbody></table>
<div class="tip"><b>Zona segura.</b> Ninguna bala enemiga nace pegada a tu nave: siempre tendrás un instante para reaccionar. En Hardcore ese margen es el más corto.</div>
<p class="soft" style="font-size:8pt">La pantalla de título muestra el récord de la sesión.</p>
{foot(4)}</section>''')

# marcador y nave
P(f'''<section class="page">
<h2><small>En vuelo</small>El marcador y tu nave</h2>
<div class="shot"><img src="img/full_s1_2300.png" style="height:44mm;object-fit:cover;object-position:top"></div>
<table><tbody>
<tr><td class="mono" style="width:22mm">PTS</td><td>Tu puntuación.</td></tr>
<tr><td class="mono">VIDAS</td><td>Naves que te quedan. Vida extra a los 20.000 puntos y luego cada 50.000.</td></tr>
<tr><td class="mono">NV</td><td>Nivel del disparo, de 1 a 3.</td></tr>
<tr><td class="mono">SEC</td><td>Sector en el que estás, de 1 a 5.</td></tr>
</tbody></table>
<div class="row" style="gap:4mm;align-items:center;margin-top:1mm">
 <div class="sp" style="width:30mm;height:26mm">{''.join(f'<img class="px" src="img/ship_{k}.png" style="width:7.5mm">' for k in ('izquierda','centro','derecha'))}</div>
 <div><h3>El Vórtice 5</h3><p>Caza espacial ligero, el único capaz de colarse hasta el Corazón de Acero. Se inclina al moverse de lado. Al empezar y tras perder una vida parpadea unos segundos: mientras parpadea, nada le hace daño.</p></div>
</div>
<div class="row" style="gap:4mm;align-items:center">
 <div class="sp" style="width:30mm;height:20mm"><img class="px" src="img/en_capsula_p_0.png" style="width:10mm"></div>
 <div><h3>Cápsula P</h3><p>Recógela para subir el disparo. <b>Nivel 1:</b> un disparo. <b>Nivel 2:</b> dos en paralelo. <b>Nivel 3:</b> dos con más cadencia. Con el nivel 3, cada cápsula vale 1.000 puntos. Al perder una vida vuelves al nivel 1.</p></div>
</div>
{foot(5)}</section>''')

# sectores (uno por página)
for k, S in enumerate(SECTORS):
    n = S['n']
    air = ''.join(f'''<div class="row"><div class="sp">{''.join(f'<img class="px" src="img/en_{s}_{f}.png" style="width:{11 if s=="destructor" else 6.5}mm">' for f in (0,1))}</div>
      <div><b>{nm}</b><br><span class="soft">{role} · {pts:,} puntos</span></div></div>'''.replace(',', '.') for s, nm, role, pts in S['air'])
    gr = ''.join(f'''<div class="row"><div class="sp"><img class="px" src="img/tile{n}_{s}.png" style="width:10mm"></div>
      <div><b>{nm}</b><br><span class="soft">{role} · {pts:,} puntos</span></div></div>'''.replace(',', '.') for s, nm, role, pts in S['ground'])
    bname, bsub, wps, wdesc = S['boss']
    P(f'''<section class="page">
<h2><small>Sector {n} de 5</small>{S['name']}</h2>
<div class="row" style="gap:4mm;align-items:stretch">
 <div class="shot" style="width:64mm;flex:none;align-self:flex-start"><img src="img/game_{S['shot']}.png"></div>
 <div style="display:flex;flex-direction:column;gap:2.4mm;font-size:8.6pt;min-width:0">
  <h3 style="font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:var(--soft)">En el aire</h3>{air}
  <h3 style="font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:var(--soft);margin-top:1mm">En el suelo</h3>{gr}
 </div>
</div>
<div class="box" style="display:flex;gap:4mm;align-items:center">
 <div class="shot" style="width:52mm;flex:none"><img class="px" src="img/boss{n}.png"></div>
 <div style="font-size:8.6pt"><span class="mono" style="font-size:6.5pt;letter-spacing:.14em;color:var(--red)">JEFE</span><h3 style="font-size:12pt">{bname}</h3><p>{wps} puntos débiles. {wdesc}</p></div>
</div>
<div class="tip"><b>Consejo.</b> {S['tip']}</div>
{foot(6 + k)}</section>''')

# jefes y puntuación
P(f'''<section class="page">
<h2><small>Cómo vencer a los jefes</small>Puntos débiles y puntuación</h2>
<div class="row" style="gap:3mm"><div class="shot" style="flex:1"><img class="px" src="img/boss4.png"></div><div class="shot" style="flex:1"><img class="px" src="img/boss4_hit.png"></div></div>
<p>Al final de cada sector el scroll se detiene y aparece el jefe. Cada uno tiene de 3 a 5 <b>puntos débiles</b>: cuando aciertas, parpadean en blanco. El <b>núcleo</b> central solo se puede dañar cuando han caído todos los demás. Mientras tanto, el jefe no deja de disparar.</p>
<table><thead><tr><th>Acción</th><th style="text-align:right">Puntos</th></tr></thead><tbody>
<tr><td>Impacto en un punto débil</td><td class="n">10</td></tr>
<tr><td>Punto débil destruido</td><td class="n">1.000</td></tr>
<tr><td>Jefe destruido · sector superado</td><td class="n">5.000</td></tr>
<tr><td>Enemigos del aire</td><td class="n">100 – 1.000</td></tr>
<tr><td>Objetivos de suelo</td><td class="n">300 – 2.000</td></tr>
<tr><td>Cápsula P con el disparo a nivel 3</td><td class="n">1.000</td></tr>
</tbody></table>
<div class="tip"><b>Pista.</b> Los objetivos de suelo destruidos dejan su cráter: así sabes qué zona está ya limpia.</div>
{foot(11)}</section>''')

# consejos, fin y secreto
P(f'''<section class="page">
<h2><small>Para pilotos</small>Consejos, final y un secreto</h2>
<ul style="font-size:9.2pt">
<li>Mantén FIRE pulsado: el disparo automático no se cansa.</li>
<li>Sube al nivel 2 cuanto antes. Dos disparos en paralelo cubren el doble de suelo.</li>
<li>Muévete a menudo de lado: las torretas apuntan adonde estás, no adonde vas.</li>
<li>Si una franja se llena de enemigos, alguno puede parpadear. Sigue ahí: el Atari los dibuja por turnos.</li>
<li>Si pierdes una vida, aprovecha el parpadeo para recolocarte.</li>
</ul>
<div class="row" style="gap:3mm"><div class="shot" style="flex:1"><img src="img/full_go_1200.png"></div><div class="shot" style="flex:1"><img src="img/full_v_44500.png"></div></div>
<p class="soft" style="font-size:8pt">Sin vidas, GAME OVER y vuelta al título. Si derribas a Leviatán V, el Corazón de Acero cae: la pantalla de victoria espera dos pulsaciones de FIRE antes de volver al título.</p>
<div class="box" style="background:#17181f;color:#e9ebf2;border-color:#17181f">
 <h3 style="color:#f2b84b">Solo para quien se rinde</h3>
 <p>En la pantalla de título mueve el joystick <b>arriba, arriba, abajo, abajo, izquierda, derecha</b> y pulsa <b>FIRE</b>. Si oyes un BEEP, el Vórtice 5 será invencible hasta terminar el juego. Después habrá que volver a introducir el truco.</p>
</div>
{foot(12)}</section>''')

# contraportada
P(f'''<section class="page dark" style="justify-content:center;text-align:center;gap:6mm;background:radial-gradient(100% 70% at 50% 40%,#2b0f18 0%,#0b0d14 70%)">
<h1 style="font-size:34pt;font-weight:800">VÓRTICE <span style="color:#f07a6a">5</span></h1>
<div style="font:600 12pt 'Inter Display',sans-serif;color:#f2b84b">{SUBTITLE}</div>
<div style="align-self:center;border:1.3px solid #e9ebf2;border-radius:1.5mm;padding:1.2mm 3mm;font:700 8.5pt 'Inter Display',sans-serif">{DESIGN}</div>
<p style="font-size:10pt;font-style:italic;color:#cfd3e0;margin:0 4mm">{TAGLINE}</p>
<p style="font-size:9.5pt;margin:0 4mm">{CREDITS}</p>
<p class="mono" style="font-size:7pt;color:#959cb2;letter-spacing:.08em">{SIGN.upper()}<br>{MACHINE.upper()}</p>
</section>''')

html = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Vórtice 5 · Instrucciones</title><style>{css}</style></head><body>{"".join(pages)}</body></html>'
open('manual.html', 'w').write(html)
print('páginas', len(pages))
