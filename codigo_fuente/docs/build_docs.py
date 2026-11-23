#!/usr/bin/env python3
"""ZAK ATTACK · genera el atlas visual y el folleto de instrucciones (HTML -> PDF con Chromium)."""
import sys, os, html
sys.path.insert(0, '/home/claude/zak/gfx')
from pal import atari_rgb
import world

R = '/home/claude/final/'
def hx(c): return '#%02x%02x%02x' % atari_rgb(c)
def esc(s): return html.escape(s)

PH = [world.fase1(), world.fase2(), world.fase3(), world.fase4(), world.fase5()]
NAMES = ['Callejón Neón', 'Metro', 'Factoría del Miedo', 'Planta Química', 'Industrias Rata']

STORY = [
    "Zak vivía entre camas, colchas y cajas de cartón de los lotes de Navidad de sus dueños. "
    "Le encantaba dormir y las latas «Doble Placer» con salsita. Y sobre todo… las <b>GALLETITAS</b> de salmón "
    "que le daban cada día antes de irse todos a dormir…",
    "Pero lo que nadie sabe es que una vez, hace muchos años, mientras su familia estaba trabajando o en el colegio, "
    "una vez… <b>¡salvó al mundo!</b>",
    "<b>Industrias Rata</b> estuvo elaborando un plan de <b>Asedio Global</b> con su ejército, sus MEKAS y sus "
    "experimentos biológicos, para invadir las calles, eliminar a todos los michis y tratar de ser la nueva moda "
    "entre modernos. No se podía permitir.",
    "Ese día, ese día… Zak, el gato feliz…",
]
STORY_END = "COGIÓ SU FUSIL."

CREDITS = [
    ("Diseño gráfico, fases, nombres, historia y demás", "Tony, 2026"),
    ("Diseño V3", "Run'n'Gun Felino en 8 bits · GATO, COMANDO, CAOS"),
    ("Música", "Yo, Claudio"),
    ("Programación y versión Atari 8 bits", "Claude A.I."),
    ("Gato protagonizado por", "ZAK, el Gato"),
]

PHASE_INFO = [
    dict(desc="Ciudad nocturna de ladrillo rojo: escalera de incendios, toldos, cajas, cubos de basura, fosos en la calle "
              "y el cartel de neón <b>VORTICE 5</b>, en honor al primer juego de Tony.",
         en=[('soldier1', 'Rata soldado'), ('drone1', 'Dron mosquito')],
         boss="MEKDOZER 1", bdesc="Excavadora bulldog. Dispara desde la cabeza con aviso y, cada cuatro ataques, deja caer un "
              "escombro: tiembla arriba y unas flechas blancas marcan dónde caerá. Sus ojos se encienden y se apagan. "
              "Punto débil: la cabeza.", parts="2 partes con vida propia"),
    dict(desc="Estación de metro: azulejos, andenes, bancos y pasarelas sobre las vías. Caer a la vía es perder una vida.",
         en=[('drone1', 'Dron mosquito'), ('dog1', 'Perro guardián'), ('soldier1', 'Rata soldado')],
         boss="METROPLEX III", bdesc="Cabina de metro. Los faros disparan por turnos, con aviso; rotos los faros, a por la "
              "conductora. Los ojos de la conductora y los faros parpadean.", parts="3 partes con vida propia"),
    dict(desc="Fábrica oscura de vigas, tuberías y cintas transportadoras, con metal fundido animado en los fosos.",
         en=[('soldier1', 'Rata soldado'), ('jumper1', 'Rata saltadora'), ('drone1', 'Dron mosquito')],
         boss="CONTROL CENTRAL II", bdesc="Computadora de ciencia ficción. Dos bobinas de cinta hacen de ojos (giran, el buje "
              "parpadea) y una rejilla de luces de colores hace de boca. Las bobinas caen con el disparo diagonal; la boca, "
              "con el disparo normal hacia delante. Dispara balas a ras de suelo que hay que saltar.", parts="3 partes con vida propia"),
    dict(desc="Planta química: tubos de cultivo burbujeantes, estanterías y charcos tóxicos que no perdonan.",
         en=[('jumper1', 'Rata saltadora'), ('bug1', 'Bicho mutágeno')],
         boss="QUIMERA-9", bdesc="Experimento biológico hecho con dos sprites unidos (32 × 24). Salta entre alturas hacia Zak "
              "y cambia de color justo antes de saltar. Todo él es punto débil.", parts="1 parte"),
    dict(desc="Fortaleza de Industrias Rata: paneles, alarmas que parpadean, el núcleo y arcos eléctricos en el suelo.",
         en=[('soldier1', 'Rata soldado'), ('dog1', 'Perro guardián'), ('drone1', 'Dron mosquito'), ('bug1', 'Bicho mutágeno')],
         boss="RATTUS PRIME", bdesc="Cabeza de rata gigante con casco. Los ojos son los puntos débiles: laten y se apagan. "
              "Sin ojos, la boca con incisivos queda expuesta. Es el jefe final: dispara más a menudo que nadie.",
         parts="3 partes con vida propia"),
]

TRACKS = [("01", "Zak coge su fusil", "Título y Callejón Neón", "0:32"), ("02", "Metro", "Fase 2", "0:28"),
          ("03", "Factoría del Miedo", "Fase 3", "0:37"), ("04", "Planta Química", "Fase 4", "0:32"),
          ("05", "Industrias Rata", "Fase 5", "0:28"), ("06", "Jefe a la vista", "Todos los jefes", "0:28"),
          ("07", "Misión cumplida", "Fase superada y final", "0:06"), ("08", "Game Over", "Fin de partida", "0:08")]

CSS = """
@font-face{font-family:'ID';src:local('Inter Display Black'),local('InterDisplay-Black');font-weight:900}
:root{--bg:#0e0c1a;--panel:#1a1630;--edge:#4b3a86;--gold:#ffc440;--txt:#e6e4f0;--dim:#a19fbc;--red:#e3312b;--cyan:#6fd3ff;--green:#b6e35a}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--bg);color:var(--txt);font-family:'Inter',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:PW;height:PH;position:relative;overflow:hidden;page-break-after:always;background:var(--bg);padding:PAD}
.page:last-child{page-break-after:auto}
img{display:block}
.px{image-rendering:pixelated}
h1,h2,h3{font-family:'Inter Display',sans-serif;font-weight:900;letter-spacing:.01em}
h2{font-size:H2;color:var(--gold);text-transform:uppercase;margin-bottom:3mm;font-style:italic}
h2 small{display:block;font-size:.42em;color:var(--dim);font-style:normal;letter-spacing:.12em;font-weight:600;margin-top:1mm}
h3{font-size:H3;color:var(--gold);margin:0 0 1.5mm}
p{font-size:FS;line-height:1.5;margin-bottom:2.2mm}
.mono{font-family:'DejaVu Sans Mono',monospace}
.kick{font-family:'DejaVu Sans Mono',monospace;font-size:7.5pt;letter-spacing:.2em;color:var(--red);text-transform:uppercase;font-weight:700}
.panel{background:var(--panel);border:.5mm solid var(--edge);border-radius:2.5mm;padding:4mm}
.grid{display:grid;gap:4mm}
.shot{width:100%;border:.5mm solid var(--edge);border-radius:1.5mm;image-rendering:pixelated}
.cap{font-size:7.5pt;color:var(--dim);margin-top:1.2mm}
.tag{display:inline-block;font-family:'DejaVu Sans Mono',monospace;font-size:7pt;padding:.6mm 2mm;border-radius:1mm;background:#2a2450;color:var(--gold);margin:0 1mm 1mm 0}
table{border-collapse:collapse;width:100%;font-size:8.5pt}
td,th{padding:1.6mm 2mm;border-bottom:.3mm solid #2f2858;text-align:left;vertical-align:top}
th{color:var(--gold);font-family:'Inter Display';font-weight:800;text-transform:uppercase;font-size:7.5pt;letter-spacing:.08em}
.foot{position:absolute;bottom:6mm;left:PADX;right:PADX;display:flex;justify-content:space-between;font-family:'DejaVu Sans Mono',monospace;font-size:6.5pt;color:#6d6a8c;letter-spacing:.15em}
.sw{display:inline-block;width:6mm;height:6mm;border-radius:1mm;border:.3mm solid #000;vertical-align:middle;margin-right:1mm}
.spr{display:flex;flex-wrap:wrap;gap:4mm;align-items:flex-end}
.spr div{text-align:center;font-size:7pt;color:var(--dim)}
.spr img{margin:0 auto 1.5mm;image-rendering:pixelated}
ul{margin-left:4.5mm}
li{font-size:FS;line-height:1.45;margin-bottom:1.2mm}
.big{font-family:'Inter Display';font-weight:900;font-style:italic;color:var(--red);text-shadow:0 0 6mm rgba(227,49,43,.5)}
"""

def page_css(pw, ph, pad, padx, fs, h2, h3):
    return (CSS.replace('PW', pw).replace('PH', ph).replace('PADX', padx).replace('PAD', pad)
            .replace('FS', fs).replace('H2', h2).replace('H3', h3) + '@page{size:%s %s;margin:0}' % (pw, ph))

def spr(name, h):
    return '<img class="px" src="sprites/%s.png" style="height:%s">' % (name, h)

def palette(L):
    return ''.join('<span class="sw" style="background:%s"></span>' % hx(L.colors[k]) for k in ('bk', 'pf0', 'pf1', 'pf2', 'pf3'))

def foot(left, n):
    return '<div class="foot"><span>%s</span><span>%02d</span></div>' % (left, n)

# =====================================================================================  ATLAS
def atlas():
    P = []; n = [0]
    def pg(body, cls='', style='', f=True):
        n[0] += 1
        P.append('<section class="page %s" style="%s">%s%s</section>' % (cls, style, body,
                 foot('ZAK ATTACK · ATLAS VISUAL DEL PROYECTO', n[0]) if f else ''))
    # 1 portada
    pg('''<img src="assets/caratula.png" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
    <div style="position:absolute;left:0;right:0;bottom:0;height:62mm;background:linear-gradient(transparent,rgba(8,6,16,.94) 38%)"></div>
    <div style="position:absolute;left:14mm;right:14mm;bottom:14mm">
      <div class="kick" style="color:var(--gold)">Atlas visual completo del proyecto</div>
      <div style="font-family:'Inter Display';font-weight:900;font-size:26pt;font-style:italic;line-height:1.05;margin:2mm 0 3mm">Run'n'Gun Felino en 8 bits</div>
      <div class="mono" style="font-size:8pt;color:var(--dim);letter-spacing:.14em">ATARI 400 · 800 · XL · XE &nbsp;—&nbsp; GATO. COMANDO. CAOS. &nbsp;—&nbsp; TONY Y CLAUDE A.I. · 2026</div>
    </div>''', style='padding:0', f=False)
    # 2 historia
    pg('''<div style="position:absolute;inset:0;background:url(assets/ilustracion.png) center/cover;opacity:.28"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,12,26,.98) 55%%,rgba(14,12,26,.55))"></div>
    <div style="position:relative;width:118mm;margin-top:18mm">
      <div class="kick">La historia</div>
      <h2 style="font-size:30pt;margin:2mm 0 8mm">El gato que<br>salvó al mundo</h2>
      %s
      <div class="big" style="font-size:30pt;margin-top:7mm">%s</div>
    </div>
    <img class="px" src="assets/zak_retrato_pixelart.png" style="position:absolute;right:14mm;bottom:22mm;width:58mm;border:.6mm solid var(--gold);border-radius:2mm">
    ''' % (''.join('<p style="font-size:11pt;line-height:1.6;margin-bottom:4mm">%s</p>' % s for s in STORY), STORY_END))
    # 3 créditos
    rows = ''.join('<div style="margin-bottom:6mm"><div class="kick" style="color:var(--dim)">%s</div>'
                   '<div style="font-family:Inter Display;font-weight:900;font-size:17pt;color:var(--gold);margin-top:1mm">%s</div></div>'
                   % (esc(a), esc(b)) for a, b in CREDITS)
    pg('''<div class="kick">Créditos</div><h2 style="font-size:26pt;margin:2mm 0 8mm">Quién hizo qué</h2>
    <div style="display:grid;grid-template-columns:1fr 78mm;gap:10mm">
      <div>%s
        <p style="color:var(--dim);margin-top:6mm">Un juego de <b style="color:var(--txt)">Tony y Claude A.I.</b> para Atari 400/800/XL/XE.
        Hecho a la manera de siempre: adaptar la idea a los límites reales de la máquina en vez de clonarla.</p>
      </div>
      <div>
        <img src="assets/zak_foto.jpg" style="width:100%%;border-radius:2mm;border:.6mm solid var(--gold)">
        <div class="cap" style="font-size:9pt;color:var(--txt);margin-top:2.5mm"><b>ZAK, el Gato.</b> El de verdad, en su caja de cartón.</div>
        <div style="display:flex;gap:4mm;margin-top:6mm;align-items:center">
          <img class="px" src="assets/zak_retrato_pixelart.png" style="width:36mm;border-radius:1.5mm">
          %s
        </div>
        <div class="cap">De la foto al píxel: el retrato redibujado para la portada y el sprite de 8 × 20 del juego.</div>
      </div>
    </div>''' % (rows, spr('zak_stand', '24mm')))
    # 4 ficha
    pg('''<div class="kick">Ficha del proyecto</div><h2 style="font-size:22pt;margin:2mm 0 6mm">Diseño V3 · Run'n'Gun Felino en 8 bits</h2>
    <div class="grid" style="grid-template-columns:1fr 1fr">
      <div class="panel"><h3>La máquina</h3><table>
        <tr><td>Ordenadores</td><td>Atari 400 / 800 / XL / XE, 48 KB</td></tr>
        <tr><td>Vídeo</td><td>NTSC (en PAL va algo más lento)</td></tr>
        <tr><td>Control</td><td>Joystick de un botón</td></tr>
        <tr><td>Gráficos</td><td>ANTIC modo 4 (4 colores + PF3) y Player/Missile</td></tr>
        <tr><td>Sonido</td><td>POKEY: melodía, bajo, batería y efectos</td></tr></table></div>
      <div class="panel"><h3>Formatos</h3><table>
        <tr><td class="mono">zakattack.xex</td><td>Ejecutable, 30,7 KB ($2000–$97BD)</td></tr>
        <tr><td class="mono">zakattack.atr</td><td>Disco autoarrancable sin DOS, 240 sectores</td></tr>
        <tr><td class="mono">zakattack.car</td><td>Cartucho AtariMax 128 KB (tipo 41) que copia el juego a RAM</td></tr>
        <tr><td>Probado en</td><td>atari800 (NTSC, XL 64 KB) y un bot que se pasa las 5 fases</td></tr></table></div>
      <div class="panel"><h3>Dificultad</h3><table>
        <tr><th></th><th>Fácil</th><th>Normal</th><th>HARDCORE</th></tr>
        <tr><td>Vidas / corazones</td><td>5 / 4</td><td>3 / 3</td><td>3 / 2</td></tr>
        <tr><td>Balas enemigas</td><td>1</td><td>2</td><td>2, más rápidas</td></tr>
        <tr><td>Vida de los jefes</td><td>−25 %%</td><td>normal</td><td>+25 %%</td></tr>
        <tr><td>Aviso de ataque</td><td>1 s</td><td>0,7 s</td><td>0,4 s</td></tr></table></div>
      <div class="panel"><h3>Lo que cabe</h3><ul>
        <li>Un jugador: Zak con dos sprites superpuestos (pelo blanco + equipo rojo).</li>
        <li>Hasta 4 enemigos a la vez: 2 en el aire y 2 en tierra, con los mismos dos sprites recolocados a media pantalla.</li>
        <li>Un solo arma con dos balas en pantalla y 8 direcciones de tiro.</li>
        <li>Cinco fases de 300 columnas, cada una con su juego de caracteres y su jefe.</li>
        <li>Recogibles: pescado (vida) y lata dorada (vida extra).</li></ul></div>
    </div>
    <div class="panel" style="margin-top:4mm;display:flex;gap:6mm;align-items:center">
      <img class="px" src="sprites/logo_atari.png" style="width:80mm">
      <p style="margin:0;color:var(--dim)">El logotipo del título está dibujado con el juego de caracteres y un degradado línea a línea hecho con interrupciones de pantalla. Nunca entra el modo atracción del Atari.</p>
    </div>
    <div class="grid" style="grid-template-columns:repeat(5,1fr);gap:3mm;margin-top:4mm">%s</div>''' % ''.join(
      '<div><img class="shot" src="capturas/f%d_juego.png"><div class="cap"><b style="color:var(--gold)">%d</b> · %s</div></div>' % (i + 1, i + 1, NAMES[i]) for i in range(5)))
    # 5 Zak
    zf = [('stand', 'Quieto'), ('run1', 'Correr 1'), ('run2', 'Correr 2'), ('run3', 'Correr 3'), ('jump', 'Salto'),
          ('crouch', 'Agachado'), ('up', 'Tiro arriba'), ('diag', 'Diagonal'), ('dead', 'Caído')]
    pg('''<div class="kick">El héroe</div><h2 style="font-size:24pt;margin:2mm 0 5mm">Zak · sprites P0 + P1</h2>
    <div class="panel"><div class="spr" style="justify-content:space-between">%s</div>
    <p style="margin-top:4mm;color:var(--dim)">8 × 20 píxeles por cuadro, en anchura normal de player (8 color clocks). Se refleja para mirar a la izquierda.
    Pelo blanco <span class="sw" style="background:%s"></span> y bandana y equipo rojo <span class="sw" style="background:%s"></span>; el arma blanca asoma para que se note que va armado.</p></div>
    <div class="grid" style="grid-template-columns:1fr 1fr;margin-top:4mm">
      <div class="panel"><h3>Cómo dispara</h3><ul>
        <li><b>FIRE corriendo:</b> disparo recto sin dejar de correr ni de saltar.</li>
        <li><b>FIRE desde quieto:</b> Zak se planta y, mientras mantienes FIRE, la palanca apunta adelante, en diagonal, arriba o agachado.</li>
        <li><b>En el aire:</b> 8 direcciones.</li>
        <li>Dos balas a la vez como máximo.</li></ul></div>
      <div class="panel"><h3>En el juego</h3><img class="shot" src="capturas/f2_juego.png"><div class="cap">Zak saltando en el Metro.</div></div>
    </div>
    <div class="panel" style="margin-top:4mm;display:grid;grid-template-columns:30mm 1fr;gap:5mm;align-items:center">
      <img src="assets/zak_attack_portada.png" style="width:30mm;border-radius:1.5mm">
      <div><h3>La portada en píxeles</h3><p style="margin:0">La cara de Zak, el gato de verdad, redibujada a mano en pixel art (no es un filtro sobre la foto): pelo gris atigrado, mancha blanca en el hocico, ojos amarillo verdoso y la bandana roja de comando.</p></div></div>''' % (''.join('<div>%s%s</div>' % (spr('zak_' + k, '27mm'), v) for k, v in zf), hx(0x0C), hx(0x44)))
    # 6 enemigos
    ens = [('soldier', 'Rata soldado', 'Patrulla y dispara. Fases 1, 2, 3 y 5.'), ('drone', 'Dron mosquito', 'Vuela en la franja alta. Fases 1, 2, 3 y 5.'),
           ('dog', 'Perro guardián', 'Corre hacia Zak y se da la vuelta en paredes y bordes. Fases 2 y 5.'),
           ('jumper', 'Rata saltadora', 'Salta comprobando antes el suelo de destino. Fases 3 y 4.'),
           ('bug', 'Bicho mutágeno', 'Salta a ras de suelo. Fases 4 y 5.')]
    rows = ''.join('<div class="panel" style="display:flex;gap:5mm;align-items:center">%s%s<div><h3>%s</h3><p style="margin:0;color:var(--dim)">%s</p></div></div>'
                   % (spr('en_%s1' % k, '17mm'), spr('en_%s2' % k, '17mm'), a, b) for k, a, b in ens)
    pg('''<div class="kick">El ejército de Industrias Rata</div><h2 style="font-size:24pt;margin:2mm 0 5mm">Enemigos y objetos</h2>
    <div class="grid" style="grid-template-columns:1fr 1fr">%s
      <div class="panel" style="display:flex;gap:5mm;align-items:center">%s%s<div><h3>Pescado y lata dorada</h3><p style="margin:0;color:var(--dim)">El pescado recupera la vida; la lata dorada «Doble Placer» da una vida extra.</p></div></div>
    </div>
    <div class="panel" style="margin-top:4mm"><h3>Reglas de comportamiento</h3><ul>
      <li>Cada enemigo es un sprite de 8 × 16 y un color; la explosión de 2 cuadros es la misma para todos.</li>
      <li>Ninguno se tira a los fosos ni se queda pegado encima de Zak: eligen dirección al aparecer y solo se dan la vuelta en paredes y bordes.</li>
      <li>Lava y electricidad también los matan a ellos. Sin torretas: más enemigos de los tipos que ya existen.</li></ul></div>
    <div class="grid" style="grid-template-columns:1fr 1fr;margin-top:4mm">
      <div><img class="shot" src="capturas/f3_juego.png"><div class="cap">Ratas soldado y saltadoras en la Factoría del Miedo.</div></div>
      <div><img class="shot" src="capturas/f5_juego.png"><div class="cap">Las cuatro familias juntas en Industrias Rata.</div></div></div>'''
       % (rows, spr('en_fish', '17mm'), spr('en_can', '17mm')))
    # 7-11 fases
    for i, (L, I) in enumerate(zip(PH, PHASE_INFO)):
        f = i + 1
        en = ''.join('<div>%s%s</div>' % (spr('en_' + k, '13mm'), v) for k, v in I['en'])
        pg('''<div style="display:flex;justify-content:space-between;align-items:flex-end">
          <div><div class="kick">Fase %d</div><h2 style="font-size:28pt;margin:1mm 0 0">%s</h2></div>
          <div style="text-align:right"><div class="kick" style="color:var(--dim)">Paleta BK/PF0/PF1/PF2/PF3</div><div style="margin-top:1.5mm">%s</div></div></div>
        <p style="font-size:10pt;margin:4mm 0">%s</p>
        <div class="grid" style="grid-template-columns:1fr 1fr">
          <div><img class="shot" src="capturas/f%d_cartel.png"><div class="cap">Cartel de entrada a la fase.</div></div>
          <div><img class="shot" src="capturas/f%d_juego.png"><div class="cap">En plena fase (captura real del emulador).</div></div>
          <div><img class="shot" src="capturas/f%d_jefe.png"><div class="cap">Jefe: %s.</div></div>
          <div><img class="shot" src="capturas/f%d_explota.png"><div class="cap">%s explota: hasta 8 explosiones a la vez.</div></div>
        </div>
        <div class="grid" style="grid-template-columns:1.6fr 1fr;margin-top:4mm">
          <div class="panel"><h3>Jefe · %s</h3><p style="margin:0">%s</p><div style="margin-top:2mm"><span class="tag">%s</span><span class="tag">solo dispara</span></div></div>
          <div class="panel"><h3>Enemigos</h3><div class="spr">%s</div></div>
        </div>''' % (f, esc(NAMES[i]), palette(L), I['desc'], f, f, f, I['boss'], f, I['boss'], I['boss'], I['bdesc'], I['parts'], en))
    # 12 diseños de jefes
    pg('''<div class="kick">Hojas de diseño aprobadas</div><h2 style="font-size:24pt;margin:2mm 0 5mm">Los jefes nuevos</h2>
    <div class="grid" style="grid-template-columns:1fr">
      <div class="panel"><img src="assets/control_central.png" style="width:100%;border-radius:1.5mm"><div class="cap">CONTROL CENTRAL II, a partir del boceto de Tony: bobinas por ojos y rejilla de luces por boca.</div></div>
      <div class="panel"><img src="assets/rattus_prime.png" style="width:100%;border-radius:1.5mm"><div class="cap">RATTUS PRIME: cabeza de rata gigante; ojos y boca como puntos débiles.</div></div>
    </div>''')
    # 13 jefes resumen
    bt = ''.join('<tr><td><b style="color:var(--gold)">%s</b><br><span style="color:var(--dim)">%s</span></td><td>%s</td></tr>' % (I['boss'], NAMES[i], I['bdesc']) for i, I in enumerate(PHASE_INFO))
    pg('''<div class="kick">Cómo se lucha</div><h2 style="font-size:24pt;margin:2mm 0 5mm">Jefes · reglas y efectos</h2>
    <div class="panel"><table>%s</table></div>
    <div class="grid" style="grid-template-columns:1fr 1fr;margin-top:4mm">
      <div class="panel"><h3>Reglas comunes</h3><ul>
        <li>Los jefes solo disparan: ráfagas de balas naranjas que salen de su borde. La única excepción es el escombro de MEKDOZER 1.</li>
        <li>Cada ataque se avisa: parpadea la pieza que va a disparar.</li>
        <li>Con piezas, el núcleo solo se expone cuando caen las demás, y entonces parpadea.</li>
        <li>Ojos y luces que se encienden y apagan, animados reescribiendo caracteres, sin sprites.</li></ul></div>
      <div class="panel"><h3>La explosión final</h3>
        <div class="spr" style="margin-bottom:3mm">%s</div>
        <p style="margin:0">Al morir, el jefe se reparte en 4 franjas y en cada una se recolocan 2 sprites con una interrupción de pantalla: hasta 8 explosiones sin parpadeo. Cada una nace blanca y pasa por amarillo y naranja hasta el rojo. Encima, destellos de fondo, retumbe y un fogonazo blanco.</p></div>
    </div>''' % (bt, ''.join(spr('boom_%d' % k, '15mm') for k in range(4))))
    # 14 técnica
    pg('''<div class="kick">Bajo el capó</div><h2 style="font-size:24pt;margin:2mm 0 5mm">Técnica de pantalla</h2>
    <div class="grid" style="grid-template-columns:1fr 1fr">
      <div class="panel"><h3>Display list</h3><ul>
        <li>Marcador: 1 línea ANTIC 2 con la fuente de la ROM.</li>
        <li>Juego: 22 filas ANTIC 4 = 160 × 176 píxeles, 4 colores + PF3 en caracteres inversos.</li>
        <li>Scroll fino horizontal (HSCROL) sobre un anillo de 64 columnas por fila.</li>
        <li>Un juego de caracteres de 1 KB por fase (máx. 128): fondo, peligros, plataformas de un sentido, sólidos y jefe.</li>
        <li>Fondo repetido cada 16 columnas más un primer plano comprimido por columnas.</li></ul></div>
      <div class="panel"><h3>Interrupciones (DLI)</h3><ul>
        <li><b>Tras el marcador:</b> juego de caracteres y colores del nivel.</li>
        <li><b>Fila 7:</b> recoloca P2 y P3 para la franja de tierra (2 enemigos arriba + 2 abajo).</li>
        <li><b>Filas 9, 11 y 13:</b> solo mientras explota un jefe; 4 franjas × 2 sprites.</li>
        <li><b>Abajo:</b> fondo a negro.</li>
        <li>La VBI copia el indicador de explosiones y pone o quita los bits DLI, para que la lista y la cadena siempre coincidan.</li></ul></div>
      <div class="panel"><h3>Sprites y balas</h3><ul>
        <li>P0 + P1: Zak. P2 + P3: enemigos o QUIMERA-9.</li>
        <li>Se pintan al principio del cuadro, justo tras la VBI, y HPOS se escribe directo: sin sprites partidos.</li>
        <li>Sin quinto player: cada misil va con el color de su player y por delante del fondo (GPRIOR $01).</li>
        <li>Balas enemigas a doble anchura y 4 líneas de alto.</li></ul></div>
      <div class="panel"><h3>Mapa de memoria</h3><table class="mono" style="font-size:7.5pt">
        <tr><td>$0080–$00FF</td><td>página cero</td></tr><tr><td>$0700–$080D</td><td>variables</td></tr>
        <tr><td>$2000–$97BD</td><td>código, datos, música</td></tr><tr><td>$AC00</td><td>display list del juego</td></tr>
        <tr><td>$B400</td><td>display list de textos</td></tr><tr><td>$B800</td><td>Player/Missile</td></tr></table>
        <p style="margin:2mm 0 0;color:var(--dim)">El cartucho copia los bancos 1–4 a $2000–$9FFF, se desconecta y avisa al OS (GINTLK) para que el XL original no se cuelgue.</p></div>
    </div>''')
    # 15 pantallas
    pg('''<div class="kick">Pantallas</div><h2 style="font-size:24pt;margin:2mm 0 5mm">Título, menú y finales</h2>
    <div class="grid" style="grid-template-columns:1fr 1fr">
      <div><img class="shot" src="capturas/titulo.png"><div class="cap">Título. Izquierda/derecha elige dificultad; FIRE empieza.</div></div>
      <div><img class="shot" src="capturas/titulo_hardcore.png"><div class="cap">La dificultad difícil se llama siempre HARDCORE.</div></div>
      <div><img class="shot" src="capturas/titulo_invencible.png"><div class="cap">Truco: abajo, abajo, FIRE en el título.</div></div>
      <div><img class="shot" src="capturas/hud.png"><div class="cap">Marcador: puntos, corazones, vidas y fase.</div></div>
      <div><img class="shot" src="capturas/game_over.png"><div class="cap">GAME OVER: Industrias Rata celebra su victoria.</div></div>
      <div><img class="shot" src="capturas/final.png"><div class="cap">MISIÓN CUMPLIDA: la ciudad vuelve a ser de los gatos.</div></div>
    </div>''')
    # 16 música
    tr = ''.join('<tr><td class="mono" style="color:var(--gold)">%s</td><td><b>%s</b></td><td style="color:var(--dim)">%s</td><td class="mono">%s</td></tr>' % t for t in TRACKS)
    pg('''<div class="kick">Banda sonora</div><h2 style="font-size:24pt;margin:2mm 0 5mm">Música por Yo, Claudio</h2>
    <div class="grid" style="grid-template-columns:1.3fr 1fr">
      <div class="panel"><table><tr><th>#</th><th>Tema</th><th>Dónde suena</th><th>Duración</th></tr>%s</table>
        <p style="margin-top:3mm;color:var(--dim)">Grabada directamente del chip POKEY en el emulador: cada tema son dos vueltas del bucle con un fundido. Va en la carpeta <span class="mono">banda_sonora</span> del paquete, en MP3.</p></div>
      <div class="panel"><h3>Cómo suena</h3><ul>
        <li>Marcha militar y aventurera: melodía, bajo y una batería rítmica de bombo, caja y charles.</li>
        <li>Cada fase tiene su tema y su ritmo de batería: marcha, galope, pesado, rápido.</li>
        <li>Un golpe de batería tapa el sonido de los disparos; las explosiones y los golpes no se tapan.</li>
        <li>Los jefes tienen tema propio; al morir, la música se corta y solo queda el retumbe.</li></ul></div>
    </div>
    <img src="assets/ilustracion.png" style="width:100%%;height:92mm;object-fit:cover;object-position:center 30%%;border-radius:2mm;margin-top:4mm;border:.5mm solid var(--edge)">''' % tr)
    # 17 evolución
    pg('''<div class="kick">Diario de desarrollo</div><h2 style="font-size:24pt;margin:2mm 0 5mm">Cómo llegó hasta aquí</h2>
    <div class="grid" style="grid-template-columns:1fr 1fr">
      <div class="panel"><h3>Nombres</h3><table>
        <tr><th>Ahora</th><th>Antes</th></tr>
        <tr><td>Metro · METROPLEX III</td><td>Tren</td></tr>
        <tr><td>Factoría del Miedo</td><td>Fundición Omega</td></tr>
        <tr><td>CONTROL CENTRAL II</td><td>EL HORNO</td></tr>
        <tr><td>Planta Química</td><td>Laboratorio Umbral</td></tr>
        <tr><td>Industrias Rata</td><td>Corazón R.A.T.A.</td></tr>
        <tr><td>MEKDOZER 1</td><td>GRUÑÓN-01</td></tr>
        <tr><td>HARDCORE</td><td>Difícil</td></tr></table></div>
      <div class="panel"><h3>Decisiones de diseño</h3><ul>
        <li>Enemigos ratas; Zak es blanco, como el gato de verdad.</li>
        <li>Cartel VORTICE 5 en el Callejón Neón.</li>
        <li>Disparo diagonal plantándose con FIRE; tres dificultades; avisos en cada ataque de jefe.</li>
        <li>Fuera torretas; más enemigos de los que ya hay.</li>
        <li>Regla de oro: los jefes solo disparan.</li>
        <li>Fuera 7 plataformas a las que Zak no llegaba (el salto sube 39 píxeles y estaban a 40).</li>
        <li>La boca de CONTROL CENTRAL II, a la altura del disparo normal.</li></ul></div>
      <div class="panel" style="grid-column:span 2"><h3>Lecciones para el banco de trabajo</h3><ul>
        <li>Un sprite solo existe dentro de su franja: si se recoloca por DLI, todo lo que dibuje debe vivir en esas líneas.</li>
        <li>El modo quinto player deja los misiles detrás de PF0–PF2: mejor sin él.</li>
        <li>Simular la física cuadro a cuadro para saber qué plataformas se pueden pisar.</li>
        <li>Un cartucho que se desconecta debe copiar TRIG3 a GINTLK o el OS XL original se cuelga.</li></ul></div>
    </div>''')
    # 18 contraportada
    pg('''<img src="assets/zak_attack_portada.png" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.9">
    <div style="position:absolute;left:0;right:0;bottom:0;height:70mm;background:linear-gradient(transparent,rgba(8,6,16,.96) 40%)"></div>
    <div style="position:absolute;left:14mm;right:14mm;bottom:14mm;text-align:center">
      <div style="font-family:'Inter Display';font-weight:900;font-size:15pt;font-style:italic">Ese día, Zak cogió su fusil.</div>
      <div class="mono" style="font-size:7.5pt;color:var(--dim);margin-top:3mm;letter-spacing:.14em">DISEÑO, FASES, NOMBRES E HISTORIA: TONY · MÚSICA: YO, CLAUDIO · PROGRAMACIÓN: CLAUDE A.I. · PROTAGONIZADO POR ZAK, EL GATO</div>
    </div>''', style='padding:0', f=False)
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8"><title>ZAK ATTACK · Atlas visual</title><style>%s</style></head><body>%s</body></html>'
            % (page_css('210mm', '297mm', '14mm', '14mm', '9pt', '24pt', '11pt'), ''.join(P)))

# =====================================================================================  FOLLETO (A5)
def folleto():
    P = []; n = [0]
    def pg(body, style='', f=True):
        n[0] += 1
        P.append('<section class="page" style="%s">%s%s</section>' % (style, body, foot('ZAK ATTACK · INSTRUCCIONES', n[0]) if f else ''))
    pg('''<img src="assets/caratula.png" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
    <div style="position:absolute;left:0;right:0;bottom:0;height:42mm;background:linear-gradient(transparent,rgba(8,6,16,.95) 40%)"></div>
    <div style="position:absolute;left:10mm;right:10mm;bottom:10mm">
      <div class="kick" style="color:var(--gold)">Manual de instrucciones</div>
      <div class="mono" style="font-size:6.5pt;color:var(--dim);letter-spacing:.14em;margin-top:2mm">ATARI 400 · 800 · XL · XE · 48 KB · JOYSTICK</div></div>''', style='padding:0', f=False)
    pg('''<div style="position:absolute;inset:0;background:url(assets/ilustracion.png) center/cover;opacity:.22"></div>
    <div style="position:absolute;inset:0;background:rgba(14,12,26,.82)"></div>
    <div style="position:relative">
    <div class="kick">La historia</div><h2 style="margin:1.5mm 0 5mm">El gato que salvó al mundo</h2>
    %s<div class="big" style="font-size:20pt;margin-top:4mm">%s</div>
    <img class="px" src="assets/zak_retrato_pixelart.png" style="width:38mm;margin:6mm 0 0 auto;border:.5mm solid var(--gold);border-radius:1.5mm"></div>'''
       % (''.join('<p style="font-size:9pt;line-height:1.55">%s</p>' % s for s in STORY), STORY_END))
    pg('''<div class="kick">Para empezar</div><h2 style="margin:1.5mm 0 4mm">Cargar el juego</h2>
    <div class="panel" style="margin-bottom:3mm"><h3>Cartucho · zakattack.car</h3><p style="margin:0">Insértalo y enciende el ordenador. En un emulador, abre el archivo como cartucho (AtariMax 128 KB, tipo 41).</p></div>
    <div class="panel" style="margin-bottom:3mm"><h3>Disco · zakattack.atr</h3><p style="margin:0">Disco autoarrancable, sin DOS: ponlo en la unidad 1 y enciende sin BASIC (en los XL/XE, con OPTION pulsado).</p></div>
    <div class="panel" style="margin-bottom:3mm"><h3>Ejecutable · zakattack.xex</h3><p style="margin:0">Para emuladores y cargadores SD. Desactiva BASIC por sí solo.</p></div>
    <p style="color:var(--dim)">Pensado para NTSC; en PAL funciona algo más lento. Conecta el joystick en el puerto 1.</p>
    <img class="shot" src="capturas/titulo.png" style="margin-top:2mm">
    <div class="cap">En el título: izquierda y derecha eligen la dificultad, FIRE empieza la partida.</div>''')
    pg('''<div class="kick">Los mandos</div><h2 style="margin:1.5mm 0 4mm">Controlar a Zak</h2>
    <table>
      <tr><td style="width:24mm">%s</td><td><b>Izquierda / derecha:</b> correr.</td></tr>
      <tr><td>%s</td><td><b>Arriba:</b> saltar. Cada salto es una nueva pulsación.</td></tr>
      <tr><td>%s</td><td><b>Abajo:</b> agacharse.</td></tr>
      <tr><td>%s</td><td><b>FIRE corriendo:</b> disparo recto sin dejar de correr ni de saltar.</td></tr>
      <tr><td>%s</td><td><b>FIRE desde quieto:</b> Zak se planta. Mientras mantienes FIRE, la palanca apunta: adelante, arriba + lado (diagonal), arriba o abajo. Suelta FIRE para volver a moverte.</td></tr>
      <tr><td></td><td><b>En el aire:</b> dispara en 8 direcciones.</td></tr>
      <tr><td></td><td><b>P o espacio:</b> pausa.</td></tr></table>
    <div class="panel" style="margin-top:4mm"><h3>Plantado con FIRE: hacia dónde apunta</h3>
      <div class="spr" style="justify-content:space-around;margin-top:2mm">
        <div>%s→ adelante</div><div>%s↗ arriba + lado</div><div>%s↑ arriba</div><div>%s↓ abajo</div></div></div>'''
       % tuple(spr('zak_' + k, '16mm') for k in ('run1', 'jump', 'crouch', 'stand', 'diag', 'stand', 'diag', 'up', 'crouch')))
    pg('''<div class="kick">En pantalla</div><h2 style="margin:1.5mm 0 4mm">El marcador</h2>
    <img class="shot" src="capturas/hud.png">
    <table style="margin-top:3mm">
      <tr><td class="mono" style="color:var(--gold)">PUNTOS</td><td>Tu puntuación.</td></tr>
      <tr><td class="mono" style="color:var(--gold)">VIDA ♥♥♥</td><td>Corazones: cada golpe quita uno. Sin corazones pierdes una vida.</td></tr>
      <tr><td class="mono" style="color:var(--gold)">ZAKx3</td><td>Vidas que te quedan.</td></tr>
      <tr><td class="mono" style="color:var(--gold)">FASE</td><td>Fase en la que estás, de 1 a 5.</td></tr></table>
    <div class="panel" style="margin-top:4mm;display:flex;gap:4mm;align-items:center">%s%s<p style="margin:0">El <b>pescado</b> recupera la vida. La <b>lata dorada</b> «Doble Placer» da una vida extra.</p></div>
    <p style="margin-top:3mm;color:var(--dim)">Cuidado con los fosos, la lava, los charcos tóxicos y los arcos eléctricos: tocarlos cuesta caro.</p>'''
       % (spr('en_fish', '13mm'), spr('en_can', '13mm')))
    ens = [('soldier', 'Rata soldado', 'Patrulla y dispara.'), ('drone', 'Dron mosquito', 'Ataca desde el aire.'),
           ('dog', 'Perro guardián', 'Corre a por ti.'), ('jumper', 'Rata saltadora', 'Salta para alcanzarte.'),
           ('bug', 'Bicho mutágeno', 'Brinca a ras de suelo.')]
    pg('''<div class="kick">El enemigo</div><h2 style="margin:1.5mm 0 4mm">El ejército de Industrias Rata</h2>
    %s<p style="margin-top:3mm;color:var(--dim)">Puede haber hasta cuatro a la vez: dos en el aire y dos en tierra.</p>
    <img class="shot" src="capturas/f5_juego.png" style="margin-top:2mm"><div class="cap">Industrias Rata: las cuatro familias juntas.</div>'''
       % ''.join('<div class="panel" style="display:flex;gap:4mm;align-items:center;margin-bottom:2.5mm;padding:3mm">%s%s<div><h3 style="margin:0">%s</h3><p style="margin:0;color:var(--dim)">%s</p></div></div>'
                 % (spr('en_%s1' % k, '11mm'), spr('en_%s2' % k, '11mm'), a, b) for k, a, b in ens))
    pg('''<div class="kick">La misión</div><h2 style="margin:1.5mm 0 4mm">Las cinco fases</h2>%s'''
       % ''.join('<div style="display:grid;grid-template-columns:44mm 1fr;gap:3mm;margin-bottom:2.6mm;align-items:center"><img class="shot" src="capturas/f%d_juego.png"><div><h3 style="margin:0">%d · %s</h3><p style="margin:0;font-size:8pt;color:var(--dim)">Jefe: %s</p></div></div>'
                 % (i + 1, i + 1, NAMES[i], PHASE_INFO[i]['boss']) for i in range(5)))
    tips = ["MEKDOZER 1: dispárale a la cabeza y, cuando veas las flechas blancas, apártate del escombro.",
            "METROPLEX III: rompe primero los faros; luego, a por la conductora.",
            "CONTROL CENTRAL II: bobinas con el disparo diagonal; la boca cae con el disparo normal. Salta sus balas rasantes.",
            "QUIMERA-9: cuando cambie de color, va a saltar. No te quedes debajo.",
            "RATTUS PRIME: primero los ojos, luego la boca. Dispara más que nadie: no pares de moverte."]
    pg('''<div class="kick">Consejos</div><h2 style="margin:1.5mm 0 4mm">Cómo vencer a los jefes</h2>
    <p>Todos avisan antes de atacar: la pieza que va a disparar parpadea. Los que tienen piezas solo muestran su punto débil cuando caen las demás.</p>
    <ul>%s</ul><img class="shot" src="capturas/f3_jefe.png" style="margin-top:3mm"><div class="cap">CONTROL CENTRAL II, en la Factoría del Miedo.</div>'''
       % ''.join('<li>%s</li>' % t for t in tips))
    pg('''<div class="kick">Elige tu nivel</div><h2 style="margin:1.5mm 0 4mm">Dificultad</h2>
    <table><tr><th></th><th>Fácil</th><th>Normal</th><th>HARDCORE</th></tr>
      <tr><td>Vidas / corazones</td><td>5 / 4</td><td>3 / 3</td><td>3 / 2</td></tr>
      <tr><td>Balas enemigas</td><td>1</td><td>2</td><td>2, más rápidas</td></tr>
      <tr><td>Vida de los jefes</td><td>−25 %</td><td>normal</td><td>+25 %</td></tr>
      <tr><td>Aviso de ataque</td><td>1 s</td><td>0,7 s</td><td>0,4 s</td></tr></table>
    <div class="panel" style="margin-top:5mm;border-color:var(--red)"><div class="kick">Secreto</div>
      <p style="margin:1.5mm 0 0">En el título, pulsa <b>abajo, abajo, FIRE</b> (tienes hasta 2 segundos entre pulsaciones). Aparecerá ** MODO INVENCIBLE ** y el marcador pondrá VIDA INV.</p></div>
    <p style="margin-top:4mm;color:var(--dim)">Al acabar verás GAME OVER o MISIÓN CUMPLIDA con tu puntuación, y el juego vuelve al título.</p>
    <img class="shot" src="capturas/titulo_hardcore.png" style="margin-top:2mm"><div class="cap">HARDCORE: solo para comandos de verdad.</div>''')
    rec = ''.join('<tr><td class="mono" style="color:var(--gold)">%d</td><td style="height:9mm"></td><td></td><td></td></tr>' % k for k in range(1, 9))
    pg('''<div class="kick">Para tus partidas</div><h2 style="margin:1.5mm 0 4mm">Tabla de récords</h2>
    <table><tr><th>#</th><th style="width:45%%">Nombre</th><th>Puntos</th><th>Dificultad</th></tr>%s</table>
    <div class="panel" style="margin-top:5mm"><h3>Consejos de supervivencia</h3><ul>
      <li>Plántate con FIRE para limpiar drones en diagonal sin moverte.</li>
      <li>Guarda el pescado para cuando te quede un corazón.</li>
      <li>Los enemigos no te siguen a los fosos, pero tú sí puedes caer: salta con una pulsación nueva cada vez.</li>
      <li>En HARDCORE el aviso de los jefes dura menos de medio segundo: aprende su ritmo.</li></ul></div>''' % rec)
    pg('''<div class="kick">Créditos</div><h2 style="margin:1.5mm 0 5mm">Quién hizo qué</h2>
    %s
    <div style="display:grid;grid-template-columns:52mm 1fr;gap:4mm;margin-top:5mm;align-items:end">
      <img src="assets/zak_foto.jpg" style="width:100%%;border-radius:1.5mm;border:.5mm solid var(--gold)">
      <div><img class="px" src="assets/zak_retrato_pixelart.png" style="width:28mm;border-radius:1mm;margin-bottom:2mm">
      <div class="cap" style="color:var(--txt)"><b>ZAK, el Gato.</b> El de verdad, y su retrato en píxeles.</div></div></div>
    <p style="margin-top:5mm;color:var(--dim)">Un juego de Tony y Claude A.I. para Atari 400/800/XL/XE · 2026.</p>'''
       % ''.join('<div style="margin-bottom:3.2mm"><div class="kick" style="color:var(--dim);font-size:6.5pt">%s</div><div style="font-family:Inter Display;font-weight:900;font-size:12pt;color:var(--gold)">%s</div></div>' % (esc(a), esc(b)) for a, b in CREDITS))
    pg('''<img src="assets/ilustracion.png" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
    <div style="position:absolute;left:0;right:0;bottom:0;height:40mm;background:linear-gradient(transparent,rgba(8,6,16,.95) 45%)"></div>
    <div style="position:absolute;left:10mm;right:10mm;bottom:10mm;text-align:center">
      <div style="font-family:'Inter Display';font-weight:900;font-size:13pt;font-style:italic">Ese día, Zak cogió su fusil.</div>
      <div class="mono" style="font-size:6pt;color:var(--dim);letter-spacing:.14em;margin-top:2mm">GATO. COMANDO. CAOS.</div></div>''', style='padding:0', f=False)
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8"><title>ZAK ATTACK · Instrucciones</title><style>%s</style></head><body>%s</body></html>'
            % (page_css('148mm', '210mm', '10mm', '10mm', '8.5pt', '17pt', '10pt'), ''.join(P)))

open(R + 'atlas.html', 'w').write(atlas())
open(R + 'folleto.html', 'w').write(folleto())
print('html ok')
