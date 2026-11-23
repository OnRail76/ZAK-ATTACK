#!/usr/bin/env python3
"""Página de capturas reales + PDF del atlas (atlas.png + capturas)."""
from PIL import Image, ImageDraw, ImageFont
D = '/home/claude/zak/doc/capturas/'
names = [('title', 'Título'),
         ('f1', 'Fase 1 · Callejón Neón'), ('f1_jefe', 'GRUÑÓN-01'),
         ('f2', 'Fase 2 · Tren Colmillo'), ('f2_jefe', 'LOCOMORRÓN'),
         ('f3', 'Fase 3 · Fundición Omega'), ('f3_jefe', 'EL HORNO'),
         ('f4', 'Fase 4 · Laboratorio Umbral'), ('f4_jefe', 'QUIMERA-9'),
         ('f5', 'Fase 5 · Corazón R.A.T.A.'), ('f5_jefe', 'RATTUS PRIME'), ('final', 'Final')]
W, H = 2400, 3200
im = Image.new('RGB', (W, H), (14, 12, 26)); d = ImageDraw.Draw(im)
fb = ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf', 54)
fm = ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf', 28)
fr = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 26)
d.rectangle((0, 0, W, 200), fill=(8, 6, 16))
d.text((40, 40), 'CAPTURAS REALES DEL EMULADOR', font=fb, fill=(255, 196, 64))
d.text((40, 118), 'atari800 (NTSC, XL 64 KB) ejecutando zakattack.xex · el mismo juego que va en el ATR y en el cartucho',
       font=fr, fill=(150, 150, 175))
for i, (n, t) in enumerate(names):
    x = 60 + (i % 3) * 780; y = 240 + (i // 3) * 740
    s = Image.open(D + n + '.png').resize((720, 540), Image.NEAREST)
    im.paste(s, (x, y)); d.rectangle((x - 2, y - 2, x + 721, y + 541), outline=(92, 70, 160), width=3)
    d.text((x, y + 556), t, font=fm, fill=(255, 196, 64))
im.save('/home/claude/zak/doc/capturas_pagina.png')
a = Image.open('/home/claude/zak/shots/atlas.png').convert('RGB')
a.save('/home/claude/zak/doc/ZAK_ATTACK_atlas_atari8bits.pdf', 'PDF', resolution=200, save_all=True, append_images=[im.convert('RGB')])
print('ok')
