#!/usr/bin/env python3
"""Genera zakattack.atr (disco autoarrancable) y zakattack.car (AtariMax 128 KB) desde build/main.bin."""
import struct, sys
main = open('build/main.bin', 'rb').read()
assert len(main) <= 0x8000 - 0x0
# ---------------- ATR: arranque directo sin DOS
LOAD = 0x1FF6
body = bytes([0x4C, 0x00, 0x20, 0x60])          # $1FFC: JMP $2000 ; $1FFF: RTS (DOSINI)
img = bytearray(6) + body + main
nsec = (len(img) + 127) // 128
assert nsec <= 255
img[0] = 0; img[1] = nsec; img[2:4] = struct.pack('<H', LOAD); img[4:6] = struct.pack('<H', 0x1FFF)
img += bytes(nsec * 128 - len(img))
disk = img + bytes(720 * 128 - len(img))
par = len(disk) // 16
hdr = struct.pack('<HHHB', 0x0296, par & 0xFFFF, 128, par >> 16) + bytes(9)
open('build/zakattack.atr', 'wb').write(hdr + disk)
print('atr: %d sectores de arranque' % nsec)
# ---------------- CAR: AtariMax 128 KB (tipo 41)
bank0 = open('build/cart0.bin', 'rb').read()
assert len(bank0) == 0x2000
payload = main + b'\xff' * (4 * 0x2000 - len(main))
assert len(main) <= 4 * 0x2000
data = bank0 + payload + b'\xff' * (11 * 0x2000)
assert len(data) == 128 * 1024
chk = sum(data) & 0xFFFFFFFF
open('build/zakattack.car', 'wb').write(b'CART' + struct.pack('>II', 41, chk) + bytes(4) + data)
print('car: AtariMax 128 KB, checksum %08X' % chk)
