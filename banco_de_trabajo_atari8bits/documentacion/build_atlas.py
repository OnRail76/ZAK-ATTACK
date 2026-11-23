# -*- coding: utf-8 -*-
"""Atlas visual de Vórtice 5 (A4 apaisado) -> atlas.html (luego make_pdf.py)."""
import sys, os
sys.path.insert(0, sys.argv[1])          # carpeta gfx del juego
from tiles import SECTORS as TS, PF3
from sprites import SHIP_COLORS, ENEMIES
from bosses import BOSS_DEF
from pal import atari_rgb
from common import *

def rgb(c): r, g, b = atari_rgb(c); return '#%02x%02x%02x' % (r, g, b)
def hx(c): return '$%02X' % c
def reg(name, c): return f'<div class="reg"><i style="background:{rgb(c)}"></i><b>{name}</b><span>{hx(c)}</span></div>'
EN = {e[0]: e for e in ENEMIES}
def en_key(slug):
    import unicodedata
    for e in ENEMIES:
        s = unicodedata.normalize('NFKD', e[0]).encode('ascii', 'ignore').decode().lower().replace(' ', '_')
        if s == slug: return e
CHARS = [54, 79, 68, 74, 77]
BCH = [(59, 60), (58, 85), (84, 1), (63, 66), (102, 77)]

css = '''
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box}
:root{--bg:#0b0d14;--panel:#121623;--line:#2a3147;--fg:#e9ebf2;--muted:#959cb2;--amber:#f2b84b;--red:#f07a6a}
html,body{margin:0;background:var(--bg);color:var(--fg);font-family:Inter,sans-serif;font-size:10.5pt;line-height:1.5;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:14mm 16mm 12mm;position:relative;overflow:hidden;page-break-after:always;display:flex;flex-direction:column;gap:7mm}
.page:last-child{page-break-after:auto}
h1,h2,h3{font-family:"Inter Display",Inter,sans-serif;margin:0;letter-spacing:.01em}
h2{font-size:24pt;font-weight:800;line-height:1.05}
h3{font-size:8.5pt;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
p{margin:0}
.eyebrow{font:600 8pt "DejaVu Sans Mono",monospace;letter-spacing:.16em;text-transform:uppercase;color:var(--amber)}
.mono{font-family:"DejaVu Sans Mono",monospace}
.muted{color:var(--muted)}
.foot{position:absolute;left:16mm;right:16mm;bottom:6mm;display:flex;justify-content:space-between;font:7pt "DejaVu Sans Mono",monospace;color:#6a7187;letter-spacing:.06em}
img.px{image-rendering:pixelated;display:block}
.head{display:flex;align-items:baseline;gap:6mm;border-bottom:2px solid var(--c,var(--line));padding-bottom:4mm}
.head .sub{color:var(--muted);font-size:11pt}
.reg{display:inline-grid;grid-template-columns:6mm auto;grid-template-rows:auto auto;column-gap:2mm;align-items:center;border:1px solid var(--line);border-radius:2mm;padding:1.4mm 2.6mm 1.4mm 1.4mm;margin:0 1.6mm 1.6mm 0}
.reg i{grid-row:span 2;width:6mm;height:6mm;border-radius:1mm;box-shadow:inset 0 0 0 .3mm rgba(255,255,255,.18)}
.reg b{font:600 6.5pt "DejaVu Sans Mono",monospace;color:var(--muted);letter-spacing:.06em}
.reg span{font:600 8.5pt "DejaVu Sans Mono",monospace}
.card{display:flex;flex-direction:column;gap:1.6mm}
.card .pix{background:#000;border:1px solid var(--line);border-radius:1.5mm;display:flex;gap:4mm;align-items:center;justify-content:center;padding:3mm;min-height:24mm}
.card .name{font:700 9.5pt "Inter Display",sans-serif}
.card .meta{font:7.5pt "DejaVu Sans Mono",monospace;color:var(--muted)}
.cards{display:grid;gap:4mm}
.shot{border:1px solid var(--line);border-radius:1.5mm;overflow:hidden;background:#000}
.shot img{width:100%;display:block;image-rendering:pixelated}
dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:1.4mm 5mm;font-size:9.5pt}
dt{font:600 7pt "DejaVu Sans Mono",monospace;color:var(--muted);letter-spacing:.08em;padding-top:.8mm}
dd{margin:0}
.rules{list-style:none;margin:0;padding:0;display:grid;gap:1.6mm}
.rules li{display:grid;grid-template-columns:25mm 1fr;gap:3mm;border-top:1px solid var(--line);padding-top:1.6mm;font-size:8.8pt;line-height:1.42}
.rules li span:first-child{font:600 7.5pt "DejaVu Sans Mono",monospace;color:var(--amber);letter-spacing:.06em;padding-top:.6mm}
table{border-collapse:collapse;width:100%;font-size:9pt}
th,td{text-align:left;padding:1.6mm 2.4mm;border-bottom:1px solid var(--line)}
th{font:600 7pt "DejaVu Sans Mono",monospace;color:var(--muted);letter-spacing:.08em;text-transform:uppercase}
td.n{font-family:"DejaVu Sans Mono",monospace;text-align:right}
.pill{font:600 6.5pt "DejaVu Sans Mono",monospace;padding:.4mm 2mm;border-radius:9mm;border:1px solid currentColor;color:#6fd39a}
.credit{border-left:3px solid var(--amber);padding:2mm 0 2mm 5mm;font-size:11pt;max-width:150mm}
'''

def foot(n, label):
    return f'<div class="foot"><span>VÓRTICE 5 · ATLAS VISUAL · {label}</span><span>{CREDITS}</span><span>{n:02d}</span></div>'

pages = []
P = pages.append
# 1 · portada
P(f'''<section class="page" style="padding:0;background:radial-gradient(120% 90% at 78% 40%,#1b1030 0%,#0b0d14 60%)">
<div style="position:absolute;right:14mm;top:22mm;width:158mm" class="shot"><img src="img/full_t_60.png"></div>
<div style="position:absolute;left:16mm;top:20mm;width:110mm;display:flex;flex-direction:column;gap:6mm">
 <span class="eyebrow">Atlas visual</span>
 <span class="mono muted" style="font-size:8pt;margin-top:-4mm">{MACHINE}</span>
 <h1 style="font-size:62pt;font-weight:800;line-height:.92">VÓRTICE<br><span style="color:var(--red)">5</span></h1>
 <div style="font:600 20pt 'Inter Display',sans-serif;color:var(--amber);letter-spacing:.02em">{SUBTITLE}</div>
 <div style="display:inline-block;align-self:flex-start;border:1.5px solid var(--fg);border-radius:2mm;padding:2mm 4mm;font:700 11pt 'Inter Display',sans-serif;letter-spacing:.04em">{DESIGN}</div>
 <p style="font-size:12pt;font-style:italic;color:#cfd3e0;max-width:100mm">{TAGLINE}</p>
</div>
<div style="position:absolute;left:16mm;right:16mm;bottom:14mm;display:flex;justify-content:space-between;align-items:end;gap:10mm">
 <p class="credit">{CREDITS}</p>
 <span class="mono muted" style="font-size:8pt;white-space:nowrap">{SIGN}</span>
</div></section>''')

# 2 · historia + créditos + índice
P(f'''<section class="page">
<div class="head"><span class="eyebrow">La historia</span><h2>El Ordenador Estelar se ha vuelto loco</h2></div>
<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:12mm;flex:1">
 <div style="display:flex;flex-direction:column;gap:5mm;font-size:14pt;line-height:1.55">
  {''.join(f'<p>{s}</p>' for s in STORY)}
  <p style="font:800 30pt 'Inter Display',sans-serif;color:var(--red);letter-spacing:.02em">{STORY_PUNCH}</p>
  <p style="font-size:10.5pt;font-style:italic;color:var(--muted);margin-top:4mm">{TAGLINE}</p>
 </div>
 <div style="display:flex;flex-direction:column;gap:5mm">
  <div class="shot"><img src="img/full_b5_39500.png"></div>
  <p class="credit" style="font-size:10pt">{CREDITS}</p>
  <dl><dt>NAVE</dt><dd>Vórtice 5, caza espacial</dd><dt>ENEMIGO</dt><dd>Leviatán V, el Ordenador Estelar</dd>
  <dt>OBJETIVO</dt><dd>Cinco sectores hasta el Corazón de Acero</dd><dt>DISEÑO</dt><dd>{DESIGN}</dd></dl>
 </div>
</div>{foot(2, 'HISTORIA')}</section>''')

# 3 · reglas
P(f'''<section class="page">
<div class="head"><span class="eyebrow">Cómo cabe en un Atari</span><h2>Reglas del hardware y {DESIGN}</h2></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12mm">
<div><h3 style="margin-bottom:3mm">Reglas del hardware</h3><ul class="rules">
<li><span>PANTALLA</span><span>ANTIC 4 con playfield estrecho de 32 columnas: 128 × 192 píxeles. Scroll fino con VSCROL y grueso moviendo los LMS de la display list. Marcador en una línea ANTIC 2 aparte.</span></li>
<li><span>COLOR</span><span>4 colores de escenario por fase: COLBK y COLPF0–2. Los jefes tienen su propia paleta.</span></li>
<li><span>NAVE</span><span>P0 + P1 superpuestos en multicolor: gris, azul y su mezcla. 3 colores en 8 píxeles.</span></li>
<li><span>AIRE</span><span>P2 y P3 reutilizados por bandas con DLI (posición, color y anchura). Hasta 8 enemigos en pantalla, 2 por franja.</span></li>
<li><span>DISPAROS</span><span>Quinto player: los 4 misiles salen en COLPF3 = {hx(PF3)}. Disparos y balas comparten los 4 misiles, ordenados por altura.</span></li>
<li><span>TURNOS</span><span>Si en una franja no cabe todo, lo que no se dibujó va primero en el cuadro siguiente: nada queda invisible dos cuadros seguidos.</span></li>
<li><span>SUELO</span><span>Torretas y objetivos son caracteres. Destruir uno es escribir 8 bytes en pantalla y deja su cráter. No gastan sprites.</span></li>
<li><span>JEFES</span><span>112 × 56 píxeles en caracteres, con uno o dos juegos propios; una DLI cambia CHBASE a mitad. PF2 marca los puntos débiles.</span></li>
<li><span>PRIOR</span><span class="mono">$31 · multicolor $20 + quinto player $10 + players delante $01</span></li>
</ul></div>
<div><h3 style="margin-bottom:3mm">{DESIGN}</h3><ul class="rules">
<li><span>ESPÍRITU</span><span>Más Star Force y Xevious que Xenon 2: un shoot 'em up vertical directo, de reflejos, hecho a la medida de la máquina.</span></li>
<li><span>DISPARO</span><span>Uno solo, el Pulso. Daña a lo que vuela y a lo que hay en el suelo.</span></li>
<li><span>CÁPSULA P</span><span>Nivel I: un disparo. II: dos en paralelo. III: dos con más cadencia. Al morir vuelves a I. Con nivel III da 1.000 puntos.</span></li>
<li><span>POR FASE</span><span>2 enemigos aéreos, 2 objetivos de suelo y un jefe con 3 a 5 puntos débiles.</span></li>
<li><span>DIFICULTAD</span><span>Fácil, Normal y Hardcore: vidas, velocidad de las balas, cadencia y margen de seguridad.</span></li>
<li><span>JUSTICIA</span><span>Ninguna bala nace pegada a la nave; tope de balas a la vez según la dificultad.</span></li>
<li><span>MÚSICA</span><span>Canciones de Tony C. adaptadas a POKEY, en bucle y sin cortes: nada se para en seco.</span></li>
<li><span>FORMATOS</span><span>XEX, disco ATR autoarrancable y cartucho AtariMax de 128 KB.</span></li>
</ul></div></div>{foot(3, 'REGLAS')}</section>''')

# 4 · la nave
P(f'''<section class="page" style="--c:#8fb0ff">
<div class="head"><span class="eyebrow">Nave del jugador</span><h2>VÓRTICE 5</h2><span class="sub">8 × 15 líneas · P0 + P1 superpuestos</span></div>
<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:12mm">
 <div><h3 style="margin-bottom:3mm">Frames</h3><div class="cards" style="grid-template-columns:repeat(4,1fr)">
 {''.join(f'<div class="card"><div class="pix" style="min-height:44mm"><img class="px" src="img/ship_{k}.png" style="width:22mm"></div><div class="name">{n}</div><div class="meta">P0 {hx(SHIP_COLORS["P0"])} · P1 {hx(SHIP_COLORS["P1"])}</div></div>' for k, n in (('centro','Centro'),('izquierda','Inclina izq.'),('derecha','Inclina der.'),('motor_b','Llama B')))}
 </div>
 <h3 style="margin:7mm 0 3mm">Cómo se monta</h3><div class="cards" style="grid-template-columns:repeat(3,1fr)">
 <div class="card"><div class="pix"><img class="px" src="img/ship_p0.png" style="width:16mm"></div><div class="name">P0 solo</div><div class="meta">{hx(SHIP_COLORS["P0"])}</div></div>
 <div class="card"><div class="pix"><img class="px" src="img/ship_p1.png" style="width:16mm"></div><div class="name">P1 solo</div><div class="meta">{hx(SHIP_COLORS["P1"])}</div></div>
 <div class="card"><div class="pix"><img class="px" src="img/ship_centro.png" style="width:16mm"></div><div class="name">Resultado</div><div class="meta">OR = {hx(SHIP_COLORS["P0"]|SHIP_COLORS["P1"])}</div></div>
 </div></div>
 <div style="display:flex;flex-direction:column;gap:5mm">
 <div class="shot"><img src="img/game_s1_3100.png"></div>
 <p class="muted" style="font-size:9.5pt">El tercer color no se elige: es el OR de los dos registros. Por eso la cabina sale celeste sin gastar otro player. La nave solo se redibuja cuando cambia de posición o de frame.</p>
 </div>
</div>{foot(4, 'NAVE')}</section>''')

# sectores y jefes
for k, S in enumerate(SECTORS):
    t = TS[k]; n = S['n']; bd = BOSS_DEF[k]; pal = bd[3]
    cards_air = ''
    for slug, name, role, pts in S['air']:
        e = en_key(slug); wd = 'doble ancho · ' if e[4] == 'D' else ''
        w = 26 if e[4] == 'D' else 13
        cards_air += f'''<div class="card"><div class="pix" style="background:{rgb(t['BG'])}"><img class="px" src="img/en_{slug}_0.png" style="width:{w}mm"><img class="px" src="img/en_{slug}_1.png" style="width:{w}mm"></div>
        <div class="name">{name}</div><div class="meta">{hx(e[3])} · {wd}{role}</div></div>'''
    gl = [(s, nm) for s, nm, *_ in S['ground']] + S.get('extra_ground', []) + [(c, CRATER_NAMES[c]) for c in S['craters']]
    cards_g = ''.join(f'<div class="card"><div class="pix" style="padding:2mm;min-height:0"><img class="px" src="img/tile{n}_{s}.png" style="width:15mm"></div><div class="meta" style="color:var(--fg)">{nm}</div></div>' for s, nm in gl)
    P(f'''<section class="page" style="--c:{rgb(t['PF2'])}">
<div class="head"><span class="eyebrow">Sector 0{n}</span><h2>{S['name'].upper()}</h2><span class="sub">{S['sub']}</span></div>
<div style="display:grid;grid-template-columns:118mm 1fr;gap:9mm;flex:1;min-height:0">
 <div class="shot" style="align-self:start"><img src="img/game_{S['shot']}.png"></div>
 <div style="display:flex;flex-direction:column;gap:5mm;min-width:0">
  <div><h3 style="margin-bottom:2.5mm">Registros del escenario</h3>{reg('COLBK',t['BG'])}{reg('COLPF0',t['PF0'])}{reg('COLPF1',t['PF1'])}{reg('COLPF2',t['PF2'])}{reg('COLPF3',PF3)}</div>
  <div><h3 style="margin-bottom:2.5mm">En el aire · P2 / P3</h3><div class="cards" style="grid-template-columns:1fr 1fr">{cards_air}</div></div>
  <div><h3 style="margin-bottom:2.5mm">En el suelo · tiles de 16 × 16</h3><div class="cards" style="grid-template-columns:repeat(5,1fr);gap:3mm">{cards_g}</div></div>
  <p class="muted" style="font-size:8.5pt">Juego de caracteres del sector: {CHARS[k]} de 128. Mapa de 150 filas de metatiles de 16 × 16 (4 × 2 caracteres).</p>
 </div>
</div>{foot(5 + 2 * k, 'SECTOR %d' % n)}</section>''')
    name, sub, wps, wdesc = S['boss']
    a, b = BCH[k]
    js = f'{a} + {b} caracteres (dos juegos; una DLI cambia CHBASE)' if b > 1 else f'{a} caracteres (un juego)'
    P(f'''<section class="page" style="--c:{rgb(pal['PF2'])}">
<div class="head"><span class="eyebrow">Jefe del sector 0{n}</span><h2>{name}</h2><span class="sub">{sub}</span></div>
<div style="display:grid;grid-template-columns:1fr 112mm;gap:9mm;flex:1;min-height:0">
 <div style="display:flex;flex-direction:column;gap:5mm">
  <div class="shot" style="padding:5mm;background:{rgb(pal['BG'])}"><img class="px" src="img/boss{n}.png" style="width:100%"></div>
  <div style="display:grid;grid-template-columns:1fr 1.25fr;gap:6mm;align-items:start">
   <div class="shot" style="padding:3mm;background:{rgb(pal['BG'])}"><img class="px" src="img/boss{n}_hit.png" style="width:100%"></div>
   <dl><dt>TAMAÑO</dt><dd class="mono">112 × 56 px · 28 × 7 caracteres</dd>
   <dt>CARACTERES</dt><dd>{js}</dd>
   <dt>PUNTOS DÉBILES</dt><dd>{wps}. {wdesc} El núcleo solo se puede dañar cuando caen los demás.</dd>
   <dt>IMPACTO</dt><dd>PF2 parpadea en blanco ($0E), como en la imagen de la izquierda.</dd>
   <dt>COLORES</dt><dd>{reg('PF0',pal['PF0'])}{reg('PF1',pal['PF1'])}{reg('PF2',pal['PF2'])}</dd></dl>
  </div>
 </div>
 <div class="shot" style="align-self:start"><img src="img/game_{S['boss_shot']}.png"></div>
</div>{foot(6 + 2 * k, 'JEFE %d' % n)}</section>''')

# comunes + música
P(f'''<section class="page">
<div class="head"><span class="eyebrow">Comunes y sonido</span><h2>Explosión, cápsula, disparos y música</h2></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12mm">
 <div style="display:flex;flex-direction:column;gap:5mm">
  <div class="cards" style="grid-template-columns:repeat(3,1fr)">
   <div class="card"><div class="pix">{''.join(f'<img class="px" src="img/en_explosion_{i}.png" style="width:8mm">' for i in range(4))}</div><div class="name">Explosión</div><div class="meta">4 frames · en el player del enemigo</div></div>
   <div class="card"><div class="pix"><img class="px" src="img/en_capsula_p_0.png" style="width:12mm"></div><div class="name">Cápsula P</div><div class="meta">$0E · sube 1 nivel</div></div>
   <div class="card"><div class="pix"><div style="display:flex;gap:3mm"><i style="width:1.6mm;height:9mm;background:{rgb(PF3)}"></i><i style="width:1.6mm;height:9mm;background:{rgb(PF3)}"></i><i style="width:3mm;height:3mm;background:{rgb(PF3)};margin-left:6mm;align-self:center"></i></div></div><div class="name">Pulso y bala</div><div class="meta">COLPF3 {hx(PF3)} · 1×6 y 2×2</div></div>
  </div>
  <h3>Pantallas</h3>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3mm">
   <div class="shot"><img src="img/full_t_dif2.png"></div><div class="shot"><img src="img/full_go_1200.png"></div><div class="shot"><img src="img/full_v_44500.png"></div>
  </div>
  <p class="muted" style="font-size:8.5pt">Título con selector de dificultad, GAME OVER y victoria.</p>
 </div>
 <div><h3 style="margin-bottom:3mm">Música de Tony C. en POKEY</h3><ul class="rules">
  <li><span>TÍTULO</span><span>«Titulo»: bucle de 12 compases, ~141 ppm, re menor. Dos voces de 16 bits.</span></li>
  <li><span>FASES</span><span>«Heart of Steel»: bucle de 32 compases, ~146 ppm, re menor. Bajo de 16 bits y melodía de 8 bits; los efectos van a su propio canal.</span></li>
  <li><span>JEFES</span><span>Dron arcade: barrido de tono sacado del sonido de ambiente aportado por Tony, más agudo y rápido.</span></li>
  <li><span>GAME OVER</span><span>Su tema de fin de partida, una vez, apagándose.</span></li>
  <li><span>CAMBIOS</span><span>Nunca en seco: los bucles cierran en el acorde que lleva al principio y cada cambio de pista funde la anterior.</span></li>
 </ul></div>
</div>{foot(15, 'COMUNES')}</section>''')

# presupuesto
rows = [('Charset sector 1', 54, 128), ('Charset sector 2', 79, 128), ('Charset sector 3', 68, 128), ('Charset sector 4', 74, 128), ('Charset sector 5', 77, 128),
        ('GARRA-9 (juegos A + B)', 60, 128), ('MADRE PÓLIPO', 85, 128), ('HORNO OMEGA', 84, 128), ('EL PRISMARCA', 66, 128), ('LEVIATÁN V', 102, 128),
        ('Enemigos en pantalla', 8, 8), ('Sprites por franja', 2, 2), ('Balas enemigas (Hardcore)', 8, 8)]
trs = ''.join(f'<tr><td>{a}</td><td class="n">{u}</td><td class="n">{l}</td><td><span class="pill">cabe</span></td></tr>' for a, u, l in rows)
perf = [('Sector 1', '90 %', '97 %'), ('Sector 2', '99 %', '99 %'), ('Sector 3', '100 %', '99 %'), ('Sector 4', '88 %', '93 %'), ('Sector 5', '87 %', '90 %')]
trp = ''.join(f'<tr><td>{a}</td><td class="n">{b}</td><td class="n">{c}</td></tr>' for a, b, c in perf)
P(f'''<section class="page">
<div class="head"><span class="eyebrow">Presupuesto comprobado</span><h2>Lo que ocupa y lo que corre</h2></div>
<div style="display:grid;grid-template-columns:1.1fr 1fr;gap:12mm">
 <div><h3 style="margin-bottom:2mm">Límites</h3><table><thead><tr><th>Comprobación</th><th style="text-align:right">Usado</th><th style="text-align:right">Límite</th><th>Estado</th></tr></thead><tbody>{trs}</tbody></table></div>
 <div style="display:flex;flex-direction:column;gap:6mm">
  <div><h3 style="margin-bottom:2mm">Velocidad media en Normal (100 % = 60 cuadros/s)</h3><table><thead><tr><th>Tramo</th><th style="text-align:right">Fase</th><th style="text-align:right">Jefe</th></tr></thead><tbody>{trp}</tbody></table></div>
  <div><h3 style="margin-bottom:2mm">Memoria</h3><dl>
   <dt>$2000–$9FFF</dt><dd>Código y datos (XEX de 31,7 KB)</dd>
   <dt>$A000–$AFFF</dt><dd>Charsets de fase y jefe, anillo de scroll de 32 filas</dd>
   <dt>$B000–$B7FF</dt><dd>PMG de una línea; el hueco de $B000 guarda tablas de trabajo</dd>
   <dt>$B800–$BFFF</dt><dd>Display lists, marcador, tablas DLI y pantalla de títulos</dd></dl></div>
  <p class="muted" style="font-size:8.5pt">Medido con partidas completas en un emulador sin pantalla, en las tres dificultades.</p>
 </div>
</div>{foot(16, 'PRESUPUESTO')}</section>''')

# contraportada
P(f'''<section class="page" style="justify-content:center;align-items:center;text-align:center;gap:8mm;background:radial-gradient(90% 80% at 50% 40%,#2a0d14 0%,#0b0d14 70%)">
<span class="eyebrow">{MACHINE}</span>
<h1 style="font-size:46pt;font-weight:800">VÓRTICE <span style="color:var(--red)">5</span></h1>
<div style="font:600 16pt 'Inter Display',sans-serif;color:var(--amber)">{SUBTITLE} · {DESIGN}</div>
<p style="max-width:190mm;font-size:13pt;font-style:italic;color:#cfd3e0">{TAGLINE}</p>
<p style="max-width:170mm;font-size:12pt">{CREDITS}</p>
<span class="mono muted" style="font-size:9pt">{SIGN}</span>
</section>''')

html = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Vórtice 5 · Atlas visual</title><style>{css}</style></head><body>{"".join(pages)}</body></html>'
open('atlas.html', 'w').write(html)
print('páginas', len(pages))
