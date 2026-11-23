# ZAK ATTACK · música original (POKEY), en clave de marcha militar y aventura.
# Melodía: canal 1 (8 bits, 64 kHz). Bajo: canales 3+4 enlazados (16 bits, 1,79 MHz).
# Batería: canal 2 (lo comparte con los efectos; un efecto la calla un momento).
# Duraciones en semicorcheas; "tempo" = cuadros por semicorchea (NTSC, 60 Hz).
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def freq(n): return 440.0 * 2 ** ((n - 69) / 12)
def midi(s):
    name, octv = s[:-1], int(s[-1])
    return NAMES.index(name) + 12 * (octv + 1)
MEL0 = 60                       # C4 .. B6 -> índices 1..36
MELTAB = [0] + [max(0, min(255, round(63921 / (2 * freq(MEL0 + i)) - 1))) for i in range(36)]
BAS0 = 30                       # F#1 .. F4 -> índices 1..36
BASTAB = [0] + [round(1789773 / (2 * freq(BAS0 + i)) - 7) for i in range(36)]
DRUM = {'-': 0, 'K': 1, 'S': 2, 'H': 3, 'R': 4}   # bombo, caja, charles, redoble (caja suave)

def seq(txt, base):
    out = []
    for tok in txt.split():
        if tok == '|': continue
        n, d = tok.split(':')
        if n == '-': out.append((0, int(d)))
        else:
            i = midi(n) - base + 1
            assert 1 <= i <= 36, tok
            out.append((i, int(d)))
    return out
def M(t): return seq(t, MEL0)
def B(t): return seq(t, BAS0)
def D(t): return [(DRUM[k], int(d)) for k, d in (tok.split(':') for tok in t.split() if tok != '|')]
def rep(t, n): return ' '.join([t] * n)
def bars(sq): return sum(d for _, d in sq) / 16

# patrones de batería (un compás = 16 semicorcheas)
MARCH = 'K:2 H:2 S:2 H:2 K:2 H:2 S:2 S:1 S:1'
MFILL = 'K:2 H:2 S:2 H:2 K:2 S:1 S:1 R:1 R:1 S:1 S:1'
GALOP = 'K:2 K:1 K:1 S:2 H:2 K:2 K:1 K:1 S:2 S:2'
HEAVY = 'K:4 S:4 K:2 K:2 S:4'
HFILL = 'K:4 S:4 K:2 S:1 S:1 R:1 R:1 S:2'
FAST = 'K:1 K:1 S:2 K:2 S:2 K:1 K:1 S:2 S:1 S:1 S:2'

SONGS = {}
# --- Fase 1 y título: "Callejón" (la menor, marcha heroica)
m1 = ('E5:3 E5:1 A5:4 G5:3 F5:1 E5:4 | D5:3 E5:1 F5:2 D5:2 E5:8 | C5:3 D5:1 E5:4 F5:3 G5:1 A5:4 | G5:3 F5:1 E5:2 D5:2 E5:8 | '
      'A5:3 B5:1 C6:4 B5:3 A5:1 G5:4 | F5:3 G5:1 A5:2 F5:2 E5:8 | D5:3 E5:1 F5:2 A5:2 G#5:4 B5:4 | A5:4 E5:2 C5:2 A4:8')
b1 = ('A2:4 E3:4 A2:4 E3:4 | E2:4 B2:4 E2:4 B2:4 | F2:4 C3:4 F2:4 C3:4 | E2:4 B2:4 E2:4 G#2:4 | '
      'A2:4 E3:4 A2:4 E3:4 | D2:4 A2:4 D2:4 A2:4 | D2:4 A2:4 E2:4 G#2:4 | A2:4 E3:4 A2:8')
d1 = rep(MARCH, 3) + ' ' + MFILL
SONGS['p1'] = (7, M(m1), B(b1), D(rep(d1, 2)))
# --- Fase 2: "Tren" (re menor, al galope)
m2 = ('D5:2 D5:1 D5:1 F5:2 A5:2 D6:6 A5:2 | C6:2 A#5:1 A5:1 G5:4 E5:6 C5:2 | A#5:2 A5:1 G5:1 F5:2 G5:2 A5:6 F5:2 | E5:2 F5:1 G5:1 A5:4 C#5:8 | '
      'D5:2 D5:1 D5:1 F5:2 A5:2 D6:6 E6:2 | F6:2 E6:1 D6:1 C6:4 G5:6 A5:2 | A#5:3 A5:1 G5:3 F5:1 E5:4 G5:4 | F5:2 E5:2 D5:12')
b2 = ('D2:4 A2:4 D2:4 A2:4 | C2:4 G2:4 C2:4 G2:4 | A#1:4 F2:4 A#1:4 F2:4 | A1:4 E2:4 A1:4 C#2:4 | '
      'D2:4 A2:4 D2:4 A2:4 | C2:4 G2:4 C2:4 G2:4 | A#1:4 F2:4 A1:4 E2:4 | D2:4 A2:4 D2:8')
SONGS['p2'] = (6, M(m2), B(b2), D(rep(GALOP, 8)))
# --- Fase 3: "Fundición" (mi menor, marcha pesada)
m3 = ('E5:4 B4:3 E5:1 G5:4 E5:4 | G5:3 F#5:1 E5:4 C5:8 | D5:3 E5:1 F#5:4 A5:4 F#5:4 | B5:6 A5:2 F#5:4 D#5:4 | '
      'E5:4 B4:3 E5:1 G5:4 B5:4 | C6:3 B5:1 A5:4 E5:8 | G5:3 A5:1 G5:4 F#5:3 G5:1 F#5:4 | E5:16')
b3 = ('E2:4 B2:4 E2:4 B2:4 | C2:4 G2:4 C2:4 G2:4 | D2:4 A2:4 D2:4 A2:4 | B1:4 F#2:4 B1:4 D#2:4 | '
      'E2:4 B2:4 E2:4 B2:4 | A1:4 E2:4 A1:4 E2:4 | C2:4 G2:4 B1:4 F#2:4 | E2:4 B1:4 E2:8')
SONGS['p3'] = (8, M(m3), B(b3), D(rep(HEAVY + ' ' + HEAVY + ' ' + HEAVY + ' ' + HFILL, 2)))
# --- Fase 4: "Laboratorio" (do menor, aventura con misterio)
m4 = ('C5:3 D#5:1 G5:4 C6:4 G5:4 | G#5:3 G5:1 F5:4 D#5:8 | F5:3 G5:1 G#5:4 C6:4 G#5:4 | G5:6 F5:2 D5:4 B4:4 | '
      'C5:3 D#5:1 G5:4 C6:3 D6:1 D#6:4 | D6:3 C6:1 A#5:4 G5:8 | G#5:3 G5:1 F5:4 D5:3 D#5:1 B4:4 | C5:16')
b4 = ('C2:4 G2:4 C2:4 G2:4 | G#1:4 D#2:4 G#1:4 D#2:4 | F2:4 C3:4 F2:4 C3:4 | G1:4 D2:4 G1:4 B1:4 | '
      'C2:4 G2:4 C2:4 G2:4 | A#1:4 F2:4 A#1:4 F2:4 | G#1:4 D#2:4 G1:4 B1:4 | C2:4 G2:4 C2:8')
SONGS['p4'] = (7, M(m4), B(b4), D(rep(MARCH, 3) + ' ' + MFILL + ' ' + rep(MARCH, 3) + ' ' + MFILL))
# --- Fase 5: "Corazón R.A.T.A." (si menor, marcha urgente)
m5 = ('B4:2 B4:1 B4:1 D5:2 F#5:2 B5:8 | B5:2 A5:1 G5:1 F#5:2 G5:2 D5:8 | C#5:2 C#5:1 C#5:1 E5:2 A5:2 C#6:8 | C#6:2 B5:1 A#5:1 F#5:4 C#5:8 | '
      'B4:2 B4:1 B4:1 D5:2 F#5:2 B5:8 | E5:2 G5:1 B5:1 E6:4 D6:2 C#6:2 B5:4 | A#5:3 B5:1 C#6:4 F#5:3 A#5:1 C#6:4 | B5:4 F#5:2 D5:2 B4:8')
b5 = ('B1:4 F#2:4 B1:4 F#2:4 | G1:4 D2:4 G1:4 D2:4 | A1:4 E2:4 A1:4 E2:4 | F#1:4 C#2:4 F#1:4 A#1:4 | '
      'B1:4 F#2:4 B1:4 F#2:4 | E2:4 B2:4 E2:4 B2:4 | F#1:4 C#2:4 F#1:4 C#2:4 | B1:4 F#2:4 B1:8')
SONGS['p5'] = (6, M(m5), B(b5), D(rep(FAST, 7) + ' ' + MFILL))
# --- Jefe (mi menor, ostinato tenso)
mb = ('E5:2 E5:1 E5:1 G5:2 E5:2 F5:2 F5:1 F5:1 A5:2 F5:2 | G5:2 G5:1 G5:1 A#5:2 G5:2 F#5:4 D#5:4 | '
      'E5:2 E5:1 E5:1 G5:2 E5:2 F5:2 F5:1 F5:1 A5:2 F5:2 | B5:4 A#5:4 G5:4 D#5:4')
bb = ('E2:2 E3:2 E2:2 E3:2 F2:2 F3:2 F2:2 F3:2 | G2:2 G3:2 G2:2 G3:2 F#2:2 F#3:2 D#2:2 D#3:2 | '
      'E2:2 E3:2 E2:2 E3:2 F2:2 F3:2 F2:2 F3:2 | B1:2 B2:2 B1:2 B2:2 D#2:2 D#3:2 B1:2 B2:2')
SONGS['boss'] = (6, M(mb), B(bb), D(rep('K:2 S:2 K:2 S:2 K:2 S:2 K:1 S:1 S:1 S:1', 4)))
# --- Fanfarrias (no se repiten)
SONGS['clear'] = (6, M('G4:2 C5:1 C5:1 C5:2 E5:2 G5:4 E5:2 G5:2 | C6:12 -:24'),
                  B('C2:2 C2:2 C2:2 G2:2 C3:4 G2:2 C3:2 | C2:12 -:24'),
                  D('K:2 S:1 S:1 S:2 S:2 K:4 S:2 S:2 | K:2 R:1 R:1 R:1 R:1 R:1 R:1 S:4 -:24'))
SONGS['over'] = (8, M('E5:4 D#5:4 D5:4 C#5:4 | C5:12 -:24'), B('A2:4 G#2:4 G2:4 F#2:4 | F2:12 -:24'),
                 D('K:4 -:4 K:4 -:4 | K:4 -:16 -:16'))

if __name__ == '__main__':
    for k, v in SONGS.items():
        print(k, 'melodía %.1f compases, bajo %.1f, batería %.1f' % (bars(v[1]), bars(v[2]), bars(v[3])))
