; =====================================================================
;  ZAK ATTACK · run and gun para Atari 400/800/XL/XE (48 KB)
;  Por Tony y Claude A.I.
;  ANTIC 4 con scroll fino horizontal, Zak = P0+P1, enemigos = P2/P3,
;  balas = misiles (quinto player, color PF3). Jefes de caracteres.
; =====================================================================
        .include "hw.inc"
HSCROL  = $D404
DLISTL_ = $D402
SKSTAT  = $D20F
STIMER  = $D209
SETVBV_ = $E45C

SCR     = $A000             ; 22 filas x 128 (anillo de 64 columnas duplicado)
DL      = $AC00
HUD     = $AD00
TXT     = $B000             ; pantallas de texto
TDL     = $B400             ; display list de pantallas de texto
PMG     = $B800
MIS     = PMG+$300
PL0     = PMG+$400
PL1     = PMG+$500
PL2     = PMG+$600
PL3     = PMG+$700

PFTOP   = 40                ; línea PMG de la fila 0 del campo de juego
BOOMTOP = PFTOP+64          ; explosiones de jefe: filas 8 a 16 (4 franjas)
HPOFS   = 36                ; HPOS = (x - camx) + 36 (medido en atari800)
VIS0    = 12                ; primer píxel visible = camx + 12
NROWS   = 22
GROUNDY = 136

; ---------------------------------------------------------------------
        .zeropage
zp_start:
frame:  .res 1
vbflag: .res 1
tmp:    .res 4
ptr:    .res 2
ptr2:   .res 2
ptr3:   .res 2
tx:     .res 2              ; consulta de tile: x mundo
ty:     .res 1
phase:  .res 1
camx:   .res 2
camxmax:.res 2
coarse: .res 2
drawn:  .res 2              ; siguiente columna del mundo por dibujar
hsc:    .res 1
lmsdirty:.res 1
haz_t:  .res 1
plat_t: .res 1
solid_t:.res 1
evptr:  .res 2
seqp:   .res 2
collo_p:.res 2
colhi_p:.res 2
bgp:    .res 2
stick:  .res 1
trig:   .res 1
oldtrig:.res 1
; Zak
px:     .res 2
py:     .res 1
pysub:  .res 1
vy:     .res 1
onground:.res 1
pdir:   .res 1
pframe: .res 1
panim:  .res 1
crouch: .res 1
pstate: .res 1              ; 0 vivo, 1 muriendo
ptimer: .res 1
inv:    .res 1
firecd: .res 1
uplatch:.res 1
hp:     .res 1
lives:  .res 1
score:  .res 3
hudflag:.res 1
oldpy:  .res 1
aimup:  .res 1
; sonido (propios de la VBI)
mus_on: .res 1
mptr:   .res 2
mstart: .res 2
mtime:  .res 1
mvol:   .res 1
bptr:   .res 2
bstart: .res 2
btime:  .res 1
bvol:   .res 1
dptr:   .res 2
dstart: .res 2
dtime:  .res 1
dkind:  .res 1
dt:     .res 1
mloop:  .res 1
sfx:    .res 1
sfxt:   .res 1
sfxf:   .res 1
vtmp:   .res 2
vbt:    .res 1              ; temporal exclusivo de la VBI
lagcnt: .res 1
loopf:  .res 1
; jefe
boss_on:.res 1
bossst: .res 1
btimer: .res 1
btimer2:.res 1
bflash: .res 1
bkind:  .res 1
bcol:   .res 2
brow:   .res 1
bnp:    .res 1
dlivec: .res 2
seed:   .res 1
paused: .res 1
waitcnt:.res 2
zp_end:

; ---------------------------------------------------------------------
        .segment "INITSEG"
        lda PORTB                ; XL/XE: fuera BASIC
        ora #$02
        sta PORTB
        rts

; ---------------------------------------------------------------------
        .segment "CODE"
        jmp start
        .res $400-3
        .include "data.s"

; ---------------------------------------------------------------------
        .bss
; balas: 0,1 de Zak; 2,3 enemigas
NB = 4
b_on:   .res NB
b_xl:   .res NB
b_xh:   .res NB
b_y:    .res NB
b_vx:   .res NB
b_vy:   .res NB
b_oy:   .res NB
; enemigos: 2 huecos (P2, P3)
NE = 4                      ; 0,1: franja alta (P2,P3)  2,3: franja baja (P2,P3 recolocados por DLI)
e_type: .res NE
e_xl:   .res NE
e_xh:   .res NE
e_y:    .res NE
e_vx:   .res NE
e_vy:   .res NE
e_st:   .res NE
e_t:    .res NE
e_hp:   .res NE
e_fr:   .res NE
e_dir:  .res NE
e_oy:   .res NE
e_base: .res NE
e_ysub: .res NE
e_gnd:  .res NE
; torretas (de caracteres)
NT = 3
t_on:   .res NT
t_cl:   .res NT
t_ch:   .res NT
t_row:  .res NT
t_hp:   .res NT
t_t:    .res NT
; jefe: partes
bp_c:   .res 4
bp_r:   .res 4
bp_w:   .res 4
bp_h:   .res 4
bp_hp:  .res 4
colbuf: .res NROWS
e_life: .res 4
mvres:  .res 1
ehpos:  .res 4
ecol:   .res 4
hposb:  .res 2
bh:     .res 8              ; explosiones de jefe: x y color por franja y player
bc:     .res 8
boomon: .res 1
boomv:  .res 1              ; copia de boomon que usa la VBI y las DLI
bi:     .res 1
evwait: .res 1
planted:.res 1              ; Zak plantado apuntando (FIRE mantenido desde quieto)
diff:   .res 1              ; 0 fácil, 1 normal, 2 difícil
cheat:  .res 1              ; truco: invencible
hp_max: .res 1
cseq:   .res 1              ; truco en el título: abajo, abajo, FIRE
ctim:   .res 1
oldstk: .res 1
oldtrg: .res 1
tedge:  .res 1
bwarn:  .res 1              ; aviso de ataque de jefe
bwpart: .res 1
bwpar:  .res 1
mark_on:.res 1
mark_cl:.res 1
mark_ch:.res 1
mark_par:.res 1
mark_sv:.res 2
mark_x: .res 1
t_save: .res 1
sfx_sx: .res 1
sfx_sy: .res 1
hpos:   .res 8              ; sombras HPOSP0-3, HPOSM0-3
animptr:.res 2
animcnt:.res 1
dl_pf:  .res 5              ; colores del campo (bk,pf0,pf1,pf2,pf3) para la DLI
dl_ch:  .res 1
hsc_v:  .res 1
coarse_v:.res 1
spr_sy: .res 2              ; jefe sprite (QUIMERA)
spr_x:  .res 2

        .code
; =====================================================================
start:
        lda PORTB                ; XL/XE: BASIC fuera también al arrancar del disco
        ora #$02
        sta PORTB
        sei
        lda #0
        sta NMIEN
        ldx #zp_end-zp_start-1
@z:     sta zp_start,x
        dex
        bpl @z
        cli
        lda #0
        sta SDMCTL
        lda #7
        ldx #>vbi
        ldy #<vbi
        jsr SETVBV_
        lda #<dli_none
        sta dlivec
        lda #>dli_none
        sta dlivec+1
        lda #$40
        sta NMIEN
        jsr hw_off
        lda #>PMG
        sta PMBASE
        lda #3
        sta GRACTL
        lda #$01                 ; jugadores y misiles sobre el fondo (sin quinto player)
        sta GPRIOR
        lda #$50                 ; balas enemigas (M2, M3) a doble anchura
        sta SIZEM
        lda #0
        sta SIZEP0
        sta SIZEP1
        sta SIZEP2
        sta SIZEP3
        ; sonido
        lda #3
        sta SKCTL
        lda #$28
        sta AUDCTL
        ; VBI diferida
        lda #7
        ldx #>vbi
        ldy #<vbi
        jsr SETVBV_
        lda #$C0
        sta NMIEN
        lda RANDOM
        sta seed
        lda #1                  ; dificultad por defecto: NORMAL
        sta diff
        jmp title

; ---------------------------------------------------------------------
hw_off: lda #0
        sta SDMCTL
        sta DMACTL
        jsr waitvb
        jsr clear_pmg
        rts

waitvb: lda frame
@w:     cmp frame
        beq @w
        rts

clear_pmg:
        lda #0
        tax
@c:     sta MIS,x
        sta PL0,x
        sta PL1,x
        sta PL2,x
        sta PL3,x
        inx
        bne @c
        ldx #7
@h:     sta hpos,x
        dex
        bpl @h
        rts

; =====================================================================
;  VBI diferida: scroll, HPOS, sonido, sin modo atracción
; =====================================================================
vbi:
        cld
        lda #0
        sta ATRACT
        inc frame
        lda hsc_v
        sta HSCROL
        lda lmsdirty
        beq @nol
        lda #0
        sta lmsdirty
        lda coarse_v
        and #63
        sta vbt
        ldx #0
        ldy #0
@l:     lda rowlo,x
        clc
        adc vbt
        sta DL+7,y
        iny
        iny
        iny
        inx
        cpx #NROWS
        bne @l
@nol:   lda boomon
        sta boomv
        beq @nbm
        lda #$D4
@nbm:   bne @bm
        lda #$54
@bm:    sta DL+6+3*9
        sta DL+6+3*11
        sta DL+6+3*13
        ldx #7
@hp:    lda hpos,x
        sta HPOSP0,x
        dex
        bpl @hp
        lda dlivec
        sta VDSLST
        lda dlivec+1
        sta VDSLST+1
        jsr sound
        jmp XITVBV

; DLI del juego: tras el marcador, juego de caracteres y colores del nivel
dli_game:
        pha
        txa
        pha
        ldx dl_ch
        lda dl_pf+1
        sta WSYNC
        stx CHBASE
        sta COLPF0
        lda dl_pf+2
        sta COLPF1
        lda dl_pf+3
        sta COLPF2
        lda dl_pf+4
        sta COLPF3
        lda dl_pf
        sta COLBK
        lda #<dli_mid
        sta VDSLST
        lda #>dli_mid
        sta VDSLST+1
        pla
        tax
        pla
        rti
dli_mid:
        pha
        lda hposb
        sta WSYNC
        sta HPOSP2
        lda hposb+1
        sta HPOSP3
        lda ecol+2
        sta COLPM2
        lda ecol+3
        sta COLPM3
        lda boomv
        bne @bm
        lda #<dli_bot
        sta VDSLST
        lda #>dli_bot
        sta VDSLST+1
        pla
        rti
@bm:    lda #2
        sta bi
        lda #<dli_band
        sta VDSLST
        lda #>dli_band
        sta VDSLST+1
        pla
        rti
; franjas de explosiones (filas 10, 12 y 14): dos players por franja
dli_band:
        pha
        txa
        pha
        tya
        pha
        ldx bi
        lda bh,x
        ldy bh+1,x
        sta WSYNC
        sta HPOSP2
        sty HPOSP3
        lda bc,x
        sta COLPM2
        lda bc+1,x
        sta COLPM3
        inx
        inx
        stx bi
        cpx #8
        bne @k
        lda #<dli_bot
        sta VDSLST
        lda #>dli_bot
        sta VDSLST+1
@k:     pla
        tay
        pla
        tax
        pla
        rti
dli_bot:
        pha
        lda #0
        sta WSYNC
        sta COLBK
        pla
        rti

; =====================================================================
;  SONIDO
; =====================================================================
; A = canción (índice en song_tab), X = bucle (1) o no (0)
play_song:
        stx mloop
        asl
        tay
        lda #0
        sta mus_on
        lda song_tab,y
        sta vtmp
        lda song_tab+1,y
        sta vtmp+1
        ldy #0
        lda (vtmp),y
        sta mstart
        sta mptr
        iny
        lda (vtmp),y
        sta mstart+1
        sta mptr+1
        iny
        lda (vtmp),y
        sta bstart
        sta bptr
        iny
        lda (vtmp),y
        sta bstart+1
        sta bptr+1
        iny
        lda (vtmp),y
        sta dstart
        sta dptr
        iny
        lda (vtmp),y
        sta dstart+1
        sta dptr+1
        lda #1
        sta mtime
        sta btime
        sta dtime
        sta mus_on
        rts

stop_music:
        lda #0
        sta mus_on
        sta AUDC1
        sta AUDC3
        sta AUDC4
        rts

sound:  lda mus_on
        bne @m
        jmp sfx_run
@m:     dec mtime
        bne @menv
        ldy #0
        lda (mptr),y
        cmp #$FF
        bne @mn
        lda mloop
        bne @mrst
        sta mus_on
        sta AUDC1
        sta AUDC4
        jmp sfx_run
@mrst:  lda mstart
        sta mptr
        lda mstart+1
        sta mptr+1
        lda bstart
        sta bptr
        lda bstart+1
        sta bptr+1
        lda dstart
        sta dptr
        lda dstart+1
        sta dptr+1
        lda #1
        sta btime
        sta dtime
        lda (mptr),y
@mn:    tax
        iny
        lda (mptr),y
        sta mtime
        lda mptr
        clc
        adc #2
        sta mptr
        bcc @m2
        inc mptr+1
@m2:    cpx #0
        beq @mrest
        lda mel_tab,x
        sta AUDF1
        lda #9
        sta mvol
        bne @menv
@mrest: lda #0
        sta mvol
@menv:  lda mvol
        cmp #5
        bcc @ms
        lda frame
        and #3
        bne @ms
        dec mvol
@ms:    lda mvol
        lsr
        ora #$A0
        sta AUDC1
        ; bajo
        dec btime
        bne @benv
        ldy #0
        lda (bptr),y
        cmp #$FF
        bne @bn
        lda bstart
        sta bptr
        lda bstart+1
        sta bptr+1
        lda (bptr),y
@bn:    tax
        iny
        lda (bptr),y
        sta btime
        lda bptr
        clc
        adc #2
        sta bptr
        bcc @b2
        inc bptr+1
@b2:    cpx #0
        beq @brest
        lda bas_lo,x
        sta AUDF3
        lda bas_hi,x
        sta AUDF4
        lda #8
        sta bvol
        bne @benv
@brest: lda #0
        sta bvol
@benv:  lda bvol
        cmp #4
        bcc @bs
        lda frame
        and #3
        bne @bs
        dec bvol
@bs:    lda bvol
        ora #$A0
        sta AUDC4
        lda #0
        sta AUDC3
        ; batería
        dec dtime
        bne sfx_run
        ldy #0
        lda (dptr),y
        cmp #$FF
        bne @dn
        lda dstart
        sta dptr
        lda dstart+1
        sta dptr+1
        lda (dptr),y
@dn:    sta dkind
        iny
        lda (dptr),y
        sta dtime
        lda dptr
        clc
        adc #2
        sta dptr
        bcc @d2
        inc dptr+1
@d2:    lda #0
        sta dt
        ; un golpe de batería tapa el sonido de los disparos (no explosiones ni golpes)
        lda dkind
        beq sfx_run
        lda sfx
        cmp #1
        beq @cut
        cmp #6
        bne sfx_run
@cut:   lda #0
        sta sfx
sfx_run:
        lda sfx
        bne @s
        jmp drum_run
@s:     dec sfxt
        bne @go
        lda #0
        sta sfx
        sta AUDC2
        rts
@go:    cmp #1
        bne @n1
        ; disparo: tono que sube
        lda sfxf
        clc
        adc #6
        sta sfxf
        sta AUDF2
        lda sfxt
        ora #$A0
        sta AUDC2
        rts
@n1:    cmp #2
        bne @n2
        ; salto: tono que baja
        lda sfxf
        sec
        sbc #5
        sta sfxf
        sta AUDF2
        lda #$A5
        sta AUDC2
        rts
@n2:    cmp #3
        bne @n3
        ; explosión: ruido
        lda sfxf
        clc
        adc #3
        sta sfxf
        sta AUDF2
        lda sfxt
        lsr
        ora #$80
        sta AUDC2
        rts
@n3:    cmp #4
        bne @n4
        ; golpe a Zak: zumbido
        lda frame
        and #4
        asl
        asl
        adc #$60
        sta AUDF2
        lda #$CA
        sta AUDC2
        rts
@n4:    cmp #5
        bne @n5
        ; recogida: arpegio
        lda sfxt
        and #3
        tax
        lda arp,x
        sta AUDF2
        lda #$A8
        sta AUDC2
        rts
@n5:    cmp #7
        bne @n7
        ; silbido de algo que cae: tono que baja despacio
        inc sfxf
        lda frame
        and #1
        beq @w7
        inc sfxf
@w7:    lda sfxf
        sta AUDF2
        lda #$A6
        sta AUDC2
        rts
@n7:    cmp #8
        bne @n8
        ; alerta: dos tonos
        lda sfxt
        and #4
        beq @a1
        lda #30
        bne @a2
@a1:    lda #45
@a2:    sta AUDF2
        lda #$A8
        sta AUDC2
        rts
@n8:    ; disparo enemigo
        lda sfxf
        clc
        adc #2
        sta sfxf
        sta AUDF2
        lda #$C4
        sta AUDC2
        rts
; batería en el canal 2 (si no suena un efecto)
drum_run:
        lda mus_on
        beq @off
        ldx dkind
        beq @off
        ldy dt
        cpy #6
        bcs @off
        inc dt
        lda dr_f,x
        clc
        adc dr_sw,y
        sta AUDF2
        lda dr_c,x
        sec
        sbc dr_dec,y
        bcc @off
        cmp dr_min,x
        bcc @off
        sta AUDC2
        rts
@off:   lda #0
        sta AUDC2
        rts
;            -    bombo caja charles redoble
dr_f:   .byte 0,  $60, $06, $01, $08
dr_c:   .byte 0,  $AC, $8A, $84, $86
dr_min: .byte 0,  $A1, $81, $81, $81
dr_sw:  .byte 0,$18,$38,$58,$78,$98      ; el bombo baja de tono
dr_dec: .byte 0,2,4,6,8,10
arp:    .byte 60,47,40,30
hardv:  .byte $FD,$FE,0,2,3
turret_base: .byte 110,70,45
diff_lives:  .byte 5,3,3
diff_hp:     .byte 4,3,2
warn_len:    .byte 60,40,25
sfx_len:.byte 0,8,12,30,20,24,6,40,16
sfx_pri:.byte 0,1,2,4,5,3,0,3,2
sfx_f0: .byte 0,20,40,10,0,0,30,24,40
; A = efecto
play_sfx:                       ; conserva X e Y
        stx sfx_sx
        sty sfx_sy
        tax
        lda sfx_pri,x
        ldy sfx
        cmp sfx_pri,y
        bcc @no
        stx sfx
        lda sfx_len,x
        sta sfxt
        lda sfx_f0,x
        sta sfxf
@no:    ldx sfx_sx
        ldy sfx_sy
        rts

; =====================================================================
;  Utilidades
; =====================================================================
rand:   lda seed
        asl
        bcc @n
        eor #$1D
@n:     sta seed
        eor RANDOM
        rts

; suma A (BCD, centenas) * 100 a la puntuación: A = puntos/100 en BCD
add_score:
        sed
        clc
        adc score+1
        sta score+1
        lda score
        adc #0
        sta score
        sed
        cld
        lda #1
        sta hudflag
        rts

; ASCII -> código interno de pantalla
a2i:    cmp #$20
        bcc @lo
        cmp #$60
        bcs @r
        sec
        sbc #$20
@r:     rts
@lo:    ora #$40
        rts

; imprime cadena (ptr) terminada en 0 en (ptr2); color en tmp+3 (ORA)
print:  ldy #0
@l:     lda (ptr),y
        beq @e
        jsr a2i
        ora tmp+3
        sta (ptr2),y
        iny
        bne @l
@e:     rts

; =====================================================================
;  HUD
; =====================================================================
hud_txt:.byte "PUNTOS 000000   VIDA ",0
draw_hud:
        lda #0
        sta hudflag
        ldx #39
        lda #0
@c:     sta HUD,x
        dex
        bpl @c
        lda #<hud_txt
        sta ptr
        lda #>hud_txt
        sta ptr+1
        lda #<(HUD+1)
        sta ptr2
        lda #>(HUD+1)
        sta ptr2+1
        lda #0
        sta tmp+3
        jsr print
        ; puntuación
        ldx #0
        ldy #8
@s:     lda score,x
        lsr
        lsr
        lsr
        lsr
        ora #$10
        sta HUD,y
        iny
        lda score,x
        and #$0F
        ora #$10
        sta HUD,y
        iny
        inx
        cpx #3
        bne @s
        ; vida: corazones (o INV con el truco)
        lda cheat
        beq @nh0
        lda #$29            ; I
        sta HUD+22
        lda #$2E            ; N
        sta HUD+23
        lda #$36            ; V
        sta HUD+24
        jmp @hd
@nh0:   ldx hp
        ldy #22
@h:     cpx #0
        beq @hd
        lda #$40
        sta HUD,y
        iny
        dex
        bne @h
@hd:    ; vidas
        lda #$3A            ; 'Z'
        sta HUD+27
        lda #$21            ; 'A'
        sta HUD+28
        lda #$2B            ; 'K'
        sta HUD+29
        lda #$78            ; 'x'
        sta HUD+30
        lda lives
        ora #$10
        sta HUD+31
        lda #$26            ; F
        sta HUD+34
        lda #$21
        sta HUD+35
        lda #$33
        sta HUD+36
        lda #$25
        sta HUD+37
        ldx phase
        inx
        txa
        ora #$10
        sta HUD+39
        rts

; =====================================================================
;  MAPA: dibujo de columnas en el anillo
; =====================================================================
; carga punteros de la fase
setup_phase:
        ldx phase
        lda ph_charhi,x
        sta dl_ch
        lda ph_bk,x
        sta dl_pf
        lda ph_pf0,x
        sta dl_pf+1
        lda ph_pf1,x
        sta dl_pf+2
        lda ph_pf2,x
        sta dl_pf+3
        lda ph_pf3,x
        sta dl_pf+4
        lda ph_haz,x
        sta haz_t
        lda ph_plat,x
        sta plat_t
        lda ph_solid,x
        sta solid_t
        lda ph_seqlo,x
        sta seqp
        lda ph_seqhi,x
        sta seqp+1
        lda ph_collolo,x
        sta collo_p
        lda ph_collohi,x
        sta collo_p+1
        lda ph_colhilo,x
        sta colhi_p
        lda ph_colhihi,x
        sta colhi_p+1
        lda ph_bglo,x
        sta bgp
        lda ph_bghi,x
        sta bgp+1
        lda ph_eventslo,x
        sta evptr
        lda ph_eventshi,x
        sta evptr+1
        lda ph_animlo,x
        sta animptr
        lda ph_animhi,x
        sta animptr+1
        ; cámara máxima = arena*4
        lda ph_arenalo,x
        sta camxmax
        lda ph_arenahi,x
        sta camxmax+1
        asl camxmax
        rol camxmax+1
        asl camxmax
        rol camxmax+1
        lda ph_en1,x
        sta PCOLR2
        lda ph_en2,x
        sta PCOLR3
        rts

; dibuja la columna del mundo (tmp,tmp+1)
drawcol:
        lda tmp
        and #63
        sta tmp+2
        ; fondo: (w & 15) * 22
        lda tmp
        and #15
        tax
        lda mul22,x
        clc
        adc bgp
        sta ptr
        lda bgp+1
        adc mul22h,x
        sta ptr+1
        ldy #NROWS-1
@bg:    lda (ptr),y
        sta colbuf,y
        dey
        bpl @bg
        ; primer plano
        lda seqp
        clc
        adc tmp
        sta ptr
        lda seqp+1
        adc tmp+1
        sta ptr+1
        ldy #0
        lda (ptr),y
        tay
        lda (collo_p),y
        sta ptr
        lda (colhi_p),y
        sta ptr+1
        ldy #0
@run:   lda (ptr),y
        cmp #$FF
        beq @wr
        tax                     ; fila
        iny
        lda (ptr),y
        sta tmp+3               ; cuántas
        iny
@rc:    lda (ptr),y
        sta colbuf,x
        iny
        inx
        dec tmp+3
        bne @rc
        beq @run
@wr:    ldx #0
@w:     lda rowlo,x
        clc
        adc tmp+2
        sta ptr
        lda rowhi,x
        sta ptr+1
        lda colbuf,x
        ldy #0
        sta (ptr),y
        ldy #64
        sta (ptr),y
        inx
        cpx #NROWS
        bne @w
        rts

; escribe el carácter A en (columna tx/tx+1, fila Y) en ambas copias del anillo
putchar:
        sta tmp+3
        lda tx
        and #63
        clc
        adc rowlo,y
        sta ptr
        lda rowhi,y
        sta ptr+1
        ldy #0
        lda tmp+3
        sta (ptr),y
        ldy #64
        sta (ptr),y
        rts

; lee el carácter en columna tx, fila Y  -> A
getchar:
        lda tx
        and #63
        clc
        adc rowlo,y
        sta ptr
        lda rowhi,y
        sta ptr+1
        ldy #0
        lda (ptr),y
        rts

; tile en x mundo (tx,tx+1 en color clocks), y = ty (línea) -> A = carácter & $7F
; C=1 si sólido (A conserva el carácter)
tile_at:
        lda ty
        cmp #176
        bcs @e
        lsr
        lsr
        lsr
        tay
        lda tx
        lsr
        lsr
        clc
        adc rowlo,y
        sta ptr
        lda rowhi,y
        sta ptr+1
        ldy #0
        lda (ptr),y
        and #$7F
        cmp solid_t
        rts
@e:     lda #0
        clc
        rts

; dibuja columnas pendientes hasta coarse+44
fill_cols:
        lda coarse
        clc
        adc #44
        sta tmp
        lda coarse+1
        adc #0
        sta tmp+1
        lda drawn+1
        cmp tmp+1
        bcc @do
        bne @x
        lda drawn
        cmp tmp
        bcc @do
        beq @do
@x:     rts
@do:    lda drawn
        sta tmp
        lda drawn+1
        sta tmp+1
        jsr drawcol
        inc drawn
        bne fill_cols
        inc drawn+1
        jmp fill_cols

; calcula coarse/hscrol desde camx y avisa a la VBI
set_scroll:
        lda camx+1
        sta coarse+1
        lda camx
        sta tmp
        lsr coarse+1
        ror
        lsr coarse+1
        ror
        sta coarse
        lda tmp
        and #3
        eor #3
        sta hsc_v
        lda coarse
        cmp coarse_v
        beq @s
        sta coarse_v
        lda #1
        sta lmsdirty
@s:     rts

; caracteres animados de la fase (cada entrada: código, nframes, velocidad, datos)
anim_chars:
        lda animptr
        sta ptr3
        lda animptr+1
        sta ptr3+1
@n:     ldy #0
        lda (ptr3),y
        cmp #$FF
        beq @x
        sta tmp                 ; código
        iny
        lda (ptr3),y
        sta tmp+1               ; nframes
        iny
        lda (ptr3),y            ; velocidad (máscara)
        and frame
        bne @skip
        ; frame = (frame / (vel+1)) % nframes  -> usamos contador simple
        lda frame
        ldy #2
        lda (ptr3),y
        tax
        lda frame
@dv:    cpx #0
        beq @dd
        lsr
        pha
        txa
        lsr
        tax
        pla
        jmp @dv
@dd:    ; A = frame >> bits(vel)
@mod:   cmp tmp+1
        bcc @ok
        sbc tmp+1
        jmp @mod
@ok:    asl
        asl
        asl
        clc
        adc #3
        tay                     ; origen en la entrada
        ; destino: charset + código*8
        lda tmp
        lsr
        lsr
        lsr
        lsr
        lsr
        clc
        adc dl_ch
        sta ptr2+1
        lda tmp
        asl
        asl
        asl
        ; ptr2 = destino - Y: así origen y destino usan el mismo índice
        sty tmp+2
        sec
        sbc tmp+2
        sta ptr2
        bcs @nb
        dec ptr2+1
@nb:    ldx #8
@cp:    lda (ptr3),y
        sta (ptr2),y
        iny
        dex
        bne @cp
@skip:  ; siguiente entrada: 3 + nframes*8
        lda tmp+1
        asl
        asl
        asl
        clc
        adc #3
        adc ptr3
        sta ptr3
        bcc @n
        inc ptr3+1
        bne @n
@x:     rts

; =====================================================================
;  DISPLAY LIST del juego
; =====================================================================
build_game_dl:
        ldx #0
        lda #$70
        sta DL,x
        inx
        sta DL,x
        inx
        sta DL,x
        inx
        lda #$C2
        sta DL,x
        inx
        lda #<HUD
        sta DL,x
        inx
        lda #>HUD
        sta DL,x
        inx
        ldy #0
@r:     lda #$54
        cpy #NROWS-1
        beq @dl
        cpy #7
        bne @nd
@dl:    lda #$D4
@nd:    sta DL,x
        inx
        lda rowlo,y
        sta DL,x
        inx
        lda rowhi,y
        sta DL,x
        inx
        iny
        cpy #NROWS
        bne @r
        lda #$41
        sta DL,x
        inx
        lda #<DL
        sta DL,x
        inx
        lda #>DL
        sta DL,x
        rts

game_screen_on:
        jsr build_game_dl
        lda #<dli_game
        sta dlivec
        lda #>dli_game
        sta dlivec+1
        lda #<DL
        sta SDLSTL
        lda #>DL
        sta SDLSTH
        lda #$E0
        sta CHBAS
        lda #$00
        sta COLOR4
        sta COLOR2
        lda #$0C
        sta COLOR1
        lda #$0C
        sta PCOLR0
        lda #$44
        sta PCOLR1
        lda #$3E                 ; ancho normal + PMG 1 línea + misiles + players
        sta SDMCTL
        rts

; =====================================================================
;  INICIO DE FASE
; =====================================================================
start_phase:
        jsr hw_off
        jsr setup_phase
        lda #0
        sta camx
        sta camx+1
        sta drawn
        sta drawn+1
        sta boss_on
        sta bossst
        sta coarse_v
        lda #$FF
        sta coarse_v
        ldx #NB-1
@b:     lda #0
        sta b_on,x
        dex
        bpl @b
        ldx #NE-1
@e:     lda #0
        sta e_type,x
        dex
        bpl @e
        ldx #NT-1
@t:     lda #0
        sta t_on,x
        dex
        bpl @t
        jsr set_scroll
        jsr fill_cols
        ; Zak
        lda #24
        sta px
        lda #0
        sta px+1
        jsr find_ground
        lda py
        sta oldpy
        lda #0
        sta vy
        sta pysub
        sta pdir
        sta pstate
        sta crouch
        sta firecd
        lda #1
        sta onground
        sta uplatch
        lda hp_max
        sta hp
        lda #90
        sta inv
        jsr draw_hud
        jsr game_screen_on
        ldx phase
        lda phase_song,x
        ldx #1
        jsr play_song
        rts

phase_song: .byte 0,1,2,3,4

; =====================================================================
;  BUCLE DEL JUEGO
; =====================================================================
game_loop:
        jsr waitvb
        lda frame
        cmp loopf
        beq @ok
        inc lagcnt
@ok:
        lda CH
        cmp #$FF
        beq @nk
        ldx #$FF
        stx CH
        and #$3F
        cmp #$0A                 ; P = pausa
        beq @tp
        cmp #$21                 ; espacio
        bne @nk
@tp:    lda paused
        eor #1
        sta paused
        beq @nk
        jsr stop_music_soft
@nk:    lda paused
        bne game_loop
        jsr draw_sprites        ; primero: los sprites se pintan antes de que el haz llegue al campo
        jsr read_input
        jsr player_update
        jsr camera_update
        jsr events_update
        jsr enemies_update
        jsr turrets_update
        jsr boss_update
        jsr bullets_update
        jsr collide
        jsr anim_chars
        lda hudflag
        beq @nh
        jsr draw_hud
@nh:    lda frame
        sta loopf
        lda pstate
        cmp #3                  ; game over
        beq @go
        lda bossst
        cmp #9                  ; fase superada
        beq @clr
        jmp game_loop
@go:    jmp game_over
@clr:   jmp phase_clear

stop_music_soft:
        lda #0
        sta AUDC1
        sta AUDC2
        sta AUDC4
        rts

read_input:
        lda STICK0
        eor #$0F
        sta stick               ; bits a 1 = pulsado: 1 arriba 2 abajo 4 izq 8 der
        lda trig
        sta oldtrig
        lda STRIG0
        eor #1
        sta trig
        rts

; =====================================================================
;  ZAK
; =====================================================================
JUMPV = $B8                     ; -72/16 líneas por cuadro
player_update:
        lda inv
        beq @ni
        dec inv
@ni:    lda pstate
        beq @alive
        jmp player_dying
@alive: lda firecd
        beq @nf
        dec firecd
@nf:    ; ¿plantado? FIRE pulsado estando quieto en el suelo: la palanca apunta
        lda onground
        beq @unpl
        lda trig
        beq @unpl
        lda planted
        bne @pl
        lda oldtrig
        bne @np
        lda stick
        and #12
        bne @np
        lda #1
        sta planted
@pl:    lda stick
        and #4
        beq @pr
        lda #1
        sta pdir
@pr:    lda stick
        and #8
        beq @pc
        lda #0
        sta pdir
@pc:    lda #0
        sta crouch
        sta panim
        lda stick
        and #2
        beq @pu
        lda #1
        sta crouch
@pu:    lda stick
        and #1
        sta uplatch             ; al soltar FIRE con arriba pulsado no salta
        jmp @grav
@unpl:  lda #0
        sta planted
@np:    ; agacharse
        lda #0
        sta crouch
        lda onground
        beq @nc
        lda stick
        and #2
        beq @nc
        lda #1
        sta crouch
@nc:    ; movimiento horizontal
        lda crouch
        bne @nomove
        lda stick
        and #4
        beq @nl
        lda #1
        sta pdir
        jsr try_left
        jmp @moved
@nl:    lda stick
        and #8
        beq @nomove
        lda #0
        sta pdir
        jsr try_right
@moved: inc panim
        jmp @jump
@nomove:lda #0
        sta panim
@jump:  ; salto con nueva pulsación de arriba
        lda stick
        and #1
        beq @noup
        lda uplatch
        bne @upd
        lda onground
        beq @upd
        lda #JUMPV
        sta vy
        lda #0
        sta onground
        lda #2
        jsr play_sfx
@upd:   lda #1
        sta uplatch
        bne @grav
@noup:  lda #0
        sta uplatch
@grav:  lda onground
        bne @supp
        jsr fall
        jmp @fire
@supp:  ; ¿sigue habiendo suelo?
        jsr feet_solid
        bcs @fire
        lda #0
        sta onground
        sta vy
@fire:  ; disparo
        lda trig
        beq @nofire
        lda firecd
        bne @nofire
        jsr player_fire
@nofire:; caída a un foso
        lda cheat
        beq @nch
        lda py
        cmp #176
        bcc @alive2
        cmp #240
        bcs @alive2
        lda #$A0
        sta vy
        jmp @alive2
@nch:
        lda py
        cmp #200
        bcc @alive2
        cmp #240
        bcs @alive2
        jsr kill_player
@alive2:; casillas peligrosas
        jsr hazard_check
        ; cuadro de animación
        jsr player_frame
        rts

player_frame:
        jsr aim_dir
        tax
        lda onground
        bne @g
        lda air_fr,x
        bne @s
@g:     lda crouch
        beq @g2
        lda #5
        bne @s
@g2:    lda planted
        beq @r
        lda gnd_fr,x
        jmp @s
@r:     lda panim
        beq @st
        lsr
        lsr
        lsr
        and #3
        tax
        lda runseq,x
        bne @s
@st:    lda #0
@s:     sta pframe
        rts
runseq: .byte 1,2,3,2
;          hor diagA arr agach diagB abajo
air_fr: .byte 4,  8,   6,   4,    4,    4
gnd_fr: .byte 0,  8,   6,   5,    0,    0

; pies sobre sólido o plataforma: C=1
feet_solid:
        lda py
        sta ty
        lda px
        clc
        adc #2
        sta tx
        lda px+1
        adc #0
        sta tx+1
        jsr tile_at
        cmp plat_t
        bcs @y
        lda px
        clc
        adc #5
        sta tx
        lda px+1
        adc #0
        sta tx+1
        jsr tile_at
        cmp plat_t
        bcs @y
        clc
@y:     rts

fall:   lda py
        sta tmp+1               ; pies antes
        lda vy
        bmi @up
        cmp #64
        bcs @cap
@up:    clc
        adc #4
        sta vy
@cap:   ; y += vy/16 (con signo)
        lda vy
        asl
        asl
        asl
        asl
        clc
        adc pysub
        sta pysub
        lda vy
        php
        lsr
        lsr
        lsr
        lsr
        plp
        bpl @pos
        ora #$F0
@pos:   adc py
        sta py
        lda vy
        bmi @ceil
        ; aterrizaje: sólo si antes estábamos por encima del borde superior de la fila
        lda py
        cmp #176
        bcs @nl
        and #$F8
        sta tmp+2               ; borde de la fila
        lda tmp+1
        cmp tmp+2
        beq @chk
        bcs @nl
@chk:   lda tmp+2
        pha
        lda py
        pha
        lda tmp+2
        sta py
        jsr feet_solid
        pla
        tax
        pla
        bcs @land
        stx py
@nl:    rts
@land:  lda #0
        sta vy
        sta pysub
        lda #1
        sta onground
        rts
@ceil:  ; techo
        lda py
        sec
        sbc #20
        sta ty
        cmp #176
        bcs @nc
        lda px
        clc
        adc #4
        sta tx
        lda px+1
        adc #0
        sta tx+1
        jsr tile_at
        bcc @nc
        lda #0
        sta vy
@nc:    rts

; ¿pared a la derecha/izquierda? (x de prueba en tx), C=1 si sólida
wall_at:
        lda py
        sec
        sbc #3
        sta ty
        jsr tile_at
        bcs @w
        lda py
        sec
        sbc #11
        sta ty
        jsr tile_at
        bcs @w
        lda py
        sec
        sbc #18
        sta ty
        jsr tile_at
@w:     rts

try_right:
        ; límite: pantalla (x-camx <= 152) y jefe
        lda px
        sec
        sbc camx
        cmp #164
        bcs @no
        lda boss_on
        beq @nb
        jsr boss_left_edge      ; A = x pantalla del borde izquierdo del jefe
        sec
        sbc #10
        sta tmp
        lda px
        sec
        sbc camx
        cmp tmp
        bcs @no
@nb:    lda px
        clc
        adc #8
        sta tx
        lda px+1
        adc #0
        sta tx+1
        jsr wall_at
        bcs @no
        inc px
        bne @no
        inc px+1
@no:    rts

try_left:
        lda px
        sec
        sbc camx
        cmp #VIS0+1
        bcc @no
        lda px
        sec
        sbc #1
        sta tx
        lda px+1
        sbc #0
        sta tx+1
        jsr wall_at
        bcs @no
        lda px
        bne @d
        dec px+1
@d:     dec px
@no:    rts

hazard_check:
        lda py
        sec
        sbc #2
        sta ty
        lda px
        clc
        adc #4
        sta tx
        lda px+1
        adc #0
        sta tx+1
        jsr tile_at
        cmp haz_t
        bcc @n
        cmp plat_t
        bcs @n
        jsr hurt_player
@n:     rts

; ---- disparo de Zak
player_fire:
        ldx #0
        lda b_on
        beq @f
        inx
        lda b_on+1
        beq @f
        rts
@f:     lda #1
        sta b_on,x
        lda #8
        sta firecd
        jsr aim_dir             ; A = dirección 0..5
        tay
        ; velocidad: horizontal se refleja según hacia dónde mira Zak
        lda aim_vy,y
        sta b_vy,x
        lda aim_vx,y
        sty tmp
        ldy pdir
        beq @r
        eor #$FF
        clc
        adc #1
@r:     sta b_vx,x
        ldy tmp
        ; salida: x = px + (derecha ? ox_r : ox_l)
        lda pdir
        bne @l
        lda aim_oxr,y
        jmp @ox
@l:     lda aim_oxl,y
@ox:    clc
        adc px
        sta b_xl,x
        lda #0
        bit aim_oxl              ; (sin signo: todos los desplazamientos son >= 0 salvo izq.)
        lda px+1
        adc #0
        sta b_xh,x
        lda pdir
        beq @y
        ; izquierda horizontal/diagonal: un píxel antes de px
        lda aim_oxl,y
        bne @y
        lda b_xl,x
        bne @dl
        dec b_xh,x
@dl:    dec b_xl,x
@y:     lda py
        sec
        sbc aim_oy,y
        sta b_y,x
        lda #1
        jmp play_sfx

; dirección de disparo según palanca y estado: 0 horiz, 1 diag arriba, 2 arriba,
; 3 agachado, 4 diag abajo, 5 abajo
aim_dir:
        lda onground
        beq @air
        lda crouch
        bne @cr
        lda planted
        beq @h
        lda stick
        and #1
        beq @h
        lda stick
        and #12
        bne @d1
        lda #2
        rts
@d1:    lda #1
        rts
@cr:    lda #3
        rts
@h:     lda #0
        rts
@air:   lda stick
        and #1
        beq @na
        lda stick
        and #12
        bne @d1
        lda #2
        rts
@na:    lda stick
        and #2
        beq @h
        lda stick
        and #12
        bne @d4
        lda #5
        rts
@d4:    lda #4
        rts
;            hor diagA arr agach diagB abajo
aim_vx:  .byte 4,  3,    0,   4,    3,    0
aim_vy:  .byte 0,  $FB,  $F9, 0,    5,    7
aim_oxr: .byte 8,  7,    6,   8,    7,    3
aim_oxl: .byte 0,  0,    1,   0,    0,    3
aim_oy:  .byte 12, 17,   22,  5,    6,    1

; ---- daño y muerte
hurt_player:
        lda cheat
        beq @go
        rts
@go:    lda inv
        bne @n
        lda pstate
        bne @n
        lda #4
        jsr play_sfx
        dec hp
        lda #1
        sta hudflag
        lda hp
        beq kill_player
        lda #65
        sta inv
@n:     rts

kill_player:
        lda pstate
        bne @n
        lda #1
        sta pstate
        lda #0
        sta hp
        lda #90
        sta ptimer
        lda #7
        sta pframe
        lda #3
        jsr play_sfx
        lda #1
        sta hudflag
@n:     rts

player_dying:
        lda #7
        sta pframe
        dec ptimer
        bne @w
        lda cheat
        bne @resp
        dec lives
        bne @resp
        lda #3
        sta pstate
@w:     rts
@resp:  ; reaparición: buscar suelo firme desde la izquierda de la pantalla
        lda #0
        sta pstate
        lda hp_max
        sta hp
        lda #120
        sta inv
        lda #1
        sta hudflag
        ; borrar balas enemigas
        lda #0
        sta b_on+2
        sta b_on+3
        lda camx
        clc
        adc #VIS0+8
        sta px
        lda camx+1
        adc #0
        sta px+1
find_ground:
@col:   lda #48
        sta py
@row:   jsr feet_solid
        bcs @ok
        lda py
        clc
        adc #8
        sta py
        cmp #176
        bcc @row
        lda px
        clc
        adc #4
        sta px
        bcc @col
        inc px+1
        bne @col
@ok:    lda #1
        sta onground
        lda #0
        sta vy
        rts

; =====================================================================
;  CÁMARA
; =====================================================================
camera_update:
        lda pstate
        bne @x
        lda px
        sec
        sbc camx
        cmp #84
        bcc @x
        ; ¿máximo?
        lda camx+1
        cmp camxmax+1
        bcc @adv
        lda camx
        cmp camxmax
        bcs @x
@adv:   inc camx
        bne @s
        inc camx+1
@s:     jsr set_scroll
        jsr fill_cols
@x:     rts

; =====================================================================
;  EVENTOS (aparición por columna)
; =====================================================================
events_update:
        ldy #1
        lda (evptr),y
        cmp #$FF
        beq @x
        ; ¿col_evento <= coarse+40?
        lda coarse
        clc
        adc #43
        sta tmp
        lda coarse+1
        adc #0
        sta tmp+1
        ldy #1
        lda (evptr),y
        cmp tmp+1
        bcc @go
        bne @x
        dey
        lda (evptr),y
        cmp tmp
        beq @go
        bcs @x
@go:    jsr spawn_event
        bcs @x                  ; recogible sin hueco: se reintenta
        lda evptr
        clc
        adc #5
        sta evptr
        bcc events_update
        inc evptr+1
        bne events_update
@x:     rts

spawn_event:
        ldy #2
        lda (evptr),y
        cmp #8
        bne @en
        ; torreta
        ldx #NT-1
@ft:    lda t_on,x
        beq @tf
        dex
        bpl @ft
        clc
        rts
@tf:    lda #1
        sta t_on,x
        ldy #0
        lda (evptr),y
        sta t_cl,x
        iny
        lda (evptr),y
        sta t_ch,x
        ldy #3
        lda (evptr),y
        sta t_row,x
        lda #5
        sta t_hp,x
        lda #40
        sta t_t,x
        clc
        rts
@en:    sta tmp+2               ; tipo
        ldx #0
        cmp #2                  ; dron: franja alta
        beq @sl
        ldx #2
@sl:    lda e_type,x
        beq @ef
        inx
        lda e_type,x
        beq @ef
        ; sin hueco: esperar; los enemigos se pierden tras 90 cuadros, los recogibles no
        inc evwait
        lda tmp+2
        cmp #6
        bcs @wt
        lda evwait
        cmp #90
        bcc @wt
        lda #0
        sta evwait
        clc
        rts
@wt:    sec
        rts
@ef:    lda #0
        sta evwait
        lda tmp+2
        sta e_type,x
        ; x = (coarse+43)*4: borde derecho del campo visible
        lda coarse
        clc
        adc #43
        sta tmp
        lda coarse+1
        adc #0
        asl tmp
        rol
        asl tmp
        rol
        sta e_xh,x
        lda tmp
        sta e_xl,x
        ldy #3
        lda (evptr),y
        asl
        asl
        asl
        sta e_y,x
        sta e_base,x
        lda #0
        sta e_vy,x
        sta e_st,x
        sta e_fr,x
        sta e_ysub,x
        sta e_gnd,x
        lda #1
        sta e_dir,x             ; mirando a la izquierda
        lda #30
        sta e_t,x
        ldy tmp+2
        lda en_hp,y
        sta e_hp,x
        lda #0
        sta e_life,x
        ; enemigos de tierra: no aparecer sobre un foso (esperar)
        lda tmp+2
        cmp #2
        beq @ok
        cmp #6
        bcs @ok
        lda #0
        jsr en_floor_at
        bcs @ok
        lda #0
        sta e_type,x
        sec
        rts
@ok:    clc
        rts
;             -  sold drone dog jump bug fish can
en_hp:  .byte 0, 1,   1,    2,  2,   3,  1,   1
en_pts: .byte 0, $01, $02,  $02,$02, $03,$00, $00
en_f0:  .byte 0, EF_SOLDIER1, EF_DRONE1, EF_DOG1, EF_JUMPER1, EF_BUG1, EF_FISH, EF_CAN

; =====================================================================
;  ENEMIGOS
; =====================================================================
enemies_update:
        ldx #0
        jsr enemy_one
        ldx #1
        jsr enemy_one
        ldx #2
        jsr enemy_one
        ldx #3
enemy_one:
        lda e_type,x
        bne @a
        rts
@a:     ; ¿fuera por la izquierda?
        lda e_xl,x
        clc
        adc #12
        sta tmp
        lda e_xh,x
        adc #0
        cmp camx+1
        bcc @kill
        bne @in
        lda tmp
        cmp camx
        bcs @in
@kill:  lda #0
        sta e_type,x
        rts
@in:    ; ¿muy a la derecha? (se fue andando)
        lda e_xl,x
        sec
        sbc camx
        sta tmp
        lda e_xh,x
        sbc camx+1
        bne @kill2
        lda tmp
        cmp #VIS0+176
        bcs @kill2
        ; vida máxima en pantalla: ~13 s
        lda frame
        and #7
        bne @nl
        inc e_life,x
        lda e_life,x
        cmp #100
        bcc @nl
        lda e_st,x
        bmi @nl
@kill2: lda #0
        sta e_type,x
        rts
@nl:    lda e_y,x
        cmp #192
        bcc @in2
        cmp #240
        bcs @in2
        lda #0
        sta e_type,x
        rts
@in2:   lda e_st,x
        cmp #$80
        bcc @live
        ; explotando
        dec e_t,x
        beq @kill
        lda e_t,x
        lsr
        lsr
        lsr
        and #1
        clc
        adc #EF_BOOM1
        sta e_fr,x
        rts
@live:  lda e_type,x
        cmp #1
        beq @hz
        cmp #3
        bcc @go
        cmp #6
        bcs @go
@hz:    jsr en_hazard
        bcc @go
        lda #$80
        sta e_st,x
        lda #24
        sta e_t,x
        lda #3
        jsr play_sfx
        rts
@go:    lda e_type,x
        asl
        tay
        lda en_code,y
        sta ptr
        lda en_code+1,y
        sta ptr+1
        jmp (ptr)
;           -   sold drone dog  jump bug  fish can  -   onda roca fuego brazo
en_col: .byte 0,  $08, $46,  $96, $C6, $DA, $9C, $1C, 0,  $0C, $0A, $36,  $1E
en_code:.word 0, en_soldier, en_drone, en_dog, en_jumper, en_bug, en_fish, en_fish, 0, en_proj, en_proj, en_proj, en_proj

; dirección hacia Zak (e_dir: 1 izquierda)
face_player:
        lda e_xl,x
        sec
        sbc px
        lda e_xh,x
        sbc px+1
        lda #1
        bcs @l
        lda #0
@l:     sta e_dir,x
        rts

; ¿pared delante del enemigo X? C=1 si sólida
en_wall:
        stx tmp+3
        lda e_vx,x
        bmi @l
        lda e_xl,x
        clc
        adc #8
        sta tx
        lda e_xh,x
        adc #0
        sta tx+1
        jmp @t
@l:     lda e_xl,x
        sec
        sbc #1
        sta tx
        lda e_xh,x
        sbc #0
        sta tx+1
@t:     lda e_y,x
        sec
        sbc #4
        sta ty
        jsr tile_at
        bcs @y
        ldx tmp+3
        lda e_y,x
        sec
        sbc #12
        sta ty
        jsr tile_at
@y:     ldx tmp+3
        rts
; ¿pisa lava o electricidad? C=1
en_hazard:
        stx tmp+3
        lda e_xl,x
        clc
        adc #4
        sta tx
        lda e_xh,x
        adc #0
        sta tx+1
        lda e_y,x
        sec
        sbc #3
        sta ty
        jsr tile_at
        ldx tmp+3
        cmp haz_t
        bcc @n
        cmp plat_t
        bcs @n
        sec
        rts
@n:     clc
        rts

; impulso de salto que no cruce la línea de franjas (fila 8): A = vy negativo o 0
jump_v:
        lda e_y,x
        sec
        sbc #80
        bcc @z
        cmp #44
        bcs @a
        cmp #24
        bcs @b
        cmp #12
        bcs @c
@z:     lda #0
        rts
@a:     lda #$C0
        rts
@b:     lda #$D0
        rts
@c:     lda #$DC
        rts

; ¿hay suelo en x = e_x + 4 + A (con signo), a la altura de los pies? C=1 sí
en_floor_at:
        stx tmp+3
        clc
        adc #4
        pha
        clc
        adc e_xl,x
        sta tx
        pla
        bmi @n
        lda e_xh,x
        adc #0
        jmp @s
@n:     lda e_xh,x
        adc #$FF
@s:     sta tx+1
        lda e_y,x
        sta ty
        jsr tile_at
        ldx tmp+3
        cmp plat_t
        rts
; andar por el suelo: no atraviesa paredes ni se tira a los fosos
; C=1 si no avanza; mvres = 1 pared, 2 borde
move_xg:
        jsr en_wall
        bcc @nw
        lda #1
        sta mvres
        rts
@nw:    lda e_vx,x
        bmi @l
        lda #5
        bne @t
@l:     lda #$F9
@t:     jsr en_floor_at
        bcs @ok
        lda #2
        sta mvres
        sec
        rts
@ok:    jsr move_x
        lda #0
        sta mvres
        clc
        rts
; salto: si no hay suelo donde caer, da media vuelta
jump_target_ok:
        inc e_y,x               ; ya se despegó un píxel: mirar a la altura de los pies
        lda e_vx,x
        beq @y
        bmi @l
        lda #28
        bne @t
@l:     lda #$E4
@t:     jsr en_floor_at
        bcs @y
        jsr turn_back
@y:     dec e_y,x
        rts
; media vuelta
turn_back:
        lda e_dir,x
        eor #1
        sta e_dir,x
        lda e_vx,x
        eor #$FF
        clc
        adc #1
        sta e_vx,x
        rts

; movimiento con pared: si choca no avanza (C=1)
move_xw:
        jsr en_wall
        bcs @w
        jsr move_x
        clc
@w:     rts

; mueve e_x según e_vx (con signo)
move_x: lda e_vx,x
        clc
        adc e_xl,x
        sta e_xl,x
        lda e_vx,x
        bmi @n
        lda e_xh,x
        adc #0
        sta e_xh,x
        rts
@n:     lda e_xh,x
        adc #$FF
        sta e_xh,x
        rts

; gravedad + suelo para enemigos terrestres (C=1 si en el suelo)
en_gravity:
        stx tmp+3
        lda e_xl,x
        clc
        adc #4
        sta tx
        lda e_xh,x
        adc #0
        sta tx+1
        lda e_vy,x
        bmi @air
        lda e_y,x
        sta ty
        jsr tile_at
        ldx tmp+3
        cmp plat_t
        bcc @air
        lda #0
        sta e_vy,x
        lda e_y,x
        and #$F8
        sta e_y,x
        sec
        rts
@air:   ldx tmp+3
        lda e_vy,x
        bmi @g
        cmp #48
        bcs @ng
@g:     clc
        adc #3
        sta e_vy,x
@ng:    lda e_vy,x
        asl
        asl
        asl
        asl
        clc
        adc e_ysub,x
        sta e_ysub,x
        lda e_vy,x
        php
        lsr
        lsr
        lsr
        lsr
        plp
        bpl @p
        ora #$F0
@p:     adc e_y,x
        sta e_y,x
        clc
        rts

en_soldier:
        jsr en_gravity
        bcc @x
        inc e_t,x
        lda e_t,x
        and #$7F
        cmp #90
        bcs @stop
        ; anda en su dirección (sin girarse a cada paso)
        lda frame
        and #1
        beq @anim
        lda #$FF
        ldy e_dir,x
        bne @l
        lda #1
@l:     sta e_vx,x
        jsr move_xg
        bcc @anim
        lda e_dir,x
        eor #1
        sta e_dir,x
@anim:  lda e_t,x
        lsr
        lsr
        lsr
        and #1
        clc
        adc #EF_SOLDIER1
        sta e_fr,x
@x:     rts
@stop:  lda #EF_SOLDIER1
        sta e_fr,x
        lda e_t,x
        and #$7F
        cmp #105
        bne @nf
        jsr face_player
        lda e_y,x
        sec
        sbc #10
        jsr enemy_fire_h
@nf:    lda e_t,x
        and #$7F
        cmp #120
        bcc @x
        lda e_t,x
        and #$80
        sta e_t,x
        rts

en_drone:
        inc e_t,x
        lda #$FF
        sta e_vx,x
        jsr move_x
        lda e_t,x
        lsr
        and #31
        tay
        lda sine,y
        clc
        adc e_base,x
        sta e_y,x
        lda e_t,x
        lsr
        lsr
        and #1
        clc
        adc #EF_DRONE1
        sta e_fr,x
        lda e_t,x
        cmp #70
        bne @x
        lda e_y,x
        sec
        sbc #6
        jsr enemy_fire_aim
@x:     rts

en_dog: jsr en_gravity
        bcc @x
        lda #$FE
        ldy e_dir,x
        bne @l
        lda #2
@l:     sta e_vx,x
        jsr move_xg
        bcc @dm
        lda mvres
        cmp #1
        bne @tb
        jsr jump_v
        beq @tb
        sta e_vy,x
        dec e_y,x
        jmp @dm
@tb:    lda e_dir,x
        eor #1
        sta e_dir,x
@dm:    inc e_t,x
        lda e_t,x
        lsr
        lsr
        and #1
        clc
        adc #EF_DOG1
        sta e_fr,x
@x:     rts

en_jumper:
        jsr en_gravity
        bcs @g
        lda #EF_JUMPER2
        sta e_fr,x
        jmp move_xw
@g:     lda #EF_JUMPER1
        sta e_fr,x
        lda #0
        sta e_vx,x
        dec e_t,x
        bne @x
        lda #50
        sta e_t,x
        jsr jump_v
        beq @x
        sta e_vy,x
        dec e_y,x
        lda #$FF
        ldy e_dir,x
        bne @l
        lda #1
@l:     sta e_vx,x
        jsr jump_target_ok
@x:     rts

en_bug: jsr en_gravity
        bcs @g
        lda #EF_BUG2
        sta e_fr,x
        lda frame
        and #1
        beq @x
        jsr move_xw
@x:     rts
@g:     lda #EF_BUG1
        sta e_fr,x
        dec e_t,x
        bne @x
        lda #36
        sta e_t,x
        jsr jump_v
        beq @x
        cmp #$D0
        bcs @bj
        lda #$D0
@bj:    sta e_vy,x
        dec e_y,x
        lda #$FF
        ldy e_dir,x
        bne @l
        lda #1
@l:     sta e_vx,x
        jmp jump_target_ok

en_fish:
        inc e_t,x
        lda e_t,x
        lsr
        lsr
        and #31
        tay
        lda sine,y
        cmp #$80
        ror
        cmp #$80
        ror
        clc
        adc e_base,x
        sta e_y,x
        ldy e_type,x
        lda en_f0,y
        sta e_fr,x
        rts

sine:   .byte 0,2,4,6,8,9,10,11,12,11,10,9,8,6,4,2
        .byte 0,$FE,$FC,$FA,$F8,$F7,$F6,$F5,$F4,$F5,$F6,$F7,$F8,$FA,$FC,$FE

; ---- balas enemigas. A = y; x origen = enemigo X
enemy_fire_h:
        sta tmp+2
        lda e_xl,x
        sta tmp
        lda e_xh,x
        sta tmp+1
        lda e_dir,x
        tay
        lda #2
        cpy #0
        beq @r
        lda #$FE
@r:     ldy #0
        jmp new_ebullet
enemy_fire_aim:
        sta tmp+2
        lda e_xl,x
        clc
        adc #3
        sta tmp
        lda e_xh,x
        adc #0
        sta tmp+1
        jmp aim_bullet

; tmp/tmp+1 = x, tmp+2 = y: dispara hacia Zak con 1 de 5 pendientes
aim_bullet:
        stx tmp+3
        ; dx = (px+4) - x
        lda px
        clc
        adc #4
        sec
        sbc tmp
        sta ptr2
        lda px+1
        adc #0
        sbc tmp+1
        sta ptr2+1               ; signo en el byte alto
        ; |dx| limitado a 255
        bpl @dxp
        lda #0
        sec
        sbc ptr2
        sta ptr2
        lda #0
        sbc ptr2+1
        beq @dxok
        lda #255
        sta ptr2
        lda #$FF
        sta ptr2+1
        bne @dy
@dxok:  lda #$FF
        sta ptr2+1
        bne @dy
@dxp:   beq @dy
        lda #255
        sta ptr2
        lda #0
        sta ptr2+1
@dy:    ; dy = (py-10) - y
        lda py
        sec
        sbc #10
        sec
        sbc tmp+2
        sta ptr3                 ; con signo
        bcs @dyp
        eor #$FF
        adc #1
        sta ptr3+1               ; |dy|
        lda #$FF
        bne @dys
@dyp:   sta ptr3+1
        lda #0
@dys:   sta vtmp+1               ; signo dy (FF neg)
        ; pendiente: compara |dy|*4 con |dx|...
        lda ptr3+1
        lsr
        lsr
        cmp ptr2                 ; |dy|/4 >= |dx| -> vertical
        bcs @vert
        lda ptr2
        lsr
        lsr
        cmp ptr3+1               ; |dx|/4 >= |dy| -> horizontal
        bcs @horz
        lda ptr2
        lsr
        cmp ptr3+1
        bcs @shal                ; |dx|/2 >= |dy|
        lda ptr3+1
        lsr
        cmp ptr2
        bcs @steep
        lda #2
        ldy #2
        bne @set
@shal:  lda #2
        ldy #1
        bne @set
@steep: lda #1
        ldy #2
        bne @set
@vert:  lda #0
        ldy #2
        bne @set
@horz:  lda #2
        ldy #0
@set:   ; aplicar signos
        bit ptr2+1
        bpl @sx
        eor #$FF
        clc
        adc #1
@sx:    sta vtmp
        tya
        bit vtmp+1
        bpl @sy
        eor #$FF
        clc
        adc #1
@sy:    tay
        lda vtmp
        ldx tmp+3
; A = vx, Y = vy, tmp/tmp+1 = x, tmp+2 = y
new_ebullet:
        sta vtmp
        stx tmp+3
        lda diff
        cmp #2
        bne @nh
        ; difícil: balas más rápidas
        lda vtmp
        clc
        adc #2
        tax
        lda hardv,x
        sta vtmp
        tya
        clc
        adc #2
        tax
        ldy hardv,x
@nh:    ldx #2
        lda b_on+2
        beq @f
        lda diff
        beq @full               ; fácil: una sola bala enemiga a la vez
        inx
        lda b_on+3
        beq @f
@full:  ldx tmp+3
        rts
@f:     lda #1
        sta b_on,x
        lda vtmp
        sta b_vx,x
        tya
        sta b_vy,x
        lda tmp
        sta b_xl,x
        lda tmp+1
        sta b_xh,x
        lda tmp+2
        sta b_y,x
        lda #6
        jsr play_sfx
        ldx tmp+3
        rts

; =====================================================================
;  TORRETAS
; =====================================================================
turrets_update:
        ldx #NT-1
@l:     lda t_on,x
        beq @n
        ; ¿salió por la izquierda?
        lda t_cl,x
        clc
        adc #3
        sta tmp
        lda t_ch,x
        adc #0
        cmp coarse+1
        bcc @off
        bne @in
        lda tmp
        cmp coarse
        bcs @in
@off:   lda #0
        sta t_on,x
        beq @n
@in:    lda t_hp,x
        beq @n
        dec t_t,x
        bne @n
        jsr rand
        and #63
        ldy diff
        adc turret_base,y
        sta t_t,x
        ; disparo desde el cañón (col*4, fila*8+2)
        lda t_cl,x
        sta tmp
        lda t_ch,x
        asl tmp
        rol
        asl tmp
        rol
        sta tmp+1
        lda t_row,x
        asl
        asl
        asl
        adc #2
        sta tmp+2
        stx t_save
        jsr aim_bullet
        ldx t_save
@n:     dex
        bpl @l
        rts

; destruye la torreta X: dibuja los caracteres de "torreta rota"
turret_destroy:
        stx ptr3
        lda #0
        sta t_hp,x
        lda #3
        jsr play_sfx
        lda #$05
        jsr add_score
        ldx phase
        lda ph_turretxlo,x
        sta ptr2
        lda ph_turretxhi,x
        sta ptr2+1
        ldx ptr3
        lda t_cl,x
        sta tx
        lda t_ch,x
        sta tx+1
        lda #0
        sta tmp+1               ; índice en la tabla 2x2
@c:     ldx ptr3
        lda tmp+1
        and #1
        clc
        adc t_cl,x
        sta tx
        lda tmp+1
        lsr
        clc
        adc t_row,x
        tay
        sty tmp+2
        ldy tmp+1
        lda (ptr2),y
        ldy tmp+2
        jsr putchar
        inc tmp+1
        lda tmp+1
        cmp #4
        bne @c
        ldx ptr3
        rts

; =====================================================================
;  BALAS
; =====================================================================
bullets_update:
        ldx #NB-1
@l:     lda b_on,x
        beq @n
        ; x += vx
        lda b_vx,x
        clc
        adc b_xl,x
        sta b_xl,x
        lda b_vx,x
        bmi @neg
        lda b_xh,x
        adc #0
        jmp @s
@neg:   lda b_xh,x
        adc #$FF
@s:     sta b_xh,x
        lda b_y,x
        clc
        adc b_vy,x
        sta b_y,x
        cmp #176
        bcs @kill
        cmp #2
        bcc @kill
        ; ¿en pantalla?
        lda b_xl,x
        sec
        sbc camx
        sta tmp
        lda b_xh,x
        sbc camx+1
        bne @kill
        lda tmp
        cmp #VIS0+160
        bcs @kill
        cmp #VIS0-4
        bcc @kill
        ; ¿choca con sólido?
        lda b_xl,x
        sta tx
        lda b_xh,x
        sta tx+1
        lda b_y,x
        sta ty
        stx tmp+3
        jsr tile_at
        ldx tmp+3
        bcc @n
@kill:  lda #0
        sta b_on,x
@n:     dex
        bpl @l
        rts

; =====================================================================
;  COLISIONES
; =====================================================================
collide:
        ; balas de Zak contra enemigos, torretas y jefe
        ldx #1
@b:     lda b_on,x
        bne @b1
        jmp @bn
@b1:    ; enemigos
        ldy #NE-1
@e:     lda e_type,y
        beq @en
        cmp #6
        bcs @en                 ; recogibles no
        lda e_st,y
        bmi @en
        ; dx = bx - ex en [0,8)
        lda b_xl,x
        sec
        sbc e_xl,y
        sta tmp
        lda b_xh,x
        sbc e_xh,y
        bne @en
        lda tmp
        cmp #8
        bcs @en
        ; dy = by - (ey-15) en [0,15)
        lda e_y,y
        sec
        sbc #15
        sta tmp
        lda b_y,x
        sec
        sbc tmp
        cmp #16
        bcs @en
        ; impacto
        lda #0
        sta b_on,x
        lda e_hp,y
        sec
        sbc #1
        sta e_hp,y
        bne @hit
        lda #$80
        sta e_st,y
        lda #24
        sta e_t,y
        stx tmp+3
        sty tmp+2
        ldx e_type,y
        lda en_pts,x
        jsr add_score
        lda #3
        jsr play_sfx
        ldy tmp+2
        ldx tmp+3
        jmp @bn
@hit:   lda #6
        stx tmp+3
        jsr play_sfx
        ldx tmp+3
        jmp @bn
@en:    dey
        bpl @e
        ; torretas
        ldy #NT-1
@t:     lda t_on,y
        beq @tn
        lda t_hp,y
        beq @tn
        lda t_cl,y
        sta tmp
        lda t_ch,y
        asl tmp
        rol
        asl tmp
        rol
        sta tmp+1
        lda b_xl,x
        sec
        sbc tmp
        sta tmp
        lda b_xh,x
        sbc tmp+1
        bne @tn
        lda tmp
        cmp #8
        bcs @tn
        lda t_row,y
        asl
        asl
        asl
        sta tmp
        lda b_y,x
        sec
        sbc tmp
        cmp #16
        bcs @tn
        lda #0
        sta b_on,x
        lda t_hp,y
        sec
        sbc #1
        sta t_hp,y
        bne @th
        stx tmp+3
        tya
        tax
        jsr turret_destroy
        ldx tmp+3
        jmp @bn
@th:    stx tmp+3
        lda #6
        jsr play_sfx
        ldx tmp+3
        jmp @bn
@tn:    dey
        bpl @t
        ; jefe
        lda boss_on
        beq @bn
        stx tmp+3
        jsr boss_hit_test
        ldx tmp+3
@bn:    dex
        bmi @zak
        jmp @b
@zak:   ; Zak contra enemigos y balas enemigas
        lda pstate
        beq @zk
        rts
@zk:
        lda py
        sec
        sbc #18
        ldy crouch
        beq @c0
        clc
        adc #9
@c0:    sta tmp+1               ; y superior de Zak
        ldx #3
@eb:    cpx #2
        bcc @ebn
        lda b_on,x
        beq @ebn
        lda b_xl,x
        sec
        sbc px
        sta tmp
        lda b_xh,x
        sbc px+1
        bne @ebn
        lda tmp
        sec
        sbc #1
        cmp #6
        bcs @ebn
        lda b_y,x
        cmp tmp+1
        bcc @ebn
        cmp py
        bcs @ebn
        lda #0
        sta b_on,x
        jsr hurt_player
@ebn:   dex
        cpx #2
        bcs @eb
        ; cuerpos
        ldx #NE-1
@ec:    lda e_type,x
        beq @ecn
        lda e_st,x
        bmi @ecn
        lda e_xl,x
        sec
        sbc px
        sta tmp
        lda e_xh,x
        sbc px+1
        sta tmp+2
        lda tmp
        clc
        adc #6
        sta tmp
        lda tmp+2
        adc #0
        bne @ecn
        lda tmp
        cmp #12
        bcs @ecn
        ; vertical: [ey-14, ey) contra [top, py)
        lda e_y,x
        sec
        sbc #2
        cmp tmp+1
        bcc @ecn
        lda e_y,x
        sec
        sbc #14
        cmp py
        bcs @ecn
        lda e_type,x
        cmp #6
        bcc @hurt
        cmp #8
        bcc @pick
@hurt:  jsr hurt_player
        jmp @ecn
@pick:  cmp #6
        bne @can
        lda hp_max
        sta hp
        bne @pk
@can:   inc lives
@pk:    lda #0
        sta e_type,x
        lda #1
        sta hudflag
        lda #$10
        jsr add_score
        lda #5
        jsr play_sfx
@ecn:   dex
        bpl @ec
        ; jefe-sprites
        lda boss_on
        beq @x
        jsr boss_touch
@x:     rts

; =====================================================================
;  DIBUJO DE SPRITES (PMG)
; =====================================================================
draw_sprites:
        ; --- Zak
        lda oldpy
        clc
        adc #PFTOP-20
        tay
        ldx #20
        lda #0
@cz:    sta PL0,y
        sta PL1,y
        iny
        dex
        bne @cz
        lda py
        sta oldpy
        ; ¿visible? (parpadeo de invulnerable)
        lda inv
        and #4
        bne @hidez
        lda py
        cmp #200
        bcs @hidez
        ldy pframe
        lda mul20,y
        sta tmp
        ldy pdir
        lda zak_a_lo,y
        clc
        adc tmp
        sta ptr
        lda zak_a_hi,y
        adc #0
        sta ptr+1
        lda zak_b_lo,y
        clc
        adc tmp
        sta ptr2
        lda zak_b_hi,y
        adc #0
        sta ptr2+1
        lda py
        clc
        adc #PFTOP-20
        sta tmp
        lda #<PL0
        clc
        adc tmp
        sta ptr3
        lda #>PL0
        sta ptr3+1
        ldy #0
@dz:    lda (ptr),y
        sta (ptr3),y
        inc ptr3+1
        lda (ptr2),y
        sta (ptr3),y
        dec ptr3+1
        iny
        cpy #20
        bne @dz
@hidez: lda px
        sec
        sbc camx
        clc
        adc #HPOFS
        sta hpos
        sta hpos+1
        ; --- enemigos
        lda boomon
        beq @nbo
        jsr draw_booms
        jmp @nb
@nbo:   lda boss_on
        beq @de
        lda bkind
        cmp #4
        bne @de
        lda bossst
        cmp #1
        beq @nde
@de:    ldx #0
        jsr draw_enemy
        ldx #1
        jsr draw_enemy
        ldx #2
        jsr draw_enemy
        ldx #3
        jsr draw_enemy
        lda ehpos
        sta hpos+2
        lda ehpos+1
        sta hpos+3
        lda ehpos+2
        sta hposb
        lda ehpos+3
        sta hposb+1
        lda ecol
        sta PCOLR2
        lda ecol+1
        sta PCOLR3
@nde:   ; --- jefe sprite (si aplica)
        lda boss_on
        beq @nb
        jsr boss_draw_sprites
        lda hpos+2
        sta hposb
        lda hpos+3
        sta hposb+1
        lda PCOLR2
        sta ecol+2
        lda PCOLR3
        sta ecol+3
@nb:    ; --- misiles
        jsr draw_missiles
        ; posiciones directas al hardware (aún estamos por encima del campo de juego)
        ldx #7
@hw:    lda hpos,x
        sta HPOSP0,x
        dex
        bpl @hw
        rts

mul20:  .byte 0,20,40,60,80,100,120,140,160
zak_a_lo:.byte <zak_a0,<zak_a1
zak_a_hi:.byte >zak_a0,>zak_a1
zak_b_lo:.byte <zak_b0,<zak_b1
zak_b_hi:.byte >zak_b0,>zak_b1

; X = hueco (0 -> P2, 1 -> P3)
draw_enemy:
        txa
        and #1
        tay
        lda pl_hi,y
        sta ptr3+1
        lda e_oy,x
        sta ptr3
        ldy #15
        lda #0
@c:     sta (ptr3),y
        dey
        bpl @c
        lda e_type,x
        bne @v
        lda #0
        sta ehpos,x
        lda #$3C
        sta ecol,x
        rts
@v:     ; color según el tipo
        lda e_type,x
        tay
        lda en_col,y
        sta ecol,x
        lda e_y,x
        clc
        adc #PFTOP-16
        sta e_oy,x
        sta ptr3
        lda e_xl,x
        sec
        sbc camx
        sta tmp
        lda e_xh,x
        sbc camx+1
        beq @on
        cmp #$FF
        bne @off
        lda tmp
        cmp #$F8
        bcs @on2
@off:   lda #0
        sta ehpos,x
        rts
@on:    lda tmp
        cmp #VIS0+164
        bcs @off
@on2:   lda tmp
        clc
        adc #HPOFS
        sta ehpos,x
        ; gráfico
        lda e_fr,x
        asl
        asl
        asl
        asl
        sta tmp
        lda e_dir,x
        tay
        lda en_lo,y
        clc
        adc tmp
        sta ptr
        lda en_hi,y
        adc #0
        sta ptr+1
        ldy #15
@d:     lda (ptr),y
        sta (ptr3),y
        dey
        bpl @d
        rts
pl_hi:  .byte >PL2,>PL3
en_lo:  .byte <en_gfx1,<en_gfx0
en_hi:  .byte >en_gfx1,>en_gfx0

mmask:  .byte $FC,$F3,$CF,$3F
mbits:  .byte $03,$0C,$30,$C0
draw_missiles:
        ldx #NB-1
@l:     ; borrar
        ldy b_oy,x
        lda mlen,x
        sta tmp
@c:     lda MIS,y
        and mmask,x
        sta MIS,y
        iny
        dec tmp
        bne @c
        lda b_on,x
        beq @off
        lda b_y,x
        clc
        adc #PFTOP
        sta b_oy,x
        tay
        lda mlen,x
        sta tmp
@d:     lda MIS,y
        ora mbits,x
        sta MIS,y
        iny
        dec tmp
        bne @d
        lda b_xl,x
        sec
        sbc camx
        clc
        adc #HPOFS
        sta hpos+4,x
        jmp @n
@off:   lda #0
        sta hpos+4,x
@n:     dex
        bpl @l
        rts
mlen:   .byte 2,2,4,4

        .include "boss.s"
        .include "screens.s"

; ---------------------------------------------------------------------
; tablas
rowlo:
        .repeat NROWS, I
        .byte <(SCR+I*128)
        .endrepeat
rowhi:
        .repeat NROWS, I
        .byte >(SCR+I*128)
        .endrepeat
mul22:
        .repeat 16, I
        .byte <(I*22)
        .endrepeat
mul22h:
        .repeat 16, I
        .byte >(I*22)
        .endrepeat
song_tab:
        .word s_p1,s_p2,s_p3,s_p4,s_p5,s_boss,s_clear,s_over
s_p1:   .word song_p1_m, song_p1_b, song_p1_d
s_p2:   .word song_p2_m, song_p2_b, song_p2_d
s_p3:   .word song_p3_m, song_p3_b, song_p3_d
s_p4:   .word song_p4_m, song_p4_b, song_p4_d
s_p5:   .word song_p5_m, song_p5_b, song_p5_d
s_boss: .word song_boss_m, song_boss_b, song_boss_d
s_clear:.word song_clear_m, song_clear_b, song_clear_d
s_over: .word song_over_m, song_over_b, song_over_d
