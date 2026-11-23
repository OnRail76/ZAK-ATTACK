# -*- coding: utf-8 -*-
"""Textos y datos compartidos por el atlas y el manual de Vórtice 5."""

TITLE = 'VÓRTICE 5'
SUBTITLE = 'Corazón de Acero'
DESIGN = 'Diseño V2: El Star Force Europeo'
CREDITS = ('Diseño, nombres, fases, gráficos y música por Tony C., '
           'adaptados a los límites de la máquina con asistencia IA.')
TAGLINE = ('Una idea de hace décadas, por fin ve la luz de la manera más sorprendente, '
           'en la máquina que nadie esperaba.')
STORY = [
    'Leviatán V, el Ordenador Estelar, se ha vuelto loco. Sus fuerzas robotizadas y sus '
    'organismos cyborg amenazan la paz de todo el universo.',
    'Solo un caza espacial como el Vórtice 5 puede tratar de parar ese ejército de asesinos '
    'computerizados y llegar al Corazón de Acero. Y resulta que el piloto…',
]
STORY_PUNCH = '…ES USTED.'
SIGN = '2026 · Tony y Claude I.A.'
MACHINE = 'Atari 400 / 800 / XL / XE · 48 KB · NTSC'

SECTORS = [
    dict(n=1, name='Cementerio de Titanes', sub='Chatarra, cascos partidos y vacío',
         shot='s1_3900', boss_shot='b1_6400',
         air=[('aguja', 'Aguja', 'Pica en columna', 100), ('carronero', 'Carroñero', 'Curva, dispara y huye', 200)],
         ground=[('torreta', 'Centinela', 'Torreta que apunta', 300), ('contenedor', 'Contenedor', 'Suelta una cápsula P', 500)],
         craters=['crater'],
         boss=('GARRA-9', 'Recolector de restos', 3, 'Dos articulaciones y el ojo-núcleo.'),
         tip='Los contenedores sueltan cápsulas P: revienta todos los que puedas al principio.'),
    dict(n=2, name='Arrecife de Ácido', sub='Coral técnico, membranas y ácido',
         shot='s2_9800', boss_shot='b2_14000',
         air=[('zangano', 'Zángano', 'Zigzag de cuatro giros', 100), ('lapa', 'Lapa', 'Salta desde el muro', 200)],
         ground=[('polipo_abierto', 'Pólipo', 'Solo es vulnerable abierto', 500), ('bolsa_acida', 'Bolsa ácida', 'Estalla en cruz', 300)],
         extra_ground=[('polipo_cerrado', 'Pólipo cerrado')],
         craters=['crater', 'crater_redondo'],
         boss=('MADRE PÓLIPO', 'Órgano criogénico', 3, 'Dos bocas laterales y la boca central.'),
         tip='No gastes disparos en un pólipo cerrado: espera a que se abra.'),
    dict(n=3, name='Fundición Orbital', sub='Calderas, cintas y metal fundido',
         shot='s3_18600', boss_shot='b3_22400',
         air=[('aguja_termica', 'Aguja térmica', 'Taladro en picado', 200), ('cazador_delta', 'Cazador delta', 'Entra desde abajo', 300)],
         ground=[('torreta_cuadrada', 'Centinela térmico', 'Torreta que apunta', 300), ('surtidor_activo', 'Surtidor', 'Activo, lanza ráfagas', 500)],
         extra_ground=[('surtidor', 'Surtidor en reposo')],
         craters=['crater'],
         boss=('HORNO OMEGA', 'Reactor de asedio', 5, 'Cuatro válvulas y la boca de fuego.'),
         tip='El cazador delta sube desde abajo: no te pegues al borde inferior.'),
    dict(n=4, name='Santuario Prisma', sub='Cristal facetado, espejos y láser',
         shot='s4_25600', boss_shot='b4_31200',
         air=[('orbe_espejo', 'Orbe espejo', 'Te devuelve el disparo', 300), ('zangano_prisma', 'Zángano prisma', 'Bandada en V', 200)],
         ground=[('cristal_torreta', 'Centinela prisma', 'Torreta que apunta', 300), ('emisor_laser', 'Emisor láser', 'Ráfagas hacia abajo', 500)],
         craters=['crater', 'crater_redondo', 'crater_suelo'],
         boss=('EL PRISMARCA', 'Guardián de refracción', 5, 'Nodos de las alas, nodos superiores y el prisma central.'),
         tip='Cada impacto en un orbe espejo puede volver hacia ti: dispárale desde un lado.'),
    dict(n=5, name='Corazón de Acero', sub='Carne metálica, latidos y núcleo',
         shot='s5_35500', boss_shot='b5_39500',
         air=[('destructor', 'Destructor', 'Pesado, bloquea el carril', 1000), ('mina_nerviosa', 'Mina nerviosa', 'Estalla en cruz', 300)],
         ground=[('torreta_parasita', 'Centinela parásito', 'Torreta que apunta', 300), ('bomba_bio', 'Bomba biológica', 'Cruz al morir y cápsula P', 2000)],
         craters=['crater', 'crater_redondo', 'crater_suelo'],
         boss=('LEVIATÁN V', 'El Ordenador Estelar', 3, 'Dos nodos y el ojo central.'),
         tip='Las minas estallan en cruz al morir: no las revientes cuando las tengas encima.'),
]

CRATER_NAMES = {'crater': 'Cráter con placa', 'crater_redondo': 'Cráter redondo', 'crater_suelo': 'Cráter sobre el suelo'}

FONTS = '''
@font-face{font-family:"Disp";src:local("Inter Display ExtraBold"),local("InterDisplay-ExtraBold");font-weight:800}
@font-face{font-family:"Disp";src:local("Inter Display SemiBold"),local("InterDisplay-SemiBold");font-weight:600}
'''
